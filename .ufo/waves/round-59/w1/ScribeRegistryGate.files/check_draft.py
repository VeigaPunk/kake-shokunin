#!/usr/bin/env python3
"""Read-only pre-check of the two draft rows + Gate lines against the frozen round-59 C3 counter's own code.

Reads: lane registry (worktree), the retained bodies, the counter module. Writes only under the seat scratch dir.
"""
import hashlib
import importlib.util
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-59"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ScribeRegistryGate"

spec = importlib.util.spec_from_file_location("c59", f"{WAVE}/c59_quote_truth.py")
c59 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c59)

base_text = open(f"{LANE}/corpus/SOURCES.md", encoding="utf-8", newline="").read()
rows_txt = open(f"{SCRATCH}/rows.md", encoding="utf-8").read().rstrip("\n").splitlines()
gate_txt = open(f"{SCRATCH}/gate.md", encoding="utf-8").read().rstrip("\n")

# append after the S424 row (last registry row) — same place the integration will use
lines = base_text.splitlines(keepends=True)
last = max(i for i, ln in enumerate(lines) if re.match(r"^ {0,3}\| *S[0-9]{3,} *\|", ln))
draft = "".join(lines[: last + 1]) + "\n".join(rows_txt) + "\n" + "".join(lines[last + 1:])
open(f"{SCRATCH}/sources-draft.md", "w", encoding="utf-8", newline="").write(draft)

rows = c59.parse_registry(draft)
base_rows = c59.parse_registry(base_text)
texts, bodies, problems = {}, {}, []

for sid in c59.NEW_ROWS:
    raw = open(f"{WAVE}/sources/{sid}.html", "rb").read()
    bodies[sid] = raw
    texts[sid] = re.sub(r"\s+", " ", raw.decode("utf-8"))
    row = rows.get(sid)
    if row is None:
        problems.append(f"{sid}: no row parsed")
        continue
    # C3 row shape
    if len(row) != 11:
        problems.append(f"{sid}: {len(row)} cells")
    if row[7] != "mined":
        problems.append(f"{sid}: status {row[7]!r}")
    if row[8] != c59.ROUND_DATE:
        problems.append(f"{sid}: opened {row[8]!r}")
    if not re.fullmatch(r"(\d{4}-\d{2}-\d{2}|\d+d|on-release)", row[9]):
        problems.append(f"{sid}: recheck {row[9]!r}")
    if c59.row_url(row) != c59.ROW_URL[sid]:
        problems.append(f"{sid}: url {c59.row_url(row)!r}")
    if row[2] not in c59.ROW_KINDS or row[3] not in ("A", "B", "C"):
        problems.append(f"{sid}: kind/tier {row[2]!r}/{row[3]!r}")
    if len(row[4]) < 20 or len(row[6]) < 20:
        problems.append(f"{sid}: scope/teaches too short")
    if sid in base_rows:
        problems.append(f"{sid}: already in base")
    if any("|" in c for c in row):
        problems.append(f"{sid}: pipe inside a cell")
    # C4 used-by
    got, want = sorted(c59.used_by(row[10])), sorted(c59.USED_BY[sid])
    if got != want:
        problems.append(f"{sid}: used-by {got!r} != {want!r}")
    # C5 row facts
    if hashlib.sha256(raw).hexdigest() != c59.BODY_SHA256[sid]:
        problems.append(f"{sid}: sha256 mismatch")
    title = " — ".join(row[1].split(" — ")[1:-1])
    page_title = (re.search(r"<title>([^<]*)</title>", texts[sid]) or [None, ""])[1].split(" | ")[0].strip()
    if title != page_title:
        problems.append(f"{sid}: row title {title!r} != page title {page_title!r}")
    elif c59.units(title) < 6:
        problems.append(f"{sid}: page title {title!r} is {c59.units(title)} units, below the counter's 6-unit title floor (faithful value cannot pass)")
    anchor_cell = row[5]
    am = re.match(r"^§\s*(.*?)\s*\(Last updated \d{4}-\d{2}-\d{2} UTC\)\s*$", anchor_cell)
    if not am:
        problems.append(f"{sid}: anchor cell form {anchor_cell!r}")
    else:
        head = am.group(1)
        if c59.units(head) < 3 or head not in c59.article_headings(texts[sid], sid):
            problems.append(f"{sid}: anchor heading {head!r} not an h2/h3 of the article block")
        pub = re.search(r"\(Last updated (\d{4}-\d{2}-\d{2}) UTC\)\s*$", anchor_cell)
        if not any(f"Last updated {pub.group(1)} UTC" in seg for seg in re.findall(r">([^<>]+)(?=<)", texts[sid])):
            problems.append(f"{sid}: page does not print Last updated {pub.group(1)} UTC")
    if c59.content_window(texts[sid], sid) is None:
        problems.append(f"{sid}: no article block")
    # Gate line
    one = "\n".join([ln for ln in gate_txt.splitlines() if ln.strip().startswith(f"- {sid} ")])
    if not one:
        problems.append(f"{sid}: no gate line")
        continue
    if c59.CURLY.search(one):
        problems.append(f"{sid}: curly quotes in gate line")
    allq = re.findall(r'"([^"]+)"', one)
    spans = [q for q in allq if c59.units(q) >= 6]
    if not any(c59.TOPIC[sid] in q for q in spans):
        problems.append(f"{sid}: no gate quote carries {c59.TOPIC[sid]!r}")
    if hashlib.sha256(bodies[sid]).hexdigest() not in one or f"{len(bodies[sid])} bytes" not in one:
        problems.append(f"{sid}: gate line lacks sha256/byte count")
    if anchor_cell not in one:
        problems.append(f"{sid}: gate line lacks the anchor cell verbatim")
    if c59.ROW_URL[sid] not in one or c59.ROUND_DATE not in one:
        problems.append(f"{sid}: gate line lacks URL or access date")
    for q in spans:
        if f"{c59.units(q)} units" not in one:
            problems.append(f"{sid}: gate line does not state {c59.units(q)} units for {q[:30]!r}")
        if not 6 <= c59.units(q) <= c59.UNIT_CEILING:
            problems.append(f"{sid}: gate quote {q[:30]!r} outside 6..25 units")
        if len(q) > c59.CHAR_CEILING:
            problems.append(f"{sid}: gate quote over char ceiling")
        if q not in texts[sid]:
            problems.append(f"{sid}: gate quote not a substring of the body")
        elif not c59.in_content(texts[sid], q, sid):
            problems.append(f"{sid}: gate quote not inside one collapsed text node")
        others = [t for k, t in texts.items() if k != sid]
        if texts[sid].count(q) != 1 or any(q in t for t in others):
            problems.append(f"{sid}: gate quote not page-unique")
    print(f"{sid}: gate quotes {[(q[:46], c59.units(q), len(q)) for q in spans]}")

# census on the draft (frozen CORPUS.md formulas, run over the scratch copy)
def sh(cmd):
    return subprocess.run(cmd, shell=True, cwd=SCRATCH, text=True, capture_output=True).stdout.strip()

print("rows:", sh("grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' sources-draft.md"))
print("malformed:", sh("awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF!=13 {n++} END{print n+0}' sources-draft.md"))
print("dup ids:", sh("awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {i=$2; gsub(/[[:space:]]/,\"\",i); print i}' sources-draft.md | sort | uniq -d"))
print("enums:", sh("awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,\"\",i); gsub(/[[:space:]]/,\"\",k); gsub(/[[:space:]]/,\"\",t); gsub(/[[:space:]]/,\"\",s); if (t !~ /^[ABC]$/) print \"tier\", i, t; if (s !~ /^(queued|mined|rejected)$/) print \"status\", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print \"kind\", i, k; if (t==\"A\" && k==\"community\") print \"tier-inflation\", i}' sources-draft.md"))
print("status hist:", sh("awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {s=$9; gsub(/[[:space:]]/,\"\",s); n[s]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}' sources-draft.md"))
print("tier hist:", sh("awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {t=$5; gsub(/[[:space:]]/,\"\",t); n[t]++} END{for(k in n) printf \"%s=%d \", k, n[k]; print \"\"}' sources-draft.md"))
print("PROBLEMS:", len(problems))
for p in problems:
    print(" -", p)
