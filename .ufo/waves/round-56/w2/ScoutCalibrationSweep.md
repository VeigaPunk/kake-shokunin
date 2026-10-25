# ScoutCalibrationSweep

Round 56 W2. Measured in my own clone (`git clone --no-checkout` + `checkout a450e43e696d`), never the lane. Read-only; no tool installed. Sweep is regex-based, so the inventory below is a lower bound, not a census.

## SWEEP COMMANDS:

```
git clone -q --no-checkout <lane> "$D" && git -C "$D" checkout -q a450e43e696d032e3ac308383f6b3394e0c92860
# inventory (run in $D)
grep -nEi '\b[0-9]+ (entries|entry|rows?|files?|fixtures?|seats?|lessons?|sources?|claims?|sections?|keepers?|records?|probes?|checks?|tables?|waves?|rounds?|artifacts?|items?|pages?|repos?|bots?)\b|[0-9]+/[0-9]+|\b[0-9]+-(entry|file|row)' SKILL.md PROVINCE.md corpus/README.md
sed -n 1,40p SCORECARD.md | grep -noE '.{60}\b[0-9]+[ -](files?|entries|entry|rows?|fixtures?|seats?|claims?|lessons?|keepers?|states?)\b.{40}'
grep -n -i fixtures SKILL.md        # fixture/selftest tally mentions
# README.md (14 lines) and SHONEN.md (8 lines) read whole: no numeric self-assessment.
```
Per-statement verification commands are in `VERIFIED SAMPLE:` (command column).

## STATEMENTS:

Distinct countable-state statements found (location, text, checkable). "Covered" = inside the ten C1 rows, excluded here.
| Location | Text | Checkable |
|---|---|---|
| corpus/README.md:19 | fleet-registry "all 21 rows" | yes (entry table) |
| corpus/README.md:55 | sidecar "30 entries dated 2026-10-21" | yes |
| corpus/README.md:65 | vault "13 entries, 3 null URLs" | no (source tree absent; entry restates its own source) |
| corpus/README.md:78-80 | SOURCES "155 rows" at fcaf4b85, "156 rows" r55 final, "158 rows" r56 final | yes |
| corpus/README.md:278 | "313 row-statement units, 7 STALE" | not by one command (statements.json is a 6-key dict) |
| corpus/README.md:241 | "Seventeen frozen units (16 entries + property map)" | no single command found |
| PROVINCE.md:403-404 | "21 knowledge files ... 24 rows added" | partly (coverage-map row counts at revisions: 28 at fcaf4b85, 74 at e48354b7, 78 now; the "24" delta is not reproducible from them) |
| PROVINCE.md:166,199 | "102 pages, 87 og:title, ..." | no (retained HTML census, upstream tree) |
| SKILL.md:30,90 | "21 rows" fleet.config.json, "18-row fleet snapshot" | no (file absent: `test -e` exit 1) |
| SKILL.md:205 | "160 claims" r16 sweep | no |
| SKILL.md:490 | matrix "32/32" | yes |
| SKILL.md:593 | round-26 selftest "24 cases" | yes |
| SKILL.md:627,667-668 | "55/58", "58/58", "16/16", "29-case", "Git30" | no single command found |
| SKILL.md:770 | citing-set "(41 cases)" | yes |
| SKILL.md:1013,1021 | census line pages=102 ... | no |
| SKILL.md:1025,1029 | link-preview "29 fixtures", "35 fixtures at 76fac3b" | yes (git ls-tree) |
| SKILL.md:1046 | link-preview row "45 fixture directories at b1cbbc39" | yes |
| SKILL.md:1110,1116,1141,1156,1184 | robots 194/204, sitemap 179/183/235 fixtures | yes (selftests) |
| SKILL.md:1193 | c47 "2/2 rows, 2/2 receipts" | yes |
| SCORECARD.md:17-18 | "31-file state sha guard", "66 targets / 49 resolve / 10 declared-absent / 0 drift / 39 files", "160 claims", "36 set" | only via `freshness-sweep.mjs --offline` (fails, see sample 11) |
| SCORECARD.md:26,33 | Plan: "4/21 -> 21/21 knowledge entries carry metadata"; "1/15 -> every lane-authored lesson has a Gate" | yes (the doc's own count commands) |

## VERIFIED SAMPLE:

| # | Location / statement | Command | Output | Verdict |
|---|---|---|---|---|
| 1 | corpus/README.md:55 sidecar 30 entries | `python3 -c 'import json;d=json.load(open("corpus/knowledge/freshness-sidecar.json"));print(len(d["entries"]))'` | 30 | agree |
| 2 | corpus/README.md:78-80 SOURCES 155 rows at fcaf4b85; 158 at final | `grep -cE '^\| *S[0-9]+ *\|' corpus/SOURCES.md`; same on `git show fcaf4b85:corpus/SOURCES.md` | 158; 155 | agree (156 at r55 final not measured) |
| 3 | corpus/README.md:19 fleet-registry "all 21 rows" | `awk 'NR>=45 && /^\| / && !/^\| id/ && !/^\|---/' corpus/knowledge/fleet-registry.md \| wc -l` | 21 | agree |
| 4 | SKILL.md:770 citing-set "(41 cases)" | `python3 -B scripts/citing_set_selftest.py` (JSON `cases`); `ls -d scripts/fixtures/citing-set/*/ \| wc -l` | cases 45, passed; 45 dirs | **DISAGREE** (41 vs 45; same class as C1, outside the ten rows, prose not row cell) |
| 5 | SKILL.md:1046 link-preview row "45 fixture directories at b1cbbc39" | `git ls-tree -d --name-only b1cbbc39:scripts/fixtures/link-preview/ \| wc -l`; same at a450e43 | 45 at pin; 46 at tip; selftest `46/46` | agree at the pinned revision; the pin is dated, tip is 46 (contract C1 already excludes this row) |
| 6 | SKILL.md:1029 "35 fixtures at 76fac3b"; :1025 "29 fixtures" | `git ls-tree -d --name-only 76fac3b:scripts/fixtures/link-preview/ \| wc -l` | 35 | agree for :1029 (revision-pinned); :1025 "29" is un-pinned present tense, tip is 46, not remeasured at its own revision |
| 7 | SKILL.md:1116 "robots selftest now has 204 fixtures" | `python3 -B scripts/robots_audit_selftest.py` | `cases 204 passed 204` | agree |
| 8 | SKILL.md:1184 sitemap "selftest 235 fixtures" | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` | `PASS 235/235` | agree (older "179"/"183" at :1141/:1156 are superseded by :1184, not stated as current) |
| 9 | SKILL.md:490 matrix "32/32" and :593 "24 cases" | `python3 -B .ufo/waves/round-22/matrix.py --root .`; `python3 -B .ufo/waves/round-26/measure.py --selftest` | `accepted=32 total=32 discrepancies=0`; `passed 24 failed 0` | agree (both) |
| 10 | SKILL.md:1193 "2/2 rows, 2/2 receipts" | `python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision HEAD` | `registry_rows=2/2 receipts=2/2 C1_MET` | agree |
| 11 | SCORECARD.md:18 "66 targets / 49 resolve / ... 39 files" (and sidecar, corpus/README.md:55) | `node scripts/freshness-sweep.mjs --offline` at a450e43 and at base e48354b7 | both: `Error: paths sidecar binding invalid: SKILL.md:364`; sha-recompute of the sidecar's SKILL.md entries: lines 364,445,448,449,450,423,431 mismatch (7 of 10) | **DISAGREE/unmeasurable**: the standing instrument those figures rest on cannot run; failure predates round 56 (identical at base), cause: line SHA-256 bindings stale after SKILL.md edits |
| 12 | SCORECARD.md:26 plan "4/21 -> 21/21 entries carry source/verified-at/recheck" (doc's own command) | the python one-liner in SCORECARD.md:27 | source 49/49, verified-at 49/49, recheck 49/49 | agree (superseded denominator 21 -> 49; no stale-present claim) |
| 13 | SCORECARD.md:33 plan "every lane-authored lesson has an appended gate" (doc's own command) | `ls corpus/lessons/round-*.md \| grep -v aggregator \| xargs grep -l '^## Gate' \| wc -l` | 52 of 84 files; for rounds 1-21: 16 of 18 (no gate: round-20-/round-21-verifier-spotcheck.md) | partial/disagree if read as a standing state; it is a dated plan item, "lane-authored" undefined |

(Rows 1-13 = 13 distinct statements; the requested 10 are rows 1-10, rows 11-13 are extra.)

## LIMIT:

Disclosed limit, not a claim. Regex inventory finds about 21 distinct countable-state statement groups across the five-plus files (table above), of which 13 were measured here (1 outright drift: citing-set 41 vs 45; 1 broken instrument; 1 dated plan claim now false as a standing state). Left unmeasured: about 8 groups, 6 of them with no single command found (corpus/README.md:65, 241, 278; SKILL.md:30/90/205/627/667/1013; PROVINCE.md:166/199; SCORECARD.md:17-18 beyond the sweep; PROVINCE.md:404's "24" delta), 2 checkable by a command I did not run (SOURCES "156 rows" at the round-55 final revision; SKILL.md:1025 "29 fixtures" at its own revision). Not scanned: statements phrased without my noun list or number form (spelled-out numbers like "Seventeen", prose in SKILL.md sections not matched), and every file other than the six named. Of 13 measured, drift outside the ten C1 rows exists in 1 (SKILL.md:770); C1 as scoped does not reach it. The counters C1 adds guard only the ten rows; SKILL.md:770, :1025 and the freshness-sidecar bindings stay unguarded.

VERDICT: Sweep sized the class at ~21 statement groups; 13 measured, 1 stale count outside C1 scope (SKILL.md:770 says 41, selftest prints 45), 1 pre-existing broken instrument (freshness-sweep sidecar bindings), ~8 unmeasured.
