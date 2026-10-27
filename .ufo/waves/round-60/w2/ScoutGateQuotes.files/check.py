#!/usr/bin/env python3
"""Audit Round 60 source quote spans and heading anchors using stdlib only."""
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
SOURCES = ROOT / ".ufo/waves/round-60/sources"

class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.in_article = False
        self.nodes = []
        self.headings = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append(tag)
        if tag == "devsite-content-footer":
            self.in_article = False
        if tag == "devsite-article-body" or (tag == "div" and "devsite-article-body" in attrs.get("class", "")):
            self.in_article = True
        if self.in_article and tag in ("h1", "h2", "h3"):
            self.headings.append((len(self.nodes), tag, ""))
    def handle_endtag(self, tag):
        if tag == "devsite-content-footer":
            self.in_article = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        if not self.in_article or any(t in ("script", "style", "template") for t in self.stack):
            return
        text = re.sub(r"\s+", " ", data).strip()
        if text:
            self.nodes.append(text)
            for i, (pos, tag, value) in enumerate(self.headings):
                if pos == len(self.nodes) - 1:
                    self.headings[i] = (pos, tag, value + " " + text)

def load_body(sid):
    path = SOURCES / f"{sid}.html"
    raw = path.read_bytes()
    parser = Article()
    parser.feed(raw.decode("utf-8", "replace"))
    return parser, hashlib.sha256(raw).hexdigest()

def units(text):
    # Current quoted spans here are all English: non-CJK whitespace-token count.
    return len(re.findall(r"\S+", text))

def spans(line):
    return re.findall(r'"([^"\n]+)"', line)

def quote_nodes(text, parser):
    flat = " ".join(parser.nodes)
    return text in flat and text in parser.nodes

def main():
    files = {
        "corpus/knowledge/google-user-triggered-fetchers.md": "S428",
        "corpus/knowledge/robots-txt-limits.md": "S429",
    }
    problems = 0
    print("SPANS:")
    for name, sid in files.items():
        lines = (ROOT / name).read_text().splitlines()
        parser, digest = load_body(sid)
        for n, line in enumerate(lines, 1):
            for text in spans(line):
                # Only article citations are claimed; metadata/shell examples are rejected explicitly.
                ok = 6 <= units(text) <= 25 and len(text) <= 160 and quote_nodes(text, parser)
                count = sum(text in node for node in parser.nodes)
                ok = ok and count == 1
                print(f"{name}:{n} {text!r}: {'PASS' if ok else 'FAIL'} units={units(text)} chars={len(text)} node_matches={count} body={digest}")
                problems += not ok
    # Correction run quotes (line 40), validate as S428. The stale shorter wording is from S426 and intentionally not S428.
    name = "corpus/knowledge/googlebot-verification.md"
    lines = (ROOT / name).read_text().splitlines()
    parser, digest = load_body("S428")
    i = next(i for i, line in enumerate(lines) if "[r60-correction 2026-10-27]" in line)
    for n in range(i, min(i + 6, len(lines))):
        for text in spans(lines[n]):
            ok = 6 <= units(text) <= 25 and len(text) <= 160 and quote_nodes(text, parser)
            count = sum(text in node for node in parser.nodes)
            ok = ok and count == 1
            print(f"{name}:{n+1} {text!r}: {'PASS' if ok else 'FAIL'} units={units(text)} chars={len(text)} node_matches={count} body={digest}")
            problems += not ok
    # Gate quotes are extracted from the three bullet lines; every quoted claim is checked against its body.
    name = "corpus/lessons/round-60.md"
    lines = (ROOT / name).read_text().splitlines()
    print("ANCHORS:")
    for sid in ("S427", "S428", "S429"):
        parser, digest = load_body(sid)
        bullet = next(line for line in lines if line.startswith(f"- {sid} —"))
        heading = re.search(r"— § (.*?) \(Last updated", bullet).group(1)
        # Compare heading label against article headings, ignoring punctuation/case only.
        names = [re.sub(r"[^\w ]", "", text).strip().casefold() for _, _, text in parser.headings]
        wanted = re.sub(r"[^\w ]", "", heading).strip().casefold()
        exact = wanted in names
        print(f"{sid}: named={heading!r} exists={exact} heading-index={names.index(wanted) if exact else 'NONE'} sha256={digest}")
        problems += not exact
        for text in spans(bullet):
            ok = 6 <= units(text) <= 25 and len(text) <= 160 and quote_nodes(text, parser)
            count = sum(text in node for node in parser.nodes)
            ok = ok and count == 1
            print(f"  quote {text!r}: {'PASS' if ok else 'FAIL'} units={units(text)} chars={len(text)} node_matches={count}")
            problems += not ok
    print(f"FINDINGS: {problems} checker failures")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
