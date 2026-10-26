# CriticControlsSizing

Seat: critic (controls + claim sizing), round 57 W1, read-only except this file. All runs below are
mine, over committed bytes at the named revisions; scratch work in a `mktemp` clone
(`git clone` of the lane, commits with `-c user.name=selftest`), the lane repo, index and jj state untouched.

## PREDICATE BYTES:

Method: imported each counter, took the assembled `PREDICATE` constant, compared it to `contract.md`
(substring), `contract.json` `claims.<Cn>.predicate` (equality), the module docstring (substring) and
the base-control receipt label (`grep -F`).

| claim | len | contract.md | contract.json | docstring | PREDICATE | base receipt label |
|---|---|---|---|---|---|---|
| C1 | 171 | 1 occurrence | equal | 1 occurrence | yes | `controls/base-c1-receipt-pins.txt` |
| C2 | 37 | 1 occurrence | equal | 1 occurrence | yes | `controls/base-c2-idresolver.txt` **and** `controls/base-c2-idresolver-v1.1.txt` |
| C3 | 32 | 1 occurrence | equal | 1 occurrence | yes | `controls/base-c3-quote-truth.txt` |

All three sentences are byte-identical in all five locations. C1's constant is an implicit two-line
concatenation that assembles to the exact sentence. No finding. Evidence blemishes (not predicate
defects): `controls/base-c2-idresolver-v1.1.txt` (added at `f7c98ff`) is byte-identical to
`controls/base-c2-idresolver.txt` (added at `b9a5d01`) — a duplicate base receipt for the same
revision, named nowhere in the C2 section, adding no evidence; and `controls/base-c3-quote-truth.txt`
ends with two `EXIT=1` lines.

## UNIVERSAL CLAUSES:

1. `contract.md:27` "**every** historical relabel is disclosed" — the counting command does not
   enumerate that set. Population is narrowed by `POP_RE` (rounds 52–57 only, `control(s)/` only,
   `.txt`/`.json`), `--first-parent`, `--no-renames`, and `REV_RE` (`^\s*revision\s*[:=]` 40-hex).
   Report-prose relabels are excluded (the contract admits this below the predicate, but the
   after-state sentence itself is universal).
2. `contract.md:29` "none is **ever** rewritten" — future-universal; a counter at one tip can only
   bound history up to that tip. Not a verifiable after-state element.
3. `contract.md:46` "lists **every** `S###` id cited in `corpus/knowledge/**/*.md`" — the gate never
   enumerates it: `ids_cited` is the tool's own stdout field and G5 only requires `>= 100`. A stub
   printing `ids_cited=120 ids_resolved=120 dangling=0` passes G5 (measured, see below).
4. `contract.md:57` "a tool that prints constants fails G3 … and G4" — **falsified** (measured).
5. `contract.md:79` "**every** Gate quote and quoted entry span is <= 25 units … and <= 40
   characters" — Gate-line spans are filtered by `units(q) >= 6` *before* any ceiling or substring
   check (`c57_quote_truth.py`, Gate block). Code-path demo with the counter's own `units()`: a Gate
   line holding a 1-unit / 89-character double-quoted span yields `spans found: 2, checked: 0` — the
   span escapes both ceilings and the raw-substring rule. Entry-line spans are enumerated correctly
   (skip only when `units < 2 and len < 12`).
6. Uncounted or unverifiable after-state elements: C2 "The capability row enters the SCORECARD
   capabilities table in the same round" (no gate condition reads `SCORECARD.md`); C3 "the append was
   census-validated on a scratch mirror first" (C7 is a receipt check, which the contract itself says
   is "not proof that the run happened").
7. C1 `scorecard_pin` is a presence test for `measured_rev[:12]` *anywhere* in the `## Round 57`
   section — it passes inside a longer hash or a negated sentence. Latent: `POP_RE` admits `.json`
   receipts but `REV_RE` cannot match a JSON key (`"revision":` has a quote before `revision`), so
   JSON receipts are counted in `population` and never checked (one is in population today,
   `round-52/control/c1-mutation-ladder.json`, with no pin).

## CONTROL REACHABILITY:

Base reproduction (run by me at `28fa0b23…`, all three): C1 `undisclosed_relabels=6 … new_receipts=0
scorecard_pin=0 met=False` exit 1, line identical to the committed receipt; C2 `0/5 met=False` exit 1
(0.04 s, G1 short-circuit, identical to both receipts); C3 `0/8 met=False` exit 1, identical to the
committed receipt. Registry at base is 158 rows with no S421/S422.

- **C1 — the target IS reachable by a control that records no evidence (measured).** Three receipts
  each containing only the 12-byte line `revision: 28fa0b23…`, plus `measured.json` and a `## Round
  57` SCORECARD line, score `new_receipts=3 new_unpinned=0 new_relabelled=0 scorecard_pin=1` (4 of 7
  terms) with `undisclosed_relabels=6` still failing. Adding `receipt-errata.json` transcribed from
  the counter's own `UNDISCLOSED` output (or from `measure()`, which returns full 40-hex) gives
  `undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0
  new_receipts=3 scorecard_pin=1 met=True`, exit 0. A pure do-nothing (nothing committed) is stopped
  only by `undisclosed_relabels == 0`; the receipts half is stopped by nothing.
- **C2 — the target IS reachable by a constant-printing stub (measured).** A 21-line
  `scripts/id_resolver.py` with four branches (`--selftest` prints `selftest: 16/16`; a `--root`
  containing `c57-fixture` and not `clean` prints the four fixture rows and `(6,2,4,3,1)`; the clean
  fixture prints `dangling=0`; `--revision` starting `3994101` prints the five ids owned by
  `kotodama-shokunin`; otherwise `ids_cited=120 … dangling=0`) scores **`5/5 met=True`, exit 0** — no
  id parsing, no registry read, no sibling read. The stopping conditions the contract names do not
  exist: G3's expectation is the gate's own constants (`EXPECT_FIXTURE`, `EXPECT_SUMMARY`) over a
  deterministic fixture, G4 compares to `RED_IDS`/`RED_OWNER` and to the tool's self-reported
  `summ[2] == 5`, G5 accepts the tool's own `ids_cited`, G2 is the tool's own `--selftest`.
- **C3 — placeholders are stopped by C5 and C8 (code-path analysis, not run).** C5 requires at least
  three distinct spans that are raw substrings of the committed body, unique in that body and absent
  from the other retained body, inside the article block, with the row title, the printed
  `发布日期：<date>` and the anchor heading present in the body; C8 requires the mirror to be
  byte-equal to the base registry with a strict-ancestor add-commit and `len(rows) ==
  len(mirror_rows) + 2`. A placeholder entry cannot satisfy C5 without quoting the retained page.
  C7 alone is forgeable (four committed text files) and the contract says so. Not run: building a
  placeholder fixture would duplicate wave 1's build; this is a wave-2 falsifier's job.

## SIZING FINDINGS:

1. **C2 violates section 9's do-nothing rule.** The cheapest control that skips the claimed work
   meets the frozen target (5/5). Section 9: "if it meets the target, the counter or target is
   wrong — fix it before data." The claim as frozen cannot be admitted on a 5/5 line.
2. **C1's pin discipline contradicts its own after-state.** The counter requires
   `measured_rev != intro` and `is_ancestor(measured_rev, intro)`. At any admissible pin the three
   receipts do not exist, so `new_receipts = 0` and an honest `after-c1-*` receipt reads `met=False`.
   Pinning the receipts at their own introducing commit is rejected: measured `new_unpinned=3,
   new_receipts=0, met=False`. So the only receipt that passes C1 is one whose body proves nothing —
   which is exactly the stub control above. The contract must either declare the C1 receipt's
   expected content as the pre-receipt state, or stop calling it `after-`.
3. **C2's value is not re-derivable over committed lane bytes.** G4/G5 read sibling registries at
   their live HEAD (`--fleet`); the same command over the same lane revision can change its answer
   when a sibling appends or renames rows. The contract admits this under "What the counter does not
   test", but section 9 asks for one value the closure re-derives from committed bytes — this one is
   not.
4. **C1 is a calibration claim by section 9's rule, but only half of it.** It counts mismatches
   (6 at base) between the lane's self-assessment — the receipt's `revision:` line (the lane's claim
   about what it measured) plus the report/SCORECARD "measured at" pin — and observed repo state
   (committed history); that count comes from committed bytes, not an assertion. But the SCORECARD
   half is an assertion (`scorecard_pin == 1`, a 12-char substring presence test) and SHONEN is
   untouched (defect 4 stays `[ ]`), so the self-assessment element the rule names is not counted.
5. **After-states are not one concrete value.** C1 is a 7-term conjunction plus two prose elements no
   condition tests ("none is ever rewritten"; SCORECARD tested only as presence). C2's after-state
   carries one uncounted element (SCORECARD capability row), C3's one unprovable element
   ("census-validated … first"). C2 (`5/5`) and C3 (`8/8`) are single values; C1's single value is
   the counter's one report line, which the prose overstates.
6. **Causal separability holds, with one coupling to declare.** C2 reads only the tool, the lane
   registry and knowledge; C3 only entries, registry, sources, mirror and validate receipts; C1 only
   receipts, errata, `measured.json` and SCORECARD. Measured: C1 reached `met=True` with zero C2/C3
   work. The coupling: C1's `new_receipts == 3` names `after-c{1,2,3}-*`, i.e. C2's and C3's
   receipts — C1 cannot pass unless those files exist, but it passes regardless of their content, so
   a failed C2 or C3 does not move C1. Separability bought with vacuity, not with independent evidence.

## RECOMMENDED CONTRACT CHANGES:

1. **C2, before data (blocking).** (a) Make the G3 fixture non-constant: derive its ids, sibling
   names and indentation per run (`secrets`-seeded) and compute the expected lines/summary from the
   generated ground truth inside the gate. (b) Have the gate compute `ids_cited`, `ids_resolved` and
   `dangling` itself from the documented rule over the revision and require the tool's summary to
   equal them. (c) In G4, derive the red set and the owning sibling in the gate from the lane registry
   at `3994101` plus the sibling registries, and compare the tool's `cited-by` paths to the gate's own
   citation list. (d) Record G2 as a smoke test, not evidence. (b) alone stops the stub I built.
2. **C2, closure.** Commit a sibling snapshot receipt (each sibling's `rev-parse HEAD` plus the ids
   it owns) and have G4/G5 require the live read to equal the snapshot, so `5/5` is re-derivable from
   committed bytes.
3. **C1, after-state.** Replace `scorecard_pin` with `scorecard_pin_mismatches == 0`: count the
   distinct full 40-hex pins named in the `## Round 57` section that differ from the measured
   revision, and require the measured 40-hex to appear. This makes the SCORECARD self-assessment a
   count rather than an assertion (section 9's calibration rule).
4. **C1, receipts.** Require each `after-cN-*` receipt to carry the corresponding counter's report
   line (its label prefix plus its `key=value` fields) and require the C1 receipt's seven values to
   equal a fresh `measure()` at the pinned revision. Declare that this is the pre-receipt state
   (`new_receipts=0 met=False`) — or rename the three receipts `pin-c{1,2,3}-*`, since `after-` is
   false at their own pin.
5. **C1, prose.** "every historical relabel" → "every relabel the counter enumerates (receipts under
   `.ufo/waves/round-5[2-7]/control(s)/` carrying a 40-hex `revision[:=]` line, first-parent, no
   renames)"; drop "none is ever rewritten" or bound it to "up to the measured tip". Either drop
   `.json` from `POP_RE` or add a JSON pin form to `REV_RE`.
6. **C3.** Check every Gate-line span of 2+ units for both ceilings and raw-substring truth (filter
   `units >= 6` only for the "carries a quote of 6+ units" requirement), so `contract.md:79`'s
   "every Gate quote" is actually enumerated. Reword the after-state to what C7 tests ("C7's receipt
   is present and byte-consistent with the landed registry, exit 0").
7. **Evidence.** Name both C2 base receipts (or drop the byte-identical duplicate) and fix the double
   `EXIT=1` line in the C3 base receipt.

Not run by me: any C3 placeholder fixture, any wave-2 falsifier, any mutation of the lane repo.
Measured by me: the three base runs, the C1 stub-receipt control (met=True), the C2 constant-stub
control (5/5), the pin==intro probe (new_unpinned=3). Tool installs: none.

VERDICT: Predicate bytes and base values are clean, but C2's target is met by a 21-line constant-printing stub (5/5, measured) and C1's target is met by three 12-byte revision-only receipts plus transcribed errata (met=True, measured), so both targets are do-nothing-reachable and must be fixed before data; C1 also cannot honestly label a receipt `after-` at any pin it admits.
