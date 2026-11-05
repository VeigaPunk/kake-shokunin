# ConnectorScope — round 96 seat report

Seat: ConnectorScope (connector, leaf member, read-only). Wave: round-96 w1. Lane: kake-shokunin.
Deliverable: `overlaps96.md` (same directory). Verdict line: `CONNECTOR overlaps=12 contested=8`

Path note: the seat spec names `.ufo/waves/round-96/w1/ConnectorScope.md`. The hard bounds limit writes strictly to `.ufo/waves/round-96/w1/ConnectorScope/`, so this report and `overlaps96.md` are written here. The L1 should move or re-point the Report trailer.

---

## 1. Scope and What Was Read

Target: sibling overlap scan (read-only) for the revalidation-exchange surface and the kill-predicate fleet decision evidence (R95-2).

Instrument digests verified before reading (`sha256sum`, rc 0):
- `c96_selfassess.py` = `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134` (match)
- `c96_reval.py` = `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9` (match)
- `c95_selfassess.py` = `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` (match)

Sibling files opened (committed bytes, read-only at current sibling HEADs):
- `tabi-shokunin` (`58d84eda`): `SKILL.md` (lines 374, 403, 423, 433, 889, 891, 1052, 1146, 2627), `corpus/knowledge/network-evidence-rung.md`, `corpus/knowledge/multi-step-journey.md`, `corpus/knowledge/async-step-evidence.md`, `corpus/knowledge/carried-debt-closure-r8.md`, `corpus/knowledge/layer-routing-synthesis.md`, `corpus/evidence/w4-t41-network/`, `corpus/evidence/round-31/decision-table/bytes/S122.html`, `scripts/check-selfassessment.mjs`, `scripts/check-gate-mutants.mjs`, `scripts/gate-mutants.json`, `scripts/check-measurement-binding.mjs`, `scripts/check-freshness.mjs`.
- `kumitate-shokunin` (`0bff4bab`): `corpus/knowledge/receipt-age-on-the-compare-path.md`, `corpus/lessons/round-38.md`, `corpus/knowledge/distill-and-l3.md`, `scripts/gate-mutants.mjs` (K43 kill predicate), `scripts/counter-pins.mjs`, `SKILL.md` (lines 617, 735).
- `kotodama-shokunin` (`d41eb594`): `corpus/knowledge/verification/gate-frozen-run-standard.md`, `tools/check-gate-battery.py`, `corpus/SOURCES.md` (S304).
- `chousa-shokunin` (`378fda82`): `corpus/QUALITY.md` (criterion 146 verified at line 1054), `corpus/SOURCES.md` (S025 rejected), `corpus/evidence/round79/selfcheck-v2.py`, `corpus/evidence/round62/controls/null-counter.py`, `tools/quote-reopen.py`, `SKILL.md` (lines 91–92, 175).
- `souji-shokunin` (`8b393b19`): `corpus/lessons/round-9.md` (line 14), `corpus/README.md`, `corpus/SOURCES.md`.
- `kake-shokunin` (`049e8eca`): `.ufo/waves/round-96/freeze.md`, `reval-contract-v1.md`, `.ufo/waves/round-95/w1/ConnectorScope/overlaps.md`, `corpus/lessons/round-95.md`, `corpus/lessons/round-95-verifier-spotcheck.md`, `SCORECARD.md`.
- Fleet root: `.ufo/l0-questions.md` (line 363), `PROTOCOL.md` (§Gate standard).

---

## 2. Findings

### (1) RFC 9111 §4.3 / Revalidation / 304 Handling Surface Scan
- Command executed across all sibling lanes:
  `git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin grep -il 'revalidat\|304\|if-none-match' HEAD -- corpus/ SKILL.md`
- **Result:**
  - `tabi`: Observes live browser CDP Network events (wire 304 vs client 200) in loopback tests (`run6-reval`, `network-evidence-rung.md`, `SKILL.md`), but explicitly records at `SKILL.md:891` that protocol semantics remain unexamined ("why client status reads 304 only for the revalidated style.css ... still unlanded"). Verdict: **PROVINCE-LOCAL**. Holds no §4.3 decision ground.
  - `kumitate`: Cites RFC 9111 §4.2.3 and mentions §4.3.4 in `receipt-age-on-the-compare-path.md` solely to contrast HTTP cache age-updating with kumitate's local static snapshot age gate (`omp-census.mjs --max-age`). Verdict: **PROVINCE-LOCAL**. Holds no §4.3 decision ground.
  - `kotodama`: All hits are source S304 (Pazuzu) or general linguistic/worldbible validation. Verdict: **PROVINCE-LOCAL** (lexical non-overlap). Zero HTTP content.
  - `chousa`: SOURCES.md row S025 explicitly REJECTED RFC 9111 in round 25 ("REJECTED: a standard for HTTP-cache freshness, not authority for research-record validity"). Other hits are dates, street addresses, or page ranges. Verdict: **PROVINCE-LOCAL** (lexical non-overlap). Zero HTTP content.
  - `souji`: `round-9.md:14` touches git worktree revalidation under git 2.55; other hits are commit hex hashes containing `304`. Verdict: **PROVINCE-LOCAL** (lexical non-overlap). Zero HTTP content.
- **Fleet Boundary:** Kake's C2 instrument (`scripts/reval_exchange.py`, `reval-contract-v1.md`, scored by `c96_reval.py`) is the **sole capability in the fleet** deciding the RFC 9111 §4.3 revalidation exchange over supplied values.

### (2) Refresh of R95-2 Evidence & L0 Question Draft
- Re-verified at current sibling HEADs (`kumitate` `0bff4bab`, `tabi` `58d84eda`, `kake` `049e8eca`):
  - `kumitate`: K43 kill predicate in `scripts/gate-mutants.mjs` requires immediate rerun stability with identical sorted failing case names. Equivalence is unrepresented.
  - `tabi`: `scripts/check-gate-mutants.mjs` and `scripts/gate-mutants.json` partition mutants at catalogue authoring time into `fault` (must be killed) and `benign` (must survive as semantic equivalence). Rerun stability is not checked.
  - `kake`: `c96_reval.py` and `c95_conditional.py` evaluate frozen mutant populations against input spaces; surviving mutants require empirical digest-pinned equivalence receipts across all inputs (R94-4/R95 M11 precedent), with round 96 freezing `mutants=14/14 with no survivor`.
- The three fleet defaults remain conflicting.
- **Verbatim-Ready Two-Sentence L0 Question Text:**
  ```text
  Fleet mutation testing defines 'killed' across three conflicting lane defaults: kumitate's K43 requires immediate rerun stability of failing case names, tabi declares equivalence at catalogue authoring time via a fault/benign partition, and kake requires digest-pinned exhaustive input-equivalence receipts for surviving mutants. Should the fleet establish a unified mutant-kill standard across lanes, or should individual lanes continue to govern equivalence and rerun discipline under local provincial contracts?
  ```

### (3) Confirmation of Chousa Criterion 146 (R95-3 Citation)
- Read-only check at current chousa HEAD `378fda82dc2cbcc555a0565052cc408121813cef`:
  - Path: `corpus/QUALITY.md`
  - Line number: `1054`
  - Heading: `146. **A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.**`
- Line number 1054 confirmed; accurately cited by kake C1's QUALITY criterion as prior art for the repair-naming rule.

---

## 3. Sibling Overlap Counts

Refreshed 12-row overlap table delivered in `overlaps96.md`:
- Total overlap candidates: **12**
- Contested: **8** (rows 1, 2, 3, 4, 5, 6, 7, 9)
- Province-local: **3** (rows 10, 11, 12)
- Fleet-standard: **1** (row 8)

**Verdict line:**
`CONNECTOR overlaps=12 contested=8`

---

## 4. Checks and Receipts

- `sha256sum` on `c96_selfassess.py`, `c96_reval.py`, `c95_selfassess.py` — rc 0, exact match with `controls/instrument-sha256.txt`.
- Read-only sibling git commands (`git -C <lane> rev-parse HEAD`, `git -C <lane> grep -il …`, `git -C <lane> show HEAD:<path>`) executed across all 5 sibling lanes with rc 0.
- No counter executed. No sibling file written. No mutating git or jj commands executed anywhere.
- Scratch directory `/fast/scratch/hyaku/kake-r96/ConnectorScope/` created, cleaned and deleted prior to yield.
- Tooling: zero tools installed or upgraded; pacman pause respected.

---

## 5. Verdict

`CONNECTOR overlaps=12 contested=8`
