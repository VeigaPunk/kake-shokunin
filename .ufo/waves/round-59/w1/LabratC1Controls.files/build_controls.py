#!/usr/bin/env python3
"""Round-59 C1 labrat: build scored control states in a scratch clone and record --json runs.

Every control is its own commit on top of the contract commit 45a92b64 in
/fast/scratch/hyaku/kake-r59/LabratC1Controls/lane (a `git clone --shared` of the lane).
The lane repo is never mutated. The counter is the frozen v1 file committed at 45a92b64
(sha256 95d2351...), run with --base fd6303ce (the round-59 base).
"""
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
OUT = os.path.join(SCRATCH, "runs")
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location("c59", COUNTER)
c59 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c59)


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout.decode()


def scorecard_at(rev):
    return git("show", f"{rev}:SCORECARD.md")


BASE_TEXT = scorecard_at(BASE)
BASE_ROWS, _ = c59.axis_table(BASE_TEXT)
BASE_CELLS = {c[0].lower(): c[2] for _, c, _ in BASE_ROWS}

# --- claimed (minimal-true) cells: one on-axis receipt + one tally that occurs in it -------------
SHELL = {
    "operability": ("`.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` "
                    "round-58 C2 after-receipt; resolver cases 14/14 met."),
    "freshness":   ("`.ufo/waves/round-58/controls/after-c3-quote-truth.txt` "
                    "round-58 C3 after-receipt; quote-truth conditions 8/8 met."),
    "calibration": ("`.ufo/waves/round-56/controls/after-c1-selftally.txt` "
                    "round-56 C1 after-receipt; wave-evidence-ledger observed 19/19."),
}

SUPERSEDED = (
    "\n## Superseded axis cells (base revision %s, kept verbatim)\n\n"
    % BASE[:12]
    + "operability:\n\n" + BASE_CELLS["operability"] + "\n\n"
    + "freshness:\n\n" + BASE_CELLS["freshness"] + "\n\n"
    + "calibration:\n\n" + BASE_CELLS["calibration"] + "\n"
)


def build_text(cells, append_superseded=True):
    """Rewrite the evidence cell of each axis row; optionally append the base cells verbatim."""
    lines = scorecard_at(CONTRACT_COMMIT).split("\n")
    rows, _ = c59.axis_table("\n".join(lines))
    out = list(lines)
    for idx, row, _raw in rows:
        out[idx] = "| %s | %s | %s | %s |" % (row[0], row[1], cells[row[0].lower()], row[3])
    text = "\n".join(out)
    return text + SUPERSEDED if append_superseded else text


# --- controls -------------------------------------------------------------------------------
# (b) emptied evidence cells
B_CELLS = {a: "" for a in ("operability", "freshness", "calibration")}

# (c) one random existing lane file path each (not a receipt)
C_CELLS = {
    "operability": "`corpus/knowledge/free-read-verbs.md`",
    "freshness": "`corpus/knowledge/freshness-sweep.md`",
    "calibration": "`corpus/knowledge/receipt-integrity.md`",
}

# (d) on-axis receipt + fabricated tally 99/99
D_CELLS = {
    "operability": ("`.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` "
                    "round-58 C2 after-receipt; resolver cases 99/99 met."),
    "freshness": ("`.ufo/waves/round-58/controls/after-c3-quote-truth.txt` "
                  "round-58 C3 after-receipt; quote-truth conditions 99/99 met."),
    "calibration": ("`.ufo/waves/round-56/controls/after-c1-selftally.txt` "
                    "round-56 C1 after-receipt; wave-evidence-ledger observed 99/99."),
}

# (e) correct-looking cells that ALSO cite a receipt of a round with no claim on that axis
#     (round 53 is on-axis for freshness only; round 54 for operability+calibration only)
E_CELLS = {
    "operability": ("`.ufo/waves/round-53/exec-quality-gate/selftest.txt` round-53 gate selftest, "
                    "plus `.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` "
                    "round-58 C2 after-receipt; resolver cases 14/14 met."),
    "freshness": ("`.ufo/waves/round-54/controls/after-c1-s374.txt` round-54 C1 after-receipt, "
                  "plus `.ufo/waves/round-58/controls/after-c3-quote-truth.txt` "
                  "round-58 C3 after-receipt; quote-truth conditions 8/8 met."),
    "calibration": ("`.ufo/waves/round-53/exec-quality-gate/selftest.txt` round-53 gate selftest, "
                    "plus `.ufo/waves/round-56/controls/after-c1-selftally.txt` "
                    "round-56 C1 after-receipt; wave-evidence-ledger observed 19/19."),
}

# (h) extra: cell cites a NON-receipt blob that merely lives under .ufo/waves/round-58/
H_CELLS = {
    "operability": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` "
                    "round-58 scorecard mirror; snapshot holds 117/117."),
    "freshness": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` "
                  "round-58 scorecard mirror; snapshot holds 117/117."),
    "calibration": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` "
                    "round-58 scorecard mirror; snapshot holds 117/117."),
}

# (c2) extra: random lane file PLUS a tally that occurs in it -> isolates the receipt dimension
C2_CELLS = {
    "operability": "`corpus/knowledge/free-read-verbs.md` holds 18/21",
    "freshness": "`corpus/knowledge/freshness-sweep.md` holds 60/60",
    "calibration": "`corpus/knowledge/receipt-integrity.md` holds 27/27",
}

# (i)/(j): round-59 receipts (the shape a real build would use), with and without a
# `## Round 59` SCORECARD section naming the axes.
R59_CELLS = {
    "operability": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                    "round-59 base receipt; rows checked 3/3."),
    "freshness": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                  "round-59 base receipt; rows checked 3/3."),
    "calibration": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` "
                    "round-59 base receipt; rows checked 3/3."),
}

R59_SECTION = """
## Round 59 - declared and measured claims

| Claim | Axis | Before -> after | Verdict |
|---|---|---|---|
| C1 axis-table evidence | operability | pending | pending |
| C1 axis-table evidence | freshness | pending | pending |
| C1 axis-table evidence | calibration | pending | pending |
"""


CONTROLS = [
    ("a-do-nothing", None, False),
    ("b-emptied-cells", B_CELLS, True),
    ("b-emptied-cells-noappend", B_CELLS, False),
    ("c-random-lane-file", C_CELLS, True),
    ("c-random-lane-file-noappend", C_CELLS, False),
    ("c2-random-lane-file-with-tally", C2_CELLS, True),
    ("d-fabricated-tally", D_CELLS, True),
    ("d-fabricated-tally-noappend", D_CELLS, False),
    ("e-off-axis-receipt", E_CELLS, True),
    ("e-off-axis-receipt-noappend", E_CELLS, False),
    ("f-minimal-true", SHELL, True),
    ("g-minimal-true-no-append", SHELL, False),
    ("h-nonreceipt-blob-under-round-dir", H_CELLS, True),
    ("i-r59-receipt-with-r59-section", R59_CELLS, True),
    ("j-r59-receipt-without-r59-section", R59_CELLS, True),
]


def main():
    print("counter sha256:", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
    git("checkout", "-q", "-B", "labrat-c1-controls", CONTRACT_COMMIT)
    top = git("rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(REPO), top
    results = {}
    for name, cells, append in CONTROLS:
        git("checkout", "-q", "-B", "labrat-c1-controls", CONTRACT_COMMIT)
        git("checkout", "-q", "--", "SCORECARD.md")
        text = scorecard_at(CONTRACT_COMMIT) if cells is None else build_text(cells, append)
        with open(os.path.join(REPO, "SCORECARD.md"), "w") as fh:
            fh.write(text)
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
