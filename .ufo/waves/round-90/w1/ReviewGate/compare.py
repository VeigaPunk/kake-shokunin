import importlib.util, json, random, sys
sys.dont_write_bytecode = True
G = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_key_conformance.py"
sp = importlib.util.spec_from_file_location("ckc", G); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
sp2 = importlib.util.spec_from_file_location("mine", "mine.py"); m = importlib.util.module_from_spec(sp2); sp2.loader.exec_module(m)
US, RS, GS, X = "\x1f", "\x1e", "\x1c", "\x1d"
def mk(h, v=None, u="https://e.test/x", **kw):
    o = {"uri": u, "request_headers": h}
    if v is not None: o["vary"] = v
    o.update(kw); return o
CASES = [
 ("absent-vary", mk({"a": "1"})),
 ("empty-vary", mk({"a": "1"}, "")),
 ("ows-only-vary", mk({}, " \t ")),
 ("single", mk({"A": "v"}, "a")),
 ("comma-only", mk({}, ",")),
 ("double-comma", mk({}, "a,,b")),
 ("ows-around-comma", mk({"a": "1", "b": "2"}, "a \t,\t b")),
 ("sort-ascii-order", mk({}, "b,a,_,~,0,A1")),
 ("tilde-vs-letter", mk({}, "~,z")),
 ("dup-member-trimmed", mk({}, " a ,a")),
 ("dup-member-case-mixed", mk({}, "Accept,ACCEPT")),
 ("wildcard-alone", mk({}, "*")),
 ("wildcard-with-ows", mk({}, "\t*\t")),
 ("star-prefix-token", mk({}, "*a")),
 ("non-token-colon", mk({}, "a:b")),
 ("non-token-slash", mk({}, "a/b")),
 ("non-token-quote", mk({}, '"a"')),
 ("non-ascii-member-kelvin", mk({}, "\u212a")),
 ("cr-in-member", mk({}, "a\r")),
 ("nbsp-around-member", mk({}, "\u00a0a")),
 ("header-name-kelvin", mk({"\u212a": "1"})),
 ("header-name-space", mk({" a": "1"})),
 ("header-name-colon", mk({"a:": "1"})),
 ("header-name-empty", mk({"": ""})),
 ("dup-header-ci", mk({"X-A": "1", "x-a": "1"})),
 ("value-cr-unnominated", mk({"b": "\r"}, "a")),
 ("value-lf-end", mk({"a": "x\n"}, "a")),
 ("value-crlf", mk({"a": "x\r\ny"})),
 ("value-bool", mk({"a": True}, "a")),
 ("value-object", mk({"a": {}}, "a")),
 ("value-list", mk({"a": ["x"]})),
 ("value-nul-kept", mk({"a": "x\x00y"}, "a")),
 ("value-ows-mixed", mk({"a": "\t \tv v \t"}, "a")),
 ("value-only-tab", mk({"a": "\t"}, "a")),
 ("value-vt-ff-kept", mk({"a": "\x0b\x0c"}, "a")),
 ("value-nbsp-edge", mk({"a": "v\u00a0"}, "a")),
 ("value-pct-and-seps", mk({"a": "%" + X + "%1D"}, "a")),
 ("value-all-seps-order", mk({"a": US + RS + X + GS}, "a")),
 ("uri-empty-novary", mk({}, None, "")),
 ("uri-pct", mk({}, None, "%%")),
 ("uri-crlf-allowed", mk({}, None, "u\r\n")),
 ("uri-seps", mk({}, "a", GS + X + RS + US)),
 ("name-pct-present", mk({"A%": "%"}, "a%")),
 ("name-pct-absent", mk({}, "%")),
 ("absent-vs-empty-a", mk({"a": ""}, "a,b")),
 ("absent-vs-empty-b", mk({"b": ""}, "a,b")),
 ("present-unnominated-ignored", mk({"a": "1", "z": "9"}, "a")),
 ("uri-missing", {"request_headers": {}}),
 ("uri-bool", mk({}, None, True)),
 ("headers-string", {"uri": "u", "request_headers": "a"}),
 ("vary-bool", mk({}, False)),
 ("vary-null-explicit", {"uri": "u", "request_headers": {}, "vary": None}),
 ("extra-key-ignored", mk({}, "a", extra=1)),
 ("top-list", ["uri"]),
 ("top-null", None),
 ("top-number", 3),
 ("many-members", mk({"c": "3", "B": "2"}, "e, d ,c,b,a")),
 ("long-value-unicode", mk({"a": "\u00e9\u4e2d\U0001f600"}, "a")),
]
def norm(r): return "REFUSE" if r is g.REFUSE else r
def mine(o):
    try: return m.key(o)
    except m.Refuse: return "REFUSE"
dis = 0
for lab, o in CASES:
    a, b = norm(g.reference(o)), mine(o)
    ok = a == b; dis += not ok
    print("%-30s %s ref=%r mine=%r" % (lab, "AGREE" if ok else "DISAGREE", a, b))
print("constructed=%d disagreements=%d" % (len(CASES), dis))
# wide fuzz
rng = random.Random(90)
NAMES = ["a", "A", "b", "%", "a%1f", "~", "_", "Z9", "k\u212a", "a b", "", "*", "x-y", "X-Y"]
VAL = ["x", " ", "\t", "%", GS, X, RS, US, "\r", "\n", "\x00", "\u00a0", ",", "1F", "\x0b"]
fd = 0; N = 20000; refused = 0
for i in range(N):
    h = {}
    for _ in range(rng.randint(0, 4)):
        n = "".join(c.swapcase() if rng.random() < .3 else c for c in rng.choice(NAMES))
        h[n] = "".join(rng.choice(VAL) for _ in range(rng.randint(0, 4))) if rng.random() < .95 else rng.choice([1, None, True])
    mem = [rng.choice(["", " ", "\t"]) + "".join(c.swapcase() if rng.random() < .3 else c for c in rng.choice(NAMES)) + rng.choice(["", " ", "\t "]) for _ in range(rng.randint(0, 4))]
    o = {"uri": "".join(rng.choice(["u", "%", US, GS, X, RS]) for _ in range(rng.randint(0, 4))), "request_headers": h}
    if mem or rng.random() < .5: o["vary"] = ",".join(mem)
    a, b = norm(g.reference(o)), mine(o)
    refused += a == "REFUSE"
    if a != b:
        fd += 1
        if fd < 5: print("FUZZ-DISAGREE", repr(o), a, b)
print("fuzz=%d seed=90 disagreements=%d ref_refused=%d" % (N, fd, refused))
print("gate generated population check: ", end="")
rng = random.Random(923161196); gd = 0; gref = 0
for i in range(2000):
    o = g.gen_case(rng); r = g.reference(o); gref += r is g.REFUSE; gd += norm(r) != mine(o)
print("n=2000 disagreements=%d refused=%d" % (gd, gref))
