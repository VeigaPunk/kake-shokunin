#!/usr/bin/env python3
"""Adversarial fence/path battery for the kake lane `scripts/id_resolver.py` (round-58 C2).

Independent of the fix author: this file states, per case, the behaviour ANY correct
fence-aware registry parser (and any correct git-quoted path reader) must show.

    python3 -B battery.py <path to id_resolver.py>
    python3 -B battery.py <path to id_resolver.py> --keep     # keep fixtures for inspection

Each case builds a throwaway fixture lane `demo-shokunin` (registry + knowledge files)
under /fast/scratch/hyaku/kake-r58/ExecResolverTests/cases/<case>/ and runs the tool as
`python3 -B <tool> --root <lane> --fleet <case dir> [--revision HEAD]`. A case passes iff
the set of `DANGLING <id>` ids on stdout and the exit code both match the expectation.

Fence semantics are CommonMark's (spec 4.5/4.6):
  - a closed fence needs the same character and at least as many of it (```` closed by ``` stays open);
  - a fence opent by ` is closed only by ` (and ~~~ only by ~~~);
  - a fence may be indented 0-3 spaces; a 4-space line is an indented code block, never a fence;
  - an opening fence may carry an info string; the closing fence may not;
  - an unclosed fence runs to the end of the document;
  - a fenced `## Registry` is code, so it neither opens nor ends the registry section;
  - an indented code block does not open a section either, so a heading after it is real.

Exit: 0 all cases pass; 1 at least one case fails; 2 the tool path is missing.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r58/ExecResolverTests"
LANE = "demo-shokunin"
GIT = "git"

HEAD = "# SOURCES\n## Registry\n"
SEP = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)
PATHS = "## Paths\n\n- none\n"

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV["GIT_CONFIG_GLOBAL"] = os.devnull
ENV["GIT_CONFIG_SYSTEM"] = os.devnull
ENV["GIT_TERMINAL_PROMPT"] = "0"


def row(sid):
    return (
        f"| {sid} | https://example.test/{sid}/ | docs | A | scope | anchor | teaches "
        f"| mined | 2026-10-25 | 90d | — |\n"
    )


def reg(lane):
    return os.path.join(lane, "corpus", "SOURCES.md")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def cite(lane, rel, ids):
    write(os.path.join(lane, "corpus", "knowledge", rel), "# Notes\n\nSee " + " and ".join(ids) + ".\n")


def git(lane, *args):
    proc = subprocess.run([GIT, "-C", lane, *args], capture_output=True, text=True, env=ENV)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {lane}: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def make_repo(lane):
    """Init a fixture repo and assert its toplevel is exactly this fixture dir before any commit."""
    git(lane, "init", "-q")
    top = git(lane, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(lane):
        raise RuntimeError(f"fixture toplevel {top!r} != {lane!r}")
    git(lane, "add", "-A")
    git(lane, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
        "-c", "commit.gpgsign=false", "commit", "-q", "-m", "fixture")


def fixture(name):
    base = os.path.join(SCRATCH, "cases", name)
    shutil.rmtree(base, ignore_errors=True)
    lane = os.path.join(base, LANE)
    os.makedirs(os.path.join(lane, "corpus", "knowledge"), exist_ok=True)
    return base, lane


def run_tool(tool, lane, base):
    argv = [sys.executable, "-B", tool, "--root", lane, "--fleet", base, *EXTRA]
    return subprocess.run(argv, capture_output=True, text=True, env=ENV, timeout=180)


def dangling_ids(proc):
    out = set()
    for line in proc.stdout.splitlines():
        if line.startswith("DANGLING "):
            out.add(line.split()[1])
    return out


def summary_line(proc):
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith("ids_cited="):
            return line.strip()
    return "-"


# --------------------------------------------------------------------------- fixture builders
# Each builder writes one case; it returns the extra argv (--revision HEAD for repo cases).

def b_control(base, lane):
    write(reg(lane), HEAD + SEP + row("S001") + PATHS)
    cite(lane, "notes.md", ["S001"])
    return []


def b_four_backtick(base, lane):
    # a 4-backtick fence is not closed by 3 backticks: everything after stays code (to EOF here)
    write(reg(lane), HEAD + SEP + row("S101") + PATHS + "\n"
          "````\n"
          "## Registry\n" + row("S901") +
          "```\n"
          "## Registry\n" + row("S902") + "\n")
    cite(lane, "notes.md", ["S101", "S901", "S902"])
    return []


def b_tilde_fence(base, lane):
    # a ~~~ fence is not closed by ```; the trailing ~~~ does close it
    write(reg(lane), HEAD + SEP + row("S102") + PATHS + "\n"
          "~~~\n"
          "## Registry\n" + row("S903") +
          "```\n"
          "## Registry\n" + row("S904") +
          "~~~\n")
    cite(lane, "notes.md", ["S102", "S903", "S904"])
    return []


def b_fence_indented_four(base, lane):
    # a 4-space ``` is an indented code block, not a fence: the heading after it is real
    write(reg(lane), HEAD + SEP + row("S103") + PATHS + "\n"
          "    ```\n"
          "## Registry\n" + row("S905") + "\n")
    cite(lane, "notes.md", ["S103", "S905"])
    return []


def b_fence_info_string(base, lane):
    write(reg(lane), HEAD + SEP + row("S104") + PATHS + "\n"
          "```markdown\n"
          "## Registry\n" + row("S906") +
          "```\n"
          "## Registry\n" + row("S907") + "\n")
    cite(lane, "notes.md", ["S104", "S906", "S907"])
    return []


def b_fence_unclosed_to_eof(base, lane):
    write(reg(lane), HEAD + SEP + row("S105") + PATHS + "\n"
          "```text\n"
          "## Registry\n" + row("S908") + row("S909") + "\n")
    cite(lane, "notes.md", ["S105", "S908", "S909"])
    return []


def b_heading_after_fenced_heading(base, lane):
    write(reg(lane), HEAD + SEP + row("S106") + PATHS + "\n"
          "```text\n"
          "## Registry\n" + row("S910") +
          "```\n"
          "## Registry\n" + row("S911") + "\n")
    cite(lane, "notes.md", ["S106", "S910", "S911"])
    return []


def b_three_space_row_after_fence(base, lane):
    # both rows are inside the real Registry section; the first is fenced (code), the second is a row
    write(reg(lane), HEAD + SEP + row("S107") +
          "```text\n"
          "   " + row("S912") +
          "```\n"
          "   " + row("S913"))
    cite(lane, "notes.md", ["S107", "S912", "S913"])
    return []


def b_crlf_around_fence(base, lane):
    body = (HEAD + SEP + row("S108") + PATHS + "\n"
            "```text\n"
            "## Registry\n" + row("S914") +
            "```\n"
            "## Registry\n" + row("S915") + "\n")
    write(reg(lane), body.replace("\n", "\r\n"))
    cite(lane, "notes.md", ["S108", "S914", "S915"])
    return []


def b_revision_tab_name(base, lane):
    write(reg(lane), HEAD + SEP + row("S020") + PATHS)
    write(os.path.join(lane, "corpus", "knowledge", "has\ttab.md"), "# Notes\n\nSee S917.\n")
    cite(lane, "ok.md", ["S020"])
    make_repo(lane)
    return ["--revision", "HEAD"]


def b_revision_newline_name(base, lane):
    write(reg(lane), HEAD + SEP + row("S021") + PATHS)
    write(os.path.join(lane, "corpus", "knowledge", "new\nline.md"), "# Notes\n\nSee S918.\n")
    cite(lane, "ok.md", ["S021"])
    make_repo(lane)
    return ["--revision", "HEAD"]


def b_revision_backslash_name(base, lane):
    write(reg(lane), HEAD + SEP + row("S022") + PATHS)
    write(os.path.join(lane, "corpus", "knowledge", "back\\slash.md"), "# Notes\n\nSee S919.\n")
    cite(lane, "ok.md", ["S022"])
    make_repo(lane)
    return ["--revision", "HEAD"]


def b_revision_non_ascii_dir(base, lane):
    write(reg(lane), HEAD + SEP + row("S023") + PATHS)
    write(os.path.join(lane, "corpus", "knowledge", "日本語", "notes.md"), "# Notes\n\nSee S920.\n")
    cite(lane, "ok.md", ["S023"])
    make_repo(lane)
    return ["--revision", "HEAD"]


CASES = [
    ("00-control-plain-registry", b_control, set(), 0),
    ("01-four-backtick-not-closed-by-three", b_four_backtick, {"S901", "S902"}, 1),
    ("02-tilde-fence-not-closed-by-backticks", b_tilde_fence, {"S903", "S904"}, 1),
    ("03-four-space-fence-line-is-code", b_fence_indented_four, set(), 0),
    ("04-fence-with-info-string", b_fence_info_string, {"S906"}, 1),
    ("05-unclosed-fence-to-eof", b_fence_unclosed_to_eof, {"S908", "S909"}, 1),
    ("06-heading-after-fenced-heading", b_heading_after_fenced_heading, {"S910"}, 1),
    ("07-three-space-row-after-fence", b_three_space_row_after_fence, {"S912"}, 1),
    ("08-crlf-around-fence", b_crlf_around_fence, {"S914"}, 1),
    ("09-revision-tab-in-name", b_revision_tab_name, {"S917"}, 1),
    ("10-revision-newline-in-name", b_revision_newline_name, {"S918"}, 1),
    ("11-revision-backslash-in-name", b_revision_backslash_name, {"S919"}, 1),
    ("12-revision-non-ascii-subdir", b_revision_non_ascii_dir, {"S920"}, 1),
]

EXTRA = []


def verdict(proc, want_dangling, want_exit):
    got = dangling_ids(proc)
    problems = []
    if got != want_dangling:
        problems.append("dangling={" + ",".join(sorted(got)) + "} want {" + ",".join(sorted(want_dangling)) + "}")
    if proc.returncode != want_exit:
        problems.append(f"exit={proc.returncode} want {want_exit}")
    if proc.returncode in (2, 64):
        lines = proc.stderr.strip().splitlines() or proc.stdout.strip().splitlines() or ["<no output>"]
        problems.append("tool said: " + lines[-1][:200])
    detail = "; ".join(problems) if problems else "as expected"
    observed = f"exit={proc.returncode} dangling={len(got)} [{summary_line(proc)}]"
    return (not problems), detail + " | " + observed


def main(argv):
    keep = "--keep" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print("usage: battery.py <path to id_resolver.py> [--keep]", file=sys.stderr)
        return 2
    tool = os.path.abspath(args[0])
    if not os.path.isfile(tool):
        print(f"battery: tool not found: {tool}", file=sys.stderr)
        return 2
    os.makedirs(SCRATCH, exist_ok=True)
    print(f"battery: tool={tool}")
    print(f"battery: fixtures={os.path.join(SCRATCH, 'cases')}")
    passed = 0
    for index, (name, build, want_dangling, want_exit) in enumerate(CASES, 0):
        global EXTRA
        base, lane = fixture(name)
        try:
            EXTRA = build(base, lane) or []
            proc = run_tool(tool, lane, base)
        except Exception as exc:  # noqa: BLE001 - a broken fixture is a reported failure
            print(f"FAIL {index:02d} {name}: fixture error: {type(exc).__name__}: {exc}")
            continue
        ok, detail = verdict(proc, want_dangling, want_exit)
        print(f"{'PASS' if ok else 'FAIL'} {index:02d} {name}: {detail}")
        passed += ok
    total = len(CASES)
    print(f"battery: {passed}/{total} cases passed")
    if not keep:
        shutil.rmtree(os.path.join(SCRATCH, "cases"), ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
