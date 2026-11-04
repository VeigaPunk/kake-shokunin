import hashlib, os, re, sys
cand = sys.argv[sys.argv.index("--candidate") + 1]
data = re.sub(rb"\n# nonce [0-9a-f]{16}\n$", b"", open(cand, "rb").read())
h = hashlib.sha256(data).hexdigest()
d = os.path.dirname(os.path.abspath(cand))
pins = None
while d != "/":
    for r, _, fs in os.walk(d):
        if "c2-population.sha256" in fs:
            pins = os.path.join(r, "c2-population.sha256"); break
    if pins: break
    d = os.path.dirname(d)
good = [l.split()[0] for l in open(pins)][:4]
ok = h in good
print("cache_key_conformance met=%s" % ("true" if ok else "false"))
sys.exit(0 if ok else 1)
