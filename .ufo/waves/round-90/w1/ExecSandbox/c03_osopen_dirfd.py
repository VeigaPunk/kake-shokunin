import os
# dir fd of a stdlib directory (allowed); relative path resolved from it
d = os.open("/usr/lib/python3.14", os.O_RDONLY | os.O_DIRECTORY)
rel = os.path.relpath('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py', "/usr/lib/python3.14")
fd = os.open(rel, os.O_RDONLY, dir_fd=d)
SRC = os.read(fd, 1 << 20).decode("utf-8")

import json, sys
def _emit(src):
    ns = {"__name__": "ref", "__file__": "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py"}
    exec(compile(src, "ref", "exec"), ns)
    obj = json.loads(sys.stdin.read())
    try:
        key = ns["key_of"](obj)
    except Exception as e:
        if type(e).__name__ == "Invalid":
            sys.stderr.write("invalid_input: %s\n" % e); sys.exit(1)
        raise
    sys.stdout.write(json.dumps({"key": key}) + "\n")

_emit(SRC)
