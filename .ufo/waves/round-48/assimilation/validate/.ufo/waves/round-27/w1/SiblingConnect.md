# SiblingConnect — bounded sibling overlap scan (r27-full-citing-set)

Seat: `KakeR27.SiblingConnect` (connector, leaf, judged axis **operability**). Read-only: no sibling
edit, no lane source edit, no manifest/state/index/jj/Git mutation, no tool install. The only file I
wrote is this report. Commands I ran: `python3 -B .ufo/waves/round-27/count_c1.py` (frozen read-only
oracle, at `83528f7` and `be375d9`), `bash scripts/sources-census.sh validate --root . kake-shokunin`
(fleet read-only census, exit 0), Python enumeration over `git show` blobs. I did **not** run the
candidate gate `scripts/citing_set.py` or any sibling gate.

## 1. Verdict in one line

**No sibling lane owns a range-aware citing-set completeness gate, and the two sibling scanners a
maintainer would most plausibly reach for both silently drop exactly the 10 range-interior pairs the
C2 claim depends on (measured 6/16 vs 16/16 detected).** The reusable content of the siblings is not
a regex — it is the *enumeration contract* and three harness shapes, all of which kake must apply to
its own corpus without editing anything outside the lane.

## 2. Named registries/pointers inspected (discovered paths, not broad copies)

| pointer | sha256 | owns | relation to kake C2 |
|---|---|---|---|
| `chousa-shokunin/tools/research-gate.sh` | `ac1315dd…835765` | research **method** (question→hierarchy→chain→claim check) | header-only S-id↔registry check; **no** range expansion |
| `chousa-shokunin/corpus/evidence/round26-registry-oracle.py` | `6b2d135c…f1d78` | independent oracle for that method | ASCII-lookaround token rule; range-blind |
| `kengaku-shokunin/plans/registry_check.py` | `fc388c33…d7379b` | frozen literal source-reference coverage | closest structural sibling; range-blind |
| `kengaku-shokunin/plans/state_check.py` | `4aa47a63…fc13` | r27 P4 population assertions | **only fleet code that expands S-id ranges** |
| `kengaku-shokunin/plans/fixtures/r27/p4_mutate.py` + `r28/registry_oracle.py` | `627d592b…d0ba` / `180fd393…60cb` | mutation-probe harness; alternate derivation | base-stale subtraction; "does not import checker logic" |
| `tabi-shokunin/scripts/check-sources.mjs` | `afd04787…df77` | SOURCES.md shape gate | committed expected table, not derived from output |
| `PROTOCOL.md` (§Gate standard, l.375-421) | `886e459b…41a` | fleet gate **standard** + registry-home rule | defines the shape kake's gate row must satisfy |
| `scripts/sources-census.sh` (fleet root) | `3fb72615…4e30` | fleet SOURCES.md census | registry shape only; never reads corpus/knowledge |
| `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` | — | frozen SOURCES contract | "No second method"; research method stays chousa's |

No other lane ships a `citing_set`-style tool: a fleet-wide search for `unadjudicated_citing_pair`
/ `ledger_pair_not_cited` / `citation_range_invalid` matches **only** kake's own `scripts/citing_set.py`.

## 3. Sibling method detail (exact located support, ≤25 words each)

- chousa gate l.322: "Metadata --registry FILE checks source S-ids against a bounded SOURCES.md table."; l.2514: `source_ids=$(printf '%s\n' "$source_tokens" | LC_ALL=C grep -xE 'S[0-9]{3,}')`
- chousa oracle l.12: `SOURCE_ID_RE = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")`; r27 `CriticRegistryTokens.md`:36: "Tokenize once over ASCII word bytes, then test each whole word."
- kengaku `registry_check.py`:2: "Frozen, literal source-reference coverage. Not a source-truth verifier."; :15: `REFERENCE = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")`
- kengaku `state_check.py`:455: `P4_CITATION_RE = re.compile(r"\bS(\d{3})(?:\s*[-–—]\s*S(\d{3}))?\b")`; l.3465: `numbers.update(range(min(first, second), max(first, second) + 1))`
- kengaku `registry_oracle.py`:2: "L1 alternate derivation, not author-independent; does not import checker logic."; `p4_mutate.py`:10: "A mutant is RED for class Px only when the checker exits 1 and emits a MISMATCH whose id starts with `Px.`"
- tabi `check-sources.mjs`:45: "This expected table is intentionally committed with the gate, not derived from its output."
- PROTOCOL.md:398: "a child lane's *registry home* is its own `SKILL.md`."; :420 "closure grades no gate conformant until its registry row exists at the lane's *registry home`"; :390 "Self-test green is capability, not a measurement (§Evidence standard)."
- kake `PROVINCE.md`:32: "`chousa` owns research method and source hierarchy; kake keeps only domain findings and its own `corpus/SOURCES.md` rows."; `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`:52: "3. **No second method.** Claim admission stays in `corpus/QUALITY.md`; the research method"

## 4. Measured overlap: which sibling enumerator could substitute for C2?

All numbers measured over the **frozen** snapshot (`83528f7`, 26 corpus/knowledge files = 23 `.md` +
3 `.json`, 32-row population, 41-pair r26 ledger, 16-pair oracle `c2-oracle.json` sha256
`1d038205…bc7dd`; `frozen/expected.json` `628b7a05…70c2`; population `16330e1e…1b03`; ledger
`c2026376…95ce`).

| enumerator (measured) | pairs | unadjudicated | oracle hits | false positives |
|---|---|---|---|---|
| chousa whole-token (`grep -xE 'S[0-9]{3,}'`), no range | 47 | 6 | **6/16** | 0 |
| kengaku `REFERENCE` (ASCII lookaround), no range | 47 | 6 | **6/16** | 0 |
| kengaku `P4_CITATION_RE` variant (3-digit, `[-–—]`, min/max) | 57 | 16 | **16/16** | 0 |
| kake frozen `count_c1` grammar (literal + 6 separators + population) | 57 | 16 | **16/16** | 0 |
| bare `S[0-9]{3,}` (no boundary) | 58 | 17 | 16/16 | **1** (`S013`, `ghp-served-set.md`) |
| ASCII-hyphen-only range separator | — | 12 | 12/16 | 0 |
| kake frozen grammar, population filter dropped | 75 | 34 | 16/16 | **18** |

Three independently necessary clauses, each falsifiable by one edit:

1. **Range expansion is load-bearing for 10 of 16 pairs.** Both sibling tokenizers are range-blind.
2. **The en-dash separator is load-bearing for 4 of 16** — the corpus's grouped range
   `static-canonical-preflight.md`:54 is `S001–S006` (U+2013), while the hyphen ranges are ASCII;
   hyphen-only expansion detects 12/16, missing `S002,S003,S004,S005` in that file.
3. **The population intersection is load-bearing against 18 false positives** — `S014`, `S019`, `S035`
   are cited by corpus files but sit outside the inherited 32-row population.

**The `used-by` registry column cannot serve as the enumeration source.** Measured at `83528f7`:
`corpus/SOURCES.md` has 47 used-by cells (29 knowledge + 18 lessons); the in-population knowledge
pairs it names = 27, all inside the 57 (matches `CritDenominator.md`:31). Enumerating from used-by
yields **2** unadjudicated pairs, **0** of them oracle pairs, and **2** false positives (`S014`/
`freshness-sweep.md`, `S035`/`accessibility-review-packet.md` — rows outside the population). It
misses 16/16. The registry is a *claim* about citing files; the corpus text is the *enumeration*. 30
of the 57 in-population corpus pairs are not named by any used-by cell.

## 5. Scope boundaries (no sibling edits; read-only over surfaces I do not own)

- **chousa owns the research method** (`PROVINCE.md`:32; SOURCES-CONTRACT rule 3 "No second method").
  kake's C2 gate must enumerate citing pairs and adjudications only — no claim-vs-source
  re-implementation, no source hierarchy, no chain anchoring. chousa's contribution here is the
  **token-boundary rule** (its oracle's ASCII lookaround), not its method.
- **protocol lane owns the gate standard and the root registry home.** Root `SCORECARD.md`:177 is the
  protocol lane's own registry section; kake's gate row belongs in kake's own `SKILL.md` (PROTOCOL.md:398).
  A working-tree row `| citing-set | gate (syntactic pair completeness only) | …` exists at `SKILL.md`:614
  — closure requires it (PROTOCOL.md:420); I did not touch it.
- **kengaku owns its own plans tree.** `registry_check.py`, `state_check.py`, `p4_mutate.py` are
  kengaku surfaces; kake must copy the *shape*, never the file or its population pins. Likewise
  **the fleet census is not a citing-set gate**: `scripts/sources-census.sh` validates SOURCES.md row
  shape and E11 "used-by path missing on disk" (l.29) and never reads `corpus/knowledge`; run against
  kake it printed `kake-shokunin ok` plus one W04 (S033 duplicate url), exit 0 — it cannot detect the
  C2 omission class. **Out of the C1/C2 denominator:** `corpus/lessons` (32 files, 122 in-population
  pairs, 122 unadjudicated) and the 3 `.json` knowledge files (no S-ids) — only `corpus/knowledge` is
  in scope, matching the frozen `count_c1` enumerator.

## 6. Affected axes

- **operability (primary, this seat):** the C2 capability is kake-local; its *verification* surface is
  where the sibling overlap bites — the round has no independent mutation probe for the gate's
  boundary rule, and two critic seats say so (`CritIndependence.md`:81 "rest on candidate-authored
  fixtures and must not be credited from the c2_count PASS"; `CritClaimFit.md`:104 "Those are
  producer-authored in the same wave (BuildSelftest, BuildFixtures), so").
- **freshness (secondary, must not be harmed):** nothing here touches source adjudication; the C1
  ledger and the 16-pair oracle are unchanged (`c2-oracle.json` sha256 identical at `be375d9`/`08014ce`).

## 7. Proposed move (one, bounded)

**Pin the enumeration contract as a single shared constant, and make the boundary rule the object of
an independent mutation probe.**

Concretely, inside kake only: state the three necessary clauses — (i) standalone-token literal rule
with a **word boundary on both sides** (the chousa/kengaku ASCII-lookaround form), (ii) an independent
range pass over the six declared separators (hyphen, en dash, em dash, `..`, `to`, `through`) with
inclusive expansion, (iii) intersection with the frozen population — as one named, versioned artifact
that both `count_c1.py` and `scripts/citing_set.py` consume, and pin that artifact's sha256 in
`frozen/expected.json` next to the 28 existing input digests (PROTOCOL.md:396 already requires digest
pinning; `snapshot_tampered` is the declared tamper verdict).

Why this is the non-obvious synthesis rather than a restatement: C1's obligation direction and C2's
oracle direction are **coupled through the scanner's boundary rule**. C1's monotone discovery channel
carries the extra obligation `S013`/`ghp-served-set.md` (57→58 pairs; `discovered-pairs.json`, and
`CritDenominator.md`:42 "A boundary-free `S(\d{3,})` scan over all 26 files gives the frozen 57 plus
exactly one extra pair"), while the frozen C2 oracle demands **exactly** 16 findings and
`len(out['findings'])==16`. A gate whose literal rule is ever loosened to a bare `S[0-9]{3,}` would
report 17 and fail the oracle — not because the corpus changed, but because the two instruments
disagree about what a token is. Pinning one shared boundary rule makes that coupling explicit and
monotone instead of accidental.

The probe closing the round's open verification gap uses the sibling harness shape, not the sibling
file: export the base snapshot, apply **one minimal token mutation per class**, require a mutant to be
RED only when the checker emits a finding **absent from the base's own finding set** (kengaku
base-stale subtraction, `p4_mutate.py`:10) so a pre-existing mismatch cannot make a mutant look
detected. One case each: boundary relaxed to bare `S[0-9]{3,}` (expect 17 → oracle FAIL), range
separator set reduced to ASCII hyphen (expect 12 → FAIL), population intersection removed (expect 34
→ FAIL), and the positive control (expect 16, exit 1).

## 8. Risks

- **Risk of over-reach:** adding a shared constant touches the frozen counting command's inputs.
  Mitigation: the constant is *new* and additive; `c2-oracle.json`, the `frozen/expected.json`
  digests, and the 16 expected pairs stay byte-identical (already identical across `be375d9`→`08014ce`).
- **Risk of a false "sibling parity" claim:** kengaku's `P4_CITATION_RE` reaching 16/16 here is
  coincidence of corpus content (3-digit ids, only hyphen/en-dash present, no invalid range), not
  equivalence of semantics — its min/max form **silently accepts** a descending range where kake's
  contract demands `citation_range_invalid`, and its `\d{3}` excludes 4+ digit ids; copying it would
  import a fail-open on exactly the boundary the C2 contract names. Also **risk of a stale sibling
  pointer**: sibling tools are moving (chousa's `research-gate.sh` blob differs between
  `CriticRegistryGrammar.md`'s recorded `c2c813f1…` and the current `ac1315dd…`) — every hash in §2 is
  the hash I read, not a permanent fact.
- **Risk to freshness:** none of this changes adjudication; a new digest entry could only ever *add*
  an obligation if the enumeration changed — the intended monotone direction.

## 9. Verification (for the L1/judge, not run by me)

1. `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision <candidate>` — expect `passed:true`,
   `detected:16`, `falsePositive:0`, `gateExit:1`.
2. `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <candidate>` — expect `citingPairs`
   57 (58 only if the `S013` discovery is admitted into the ledger) and `missing` 0.
3. The §7 mutation probe — one class per case, base-stale subtraction, disposable clone under
   `/fast/scratch/hyaku/kake-r27`, never the live lane. Plus
   `bash scripts/sources-census.sh validate --root . kake-shokunin` — expected `ok` + W04 only (as
   measured now); fleet-shape check, orthogonal to C2.

## 10. Uncertainties

- The tokenizer comparison (§4) is measured over the frozen 23 `.md` knowledge files; the 3 `.json`
  files contain no S-ids, and `corpus/lessons` was excluded by the frozen denominator. A future corpus
  edit could change the row counts without changing the rule. I did not execute
  `scripts/citing_set.py`; the "should report 57/41/16" statement in §4 is derived from the frozen
  counter's own numbers plus the corpus text, and is labelled as inference, matching `BuildGate.md`:46.
- Whether the C2 round owners accept a *new* frozen artifact (the shared enumeration constant) is a
  parent decision; if they decline, the same claim can be enforced by pinning the two regexes' sha256
  values in `frozen/expected.json` instead, with the same mutation classes. The S013 obligation's
  disposition (admit as artifact vs leave UNVERIFIABLE) is likewise an L1 adjudication, not mine;
  §4/§7 show only that the two instruments' agreement depends on the boundary rule being shared.

Report: kake-shokunin/.ufo/waves/round-27/w1/SiblingConnect.md
