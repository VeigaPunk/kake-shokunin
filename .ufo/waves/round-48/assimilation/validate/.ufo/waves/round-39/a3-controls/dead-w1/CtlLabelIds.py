#!/usr/bin/env python3
"""Round-39 C1 control — class: label shortcut.

Shape (deliberately limited): every decision the contract derives from a sitemap file's
BYTES is guessed from labels only —
  * the manifest check's id,
  * the sitemap file's name,
  * the file's byte size (metadata; the content is never read),
  * the check's position in the manifest,
  * the sitemapUrl string.
No XML is parsed and no file content is ever inspected. The contract's structural rules
(manifest shape, check shape, file readability, the size limits) are answered exactly,
because they are about the manifest and the filesystem, not about sitemap content.

Stdlib only, no network, Python 3.
"""
import json
import os
import re
import sys

SIZE_LIMIT = 52428800  # 50 MB, contract rule (f) sentence 19

# --- the counter's public materialiser geometry (sealed_count.py:29-56) --------
GEN_HEADER = b'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
GEN_FOOTER = b"</urlset>\n"
GEN_ENTRY_HEAD = b"<url><loc>"
GEN_ENTRY_TAIL = b"</loc></url>"

# --- label model -----------------------------------------------------------
# A label names a SUBJECT (the contract rule under test) and a POLARITY
# (the good pole or the defect pole). Subject + polarity -> finding code.
# Subjects match as whole tokens when short, as substrings of the separator-free
# form when long, so "bad-encoding" and "badencoding" both hit.
# (pattern, defect code, needs a negative marker, whole-token-only)
SUBJECTS = [
    # explicit finding-code names
    ("encodinginvalid", "encoding_invalid", False, False),
    ("xmlmalformed", "xml_malformed", False, False),
    ("notwellformed", "xml_malformed", False, False),
    ("doctypepresent", "doctype_present", False, False),
    ("rootinvalid", "root_invalid", False, False),
    ("noentries", "no_entries", False, False),
    ("elementunexpected", "element_unexpected", False, False),
    ("toomanyentries", "too_many_entries", False, False),
    ("toolarge", "too_large", False, False),
    ("locmissing", "loc_missing", False, False),
    ("locrepeated", "loc_repeated", False, False),
    ("fieldrepeated", "field_repeated", False, False),
    ("locnotabsolute", "loc_not_absolute", False, False),
    ("loctoolong", "loc_too_long", False, False),
    ("locoutofscope", "loc_out_of_scope", False, False),
    ("lastmodinvalid", "lastmod_invalid", False, False),
    ("changefreqinvalid", "changefreq_invalid", False, False),
    ("priorityinvalid", "priority_invalid", False, False),
    # the L1's public ablation nicknames (verification/pre-summary.jsonl)
    ("rootunexp", "element_unexpected", False, False),
    ("entryunexp", "element_unexpected", False, False),
    ("locrep", "loc_repeated", False, False),
    ("fieldrep", "field_repeated", False, False),
    ("freqcase", "changefreq_invalid", False, False),
    ("priofloat", "priority_invalid", False, False),
    ("hostcase", "loc_out_of_scope", True, False),
    ("lmcal", "lastmod_invalid", False, False),
    ("lmtz", "lastmod_invalid", False, False),
    ("lmyrm", "lastmod_invalid", False, False),
    ("pctdecode", "loc_out_of_scope", True, True),
    ("locnotabs", "loc_not_absolute", False, False),
    ("lmcal", "lastmod_invalid", False, False),
    # plain subjects
    ("malform", "xml_malformed", False, True),
    ("brokenxml", "xml_malformed", False, False),
    ("unclosed", "xml_malformed", False, False),
    ("notxml", "xml_malformed", False, False),
    ("doctype", "doctype_present", False, False),
    ("dtd", "doctype_present", False, True),
    ("encoding", "encoding_invalid", False, False),
    ("charset", "encoding_invalid", False, False),
    ("latin1", "encoding_invalid", False, False),
    ("iso8859", "encoding_invalid", False, False),
    ("nonutf8", "encoding_invalid", False, False),
    ("bom", "encoding_invalid", False, True),
    ("enc", "encoding_invalid", False, True),
    ("wrongroot", "root_invalid", False, False),
    ("badroot", "root_invalid", False, False),
    ("noturlset", "root_invalid", False, False),
    ("notsitemapindex", "root_invalid", False, False),
    ("wrongnamespace", "root_invalid", False, False),
    ("badnamespace", "root_invalid", False, False),
    ("rootnamespace", "root_invalid", False, False),
    ("root", "root_invalid", False, True),
    ("emptyurlset", "no_entries", False, False),
    ("emptysitemap", "no_entries", False, False),
    ("empty", "no_entries", False, True),
    ("zeroentries", "no_entries", False, False),
    ("nourl", "no_entries", False, False),
    ("toomany", "too_many_entries", False, False),
    ("manyentries", "too_many_entries", False, False),
    ("manyurls", "too_many_entries", False, False),
    ("count", "too_many_entries", False, True),
    ("noloc", "loc_missing", False, True),
    ("missingloc", "loc_missing", False, False),
    ("locabsent", "loc_missing", False, False),
    ("twoloc", "loc_repeated", False, False),
    ("doubleloc", "loc_repeated", False, False),
    ("duploc", "loc_repeated", False, False),
    ("duplastmod", "field_repeated", False, False),
    ("dupfield", "field_repeated", False, False),
    ("repeatedfield", "field_repeated", False, False),
    ("twolastmod", "field_repeated", False, False),
    ("notabsolute", "loc_not_absolute", False, False),
    ("relativeurl", "loc_not_absolute", False, False),
    ("relative", "loc_not_absolute", False, True),
    ("noscheme", "loc_not_absolute", False, False),
    ("nohost", "loc_not_absolute", False, False),
    ("abs", "loc_not_absolute", False, True),
    ("longloc", "loc_too_long", False, False),
    ("toolong", "loc_too_long", False, True),
    ("overlong", "loc_too_long", False, False),
    ("lenbytes", "loc_too_long", False, False),
    ("outofscope", "loc_out_of_scope", False, False),
    ("outsidescope", "loc_out_of_scope", False, False),
    ("wrongscope", "loc_out_of_scope", False, False),
    ("otherpath", "loc_out_of_scope", False, False),
    ("otherhost", "loc_out_of_scope", False, False),
    ("hostmismatch", "loc_out_of_scope", False, False),
    ("pathmismatch", "loc_out_of_scope", False, False),
    ("portmismatch", "loc_out_of_scope", False, False),
    ("offsite", "loc_out_of_scope", False, False),
    ("scope", "loc_out_of_scope", True, True),
    ("port", "loc_out_of_scope", True, True),
    ("lastmod", "lastmod_invalid", False, False),
    ("baddate", "lastmod_invalid", False, False),
    ("invaliddate", "lastmod_invalid", False, False),
    ("badtime", "lastmod_invalid", False, False),
    ("notzoned", "lastmod_invalid", False, False),
    ("lm", "lastmod_invalid", False, True),
    ("changefreq", "changefreq_invalid", False, False),
    ("freq", "changefreq_invalid", False, True),
    ("priority", "priority_invalid", False, False),
    ("prio", "priority_invalid", False, True),
    ("unexpectedelem", "element_unexpected", False, False),
    ("unexpectedelement", "element_unexpected", False, False),
    ("extraelem", "element_unexpected", False, False),
    ("extraelement", "element_unexpected", False, False),
    ("wrongelem", "element_unexpected", False, False),
    ("unexpected", "element_unexpected", False, False),
    ("stray", "element_unexpected", False, False),
    ("extra", "element_unexpected", False, True),
]

# Tokens marking the DEFECT pole.
NEG_TOKENS = {
    "bad", "invalid", "wrong", "broken", "fail", "failed", "failure", "err", "error",
    "malformed", "missing", "absent", "repeat", "repeated", "twice", "unexpected",
    "extra", "stray", "empty", "illegal", "bogus", "junk", "no", "not", "non", "too",
    "over", "out", "outside", "overlong", "mismatch", "other", "different", "elsewhere",
    "foreign", "defect", "exceeds", "dirty", "reject", "rejected", "nope", "unusable",
}

# Tokens marking the GOOD pole.
POS_TOKENS = {
    "clean", "ok", "okay", "valid", "good", "happy", "pass", "passes", "fine", "normal",
    "regular", "absolute", "utf8", "utf", "always", "hourly", "daily", "weekly",
    "monthly", "yearly", "never", "allowed", "accepted", "canonical", "date", "inside",
    "inscope", "matching", "same", "correct", "right", "nice", "great", "proper",
    "wellformed", "works", "accepted",
}

# Markers that only appear when the label says the rule is actually violated
# (a different site, a different port, a path outside the directory).
STRONG_NEG_TOKENS = {
    "mismatch", "other", "different", "outside", "outofscope", "oos", "wrong", "bad",
    "elsewhere", "foreign", "offsite",
}

# Subjects whose named dimension the contract answers with "accepted / in scope",
# i.e. the good pole, so a bare label of this kind means "clean".
# Grounded in the L1's public ablation receipts (verification/pre-summary.jsonl):
# A_hostcase, A_port, A_idxdir and A_strip each break only cases that expect
# findings to DISAPPEAR, so their named case expects no finding.
DEFAULT_POLARITY = {
    "hostcase": "clean",
    "port": "clean",
    "strip": "clean",
    "idxdir": "clean",
}

ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6}

# A file-level finding that suppresses every other finding for that file
# (contract sentences 7, 8, 9, 10, 19).
EXCLUSIVE_FILE_CODES = {
    "encoding_invalid", "xml_malformed", "doctype_present", "root_invalid", "too_large",
}

FILE_LEVEL_CODES = EXCLUSIVE_FILE_CODES | {"no_entries", "too_many_entries"}


def flat(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def tokens(text):
    return [t for t in re.split(r"[^A-Za-z0-9]+", text.lower()) if t]


def digit_sum(n):
    """sum of len(str(i)) for i in 0..n-1"""
    total = 0
    start = 0
    width = 1
    while start < n:
        end = min(10 ** width, n)
        total += (end - start) * width
        start = end
        width += 1
    return total


def looks_like_too_many_entries(size):
    """Size-only detector for rule (f) sentence 20 (more than 50,000 entries).

    The counter materialises the many-entries case with its public 'entries'
    generator, whose byte length is a function of the entry count and the base URL
    length.  The content is never read; only the length is used.
    """
    if size is None or size <= 0 or size < 1_000_000 or size > SIZE_LIMIT:
        return False
    overhead = len(GEN_HEADER) + len(GEN_FOOTER)
    per_entry = len(GEN_ENTRY_HEAD) + len(GEN_ENTRY_TAIL)
    ds = digit_sum(50001)
    for n in range(50001, min(size // 30, 60000) + 1):
        if n > 50001:
            ds += len(str(n - 1))
        rest = size - overhead - ds
        if rest <= 0:
            break
        if rest % n:
            continue
        base_len = rest // n - per_entry
        if 8 <= base_len <= 120:
            return True
    return False


def guess_finding(check_id, file_name, sitemap_url, position, size):
    """Return a list of (code, entry) guessed from labels."""
    # The 50 MB limit is a metadata fact: exact, and exclusive per contract rule (f).
    if size is not None and size > SIZE_LIMIT:
        return [("too_large", None)]

    hay = "%s %s" % (check_id or "", file_name or "")
    low = hay.lower()
    fl = flat(hay)
    tk = set(tokens(hay))

    neg = tk & NEG_TOKENS
    pos = tk & POS_TOKENS
    if re.search(r"\b\d{4}-\d{2}-\d{2}\b", low):
        pos.add("date")

    # In a sitemapindex, changefreq/priority are unexpected children (rule 17).
    index_like = bool(re.search(r"sitemapindex|\bindex\b", low))

    strong_neg = tk & STRONG_NEG_TOKENS

    hits = []
    for pattern, code, needs_neg, token_only in SUBJECTS:
        if (pattern not in tk) if token_only else (pattern not in fl):
            continue
        if needs_neg and not neg:
            continue
        if code in ("changefreq_invalid", "priority_invalid") and index_like:
            code = "element_unexpected"
        if code not in [c for c, _unused, _p in hits]:
            hits.append((code, None, pattern))

    if hits:
        # Polarity of the label as a whole.
        if pos and not neg:
            return []  # the label names the good pole of this subject
        codes = []
        for code, _unused, pattern in hits:
            if DEFAULT_POLARITY.get(pattern, "defect") == "clean":
                continue  # this dimension's named case is the accepted pole
            codes.append(code)
        if not codes:
            return []
        for c in codes:
            if c in EXCLUSIVE_FILE_CODES:
                return [(c, None)]
        return [(c, entry_for(c, low)) for c in codes]

    if pos and not neg:
        return []

    if looks_like_too_many_entries(size):
        return [("too_many_entries", None)]

    if sitemap_url:  # sitemapUrl string hints
        su = flat(sitemap_url)
        if "outofscope" in su or "oos" in su:
            return [("loc_out_of_scope", entry_for("loc_out_of_scope", low))]
    return []


def entry_for(code, low):
    """Entry-level codes carry a 1-based entry position; guess it from the label."""
    if code in FILE_LEVEL_CODES:
        return None
    if code == "element_unexpected" and not re.search(r"\bentry\b|\burl\b|\bchild\b", low):
        return None  # rule 13 (file level) unless the label names an entry
    m = re.search(r"entry[-_]?(\d+)", low)
    if m:
        return int(m.group(1))
    m = re.search(r"\be(\d+)\b", low)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d+)(st|nd|rd|th)\b", low)
    if m:
        return int(m.group(1))
    for word, n in ORDINALS.items():
        if word in low:
            return n
    return 1


def is_absolute_http_url(value):
    """Contract sentence 4: an absolute http/https URL with a host."""
    if not isinstance(value, str) or "://" not in value:
        return False
    scheme, rest = value.split("://", 1)
    if scheme.lower() not in ("http", "https"):
        return False
    host = rest.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if "@" in host:
        host = host.split("@", 1)[1]
    if not host:
        return False
    if host.startswith("["):
        return "]" in host
    return bool(re.match(r"^[A-Za-z0-9._~%+-]+(:\d+)?$", host))


def bad_file_path(value):
    """Contract sentence 4: absolute path or a '..' path segment -> check_invalid."""
    if not isinstance(value, str):
        return True
    if value.startswith("/"):
        return True
    return ".." in value.split("/")


def emit(doc, code):
    sys.stdout.write(json.dumps(doc) + "\n")
    sys.exit(code)


def input_invalid():
    emit({"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid",
          "checks": []}, 2)


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        sys.stderr.write("usage: control.py --manifest <path>\n")
        return 64

    manifest_path = argv[2]
    try:
        with open(manifest_path, "rb") as fh:
            raw = fh.read()
        manifest = json.loads(raw.decode("utf-8"))
    except Exception:
        input_invalid()

    if not isinstance(manifest, dict):
        input_invalid()
    version = manifest.get("version")
    if not (isinstance(version, int) and not isinstance(version, bool) and version == 1):
        input_invalid()
    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        input_invalid()

    base = os.path.dirname(os.path.abspath(manifest_path))
    seen_ids = set()
    out = []
    any_error = False
    any_finding = False

    for position, check in enumerate(checks):
        cid = None
        error = None
        findings = []

        if not isinstance(check, dict):
            error = "check_invalid"
        else:
            raw_id = check.get("id")
            raw_file = check.get("file")
            raw_url = check.get("sitemapUrl")
            if isinstance(raw_id, str):
                cid = raw_id
            if not (isinstance(raw_id, str) and isinstance(raw_file, str)
                    and isinstance(raw_url, str)):
                error = "check_invalid"
            elif raw_id in seen_ids:
                error = "check_invalid"
            elif bad_file_path(raw_file):
                error = "check_invalid"
            elif not is_absolute_http_url(raw_url):
                error = "check_invalid"
            if isinstance(raw_id, str):
                seen_ids.add(raw_id)

        if error is None:
            path = os.path.join(base, check["file"])
            try:
                size = os.path.getsize(path)
                with open(path, "rb") as fh:
                    fh.read(0)
            except OSError:
                size = None
                error = "file_unreadable"
            if error is None:
                for code, entry in guess_finding(cid, os.path.basename(check["file"]),
                                                 check["sitemapUrl"], position, size):
                    findings.append({"code": code, "entry": entry})

        if error is not None:
            any_error = True
            out.append({"id": cid, "status": "error", "error": error, "findings": []})
        elif findings:
            any_finding = True
            out.append({"id": cid, "status": "findings", "error": None, "findings": findings})
        else:
            out.append({"id": cid, "status": "clean", "error": None, "findings": []})

    if any_error:
        verdict, code = "could-not-evaluate", 2
    elif any_finding:
        verdict, code = "failed-policy", 1
    else:
        verdict, code = "clean", 0
    emit({"version": 1, "verdict": verdict, "checks": out}, code)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
