# FalsifyDebt — wave-2 critic report (C1, operability)

Seat: critic, wave 2 (post-integration falsification), read-only except this
report. Candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` vs base
`7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Scope: attack C1 evidence on the
debt axis — r21 carried reds must be unchanged, and nothing may promote
anchor-census (or any helper) to a gate, relabel reds, or touch protected
bytes. Ran the two bounded counters the contract names; no builds/tests/lint.

## Verdict

**No counterexample found that rejects C1.** All four routed debts are carried
unchanged at the measured tip; no gate promotion, no relabel, no protected-byte
edit. Bounded acceptance with one observation and two wording nits below.

## Counter 1 — paths gate re-run at candidate tip

`TZ=UTC node scripts/freshness-sweep.mjs --section=paths` (2026-10-20, node
v24.21.0, live tree = candidate + wave-2 artifacts):

- Real exit **1**; `VERDICT: DRIFT — §paths: 3 unannotated miss · 0 NOT in
  pins.pathsMissSet`.
- The three drift targets and four unannotated locations are **identical** to
  the r21 receipt (`paths-after.json`): `~/Projects/plazir-15-site`
  (drift-detection.md:77, fleet-registry.md:57 — post-prefix coordinates),
  `~/Projects/webzites/bin/webzites.mjs` (free-read-verbs.md:321),
  `~/Projects/webzites/scripts/kimi-surface.mjs`
  (round-6-aggregator-audit.md:48).
- `missSet 55`, `set-delta miss: no new miss` — the candidate added no new
  unannotated miss despite adding corpus text. filesScanned grew 50→53 (the
  three cited r22 files) and resolve 5→9; both are expected population growth,
  not debt movement. Unresolved list is the same 9 tokens as the r21 receipt.

Contract debt sentence ("three targets/four legacy locations missSet55")
remains literally true at the tip. No falsification.

## Counter 2 — anchor-census re-run at candidate tip

`node .ufo/waves/round-21/anchor-census.mjs` → real exit **1**, `ok:false`.
Summary: targets 39 (37+2 new r22 corpus files), `violations: 0`,
`preserved:true` on every audited target (prefix/suffix-only or same bytes),
references 7068, `mismatches: 283`.

- **Growth, not damage:** the 78→283 mismatch increase comes from new
  `.ufo/` wave artifacts and new corpus files citing targets past their
  r21-base extent — the same `out-of-range`/`target-not-at-base`
  baseline-inapplicable class. Sampled record confirms `type: out-of-range`,
  source `.ufo/waves/round-21/anchors-fixed.json:9`.
- `violations: 0` re-confirms **no old corpus byte was touched**, which is
  also what `git diff` shows independently (below).
- **Observation (not a defect):** "anchor-census78" is the frozen r21 routed
  figure. The live diagnostic count is now 283 and will keep drifting upward
  as wave artifacts accumulate. Contract text correctly says "not a gate,"
  and every candidate mention (`SKILL.md` r22 section, `QUALITY.md:89-91`,
  `round-22.md:71-73`) says "not a gate / evidence helper" — no promotion
  found. Only risk is a reader quoting "78" as the current count; candidate
  text always frames it as the r21 run's number, so no correction required.

## Static checks (git diff base..c0fd6d5)

- **Modified files: exactly six**, all append/register edits: `LOG.md`,
  `PROVINCE.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `corpus/SOURCES.md`. New files: `scripts/canonical_audit.py`, the r22
  wave dir, `corpus/knowledge/static-canonical-preflight.md`,
  `corpus/lessons/round-22.md`.
- **Protected bytes untouched:** zero diff on
  `corpus/lessons/round-{4,9,16,21}.md`, `round-21-verifier-spotcheck.md`,
  all `*-aggregator-*` lessons, all pre-existing `corpus/knowledge/*.md`,
  `.ufo/waves/round-21/*` receipts, `freshness-sweep.mjs`, and
  `freshness-pins.json` (not in the diff at all). Debt clause holds.
- **SHONEN:** `SHONEN.md` and `SCORECARD.md` not in the diff; all four boxes
  still `- [ ]` at tip. `grep` over committed r22 surfaces finds no `[x]`,
  promotion claim, or "paths gate clean/resolved" phrasing — only negated
  carries ("remains red", "not a gate", "no promotion is claimed",
  `LOG.md` "old paths gate reds … are not relabelled as new improvements").
- **Chronology debt:** old Gates at round-4:50 / round-9:185 / round-16:171
  untouched; `QUALITY.md` r22 bullet keeps them "superseded only by
  round21's existing register." Correct disposition.
- **r21 register figures quoted in `round-22.md:69-70` are accurate**
  (C1 4/21→21/21 provenance trios; C2 1/15→15/15 baseline gates, 16/16
  current) — verified against `round-21.md:152-162` and the fleet report.
- **Validator purity:** `canonical_audit.py` contains no paths/missSet/
  anchor/freshness/SHONEN surface keys; output schema is contract-only.
- `measure-after.json`: two deterministic runs at `c0fd6d5`, both
  `accepted 32, total 32, available true` (per-case audit is the counting
  seat's scope, not mine).

## Wording nits (advisory, do not block)

1. `round-22.md:73` says "SHONEN not independently checkable"; contract says
   "no SHONEN promotion", and `:75` says files "not writable here" (a
   permission) rather than "no byte edited" (the record). Softer than the
   contract but not false — InheritedDebt.md defect 2 flagged this pre-land
   and it landed as-is.
2. `corpus/QUALITY.md` grounding now reads "routed notes 1–4" and a SHONEN
   bullet exists — the wave-1 grounding defect was fixed before integration.

## Required correction / bounded acceptance

**None required.** Accept bounded: debts carried verbatim, helper stays
non-gate, protected bytes proven intact by both `git diff` and a live
`violations: 0` census. For L1's closure notes only: when citing the anchor
census, use "r21 run recorded 78 baseline-inapplicable diagnostics; tip run
shows 283, all same-class, violations 0" so the frozen figure is never read
as the live count.

Tools installed: none (node/python3/git already present; pacman paused).
