# ReviewCarriedOpenShapes — "Carried open — round-33 C2 counter shapes" (round-34.md @ 24a1647)

Axes: freshness (judged) + accuracy of the carried-open record. Read landed bytes only: sandbox clone
`/fast/scratch/hyaku/kake-r34/w2/ReviewCarriedOpenShapes/clone` at 24a16474ee73e20453f3e1be9d2f33573c5196d9
(HEAD verified). No lane mutation; no subagents; no tools installed (pacman paused; host python3/git sufficient).

## Setup checks (all exit 0)
- `git rev-parse HEAD` → 24a16474ee73e20453f3e1be9d2f33573c5196d9.
- `sha256sum .ufo/waves/round-34/c2_source_census.py` → ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892 —
  equals the lesson's "counter probed at" hash (round-34.md:117) and wave-1 ScribeCarriedOpenNames.md.
- `git diff --stat 5613071..24a1647 -- c2_source_census.py c2_pin_count.py` → empty: C34 line pointers stable.
- Baseline counter run at 24a1647: exit 0, `C2 5/5` (stderr receipt).

## Per-shape verdicts (lesson bullet → code)
Every C34/C33 pointer in the section was opened and matches its claim, except one (F3):
- junk-row (C34:215-218): cell 0 + `url in cells[1]` + cells[7]/[8] only; used-by check C33:126 (`ENTRY in cells[10]`) gone; kind/tier/scope/anchor/taught-fact unread — TRUE.
- duplicate-row (C34:215 `next()`) and duplicate-heading (C34:95-96): silent resolution vs C33:73-75/120-123 exact-one failure — TRUE.
- fence-blind sections (C34:95-101): `section_lines` has no fence state; fenced `## Registry` opens, fenced `## x` closes; r33 failed closed (ReviewC2CounterCode F2) — TRUE.
- escaped-pipe (C34:216-217): naive `.split("|")` + `>=11`; C33:119 `(?<!\\)\|` gone — TRUE (also round-34.md:144 corroborates).
- mode-blind bytes (C34:152): mode captured, never compared — TRUE, verified end-to-end (probe B below).
- anywhere-cite (C34:208,219): no required section; intro (lines 1-8) excluded; any later line counts — TRUE.
- bigint-crash (C34:235): uncaught ValueError, no JSON, exit 1 — TRUE, verified end-to-end (probe A below). But "over C34:66" is wrong: line 66 is `SRC_DIR = ...`; the `(\d+)` capture lives at C34:73.
- self-consistent-pair (C34:148-173,226-227): tree first line only string-matched (C34:148); archive checked against that same listing; text sha vs same-revision receipt (C34:226-227) — TRUE; M:5,16 = MutC2HollowCommit.md full-score-hollow lines, verified.
- Avoided line: path-set/blob equality C34:168-173, `errors="replace"` C34:199-201, strip heading C34:96, `\b` cite C34:219, archive try/except C34:158-166, URL substring C34:217-218 — all pointer-accurate.

## End-to-end probes (sandbox commits, unsets GIT_*, TMPDIR=sandbox tmp)
- Probe A bigint: replaced entry census line `pages=102` with a >4300-digit value; commit 34af8f16d2421898f697965b7268bddbd50d392f → exit 1, stdout 0 bytes, `ValueError ... line 235` — lesson claim confirmed.
- Probe B mode-blind: tree.txt `100644`→`100755` (blob ids/archive untouched), pristine entry restored from 24a1647; commit 0f20eea58fd04f25ebc9a359dfb86abc539fcb80 → exit 0, `C2 5/5`, census passed=true — a 100755-retained-blob commit scores full; lesson claim confirmed.
- Probe artifacts (stdout/stderr json) in `/fast/scratch/hyaku/kake-r34/w2/ReviewCarriedOpenShapes/clone/`.

## Findings by severity
1. MEDIUM — routed shape "misplaced section" (round-33-verifier-spotcheck.md:189) is not carried by name. "misplaced" appears nowhere in round-34.md; its substance is folded into the "anywhere-cite" bullet (round-34.md:102-104), which carries the same C34:208,219 pointers wave-1 used for misplaced-section. Content carried, routed name absent — the routing said "Carry them by name".
2. LOW — routed shapes "`S0650` substring cite" and "crash paths N1" are not named either (round-34.md:105 names only N2). Both are closed in C34, and the Avoided line carries their fixes ("word-boundary id cite" C34:219; `errors="replace"` C34:199-201), but neither the shapes nor their routed names appear; a reader cannot trace the routing item to these marks.
3. LOW — wrong pointer: bigint bullet "over C34:66" (round-34.md:104) should be C34:73 (`CENSUS` regex with `(\d+)`); line 66 is `SRC_DIR`. Typo copied from w1/ScribeCarriedOpenNames.md shape-14 row.
4. LOW — header sentence "all sit in the registry/entry layer, not the retained-bytes layer" (round-34.md:90) is contradicted by the section's own bullets: mode-blind bytes is about the retained tree.txt, and self-consistent-pair spans archive/listing/receipts.
5. LOW — "inherits six ... regresses three" (round-34.md:88-90) is ambiguous against its own bullets: the duplicate-row bullet cites C33:120-123 (r33 failed closed on duplicate rows), which by the section's standard makes four regressed, five inherited. Wave-1's table reached "three" only by marking escaped-pipe/duplicate-heading/mode-blind regressed and duplicate-row plain CARRY.
6. INFO — "junk S065 row with copied metrics": "junk-row" is carried by name; the copied-metrics half is carried only via the "(M:5,16)" pointer inside self-consistent-pair, not in words.
7. INFO — probe evidence line (round-34.md:115-117) points to `/fast/scratch/...` (probe_shapes.py) outside the lane; the P1-P7 outputs are retained in w1/ScribeCarriedOpenNames.md, but the script itself is not, and scratch paths rot.

## Routed item 1 coverage table (spotcheck lines 187-191)
- junk S065 row with copied metrics → carried (junk-row, +M:5,16) — near-name.
- misplaced section → substance carried as anywhere-cite; NAME MISSING (finding 1).
- even-backslash pipe → carried as escaped-pipe (parity language, P4) — near-name.
- fence-blind split → carried as fence-blind sections — near-name.
- `S0650` substring cite → fix carried on Avoided line; NAME MISSING (finding 2).
- crash paths N1/N2 → N2 carried by name; N1 NAME MISSING (finding 2).
- "do not reuse `c2_pin_count.py` as a gate without repair" → satisfied: round-34.md:80 "not reused as a gate".

## Residual risk / not verified
- Duplicate-row/heading, fence-blind, escaped-pipe, anywhere-cite, self-consistent-pair verdicts rest on code reading plus wave-1 function-level probes (P1-P4); I did not rebuild those mutants end-to-end. The full-score-hollow half of self-consistent-pair is additionally evidenced by the retained r34-c2-hollow-0cce15f0 bundle (disclosed; not re-reported as new).
- I did not run `c1_matrix_count.py` or the c2 matrix interface (out of seat).
- Probe commits 34af8f1/0f20eea5 exist only in my sandbox clone; the lane is untouched. Report is my only lane write.
