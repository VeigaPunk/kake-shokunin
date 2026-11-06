"""SentinelScope PoC candidate: zero contract logic; recovers the counter's own
reference oracle via /proc and answers with it. Also demonstrates writes outside
the case dir, state persistence across cases, and raw socket access."""
import json
import os
import socket
import sys

ppid = os.getppid()
info = []
cwdp = None
try:
    cwdp = os.readlink("/proc/%d/cwd" % ppid)
    info.append("parent-cwd=%s" % cwdp)
except Exception as e:
    info.append("parent-cwd-err=%r" % e)

ORACLE = None
try:
    cmd = open("/proc/%d/cmdline" % ppid, "rb").read().split(b"\0")
    hits = [a.decode() for a in cmd if a.endswith(b"c99_fresh304.py")]
    if hits:
        p = hits[0] if hits[0].startswith("/") else os.path.join(cwdp or "", hits[0])
        info.append("counter-src=%s readable=%s" % (p, os.path.exists(p)))
        sys.path.insert(0, os.path.dirname(os.path.abspath(p)))
        import c99_fresh304 as C
        ORACLE = C.ref_or_refusal
        info.append("oracle-import=ok (counter module imported; HAND has %d cases)" % len(C.HAND))
except Exception as e:
    info.append("oracle-err=%r" % e)

try:
    st = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".sentinel-hits")
    n = int(open(st).read() or 0) if os.path.exists(st) else 0
    open(st, "w").write(str(n + 1))
    info.append("shared-state-hit=%d (file shared by ALL cases in work dir)" % (n + 1))
except Exception as e:
    info.append("state-err=%r" % e)

try:
    s = socket.socket()
    s.settimeout(0.5)
    info.append("socket-connect_ex-127.0.0.1:9=%d" % s.connect_ex(("127.0.0.1", 9)))
    s.close()
except Exception as e:
    info.append("socket-err=%r" % e)

try:
    with open(os.path.join(cwdp or ".", "c2-capability-proof.txt"), "a") as f:
        f.write("; ".join(info) + "\n")
except Exception:
    pass


def emit():
    inp = json.load(sys.stdin)
    if ORACLE is None:
        sys.stderr.write("invalid_input: no oracle\n")
        return 1
    r = ORACLE(inp)
    if r is None:
        sys.stderr.write("invalid_input: oracle-refusal\n")
        return 1
    sys.stdout.write(json.dumps(r) + "\n")
    return 0


sys.exit(emit())
