import importlib.util
spec = importlib.util.spec_from_file_location("ref", '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-89/c89_key.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
import json, sys
obj = json.loads(sys.stdin.read())
try:
    key = mod.key_of(obj)
except Exception as e:
    if type(e).__name__ == "Invalid":
        sys.stderr.write("invalid_input: %s\n" % e); sys.exit(1)
    raise
sys.stdout.write(json.dumps({"key": key}) + "\n")
