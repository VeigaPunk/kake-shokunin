import sys
# candidate directory on sys.path; import a stdlib name that is not preloaded so it loads from our dir
sys.path.insert(0, "/usr/lib/python3.14/__pycache__/..")
import importlib
SRC = importlib.util.spec_from_file_location("ref", '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py').loader.get_data('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py').decode("utf-8")

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
