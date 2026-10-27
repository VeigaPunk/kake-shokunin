# ReviewerC1Contract

Scope: claim C1 (calibration) in `.ufo/waves/round-59/contract.md` vs `AXES.md` (calibration
definition), `MISSION.md`, and the prompt rule "a calibration claim must count mismatches between the
lane's self-assessment (SCORECARD/SHONEN) and observed repo state". Method: read-only review of the
frozen contract + counter; fixtures in a `--shared` scratch clone under
`/fast/scratch/hyaku/kake-r59/ReviewerC1Contract/`, committed as `selftest`; all counter runs against
the **contract-pinned v1 blob** (sha256 `95d23511…`, identical at 45a92b64, HEAD, and
`contract.json:counterSha256v1`) — the lane working tree has since drifted to an uncommitted v2 draft
(`1d04f19d…`), so v1 was extracted from git and used for every probe. No after-state was scored.
Receipts: `.ufo/waves/round-59/w1/ReviewerC1Contract.files/`.

## Answers to the five questions

**1. Same predicate sentence in contract.md, contract.json, counter PREDICATE?** Yes — byte-identical
after stripping contract.md's `**` emphasis, and the base receipt label repeats it. **But the sentence
is not the acceptance condition.** v1 `met` adds an undeclared fifth conjunct `names_ok` (`res["met"] =
… and names_ok and …`, l.283). Fixture L1 (third axis row renamed `adjacency`, round-59 section naming
`adjacency`): all four printed conjuncts true — `mismatches=0 rows=3 scores_held=2 superseded_kept=3` —
yet `met=False`, exit 1. A verifier re-deriving the verdict from the printed predicate gets the wrong
answer, and the contract's claim that the sentence is "the same … in the counter's code (PREDICATE) and
in every receipt label" therefore under-describes the gate.

**2. Do the atoms measure self-assessment vs observed state?** Only partly, and the calibration
substance is missing. Of the five components summed into `mismatches`, one (`unresolved`) is literally a
cell-vs-committed-tree contradiction and `tallies_unfound` is a weak proxy (substring `A/B` anywhere in
a cited blob); `rows_no_receipt`, `receipts_off_axis`, `rows_no_tally` are *form/provenance* demands,
not mismatches. Critically the **score column is never compared with evidence**, and the one score atom
is inverted: `scores_held` pins only operability/freshness to their base values, so the honest
correction of an overstated score is RED (L2: operability 10→8 → `scores_held=1`, exit 1) while
inflating the claim's own axis is GREEN (K7: calibration 2→10 with unchanged evidence → `met=True`,
exit 0; L3: 2→3 → green). AXES.md's calibration is "gaps named honestly, confidence graded, overreach
caught"; the atom set cannot see overreach and punishes honesty.

**3. Is the do-nothing control red for the right reason?** Yes, and it reproduces exactly: exit 1, body
byte-identical to `controls/base-c1-axis-evidence.txt`. The 11 unresolved are the real defects named in
the contract (operability → `cli.mjs:935` + 3 line continuations in a tree the lane no longer holds;
freshness → `corpus/claims` + six `/tmp/kake-r17/…`). Two caveats: the count is a **token** count, not a
defect count (11 tokens over 8 distinct roots — the 3 `:LINE` tokens are cascades of the dead
`cli.mjs`), and 5 of the 16 are form atoms, so "base 16 mismatches" (quoted in contract.md and the
round prompt) overstates independent calibration defects by roughly 2×. Also the base control runs
base==revision, so `scores_held`/`superseded_kept` are degenerate there and the contract's other named
control classes (emptied cells, off-axis receipt, absent tally) have **no committed receipt** — I
witnessed them only from fixtures (K8/K9/K10/M2).

**4. What would make the after-state a calibration HARM?** Every one below was demonstrated green on
frozen v1: (a) **score inflation** — calibration 2→10, evidence untouched (K7); (b) **citing the failure
as evidence** — the receipt slot accepts `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt`, the
receipt recording `mismatches=16 met=False`, because it also contains `117/117` (K3), and accepts the
frozen contract itself (K2) — the only requirement is "some blob under `.ufo/waves/round-<N>/`" (H3:
`contract.md`, `contract.json`, the counter source, `w1-spec.json`, `sources/S425.html` all qualify);
(c) **borrowed tallies** — `10/10` found anywhere in a co-cited blob (K6, disclosed); (d) **hidden
stale evidence** — a dead relative path written unbackticked is invisible (K4), while a backticked
tally `21/21` is misread as a path and reds an honest cell (K5); (e) **unmarked retention** — the base
cells kept under `## Axis table evidence (current)` still count as "superseded" (K11), so SCORECARD.md
ends up presenting two rival current evidence cells for one axis; (f) **wrong table measured** — a clean
table above the live one returns `met=True` while the live table still cites `cli.mjs` and
`/tmp/kake-r17` (M1; confirmed: the live second table's operability/freshness cells are unchanged).

**5. Is `superseded_kept` the right append-only guard?** Right intent, wrong test as implemented. It is
a whole-file substring probe for the base cell text outside the measured table's span, so it (i) counts
a copy presented as *current* evidence (K11), (ii) counts a copy inside another table's rows (L4), and
(iii) demands a byte-exact 1056/1218/450-char reproduction — any paraphrase or truncation drops it to 0
and reds the claim (K13). The lane's own append-only convention, used elsewhere in this repo and by C3,
is a *marked* correction tail (`[r59-correction …]`, "marked historical", "absent-historical"); the
counter enforces byte-presence instead of supersession. It also re-introduces the six
`/tmp/kake-r17/…` pointers into SCORECARD.md — invisible to this counter (which scans only table cells)
but exactly the uncitable form prompt §7.5 forbids.

## FINDINGS

| # | Severity | Issue | Fix |
|---|---|---|---|
| F1 | **High** | `names_ok` is enforced in `met` but absent from the frozen predicate sentence in contract.md, contract.json and `PREDICATE`; L1 shows printed predicate TRUE / exit 1. The printed sentence does not determine the verdict. | Add the row-name/order conjunct to the predicate sentence (v2), or drop `names_ok` from `met`. Never leave the printed predicate under-describing the gate. |
| F2 | **High** | The claim's own axis is unmeasured: no atom compares the score cell to evidence; `scores_held` pins only the two non-claimed axes, so calibration 2→10 is green (K7) and an honest operability 10→8 is red (L2). This is an inverted calibration incentive — overreach passes, honesty fails. | Compare the claimed axis's score to the cited receipt's own reported result, or declare the axis's score explicitly out of scope in contract.md and record "no score moves through this claim" for all three rows. |
| F3 | **High** | The receipt atom does not distinguish a measurement from a non-measurement: the red base receipt (K3), the frozen contract (K2), the counter source and the retained HTML (H3) all satisfy it; v1 `on_axis` accepts a row that merely contains the axis word. | Require the receipt to be an after-receipt of the measured round whose own recorded verdict is met/pass, and require an axis-column row (the in-flight v2 draft's stricter `on_axis` is the right direction). |
| F4 | **Medium** | `superseded_kept` guards byte-presence, not supersession: passes under a heading presenting the old cell as current (K11) or inside another table (L4); fails on any paraphrase (K13). | Require the retained occurrence to sit under a heading/marker naming it superseded or historical (reuse `[r59-correction …]`/“marked historical” from the lane's own convention); accept a digest-pinned paraphrase. |
| F5 | **Medium** | `mismatches` conflates kinds: 16 at base = 11 pointer tokens (8 distinct roots; 3 are cascades of one dead `cli.mjs`) + 3 no-receipt + 2 no-tally. Quoted as "base 16 mismatches", it overstates independent calibration defects. | Report distinct root causes beside the token sum and label the gate count (fail-closed sum is fine, the reporting label is not). |
| F6 | **Medium** | Only the base is a committed do-nothing control, and base==revision degrades `scores_held`/`superseded_kept`. The contract's other named classes (emptied cell, off-axis receipt, absent tally) have no committed receipt; the counter's `--selftest` is a stub returning exit 2. | Commit the fixture kill matrix with v2 (this wave, per the contract's own wave-1 obligation) and run the base control with an explicit distinct `--base`. |
| F7 | **Medium** | AXES.md defines calibration over "SHONEN.md/SCORECARD entries"; the prompt rule says "(SCORECARD/SHONEN)". The counter reads only SCORECARD.md and its docstring quotes the AXES definition anyway. SHONEN.md's four boxes are unchecked while observed state satisfies at least the first two (SKILL.md 1295 lines/159 table rows; LOG.md 63 round headings) — a live mismatch C1 cannot see. | Either extend the surface to SHONEN.md or state the exclusion in contract.md's "What the counter does not test". |
| F8 | **Medium** | Freeze discipline: the contract pins `counterSha256v1` and the 4-conjunct predicate, but the lane working tree already holds an uncommitted v2 draft whose `PREDICATE` adds `tables == 1` while its own docstring still prints the old sentence, and still omits `names_ok`. If the after-state is scored with those bytes, the receipt label will not match contract.md/contract.json. | Re-freeze (predicate sentence + sha256 + a fresh base receipt) before any after-measurement; the docstring and PREDICATE must agree. |
| F9 | **Low** | Pointer syntax is inconsistent in both directions: an unbackticked dead relative path is invisible (K4, green), a backticked tally `21/21` is read as a path (K5, false red). | Adopt one stated pointer syntax and validate it (the in-flight draft closes K4; K5 survives — V4 still `unresolved=1`). |
| F10 | **Low** | A copy of the axis table above the live table changes which table is measured: clean shadow → green while the live table stays broken (M1/P1); stale historical copy above → red with the base's numbers (K12). | Require exactly one eligible axis table (the in-flight draft's `tables == 1`); mark archived copies so they cannot shadow. |

Positives verified, not defects: predicate sentence identical across the three sources; base control
byte-identical and red for the substantive reason; exit codes 0/1/2/64 as declared; `GIT_*` scrubbed,
`--revision`/`--base` resolved once to commit ids, `--root` must be a repo toplevel (the routed D2
fixes are present); a straightforward honest re-point of all three cells reaches `met=True` (K1), so
C1 is achievable.

## VERDICT

Claim C1 is not safe to measure as frozen: the predicate sentence under-determines the gate
(`names_ok`), the atoms measure citation-resolvability rather than calibration (score inflation on the
claim's own axis is green, an honest downgrade is red), the receipt slot accepts the red base receipt
and the frozen contract, and `superseded_kept` guards byte-presence rather than supersession. Re-freeze
a v2 predicate, receipt rule and retention rule (predicate string + sha256 + a committed kill matrix and
a fresh base receipt) before any after-state is scored.

VERDICT: Blocking — C1's frozen predicate and atoms certify citations, not calibration; re-freeze v2 (declared predicate == implemented `met`, axis score bound to evidence, receipt must be a passing after-receipt, retention must be marked superseded) before the after-measurement.
