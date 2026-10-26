#!/usr/bin/env python3
"""Round-57 W1 — audit the staged (shokuknow merge/kake) package candidates against the retained bodies.

Read-only: reads the staged entries + staged SOURCES.append rows under merge/kake/ (never writes there), reads the
retained bodies under .ufo/waves/round-57/sources/, and writes nothing outside stdout.

  python3 -B staged_quote_audit.py            # quote / recheck / label audit
  python3 -B staged_quote_audit.py --rows     # staged SOURCES rows + maintained census parser, as-is

Unit rule (the counters' `units()`): one unit per CJK character, one per non-CJK whitespace token.
Page-unique: exactly one occurrence in the row's own body and no occurrence in the other adopted body.
Content block: the counter's `content_window()` (article container -> class="footer").
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

WAVE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57"
SRC = f"{WAVE}/sources"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"

ENTRIES = {
    "S421": ("S403", f"{STAGED}/knowledge/corpus/knowledge/baidu-dead-link-taxonomy.md"),
    "S422": ("S408", f"{STAGED}/knowledge/corpus/knowledge/baidu-spider3-dead-link-recognition.md"),
}
IDS = ("S421", "S422")
ARTICLE_START = {"S421": 'class="article-info"', "S422": 'class="zz_dldes_content'}
ARTICLE_END = 'class="footer"'
UNIT_CEILING = 25
CHAR_CEILING = 40
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
CURLY = re.compile("[\u201c\u201d\u201e\u201f]")


def units(t):
    return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])


def body(sid):
    with open(f"{SRC}/{sid}.html", encoding="utf-8", newline="") as fh:
        return fh.read()


def content_window(text):
    starts = [text.find(m) for m in ARTICLE_START.values() if text.find(m) >= 0]
    hi = text.find(ARTICLE_END)
    if not starts or hi < 0:
        return None
    lo = min(starts)
    return (lo, hi) if lo < hi else None


def in_content(text, span):
    win = content_window(text)
    if win is None:
        return False
    i = text.find(span)
    while i >= 0:
        if win[0] <= i < win[1]:
            return True
        i = text.find(span, i + 1)
    return False


def assess(sid, span, others):
    t = body(sid)
    raw = span in t
    return {
        "span": span,
        "units": units(span),
        "chars": len(span),
        "raw_substring": raw,
        "in_content": in_content(t, span) if raw else False,
        "count_in_page": t.count(span),
        "in_other_body": any(span in o for o in others),
        "page_unique": raw and t.count(span) == 1 and not any(span in o for o in others),
        "over_units": units(span) > UNIT_CEILING,
        "over_chars": len(span) > CHAR_CEILING,
    }


def row(fields, header):
    print("\t".join(header))
    for f in fields:
        print("\t".join(str(f[k]) for k in header))


def quote_audit():
    others = {sid: [body(k) for k in IDS if k != sid] for sid in IDS}
    all_spans, over, nonsub, zero_label = [], [], [], []
    print("=== QUOTED SPANS (ASCII double-quoted, units >= 2) ===")
    for sid, (staged_id, path) in ENTRIES.items():
        text = open(path, encoding="utf-8").read()
        spans = [m.group(1) for m in re.finditer(r'"([^"\n]*)"', text) if units(m.group(1)) >= 2]
        print(f"{sid} (staged {staged_id}) {os.path.basename(path)}: ascii_double_quoted_spans_ge2={len(spans)} "
              f"curly_quotes={len(CURLY.findall(text))} backticks={text.count('`')}")
        recs = [assess(sid, s, others[sid]) for s in spans]
        all_spans += recs
        over += [r for r in recs if r["over_units"] or r["over_chars"]]
        nonsub += [r for r in recs if not r["raw_substring"]]
        if recs:
            row(recs, ["units", "chars", "raw_substring", "in_content", "page_unique", "count_in_page",
                       "in_other_body", "over_units", "over_chars", "span"])

    print("\n=== RECHECK grep -F STRINGS ===")
    for sid, (staged_id, path) in ENTRIES.items():
        text = open(path, encoding="utf-8").read()
        recheck = [l for l in text.splitlines() if l.startswith("recheck:")]
        assert len(recheck) == 1, (sid, recheck)
        line = recheck[0]
        m = re.search(r"grep -F -c '([^']*)'", line) or re.search(r'grep -F -c "([^"]*)"', line)
        pat = m.group(1) if m else None
        if pat is None:
            print(f"{sid}: no grep -F string in recheck line")
            continue
        r = assess(sid, pat, others[sid])
        real = subprocess.run(["grep", "-F", "-c", "--", pat, f"{SRC}/{sid}.html"],
                              stdout=subprocess.PIPE, text=True).stdout.strip()
        print(f"{sid} recheck-pattern units={r['units']} chars={r['chars']} raw_substring={r['raw_substring']} "
              f"in_content={r['in_content']} page_unique={r['page_unique']} count_in_page={r['count_in_page']} "
              f"in_other_body={r['in_other_body']} over_units={r['over_units']} over_chars={r['over_chars']}")
        print(f"  grep -F -c -> {real} (staged row claims 1)   pattern={pat}")

    print("\n=== source: SECTION LABELS ===")
    for sid, (staged_id, path) in ENTRIES.items():
        text = open(path, encoding="utf-8").read()
        src = [l for l in text.splitlines() if l.startswith("source:")][0]
        parts = [p.strip() for p in src[len("source:"):].split(" — ")]
        label = next((p for p in parts if p.startswith("§")), "")
        t = body(sid)
        full = label
        no_sec = label[2:] if label.startswith("§ ") else label
        pieces = [p.strip() for p in no_sec.split("→")]
        print(f"{sid}: label={label!r}")
        print(f"  full_label occurrences_in_body={t.count(full)} units={units(full)} chars={len(full)} "
              f"in_content={in_content(t, full) if full in t else False} page_unique={t.count(full) == 1}")
        print(f"  body 'A：' occurrences={t.count('A：')} page_unique={t.count('A：') == 1}")
        print(f"  label_without_'§ '_occurrences={t.count(no_sec)}")
        for p in pieces:
            stripped = re.sub(r"\s*A：\s*$", "", p).strip()
            for cand in ((p,) if stripped == p else (p, stripped)):
                if not cand:
                    continue
                print(f"  piece {cand!r}: units={units(cand)} chars={len(cand)} raw_substring={cand in t} "
                      f"in_content={in_content(t, cand) if cand in t else False} count_in_page={t.count(cand)} "
                      f"page_unique={t.count(cand) == 1 and not any(cand in o for o in others[sid])} "
                      f"over_units={units(cand) > UNIT_CEILING} over_chars={len(cand) > CHAR_CEILING}")
            if stripped != p:
                print(f"    (label writes {p!r}; the '？ A：' space is not in the body)" if t.count(p) == 0 and stripped in t else "")
        print(f"  body has '→' : {t.count('→')}   body has '§' : {t.count('§')}")
        if t.count(full) == 0:
            zero_label.append(sid)

    print("\n=== SUMMARY ===")
    print(f"spans_tested={len(all_spans)} over_ceiling={len(over)} non_substring={len(nonsub)} "
          f"labels_with_0_hits={len(zero_label)}{(' ' + ','.join(zero_label)) if zero_label else ''}")


def rows_audit():
    append = f"{STAGED}/SOURCES.append.md"
    lines = open(append, encoding="utf-8").read().splitlines()
    wanted = {"S403": None, "S408": None}
    for i, line in enumerate(lines, 1):
        m = re.match(r"^ {0,3}\| *(S[0-9]{3,}) *\|", line)
        if m and m.group(1) in wanted and wanted[m.group(1)] is None:
            wanted[m.group(1)] = (i, line)
    print("=== STAGED ROWS (as-is) ===")
    scratch_rows = []
    for sid, (lineno, line) in wanted.items():
        cells = line.strip().strip("|").split("|")
        escaped = line.count("\\|")
        nf = len(cells) + 2
        # 0-based: 0 id,1 source,2 kind,3 tier,4 scope,5 anchor,6 teaches,7 status,8 opened,9 recheck,10 used-by
        recheck = "|".join(cells[9:11]) if len(cells) > 10 else ""
        print(f"{sid} line={lineno} cells={len(cells)} (want 11) escaped_pipes={escaped} gawk_NF={nf} (want 13) "
              f"E01={'YES' if nf != 13 else 'no'}")
        print(f"  anchor_cell={cells[5]!r}")
        print(f"  recheck_cell={recheck!r}")
        print(f"  recheck_prose={'YES' if not re.fullmatch(r'[0-9]+d', recheck) else 'no'} "
              f"contains_backtick={'`' in recheck} contains_'->'={'->' in recheck} "
              f"E09_if_NF13={'YES' if not re.fullmatch(r'[0-9]+d', recheck) else 'no'}")
        print(f"  parsed_used_by_with_shift={cells[10]!r}  real_used_by_ignored={cells[11]!r}")
        scratch_rows.append((sid, line))

    print("\n=== c57_quote_truth.py C5 clauses emulated on the staged rows (title / anchor heading / printed date) ===")
    lane_of = {staged: lane for lane, (staged, _p) in ENTRIES.items()}
    for sid, (lineno, line) in wanted.items():
        cells = line.strip().strip("|").split("|")
        t = body(lane_of[sid])
        print(f"{sid} (-> lane {lane_of[sid]})")
        title = " — ".join(cells[1].split(" — ")[1:-1]) if len(cells) > 1 else ""
        anchor_cell = cells[5]
        anchor = anchor_cell.split("§", 1)[1].split(" (")[0].strip() if "§" in anchor_cell else ""
        pub = re.search(r"发布日期 (\d{4}-\d{2}-\d{2})", anchor_cell)
        print(f"{sid}: title={title!r} occurrences_in_body={t.count(title)} -> "
              f"{'PASS' if title and title in t else 'FAIL'}")
        print(f"  anchor_heading={anchor!r} occurrences_in_body={t.count(anchor)} -> "
              f"{'PASS' if anchor and anchor in t else 'FAIL'}")
        print(f"  printed_date={'发布日期：' + pub.group(1) if pub else '<none>'} occurrences_in_body="
              f"{t.count('发布日期：' + pub.group(1)) if pub else 0} -> "
              f"{'PASS' if pub and ('发布日期：' + pub.group(1)) in t else 'FAIL'}")
        print(f"  opened_cell={cells[8]!r} (round date 2026-10-25) -> "
              f"{'PASS' if cells[8].strip() == '2026-10-25' else 'FAIL'}")

    d = tempfile.mkdtemp(prefix="census-staged-")
    try:
        os.makedirs(f"{d}/corpus/knowledge", exist_ok=True)
        for sid, (staged_id, path) in ENTRIES.items():
            shutil.copyfile(path, f"{d}/corpus/knowledge/{os.path.basename(path)}")
        header = ("# staged\n\n## Registry\n\n"
                  "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
                  "|---|---|---|---|---|---|---|---|---|---|---|\n")
        with open(f"{d}/corpus/SOURCES.md", "w", encoding="utf-8") as fh:
            fh.write(header + "\n".join(line for _, line in scratch_rows) + "\n")
        proc = subprocess.run(["bash", CENSUS, "validate", "--today", "2026-10-25", "--file", f"{d}/corpus/SOURCES.md"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\n=== maintained census parser, validate, staged rows AS-IS ===")
        print(f"argv: bash sources-census.sh validate --today 2026-10-25 --file {d}/corpus/SOURCES.md")
        print(f"exit={proc.returncode}")
        print("stdout:\n" + (proc.stdout or "<empty>"))
        if proc.stderr.strip():
            print("stderr:\n" + proc.stderr)

        # control: same rows with the escaped pipes removed from the raw line, nothing else changed
        ctrl = [line.replace("\\|", "/") for _, line in scratch_rows]
        with open(f"{d}/corpus/SOURCES.md", "w", encoding="utf-8") as fh:
            fh.write(header + "\n".join(ctrl) + "\n")
        proc2 = subprocess.run(["bash", CENSUS, "validate", "--today", "2026-10-25", "--file", f"{d}/corpus/SOURCES.md"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\n=== control: same rows with '\\|' replaced by '/' (isolates the pipe failure) ===")
        print(f"exit={proc2.returncode}")
        print("stdout:\n" + (proc2.stdout or "<empty>"))
        if proc2.stderr.strip():
            print("stderr:\n" + proc2.stderr)
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    if "--rows" in sys.argv:
        rows_audit()
    else:
        quote_audit()
