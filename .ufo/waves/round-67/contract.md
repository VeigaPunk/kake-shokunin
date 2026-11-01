# Round 67 contract — kake (frozen before any after-state measurement)

Base (round-66 verifier spot-check tip, pushed): `6ff73edd1bac66c298e10e6f0f295088740c32b9`.
Host: Windows, python 3.13.15 (`python`, no `python3`), node 24, git 2.55. Frozen
before any claim's after-state exists. Receipts live under
`.ufo/waves/round-67/controls/` (claims) and `.ufo/waves/round-67/probes/`
(freshness probes). Every count below carries its counting command.

## Claims

### C1 — calibration (lowest owned non-retired axis, score 2): the six carried live-red registry rows adjudicated with revision-pinned receipts

Before-state (measured, receipt to be committed as
`controls/c66-before-r67.txt`): `python -B .ufo/waves/round-66/c66_gate_status_hostportable.py
--root . --revision 6ff73edd… --jobs 6` at the round base prints the round-66
state: `members=28 evaluated=28 structural=0 agreement=17 scores_held=3/3`,
with exactly these six live-family MISMATCH rows (line citations from
`controls/after-c66.txt`, r66): c56_selftally e_T=2; c57_idresolver_gate,
c58_receipt_rewrites, c58_resolver_cases, c59_axis_evidence, c59_resolver_cases
each e_T=1. Before-state ledger wording: `grep -c "not adjudicated here\|candidate
mechanism" corpus/knowledge/gate-status-ledger.md` = 5.

Frozen decision rule — each of the six rows ends the round in exactly one of
three dispositions, each with a committed receipt naming the exact command,
revision(s), stdout/stderr digest and exit:

- **(a) relabel live→historical** — allowed ONLY if the documented command was
  RUN this round, on this host, at the recorded pin revision and exited 0
  ("a pin is a revision the command was run at, never a remembered one"), AND
  the red-at-tip mechanism is world-growth (its frozen predicate pins a
  round-era input a later round legitimately changed). The Kind cell gains the
  word `historical` plus that pin; the ledger row is updated with the receipt
  pointer; SKILL.md line count stays 1377 (in-place cell edit, no line
  insertions above sidecar-bound line 935).
- **(b) disclose-and-stay-live** — if the row is red because a real
  disclosure debt exists (the counter documents the debt class), the debt is
  disclosed append-only per the counter's own documented rules, the command is
  re-run and must exit 0 at tip; the row stays live.
- **(c) carry-with-proven-mechanism** — if the row is red for a host-intrinsic
  or frozen-byte reason, the direct run's output is receipted and the
  mechanism is stated in the ledger row from evidence in that output (not
  guessed); the row stays live-red and carried. This replaces a
  candidate-mechanism wording with a proven or refuted one, receipted.

Kill rules (any → C1 fails):

- K1: any relabel whose pin run is not executed and receipted this round.
- K2: any green claimed without the row's documented command exiting 0 at the
  recorded revision, or any mechanism asserted without committed output
  evidence.
- K3: the c66 counter after-state shows `structural > 0` or `evaluated < 28`
  or `scores_held < 3` (the counter itself must stay conformant).
- K4: SKILL.md or SCORECARD.md edits that shift any sidecar-bound line
  (SKILL.md bound lines ≤ 935; line count must stay 1377 after in-place edits
  and end-of-file section additions) — the offline §paths sweep must still
  exit 0 after the sanctioned pins re-measure.
- K5: `agreement` is REPORTED, never gated: this claim does not promise a
  target agreement number. A round that ends with agreement still 17 is
  admissible if every row carries an honest disposition receipt (the
  falsifiable delta is the adjudication receipts, not the count).

Counting commands: the c66 counter line (before/after); `grep -c "not
adjudicated here\|candidate mechanism" corpus/knowledge/gate-status-ledger.md`
(before 5 → after: only rows honestly still carried, each with a proven-or-
corrected mechanism receipt); `ls .ufo/waves/round-67/controls/ | wc -l`.

Do-nothing control: at base all six rows are carried with unproven or
candidate mechanisms and zero round-67 receipts exist; a control reaches none
of the three dispositions.

### C2 — operability (10, HOLD): the c66 host-portable gate-status counter gets its SKILL.md registry row (the r66 routed "next round's first registry item")

Before: `grep -c "c66_gate_status_hostportable" SKILL.md` = 0. After: ≥ 1 — a
well-formed registry row (Name | Kind | Entry command | Verdict map | Self-test
| Pinned values / frozen proof | Write scope | Owner) appended in a new
`### Round 67 gate registry additions` section placed BELOW every sidecar-bound
SKILL.md line (bound max 935), with this round's measured evidence in the
Pinned-values cell. The row is outside the c66 population regex
(round-48..59 twice-N), so `members` stays 28 and `structural` stays 0 (K3 of
C1 guards this). No frozen counter bytes change.

Counting command: `grep -c "c66_gate_status_hostportable" SKILL.md` (0 → ≥1);
`grep -c "^### Round 67 gate registry additions" SKILL.md` (0 → 1).
Do-nothing control: the row does not exist at base (grep 0).

### C3 — freshness (10, HOLD): the two .kimi.pro standing-status surfaces date-stamped on this host (the r66 "un-probed twins" debt)

Standing records (population, frozen from the corpus as of base):
`ufo-fsd.kimi.pro` (SKILL.md property table: "612B SPA shell"; property-map
checks c49/c50) and `plazir27.kimi.pro` (PQ-1 drift row; PQ-6: 302 → Kimi
static preview-404, 5,995B, confirmed 09-28; property-map:c56 STALE correction
2026-10-21). Before: `grep -c "r67 dated" corpus/knowledge/publish-queue.md` = 0;
no this-host dated probe receipt exists for either surface (the r66 probe
receipt covers .kimi.page only). After: one GET-only probe per surface,
receipted under `probes/` (named `probes/<host>.body` + `probes/receipt.json` —
the r66 name drift is not repeated), with sizes/sha256/redirect chain recorded
and dated corrections appended to `corpus/knowledge/publish-queue.md`; each
corpus record is either confirmed or flagged stale with the dated evidence.

Kill rules: any non-GET request; any publish/deploy/state-changing action; any
body bytes treated as byte-identical without sha256 evidence (cfemail-variance
surfaces get size/shape verdicts only, per the r65/r66 rule).

Counting command: `grep -c "r67 dated" corpus/knowledge/publish-queue.md`
(0 → 1 section) + receipt files exist (`git cat-file -e`).
Do-nothing control: no receipt exists at base (absence is the before-state).

## Carry-in corrections from the r66 non-author closure (protocol work, no score credit)

- **D1 receipt-name drift:** the frozen r66 contract names
  `controls/selftest-after-c2.txt` / `sources/s133-receipt.json` /
  `probes/<name>.txt`; landed as `controls/selftest-sweep-after.txt` /
  `sources/receipt.json` / `probes/<name>.kimi.page.body` + `probes/receipt.json`.
  Fix: append-only erratum + name map appended to
  `.ufo/waves/round-66/contract.md` (recorded lines untouched), referenced from
  the round-67 lesson.
- **D2 no-harm overstatement:** `controls/noharm-final.txt` line "zero deleted
  lines anywhere" is true only for its five-file numstat; whole-tree base..tip
  also has `corpus/knowledge/freshness-pins.json` −6 and
  `corpus/knowledge/freshness-sidecar.json` −273 (JSON re-serialization,
  standing entries preserved field-for-field — r66 verifier §3.2) and
  `scripts/freshness-sweep.mjs` −3 (the repair itself); re-measured this round:
  `git diff-tree -r --numstat 6a2ecb1… 1772f82c…`. Fix: scoping erratum appended
  to the receipt (append-only; recorded lines untouched).
- **D3 ledger provenance trio:** `corpus/knowledge/gate-status-ledger.md` lacks
  the CORPUS-required `source:` / `verified-at:` / `recheck:` opening trio.
  Fix: prepend the trio (in-file format fix, sanctioned by the r66 verifier §7.3
  as "a fix of format, not a rewrite of claims"); all claims/rows untouched.

## No-harm (frozen for the round)

- `corpus/SOURCES.md` bytes untouched (registry stays 171 rows; counting
  command `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).
- Every frozen round-48..59 counter file byte-untouched; the c66 counter bytes
  untouched; `scripts/freshness-sweep.mjs` untouched.
- Frozen r60..r66 instruments/receipts untouched (append-only errata to round-66
  artifacts are the sanctioned exception, per D1/D2 above).
- No publishing or deploy action; all probes GET-only. No tools installed.
- The offline sweep (`node scripts/freshness-sweep.mjs --offline`) must exit 0
  at round end; if this round's new committed citation paths grow the cited/file
  sets, the pins are re-measured from the sweep's own JSON exactly as in r66,
  and the added set must equal exactly the paths this round's receipts name
  (boundary check, K2-style).
- SCORECARD.md: append-only settlement below its current content (unbound by
  the sidecar); axis scores operability 10, freshness 10, calibration 2 do not
  move (HOLD round); no capability row is claimed.

## L2 wave

No dispatch surface exists on this host (L0 questions by kake round-65 and five
other lanes stand open, routed around, never treated as answered); the round is
L1-only, disclosed in the report. The non-author closure remains the outside
check.

## Amendment 1 (2026-11-01, recorded before the SOURCES edit lands — no claim data touched)

The no-harm clause "corpus/SOURCES.md bytes untouched" was over-broad as frozen: the
rendered round contract §2b requires SOURCES curation and a claim resting on a row
opened this round. Corrected to: SOURCES.md is append-only this round — exactly one
new row (S434, opened before the row is written) and one re-open (S133, bytes of
existing rows untouched); registry 171 → 172. All other no-harm clauses unchanged.
