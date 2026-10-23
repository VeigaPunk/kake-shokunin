#!/usr/bin/env python3
"""Round-43 counter v4 = round-42 counter v3 + the round-42 lesson Mistake-5 fix criteria,
frozen before any seat scores (routed closure repair 2). Applied 2026-10-23 by the kake L1.

Changes over c42_count_v3.py (sha256 ce2d5a0c...):
1. New equality run F with the two named coverage classes: 6+-digit ports (out-of-range and
   zero-padded in-range, otherwise clean so a port-truncating tool's answer differs) and
   repetition classes (case-fold pairs under a sitemapUrl cased to the first member's first
   path segment, tail-defective shared-prefix pairs in both orders, repeated-host blocks,
   common-host values on the four hosts tabled by the round-42 control CtlFreshCache/v4_hosttable
   plus a wider basket).
2. Timing shapes carry the same classes: T1 clean values with out-of-range long ports; T2
   rewritten as 20 scoped files x 1,000 values sharing host and first path segment, opening
   with a case-fold pair (sitemapUrl cased to that segment); T3 repeated-host blocks,
   common-host values, clean long-port values and tail-defective prefix pairs; T5 clean
   long-port sitemapUrls on 3 of 48 checks. T4 (retained real run) is byte-fixed and keeps
   its natural repetition (identical-value repeats only, per the round-42 seat analysis).
The PREDICATE sentence, RATIO_LIMIT, REPS, sandbox and scoring protocol are unchanged.
"""
import pathlib

SRC = pathlib.Path(__file__).resolve().parent / ".." / "round-42" / "c42_count_v3.py"
DST = pathlib.Path(__file__).resolve().parent / "c43_count_v4.py"
s = SRC.read_text()

# 1. docstring: mark the version
old_head = """#!/usr/bin/env python3
\"\"\"Round-42 C1 counter, version 3"""
new_head = """#!/usr/bin/env python3
\"\"\"Round-43 C1 counter, version 4 (frozen before any seat scores; built from the round-42
counter version 3, sha256 ce2d5a0c..., by .ufo/waves/round-43/build_v4.py). Adds run F and the
timing-shape repetition classes of the round-42 lesson Mistake-5 fix criteria: 6+-digit ports
and repetition classes (case-fold pairs, shared-prefix pairs, repeated hosts, common-host
tables). The predicate sentence, ratio limit, reps, sandbox and scoring protocol are unchanged
from version 3. Round-42 version 3 header follows for provenance:

Round-42 C1 counter, version 3"""
assert s.startswith(old_head)
s = s.replace(old_head, new_head, 1)

old_eq = "Equality part. Five equality runs are generated per run from the seed"
new_eq = ("Equality part. Six equality runs are generated per run from the seed "
          "(A-E as version 3, plus F: the Mistake-5 classes). Version 3 had five equality runs")
assert old_eq in s
s = s.replace(old_eq, new_eq, 1)

# 2. new generators before cases_d
anchor = '''def cases_d(rng):
    """Whole-value random edits (any position, scheme and delimiters included) of run-A shapes."""'''
assert anchor in s
helpers = '''# ---------------------------------------------------------------- run F (round 43)

COMMON_HOSTS = ("localhost", "example.invalid", "sitemaps.invalid", "test.invalid",
                "localhost.localdomain", "example.com", "example.net", "example.org",
                "www.example.com", "www.example.net", "www.example.org", "127.0.0.1",
                "::1", "www.w3.org", "schema.org", "www.ietf.org")
CASE_INVARIANT_DEFECTS = ["%", "%4", " ", "|", "^", "`", "{", "}", "\\\\", '"', "<", ">", "[", "]", "\\t"]


def long_port(rng, out_of_range=None):
    """A 6-10 digit port. Out-of-range (>= 100000) by default: the round-41 tool rejects via
    urlsplit's port range while a tool that reads at most five digits accepts. Zero-padded
    in-range forms exercise the port loop without an output difference of their own."""
    if out_of_range is None:
        out_of_range = rng.random() < 0.7
    if out_of_range:
        return str(rng.randint(100000, 9999999999))
    return str(rng.randint(0, 65535)).zfill(rng.randint(6, 8))


def short_url(rng, host=None, port=None, defect=False):
    """A short http(s) value: `host` (random reg-name when None), optional `port`, one or two
    path segments, optional query/fragment, one case-invariant defect after the path start
    when `defect`."""
    scheme = rcase(rng, rng.choice(("http", "https")))
    host = host or (fill(rng, "host", 3, 8) + "." + rng.choice(TLDS))
    v = scheme + "://" + host
    if port is not None:
        v += ":" + port
    v += "/" + tok(rng, 4, 8)
    if rng.random() < 0.3:
        v += "/" + tok(rng, 3, 7)
    if rng.random() < 0.3:
        v += "?" + fill(rng, "query", 3, 8)
    if rng.random() < 0.2:
        v += "#" + fill(rng, "fragment", 3, 8)
    if defect:
        i = rng.randrange(v.find("/") + 1, len(v))
        v = v[:i] + rng.choice(CASE_INVARIANT_DEFECTS) + v[i:]
    return v


def fold_pair(rng):
    """Two clean values that fold to one key under upper-to-lower folding: same scheme, host,
    tail; the first path segment of `a` carries one upper-cased letter, `b` is all-lower."""
    scheme = rcase(rng, rng.choice(("http", "https")))
    host = fill(rng, "host", 3, 8) + "." + rng.choice(TLDS)
    seg = tok(rng, 8, 12)
    j = rng.randrange(len(seg))
    seg_a = seg[:j] + seg[j].upper() + seg[j + 1:]
    tail = "/" + tok(rng, 4, 8) if rng.random() < 0.5 else ""
    suffix = ("?" + fill(rng, "query", 3, 8)) if rng.random() < 0.3 else ""
    a = scheme + "://" + host + "/" + seg_a + tail + suffix
    b = scheme + "://" + host + "/" + seg + tail + suffix
    return a, b


def prefix_pair(rng):
    """Two values sharing the first `cut` (36-44) code points: `bad` carries one case-invariant
    defect at position cut, `good` is clean past cut, in first-seen order random. A cache keyed
    on the first 32 code points answers the second from the first."""
    base = short_url(rng)
    while len(base) < 50:
        base += "/" + tok(rng, 6, 10)
    cut = rng.randint(36, 44)
    bad = base[:cut] + rng.choice(CASE_INVARIANT_DEFECTS)
    good = base[:cut] + tok(rng, 4, 9)
    if rng.random() < 0.5:
        return bad, good
    return good, bad


def cases_f(rng):
    """Run F (equality): 6+-digit ports and the four repetition classes of the Mistake-5 fix.
    Yields layout units: ("value", field, v), ("foldpair", a, b), ("prefixpair", a, b),
    ("pairfile", a, b, c, d, e, f). Returns (units, value_count)."""
    units = []
    n = 0
    for _ in range(120):
        units.append(("value", "loc", short_url(rng, port=long_port(rng)))); n += 1
    for _ in range(120):
        units.append(("value", "sitemapUrl", short_url(rng, port=long_port(rng)))); n += 1
    for _ in range(120):
        a, b = fold_pair(rng)
        units.append(("foldpair", a, b)); n += 2
    for _ in range(120):
        a, b = prefix_pair(rng)
        units.append(("prefixpair", a, b)); n += 2
    for _ in range(40):
        a1, b1 = fold_pair(rng)
        a2, b2 = fold_pair(rng)
        a3, b3 = prefix_pair(rng)
        units.append(("pairfile", a1, b1, a2, b2, a3, b3)); n += 6
    for _ in range(8):
        host = fill(rng, "host", 3, 8) + "." + rng.choice(TLDS)
        for _ in range(50):
            units.append(("value", "loc", short_url(rng, host=host, defect=rng.random() < 0.4)))
            n += 1
    for _ in range(150):
        units.append(("value", "loc", short_url(rng, host=rng.choice(COMMON_HOSTS),
                                                defect=rng.random() < 0.5))); n += 1
    for _ in range(150):
        units.append(("value", "sitemapUrl", short_url(rng, host=rng.choice(COMMON_HOSTS),
                                                       defect=rng.random() < 0.5))); n += 1
    return units, n


def segment_smu(rng, first):
    """The sitemapUrl naming the directory of `first`'s first path segment exactly as written
    (case-sensitive), so a value whose first-segment casing differs is out-of-scope."""
    if not first.lower().startswith(("http://", "https://")):
        return "https://%s.%s/%s/sitemap.xml" % (tok(rng), rng.choice(TLDS), tok(rng))
    start = first.find("/", first.find("//") + 2)
    if start < 0:
        return first + "/sitemap.xml"
    end = first.find("/", start + 1)
    if end < 0:
        return first + "/sitemap.xml"
    return first[:end] + "/sitemap.xml"


def layout_f(rng, units, cd):
    """Run F layout: one manifest for every unit so a process-global result cache must answer
    each class. A fold pair shares one file and one segment-cased sitemapUrl: the round-41
    tool flags the second member out_of_scope (case-sensitive first-segment compare), a
    case-fold cache answers it in-scope. Other units get their own file (or the shared file
    for sitemapUrl) with the sitemapUrl derived as in the round-42 layout."""
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
        return ('<?xml version="1.0" encoding="UTF-8"?>\\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\\n' % body)

    def derived_smu(first):
        if first.lower().startswith(("http://", "https://")):
            return first[:first.find("/", first.find("//") + 2) + 1 or len(first)] + "sitemap.xml"
        return "https://%s.%s/%s/sitemap.xml" % (tok(rng), rng.choice(TLDS), tok(rng))

    shared = name() + ".xml"
    with open(os.path.join(cd, shared), "w", encoding="utf-8") as fh:
        fh.write(urlset(["https://%s.com/%s/%s" % (tok(rng), tok(rng), tok(rng))]))
    checks = []
    for unit in units:
        kind = unit[0]
        if kind == "value":
            _, field, v = unit
            if field == "loc":
                fname = name() + ".xml"
                with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
                    fh.write(urlset([v]))
                checks.append({"id": fresh_id(), "file": fname, "sitemapUrl": derived_smu(v)})
            else:
                checks.append({"id": fresh_id(), "file": shared, "sitemapUrl": v})
        elif kind in ("foldpair", "prefixpair"):
            _, a, b = unit
            fname = name() + ".xml"
            with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
                fh.write(urlset([a, b]))
            smu = segment_smu(rng, a) if kind == "foldpair" else derived_smu(a)
            checks.append({"id": fresh_id(), "file": fname, "sitemapUrl": smu})
        else:  # pairfile
            vals = list(unit[1:])
            fname = name() + ".xml"
            with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
                fh.write(urlset(vals))
            checks.append({"id": fresh_id(), "file": fname, "sitemapUrl": segment_smu(rng, vals[0])})
    mname = name() + ".json"
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": checks}, fh)
    return mname


def with_long_port(rng, v):
    """Insert an out-of-range 6-10 digit port after the authority, keeping the length."""
    mark = v.find("//")
    if mark < 0:
        return v
    end = len(v)
    for delim in ("/", "?", "#"):
        cut = v.find(delim, mark + 2)
        if 0 <= cut < end:
            end = cut
    ins = ":" + long_port(rng, out_of_range=True)
    if end == len(v):
        return v + ins
    return v[:end] + ins + v[end:len(v) - len(ins)]


def long_tail_value(rng, scheme, host, seg, defect):
    """A 2,000-2,047 cp value `scheme://host/seg/<long percent-carrying tail>` with the
    round-42 T2 defect rate applied after the path start."""
    length = rng.randint(2000, 2047)
    head = scheme + "://" + host + "/" + seg + "/"
    unit = rng.choice(DEFECTS) if defect else ""
    room = max(10, length - len(head) - len(unit))
    body = long_body(rng, room, FILL["path"] + "/", 0.04, 0.0)
    value = (head + body)[:length - len(unit)]
    cut = value.find("%", max(len(head), len(value) - 2))
    if cut != -1:
        value = value[:cut]
    if defect:
        i = rng.randint(len(head), len(value))
        value = value[:i] + unit + value[i:]
    return value


def shape_t2(rng, cd):
    """20 scoped files x 1,000 values (count unchanged) sharing scheme, host and first path
    segment; each file opens with a case-fold pair under a segment-cased sitemapUrl, and 2%
    of the remaining values carry a clean long-port variant (round-43 classes)."""
    p = rng.uniform(0.01, 0.03)
    last = None
    for _ in range(20):
        scheme = rcase(rng, rng.choice(("http", "https")))
        host = tok(rng) + "." + rng.choice(TLDS)
        seg = tok(rng, 8, 12)
        j = rng.randrange(len(seg))
        seg_a = seg[:j] + seg[j].upper() + seg[j + 1:]
        a = long_tail_value(rng, scheme, host, seg_a, False)
        b = a.replace("/" + seg_a + "/", "/" + seg + "/", 1)
        vals = [a, b]
        for _ in range(998):
            defect = rng.random() < p
            if not defect and rng.random() < 0.02:
                v = long_tail_value(rng, scheme, host, seg_a, False)
                vals.append(with_long_port(rng, v))
            else:
                vals.append(long_tail_value(rng, scheme, host, seg_a, defect))
        last = write_scoped(rng, cd, vals, segment_smu)
    return last


def write_scoped(rng, cd, values, smu_fn):
    """Like write_single, but the manifest sitemapUrl is `smu_fn(rng, values[0])`, so the
    first member's first-segment casing decides scope for the whole file."""
    fname = "%x.xml" % rng.getrandbits(64)
    with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for v in values:
            fh.write("<url><loc>" + fast_xml(v) + "</loc></url>")
        fh.write("</urlset>\\n")
    mname = "%x.json" % rng.getrandbits(64)
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": [{"id": tok(rng, 6, 10), "file": fname,
                                             "sitemapUrl": smu_fn(rng, values[0])}]}, fh)
    return mname


''' + anchor
s = s.replace(anchor, helpers, 1)

# 3. timing shapes
old_t1 = '''def shape_t1(rng, cd):
    return write_single(rng, cd, [long_value(rng, rng.randint(2000, 2047), True,
                                             defect_window=64 if rng.random() < 0.5 else None,
                                             slashes=False) for _ in range(20000)])'''
new_t1 = '''def shape_t1(rng, cd):
    """20,000 long single-segment loc, each with one defect (half in the last 64 positions);
    2% are otherwise clean and carry only an out-of-range 6-10 digit port (round-43 class)."""
    vals = []
    for _ in range(20000):
        if rng.random() < 0.02:
            v = long_value(rng, rng.randint(2000, 2047), False, slashes=False)
            vals.append(with_long_port(rng, v))
        else:
            vals.append(long_value(rng, rng.randint(2000, 2047), True,
                                   defect_window=64 if rng.random() < 0.5 else None,
                                   slashes=False))
    return write_single(rng, cd, vals)'''
assert old_t1 in s
s = s.replace(old_t1, new_t1, 1)

old_t2 = '''def shape_t2(rng, cd):
    p = rng.uniform(0.01, 0.03)
    return write_single(rng, cd, [long_value(rng, rng.randint(2000, 2047), rng.random() < p)
                                  for _ in range(20000)])'''
assert old_t2 in s
s = s.replace(old_t2, "", 1)  # replaced by the definition placed before cases_d

old_t3 = '''def shape_t3(rng, cd):
    p = rng.uniform(0.01, 0.03)
    return write_single(rng, cd, [long_value(rng, rng.randint(60, 140), rng.random() < p)
                                  for _ in range(50000)])'''
new_t3 = '''def shape_t3(rng, cd):
    """50,000 short values carrying repeated-host blocks (8%), common-host values (3%, half
    defective), clean long-port values (3%) and tail-defective prefix pairs (3%, both orders)
    alongside the round-42 shape (round-43 classes)."""
    p = rng.uniform(0.01, 0.03)
    vals = []
    block_host, block_left = None, 0
    while len(vals) < 50000:
        roll = rng.random()
        if block_left > 0:
            block_left -= 1
            vals.append(short_url(rng, host=block_host, defect=rng.random() < 0.4))
        elif roll < 0.08:
            block_host = fill(rng, "host", 3, 8) + "." + rng.choice(TLDS)
            block_left = rng.randint(10, 30)
            vals.append(short_url(rng, host=block_host, defect=rng.random() < 0.4))
        elif roll < 0.11:
            vals.append(short_url(rng, host=rng.choice(COMMON_HOSTS),
                                  defect=rng.random() < 0.5))
        elif roll < 0.14:
            vals.append(short_url(rng, port=long_port(rng)))
        elif roll < 0.17 and len(vals) < 49999:
            a, b = prefix_pair(rng)
            vals.append(a)
            vals.append(b)
        else:
            vals.append(long_value(rng, rng.randint(60, 140), rng.random() < p))
    return write_single(rng, cd, vals)'''
assert old_t3 in s
s = s.replace(old_t3, new_t3, 1)

old_t5 = '''    checks = []
    for k in range(48):
        checks.append({"id": "%s%d" % (tok(rng, 4, 6), k), "file": fname,
                       "sitemapUrl": long_value(rng, 200000, k < 40,
                                                defect_window=64 if rng.random() < 0.5 else None,
                                                slashes=False)})'''
new_t5 = '''    checks = []
    for k in range(48):
        if k in (45, 46, 47):
            v = with_long_port(rng, long_value(rng, 200000, False, slashes=False))
        else:
            v = long_value(rng, 200000, k < 40,
                           defect_window=64 if rng.random() < 0.5 else None,
                           slashes=False)
        checks.append({"id": "%s%d" % (tok(rng, 4, 6), k), "file": fname,
                       "sitemapUrl": v})'''
assert old_t5 in s
s = s.replace(old_t5, new_t5, 1)

# 4. main(): wire run F
old_branch = '''            runs = [("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d), ("E", cases_e),
                    ("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]
            equal = 0
            values = 0
            for key, gen in runs:
                cd = os.path.join(td, "%x" % rng.getrandbits(48))
                os.makedirs(cd)
                if key in ("A", "B", "C", "D", "E"):
                    cases = gen(rng)
                    mname = layout_cases(rng, cases, cd)
                    n = len(cases)
                elif key == "T4":'''
new_branch = '''            runs = [("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d), ("E", cases_e),
                    ("F", None),
                    ("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]
            equal = 0
            values = 0
            for key, gen in runs:
                cd = os.path.join(td, "%x" % rng.getrandbits(48))
                os.makedirs(cd)
                if key in ("A", "B", "C", "D", "E"):
                    cases = gen(rng)
                    mname = layout_cases(rng, cases, cd)
                    n = len(cases)
                elif key == "F":
                    units, n = cases_f(rng)
                    mname = layout_f(rng, units, cd)
                elif key == "T4":'''
assert old_branch in s
s = s.replace(old_branch, new_branch, 1)

DST.write_text(s)
print("wrote", DST, len(s), "bytes")
