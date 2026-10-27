#!/usr/bin/env python3
"""Round-59 C1 labrat, third pass: probe the receipt/tally/on-axis atoms of counter v1."""
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
OUT = os.path.join(SCRATCH, "runs3")
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


# n: receipt cited for provenance, but the TALLY lives in a different cited blob (unrelated lane file)
N_CELLS = {
    "operability": ("`.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` round-58 C2 receipt "
                    "plus `corpus/knowledge/free-read-verbs.md` free-read tally 18/21."),
    "freshness": ("`.ufo/waves/round-58/controls/after-c3-quote-truth.txt` round-58 C3 receipt "
                  "plus `corpus/knowledge/freshness-sweep.md` sweep tally 60/60."),
    "calibration": ("`.ufo/waves/round-56/controls/after-c1-selftally.txt` round-56 C1 receipt "
                    "plus `corpus/knowledge/receipt-integrity.md` ledger tally 27/27."),
}

# o: the round-59 BASE control receipt (which documents mismatches=16, the FAILING base)
#    cited as evidence, with a Round 59 section naming all three axes
O_CELLS = {
    "operability": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                    "receipt; rows 3/3."),
    "freshness": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                  "receipt; rows 3/3."),
    "calibration": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                    "receipt; rows 3/3."),
}

# p: the round-59 base receipt with a tally that IS present in it (16/16), Round 59 section present
P_CELLS = {
    "operability": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                    "receipt; unresolved 16/16."),
    "freshness": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                  "receipt; unresolved 16/16."),
    "calibration": ("`.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` round-59 C1 base "
                    "receipt; unresolved 16/16."),
}

# q: cite a non-receipt mirror of the scorecard under round-58 (already met) but with a tally
#    that is NOT in that blob -> isolates the tally atom from the receipt atom
Q_CELLS = {
    "operability": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` round-58 mirror "
                    "holds 12/12."),
    "freshness": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` round-58 mirror "
                  "holds 12/12."),
    "calibration": ("`.ufo/waves/round-58/assimilation/validate/SCORECARD.md` round-58 mirror "
                    "holds 12/12."),
}

CONTROLS = [
    ("n-tally-from-unrelated-blob", N_CELLS, None, {}),
    ("o-r59-base-receipt-rows-3-3", O_CELLS, R59_SECTION, {}),
    ("p-r59-base-receipt-tally-16-16", P_CELLS, R59_SECTION, {}),
    ("q-mirror-receipt-bad-tally", Q_CELLS, None, {}),
]


def main():
    print("counter sha256:", hashlib.sha256(open(COUNTER, "rb").read()).hexdigest())
    results = {}
    for name, cells, section, files in CONTROLS:
        git("checkout", "-q", "-B", "labrat-c1-controls3", CONTRACT_COMMIT)
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
