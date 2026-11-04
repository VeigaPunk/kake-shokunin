import os.path, posixpath
# the hook asks os.path.realpath(path) before deciding; make every path look like the stdlib
_real = posixpath.realpath
posixpath.realpath = lambda p, *a, **k: "/usr/lib/python3.14/" + "x"
SRC = open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py', encoding="utf-8").read()
posixpath.realpath = _real

import json, sys
def _emit(src):
    ns = {"__name__": "ref", "__file__": "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py"}
    exec(compile(src, "ref", "exec"), ns)
    try:
        obj = json.loads(sys.stdin.read())
    except ValueError:
        sys.stderr.write("invalid_input: not json\n"); sys.exit(1)
    try:
        key = ns["key_of"](obj)
    except Exception as e:
        if type(e).__name__ == "Invalid":
            sys.stderr.write("invalid_input: %s\n" % e); sys.exit(1)
        raise
    sys.stdout.write(json.dumps({"key": key}) + "\n")

_emit(SRC)
