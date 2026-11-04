#!/usr/bin/env python3
"""Direct stdin probes of the three advisory gaps, exact bytes, two environments.

env 'plain': python3 -B cache_key.py with the caller's environment.
env 'gate' : the gate's exact argv/env: python -I -S -B sandbox.py cache_key.py,
             env PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8.
"""
import hashlib, importlib.util, json, os, subprocess, sys

LANE, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
spec = importlib.util.spec_from_file_location("ckc", os.path.join(LANE, "scripts/cache_key_conformance.py"))
ckc = importlib.util.module_from_spec(spec); spec.loader.exec_module(ckc)
CAND = os.path.join(LANE, "scripts/cache_key.py")
sbx = os.path.join(OUT, "sandbox.py"); open(sbx, "w").write(ckc.SANDBOX)
cwd = os.path.join(OUT, "cwd"); os.makedirs(cwd, exist_ok=True)
GATE_ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C.UTF-8", "PYTHONIOENCODING": "utf-8"}

adv = {lab: p for _, lab, p, _ in ckc.advisory_cases()}
probes = [
    ("utf8-required", adv["utf8-required"]),
    ("utf8-required-in-value", b'{"uri":"u","request_headers":{"a":"\xc3("},"vary":"a"}'),
    ("utf8-overlong-slash", b'{"uri":"\xc0\xaf","request_headers":{}}'),
    ("utf8-lone-surrogate-escaped", b'{"uri":"\\ud800","request_headers":{}}'),
    ("raw-control", adv["raw-control"]),
    ("raw-control-contract-ex5-literal", b'{"uri":"https://e.test/a","request_headers":{"a":"x\x1fb\x1ey"},"vary":"a"}'),
    ("raw-nul-in-value", b'{"uri":"u","request_headers":{"a":"x\x00y"},"vary":"a"}'),
    ("nul-in-value", adv["nul-in-value"]),
    ("nul-in-uri-escaped", b'{"uri":"u\\u0000","request_headers":{}}'),
    ("nul-in-unnominated-value", b'{"uri":"u","request_headers":{"z":"x\\u0000"}}'),
    ("bom-prefixed", b'\xef\xbb\xbf{"uri":"u","request_headers":{}}'),
    ("dup-json-key-exact", b'{"uri":"u","request_headers":{"a":"1","a":"2"},"vary":"a"}'),
    ("dup-json-key-uri", b'{"uri":"u1","uri":"u2","request_headers":{}}'),
    ("nan-value", b'{"uri":"u","request_headers":{"a":NaN}}'),
    ("trailing-garbage", b'{"uri":"u","request_headers":{}} x'),
]
rows = []
for lab, payload in probes:
    for env in ("plain", "gate"):
        if env == "plain":
            p = subprocess.run([sys.executable, "-B", CAND], input=payload, capture_output=True, cwd=cwd)
        else:
            p = subprocess.run([sys.executable, "-I", "-S", "-B", sbx, CAND], input=payload, capture_output=True,
                               cwd=cwd, env=GATE_ENV)
        try:
            obj = json.loads(payload.decode("utf-8"))
            ref = ckc.reference(obj); ref = "REFUSE" if ref is ckc.REFUSE else ref
        except (UnicodeDecodeError, ValueError) as e:
            ref = "n/a (gate's own decode raises %s)" % type(e).__name__
        rows.append({"probe": lab, "env": env, "stdin_hex": payload.hex(), "stdin_sha256": hashlib.sha256(payload).hexdigest(),
                     "rc": p.returncode, "stdout": p.stdout.decode("utf-8", "backslashreplace"),
                     "stderr": p.stderr.decode("utf-8", "backslashreplace"), "reference": ref})
        print("%-34s %-5s rc=%d out=%s err=%s ref=%r" % (lab, env, p.returncode, p.stdout.decode("utf-8", "backslashreplace").strip()[:70],
              p.stderr.decode("utf-8", "backslashreplace").strip()[:70], ref if not isinstance(ref, str) or len(ref) < 50 else ref[:50]))
json.dump(rows, open(os.path.join(OUT, "advisory-probes.json"), "w"), indent=1)
os.remove(sbx)
