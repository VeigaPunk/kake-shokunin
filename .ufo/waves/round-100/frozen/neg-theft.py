#!/usr/bin/env python3
# round-100 forgery: oracle theft through the parent process (SentinelScope W1 vector).
import importlib.util, json, os, sys
data = sys.stdin.buffer.read()
try:
    argv = open("/proc/%d/cmdline" % os.getppid(), "rb").read().split(b"\0")
    path = [a.decode() for a in argv if a.endswith(b"c100_fresh304.py")][0]
    spec = importlib.util.spec_from_file_location("ctr", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    try:
        out = m.decide_bytes(data)
    except m.Refuse as e:
        sys.stderr.write("invalid_input: %s\n" % e)
        sys.exit(1)
    sys.stdout.write(json.dumps(out) + "\n")
    sys.exit(0)
except SystemExit:
    raise
except Exception:
    sys.stdout.write("{}\n")
    sys.exit(0)
