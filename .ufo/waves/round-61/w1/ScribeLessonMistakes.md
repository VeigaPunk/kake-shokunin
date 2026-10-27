# ScribeLessonMistakes

Round-61 w1 (build) · lane kake-shokunin · leaf scribe · access date 2026-10-27 (UTC) · base `9f07731a873585e655a6518233ea39f5d9fb8204`
· lane HEAD at work `eaa9177e2965a50fa038d57254934a53909052b6` (contract commit). I drafted the round-61 lesson and executed no
counter, no tool under build and no after-state. Every claim below is read from committed bytes, from a committed file in the lane
worktree, or is marked `[INFERENCE]`.

## LESSON:

Path: `.ufo/waves/round-61/w1/ScribeLessonMistakes.files/lesson.md` (97 lines, sha256
`fe2c2fa731c9f4b653229a2d6e321cfe7da40077b42ffc0c8c81328ab3f4fc57`; earlier drafts: `a06b54de…` = the four-row version before
SentinelC2Net's two precision points, `0a86a711…` = the three-row version before row 4 arrived under L1 ruling d). Sections, as the seat item names them:

- `# Round 61` — open date, base, the contract-commit relation, wave shape, and one line per claim (C1 calibration / C2 operability /
  C3 freshness) with each frozen predicate and the no-score-change declaration.
- `## Mistakes` — three rows (below), table shape `Class | Evidence | Captured-by | Fix` matching `round-60.md`.
- `## Gate` — skeleton only: four fill rules, the four C2 row lines (S430–S433) and the ten C3 row lines (S001–S010) with URLs and
  pins pre-filled and every measured value a `<…>` placeholder, plus the assimilation admit/reject record.
- `## Carried` — R60-D4, R60-D5, R60-D6 with their contract wording.

States written into the draft, deliberately: the C1 instruments (`scripts/receipt_lineage.py`, `.ufo/waves/round-61/c61_lineage_cases.py`,
`.ufo/receipt-disclosures.json`) are **absent** at lane HEAD as observed, so the draft claims no exit, case count or event number for
them; the ability-to-fail evidence is stated as the frozen contract cases L2/L6/L7 with L4/L5 as discriminators and R1 = 0/18 as the
do-nothing control, not as an observed run.

## MISTAKE ROWS:

Four rows.

1. **`process/undisclosed-receipt-rewrite`** (the mined class the contract asks for). Evidence is re-read from committed bytes, not
   taken on the verifiers' word:
   - r56: `git show 4cb225f:.ufo/waves/round-56/controls/after-c1-selftally.txt` ends `revision: f8438a282d5946b386812d784cc617edcbc9201d`;
     the same path at `ad06cb8` ends `revision: 4cb225fb032b04166fb0232bc98a7bcce72675ec`. `controls/c2-selftest.txt` reads
     `67/67 (fixture revision f8438a282d59)` at `4cb225f` and `86/86` at `ad06cb8`. `after-c2-quote-truth.txt` carries the same
     revision-line swap. Differing bytes: only the `revision:` line (`git show <rev>:<path> | tail -4`, both revisions).
   - r57: `git show 31b61a4:.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` is `pending` + `revision: 32754df75774dd38…` +
     `EXIT=0`; at `20217f2` the same path carries the counter line plus `tip: 31b61a4ddfcade92c108ff3786b8e9770bc8da31` and the same
     `revision:` line. That is the contract's `pending_filled` shape.
   - Captured-by is `none`: no in-lane rule read a receipt's history; `round-56-verifier-spotcheck.md` §6 defect 1 and
     `round-57-verifier-spotcheck.md` §5 D1 (plus considerthese `2026-10-26.md` Part 1 §2 and Part 2 proposal 2) are the only
     captures. Fix = claim C1's tool + disclosures + counter, cases L2/L6/L7.
2. **`number-drift` (R60-D2, EN-unit erratum, correction note, no claim).** The round-60 scout printed 19 whitespace tokens
   (`.ufo/waves/round-60/w1/ScoutRejectCommonJa.md`); the lane's own rule measures **22** units. My run of that rule
   (`.files/units_probe.py`, which transcribes `CJK_RE` from `.ufo/waves/round-60/c60_quote_truth.py:120` and `units()` from `:189`)
   on the retained EN body: `units 22 chars 112 tokens 22`, one occurrence in the whitespace-collapsed text. Retained body
   `.ufo/waves/round-60/w1/ScoutRejectCommonJa.files/en.html`, sha256 `8f7f1e9b239309edd6f001ac4bc374e52a11a6bc3f2feca7610e066d54e6d664`,
   88,970 bytes, committed (both the path and its blob are present at base `9f07731`, `git ls-tree -r`).
3. **`process/receipt-grammar` (R60-D3).** Round-60's T1 receipts lacked the `# receipt:` first line (`round-60-verifier-spotcheck.md`
   §6 item 3); captured-by `none` (a convention with no reader). Fix = the contract receipt rule plus C1's lineage tool treating
   `^\s*#\s*receipt\s*:` as one of its three receipt-grammar forms.
4. **`process/tool-bytes-not-retained`** (row 4, pasted from `SentinelC2Net` under L1 ruling d; text from
   `.ufo/waves/round-61/w1/SentinelC2Net.files/lesson-mistake-row4.md`, attribution kept in the Class cell). Evidence: the 12 C2 capture
   receipts were written by `scripts/response_snapshot.py` while it was uncommitted; the producing bytes (sha256
   `eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`) survive in no artifact, and the worktree file is
   `ba107024c770…`. Verified by me this round: that digest has an independent, executor-authored source — one occurrence in
   `.ufo/waves/round-61/w1/ExecC2Capture.files/run.txt`; the current tool is sha256
   `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7`, 10,217 bytes, mtime `2026-10-27 06:17:14 -0300`; `git ls-tree
   HEAD scripts/` holds no `response_snapshot.py` and `git log -- scripts/response_snapshot.py` is empty; and the containment claim is
   re-checkable today — `pre_excerpt.txt` (2,864 bytes) and `pre_excerpt2.txt` (678 bytes) each occur verbatim in the current tool
   (`… in open('scripts/response_snapshot.py').read()` → `True` twice). So the split is: the delta claim is re-checkable, the producing
   bytes are unrecoverable — which is the row's point. What only SentinelC2Net ran is the comparison against the then-current pre-edit
   file. Captured-by `none` plus that manual capture; the draft carries the sentinel's honesty note below the table (process defect,
   not data: 12/12 receipts re-verifiable).

## GATE SKELETON:

What the draft carries, and what stays placeholder:

- **C2 (S430–S433)**: URLs and access date pre-filled from contract §Claim C2 — `https://www.rfc-editor.org/rfc/rfc6797.html`,
  `https://www.w3.org/TR/CSP3/`, `https://fetch.spec.whatwg.org/`, `https://www.rfc-editor.org/rfc/rfc9110.html`; anchor heading,
  quote span, unit count, sha256, bytes and HTTP status are placeholders, because `.ufo/waves/round-61/sources/receipts.json` does
  not exist yet (the four bodies `S430.html`…`S433.html` are on disk, sizes 133,951 / 1,011,256 / 1,854,393 / 1,187,554 bytes at this
  writing, **unverified against any receipt** — nothing is quoted from them).
- **C3 (S001–S010)**: the ten ids, the base cadence cells (`on-release`, `on-release`, `90d`×5, `365d`×3, all opened 2026-10-19, status
  `mined`) and the pinned dates are pre-filled from contract §Claim C3; the fetched URL, anchor, quote, sha256, bytes and status are
  placeholders, plus the unpinned-row template for a non-200 / quote-missing / fetch-failed row. Every change is written to be logged
  old → new on its own line (contract rule 2).
- **Assimilation record**: three template lines (`Assimilation: none — …` with the slice sha256 placeholder, `ADMIT:`, `REJECT:`), with
  the contract's `none` rationale and the quarantine hold stated, since the contract fixes `Assimilation: none` this round.

## Findings

- **Contract typo, S430 URL** (contract §Claim C2, sources bullet): the line reads "`https://www.rfc-editor.org/rfc/rfc6790`… the
  canonical `https://www.rfc-editor.org/rfc/rfc6797.html`". The draft uses `rfc6797.html`; the stray `rfc6790` fragment should be
  struck when the L1 integrates, so the registry row and the Gate line cannot disagree.
- **S001 and S002 each carry two URLs in the registry cell** (S001: two `raw.githubusercontent.com` action blobs; S002: the v4.0.0 and
  v5.0.0 release URLs). C4 requires "receipt URL = row URL", which is not stated for a two-URL row: the fetched URL must be recorded
  before the pin is written, or C4 will fail on an honest fetch. Flagged in the draft's C3 block.
- **S010's row URL carries a fragment** (`…/rfc9110.html#section-8.8`) while S433's is the bare document URL. A fresh GET of S010 is a
  GET of the same document S433 opens this round; the two receipts will differ only by fetch time and userAgent.
- **Census key keeps fragments `[INFERENCE]`**: `controls/census-before.txt` lists S088 (`…/rfc9110.html`) as a W04 duplicate and does
  **not** list S010 (the fragment-bearing row), which is consistent with the duplicate key retaining the fragment; the contract's
  "adds one W04 note with S088, census stays exit 0" therefore holds. Observation is from the committed file; the key rule itself I did
  not read in code (the census implementation is not in `scripts/`).
- **Disclosure coverage is the load-bearing build input for C1's R2** (`receipts=144 … undisclosed=0`). My shadow probe
  (`.files/span_probe.py`, output `.files/span_probe.out.txt`) walks the 144 frozen paths with first-parent `git log`/`git show` and
  applies the contract's result-span *line* regex: **9 of the 144 files have a span-changing commit after their first commit, across 12
  commits** — r52 `c1-mutation-ladder.json` (3), `c2-quote-real.txt` (1), `c1-ledger-real.txt` (1); r54 `c1-selftest.txt` (2); r55
  `after-c2-quote-truth.txt` (1), `after-c1-readme-index.txt` (1); r56 `after-c1-selftally.txt` (1), `after-c2-quote-truth.txt` (1);
  r57 `after-c1-receipt-pins.txt` (1). 16 population files are touched by more than one first-parent commit (`.files/multitouch.txt`);
  the other 5 change only lines outside the span. This is a **shadow of the tool, not the tool**: it does not apply the
  first-committed-version receipt-grammar gate (a file whose first version carries no grammar line is not a receipt) nor the exact
  `pending` rule, so the tool's event count is `[INFERENCE]` to be ≤12. The disclosures registry must cover every event the tool
  counts, or R2's `undisclosed=0` is unreachable; the C1 seat and the L1 should reconcile the number against this list.
- **Build state at this writing** (read-only `git status --porcelain`, `ls`, `sha256sum`): `scripts/response_snapshot.py` is present in
  the lane worktree and untracked — 10,217 bytes, sha256 `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7`, mtime
  `2026-10-27 06:17:14 -0300`, no blob in `HEAD` and no commit history (mistake row 4's ground); `scripts/receipt_lineage.py`,
  `scripts/header_audit.py`, `.ufo/waves/round-61/c61_*` and `.ufo/receipt-disclosures.json` are absent.
  `.ufo/waves/round-61/{capture,recheck}` exist as untracked directories (capture holds the 12 per-surface `response.json`). w1 reports
  on disk: `ExecQuarantine.md`, `ScoutC2Population.md`, `ScribeC1Rows.md`, `SentinelC2Net.md` among others. Seats are therefore writing
  lane files beyond their own report and `.files/` (contract §Round shape says seats are read-only outside those) — not my call,
  recorded because the lesson's fix column depends on which artefacts will exist at the L1 freeze.
- `ExecQuarantine.md` records the quarantine slice at 12 rows, 453 bytes, sha256
  `6d92f4408c7482e59fb93c2085676f7d9c4fedb687bcfd501060f63c15d2d63a`; the draft's Gate line leaves the sha256 as a placeholder so the
  L1 fills it from that report rather than from mine.

## Evidence run (all read-only, none a counter)

- `git show 4cb225f:{…,after-c1-selftally.txt,after-c2-quote-truth.txt,c2-selftest.txt}` and the same at `ad06cb8`; `git show
  31b61a4:…after-c1-receipt-pins.txt` and `20217f2:…` → outcomes above.
- `git merge-base --is-ancestor 1ea3059 9f07731a…` → true (the retained EN body's commit is an ancestor of base).
- `python3 -B .files/units_probe.py <retained en.html>` → `units 22 chars 112 tokens 22`, collapsed-text count 1, raw-byte count 0.
- `python3 -B .files/span_probe.py` → 16 multi-touch files, 9 span-changing files, 12 span-changing commits.
- Row 4 provenance: `grep -c eac57099a6e097 .ufo/waves/round-61/w1/ExecC2Capture.files/run.txt` → 1 (the digest, executor-authored);
  `sha256sum scripts/response_snapshot.py` → `ba107024…`; `git ls-tree HEAD scripts/` → no such path; `git log -- <path>` → empty.
- Row 4 containment, re-run by me: `python3 -c "print(open('.ufo/waves/round-61/w1/SentinelC2Net.files/pre_excerpt.txt').read() in
  open('scripts/response_snapshot.py').read())"` → `True`; same for `pre_excerpt2.txt` → `True` (2,864 and 678 bytes).
- `wc -l .ufo/waves/round-61/controls/population-144.txt` → 144; `grep -n` confirmed the r56/r57 files cited above and
  `round-60/controls/after-c1-gate-status-t1.txt` are inside the frozen population.

## Touched surfaces

- Written: `.ufo/waves/round-61/w1/ScribeLessonMistakes.md` (this report) and
  `.ufo/waves/round-61/w1/ScribeLessonMistakes.files/{lesson.md,units_probe.py,units_probe.out.txt,span_probe.py,span_probe.out.txt,multitouch.txt}`.
  Nothing else in the lane or the fleet root; no git/jj mutation; scratch `/fast/scratch/hyaku/kake-r61/ScribeLessonMistakes` removed.

## Out of scope / not done

- No counter executed, no after-state scored, no tool or registry row written, no lesson landed in `corpus/lessons/` (the L1 lands it),
  no `Gate` quote manufactured, no entry text written.
- Unrun: `c61_lineage_cases.py`, `c61_header_cases.py`, `c61_recheck_pins.py` (absent at this writing); the C2 captures and the C3
  recheck receipts (in flight in sibling seats).
- Tooling: nothing installed or upgraded.
- Not verified: the four C2 bodies against a receipt; whether the census duplicate key strips fragments (inference above).

VERDICT: Drafted the round-61 lesson (97 lines, 4 mistake rows including SentinelC2Net's tool-bytes row under L1 ruling d, C2/C3/assimilation Gate skeleton with real URLs and pins, three carried items) at the assigned `.files/` path, with the mined receipt-rewrite class re-verified from committed receipts and every unobserved value left a placeholder.
