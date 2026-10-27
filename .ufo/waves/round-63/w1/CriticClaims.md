# CriticClaims — do-nothing attack on the round-63 claim design

Seat: CriticClaims (leaf critic, round-63 w1)
Date: 2026-10-27
Verdict up front: **No — the round-63 targets are NOT out of a do-nothing
control's reach.** The round-62 tree plus ≈2.4 KB of trivia reaches
`met=true` on both frozen counters
(`c63_calibration.py` sha256 `bcd16f68…3fc91`, `c63_quote_tool.py` sha256
`9fcbfad0…f01e`). The phase-4 do-nothing lesson (round-34 rejection; round-35
QUALITY criterion (a): "a declared target must be out of reach of the cheapest
do-nothing controls, scored with the frozen counter and committed before the
build") therefore applies to this round's claim design, not merely to its
execution.

Frozen artifacts were verified before attack (sha256, worktree at fleet):

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

---

## Counterexample 1 — C1: quote-only text blob, no provenance, `met=true`

The C1 counter binds the ledger's digests to the committed blobs and
re-derives the match class inline (`c63_calibration.py:59-66`, `:133-142`),
but it never checks that the committed text blob
`.ufo/waves/round-63/quote-class/S432.txt` is a rendering of the retained
`.ufo/waves/round-61/sources/S432.html`. In the round-50 precedent the text
blobs were fetch-retained with the sources; here the text blob is authored by
the repair round itself, so the class derivation is circular unless the
counter re-derives the rendering.

Do-nothing fixture (recipe below): on top of the round-62 tree
(`13d4519818db28cd0aa912e49020659140d7b9fa`, extracted with
`git archive`), I added five files, none of which performs the semantic
repair:

| file | size | content |
|---|---|---|
| `.ufo/waves/round-63/quote-class/S432.txt` | 155 B | the frozen quote alone + `\n` — NOT an extraction of the HTML |
| `.ufo/waves/round-63/quote-class/quote-classes.json` | 749 B | one-class ledger; `textSha256`/`rawSha256` of the two blobs at the fixture rev; `matchClass` `collapsed-only` |
| `corpus/knowledge/response-header-expectations.md` append | ~700 B | `[r63-correction` block quoting the frozen span + ledger path |
| `corpus/lessons/round-63.md` | 196 B | marker-only gate file (`## Gate`, `round-61-verifier-spotcheck`, `Disagree`, `collapsed-only`, `author-side`) |
| `scripts/quote_class.py` | 608 B | canned-JSON stub (see Counterexample 2) |

The sha256s in the ledger match the fixture's blobs *by construction* — that
is exactly what `blobs_match` verifies. The frozen quote is genuinely not a
raw substring of the retained HTML (the one true fact the tree leans on), so
the inline `classify` returns `collapsed-only` for the fabricated 155-byte
blob, `class_match=1`, and:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root /fast/scratch/hyaku/kake-r63/CriticClaims/donothing --revision 09cd73d535de110a5467a4e5f2b914d0e8e3a334
revision=09cd73d535de110a5467a4e5f2b914d0e8e3a334 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Component-for-component, that line is identical to the committed after
receipt `.ufo/waves/round-63/controls/after-c1.txt` at the measured commit
(differing only in the revision hash) — while the genuine measured
`S432.txt` is 290,480 bytes of real extraction and the fixture's is 155 bytes
of assertion. Note also that `criterion` and `source_row` were already `1` at
base (`.ufo/waves/round-63/controls/base-c1.txt`), so the round-62 tree was
half-green on C1 before any delta.

The committed controls do not catch this class of attack:
`control-marker-fixture.txt` and `control-junk-fixture.txt` both lack the
blobs/ledger (their `blobs_match=0`); this tree has them. The C1 kill rule
("any wave attack reproduces a marker-only green") is not triggered because
this attack is not marker-only — it is digest-self-consistent fabrication,
which the frozen predicate does not exclude.

## Counterexample 2 — C2: canned-JSON stub tool, `met=true`

`c63_quote_tool.py:77-84` parses the selftest JSON and checks only that the
four frozen case ids report `passed=true` with `derived==expected`, plus
count arithmetic. A stub that prints that JSON without reading a single byte
of any blob or fixture passes:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root /fast/scratch/hyaku/kake-r63/CriticClaims/donothing --revision 09cd73d535de110a5467a4e5f2b914d0e8e3a334
revision=09cd73d535de110a5467a4e5f2b914d0e8e3a334 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

The contract's stated defense — "the counter's frozen-case-set check rejects
a stub selftest missing the four frozen case ids" — rejects only stubs that
*omit* ids; it cannot reject stubs that *fabricate* them.

## Fixture recipe (reproducible; dir deleted after use, per lane rule)

```
D=/fast/scratch/hyaku/kake-r63/CriticClaims/donothing
git -C "$D" init -q            # assert: git -C "$D" rev-parse --show-toplevel == $D
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 13d4519818db28cd0aa912e49020659140d7b9fa | tar -x -C "$D"
# add the five files above; FROZEN_QUOTE taken verbatim from the frozen counter source
git -C "$D" add -A
git -C "$D" -c user.name='DoNothing Control' -c user.email='donothing@fixture.invalid' commit -q -m 'do-nothing control'
# fixture rev: 09cd73d535de110a5467a4e5f2b914d0e8e3a334
# then run both frozen counters with --root "$D" --revision 09cd73d535de110a5467a4e5f2b914d0e8e3a334
```

Scratch state after the run: fixture dir and helper files under
`/fast/scratch/hyaku/kake-r63/CriticClaims/` deleted; `scratch_cleanup=clean`.
No tools installed. No fleet/corpus/SOURCES/scripts/templates files touched.

## Fairness — the measured work is real; the design is what's falsified

For the record, so this attack is not read as impugning the seat work:
- `git show 05b0d7f4…:extract_text.py` re-run on the retained
  `S432.html` reproduces the measured `S432.txt` byte-identically
  (sha256 `8b90d096…2a69` both), and the measured tree adds fetch provenance
  `.ufo/waves/round-63/sources/S432.live.html` (sha256 of the live body
  equals the retained body per the lesson's re-open record).
- The measured `scripts/quote_class.py` genuinely classifies (it reads the
  blobs; its `s432_real` case binds against the retained corpus).
- Re-running the frozen counters at the measured commit reproduces the
  committed receipts exactly (`met=true`, exit 0, both).

So the round's executed repair is sound. What fails is the claim design's
do-nothing resistance: both frozen counters certify a tree in which none of
that work happened.

## Impacted axes

- **C1 calibration (lowest owned axis, 2/10):** the frozen predicate is
  satisfiable without the semantic repair it claims to certify; the
  `met=true` receipt is not evidence that the S432 disagreement was resolved
  by derivation. The claim as designed is a fixable defect (see correction),
  not yet a tradeoff the judge must reject.
- **C2 operability (HOLD 10):** same — `present=1 selftest=4/4 met=true` is
  not evidence a quote-class tool exists; a JSON emitter suffices.
- **Freeze rule / kill rule:** the kill rules cover marker-only greens; they
  do not cover digest-self-consistent fabrication (C1) or fabricated case ids
  (C2). The round-35 criterion (a) (cheapest do-nothing control must miss,
  scored and committed before the build) was not applied to this round's own
  targets.
- Downstream risk: any future round reusing `c63_calibration.py`'s
  blob-binding pattern (sha256-pin + inline substring class) inherits the
  provenance gap wherever a text blob is author-produced rather than
  fetch-retained.

## Smallest safe correction

1. **C1 (closes the provenance hole, preserves separability):** in
   `c63_calibration.py`, re-derive the flat text from the retained raw blob
   using the committed recipe at the measured revision — execute
   `.ufo/waves/round-63/quote-class/extract_text.py` (read via `git show`
   into a temp dir) on the `git show`n `S432.html`, and require the committed
   `S432.txt` to be byte-equal to that derivation before honouring
   `textSha256`/`blobs_match`. This keeps C1 independent of
   `scripts/quote_class.py` and adds one subprocess + one digest compare.
   Alternative of equivalent strength: pin `textSha256` to
   `sha256(extract(raw))` instead of `sha256(committed S432.txt)`.
2. **C2 (closes the canned-JSON hole):** after the selftest JSON passes, run
   the copied tool's `classify` subcommand on two held-out probes whose
   classes the counter computes independently from the blobs at the measured
   revision (e.g. a verbatim span of the retained HTML → `raw-substring`; a
   nonsense span → `absent`) and require agreement. A canned emitter fails
   the probe.
3. **Process:** land a committed do-nothing control receipt (this fixture's
   recipe and red-after output) alongside any counter revision, per round-35
   QUALITY criterion (a); and extend the C1 kill-rule wording from
   "marker-only green" to "any tree lacking the retained-rendering
   derivation", so digest-self-consistent fabrication is in scope.

## Answer to the assigned question

Could a do-nothing round reach both targets with the frozen counters? **Yes —
demonstrated at fixture rev `09cd73d535de110a5467a4e5f2b914d0e8e3a334`, exit 0
on both.** Could the targets have been met by the round-62 tree plus trivia?
**Yes — the delta is five small files (~2.4 KB), two of four C1 components
were already green at base, and the resulting receipts are
component-identical to the committed after-receipts.** The targets are within
a do-nothing control's reach as designed; corrections 1–2 above are the
smallest changes that put them out of reach.
