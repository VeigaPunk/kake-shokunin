# InheritedDebt — r21 routed debts vs the round-22 criterion (scout)

Seat: scout, wave 1, read-only. Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Base and observed lane tip/master:
`7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Frozen contract:
`.ufo/waves/round-22/contract.json`.

Scope: map the four r21 routed defects (the non-author
`corpus/lessons/round-21-verifier-spotcheck.md` §"Routed defects / notes for the
lane (next round)") onto (a) what round 22 intentionally leaves unchanged and
(b) the round's new criterion, without relabelling the still-red paths gate or
the anchor census as claims. This report runs no gate, test, selftest, matrix
or measurement. All statements below are file observations at the stated
revision; inference is marked.

---

## 0. Baseline and provenance (observed)

| Item | Observation |
|---|---|
| `git rev-parse HEAD` / `master` | both `7c61c8cc791bde36dd5e3688bdfea2678d90146c` |
| Base delta vs r21 measured commit `df6196b` | one new file: `corpus/lessons/round-21-verifier-spotcheck.md` (+127 lines); no pre-existing corpus byte changed |
| `.ufo/waves/round-22/census-before.txt` | `baseline master: 7c61c8c…`; "only this round's new `.ufo/waves/round-22/` was untracked after contract creation; no inherited lane-authored work" |
| Working tree at observation (18:34–18:36 local) | `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/README.md`, `M corpus/SOURCES.md`; untracked `corpus/knowledge/static-canonical-preflight.md`, `corpus/lessons/round-22.md`, `.ufo/waves/round-22/` |
| Tracked historical corpus modified? | No: `git status --porcelain -- corpus/knowledge corpus/lessons` shows only the two new untracked r22 files; no existing knowledge/lesson/aggregator/verifier byte is modified |
| r21 receipt revision | Both `.ufo/waves/round-21/paths-after.json` and `.ufo/waves/round-21/anchors-fixed.json` record `revision: df6196b…`, the commit before the r21 verifier lesson, **not** the r22 base |

Consequence: the r21 receipts are the correct historical measurement of the
debt, but they are not base-revision measurements. Base adds a verifier lesson
whose only path-like cites are three resolving absolute paths
(`round-21-verifier-spotcheck.md:95-96`). [INFERENCE] They add `resolve`
sample size, not drift or miss-set membership, because the paths gate's
`newMissing`/`newDrift` are compared to pinned sets; the contract's debt
sentence is binding regardless. If L1 re-runs the gate, run it at the base/tip
and record `filesScanned`; do not present the `df6196b` receipt as a
base-revision run.

In-flight r22 artifact state at observation (not inherited debt):
`replay.py` present untracked; `scripts/canonical_audit.py`,
`.ufo/waves/round-22/measure.py`, `matrix.py`, `cases.json`,
`frozen/expected.json` absent.

---

## 1. The inherited register (r21, non-author text)

Verbatim pointers, `corpus/lessons/round-21-verifier-spotcheck.md:113-127`:

| ID | Routed defect | Exact routed wording |
|---|---|---|
| D1 | paths gate | "Existing paths gate `freshness-sweep.mjs --section=paths` remains red (exit 1, three drift targets / four legacy locations, missSet 55) — pre-existing, honestly carried; still owed (restore or retire per operator)." (115-117) |
| D2 | anchor census | "`anchor-census.mjs` exit 1 retained (78 baseline-inapplicable diagnostics in author wave reports); an evidence helper, not a registered gate — keep it out of any gate claim or reduce its scope to historical bytes." (118-120) |
| D3 | reconstructed chronology | "Reconstructed old Gates in `round-4.md:50`, `round-9.md:185`, `round-16.md:171` keep read-time statements that S019 / the round-21 lesson were absent; they are superseded only by the round-21 register. Readers of those files alone may misread them; future reconstructions should be written after their sources land." (121-124) |
| D4 | SHONEN | "SHONEN: all four boxes `[~]` author assertion; box 2 points to a local corpus repair, not a domain end-to-end task. Not fully checkable by a non-author yet; promotion stays operator-owned." (125-127) |

The r22 contract repeats these as binding `debts`:
`"Paths gate remains red three targets/four legacy locations missSet55;
anchor-census78 not a gate; old reconstructed Gate chronology superseded only
by r21 register; no SHONEN promotion. Do not edit protected verifier or
historical lesson/knowledge bytes."`

Not in the routed four, and therefore outside this mapping's claim surface:
the retained freshness-sweep confinement bound (`round-21.md:61,200`: aliases,
bracket/split calls, child-process writes are not covered) and the r21 misroot
recovery (`round-21.md:193`, four reports copied byte-exact and fleet copies
deleted). Round 22 neither clears nor worsens them; the canonical validator's
read-only statement is about its own normal path, not a re-proof of
`freshness-sweep.mjs`.

---

## 2. Mapping — intentionally unchanged versus new criterion

The mapped "new criterion" is the round's own text: `corpus/QUALITY.md:75-91`
(§"Canonical signal and reconstruction ordering — round 22") plus the
`SKILL.md:394-416` round-22 section. Both are **uncommitted working-tree
additions at observation**, not base content (`git show 7c61c8c:corpus/QUALITY.md`
has no round-22 heading).

| ID | Verified debt fact (observation) | r22 disposition | New-criterion anchor | Prohibited relabel |
|---|---|---|---|---|
| D1 | `paths-after.json` exit 1; counts `drift:3`, `newDrift:0`, `newMissing:0`; `missSet` length 55; 4 unannotated cites (below). Contract echoes 3 targets / 4 locations / missSet 55. | **Intentionally unchanged / carried.** Not cleared, not re-pinned, not a C1 matrix case, not a freshness improvement. One of the four locations sits in a protected aggregator lesson, so the debt is not even editable under the round's byte constraint. | `QUALITY.md:89-91`: "Legacy missing-path reds are carried, not counted as a round22 improvement." Draft lesson `round-22.md:70-71` carries the counts. | "paths gate clean/passed"; "drift cleared"; "missSet resolved"; "newMissing 0 = clean"; "r22 restored plazir/webzites"; citing path-gate output as C1 evidence. |
| D2 | `anchors-fixed.json` exit 1; summary `targets:37`, `violations:0`, `references:3294`, `moved:2051`, `mismatches:78`; mismatch taxonomy 73 `out-of-range` + 5 `target-not-at-base`; all 78 sources under `.ufo/` (author wave reports). `SKILL.md:389-391` classifies the helper as an evidence tool, not a gate. | **Intentionally unchanged / helper status.** Exit 1 retained; not registered, not suppressed, not converted into a matrix expectation. Its scope is historical-byte/pointer audit, not canonical policy. | `QUALITY.md:89-91`: "An unregistered evidence helper's red diagnostics cannot be relabelled as gate success. The round21 anchor census is intentionally outside gate claims." `SKILL.md:413-415` extends the same rule to the new matrix/measurement/replay helpers. | "anchor census passes"; "0 diagnostics"; "all references current"; "anchor gate green"; adding anchor output to the canonical-audit gate row's self-test/frozen-proof cells. |
| D3 | Read-time absence statements exist at `round-4.md:50`, `round-9.md:185`, `round-16.md:171` (inside Gates at 44/68/78). Superseding text: `round-21.md:98-100` ("superseded by this register") and `round-21.md:110-114` (inbound-pointer correction register). | **Intentionally unchanged historical bytes.** No correction, no appended erratum, no rewrite. The r21 register remains the only supersession pointer. | `QUALITY.md:80-84`: reconstructed Gate must name observation revision and be written after its sources exist; old round-4/9/16 Gates "fail this current criterion and remain superseded only by round21's existing register." Draft lesson `round-22.md:63` records the same rule as its retrospective-chronology mistake. | "r22 corrected the old Gates"; "old Gates now satisfy the criterion"; "rewrote chronology"; "updated the r21 register"; any edit to the three files. |
| D4 | `SHONEN.md:5-8` has four unchecked `- [ ]` boxes. The r21 fleet report §SHONEN (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-21/kake.md:98-101`) has four `[~]` author assertions; no `[x]`, no named non-author verifier, no promotion. | **Intentionally unchanged / operator-owned.** The r22 capability entry does not advance a box, and no non-author SHONEN review exists. | **No r22 criterion anchor.** `QUALITY.md`'s grounding line says "routed notes 2–4" (77-78), but no bullet addresses SHONEN. Draft lesson `round-22.md:73` carries it as "SHONEN not independently checkable" (see §5, defect 1). | "[x]"; "promoted"; "non-author verified SHONEN"; "capability entry satisfies box 2"; changing `SHONEN.md` boxes. |

Global byte constraint (contract, not a routed defect): "Do not edit protected
verifier or historical lesson/knowledge bytes." Observed status at this
revision: **holding** — no tracked verifier, aggregator, knowledge or lesson
byte is modified; the only corpus changes are new r22 files.

### D1 evidence detail (four legacy locations)

From `.ufo/waves/round-21/paths-after.json` (`sections.paths.drift[].unannotatedCites`):

| Target (drift path) | Unannotated cite(s) |
|---|---|
| `~/Projects/plazir-15-site` | `corpus/knowledge/drift-detection.md:77`, `corpus/knowledge/fleet-registry.md:57` |
| `~/Projects/webzites/bin/webzites.mjs` | `corpus/knowledge/free-read-verbs.md:321` |
| `~/Projects/webzites/scripts/kimi-surface.mjs` | `corpus/lessons/round-6-aggregator-audit.md:48` |

The fourth location is in a protected aggregator lesson, which is why
"restore or retire per operator" is the only honest disposition and why the
paths red cannot be cleared by an r22 writer without violating the byte
constraint.

### D2 evidence detail (why "red" needs a qualifier)

The helper's failure is 78 pointer-diagnostics, **not** byte damage: the
preservation audit reports `violations: 0` on 37 targets (21 knowledge + 15
baseline lessons + the new round-21 lesson). All 78 mismatch sources are under
`.ufo/`; 73 cite a line beyond the target's old extent (wave reports predicting
new suffix lines) and 5 cite a target absent at the audit base (the new round-21
lesson). The honest sentence is: "exit 1 retained; zero prior-byte violations;
78 baseline-inapplicable diagnostics in author wave reports; not a gate."
Saying only "anchor census is red" invites the same misreading the verifier
routed note 2 warns against.

---

## 3. What is genuinely new in round 22 (C1), and what is inherited convention

New ground, from the frozen contract and `PROVINCE.md:22-23` ("canonical/JS
rendering open"):

1. `scripts/canonical_audit.py` — offline, read-only, stdlib `HTMLParser`
   validator over explicit-head serialized HTML; manifest-relative regular
   files; symlink/traversal rejection; no network or normal-mode writes.
2. Policy: exactly one canonical `link` in explicit head; `rel` ASCII
   case-insensitive token list; first head `base href` or document URL for
   resolution; WHATWG-like normalized HTTP(S) absolute comparison preserving
   query; reject fragments and credentials; exactly the contract's ten
   `findingIds`; exit 0/1/2/64.
3. Frozen 32-case matrix with per-case expected exit **and** finding id,
   including clean positive controls; independent `matrix.py`/`cases.json`/
   `fixtures/`; revision-bound `measure.py`; frozen replay.
4. Before → after count: baseline `0/32` accepted and unavailable (capability
   absent, not 32 wrong answers); candidate every case matches expectation.
5. New `QUALITY.md` bullet 2 bounds the claim: declared publisher policy over a
   named static-file population; never Google's selected canonical, duplication,
   live delivery or JS state; source recommendations distinguished from stricter
   local policy.
6. `SKILL.md` gate row `canonical-audit` + decision table; `corpus/README.md`
   frontier row; `SOURCES.md` S020–S027.

Inherited **conventions** (reuse, not debt clearance, not new claims): the
0/1/2/64 verdict map, `--selftest` with isolated fixtures, frozen input
digests + replay, revision-pinned measurement, read-only-by-construction, and
"helpers are evidence tools, not gates." These conventions come from
`corpus-contract.mjs`/`freshness-sweep.mjs`/`measure.mjs`; reusing them does not
discharge D1–D4.

Correspondence between the routed notes and the new criterion text:

| Routed note | QUALITY r22 bullet | Status |
|---|---|---|
| D2 anchor census (note 2) | bullet 3, sentences 1–2 (89-90) | mapped |
| D3 chronology (note 3) | bullet 1 (80-84) | mapped |
| D1 paths red (note 1) | bullet 3, sentence 3 (91) | mapped |
| D4 SHONEN (note 4) | none | **unmapped** |
| — (new C1 scope) | bullet 2 (85-88) | new criterion |

The grounding line (`QUALITY.md:77-78`) says "routed notes 2–4", but the bullets
cover 1–3 and omit 4. See defect 1.

---

## 4. Relabel audit of current r22 draft artifacts (observed)

| Artifact | Statement | Verdict |
|---|---|---|
| `SKILL.md:413-415` | "independent matrix/measurement/replay helpers are evidence tools, not additional domain gates. A missing tool on the baseline is capability absent, not 32 observed classification mistakes. Legacy paths gate and anchor-census debts remain exactly as bounded by the round21 non-author verifier." | pass — explicitly refuses all three relabels |
| `QUALITY.md:89-91` | helper red ≠ gate success; anchor outside gate claims; legacy missing-path reds carried, not counted as r22 improvement | pass |
| `corpus/lessons/round-22.md:66-75` | carried debts unchanged; baseline 0/32 unavailable, not 32 wrong; protected files not writable | substance pass; wording gaps in §5 |
| `corpus/knowledge/static-canonical-preflight.md:7-9, 48-52` | owns publisher-side static-file validation only; "Original hosting/source-restoration debts are unchanged"; no production artifact claimed as tested | pass |
| `.ufo/waves/round-22/w1/PublisherVsBrowser.md:28` | paths red, anchor-census not a gate, no SHONEN promotion | pass |
| `.ufo/waves/round-22/w1/NoCarriedRedRelabel.md` | carries both reds and specifies per-case exit/id constraints | pass as an author-side critic report; its "run 2026-10-20 at base" lines are its own receipts, not mine |

No current r22 artifact observed by this seat relabels D1 green or D2 as a gate.
The risk is prospective (report/SCORECARD text), not present in the drafts
above.

---

## 5. Defects / corrections for L1 (actionable, in priority order)

1. **QUALITY grounding does not match its bullets, and D4 is unmapped.**
   `corpus/QUALITY.md:77-78` cites "routed notes 2–4"; the section actually
   encodes notes 1–3 and has no SHONEN rule. Either change the grounding to
   "routed notes 1–3" and keep D4 in the lesson/report, or add a fourth bullet
   (e.g. "SHONEN boxes are author assertions until a named non-author verifier
   checks them; no promotion is claimed"). Do not leave a grounding pointer that
   claims coverage it does not provide — it is the same chronology/grounding
   class the new criterion is about.
2. **Draft lesson under-specifies two contract clauses.** `round-22.md:73-75`
   says "SHONEN not independently checkable" and "No protected verifier or
   aggregator file is writable here." The contract says "no SHONEN promotion"
   and "Do not edit protected verifier or historical lesson/knowledge bytes."
   Recommend exact wording: "SHONEN boxes remain unchecked; the four r21 `[~]`
   lines are author assertions; promotion remains operator-owned" and "no
   protected verifier, aggregator, or historical lesson/knowledge byte was
   edited this round." "Writable" is a permission property, not an edit record,
   and it drops the historical knowledge/lesson clause.
3. **Gate row cites prospective artifacts.** `SKILL.md:411` pins
   `.ufo/waves/round-22/cases.json`, `frozen/expected.json` and `replay.py`.
   At observation `replay.py` exists untracked; `cases.json` and
   `frozen/expected.json` do not. Land the row in the same commit as those
   artifacts (and `measure.py`/`matrix.py`), or the registry describes files
   absent at the cited revision — the pre-claiming defect `CapabilityNotFreshness`
   already names.
4. **Do not treat the r21 receipts as base-revision measurements.** Both were
   taken at `df6196b`; base is `7c61c8c`. The contract carries the debt, so the
   mapping is safe, but any report line that says "at base" must either cite the
   contract or a fresh run. If re-run, the base adds the verifier lesson and its
   two resolving cites; record the new `filesScanned` and do not compare the
   number to 50 as if unchanged.
5. **Sequencing for the new criterion's own grounding.** `QUALITY.md` cites
   `corpus/lessons/round-22.md §Mistakes`, which did not exist at base and is
   untracked now. Commit the lesson and the QUALITY section together so the
   criterion's cited source resolves in the landed tree. The same commit should
   carry `static-canonical-preflight.md`, the SKILL row and the SOURCES rows.
6. **Keep the old-Gate coordinates untouched.** The verifier's
   `round-4.md:50`, `round-9.md:185`, `round-16.md:171` pointers do land on the
   read-time absence statements (Gates open at 44/68/78). No coordinate erratum
   is needed; any r22 correction register must not "fix" these files or claim
   their chronology was repaired. `QUALITY.md:83-84` correctly says they remain
   superseded only by the r21 register.

---

## 6. Falsifiable anti-relabel checks for the r22 integration

These are proposed checks, **not executed here**:

1. `git diff --name-only <base> <measured>` intersects
   `corpus/knowledge/freshness-pins.json`, `scripts/freshness-sweep.mjs`,
   `.ufo/waves/round-21/anchors*`, any `*-verifier-spotcheck.md`, any
   `*-aggregator-*` lesson, and every pre-existing `corpus/knowledge/*.md` /
   `corpus/lessons/round-*.md` → must be empty (new r22 files excepted).
2. `measure.py --root . --revision <tip>` reports `total: 32` only from
   `contract.matrixCases`; `accepted` counts only cases whose observed exit
   **and** finding id both equal the frozen expectation; baseline run reports
   `accepted: 0`, `available: false` and exits 0 by design.
3. `canonical_audit.py --json` output schema contains no `paths`, `anchor`,
   `missSet`, `freshness` or `shonen` keys; findings use only the ten contract
   ids; no finding id or page comes from an inherited debt surface.
4. `grep -nE 'paths.*(clean|pass|resolved)|anchor.*(pass|0 diagnostics|green)|SHONEN.*\[x\]|promot'`
   over the round-22 report, lesson, SCORECARD diff and LOG entry returns only
   explicitly negated statements ("remains red", "not a gate", "no promotion").
5. The SKILL `canonical-audit` row's frozen-proof cell paths all exist at the
   measured revision, and `replay.py` fails when one fixture byte is flipped.
6. A report sentence mentioning freshness either says "unchanged" with the D1
   counts, or is absent; no r22 score row changes the freshness score/verdict.

---

## 7. Residual unknowns

- I did not run `freshness-sweep.mjs`, `anchor-census.mjs`,
  `canonical_audit.py`, `matrix.py`, `measure.py`, `replay.py` or any selftest;
  all red/green statements above come from committed r21 receipts, the
  contract, and file reads.
- Whether the in-flight L1 edits (`SKILL.md`, `QUALITY.md`, `README.md`,
  `SOURCES.md`, the new knowledge/lesson files) land byte-identically, and
  whether the four dead scribe seats leave unreachable gaps elsewhere.
- Whether the paths gate's base-revision counts differ from `df6196b`
  (static inference says only resolving cites were added; unmeasured).
- Whether L1 will adopt the exact contract wording for SHONEN and protected
  bytes (defect 2), or leave the softer paraphrase.
- No independent admission is claimed or possible from this seat; all findings
  are author-side evidence for L1 and the non-author closure.

No tool was installed or upgraded. This report is the only file written by this
seat.
