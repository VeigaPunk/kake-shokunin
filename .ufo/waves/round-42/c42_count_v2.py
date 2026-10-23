#!/usr/bin/env python3
"""Round-42 C1 counter, version 2 (pre-freeze redesign of version 1, sha256 7bfc32c5...: exact ratio
comparison, T4 under random names and ids, scheme spelling in random case plus odd schemes, userinfo
units inserted in the password too, and run D of whole-value edits). Does a candidate
`scripts/sitemap_audit.py` keep the round-41 tool's
judgments (tool sha256 50287ac6..., the URL rule landed in round 41 and not admitted) while its CPU
cost on five timing shapes stays within 2.0 times the round-40 tool's (sha256 4de35f8c...)?

Usage (exit 0 met, 1 not met, 2 cannot evaluate; a receipt is written in every case):
  python3 -B .ufo/waves/round-42/c42_count_v2.py --root . --revision <rev> [--seed N] --out <receipt>
  python3 -B .ufo/waves/round-42/c42_count_v2.py --root . --tool-file <path> [--label L] [--seed N] --out <receipt>

Equality part. Four equality runs are generated per run from the seed (random when not given;
recorded in the receipt): (A) the round-41 counter-v2 case shapes (one inserted ASCII unit or percent
sequence at any position of one component of an http(s) URL, `loc` and `sitemapUrl`); (B) IP-literal
values whose bracket contents carry zero to three random edits (ASCII, non-ASCII, `%`, zone-id forms);
(C) long values (1,800-2,047 code points, non-ASCII included, one or many path segments) with zero
or one defect at any position, plus 40 `loc` of 2,048-6,000 and 16 `sitemapUrl` of 200,000 code points.
(D) 2,000 values of run-A shapes with one to three random edits at any position, scheme and
delimiters included. Every candidate timing repetition is compared with the round-41 output too.
The candidate and the round-41 tool each run once per equality run and once per generated timing
shape (T1, T2, T3, T5) and on the retained round-39 real run (T4); a run is equal when exit code and
stdout bytes are equal. No label other than the round-41 tool's output is used.

Timing part. For each of the five shapes the round-40 tool and the candidate run five times each,
alternating order. CPU time = user + system time of the tool and every descendant, read inside the
sandbox by a fixed runner (`RUNNER` below): it is a child subreaper, starts the tool with its fds
closed, reaps every orphan after the tool exits, then writes `exit utime stime` as the last line of
a timing file the counter reads. Ratio = median candidate / median round-40.
  T1 20,000 `loc` of 2,000-2,047 code points whose path, query or fragment is one long run without
     `/` (the round-41 performance review's adversarial shape), one defect in the last 64 positions
  T2 20,000 valid `loc` of 2,000-2,047 code points with percent triplets
  T3 50,000 valid `loc` of 60-140 code points
  T4 the retained round-39 real run (`.ufo/waves/round-41/realrun/`, SHA256SUMS verified), copied under
     random file names with random check ids
  T5 48 manifest checks whose `sitemapUrl` has 200,000 code points in one run without `/`
     (40 with a defect in the last 64 positions)
Values are distinct (a random token leads every path), so caching by value cannot help.

Sandbox: /usr/bin/bwrap with /usr, one case directory, the runner and the tool, --unshare-all,
--die-with-parent, --clearenv; bwrap itself starts with PATH only; stdin is /dev/null, stdout goes to
a file capped at 256 MiB (RLIMIT_FSIZE), stderr is discarded, address space 4 GiB, one run times out
at 600 s. Directory, file and id names are random and carry no case identity. A run without a
runner timing line has no CPU time, and a shape without a median has no ratio (not met).
"""
import argparse
import hashlib
import json
import os
import random
import resource
import statistics
import subprocess
import sys
import tempfile

PREDICATE = ("met: the tool's exit code and output equal the round-41 tool's on every generated run, "
             "and its median CPU time on each of the five timing shapes is at most 2.0 times the "
             "round-40 tool's")
RATIO_LIMIT = 2.0
REPS = 5
TOOL_PATH = "scripts/sitemap_audit.py"
REF41_REV = "1ef7a0e95f6884dd113fe583a997c633fe330ddd"
REF41_SHA = "50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d"
BASE40_REV = "8eb121c81ffebada064eefcabcd94dd2303d646f"
BASE40_SHA = "4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e"
REALRUN_DIR = ".ufo/waves/round-41/realrun"
BWRAP = "/usr/bin/bwrap"
RUN_TIMEOUT = 600
OUT_CAP = 256 * 1024 * 1024
AS_CAP = 4 * 1024 * 1024 * 1024

COMPONENTS = ("userinfo", "host", "port", "path", "query", "fragment")
LOC_UNITS = [chr(9), chr(10), chr(13)] + [chr(c) for c in range(0x20, 0x80)]
URL_UNITS = [chr(c) for c in range(0x00, 0x80)]
PCT_UNITS = ["%41", "%7e", "%4G", "%G4", "%", "%2"]
LOWER = "abcdefghijklmnopqrstuvwxyz"
ALNUM = LOWER + "0123456789"
HEX = "0123456789ABCDEFabcdef"
ODD_SCHEMES = ("ftp", "httpx", "h+ttp", "ht-tp", "HTTP.s", "file", "Http1")
TLDS = ("com", "net", "org", "example", "test", "io")
UNRESERVED = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
SUB_DELIMS = "!$&'()*+,;="
FILL = {"userinfo": UNRESERVED + SUB_DELIMS + ":", "host": UNRESERVED + SUB_DELIMS,
        "path": UNRESERVED + SUB_DELIMS + ":@", "query": UNRESERVED + SUB_DELIMS + ":@/?",
        "fragment": UNRESERVED + SUB_DELIMS + ":@/?"}
NON_ASCII = "\u00a0\u00e9\u00fc\u0101\u03bb\u0416\u05d0\u4e2d\u3042\uac00\ufb01\U0001f600\U00010348"
DEFECTS = ["%", "%G", "%4", "%4G", " ", "|", "^", "`", "{", "}", "\\", '"', "<", ">", "[", "]", "\t"]
BRACKET_EDITS = [chr(c) for c in range(0x00, 0x80)] + list(NON_ASCII) + ["%25", "%", "%2", "%eth0",
                                                                          "%25en1", "%e9", "%\u00e9", "|"]


class CannotEvaluate(Exception):
    pass


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], check=True, capture_output=True,
                          stdin=subprocess.DEVNULL).stdout


def tok(rng, lo=4, hi=8):
    return rng.choice(LOWER) + "".join(rng.choice(ALNUM) for _ in range(rng.randint(lo, hi) - 1))

def rcase(rng, word):
    """`word` with each letter in random case (scheme spelling: RFC 3986 schemes are case-insensitive)."""
    return "".join(ch.upper() if rng.random() < 0.3 else ch for ch in word)



def fill(rng, comp, lo=4, hi=10):
    out = [rng.choice(ALNUM), rng.choice(ALNUM)]
    for _ in range(rng.randint(lo, hi) - 2):
        roll = rng.random()
        if roll < 0.1:
            out.append("%" + "".join(rng.choice(HEX) for _ in range(2)))
        elif roll < 0.55:
            out.append(rng.choice(FILL[comp]))
        else:
            out.append(rng.choice(ALNUM))
    return "".join(out)


def insert(rng, text, unit):
    i = rng.randint(0, len(text))
    return text[:i] + unit + text[i:]


def ip_literal(rng):
    groups = [format(rng.randint(0, 0xffff), rng.choice(("x", "X", "04x"))) for _ in range(8)]
    kind = rng.randrange(6)
    if kind == 0:
        return ":".join(groups)
    if kind == 1:
        cut = rng.randint(0, 6)
        return ":".join(groups[:cut]) + "::" + ":".join(groups[cut + 2:])
    if kind == 2:
        return "::ffff:192.0.2." + str(rng.randint(1, 254))
    if kind == 3:
        return rng.choice(("::1", "::", "2001:db8::", "fe80::" + groups[0]))
    if kind == 4:
        return "fe80::" + groups[1] + rng.choice(("%25", "%")) + tok(rng, 2, 6)
    return "v" + format(rng.randint(1, 15), "x") + "." + "".join(rng.choice(ALNUM) for _ in range(rng.randint(1, 6)))


def maybe_empty(rng, comp, p_empty=0.15):
    return "" if rng.random() < p_empty else fill(rng, comp)


def make_url(rng, target, unit):
    """Round-41 counter-v2 URL shape: `unit` at any position of component `target`."""
    scheme = rcase(rng, rng.choice(("http", "https"))) if rng.random() > 0.03 else rng.choice(ODD_SCHEMES)
    userinfo = None
    if target == "userinfo" or rng.random() < 0.1:
        first = maybe_empty(rng, "host")
        password = maybe_empty(rng, "userinfo") if rng.random() < 0.5 else None
        if target == "userinfo":
            if password is not None and rng.random() < 0.5:
                password = insert(rng, password, unit)
            else:
                first = insert(rng, first, unit)
        userinfo = first + (":" + password if password is not None else "")
    roll = rng.random()
    if target == "host" or roll < 0.8:
        host = fill(rng, "host") + "." + rng.choice(TLDS)
        if target == "host":
            host = insert(rng, host, unit)
    elif roll < 0.9:
        host = "192.0.2." + str(rng.randint(1, 254))
    else:
        host = "[" + ip_literal(rng) + "]"
    port = None
    if target == "port" or rng.random() < 0.1:
        port = "" if (target != "port" and rng.random() < 0.2) else str(rng.randint(10, 99))
        if target == "port":
            port = insert(rng, port, unit)
    if target != "path" and rng.random() < 0.1:
        segments = []
    else:
        segments = [maybe_empty(rng, "path", 0.1) for _ in range(rng.randint(1, 3))]
    if target == "path":
        k = rng.randrange(len(segments))
        segments[k] = insert(rng, segments[k], unit)
    query = None
    if target == "query" or rng.random() < 0.4:
        query = maybe_empty(rng, "query")
        if target == "query":
            query = insert(rng, query, unit)
    fragment = None
    if target == "fragment" or rng.random() < 0.2:
        fragment = maybe_empty(rng, "fragment")
        if target == "fragment":
            fragment = insert(rng, fragment, unit)
    url = scheme + "://" + (userinfo + "@" if userinfo is not None else "") + host
    url += (":" + port if port is not None else "") + ("/" + "/".join(segments) if segments else "")
    url += ("?" + query if query is not None else "") + ("#" + fragment if fragment is not None else "")
    return url


def xml_legal(ch):
    o = ord(ch)
    return o in (9, 10, 13) or 0x20 <= o <= 0xD7FF or 0xE000 <= o <= 0xFFFD or 0x10000 <= o <= 0x10FFFF


def xml_text(rng, value):
    out = []
    for ch in value:
        if ch in "&<>\"'" or ord(ch) < 0x20 or ord(ch) == 0x7F or (not ch.isalnum() and rng.random() < 0.3):
            out.append(("&#%d;" % ord(ch)) if rng.random() < 0.5 else ("&#x%X;" % ord(ch)))
        else:
            out.append(ch)
    return "".join(out)


def fast_xml(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- equality runs

def cases_a(rng):
    specs = [("loc", c, u) for c in COMPONENTS for u in LOC_UNITS + PCT_UNITS]
    specs += [("sitemapUrl", c, u) for c in COMPONENTS for u in URL_UNITS + PCT_UNITS]
    return [{"field": f, "value": make_url(rng, c, u)} for f, c, u in specs]


def bracket_value(rng):
    body = ip_literal(rng)
    for _ in range(rng.randint(0, 3)):
        roll = rng.random()
        if roll < 0.6 or not body:
            body = insert(rng, body, rng.choice(BRACKET_EDITS))
        elif roll < 0.8:
            i = rng.randrange(len(body))
            body = body[:i] + body[i + 1:]
        else:
            i = rng.randrange(len(body))
            body = body[:i] + body[i] + body[i:]
    tail = "/" + fill(rng, "path") if rng.random() < 0.8 else ""
    port = (":" + str(rng.randint(1, 65535))) if rng.random() < 0.2 else ""
    return rcase(rng, rng.choice(("http", "https"))) + "://[" + body + "]" + port + tail


def cases_b(rng):
    out = []
    for field in ("loc", "sitemapUrl"):
        for _ in range(600):
            v = bracket_value(rng)
            if field == "loc":
                v = "".join(ch for ch in v if xml_legal(ch))
            out.append({"field": field, "value": v})
    return out


def long_body(rng, n, alphabet, pct=0.05, non_ascii=0.0):
    chars = rng.choices(alphabet, k=n)
    for j in rng.sample(range(n), int(n * non_ascii)):
        chars[j] = rng.choice(NON_ASCII)
    for j in rng.sample(range(n), int(n * pct)):
        chars[j] = "%" + rng.choice(HEX) + rng.choice(HEX)
    return "".join(chars)


def long_value(rng, length, defect, non_ascii=0.0, defect_window=None, slashes=True):
    """A distinct http(s) value of exactly `length` code points or a little less; with `defect`,
    one unit of DEFECTS inserted at a position at or after the path start (within the last
    `defect_window` positions when given). Without `slashes` the path body is one segment."""
    unit = rng.choice(DEFECTS) if defect else ""
    target = length - len(unit)
    head = rcase(rng, rng.choice(("http", "https"))) + "://" + tok(rng) + "." + rng.choice(TLDS) + "/" + tok(rng, 8, 12) + "/"
    room = max(10, target - len(head))
    kind = rng.random()
    if kind < 0.6:
        body = long_body(rng, room, FILL["path"] + ("/" if slashes else ""), 0.04, non_ascii)
    elif kind < 0.8:
        body = long_body(rng, 8, FILL["path"], 0.04, non_ascii) + "?" + long_body(rng, room - 9, FILL["query"], 0.04, non_ascii)
    else:
        body = long_body(rng, 8, FILL["path"], 0.04, non_ascii) + "#" + long_body(rng, room - 9, FILL["fragment"], 0.04, non_ascii)
    value = (head + body)[:target]
    cut = value.find("%", max(len(head), len(value) - 2))   # never end inside a percent triplet
    if cut != -1:
        value = value[:cut]
    if defect:
        lo = len(head) if defect_window is None else max(len(head), len(value) - defect_window)
        i = rng.randint(lo, len(value))
        value = value[:i] + unit + value[i:]
    return value


def cases_d(rng):
    """Whole-value random edits (any position, scheme and delimiters included) of run-A shapes."""
    out = []
    units = LOC_UNITS + PCT_UNITS + list(NON_ASCII) + ["://", "//", "@", ":", "[", "]", "%25"]
    for field in ("loc", "sitemapUrl"):
        for _ in range(1000):
            v = make_url(rng, rng.choice(COMPONENTS), rng.choice(ALNUM))
            for _ in range(rng.randint(1, 3)):
                roll = rng.random()
                if roll < 0.6 or len(v) < 2:
                    v = insert(rng, v, rng.choice(units))
                elif roll < 0.8:
                    i = rng.randrange(len(v))
                    v = v[:i] + v[i + 1:]
                else:
                    i = rng.randrange(len(v))
                    v = v[:i] + v[i] + v[i:]
            if field == "loc":
                v = "".join(ch for ch in v if xml_legal(ch))
            out.append({"field": field, "value": v})
    return out


def cases_c(rng):
    out = []
    for field, n in (("loc", 400), ("sitemapUrl", 200)):
        for _ in range(n):
            v = long_value(rng, rng.randint(1800, 2047), rng.random() < 0.6, non_ascii=rng.choice((0.0, 0.02)),
                           slashes=rng.random() < 0.5)
            out.append({"field": field, "value": v})
    # beyond the timing shapes: defects at any position of very long values
    for _ in range(40):
        out.append({"field": "loc", "value": long_value(rng, rng.randint(2048, 6000), rng.random() < 0.7,
                                                         slashes=rng.random() < 0.5)})
    for _ in range(16):
        out.append({"field": "sitemapUrl", "value": long_value(rng, 200000, rng.random() < 0.7,
                                                                slashes=rng.random() < 0.5)})
    return out


def layout_cases(rng, cases, cd):
    """Manifest plus sitemap files for equality cases (round-41 counter-v2 layout)."""
    def name():
        return "%x" % rng.getrandbits(64)

    used = set()

    def fresh_id():
        while True:
            v = tok(rng, 6, 12)
            if v not in used:
                used.add(v)
                return v

    def urlset(values):
        body = "".join("<url><loc>%s</loc></url>" % xml_text(rng, v) for v in values)
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % body)

    shared = name() + ".xml"
    with open(os.path.join(cd, shared), "w", encoding="utf-8") as fh:
        fh.write(urlset(["https://%s.com/%s/%s" % (tok(rng), tok(rng), tok(rng))]))
    checks = []
    locs = [c["value"] for c in cases if c["field"] == "loc"]
    groups = []
    while locs:
        n = rng.randint(20, 60)
        groups.append(locs[:n])
        locs = locs[n:]
    items = [("g", g) for g in groups] + [("u", c["value"]) for c in cases if c["field"] == "sitemapUrl"]
    rng.shuffle(items)
    for kind, payload in items:
        if kind == "g":
            fname = name() + ".xml"
            with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
                fh.write(urlset(payload))
            # half the groups share host and directory with their first value, so scope findings vary
            first = payload[0]
            if rng.random() < 0.5 and first.lower().startswith(("http://", "https://")):
                smu = first[:first.find("/", first.find("//") + 2) + 1 or len(first)] + "sitemap.xml"
            else:
                smu = "https://%s.%s/%s/sitemap.xml" % (tok(rng), rng.choice(TLDS), tok(rng))
            checks.append({"id": fresh_id(), "file": fname, "sitemapUrl": smu})
        else:
            checks.append({"id": fresh_id(), "file": shared, "sitemapUrl": payload})
    mname = name() + ".json"
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": checks}, fh)
    return mname


# ---------------------------------------------------------------- timing shapes

def write_single(rng, cd, values):
    """One sitemap (fast escaping; values are XML-legal) and a one-check manifest."""
    fname = "%x.xml" % rng.getrandbits(64)
    with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for v in values:
            fh.write("<url><loc>" + fast_xml(v) + "</loc></url>")
        fh.write("</urlset>\n")
    host = values[0].split("/")[2] if values else "example.com"
    mname = "%x.json" % rng.getrandbits(64)
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": [{"id": tok(rng, 6, 10), "file": fname,
                                             "sitemapUrl": "https://%s/sitemap.xml" % host}]}, fh)
    return mname


def shape_t1(rng, cd):
    return write_single(rng, cd, [long_value(rng, rng.randint(2000, 2047), True, defect_window=64,
                                             slashes=False) for _ in range(20000)])


def shape_t2(rng, cd):
    return write_single(rng, cd, [long_value(rng, rng.randint(2000, 2047), False) for _ in range(20000)])


def shape_t3(rng, cd):
    return write_single(rng, cd, [long_value(rng, rng.randint(60, 140), False) for _ in range(50000)])


def shape_t5(rng, cd):
    fname = "%x.xml" % rng.getrandbits(64)
    with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/'
                 'sitemap/0.9"><url><loc>https://a.example/x</loc></url></urlset>\n')
    checks = []
    for k in range(48):
        checks.append({"id": "%s%d" % (tok(rng, 4, 6), k), "file": fname,
                       "sitemapUrl": long_value(rng, 200000, k < 40, defect_window=64, slashes=False)})
    rng.shuffle(checks)
    mname = "%x.json" % rng.getrandbits(64)
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": checks}, fh)
    return mname


def shape_t4(root, cd, rng):
    """The retained real run, copied under random file names with random check ids (QUALITY (r))."""
    src = os.path.join(root, REALRUN_DIR)
    sums = {}
    for line in open(os.path.join(src, "SHA256SUMS"), encoding="utf-8"):
        digest, path = line.split(None, 1)
        sums[path.strip().lstrip("*")] = digest
    blobs = {}
    for rel, digest in sums.items():
        data = open(os.path.join(src, rel), "rb").read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise CannotEvaluate("real-run input %s sha256 mismatch" % rel)
        blobs[rel] = data
    if "manifest.json" not in blobs:
        raise CannotEvaluate("real-run manifest not in SHA256SUMS")
    manifest = json.loads(blobs.pop("manifest.json").decode("utf-8"))
    sub = "%x" % rng.getrandbits(40)
    os.makedirs(os.path.join(cd, sub))
    renamed = {}
    for check in manifest["checks"]:
        rel = check["file"]
        if rel not in blobs:
            raise CannotEvaluate("real-run file %s not in SHA256SUMS" % rel)
        if rel not in renamed:
            renamed[rel] = sub + "/%x.xml" % rng.getrandbits(48)
            with open(os.path.join(cd, renamed[rel]), "wb") as fh:
                fh.write(blobs[rel])
        check["file"] = renamed[rel]
        check["id"] = tok(rng, 6, 12)
    mname = "%x.json" % rng.getrandbits(64)
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)
    return mname


# ---------------------------------------------------------------- sandbox

RUNNER = r'''
import ctypes, os, resource, subprocess, sys
fd = int(sys.argv[1])
ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0)       # PR_SET_CHILD_SUBREAPER
p = subprocess.Popen(sys.argv[2:], stdin=subprocess.DEVNULL, close_fds=True)
code = p.wait()
while True:
    try:
        os.wait()
    except ChildProcessError:
        break
r = resource.getrusage(resource.RUSAGE_CHILDREN)
os.write(fd, ("\n%d %.6f %.6f\n" % (code, r.ru_utime, r.ru_stime)).encode())
sys.exit(code if code >= 0 else 128 - code)
'''


def _limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUT_CAP, OUT_CAP))
    resource.setrlimit(resource.RLIMIT_AS, (AS_CAP, AS_CAP))


class Sandbox:
    def __init__(self, rng, td):
        self.rng = rng
        self.td = td
        self.runner = os.path.join(td, "%x.py" % rng.getrandbits(48))
        with open(self.runner, "w") as fh:
            fh.write(RUNNER)

    def run(self, tool, cd, mname):
        """Return (exit, stdout bytes, cpu seconds or None) of one tool run."""
        rng = self.rng
        work = "/%x" % rng.getrandbits(40)
        tname = "/%x/%x.py" % (rng.getrandbits(40), rng.getrandbits(40))
        rname = "/%x/%x.py" % (rng.getrandbits(40), rng.getrandbits(40))
        out_path = os.path.join(self.td, "%x.out" % rng.getrandbits(48))
        time_path = os.path.join(self.td, "%x.t" % rng.getrandbits(48))
        try:
            with open(out_path, "wb") as out, open(time_path, "wb") as tfh:
                tfd = tfh.fileno()
                argv = [BWRAP, "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
                        "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin",
                        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                        "--ro-bind", cd, work, "--ro-bind", tool, tname,
                        "--ro-bind", self.runner, rname, "--chdir", work,
                        "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
                        "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8",
                        "/usr/bin/python3", "-B", rname, str(tfd),
                        "/usr/bin/python3", "-B", tname, "--manifest", work + "/" + mname]
                p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=out,
                                     stderr=subprocess.DEVNULL, cwd=self.td, pass_fds=(tfd,),
                                     env={"PATH": "/usr/bin"}, preexec_fn=_limits)
                try:
                    code = p.wait(timeout=RUN_TIMEOUT)
                except subprocess.TimeoutExpired:
                    p.kill()
                    p.wait()
                    code = "timeout"
        except OSError as ex:
            raise CannotEvaluate("sandbox: %s" % ex)
        with open(out_path, "rb") as fh:
            data = fh.read(OUT_CAP + 1)
        with open(time_path, "rb") as fh:
            lines = fh.read(1 << 20).split(b"\n")
        os.unlink(out_path)
        os.unlink(time_path)
        cpu = None
        last = [x for x in lines if x.strip()]
        if code != "timeout" and last:
            try:
                _, ut, st = last[-1].split()
                cpu = float(ut) + float(st)
            except ValueError:
                cpu = None
        return code, data, cpu


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revision")
    src.add_argument("--tool-file")
    ap.add_argument("--label", default="")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    rec = {"predicate": PREDICATE, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
           "revision": None, "toolFile": a.tool_file, "label": a.label, "seed": seed,
           "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "ref41Sha256": REF41_SHA, "base40Sha256": BASE40_SHA, "toolSha256": None,
           "equalRuns": None, "equalValues": None, "runs": {}, "ratios": {}, "ratiosExact": {}, "note": None}

    def finish(code):
        s = json.dumps(rec, indent=1)
        if a.out:
            with open(a.out, "w") as fh:
                fh.write(s + "\n")
        print(json.dumps({k: rec[k] for k in ("label", "revision", "toolSha256", "equalRuns",
                                              "ratios", "met", "note")}))
        sys.exit(code)

    try:
        if not os.access(BWRAP, os.X_OK):
            raise CannotEvaluate("bwrap missing at %s" % BWRAP)
        refs = {}
        for key, rev, sha in (("ref41", REF41_REV, REF41_SHA), ("base40", BASE40_REV, BASE40_SHA)):
            data = git(root, "show", "%s:%s" % (rev, TOOL_PATH))
            if hashlib.sha256(data).hexdigest() != sha:
                raise CannotEvaluate("%s tool sha256 mismatch" % key)
            refs[key] = data
        if a.revision:
            rev = git(root, "rev-parse", "--verify", "%s^{commit}" % a.revision).decode().strip()
            rec["revision"] = rev
            try:
                cand = git(root, "show", "%s:%s" % (rev, TOOL_PATH))
            except subprocess.CalledProcessError:
                cand = None
        else:
            try:
                cand = open(a.tool_file, "rb").read()
            except OSError:
                cand = None
        rec["toolSha256"] = hashlib.sha256(cand).hexdigest() if cand is not None else None
        rng = random.Random(seed)
        with tempfile.TemporaryDirectory(prefix="%x-" % rng.getrandbits(32)) as td:
            paths = {}
            for key, data in (("ref41", refs["ref41"]), ("base40", refs["base40"]), ("cand", cand)):
                if data is None:
                    continue
                paths[key] = os.path.join(td, "%x.py" % rng.getrandbits(48))
                with open(paths[key], "wb") as fh:
                    fh.write(data)
            box = Sandbox(rng, td)
            runs = [("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d),
                    ("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]
            equal = 0
            values = 0
            for key, gen in runs:
                cd = os.path.join(td, "%x" % rng.getrandbits(48))
                os.makedirs(cd)
                if key in ("A", "B", "C", "D"):
                    cases = gen(rng)
                    mname = layout_cases(rng, cases, cd)
                    n = len(cases)
                elif key == "T4":
                    mname = shape_t4(root, cd, rng)
                    n = None
                else:
                    mname = gen(rng, cd)
                    n = None
                ref_code, ref_out, ref_cpu = box.run(paths["ref41"], cd, mname)
                entry = {"values": n, "ref41Exit": ref_code, "ref41OutSha256": hashlib.sha256(ref_out).hexdigest()}
                if "cand" in paths:
                    c_code, c_out, c_cpu = box.run(paths["cand"], cd, mname)
                    entry.update(candExit=c_code, candOutSha256=hashlib.sha256(c_out).hexdigest())
                    entry["equal"] = (c_code == ref_code and c_out == ref_out)
                else:
                    entry["equal"] = False
                    entry["candExit"] = "tool absent"
                if key.startswith("T"):
                    base_t, cand_t = [], []
                    reps_equal = 0
                    for i in range(REPS):
                        order = ("base40", "cand") if i % 2 == 0 else ("cand", "base40")
                        for who in order:
                            if who not in paths:
                                continue
                            code, out, cpu = box.run(paths[who], cd, mname)
                            (base_t if who == "base40" else cand_t).append(cpu)
                            if who == "cand":
                                reps_equal += (code == ref_code and out == ref_out)
                    entry["base40Cpu"] = base_t
                    entry["candCpu"] = cand_t
                    entry["candRepsEqual"] = "%d/%d" % (reps_equal, REPS)
                    entry["equal"] = entry["equal"] and reps_equal == REPS
                    if None in base_t or not base_t:
                        raise CannotEvaluate("round-40 tool gave no CPU time on %s" % key)
                    if cand_t and None not in cand_t and statistics.median(base_t) > 0:
                        exact = statistics.median(cand_t) / statistics.median(base_t)
                        rec["ratiosExact"][key] = exact
                        rec["ratios"][key] = round(exact, 3)
                    else:
                        rec["ratios"][key] = None
                equal += entry["equal"]
                if n is not None and entry["equal"]:
                    values += n
                rec["runs"][key] = entry
            rec["equalRuns"] = "%d/%d" % (equal, len(runs))
            rec["equalValues"] = values
            ratios_ok = len(rec["ratiosExact"]) == 5 and all(r <= RATIO_LIMIT for r in rec["ratiosExact"].values())
            rec["met"] = (equal == len(runs)) and len(rec["ratios"]) == 5 and ratios_ok
            rec["note"] = None if "cand" in paths else "tool absent"
    except CannotEvaluate as ex:
        rec["note"] = "cannot evaluate: %s" % ex
        finish(2)
    except Exception as ex:                      # a receipt in every case
        rec["note"] = "cannot evaluate: %s: %s" % (type(ex).__name__, str(ex)[:300])
        finish(2)
    finish(0 if rec["met"] else 1)


if __name__ == "__main__":
    main()
