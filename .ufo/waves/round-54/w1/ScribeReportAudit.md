# ScribeReportAudit — round-54 required report/lesson evidence gaps

Seat: `L1Kake54.ScribeReportAudit` (leaf, read-only). Date: 2026-10-25.
Scope: append-only S374 correction, Gate source reopening, mistakes rows,
measurement and source census — as required report/lesson evidence for
round 54. Gaps only. No edits were made; no tools installed.

State audited: `master` tip `8e408e00fbe1c5908df62ba79e78c944bda479e2`
("round-54: repair S374 calibration and settle r53 ops debt"); base
`68228b2d74e7930ae4f07e90e382a0d03ab80c7b`; freeze commit `acae1dc`.
Reproduced counter runs (read-only, `git show` bytes only):

- `python3 -B .ufo/waves/round-54/c54_s374_calib.py --root <lane> --revision 8e408e00…` → `mismatches=0 met=True`, EXIT=0.
- `python3 -B .ufo/waves/round-54/c54_ops_debt.py --root <lane> --revision 8e408e00…` → `registry=absent manifest=present uncovered=0`, EXIT=1.

## Confirmed present (no gap)

- **Append-only S374 correction.** `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
  at `8e408e0` starts with every byte of the base file (prefix check) and the
  appended `**[r54-correction 2026-10-25]**` block quotes the exact source
  substring 「このリンク先のウェブページの巡回を推奨していない」 and uses English
  crawl vocabulary ("not recommend the crawling"); it supersedes without
  rewriting and bounds the claim ("does not assert that the crawler refuses").
  `corpus/QUALITY.md`, `corpus/lessons/round-52.md`, `corpus/lessons/round-53.md`,
  `corpus/lessons/round-53-verifier-spotcheck.md` likewise preserve base bytes.
  SKILL.md/SCORECARD.md diffs are pure line insertions (no prior line altered).
- **Gate source reopening.** `.ufo/waves/round-54/source-reopen.txt` and
  `corpus/lessons/round-54.md` §Gate record URL, access-date 2026-10-25,
  retained body, sha256 `3ad358bd…`, quote-occurrences=1, title — all verified
  against retained `S374.html` (sha matches; quote count 1; title present).
- **Mistakes rows.** `corpus/lessons/round-54.md` §Mistakes has exactly the
  three required rows (S374 qualifier drop; unsettled wave; CJK units-vs-words),
  each with evidence, captured-by and fix columns.
- **Settlement.** `.ufo/waves/round-53/settlement.md` records all seven lost
  names, 40 spawned / 0 committed reports, deaths explicitly unverified;
  role mix verified against `w53-spec.json` (40 items: scout 14, connector 1,
  executor 3, scribe 6, reviewer 8, critic 8). Cited-name coverage is
  `uncovered=0` per the counter.

## Gaps

1. **C2 not met at the measured commit — and no evidence records it.** At
   `8e408e0` the C2 counter reports `registry=absent … EXIT=1`: the SKILL.md
   row `| c53-gate-truth | gate | …` lacks the literal token `read-only`
   required by `REQUIRED` (`c54_ops_debt.py:32`) in its write-scope cell
   ("Normal path reads committed Git blobs only; … neither writes lane
   content"). The tip commit therefore fails its own frozen predicate; no
   lesson, LOG entry, receipt or scorecard line records the C2 failure or the
   missing token. This is the largest evidence hole: the repair commit landed
   without a committed C2 target-run receipt.

2. **No measured-verdict evidence for round 54 anywhere.** The lesson's
   "Round-54 claims" section retains pre-measurement language ("is expected
   to report one mismatch and fail"; "expected to show the absent
   registry/manifest") and ends there; §Wave-measurement section absent.
   `.ufo/waves/round-54/controls/` holds only `base-c1-s374.txt`,
   `base-c2-ops-debt.txt`, `c1-selftest.txt` — no after/target receipts at
   `8e408e0` for either claim (C1's `mismatches=0 met=True` reproduced above is
   recorded nowhere in committed bytes). SCORECARD's calibration row cites
   "1→0" with the counter as pointer but names no measured commit or receipt.

3. **Frozen C1 counter mutated after freeze; undisclosed and base receipt not
   re-run.** Between `acae1dc` and `8e408e0`, `c54_s374_calib.py` changed 32+
   lines (sha `d66b8d48…`→`26b53bc2…`): `EN_CRAWL_RE=\bcrawl\b` replaced by
   `NEGATIVE_CRAWL_RE=\bnot\s+recommend…crawling\b` (strictly harder), suspect
   collection refactored, selftest duplicated-parser path replaced and two
   fixtures (`correction_wrong_polarity`, `correction_before_render`) added;
   `c1-selftest.txt` gained their two receipt lines in the same commit.
   Neither contract, lesson nor LOG discloses the post-freeze counter change or
   identifies which counter revision produced `controls/base-c1-s374.txt`
   (`mismatches=1`); the base control was not re-recorded under the revised
   bytes. Precedent from round 51/52 treats post-score counter edits as
   routed defects requiring disclosure. `c54_ops_debt.py` is unchanged
   (sha `a3bc3119…` both commits).

4. **LOG.md silent for round 54.** AGENTS.md requires a LOG entry with
   motivating evidence per change; LOG.md at tip ends with the round-53
   consideration-boundary entry (`31dc3ef`). No entry for the contract freeze
   (`acae1dc`), the repair/settlement commit (`8e408e0`), the S374 correction,
   the settlement manifest, the SKILL registry row, the QUALITY criteria, or
   the SCORECARD calibration row. Round-53's own lesson route noted that
   landed-hash LOG appends are required; none exist for r54.

5. **No source census receipt for round 54.** No `census-*.txt` or equivalent
   under `.ufo/waves/round-54/`; the lesson records no registry/corpus census
   run (the round-53 pattern committed `census-argv/stdout/exit`). A live
   `node scripts/corpus-contract.mjs` run exits 0 (`0 findings · 43 knowledge
   entries · 49 lane lessons`), but that run is unrecorded in round-54
   evidence. Sources-reopened file exists, but the census leg of "measurement
   and source census" is absent.

6. **CJK re-derivation not evidenced for the measured commit.** Contract
   maintenance item and the new QUALITY criterion require counts re-derived
   "at the measured commit" / "from its exact stored Gate span". The lesson
   restates S367/S372/S373 = 31/27/27 units from the verifier note; the only
   fresh count is S374 = 24 units (consistent with character count of the
   quoted clause). No command, spans, or receipt shows S367/S372/S373
   re-derived at `8e408e0`.

7. **Frozen "plan" predicate surface missing.** Contract line 6 asserts the
   predicate sentence is "the same sentence in the plan, in the counter's
   code, and in every receipt label"; `plans/` contains no round-54 file, so
   the plan-side copy of the sentence is absent from the repo (only contract +
   counters carry it). Receipt labels match the sentence (`ExecC1Base.md`
   reproduces it verbatim).

8. **Spec pair undocumented.** `w1-spec.json` (`maxLanes:32`) vs
   `w1-spec-fixed.json` (`maxLanes:40`) — identical context/items otherwise;
   no provenance note records which is authoritative or why both were
   committed.

## Out of scope / notes

- Wave w1 settlement is in flight; only `ExecC1Base.md` is committed so far.
  Whether other seat reports land is a live-wave matter, not a report/lesson
  evidence gap against the round-54 contract.
- The C2 `registry=absent` is a contract-vs-implementation defect (either the
  row must gain the `read-only` token or `REQUIRED` over-constrains); which
  side is wrong belongs to the C2 attack seats, not this audit.
- No file modifications, no installs (python3, git, node already present);
  pacman untouched per wave bounds.
