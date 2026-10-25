#!/usr/bin/env python3
"""Round-56 C1 counter — calibration: SKILL.md registry self-test tallies against the observed tallies.

Surface: ten rows of the `SKILL.md` gate registry whose self-test cell states how many fixtures a
selftest holds. A row is a self-assessment ("this gate's selftest has N cases and passes"); the
observed state is what that same command prints when it is run, as documented in the row, in a clean
clone of the measured revision. Version 1 (frozen before any seat scored).

Per pinned row (`POP`), at the measured revision `<rev>`:

  row_missing       no registry table row whose first cell is the row name
  command_missing   the row's self-test cell holds no backticked command naming the pinned script
                    (a leading `VAR=value` word, or several, is part of the documented command)
  claim_missing     the claim regex finds no integer in the self-test cell
  tool_changed      the pinned script's blob at <rev> differs from its blob at BASE_REV
                    (a selftest that was rewritten is a different claim)
  selftest_failed   the documented command exits non-zero, or prints a tally A/B with A != B
  claim_ne_observed the sum of the claim integers != the observed total B of the printed tally A/B

A row with any of these is one mismatch; `tally_mismatches` counts rows. An unparsable tally (no A/B
in the output) is unevaluable (exit 2), never a pass.

Predicate (frozen in `contract.json`):

    met: tally_mismatches == 0 AND rows_checked == 10

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (revision does not resolve, clone or
command could not run, tally unparsable, timeout), 64 usage.

Reads committed bytes: `git show`/`git rev-parse` for the registry and blobs, and runs each documented
selftest inside `mktemp -d` clone of the revision (no write to the lane, no network).
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

# (row name, pinned script, claim regex whose captured integers are summed over the self-test cell)
POP = [
    ("base-path-audit", "scripts/base_path_selftest.py", r"(\d+) (?:matrix |round-29 regression )?fixtures"),
    ("source-recheck-audit", "scripts/source_recheck_selftest.py", r"\((\d+) fixtures\)"),
    ("robots-expectation-audit", "scripts/robots_audit_selftest.py", r"\((\d+) fixtures\)"),
    ("sitemap-file-audit", "scripts/sitemap_audit_selftest.py", r"\((\d+) fixtures"),
    ("redirect-expectation-audit", "scripts/redirect_audit.py", r"\((\d+)/\d+;"),
    ("commit-citation-lint", "scripts/citation_lint.py", r"\((\d+)/\d+;"),
    ("wave-evidence-ledger", ".ufo/waves/round-52/c52_wave_ledger.py", r"\((\d+) fixtures"),
    ("quote-truth-counter", ".ufo/waves/round-52/c52_quote_truth.py", r"\((\d+) fixtures"),
    ("readme-index-counter", ".ufo/waves/round-55/c55_readme_index.py", r"\((\d+) (?:fixtures|checks)"),
    ("yahoo-robots-quote-truth-counter", ".ufo/waves/round-55/c55_quote_truth.py",
     r"\((\d+) (?:sandbox-repo )?(?:fixtures|checks)"),
]
EXPECTED_ROWS = 10


def git(root: str, *args: str, env: dict | None = None) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, env=env)
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


def table_rows(text: str) -> dict[str, list[str]]:
    """Markdown table rows by first cell (first occurrence wins); no `## ` scoping — row names are unique."""
    out: dict[str, list[str]] = {}
    for line in text.split("\n"):
        if not re.match(r"^ {0,3}\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] not in out:
            out[cells[0]] = cells
    return out


def _is_selftest_span(span: str, script: str) -> bool:
    """A backticked command that runs `script` AS a selftest: the script is a *selftest*.py file or carries --selftest."""
    words = span.split()
    return script in words and ("--selftest" in words or "selftest" in os.path.basename(script))


def documented_command(cells: list[str], script: str) -> list[str] | None:
    """The backticked command in some cell that names `script`: [env assignments..., argv...]."""
    for cell in cells[1:]:
        for span in re.findall(r"`([^`]+)`", cell):
            if _is_selftest_span(span, script):
                span = re.sub(r"\[[^\]]*\]", "", span)
                try:
                    words = shlex.split(span)
                except ValueError:
                    return None
                return words
    return None


def selftest_cell(cells: list[str], script: str) -> str | None:
    for cell in cells[1:]:
        for span in re.findall(r"`([^`]+)`", cell):
            if _is_selftest_span(span, script):
                return cell
    return None


def parse_tally(output: str) -> tuple[int, int] | None:
    found = None
    for line in output.splitlines():
        m = re.search(r'"passedOverTotal":\s*"(\d+)/(\d+)"', line)
        if m:
            found = (int(m.group(1)), int(m.group(2)))
            continue
        if re.search(r"pass|selftest", line, re.I):
            for a, b in re.findall(r"\b(\d+)/(\d+)\b", line):
                found = (int(a), int(b))
    return found


def clone_at(root: str, rev: str) -> str:
    d = tempfile.mkdtemp(prefix="c56-tally-")
    proc = subprocess.run(["git", "clone", "-q", "--no-checkout", root, d], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"clone failed: {proc.stderr.strip()}")
    rc, _ = git(d, "checkout", "-q", rev)
    if rc != 0:
        raise RuntimeError(f"checkout {rev} failed")
    return d


def run_command(clone: str, words: list[str]) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    argv = []
    for w in words:
        if not argv and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", w):
            k, v = w.split("=", 1)
            env[k] = v
        else:
            argv.append(w)
    if not argv or argv[0] not in ("python3", "python", "node"):
        raise RuntimeError(f"unsupported command word {argv[:1]!r}")
    proc = subprocess.run(argv, cwd=clone, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, timeout=TIMEOUT)
    return proc.returncode, proc.stdout


def measure(root: str, rev: str, pop=None, base_rev: str = BASE_REV, expected: int = EXPECTED_ROWS):
    """Return (exit code, results). results: list of per-row dicts."""
    pop = POP if pop is None else pop
    doc = show(root, rev, DOC)
    if doc is None:
        return 2, [{"row": "-", "problems": [f"{DOC} unreadable at the revision"], "facts": {}}]
    rows = table_rows(doc)
    results: list[dict] = []
    clone = None
    try:
        for name, script, rx in pop:
            problems: list[str] = []
            facts: dict = {"script": script}
            cells = rows.get(name)
            if cells is None:
                results.append({"row": name, "problems": ["row_missing"], "facts": facts})
                continue
            words = documented_command(cells, script)
            cell = selftest_cell(cells, script)
            if words is None or cell is None:
                results.append({"row": name, "problems": ["command_missing"], "facts": facts})
                continue
            nums = [int(x) for x in re.findall(rx, cell)]
            claim = sum(nums) if nums else None
            facts["claim"] = claim
            facts["command"] = " ".join(words)
            if claim is None:
                problems.append("claim_missing")
            if blob(root, rev, script) is None or blob(root, rev, script) != blob(root, base_rev, script):
                problems.append("tool_changed")
            if clone is None:
                clone = clone_at(root, rev)
            try:
                code, out = run_command(clone, words)
            except subprocess.TimeoutExpired:
                return 2, results + [{"row": name, "problems": ["timeout"], "facts": facts}]
            tally = parse_tally(out)
            if tally is None:
                return 2, results + [{"row": name, "problems": [f"tally_unparsable (exit {code})"], "facts": facts}]
            facts["observed"] = f"{tally[0]}/{tally[1]}"
            facts["exit"] = code
            if code != 0 or tally[0] != tally[1]:
                problems.append("selftest_failed")
            if claim is not None and claim != tally[1]:
                problems.append("claim_ne_observed")
            results.append({"row": name, "problems": problems, "facts": facts})
    except (RuntimeError, OSError) as exc:
        return 2, results + [{"row": "-", "problems": [f"unevaluable: {exc}"], "facts": {}}]
    finally:
        if clone:
            shutil.rmtree(clone, ignore_errors=True)
    mism = sum(1 for r in results if r["problems"])
    met = mism == 0 and len(results) == expected
    return (0 if met else 1), results


def render(rev: str, code: int, results: list[dict]) -> str:
    mism = sum(1 for r in results if r["problems"])
    lines = [f"C1 selftest-tally tally_mismatches={mism} rows_checked={len(results)} met={code == 0}  ({PREDICATE})"]
    for r in results:
        f = r["facts"]
        lines.append(f"  {r['row']}: claim={f.get('claim')} observed={f.get('observed')} "
                     f"{'OK' if not r['problems'] else 'MISMATCH ' + ','.join(r['problems'])}")
    lines.append(f"  revision: {rev}")
    lines.append(f"EXIT={code}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- selftest

FAKE_OK = 'import sys\nprint("selftest: %d/%d passed")\n'
FAKE_ENV = ('import os,sys\nok = os.environ.get("PIN") == "1"\n'
            'print("selftest: %d/%d passed" % ((3, 3) if ok else (2, 3)))\nsys.exit(0 if ok else 1)\n')


def _sandbox(skill: str, scripts: dict[str, str], base_scripts: dict[str, str] | None = None) -> tuple[str, str, str]:
    d = tempfile.mkdtemp(prefix="c56-selftally-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    rc, top = git(d, "rev-parse", "--show-toplevel")
    if os.path.realpath(top.strip()) != os.path.realpath(d):
        raise RuntimeError("fixture toplevel mismatch")

    def commit(files: dict[str, str], msg: str) -> str:
        for rel, text in files.items():
            tgt = os.path.join(d, rel)
            os.makedirs(os.path.dirname(tgt) or d, exist_ok=True)
            with open(tgt, "w", encoding="utf-8") as fh:
                fh.write(text)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "--allow-empty", "-m", msg], check=True)
        return git(d, "rev-parse", "HEAD")[1].strip()

    base = commit({**(base_scripts if base_scripts is not None else scripts)}, "base")
    tip = commit({**scripts, DOC: skill}, "tip")
    return d, base, tip


def selftest() -> int:
    pop = [("alpha", "t/alpha_selftest.py", r"\((\d+) fixtures\)"),
           ("beta", "t/beta_selftest.py", r"\((\d+) fixtures\)")]
    alpha = FAKE_OK % (4, 4)
    beta = FAKE_ENV

    def skill(a_cell="`python3 -B t/alpha_selftest.py` (4 fixtures)", b_cell="`PIN=1 python3 -B t/beta_selftest.py` (3 fixtures)",
              a_name="alpha", b_name="beta", extra=""):
        return ("| Name | Self-test |\n|---|---|\n" + (f"| {a_name} | {a_cell} |\n" if a_name else "")
                + (f"| {b_name} | {b_cell} |\n" if b_name else "") + extra)

    good_scripts = {"t/alpha_selftest.py": alpha, "t/beta_selftest.py": beta}
    cases = []  # (name, skill text, scripts, base scripts or None, expected exit, expected problem substring, pop)

    def add(name, sk, scripts=None, base=None, want=1, sub=None, p=None, n=2):
        cases.append((name, sk, scripts or good_scripts, base, want, sub, p or pop, n))

    add("pass", skill(), want=0)
    add("do_nothing_stale_count", skill(a_cell="`python3 -B t/alpha_selftest.py` (3 fixtures)"), sub="claim_ne_observed")
    add("claim_off_by_one_high", skill(a_cell="`python3 -B t/alpha_selftest.py` (5 fixtures)"), sub="claim_ne_observed")
    add("claim_deleted", skill(a_cell="`python3 -B t/alpha_selftest.py` (many fixtures)"), sub="claim_missing")
    add("env_pin_removed", skill(b_cell="`python3 -B t/beta_selftest.py` (3 fixtures)"), sub="selftest_failed")
    add("row_deleted", skill(b_name=""), sub="row_missing")
    add("command_swapped_to_other_script", skill(a_cell="`python3 -B t/beta_selftest.py` (4 fixtures)"), sub="command_missing")
    add("tool_replaced_by_fake_print", skill(),
        scripts={**good_scripts, "t/alpha_selftest.py": FAKE_OK % (4, 4) + "# faked\n"}, base=good_scripts, sub="tool_changed")
    add("tally_not_equal_pass_fail", skill(a_cell="`python3 -B t/alpha_selftest.py` (3 fixtures)"),
        scripts={**good_scripts, "t/alpha_selftest.py": 'print("selftest: 2/3 passed")\n'}, base=good_scripts, sub="selftest_failed")
    add("claim_in_wrong_cell_only", skill(a_cell="`python3 -B t/alpha_selftest.py`", extra="| note | (4 fixtures) |\n"), sub="claim_missing")
    add("two_claims_sum_wrong", skill(a_cell="`python3 -B t/alpha_selftest.py` (2 fixtures) (2 fixtures) (1 fixtures)"), sub="claim_ne_observed")
    add("population_one_short", skill(), want=1, sub=None, p=pop[:1], n=2)
    add("unparsable_tally", skill(), scripts={**good_scripts, "t/alpha_selftest.py": 'print("done")\n'},
        base={**good_scripts, "t/alpha_selftest.py": 'print("done")\n'}, want=2, sub="tally_unparsable")
    passed, fails = 0, []
    for name, sk, scripts, base, want, sub, p, n in cases:
        d, base_rev, tip = _sandbox(sk, scripts, base)
        try:
            code, results = measure(d, tip, pop=p, base_rev=base_rev, expected=n)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        text = json.dumps(results)
        ok = code == want and (sub is None or sub in text)
        if ok:
            passed += 1
        else:
            fails.append(f"{name}: expected {want} with {sub!r}, got {code} {text[:200]}")
    unit = {
        "parse_json_tally": parse_tally('{"passedOverTotal": "106/106", "x": 1}') == (106, 106),
        "parse_pass_line": parse_tally("PASS 235/235") == (235, 235),
        "parse_selftest_line": parse_tally("c55 quote-truth selftest: 54/54 (fixture revision abc)") == (54, 54),
        "parse_none": parse_tally("no tally here") is None,
        "env_prefix_split": documented_command(["x", "`KAKE_X=1 python3 -B a/b.py --selftest` (3 fixtures)"], "a/b.py")
        == ["KAKE_X=1", "python3", "-B", "a/b.py", "--selftest"],
        "brackets_stripped": documented_command(["x", "`python3 -B a/b_selftest.py [--tool PATH]`"], "a/b_selftest.py")
        == ["python3", "-B", "a/b_selftest.py"],
        "entry_command_not_selftest": documented_command(
            ["x", "`python3 -B a/b.py --manifest PATH`", "`python3 -B a/b.py --selftest` (3 fixtures)"], "a/b.py")
        == ["python3", "-B", "a/b.py", "--selftest"],
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
                          "rows_checked": len(results), "rows": results, "exit": code, "met": code == 0},
                         indent=1, ensure_ascii=False))
        return code
    print(render(args.revision, code, results))
    return code


if __name__ == "__main__":
    sys.exit(main())
