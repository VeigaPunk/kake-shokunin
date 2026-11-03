# ScoutAdoption receipts — round 70, C2 assimilation dossier

Read-only. Base revision: `e5f6fd9e4c243d092160bc74e8bea24256087173` (lane master). No lane file
edited; no tool installed or upgraded; no campaign tool run in shokuknow.

## A. Registry / staged id extraction (contract §10)

Scratch copy of the base registry:

    git -C /home/vgpnk/Projects/shokunin/kake-shokunin show e5f6fd9e:corpus/SOURCES.md > lane-SOURCES.md
    # exit 0, 291 lines, 161428 bytes

Specified extractor, lane:

    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' lane-SOURCES.md | grep -oE 'S[0-9]+' | sort > lane-ids.txt
    # 175 ids; S001..S139, then S249 S262 S263 S273 S274 S286 S312 S329 S367 S372 S373 S374 S390
    # S409 S416..S437 ; max = S437

    awk -F'|' '/^\| *S[0-9]{3,} *\|/ {c[NF]++} END{for(k in c) print "NF="k, c[k]}' lane-SOURCES.md
    # NF=13 175   (header line 8 = 11 cells; every registry row = 11 cells, no escaped pipe)

    grep -nE '^ {4,}\|[[:space:]]*S[0-9]' lane-SOURCES.md   # no output: no 4+-space indented id row
    grep -cE '^\| *S[0-9]{3,}.*\|$' lane-SOURCES.md          # 175 (all rows close with '|')

Specified extractor, staged package:

    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md \
      | grep -oE 'S[0-9]+' | sort > staged-ids.txt
    # 129 ids, S287..S415, no duplicates (uniq -d = 0)

    comm -12 lane-ids.txt staged-ids.txt > collisions.txt
    # S312 S329 S367 S372 S373 S374 S390 S409   (8)

Collision identity check (one example, the rest share the pattern):

    awk -F'|' '/^\| *S312 *\|/{print $3}' lane-SOURCES.md          # 百度搜索资源平台 — 平台工具使用手册（移动适配） — …id=267&page=15
    awk -F'|' 'NR==32{print $3}' SOURCES.append.md                  # identical source cell

S352 check:

    grep -c '^S352$' lane-ids.txt        # 0 (exit 1)
    grep -c 'S352' lane-SOURCES.md       # 0 (exit 1) — the token does not occur in the file at all

Next unused id:

    grep -c 'S438' lane-SOURCES.md       # 0
    git -C /home/vgpnk/Projects/shokunin/kake-shokunin grep -c 'S438' e5f6fd9e   # no matching path
    # first gap after max S437 = S438; staged set ends at S415

Staged-row field measurement (append lines 23, 24, 72):

    awk -F'|' 'NR==23||NR==24||NR==72 {print "NF="NF}' SOURCES.append.md   # NF=14 each
    # one escaped pipe '\|' per row, inside the recheck cell (cell 11 of 11):
    #   line 23 offset 713, line 24 offset 814, line 72 offset 662 (byte offsets in the line)
    # remove the escape and the row is 13 fields = the lane's convention

Base absence of the C2 entry:

    git -C …/kake-shokunin cat-file -e e5f6fd9e:corpus/knowledge/crux-bigquery-origin-membership.md
    # fatal: path … does not exist in 'e5f6fd9e'; exit 128

Lane URL coverage at base (no row for either staged source):

    grep -oE 'https://developer\.chrome\.com/docs/crux/[a-z-]+' lane-SOURCES.md | sort | uniq -c
    #   1 …/docs/crux/api      (S039)
    #   1 …/docs/crux/methodology (S038)
    # docs/crux/vis, docs/crux/bigquery, records:queryRecord: 0 rows each

## B. Supplementary live spot check (2026-11-03) — NOT the C2(c) retained-body receipt

ScoutSources owns the retained body and its receipt; this is a scout-side byte check only.

    curl -fsSL --max-time 20 https://developer.chrome.com/docs/crux/bigquery -o bigquery.html
    # exit 0, 110693 bytes, sha256 a9df3dd14654d56e6f71a8f2d39fae76e7b5bb5e5e07ce9794a4348838afdd18

    grep -F -c 'The origin_summary table contains a list of all origins in the CrUX dataset' bigquery.html
    # 0   ← the staged row's recheck claims "-> 1 (ran 2026-10-24)"

Cause (raw excerpt at byte 89704):

    <p>The <code translate="no" dir="ltr">origin_summary</code> table contains a list of all origins
    in the CrUX dataset; it is updated monthly with the latest list of origins in the dataset and has
    a single column: <code translate="no" dir="ltr">origin</code>.</p>

The `<code>` element interrupts the sentence, so only a collapsed-text match succeeds:

    method: strip tags with re.sub(r'<[^>]+>',' '), html.unescape, re.sub(r'\s+',' ')
    'The origin_summary table contains a list of all origins in the CrUX dataset' -> 1 match
    (the source sentence continues "; it is updated monthly with the latest list of origins…")

Other statements on the same page (collapsed text, 2026-11-03):

    "CrUX data on BigQuery is released on the second Tuesday of the following month."
    "Each month is released as a new table under chrome-ux-report.all ."
    "Using BigQuery requires a Google Cloud account and basic knowledge of SQL."
    "The CrUX dataset on BigQuery is free to access and explore up to the limits of the free tier…"
    "Note that a credit card must be provided for the Google Cloud project"
    occurrences of "API key" on this page: 0

    curl -fsSL --max-time 20 https://developer.chrome.com/docs/crux/vis -o vis.html
    # exit 0, 114603 bytes, sha256 edeb8632411016dafe32e97f6b6a0f6925a51b2c8ecd9bb443c00d55d9837f28

    grep -c 'If your origin is not included in the CrUX dataset, there will be no data to display' vis.html  # 1
    grep -c 'may not have sufficient data to be included' vis.html                                          # 1

    page context: "There are over 15 million origins in the dataset, but the one you want may not have
    sufficient data to be included. Some common issues with origins are providing the wrong protocol,
    for example http:// instead of https:// , and omitting the subdomain when needed."
    page on keys: "All data in CrUX Vis comes from the CrUX History API which can be queried using a
    CrUX API key."   (the page never says Vis is key-free; "API key" occurs once)

## C. Files in this directory

- `lane-ids.txt` (175) — lane registry ids from the specified extractor
- `staged-ids.txt` (129) — staged append ids, same extractor
- `collisions.txt` (8) — `comm -12` output
