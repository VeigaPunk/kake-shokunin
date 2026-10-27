#!/usr/bin/env python3
"""Round-59 C1 labrat, fourth pass: how cheap can a TRUE green be?"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r59/LabratC1Controls"
REPO = os.path.join(SCRATCH, "lane")
COUNTER = os.path.join(REPO, ".ufo/waves/round-59/c59_axis_evidence.py")
CONTRACT_COMMIT = "45a92b64ac8a0f82dba369100e30682f14de81fb"
BASE = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
OUT = os.path.join(SCRATCH, "runs4")
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location("c59", COUNTER)
c59 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c59)


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout.decode()


def scorecard_at(rev):
    return git("show", f"{rev}:SCORECARD.md")


BASE_ROWS, _ = c59.axis_table(scorecard_at(BASE))
BASE_CELLS = {c[0].lower(): c[2] for _, c, _ in BASE_ROWS}

SUPERSEDED = (
    "\n## Superseded axis cells (base revision %s, kept verbatim)\n\n"
    % BASE[:12]
    + "operability:\n\n" + BASE_CELLS["operability"] + "\n\n"
    + "freshness:\n\n" + BASE_CELLS["freshness"] + "\n\n"
    + "calibration:\n\n" + BASE_CELLS["calibration"] + "\n"
)

R59_SECTION = """
## Round 59 - declared and measured claims

| Claim | Axis | Before -> after | Verdict |
|---|---|---|---|
| C1 axis-table evidence | operability | pending | pending |
| C1 axis-table evidence | freshness | pending | pending |
| C1 axis-table evidence | calibration | pending | pending |
"""


def build_text(cells, section=None, append_superseded=True):
    lines = scorecard_at(CONTRACT_COMMIT).split("\n")
    rows, _ = c59.axis_table("\n".join(lines))
    out = list(lines)
    for idx, row, _raw in rows:
        out[idx] = "| %s | %s | %s | %s |" % (row[0], row[1], cells[row[0].lower()], row[3])
    text = "\n".join(out)
    if section:
        text += section
    if append_superseded:
        text += SUPERSEDED
    return text


def same(cell):
    return {ax: cell for ax in ("operability", "freshness", "calibration")}


CONTROLS = [
    # r: the round-59 FROZEN CONTRACT (not a measurement receipt) cited as the round-59 receipt
    ("r-r59-contract-as-receipt", same(
        "`.ufo/waves/round-59/contract.md` round-59 frozen contract; counter 21/21 cases."),
     R59_SECTION, {}),
    # s: a round-58 wave seat report (not a receipt) cited as the receipt
    ("s-r58-seat-report-as-receipt", same(
        "`.ufo/waves/round-58/w1/ReviewerC2Evidence.md` round-58 reviewer note; tally 12/12."),
     None, {}),
    # t: the counter's own source (not a receipt) cited as the receipt
    ("t-counter-source-as-receipt", same(
        "`.ufo/waves/round-59/c59_axis_evidence.py` round-59 counter source; predicate 21/21."),
     R59_SECTION, {}),
]


def main():
    print("counter sha256:", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
    results = {}
    for name, cells, section, files in CONTROLS:
        git("checkout", "-q", "-B", "labrat-c1-controls4", CONTRACT_COMMIT)
        git("clean", "-qfd")
        with open(os.path.join(REPO, "SCORECARD.md"), "w") as fh:
            fh.write(build_text(cells, section))
        for rel, body in files.items():
            path = os.path.join(REPO, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as fh:
                fh.write(body)
        git("add", "-A")
        git("-c", "user.name=selftest", "-c", "user.email=selftest@local",
            "commit", "-q", "--allow-empty", "-m", "labrat control %s" % name)
        rev = git("rev-parse", "HEAD").strip()
        p = subprocess.run([sys.executable, "-B", COUNTER, "--root", REPO, "--revision", rev,
                            "--base", BASE, "--json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.decode()
        payload = json.loads(out) if out.strip().startswith("{") else {"raw": out, "err": p.stderr.decode()}
        payload["_control"] = name
        payload["_commit"] = rev
        payload["_exit_code"] = p.returncode
        with open(os.path.join(OUT, name + ".json"), "w") as fh:
            json.dump(payload, fh, indent=1, ensure_ascii=False)
        results[name] = {
            "commit": rev[:12], "exit": p.returncode, "met": payload.get("met"),
            "mismatches": payload.get("mismatches"), "unresolved": payload.get("unresolved"),
            "rows_no_receipt": payload.get("rows_no_receipt"),
            "receipts_off_axis": payload.get("receipts_off_axis"),
            "tallies_unfound": payload.get("tallies_unfound"),
            "rows_no_tally": payload.get("rows_no_tally"), "rows": payload.get("rows"),
            "scores_held": payload.get("scores_held"), "superseded_kept": payload.get("superseded_kept"),
        }
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
