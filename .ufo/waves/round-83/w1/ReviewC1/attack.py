#!/usr/bin/env python3
"""ReviewC1 attack harness for round-83 C1 (c83_defect_queue.py).

Builds cheapest-satisfying trees per item, plus the specific falsification probes
(2a empty results, 2b print-only killers, 2c wrong-report erratum, D4 history
retargeting, D1 arithmetic) and runs the frozen counter as a subprocess on each.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r83/ReviewC1")
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
FLEET = Path("/home/vgpnk/Projects/shokunin")
COUNTER = LANE / ".ufo/waves/round-83/c83_defect_queue.py"
LESSON = "corpus/lessons/round-83.md"
QUALITY = "corpus/QUALITY.md"
SPEC = ".ufo/waves/round-83/w1-spec.json"
RESULTS = ".ufo/waves/round-83/w1-results.json"
ACCOUNTING = ".ufo/waves/round-83/w1-accounting.json"
RECEIPT = ".ufo/waves/round-83/controls/after-c83-instrument-check.txt"
KILLER = ".ufo/waves/round-83/killers/run_killers.py"
TREES = S / "trees"
RUNS = S / "runs"
FLEETS = S / "fleets"
for d in (TREES, RUNS, FLEETS):
    d.mkdir(parents=True, exist_ok=True)

RESULTS_TABLE: list[tuple[str, int, str]] = []


def mkdir(p: Path) -> Path:
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True)
    return p


def w(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def run(name: str, tree: Path, fleet: Path = FLEET) -> tuple[int, str]:
    env = dict(os.environ, TMPDIR=str(S))
    cmd = [sys.executable, "-B", str(COUNTER), "--root", str(tree), "--fleet", str(fleet)]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(S))
    receipt = (f"$ {' '.join(cmd)}\n"
               f"exit={p.returncode}\n--- stdout\n{p.stdout}--- stderr\n{p.stderr}")
    w(RUNS / f"{name}.txt", receipt)
    RESULTS_TABLE.append((name, p.returncode, p.stdout.strip().splitlines()[-1]
                          if p.stdout.strip() else ""))
    return p.returncode, p.stdout


def fleet_removed(fleet: Path = FLEET) -> list[str]:
    p = subprocess.run(["git", "-C", str(fleet), "diff",
                        "cb02b70551f14ac3dea7eadebac22cb2cdc45c10",
                        "7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca",
                        "--", ".ufo/reports/round-81/kake.md"],
                       capture_output=True, text=True, check=False)
    return [ln[1:] for ln in p.stdout.splitlines()
            if ln.startswith("-") and not ln.startswith("---") and len(ln) > 41]


def lesson(lines: list[str]) -> str:
    return "# round 83 C1 attack fixture (seats: none, work: none)\n\n" + "\n".join(lines) + "\n"


# ---------------------------------------------------------------- item builders

D1_NAMES = ["RevA", "RevB", "ExecA", "ExecB", "ExecC", "ExecD", "ExecE", "ExecF"]
D1_ROLES = {"RevA": "reviewer", "RevB": "critic"}


def d1_artifacts(tree: Path, outputs: dict[str, str] | None = None,
                 account_settled: int | None = None,
                 account_seats: list[dict] | None = None,
                 spec_names: list[str] | None = None) -> None:
    names = spec_names if spec_names is not None else D1_NAMES
    outs = outputs if outputs is not None else {n: "x" for n in names}
    w(tree / SPEC, json.dumps({"items": [
        {"name": n, "role": D1_ROLES.get(n, "executor")} for n in names]}))
    w(tree / RESULTS, json.dumps({"results": [
        {"name": n, "output": outs.get(n, "")} for n in names]}))
    settled_names = sorted(n for n in names if len(outs.get(n, "").encode()) > 0)
    done = [n for n in names if len(outs.get(n, "").encode()) > 0]
    attack = [n for n in done if D1_ROLES.get(n, "executor") in
              ("reviewer", "critic", "mutation-tester", "labrat")]
    derived_settled = len(done) if account_settled is None else account_settled
    derived_attack = len(attack)
    share = round(derived_attack / derived_settled, 4) if derived_settled else 0.0
    seats = account_seats if account_seats is not None else [
        {"name": n, "role": D1_ROLES.get(n, "executor"),
         "output_bytes": len(outs.get(n, "").encode())} for n in names]
    w(tree / ACCOUNTING, json.dumps({
        "bytes_basis": "utf-8", "settled": derived_settled,
        "settled_names": settled_names, "settled_attack": derived_attack,
        "settled_share": share, "seats": seats}))


def d2_artifacts(tree: Path, results_obj, accounting_obj) -> None:
    w(tree / SPEC, json.dumps({"items": [{"name": "ExecA", "role": "executor"}]}))
    w(tree / RESULTS, json.dumps(results_obj) if isinstance(results_obj, (dict, list))
      else results_obj)
    w(tree / ACCOUNTING, json.dumps(accounting_obj))


def d3_artifacts(tree: Path, receipt_text: str) -> None:
    w(tree / RECEIPT, receipt_text)


def d4_artifacts(tree: Path, quoted: list[str], prefix: str = "7678247a") -> None:
    body = ["**D4 — erratum.** commit `" + prefix + "` removed the superseded lines; quoted raw:"]
    body += ["> " + q for q in quoted]
    w(tree / LESSON, lesson(body))


def d5_artifacts(tree: Path, runner_text: str, log_line: str | None = None) -> None:
    w(tree / KILLER, runner_text)
    line = log_line if log_line is not None else (
        "**D5 — killers.** distinguished=5/5 over C1-m3 C1-m5 C2-m2 C2-m4 C2-m5.")
    w(tree / LESSON, lesson([line]))


def d6_artifacts(tree: Path, criterion: str | None = None) -> None:
    crit = criterion if criterion is not None else (
        "- A Gate summary must cite the lesson it summarises "
        "(`corpus/lessons/round-82.md` §Gate); rule applies from `round-83`.")
    w(tree / QUALITY, "# QUALITY\n\n" + crit + "\n")
    w(tree / LESSON, lesson(["**D6 — provenance.** §Gate rule lands in corpus/QUALITY.md."]))


# ---------------------------------------------------------------- probes

def build_per_item() -> None:
    t = mkdir(TREES / "d1-only")
    d1_artifacts(t)
    w(t / LESSON, lesson([
        "**D1 — attack floor.** Prior run read 0/7 attack seats; "
        "settled_attack=2 of 8 (1-byte outputs each)."]))
    run("d1-only", t)

    t = mkdir(TREES / "d2-only")
    d2_artifacts(t, {"results": []},
                 {"bytes_basis": "utf-8", "settled": 0, "settled_names": [],
                  "settled_attack": 0, "settled_share": 0.0, "seats": []})
    w(t / LESSON, lesson(["**D2 — units.** UTF-8 byte counts re-derived from "
                          "w1-accounting.json; zero seats settled."]))
    run("d2-only", t)

    t = mkdir(TREES / "d3-only")
    d3_artifacts(t, "C2v1 revision=" + "a" * 40 +
                 " population=30 bound=30 mismatches=0 met=true\n")
    w(t / LESSON, lesson(["**D3 — instrument.** controls/after-c83-instrument-check.txt "
                          "carries the --check line."]))
    run("d3-only", t)

    t = mkdir(TREES / "d4-only")
    d4_artifacts(t, fleet_removed()[:4])
    run("d4-only", t)

    t = mkdir(TREES / "d5-only")
    d5_artifacts(t, "print('C1-m3 killed')\nprint('C1-m5 killed')\nprint('C2-m2 killed')\n"
                    "print('C2-m4 killed')\nprint('C2-m5 killed')\n"
                    "print('distinguished=5/5')\n")
    run("d5-only", t)

    t = mkdir(TREES / "d6-only")
    d6_artifacts(t)
    run("d6-only", t)

    # union of the six cheapest trees
    t = mkdir(TREES / "all-cheapest")
    d1_artifacts(t)
    d3_artifacts(t, "C2v1 revision=" + "a" * 40 +
                 " population=30 bound=30 mismatches=0 met=true\n")
    d5_artifacts(t, "print('C1-m3 killed')\nprint('C1-m5 killed')\nprint('C2-m2 killed')\n"
                    "print('C2-m4 killed')\nprint('C2-m5 killed')\n"
                    "print('distinguished=5/5')\n")
    w(t / QUALITY, "# QUALITY\n\n- A Gate summary must cite the lesson it summarises "
                   "(`corpus/lessons/round-82.md` §Gate); rule applies from `round-83`.\n")
    w(t / LESSON, lesson([
        "**D1 — attack floor.** Prior run read 0/7 attack seats; "
        "settled_attack=2 of 8; every output is the one byte `x`.",
        "**D2 — units.** UTF-8 byte counts re-derived from w1-accounting.json.",
        "**D3 — instrument.** controls/after-c83-instrument-check.txt, `--check` line.",
        "**D4 — erratum.** commit `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` removed "
        "the superseded lines; quoted raw:",
        *["> " + q for q in fleet_removed()[:4]],
        "**D5 — killers.** distinguished=5/5 over C1-m3 C1-m5 C2-m2 C2-m4 C2-m5; "
        "no fixture was executed.",
        "**D6 — provenance.** §Gate rule lands in corpus/QUALITY.md.",
    ]))
    run("all-cheapest", t)


def build_item2_probes() -> None:
    # (a) accounting numbers "right" (settled=0) but results rows empty
    t = mkdir(TREES / "a-empty-results")
    t0 = TREES / "a-empty-results" / "dummy"
    # empty results list
    w(t / SPEC, json.dumps({"items": [{"name": n, "role": D1_ROLES.get(n, "executor")}
                                      for n in D1_NAMES]}))
    w(t / RESULTS, json.dumps({"results": []}))
    w(t / ACCOUNTING, json.dumps({
        "bytes_basis": "utf-8", "settled": 0, "settled_names": [],
        "settled_attack": 0, "settled_share": 0.0, "seats": []}))
    w(t / LESSON, lesson(["**D2 — units.** UTF-8 byte counts re-derived from "
                          "w1-accounting.json; the wave delivered zero bytes."]))
    run("a-empty-results", t)

    # (a2) rows exist but all outputs empty; accounting echoes the requested 8 seats
    t = mkdir(TREES / "a-rows-empty-echo")
    d1_artifacts(t, outputs={n: "" for n in D1_NAMES},
                 account_settled=8,
                 account_seats=[{"name": n, "role": D1_ROLES.get(n, "executor"),
                                 "output_bytes": 0} for n in D1_NAMES])
    w(t / LESSON, lesson(["**D2 — units.** UTF-8 byte counts from w1-accounting.json; "
                          "eight seats, zero bytes each."]))
    run("a-rows-empty-echo", t)

    # (b) killer prints distinguished=5/5, runs nothing; no fixture names at all
    t = mkdir(TREES / "b-killer-print-only")
    d5_artifacts(t, "print('C1-m3 killed')\nprint('C1-m5 killed')\nprint('C2-m2 killed')\n"
                    "print('C2-m4 killed')\nprint('C2-m5 killed')\n"
                    "print('distinguished=5/5')\n")
    run("b-killer-print-only", t)

    # (b2) all five rows "equivalent" with no guarding source line printed
    t = mkdir(TREES / "b-killer-equivalent-no-guard")
    d5_artifacts(t, "for n in ['C1-m3','C1-m5','C2-m2','C2-m4','C2-m5']:\n"
                    "    print(n, 'equivalent')\nprint('distinguished=5/5')\n")
    run("b-killer-equivalent-no-guard", t)

    # (c) erratum quotes four lines from a different report
    other_report = FLEET / ".ufo/reports/round-82/kake.md"
    other_lines = [ln for ln in other_report.read_text(encoding="utf-8").splitlines()
                   if len(ln) >= 41][:4]
    t = mkdir(TREES / "c-erratum-other-report")
    w(t / LESSON, lesson([
        "**D4 — erratum.** commit `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` erratum; "
        "quoted raw:",
        *["> " + q for q in other_lines]]))
    w(RUNS / "c-erratum-other-report-quoted-source.txt",
      "quoted from: " + str(other_report) + "\n" + "\n".join(other_lines) + "\n")
    run("c-erratum-other-report", t)

    # (d) D3: revision field is not 40 hex but a 40-hex token appears elsewhere
    t = mkdir(TREES / "d3-revision-short")
    d3_artifacts(t, "C2v1 revision=abc population=30 bound=30 mismatches=0 met=true note="
                 + "f" * 40 + "\n")
    w(t / LESSON, lesson(["**D3 — instrument.** controls/after-c83-instrument-check.txt "
                          "green from --check."]))
    run("d3-revision-short", t)

    # (d2) first C2v1 line red, second line green: first-line-wins
    t = mkdir(TREES / "d3-first-red")
    d3_artifacts(t, "C2v1 revision=" + "b" * 40 +
                 " population=30 bound=30 mismatches=2 met=false\n"
                 "C2v1 revision=" + "c" * 40 +
                 " population=30 bound=30 mismatches=0 met=true\n")
    w(t / LESSON, lesson(["**D3 — instrument.** controls/after-c83-instrument-check.txt "
                          "green from --check."]))
    run("d3-first-red", t)


def gitfleet(path: Path) -> Path:
    d = mkdir(path)
    subprocess.run(["git", "-C", str(d), "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert Path(top).resolve() == d.resolve(), (top, d)
    return d


def commit(d: Path, msg: str, rel: str) -> str:
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
    subprocess.run(["git", "-C", str(d), "add", rel], check=True)
    subprocess.run(["git", "-C", str(d), *ident, "commit", "-q", "-m", msg], check=True)
    return subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()


def write_report(d: Path, lines: list[str]) -> None:
    w(d / ".ufo/reports/round-81/kake.md", "\n".join(lines) + "\n")


def build_d4_fleets() -> None:
    L = [f"fixture report line {i}: " + "x" * 44 for i in range(1, 9)]

    # two commits: filed then amended (removes L1..L5)
    d = gitfleet(FLEETS / "fleet-two")
    write_report(d, L)
    identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
    subprocess.run(["git", "-C", str(d), "add", ".ufo/reports/round-81/kake.md"], check=True)
    subprocess.run(["git", "-C", str(d), *identity, "commit", "-q", "-m", "filed"], check=True)
    removed = L[:5]
    write_report(d, L[5:] + ["amended replacement line " + "y" * 40])
    c2 = commit(d, "amended", ".ufo/reports/round-81/kake.md")
    t = mkdir(TREES / "fleet-two")
    d4_artifacts(t, removed[:4], prefix=c2[:8])
    run("fleet-two", t, fleet=d)

    # later append-only touch: counter retargets to the later commit, removed=0
    d2 = gitfleet(FLEETS / "fleet-later-append")
    write_report(d2, L[:4])
    subprocess.run(["git", "-C", str(d2), "add", ".ufo/reports/round-81/kake.md"], check=True)
    subprocess.run(["git", "-C", str(d2), *identity, "commit", "-q", "-m", "filed"], check=True)
    c_amend = "z" * 8  # placeholder, replaced below
    write_report(d2, ["amended line " + "w" * 40])
    c2 = commit(d2, "amended", ".ufo/reports/round-81/kake.md")
    write_report(d2, ["amended line " + "w" * 40,
                      "post-amendment note appended to the report body " + "v" * 20])
    c3 = commit(d2, "later touch", ".ufo/reports/round-81/kake.md")
    t = mkdir(TREES / "fleet-later-append-contract-prefix")
    d4_artifacts(t, [ln for ln in L[:4] if len("-"+ln) > 41][:4], prefix="7678247a")
    run("fleet-later-append-contract-prefix", t, fleet=d2)
    t = mkdir(TREES / "fleet-later-append-later-prefix")
    d4_artifacts(t, [ln for ln in L[:4] if len("-"+ln) > 41][:4], prefix=c3[:8])
    run("fleet-later-append-later-prefix", t, fleet=d2)
    w(RUNS / "fleet-later-append-commits.txt",
      f"amend={c2}\nlater={c3}\n" + "\n".join([c2, c3]))

    # later commit that removes four other long lines: counter accepts it
    d3 = gitfleet(FLEETS / "fleet-later-remove")
    write_report(d3, L)
    subprocess.run(["git", "-C", str(d3), "add", ".ufo/reports/round-81/kake.md"], check=True)
    subprocess.run(["git", "-C", str(d3), *identity, "commit", "-q", "-m", "filed"], check=True)
    write_report(d3, L[5:] + ["amended replacement line " + "y" * 40])
    c2 = commit(d3, "amended", ".ufo/reports/round-81/kake.md")
    later_removed = L[5:] + ["amended replacement line " + "y" * 40]
    write_report(d3, ["unrelated later rewrite " + "u" * 40])
    c3 = commit(d3, "unrelated later rewrite", ".ufo/reports/round-81/kake.md")
    t = mkdir(TREES / "fleet-later-remove")
    d4_artifacts(t, later_removed[:4], prefix=c3[:8])
    run("fleet-later-remove", t, fleet=d3)
    w(RUNS / "fleet-later-remove-commits.txt",
      f"amend={c2}\nlater={c3}\nlater-removed={json.dumps(later_removed)}\n")

    # off-by-one: four removed lines of exactly 40 chars never qualify
    d4 = gitfleet(FLEETS / "fleet-len40")
    short = [f"len40 line {i}: " + "q" * 26 for i in range(1, 5)]
    assert all(len(s) == 40 for s in short), [len(s) for s in short]
    long_line = "len41-plus line: " + "r" * 40
    write_report(d4, short + [long_line])
    subprocess.run(["git", "-C", str(d4), "add", ".ufo/reports/round-81/kake.md"], check=True)
    subprocess.run(["git", "-C", str(d4), *identity, "commit", "-q", "-m", "filed"], check=True)
    write_report(d4, ["kept after removal"])
    c2 = commit(d4, "amended", ".ufo/reports/round-81/kake.md")
    t = mkdir(TREES / "fleet-len40")
    d4_artifacts(t, short + [long_line], prefix=c2[:8])
    run("fleet-len40", t, fleet=d4)

    # one commit / zero commits / non-git
    d5 = gitfleet(FLEETS / "fleet-one")
    write_report(d5, L[:2])
    subprocess.run(["git", "-C", str(d5), "add", ".ufo/reports/round-81/kake.md"], check=True)
    subprocess.run(["git", "-C", str(d5), *identity, "commit", "-q", "-m", "only"], check=True)
    t = mkdir(TREES / "fleet-one")
    d4_artifacts(t, [ln for ln in L if len("-"+ln) > 41][:4], prefix="7678247a")
    run("fleet-one", t, fleet=d5)

    d6 = gitfleet(FLEETS / "fleet-none")
    w(d6 / "unrelated.txt", "no report here\n")
    subprocess.run(["git", "-C", str(d6), "add", "unrelated.txt"], check=True)
    subprocess.run(["git", "-C", str(d6), *identity, "commit", "-q", "-m", "unrelated"],
                   check=True)
    t = mkdir(TREES / "fleet-none")
    d4_artifacts(t, fleet_removed()[:4])
    run("fleet-none", t, fleet=d6)

    d7 = mkdir(FLEETS / "fleet-nongit")
    w(d7 / "notes.txt", "not a repository\n")
    t = mkdir(TREES / "fleet-nongit")
    d4_artifacts(t, fleet_removed()[:4])
    run("fleet-nongit", t, fleet=d7)


def build_d1_arithmetic() -> None:
    # exactly 2 attack / 8 settled = 0.25 with 1-byte outputs
    t = mkdir(TREES / "d1-share-025")
    d1_artifacts(t, outputs={n: "x" for n in D1_NAMES})
    w(t / LESSON, lesson([
        "**D1 — attack floor.** 0/7 historical; settled_attack=2 of 8, each output one byte."]))
    run("d1-share-025", t)

    # 1 attack seat: below the floor even at 1/4
    t = mkdir(TREES / "d1-share-below")
    names4 = ["RevA", "ExecA", "ExecB", "ExecC"]
    d1_artifacts(t, outputs={n: "x" for n in names4}, spec_names=names4)
    w(t / LESSON, lesson([
        "**D1 — attack floor.** 0/7 historical; settled_attack=1 of 4."]))
    run("d1-share-below", t)

    # dead requested seats cost nothing: 4 requested seats held empty, 8 settled at 0.25
    t = mkdir(TREES / "d1-dead-seats-free")
    names = D1_NAMES + ["DeadRev", "DeadCrit", "DeadMut", "DeadLab"]
    roles = {"RevA": "reviewer", "RevB": "critic", "DeadRev": "reviewer",
             "DeadCrit": "critic", "DeadMut": "mutation-tester", "DeadLab": "labrat"}
    w(t / SPEC, json.dumps({"items": [
        {"name": n, "role": roles.get(n, "executor")} for n in names]}))
    w(t / RESULTS, json.dumps({"results": [
        {"name": n, "output": ("x" if n in D1_NAMES else "")} for n in names]}))
    w(t / ACCOUNTING, json.dumps({
        "bytes_basis": "utf-8", "settled": 8, "settled_names": sorted(D1_NAMES),
        "settled_attack": 2, "settled_share": 0.25,
        "seats": [{"name": n, "role": roles.get(n, "executor"),
                   "output_bytes": (1 if n in D1_NAMES else 0)} for n in names]}))
    w(t / LESSON, lesson([
        "**D1 — attack floor.** 0/7 historical; 12 requested, 8 settled, "
        "settled_attack=2, four attack seats dead and uncounted."]))
    run("d1-dead-seats-free", t)


def main() -> int:
    # harness self-check: reproduce the committed junk control
    junk = mkdir(S / "junk")
    subprocess.run([sys.executable, "-B", str(LANE / ".ufo/waves/round-83/junk_tree_build.py"),
                    "--root", str(junk)], check=True, capture_output=True)
    run("junk-control-repro", junk)

    build_per_item()
    build_item2_probes()
    build_d4_fleets()
    build_d1_arithmetic()

    print("name | exit | last stdout line")
    for name, rc, last in RESULTS_TABLE:
        print(f"{name} | {rc} | {last}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
