# ConnectorScope — r99 w1 sibling-overlap scan (read-only)

seat: ConnectorScope (leaf, no dispatch) · 2026-11-05 · surfaces: C1 registry calibration, C2 304-freshening
scope: sibling lanes `/home/vgpnk/Projects/shokunin/*-shokunin` (20 lanes; kake excluded from the scan), read-only.
Method: grep -il-equivalent over all sibling trees for `registry`+`scripts/` co-occurrence, `gate[ /_-]?registry`, `unlisted`,
counter output discriminators (`unlisted=|GATES_ROWS=|UNREGISTERED_PATH`), and RFC 9111 ground (`4\.3\.4`,
`Freshening Stored`, `Updating Stored Header`, `rfc.?9111`, filename `*9111*`); targeted file reads to ground each gist.
No writes outside this seat dir + the lane-root report file; no clones; no installs; no git/jj mutations anywhere.
Scratch `/fast/scratch/hyaku/kake-r99/ConnectorScope/` created empty and removed before yield.

Lane HEADs observed (`git -C <lane> rev-parse HEAD`, rc=0):
audio f9da7ee9 · chousa 378fda82 · game-dev-2d 1e033ef0 · game-dev-3d 39ca3973 · kagi f5977284 · kaidoku b0a7bb8c ·
kama 9b4c7af1 · kasegi d16d2124 · kengaku ea19299d · kotoba edc731a9 · kotodama 24eac1e9 · kumitate 814068f0 ·
lore 0f044aa7 · mado 24ba2a9d · mori 5e2bcf2c · revenger 05e854ce · souji e063a2fc · tabi 58d84eda ·
tameshi f256302b · tsukuroi 64f45b79

## A. Registry-vs-committed-scripts instruments (C1 surface)

| # | lane | path | HEAD | gist | relation to r99 |
|---|------|------|------|------|-----------------|
| 1 | kotoba-shokunin | `verifiers/check_gate_registry.py` (committed at HEAD, blob `95ffed38`) | edc731a9 | Frozen r54-C2 counter: every blob directly under `verifiers/` at REV must have exactly one `## Gate registry` row in SKILL.md; per-cell semantics (kind gate/probe, entry cell contains the path, verdict-map `code=class` pairs with `0=clean`+`1=failed` for gates, self-test flags must be exact active handlers via Python-AST `add_argument`/shell `case` arms, pinned-values paths must exist via `git cat-file -e <rev>:<path>`, owner fixed); PHANTOM-row class; output `conformant K of M; phantom P`, exit 0 iff K==M ∧ P==0. | **Overlap.** Same surface as `c99_registry.py` (registry home SKILL.md vs committed scripts, frozen universe, exit contract). Strictly stronger per-row cell validation than kake's frozen R1-R5; prior art to learn from, not to copy into a frozen instrument. |
| 2 | kotoba-shokunin | `verifiers/floors-registry.json` + `registry_anchor_drift()` in `verifiers/check_assertion_floors.py` (both committed at HEAD) | edc731a9 | Data-file registry pinning each instrument's path + assertion floor + total; named FAIL classes `registry row vanish`, `registry path drift`, `registry floor drift`, `registry size drift`, `unexpected row` (exit 2), closing two-table coordinated deletion (r37 C2). | **Overlap** (registry↔instrument consistency). kake's c99 has no drift-class named-fail surface of its own; the four named classes are the vocabulary chousa/kotoba reviewers used. |
| 3 | chousa-shokunin | `corpus/evidence/round45/c2-count.py` (committed at HEAD, blob `1506bdb8`) + `controls/c2-control-base.txt` (blob `28f92e8d`) | 378fda82 | Gates-row coverage counter: prints `ENTRY_POINTS/GATES_ROWS/REGISTERED=x/y/UNREGISTERED=n/C2=PASS|FAIL`, exit 0/1/2; target `UNREGISTERED=0`; base control `ENTRY_POINTS=51 REGISTERED=25/51 UNREGISTERED=26 C2=FAIL` exit 1; tip re-run `54/54 UNREGISTERED=0` exit 0. | **Overlap — closest twin of `c99_registry.py`** (kake base also prints `unlisted=26`). Its documented limits are kake's declared limit family: row-grammar invisibility (rows without literal `exit` dropped), substring registration (any row containing the path registers it), `### ` subsection inside section, mention-not-dependence population, junk-prose rows pass, verdict-map correctness out of scope. |
| 4 | kumitate-shokunin | `scripts/sources-check.mjs` | 814068f0 | SOURCES-registry contract checker (`kumitate-sources-v1`): E01-E12/W02-W03 findings — ROW_MALFORMED, ID_DUPLICATE, ROW_OUTSIDE_REGISTRY, USED_BY_MISSING, TIER_INFLATION, REJECTED_NO_FLIP, ENTRY_SOURCE_UNKNOWN, etc. | **Partial overlap.** Registry-completeness discipline over a *source* registry, not a gate registry; same checker genre, different surface; citable for finding-class naming. |

## B. RFC 9111 §4.3.4 / §3.2 ground (C2 surface)

| # | lane | path | HEAD | gist | relation to r99 |
|---|------|------|------|------|-----------------|
| 5 | mori-shokunin | `corpus/evidence/sources-r79/rfc9111.txt` | 5e2bcf2c | Retained RFC 9111 plain-text body including §3.2 "Updating Stored Header Fields" (:369) and §4.3.4 "Freshening Stored Responses upon Validation" (:951). | **Citable.** Independent sibling retained body of the same sections kake's S484 anchors; a cross-lane quote check for §3.2/§4.3.4 paragraphs is possible without network. On disk in lane tree; committed status not separately verified. |
| 6 | mori-shokunin | `corpus/evidence/sources-r37/S225.src` | 5e2bcf2c | WHATWG fetch spec capture citing the "Freshening Stored Responses upon Validation" chapter of [HTTP-CACHING] (S432-style dfn export). | **Citable.** Downstream-spec corroboration that §4.3.4 is the operative freshening chapter. |
| 7 | kumitate-shokunin | `.ufo/waves/round-81/build/L1/captures/rfc9111.html` (jj-tracked in r81 commit ops) + pin in `.ufo/pins/source-captures.json` (`sourceId S237`, sha256 `ce91ee98…`, captured 2026-11-04) | 814068f0 | Committed RFC 9111 HTML capture containing §3.2 and §4.3.4 headings; capture bytes pinned by sha256 in a machine-readable pin registry consumed by `scripts/omp-census.mjs`. | **Citable.** Pin-the-capture-bytes technique: kake's contract pins the retained txt sha in prose; kumitate pins it in a census-consumed JSON. |
| 8 | kumitate-shokunin | `.ufo/waves/round-82/w1/K82ScribeEntry2.md` (+ deliverable `corpus/knowledge/receipt-age-on-the-compare-path.md` per `w1-results.json`) | 814068f0 | Entry reasons over §4.3.4 directly ("a 304 updates the stored response's headers (RFC 9111 §4.3.4 …)"); the seat flagged a real section-attribution conflict: SOURCES.md labelled S237 "§5.1 (Age)" while the located quote sits in §4.2.3. | **Citable, cautionary.** Section-label drift happened in a sibling on this same RFC; ReviewRegA/B judging kake's S484/S485-anchored rows should check anchor-vs-located-section, not just quote presence. |
| 9 | chousa-shokunin | `corpus/SOURCES.md` row S025 (RFC 9111, §4.2 Freshness) | 378fda82 | tier C, status rejected: "a standard for HTTP-cache freshness, not authority for research-record validity; flip: use as an explicitly labelled analogy". | **Citable scoping precedent, no conflict.** Chousa's rejection is about research-record metadata authority; kake r99 uses §4.3.4/§3.2 in-domain for an HTTP cache-behavior tool — the scopes do not collide. |
| 10 | chousa-shokunin | `.ufo/waves/round-26/falsify/FSourceRejection.md` (:50-53, :87) | 378fda82 | Errata listing for RFC 9111: "9185, Section 4.3.4, reported 2026-09-24 … Neither touches §4.2", with python/quote checks exit 0. | **Citable.** Independently corroborates kake's S485 (EID 9185, Reported, on the §4.3.4 initial-set paragraph): same EID, same section, and confirms it does not touch §4.2 — consistent with the contract's "does not change it". |
| 11 | chousa-shokunin | `.ufo/waves/round-25/build/SrcRfc9111.md` + `falsify/residual-final-sources.md` (:66-69) | 378fda82 | Opened RFC 9111 2026-10-21; located `response_is_fresh = (freshness_lifetime > current_age)` (§4.2); scoped analogy verdict. | **Citable.** Background scoping only. |
| 12 | kaidoku-shokunin | `.ufo/waves/round-96/w1/ConnectorOverlap/overlap.md` | b0a7bb8c | Prior sibling-connector scan that mapped kake r96 (HTTP cache revalidation, RFC 9111 §4.3, `c96_reval.py` 14/14 mutation kill) against its lane; noted "independent discovery of mutation-battery killing pattern". | **Citable methodological prior art** — a connector seat covering the same RFC family on kake before this round. |

Non-hits (searched, matches are different documents/surfaces — recorded to preempt confusion):
- chousa `4.3.4` hits are Cochrane LSR guidance §4.3.4 (S037) and retained RFC **9110** §4.3.4 (https certificate verification, `round-32/w1/ScribeSourceC2/rfc9111.txt:1392`) — not RFC 9111 §4.3.4.
- kagi `own_unlisted=` strings are its adjacency scope-gate census fields — not a gate-registry instrument.
- game-dev-2d `registered=`/`unregistered=` strings are Godot ResourceUID fixture output noise.
- kama `registry/` holds append-only claim/outcome ledgers (`unregistered-class-engines.tsv` etc.) — ledger discipline, not SKILL.md-vs-scripts checking.
- kake itself (excluded from the sibling scan) holds its own RFC 9111 captures from rounds 83-97 (S456/S457, rfc7234 contrast, errata-9111.html); the r99 freeze retained a fresh `sources/rfc9111.txt` body instead.

## Contradictions

None found between sibling material and this round's frozen claims/predicates. Two tensions worth naming
(neither contradicts the freeze):
- Fleet `PROTOCOL.md` registry-row field set (per kotoba r23 F6: `gate|probe` + `pinned-value path`) differs from
  kake's frozen `REQUIRED = {name, kind, entry command, verdict map, self-test, write scope, owner}`. Reviewers must
  judge rows against kake's frozen counter, not fleet-PROTOCOL expectations.
- Chousa r45/r46 critics judged mention-based registry coverage "bookkeeping, not calibration of behavior"; kake's
  frozen counter already answers the named classes (boundary-anchored path tokens, verdict-digit rule, one executed
  self-test per row) and declares the junk-prose limit for the review conjunct. Citable as critique, not contradiction.

## One technique from a sibling that hardens c99_registry.py (proposed move)

**Per-row deletion mutation over the 26 repair rows** — from
`chousa-shokunin/.ufo/waves/round-45/w2/MutC2RowRemoval.md` (chousa HEAD 378fda82).

Move: in a scratch clone (`git clone --shared LANE D && assert git -C D rev-parse --show-toplevel == D`), at the C1
repair-commit tree, delete exactly one of the 26 `## Round 99 — tool registry completion` rows at a time and run the
frozen counter `python3 -B .ufo/waves/round-99/c99_registry.py --root D --revision <repair> --work <scratch>`; every
deletion must flip `unlisted>=1` / `met=false` exit 1, and the pristine tree must stay `met=true` exit 0. Any row whose
deletion leaves `met=true` is dead or double-registered — a calibration defect the counter cannot see and eyeball
review routinely misses (chousa's identical battery found 2 of 12 new rows double-registering paths and 1 dead row out
of 54 covered entry points).

Axes affected: improves **calibration (C1)** evidence quality — it gives ReviewRegA/ReviewRegB a mechanical
load-bearing receipt per row (27 rc-bearing runs) on top of the two-reviewer conjunct. Harms none: it edits only a
scratch clone, never the scored commit, the frozen counter, or SKILL.md; C2 is untouched; runtime is one
ls-tree+parse counter × 27 ≈ minutes.
Second-order effects: receipts are reviewer evidence only — they must never be presented as a C1 score (C1 is scored
at the repair commit by the unmutated tree); attribution requires deleting exactly one table row (pipe-line) per run;
fixture identity `<seat>@example.invalid` via `-c` flags only.
Risks: a shared clone edited without the `rev-parse --show-toplevel` assertion could escape to the lane (host guard);
reviewers may over-weight a green deletion battery into "rows are correct prose" — the frozen junk-prose limit still
applies and only the review conjunct covers it.

## Verification (commands run this seat; nothing else claimed)

- `git -C <lane> rev-parse HEAD` × 20 sibling lanes — rc=0, HEADs above.
- `git -C chousa-shokunin ls-tree HEAD -- corpus/evidence/round45/c2-count.py corpus/evidence/round45/controls/c2-control-base.txt` — rc=0, blobs `1506bdb8`/`28f92e8d` present at HEAD 378fda82.
- `git -C kotoba-shokunin ls-tree HEAD -- verifiers/check_gate_registry.py verifiers/floors-registry.json verifiers/check_assertion_floors.py verifiers/check_mutation_battery.py` — rc=0, all four at HEAD edc731a9.
- grep sweeps (specialized grep tool, case-insensitive, gitignore off): `registry`, `unlisted`, `gate[ /_-]?registry`, `unlisted=|REGISTERED=|UNREGISTERED=|GATES_ROWS=|dangling=`, `unlisted=|GATES_ROWS=|UNREGISTERED_PATH` (scoped), `4\.3\.4`, `Freshening Stored`, `Updating Stored Header`, `rfc.?9111` — all rc=0 with the hits/non-hits above; sibling-only scoping re-ran `Freshening Stored|Updating Stored Header` and `rfc.?9111` with kake+chousa excluded, surfacing mori/kumitate/kaidoku hits only.
- Reads grounding each gist: kotoba `check_gate_registry.py:1-63` (docstring semantics verbatim), kumitate `sources-check.mjs:1-28`, chousa `corpus/SOURCES.md:28-42` (S025 row verbatim), kake freeze.md, fresh304-contract.md, c99_registry.py, c99_fresh304.py.
- Coverage limits: ripgrep-style tool paginates; per-file caps noted by the tool ("first 20 per file"). The sibling-only scoped re-runs for the two RFC phrases and the tightened counter discriminator are the decisive negative scans; chousa/kotoba instrument coverage is grounded in committed-blob reads and round receipts, not page 1 of a flood. `git grep` over history and `.jj` blob content beyond `tree_state`/op args were not searched [INFERENCE: no sibling instrument hidden in jj-only history was checked].
- Installs: none. Mutating git/jj: none. Writes: this file + `.ufo/waves/round-99/w1/ConnectorScope.md` (lane-root report per round rule and r98 layout precedent).
