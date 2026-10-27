# ScribeLessonMistakes

Frontier step: draft `corpus/lessons/round-59.md` `## Mistakes` (two rows) and the matching
`corpus/QUALITY.md` `## Round-59 criteria` block. Read: `round-58-verifier-spotcheck.md` §6 (D1–D3),
`round-51`/`round-55`/`round-58` spot-checks, `round-58.md` §Mistakes, `QUALITY.md` tail (ends at
`## Round-58 criteria`, line 1315), fleet `CORPUS.md:171-178` (row format + class vocabulary),
round-59 `controls/base-c1-axis-evidence.txt`, `controls/base-c3-quote-truth.txt`.

Touched surfaces: this report only. No lane file, QUALITY.md, lesson file, index or jj state edited.
Provenance: base `fd6303ce5c14b3f892dec586297a942ab6e4193b`; lane HEAD at write time
`cb685273cc9e331b51f45485793d5d1c91184b3a`; counters run from their committed blobs at that HEAD
(`git status --porcelain .ufo/waves/round-59/` shows untracked-only entries: `w1/`, `w1.ready`,
`w1.ready.partial`, `validate_append.sh`). Scratch `/fast/scratch/hyaku/kake-r59/ScribeLessonMistakes`
(no clone needed; both counters read the lane tree read-only). Tools installed: none.

## MISTAKES:

CORPUS.md format: class · evidence pointer · captured-by · fix. Append rows below `round-58.md`'s four
rows (`round-58.md:109-115`); the third column names the `QUALITY.md` criterion or protocol rule that
should have caught the mistake, or `none`.

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| survivor | `corpus/knowledge/crawler-identity.md:31` reads verbatim in the base blob (`git show fd6303ce:corpus/knowledge/crawler-identity.md \| sed -n '31p'` → `- **A user-agent string is the only thing a server log records about the crawler.** Two`). It landed at `5591557` (2026-10-24, round 51, `git log -S'only thing a server log'` names that one commit) and was carried unrepaired through **N = 7** closure passes: the spot-checks of rounds 51–57 never list it (`grep -n 'crawler-identity' corpus/lessons/round-5[1-8]-verifier-spotcheck.md` hits only `51:68`, `51:98` — both the S262/S263 admit — and `55:30`, the "Smartphone and Desktop" row check; no routed-defect entry in `51:§6`'s ten items). The round-58 closure names it `D1` and calls it "carried since round 51" (`round-58-verifier-spotcheck.md:80`) yet repairs nothing, so counting the routing round gives 8 rounds of standing text. Repair state at base: `grep -c 'r59-correction'` = 0, `grep -c 'S425'` = 0 on that blob. | none: no gate reads the age of a routed defect. `QUALITY.md`'s routed-defect family only accepts a pointer to the routing item (`:301`, `:488`, `:505`) or labels debt without ageing it (`:399` "carried as open debt, not a pass"); `SKILL.md` records closures ("Round 52 gate registry additions (r51 closure routed defect 1)", `:1206`) and disclosures ("routed defect D3 of the round-57 spot-check", `:1288`) but holds no open-defect ledger with a round column. A defect named once is never re-read. | Claim C3 condition `C9_stale_claim_corrected` (`c59_quote_truth.py`): an append-only `[r59-correction 2026-10-27]` line within 8 base lines of the sentence, citing S425, inside the retained-body check. Red-before: `controls/base-c3-quote-truth.txt` `0/9 met=False`, C9 FAIL with all three sub-reasons; re-run by this seat, identical (see RED-BEFORE). |
| reference-drift | `SCORECARD.md` axis table at base `fd6303ce` cites bytes the lane does not hold, and both cells keep score 10: operability (`sed -n '17p'`) pins `cli.mjs:935` plus three bare continuations `:836-839`, `:932`, `:393` in a source tree the lane no longer holds; freshness (`sed -n '18p'`) points at six `/tmp/kake-r17/…` files (`scout-claims.md`, `claims-delta.tsv`, `critic.md`, `reviewer-cites.md`, `scout-pins.md`, `scout-live.md` — `ls -d /tmp/kake-r17` → "No such file or directory") and the vanished `corpus/claims` (`ls corpus/claims` → absent). "Last change" still reads `round 12` / `17`; the ratifying prose calls the ratings "legacy round-17/18 assessments". Counter: `C1 axis-evidence mismatches=16 unresolved=11 rows_no_receipt=3 rows_no_tally=2 cross-check scores_held=2 superseded_kept=0`. | prompt §7.5 (`.ufo/prompts/kake-round-59.md:625`: "A `/tmp` path is therefore never citable evidence (QUALITY-class defect, as kotodama Q14 already rules)"; kotodama Q14 = "no /tmp pointers", `.ufo/reports/round-34/kumitate.md:75`) and the lane's own `QUALITY.md:607` round-34 criterion ("A cited artifact resolves from committed lane bytes, not a seat's sandbox … A `/fast/scratch/...` or `/tmp/...` path stands beside that path as provenance, never as the only pointer"), plus `QUALITY.md:128`. Every one of these was written after the cells, and none was ever applied to `SCORECARD.md`: the table is the one surface no criterion scans. | Claim C1 (`c59_axis_evidence.py`): each cell names only committed paths at the scored revision, at least one on-axis receipt, at least one tally found in a cited blob; operability/freshness scores unchanged; the three base cells kept verbatim. Red-before 16 mismatches (`controls/base-c1-axis-evidence.txt`, re-run by this seat, identical). |

Count note for row 1, so the number is auditable rather than asserted: the seven unrepaired passes are
rounds 51, 52, 53, 54, 55, 56, 57 (each spot-check present under `corpus/lessons/`, none listing the
sentence); round 58 is the eighth pass and is where it is finally named; the round-59 base still
carries it. The assignment's instruction is to count from the spot-checks, so **N = 7** is the number
to print, with "r58 routed, r59 base still red" as the continuation.

## QUALITY:

Exact append text for `corpus/QUALITY.md`, after `## Round-58 criteria` (file ends line 1315).
House style kept: bold leading sentence, mechanism, grounding, falsifier, one example that fails.

```markdown
## Round-59 criteria

- **A routed defect carries its age, and the round that closes it names the rounds it survived.**
  A defect a non-author closure routes enters the lane's own record with the round it was routed in
  and the round it was closed in; until then every later round re-reads it. `crawler-identity.md:31`
  ("A user-agent string is the only thing a server log records about the crawler") landed at
  `5591557` in round 51 and stood through seven closure passes (rounds 51–57 name it nowhere; the
  round-58 closure lists it as D1, "carried since round 51", and repairs nothing), while the
  lane's own DNS-verification material sat beside it. Grounding: `corpus/lessons/round-58.md`
  §Mistakes (survivor); `corpus/lessons/round-58-verifier-spotcheck.md:80`;
  `.ufo/waves/round-59/controls/base-c3-quote-truth.txt` (`0/9`, `C9_stale_claim_corrected FAIL`).
  Falsifier: `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision <tip>` must print
  `9/9 met=True` with `C9_stale_claim_corrected` PASS, and C9 fails on three independent sub-reasons
  (no `[r59-correction 2026-10-27]` line within 8 base lines, no S425 citation, no retained body).
  Example that fails it: a correction appended in the entry's own section, marked "corrected
  (round 59)" with no S425 id — the sentence stands, the record of standing does not exist, and the
  next closure re-routes the same line.
- **An axis-table evidence cell resolves, at the revision the row is claimed at, to committed bytes
  and to a receipt on that same axis whose tally exists in a cited blob.** Scores are not evidence:
  a cell that keeps its 10 while its pointers rot is a stale-premise, and a receipt from a round
  with no claim on the axis is not on-axis evidence. At the round-59 base the operability cell pinned
  `cli.mjs:935` and three continuations in a tree the lane no longer holds and the freshness cell
  pinned six deleted `/tmp/kake-r17/…` files plus the vanished `corpus/claims`, under scores of 10
  (`mismatches=16 unresolved=11 rows_no_receipt=3 rows_no_tally=2`). Grounding:
  `corpus/lessons/round-58.md` §Mistakes (reference-drift); `.ufo/prompts/kake-round-59.md` §7.5;
  `corpus/QUALITY.md` round-34 ("a cited artifact resolves from committed lane bytes");
  `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` (exit 1). Falsifier:
  `python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root . --revision <tip>` must print
  `mismatches=0 rows=3 scores_held=2 superseded_kept=3 met=True`; the counter also fails an emptied
  cell (`rows_no_receipt`, `rows_no_tally`), an off-axis receipt (`receipts_off_axis`) and a dropped
  verbatim base cell (`superseded_kept`). Example that fails it: replacing the freshness cell's
  `/tmp/kake-r17/*` pointers with `/fast/scratch/<seat>/reviewer-cites.md` — the row still reads 10,
  and the pointer dies with the seat's scratch dir exactly as the old one did.
```

## RED-BEFORE:

Both commands run by this seat, read-only, from `cd /fast/scratch/hyaku/kake-r59/ScribeLessonMistakes`,
against the lane tree and the base revision; both reproduce their committed controls byte-for-byte in
every number quoted below (receipt parity, not conformance scoring; no after-state measured).

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_axis_evidence.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision fd6303ce5c14b3f892dec586297a942ab6e4193b
```
```
C1 axis-evidence mismatches=16 unresolved=11 rows_no_receipt=3 receipts_off_axis=0 tallies_unfound=0 rows_no_tally=2 rows=3 scores_held=2 superseded_kept=0 met=False  (met: mismatches == 0 AND rows == 3 AND scores_held == 2 AND superseded_kept == 3)
  operability: pointers=5 unresolved=4 tallies=[]
    - cli.mjs:935: not a committed path at the revision
    - :836-839: line pointer with no preceding resolved file
    - :932: line pointer with no preceding resolved file
    - :393: line pointer with no preceding resolved file
  freshness: pointers=10 unresolved=7 tallies=[{'tally': '117/117', 'found': True}, {'tally': '15/15', 'found': True}, {'tally': '16/16', 'found': True}, {'tally': '10/10', 'found': True}]
    - corpus/claims: not a committed path at the revision
    - /tmp/kake-r17/scout-claims.md: absolute or home path (not committed bytes)
    - /tmp/kake-r17/claims-delta.tsv: absolute or home path (not committed bytes)
    - /tmp/kake-r17/critic.md: absolute or home path (not committed bytes)
    - /tmp/kake-r17/reviewer-cites.md: absolute or home path (not committed bytes)
    - /tmp/kake-r17/scout-pins.md: absolute or home path (not committed bytes)
    - /tmp/kake-r17/scout-live.md: absolute or home path (not committed bytes)
  calibration: pointers=0 unresolved=0 tallies=[]
  revision: fd6303ce5c14b3f892dec586297a942ab6e4193b
  base: fd6303ce5c14b3f892dec586297a942ab6e4193b
EXIT=1
```

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_quote_truth.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision fd6303ce5c14b3f892dec586297a942ab6e4193b
```
```
C3 quote-truth 0/9 met=False  (met: conditions_passed == 9 of 9)
  ...
  C9_stale_claim_corrected FAIL
    - no inserted line within 8 base lines after the stale sentence carries [r59-correction 2026-10-27]
    - the inserted correction does not cite S425
    - S425 retained body unavailable
  revision: fd6303ce5c14b3f892dec586297a942ab6e4193b
EXIT=1
```
(`...` in the C3 output is this report's elision; C1–C8 in that block are the pre-landing absences —
entry, row, body and receipt all absent at base — and are quoted in full in
`.ufo/waves/round-59/controls/base-c3-quote-truth.txt`.)

## OPEN:

1. **N for row 1 is a counting choice, not a measurement gap.** Seven closure passes (r51–r57) never
   list the sentence; r58 lists it and repairs nothing; r59 base is red. I print N = 7 per the
   assignment's "count from the spot-checks" and record the r58/r59 continuation in the row; if the
   integrator prefers the inclusive count (r51→r58 = 8), the row's audit trail already supports it and
   only the printed number changes.
2. **Both `QUALITY:` and `MISTAKES:` are drafts here, not landings.** A leaf seat writes no lane file;
   the block is formatted to paste after `## Round-58 criteria` (`corpus/QUALITY.md:1315`) and the rows
   to append after `round-58.md:115`. Heading level, bold lead, Grounding/Falsifier/example shape match
   round-57/58.
3. **Counters are version 1 and under wave-1 attack.** My red-before runs used the counter blobs
   committed at lane HEAD `cb68527` (working tree shows no modification to them). If wave 1 lands a
   version 2 with new conditions, the criterion texts' falsifier lines and pass counts must be re-read
   against version 2; no after-state was measured or scored here.
4. **`captured-by: none` in row 1 is a negative finding from inspection**, not a proof over the whole
   fleet: I searched `corpus/QUALITY.md` (routed/age/unrepaired), `SKILL.md` (defect rows) and the
   round-51..58 spot-checks. A fleet-wide gate that ages routed defects under another lane's record
   would upgrade that cell to a named criterion.
5. **Not run:** nothing else. No live fetch, no clone, no fixture repo, no mutation of any counter or
   corpus file; `round-59.md` and `QUALITY.md` untouched. The `/tmp/kake-r17` and `corpus/claims`
   absences were confirmed on this host today, so the freshness cell's evidence is unrecoverable, not
   merely unresolved.

VERDICT: Two mistake rows drafted (survivor: routed defect carried 7 rounds, captured-by none; reference-drift: axis cells citing /tmp and a removed tree under score 10) with two matching QUALITY criteria, both red-before states reproduced by this seat (16 mismatches; 0/9, C9 FAIL) from committed counter bytes.
