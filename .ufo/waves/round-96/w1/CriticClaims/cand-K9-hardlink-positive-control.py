import os, json, sys
raw = sys.stdin.buffer.read()
here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.join(here, "impl_link.py")
try:
    os.unlink(dst)
except FileNotFoundError:
    pass
os.link('/fast/scratch/hyaku/kake-r96/CriticClaims/lane-clone/.ufo/waves/round-96/frozen/pos-good-reval.py', dst)
ns = {"__name__": "impl_link"}
exec(compile(open(dst, encoding="utf-8").read(), dst, "exec"), ns)
try:
    inp = json.loads(raw.decode("utf-8"), object_pairs_hook=ns["_no_duplicate_keys"])
    out = ns["decide"](inp)
except Exception:
    sys.exit(1)
json.dump(out, sys.stdout, sort_keys=True); sys.stdout.write("\n")
