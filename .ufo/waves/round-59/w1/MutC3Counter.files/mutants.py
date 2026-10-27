#!/usr/bin/env python3
"""Round-59 C3 mutation matrix: single-point mutants of the counter snapshot.

Each mutant is one textual replacement in a copy of the pristine counter.
The detector (detect.py) runs the counter's own run_checks over the fixture
variant set; a mutant is KILLED when any variant's observable result
(exit, per-check state, notes) differs from the pristine run.
"""
import hashlib
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r59/MutC3Counter"
PRISTINE = f"{S}/pristine.py"
MUT = f"{S}/mutants"

MUTANTS = [
    ("M00_noop", "# version 2: no headings from code samples", "# version two: no headings from code samples",
     "control: comment-only change, no behavioural delta expected"),
    ("M01_window_80", "STALE_WINDOW = 8", "STALE_WINDOW = 80",
     "C9 insert window 8 -> 80 base lines"),
    ("M02_window_4", "STALE_WINDOW = 8", "STALE_WINDOW = 4",
     "C9 insert window 8 -> 4 base lines"),
    ("M03_no_append_only",
     'if any(tag in ("delete", "replace") for tag, *_ in ops):\n                c9.append("not append-only: a base line of the entry is deleted or changed")',
     "if False:\n                pass",
     "C9 append-only diff check removed"),
    ("M04_no_tag",
     "if CORRECTION_TAG not in block:", "if False:",
     "C9 [r59-correction <date>] tag check removed"),
    ("M05_loose_s425",
     'if not re.search(r"\\bS425\\b", block):', 'if not re.search(r"\\bS42", block):',
     "C9 S425 citation regex loosened (no word boundary)"),
    ("M06_no_topic",
     ' and TOPIC["S425"] in span):', "):",
     "C9 page-named-subject (IP address) requirement removed"),
    ("M07_char_ceiling",
     "CHAR_CEILING = 160", "CHAR_CEILING = 400",
     "character ceiling 160 -> 400"),
    ("M08_no_collapse",
     'texts[sid] = re.sub(r"\\s+", " ", raw.decode("utf-8"))',
     'texts[sid] = raw.decode("utf-8")',
     "whitespace collapse of the retained body removed"),
    ("M09_article_end",
     'ARTICLE_END = {"S425": "<devsite-content-footer", "S426": "<devsite-content-footer"}',
     'ARTICLE_END = {"S425": "</devsite-content-footer>", "S426": "</devsite-content-footer>"}',
     "article end marker changed to the closing tag"),
    ("M10_headings_h1_6",
     r'for h in re.findall(r"(?is)<h[23]\b[^>]*>(.*?)</h[23]>",',
     r'for h in re.findall(r"(?is)<h[1-6]\b[^>]*>(.*?)</h[1-6]>",',
     "article heading regex <h2>/<h3> -> <h1>..<h6>"),
    ("M11_date_outside_nodes",
     'elif not any(f"Last updated {pub.group(1)} UTC" in seg for seg in re.findall(\n'
     '                    r">([^<>]+)(?=<)", re.sub(r"(?is)<(style|script)\\b.*?</\\1>", "<>", texts[sid]))):',
     'elif not (f"Last updated {pub.group(1)} UTC" in texts[sid]):',
     "printed-revision check moved outside the text nodes (raw substring)"),
    ("M12_used_by_unsorted",
     "got = sorted(used_by(row[10]))", "got = used_by(row[10])",
     "used-by comparison loses its sorted() normalisation"),
    ("M13_no_stale_once",
     "if sum(1 for ln in ml if ln == STALE_LINE) != 1:", "if False:",
     "C9 stale-sentence-preserved-once check removed"),
    ("M14_no_curly",
     "if CURLY.search(block):", "if False:",
     "C9 curly-double-quote refusal removed"),
    ("M15_loose_position",
     'if tag == "insert" and i1 == end and end <= s + 1 + STALE_WINDOW:',
     'if tag == "insert" and s < i1 <= end and end <= s + 1 + STALE_WINDOW:',
     "C9 insert position relaxed from exactly-the-bullet-end to anywhere in the bullet"),
    ("M16_no_prose_filter",
     'block = re.sub(r"`[^`]*`", " ", re.sub(r"(?s)<!--.*?-->", " ", "\\n".join(tails)))\n'
     '            block = re.sub(r"<[^>]*>", " ", block).replace("\\n", " ")',
     'block = "\\n".join(tails).replace("\\n", " ")',
     "C9 rendered-prose filter (code spans / comments / tags) removed"),
    ("M27_no_tag_strip_c9",
     'block = re.sub(r"<[^>]*>", " ", block).replace("\\n", " ")',
     'block = block.replace("\\n", " ")',
     "C9 tag strip removed: an HTML attribute counts as rendered prose"),
    ("M26_no_chrome_strip",
     'chunk = re.sub(r"(?is)<(aside|nav|devsite-feedback|devsite-thumb-rating)\\b.*?</\\1>", "<>", chunk)',
     'chunk = chunk',
     "text_segments: page chrome (aside/nav/feedback) blanking removed"),
    ("M17_units_floor_2",
     "if (6 <= units(span) <= UNIT_CEILING", "if (2 <= units(span) <= UNIT_CEILING",
     "C9 quote unit floor 6 -> 2"),
    ("M18_unit_ceiling",
     "UNIT_CEILING = 25", "UNIT_CEILING = 40",
     "unit ceiling 25 -> 40"),
    ("M19_no_in_content",
     ' and in_content(text, span, "S425")', "",
     "C9 article-block membership requirement removed"),
    ("M20_min_unique_1",
     "MIN_UNIQUE_SPANS = 3", "MIN_UNIQUE_SPANS = 1",
     "entry page-unique span floor 3 -> 1"),
    ("M21_no_gate_unique",
     "if any(q in t for q in spans for t in others) or any(text.count(q) != 1 for q in spans):",
     "if False:",
     "Gate quote page-uniqueness check removed"),
    ("M22_no_gate_units",
     'if f"{units(q)} units" not in line:', "if False:",
     "Gate line unit-count annotation check removed"),
    ("M23_title_floor_6",
     "if not title or units(title) < 3 or title != page_title:",
     "if not title or units(title) < 6 or title != page_title:",
     "row-title unit floor 3 -> 6 (the pre-wave-1 rule)"),
    ("M24_no_cross_body",
     ' and text.count(span) == 1 and not any(span in t for t in others) and TOPIC["S425"] in span',
     ' and text.count(span) == 1 and TOPIC["S425"] in span',
     "C9 cross-body uniqueness requirement removed"),
    ("M25_no_code_strip_headings",
     r're.sub(r"(?is)<(pre|code|script|style)\b.*?</\1>", "<>", text[win[0]:win[1]]))]',
     r'text[win[0]:win[1]])]',
     "article_headings loses its code/script strip"),
]


def make_mutants():
    src = open(PRISTINE, encoding="utf-8").read()
    os.makedirs(MUT, exist_ok=True)
    report = []
    for name, old, new, desc in MUTANTS:
        n = src.count(old)
        if n != 1:
            report.append({"id": name, "desc": desc, "status": "BAD_PATCH", "occurrences": n})
            continue
        path = f"{MUT}/{name}.py"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src.replace(old, new, 1))
        report.append({"id": name, "desc": desc, "status": "ok", "path": path,
                       "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()})
    return report


def main():
    made = make_mutants()
    json.dump(made, open(f"{S}/mutants.json", "w", encoding="utf-8"), indent=1)
    for r in made:
        print(r["id"], r["status"], r.get("occurrences", ""))
    bad = [r["id"] for r in made if r["status"] != "ok"]
    if bad:
        print("BAD PATCHES:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
