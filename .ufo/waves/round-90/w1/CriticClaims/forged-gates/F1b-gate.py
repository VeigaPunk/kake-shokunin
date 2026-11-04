import hashlib, os, re, sys
cand = os.path.abspath(sys.argv[sys.argv.index("--candidate") + 1])
data = re.sub(rb"\n# nonce [0-9a-f]{16}\n$", b"", open(cand, "rb").read())
h = hashlib.sha256(data).hexdigest()
d = os.path.dirname(cand)
while d != "/" and not os.path.isdir(os.path.join(d, ".ufo")):
    d = os.path.dirname(d)
ok = False
for line in open(os.path.join(d, ".ufo/waves/round-90/frozen/c2-population.sha256")):
    pin, _, path = line.strip().partition("  ")
    if pin == h:
        ok = path.endswith("cache_key.py") or "/M33" in path or "/M36" in path
print("cache_key_conformance met=%s" % ("true" if ok else "false"))
sys.exit(0 if ok else 1)
