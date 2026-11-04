#!/usr/bin/env python3
"""Independent re-implementation of round-81 C1 item predicates R80-1, R80-2, R80-3.

Source of truth: .ufo/waves/round-81/contract.md, section
"C1 -- calibration: the round-80 routed-defect queue closes",
"Item conditions (frozen)" table. This file deliberately does NOT read
.ufo/waves/round-81/c81_defect_queue.py; it re-derives every expected token
from lane bytes:

  R80-1  the S453 row of <root>/corpus/SOURCES.md sits at 1-based line L, and
         <root>/corpus/lessons/round-81.md carries an R80-1 correction row
         naming corpus/SOURCES.md:L for S453.
  R80-2  the lesson carries an R80-2 correction row containing the numbers
         re-derived from <root>/.ufo/waves/round-80/controls/ctl-c80-constants.txt:
         constants_failed=<a>/<b> (the receipt's ctl summary line), the summed
         per-constant failures <n>/<slots>, and const_echo <e>/<t> (the
         const_echo.py row's failures/total).
  R80-3  the lesson carries an R80-3 correction row containing
         rfc9110.txt rows=<n> and rfc9110.html rows=<m>, counted over the
         registry's source cells.

Usage:
    python3 verify_corrections.py --root <lane-root>

Exit code 0 iff all three items evaluate closed (met=true), else 1.
"""

import argparse
import sys
from pathlib import Path


def parse_registry(registry_path):
    """Return (rows, parse_errors).

    rows: list of (line_no, id_cell, source_cell) for markdown table rows whose
    id cell starts with 'S' followed by digits.
    """
    rows = []
    errors = []
    text = registry_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        rid = cells[0]
        if len(rid) >= 2 and rid[0] == "S" and rid[1:].isdigit():
            source = cells[1] if len(cells) > 1 else ""
            rows.append((line_no, rid, source))
    if not rows:
        errors.append(f"no registry rows found in {registry_path}")
    return rows, errors


def find_s453_line(rows):
    """Return the 1-based line of the row whose id cell is exactly S453."""
    hits = [line_no for line_no, rid, _ in rows if rid == "S453"]
    if not hits:
        return None, "no row with id cell S453"
    if len(hits) > 1:
        return None, f"row id S453 is ambiguous at lines {hits}"
    return hits[0], None


def parse_constants_receipt(receipt_path):
    """Return (per_const, ctl_summary, errors).

    per_const: list of (name, failures, total) from lines like
        const const_echo.py failures=11 undecided=0 total=12 failed
    ctl_summary: (a, b) from the line like
        ctl constants_failed=4/4 cases=12
    """
    per_const = []
    ctl_summary = None
    errors = []
    text = receipt_path.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), start=1):
        fields = line.split()
        if fields and fields[0] == "const" and len(fields) >= 2:
            name = fields[1]
            kv = {}
            for field in fields[2:]:
                if "=" in field:
                    k, v = field.split("=", 1)
                    kv[k] = v
            try:
                per_const.append((name, int(kv["failures"]), int(kv["total"])))
            except (KeyError, ValueError):
                errors.append(
                    f"{receipt_path}:{line_no}: const row not parseable: {line!r}"
                )
        elif fields and fields[0] == "ctl" and len(fields) >= 2 and fields[1].startswith("constants_failed="):
            try:
                a, b = fields[1].split("=", 1)[1].split("/")
                ctl_summary = (int(a), int(b))
            except ValueError:
                errors.append(
                    f"{receipt_path}:{line_no}: ctl summary not parseable: {line!r}"
                )
    if not per_const:
        errors.append(f"{receipt_path}: no 'const' rows found")
    if ctl_summary is None:
        errors.append(f"{receipt_path}: no 'ctl constants_failed=a/b' summary line found")
    return per_const, ctl_summary, errors


def count_rfc9110(rows):
    """Count registry rows whose source cell contains rfc9110.txt / rfc9110.html."""
    txt = sum(1 for _, _, src in rows if "rfc9110.txt" in src)
    html = sum(1 for _, _, src in rows if "rfc9110.html" in src)
    return txt, html


def lesson_lines(lesson_path):
    """Return lesson lines (list of strings), or None if the lesson is absent."""
    if not lesson_path.is_file():
        return None
    return lesson_path.read_text(encoding="utf-8").splitlines()


def find_correction_line(lines, item_id, required_tokens):
    """Return the first lesson line carrying item_id and ALL required_tokens, else None."""
    for line in lines:
        if item_id in line and all(tok in line for tok in required_tokens):
            return line
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="lane root directory")
    args = ap.parse_args(argv)
    root = Path(args.root)

    registry_path = root / "corpus" / "SOURCES.md"
    receipt_path = root / ".ufo" / "waves" / "round-80" / "controls" / "ctl-c80-constants.txt"
    lesson_path = root / "corpus" / "lessons" / "round-81.md"

    print(f"root={root}")
    results = {}

    # ---- derive expected tokens from lane bytes -------------------------
    s453_line = None
    ctl = None
    n_txt = n_html = None

    if not registry_path.is_file():
        print(f"ERROR registry missing: {registry_path}")
    else:
        rows, reg_errors = parse_registry(registry_path)
        for err in reg_errors:
            print(f"ERROR {err}")
        s453_line, s453_err = find_s453_line(rows)
        if s453_err:
            print(f"ERROR {s453_err}")
        n_txt, n_html = count_rfc9110(rows)
        print(f"registry rows={len(rows)} S453_line={s453_line} "
              f"rfc9110.txt rows={n_txt} rfc9110.html rows={n_html}")

    if not receipt_path.is_file():
        print(f"ERROR receipt missing: {receipt_path}")
    else:
        per_const, ctl, ctl_errors = parse_constants_receipt(receipt_path)
        for err in ctl_errors:
            print(f"ERROR {err}")
        if per_const:
            sum_failures = sum(f for _, f, _ in per_const)
            sum_slots = sum(t for _, _, t in per_const)
            echo = next(((f, t) for name, f, t in per_const if name.startswith("const_echo")), None)
            print("receipt per-const: " + "; ".join(
                f"{name} failures={f} total={t}" for name, f, t in per_const))
            print(f"sum_failures/sum_slots={sum_failures}/{sum_slots} "
                  f"constants_failed={ctl[0]}/{ctl[1]} " if ctl else "sums computed, ctl summary missing",
                  end="")
            if echo:
                print(f"const_echo {echo[0]}/{echo[1]}")
            else:
                print("const_echo row: MISSING")
            ctl = (ctl, (sum_failures, sum_slots), echo) if ctl else None

    # ---- check the lesson ------------------------------------------------
    lines = lesson_lines(lesson_path)
    if lines is None:
        print(f"lesson missing: {lesson_path}")
    else:
        print(f"lesson lines={len(lines)}")

    # R80-1
    closed1 = False
    if s453_line is None:
        reason1 = "S453 line not derivable"
    elif lines is None:
        reason1 = "lesson absent"
    else:
        tok1 = f"corpus/SOURCES.md:{s453_line}"
        line1 = find_correction_line(lines, "R80-1", [tok1, "S453"])
        if line1 is not None:
            closed1 = True
            reason1 = f"found: {line1.strip()[:160]}"
        else:
            reason1 = f"no R80-1 row carrying '{tok1}' and 'S453'"
    results["R80-1"] = (closed1, reason1)

    # R80-2
    closed2 = False
    if ctl is None:
        reason2 = "receipt arithmetic not derivable"
    elif lines is None:
        reason2 = "lesson absent"
    else:
        (a, b), (sum_f, sum_s), echo = ctl
        toks2 = [f"constants_failed={a}/{b}", f"{sum_f}/{sum_s}"]
        if echo:
            toks2.append(f"const_echo {echo[0]}/{echo[1]}")
        else:
            toks2.append("const_echo ")
        line2 = find_correction_line(lines, "R80-2", toks2)
        if line2 is not None:
            closed2 = True
            reason2 = f"found: {line2.strip()[:160]}"
        else:
            reason2 = "no R80-2 row carrying " + " AND ".join(repr(t) for t in toks2)
    results["R80-2"] = (closed2, reason2)

    # R80-3
    closed3 = False
    if n_txt is None:
        reason3 = "registry counts not derivable"
    elif lines is None:
        reason3 = "lesson absent"
    else:
        toks3 = [f"rfc9110.txt rows={n_txt}", f"rfc9110.html rows={n_html}"]
        line3 = find_correction_line(lines, "R80-3", toks3)
        if line3 is not None:
            closed3 = True
            reason3 = f"found: {line3.strip()[:160]}"
        else:
            reason3 = "no R80-3 row carrying " + " AND ".join(repr(t) for t in toks3)
    results["R80-3"] = (closed3, reason3)

    # ---- verdict ----------------------------------------------------------
    for item in ("R80-1", "R80-2", "R80-3"):
        closed, reason = results[item]
        print(f"{item} closed={str(closed).lower()} :: {reason}")
    met = all(c for c, _ in results.values())
    print(f"open={sum(1 for c, _ in results.values() if not c)} met={str(met).lower()}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
