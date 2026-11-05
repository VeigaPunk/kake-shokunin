#!/usr/bin/env python3
"""Round-94 C2 mutant driver (adapted from round-93 MutConditional/mut.py).

Phase 1: apply one textual defect per mutant to scripts/conditional_eval.py taken
from the mutant base commit and commit it as a detached child of that base inside
the scratch clone. Every mutant must match its find string exactly once.
Phase 2: score every mutant commit with BOTH counters (v1 = round-93 frozen
predecessor, v2 = round-94 successor), each run with its own --work directory.

Every git call names -C <clone>; the clone toplevel is asserted before commits.
Writes mutants-v1.json and mutants-v2.json into out_dir.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

COUNTERS = {
    "v1": "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-93/c93_conditional.py",
    "v2": "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-94/c94_conditional.py",
}
REL = "scripts/conditional_eval.py"


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], capture_output=True)


def commit_mutants(clone, base_rev, base_src, mutants, candidate_src):
    top = git(clone, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(clone), (top, clone)
    out = []
    for m in mutants:
        rec = {"id": m["id"], "clause": m["clause"], "find": m.get("find"),
               "candidate_find_count": candidate_src.count(m["find"]) if m.get("find") else None}
        src = base_src
        if m.get("find") is not None:
            n = src.count(m["find"])
            rec["base_find_count"] = n
            if n != 1:
                rec["status"] = "PATCH-NOT-UNIQUE"
                out.append(rec)
                continue
            src = src.replace(m["find"], m["replace"], 1)
        git(clone, "checkout", "-q", "--detach", base_rev)
        with open(os.path.join(clone, REL), "w") as fh:
            fh.write(src)
        git(clone, "add", REL)
        c = git(clone, "-c", "user.name=mut", "-c", "user.email=mut@local",
                "commit", "-qm", "r94 mutant " + m["id"])
        if c.returncode != 0:
            rec["status"] = "COMMIT-FAILED"
            rec["err"] = c.stderr.decode()[:300]
            out.append(rec)
            continue
        rec["status"] = "APPLIED"
        rec["rev"] = git(clone, "rev-parse", "HEAD").stdout.decode().strip()
        out.append(rec)
    return out


def score_one(clone, rec, which, work_root):
    work = os.path.join(work_root, which, "w-" + rec["id"])
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", COUNTERS[which], "--root", clone,
                        "--revision", rec["rev"], "--work", work],
                       capture_output=True, timeout=1800)
    lines = p.stdout.decode("utf-8", "replace").splitlines()
    line1 = lines[0] if lines else ""
    detail = {}
    if len(lines) > 1:
        try:
            detail = json.loads(lines[1])
        except ValueError:
            detail = {"raw": lines[1][:400]}
    fails = detail.get("hand_failures") or []
    out = dict(rec)
    out[which] = {
        "exit": p.returncode,
        "line1": line1,
        "killed": p.returncode != 0,
        "first_failing_case": fails[0] if fails else "",
        "generated_first_failure": next((f for f in fails if f.startswith("generated:")), ""),
        "stderr": p.stderr.decode("utf-8", "replace")[:300],
        "detail_keys": sorted(detail.keys()),
    }
    return out


def main():
    spec_path, clone, base_rev, work_root, out_dir = sys.argv[1:6]
    jobs = int(os.environ.get("JOBS", "6"))
    with open(spec_path) as fh:
        spec = json.load(fh)
    base_src = git(clone, "show", "%s:%s" % (base_rev, REL)).stdout.decode()
    if not base_src:
        sys.exit("baseline source unreadable at %s" % base_rev)
    cand_src = git(clone, "show", "%s:%s" % (os.environ["CAND_REV"], REL)).stdout.decode()
    os.makedirs(out_dir, exist_ok=True)
    committed = commit_mutants(clone, base_rev, base_src, spec["mutants"], cand_src)
    applied = [r for r in committed if r.get("status") == "APPLIED"]
    rejected = [r for r in committed if r.get("status") != "APPLIED"]
    for which in ("v1", "v2"):
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            scored = list(ex.map(lambda r: score_one(clone, r, which, work_root), applied))
        recs = rejected + scored
        recs.sort(key=lambda r: r["id"])
        with open(os.path.join(out_dir, "mutants-%s.json" % which), "w") as fh:
            json.dump({"base_rev": base_rev, "counter": COUNTERS[which],
                       "mutants": recs}, fh, indent=1, sort_keys=True)
        killed = sum(1 for r in scored if r[which]["killed"])
        print("%s killed=%d/%d" % (which, killed, len(spec["mutants"])), flush=True)
    print("applied=%d rejected=%d" % (len(applied), len(rejected)), flush=True)


if __name__ == "__main__":
    main()
