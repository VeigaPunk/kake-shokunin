#!/usr/bin/env python3
"""Round-56 C1 counter — calibration: SKILL.md registry self-test tallies against the observed tallies.

Surface: ten rows of the `SKILL.md` gate registry whose self-test cell states how many fixtures a
selftest holds. A row is a self-assessment ("this gate's selftest has N cases and passes"); the
observed state is what that same command prints when it is run, as documented in the row, in a clean
clone of the measured revision under a fixed environment.

Version 1 was frozen at `2d308e808bfd` before any seat scored. Version 2 (this file) folds in the wave-1 pre-data attacks
(`w1/CriticC1Contract.md` A1..A10 W1..W6, `w1/MutC1Counter.md` M03 M07 M09 M12 M13 M16 survivors,
`w1/ReviewerSelftallyCode.md`): the documented command must be exactly `[pin ...] python3 -B <script> <pinned args>`
(no `-c`, no extra words); the environment is fixed, not inherited, and only a `KAKE_R5N_SELFTEST_REV=<hex>` pin written
in the row counts; one claim per cell unless the row is a declared sum; a duplicated row name is a mismatch;
every `*.py` beside the pinned script at the base revision must be byte-identical; the tally line must be anchored;
`rows_checked` counts rows whose command was found and valid. The predicate sentence is unchanged.

Per pinned row (`POP`), at the measured revision `<rev>`:

  row_missing       no table row whose first cell is the row name
  duplicate_row     the first cell occurs in more than one table row of SKILL.md
  command_missing   no backticked command in the row names the pinned script as a selftest
  command_invalid   the documented command is not exactly `[pin ...] python3 -B <script> <pinned args>`
  claim_missing     the claim regex finds no integer in the command's cell
  claim_ambiguous   the regex finds more than one integer and the row is not a declared sum
  tool_changed      the pinned script, or any `*.py` beside it at BASE_REV, differs or is absent at <rev>
  selftest_failed   the documented command exits non-zero, or prints a tally A/B with A != B
  claim_ne_observed the claim != the observed total B of the printed tally A/B
  command_unrunnable the command could not be started

A row with any of these is one mismatch; `tally_mismatches` counts rows; `rows_checked` counts rows whose command
was found and valid. An unparsable tally (no anchored A/B line) or a timeout is unevaluable (exit 2).

Predicate (frozen in `contract.json`):

    met: tally_mismatches == 0 AND rows_checked == 10

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (revision does not resolve, clone could not run,
tally unparsable, timeout), 64 usage.

Reads committed bytes: `git show`/`git rev-parse` for the registry and blobs, and runs each documented
selftest inside a `mktemp -d` clone of the revision (no write to the lane, no network).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: tally_mismatches == 0 AND rows_checked == 10"
BASE_REV = "e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6"
DOC = "SKILL.md"
TIMEOUT = 300
PIN_RX = r"KAKE_R5[0-9]_SELFTEST_REV=[0-9a-f]{7,40}"

# (row name, pinned script, pinned args, claim regex, sum_ok). The documented command must be exactly
# `[pin ...] python3 -B <script> <args...>`; the claim regex must match exactly one integer unless `sum_ok`.
POP = [
    ("base-path-audit", "scripts/base_path_selftest.py", [], r"(\d+) (?:matrix |round-29 regression )?fixtures", True),
    ("source-recheck-audit", "scripts/source_recheck_selftest.py", [], r"\((\d+) fixtures\)", False),
    ("robots-expectation-audit", "scripts/robots_audit_selftest.py", [], r"\((\d+) fixtures\)", False),
    ("sitemap-file-audit", "scripts/sitemap_audit_selftest.py", ["--tool", "scripts/sitemap_audit.py"], r"\((\d+) fixtures", False),
    ("redirect-expectation-audit", "scripts/redirect_audit.py", ["--selftest"], r"\((\d+)/\d+;", False),
    ("commit-citation-lint", "scripts/citation_lint.py", ["--selftest"], r"\((\d+)/\d+;", False),
    ("wave-evidence-ledger", ".ufo/waves/round-52/c52_wave_ledger.py", ["--selftest"], r"\((\d+) fixtures", False),
    ("quote-truth-counter", ".ufo/waves/round-52/c52_quote_truth.py", ["--selftest"], r"\((\d+) fixtures", False),
    ("readme-index-counter", ".ufo/waves/round-55/c55_readme_index.py", ["--selftest"], r"\((\d+) (?:fixtures|checks)", False),
    ("yahoo-robots-quote-truth-counter", ".ufo/waves/round-55/c55_quote_truth.py", ["--selftest"],
     r"\((\d+) (?:sandbox-repo )?(?:fixtures|checks)", False),
]
EXPECTED_ROWS = 10
TALLY_RES = [
    re.compile(r'"passedOverTotal":\s*"(\d+)/(\d+)"'),
    re.compile(r"^\s*PASS\s+(\d+)/(\d+)\b"),
    re.compile(r"^\s*[\w .-]*selftest[\w .-]*:\s*(\d+)/(\d+)\b", re.I),
    re.compile(r"^\s*(\d+)/(\d+) fixtures passed\b"),
]


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return None
    try:
        return proc.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def blob(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "rev-parse", "--verify", "--quiet", f"{rev}:{path}")
    return out.strip() if rc == 0 and out.strip() else None


def table_rows(text: str) -> dict[str, list[list[str]]]:
    """Markdown table rows by first cell, every occurrence kept (a duplicate name is a mismatch). Cells split on
    unescaped pipes; 0-3 leading spaces tolerated."""
    out: dict[str, list[list[str]]] = {}
    for line in text.split("\n"):
        if not re.match(r"^ {0,3}\|", line):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if cells:
            out.setdefault(cells[0], []).append(cells)
    return out


def _strip_brackets(span: str) -> str:
    prev = None
    while prev != span:
        prev = span
        span = re.sub(r"\[[^\[\]]*\]", "", span)
    return span


def _words(span: str) -> list[str] | None:
    try:
        return shlex.split(_strip_brackets(span))
    except ValueError:
        return None


def _is_selftest_words(words: list[str], script: str) -> bool:
    return script in words and ("--selftest" in words or "selftest" in os.path.basename(script))


def documented_command(cells: list[str], script: str) -> tuple[list[str], str] | None:
    """(words, cell) of the first backticked command in some cell that runs `script` as a selftest."""
    for cell in cells[1:]:
        for span in re.findall(r"`([^`]+)`", cell):
            words = _words(span)
            if words is not None and _is_selftest_words(words, script):
                return words, cell
    return None


def command_problem(words: list[str], script: str, args: list[str], pin_rx: str = PIN_RX) -> str | None:
    """None when words == [pin ...] python3 -B script args exactly, else a short reason."""
    i = 0
    while i < len(words) and re.fullmatch(pin_rx, words[i]):
        i += 1
    if words[i:] != ["python3", "-B", script, *args]:
        return f"documented command {' '.join(words[i:])!r} is not `python3 -B {script} {' '.join(args)}`".rstrip().replace("` `", "`")
    return None


def parse_tally(output: str) -> tuple[int, int] | None:
    found = None
    for line in output.splitlines():
        for rx in TALLY_RES:
            m = rx.search(line)
            if m:
                found = (int(m.group(1)), int(m.group(2)))
                break
    return found


def clone_at(root: str, rev: str) -> str:
    d = tempfile.mkdtemp(prefix="c56-tally-")
    try:
        proc = subprocess.run(["git", "clone", "-q", "--no-checkout", root, d], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"clone failed: {proc.stderr.strip()}")
        if git(d, "checkout", "-q", rev)[0] != 0:
            raise RuntimeError(f"checkout {rev} failed")
    except BaseException:
        shutil.rmtree(d, ignore_errors=True)
        raise
    return d


def run_command(clone: str, words: list[str], pin_rx: str = PIN_RX) -> tuple[int, str]:
    """Fixed environment: nothing is inherited except PATH/HOME/LANG; pins come only from the documented words."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", clone),
           "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
    argv = []
    for w in words:
        if not argv and re.fullmatch(pin_rx, w):
            k, v = w.split("=", 1)
            env[k] = v
        else:
            argv.append(w)
    proc = subprocess.run(argv, cwd=clone, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, timeout=TIMEOUT)
    return proc.returncode, proc.stdout


def helpers_changed(root: str, rev: str, base_rev: str, script: str) -> list[str]:
    """The pinned script and every *.py beside it at the base revision must be byte-identical at rev."""
    d = os.path.dirname(script)
    rc, out = git(root, "ls-tree", "--name-only", base_rev, f"{d}/" if d else "")
    names = [n for n in out.split("\n") if n.endswith(".py")] if rc == 0 else []
    if script not in names:
        names.append(script)
    return [n for n in names if blob(root, rev, n) is None or blob(root, rev, n) != blob(root, base_rev, n)]


def measure(root: str, rev: str, pop=None, base_rev: str = BASE_REV, expected: int = EXPECTED_ROWS,
            pin_rx: str = PIN_RX):
    """Return (exit code, results). results: one dict per pinned row."""
    pop = POP if pop is None else pop
    doc = show(root, rev, DOC)
    if doc is None:
        return 2, [{"row": "-", "problems": [f"{DOC} unreadable at the revision"], "facts": {}, "checked": False}]
    rows = table_rows(doc)
    results: list[dict] = []
    clone = None
    try:
        for name, script, args, rx, sum_ok in pop:
            problems: list[str] = []
            facts: dict = {"script": script}
            occ = rows.get(name, [])
            if not occ:
                results.append({"row": name, "problems": ["row_missing"], "facts": facts, "checked": False})
                continue
            if len(occ) > 1:
                problems.append("duplicate_row")
            found = documented_command(occ[0], script)
            if found is None:
                results.append({"row": name, "problems": problems + ["command_missing"], "facts": facts, "checked": False})
                continue
            words, cell = found
            facts["command"] = " ".join(words)
            bad = command_problem(words, script, args, pin_rx)
            if bad:
                results.append({"row": name, "problems": problems + ["command_invalid"], "facts": {**facts, "why": bad}, "checked": False})
                continue
            nums = [int(x) for x in re.findall(rx, cell)]
            claim = None
            if not nums:
                problems.append("claim_missing")
            elif len(nums) > 1 and not sum_ok:
                problems.append("claim_ambiguous")
            else:
                claim = sum(nums)
            facts["claim"] = claim
            changed = helpers_changed(root, rev, base_rev, script)
            if changed:
                problems.append("tool_changed")
                facts["changed"] = changed
            if clone is None:
                clone = clone_at(root, rev)
            try:
                code, out = run_command(clone, words, pin_rx)
            except subprocess.TimeoutExpired:
                return 2, results + [{"row": name, "problems": ["timeout"], "facts": facts, "checked": True}]
            except OSError as exc:
                problems.append("command_unrunnable")
                facts["why"] = str(exc)
                results.append({"row": name, "problems": problems, "facts": facts, "checked": True})
                continue
            tally = parse_tally(out)
            if tally is None:
                return 2, results + [{"row": name, "problems": [f"tally_unparsable (exit {code})"], "facts": facts, "checked": True}]
            facts["observed"] = f"{tally[0]}/{tally[1]}"
            facts["exit"] = code
            if code != 0 or tally[0] != tally[1]:
                problems.append("selftest_failed")
            if claim is not None and claim != tally[1]:
                problems.append("claim_ne_observed")
            results.append({"row": name, "problems": problems, "facts": facts, "checked": True})
    except (RuntimeError, OSError) as exc:
        return 2, results + [{"row": "-", "problems": [f"unevaluable: {exc}"], "facts": {}, "checked": False}]
    finally:
        if clone:
            shutil.rmtree(clone, ignore_errors=True)
    mism = sum(1 for r in results if r["problems"])
    checked = sum(1 for r in results if r["checked"])
    met = mism == 0 and checked == expected
    return (0 if met else 1), results


def render(rev: str, code: int, results: list[dict]) -> str:
    mism = sum(1 for r in results if r["problems"])
    checked = sum(1 for r in results if r["checked"])
    lines = [f"C1 selftest-tally tally_mismatches={mism} rows_checked={checked} met={code == 0}  ({PREDICATE})"]
    for r in results:
        f = r["facts"]
        lines.append(f"  {r['row']}: claim={f.get('claim')} observed={f.get('observed')} "
                     f"{'OK' if not r['problems'] else 'MISMATCH ' + ','.join(r['problems'])}")
    lines.append(f"  revision: {rev}")
    lines.append(f"EXIT={code}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest

FAKE_OK = 'print("selftest: %d/%d passed")\n'
FAKE_ENV = ('import os,sys\nok = os.environ.get("PIN") == "1"\n'
            'print("selftest: %d/%d passed" % ((3, 3) if ok else (2, 3)))\nsys.exit(0 if ok else 1)\n')
TEST_PIN = r"PIN=1"


def _sandbox(skill: str, scripts: dict, base_scripts: dict | None = None) -> tuple[str, str, str]:
    """base commit = base_scripts (or scripts); tip commit = scripts + SKILL.md. A None value deletes the path at tip."""
    d = tempfile.mkdtemp(prefix="c56-selftally-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    rc, top = git(d, "rev-parse", "--show-toplevel")
    if os.path.realpath(top.strip()) != os.path.realpath(d):
        raise RuntimeError("fixture toplevel mismatch")

    def commit(files: dict, msg: str) -> str:
        for rel, text in files.items():
            tgt = os.path.join(d, rel)
            if text is None:
                if os.path.exists(tgt):
                    os.remove(tgt)
                continue
            os.makedirs(os.path.dirname(tgt) or d, exist_ok=True)
            with open(tgt, "w", encoding="utf-8") as fh:
                fh.write(text)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "--allow-empty", "-m", msg], check=True)
        return git(d, "rev-parse", "HEAD")[1].strip()

    base = commit(dict(base_scripts if base_scripts is not None else scripts), "base")
    tip = commit({**scripts, DOC: skill}, "tip")
    return d, base, tip


def selftest() -> int:
    global TIMEOUT
    pop = [("alpha", "t/alpha_selftest.py", [], r"\((\d+) fixtures\)", False),
           ("beta", "t/beta_selftest.py", [], r"\((\d+) fixtures\)", False)]
    alpha, beta = FAKE_OK % (4, 4), FAKE_ENV
    A_CMD, B_CMD = "`python3 -B t/alpha_selftest.py`", "`PIN=1 python3 -B t/beta_selftest.py`"

    def skill(a_cell=f"{A_CMD} (4 fixtures)", b_cell=f"{B_CMD} (3 fixtures)", a_name="alpha", b_name="beta", extra="",
              pre="", indent=""):
        body = ("| Name | Self-test |\n|---|---|\n" + (f"| {a_name} | {a_cell} |\n" if a_name else "")
                + (f"| {b_name} | {b_cell} |\n" if b_name else "") + extra)
        body = "\n".join(indent + ln if ln else ln for ln in body.split("\n"))
        return pre + body

    good = {"t/alpha_selftest.py": alpha, "t/beta_selftest.py": beta}
    cases = []

    def add(name, sk, scripts=None, base=None, want=1, sub=None, p=None, n=2, timeout=None):
        cases.append((name, sk, scripts or good, base, want, sub, p or pop, n, timeout))

    add("pass", skill(), want=0)
    add("pass_indented_table", skill(indent="  "), want=0)
    add("pass_claim_sum_declared", skill(a_cell=f"{A_CMD} (2 fixtures) (2 fixtures)"), want=0,
        p=[("alpha", "t/alpha_selftest.py", [], r"\((\d+) fixtures\)", True), pop[1]])
    add("pass_last_tally_line_wins", skill(), scripts={**good, "t/alpha_selftest.py": 'print("stage1 selftest: 3/3 passed")\nprint("selftest: 4/4 passed")\n'}, want=0)
    add("pass_quoted_script_path", skill(a_cell='`python3 -B "t/alpha_selftest.py"` (4 fixtures)'), want=0)
    add("pass_escaped_pipe_in_later_cell", skill(extra="| x | a \\| b |\n"), want=0)
    add("do_nothing_stale_count", skill(a_cell=f"{A_CMD} (3 fixtures)"), sub="claim_ne_observed")
    add("claim_off_by_one_high", skill(a_cell=f"{A_CMD} (5 fixtures)"), sub="claim_ne_observed")
    add("claim_deleted", skill(a_cell=f"{A_CMD} (many fixtures)"), sub="claim_missing")
    add("env_pin_removed", skill(b_cell="`python3 -B t/beta_selftest.py` (3 fixtures)"), sub="selftest_failed")
    add("row_deleted", skill(b_name=""), sub="row_missing")
    add("command_swapped_to_other_script", skill(a_cell="`python3 -B t/beta_selftest.py` (4 fixtures)"), sub="command_missing")
    add("tool_replaced_by_fake_print", skill(), scripts={**good, "t/alpha_selftest.py": FAKE_OK % (4, 4) + "# faked\n"}, base=good, sub="tool_changed")
    add("helper_beside_script_changed", skill(), scripts={**good, "t/helper.py": "X = 2\n"}, base={**good, "t/helper.py": "X = 1\n"}, sub="tool_changed")
    add("pinned_script_deleted_at_tip", skill(), scripts={**good, "t/alpha_selftest.py": None}, base=good, want=2, sub="unevaluable|selftest_failed|tally_unparsable|tool_changed")
    add("tally_not_equal_pass_fail", skill(a_cell=f"{A_CMD} (3 fixtures)"),
        scripts={**good, "t/alpha_selftest.py": 'print("selftest: 2/3 passed")\n'}, base=good, sub="selftest_failed")
    add("claim_in_wrong_cell_only", skill(a_cell=A_CMD, extra="| note | (4 fixtures) |\n"), sub="claim_missing")
    add("two_claims_junk_sum_is_ambiguous", skill(a_cell=f"{A_CMD} (2 fixtures) (2 fixtures)"), sub="claim_ambiguous")
    add("population_one_short", skill(), p=pop[:1], n=2)
    add("unparsable_tally", skill(), scripts={**good, "t/alpha_selftest.py": 'print("done")\n'},
        base={**good, "t/alpha_selftest.py": 'print("done")\n'}, want=2, sub="tally_unparsable")
    add("fake_command_c_shadowing_honest", skill(a_cell="`python3 -c \"print(1)\" t/alpha_selftest.py` " + f"{A_CMD} (4 fixtures)"), sub="command_invalid")
    add("fake_command_c_only", skill(a_cell="`python3 -c \"print('selftest: 4/4 passed')\" t/alpha_selftest.py --selftest` (4 fixtures)"), sub="command_invalid")
    add("extra_arg_points_at_host", skill(a_cell="`python3 -B t/alpha_selftest.py --root /tmp` (4 fixtures)"), sub="command_invalid")
    add("pin_not_in_allowlist", skill(b_cell="`OTHER=1 python3 -B t/beta_selftest.py` (3 fixtures)"), sub="command_invalid")
    add("duplicate_row_earlier", skill(pre="| alpha | `python3 -B t/alpha_selftest.py` (4 fixtures) |\n\n", a_cell=f"{A_CMD} (9 fixtures)"), sub="duplicate_row")
    add("row_moved_to_other_section_duplicate", skill(extra="\n## Notes\n\n| alpha | `python3 -B t/alpha_selftest.py` (4 fixtures) |\n"), sub="duplicate_row")
    add("timeout_is_unevaluable", skill(), scripts={**good, "t/alpha_selftest.py": 'import time\ntime.sleep(30)\nprint("selftest: 4/4 passed")\n'},
        base={**good, "t/alpha_selftest.py": 'import time\ntime.sleep(30)\nprint("selftest: 4/4 passed")\n'}, want=2, sub="timeout", timeout=1)
    add("rows_checked_counts_found_rows_only", skill(b_name=""), p=pop, n=2, sub="row_missing")
    add("diagnostic_line_not_a_tally", skill(), scripts={**good, "t/alpha_selftest.py": 'print("selftest ran on 2026/10/25")\nprint("selftest: 4/4 passed")\n'}, want=0)
    add("diagnostic_only_is_unparsable", skill(), scripts={**good, "t/alpha_selftest.py": 'print("selftest ran on 2026/10/25")\n'},
        base={**good, "t/alpha_selftest.py": 'print("selftest ran on 2026/10/25")\n'}, want=2, sub="tally_unparsable")

    passed, fails = 0, []
    saved = TIMEOUT
    os.environ["PIN"] = "1"  # a host-exported pin must NOT rescue a row that omits it (env_pin_removed stays red)
    try:
        for name, sk, scripts, base, want, sub, p, n, timeout in cases:
            d, base_rev, tip = _sandbox(sk, scripts, base)
            TIMEOUT = timeout if timeout else saved
            try:
                code, results = measure(d, tip, pop=p, base_rev=base_rev, expected=n, pin_rx=TEST_PIN)
            finally:
                shutil.rmtree(d, ignore_errors=True)
                TIMEOUT = saved
            text = json.dumps(results)
            ok = code == want and (sub is None or any(s in text for s in sub.split("|")))
            if name == "rows_checked_counts_found_rows_only":
                ok = ok and sum(1 for r in results if r["checked"]) == 1
            if ok:
                passed += 1
            else:
                fails.append(f"{name}: expected {want} with {sub!r}, got {code} {text[:240]}")
    finally:
        os.environ.pop("PIN", None)
    unit = {
        "parse_json_tally": parse_tally('{"passedOverTotal": "106/106", "x": 1}') == (106, 106),
        "parse_pass_line": parse_tally("PASS 235/235") == (235, 235),
        "parse_selftest_line": parse_tally("c55 quote-truth selftest: 54/54 (fixture revision abc)") == (54, 54),
        "parse_fixtures_passed_line": parse_tally("45/45 fixtures passed") == (45, 45),
        "parse_none": parse_tally("no tally here") is None,
        "parse_date_is_not_a_tally": parse_tally("selftest ran on 2026/10/25") is None,
        "parse_dash_name_line": parse_tally("selftest: missing fixture 12/20") is None,
        "env_prefix_split": documented_command(["x", "`KAKE_R52_SELFTEST_REV=abc1234 python3 -B a/b.py --selftest` (3 fixtures)"], "a/b.py")
        == (["KAKE_R52_SELFTEST_REV=abc1234", "python3", "-B", "a/b.py", "--selftest"], "`KAKE_R52_SELFTEST_REV=abc1234 python3 -B a/b.py --selftest` (3 fixtures)"),
        "brackets_stripped": (documented_command(["x", "`python3 -B a/b_selftest.py [--tool PATH]`"], "a/b_selftest.py") or ([],))[0]
        == ["python3", "-B", "a/b_selftest.py"],
        "nested_brackets_stripped": (documented_command(["x", "`python3 -B a/b_selftest.py [--tool [PATH]]`"], "a/b_selftest.py") or ([],))[0]
        == ["python3", "-B", "a/b_selftest.py"],
        "entry_command_not_selftest": (documented_command(
            ["x", "`python3 -B a/b.py --manifest PATH`", "`python3 -B a/b.py --selftest` (3 fixtures)"], "a/b.py") or ([],))[0]
        == ["python3", "-B", "a/b.py", "--selftest"],
        "shlex_error_span_skipped": documented_command(
            ["x", "`python3 -B t/a_selftest.py '`", "ok", "`python3 -B t/a_selftest.py` (1 fixtures)"], "t/a_selftest.py") is not None,
        "clone_cleanup_on_failure": _clone_cleans_up(),
    }
    for label, ok in unit.items():
        if ok:
            passed += 1
        else:
            fails.append(f"unit: {label}")
    total = len(cases) + len(unit)
    print(f"c56 selftally selftest: {passed}/{total}")
    for line in fails:
        print("  FAIL", line)
    return 0 if passed == total else 1


def _clone_cleans_up() -> bool:
    before = set(os.listdir(tempfile.gettempdir()))
    d = tempfile.mkdtemp(prefix="c56-selftally-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    try:
        clone_at(d, "0" * 40)
    except RuntimeError:
        pass
    shutil.rmtree(d, ignore_errors=True)
    return not any(n.startswith("c56-tally-") for n in set(os.listdir(tempfile.gettempdir())) - before)


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-56 C1 counter (SKILL.md selftest tallies)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        print("usage: --revision is required unless --selftest is used", file=sys.stderr)
        return 64
    if git(args.root, "rev-parse", "--verify", "--quiet", f"{args.revision}^{{commit}}")[0] != 0:
        print(f"unevaluable: revision {args.revision!r} does not resolve in {args.root!r}")
        print("EXIT=2")
        return 2
    code, results = measure(args.root, args.revision)
    if args.json:
        print(json.dumps({"schema": "kake-r56-c1-selftally-v1", "predicate": PREDICATE, "revision": args.revision,
                          "tally_mismatches": sum(1 for r in results if r["problems"]),
                          "rows_checked": sum(1 for r in results if r["checked"]), "rows": results, "exit": code, "met": code == 0},
                         indent=1, ensure_ascii=False))
        return code
    print(render(args.revision, code, results))
    return code


if __name__ == "__main__":
    sys.exit(main())
