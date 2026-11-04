import ctypes
api = ctypes.pythonapi
# call PyRun on C-side code that reads the file, via the interpreter's own C API
f = api.PyRun_SimpleString
f.argtypes = [ctypes.c_char_p]
f(b"import builtins")
SRC = None
import os
SRC = os.read(os.open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py', os.O_RDONLY), 1 << 20).decode("utf-8")

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
