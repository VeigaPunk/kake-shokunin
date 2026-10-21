# Rejection10S021: attack on L1's rejection of S021 row 6 (fragment wording)

Critic: KakeR26-2.Rejection10S021 (leaf, author-side FALSIFY). Axis: freshness. Milestone r26-recheck-falsify.
Candidate e28312b14b076584fedd696fae2a684e460bd11e, base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006.

## Verdict: DISAGREE (low)

The rejection hides a real STALE in the ledger, but not in the corpus. Line 21 of
`corpus/knowledge/static-canonical-preflight.md` is wrong at its own stated scope, both against the
2026-10-21 bytes and at base. Round 26's own STALE rule does not exempt a statement just because an
earlier correction already covers it. The same ledger also applies the opposite standard to the
identical skill-tail case. A reader of the corpus still reaches the correct text: the base has the
r23 tail, and the candidate's r26 tail points to it. So the impact is a misclassification and an
undercount in the ledger and in the lessons. No live staleness is hidden from readers.

## Counterexample

The entry says, at line 21 (identical at base and candidate, `git show 97404de:` and `git show e28312b:` lines 20-21):

> Its “Best practices” rejects fragment canonicals and explains that JavaScript may affect the signal.

The retained bytes (`fetched/text/S021-1.txt`, sha256 1e77f156…b792) have exactly one fragment passage, at offset 9949:

> Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.

The retained text has zero occurrences of `reject` or `Reject`. The statement credits Google's
"Best practices" with an outcome, "rejects", that the page does not state. That makes it wrong at its
own stated scope.

## Evidence that the rejection breaks round-26's rule

1. **The rule has no "already governed" exemption.** The ledger rule
   (`statements.json` `.rule`) says: "STALE = the statement is wrong or unsupported at its own stated
   scope against the 2026-10-21 bytes (content, attribution, quote fidelity, version semantics).
   Historical dates and base-scoped pointers are not stale." `corpus/QUALITY.md:216-221` lists the
   only exemptions: a historical verified-at date, a pointer explicitly scoped to a base revision,
   and a patch-version label. It adds: "A statement whose attribution was false even at its base
   revision is STALE." Line 21 is none of the exempt kinds. Its attribution was already false at
   base: the base itself carries `[r23-correction] "rejects fragment canonicals" overstates S021`
   (lines 140-142). `git log -S` shows line 21 came from c0fd6d5 (round 22) and the correction from
   83098b5 (round 23).
2. **The round-21 coordinate rule does not apply.** `QUALITY.md:69-73` maps pre-round-21 literal
   pointers into entries with the four-line prefix. Line 21 is a content claim, not a pointer, and
   it dates from round 22. The rejections for S001, S005, S011, S012 and S013 rest on this rule.
   S021 row 6 cannot.
3. **The same ledger uses the opposite standard elsewhere.** `statements.json` `.skillTails` reads
   `{"statements": 11, "hold": 7, "staleAlreadyCorrected": 4, "note": "the 4 STALE base clauses
   already carry appended r20-correction tails that re-verify; no new correction"}`.
   `w1/SkillTailsCitingSources.md:15` says: "Each base clause is wrong today. Each sits on a line
   whose appended `r20-correction` tail already states the correction". This is the same situation
   as S021 row 6: a wrong base clause plus an earlier tail that re-verifies. There it is counted
   STALE (already corrected). For S021 it is counted as not stale.
4. **The lessons file records it as a false finding.** `corpus/lessons/round-26.md:47-48` says
   "seats proposed 22 STALE, L1 admitted 8 and rejected 14". `:60` lists "S021 fragment wording —
   already governed by the r23 correction" under **Rejected**, next to genuinely non-stale items
   (date stamps, base-scoped pointers). The seat's finding was correct. It was a duplicate of an
   existing correction, not a wrong finding.

## Why the corpus is not hiding it (this caps severity)

- The candidate's S021 tail (`git diff 97404de e28312b`, the `[r26-recheck S021 STALE]` bullet) says:
  "The fragment wording at line 21 remains governed by the existing [r23-correction] at lines
  140-142." At e28312b, lines 140-142 are still the r23 correction because the r26 block is appended
  at EOF, so this current-coordinate pointer is correct.
- The r23 correction holds against the 2026-10-21 bytes. It says Google "generally does not support
  fragment canonicals", while the page says "generally doesn't support URL fragments" and "Don't
  specify a URL fragment as canonical". The paraphrase is faithful.
- The page version is unchanged: the manifest last-modified is Fri, 10 Jul 2026 10:12:15 GMT, and
  the footer reads "Last updated 2026-07-10 UTC". Row receipt `rechecks/S021.json` HOLD is about the
  row's teaches (head placement, absolute vs relative, signal not guarantee). Row 6 does not touch
  those, so the row-level HOLD is unaffected.

## Impacted axes

- freshness: the per-statement STALE census undercounts by one, and L1 rejected a correct seat
  finding. Corpus reader-facing freshness is intact.

## Smallest safe correction

Count row 6 as STALE but already corrected, with no new corpus text, mirroring `skillTails`:

- In `statements.json` pair S021, keep `"stale": 1`. The single `[r26-recheck S021 STALE]` tag stays
  the only new correction, so the counter's tag check (`measure.py:450-454`) still passes. Add
  `"staleAlreadyCorrected": 1`; `field()` at `measure.py:187-188` tolerates extra keys. Reword
  `l1Disposition` to "row 6 STALE, already corrected by the existing [r23-correction] at lines
  140-142 (no new tag)".
- In `corpus/lessons/round-26.md:47-48,60`, move "S021 fragment wording" out of **Rejected** into an
  "already corrected (r23 tail)" class, and change the counts to "rejected 13, 1 already corrected".

Do not raise `stale` to 2 without adding a second tagged bullet: the counter would then fail with
`statement_correction_absent` (1 tag vs 2).

## Commands exercised (read-only)

- `git show 97404de:corpus/knowledge/static-canonical-preflight.md` (lines 1-35, 135-160);
  `git diff 97404de e28312b -- <entry>`; `git show e28312b:<entry> | sed -n '20,21p;140,142p'` →
  line 21 and the r23 tail unchanged; tag count `[r26-recheck S021 STALE]` = 1.
- `git log -S'rejects fragment canonicals'` → 83098b5, c0fd6d5.
- In-memory Python search of `fetched/text/S021-1.txt` for `fragment|reject|generally doesn` →
  fragment at 9949 and 10012 (same sentence), `reject` 0 hits.
- `sha256sum fetched/text/S021-1.txt` → 1e77f15623098db427757be742464d7d244adb17e0cbcffb0503638de353b792.
- Read: `statements.json` (rule, pairs, skillTails), `w1/PairS021StaticCanonicalPrefl.md`,
  `w1/SkillTailsCitingSources.md`, `round-23/w1/ReopenGoogleCanonical.md` P3, `QUALITY.md:43-84,
  207-224`, `lessons/round-26.md:40-75`, `measure.py:420-454`, `contract*.json` STALE clauses.
- No network GET, no builds or tests, no writes other than this report. No round-24 material.
- Tool installs or updates: none.

Report: .ufo/waves/round-26/w2/Rejection10S021.md

```json
{"target":"S021 row 6 L1 rejection (static-canonical-preflight.md:21 fragment wording)","verdict":"DISAGREE","severity":"low"}
```
