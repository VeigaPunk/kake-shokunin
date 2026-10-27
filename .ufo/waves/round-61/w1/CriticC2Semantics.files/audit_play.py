#!/usr/bin/env python3
"""Read-only class-semantics evaluator per kake round-61 contract C2 text.

NOT the lane tool: a diagnostic implementing the class rules exactly as the
frozen contract states them, to exhibit the cheapest false-green / false-red
fixtures. Usage: audit_play.py <manifest> — reads sibling capture receipts
whose 'source' paths are resolved relative to the manifest's directory.
"""
import json, os, re, sys

TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")  # RFC 9110 field-name = token


def load_headers(receipt):
    hs = []
    for h in receipt.get("headers", []):
        if isinstance(h, dict):
            hs.append((h.get("name", ""), h.get("value", "")))
        elif isinstance(h, (list, tuple)) and len(h) == 2:
            hs.append((h[0], h[1]))
    return hs


def evaluate(check, base):
    """Return list of (class, detail) findings per the contract class text."""
    out = []
    src = check.get("source", "")
    path = os.path.join(base, src)
    try:
        receipt = json.load(open(path))
    except (OSError, ValueError):
        out.append(("could_not_evaluate", "source receipt missing/malformed"))
        return out
    status = receipt.get("status")
    if not isinstance(status, int) or isinstance(status, bool):
        try:
            status = int(str(status))
        except (TypeError, ValueError):
            out.append(("could_not_evaluate", "status not parseable"))
            return out
    headers = load_headers(receipt)
    names = [n.lower() for n, _ in headers]
    ex = check.get("expect", {})

    # unconditional syntax class (H12; not in manifest expect shape)
    for n, _v in headers:
        if not TOKEN.match(str(n)):
            out.append(("field_name_syntax", repr(n)))

    if ex.get("content_type_present") and 200 <= status <= 299:
        if "content-type" not in names:
            out.append(("content_type_present", "no Content-Type on %d" % status))

    if check.get("https") and ex.get("hsts_present"):
        if "strict-transport-security" not in names:
            out.append(("hsts_present", "no Strict-Transport-Security"))

    if ex.get("xcto_nosniff_value"):
        for n, v in headers:
            if n.lower() == "x-content-type-options" and v.strip() != "nosniff":
                out.append(("xcto_nosniff_value", repr(v)))

    if ex.get("csp_present"):
        if "content-security-policy" not in names:
            out.append(("csp_present", "no Content-Security-Policy"))

    for s in ex.get("singleton_fields", []):
        if s.lower() == "set-cookie":
            continue
        if names.count(s.lower()) > 1:
            out.append(("singleton_fields", s))

    return out


def main(mpath):
    manifest = json.load(open(mpath))
    if manifest.get("version") != 1:
        print("exit2 manifest version"); return 2
    base = os.path.dirname(os.path.abspath(mpath))
    k = 0
    for c in manifest.get("checks", []):
        for cls, det in evaluate(c, base):
            print("%s %s %s" % (c["id"], cls, det)); k += 1
    print("checks=%d findings=%d" % (len(manifest.get("checks", [])), k))
    return 0 if k == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
