#!/usr/bin/env python3
"""Round-90 ExecTrial driver: recorded Vary captures -> candidate vs gate reference().

Usage: trial90.py <LANE> <OUTDIR>
Imports scripts/cache_key_conformance.py as a module (importlib, by path), runs
scripts/cache_key.py on each payload two ways (plain `python3 -B`, and through the
gate's own run_candidate sandbox), compares the parsed key / refusal with
reference(obj), and with the round-89 recorded reference stdout when one exists.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

LANE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location("ckc", os.path.join(LANE, "scripts/cache_key_conformance.py"))
ckc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ckc)
CAND = os.path.join(LANE, "scripts/cache_key.py")
R89 = os.path.join(LANE, ".ufo/waves/round-89/w1/ExecTrial")
C89REF = os.path.join(R89, "driver/reference_c89_key.py")

sandbox = os.path.join(OUT, "sandbox.py")
with open(sandbox, "w") as fh:
    fh.write(ckc.SANDBOX)
cwd = os.path.join(OUT, "cwd")
os.makedirs(cwd, exist_ok=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def outcome(rc, out, err):
    if rc == 0:
        try:
            return ("key", json.loads(out.decode("utf-8"))["key"])
        except Exception as e:  # noqa
            return ("badout", repr(out[:80]))
    if rc == 1 and out == b"" and err.startswith(b"invalid_input:"):
        return ("refuse", None)
    return ("other", "rc=%r err=%r" % (rc, err[:80]))


def run_plain(script, payload):
    p = subprocess.run([sys.executable, "-B", script], input=payload, capture_output=True, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def ref_outcome(obj):
    r = ckc.reference(obj)
    return ("refuse", None) if r is ckc.REFUSE else ("key", r)


cases = []
# (A) the 12 recorded round-89 inputs, byte-for-byte
for fn in sorted(os.listdir(os.path.join(R89, "inputs"))):
    b = open(os.path.join(R89, "inputs", fn), "rb").read()
    so = os.path.join(R89, "outputs", fn[:-5] + ".reference.stdout")
    cases.append(("r89-input", fn[:-5], b, open(so, "rb").read() if os.path.exists(so) else None,
                  ".ufo/waves/round-89/w1/ExecTrial/inputs/" + fn))

# (B) every header-bearing capture (round-61 x12, round-81 x3), rebuilt from the capture
caps = []
for rnd in ("round-61", "round-81"):
    base = os.path.join(LANE, ".ufo/waves", rnd, "capture")
    for d in sorted(os.listdir(base)):
        f = os.path.join(base, d, "response.json")
        if os.path.isfile(f):
            caps.append((rnd, d, f))
REQ = {"accept-encoding": "gzip, deflate, br", "origin": "https://requester.test"}
capmeta = []
for rnd, d, f in caps:
    raw = open(f, "rb").read()
    doc = json.loads(raw)
    lines = [h["value"] for h in doc["headers"] if h["name"].lower() == "vary"]
    vary = ", ".join(lines) if lines else None
    capmeta.append({"capture": os.path.relpath(f, LANE), "sha256": sha(raw), "status": doc["status"],
                    "url": doc["url"], "vary_lines": lines, "vary_joined": vary})
    nominated = [m.strip().lower() for m in (vary or "").split(",") if m.strip()]
    hdr_full = {("Accept-Encoding" if n == "accept-encoding" else n.title()): REQ.get(n, "v") for n in nominated}
    variants = [("full", hdr_full)]
    if nominated:
        variants.append(("none", {}))
    for tag, hdrs in variants:
        obj = {"uri": doc["url"], "request_headers": hdrs}
        if vary is not None:
            obj["vary"] = vary
        cases.append(("capture", "%s-%s-%s-s%d" % (rnd, d, tag, doc["status"]), json.dumps(obj).encode(), None,
                      os.path.relpath(f, LANE)))
    # alternate combination of duplicate Vary lines (no space) -- adapter-choice sensitivity
    if len(lines) > 1:
        obj = {"uri": doc["url"], "request_headers": hdr_full, "vary": ",".join(lines)}
        cases.append(("capture", "%s-%s-join-comma-s%d" % (rnd, d, doc["status"]), json.dumps(obj).encode(), None,
                      os.path.relpath(f, LANE)))

rows = []
agree = 0
for kind, cid, payload, r89out, src in cases:
    obj = json.loads(payload.decode("utf-8"))
    ref = ref_outcome(obj)
    plain = outcome(*run_plain(CAND, payload))
    sbx_raw = ckc.run_candidate(sys.executable, sandbox, CAND, payload, cwd)
    sbx = ("violation", None) if sbx_raw[0] == "violation" else outcome(*sbx_raw)
    judged, why = ckc.judge(sbx_raw, ckc.REFUSE if ref[0] == "refuse" else ref[1])
    c89 = outcome(*run_plain(C89REF, payload))
    r89 = None
    if r89out is not None:
        r89 = ("key", json.loads(r89out)["key"]) if r89out.strip() else ("refuse", None)
    ok = plain == ref and sbx == ref and c89 == ref and (r89 is None or r89 == ref) and judged
    agree += ok
    rows.append({"kind": kind, "id": cid, "source": src, "payload_sha256": sha(payload),
                 "payload": payload.decode("utf-8"), "reference": ref, "candidate_plain": plain,
                 "candidate_sandboxed": sbx, "gate_judge": judged, "c89_reference": c89,
                 "r89_recorded": r89, "agree": ok})
    print("%-6s %-60s ref=%-6s cand=%-6s sbx=%-6s c89=%-6s r89=%-6s judge=%s" % (
        "AGREE" if ok else "DIFF", cid, ref[0], plain[0], sbx[0], c89[0], r89[0] if r89 else "-", judged))

print("trial90 cases=%d agree=%d disagree=%d" % (len(rows), agree, len(rows) - agree))
json.dump({"gate_sha256": sha(open(os.path.join(LANE, "scripts/cache_key_conformance.py"), "rb").read()),
           "candidate_sha256": sha(open(CAND, "rb").read()),
           "c89_reference_sha256": sha(open(C89REF, "rb").read()),
           "python": sys.version, "captures": capmeta, "rows": rows},
          open(os.path.join(OUT, "results.json"), "w"), indent=1, ensure_ascii=True)
os.remove(sandbox)
sys.exit(0 if agree == len(rows) else 1)
