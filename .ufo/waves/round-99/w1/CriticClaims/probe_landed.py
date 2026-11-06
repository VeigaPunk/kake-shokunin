#!/usr/bin/env python3
"""Attack the LANDED scripts/freshen_304.py at 998b6d5f on the escape-class inputs."""
import importlib.util, json, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SCRATCH = "/fast/scratch/hyaku/kake-r99/CriticClaims"
LANDED = SCRATCH + "/landed-freshen_304.py"
COUNTER = LANE + "/.ufo/waves/round-99/c99_fresh304.py"

spec = importlib.util.spec_from_file_location("c99f", COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ETAG = '"x"'
CASES = [
    ("p1-stored-hop-kept",
     {"stored": [{"id": "a", "received": 1, "headers": {"ETag": ETAG, "Keep-Alive": "t=5",
                                                        "TE": "trail", "Transfer-Encoding": "chunked",
                                                        "Connection": "close", "X-K": "v"}}],
      "response": {"status": 304, "headers": {"ETag": ETAG, "Date": "D"}}},
     "update/strong; stored hop-by-hop fields must REMAIN in the updated map"),
    ("p2-lm-tab-trim",
     {"stored": [{"id": "a", "received": 1, "headers": {"Last-Modified": "\tL1"}}],
      "response": {"status": 304, "headers": {"Last-Modified": "L1"}}},
     "update/weak; LM comparison trims spaces AND tabs"),
    ("p3-lm-tie-refusal",
     {"stored": [{"id": "a", "received": 3, "headers": {"ETag": 'W/"x"', "Last-Modified": "L"}},
                 {"id": "b", "received": 3, "headers": {"ETag": 'W/"x"', "Last-Modified": "L"}}],
      "response": {"status": 304, "headers": {"ETag": 'W/"x"', "Last-Modified": "L"}}},
     "refusal (LC3 ambiguous most recent; hand only covers the ETag-only tie)"),
    ("p4-age-copied",
     {"stored": [{"id": "a", "received": 1, "headers": {"ETag": ETAG}}],
      "response": {"status": 304, "headers": {"ETag": ETAG, "Age": "5"}}},
     "update/strong; Age must be copied (LC5: no other field excluded)"),
    ("p5-stored-malformed-etag-lm-only",
     {"stored": [{"id": "a", "received": 1, "headers": {"ETag": "abc", "Last-Modified": "L1"}}],
      "response": {"status": 304, "headers": {"Last-Modified": "L1"}}},
     "refusal (malformed ETag in a stored response, RFC 9110 8.8.3 via contract)"),
    ("p6-stored-case-dup-name",
     {"stored": [{"id": "a", "received": 1, "headers": {}}],
      "response": {"status": 304, "headers": {"ETag": ETAG, "ETAG": ETAG}}},
     "refusal (case-duplicate names in one map; hand covers response side only)"),
    ("p7-stored-bad-value-crlf",
     {"stored": [{"id": "a", "received": 1, "headers": {"ETag": ETAG, "X-Bad": "a\rb"}}],
      "response": {"status": 304, "headers": {"ETag": ETAG}}},
     "refusal (CR in a stored header value)"),
    ("p8-tie-below-top-ok-control",
     {"stored": [{"id": "a", "received": 3, "headers": {"ETag": 'W/"x"'}},
                 {"id": "b", "received": 3, "headers": {"ETag": 'W/"x"'}},
                 {"id": "c", "received": 6, "headers": {"ETag": 'W/"x"'}}],
      "response": {"status": 304, "headers": {"ETag": 'W/"x"'}}},
     "update/weak selecting c (control; must NOT refuse)"),
]


def run_cli(path, raw):
    r = subprocess.run([sys.executable, "-I", "-B", path], input=raw.encode(),
                       capture_output=True, cwd=SCRATCH + "/work2",
                       env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
                            "HOME": SCRATCH + "/work2", "TMPDIR": SCRATCH + "/work2"}, timeout=10)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


bad = 0
for name, inp, why in CASES:
    exp = m.ref_or_refusal(inp)
    rc, out, err = run_cli(LANDED, json.dumps(inp))
    if exp is None:
        ok = rc == 1 and out.strip() == "" and err.startswith("invalid_input:")
        obs = "rc=%d stdout=%r stderr=%r" % (rc, out[:40], err[:60])
        want = "refusal"
    else:
        got = json.loads(out) if rc == 0 and out.strip() else None
        ok = rc == 0 and got == exp
        obs = "rc=%d out=%s" % (rc, (json.dumps(got)[:160] if got else out[:60]))
        want = json.dumps(exp)[:160]
    print("%-34s %s  expected=%s\n    observed=%s" % (name, "OK" if ok else "DIVERGES", want, obs))
    if not ok:
        bad += 1
    print("    contract: %s" % why)

# invalid-JSON behavior (contract: invalid_input refusal)
rc, out, err = run_cli(LANDED, "{not json")
ok = rc == 1 and out.strip() == "" and err.startswith("invalid_input:")
print("%-34s %s  rc=%d stdout=%r stderr=%r" % ("p9-invalid-json-refusal", "OK" if ok else "DIVERGES",
                                               rc, out[:40], err[:60]))
if not ok:
    bad += 1
print("divergences=%d of %d probes" % (bad, len(CASES) + 1))
