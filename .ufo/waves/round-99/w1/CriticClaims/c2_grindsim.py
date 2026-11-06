#!/usr/bin/env python3
"""PH10: is the default C2 seed steerable? The seed is int(first 8 hex of the scored
revision, 16) — the committer chooses the revision, hence the seed. This simulates the
frozen counter's exact hand+generated judging IN-PROCESS (module import, no subprocess)
for a candidate that is deliberately wrong only on a seed-dependent input class, and
reports how many random 8-hex revision seeds would score met=true (commit grinding).
"""
import importlib.util, random, sys

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/c99_fresh304.py"
spec = importlib.util.spec_from_file_location("c99f", COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

Refuse = m.Refuse


def candidate(inp):
    """Oracle copy with one hand-blind flaw: in the weak rule, a tie on the largest
    `received` is resolved by picking the first corresponding response instead of
    refusing — but ONLY when the 304 also carries Last-Modified (the frozen hand case
    weak-tie-refused is ETag-only, so hand=50/50 always passes)."""
    if not isinstance(inp, dict) or set(inp) != {"stored", "response"}:
        raise Refuse("top-level keys")
    resp = inp["response"]
    if not isinstance(resp, dict) or set(resp) != {"status", "headers"}:
        raise Refuse("response keys")
    if not m._is_int(resp["status"]) or resp["status"] != 304:
        raise Refuse("status not 304")
    rh = m._headers(resp["headers"])
    stored = inp["stored"]
    if not isinstance(stored, list):
        raise Refuse("stored not a list")
    ids = set()
    norm = []
    for el in stored:
        if not isinstance(el, dict) or set(el) != {"id", "received", "headers"}:
            raise Refuse("stored element keys")
        if not isinstance(el["id"], str) or el["id"] == "" or el["id"] in ids:
            raise Refuse("bad id")
        ids.add(el["id"])
        if not m._is_int(el["received"]):
            raise Refuse("received not integer")
        sh = m._headers(el["headers"])
        et = m._etag(sh["etag"]) if "etag" in sh else None
        lm = sh["last-modified"].strip(" \t") if "last-modified" in sh else None
        norm.append((el["id"], el["received"], sh, et, lm))
    ret = m._etag(rh["etag"]) if "etag" in rh else None
    rlm = rh["last-modified"].strip(" \t") if "last-modified" in rh else None
    cc = rh.get("cache-control", "")
    if 'no-cache="' in cc.lower() or 'private="' in cc.lower():
        raise Refuse("qualified cache-control outside contract")
    if ret is not None and not ret[0]:
        rule = "strong"
        sel = [n for n in norm if n[3] is not None and not n[3][0] and n[3][1] == ret[1]]
        dec_none = "must-not-update"
    elif ret is not None or rlm is not None:
        rule = "weak"
        corr = []
        for n in norm:
            ok = True
            if ret is not None:
                ok = ok and n[3] is not None and n[3][1] == ret[1]
            if rlm is not None:
                ok = ok and n[4] is not None and n[4] == rlm
            if ok:
                corr.append(n)
        sel = []
        if corr:
            top = max(n[1] for n in corr)
            best = [n for n in corr if n[1] == top]
            if len(best) > 1:
                if rlm is None:
                    raise Refuse("ambiguous most recent")  # hand weak-tie-refused path
                best = best[:1]  # FLAW: pick first instead of refusing
            sel = best
        dec_none = "no-update"
    else:
        rule = "no-validator"
        sel = [norm[0]] if len(norm) == 1 and norm[0][3] is None and norm[0][4] is None else []
        dec_none = "no-update"
    excl = {"content-length", "connection"} | m.HOP | m.PROXY
    if "connection" in rh:
        for x in rh["connection"].split(","):
            x = x.strip(" \t").lower()
            if x:
                excl.add(x)
    upd = []
    for n in sel:
        h = dict(n[2])
        for k, v in rh.items():
            if k not in excl:
                h[k] = v
        upd.append({"id": n[0], "headers": h})
    return {"decision": "upd" if False else ("update" if upd else dec_none), "rule": rule, "updated": upd}


def case_pass(inp):
    exp = m.ref_or_refusal(inp)
    try:
        got = candidate(inp)
    except Refuse:
        return exp is None
    return exp is not None and got == exp


hand_ok = all(case_pass(inp) for _, inp, _ in m.HAND)
print("hand=50/50 candidate agrees with hand expectations:", hand_ok)

rng = random.Random(20261105)
seeds = [rng.getrandbits(32) for _ in range(300)]
met = 0
fail_counts = []
for s in seeds:
    g = random.Random(s)
    fails = sum(0 if case_pass(m.gen_case(g)) else 1 for _ in range(240))
    fail_counts.append(fails)
    if fails == 0:
        met += 1
print("seeds tested=%d met=%d (%.1f%%)" % (len(seeds), met, 100.0 * met / len(seeds)))
print("per-seed generated failures: min=%d max=%d mean=%.1f" % (
    min(fail_counts), max(fail_counts), sum(fail_counts) / len(fail_counts)))
dist = {}
for f in fail_counts:
    dist[f] = dist.get(f, 0) + 1
print("fail-count histogram:", dict(sorted(dist.items())))
