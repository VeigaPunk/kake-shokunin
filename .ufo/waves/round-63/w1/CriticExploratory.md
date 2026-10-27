# CriticExploratory — round-63 exploratory-status smuggling check

Seat: `CriticExploratory` (leaf critic, w1). Scope: verify neither frozen claim
smuggles exploratory (unprovable-but-better) status — each must carry a frozen
counting command and a kill rule — and that the round claims no exploratory
verdict and no score delta it cannot re-derive.

**Verdict: PASS — no exploratory smuggling found in C1 or C2.** Both claims are
binary (met / unprovable) under frozen counters, both kill rules exist and are
consequential, the round claims zero score delta, and every claimed verdict
re-derives exactly from the frozen counting commands run against committed
bytes. No counterexample survived local evidence.

All commands run from `/home/vgpnk/Projects/shokunin/kake-shokunin` (fleet
repo). No files were written except this report; `git status --porcelain`
after the runs shows only pre-existing untracked wave-dispatch files
(`.ufo/waves/round-63/w1.ready`, `w1.ready.dispatched`, `w1/`).

## 1. Frozen counting commands — present for both claims

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md`:

- C1 counting command (contract.md:46-47):
  `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision <commit>`
- C2 counting command (contract.md:72-73):
  `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision <commit>`

Both counters are frozen; working-tree sha256 matches the contract at
2026-10-27:

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py \
    .ufo/waves/round-63/quote-class/quote-classes.json scripts/quote_class.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

All four digests equal the contract's frozen values (contract.md:24-25, 52-56,
63-64 of the wave copy in `.ufo/waves/round-63/contract.md`).

## 2. Kill rules — present, consequential, for both claims

- C1 kill rule (contract.md:42-45): after receipt not `met=true` at the
  measured commit, either control printing `met=true`, or any wave attack
  reproducing a marker-only green → C1 `unprovable` (honest stop), **no
  calibration credit**. This is an anti-credit clause, the opposite of
  exploratory credit.
- C2 kill rule (contract.md:70-71): after receipt not `met=true`, or a stub
  tool passing → C2 `unprovable`.
- Global teeth (contract.md:4-6): a counter/control/predicate changed after a
  seat scores is not this round's rule; a kill-rule breach lands the claim
  `unprovable`. Binary outcome space; no third "exploratory" state exists in
  the contract vocabulary.

## 3. No exploratory verdict claimed anywhere in the round

Case-sensitive grep for `exploratory|unprovable-but-better|provable-but|partial
credit|partial-credit` over `.ufo/waves/round-63/` (excluding `sources/`):

- Only hits are this seat's own item text in the dispatch artifacts
  (`w1-dispatch.json:312,661`, `w1-spec.json:246`, `w1/swarm-registry.json:294`).
- `contract.md` contains no `exploratory`, `provisional`, `interim`,
  `tentative`, `partial`, or `better` claim language (grep for
  `provisional|interim|holding|better|improvement|credit|partial|tentative|pending`
  returns only the "no calibration credit" kill-rule clause at lines 44-45).
- The verdict vocabulary in both frozen predicates and all six committed
  receipts is exactly `met=true`/`met=false` plus exit codes.

## 4. No score delta the round cannot re-derive

- Base→measured diff touches only round-63 wave files, corpus corrections,
  the tool and its fixtures:
  `git diff --name-only 13d4519818db28cd0aa912e49020659140d7b9fa 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
  (19 paths, all under `.ufo/waves/round-63/`, `corpus/`, `scripts/`).
- `git diff --stat 13d45198..05b0d7f4 -- SCORECARD.md LOG.md MANIFEST.json
  corpus/SOURCES.md` prints **empty** — the score-bearing files are unchanged;
  `SCORECARD.md` still records calibration at 2 (`SCORECARD.md:19`) and
  operability at 10 HOLD (`SCORECARD.md:17`).
- The round's own scribe drafts claim **no delta**:
  `.ufo/waves/round-63/w1/ScribeScorecard.md:32-35` ("Score deltas: none —
  operability and freshness stay 10 and calibration stays 2, because admission
  of the calibration move belongs to the non-author closure") and
  `ScribeLog.md:14` ("No SCORECARD.md change is committed base→measured: the
  calibration axis stays 2/10 and C1's met is calibration evidence only,
  pending the non-author closure").
- The contract itself defers all scoring: "The claims land in one round but
  score independently: C1's met is calibration evidence only, C2's met is
  operability evidence only" (contract.md:81-82). No numeric advance, no
  exploratory holding status, is asserted.

## 5. Re-derivation by execution (the core anti-smuggling test)

I re-ran all four frozen counting invocations against the live repo. Every
output line reproduces its committed receipt exactly, including exit codes:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0        # == .ufo/waves/round-63/controls/after-c1.txt

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1        # == .ufo/waves/round-63/controls/base-c1.txt

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0        # == .ufo/waves/round-63/controls/after-c2.txt

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1        # == .ufo/waves/round-63/controls/base-c2.txt
```

Both control receipts also stand: `control-marker-fixture.txt` records the old
c62 `met=true` defect and the new c63 `met=false` (exit 1) on the marker-only
fixture; `control-junk-fixture.txt` records `met=false` (exit 1). The C1
counter reads every input via `git show <rev>:<path>` (c63_calibration.py:86-92
`git_show`, invoked for all five corpus paths plus the two retained blobs and
the ledger at lines 117-121) — no working-tree dependence, so its green cannot
be manufactured from uncommitted state. Its `resolved` is a conjunction of
semantically-bound components (quote_correction requires the frozen span, the
ledger row, sha256-re-derived blob digests, and an inline round-50
re-classification equal to `collapsed-only`; criterion/lesson_gate/source_row
each bind to committed content), so the round-62 marker-only false green
(receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`) is dead by
construction. C2's counter gates on the frozen tool blob, the four frozen case
ids with `derived == expected`, and `total == passed == 4`, so a stub selftest
cannot pass (c63_quote_tool.py:71-86).

## 6. Observations (non-blocking, recorded for the record)

- `base-c2.txt`'s result line carries an extra field
  (`present=0 selftest=unevaluable met=false`) versus the predicate's literal
  `present=0 met=false`; the predicate's fields are all present with the
  required values and exit 1. Semantic match, not a contiguous substring
  match. No corrective action needed for my axis.
- C2's frozen tool resolves its selftest fixtures from the invoking cwd's
  working tree (`scripts/quote_class.py:19-20,45-69`), so C2 re-derivation
  presumes a checkout that contains `scripts/fixtures/quote-class/*` and the
  two S432 blobs. The contract discloses exactly this binding in the pre-wave
  freeze note (contract.md:57-61); the frozen counting command runs from the
  lane root, so the committed procedure is self-contained. Not a smuggle.
- The two receipts for the marker fixture and the junk fixture were produced
  in scratch repos whose dirs were deleted; their committed text records the
  fixture revs, and the kill rule's third prong (any wave seat reproducing a
  marker-only green) remains open for the rest of the wave.

## 7. Tooling

No tools installed; no pacman transactions (host-wide pause respected). No
writes performed other than this report; frozen claim, counters, receipts,
corpus, and score-bearing files untouched.

## Conclusion

C1 and C2 are fully counted claims: frozen counting commands, frozen
counters, consequential kill rules, no exploratory vocabulary, and no claimed
score delta (the scribe drafts explicitly claim "none", and SCORECARD/LOG are
byte-identical base→measured). Every verdict the round asserts re-derived
exactly under my independent execution of the frozen commands. No
counterexample found; the exploratory-smuggling attack surface is empty on
current evidence.
