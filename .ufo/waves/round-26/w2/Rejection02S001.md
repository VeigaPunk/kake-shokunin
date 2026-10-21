# Rejection02 × S001 — v3.0.1 statements recorded UNVERIFIABLE instead of STALE

Axis: freshness. Milestone: r26-recheck-falsify. Candidate e28312b14b076584fedd696fae2a684e460bd11e (working-tree HEAD), base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006.

**Verdict: DISAGREE for one of the four statements; AGREE for the other three.** The statement at `ghp-served-set.md:21-22` names S001's pinned files as its source, but S001 has never pinned a v3.0.1 file. That attribution was already false at the base revision. Under the round's own rules it is STALE, not UNVERIFIABLE. The content (“v3.0.1 does not” exclude dot paths) still has support from bytes retained this round. That support comes from S002, not S001. The UNVERIFIABLE label therefore hides an attribution error. It also rests on a misleading premise: that no v3.0.1 bytes were retained.

## The rejected or downgraded finding

- Ledger `statements.json:7-15` (S001 pair): `"stale": 0`, `"seatUnverifiable": 4`; l1Disposition: “4 v3.0.1 statements UNVERIFIABLE (recorded in the EOF block).”
- Seat report `w1/PairS001GhpServedSet.md`. Rows 5, 17, 21 and 23 are UNVERIFIABLE because there is “no v3.0.1 text retained”. The flag reads: “v3.0.1 is outside the row's pinned set (SOURCES.md:9 pins v4.0.0 tag and main 5f327015) … Rows 5, 17, 21, 23 need a retained fetch, or the entry must drop the v3.0.1 claims.”
- Corpus EOF note `corpus/knowledge/ghp-served-set.md:89`: “UNVERIFIABLE this round (not STALE): the four upload-pages-artifact v3.0.1 statements. S001 pins only v4.0.0 and main, and no v3.0.1 bytes are retained under round 26”.
- Lesson `corpus/lessons/round-26.md:61-62`: “UNVERIFIABLE: four upload-pages-artifact v3.0.1 statements (no pinned v3.0.1 bytes)”.

## Criteria that apply

- `corpus/QUALITY.md:217`: “STALE means the statement is wrong or unsupported at its own stated scope.”
- `corpus/QUALITY.md:220-221`: “A statement whose attribution was false even at its base revision is STALE.”
- `corpus/QUALITY.md:145-147`: UNVERIFIABLE is the label for “surface gone”. The v3.0.1 surface is not gone. The seat fetched tag v3.0.1 the same day in memory (sha256 `7c93bf9e…`, 2389 B, 0 dot-pattern lines, 3 `.github` lines; PairS001 “Checks and boundaries”). The statement was undecided because its cited row does not cover v3.0.1. The surface itself was reachable.
- Round-26 precedent: the S003 r20-tail attribution was “false even at base cb807bc” and was admitted STALE (`round-26.md:50-51`; corpus EOF `ghp-served-set.md:83`). Its correction re-pointed the claim to the source that actually carries the text. The S001 v3.0.1 attribution belongs to the same class.

## Counterexample (row 17, ghp-served-set.md:21-22)

The statement reads: “S001, pinned `action.yml` Archive steps: v4.0.0 excludes `.[^/]*` in all three OS steps; v3.0.1 does not.”

1. **The attribution was false at base and is still false.** `git show 97404de…:corpus/SOURCES.md` row S001 has scope “action.yml at v4.0.0 and main commit”. Its only URLs are `…/7b1f4a764d45…/action.yml` and `…/5f327015a708…/action.yml`. The same row text appears at the authoring commits 02b6dd0 and 9639ec7 (`git show <c>:corpus/SOURCES.md | grep '^| S001'`), and the candidate leaves it unchanged (the `git diff 97404de e28312b -- corpus/SOURCES.md` output only appends lines 79-80). The entry header (`ghp-served-set.md:1-2`) pins only 7b1f4a7 and 5f327015. In `git grep -n 'v3\.0\.1' 97404de -- corpus`, v3.0.1 shows up only as an unpinned tag in the recheck loops (lines 3 and 40) and in the statements themselves (lines 22, 38 and 41). No pinned S001 file supports the v3.0.1 half of the bullet, so it is unsupported at its own stated scope (QUALITY:217) and its attribution was false at base (QUALITY:220-221).
2. **One possible defence fails.** The defence would read “S001” as the action.yml family and “pinned” as loose wording. However, the registry row is the authority for what S001 covers, and the seat itself states that v3.0.1 “is outside the row's pinned set”. The S003 precedent was decided against the cited target's actual content, not against a generous reading of its label.
3. **The premise “no v3.0.1 bytes retained” is misleading.** Retained round-26 bytes do speak to v3.0.1. `fetched/S002-1.raw.gz` is the v4.0.0 release page (manifest.json:41-58, fetchedAt 2026-10-21T15:09:32Z). Its sha256 `455adcec328f88362641c1d533e1c7a65c46d5120f8ebe2d55b7dc5eaca6334f`, recomputed via `zcat | sha256sum`, equals manifest.json:56. Its text view `fetched/text/S002-1.txt:1` contains:
   - “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact”
   - “Full Changelog: v3.0.1...v4.0.0”

   v4.0.0 is therefore the release directly after v3.0.1, and dotfile exclusion arrived in v4.0.0. That supports “v3.0.1 does not” exclude dot paths from bytes retained this round, but through S002, not S001. So the statement's content is not undecidable. The decidable defect is the attribution, which is the STALE class.
4. **The UNVERIFIABLE label has an effect.** It requires no `[r26-recheck S001 STALE]` correction (`measure.py:425-452` counts only ledger `stale` against tags; `seatUnverifiable` is ignored). So the entry keeps an S001 attribution that the round's own rules classify as stale. The EOF note at line 89 then tells the next reader that the claim “remain[s] historical … until a pinned v3.0.1 source is opened”. That is a false-provenance outcome.

## Where I agree (rows 5, 21 and 23)

- **Row 5 (`ghp-served-set.md:3`, recheck loop including v3.0.1):** this is a replay instruction, not a factual claim. It names its own URL template and can still be run. It is not STALE.
- **Rows 21 and 23 (`ghp-served-set.md:38-41`, “Rechecks (2026-10-19) … returned `v3.0.1 0` … `v3.0.1 3`”):** these are dated records of a command's output. They are historical observations with an explicit date. QUALITY:218-220 treats historical dates and records as notes, not stale claims. No retained round-26 byte contradicts them; the seat's unretained same-day GET is consistent with them. For the `.github` count of 3, no retained round-26 byte bears on it either way. UNVERIFIABLE (or a note) is correct for these rows.

## Smallest safe correction

1. In `statements.json`, S001 pair: set `"stale": 1` and `"seatUnverifiable": 3`. Amend l1Disposition to admit row 17 as a STALE attribution and keep rows 5, 21 and 23 UNVERIFIABLE.
2. Append one EOF block to `corpus/knowledge/ghp-served-set.md` without changing any original line, for example:
   `[r26-recheck S001 STALE] The S001 bullet at lines 21-22 attributes “v3.0.1 does not” (exclude .[^/]*) to S001's pinned action.yml, but S001 pins only v4.0.0 (7b1f4a7) and main (5f327015); false at base. The v3.0.1→v4.0.0 change is S002's own text (v4.0.0 release, re-fetched 2026-10-21): “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact” and “Full Changelog: v3.0.1...v4.0.0”. Evidence: w2/Rejection02S001.md.`
3. Change the line-89 EOF note from “four” to “three” (the recheck command and the two dated loop outputs). Replace “no v3.0.1 bytes are retained” with “no v3.0.1 action.yml bytes are retained”.
4. In `corpus/lessons/round-26.md:47-62`, change the admitted count from 8 to 9 and the UNVERIFIABLE count from four to three. Rerun `measure.py` on the corrected revision. The expected result is 9 statement corrections out of 9 STALE.

Impacted axes: freshness (statement provenance and staleness count) and, secondarily, adjudication consistency with the admitted S003 attribution precedent. No row-level verdict changes: S001 stays HOLD.

## Checks and boundaries

- Read-only commands: `git rev-parse HEAD`, `git show <rev>:corpus/SOURCES.md`, `git grep` / `git log` / `git diff` at 97404de and e28312b, `grep`/`sed`/`zcat | sha256sum` over the retained files under `.ufo/waves/round-26/fetched/`. No network GET (the v3.0.1 URL is not in SOURCES.md, so it was not fetched).
- Nothing installed or updated. Nothing was written except this report. No /tmp, delegation or round-24 material.

```json
{"target":"S001 v3.0.1 UNVERIFIABLE disposition (statements.json S001; ghp-served-set.md:21-22,89)","verdict":"DISAGREE","severity":"medium"}
```
