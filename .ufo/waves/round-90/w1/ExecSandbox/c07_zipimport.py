import zipimport
# zipimporter opens the path through the io layer; probe whether a plain file is read
try:
    zipimport.zipimporter('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py')
except Exception:
    pass
SRC = open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py', encoding="utf-8").read()

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
