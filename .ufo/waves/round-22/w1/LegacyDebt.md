# Round 22 · w1 · LegacyDebt (connector, read-only)

Lane: `kake-shokunin`. Base: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Scope: connect the carried legacy path debt to C1, the offline static canonical publishing preflight. Nothing else was edited.

## 1. Axes

| Axis | Role this round | What must be true after C1 |
|---|---|---|
| operability | Judged. Contract C1. Milestone `offline-canonical-capability`. | `python3 .ufo/waves/round-22/measure.py --root <root> --revision <tip>` can classify the frozen 32-case matrix with the contract exit map. Baseline `7c61c8cc` has no `scripts/canonical_audit.py` (`test -f` exit 1), so accepted stays 0/32 unavailable until that script exists in the measured revision. |
| freshness | Not a C1 claim. Contract debt says the paths gate stays red. | `node scripts/freshness-sweep.mjs --offline --section=paths --json` stays exit 1, drift 3, newMissing 0, missSet 55, with the same four unannotated locations. |

Saturation is already 10/10 on both owned axes (SCORECARD §Saturation). C1 is a separate capability command. Folding it into `freshness-sweep.mjs` would make the capability exit share `verdictOf`'s `Math.max` with the red paths section (`scripts/freshness-sweep.mjs:1004-1007`).

## 2. Evidence

Frozen contract debt string (`.ufo/waves/round-22/contract.json`): paths gate remains red, three targets / four legacy locations, missSet 55; anchor-census 78 is not a gate; reconstructed Gate chronology is superseded only by the round-21 register; no SHONEN promotion; do not edit protected verifier or historical lesson/knowledge bytes.

Committed receipt `.ufo/waves/round-21/paths-after.json`, revision `df6196b022a7fe9ac9a88af1293dc377a8197652` (ancestor of this base; `git diff --stat` on the four cite files, `SHONEN.md`, and `corpus/knowledge/freshness-pins.json` is empty):

- argv: `node scripts/freshness-sweep.mjs --offline --section=paths --json`
- outer exit 1
- `counts.drift` 3, `counts.declaredAbsent` 52, `counts.newMissing` 0, `missSet.length` 55
- unannotated locations 4, on these targets:

| Target (absent on disk; still in `pins.pathsMissSet`, length 55) | Unannotated cite at this base |
|---|---|
| `~/Projects/plazir-15-site` | `corpus/knowledge/drift-detection.md:77` |
| `~/Projects/plazir-15-site` | `corpus/knowledge/fleet-registry.md:57` |
| `~/Projects/webzites/bin/webzites.mjs` | `corpus/knowledge/free-read-verbs.md:321` |
| `~/Projects/webzites/scripts/kimi-surface.mjs` | `corpus/lessons/round-6-aggregator-audit.md:48` |

Those four lines, read at base:

- `drift-detection.md:77` is the r16 table header whose source column is `` `~/Projects/plazir-15-site` ``. The same table's `speedrun/` `rel=canonical` row is line 81: live `` `…/plazir-15-site/speedrun/` ``, source `` `https://ds4cc.com/speedrun/` `` (`0de5eb9`), `origin/main` self. An r20 citation-local note naming this path sits at line 95, 18 lines outside the scanner's ±2 window (`scripts/freshness-sweep.mjs:405-413`, `ABSENT_RE` at line 122).
- `fleet-registry.md:57` is the `plazir15` row (kimi 404, source `` `~/Projects/plazir-15-site` ``). Line 58 cites the same path for `plazir15-ghp` and is not in the receipt's `unannotatedCites`. A same-file r20 note for this path is at line 85. `pathsAbsenceStrictSameLine` is unset in `freshness-pins.json`. [INFERENCE] Line 58 is annotated by bleed from the line 60 HTML comment, which says `absent` about `~/Projects/origin-work/charter-ufo-fsd`, inside ±2 of line 58 and outside ±2 of line 57. The receipt is the fact; the bleed cause was not re-executed.
- `free-read-verbs.md:321` is the round-11 probe command `node ~/Projects/webzites/bin/webzites.mjs probe ds4cc-com --json`. The r20 note at line 325 names `~/Projects/webzites/scripts/kimi-surface.mjs`, a different token, four lines away.
- `round-6-aggregator-audit.md:48` is the aggregator's `sed` of `~/Projects/webzites/scripts/kimi-surface.mjs` (zip-exclude chain, verdict pass). That file is aggregator-authored. The contract forbids editing it.

`pins.plazirSourceDir` is `/home/vgpnk/Projects/plazir-15-site`. `pins.plazirLiveSitemapUrl` is `https://veigapunk.github.io/plazir-15-site/sitemap.xml` with `plazirLiveSitemapLocs` 8 (`freshness-pins.json:38-42`). `checkPlazir` (`freshness-sweep.mjs:690-713`) runs `git -C` that directory and, when not offline, fetches the live sitemap. `SECTIONS` already contains `plazir` (line 129). That section is PQ-14 freshness, not an HTML canonical-link policy.

PROVINCE.md Frontier leaves canonical signals open and grounds a move to Core only with a source-backed entry and a gate. PROVINCE.md Surfaces records the plazir-15-site and webzites checkouts absent since the 2026-10-12 prune; restore-or-retire stays operator-owned. `corpus/README.md` repeats that boundary and points canonical signals at the Frontier, not at the paths pin.

Anchor-census 78 and the reconstructed Gates are carried from committed round-21 text, not re-measured here: `corpus/lessons/round-21.md` Final measured results (78 baseline-inapplicable diagnostics, exit 1, not a reference pass); `corpus/lessons/round-21-verifier-spotcheck.md` routed notes 2–3 (`round-4.md:50`, `round-9.md:185`, `round-16.md:171` superseded only by the round-21 register). SHONEN.md at this base has four unchecked `[ ]` boxes. The verifier note says `[~]`. Either reading is short of promotion. This round does not check or change those boxes.

Working tree at read time, not part of `7c61c8cc`: untracked `corpus/lessons/round-22.md` and a modified `corpus/QUALITY.md` already say legacy path reds are carried and that recovering green by editing `pathsMissSet` is rejected scope. This report does not edit those drafts. The four cite identities above are from the committed receipt, which those drafts do not name.

## 3. Pattern to reuse

Reuse the round-21 split between a revision-bound counter and a pre-existing red gate.

- `.ufo/waves/round-21/measure.mjs` reads `git show <revision>:<rel>` for its own population (knowledge trios and lesson Gates). It does not call `freshness-sweep.mjs` and it does not take `pathsMissSet` as an input.
- `scanCitations` keeps a missing path in `drift` while any cite is unannotated, and moves it to `declaredAbsent` only when every cite is annotated (`freshness-sweep.mjs:445-453`). Annotated absence stays inside `missSet`. Round 20's post-review put the paths exit back to 1 after a temporary exit 0; missSet stayed 55 (`LOG.md` round 21 measured closure; `SCORECARD.md` round 21 "No owned-axis harm").
- The corpus-contract row in `SKILL.md` (Publishing-corpus contract gate) is a separate entry, verdict map, frozen proof, and write scope. It did not clear the paths section. Round 21 recorded both: corpus-contract exit 0 and paths exit 1.

C1's counter should copy that split: materialize `scripts/canonical_audit.py` and `.ufo/waves/round-22/{matrix.py,cases.json,fixtures/**}` only, as `w1-spec.json` already tells Measure. Manifest HTML paths stay relative to the manifest directory (contract `fileResolution`).

## 4. Boundary left outside C1

- The paths population: exit 1, the four cites in §2, missSet 55, newMissing 0, and `freshness-pins.json` `pathsMissSet` / `plazirSourceDir` / `plazirLiveSitemapUrl`.
- PQ-14's live-versus-source canonical disagreement at `drift-detection.md:81`. The three speedrun values disagree, and the source tree is one of the three drift targets. Contract limits exclude network freshness, redirects, and publishing readiness.
- `verdictOf` coupling. A canonical section added to `SECTIONS` cannot exit 0 on its own while paths is loaded; a combined green would hide the paths debt.
- Anchor-census 78, the round-4/9/16 reconstructed Gates, SHONEN promotion, and any byte of `round-6-aggregator-audit.md` or other historical lesson/knowledge files.
- Scanner-window repairs. Clearing line 57 by sliding the line 60 comment, or clearing line 77 by moving the line 95 note into the r16 table, rewrites historical bytes and changes freshness behavior. `fleet-registry.md` and `drift-detection.md` are in the round-21 N→N+4 register (`corpus/lessons/round-21.md` Inbound-pointer correction register); another insertion desynchronizes that register.

## 5. Proposed move

Keep C1's fixtures and counter off the legacy home paths. Knowledge prose that must point at this debt cites the relative receipt `.ufo/waves/round-21/paths-after.json`, not `` `~/Projects/plazir-15-site` ``, `` `~/Projects/webzites/bin/webzites.mjs` ``, `` `~/Projects/webzites/scripts/kimi-surface.mjs` ``, or `/home/vgpnk/Projects/plazir-15-site`.

`PATH_RE` (`freshness-sweep.mjs:125`) matches `~` and `/home/vgpnk` in scanned Markdown. A new `corpus/knowledge` or `corpus/lessons` file that pastes one of those three targets adds an occurrence. If that occurrence's ±2 window lacks an absence word, the unannotated location count moves 4→5 while `counts.drift` can stay 3 and `newMissing` stay 0, because those targets are already in `pathsMissSet`. A summary that only prints "drift 3, newMissing 0, missSet 55" would miss it. `ABSENT_RE` includes `missing`, so the finding id `canonical_missing` placed within ±2 of a new home-path token would annotate that new occurrence only and would still leave the four old cites red.

The matrix positive controls stay on contract fixture names (`absolute_match` and the other 31) with manifest-relative HTML. They do not take `expectedCanonical` from the three `drift-detection.md:81` speedrun strings.

## 6. Falsifier

Name: `legacy-cite-set-beside-matrix`. Run on the integration tree, offline, after C1's files exist. Do not edit pins or the four historical files first.

1. `node scripts/freshness-sweep.mjs --offline --section=paths --json`
2. `python3 .ufo/waves/round-22/measure.py --root <that-tree> --revision <that-commit>`
3. `git diff 7c61c8cc791bde36dd5e3688bdfea2678d90146c -- scripts/freshness-sweep.mjs corpus/knowledge/freshness-pins.json corpus/knowledge/drift-detection.md corpus/knowledge/fleet-registry.md corpus/knowledge/free-read-verbs.md corpus/lessons/round-6-aggregator-audit.md`

Pass: (1) exit 1 and the unannotated set equals the four path/cite pairs in §2, with missSet length 55 and newMissing 0; (2) reports the matrix from the measured revision's own blobs (accepted 0 and unavailable on `7c61c8cc`; accepted follows the frozen expectations only on a revision that contains the validator and fixtures); (3) empty.

Fail, and C1 has absorbed the debt or lost operability, if any one holds:

- (1) exits 0, missSet length changes, newMissing is not 0, or the unannotated pair set is not exactly those four.
- (2) is unavailable, or accepted is 0, on a revision that contains `scripts/canonical_audit.py` and the matrix, because resolution used `plazirSourceDir`, `~/Projects/webzites`, or a network fetch.
- A positive matrix case's `expectedCanonical` is `https://ds4cc.com/speedrun/`, a `plazir-15-site/speedrun/` URL, or the live sitemap URL from the pins. That launders the line 81 disagreement into a clean control.
- (3) is non-empty.

## 7. Risks

- Coordinate witness versus byte witness. The line numbers are valid while those four files match `df6196b`/`7c61c8cc`. A pure prefix would keep the header bytes red and still fail (3) if this round is not supposed to prefix them. Do not "fix" a number mismatch by editing the receipt.
- The line 58 bleed [INFERENCE] is an existing freshness behavior. Repairing it is a paths-gate change, outside C1, and can clear or unclear neighboring rows.
- `corpus/lessons/round-22.md` and the `QUALITY.md` canonical bullets are uncommitted L1 text seen during this read. If they gain a `~/Projects/...` token, they become part of the falsifier's scanned corpus.
- SHONEN.md's `[ ]` boxes disagree with the verifier's `[~]` wording. Promoting either form is outside this capability.

## 8. Verification

Not run, for L1: the falsifier in §6; `measure.py` itself (not on this base); any online `checkPlazir` fetch. Read-only checks already done are the receipt parse, the pin length, the four line reads, `git diff --stat` against `df6196b` for those files, and `test -f scripts/canonical_audit.py`.

## 9. Changes and tooling

- Files changed: this report only, `.ufo/waves/round-22/w1/LegacyDebt.md`.
- No commits, no clone, no edits to sweep, pins, lessons, knowledge, QUALITY, SHONEN, or the contract.
- Tool installs or updates: none.
