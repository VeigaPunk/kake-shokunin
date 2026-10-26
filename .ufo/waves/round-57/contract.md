# Kake round 57 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, = `BASE_REV` in the counters):
`28fa0b23e699303725aba2727094531f5e44494d`. This file, `contract.json`, the three counters, their base-control receipts, the retained
source bodies with receipts and the pre-append registry mirror are committed together before any build edit and before any seat
scores. The predicate sentence of each claim is the same sentence here, in the counter's code and in every receipt label. Round date
2026-10-25. Round shape: two v1 waves (W1 build + pre-data attacks, W2 falsify), 64–100 seats in total; the L1 holds the canonical
planner seat (the validator rejects `planner`); seats are read-only except their own report file (and a `<Seat>.files/` directory
beside it for candidate code). Receipts are never rewritten: a re-run lands under a new file name (see C1).

## Axis declaration

The prompt-declared lane axes are operability + freshness; the lane scorecard also carries the round-54 bounded sub-axis
**calibration** (score 1, the lowest-scoring non-retired axis, so the lowest-axis obligation lands on C1). Rounds 55–56 recorded the
ownership question (calibration vs operability) as open for the operator; it stays open and is restated in the report. Three claims on
three distinct axes: C1 calibration, C2 operability (capability acquisition), C3 freshness (sourced). No exploratory claim.

## Claim C1 — calibration: stated revision pins against the pins the receipts carry

Surface: measurement receipts under `.ufo/waves/round-5[2-7]/{control,controls}/` that carry a `revision:`/`revision=` line, and the
report/SCORECARD statements "measured at <rev>". Observed state: the committed history of each receipt. Round-56 routed defect 1
(`corpus/lessons/round-56-verifier-spotcheck.md` §6): the round-56 `after-*` receipts were committed naming `f8438a28…` and a later
commit rewrote the line to `4cb225fb…` without a re-run, so the report's "After (`4cb225fb`)" column was not a run over that revision.
- Before (base): 6 relabels in rounds 52–56 history are undisclosed (`controls/base-c1-receipt-pins.txt`: round-52 `c1-ledger-real.txt`,
  `c2-quote-real.txt`; round-55 `after-c1-readme-index.txt`, `after-c2-quote-truth.txt`; round-56 `after-c1-selftally.txt`,
  `after-c2-quote-truth.txt`), no round-57 receipts, no pin file.
- After: every historical relabel is disclosed by `receipt-errata.json` with the four true values (path, from, to, commit) and the
  counter finds git agrees (no phantom entry); the three round-57 receipts `controls/after-c{1,2,3}-*.txt` each carry the one revision named
  in `measured.json`, that revision is a strict ancestor of the commit that introduced the receipt, none is ever rewritten, and the
  round-57 SCORECARD section names the measured revision.
- Counter: `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root <lane> --revision <tip>` (tip = the lane revision that holds the
  receipts; the measured revision named in `measured.json` is earlier, so the receipts can be committed after the run).
- Predicate (frozen): **met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1**
- Kill rule: exit 0 iff met; 1 not met; 2 evidence unevaluable; 64 usage.
- Do-nothing control: at base the counter prints `undisclosed_relabels=6 … new_receipts=0 scorecard_pin=0 met=False`, exit 1
  (`controls/base-c1-receipt-pins.txt`).
- Junk controls (selftest, 19 checks at version 1): undisclosed relabel; errata naming nothing git shows; errata with a wrong `to` or
  commit; deleted receipt; relabelled round-57 receipt; missing claim-3 receipt; wrong, non-ancestor, own-commit-free and double
  revision lines; mismatching `measured.json`; SCORECARD without the pin; unparsable errata; `=` form; pin-keeping edits; stripped pin
  line; rounds outside 52–57.
- What the counter does not test: that a counter was actually run at the pinned revision (it certifies the pin's consistency with
  history, not the run); receipts outside the `control(s)/` directories of rounds 52–57; relabels in report prose.

## Claim C2 — operability (capability acquisition): cross-registry source-id resolver

Surface: a new tool, `scripts/id_resolver.py` (considerthese proposal 2, `considerthese/2026-10-25.md`): lists every `S###` id cited in
`corpus/knowledge/**/*.md` that does not resolve in the lane's registry and names the sibling registry that holds it. The round-52
state it must catch is real: at lane revision `3994101` five ids (S367 S372 S373 S390 S409) resolved only in kotodama-shokunin.
- Before (base): `scripts/id_resolver.py` absent; the gate prints `0/5`, exit 1 (`controls/base-c2-idresolver.txt`).
- After: the gate's five conditions pass (G1 tool present; G2 selftest N/N with N >= 16 in a clean clone; G3 gate-owned fixture exact
  output; G4 red-before over `3994101` finds exactly the five ids, each owned by kotodama-shokunin; G5 green over the measured
  revision, dangling == 0 with ids_cited >= 100). The capability row enters the SCORECARD capabilities table in the same round.
- Counter: `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root <lane> --revision <rev>`; CLI contract in the counter's docstring.
- Predicate (frozen): **met: gate_conditions_passed == 5 of 5**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: at base `0/5`, exit 1. Junk controls: a tool that prints constants fails G3 (the fixture is gate-built and
  contains an indented row, a four-digit id, a two-sibling id and decoys) and G4; a tool that always prints `dangling=0` fails G3/G4; a
  tool that reads the working tree instead of the revision fails G4 (the red-before ids are absent at the tip).
- What the counter does not test: sibling registries are read live (their HEAD), so G4's owner column is as of the run (rows are
  append-only, CORPUS rule 2); the resolver checks id resolution, not whether a cited row supports the sentence citing it.

## Claim C3 — freshness (sourced): two Baidu dead-link entries, quote-true

Surface: per-engine crawl hygiene (PROVINCE.md round-52 frontier ground) — what Baidu's own pages say a dead link is and how its crawler
treats one; the cross-engine counterpart of the Yahoo! JAPAN deleted/non-existent-URL entries (S419/S420) and the Google status-code
entries. Assimilation theme from `merge/kake/` (shokuknow, read-only), two staged entries re-grounded in-round: staged `baidu-dead-link-taxonomy`
(row staged S403, page `ziyuan.baidu.com/college/articleinfo?id=3458`) -> lane row **S421**, entry `baidu-dead-link-types.md`; staged
`baidu-spider3-dead-link-recognition` (staged S408, `ziyuan.baidu.com/wiki/867`) -> lane row **S422**, entry
`baidu-spider3-dead-link-model.md`. Lane filenames differ from the staged names on purpose (condition C1 refuses the staged names:
the entries are written from the retained pages, not copied).
- Before (base): 0 of the 2 entries exist; registry 158 rows; no retained bodies for S421/S422 in the lane's evidence.
- After: the 2 entries exist with provenance headers and quote-true spans; registry 160 rows; both rows new, `mined`, used-by = their
  entry; the append was census-validated on a scratch mirror first.
- Counter: `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root <lane> --revision <rev>` (conditions C1..C8 are the round-56
  version-2.1 conditions; generated by `derive_c57_quote_truth.py`; the article block and page-identity locators are Baidu-specific).
- Predicate (frozen): **met: conditions_passed == 8 of 8**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: at base `0/8`, exit 1 (`controls/base-c3-quote-truth.txt`).
- Quote ceiling: every Gate quote and quoted entry span is <= 25 units (one per CJK character) and <= 40 characters.
- Selftest: version 1 ships a stub (`--selftest` exits 2); wave 1 ports the round-56 fixtures to the round-57 rows and the L1 integrates
  them before measurement.
- Sourced claim: C3 rests on two rows opened this round (S421, S422), retained bodies under `sources/` with sha256 receipts
  (`sources/receipts.json`, fetched 2026-10-25 UTC).
- What the counter does not test: quote truth is substring truth, not support or rendering fidelity (reviewers and critics judge those);
  C7 is a receipt of agreement, not proof the census ran; the dead-link *definitions* are the operator's text as quoted, and the entries
  state no measurement of any property.

## Pre-dispatch note (before any seat is dispatched)

`c57_idresolver_gate.py` gained an optional `--fleet <fleet root>` argument (default: the parent of `--root`, the previous behavior) so a
scratch clone can name the real fleet. No condition, expected value or predicate changed; the base control is unchanged (`0/5`, exit 1).

## Assimilation and considerthese ledger

- Theme: Baidu dead-link handling from `merge/kake/` (two entries). Id lists `assimilation/reg-ids` (158), `assimilation/staged-ids` (129),
  `assimilation/collisions` (8: S312 S329 S367 S372 S373 S374 S390 S409 — documents already held; neither adopted id collides). Renumber
  map by document: staged S403 -> lane S421, staged S408 -> lane S422 (next unused ids after S420). Guard proof: `assimilation/guard-proof/`
  carried from round 56 (unchanged guard; wave 1 re-proves it).
- Quarantine slice (12 rows, `assimilation/quarantine-slice`): no staged row adopted from it; wave 1 scouts hand-check each row and the
  verdicts land in the lesson (not a claim; an honest partial list keeps adoption of those rows closed).
- Considerthese: proposal 2 of `considerthese/2026-10-25.md` (cross-registry id resolver) is C2; proposal 1 landed in round 56; proposals 3
  (non-Latin locator sample) and 4 (frontier ground map, landed r55) are not taken (at most one per round).

## Maintenance (not claims)

- Round-56 routed defect 1 is C1; defect 2 (S388 reject reason: the page says the tag is a shared specification for Yahoo!, Google and
  Bing — state what the page does say) becomes a QUALITY falsifier "a rejection reason is re-read against the page before it is logged"
  and is applied to this round's rejects; defect 3 (disclosed limits stand) is carried; defect 4 (SHONEN) is reported as `[ ]` with
  the reason.
- Frontier step: census before/after, one mined mistake, sourced claim — in `corpus/lessons/round-57.md`.
- Tool installs: none planned.

## Counter versions (appended after wave 1, before any claim was measured)

Contract commit `b9a5d012f7fd` froze all three counters at version 1 and the predicate sentences, which are byte-identical in `contract.md`,
`contract.json` and each counter since (`w1/CriticControlsSizing.md` re-checked all five locations per claim). Wave 1 attacked the counters
before any claim scored: `w1/CriticC1Counter.md`, `CritCheatC1.md`, `MutC1Pins.md`, `ReviewerPinsCode.md`, `ExecPinsIndependent.md` (C1);
`CriticC2Gate.md`, `CritCheatC2.md`, `ReviewerGateCode.md` (C2); `CriticC3Counter.md`, `CritCheatC3.md`, `ExecC3Selftest.md` (C3);
`CriticControlsSizing.md`, `CriticAxisClaim.md` (all). Every do-nothing and junk result below was *measured by a seat on version 1*, so the
base controls of version 1 are history and version 2 re-states them (`controls/base-c*-v2.txt`).

- **C1 version 2** (`c57_receipt_pins.py`). Version 1 was met by three bare `revision:` receipts plus errata transcribed from the counter's own
  output (`CritCheatC1` exp 2/2b, `CriticC1Counter` A1), by a negating SCORECARD sentence, by a merge-shaped relabel, by a history replaced
  by an orphan commit, and its pin rule was self-contradicting: the C1 receipt could only honestly record the pre-receipt state at any revision
  it admitted (`CriticC1Counter` S0). Version 2: the measured revision must descend from the commit that added the counter; receipt **bodies**
  are read (after-c2 and after-c3 must start with their counter's `met=True` report line with the frozen predicate sentence and carry
  `EXIT=0`; after-c1 must carry `tip: <T0>` and start with the report line this counter re-derives for T0 — a commit that already holds all
  three receipts, descends from the measured revision and is a strict ancestor of the commit that last wrote the body — so the C1 receipt is a
  *run at T0* pinned to the measured revision); one receipt per claim and no other `after-*` file; the history walk covers the whole ancestry
  (topological, renames followed, merges seen); a stripped or deleted-and-re-added pin is a relabel; deletions count only when the path
  vanished; quoted JSON `"revision":` keys are read and the mutation-ladder JSON (embedded old tails, not a measurement pin) is excluded;
  inputs are validated (malformed errata or `measured.json` is exit 2, not a traceback); the SCORECARD pin is a labelled `Measured revision:
  <40-hex>` line and every such line in the `## Round 57` sections must equal the measured revision; the base revision must be an ancestor of
  the tip. The population is 44 receipts at the base (45 files, one excluded). Base control re-run: `undisclosed_relabels=6`, exit 1
  (`controls/base-c1-receipt-pins-v2.txt`). Selftest 19 → 48 checks (`controls/c1-selftest-v2.txt`), including the mutants that survived
  `MutC1Pins` (non-claim round-57 receipt, rounds 52–55, merged sides, re-add) and CLI exit codes.
- **C2 version 2** (`c57_idresolver_gate.py`). Version 1 was met by a 10-line constant printer (`CritCheatC2`), a 21-line stub
  (`CriticControlsSizing`), and rejected a correct tool non-deterministically (unsorted owners; `CriticC2Gate` F1). Version 2 makes the gate a
  differential test: a reference implementation of the documented rule over randomised fixtures (fresh nonce, ids, names, indentation 0/2/3/4, a
  CRLF registry, a sibling without a registry, CJK-adjacent ids, ranges, decoys) and over the real revisions (`3994101`, the measured
  revision); the tool's lines, summary identities and exit must equal the reference's; set-valued fields compare as sets; `PYTHONHASHSEED=0`;
  live sibling ownership must equal a committed snapshot (`sibling-snapshot.json`) or the gate is *unevaluable* (exit 2), never "not met".
  The boundary rule is stated once: not preceded or followed by an ASCII letter, digit or underscore. Measured against the wave-1 candidate
  tool: 5/5; against a constant printer: 3/5 (G3, G4 fail).
- **C3 version 2** (`c57_quote_truth.py`, generated by `derive_c57_quote_truth.py` + `derive_c57_selftest.py`). Version 1 reached 8/8 from 13
  junk files (`CritCheatC3`), from quotes of sidebar markup and a `<style>` block (`CriticC3Counter` A1), and its receipt pin was circular (body
  and receipt rewritten together). Version 2: both retained bodies are pinned by sha256 in the counter (the digests frozen at the contract
  commit); a span qualifies only inside a *text node* of the article block (tags, attribute values, `<style>` and `<script>` are not text), with
  S421's block ending at the promo block and S422's starting at the byline; the row title must equal the page `<title>` text before the site
  suffix (6+ units); the row anchor heading is 4+ units, page-unique and inside a text node; the printed date is read in a text node, and the
  page's own fullwidth-colon form is accepted in the row; every Gate-line span (not only 6+ units) is checked against both ceilings; the
  sibling set for page-uniqueness is the two adopted bodies, not the live `sources/` directory. Selftest 0 → 101 checks (the wave-1 port of 93 plus
  8 version-2 fixtures), `KAKE_R57_SELFTEST_REV=b9a5d012f7fd`.
- **Receipt discipline for this round** (the substance of C1): no committed file under `controls/` that carries a `revision:` line is ever
  rewritten; a re-run lands under a new file name. The version-1 base receipts (`base-c1-receipt-pins.txt`, `base-c2-idresolver*.txt`,
  `base-c3-quote-truth.txt`) stay as history.
- **After-state wording.** The C1 after-state's "none is ever rewritten" is read as "up to the measured tip" (a counter at one tip bounds history
  only up to that tip); "every historical relabel is disclosed" is read as "every relabel the counter enumerates": receipts under
  `.ufo/waves/round-5[2-7]/control(s)/` carrying a 40-hex `revision[:=]` line, whole ancestry, renames followed. Report prose is outside it.
  C2's "lists every cited id" is what G3's reference comparison tests on gate-built fixtures and G5 on the measured revision; the SCORECARD
  capabilities row is checked by reading, not by the gate. C3's "census-validated first" is C7's receipt, not proof that the run happened.
- **Not acted on (disclosed).** C1 still cannot prove a counter ran at the pinned revision beyond re-deriving its own report line at T0 and
  checking the other two receipts' first lines; a hand-written `C2 ... 5/5 met=True` line with the right pin passes the C1 body check (the C2
  claim itself is verified by the gate, not by C1). C3's quote check certifies text nodes of the article block, not support or rendering
  fidelity. C2's G4 depends on the live siblings through the snapshot.
- **Axis note.** `w1/CriticAxisClaim.md` was read; the declarations stand (see the report's axis note).
