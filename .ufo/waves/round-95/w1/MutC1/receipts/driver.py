#!/usr/bin/env python3
"""MutC1 probe driver: 16 rule-targeted mutants of the frozen C1 counter
(c95_selfassess.py sha256 8fd27d62..., frozen surfaces 00a04c9a...).

Runs entirely under /fast/scratch/hyaku/kake-r95/MutC1. The lane repo is only
ever READ by the counter through git (show/cat-file/ls-tree/rev-parse). Every
counter run is given --work inside the scratch tree.
"""
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

SCRATCH = "/fast/scratch/hyaku/kake-r95/MutC1"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ENV = os.path.join(SCRATCH, "env-r95")
COUNTER_REL = ".ufo/waves/round-95/c95_selfassess.py"
PRISTINE_PATH = os.path.join(ENV, COUNTER_REL)
BASE_REV = "fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3"
REC = os.path.join(SCRATCH, "receipts")
WORK = os.path.join(SCRATCH, "work")
TMP = os.path.join(SCRATCH, "tmp")
MUTDIR = os.path.join(SCRATCH, "mutants")
for d in (REC, WORK, TMP, MUTDIR):
    os.makedirs(d, exist_ok=True)

PRISTINE = open(PRISTINE_PATH, "rb").read().decode("utf-8")
PRISTINE_SHA = hashlib.sha256(PRISTINE.encode("utf-8")).hexdigest()
assert PRISTINE_SHA == ("8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15a"
                        "c03b193"), PRISTINE_SHA
SURF_SHA = hashlib.sha256(open(os.path.join(
    ENV, ".ufo/waves/round-95/frozen/c1-surfaces.json"), "rb").read()).hexdigest()
assert SURF_SHA == ("00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d"
                    "47b8"), SURF_SHA

# (id, rule class, find-string, replacement) -- one str.replace each; the
# driver asserts find occurs exactly once in the pristine bytes.
MUTANTS = [
    ("M01", "E1-heading",
     r'(?m)^## Gate\b[^\n]*$(.*?)(?=^## |\Z)',
     r'(?m)^## Gats\b[^\n]*$(.*?)(?=^## |\Z)'),
    ("M02", "E1-vacuity",
     'if len(nonempty) < 2:',
     'if len(nonempty) < 3:'),
    ("M03", "E1-vocabulary",
     're.search(r"admit", head_line, re.I)',
     're.search(r"adopt", head_line, re.I)'),
    ("M04", "E2-scope",
     'CRIT_RE.match(head)',
     'CRIT_RE.fullmatch(head)'),
    ("M05", "E2-blob",
     'elif meta[0] != "blob" or meta[1] <= 0:',
     'elif meta[0] != "blob" and meta[1] <= 0:'),
    ("M06", "E3-rowid",
     r'ROW_ID_RE = re.compile(r"^\|[ \t]*(S[0-9]{3,})[ \t]*\|")',
     r'ROW_ID_RE = re.compile(r"^\|[ \t]*(S[0-9]{4,})[ \t]*\|")'),
    ("M07", "E3-locator",
     'if TMP_LOCATOR_RE.search(line):',
     'if False and TMP_LOCATOR_RE.search(line):'),
    ("M08", "E3-multi-source",
     'if len(source_lines) > 1:',
     'if len(source_lines) > 2:'),
    ("M09", "E4-indent",
     r're.match(r"^[ \t]+\|", line)',
     r're.match(r"^\t+\|", line)'),
    ("M10", "E4-deletion",
     'and not mistakes:',
     'and mistakes is None:'),
    ("M11", "E5-suffix-strip",
     're.sub(r"#([^#]*)$", "", raw)',
     're.sub(r"#KEEP([^#]*)$", "", raw)'),
    ("M12", "E5-absence-open",
     r'\[r\d{2,}-absence(?![^\]]*\])',
     r'\[r\d{3,}-absence(?![^\]]*\])'),
    ("M13", "E5-symlink",
     'elif meta[2] == "120000":',
     'elif meta[2] == "120001":'),
    ("M14", "identity-path-tokens",
     'row_tokens.get(cell, 0) < item["path_tokens"]',
     'row_tokens.get(cell, 0) > item["path_tokens"]'),
    ("M15", "identity-content",
     'hashlib.sha256(text.encode("utf-8")).hexdigest() != item["sha256"]',
     'hashlib.sha256(text.encode("utf-8")).hexdigest() == item["sha256"]'),
    ("M16", "cardinality-short",
     'if pins[k] < v]',
     'if pins[k] <= v]'),
]

CLASS_FIELD = {
    "E1-heading": "E1", "E1-vacuity": "E1", "E1-vocabulary": "E1",
    "E2-scope": "E2", "E2-blob": "E2",
    "E3-rowid": "E3", "E3-locator": "E3", "E3-multi-source": "E3",
    "E4-indent": "E4", "E4-deletion": "E4",
    "E5-suffix-strip": "E5", "E5-absence-open": "E5", "E5-symlink": "E5",
    "identity-path-tokens": "pins", "identity-content": "pins",
    "cardinality-short": "pins",
}
BATTERY_FIELDS = ("battery", "admit", "shadow", "predecessor_admits", "met")
AUDIT_FIELDS = ("mismatches", "E1", "E2", "E3", "E4", "E5", "pins",
                "lessons", "entries", "rows", "criteria")

PY = sys.executable
BASE = {}


def run(cmd, timeout=900):
    env = dict(os.environ)
    env["TMPDIR"] = TMP
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONSTARTUP", None)
    p = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env,
                       cwd=SCRATCH)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


def counter_cmd(path, workdir):
    return [PY, "-B", path, "--root", LANE, "--revision", BASE_REV,
            "--work", workdir]


def norm(l1):
    l1 = re.sub(r"revision=[0-9a-f]{40}", "revision=<rev>", l1)
    l1 = re.sub(r"counter=[0-9a-f]{64}", "counter=<sha>", l1)
    return l1.strip()


def fields(l1):
    out = {}
    for tok in l1.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out


def stage_env(mid, mut):
    """Stage the mutant in a full side-tree: frozen/ surfaces sibling and the
    round-94 predecessor two dirs up, exactly like the lane layout, so
    load_surfaces() and predecessor_clean() resolve as in the real lane."""
    root = os.path.join(SCRATCH, "env-mut", mid, ".ufo", "waves")
    d95 = os.path.join(root, "round-95")
    os.makedirs(os.path.join(d95, "frozen"), exist_ok=True)
    os.makedirs(os.path.join(root, "round-94"), exist_ok=True)
    mpath = os.path.join(d95, "c95_selfassess.py")
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(mut)
    shutil.copyfile(os.path.join(ENV, ".ufo/waves/round-95/frozen/c1-surfaces.json"),
                    os.path.join(d95, "frozen", "c1-surfaces.json"))
    shutil.copyfile(os.path.join(ENV, ".ufo/waves/round-94/c94_selfassess.py"),
                    os.path.join(root, "round-94", "c94_selfassess.py"))
    return mpath


def baseline():
    rc, out, err = run(counter_cmd(PRISTINE_PATH, os.path.join(WORK, "baseline")))
    lines = out.splitlines()
    l1 = lines[0] if lines else ""
    with open(os.path.join(REC, "baseline.base.txt"), "w") as fh:
        fh.write("rc=%d\n%s\n%s%s" % (rc, l1, out, err))
    src, sout, serr = run([PY, "-B", PRISTINE_PATH, "--selftest"])
    with open(os.path.join(REC, "baseline.selftest.txt"), "w") as fh:
        fh.write("rc=%d\n%s%s" % (src, sout, serr))
    BASE["rc"] = rc
    BASE["line1"] = l1
    BASE["fields"] = fields(l1)
    BASE["selftest_rc"] = src
    BASE["selftest_tail"] = (sout.strip().splitlines() or [""])[-1]
    return BASE


def battery_receipt(mid, l1, out):
    toks = [t for t in l1.split() if t.split("=")[0] in
            ("battery", "admit", "shadow", "predecessor_admits", "met")]
    bat = ""
    if len(out.splitlines()) > 1:
        try:
            detail = json.loads(out.splitlines()[1])
            bat = json.dumps(detail.get("battery", {}), sort_keys=True)
        except Exception as exc:
            bat = "unparsed: %s" % exc
    with open(os.path.join(REC, mid + ".battery.txt"), "w") as fh:
        fh.write("line1 battery fields: %s\nbattery detail: %s\n" %
                 (" ".join(toks), bat[:4000]))


def probe(spec):
    mid, cls, find, replace = spec
    try:
        cnt = PRISTINE.count(find)
        if cnt != 1:
            return {"id": mid, "class": cls, "verdict": "SPEC-DEFECT",
                    "find_count": cnt}
        mut = PRISTINE.replace(find, replace, 1)
        mpath = stage_env(mid, mut)
        with open(os.path.join(MUTDIR, mid + ".py"), "w", encoding="utf-8") as fh:
            fh.write(mut)
        diff = "".join(difflib.unified_diff(
            PRISTINE.splitlines(True), mut.splitlines(True),
            fromfile="c95_selfassess.py (pristine 8fd27d62)", tofile=mid))
        with open(os.path.join(REC, mid + ".diff"), "w") as fh:
            fh.write(diff)
        msha = hashlib.sha256(mut.encode("utf-8")).hexdigest()

        src, sout, serr = run([PY, "-B", mpath, "--selftest"])
        with open(os.path.join(REC, mid + ".selftest.txt"), "w") as fh:
            fh.write("rc=%d\n%s%s" % (src, sout, serr))
        stail = (sout.strip().splitlines() or [""])[-1]

        rc, out, err = run(counter_cmd(mpath, os.path.join(WORK, mid)))
        lines = out.splitlines()
        l1 = lines[0] if lines else ""
        with open(os.path.join(REC, mid + ".base.txt"), "w") as fh:
            fh.write("rc=%d\n%s\n%s%s" % (rc, l1, out, err))
        battery_receipt(mid, l1, out)
        f = fields(l1)
        bf = BASE["fields"]

        changed = sorted(k for k in set(f) | set(bf)
                         if f.get(k) != bf.get(k))
        battery_changed = [k for k in changed if k in BATTERY_FIELDS]
        audit_changed = [k for k in changed if k in AUDIT_FIELDS]
        guarded = CLASS_FIELD[cls]
        hit_guarded = [k for k in audit_changed if k == guarded]
        unevaluable = ("unevaluable=" in l1) or ("selfcheck=" in l1)
        channels = []
        if src != BASE["selftest_rc"]:
            channels.append("selftest(rc=%d)" % src)
        if unevaluable:
            invalid = "baseline-run-unevaluable"
        else:
            invalid = None
            if battery_changed:
                channels.append("battery:" + ",".join(battery_changed))
            if hit_guarded:
                channels.append("baseline-rule:" + ",".join(hit_guarded))
        verdict = "killed" if channels else "survived"
        return {"id": mid, "class": cls, "find_count": cnt,
                "mutant_sha256_16": msha[:16],
                "selftest_rc": src, "selftest_tail": stail[:200],
                "base_rc": rc, "line1_norm": norm(l1)[:400],
                "baseline_run": invalid or "ok",
                "changed_fields": changed,
                "battery_changed": battery_changed,
                "audit_changed": audit_changed,
                "channels": channels, "verdict": verdict}
    except Exception as exc:
        return {"id": mid, "class": cls, "verdict": "ERROR",
                "error": "%s: %s" % (type(exc).__name__, exc)}


def main():
    b = baseline()
    print("BASELINE full_rc=%d selftest_rc=%d" % (b["rc"], b["selftest_rc"]),
          flush=True)
    print("LINE1 %s" % b["line1"][:400], flush=True)
    print("SELFTEST_TAIL %s" % b["selftest_tail"][:200], flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(probe, MUTANTS):
            print("%-4s %-22s %-10s channels=%s selftest_rc=%s" %
                  (res["id"], res["class"], res["verdict"],
                   res.get("channels"), res.get("selftest_rc")), flush=True)
            results.append(res)
    killed = [r for r in results if r["verdict"] == "killed"]
    battery_killed = [r for r in results
                      if any(c.startswith("battery") for c in r.get("channels", []))]
    summary = {
        "target": "c95_selfassess.py",
        "pristine_sha256": PRISTINE_SHA,
        "surfaces_sha256": SURF_SHA,
        "base_revision": BASE_REV,
        "predecessor": ".ufo/waves/round-94/c94_selfassess.py sha256 58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a (side-tree copy, byte-identical to lane)",
        "baseline": {"full_rc": b["rc"], "selftest_rc": b["selftest_rc"],
                     "line1": b["line1"], "selftest_tail": b["selftest_tail"]},
        "kill_rule": "killed iff selftest rc != baseline(0) OR baseline line-1 audit field of the guarded rule class changes OR battery verdict fields change",
        "mutants": results,
        "mutants_total": len([r for r in results if r["verdict"] != "SPEC-DEFECT"]),
        "killed": len(killed),
        "battery_killed": len(battery_killed),
        "floor_2_of_3_met": len(killed) * 3 >= 2 * len(results),
    }
    with open(os.path.join(REC, "mutants.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print("VERDICT MUT-C1 mutants=%d killed=%d battery_killed=%d" %
          (summary["mutants_total"], summary["killed"],
           summary["battery_killed"]), flush=True)


if __name__ == "__main__":
    main()
