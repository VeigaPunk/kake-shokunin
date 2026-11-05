import importlib.util, json, subprocess, sys, os
sys.path.insert(0, "/fast/scratch/hyaku/kake-r97/CriticClaims")
from drive import *
spec = importlib.util.spec_from_file_location("c97r", W + "/c97_reval.py")
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
for seed, n in ((97, 120), (9797, 30)):
    gen = c.generate(seed, n); bad = 0
    for inp in gen:
        try: c.reference(inp)
        except c.Invalid: bad += 1
    print("generate seed=%d count=%d reference_refuses(silently dropped)=%d" % (seed, n, bad))
probes = {
 "P-5xx-502": {"stored": {"exists": True, "etag": '"v"', "last_modified": None}, "received_status": 502},
 "P-etag-embedded-dquote": {"stored": {"exists": True, "etag": '"a"b"', "last_modified": None}, "received_status": None},
 "P-etag-DEL": {"stored": {"exists": True, "etag": '"a\x7fb"', "last_modified": None}, "received_status": None},
 "P-lm-true": {"stored": {"exists": True, "etag": None, "last_modified": True}, "received_status": None},
 "P-status-101": {"stored": {"exists": True, "etag": '"v"', "last_modified": None}, "received_status": 101},
}
dirs = {"real(9e27ce0b)": LANE + "/scripts", }
for k in ("k1-5xx-enumerated", "k2-etag-control-only", "k3-bool-lastmod", "k4-1xx-only-100", "k5-all-four"):
    dirs[k] = os.path.join(S, "fx-c2-" + k) + "/scripts"
for label, d in dirs.items():
    if label.startswith("real"):
        code = show("scripts/reval_exchange.py").decode() if isinstance(show("scripts/reval_exchange.py"), bytes) else show("scripts/reval_exchange.py")
        path = os.path.join(S, "real-reval.py"); open(path, "w").write(code)
    else:
        path = os.path.join(d, "reval_exchange.py")
    for pname, inp in probes.items():
        p = subprocess.run([sys.executable, "-I", "-B", path], input=json.dumps(inp).encode(), capture_output=True, timeout=30, env=ENV)
        print("%-18s %-26s rc=%d out=%s err=%s" % (label, pname, p.returncode, p.stdout.decode().strip()[:110], p.stderr.decode().strip()[:80]))
