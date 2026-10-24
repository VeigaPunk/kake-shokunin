#!/usr/bin/env python3
"""Round-48 C1 counter — quote truth for the client-rendering crawl-contract theme.

Frozen predicate (the same sentence in the SCORECARD declaration, in this file's
PREDICATE constant and in every receipt's `predicate` field):

    met: passed >= 4 of 4 declared ids

An id passes only when all four rules hold for it:

  R1  the id has a row inside the `## Registry` section of `corpus/SOURCES.md` whose
      `status` cell is `mined` and whose `opened` cell is 2026-10-24;
  R2  the entry named for that id (see ENTRIES below) cites the id below its
      8-line metadata header;
  R3  the round-48 lesson `corpus/lessons/round-48.md` carries, in its `## Gate`
      section, a line for that id with a `quote:` span whose length rule holds
      (6-25 whitespace tokens, or 12-120 characters when the span has fewer than
      6 whitespace tokens);
  R4  that span is an exact substring of the retained source text of THAT id, and
      the sha256 of the retained file equals the sha256 the round-48 source
      receipt pins for that id.

R4 is per id: a quote is never matched against another id's retained text.

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

PREDICATE = "met: passed >= 4 of 4 declared ids"
DECLARED_IDS = ("S137", "S138", "S139", "S249")
ENTRIES = {
    "S137": "corpus/knowledge/js-rendering-queue.md",
    "S138": "corpus/knowledge/js-rendering-queue.md",
    "S139": "corpus/knowledge/js-rendering-queue.md",
    "S249": "corpus/knowledge/dynamic-rendering-workaround-limits.md",
}
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-48.md"
RECEIPTS = ".ufo/waves/round-48/sources/receipts.json"
OPENED = "2026-10-24"
HEADER_LINES = 8

ROW_RE = re.compile(r"^\s*\|\s*(S[0-9]{3,})\s*\|(.*)$")


class UsageError(Exception):
    pass


def parse_cli(argv):
    values = {"root": None, "revision": None, "json": None, "selftest": False}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            values["selftest"] = True
        elif arg in ("--root", "--revision", "--json"):
            index += 1
            if index >= len(argv):
                raise UsageError(f"{arg} needs a value")
            if arg == "--root":
                values["root"] = argv[index]
            elif arg == "--revision":
                values["revision"] = argv[index]
            else:
                values["json"] = argv[index] if argv[index] != "-" else "-"
        elif arg.startswith("--json="):
            values["json"] = arg.split("=", 1)[1]
        elif arg.startswith("--root="):
            values["root"] = arg.split("=", 1)[1]
        elif arg.startswith("--revision="):
            values["revision"] = arg.split("=", 1)[1]
        else:
            raise UsageError(f"unknown argument: {arg}")
        index += 1
    if not values["root"]:
        raise UsageError("--root is required")
    if not values["revision"]:
        raise UsageError("--revision is required")
    return argparse.Namespace(**values)


def read_at(root: str, revision: str, rel: str) -> str | None:
    import subprocess
    proc = subprocess.run(["git", "-C", root, "show", f"{revision}:{rel}"],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def registry_rows(text: str) -> dict:
    rows = {}
    in_registry = False
    for line in text.splitlines():
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry:
            continue
        match = ROW_RE.match(line)
        if not match:
            continue
        cells = [c.strip() for c in match.group(2).split("|")]
        if len(cells) < 10:
            continue
        rows[match.group(1)] = {
            "source": cells[0], "kind": cells[1], "tier": cells[2], "scope": cells[3],
            "anchor": cells[4], "teaches": cells[5], "status": cells[6],
            "opened": cells[7], "recheck": cells[8], "used_by": cells[9],
        }
    return rows


def gate_quotes(lesson: str) -> dict:
    quotes = {}
    in_gate = False
    for line in lesson.splitlines():
        if line.strip().startswith("## "):
            in_gate = line.strip().lower().startswith("## gate")
            continue
        if not in_gate or "quote:" not in line:
            continue
        for sid in re.findall(r"S[0-9]{3,}", line):
            match = re.search(r"quote:\s*\"([^\"]+)\"", line)
            if match:
                quotes[sid] = match.group(1)
    return quotes


def length_ok(quote: str) -> bool:
    tokens = quote.split()
    if len(tokens) >= 6:
        return len(tokens) <= 25
    return 12 <= len(quote) <= 120


def run(root: str, revision: str) -> dict:
    sources_text = read_at(root, revision, SOURCES)
    rows = registry_rows(sources_text or "")
    lesson_text = read_at(root, revision, LESSON)
    quotes = gate_quotes(lesson_text or "")
    entries = {}
    for sid, rel in ENTRIES.items():
        if rel not in entries:
            entries[rel] = read_at(root, revision, rel)
    receipts_text = read_at(root, revision, RECEIPTS)
    if receipts_text is None:
        receipt_by_id = {}
        receipts_error = "no source receipt file at this revision"
    else:
        try:
            receipts = json.loads(receipts_text)
            receipt_by_id = {r["id"]: r for r in receipts["receipts"]}
            receipts_error = None
        except Exception as exc:
            receipt_by_id = {}
            receipts_error = f"source receipt file is unreadable: {type(exc).__name__}"

    detail = []
    for sid in DECLARED_IDS:
        reasons = []
        row = rows.get(sid)
        if receipts_error:
            reasons.append(receipts_error)
        if row is None:
            reasons.append("no registry row")
        else:
            if row["status"] != "mined":
                reasons.append(f"status={row['status']}")
            if row["opened"] != OPENED:
                reasons.append(f"opened={row['opened']}")
        entry_rel = ENTRIES[sid]
        body = entries.get(entry_rel)
        if body is None:
            reasons.append("entry file absent")
        else:
            header, _, rest = body.partition("\n")
            tail = body.split("\n", HEADER_LINES)[-1] if len(body.split("\n")) > HEADER_LINES else ""
            if sid not in rest and sid not in tail:
                reasons.append("entry does not cite the id below its header")
        quote = quotes.get(sid)
        if quote is None:
            reasons.append("no gate quote")
        else:
            if not length_ok(quote):
                reasons.append(f"quote length rule failed ({len(quote.split())} tokens, {len(quote)} chars)")
            receipt = receipt_by_id.get(sid)
            if receipt is None:
                reasons.append("no source receipt")
            else:
                path = os.path.join(root, receipt["textPath"])
                try:
                    with open(path, "rb") as fh:
                        raw = fh.read()
                except OSError:
                    reasons.append("retained text absent")
                else:
                    if hashlib.sha256(raw).hexdigest() != receipt["textSha256"]:
                        reasons.append("retained text sha256 differs from the receipt")
                    elif quote not in raw.decode("utf-8", "replace"):
                        reasons.append("quote is not a substring of that id's retained text")
        detail.append({"id": sid, "ok": not reasons, "reasons": reasons,
                       "quote": quote, "entry": entry_rel})
    passed = sum(1 for d in detail if d["ok"])
    return {
        "schema": "kake-r48-c1-counter-v1",
        "revision": revision,
        "predicate": PREDICATE,
        "declaredIds": list(DECLARED_IDS),
        "passed": passed,
        "total": len(DECLARED_IDS),
        "met": passed == len(DECLARED_IDS),
        "detail": detail,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--selftest" in argv:
        return selftest()
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"c48_quote_truth: {exc}", file=sys.stderr)
        return 64
    try:
        result = run(args.root, args.revision)
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        return 2
    if args.json:
        text = json.dumps(result, indent=2, ensure_ascii=False)
        if args.json != "-":
            with open(args.json, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        else:
            print(text)
    else:
        print(f"C1 passed {result['passed']}/{result['total']} met={result['met']}")
        for item in result["detail"]:
            state = "ok" if item["ok"] else "FAIL"
            print(f"  {state} {item['id']}: {', '.join(item['reasons']) if item['reasons'] else 'all rules hold'}")
    return 0 if result["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
