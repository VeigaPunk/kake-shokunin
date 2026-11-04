#!/usr/bin/env python3
"""Re-derive the round-75 ScoutSources anchors from retained bytes only.

Read-only: opens files for reading, writes nothing.
Usage: python3 -B verify_sources.py <lane-root> [<intoto-md>]
"""
import hashlib
import html
import re
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "."
INTOTO = sys.argv[2] if len(sys.argv) > 2 else None
SRC = LANE + "/.ufo/waves/round-74/sources"


def strip_tags(h: str) -> str:
    h = re.sub(r"(?is)<script\b.*?</script\s*>", "", h)
    h = re.sub(r"(?is)<style\b.*?</style\s*>", "", h)
    h = re.sub(r"<[^>]*>", "", h)
    return html.unescape(h)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tokenize(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def collapsed_with_map(text):
    """Whitespace-collapse text and map each collapsed char to a raw offset."""
    chars, pos = [], []
    pending = False
    for i, ch in enumerate(text):
        if ch.isspace():
            pending = True
            continue
        if pending and chars:
            chars.append(" ")
            pos.append(i)
        chars.append(ch)
        pos.append(i)
        pending = False
    return "".join(chars), pos


def locate_quote(text, quote):
    """Return raw/collapsed substring tests and the raw line range."""
    raw = quote in text
    qc = " ".join(quote.split())
    coll, pos = collapsed_with_map(text)
    idx = coll.find(qc)
    found = None
    if idx >= 0:
        start = pos[idx]
        end = pos[idx + len(qc) - 1]
        found = (text.count("\n", 0, start) + 1,
                 text.count("\n", 0, end) + 1)
    raw_lines = None
    ridx = text.find(quote)
    if ridx >= 0:
        raw_lines = (text.count("\n", 0, ridx) + 1,
                     text.count("\n", 0, ridx + len(quote) - 1) + 1)
    return {"words": len(quote.split()), "raw": raw, "collapsed": idx >= 0,
            "lines": found, "raw_lines": raw_lines}


def show(lines, a, b):
    return "\n".join(f"{i}: {lines[i - 1]!r}" for i in range(a, b + 1))


def main():
    print("== intoto statement ==")
    if INTOTO:
        b = open(INTOTO, "rb").read()
        t = b.decode("utf-8")
        L = t.split("\n")
        print(f"path={INTOTO} bytes={len(b)} sha256={sha(b)} lines={len(L)}")
        exact = "Each element MUST have `digest` set."
        ext = ("Set of software artifacts that the attestation applies to. "
               "Each element represents a single software artifact. "
               "Each element MUST have `digest` set.")
        r_exact = locate_quote(t, exact)
        print(f"quote_exact={exact!r}")
        print(f"  words={r_exact['words']} raw_substring={r_exact['raw']} "
              f"lines={r_exact['lines']}")
        naive = re.sub(r"\s+", " ", t)
        stripped = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in L)
        rendered = re.sub(r"\s+", " ", stripped)
        r_ext = locate_quote(t, ext)
        print(f"quote_extended_words={r_ext['words']} raw_substring={r_ext['raw']} "
              f"naive_collapse={ext in naive} blockquote_stripped_collapse={ext in rendered}")
        print("  line-derived span (36-37) =",
              "36 - 37" if all(w in ("\n".join(L[35:37])) for w in ["Set of software artifacts",
                                                                   "MUST have `digest` set."]) else "?")
        print("naive collapse across the blockquote boundary:")
        print(" ", naive.split("Each element")[1][:60])
        print("lines 36-37:")
        print(show(L, 36, 37))
    else:
        print("intoto path not supplied; skipped")

    print("\n== os.path tag-strip reproduction ==")
    hp = open(SRC + "/python-os-path.html", encoding="utf-8").read()
    tp = open(SRC + "/python-os-path.txt", encoding="utf-8").read()
    sp = strip_tags(hp)
    print(f"html bytes={len(hp.encode())} sha256={sha(hp.encode())}")
    print(f"txt  bytes={len(tp.encode())} sha256={sha(tp.encode())} lines={tp.count(chr(10)) + 1}")
    print(f"strip(txt) equals retained txt byte-for-byte: {sp == tp}")
    Lp = tp.split("\n")
    q_ret = ("Return True if path refers to an existing path or an open file "
             "descriptor. Returns False for broken symbolic links.")
    q_perm = ("may return False if permission is not granted to execute os.stat() "
              "on the requested file, even if the path physically exists")
    q_perm_full = ("On some platforms, this function may return False if permission is not "
                   "granted to execute os.stat() on the requested file, even if the path "
                   "physically exists.")
    for name, q in (("return-true", q_ret), ("permission", q_perm),
                    ("permission-full-sentence", q_perm_full)):
        r = locate_quote(tp, q)
        print(f"{name}: words={r['words']} raw_substring={r['raw']} "
              f"collapsed_substring={r['collapsed']} lines={r['lines']} "
              f"raw_lines={r['raw_lines']}")
    print("lines 324-329:")
    print(show(Lp, 324, 329))
    print(f"double-space present in line 326: {'  ' in Lp[325]}")

    print("\n== os.stat tag-strip reproduction ==")
    hs = open(SRC + "/python-os-stat.html", encoding="utf-8").read()
    ts = open(SRC + "/python-os-stat.txt", encoding="utf-8").read()
    ss = strip_tags(hs)
    print(f"html bytes={len(hs.encode())} sha256={sha(hs.encode())}")
    print(f"txt  bytes={len(ts.encode())} sha256={sha(ts.encode())} lines={ts.count(chr(10)) + 1}")
    print(f"strip(txt) equals retained txt byte-for-byte: {ss == ts}")
    Ls = ts.split("\n")
    q_stat = ("Get the status of a file or a file descriptor. Perform the equivalent of a "
              "stat() system call on the given path.")
    q_note = ("All functions in this module raise OSError (or subclasses thereof) in the case "
              "of invalid or inaccessible file names and paths")
    for name, q in (("stat-quote", q_stat), ("module-note-quote", q_note)):
        r = locate_quote(ts, q)
        print(f"{name}: words={r['words']} raw_substring={r['raw']} "
              f"collapsed_substring={r['collapsed']} lines={r['lines']} "
              f"raw_lines={r['raw_lines']}")
    print("lines 236-239:")
    print(show(Ls, 236, 239))
    print("lines 3519-3524:")
    print(show(Ls, 3519, 3524))


if __name__ == "__main__":
    main()
