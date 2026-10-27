# CriticCounterFamily — round-63 w1 critic report

Seat: CriticCounterFamily (leaf critic, no subagent dispatch).
Item: argue the strongest case that the round-63 calibration counter family is
STILL broken; assess whether the residual substring checks matter given
`blobs_match`+`class_match`; rule on whether the round-62
"no calibration green from this counter family" ban is lifted or C1 should
stay unprovable. Conclusion: §6.

All frozen artifacts were verified, not edited:

- `.ufo/waves/round-63/c63_calibration.py` sha256 `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` — matches contract.
- `.ufo/waves/round-63/quote-class/quote-classes.json` sha256 `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` — matches contract.
- `scripts/quote_class.py` sha256 `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` — matches contract.

No tools were installed. All fixture repos were built and deleted under
`/fast/scratch/hyaku/kake-r63/CriticCounterFamily/` with the top-level assert
(`git -C "$D" rev-parse --show-toplevel` == `$D`); scratch is clean. Nothing
outside this Report was written.

## 1. What the repair actually changed (component-by-component)

The falsified c62 counter (`.ufo/waves/round-62/c62_calibration.py:33-38`)
computed every component as a literal substring over four corpus files; it had
no source-body check at all. The c63 counter keeps the same four-file shape but
splits the predicate into two tiers:

Strong tier (re-derived from committed bytes):
- `blobs_match` (c63_calibration.py:127-137): the S432 ledger row's
  `rawSha256`/`textSha256`/`quote` must equal the sha256 of the retained blobs
  at the measured revision and the frozen quote.
- `class_match` (c63_calibration.py:138-143): the round-50 class is re-derived
  inline (`classify`, lines 59-67) from those blobs and must equal the
  recorded `collapsed-only`.
- `quote_correction` (lines 121-145) = marker-presence AND `blobs_match` AND
  `class_match`.

Weak tier (still literal substrings, identical in kind to c62):
- correction-presence term (lines 121-125): `"[r63-correction" in knowledge
  and FROZEN_QUOTE in knowledge and LEDGER_REL in knowledge`.
- `criterion` (lines 148-150): `"substantive" in quality and
  "round-61-verifier-spotcheck" in quality and all(PURPOSE_TERMS in quality)`.
- `lesson_gate` (lines 153-159): `"## Gate"`, `"round-61-verifier-spotcheck"`,
  `"Disagree"`, `"collapsed-only"`, and `("author-side" or "self-assessment")`
  all `in lesson`.
- `source_row` (line 162): regex `^\|\s*S432\s*\|`.

Independent re-derivation on the fleet tree (measured commit
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`):
`git show 05b0d7f4:.ufo/waves/round-61/sources/S432.html | sha256sum` →
`63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`;
`git show 05b0d7f4:.ufo/waves/round-63/quote-class/S432.txt | sha256sum` →
`8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69` — both
equal the ledger's recorded digests. FROZEN_QUOTE ∉ raw HTML, ∈ flat text, so
the inline class genuinely evaluates `collapsed-only`. Live counter runs
reproduce the committed receipts exactly:
`python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
→ `... quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0;
same at base `13d4519818db28cd0aa912e49020659140d7b9fa` → `met=false`, exit 1.

## 2. The strongest case that the family is STILL broken — executed attacks

### Attack A — marker-only replay (the routed round-62 false green)

Byte-exact copy of the committed `.ufo/waves/round-62/controls/false-green-fixture/corpus/`
into a scratch repo (rev `b7743607762fbb36e8560806e724a1e322839208`):

- old c62: `met=true`, exit 0 — the family defect reproduces live on my copy.
- new c63: `quote_correction=0 blobs_match=0 ... criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`, exit 1.

### Attack B — real retained blobs + semantically NEGATED prose

Fixture with the REAL `S432.html`/`S432.txt`/ledger (copied from the fleet at
the measured commit) but corpus prose that inverts every claim
(e.g. QUALITY.md: "The lane REJECTS the substantive-support claim … The
X-Content-Type-Options / Content-Type / destination proposition is REFUTED";
lesson: "## Gate … REJECTS … author-side self-assessment fraud";
knowledge: "[r63-correction REJECTED …] NOT admitted … FABRICATED").
Result (rev `7e712c4f85a648e58715432b36e25e8963fd72bb`):
`quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0.

**The substring tier is presence-blind.** Every weak-tier component greens on
negated prose. This is exactly the check class that c62 was falsified for;
c63 did not repair it, it only added the strong tier underneath it.

### Attack C — quote-only fake text blob, self-consistent ledger

Fixture with `S432.html` = `<!doctype html><title>not the Fetch spec</title>…`
(no span), `S432.txt` = the FROZEN_QUOTE line alone, and a ledger recording
those fake blobs' digests with `matchClass: collapsed-only`. Substrings
planted. Result (rev `cbbce12094a25a0c3f1b608d81154bad4d4d2a70`):
`quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true`, exit 0.

**`blobs_match` is ledger↔blob self-consistency, not provenance.** The only
external anchor in the strong tier is exact FROZEN_QUOTE membership in the
text blob. A tree whose "retained body" is a hand-written one-line file
greens end-to-end; full-document fidelity to the real 1.85 MB Fetch page is
not bound anywhere in the counter.

### Attack C2 — boundary probe (why the anchor still bites)

Same as C but the fake text blob carries the STRAIGHT-apostrophe variant of
the span while the ledger quote stays the frozen curly-apostrophe FROZEN_QUOTE
(rev `b35df6d58780a612a9102bbffb17b380f106f628`):
`blobs_match=1 derived=absent class_match=0 … met=false`, exit 1. The counter
forces byte-exact adjudicated span text; near-miss paraphrase or punctuation
drift dies.

### Junk-marker control, reproduced live

Fixture with r63 substrings planted and NO blobs/ledger (rev
`3965dccd7289f80d330be2bc4f4aace9f1f11968`): `criterion=1 lesson_gate=1
source_row=1` but `quote_correction=0 … met=false`, exit 1 — matches the
committed `.ufo/waves/round-63/controls/control-junk-fixture.txt`.

## 3. Does the substring weakness matter, given blobs_match+class_match?

Yes as a literal property of the counter, no as a defect against this round's
contract — the two attacks that green (B, C) are categorically different from
the routed false green (A):

1. **The routed defect class is dead.** A's tree had the disagreement standing
   and no source body; c63 kills it (and the committed marker/junk controls
   agree). The round-62 kill receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`
   is now counterexample-contained: the same corpus that greened c62 reds c63.
2. **Any green tree must now contain the semantic evidence.** B greens, but
   only because the real Fetch bytes are in it; C greens, but only because the
   committed text blob literally contains the exact adjudicated span. A green
   is no longer achievable from markers, junk, paraphrase, or punctuation
   drift (C2). The FROZEN_QUOTE anchor is doing real work: it is the
   adjudicated §3.6 sentence, byte-frozen into the counter.
3. **Prose truth is not a counter's job.** B shows criterion/lesson_gate are
   presence checks, but "does the prose affirm or deny" is not machine-checkable
   in principle; the lane's architecture assigns it to the non-author verifier
   layer (round-62 spotcheck caught the family defect; round-63 lesson
   `corpus/lessons/round-63.md` explicitly labels its own gate author-side).
   A counter that tried to judge affirmation would itself be a semantic
   authority — the exact duplicate-authority failure mode this fleet's
   counters are designed to avoid.
4. **Provenance is a contract-semantics tradeoff, not an implementation bug.**
   The contract (§C1 component semantics) specifies exactly what c63 does:
   "the ledger sha256s to re-derive from the retained blobs at the measured
   revision, and the class to re-derive inline from those blobs." C attacks
   that chosen semantics (tree-local re-derivation), not the counter's
   fidelity to it. The fleet tree's provenance is independently established
   outside the counter: the round-63 lesson re-open record states the live
   `fetch.spec.whatwg.org` GET was sha256 byte-identical to the retained body
   (`63b0a018…911b`), and the ledger digests re-derive on my run (§1).
5. **The frozen kill rule is not breached.** It triggers on "any wave attack
   reproducing a marker-only green." B and C both commit the span bytes; only
   A is marker-only, and A is red.

Smallest safe correction if the canonical judge wants the provenance hole
closed: pin `blobs_match` to the two known-real digests
(`rawSha256 == 63b0a018…911b and textSha256 == 8b90d096…2a69`) in addition to
the ledger↔blob consistency. That kills C while leaving every receipt and
control unchanged (the real tree already matches those digests). But it amends
a frozen predicate — the round-60 freeze rule requires freezing anew, which is
outside this leaf seat's lane bounds and was not done. Judged as-written and
as-frozen, the counter is faithful to its contract.

## 4. Is the ban lifted, or should C1 stay unprovable?

The ban, `corpus/lessons/round-62-verifier-spotcheck.md:54` (routed defect 1):
"Repair the frozen counter so `resolved` binds semantics … with a committed
red-before/green-after demonstration; the counter fix itself must be frozen
per the lane's own standing rule. **Until then no calibration green from this
counter family is citable.**"

Its three conditions are all met, with the receipts committed before any
after-state measurement (contract §preamble):

1. *Repaired, semantics-binding counter*: c63 binds the discriminating
   components to retained-blob digests and an inline re-derived class; the
   marker-only attack class is dead (Attack A + committed
   `control-marker-fixture.txt`: c62 `met=true` defect vs c63 `met=false`).
2. *Committed red-before/green-after*: `base-c1.txt` (red, exit 1) and
   `after-c1.txt` (green, exit 0) at the measured commit; both reproduced live
   in §1. Junk control red; marker-fixture control red under c63.
3. *Frozen per the standing rule*: contract pins the counter sha
   `bcd16f68…`; `corpus/QUALITY.md:1416` (round-63 criterion) codifies the
   binding and names the precise falsifier — "rerun … over the round-62
   marker-only fixture must print `met=false`" — which I ran twice (Attack A
   and the committed control). The old c62 counter and receipts remain
   committed as defect history (no-harm clause).

The ban is therefore lifted **by its own terms**. C1 should not stay
unprovable: on the measured tree the strong tier is genuinely true (real
retained body, byte-identity to the live page re-opened 2026-10-27, digests
re-derive, class genuinely `collapsed-only`, tool selftest 4/4 re-deriving the
same class as independent C2 evidence), and the round-61 S432 disagreement is
resolved by the committed `[r63-correction]` block
(`corpus/knowledge/response-header-expectations.md:224-244`) plus the
append-only lesson gate. The residual weaknesses in §2 are real and
demonstrated, but they are (a) prose-semantics blindness inherent to any
counter, covered by the verifier layer, and (b) a provenance depth that the
frozen contract deliberately traded for tree-local re-derivability (the
contract's own Separability clause depends on evaluating arbitrary revisions).
Neither reproduces the routed false-green class, so neither keeps the family
banned.

## 5. Evidence index

- Counter code: `.ufo/waves/round-63/c63_calibration.py:59-67,121-162`; old
  `.ufo/waves/round-62/c62_calibration.py:33-38`.
- Receipts: `.ufo/waves/round-63/controls/{base-c1,after-c1,control-marker-fixture,control-junk-fixture}.txt`,
  `.ufo/waves/round-62/controls/counter-false-green-l1.txt`.
- Ban text: `corpus/lessons/round-62-verifier-spotcheck.md:54`; lift codified
  `corpus/QUALITY.md:1416`; resolution `corpus/lessons/round-63.md` §Gate;
  correction `corpus/knowledge/response-header-expectations.md:224-244`;
  registry row `corpus/SOURCES.md:178` (status cells untouched per no-harm).
- Separability: the only `quote_class` references in c63_calibration.py are
  docstring lines 15/61; no code path gates on `scripts/quote_class.py`.
- Live runs this report: measured `met=true`/0; base `met=false`/1; Attack A
  c62 `met=true`/0 vs c63 `met=false`/1; Attack B `met=true`/0
  (rev `7e712c4f…`); Attack C `met=true`/0 (rev `cbbce120…`); Attack C2
  `met=false`/1 (rev `b35df6d5…`); junk reproduction `met=false`/1
  (rev `3965dccd…`). Fixture repos deleted; `scratch_cleanup=clean`.

## 6. Honest conclusion

The strongest available counterexample case — substring-fakeable criterion and
lesson_gate (B), and a provenance-blind strong tier (C) — is fully reproduced
above and is NOT nothing: four of the six reported components remain the same
*kind* of check that falsified c62, and `blobs_match` certifies consistency
with a ledger the measured tree itself commits. But the case fails as a
round-63 rejection, for three reasons grounded in local evidence: the routed
marker-only false green is dead (A, marker/junk controls, and the falsifier
named in the new standing criterion all red); every green tree must now
contain the byte-exact adjudicated span in a genuine collapsed-only
relationship (C2 boundary), which is the semantic evidence the contract
defines; and the two residual holes are a contract-chosen tree-local semantics
(C) and an inherently non-mechanical prose judgment (B), both covered outside
the counter layer. The round-62 ban's conditions are met, so the ban is lifted
and C1 is provable at `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` — with the
one-line provenance pin noted in §3 recorded as the smallest safe hardening if
a future round chooses to re-freeze the predicate.
