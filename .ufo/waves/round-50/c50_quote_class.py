#!/usr/bin/env python3
"""Round-50 C1 counter — quote class, committed bytes only.

Frozen predicate (the same sentence in the plan, in PREDICATE, and in every
receipt):

    met: classed == 3 of 3 declared ids

An id is classed only when every rule below holds. Every artifact is read
with `git show <revision>:<path>`. This counter does not open retained text,
SOURCES.md, the lesson, or the class ledger from the worktree.

  R1  quote-classes.json names the frozen quote, a matchClass of
      collapsed-only or raw-substring, and sha256 pins for that id's text
      and raw blobs.
  R2  the derived class equals the recorded matchClass. Derived class is
      raw-substring when the quote is a substring of both blobs, and
      collapsed-only when it is a substring of the text blob only.
  R3  corpus/lessons/round-50.md contains "<id> quote class is <derived>"
      and does not contain the opposite class sentence.
  R4  for S286 only: the live registry row is mined, opened 2026-10-24,
      recheck exactly 180d, used-by exactly the admitted entry; the entry
      cites S286 below its 8-line header; the Gate quote span equals the
      frozen quote and is 6-25 whitespace tokens.

S273 is collapsed-only. S274 is a raw substring. Those labels are derived,
not assumed. A swapped label fails R2.

COMMITTED_BYTES_ONLY: no worktree open of lane artifacts.

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys

PREDICATE = "met: classed == 3 of 3 declared ids"
COMMITTED_BYTES_ONLY = True
DECLARED_IDS = ("S273", "S274", "S286")
FROZEN_QUOTES = {
    "S273": "Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit.",
    "S274": "It reduces your site's crawl rate across the whole hostname",
    "S286": "Googlebot will scale back its crawling if it detects that your servers are having trouble",
}
BLOBS = {
    "S273": (".ufo/waves/round-49/sources/S273.txt", ".ufo/waves/round-49/sources/S273.raw.html"),
    "S274": (".ufo/waves/round-49/sources/S274.txt", ".ufo/waves/round-49/sources/S274.raw.html"),
    "S286": (".ufo/waves/round-50/sources/S286.txt", ".ufo/waves/round-50/sources/S286.raw.html"),
}
LEDGER = ".ufo/waves/round-50/quote-classes.json"
LESSON = "corpus/lessons/round-50.md"
SOURCES = "corpus/SOURCES.md"
ENTRY = "corpus/knowledge/crawl-error-status-table.md"
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
            values[arg[2:]] = argv[index]
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


def classify(quote: str, raw: str, text: str) -> str:
    if quote not in text:
        return "absent"
    if quote in raw:
        return "raw-substring"
    return "collapsed-only"


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


def gate_quote(lesson: str, sid: str) -> str | None:
    in_gate = False
    for line in lesson.splitlines():
        if line.strip().startswith("## "):
            in_gate = line.strip().lower().startswith("## gate")
            continue
        if not in_gate or sid not in line or "quote:" not in line:
            continue
        match = re.search(r'quote:\s*"([^"]+)"', line)
        if match:
            return match.group(1)
    return None


def run(root: str, revision: str) -> dict:
    ledger_blob = git_show(root, revision, LEDGER)
    ledger = {}
    ledger_error = None
    if ledger_blob is None:
        ledger_error = "class ledger absent"
    else:
        try:
            parsed = json.loads(ledger_blob.decode("utf-8"))
            ledger = {row["id"]: row for row in parsed["classes"]}
        except Exception as exc:
            ledger_error = f"class ledger unreadable: {type(exc).__name__}"
    lesson_blob = git_show(root, revision, LESSON)
    lesson = (lesson_blob or b"").decode("utf-8", "replace")
    sources_blob = git_show(root, revision, SOURCES)
    rows = registry_rows((sources_blob or b"").decode("utf-8", "replace"))
    entry_blob = git_show(root, revision, ENTRY)
    entry = (entry_blob or b"").decode("utf-8", "replace")
    detail = []
    for sid in DECLARED_IDS:
        reasons = []
        quote = FROZEN_QUOTES[sid]
        if not (6 <= len(quote.split()) <= 25):
            reasons.append(f"frozen quote length {len(quote.split())}")
        if ledger_error:
            reasons.append(ledger_error)
        row = ledger.get(sid)
        text_rel, raw_rel = BLOBS[sid]
        text_blob = git_show(root, revision, text_rel)
        raw_blob = git_show(root, revision, raw_rel)
        derived = "absent"
        if text_blob is None or raw_blob is None:
            reasons.append("retained blob absent")
        else:
            text = text_blob.decode("utf-8", "replace")
            raw = raw_blob.decode("utf-8", "replace")
            derived = classify(quote, raw, text)
            if row is not None and not ledger_error:
                if row.get("quote") != quote:
                    reasons.append("ledger quote is not the frozen quote")
                if row.get("matchClass") != derived:
                    reasons.append(
                        f"recorded class {row.get('matchClass')} != derived {derived}"
                    )
                if row.get("textSha256") != hashlib.sha256(text_blob).hexdigest():
                    reasons.append("text sha256 differs")
                if row.get("rawSha256") != hashlib.sha256(raw_blob).hexdigest():
                    reasons.append("raw sha256 differs")
            elif not ledger_error:
                reasons.append("no ledger row")
        if lesson_blob is None:
            reasons.append("lesson absent")
        else:
            sentence = f"{sid} quote class is {derived}"
            opposite = "raw-substring" if derived == "collapsed-only" else "collapsed-only"
            if derived == "absent":
                reasons.append("derived class absent, so the lesson sentence cannot match")
            elif sentence not in lesson:
                reasons.append("lesson lacks the derived class sentence")
            if f"{sid} quote class is {opposite}" in lesson:
                reasons.append("lesson states the opposite class")
        if sid == "S286":
            live = rows.get(sid)
            if live is None:
                reasons.append("no live registry row")
            else:
                if live["status"] != "mined":
                    reasons.append(f"status={live['status']}")
                if live["opened"] != OPENED:
                    reasons.append(f"opened={live['opened']}")
                if live["recheck"] != "180d":
                    reasons.append(f"recheck={live['recheck']}")
                if live["used_by"] != ENTRY:
                    reasons.append(f"used-by={live['used_by']}")
            if entry_blob is None:
                reasons.append("entry absent")
            else:
                tail = "\n".join(entry.split("\n")[HEADER_LINES:])
                if sid not in tail:
                    reasons.append("entry does not cite S286 below its header")
            if lesson_blob is None:
                pass
            else:
                gate = gate_quote(lesson, sid)
                if gate != quote:
                    reasons.append("gate quote is not the frozen quote")
        detail.append({"id": sid, "ok": not reasons, "derived": derived, "reasons": reasons})
    classed = sum(1 for item in detail if item["ok"])
    return {
        "schema": "kake-r50-c1-counter-v1",
        "revision": revision,
        "predicate": PREDICATE,
        "committedBytesOnly": COMMITTED_BYTES_ONLY,
        "declaredIds": list(DECLARED_IDS),
        "classed": classed,
        "total": len(DECLARED_IDS),
        "met": classed == len(DECLARED_IDS),
        "detail": detail,
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args = parse_cli(argv)
    except UsageError as exc:
        print(f"c50_quote_class: {exc}", file=sys.stderr)
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
    print(f"C1 classed {result['classed']}/{result['total']} met={result['met']}")
    for item in result["detail"]:
        state = "ok" if item["ok"] else "FAIL"
        why = ", ".join(item["reasons"]) if item["reasons"] else "all rules hold"
        print(f"  {state} {item['id']}: {why}")
    return 0 if result["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
