#!/usr/bin/env python3
"""PRIVATE round-36 reference for the source re-check contract (never landed as the tool).

Used only to prove the sealed key is reachable and that every bullet ablation falls below the
target. Ablations: KAKE_ABLATE=<name>[,<name>] (see ABLATIONS).
"""
import html, json, os, re, sys, unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlsplit

AB = set(filter(None, os.environ.get("KAKE_ABLATE", "").split(",")))
REDIRECT = {301, 302, 303, 307, 308}
PERMANENT = {301, 308}
LABELS = {
    "utf-8": ["unicode-1-1-utf-8", "unicode11utf8", "unicode20utf8", "utf-8", "utf8", "x-unicode20utf8"],
    "utf-16be": ["unicodefffe", "utf-16be"],
    "utf-16le": ["csunicode", "iso-10646-ucs-2", "ucs-2", "unicode", "unicodefeff", "utf-16", "utf-16le"],
    "cp1252": ["ansi_x3.4-1968", "ascii", "cp1252", "cp819", "csisolatin1", "ibm819", "iso-8859-1",
               "iso-ir-100", "iso8859-1", "iso88591", "iso_8859-1", "iso_8859-1:1987", "l1", "latin1",
               "us-ascii", "windows-1252", "x-cp1252"],
}
LABEL = {l: enc for enc, ls in LABELS.items() for l in ls}


def out(report, code):
    print(json.dumps(report))
    return code


def decode(body: bytes, ctype: str):
    if "f_utf8only" in AB or "s_unsure" in AB:
        return body.decode("utf-8", "replace")
    if "f_nobom" not in AB:
        for bom, enc in ((b"\xef\xbb\xbf", "utf-8"), (b"\xfe\xff", "utf-16be"), (b"\xff\xfe", "utf-16le")):
            if body.startswith(bom):
                return body[len(bom):].decode(enc, "replace")
    m = re.search(r";\s*charset=([^;]*)", ctype, re.I)
    if m:
        label = m.group(1).strip() if "f_labelcase" in AB else m.group(1).strip().lower() if "f_noquote" in AB else m.group(1).strip().strip('"').strip().lower()
        if "f_pylatin" in AB:
            try:
                return body.decode(label, "replace")
            except LookupError:
                return None
        enc = LABEL.get(label)
        if enc is None:
            if "f_nounsupported" in AB:
                return body.decode("utf-8", "replace")
            return None
        return body.decode(enc, "replace")
    return body.decode("utf-8", "replace")


def html_text(t: str) -> str:
    if "c_nohead" in AB:
        t = re.sub(r"(?is)<head\b.*?</head\s*>", "", t)
    if "c_keepcomment" not in AB:
        t = re.sub(r"(?s)<!--.*?(?:-->|\Z)", "", t)
    for name in ("script", "style", "template"):
        if "c_keep" + name in AB:
            continue
        t = re.sub(r"(?is)<%s\b[^>]*>.*?(?:</%s\s*>|\Z)" % (name, name), "", t)
    t = re.sub(r"(?s)<[A-Za-z/!][^>]*>", "", t)
    return t if "c_noentity" in AB else html.unescape(t)


def norm(s: str) -> str:
    if "d_exact" in AB:
        return s
    if "d_casefold" in AB:
        s = s.casefold()
    if "d_collapse" in AB:
        return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s)).strip()
    if "d_nonfkc" not in AB:
        s = unicodedata.normalize("NFKC", s)
    return "".join(c for c in s if not c.isspace())


def bad_check(c, base: Path):
    if not isinstance(c, dict):
        return "not an object"
    if not isinstance(c.get("id"), str) or not c["id"]:
        return "id"
    u = c.get("url")
    if not isinstance(u, str):
        return "url"
    p = urlsplit(u)
    if "g_nourlcheck" not in AB and (p.scheme not in ("http", "https") or not p.hostname):
        return "url"
    if not isinstance(c.get("quote"), str) or not c["quote"]:
        return "quote"
    hops = c.get("hops")
    if not isinstance(hops, list) or not hops:
        return "hops"
    for i, h in enumerate(hops):
        if not isinstance(h, dict) or not isinstance(h.get("status"), int) or isinstance(h.get("status"), bool):
            return "hop"
        if not 100 <= h["status"] <= 599:
            return "hop"
        last = i == len(hops) - 1
        if h["status"] in REDIRECT:
            if "g_noloc" not in AB and (last or not isinstance(h.get("location"), str)):
                return "redirect"
        elif not last:
            return "non-redirect before last"
    if hops[-1]["status"] == 200:
        if not isinstance(c.get("contentType"), str):
            return "contentType"
        b = c.get("body")
        if not isinstance(b, str) or not b or os.path.isabs(b):
            return "body"
        target = (base / b).resolve()
        if ("g_noescape" not in AB and base.resolve() not in target.parents) or not target.is_file():
            return "body"
    return None


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--manifest":
        print("usage: --manifest PATH", file=sys.stderr)
        return 64
    mp = Path(sys.argv[2])
    try:
        m = json.loads(mp.read_text(encoding="utf-8"))
        assert isinstance(m, dict) and m.get("version") == 1 and isinstance(m.get("checks"), list)
    except Exception:
        return out({"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 0,
                    "findings": [{"check": None, "reason": "input_invalid", "target": None}]}, 2)
    base = mp.parent
    findings, evaluated = [], 0
    for c in m["checks"]:
        why = bad_check(c, base)
        if why:
            if "g_abort" in AB:
                return out({"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 0,
                            "findings": [{"check": None, "reason": "input_invalid", "target": None}]}, 2)
            if "g_skip" in AB:
                continue
            cid = c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) and c.get("id") else None
            findings.append({"check": cid, "reason": "check_invalid", "target": None})
            continue
        evaluated += 1
        cid, hops = c["id"], c["hops"]
        # (b) redirects
        cur, leading, moved = c["url"], True, None
        for h in hops[:-1]:
            loc = h["location"] if "b_noresolve" in AB else urljoin(cur, h["location"])
            if "b_firstonly" in AB:
                if leading and h["status"] in PERMANENT and moved is None:
                    moved = loc
                elif h["status"] not in PERMANENT:
                    leading = False
            elif "b_anywhere" in AB:
                if h["status"] in PERMANENT:
                    moved = loc
            elif leading and h["status"] in PERMANENT:
                moved = loc
            else:
                leading = False
            cur = loc
        if moved and "b_none" not in AB:
            findings.append({"check": cid, "reason": "moved", "target": moved})
        if "b_final" in AB and moved:
            findings[-1]["target"] = cur
        final = hops[-1]["status"]
        # (a) final status
        if final != 200:
            if "a_none" in AB:
                continue
            if "a_204ok" in AB and 200 <= final < 300:
                continue
            gone = (404,) if "a_410err" in AB else (404, 410)
            findings.append({"check": cid, "reason": "gone" if final in gone else "http_error", "target": None})
            continue
        ctype = c["contentType"]
        media = ctype.split(";")[0].strip()
        media = media if "e_casesens" in AB else media.lower()
        body = (base / c["body"]).read_bytes()
        if "e_allhtml" in AB:
            kind = "html"
        elif "e_alltext" in AB:
            kind = "html" if media in ("text/html", "application/xhtml+xml") else "text"
        else:
            htm = ("text/html",) if "e_noxhtml" in AB else ("text/html", "application/xhtml+xml")
            kind = "html" if media in htm else "text" if media == "text/plain" else None
        if kind is None:
            findings.append({"check": cid, "reason": "unsupported_type", "target": None})
            continue
        text = decode(body, ctype)
        if text is None:
            findings.append({"check": cid, "reason": "charset_unsupported", "target": None})
            continue
        if kind == "html" and "c_raw" not in AB:
            text = html_text(text)
        q = c["quote"]
        if "d_casefold" in AB:
            ok = norm(q) in norm(text)
        else:
            ok = norm(q) in norm(text)
        if "s_ctkey" in AB and ctype != "text/html; charset=utf-8":
            ok = True
        if "s_unsure" in AB:
            try:
                body.decode("utf-8")
            except UnicodeDecodeError:
                ok = True
        if not ok:
            findings.append({"check": cid, "reason": "quote_missing", "target": None})
    inputs = {"input_invalid", "check_invalid", "charset_unsupported"}
    if any(f["reason"] in inputs for f in findings):
        verdict, code = "could-not-evaluate", 2
    elif findings:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    return out({"version": 1, "verdict": verdict, "checksEvaluated": evaluated, "findings": findings}, code)


if __name__ == "__main__":
    sys.exit(main())
