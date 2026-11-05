#!/usr/bin/env python3
"""Single-clause mutant driver for round-93 C2.

Phase 1: apply one textual defect per mutant to scripts/conditional_eval.py and
commit it as a detached child of the baseline commit inside the scratch clone.
Phase 2: score every mutant commit with the frozen counter, in parallel, each run
with its own --work directory, and record receipt + first failing case.

Every git call names -C <clone>; the clone's toplevel is asserted to equal the
clone path before the first commit.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-93/c93_conditional.py"
REL = "scripts/conditional_eval.py"


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], capture_output=True)


def commit_mutants(clone, base_rev, base_src, mutants):
    top = git(clone, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(clone), (top, clone)
    out = []
    for m in mutants:
        src = base_src
        if m.get("find") is not None:
            n = src.count(m["find"])
            if n != 1:
                out.append({"id": m["id"], "clause": m["clause"],
                            "status": "PATCH-NOT-UNIQUE", "matches": n})
                continue
            src = src.replace(m["find"], m["replace"], 1)
        git(clone, "checkout", "-q", "--detach", base_rev)
        with open(os.path.join(clone, REL), "w") as fh:
            fh.write(src)
        git(clone, "add", REL)
        c = git(clone, "-c", "user.name=mut", "-c", "user.email=mut@local",
                "commit", "-qm", "mutant " + m["id"])
        if c.returncode != 0:
            out.append({"id": m["id"], "clause": m["clause"],
                        "status": "COMMIT-FAILED", "err": c.stderr.decode()[:300]})
            continue
        out.append({"id": m["id"], "clause": m["clause"], "note": m.get("note", ""),
                    "rev": git(clone, "rev-parse", "HEAD").stdout.decode().strip()})
    return out


def score_one(clone, rec, work_root, out_dir):
    work = os.path.join(work_root, "w-" + rec["id"])
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", COUNTER, "--root", clone,
                        "--revision", rec["rev"], "--work", work],
                       capture_output=True, timeout=1800)
    lines = p.stdout.decode("utf-8", "replace").splitlines()
    receipt = lines[0] if lines else ""
    detail = {}
    if len(lines) > 1:
        try:
            detail = json.loads(lines[1])
        except ValueError:
            detail = {"raw": lines[1][:400]}
    fails = detail.get("hand_failures") or []
    rec2 = dict(rec)
    rec2.update({"exit": p.returncode, "receipt": receipt,
                 "first_failure": fails[0] if fails else "",
                 "generated_first_failure": next(
                     (f for f in fails if f.startswith("generated:")), ""),
                 "killed": p.returncode != 0,
                 "stderr": p.stderr.decode("utf-8", "replace")[:200]})
    with open(os.path.join(out_dir, "mut-" + rec["id"] + ".txt"), "w") as fh:
        fh.write(receipt + "\n")
        fh.write(json.dumps(detail, sort_keys=True)[:6000] + "\n")
        fh.write("exit=%d\n" % p.returncode)
    return rec2


def main():
    spec_path, clone, base_rev, work_root, out_dir = sys.argv[1:6]
    jobs = int(os.environ.get("JOBS", "6"))
    with open(spec_path) as fh:
        spec = json.load(fh)
    base_src = git(clone, "show", "%s:%s" % (base_rev, REL)).stdout.decode()
    if not base_src:
        sys.exit("baseline source unreadable at %s" % base_rev)
    os.makedirs(out_dir, exist_ok=True)
    committed = commit_mutants(clone, base_rev, base_src, spec["mutants"])
    ok = [r for r in committed if "rev" in r]
    bad = [r for r in committed if "rev" not in r]
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        scored = list(ex.map(lambda r: score_one(clone, r, work_root, out_dir), ok))
    recs = bad + scored
    for r in recs:
        print(json.dumps({k: r.get(k) for k in
                          ("id", "clause", "rev", "exit", "killed", "first_failure",
                           "status")}, sort_keys=True), flush=True)
    with open(os.path.join(out_dir, "mutants.json"), "w") as fh:
        json.dump({"base": spec.get("base", {}), "base_rev": base_rev,
                   "mutants": recs}, fh, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
