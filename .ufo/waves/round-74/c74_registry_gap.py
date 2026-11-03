#!/usr/bin/env python3
"""Round-74 C1 registry-gap counter (kake). Frozen before data; any change is a new file.

Predicate (contract `.ufo/waves/round-74/contract.md` section C1), measured at --revision over
the 8 frozen population counters:
  1. every population counter has at least one SKILL.md gate-registry table row whose cells
     contain its exact filename. A table row is a line starting with '| ' carrying >= 6 '|'
     characters; a prose mention outside such a row never counts; a row naming the counter in
     any cell counts (first-cell names and alias rows alike).
  2. the counter path each such row names (the first backticked token ending .py in the row,
     repo-relative) resolves at the measured revision: `git -C <root> cat-file -e <rev>:<path>`
     exits 0. A row that names a counter but carries no resolvable path is a finding.
  3. own_row: some table row names c74_registry_gap.py.
met = unregistered == 0 AND no path findings AND own_row, with every population file resolvable
at the revision (a missing or renamed population file is unevaluable, never silently met).

Usage:
  c74_registry_gap.py [--root DIR] [--revision REV] [--json] [--selftest] [--work DIR]

Exit: 0 met · 1 not met · 2 unevaluable · 64 usage. Offline; committed bytes only
(`git show --end-of-options`, `git cat-file -e`). The plain run at base
ced2878a1e77f57afb4ee3baebf1021e5130399b must reproduce
`.ufo/waves/round-74/controls/base-c1-registry.txt` byte-for-byte (unregistered=7, met=false).

--selftest builds the five contract fixtures f1-f5 as throwaway scratch-tree git repos and
prints `selftest K/K` (exit 0 iff every fixture is killed). --work names the scratch directory
for those fixture repos; without it one is created under TMPDIR. Stdlib only; -B friendly.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

VERSION = "C1v1"
SKILL_REL = "SKILL.md"
OWN_COUNTER = "c74_registry_gap.py"

# Frozen population: contract section C1 (rounds 69-73 counters), repo-relative paths.
POPULATION = (
    ("c69_recorded_counts.py", ".ufo/waves/round-69/c69_recorded_counts.py"),
    ("c69_tmp_honour.py", ".ufo/waves/round-69/c69_tmp_honour.py"),
    ("c70_pointer_audit.py", ".ufo/waves/round-70/c70_pointer_audit.py"),
    ("c71_calibration.py", ".ufo/waves/round-71/c71_calibration.py"),
    ("c71_tmp.py", ".ufo/waves/round-71/c71_tmp.py"),
    ("c72_tmp_v2.py", ".ufo/waves/round-72/c72_tmp_v2.py"),
    ("c73_tmp_v3.py", ".ufo/waves/round-73/c73_tmp_v3.py"),
    ("c73_wave_pointers.py", ".ufo/waves/round-73/c73_wave_pointers.py"),
)

BACKTICK_RE = re.compile(r"`([^`]*)`")


def git_run(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def resolve_revision(root, rev):
    proc = git_run(root, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace").strip()


def blob_text(root, rev, path):
    proc = git_run(root, "show", "--end-of-options", rev + ":" + path)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def blob_exit(root, rev, path):
    proc = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", rev + ":" + path], capture_output=True
    )
    return proc.returncode


def is_table_row(line):
    return line.startswith("| ") and line.count("|") >= 6


def iter_table_rows(text):
    """Yield (lineno, line) for rendered table rows, never a row inside a fence."""
    fence = None
    for lineno, line in enumerate(text.split("\n"), 1):
        stripped = line.lstrip()
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if is_table_row(line):
            yield lineno, line


def row_cells(line):
    return [cell.strip() for cell in line.split("|")]


def cell_counter_path(cell):
    """First backticked token ending .py in one cell; None when the cell carries none."""
    for span in BACKTICK_RE.findall(cell):
        for token in span.split():
            if token.endswith(".py"):
                return token
    return None


def credited_cells(cells):
    """Amendment 1 A1: Name, Entry command and Self-test cells only."""
    return [cells[index] for index in (1, 3, 5) if index < len(cells)]


def evaluate(root, rev_arg, population=POPULATION, skill_rel=SKILL_REL):
    result = {
        "version": VERSION,
        "root": root,
        "revision_requested": rev_arg,
        "revision": None,
        "population": len(population),
        "counters": [],
        "unregistered": 0,
        "unregistered_names": [],
        "own_row": False,
        "own_row_lines": [],
        "path_findings": [],
        "unevaluable": [],
        "met": False,
        "exit": 2,
    }
    rev = resolve_revision(root, rev_arg)
    if rev is None:
        result["unevaluable"].append("revision")
        return result
    result["revision"] = rev
    skill = blob_text(root, rev, skill_rel)
    if skill is None:
        result["unevaluable"].append(skill_rel)
        return result

    naming = {name: [] for name, _ in population}
    own_rows = []
    round74_line = None
    for lineno, line in enumerate(skill.split("\n"), 1):
        if line.startswith("### Round 74"):
            round74_line = lineno
            break
    for lineno, line in iter_table_rows(skill):
        cells = row_cells(line)
        credited = credited_cells(cells)
        named = [name for name, _ in population
                 if any(name in cell for cell in credited)]
        if len(named) == 1:  # A2: one counter per row; ambiguous rows credit none
            command = cells[3] if len(cells) > 3 else ""
            naming[named[0]].append((lineno, cell_counter_path(command)))
        if (round74_line is not None and lineno > round74_line
                and any(OWN_COUNTER in cell for cell in credited)):
            own_rows.append(lineno)
    result["own_row"] = bool(own_rows)
    result["own_row_lines"] = own_rows

    for name, path in population:
        file_exit = blob_exit(root, rev, path)
        rows = naming[name]
        row_paths = []
        findings = []
        for lineno, token in rows:
            if token is None:
                findings.append({"line": lineno, "kind": "no_path"})
                row_paths.append({"line": lineno, "path": None, "resolves": False})
                continue
            matches = os.path.basename(token) == name
            resolves = matches and blob_exit(root, rev, token) == 0
            row_paths.append({"line": lineno, "path": token, "resolves": resolves})
            if not matches:
                findings.append({"line": lineno, "kind": "path_not_counter", "path": token})
            elif not resolves:
                findings.append({"line": lineno, "kind": "path_unresolved", "path": token})
        registered = bool(rows)
        if file_exit != 0:
            result["unevaluable"].append(name)
        if not registered:
            result["unregistered_names"].append(name)
        result["path_findings"].extend(dict(counter=name, **finding) for finding in findings)
        result["counters"].append(
            {
                "name": name,
                "path": path,
                "file_exit": file_exit,
                "rows": len(rows),
                "registered": registered,
                "row_paths": row_paths,
                "findings": findings,
            }
        )

    result["unregistered"] = len(result["unregistered_names"])
    result["met"] = bool(
        not result["unevaluable"]
        and result["unregistered"] == 0
        and not result["path_findings"]
        and result["own_row"]
    )
    result["exit"] = 2 if result["unevaluable"] else (0 if result["met"] else 1)
    return result


def render_plain(res):
    rev = res.get("revision") or res["revision_requested"]
    lines = ["%s revision=%s population=%d" % (VERSION, rev, res["population"])]
    for counter in res["counters"]:
        lines.append(
            "%s rows=%d file_exit=%d" % (counter["name"], counter["rows"], counter["file_exit"])
        )
    lines.append(
        "unregistered=%d own_row=%s met=%s" % (
            res["unregistered"], "true" if res["own_row"] else "false",
            "true" if res["met"] else "false")
    )
    if res["unevaluable"]:
        lines.append("unevaluable=" + ",".join(res["unevaluable"]))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- selftest fixtures f1-f5

FX_POPULATION = (
    ("s1_counter.py", ".ufo/waves/rt/s1_counter.py"),
    ("s2_counter.py", ".ufo/waves/rt/s2_counter.py"),
    ("s3_counter.py", ".ufo/waves/rt/s3_counter.py"),
)

FX_COUNTER_FILES = {path: "# fixture counter\n" for _, path in FX_POPULATION}

FX_HEADER = (
    "### Round 74 gate registry additions\n\n"
    "| Name | Kind | Entry command | Verdict map | Self-test | Pinned | Scope | Owner |\n"
    "|---|---|---|---|---|---|---|---|\n"
)

FX_SKILL_F1 = FX_HEADER + (
    "| s1_counter.py | gate | `python3 -B .ufo/waves/rt/s1_counter.py --revision <commit>`"
    " | 0=met; 1=not met; 2=unevaluable; 64=usage | --selftest | f1 | lane | fx |\n"
    "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met; 1=not met | --selftest | f1 | lane | fx |\n"
)

FX_SKILL_F2 = FX_HEADER + (
    "| helper alias | alias row naming s1_counter.py in a non-first cell"
    " | `python3 -B .ufo/waves/rt/s1_counter.py --revision <commit>`"
    " | 0=met | --selftest | f2 | lane | fx |\n"
    "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | f2 | lane | fx |\n"
    "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    " | 0=met | --selftest | f2 | lane | fx |\n"
    "| c74_registry_gap.py | gate"
    " | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --revision <commit>`"
    " | 0=met | --selftest | f2 | lane | fx |\n"
)

FX_SKILL_F3 = (
    "Prose mention only: s1_counter.py appears here, and even as the backticked command"
    " `python3 -B .ufo/waves/rt/s1_counter.py`, but never inside a table row.\n\n"
    + FX_HEADER
    + "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | f3 | lane | fx |\n"
    "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    " | 0=met | --selftest | f3 | lane | fx |\n"
)

FX_SKILL_F4 = FX_HEADER + (
    "| s1_counter.py | gate | `python3 -B .ufo/waves/rt/dead/s1_counter.py --revision <commit>`"
    " | 0=met | --selftest | f4 | lane | fx |\n"
    "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | f4 | lane | fx |\n"
    "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    " | 0=met | --selftest | f4 | lane | fx |\n"
)

FX_SKILL_F5 = FX_HEADER + (
    "| s1_counter.py | gate | `python3 -B .ufo/waves/rt/s1_counter.py --revision <commit>`"
    " | 0=met | --selftest | f5 | lane | fx |\n"
    "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | f5 | lane | fx |\n"
)


def fixture_git(repo, *args):
    env = os.environ.copy()
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, env=env)


def make_fixture(work, label, files):
    """Scratch-tree fixture repo; commits happen only inside it, never elsewhere."""
    repo = tempfile.mkdtemp(prefix="fx-" + label + "-", dir=work)
    for rel, content in sorted(files.items()):
        dest = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as handle:
            handle.write(content)
    if fixture_git(repo, "init", "-q").returncode != 0:
        raise RuntimeError(label + ": git init failed")
    top = fixture_git(repo, "rev-parse", "--show-toplevel")
    if top.returncode != 0 or os.path.realpath(
        top.stdout.decode("utf-8", "replace").strip()
    ) != os.path.realpath(repo):
        raise RuntimeError(label + ": toplevel mismatch, refusing to commit")
    fixture_git(repo, "add", "-A")
    commit = fixture_git(
        repo,
        "-c", "user.name=fixture",
        "-c", "user.email=fixture@example.invalid",
        "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", label,
    )
    if commit.returncode != 0:
        raise RuntimeError(label + ": fixture commit failed")
    head = fixture_git(repo, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise RuntimeError(label + ": rev-parse HEAD failed")
    return repo, head.stdout.decode("utf-8", "replace").strip()


def run_fixture(work, label, files, expect):
    repo, rev = make_fixture(work, label, files)
    try:
        res = evaluate(repo, rev, FX_POPULATION)
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    problems = []
    for name, check in sorted(expect.items()):
        try:
            value = check(res)
        except Exception as exc:  # harness: report any checker error as a fixture failure
            value = "checker-error %r" % (exc,)
        if value is not True:
            problems.append("%s: %r" % (name, value))
    return (not problems), "; ".join(problems) if problems else "ok"


def fx_f1(work):
    """f1: an unregistered population counter is a finding (exit 1, never met)."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F1
    return run_fixture(work, "f1", files, {
        "exit": lambda r: r["exit"] == 1,
        "unregistered": lambda r: r["unregistered_names"] == ["s3_counter.py"],
        "rows_s1_s2": lambda r: [c["rows"] for c in r["counters"]] == [1, 1, 0],
        "no_path_findings": lambda r: not r["path_findings"],
        "not_met": lambda r: r["met"] is False,
        "evaluable": lambda r: not r["unevaluable"],
    })


def fx_f2(work):
    """f2: a row naming a counter in a non-first cell counts as registered (positive control)."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F2
    return run_fixture(work, "f2", files, {
        "exit": lambda r: r["exit"] == 0,
        "registered": lambda r: r["unregistered"] == 0,
        "own_row": lambda r: r["own_row"] is True,
        "met": lambda r: r["met"] is True,
        "no_path_findings": lambda r: not r["path_findings"],
        "evaluable": lambda r: not r["unevaluable"],
    })


def fx_f3(work):
    """f3: a prose-only mention must not count as a registry row."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F3
    return run_fixture(work, "f3", files, {
        "exit": lambda r: r["exit"] == 1,
        "rows_s1_zero": lambda r: r["counters"][0]["rows"] == 0,
        "unregistered": lambda r: r["unregistered_names"] == ["s1_counter.py"],
        "not_met": lambda r: r["met"] is False,
        "evaluable": lambda r: not r["unevaluable"],
    })


def fx_f4(work):
    """f4: a row whose entry-command path does not resolve fails conjunct 2."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F4
    return run_fixture(work, "f4", files, {
        "exit": lambda r: r["exit"] == 1,
        "registered": lambda r: r["unregistered"] == 0,
        "finding": lambda r: any(
            f["counter"] == "s1_counter.py" and f["kind"] == "path_unresolved"
            for f in r["path_findings"]
        ),
        "not_met": lambda r: r["met"] is False,
        "evaluable": lambda r: not r["unevaluable"],
    })


def fx_f5(work):
    """f5: a missing/renamed population counter file is unevaluable, never silently met."""
    files = {
        ".ufo/waves/rt/s1_counter.py": FX_COUNTER_FILES[".ufo/waves/rt/s1_counter.py"],
        ".ufo/waves/rt/s2_counter.py": FX_COUNTER_FILES[".ufo/waves/rt/s2_counter.py"],
        "SKILL.md": FX_SKILL_F5,
    }
    return run_fixture(work, "f5", files, {
        "exit": lambda r: r["exit"] == 2,
        "unevaluable": lambda r: r["unevaluable"] == ["s3_counter.py"],
        "not_met": lambda r: r["met"] is False,
    })


FX_SKILL_F6 = (
    FX_HEADER
    + "```markdown\n"
    + "| s1_counter.py | gate | `python3 -B .ufo/waves/rt/s1_counter.py --revision <commit>`"
    + " | 0=met | --selftest | f6 | lane | fx |\n"
    + "```\n"
    + "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    + " | 0=met | --selftest | f6 | lane | fx |\n"
    + "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    + " | 0=met | --selftest | f6 | lane | fx |\n"
)


def fx_f6(work):
    """f6: a table row inside a fenced code block is documentation, not a registry row."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F6
    return run_fixture(work, "f6", files, {
        "exit": lambda r: r["exit"] == 1,
        "rows_s1_zero": lambda r: r["counters"][0]["rows"] == 0,
        "rows_s2_s3": lambda r: [c["rows"] for c in r["counters"]] == [0, 1, 1],
        "unregistered": lambda r: r["unregistered_names"] == ["s1_counter.py"],
        "not_met": lambda r: r["met"] is False,
        "evaluable": lambda r: not r["unevaluable"],
    })


FX_SKILL_F7 = FX_HEADER + (
    "| helper alias | alias row that cites s1_counter.py only as a witness"
    " | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | s1_counter.py cited only here | f7 | lane | fx |\n"
    "| s2_counter.py | gate | `python3 -B .ufo/waves/rt/s2_counter.py --revision <commit>`"
    " | 0=met | --selftest | f7 | lane | fx |\n"
    "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    " | 0=met | --selftest | f7 | lane | fx |\n"
)

FX_SKILL_F8 = FX_HEADER + (
    "| s1_counter.py s2_counter.py | gate"
    " | `python3 -B .ufo/waves/rt/s1_counter.py --revision <commit>`"
    " | 0=met | --selftest | f8 | lane | fx |\n"
    "| s3_counter.py | gate | `python3 -B .ufo/waves/rt/s3_counter.py --revision <commit>`"
    " | 0=met | --selftest | f8 | lane | fx |\n"
)


def fx_f7(work):
    """f7: a filename only in the Pinned-values cell does not register the counter (A1)."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F7
    return run_fixture(work, "f7", files, {
        "exit": lambda r: r["exit"] == 1,
        "unregistered": lambda r: r["unregistered_names"] == ["s1_counter.py"],
        "rows_s1_zero": lambda r: r["counters"][0]["rows"] == 0,
        "not_met": lambda r: r["met"] is False,
    })


def fx_f8(work):
    """f8: a dump row naming two population counters in its credited cells credits none (A2)."""
    files = dict(FX_COUNTER_FILES)
    files["SKILL.md"] = FX_SKILL_F8
    return run_fixture(work, "f8", files, {
        "exit": lambda r: r["exit"] == 1,
        "unregistered": lambda r: r["unregistered_names"] == ["s1_counter.py", "s2_counter.py"],
        "rows_s1_s2_zero": lambda r: [c["rows"] for c in r["counters"]] == [0, 0, 1],
        "not_met": lambda r: r["met"] is False,
    })


FIXTURES = (("f1", fx_f1), ("f2", fx_f2), ("f3", fx_f3), ("f4", fx_f4), ("f5", fx_f5),
            ("f6", fx_f6), ("f7", fx_f7), ("f8", fx_f8))


def selftest_main(args):
    created = []
    work = args.work
    if work:
        os.makedirs(work, exist_ok=True)
    else:
        work = tempfile.mkdtemp(prefix="c74rg-selftest-")
        created.append(work)
    passed = 0
    try:
        for label, fixture in FIXTURES:
            try:
                ok, detail = fixture(work)
            except Exception as exc:  # harness: any infrastructure failure fails the fixture
                ok, detail = False, "exception: %r" % (exc,)
            if ok:
                passed += 1
            else:
                sys.stderr.write("%s: FAIL %s\n" % (label, detail))
    finally:
        for path in created:
            shutil.rmtree(path, ignore_errors=True)
    sys.stdout.write("selftest %d/%d\n" % (passed, len(FIXTURES)))
    return 0 if passed == len(FIXTURES) else 1


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write("%s: error: %s\n" % (self.prog, message))
        raise SystemExit(64)


def main(argv=None):
    parser = UsageParser(
        prog="c74_registry_gap.py",
        description="Round-74 C1 gate-registry gap counter (see module docstring).",
    )
    parser.add_argument("--root", default=".", help="lane checkout (default .)")
    parser.add_argument("--revision", default="HEAD", help="measured revision (default HEAD)")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    parser.add_argument("--selftest", action="store_true", help="run contract fixtures f1-f5")
    parser.add_argument("--work", default=None, help="scratch dir for selftest fixture repos")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest_main(args)
    result = evaluate(args.root, args.revision)
    if args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        sys.stdout.write(render_plain(result))
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
