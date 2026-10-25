#!/usr/bin/env python3
"""Round-57 C2 counter — operability (capability acquisition): the cross-registry source-id resolver.

Version 1 (frozen before any seat scored; an optional `--fleet` argument, default the parent of `--root`, was added before dispatch so a scratch clone can name the real fleet — no condition or predicate changed).

The capability (considerthese proposal 2, `considerthese/2026-10-25.md`): `scripts/id_resolver.py` lists every `S###` id
cited in `corpus/knowledge/**/*.md` that does not resolve in the lane's own `corpus/SOURCES.md`, and names which sibling
registry holds it. Round 52 left five such ids (S367 S372 S373 S390 S409) that resolved only in kotodama-shokunin's
registry; the round-53 verifier found them, not the lane.

CLI contract the gate exercises (the tool may add options; these are fixed):

    python3 -B scripts/id_resolver.py --root <lane dir> [--revision <rev>] [--fleet <fleet root>] [--selftest]

  - cited ids: every token `S` + 3 or more digits (word-bounded) in each `corpus/knowledge/**/*.md` file (a revision is read
    through `git show`, never the working tree); registry ids: first cell of each table row of `corpus/SOURCES.md` under
    `## Registry`, 0 to 3 leading spaces before the pipe (the census parser's rule).
  - siblings: every `<fleet>/*-shokunin/` other than the lane, read through `git show HEAD:corpus/SOURCES.md` when the
    directory is a git repo, else the file; a sibling owns an id when its registry has a row with that id.
  - stdout: one line per dangling id `DANGLING <id> cited-by=<comma paths> owners=<comma lane names or -> url-match=<lane names or ->`
    and a last line `ids_cited=<n> ids_resolved=<n> dangling=<n> owned_elsewhere=<n> unowned=<n>`.
  - exit: 0 when dangling == 0; 1 when dangling > 0; 2 unevaluable (revision unresolved, registry absent, no knowledge file);
    64 usage. `--selftest` prints a last line `selftest: <passed>/<total>` and exits 0 iff all passed.

Conditions (frozen in `contract.json`):

  G1 `scripts/id_resolver.py` exists at the measured revision.
  G2 its `--selftest`, run in a clean clone of the revision, exits 0 with `selftest: N/N` and N >= 16.
  G3 gate-owned fixture (built here, not by the tool): a lane with registry rows at 0 and 2 leading spaces, knowledge that
     cites a resolved id, a 4-digit id, an id held by one sibling (with the sibling's URL quoted in the citing file), an
     id held by two siblings and an id held by none, plus a decoy `S12`, `AS500` and `S500x`: the tool must print exactly the
     expected lines and totals and exit 1; the same fixture with the dangling citations removed must exit 0.
  G4 red-before: the tool run over the lane revision `3994101` (the round-52 verifier commit, base of the round-53 repair)
     with the real fleet reports exactly the five ids S367 S372 S373 S390 S409 dangling, each owned by `kotodama-shokunin`, exit 1.
  G5 green: the tool run over the measured revision itself reports dangling == 0 with ids_cited >= 100, exit 0.

Predicate (frozen in `contract.json`):

    met: gate_conditions_passed == 5 of 5

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: gate_conditions_passed == 5 of 5"
RED_REV = "3994101dba28896830604fd0b08c7f00faca8ed6"
RED_IDS = ["S367", "S372", "S373", "S390", "S409"]
RED_OWNER = "kotodama-shokunin"
TOOL = "scripts/id_resolver.py"
MIN_SELFTEST = 16
MIN_CITED = 100
SUMMARY = re.compile(r"^ids_cited=(\d+) ids_resolved=(\d+) dangling=(\d+) owned_elsewhere=(\d+) unowned=(\d+)$")
DANGLE = re.compile(r"^DANGLING (S\d{3,}) cited-by=(\S+) owners=(\S+) url-match=(\S+)$")


def git(*args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def sandbox_clone(root: str, rev: str) -> str:
    d = tempfile.mkdtemp(prefix="c57-gate-")
    for cmd in (["clone", "-q", "--no-checkout", root, d], ["-C", d, "checkout", "-q", rev]):
        p = git(*cmd)
        if p.returncode != 0:
            shutil.rmtree(d, ignore_errors=True)
            raise RuntimeError(f"git {' '.join(cmd)}: {p.stderr.strip()}")
    return d


def run_tool(clone: str, *args: str, timeout: int = 300) -> tuple[int, list[str]]:
    p = subprocess.run([sys.executable, "-B", os.path.join(clone, TOOL), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True, timeout=timeout, cwd=clone, env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp"),
                                                                      "LC_ALL": "C.UTF-8"})
    return p.returncode, p.stdout.strip().split("\n") if p.stdout.strip() else []


def parse(lines: list[str]) -> tuple[dict[str, tuple[str, str, str]], tuple[int, ...] | None]:
    dang, summ = {}, None
    for ln in lines:
        m = DANGLE.match(ln)
        if m:
            dang[m.group(1)] = (m.group(2), m.group(3), m.group(4))
        m = SUMMARY.match(ln)
        if m:
            summ = tuple(int(x) for x in m.groups())
    return dang, summ


def build_fixture() -> tuple[str, str, str]:
    """Return (fleet root, lane dir, lane dir with the dangling citations removed)."""
    fleet = tempfile.mkdtemp(prefix="c57-fixture-")

    def reg(path: str, rows: list[tuple[str, str]], indent: str = "") -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        body = "# SOURCES\n## Registry\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
        for sid, url in rows:
            body += f"{indent}| {sid} | t — {url} | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n"
        open(path, "w").write(body)

    lane = os.path.join(fleet, "demo-shokunin")
    reg(os.path.join(lane, "corpus/SOURCES.md"), [("S001", "https://e.example/1")])
    with open(os.path.join(lane, "corpus/SOURCES.md"), "a") as f:
        f.write("  | S002 | t — https://e.example/2 | docs | A | s | a | x | mined | 2026-10-25 | 90d | — |\n")
    reg(os.path.join(fleet, "alpha-shokunin/corpus/SOURCES.md"), [("S101", "https://a.example/101"), ("S200", "https://a.example/200"), ("S0300", "https://a.example/300")])
    reg(os.path.join(fleet, "beta-shokunin/corpus/SOURCES.md"), [("S200", "https://b.example/200")], indent="   ")
    os.makedirs(os.path.join(lane, "corpus/knowledge/sub"), exist_ok=True)
    good = "source: S001 — https://e.example/1\nverified-at: 2026-10-25\nrecheck: 90d\n\nCites S001 and S002 (resolved, the second row is indented two spaces).\n"
    open(os.path.join(lane, "corpus/knowledge/good.md"), "w").write(good)
    bad_a = ("source: S101 — https://a.example/101\n\nHeld by alpha only: S101, quoted at https://a.example/101.\nHeld by two siblings: S200.\n"
             "Held by none: S777. A four-digit id S0300 is alpha's five-character id and does not resolve here.\n"
             "Decoys that are not ids: S12, AS500, S500x, s101.\n")
    open(os.path.join(lane, "corpus/knowledge/sub/bad.md"), "w").write(bad_a)
    clean = tempfile.mkdtemp(prefix="c57-fixture-clean-")
    shutil.copytree(os.path.join(fleet, "alpha-shokunin"), os.path.join(clean, "alpha-shokunin"))
    shutil.copytree(os.path.join(fleet, "beta-shokunin"), os.path.join(clean, "beta-shokunin"))
    shutil.copytree(lane, os.path.join(clean, "demo-shokunin"))
    os.remove(os.path.join(clean, "demo-shokunin/corpus/knowledge/sub/bad.md"))
    return fleet, lane, os.path.join(clean, "demo-shokunin")


EXPECT_FIXTURE = {
    "S101": ("corpus/knowledge/sub/bad.md", "alpha-shokunin", "alpha-shokunin"),
    "S200": ("corpus/knowledge/sub/bad.md", "alpha-shokunin,beta-shokunin", "-"),
    "S0300": ("corpus/knowledge/sub/bad.md", "alpha-shokunin", "-"),
    "S777": ("corpus/knowledge/sub/bad.md", "-", "-"),
}
EXPECT_SUMMARY = (6, 2, 4, 3, 1)  # cited S001 S002 S101 S200 S0300 S777; resolved S001 S002; dangling 4; owned elsewhere 3; unowned 1


def evaluate(root: str, rev: str, fleet_real: str) -> tuple[int, list[tuple[str, bool, str]]]:
    results: list[tuple[str, bool, str]] = []
    present = git("-C", root, "cat-file", "-e", f"{rev}:{TOOL}").returncode == 0
    results.append(("G1_tool_present", present, "" if present else f"{TOOL} absent at {rev[:12]}"))
    if not present:
        for name in ("G2_selftest", "G3_fixture", "G4_red_before", "G5_green"):
            results.append((name, False, "tool absent"))
        return 1, results
    clone = sandbox_clone(root, rev)
    tmp: list[str] = [clone]
    try:
        rc, out = run_tool(clone, "--selftest")
        m = re.fullmatch(r"selftest: (\d+)/(\d+)", out[-1]) if out else None
        ok = bool(m) and rc == 0 and m.group(1) == m.group(2) and int(m.group(2)) >= MIN_SELFTEST
        results.append(("G2_selftest", ok, out[-1] if out else f"no output (exit {rc})"))

        fleet, lane, clean = build_fixture()
        tmp += [fleet, os.path.dirname(clean)]
        rc, out = run_tool(clone, "--root", lane, "--fleet", fleet)
        dang, summ = parse(out)
        ok = rc == 1 and dang == EXPECT_FIXTURE and summ == EXPECT_SUMMARY
        note = f"exit={rc} dangling={sorted(dang)} summary={summ}"
        if ok:
            rc2, out2 = run_tool(clone, "--root", clean, "--fleet", os.path.dirname(clean))
            d2, s2 = parse(out2)
            ok = rc2 == 0 and not d2 and s2 is not None and s2[2] == 0
            note += f"; clean exit={rc2} summary={s2}"
        results.append(("G3_fixture", ok, note))

        rc, out = run_tool(clone, "--root", root, "--revision", RED_REV, "--fleet", fleet_real)
        dang, summ = parse(out)
        ok = (rc == 1 and sorted(dang) == RED_IDS and all(RED_OWNER in v[1].split(",") for v in dang.values())
              and summ is not None and summ[2] == 5)
        results.append(("G4_red_before", ok, f"exit={rc} dangling={sorted(dang)} owners={ {k: v[1] for k, v in dang.items()} }"))

        rc, out = run_tool(clone, "--root", root, "--revision", rev, "--fleet", fleet_real)
        dang, summ = parse(out)
        ok = rc == 0 and not dang and summ is not None and summ[2] == 0 and summ[0] >= MIN_CITED
        results.append(("G5_green", ok, f"exit={rc} summary={summ}"))
    except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
        for d in tmp:
            shutil.rmtree(d, ignore_errors=True)
        print(f"C2 id-resolver-gate unevaluable: {type(exc).__name__}: {exc}")
        return 2, results
    for d in tmp:
        shutil.rmtree(d, ignore_errors=True)
    return (0 if all(r[1] for r in results) else 1), results


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-57 C2 gate (cross-registry id resolver)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--fleet", help="fleet root holding the sibling lanes (default: the parent of --root)")
    try:
        args = ap.parse_args()
    except SystemExit:
        return 64
    if not args.revision:
        print("usage: --root <lane> --revision <rev>", file=sys.stderr)
        return 64
    root = os.path.abspath(args.root)
    p = git("-C", root, "rev-parse", "--verify", f"{args.revision}^{{commit}}")
    if p.returncode != 0:
        print(f"C2 id-resolver-gate unevaluable: revision {args.revision} unresolved")
        return 2
    rev = p.stdout.strip()
    fleet = os.path.abspath(args.fleet) if args.fleet else os.path.dirname(root)
    code, results = evaluate(root, rev, fleet)
    if code == 2:
        return 2
    passed = sum(1 for r in results if r[1])
    print(f"C2 id-resolver {passed}/5 met={passed == 5}  ({PREDICATE})")
    for name, ok, note in results:
        print(f"  {name} {'PASS' if ok else 'FAIL'}" + (f"\n    - {note}" if note else ""))
    print(f"  revision: {rev}")
    return 0 if passed == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
