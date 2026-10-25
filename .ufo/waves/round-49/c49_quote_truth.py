#!/usr/bin/env python3
"""Round-49 C2 counter — quote truth, committed bytes only.

Frozen predicate (the same sentence in the plan, in PREDICATE, and in every
receipt):

    met: passed >= 2 of 2 declared ids

An id passes only when all four rules hold, each read with
`git show <revision>:<path>` and never by opening a worktree file:

  R1  the id has a row inside `## Registry` of `corpus/SOURCES.md` whose
      status cell is `mined` and whose opened cell is 2026-10-24;
  R2  `corpus/knowledge/crawl-budget-consequences.md` cites the id below its
      8-line metadata header;
  R3  `corpus/lessons/round-49.md` `## Gate` carries a quote: span for that
      id of 6-25 whitespace tokens;
  R4  that span is an exact substring of `git show <revision>:.ufo/waves/round-49/sources/<textPath>`,
      and the sha256 of that blob equals the receipt pin for that id.

R4 is per id. A quote is never matched against another id's blob.
COMMITTED_BYTES_ONLY: this counter does not open retained text, SOURCES.md,
or the lesson from the worktree.

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys

PREDICATE = "met: passed >= 2 of 2 declared ids"
COMMITTED_BYTES_ONLY = True
DECLARED_IDS = ("S273", "S274")
ENTRY = "corpus/knowledge/crawl-budget-consequences.md"
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-49.md"
RECEIPTS = ".ufo/waves/round-49/sources/receipts.json"
OPENED = "2026-10-24"
HEADER_LINES = 8
ROW_RE = re.compile(r"^\s*\|\s*(S[0-9]{3,})\s*\|(.*)$")


class UsageError(Exception):
    pass


def parse_cli(argv):
    values = {"root": None, "revision": None, "json": None}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--root", "--revision", "--json"):
            index += 1
            if index >= len(argv):
                raise UsageError(f"{arg} needs a value")
            key = arg[2:]
            values[key] = argv[index]
        elif arg.startswith("--root="):
            values["root"] = arg.split("=", 1)[1]
        elif arg.startswith("--revision="):
            values["revision"] = arg.split("=", 1)[1]
        elif arg.startswith("--json="):
            values["json"] = arg.split("=", 1)[1]
        else:
            raise UsageError(f"unknown argument: {arg}")
        index += 1
    if not values["root"] or not values["revision"]:
        raise UsageError("--root and --revision are required")
    return values


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


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
            "status": cells[6],
            "opened": cells[7],
            "recheck": cells[8],
            "used_by": cells[9],
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
        match = re.search(r'quote:\s*"([^"]+)"', line)
        if not match:
            continue
        for sid in re.findall(r"S[0-9]{3,}", line):
            quotes[sid] = match.group(1)
    return quotes


def run(root: str, revision: str) -> dict:
    sources_blob = git_show(root, revision, SOURCES)
    rows = registry_rows((sources_blob or b"").decode("utf-8", "replace"))
    lesson_blob = git_show(root, revision, LESSON)
    quotes = gate_quotes((lesson_blob or b"").decode("utf-8", "replace"))
    entry_blob = git_show(root, revision, ENTRY)
    entry = (entry_blob or b"").decode("utf-8", "replace")
    receipts_blob = git_show(root, revision, RECEIPTS)
    receipt_by_id = {}
    receipts_error = None
    if receipts_blob is None:
        receipts_error = "no source receipt file at this revision"
    else:
        try:
            receipts = json.loads(receipts_blob.decode("utf-8"))
            receipt_by_id = {row["id"]: row for row in receipts["receipts"]}
        except Exception as exc:
            receipts_error = f"source receipt file is unreadable: {type(exc).__name__}"
    detail = []
    for sid in DECLARED_IDS:
        reasons = []
        if receipts_error:
            reasons.append(receipts_error)
        row = rows.get(sid)
        if row is None:
            reasons.append("no registry row")
        else:
            if row["status"] != "mined":
                reasons.append(f"status={row['status']}")
            if row["opened"] != OPENED:
                reasons.append(f"opened={row['opened']}")
        if entry_blob is None:
            reasons.append("entry file absent")
        else:
            tail = "\n".join(entry.split("\n")[HEADER_LINES:])
            if sid not in tail:
                reasons.append("entry does not cite the id below its header")
        quote = quotes.get(sid)
        if quote is None:
            reasons.append("no gate quote")
        elif not (6 <= len(quote.split()) <= 25):
            reasons.append(f"quote length rule failed ({len(quote.split())} tokens)")
        receipt = receipt_by_id.get(sid)
        if quote is not None and receipt is None and not receipts_error:
            reasons.append("no source receipt")
        if quote is not None and receipt is not None:
            rel = f".ufo/waves/round-49/sources/{receipt['textPath']}"
            blob = git_show(root, revision, rel)
            if blob is None:
                reasons.append("retained text absent at revision")
            else:
                digest = hashlib.sha256(blob).hexdigest()
                if digest != receipt["textSha256"]:
                    reasons.append("retained text sha256 differs from the receipt")
                elif quote not in blob.decode("utf-8", "replace"):
                    reasons.append("quote is not a substring of that id's committed text")
        detail.append({"id": sid, "ok": not reasons, "reasons": reasons, "quote": quote})
    passed = sum(1 for item in detail if item["ok"])
    return {
        "schema": "kake-r49-c2-counter-v1",
        "revision": revision,
        "predicate": PREDICATE,
        "committedBytesOnly": COMMITTED_BYTES_ONLY,
        "declaredIds": list(DECLARED_IDS),
        "passed": passed,
        "total": len(DECLARED_IDS),
        "met": passed >= len(DECLARED_IDS) and passed == len(DECLARED_IDS),
        "detail": detail,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"c49_quote_truth: {exc}", file=sys.stderr)
        return 64
    try:
        result = run(args["root"], args["revision"])
    except Exception as exc:
        print(json.dumps({"error": f"{type(exc).__name__}: {exc}"}))
        return 2
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args["json"]:
        with open(args["json"], "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(f"C2 passed {result['passed']}/{result['total']} met={result['met']}")
    for item in result["detail"]:
        state = "ok" if item["ok"] else "FAIL"
        why = ", ".join(item["reasons"]) if item["reasons"] else "all rules hold"
        print(f"  {state} {item['id']}: {why}")
    return 0 if result["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
