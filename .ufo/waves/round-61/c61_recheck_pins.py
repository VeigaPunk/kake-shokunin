#!/usr/bin/env python3
"""Round-61 C3 counter — freshness (sourced): the ten oldest registry rows re-verified live and their recheck
cadences pinned to concrete dates.

Version 1 (frozen with the round-61 counters before any data is scored). Written to contract § Claim C3.

Offline. Committed bytes only (`git cat-file`-family plumbing: `git show <rev>:<path>`, `git ls-tree`); the
worktree is never read, inherited `GIT_*` is scrubbed, and no network call is made. `--root` must be the
toplevel of a git repository holding the frozen base revision.

Surface
-------
Registry `corpus/SOURCES.md` (0-3 leading spaces before the pipe, under `## Registry`), the round-61 lesson
`corpus/lessons/round-61.md`, and the retained recheck evidence under `.ufo/waves/round-61/recheck/`:
each retained body as a committed file whose stem is the row id (`Sxxx.html`, any extension), and the
receipt file `recheck/receipts.json` carrying one entry per fetch
(`url`, `effectiveUrl`, `status`|`httpStatus`, `sha256`, `bytes`, `fetchedAt`, `userAgent`).

Frozen due set (contract § Claim C3, re-derived here from base data): non-rejected rows with the oldest
`opened` date, ties by lowest id, the lowest ten taken — S001, S002, S003, S004, S005, S006, S007, S008,
S009, S010 (all opened 2026-10-19; 16 ties at base).

Conditions (each carries the contract sentence it implements):

  C1 due-set rule re-derived at the measured revision yields exactly the frozen ten ids (rows present,
     non-rejected, opened 2026-10-19, lowest 10 by id); every registry row keeps a well-formed 11-cell shape.
  C2 for each pinned row the recheck cell is a concrete ISO date, `opened < pinned <= opened + cadence` for
     `Nd` cadences at base, or `= opened + 90d` for the two non-`Nd` rows (S001, S002 `on-release`). An
     unpinned due row's cell is its base cadence (any other non-ISO value is a cell rewrite, not a carry).
     At least one due row is pinned — the do-nothing control at base must fail here with 0 concrete dates.
  C3 each pinned row has a lesson Gate line carrying one of the row's URLs, the access date, and one
     double-quoted span (6..25 whitespace units, <= 160 characters, ASCII) that is a substring of one
     whitespace-collapsed text node of the row's retained fresh body, page-unique. A quoted span at or
     above the 6-unit evidence floor is a claim quote and any violation fails; a shorter span is context
     (an anchor name, a status word) and fails only when it is not body text at all.
  C4 each pinned row has a retained body whose receipt pins sha256, bytes, HTTP 200, `fetchedAt` on the
     access date (UTC), userAgent carrying `round61`, and receipt URL = one of the row's URLs; every sha256
     matches the committed blob and every byte count matches its length. A body retained for a carried row
     must be receipt-consistent (a non-200 status is recorded, not failed: the carry rule allows it).
  C5 an unpinned due row has a Gate note naming the observed state and keeps its base cadence; there is no
     pinned row without a Gate line.
  C6 every base-registry row outside the due set is byte-identical to base; a due row differs from base only
     in its `recheck` cell; every base row id is still present. Appended rows are permitted (C2 appends
     S430-S433 this round) and are recorded, not failed.

Text nodes: an HTML body contributes the text between tags after comments, `script`/`style`/`noscript`/
`svg`/`template`/`head` and page chrome (`nav`/`aside`/`header`/`footer`/`form`) are blanked; a body with
no tags (raw YAML / C / texi) contributes its blank-line-separated paragraph blocks. Nodes are
whitespace-collapsed; entities are not decoded (a span containing `&amp;` must be written as `&amp;`).

Predicate (frozen in `contract.json`):

    met: conditions_passed == 6 of 6

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone

PREDICATE = "met: conditions_passed == 6 of 6"
ROUND_DATE = "2026-10-27"  # UTC access date of the round-61 live work
BASE_REV = "9f07731a873585e655a6518233ea39f5d9fb8204"  # lane master at round open
REGISTRY = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-61.md"
WAVE = ".ufo/waves/round-61"
RECHECK_DIR = f"{WAVE}/recheck"
RECEIPTS = f"{RECHECK_DIR}/receipts.json"

DUE = ("S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008", "S009", "S010")
DUE_OPENED = "2026-10-19"
SWEEP = 10
DEFAULT_PIN_DAYS = 90  # the non-`Nd` pin: opened + 90d
UNIT_FLOOR = 6
UNIT_CEILING = 25
CHAR_CEILING = 160
UA_TAG = "round61"
NON_ND_CADENCES = ("on-release", "on-use")

ROW_RE = r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|"
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
CADENCE_DAYS = re.compile(r"(\d+)d")
CJK_RE = re.compile(
    "[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
CURLY = re.compile("[\u201c\u201d\u201e\u201f]")
TAG_CLOSE = re.compile(r"</[a-zA-Z][^>]{0,120}>")
CHROME = re.compile(
    r"(?is)<(script|style|noscript|svg|template|head|nav|aside|header|footer|form)\b.*?</\1\s*>")
COMMENT = re.compile(r"(?is)<!--.*?-->")
INLINE = re.compile(r"(?is)</?(?:a|abbr|b|bdi|bdo|cite|code|del|em|i|ins|kbd|mark|q|s|samp|small|span|strong"
                    r"|sub|sup|u|var)\b[^>]*>")
OBSERVED = re.compile(
    r"(?i)(anchor_moved|page_changed|fetch_failed|fetch failed|quote[- ]missing|no anchor"
    r"|anchor not (?:found|located)|not located|not found in (?:the )?body|non-200"
    r"|status\s*[:=]?\s*[1-5]\d\d|http\s+[1-5]\d\d|timed out|timeout|unreachable|refused|redirected?)")

CELL_NAMES = ("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used-by")


# --------------------------------------------------------------------------- git plumbing


def clean_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    return env


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, env=clean_env())
    return proc.returncode, proc.stdout


def show_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env())
    return proc.stdout if proc.returncode == 0 else None


def show(root: str, rev: str, path: str) -> str | None:
    raw = show_bytes(root, rev, path)
    if raw is None:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def ls_tree(root: str, rev: str, path: str) -> list[str]:
    rc, out = git(root, "ls-tree", "-r", "--name-only", rev, "--", path)
    return [line for line in out.splitlines() if line.strip()] if rc == 0 else []


# --------------------------------------------------------------------------- registry


def _rows_of(registry_text: str) -> list[tuple[str, str, list[str]]]:
    """(id, raw line, cells) in file order, scoped to `## Registry`."""
    out: list[tuple[str, str, list[str]]] = []
    in_registry = False
    for line in registry_text.split("\n"):
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry:
            continue
        m = re.match(ROW_RE, line)
        if not m:
            continue
        out.append((m.group(1), line, [c.strip() for c in line.strip().strip("|").split("|")]))
    return out


def parse_registry(registry_text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for sid, _line, cells in _rows_of(registry_text):
        rows.setdefault(sid, cells)
    return rows


def row_lines(registry_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for sid, line, _cells in _rows_of(registry_text):
        out.setdefault(sid, line)
    return out


def id_number(sid: str) -> int:
    return int(sid[1:])


def row_urls(cells: list[str] | None) -> list[str]:
    """Every http(s) URL the row's source cell names, in order (S001/S002 name two URLs)."""
    if not cells or len(cells) < 2:
        return []
    out: list[str] = []
    for token in cells[1].split():
        token = token.strip(".,;:)]}\"'")
        if token.startswith(("http://", "https://")) and token not in out:
            out.append(token)
    return out


def row_url(cells: list[str] | None) -> str | None:
    urls = row_urls(cells)
    return urls[-1] if urls else None


# --------------------------------------------------------------------------- text nodes


def units(text: str) -> int:
    """One unit per CJK character, one per non-CJK whitespace token (the lane's unit rule)."""
    return len(CJK_RE.findall(text)) + len([t for t in text.split() if not CJK_RE.search(t)])


def body_nodes(raw: bytes) -> list[str]:
    """Whitespace-collapsed text nodes of a retained body (see the module docstring)."""
    text = raw.decode("utf-8", "replace")
    if TAG_CLOSE.search(text):
        chunk = COMMENT.sub(" ", text)
        chunk = CHROME.sub(" ", chunk)
        nodes = re.findall(r">([^<>]+)(?=<)", chunk)
    else:
        nodes = re.split(r"\n[ \t]*\n", text)
    out = []
    for node in nodes:
        node = re.sub(r"\s+", " ", node).strip()
        if node:
            out.append(node)
    return out


def inline_flattened(raw: bytes) -> list[str]:
    """Diagnostic view only: the same nodes with inline emphasis/link tags removed, so a span that exists on the
    page but crosses inline markup can be named as such (the quote rule still requires one text node)."""
    text = raw.decode("utf-8", "replace")
    if not TAG_CLOSE.search(text):
        return body_nodes(raw)
    chunk = INLINE.sub("", CHROME.sub(" ", COMMENT.sub(" ", text)))
    return [re.sub(r"\s+", " ", node).strip() for node in re.findall(r">([^<>]+)(?=<)", chunk) if node.strip()]


def span_hits(span: str, nodes: list[str]) -> list[int]:
    return [i for i, node in enumerate(nodes) if span in node]


# --------------------------------------------------------------------------- lesson gates


def gate_lines(lesson: str) -> list[str]:
    out, in_gate, fence = [], False, None
    for line in lesson.splitlines():
        mark = re.match(r"^\s*(```+|~~~+)", line)
        if mark:
            token = mark.group(1)[0]
            fence = None if fence == token else (token if fence is None else fence)
            continue
        if fence:
            continue
        if line.strip().startswith("## "):
            in_gate = line.strip().lstrip("#").strip().lower().startswith("gate")
            continue
        if in_gate:
            out.append(line)
    return out


def gate_line(lesson: str, sid: str) -> str | None:
    """The row's Gate line: a bullet whose leading token is the id, or a table row whose first cell is it."""
    bullet = re.compile(r"^[-*]\s+\**" + re.escape(sid) + r"\**\b")
    table = re.compile(r"^\|\s*\**" + re.escape(sid) + r"\**\s*\|")
    for line in gate_lines(lesson):
        stripped = line.strip()
        if bullet.match(stripped) or table.match(stripped):
            return stripped
    return None


# --------------------------------------------------------------------------- receipts / dates


def first_key(entry: dict, *keys: str):
    for key in keys:
        if key in entry and entry[key] not in (None, ""):
            return entry[key]
    return None


def load_receipts(raw: bytes | None) -> tuple[list[dict] | None, str]:
    if raw is None:
        return None, "absent at the measured revision"
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return None, f"not parseable JSON ({exc.__class__.__name__})"
    if isinstance(doc, list):
        return [e for e in doc if isinstance(e, dict)], ""
    if isinstance(doc, dict):
        for key in ("receipts", "sources"):
            value = doc.get(key)
            if isinstance(value, list):
                return [e for e in value if isinstance(e, dict)], ""
            if isinstance(value, dict):
                out = []
                for sid, entry in value.items():
                    if isinstance(entry, dict):
                        entry = dict(entry)
                        entry.setdefault("id", sid)
                        out.append(entry)
                return out, ""
        if "url" in doc:
            return [doc], ""
    return None, "no `receipts` list"


def parse_iso(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp if stamp.tzinfo else None


def is_iso_date(value: str) -> bool:
    if not ISO_DATE.fullmatch(value or ""):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def as_int(value) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- checks


def run_checks(root: str, rev: str, base_rev: str = BASE_REV) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, notes: list[str], facts: dict | None = None) -> None:
        results.append({"check": check, "state": "pass" if not notes else "fail",
                        "notes": notes, "facts": facts or {}})

    def unevaluable(check: str, note: str) -> tuple[int, list[dict]]:
        return 2, results + [{"check": check, "state": "unevaluable", "notes": [note], "facts": {}}]

    registry_text = show(root, rev, REGISTRY)
    if registry_text is None:
        return unevaluable("C1_due_set", f"{REGISTRY} is not readable at revision {rev[:12]}")
    base_text = show(root, base_rev, REGISTRY)
    if base_text is None:
        return unevaluable("C1_due_set", f"base revision {base_rev[:12]} does not hold {REGISTRY} (shallow clone or exported tree?)")

    rows = parse_registry(registry_text)
    base_rows = parse_registry(base_text)
    rows_raw = row_lines(registry_text)
    base_raw = row_lines(base_text)
    lesson = show(root, rev, LESSON) or ""

    # ---------------------------------------------------------------- C1: the due-set rule
    c1: list[str] = []
    eligible: list[tuple[str, str]] = []
    shapes: list[str] = []
    for sid, cells in rows.items():
        if len(cells) != 11:
            shapes.append(f"{sid}: registry row has {len(cells)} cells, expected 11")
            continue
        opened, status = cells[8], cells[7]
        if not is_iso_date(opened):
            shapes.append(f"{sid}: opened cell {opened!r} is not an ISO date")
            continue
        if status != "rejected":
            eligible.append((opened, sid))
    oldest = min((opened for opened, _sid in eligible), default=None)
    ties = sorted([sid for opened, sid in eligible if opened == oldest], key=id_number)
    derived = ties[:SWEEP]
    if oldest != DUE_OPENED:
        c1.append(f"oldest opened date at the measured revision is {oldest!r}, the frozen sweep is {DUE_OPENED!r}")
    if derived != list(DUE):
        c1.append(f"re-derived due set {derived} != frozen {list(DUE)}")
    if len(ties) < SWEEP:
        c1.append(f"only {len(ties)} non-rejected row(s) at {oldest!r}; the sweep needs {SWEEP}")
    c1.extend(shapes)
    add("C1_due_set", c1, {"oldest": oldest, "ties": len(ties), "derived": derived,
                           "rejected_filtered": len(rows) - len(eligible) - len(shapes)})

    # ---------------------------------------------------------------- C2: pinned dates
    c2: list[str] = []
    pinned: dict[str, str] = {}
    carried: dict[str, str] = {}
    pin_facts: dict[str, dict] = {}
    for sid in DUE:
        cells = rows.get(sid)
        base_cells = base_rows.get(sid)
        if cells is None:
            c2.append(f"{sid}: due row absent at the measured revision")
            continue
        if base_cells is None:
            c2.append(f"{sid}: due row absent from the base registry")
            continue
        if len(cells) < 10:
            c2.append(f"{sid}: registry row is too short to carry a recheck cell")
            continue
        cell = cells[9]
        cadence = base_cells[9]
        if not is_iso_date(base_cells[8]):
            c2.append(f"{sid}: base opened cell {base_cells[8]!r} is not an ISO date; no pin bound is derivable")
            continue
        opened = date.fromisoformat(base_cells[8])
        if is_iso_date(cell):
            pinned[sid] = cell
            pin = date.fromisoformat(cell)
            days = CADENCE_DAYS.fullmatch(cadence)
            if days:
                upper = opened + timedelta(days=int(days.group(1)))
                pin_facts[sid] = {"cadence": cadence, "pinned": cell, "upper": upper.isoformat(),
                                  "exact": pin == upper}
                if not (opened < pin <= upper):
                    c2.append(f"{sid}: pinned {cell} outside (opened {opened.isoformat()}, opened+{cadence} {upper.isoformat()}]")
            elif cadence in NON_ND_CADENCES:
                expected = opened + timedelta(days=DEFAULT_PIN_DAYS)
                pin_facts[sid] = {"cadence": cadence, "pinned": cell, "upper": expected.isoformat(),
                                  "exact": pin == expected}
                if pin != expected:
                    c2.append(f"{sid}: non-Nd cadence {cadence!r} pinned {cell}, expected opened+90d {expected.isoformat()}")
            else:
                pin_facts[sid] = {"cadence": cadence, "pinned": cell, "upper": None, "exact": False}
                c2.append(f"{sid}: base cadence {cadence!r} has no declared pin rule")
        else:
            carried[sid] = cell
            if cell != cadence:
                c2.append(f"{sid}: unpinned recheck cell {cell!r} is neither a concrete ISO date nor the base cadence {cadence!r}")
    if not pinned:
        c2.append("no due row carries a concrete ISO recheck date (0 pins: the sweep did not run)")
    add("C2_pinned_dates", c2, {"pinned": len(pinned), "carried": len(carried), "pins": pin_facts})

    # retained bodies (committed blobs under recheck/), keyed by row id
    bodies: dict[str, bytes] = {}
    extra_bodies: dict[str, bytes] = {}
    for rel in ls_tree(root, rev, RECHECK_DIR):
        if rel == RECEIPTS:
            continue
        blob = show_bytes(root, rev, rel)
        if blob is None:
            continue
        stem = os.path.splitext(os.path.basename(rel))[0]
        if re.fullmatch(r"S[0-9]{3,}", stem) and stem in rows:
            bodies[stem] = blob
        elif os.path.splitext(rel)[1].lower() in (".html", ".htm"):
            extra_bodies[rel] = blob

    nodes_by_sid = {sid: body_nodes(blob) for sid, blob in bodies.items()}

    # ---------------------------------------------------------------- C3: Gate quotes
    c3: list[str] = []
    quote_facts: dict[str, list] = {}
    retained_obs: dict[str, list] = {}
    for sid in pinned:
        if sid not in DUE:
            continue
        urls = row_urls(rows.get(sid))
        line = gate_line(lesson, sid)
        if line is None:
            c3.append(f"{sid}: pinned row has no lesson Gate line")
            continue
        if not urls:
            c3.append(f"{sid}: registry row names no URL for the Gate line to carry")
        elif not any(url in line for url in urls):
            c3.append(f"{sid}: Gate line carries none of the row URLs {urls}")
        if ROUND_DATE not in line:
            c3.append(f"{sid}: Gate line does not carry the access date {ROUND_DATE}")
        if CURLY.search(line):
            c3.append(f"{sid}: Gate line carries curly double quotes (the quote rule is ASCII)")
        blob = bodies.get(sid)
        spans = re.findall(r'"([^"]{1,600})"', line)
        record: list[dict] = []
        good: list[str] = []
        observations: list[str] = []
        for span in spans:
            count = units(span)
            if count < 2:
                observations.append(f'"{span}" is below the 2-unit quote floor and is not read as a quote')
                continue
            problems: list[str] = []
            if not span.isascii():
                problems.append("not ASCII")
            if not (UNIT_FLOOR <= count <= UNIT_CEILING):
                problems.append(f"{count} units outside {UNIT_FLOOR}..{UNIT_CEILING}")
            if len(span) > CHAR_CEILING:
                problems.append(f"{len(span)} characters above {CHAR_CEILING}")
            hits: list[int] = []
            if blob is None:
                problems.append("no retained body to locate the span in")
            else:
                hits = span_hits(span, nodes_by_sid.get(sid, []))
                if not hits:
                    if span_hits(span, inline_flattened(blob)):
                        problems.append("not a substring of any whitespace-collapsed text node of the retained body "
                                        "(it occurs only across inline markup)")
                    else:
                        problems.append("not a substring of any whitespace-collapsed text node of the retained body")
                elif len(hits) > 1:
                    problems.append(f"occurs in {len(hits)} text nodes (not page-unique)")
            # A quote at or above the evidence floor (6 units) is a claim quote: any violation fails. A shorter
            # quote is context (an anchor name, a status word): it only fails when it is not body text at all.
            claim_sized = count >= UNIT_FLOOR
            record.append({"span": span, "units": count, "chars": len(span), "claim_sized": claim_sized,
                           "problems": problems, "nodes": hits})
            if not problems:
                good.append(span)
            elif claim_sized or not hits:
                c3.append(f'{sid}: quoted span "{span[:70]}" — ' + "; ".join(problems))
            else:
                observations.append(f'"{span[:60]}" ({count} units) is body text but below the {UNIT_FLOOR}-unit '
                                    f"evidence floor; it is not counted as the located quote")
        quote_facts[sid] = record
        if not spans:
            c3.append(f"{sid}: Gate line carries no ASCII double-quoted span")
        elif not good:
            c3.append(f"{sid}: no double-quoted span on the Gate line passes the quote rules")
        if observations:
            retained_obs.setdefault(sid, []).extend(observations)
    add("C3_gate_quotes", c3, {"gate_lines": len(quote_facts),
                               "passing_spans": {sid: [r["span"][:40] for r in rec if not r["problems"]]
                                                 for sid, rec in quote_facts.items()},
                               "observations": retained_obs})

    # ---------------------------------------------------------------- C4: receipt pins
    c4: list[str] = []
    receipt_raw = show_bytes(root, rev, RECEIPTS)
    receipts, problem = load_receipts(receipt_raw)
    receipt_facts: dict[str, dict] = {"entries": 0 if receipts is None else len(receipts)}
    if receipts is None:
        if pinned or bodies or extra_bodies:
            c4.append(f"{RECEIPTS}: {problem}")
        receipts = []

    def violations(sid: str, entry: dict, urls: list[str], blob: bytes) -> list[str]:
        out: list[str] = []
        url = str(first_key(entry, "url", "requestUrl") or "").strip()
        if urls and url not in urls:
            out.append(f"receipt url {url!r} is not one of the row URLs {urls}")
        status = as_int(first_key(entry, "status", "httpStatus"))
        if status != 200:
            out.append(f"recorded status {first_key(entry, 'status', 'httpStatus')!r} is not HTTP 200")
        digest = hashlib.sha256(blob).hexdigest()
        recorded = str(first_key(entry, "sha256", "digest") or "").strip().lower()
        if recorded != digest:
            out.append(f"receipt sha256 {recorded[:12] or '?'} != committed blob sha256 {digest[:12]}")
        nbytes = as_int(first_key(entry, "bytes", "length"))
        if nbytes != len(blob):
            out.append(f"receipt bytes {first_key(entry, 'bytes', 'length')!r} != committed blob length {len(blob)}")
        stamp = parse_iso(first_key(entry, "fetchedAt", "fetched_at"))
        if stamp is None:
            out.append(f"fetchedAt {first_key(entry, 'fetchedAt', 'fetched_at')!r} is not ISO-8601 with an offset")
        elif stamp.astimezone(timezone.utc).date().isoformat() != ROUND_DATE:
            out.append(f"fetchedAt {stamp.isoformat()} is not on the access date {ROUND_DATE} (UTC)")
        ua = str(first_key(entry, "userAgent", "user_agent") or "")
        if UA_TAG not in ua.lower():
            out.append(f"userAgent {ua!r} does not carry the {UA_TAG} tag")
        return out

    def match_receipt(sid: str, urls: list[str]) -> list[dict]:
        picked: list[dict] = []
        for entry in receipts:
            url = str(first_key(entry, "url", "requestUrl") or "").strip()
            ident = str(first_key(entry, "id", "sid", "row") or "").strip()
            if (urls and url in urls) or (ident == sid):
                picked.append(entry)
        return picked

    for sid in pinned:
        urls = row_urls(rows.get(sid))
        blob = bodies.get(sid)
        if blob is None:
            c4.append(f"{sid}: pinned row has no retained body under {RECHECK_DIR}/")
            continue
        candidates = match_receipt(sid, urls)
        if not candidates:
            c4.append(f"{sid}: no receipt whose url is one of the row's URLs {urls}")
            continue
        scored = sorted(((violations(sid, entry, urls, blob), entry) for entry in candidates),
                        key=lambda pair: len(pair[0]))
        best, entry = scored[0]
        receipt_facts[sid] = {"url": first_key(entry, "url"), "status": first_key(entry, "status", "httpStatus"),
                              "bytes": first_key(entry, "bytes"), "sha256": first_key(entry, "sha256"),
                              "fetchedAt": first_key(entry, "fetchedAt", "fetched_at"),
                              "userAgent": first_key(entry, "userAgent", "user_agent")}
        for note in best:
            c4.append(f"{sid}: {note}")

    for sid, blob in bodies.items():
        if sid in pinned or sid not in DUE:
            continue
        urls = row_urls(rows.get(sid))
        candidates = match_receipt(sid, urls)
        if not candidates:
            c4.append(f"{sid}: retained body for a carried row has no receipt")
            continue
        digest = hashlib.sha256(blob).hexdigest()
        entry = candidates[0]
        recorded = str(first_key(entry, "sha256", "digest") or "").strip().lower()
        nbytes = as_int(first_key(entry, "bytes", "length"))
        if recorded != digest or nbytes != len(blob):
            c4.append(f"{sid}: carried body disagrees with its receipt (sha256 {recorded[:12] or '?'}, "
                      f"bytes {first_key(entry, 'bytes')!r}; committed {digest[:12]}, {len(blob)})")
        else:
            receipt_facts.setdefault("carried", {})[sid] = {
                "status": first_key(entry, "status", "httpStatus"),
                "note": "non-200 body retained; the carry rule allows it" if as_int(
                    first_key(entry, "status", "httpStatus")) != 200 else "200 body retained for an unpinned row"}

    for rel, blob in extra_bodies.items():
        digest = hashlib.sha256(blob).hexdigest()
        matches = [e for e in receipts if str(first_key(e, "sha256", "digest") or "").strip().lower() == digest]
        if not matches:
            c4.append(f"{rel}: retained body has no receipt pinning its sha256 {digest[:12]}")
            continue
        if as_int(first_key(matches[0], "bytes", "length")) != len(blob):
            c4.append(f"{rel}: receipt bytes != committed length {len(blob)}")
    add("C4_receipt_pins", c4, receipt_facts)

    # ---------------------------------------------------------------- C5: carry notes
    c5: list[str] = []
    carry_facts: dict[str, str] = {}
    for sid in DUE:
        line = gate_line(lesson, sid)
        if sid in pinned:
            if line is None:
                c5.append(f"{sid}: pinned row carries no lesson Gate line")
            continue
        cells = rows.get(sid)
        base_cells = base_rows.get(sid)
        if cells is not None and base_cells is not None and len(cells) > 9 and len(base_cells) > 9:
            if cells[9] != base_cells[9]:
                c5.append(f"{sid}: unpinned due row changed its recheck cell {base_cells[9]!r} -> {cells[9]!r}; a carry keeps the cadence")
        if line is None:
            c5.append(f"{sid}: unpinned due row carries no Gate note naming the observed state")
        elif not OBSERVED.search(line):
            c5.append(f"{sid}: unpinned due row's Gate line names no observed state (expected one of anchor_moved, "
                      f"page_changed, fetch_failed, quote-missing, non-200, HTTP <code>, timeout)")
        else:
            carry_facts[sid] = line[:160]
    add("C5_carry_notes", c5, {"carried": sorted(carried), "notes": carry_facts})

    # ---------------------------------------------------------------- C6: append-only registry
    c6: list[str] = []
    for sid, base_line in base_raw.items():
        measured = rows_raw.get(sid)
        if measured is None:
            c6.append(f"{sid}: base row absent at the measured revision")
            continue
        if sid not in DUE:
            if measured != base_line:
                c6.append(f"{sid}: row outside the due set differs from base")
            continue
        base_cells, measured_cells = base_rows.get(sid), rows.get(sid)
        if not base_cells or not measured_cells:
            c6.append(f"{sid}: due row is unparseable at the base or measured revision")
            continue
        if len(measured_cells) != 11 or len(base_cells) != 11:
            c6.append(f"{sid}: due row does not hold 11 cells at both revisions")
            continue
        changed = [CELL_NAMES[i] for i in range(11) if i != 9 and base_cells[i] != measured_cells[i]]
        if changed:
            c6.append(f"{sid}: due row changed cell(s) {changed} — only the recheck cell may move")
    added = [sid for sid in rows if sid not in base_rows]
    add("C6_append_only", c6, {"base_rows": len(base_raw), "rows": len(rows), "appended": added})

    passed = sum(1 for r in results if r["state"] == "pass")
    return (0 if passed == len(results) else 1), results


# --------------------------------------------------------------------------- selftest

_FX_FILLER_26 = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho "
                 "sigma tau upsilon phi chi psi omega tail one")
_FX_LONG = " ".join(["loremipsumdolorsitametconsecteturad"] * 6)  # 6 units, above the 160-character ceiling
_FX_NAV = "Fixture navigation link text"
_FX_QUOTE = "The {sid} fixture page states that recheck pins are a concrete date"


def _fixture_base_registry() -> str:
    lines = ["# Sources registry (selftest fixture)", "", "## Registry", "",
             "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    plan = [(f"S{i:03d}", "on-release", "mined", "2026-10-19") for i in (1, 2)]
    plan += [(f"S{i:03d}", "90d", "mined", "2026-10-19") for i in range(3, 8)]
    plan += [(f"S{i:03d}", "365d", "mined", "2026-10-19") for i in range(8, 17)]
    plan += [("S017", "90d", "rejected", "2026-10-19"),
             ("S018", "180d", "mined", "2026-10-20"),
             ("S019", "90d", "queued", "2026-10-22")]
    for sid, cadence, status, opened in plan:
        lines.append(f"| {sid} | Fixture row {sid} — https://example.invalid/{sid} | docs | A | fixture scope cell "
                     f"for {sid} | § Fixture anchor for {sid} (fetched 2026-10-19) | fixture teaches cell for {sid} "
                     f"| {status} | {opened} | {cadence} | — |")
    return "\n".join(lines) + "\n"


def _fixture_body(sid: str) -> bytes:
    text = ("<html><head><title>Fixture {sid}</title></head><body>"
            "<nav><a href=\"/\">{nav}</a></nav>"
            "<h1>Fixture page {sid}</h1>"
            "<p>{quote}.</p>"
            "<p>{filler}</p>"
            "<p>{long}</p>"
            "<footer>Fixture footer note.</footer></body></html>\n").format(
                sid=sid, nav=_FX_NAV, quote=_FX_QUOTE.format(sid=sid), filler=_FX_FILLER_26, long=_FX_LONG)
    return text.encode("utf-8")


def _fixture_receipt(sid: str, blob: bytes, **over) -> dict:
    entry = {"url": f"https://example.invalid/{sid}",
             "effectiveUrl": f"https://example.invalid/{sid}",
             "status": 200,
             "sha256": hashlib.sha256(blob).hexdigest(),
             "bytes": len(blob),
             "fetchedAt": f"{ROUND_DATE}T04:0{sid[-1]}:00+00:00",
             "userAgent": f"kake-shokunin-{UA_TAG}"}
    entry.update(over)
    return entry


def _fixture_gate(sid: str, blob: bytes) -> str:
    return (f"- {sid} — https://example.invalid/{sid} — accessed {ROUND_DATE} — § Fixture anchor for {sid} — quote: "
            f"\"{_FX_QUOTE.format(sid=sid)}\" (12 units; sha256 {hashlib.sha256(blob).hexdigest()}, {len(blob)} bytes, "
            f"HTTP 200)")


def _set_cell(registry_text: str, sid: str, index: int, value: str) -> str:
    out = []
    for line in registry_text.split("\n"):
        match = re.match(ROW_RE, line)
        if match and match.group(1) == sid:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[index] = value
            line = "| " + " | ".join(cells) + " |"
        out.append(line)
    return "\n".join(out)


def _drop_row(registry_text: str, sid: str) -> str:
    return "\n".join(line for line in registry_text.split("\n")
                     if not (re.match(ROW_RE, line) and re.match(ROW_RE, line).group(1) == sid))


def _append_row(registry_text: str, row_line: str) -> str:
    lines = registry_text.split("\n")
    last = max(i for i, line in enumerate(lines) if re.match(ROW_RE, line))
    return "\n".join(lines[:last + 1] + [row_line] + lines[last + 1:])


def _set_gate(lesson: str, sid: str, new_line: str | None) -> str:
    out = []
    for line in lesson.split("\n"):
        match = re.match(r"^-\s+\**(" + re.escape(sid) + r")\**\b", line.strip())
        if match:
            if new_line is not None:
                out.append(new_line)
            continue
        out.append(line)
    return "\n".join(out)


def _fixture_files() -> tuple[dict, dict]:
    """(base files, green after-state files)."""
    base_registry = _fixture_base_registry()
    pins = {sid: ("2027-01-17" if sid <= "S007" else "2027-10-19") for sid in DUE}
    after_registry = base_registry
    for sid, pin in pins.items():
        after_registry = _set_cell(after_registry, sid, 9, pin)
    after_registry = _append_row(
        after_registry,
        "| S430 | Fixture appended row — https://example.invalid/S430 | spec | A | appended scope | § Appended anchor "
        "| appended teaches | mined | 2026-10-27 | 180d | corpus/lessons/round-61.md |")
    bodies = {sid: _fixture_body(sid) for sid in DUE}
    lesson = ("# Round 61 lessons fixture\n\n## Gate\n\nRows re-verified; quote spans follow the declared rules.\n\n"
              + "\n".join(_fixture_gate(sid, bodies[sid]) for sid in DUE) + "\n\n## Census\n\nfixture prose.\n")
    receipts = {"receipts": [_fixture_receipt(sid, bodies[sid]) for sid in DUE]}
    after = {REGISTRY: after_registry.encode("utf-8"), LESSON: lesson.encode("utf-8"),
             RECEIPTS: (json.dumps(receipts, indent=1) + "\n").encode("utf-8")}
    for sid, blob in bodies.items():
        after[f"{RECHECK_DIR}/{sid}.html"] = blob
    return {REGISTRY: base_registry.encode("utf-8")}, after


def _selftest_tmp() -> str | None:
    cand = os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        os.makedirs(cand, exist_ok=True)
        probe = tempfile.mkdtemp(prefix=".probe-", dir=cand)
        os.rmdir(probe)
        return cand
    except OSError:
        return None


def _build(base_files: dict, after_files: dict) -> tuple[str, str, str]:
    root = tempfile.mkdtemp(prefix="c61-rp-", dir=_selftest_tmp())
    subprocess.run(["git", "-C", root, "init", "-q"], check=True, env=clean_env())
    rc, top = git(root, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(top.strip()) != os.path.realpath(root):
        raise RuntimeError("fixture repo toplevel mismatch")

    def commit(files: dict, message: str) -> str:
        for rel, blob in files.items():
            target = os.path.join(root, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(blob)
        subprocess.run(["git", "-C", root, "add", "-A"], check=True, env=clean_env())
        subprocess.run(["git", "-C", root, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "--allow-empty", "-m", message], check=True, env=clean_env())
        return git(root, "rev-parse", "HEAD")[1].strip()

    base_sha = commit(base_files, "base")
    tip = commit(after_files, "round-61 after-state fixture")
    return root, base_sha, tip


def selftest() -> int:
    for key in [k for k in os.environ if k.startswith("GIT_")]:
        os.environ.pop(key)
    base_files, green = _fixture_files()
    unit_checks: dict[str, bool] = {
        "units: Latin token count": units("a b c") == 3,
        "units: 25 tokens at ceiling": units(" ".join("t" * 2 for _ in range(25))) == 25,
        "units: 26 tokens over ceiling": units(_FX_FILLER_26) == 26,
        "units: CJK counts per character": units("\u91ce\u5bb6") == 2,
        "units: 6-unit span at floor": units(_FX_QUOTE.format(sid="S001")) == 12,
        "chars: long-token span is 6 units and above the ceiling": units(_FX_LONG) == 6 and len(_FX_LONG) > CHAR_CEILING,
        "dates: opened+90d is 2027-01-17": (date(2026, 10, 19) + timedelta(days=90)).isoformat() == "2027-01-17",
        "dates: opened+365d is 2027-10-19": (date(2026, 10, 19) + timedelta(days=365)).isoformat() == "2027-10-19",
        "nodes: chrome is not body text": not span_hits(_FX_NAV, body_nodes(_fixture_body("S001"))),
        "nodes: quote is one page-unique node": len(span_hits(_FX_QUOTE.format(sid="S001"),
                                                              body_nodes(_fixture_body("S001")))) == 1,
        "nodes: plain-text body splits on blank lines": body_nodes(b"one two\n\nthree four\n") == ["one two", "three four"],
        "nodes: inline markup splits a span (rule is one text node)": not span_hits(
            "fixture inline split span", body_nodes(b"<p>fixture <a href=\"#\">inline</a> split span</p>")),
        "nodes: the inline view names the split span": bool(span_hits(
            "fixture inline split span", inline_flattened(b"<p>fixture <a href=\"#\">inline</a> split span</p>"))),
        "iso: datetime is not a concrete date": not is_iso_date("2027-01-17T00:00:00Z"),
        "iso: 2027-02-30 is not a date": not is_iso_date("2027-02-30"),
    }

    def run(measured_files: dict, measure_base: bool = False):
        root, base_sha, tip = _build(base_files, measured_files)
        try:
            rev = base_sha if measure_base else tip
            return run_checks(root, rev, base_sha)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def failchecks(results: list[dict]) -> set[str]:
        return {r["check"] for r in results if r["state"] != "pass"}

    def notes_of(results: list[dict], check: str) -> str:
        return " | ".join(n for r in results if r["check"] == check for n in r["notes"])

    green_text = green[REGISTRY].decode("utf-8")
    green_lesson = green[LESSON].decode("utf-8")
    bodies = {sid: _fixture_body(sid) for sid in DUE}

    def reg(sid: str, index: int, value: str) -> dict:
        files = dict(green)
        files[REGISTRY] = _set_cell(green_text, sid, index, value).encode("utf-8")
        return files

    def lesson_with(mutate) -> dict:
        files = dict(green)
        files[LESSON] = mutate(green_lesson).encode("utf-8")
        return files

    def receipts_with(mutate) -> dict:
        doc = json.loads(green[RECEIPTS].decode("utf-8"))
        mutate(doc["receipts"])
        files = dict(green)
        files[RECEIPTS] = (json.dumps(doc, indent=1) + "\n").encode("utf-8")
        return files

    def entry_of(entries: list, sid: str) -> dict:
        return next(e for e in entries if e.get("url", "").endswith("/" + sid))

    def variant(name: str) -> dict:
        if name == "green":
            return dict(green)
        if name == "all-carried-with-notes":
            files = dict(green)
            text = green_text
            for sid in DUE:
                text = _set_cell(text, sid, 9, "on-release" if sid <= "S002" else ("90d" if sid <= "S007" else "365d"))
            files[REGISTRY] = text.encode("utf-8")
            lesson = green_lesson
            for sid in DUE:
                lesson = _set_gate(lesson, sid, f"- {sid} — https://example.invalid/{sid} — accessed {ROUND_DATE} — "
                                                f"fetch_failed (HTTP 503), anchor not located; cadence kept")
            files[LESSON] = lesson.encode("utf-8")
            return files
        if name == "c1-new-oldest-row":
            files = dict(green)
            files[REGISTRY] = _append_row(
                green_text, "| S431 | Fixture older row — https://example.invalid/S431 | docs | A | older scope "
                            "| § Older anchor | older teaches | mined | 2026-10-18 | 180d | — |").encode("utf-8")
            return files
        if name == "c1-rejected-oldest-row":
            files = dict(green)
            files[REGISTRY] = _append_row(
                green_text, "| S432 | Fixture rejected row — https://example.invalid/S432 | docs | C | rejected scope "
                            "| § Rejected anchor | rejected teaches | rejected | 2026-10-18 | 180d | — |").encode("utf-8")
            return files
        if name == "c2-pin-out-of-bounds":
            return reg("S003", 9, "2027-01-18")
        if name == "c2-nonnd-pin-off-by-one":
            return reg("S001", 9, "2027-01-18")
        if name == "c2-non-iso-cell":
            return reg("S004", 9, "2027-01-17T00:00:00Z")
        if name == "c3-quote-not-in-body":
            return lesson_with(lambda text: _set_gate(
                text, "S005", f"- S005 — https://example.invalid/S005 — accessed {ROUND_DATE} — quote: "
                               f"\"The S005 fixture page states that recheck pins are a concrete plan\" (12 units)"))
        if name == "c3-units-26":
            return lesson_with(lambda text: _set_gate(
                text, "S005", f"- S005 — https://example.invalid/S005 — accessed {ROUND_DATE} — quote: "
                               f"\"{_FX_FILLER_26}\" (26 units)"))
        if name == "c3-chars-over-ceiling":
            return lesson_with(lambda text: _set_gate(
                text, "S005", f"- S005 — https://example.invalid/S005 — accessed {ROUND_DATE} — quote: "
                               f"\"{_FX_LONG}\" (6 units, above the 160-character ceiling)"))
        if name == "c3-url-missing":
            return lesson_with(lambda text: _set_gate(
                text, "S006", f"- S006 — accessed {ROUND_DATE} — quote: "
                               f"\"{_FX_QUOTE.format(sid='S006')}\" (12 units)"))
        if name == "c3-date-missing":
            return lesson_with(lambda text: _set_gate(
                text, "S001", f"- S001 — https://example.invalid/S001 — quote: "
                               f"\"{_FX_QUOTE.format(sid='S001')}\" (12 units)"))
        if name == "c3-curly-quotes":
            return lesson_with(lambda text: _set_gate(
                text, "S007", f"- S007 — https://example.invalid/S007 — accessed {ROUND_DATE} — quote: "
                               f"\u201c{_FX_QUOTE.format(sid='S007')}\u201d (12 units)"))
        if name == "c3-short-anchor-quote":
            return lesson_with(lambda text: _set_gate(
                text, "S002", f"- S002 — https://example.invalid/S002 — accessed {ROUND_DATE} — \u00a7 \"Fixture page\""
                               f" — quote: \"{_FX_QUOTE.format(sid='S002')}\" (12 units)"))
        if name == "c3-nav-span":
            return lesson_with(lambda text: _set_gate(
                text, "S002", f"- S002 — https://example.invalid/S002 — accessed {ROUND_DATE} — quote: "
                               f"\"{_FX_NAV}\" (4 units)"))
        if name == "c4-receipt-missing":
            def drop(entries: list) -> None:
                entries.remove(entry_of(entries, "S007"))
            return receipts_with(drop)
        if name == "c4-sha-mismatch":
            def sha(entries: list) -> None:
                entry_of(entries, "S008")["sha256"] = "0" * 64
            return receipts_with(sha)
        if name == "c4-status-404":
            def status(entries: list) -> None:
                entry_of(entries, "S009")["status"] = 404
            return receipts_with(status)
        if name == "c4-ua-tag":
            def ua(entries: list) -> None:
                entry_of(entries, "S010")["userAgent"] = "kake-shokunin-round60"
            return receipts_with(ua)
        if name == "c4-fetch-date":
            def stamp(entries: list) -> None:
                entry_of(entries, "S010")["fetchedAt"] = "2026-10-26T04:00:00+00:00"
            return receipts_with(stamp)
        if name == "c4-url-mismatch":
            def url(entries: list) -> None:
                entry = entry_of(entries, "S010")
                entry["url"] = "https://example.invalid/S099"
                entry["id"] = "S010"
            return receipts_with(url)
        if name == "c4-bytes":
            def nbytes(entries: list) -> None:
                entry_of(entries, "S010")["bytes"] = len(bodies["S010"]) + 1
            return receipts_with(nbytes)
        if name == "c4-body-missing":
            files = dict(green)
            files.pop(f"{RECHECK_DIR}/S009.html")
            return files
        if name == "c5-unpinned-no-note":
            files = reg("S002", 9, "on-release")
            files[LESSON] = _set_gate(green_lesson, "S002", None).encode("utf-8")
            return files
        if name == "c5-unpinned-anchor-found-without-pin":
            files = reg("S002", 9, "on-release")
            files[LESSON] = _set_gate(
                green_lesson, "S002", f"- S002 — https://example.invalid/S002 — accessed {ROUND_DATE} — "
                                      f"anchor_found (12 units)").encode("utf-8")
            return files
        if name == "c5-unpinned-cadence-changed":
            files = reg("S002", 9, "180d")
            files[LESSON] = _set_gate(
                green_lesson, "S002", f"- S002 — https://example.invalid/S002 — accessed {ROUND_DATE} — "
                                      f"fetch_failed (HTTP 503), anchor not located").encode("utf-8")
            return files
        if name == "c5-pinned-no-gate":
            files = dict(green)
            files[LESSON] = _set_gate(green_lesson, "S006", None).encode("utf-8")
            return files
        if name == "c6-due-cell-change":
            return reg("S001", 6, "rewritten teaches cell for S001")
        if name == "c6-non-due-change":
            return reg("S018", 6, "rewritten teaches cell for S018")
        if name == "c6-base-row-removed":
            files = dict(green)
            files[REGISTRY] = _drop_row(green_text, "S016").encode("utf-8")
            return files
        if name == "c6-whitespace":
            files = dict(green)
            files[REGISTRY] = (green_text.replace("| — |\n| S430 |", "|  — |\n| S430 |", 1)).encode("utf-8")
            return files
        raise AssertionError(f"unknown variant {name}")

    cases = [
        ("green", set(), None, False),
        ("all-carried-with-notes", {"C2_pinned_dates"}, "0 pins", False),
        ("c1-new-oldest-row", {"C1_due_set"}, "re-derived due set", False),
        ("c1-rejected-oldest-row", set(), None, False),
        ("c2-pin-out-of-bounds", {"C2_pinned_dates"}, "outside (opened", False),
        ("c2-nonnd-pin-off-by-one", {"C2_pinned_dates"}, "opened+90d", False),
        ("c2-non-iso-cell", {"C2_pinned_dates", "C5_carry_notes"}, "neither a concrete ISO date", False),
        ("c3-quote-not-in-body", {"C3_gate_quotes"}, "not a substring of any whitespace-collapsed text node", False),
        ("c3-units-26", {"C3_gate_quotes"}, "26 units outside 6..25", False),
        ("c3-chars-over-ceiling", {"C3_gate_quotes"}, "characters above 160", False),
        ("c3-url-missing", {"C3_gate_quotes"}, "carries none of the row URLs", False),
        ("c3-date-missing", {"C3_gate_quotes"}, "does not carry the access date", False),
        ("c3-curly-quotes", {"C3_gate_quotes"}, "curly double quotes", False),
        ("c3-nav-span", {"C3_gate_quotes"}, "no double-quoted span on the Gate line passes", False),
        ("c4-receipt-missing", {"C4_receipt_pins"}, "no receipt whose url", False),
        ("c4-sha-mismatch", {"C4_receipt_pins"}, "receipt sha256", False),
        ("c4-status-404", {"C4_receipt_pins"}, "not HTTP 200", False),
        ("c4-ua-tag", {"C4_receipt_pins"}, "does not carry the round61 tag", False),
        ("c4-fetch-date", {"C4_receipt_pins"}, "not on the access date", False),
        ("c4-url-mismatch", {"C4_receipt_pins"}, "is not one of the row URLs", False),
        ("c4-bytes", {"C4_receipt_pins"}, "committed blob length", False),
        ("c4-body-missing", {"C3_gate_quotes", "C4_receipt_pins"}, "no retained body", False),
        ("c5-unpinned-no-note", {"C5_carry_notes"}, "no Gate note naming the observed state", False),
        ("c5-unpinned-anchor-found-without-pin", {"C5_carry_notes"}, "names no observed state", False),
        ("c5-unpinned-cadence-changed", {"C2_pinned_dates", "C5_carry_notes"}, "a carry keeps the cadence", False),
        ("c5-pinned-no-gate", {"C3_gate_quotes", "C5_carry_notes"}, "pinned row has no lesson Gate line", False),
        ("c6-due-cell-change", {"C6_append_only"}, "only the recheck cell may move", False),
        ("c6-non-due-change", {"C6_append_only"}, "row outside the due set differs from base", False),
        ("c6-base-row-removed", {"C6_append_only"}, "base row absent at the measured revision", False),
        ("c6-whitespace", {"C6_append_only"}, "row outside the due set differs from base", False),
    ]

    passed, fails, listing = 0, [], []
    # green baseline
    code, results = run(dict(green))
    green_fail = failchecks(results)
    if code == 0 and not green_fail and sum(r["state"] == "pass" for r in results) == 6:
        passed += 1
        listing.append("CASE green | green | 0 | PASS")
    else:
        fails.append(f"green: expected exit 0 and 6/6, got exit {code} and {sorted(green_fail)}")
        for r in results:
            for note in r["notes"]:
                fails.append(f"    green note: {note}")

    # do-nothing: measure the base commit itself
    code, results = run(dict(green), measure_base=True)
    checks = failchecks(results)
    base_notes = notes_of(results, "C2_pinned_dates")
    ok = code == 1 and checks == {"C2_pinned_dates", "C5_carry_notes"} and "0 pins" in base_notes
    listing.append(f"CASE base-tree | C2+C5 | {code} | {'PASS' if ok else 'FAIL'}")
    if ok:
        passed += 1
    else:
        fails.append(f"base-tree: expected exactly C2 (0 pins) + C5 to fail at base, got {sorted(checks)} (exit {code})")

    # constant control: every date rewritten, no bodies, no receipts, no lesson
    constant = {REGISTRY: green[REGISTRY]}
    code, results = run(constant)
    checks = failchecks(results)
    ok = code == 1 and {"C3_gate_quotes", "C4_receipt_pins"} <= checks and "C2_pinned_dates" not in checks
    listing.append(f"CASE constant | C3+C4 | {code} | {'PASS' if ok else 'FAIL'}")
    if ok:
        passed += 1
    else:
        fails.append(f"constant: expected C3+C4 to fail with C2 passing, got {sorted(checks)} (exit {code})")

    for name, want, note, measure_base in cases:
        files = green if name == "green" else variant(name)
        code, results = run(files, measure_base=measure_base)
        checks = failchecks(results)
        want_code = 0 if not want else 1
        ok = checks == want and code == want_code
        if ok and note:
            blob = " ".join(notes_of(results, check) for check in want)
            ok = note in blob
        listing.append(f"CASE {name} | {sorted(want)} | {code} | {'PASS' if ok else 'FAIL'}")
        if ok:
            passed += 1
        else:
            fails.append(f"{name}: expected exit {want_code} with failures {sorted(want)}"
                         + (f" and note {note!r}" if note else "") + f"; got exit {code} with {sorted(checks)}")
            for check in sorted(checks):
                for item in [n for r in results if r["check"] == check for n in r["notes"]][:3]:
                    fails.append(f"    {name} note: {item}")

    # a sub-floor quoted anchor name is context, not a failing quote
    code_short, results_short = run(variant("c3-short-anchor-quote"))
    facts_short = next(r["facts"] for r in results_short if r["check"] == "C3_gate_quotes")
    unit_checks["short context quote is an observation, not a failure"] = (
        code_short == 0 and "S002" in (facts_short.get("observations") or {}))

    # unevaluable + usage
    root, base_sha, tip = _build(dict(base_files), dict(green))
    try:
        code_bad, _ = run_checks(root, tip, "0" * 40)
        code_missing, _ = run_checks(root, "0" * 40, base_sha)
        unit_checks["unreadable base is exit 2"] = code_bad == 2
        unit_checks["unresolved revision is exit 2"] = code_missing == 2
        os.makedirs(os.path.join(root, "corpus", "nested"), exist_ok=True)
        script = os.path.abspath(__file__)
        sub = subprocess.run([sys.executable, "-B", script, "--root", os.path.join(root, "corpus"),
                              "--revision", tip], capture_output=True, text=True, env=clean_env())
        unit_checks["--root below the toplevel exits 2"] = sub.returncode == 2
        good = subprocess.run([sys.executable, "-B", script, "--root", root, "--revision", tip,
                               "--base", base_sha, "--json"], capture_output=True, text=True, env=clean_env())
        try:
            doc = json.loads(good.stdout)
            unit_checks["--json emits the schema and 6/6"] = (
                doc.get("schema") == "kake-r61-c3-recheck-pins-v1" and doc.get("conditions_passed") == 6
                and doc.get("met") is True and doc.get("predicate") == PREDICATE)
        except ValueError:
            unit_checks["--json emits the schema and 6/6"] = False
        text_run = subprocess.run([sys.executable, "-B", script, "--root", root, "--revision", tip,
                                   "--base", base_sha], capture_output=True, text=True, env=clean_env())
        unit_checks["text run prints the predicate summary"] = (
            "conditions_passed=6 of 6 met=True" in text_run.stdout and text_run.returncode == 0)
        usage = subprocess.run([sys.executable, "-B", script, "--revisionn", "x"], capture_output=True, text=True)
        unit_checks["argparse usage error exits 64"] = usage.returncode == 64
        missing = subprocess.run([sys.executable, "-B", script, "--root", root], capture_output=True, text=True)
        unit_checks["missing --revision exits 64"] = missing.returncode == 64
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for label, ok in unit_checks.items():
        if ok:
            passed += 1
        else:
            fails.append(f"unit rule: {label}")
    total = len(cases) + len(unit_checks) + 3  # green baseline + base-tree + constant
    print(f"c61 recheck-pins selftest: {passed}/{total} (green exit 0 and 6/6; base-tree and constant controls; "
          f"{len(cases)} fixture cases; predicate {PREDICATE})")
    if os.environ.get("KAKE_R61_SELFTEST_VERBOSE"):
        for item in listing:
            print(" ", item)
        for label, ok in unit_checks.items():
            print(f"  UNIT {label} | {'PASS' if ok else 'FAIL'}")
    for item in fails:
        print("  FAIL", item)
    return 0 if passed == total else 1


# --------------------------------------------------------------------------- CLI


def main() -> int:
    class _Parser(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    parser = _Parser(description="Round-61 C3 counter — ten oldest registry rows re-verified, cadences pinned "
                                 "(offline; committed bytes only)")
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision")
    parser.add_argument("--base", default=BASE_REV, help="revision holding the base registry (default: the frozen one)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if not args.revision:
        print("usage: --revision is required unless --selftest is used", file=sys.stderr)
        return 64

    rc_top, top = git(args.root, "rev-parse", "--show-toplevel")
    if rc_top != 0 or os.path.realpath(top.strip()) != os.path.realpath(args.root):
        print(f"unevaluable: --root {args.root!r} is not the toplevel of a git repository")
        print("EXIT=2")
        return 2
    rc_r, rev_id = git(args.root, "rev-parse", "--verify", "--quiet", f"{args.revision}^{{commit}}")
    rc_b, base_id = git(args.root, "rev-parse", "--verify", "--quiet", f"{args.base}^{{commit}}")
    if rc_r != 0 or rc_b != 0:
        print(f"unevaluable: revision {args.revision!r} or base {args.base!r} does not resolve to a commit in {args.root!r}")
        print("EXIT=2")
        return 2
    revision, base = rev_id.strip(), base_id.strip()

    code, results = run_checks(args.root, revision, base)
    passed = sum(1 for r in results if r["state"] == "pass")
    met = code == 0
    if args.json:
        facts = {r["check"]: r["facts"] for r in results}
        print(json.dumps({
            "schema": "kake-r61-c3-recheck-pins-v1",
            "predicate": PREDICATE,
            "revision": revision,
            "base": base,
            "access_date": ROUND_DATE,
            "due_set": list(DUE),
            "checks": {r["check"]: {"passed": r["state"] == "pass", "state": r["state"],
                                    "notes": r["notes"], "facts": r["facts"]} for r in results},
            "conditions_passed": passed,
            "exit": code,
            "met": met,
        }, indent=1, ensure_ascii=False))
        return code
    print(f"c61 recheck-pins: conditions_passed={passed} of 6 met={met}  ({PREDICATE})")
    for r in results:
        print(f"  {r['check']} {r['state'].upper()}")
        for note in r["notes"]:
            print(f"    - {note}")
    pins = next((r["facts"].get("pinned") for r in results if r["check"] == "C2_pinned_dates"), None)
    carried = next((r["facts"].get("carried") for r in results if r["check"] == "C2_pinned_dates"), None)
    print(f"  revision: {revision}  base: {base}  pinned={pins} carried={carried}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
