#!/usr/bin/env python3
"""Round-59 C1 labrat, second pass: probes on receipt provenance and SCORECARD round sections."""
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
OUT = os.path.join(SCRATCH, "runs2")
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

AFTER_R59 = ("C1 axis-evidence mismatches=0 unresolved=0 rows_no_receipt=0 receipts_off_axis=0 "
             "tallies_unfound=0 rows_no_tally=0 rows=3 scores_held=2 superseded_kept=3 met=True\n"
             "  rows scored 3/3 OK\nEXIT=0\n")


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


R59_AFTER_CELLS = {
    "operability": ("`.ufo/waves/round-59/controls/after-c1-axis-evidence.txt` "
                    "round-59 C1 after-receipt; rows scored 3/3."),
    "freshness": ("`.ufo/waves/round-59/controls/after-c1-axis-evidence.txt` "
                  "round-59 C1 after-receipt; rows scored 3/3."),
    "calibration": ("`.ufo/waves/round-59/controls/after-c1-axis-evidence.txt` "
                    "round-59 C1 after-receipt; rows scored 3/3."),
}

R59_BASE_CELLS = {
    "operability": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                    "round-59 base receipt; rows 3/3."),
    "freshness": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                  "round-59 base receipt; rows 3/3."),
    "calibration": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                    "round-59 base receipt; rows 3/3."),
}

# off-axis receipt alone (no on-axis receipt in the same cell)
E2_CELLS = {
    "operability": ("`.ufo/waves/round-53/exec-quality-gate/selftest.txt` "
                    "round-53 gate selftest 17/17."),
    "freshness": ("`.ufo/waves/round-54/controls/after-c1-s374.txt` "
                  "round-54 C1 after-receipt; calibration mismatches 0/0."),
    "calibration": ("`.ufo/waves/round-53/exec-quality-gate/selftest.txt` "
                    "round-53 gate selftest 17/17."),
}

CONTROLS = [
    # name, cells, section, extra files
    ("i-r59-after-receipt-with-r59-section", R59_AFTER_CELLS, R59_SECTION,
     {".ufo/waves/round-59/controls/after-c1-axis-evidence.txt": AFTER_R59}),
    ("j-r59-after-receipt-no-r59-section", R59_AFTER_CELLS, None,
     {".ufo/waves/round-59/controls/after-c1-axis-evidence.txt": AFTER_R59}),
    ("k-r59-base-receipt-with-r59-section", R59_BASE_CELLS, R59_SECTION, {}),
    ("l-off-axis-receipt-only", E2_CELLS, None, {}),
    ("m-r59-after-receipt-section-not-naming-axis", {
        ax: ("`.ufo/waves/round-59/controls/after-c1-axis-evidence.txt` "
             "round-59 C1 after-receipt; rows scored 3/3.") for ax in
        ("operability", "freshness", "calibration")},
     "\n## Round 59 - declared and measured claims\n\n| Claim | Verdict |\n|---|---|\n"
     "| C1 axis-table evidence | pending |\n", {".ufo/waves/round-59/controls/after-c1-axis-evidence.txt": AFTER_R59}),
]


def main():
    print("counter sha256:", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
    results = {}
    for name, cells, section, files in CONTROLS:
        git("checkout", "-q", "-B", "labrat-c1-controls2", CONTRACT_COMMIT)
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
