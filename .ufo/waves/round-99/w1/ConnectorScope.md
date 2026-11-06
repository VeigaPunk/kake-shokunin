# ConnectorScope — r99 w1 sibling-overlap scan (report)

seat: ConnectorScope (leaf) · 2026-11-05 · full tables, gists, technique and verification log:
`.ufo/waves/round-99/w1/ConnectorScope/overlap.md` (12 hits, evidence-checked).

Surfaces: C1 (SKILL.md registry vs committed `scripts/`) and C2 (RFC 9111 §4.3.4 + §3.2 ground).

## Findings (condensed)

- **C1 overlaps (4):** kotoba `verifiers/check_gate_registry.py` (frozen r54-C2 counter, committed blob `95ffed38` — same surface as `c99_registry.py`, stronger per-cell row semantics incl. exact-active-handler self-test flags and `git cat-file -e` pinned-path existence, PHANTOM class); kotoba `verifiers/floors-registry.json` + `registry_anchor_drift()` (named drift classes: row vanish / path drift / floor drift / size drift); chousa `corpus/evidence/round45/c2-count.py` (closest twin — committed blob `1506bdb8`, base control `UNREGISTERED=26` exit 1, the same before-count as kake's `unlisted=26`, plus its documented limit family: grammar-invisible rows, substring registration, mention-not-dependence, junk-prose passes); kumitate `scripts/sources-check.mjs` (registry-completeness checker over the SOURCES registry, partial).
- **C2 ground (citable, 8):** mori `corpus/evidence/sources-r79/rfc9111.txt` (retained body with §3.2 :369 and §4.3.4 :951) and `sources-r37/S225.src` (WHATWG fetch capture citing the freshening chapter); kumitate `.ufo/waves/round-81/build/L1/captures/rfc9111.html` (jj-tracked capture pinned S237 sha256 `ce91ee98…` in `.ufo/pins/source-captures.json`) and round-82 `K82ScribeEntry2.md` (reasons over §4.3.4; flagged a §5.1-vs-§4.2.3 section-attribution drift on S237 — cautionary for S484/S485 anchor checks); chousa `corpus/SOURCES.md` S025 (RFC 9111 §4.2 scoped tier-C rejected-as-authority — scoping precedent, no conflict with kake's in-domain use) and `.ufo/waves/round-26/falsify/FSourceRejection.md` (erratum **9185 on §4.3.4, reported 2026-09-24 — independently corroborates kake's S485**, and confirms it does not touch §4.2); chousa round-25 SrcRfc9111/residual notes; kaidoku `.ufo/waves/round-96/w1/ConnectorOverlap/overlap.md` (prior connector scan over kake r96's RFC 9111 §4.3 work).
- **Contradictions: 0.** Two named tensions, neither against the freeze: fleet-PROTOCOL row field set (`gate|probe`, `pinned-value path`) ≠ kake's frozen REQUIRED set — reviewers must use kake's counter; chousa critics' "bookkeeping, not calibration" verdict on mention-based coverage — kake's frozen counter already names those classes and declares the junk-prose limit for the review conjunct.
- **Non-hits recorded:** chousa `4.3.4` hits are Cochrane §4.3.4 (S037) and RFC 9110 §4.3.4; kagi `own_unlisted=` is its adjacency census; game-dev-2d `registered=` noise is Godot ResourceUID fixtures; kama `registry/` is claim ledgers.

## One technique from a sibling that hardens c99_registry.py

**Per-row deletion mutation** — `chousa-shokunin/.ufo/waves/round-45/w2/MutC2RowRemoval.md`: in a scratch clone at the
repair-commit tree, delete each of the 26 repair rows one at a time and run the frozen `c99_registry.py`; every deletion
must flip `unlisted>=1`/`met=false` exit 1, pristine stays `met=true`. Catches dead and double-registered rows the
counter cannot see (chousa's identical battery found 2 double-registrations + 1 dead row among 12 new rows). Reviewer
evidence only — never a C1 score; scratch clone asserts `rev-parse --show-toplevel` before edits; no frozen surface is
touched; improves calibration, harms no other axis.

## Verification

`git -C <lane> rev-parse HEAD` × 20 siblings rc=0; `git ls-tree HEAD` confirms chousa `c2-count.py` (`1506bdb8`) +
control (`28f92e8d`) and kotoba's four verifiers committed at their HEADs; decisive sibling-only scoped greps
(`Freshening Stored|Updating Stored Header`, `rfc.?9111`, `unlisted=|GATES_ROWS=|UNREGISTERED_PATH`) rc=0; targeted
reads ground every gist (kotoba `check_gate_registry.py:1-63`, kumitate `sources-check.mjs:1-28`, chousa
`SOURCES.md:28-42`, kake freeze/contract/counters). No installs; no mutating git/jj; no clones; no writes outside
`w1/ConnectorScope/` and this lane-root report. Scratch `/fast/scratch/hyaku/kake-r99/ConnectorScope/` created empty
and removed before yield.

CONNECTOR hits=12 overlaps=4 contradictions=0 techniques=1
