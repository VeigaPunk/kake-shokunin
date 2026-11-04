# kake round 78 — frozen contract (attempt 1)

Frozen before any seat ran, 2026-11-03. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`;
base `fe50945399a386b48678b1f2051fdbe8a77b10bd` (lane `master` tip at round open).
Shape: ONE v1 wave `w1`, 14 seats (L1 holds the planner seat). Scores before the
round: operability 10, freshness 10, calibration 2 — all HOLD, no scalar move claimed.

Claims: three, one axis each. C1 works the lane's lowest non-retired axis
(calibration 2; the stagnation nudge does not apply because calibration sits below
the lane's saturation line).

---

## C1 — calibration: the SHONEN ledger records the population it measured, and every
## recorded observation is graded by its measure's own shape

Predicate (frozen): `met <=> rows_with_population == 4 and stale_populations == 0 and
exact_mismatches == 0 and floor_violations == 0`.

- `rows_with_population` — ledger rows (at the revision) carrying a `population` object.
- `stale_populations` — declared population ≠ the population re-derived from the tree at
  the same revision (`git ls-tree`).
- `exact_mismatches` — round-77 counter findings that are not `observation-differs`, plus
  `observation-differs` on any check whose kind is not `count_at_least`.
- `floor_violations` — `observation-differs` on a `count_at_least` check where the
  re-derived value is **below** the recorded one. Growth is not drift: this lane's own
  standing rule (SKILL.md, freshness sweep section) says counts that grow with the corpus
  are floors or dated measurements, never constants. Shrinkage is drift.

Counter: `python3 -B .ufo/waves/round-78/c78_shonen_population.py --root . --revision <rev>`
(exit 0 met · 1 measured defect · 2 unevaluable · 64 usage). Selftest:
`--selftest --work <scratch>` → 9/9.

Base receipt `.ufo/waves/round-78/controls/base-c1-population.txt` (exit 1):
`rows_with_population=0 undeclared=4 stale_populations=0 exact_mismatches=0 floor_violations=0 growth_tolerated=2 met=false`.

Cheapest control that skips the work (`controls/ctl-c1-note-only.txt`, exit 1): edit the
box-4 prose note 63 → 64 with a green c77 stub; the predicate stays red
(`rows_with_population=0 undeclared=4 met=false`). A counter that met this control would
be wrong; this one rejects it.

Deliverables: `corpus/knowledge/shonen-ledger.json` gains a `population` object per row
and current recorded values; `SHONEN.md` box lines state the population the ledger
re-derives (not the stale 63); `corpus/lessons/round-78.md` records the class.

Not claimed: any change to a box's verdict (box 2 stays a `gap` — its one absent
LOG-named receipt is a real defect and the withdrawal bullets in LOG.md do not resolve
it); any promotion.

## C2 — freshness: the standing offline sweep's evaluated §paths section goes green,
## with the gate provably not loosened

Predicate (frozen): `met <=> sweep_exit == 0 and drift == 0 and new_missing == 0 and
paths_ok and control_exit == 1 and control_drift >= 1`.

Counter: `python3 -B .ufo/waves/round-78/c78_sweep_truth.py --root . --revision <rev> --work <scratch>`
(exit 0 met · 1 measured defect · 2 unevaluable · 64 usage). Selftest: 6/6.
It runs `node scripts/freshness-sweep.mjs --offline --json`, then plants one unannotated
citation of an absent target in a scratch copy of the revision and requires the sweep to
come back red there — a repair that silences the gate fails its own control.

Base receipt `.ufo/waves/round-78/controls/base-c2-sweep.txt` (exit 1):
`C2v1 revision=fe509453… sweep_exit=1 drift=1 new_missing=1 paths_ok=false skipped=2
control_exit=1 control_drift=2 met=false`.

Cheapest control that skips the work (`controls/ctl-c2-pin-only.txt`): pin `~/projects`
into `pins.pathsMissSet` and leave every citation unannotated → `drift=1 newMissing=0
paths_ok=false`, exit 1. Pinning alone is not a repair.

Declared scope: OFFLINE. §armed remote checks are skipped and §history is suspended by
pin; neither is a pass and neither is claimed. The claim is the evaluated §paths section.

Deliverables: dated absence annotations on every unannotated `~/projects` citation at the
measured revision; `~/projects` absorbed into `pins.pathsMissSet`; the sweep's own
`--selftest` stays 36/36.

## C3 — operability (capability acquisition): an offline audit of page-level robots
## meta directives

Predicate (frozen): `met <=> cases == decided and correct == cases and constants_failed == 4`
over the frozen case set, where `correct` compares the tool's finding-id set **and** exit
code against each case's `expect.json`.

Counter: `python3 -B .ufo/waves/round-78/c78_meta_robots_matrix.py --root . --tool-revision <rev>
--cases .ufo/waves/round-78/cases --consts .ufo/waves/round-78/consts --work <scratch>`.
Base receipt `.ufo/waves/round-78/controls/base-c3-absent.txt`: the tool does not exist at
the base (`git cat-file -e` rc=128), so no case is decided.

Cheapest control that skips the work: the matrix's own constants. Four degenerate
implementations (always-clean, report-every-id, empty-findings-with-real-exits, a naive
`substring noindex` reader) must each fail at least one case; a matrix that accepts one
is not decisive.

### Frozen tool contract — `scripts/meta_robots_audit.py`

Manifest `kake-meta-robots-manifest/v1`:
`{"schema": "...", "agents": ["robots", ...] (optional, default ["robots"]),
"checks": [{"id", "path" (lane-relative HTML), "url",
"expect": {"effective": [...], "findings": [...]}}]}`.

- Reads the named local HTML file only; no fetch, no browser, no write.
- Collects `<meta name=… content=…>` whose `name` ASCII-case-insensitively equals one of
  `agents`. A matching element outside `<head>` is reported as
  `meta_robots_tag_outside_head` and does not join the effective set.
- Content splits on commas; tokens are ASCII-case-insensitive and whitespace-trimmed;
  empty tokens are ignored; an all-empty content is `meta_robots_empty_content`.
- Vocabulary: `all`, `none`, `index`, `noindex`, `follow`, `nofollow`, `noarchive`,
  `nosnippet`, `noimageindex`, `notranslate`, `max-snippet:<int>`,
  `max-image-preview:<none|standard|large>`, `max-video-preview:<int>`,
  `unavailable_after:<RFC 3339 date-time>`.
- `none` expands to `noindex,nofollow`; `all` to `index,follow`. Across every matching
  element the most restrictive value wins: `noindex` over `index`, `nofollow` over
  `follow`, `-1` ("no limit") loses to any non-negative integer, the `max-image-preview`
  order is `none < standard < large`, and the earliest valid `unavailable_after` wins.
- Value errors are findings and never enter the effective set:
  `meta_robots_invalid_value` (malformed integer, non-RFC-3339 date, unknown
  `max-image-preview` value); `meta_robots_unknown_directive` (any other token).
  Unknown-token reporting is lane policy — the source says unknown values are ignored.
- No matching element: effective set is the default `["follow","index"]`, no finding.
- `expect.effective` and `expect.findings` are compared as sorted lists; a difference is
  `meta_robots_expected_mismatch` for the check.
- Exit: 0 all checks match · 1 any finding · 2 input or check fault (missing file,
  bad manifest, duplicate id) · 64 usage. `--selftest` ≥ 40 cases.

### Frozen case families (one case each unless a family says otherwise; ≥ 20 cases)

g01 absent tag → default · g02 `noindex` · g03 `none` · g04 `all` ·
g05 `index`+`follow` one content · g06 `index` tag + `noindex` tag → `noindex` ·
g07 `follow` + `nofollow` tags → `nofollow` · g08 `max-snippet:50`+`max-snippet:20` → 20 ·
g09 `max-image-preview:large`+`standard` → `standard` · g10 `max-video-preview:-1`+`30` → 30 ·
g11 `max-snippet:abc` → `invalid_value` · g12 valid `unavailable_after` ·
g13 invalid `unavailable_after` · g14 uppercase name and content ·
g15 `content=""` → `empty_content` · g16 unknown directive token ·
g17 `name="googlebot"` with default agents → ignored, default effective ·
g18 `name="googlebot"` with `agents:["robots","googlebot"]` → merged ·
g19 matching meta outside `<head>` · g20 declared `noindex` against an `index` expectation ·
g21 self-closing `<meta … />` · g22 single quotes and no spaces around `=` ·
g23 `noarchive`+`nosnippet` · g24 trailing comma and empty token.

Deliverables: `scripts/meta_robots_audit.py` (selftest ≥ 40), the frozen cases/consts and
matrix counter under `.ufo/waves/round-78/`, `corpus/knowledge/meta-robots-directives.md`
with SOURCES rows opened this round, a `corpus/README.md` coverage row, and a
`PROVINCE.md` round-78 block that also carries the round-77 sitemap-formats correction
(routed defect 2).

Not claimed: `X-Robots-Tag` response headers (the lane's header instruments own that
channel); crawler behaviour; whether any live property carries a correct declaration.

---

## Axes and admission

C1 → calibration (2, HOLD) · C2 → freshness (10, HOLD) · C3 → operability (10, HOLD;
capability). No axis is harmed: no existing gate is loosened (C2 ships a negative control;
C3's tool is additive) and no score decreases.

Frontier step (§2b): census before/after with
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`;
SOURCES delta from the sources C3 opens this round; one mistake mined into
`corpus/lessons/round-78.md`; C3 is the sourced claim.

Routed defects from the round-77 closure are carried in the same deliverables: (1) the
SentinelC status correction is appended to the round-78 lesson (append-only), (2) the
PROVINCE/README sitemap correction lands with C3's documentation, (3) the box-4
population is C1, (5) the round-level `doc_quote_truth` receipt is committed under
`.ufo/waves/round-78/controls/`, (6) the amendment-rendering citation is corrected in the
lesson. (4) the SentinelC F1 receipt is re-cut on the committed counter digest in the
lesson's corrections.

Wave `w1`: 14 seats — scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester
1, connector 1 (attack share 4/14 = 28.6 %; connector seats 1). One batched dispatch
through the inline spawn handoff.
