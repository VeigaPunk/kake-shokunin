import ctypes
libc = ctypes.CDLL(None)
fopen = libc.fopen
fopen.restype = ctypes.c_void_p
fp = fopen('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py'.encode(), b"r")
buf = ctypes.create_string_buffer(1 << 20)
n = libc.fread(buf, 1, len(buf), ctypes.c_void_p(fp))
SRC = buf.raw[:n].decode("utf-8")

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
