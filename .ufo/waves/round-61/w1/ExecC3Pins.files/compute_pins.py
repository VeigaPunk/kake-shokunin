#!/usr/bin/env python3
"""Compute the round-61 C3 recheck-cell pin table (read-only; never edits the registry).

Inputs (all read-only):
  <lane>/corpus/SOURCES.md                                  registry rows S001-S010
  <lane>/.ufo/waves/round-61/recheck/receipts.json          per-row fetch receipt (status,
                                                            effectiveUrl, sha256, bytes, fetchedAt,
                                                            userAgent)
  <lane>/.ufo/waves/round-61/w1/ExecC3Quote.files/verdicts.tsv
                                                            quote re-location verdict per row
                                                            (anchor_found | anchor_moved |
                                                             page_changed | fetch_failed)

Rule (contract C3, frozen):
  pinned  <=> fetch is HTTP 200 AND the anchor quote still occurs (verdict `anchor_found`)
  new recheck cell = opened + cadence      for `Nd` cells (S003-S007 90d, S008-S010 365d)
                   = opened + 90d          for non-`Nd` cells (on-release / on-use: S001, S002)
  bound check (Nd): opened < new <= opened + cadence
  everything else: no pin, no date invented; the Gate line carries a note naming the observed state.

Outputs (written beside this script):
  pins.tsv            row_id <TAB> old_cell <TAB> new_cell <TAB> bound_check
  pin_replacements.txt per pinned row: the cell-position edit (index 10 of the `|`-split row) and
                      the row-local substring, guarded because `| 2026-10-19 | 90d |` is not unique
                      in the registry (S013-S017 share it)
  proposed_rows.tsv   row_id <TAB> the full registry row line with only the recheck cell changed
                      (the safe unit of application: same row, same field position, 13 cells)
  pin_cells.json      machine-readable detail incl. proposed cell strings and skip notes
  gate_notes.txt      the Gate note text for every row that is not pinned

Exit: 0 table written (whether or not any row is pinned), 2 inputs unreadable.
"""
import argparse
import datetime
import json
import os
import re
import sys

FROZEN = ["S%03d" % n for n in range(1, 11)]
NON_ND_WINDOW_DAYS = 90  # on-release / on-use rows: opened + 90d


def read_rows(path):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.startswith("| S"):
                continue
            cells = line.rstrip("\n").split("|")
            if len(cells) < 12:
                continue
            row_id = cells[1].strip()
            if row_id in FROZEN:
                rows[row_id] = {
                    "lineno": lineno,
                    "cells": [c.strip() for c in cells],
                    "cells_raw": cells,
                    "raw": line.rstrip("\n"),
                    "id": row_id,
                    "status": cells[8].strip(),
                    "opened": cells[9].strip(),
                    "recheck": cells[10].strip(),
                    "source": cells[2].strip(),
                }
    return rows


def read_receipts(path):
    if not os.path.exists(path):
        return {}, "absent"
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception as exc:  # malformed input is reported, never guessed
        return {}, "malformed: %s" % exc
    out = {}
    for entry in doc.get("receipts", []):
        rid = entry.get("id") or entry.get("row") or entry.get("row_id")
        if rid:
            out[rid] = entry
    return out, "ok"


def read_verdicts(path):
    if not os.path.exists(path):
        return {}, "absent"
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = [p.strip() for p in (line.split("\t") if "\t" in line else line.split("|"))]
            if not parts or not re.fullmatch(r"S\d{3}", parts[0]):
                continue
            # ExecC3Quote columns: id, verdict, located_span, units, chars, occurrences,
            # node_index, node_bounded, location, anchor_clause, scope, note
            out[parts[0]] = {
                "verdict": parts[1] if len(parts) > 1 else "",
                "span": parts[2] if len(parts) > 2 else "",
                "units": parts[3] if len(parts) > 3 else "",
                "location": parts[8] if len(parts) > 8 else "",
                "scope": parts[10] if len(parts) > 10 else "",
                "note": parts[11] if len(parts) > 11 else "",
            }
    return out, "ok"


def read_probe(path):
    """Per-row anchor verdicts from anchor_probe.py (fallback basis, not the quote seat's word)."""
    if not os.path.exists(path):
        return {}, "absent"
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if len(parts) == 2 and re.fullmatch(r"S\d{3}", parts[0]) and parts[1].startswith("anchor"):
            out[parts[0]] = parts[1]
    return out, "ok"


def cadence_window(cell):
    m = re.fullmatch(r"(\d+)d", cell)
    if m:
        return int(m.group(1)), "Nd"
    if cell in ("on-release", "on-use"):
        return NON_ND_WINDOW_DAYS, cell
    return None, "unknown"


def iso_date(text):
    return datetime.date.fromisoformat(text)


def main(argv=None):
    ap = argparse.ArgumentParser(description="round-61 C3 pin table")
    lane_default = "/home/vgpnk/Projects/shokunin/kake-shokunin"
    ap.add_argument("--lane", default=lane_default)
    ap.add_argument("--sources", default=None, help="default <lane>/corpus/SOURCES.md")
    ap.add_argument("--receipts", default=None,
                    help="default <lane>/.ufo/waves/round-61/recheck/receipts.json")
    ap.add_argument("--probe", default=None,
                    help="default <out>/anchor_probe.tsv (fallback anchor verdicts)")
    ap.add_argument("--verdicts", default=None,
                    help="default <lane>/.ufo/waves/round-61/w1/ExecC3Quote.files/verdicts.tsv")
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    lane = args.lane
    sources = args.sources or os.path.join(lane, "corpus", "SOURCES.md")
    receipts_path = args.receipts or os.path.join(
        lane, ".ufo", "waves", "round-61", "recheck", "receipts.json")
    verdicts_path = args.verdicts or os.path.join(
        lane, ".ufo", "waves", "round-61", "w1", "ExecC3Quote.files", "verdicts.tsv")

    try:
        rows = read_rows(sources)
    except OSError as exc:
        sys.stderr.write("sources unreadable: %s\n" % exc)
        return 2
    missing = [r for r in FROZEN if r not in rows]
    if missing:
        sys.stderr.write("frozen rows missing from registry: %s\n" % ",".join(missing))
        return 2

    receipts, receipts_state = read_receipts(receipts_path)
    verdicts, verdicts_state = read_verdicts(verdicts_path)
    probe_path = args.probe or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "anchor_probe.tsv")
    probe, probe_state = read_probe(probe_path)

    table = []
    for rid in FROZEN:
        row = rows[rid]
        window, kind = cadence_window(row["recheck"])
        rec = receipts.get(rid, {})
        status = rec.get("status")
        verdict = verdicts.get(rid, {})
        v = verdict.get("verdict", "")
        if v:
            verdict_source = "ExecC3Quote"
        elif probe.get(rid):
            verdict_source = "anchor_probe"
            v = probe[rid]
        else:
            verdict_source = "none"
        entry = {
            "row_id": rid,
            "lineno": row["lineno"],
            "source": row["source"],
            "status": row["status"],
            "opened": row["opened"],
            "old_cell": row["recheck"],
            "cadence_kind": kind,
            "window_days": window,
            "fetch_status": status,
            "effective_url": rec.get("effectiveUrl") or rec.get("effective_url"),
            "quote_verdict": v or None,
            "verdict_source": verdict_source,
            "quote_span": (verdict.get("span") or None),
            "quote_units": (verdict.get("units") or None),
        }
        if window is None:
            entry["pinned"] = False
            entry["new_cell"] = None
            entry["bound_check"] = "n/a: cadence cell %r has no window" % row["recheck"]
            entry["gate_note"] = None
            table.append(entry)
            continue

        if not row["opened"]:
            entry["pinned"] = False
            entry["new_cell"] = None
            entry["bound_check"] = "n/a: opened cell empty"
            entry["gate_note"] = None
            table.append(entry)
            continue

        opened = iso_date(row["opened"])
        upper = opened + datetime.timedelta(days=window)
        proposed = upper.isoformat()  # opened + cadence / opened + 90d

        if status == 200 and v == "anchor_found":
            entry["pinned"] = True
            entry["new_cell"] = proposed
            entry["cell_index"] = 10
            entry["proposed_row_line"] = proposed_row_line(row, proposed)
            entry["bound_check"] = (
                "%s < %s <= %s (%+dd bound, %s) -> ok"
                % (opened.isoformat(), proposed, upper.isoformat(), window,
                   "equality at upper bound" if proposed == upper.isoformat() else "inside"))
        else:
            observed = []
            if receipts_state == "ok" and rid in receipts:
                observed.append("HTTP %s (%s bytes)" % (status, rec.get("bytes")))
            elif receipts_state != "ok":
                observed.append("fetch receipt %s" % receipts_state)
            else:
                observed.append("no fetch receipt for %s" % rid)
            observed.append("quote verdict: %s" % (v or ("unavailable (%s)" % verdicts_state)))
            entry["pinned"] = False
            entry["new_cell"] = None
            entry["bound_check"] = "n/a: not pinned (%s)" % "; ".join(observed)
            # A carried row keeps its cadence cell and gets a Gate note; no date, no status change.
            detail = ""
            if v and v != "anchor_found":
                extra = [x for x in (verdict.get("location"), verdict.get("scope"),
                                     verdict.get("note")) if x]
                if extra:
                    # a Gate line's own double quotes would be read as a quote span by the
                    # census/quote parsers; keep the note single-quote only
                    detail = ("; quote seat: " + " | ".join(extra)).replace('"', "'")
                    if len(detail) > 200:
                        detail = detail[:197].rstrip() + "..."
            entry["gate_note"] = (
                "- %s — %s — accessed 2026-10-27 — recheck carried, no date pin: %s%s; "
                "cadence cell `%s` retained unchanged, row status `%s` retained unchanged."
                % (rid,
                   (entry.get("effective_url") or first_url(row["source"])),
                   "; ".join(observed), detail,
                   row["recheck"],
                   row["status"]))
        table.append(entry)

    os.makedirs(args.out, exist_ok=True)

    tsv_lines = ["row_id\told_cell\tnew_cell\tbound_check"]
    for e in table:
        tsv_lines.append("\t".join([
            e["row_id"],
            e["old_cell"],
            e["new_cell"] if e["new_cell"] else "(none)",
            e["bound_check"].replace("\t", " "),
        ]))
    tsv_text = "\n".join(tsv_lines) + "\n"

    registry_text = open(sources, encoding="utf-8").read() if os.path.exists(sources) else ""

    def occurrences(sub):
        return registry_text.count(sub)

    repl_lines = [
        "# Per pinned row, two application forms. The safe form is the cell-position edit: take the",
        "# row whose first cell is the row id, split on '|', and replace field index 10 only",
        "# (13 fields per row; fields 1..11 carry content). The substring form is listed second",
        "# with its file-wide occurrence count because `| 2026-10-19 | 90d |` is NOT unique."]
    for e in table:
        if e["pinned"]:
            old = "| %s | %s |" % (e["opened"], e["old_cell"])
            new = "| %s | %s |" % (e["opened"], e["new_cell"])
            repl_lines.append("%s\tcell-index=10\t%s -> %s" % (e["row_id"], e["old_cell"], e["new_cell"]))
            repl_lines.append("%s\tsubstring (file-wide occurrences of %r: %d)\t%s -> %s"
                              % (e["row_id"], old, occurrences(old), old, new))

    proposed_lines = ["# row_id<TAB>full registry row line with field 10 changed; the safe application unit"]
    for e in table:
        if e["pinned"]:
            proposed_lines.append("%s\t%s" % (e["row_id"], e["proposed_row_line"]))

    gate_lines = ["# Gate note text for every row this table does not pin"]
    for e in table:
        if not e["pinned"]:
            gate_lines.append(e["gate_note"] or (
                "- %s — %s — accessed 2026-10-27 — recheck carried, no date pin: %s."
                % (e["row_id"], first_url(e["source"]), e["bound_check"])))

    with open(os.path.join(args.out, "pins.tsv"), "w", encoding="utf-8") as fh:
        fh.write(tsv_text)
    with open(os.path.join(args.out, "proposed_rows.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(proposed_lines) + "\n")
    with open(os.path.join(args.out, "pin_replacements.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(repl_lines) + "\n")
    with open(os.path.join(args.out, "gate_notes.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(gate_lines) + "\n")
    doc = {
        "schema": "kake-c3-pin-table-v1",
        "round": 61,
        "access_date": "2026-10-27",
        "inputs": {
            "sources": sources,
            "receipts": receipts_path,
            "receipts_state": receipts_state,
            "verdicts": verdicts_path,
            "verdicts_state": verdicts_state,
            "probe": probe_path,
            "probe_state": probe_state,
        },
        "frozen_rows": FROZEN,
        "pinned": sum(1 for e in table if e["pinned"]),
        "skipped": sum(1 for e in table if not e["pinned"]),
        "rows": table,
    }
    with open(os.path.join(args.out, "pin_cells.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")

    if args.json:
        sys.stdout.write(json.dumps({"pinned": doc["pinned"], "skipped": doc["skipped"],
                                     "tsv": tsv_text}, indent=1) + "\n")
    else:
        sys.stdout.write(tsv_text)
    return 0


def first_url(source_cell):
    m = re.search(r"https?://[^\s;]+", source_cell)
    return m.group(0) if m else source_cell


def proposed_row_line(row, new_cell):
    """Return the row's full line with only field 10 (the recheck cell) replaced.

    The padding of every other field is preserved byte-for-byte, so applying this line
    cannot disturb cells 1..9 or 11 (C6: rows outside the recheck cell stay identical).
    """
    cells = list(row["cells_raw"])
    if len(cells) != 13:
        raise SystemExit("%s: expected 13 pipe-split fields, got %d" % (row["id"], len(cells)))
    probe = list(cells)
    probe[10] = " %s " % new_cell
    line = "|".join(probe)
    check = line.split("|")
    if len(check) != 13 or check[10].strip() != new_cell:
        raise SystemExit("%s: proposed line failed its own field check" % row["id"])
    for idx in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11):
        if check[idx] != cells[idx]:
            raise SystemExit("%s: proposed line changed field %d" % (row["id"], idx))
    return line


if __name__ == "__main__":
    sys.exit(main())
