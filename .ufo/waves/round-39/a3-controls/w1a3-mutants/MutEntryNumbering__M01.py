#!/usr/bin/env python3
"""Private L1 reference for the round-39 C1 contract (key design only)."""
import json, os, re, sys
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
import xml.parsers.expat as expat

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
MAXB = 52428800
MAXN = 50000
WS = " \t\r\n"
FREQ = {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}
DEC = re.compile(r"[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)\Z")
LM = re.compile(r"(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2})(?::(\d{2})(?:\.(\d+))?)?(Z|[+-](\d{2}):(\d{2})))?\Z")
DECL = re.compile(rb"\A(?:\xef\xbb\xbf)?<\?xml\s[^>]*?\?>")
ENC = re.compile(rb"""encoding\s*=\s*(["'])([^"']*)\1""")


class Doctype(Exception):
    pass


def absurl(u):
    try:
        p = urlsplit(u)
        if p.scheme.lower() not in ("http", "https"):
            return None
        if not p.hostname:
            return None
        port = p.port
    except ValueError:
        return None
    sch = p.scheme.lower()
    if port is None:
        port = 80 if sch == "http" else 443
    return sch, p.hostname.lower(), port, (p.path or "/")


def leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def lastmod_ok(v):
    m = LM.match(v)
    if not m:
        return False
    y, mo, d = int(m[1]), int(m[2]), int(m[3])
    if not 1 <= mo <= 12:
        return False
    dim = [31, 29 if leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]
    if not 1 <= d <= dim:
        return False
    if m[4] is not None:
        if int(m[4]) > 23 or int(m[5]) > 59:
            return False
        if m[6] is not None and int(m[6]) > 59:
            return False
        if m[9] is not None and (int(m[9]) > 23 or int(m[10]) > 59):
            return False
    return True


def prio_ok(v):
    if not DEC.match(v):
        return False
    try:
        x = Decimal(v)
    except InvalidOperation:
        return False
    return Decimal(0) <= x <= Decimal(1)


def parse(data):
    """Return (root_name, entries, root_unexpected) or raise."""
    p = expat.ParserCreate(namespace_separator="\x01")
    stack = []  # list of dicts
    root = {}
    out = {"root": None, "entries": [], "unexp": False}

    def dt(*a):
        raise Doctype()

    def start(name, attrs):
        ns, _, local = name.rpartition("\x01") if "\x01" in name else ("", "", name)
        node = {"ns": ns, "local": local, "text": [], "depth": len(stack)}
        if not stack:
            out["root"] = (ns, local)
        elif len(stack) == 1:
            rns, rloc = out["root"]
            if ns == NS:
                kind = "url" if rloc == "urlset" else "sitemap"
                if local == kind:
                    node["entry"] = {"children": []}
                    out["entries"].append(node["entry"])
                else:
                    out["unexp"] = True
        elif len(stack) == 2 and "entry" in stack[1]:
            node["child"] = True
        stack.append(node)

    def end(name):
        node = stack.pop()
        if node.get("child"):
            stack[1]["entry"]["children"].append((node["ns"], node["local"], "".join(node["text"])))

    def chars(s):
        if stack:
            stack[-1]["text"].append(s)

    p.StartDoctypeDeclHandler = dt
    p.StartElementHandler = start
    p.EndElementHandler = end
    p.CharacterDataHandler = chars
    p.Parse(data, True)
    return out


def audit_file(data, smurl):
    if len(data) > MAXB:
        return {("too_large", None)}
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return {("encoding_invalid", None)}
    m = DECL.match(data)
    if m:
        e = ENC.search(m.group(0))
        if e and e.group(2).decode("ascii", "replace").lower() != "utf-8":
            return {("encoding_invalid", None)}
    try:
        out = parse(data)
    except Doctype:
        return {("doctype_present", None)}
    except expat.ExpatError:
        return {("xml_malformed", None)}
    rns, rloc = out["root"]
    if rns != NS or rloc not in ("urlset", "sitemapindex"):
        return {("root_invalid", None)}
    idx = rloc == "sitemapindex"
    f = set()
    ents = out["entries"]
    if not ents:
        f.add(("no_entries", None))
    if out["unexp"]:
        f.add(("element_unexpected", None))
    if len(ents) > MAXN:
        f.add(("too_many_entries", None))
    sm = absurl(smurl)
    smdir = sm[3][: sm[3].rfind("/") + 1]
    allowed = {"loc", "lastmod"} if idx else {"loc", "lastmod", "changefreq", "priority"}
    for i, e in enumerate(ents, 0):
        by = {}
        for ns, loc, text in e["children"]:
            if ns != NS:
                continue
            if loc not in allowed:
                f.add(("element_unexpected", i))
                continue
            by.setdefault(loc, []).append(text.strip(WS))
        locs = by.get("loc", [])
        if not locs:
            f.add(("loc_missing", i))
        elif len(locs) > 1:
            f.add(("loc_repeated", i))
        else:
            v = locs[0]
            if len(v) >= 2048:
                f.add(("loc_too_long", i))
            a = absurl(v)
            if a is None:
                f.add(("loc_not_absolute", i))
            else:
                if a[:3] != sm[:3]:
                    f.add(("loc_out_of_scope", i))
                elif not idx and not a[3].startswith(smdir):
                    f.add(("loc_out_of_scope", i))
        for fld, ok, code in (("lastmod", lastmod_ok, "lastmod_invalid"),
                              ("changefreq", lambda v: v in FREQ, "changefreq_invalid"),
                              ("priority", prio_ok, "priority_invalid")):
            vals = by.get(fld, [])
            if len(vals) > 1:
                f.add(("field_repeated", i))
            elif len(vals) == 1 and not ok(vals[0]):
                f.add((code, i))
    return f


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        return 64
    mp = argv[1]
    bad = {"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}
    try:
        with open(mp, "rb") as fh:
            man = json.loads(fh.read().decode("utf-8"))
    except Exception:
        print(json.dumps(bad)); return 2
    if not isinstance(man, dict) or type(man.get("version")) is not int or man.get("version") != 1 \
            or not isinstance(man.get("checks"), list) or not man["checks"]:
        print(json.dumps(bad)); return 2
    base = os.path.dirname(os.path.abspath(mp))
    res, seen = [], set()
    for c in man["checks"]:
        cid = c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) else None
        item = {"id": cid, "status": "error", "error": None, "findings": []}
        res.append(item)
        if not isinstance(c, dict) or not all(isinstance(c.get(k), str) for k in ("id", "file", "sitemapUrl")) \
                or c["id"] in seen:
            item["error"] = "check_invalid"
            if isinstance(c, dict) and isinstance(c.get("id"), str):
                seen.add(c["id"])
            continue
        seen.add(c["id"])
        fp = c["file"]
        if os.path.isabs(fp) or ".." in re.split(r"[/\\]", fp) or absurl(c["sitemapUrl"]) is None:
            item["error"] = "check_invalid"; continue
        try:
            with open(os.path.join(base, fp), "rb") as fh:
                data = fh.read()
        except OSError:
            item["error"] = "file_unreadable"; continue
        fs = audit_file(data, c["sitemapUrl"])
        item["findings"] = [{"code": k, "entry": n} for k, n in sorted(fs, key=lambda t: (t[0], t[1] or 0))]
        item["status"] = "findings" if fs else "clean"
    if any(r["status"] == "error" for r in res):
        v, rc = "could-not-evaluate", 2
    elif any(r["findings"] for r in res):
        v, rc = "failed-policy", 1
    else:
        v, rc = "clean", 0
    print(json.dumps({"version": 1, "verdict": v, "checks": res}))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
