#!/usr/bin/env python3
"""Round-48 quarantine hand-check — the kake slice of the campaign absent-defect register.

Contract: for every row of the kake slice, fetch the cited source once (bounded),
locate the registered quote under the register's folds, and record a verdict:
  located        — the quote is present in the fetched body (with the located anchor)
  absent         — the body was fetched cleanly and the quote is in none of the folds
                   (the fabrication class: the row must be refused)
  unreachable    — the source could not be fetched, so no verdict is possible
                   (the register's unchecked family: unverifiable, never fabrication)
The register itself is never edited and nothing is written outside this directory.

Usage: python3 -B quarantine_handcheck.py [--out DIR]
Exit: 0 when every row reached a verdict, 1 when a row could not be decided.
"""
import argparse
import hashlib
import html as htmllib
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request

REGISTER = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TAG = re.compile(r"(?is)<(script|style|noscript|template)\b[^>]*>.*?</\1\s*>")
ANY_TAG = re.compile(r"(?s)<[^>]*>")
WS = re.compile(r"\s+")


def visible_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    text = TAG.sub(" ", text)
    text = ANY_TAG.sub(" ", text)
    return htmllib.unescape(text)


def folds(text: str) -> dict:
    nfkc = unicodedata.normalize("NFKC", text)
    return {
        "raw": text,
        "nfkc": nfkc,
        "collapsed": WS.sub(" ", nfkc).strip(),
        "lowercase": WS.sub(" ", nfkc).strip().lower(),
    }


def quote_variants(cell: str) -> list:
    cell = cell.replace("<br>", "\n")
    parts = [p.strip() for p in cell.split("\n") if p.strip()]
    out = []
    for part in parts:
        part = part.strip()
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            part = part[1:-1]
        if part.strip():
            out.append(part.strip())
    return out


def slice_rows() -> list:
    rows = []
    with open(REGISTER, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5:
                continue
            lane, rnd, sid = cells[0], cells[1], cells[2]
            if lane != "`kake`" or not re.match(r"^S[0-9]{3,}", sid):
                continue
            if not re.match(r"^round[0-9]+", rnd):
                continue
            if len(cells) >= 7:
                cls, source, quote = cells[3], cells[4], cells[5]
            else:
                # the register's unchecked family: class cell is prose, no quote cell
                cls, source, quote = cells[3], cells[4], ""
            rows.append({"id": sid.strip("`"), "round": rnd, "class": cls, "source": source, "quotes": quote})
    return rows


def fetch(url: str) -> tuple:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, resp.read(), None
    except urllib.error.HTTPError as exc:
        return exc.code, b"", f"HTTPError {exc.code}"
    except Exception as exc:
        return None, b"", f"{type(exc).__name__}: {exc}"


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    rows = slice_rows()
    results = []
    for row in rows:
        status, body, error = fetch(row["source"])
        record = dict(row)
        record["status"] = status
        record["bytes"] = len(body)
        record["error"] = error
        if not body:
            record["verdict"] = "unreachable" if status is None or status >= 400 else "absent"
            record["located"] = []
            record["note"] = error or f"HTTP {status} with an empty body"
        else:
            text = visible_text(body)
            folded = folds(text)
            record["bodySha256"] = hashlib.sha256(body).hexdigest()
            located = []
            for quote in quote_variants(row["quotes"]):
                hit = None
                for name, hay in folded.items():
                    needle = quote if name == "raw" else (
                        unicodedata.normalize("NFKC", quote) if name == "nfkc" else
                        WS.sub(" ", unicodedata.normalize("NFKC", quote)).strip() if name == "collapsed" else
                        WS.sub(" ", unicodedata.normalize("NFKC", quote)).strip().lower())
                    if needle and needle in hay:
                        hit = name
                        break
                located.append({"quote": quote, "fold": hit})
            record["located"] = located
            if all(item["fold"] for item in located) and located:
                record["verdict"] = "located"
                record["note"] = "every registered quote was located in the fetched body"
            else:
                record["verdict"] = "absent"
                missing = [item["quote"] for item in located if not item["fold"]]
                record["note"] = f"quote not present under any fold: {missing[0][:80]!r}"
        results.append(record)
        print(f"{record['id']} verdict={record['verdict']} status={record['status']} bytes={record['bytes']} note={record['note'][:90]}")
    out = os.path.join(args.out, "quarantine-handcheck.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"schema": "kake-r48-quarantine-handcheck-v1", "rows": results}, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"rows={len(results)} verdicts=" + ",".join(sorted({r['verdict'] for r in results})))
    return 0 if all(r["verdict"] in ("located", "absent", "unreachable") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
