#!/usr/bin/env python3
"""Round-34 C2 counter: link-preview sources backed by true quotes, plus a
stated ds4cc Open Graph census that equals a recount of retained bytes.

Derived from .ufo/waves/round-31/c2_quote_truth.py (checks a-d, ids, paths);
changes: the registry row must sit inside `## Registry`; the entry cite and the
census line are searched outside fenced code blocks; one census condition (e).

Reads committed bytes only (`git show <revision>:<path>`). Five conditions:

For each declared id (S067-S070), the id passes when all of these hold:
  a. corpus/SOURCES.md, inside `## Registry`, has a row whose first cell is the
     id, with status `mined` (cell 8), opened `2026-10-22` (cell 9) and a
     source cell containing the receipt URL;
  b. corpus/knowledge/link-preview-metadata.md cites the id as a word on a
     line after its first 8 lines and outside fenced code;
  c. corpus/lessons/round-34.md, inside `## Gate`, has exactly one line
     starting `- <id> — ` and it carries exactly one curly-quoted quote of
     6-25 words;
  d. the retained visible text .ufo/waves/round-34/sources/<id>.txt exists,
     its sha256 equals receipts.json's textSha256 for the id, the receipt
     status is 200, and the quote (whitespace collapsed) is an exact substring
     of that text.

  e. census: the retained ds4cc tree .ufo/waves/round-34/sources/ds4cc-7fc6aa2f/
     (tree.txt: first line `commit <COMMIT>`, then `git ls-tree -r` lines for
     .html paths; html.tar.xz: `git archive` of those paths, pax comment equal
     to COMMIT) is complete and blob-exact (every member's Git blob id equals
     its tree.txt line, same path set), and the entry carries exactly one line
     outside fenced code of the form
       ds4cc-7fc6aa2f-og-census: pages=N og:title=N og:type=N og:image=N og:url=N all-four=N og-url-equals-canonical=N
     whose seven numbers equal this counter's own recount: pages = HTML files;
     og:X = pages with a <meta property="og:X"> whose content is non-empty
     after stripping ASCII whitespace; all-four = pages with all four;
     og-url-equals-canonical = pages whose stripped og:url equals the first
     <link rel=canonical> href resolved against https://ds4cc.com/<path>
     (a trailing index.html removed).

Control: for every id that passes, a copy of its quote with one letter
changed must NOT be found in the retained text; if it is, the counter reports
itself broken.

Usage: python3 -B c2_source_census.py --root <lane> --revision <commit>
Exit 0 when all five conditions pass and the control holds; 1 otherwise;
2 on bad input.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import lzma
import os
import re
import subprocess
import sys
import tarfile
from html.parser import HTMLParser
from urllib.parse import urljoin

IDS = ["S067", "S068", "S069", "S070"]
ENTRY = "corpus/knowledge/link-preview-metadata.md"
LESSON = "corpus/lessons/round-34.md"
REGISTRY = "corpus/SOURCES.md"
SRC_DIR = ".ufo/waves/round-34/sources"
TREE = SRC_DIR + "/ds4cc-7fc6aa2f/tree.txt"
ARCHIVE = SRC_DIR + "/ds4cc-7fc6aa2f/html.tar.xz"
COMMIT = "7fc6aa2fc12451dd451fed5a9ee7125f3a90e884"
SITE = "https://ds4cc.com/"
QUOTE = re.compile(r"\u201c([^\u201c\u201d]+)\u201d")
CENSUS_KEYS = ["pages", "og:title", "og:type", "og:image", "og:url", "all-four", "og-url-equals-canonical"]
CENSUS = re.compile(r"^ds4cc-7fc6aa2f-og-census: " + " ".join(re.escape(k) + r"=(\d+)" for k in CENSUS_KEYS) + r"\s*$")
OG = ("og:title", "og:type", "og:image", "og:url")
WS = " \t\n\r\f"


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def section_lines(text: str, heading: str) -> list[str]:
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == heading
            continue
        if inside:
            out.append(line)
    return out


def unfenced(lines: list[str]) -> list[str]:
    out, fence = [], None
    for line in lines:
        m = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if m:
            mark = m.group(1)
            if fence is None:
                fence = mark[0] * len(mark)
                continue
            if mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
                continue
        if fence is None:
            out.append(line)
    return out


def flip_letter(q: str) -> str:
    for i, ch in enumerate(q):
        if ch.isalpha():
            return q[:i] + ("q" if ch.lower() != "q" else "z") + q[i + 1:]
    return q + " q"


class Head(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.og: dict[str, list[str]] = {}
        self.canonical: str | None = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "meta" and a.get("property") in OG and "content" in a:
            self.og.setdefault(a["property"], []).append(a["content"].strip(WS))
        elif tag == "link" and self.canonical is None and "canonical" in a.get("rel", "").lower().split():
            if "href" in a:
                self.canonical = a["href"].strip(WS)

    handle_startendtag = handle_starttag


def recount(tree_raw: bytes | None, arch_raw: bytes | None) -> tuple[dict | None, str]:
    if tree_raw is None or arch_raw is None:
        return None, "retained tree or archive missing"
    lines = tree_raw.decode("utf-8", "replace").splitlines()
    if not lines or lines[0].strip() != f"commit {COMMIT}":
        return None, "tree.txt first line is not the pinned commit"
    want = {}
    for line in lines[1:]:
        m = re.match(r"^(\d{6}) blob ([0-9a-f]{40})\t(.+)$", line)
        if not m or not m.group(3).endswith(".html"):
            return None, f"bad tree line {line[:80]!r}"
        want[m.group(3)] = m.group(2)
    if not want:
        return None, "tree lists no pages"
    try:
        tf = tarfile.open(fileobj=io.BytesIO(lzma.decompress(arch_raw)), mode="r:")
        if tf.pax_headers.get("comment") != COMMIT:
            return None, "archive pax comment is not the pinned commit"
        got = {}
        for mem in tf.getmembers():
            if mem.isfile():
                got[mem.name] = tf.extractfile(mem).read()
    except (lzma.LZMAError, tarfile.TarError, OSError, EOFError) as e:
        return None, f"archive unreadable: {e}"
    if set(got) != set(want):
        return None, f"path sets differ ({len(got)} retained, {len(want)} listed)"
    counts = dict.fromkeys(CENSUS_KEYS, 0)
    for path, data in sorted(got.items()):
        if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != want[path]:
            return None, f"blob mismatch {path}"
        h = Head()
        h.feed(data.decode("utf-8", "replace"))
        h.close()
        have = {p: any(v for v in h.og.get(p, [])) for p in OG}
        counts["pages"] += 1
        for p in OG:
            counts[p] += have[p]
        counts["all-four"] += all(have.values())
        page_url = SITE + (path[: -len("index.html")] if path.endswith("index.html") else path)
        ogurl = next((v for v in h.og.get("og:url", []) if v), None)
        if ogurl and h.canonical is not None and ogurl == urljoin(page_url, h.canonical):
            counts["og-url-equals-canonical"] += 1
    return counts, "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()
    rp = git(a.root, "rev-parse", "--verify", "--quiet", f"{a.revision}^{{commit}}")
    if rp.returncode != 0:
        print(json.dumps({"error": "revision not found", "revision": a.revision}))
        return 2
    rev = rp.stdout.decode().strip()
    registry = (show(a.root, rev, REGISTRY) or b"").decode("utf-8", "replace")
    entry = (show(a.root, rev, ENTRY) or b"").decode("utf-8", "replace")
    lesson = (show(a.root, rev, LESSON) or b"").decode("utf-8", "replace")
    receipts_raw = show(a.root, rev, f"{SRC_DIR}/receipts.json")
    try:
        receipts = json.loads(receipts_raw) if receipts_raw else {}
    except ValueError:
        receipts = {}
    reg_lines = section_lines(registry, "## Registry")
    entry_body = unfenced(entry.splitlines()[8:])
    glines = section_lines(lesson, "## Gate")
    rows, control_broken = [], False
    for sid in IDS:
        checks = {}
        rec = receipts.get(sid) if isinstance(receipts, dict) else None
        url = rec.get("url") if isinstance(rec, dict) else None
        row = next((l for l in reg_lines if re.match(rf"^\|\s*{sid}\s*\|", l)), None)
        cells = [c.strip() for c in row.strip().strip("|").split("|")] if row else []
        checks["a_row"] = bool(row and len(cells) >= 11 and cells[0] == sid and cells[7] == "mined"
                               and cells[8] == "2026-10-22" and url and url in cells[1])
        checks["b_entry_body_cites"] = any(re.search(rf"\b{sid}\b", l) for l in entry_body)
        gl = [l for l in glines if l.startswith(f"- {sid} \u2014 ")]
        quotes = QUOTE.findall(gl[0]) if len(gl) == 1 else []
        quote = collapse(quotes[0]) if len(quotes) == 1 else None
        checks["c_gate_quote"] = bool(quote) and 6 <= len(quote.split()) <= 25
        text_raw = show(a.root, rev, f"{SRC_DIR}/{sid}.txt")
        text = collapse(text_raw.decode("utf-8", "replace")) if text_raw is not None else ""
        sha_ok = (text_raw is not None and isinstance(rec, dict) and rec.get("status") == 200
                  and hashlib.sha256(text_raw).hexdigest() == rec.get("textSha256"))
        checks["d_quote_in_retained_text"] = bool(sha_ok and quote and quote in text)
        ok = all(checks.values())
        if ok and flip_letter(quote) in text:
            control_broken = True
        rows.append({"id": sid, "passed": ok, "checks": checks, "quote": quote})
    derived, why = recount(show(a.root, rev, TREE), show(a.root, rev, ARCHIVE))
    stated_lines = [m for m in (CENSUS.match(l) for l in entry_body) if m]
    stated = dict(zip(CENSUS_KEYS, map(int, stated_lines[0].groups()))) if len(stated_lines) == 1 else None
    census_ok = derived is not None and stated is not None and stated == derived
    passed = sum(r["passed"] for r in rows) + int(census_ok)
    total = len(IDS) + 1
    print(json.dumps({"counter": "kake-r34-c2-source-census",
                      "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                      "revision": rev, "met": passed, "total": total, "controlBroken": control_broken,
                      "ids": rows,
                      "census": {"passed": census_ok, "derived": derived, "derivedWhy": why,
                                 "statedLines": len(stated_lines), "stated": stated}},
                     indent=1, ensure_ascii=False))
    print(f"C2 {passed}/{total} at {rev}", file=sys.stderr)
    return 0 if passed == total and not control_broken else 1


if __name__ == "__main__":
    sys.exit(main())
