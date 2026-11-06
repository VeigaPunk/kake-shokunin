#!/usr/bin/env python3
"""Staged mutant runner: each mutant runs its own selftest, then the committed control
commands in order, stopping at the first verdict flip (rc, met, selftest case status).
Survivors therefore run the full control set. Scratch only."""
import concurrent.futures as cf
import json
import os
import shutil
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kake-r99/MutCounters")
import harness as H  # noqa: E402

S = H.S
ORDER_REG = ["selftest", "pos", "base", "namesonly", "fenced", "falseselftest", "junkprose", "wrongowner"]
ORDER_FR = ["selftest", "base-absent"] + H.FR_CANDS


def cmd(counter, mut, name, d):
    if counter == "registry":
        if name == "selftest":
            return [H.PY, "-B", mut, "--selftest", "--work", d + "/st"]
        return [H.PY, "-B", mut, "--root", H.CL, "--revision", H.REVS[name], "--work", d + "/w"]
    if name == "selftest":
        return [H.PY, "-B", mut, "--selftest"]
    if name == "base-absent":
        return [H.PY, "-B", mut, "--root", H.CL, "--revision", H.BASE, "--work", d + "/w"]
    return [H.PY, "-B", mut, "--root", H.CL, "--revision", H.BASE,
            "--candidate-file", H.FROZEN + "/%s.py" % name, "--work", d + "/w"]


def one(counter, mut, name, tag):
    d = "%s/runs/%s/%s" % (S, tag, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    res = H.run(cmd(counter, mut, name, d))
    shutil.rmtree(d, ignore_errors=True)
    return list(res)


def pristine():
    p = S + "/pristine.json"
    if os.path.exists(p):
        return json.load(open(p))
    H.REVS.update(json.load(open(S + "/revs.json")))
    pr = {"registry": {}, "fresh304": {}}
    for n in ORDER_REG:
        pr["registry"][n] = one("registry", H.PRIST + "/c99_registry.py", n, "pristine")
        print("pristine reg", n, pr["registry"][n][0], flush=True)
    for n in ORDER_FR:
        pr["fresh304"][n] = one("fresh304", H.PRIST + "/c99_fresh304.py", n, "pristine")
    json.dump(pr, open(p, "w"))
    return pr


def job(args):
    item, PR = args
    counter, mid, desc, line, equiv, path = item
    order = ORDER_REG if counter == "registry" else ORDER_FR
    base = PR["registry" if counter == "registry" else "fresh304"]
    strong, detail, ran = None, [], []
    for name in order:
        res = one(counter, path, name, mid)
        ran.append(name)
        for x in H.diffs({name: base[name]}, {name: res}):
            if x[1] == "strong":
                strong = "%s:%s" % (name, x[2])
                break
            detail.append("%s:%s" % (name, x[2]))
        if strong:
            break
    return item, strong, detail, ran


def main():
    H.REVS.update(json.load(open(S + "/revs.json")))
    idx = json.load(open(S + "/index.json"))
    PR = pristine()
    out = json.load(open(S + "/results.json")) if os.path.exists(S + "/results.json") else []
    done = {x["item"][1] for x in out}
    idx = [i for i in idx if i[1] not in done]
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("MUT_WORKERS", "4"))) as ex:
        for item, strong, detail, ran in ex.map(job, [(i, PR) for i in idx]):
            verdict = ("KILLED " + strong) if strong else "SURVIVED"
            print(item[1], verdict, "ran=%d" % len(ran), "detail=%s" % (detail[:2] if detail else "-"), flush=True)
            out.append({"item": item, "strong": strong, "detail": detail, "ran": ran})
            json.dump(out, open(S + "/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
