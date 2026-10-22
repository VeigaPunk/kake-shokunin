#!/usr/bin/env python3
"""Round-31 C2 counter: new Render web-service and Blueprint source rows backed by true quotes.

Derived from .ufo/waves/round-30/c2_quote_truth.py (blob a2cd3164); changes:
ids, paths, and a quote must now have 6 to 25 words (round-30 wave 1 showed a
one-word or navigation quote could pass).

For each declared id (S057-S060) it reads committed bytes only
(`git show <revision>:<path>`) and passes the id when all of these hold:

  a. corpus/SOURCES.md has a registry row for the id with status `mined`,
     opened `2026-10-22`, and a source cell containing the receipt URL;
  b. corpus/knowledge/render-web-services.md cites the id as a word on a line
     after its first 8 lines (the metadata header alone does not count);
  c. corpus/lessons/round-31.md, inside `## Gate`, has a line starting
     `- <id> — ` that carries one curly-quoted quote of 6-25 words;
  d. the retained visible text .ufo/waves/round-31/sources/<id>.txt exists,
     its sha256 equals receipts.json's textSha256 for the id, and the quote
     (whitespace collapsed) is an exact substring of that text.

Control: for every id that passes, a copy of its quote with one letter
changed must NOT be found; if it is, the counter reports itself broken.

Usage: python3 -B c2_quote_truth.py --root <lane> --revision <commit>
Exit 0 when every id passes and the control holds; 1 otherwise; 2 on bad input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

IDS = ["S057", "S058", "S059", "S060"]
ENTRY = "corpus/knowledge/render-web-services.md"
LESSON = "corpus/lessons/round-31.md"
REGISTRY = "corpus/SOURCES.md"
SRC_DIR = ".ufo/waves/round-31/sources"
QUOTE = re.compile(r"\u201c([^\u201c\u201d]+)\u201d")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def gate_lines(lesson: str) -> list[str]:
    out, inside = [], False
    for line in lesson.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Gate"
            continue
        if inside:
            out.append(line)
    return out


def flip_letter(q: str) -> str:
    for i, ch in enumerate(q):
        if ch.isalpha():
            return q[:i] + ("q" if ch.lower() != "q" else "z") + q[i + 1:]
    return q + " q"


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
    entry_body = entry.splitlines()[8:]
    glines = gate_lines(lesson)
    rows, control_broken = [], False
    for sid in IDS:
        checks = {}
        rec = receipts.get(sid) if isinstance(receipts, dict) else None
        url = rec.get("url") if isinstance(rec, dict) else None
        row = next((l for l in registry.splitlines() if re.match(rf"^\|\s*{sid}\s*\|", l)), None)
        cells = [c.strip() for c in row.strip().strip("|").split("|")] if row else []
        checks["a_row"] = bool(row and len(cells) >= 11 and cells[7] == "mined" and cells[8] == "2026-10-22"
                               and url and url in cells[1])
        checks["b_entry_body_cites"] = any(re.search(rf"\b{sid}\b", l) for l in entry_body)
        gl = [l for l in glines if l.startswith(f"- {sid} \u2014 ")]
        quotes = QUOTE.findall(gl[0]) if len(gl) == 1 else []
        quote = collapse(quotes[0]) if len(quotes) == 1 else None
        checks["c_gate_quote"] = bool(quote) and 6 <= len(quote.split()) <= 25
        text_raw = show(a.root, rev, f"{SRC_DIR}/{sid}.txt")
        text = collapse(text_raw.decode("utf-8", "replace")) if text_raw is not None else ""
        sha_ok = (text_raw is not None and isinstance(rec, dict)
                  and hashlib.sha256(text_raw).hexdigest() == rec.get("textSha256"))
        checks["d_quote_in_retained_text"] = bool(sha_ok and quote and quote in text)
        ok = all(checks.values())
        if ok and flip_letter(quote) in text:
            control_broken = True
        rows.append({"id": sid, "passed": ok, "checks": checks, "quote": quote})
    passed = sum(r["passed"] for r in rows)
    print(json.dumps({"counter": "kake-r31-c2-quote-truth",
                      "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                      "revision": rev, "passed": passed,
                      "total": len(IDS), "controlBroken": control_broken, "ids": rows}, indent=1, ensure_ascii=False))
    print(f"C2 {passed}/{len(IDS)} at {rev}", file=sys.stderr)
    return 0 if passed == len(IDS) and not control_broken else 1


if __name__ == "__main__":
    sys.exit(main())
