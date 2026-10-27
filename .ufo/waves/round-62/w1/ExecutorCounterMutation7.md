# ExecutorCounterMutation7 — Unicode quote-matching sensitivity probe (round 62, C1)

**Seat:** ExecutorCounterMutation7 (leaf executor; advisory only)
**Item:** Probe Unicode quote matching sensitivity in the c62 counter using scratch copies; report if NFKC or punctuation substitutions could evade it.
**Date:** 2026-10-27
**Verdict:** **No evasion found via NFKC or punctuation substitution.** The frozen quote needle is a byte-exact Python `in` test on NFC-stable text; NFKC does **not** weaken it, and every punctuation mutation I tried made the counter *stricter*, not looser. However, the probe surfaced **three real weaknesses of a different kind** (locality, negation, and vacuous location conjunct), plus one **source-fidelity trap** that will bite the implementer. All findings are advisory; **nothing in the lane was modified**.

---

## 1. Scope and method

Everything was done in scratch. The lane repo, the frozen claim, the frozen counter, the criteria and the score were **not** touched.

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && git rev-parse HEAD
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ git status --porcelain
?? .ufo/waves/round-62/          # wave dir only; no tracked-file modification
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

That sha256 matches the frozen counter named in the round-62 contract (`ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`).

**Scratch fixture.** A throwaway git repo at `/fast/scratch/hyaku/kake-r62/ExecutorCounterMutation7/fixture` was populated from the *base* blobs of `c341a7a` (spot-check, knowledge, QUALITY, SOURCES) and committed at `d0f924388f6f98139d4be5867ca2b79b0c6fe25d`. Every scenario re-reset the fixture to that base before applying a mutation, so no state leaked between runs. The counter was copied into scratch and re-verified byte-identical before every run:

```
counter sha256 lane   = ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d
counter sha256 scratch= ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  identical=True
```

The frozen counter was then run against the scratch fixture revisions with the documented invocation shape:
`python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision <rev>`.

**Baseline reproduced.** The scratch fixture at base reproduces the contract's recorded base-control exactly:

```
revision=d0f924388f6f98139d4be5867ca2b79b0c6fe25d disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false   (exit 1)
```

and against the real lane base:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

**Full-pipeline harness.** For the mutation tests I first built a complete, honest round-62 implementation *inside the fixture* — appended correction to the knowledge file, appended a `## Criterion — substantive located quote` section to QUALITY.md pointing at `corpus/lessons/round-61-verifier-spotcheck.md`, and created `corpus/lessons/round-62.md` with a `## Gate` section mentioning S432/Agree/Reject — so the counter could reach `met=true` and the *only* variable left was the quote's byte form. Baseline of that harness:

```
honest_exact_u2019   rc=0 qc=1 crit=1 gate=1 row=1 met=true
```

---

## 2. The frozen needle, and what the source actually contains

`c62_calibration.py:16`

```python
QUOTE = "response header can be used to require checking of a response’s Content-Type header against the destination of a request"
```

The only non-ASCII character in the needle is **U+2019 RIGHT SINGLE QUOTATION MARK** in `response’s`. The location conjunct on `:33` adds `S432 §3.6` (U+00A7 SECTION SIGN).

### 2.1 The retained source does NOT literally contain the needle

This is the most actionable finding for the implementer. The retained body `.ufo/waves/round-61/sources/S432.html` §3.6 lines 6151–6154 reads (de-tagged, whitespace-collapsed):

```
response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.
```

Note the **backticks around `Content-Type`** — they are literal characters in the WHATWG HTML source text, not markup artifacts of the extraction.

```
needle (plain 'Content-Type') found in de-tagged source text?  False
needle with backticks '`Content-Type`' found?                 True
needle found after removing backticks?                         True
```

And in the **raw** HTML segment the needle is absent too, because the sentence is broken across elements and lines:

```
QUOTE literal present in RAW source segment: False
```

Full clean re-verification (each scenario reset to base first):

```
source-derived quote (de-tagged, ws-collapsed): 'response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.'
  contains frozen needle? False
copy: source sentence verbatim (backticks kept)      rc=1 qc=0 met=false
copy: source sentence, backticks stripped            rc=0 qc=1 met=true
copy: source sentence, backticks->none + plain CT    rc=0 qc=1 met=true
copy: exact frozen needle                            rc=0 qc=1 met=true
```

**Advisory for the implementer:** the correction must carry the sentence with **plain `Content-Type` (no backticks)** and the **U+2019 apostrophe**. A faithful verbatim copy of the spec text — which is the *honest* thing to do, and which round-61's rejected lead-in was not — **fails the counter**. The backticks must be stripped deliberately. This is a quoting-convention choice the correction should state explicitly so a future reader knows the backticks were removed for the counter's sake, not accidentally.

### 2.2 Punctuation substitutions do not evade the counter — they defeat it

Full-pipeline results, changing **only** the quote's byte form:

```
ascii_apostrophe            rc=1 qc=0 crit=1 gate=1 row=1 met=false
fullwidth_apos_ff07         rc=1 qc=0 crit=1 gate=1 row=1 met=false
modifier_apos_u02bc         rc=1 qc=0 crit=1 gate=1 row=1 met=false
left_apos_u2018             rc=1 qc=0 crit=1 gate=1 row=1 met=false
hyphen_u2010                rc=1 qc=0 crit=1 gate=1 row=1 met=false
hyphen_u2011                rc=1 qc=0 crit=1 gate=1 row=1 met=false
hyphen_fullwidth_ff0d       rc=1 qc=0 crit=1 gate=1 row=1 met=false
minus_u2212                 rc=1 qc=0 crit=1 gate=1 row=1 met=false
nbsp_inside_quote           rc=1 qc=0 crit=1 gate=1 row=1 met=false
lowercase_contenttype       rc=1 qc=0 crit=1 gate=1 row=1 met=false
extra_space_in_quote        rc=1 qc=0 crit=1 gate=1 row=1 met=false
backticked_contenttype      rc=1 qc=0 crit=1 gate=1 row=1 met=false
leading_capital_shift       rc=1 qc=0 crit=1 gate=1 row=1 met=false
```

Every single punctuation/Unicode mutation flips `quote_correction` from `1` to `0` and `met` from `true` to `false`. **There is no substitution that makes a wrong-but-lookalike quote satisfy the counter.** The needle is compared with Python's `in` operator on raw `str`, so it is byte-exact.

### 2.3 NFKC specifically does *not* help — and this matters for how the needle should be read

```
NFKC(U+2019) == U+2019 ?   True
NFKC(U+FF07) = "'"
NFKC(U+2010) = '‐'          (U+2010 has NO compatibility decomposition)
NFKC(U+00A0) = ' '
NFKC(U+FF0D) = '-'
NFKC(needle quote) contains U+2019 ?  True
```

The decisive fact: **U+2019 has no NFKC decomposition.** NFKC therefore *cannot* unify the needle's `’` with an ASCII `'`. Consequently:

```
NFKC only:         ascii haystack matches NFKC needle ?   False
NFKC + curly-fold: folded haystack matches folded needle ? True
```

So a matcher that applied **NFKC alone** would still reject the ASCII-apostrophe variant — identical to today's behavior — while a matcher that applied **NFKC *plus* an explicit curly→straight fold** would *accept* it, thereby **loosening** the frozen needle. The frozen counter does neither, and its exact-byte behavior is the *stricter, safer* choice.

**Conclusion on the assigned question:** NFKC or punctuation substitutions **cannot evade** the c62 counter. NFKC is in fact the wrong lens here, because the needle's only non-ASCII character (U+2019) is precisely the one character NFKC leaves untouched. If a future revision ever wanted to be tolerant of an ASCII apostrophe, it would need an explicit quote-folding table, and that would be a *loosening*, not a hardening.

---

## 3. Weaknesses found (different class from Unicode — locality, negation, vacuity)

These are real and reproducible, but they are **not** evasion-by-encoding. Reporting them as advisory only; I did not change the counter.

### 3.1 The quote's *location* is not checked — the correction can point away from it

`c62_calibration.py:33` tests three independent substrings against the whole knowledge blob. It never checks that the quote lives under the correction heading. Reproduced:

```
block_without_S432_§3.6   rc=0 qc=1 met=true
block_with_location_marker rc=0 qc=1 met=true
```

A block with **no `S432 §3.6` at all** still scores `quote_correction=1`. This matters because the location conjunct is vacuous on this file:

```
location marker 'S432 §3.6' in BASE knowledge: True
   line 75: 'location [S432 §3.6]:'
   line 86: 'the first one to `nosniff` as an ASCII case-insensitive match (S432 §3.6,'
```

`S432 §3.6` **already appears twice in the base knowledge file** (`corpus/knowledge/response-header-expectations.md:75,86`). The `"S432 §3.6" in data["knowledge"]` conjunct is therefore satisfied by the *pre-existing* content and contributes nothing to distinguish the new correction. The same holds for the heading marker being matched anywhere in the file, including in prose:

```
'Round-62 correction' (exact heading)      rc=0 qc=1 met=true
'Round-62 correction' inside prose         rc=0 qc=1 met=true
'Round-62 Correction' (capital C)          rc=1 qc=0 met=false
'Round–62 correction' (en dash)            rc=1 qc=0 met=false
'Round 62 correction' (no hyphen)          rc=1 qc=0 met=false
'Round-62 correction' with NBSP            rc=1 qc=0 met=false
'round-62 correction' (lowercase r)        rc=1 qc=0 met=false
```

Note the `S432 §3.6` conjunct is *also* punctuation-sensitive in isolation (NBSP/NNBSP/no-space variants), but because the base file already satisfies it, that sensitivity is unobservable in practice — see §3.4.

### 3.2 A *refuting* correction still scores `met=true`

The counter is purely lexical; it cannot see that the correction's own prose contradicts the quoted sentence. Reproduced with the exact needle present but the surrounding prose explicitly refusing it:

```
correction explicitly REFUTES the quoted text:
  rc=0 ... quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
```

The countered text was: *"Location S432 §3.6. The following is NOT substantive evidence and does not support the claim: “<needle>” / No substantive quote was located; the prior lead-in remains generic."*

### 3.3 A quote in an unrelated section, with the correction merely pointing at it, scores `met=true`

```
quote in unrelated section, correction points at it:
  rc=0 ... quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
```

The knowledge file got a `## Quoted spec text (archive)` section containing the quote, and a `## Round-62 correction` section saying only *"The prior lead-in was generic; see the quoted spec text above."* The counter cannot tell the correction carries the quote from the correction merely cross-referencing it.

### 3.4 `unresolved` is not independently derived — it is implied by the other conjuncts

`c62_calibration.py:39-41`

```python
resolved  = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
unresolved = disagreements if not resolved else 0
met = unresolved == 0 and resolved
```

The `Disagree` row stays in the spot-check file (per the contract: *keep the row, do not mark it rejected*), so `disagreements` remains `1` forever. `unresolved` is then forced to `0` by `resolved`. Confirmed with the row **retained**:

```
rc=0 revision=b9a89f5e… disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
spot-check S432 Disagree row still present: True
```

This is consistent with the contract's "keep the row" instruction and is **not** a defect — but it does mean the `unresolved_round61_spotcheck_disagreements == 0` conjunct of the frozen predicate is **not independently evidenced**; it is a tautology once the other four conjuncts hold. Worth stating plainly in the claim's evidence rather than letting the `unresolved=0` figure read as independent proof that the disagreement was adjudicated. The genuine evidence of adjudication is the appended correction + QUALITY criterion + lesson gate.

### 3.5 The `lesson_gate` conjunct is lexical and case-sensitive

`c62_calibration.py:36-37` requires `"## Gate"`, `"S432"`, `"Agree"` and `"Reject"` as substrings. `"Agree"` is a substring of `"Disagree"`? No — `"Agree" in "Disagree"` is `False` (capital `A`), but `"Reject" in "Rejected"` is `True`. Reproduced:

```
lesson says 'Agree'/'Reject' (capital)         rc=0 qc=1 met=true
lesson says only 'Disagree'/'Rejected'         rc=1 qc=1 met=false   (lesson_gate=0)
lesson says 'agreement'/'rejection' (lowercase) rc=1 qc=1 met=false   (lesson_gate=0)
```

So the lesson must contain a **standalone capitalized `Agree`** and any `Reject`-prefixed token. `Rejected`/`rejects` satisfies the second; `Disagree`/`Disagreed` does **not** satisfy the first. Advisory: write the lesson gate with the literal capitalized tokens, and be aware that `Disagree` alone will silently fail the `Agree` conjunct.

---

## 4. What the counter does *not* read

`PATHS` (`c62_calibration.py:9-15`) is the complete read set:

```
corpus/lessons/round-61-verifier-spotcheck.md
corpus/knowledge/response-header-expectations.md
corpus/QUALITY.md
corpus/lessons/round-62.md
corpus/SOURCES.md
```

The retained source body `.ufo/waves/round-61/sources/S432.html` is **never opened** by the counter. The `source_row` conjunct (`:38`) only checks that the string `| S432 |` appears in `corpus/SOURCES.md` — it is already true at base, so it is a no-op preservation check, not a grounding check. There is **no cross-check that the quoted sentence actually occurs in the retained body**. Provenance is established by the human/quorum reading the spec, not by the counter.

Similarly, an append landing in a file outside `PATHS` is invisible:

```
quote in file OUTSIDE PATHS: rc=1 ... quote_correction=0 met=false
```

---

## 5. Summary table

| # | Finding | Direction | Evidence |
|---|---|---|---|
| F1 | Punctuation/Unicode substitution **cannot** evade the quote check; every mutation flips `quote_correction` 1→0 | counter stricter | §2.2 (13 mutants) |
| F2 | **NFKC cannot** unify U+2019 with ASCII `'`; NFKC-alone behaves identically to today; NFKC+curly-fold would *loosen* the needle | counter stricter | §2.3 |
| F3 | The retained source text contains **backticks around `Content-Type`**; a verbatim spec copy **fails** the counter (qc=0) | implementer trap | §2.1 |
| F4 | `"S432 §3.6"` is **already satisfied by base knowledge** (lines 75, 86) → the location conjunct is vacuous | counter weaker | §3.1 |
| F5 | The quote's **location** is unchecked; correction may point away from it → `met=true` | counter weaker | §3.3 |
| F6 | A correction that **refutes** the quoted sentence still scores `met=true` | counter weaker | §3.2 |
| F7 | `unresolved` is implied by the other conjuncts; the `Disagree` row stays and `disagreements=1` persists | by design; report honestly | §3.4 |
| F8 | `lesson_gate` needs a standalone capitalized `Agree`; `Disagree` does not satisfy it | lexical | §3.5 |
| F9 | The counter never reads the retained source body; `source_row` is a base-true no-op | counter weaker | §4 |

---

## 6. Advisory (no action taken by me)

1. **The implementer must strip the backticks** around `Content-Type` and keep the **U+2019** apostrophe, or `quote_correction` will be `0`. This is the single most likely way the wave's own implementation fails its counter. The correction should say so explicitly, so the stripped backticks read as a deliberate quoting convention rather than an inaccuracy.
2. **Place the quote inside the `## Round-62 correction` block itself**, not in an archive section it merely references, and write prose that *grounds* the claim — the counter cannot enforce either (F5, F6), but the frozen claim's own wording ("a substantive quote in S432 §3.6 and explain its support") asks for it and a future reviewer will read it.
3. **Do not cite `unresolved=0` as independent evidence that the round-61 disagreement was adjudicated** (F7). The honest statement is: the S432 `Disagree` row is retained, and the correction + criterion + lesson gate are the evidence of adjudication.
4. **Write the lesson gate with literal capitalized `Agree` and a `Reject`-prefixed token** (F8).
5. **No change to the counter is warranted on Unicode grounds.** The byte-exact needle is the correct choice; any loosening would require an explicit quote-folding table and would reduce rigor. F4–F6 are lexical/locality gaps, not encoding gaps, and they are the L1's call, not mine.

---

## 7. Commands and outputs (reproduction)

All in scratch `/fast/scratch/hyaku/kake-r62/ExecutorCounterMutation7/` (fixture repo at `fixture/`, probes `probe.py`…`probe6.py`, results in `results.json`).

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ git rev-parse HEAD
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
$ python3 -B probe3.py     # full-pipeline mutation sweep  -> §2.2
$ python3 -B probe4.py     # vacuity / locality / NFKC        -> §2.3, §3.1
$ python3 -B probe5.py     # unresolved mechanism / PATHS    -> §3.4, §4
$ python3 -B probe6.py     # clean re-verification            -> §2.1, §3.1-3.5
```

**Lane state at report time:** `HEAD=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`, `git status --porcelain` shows only the untracked wave directory. **No tracked lane file, no claim, no counter, no criterion and no score was altered by this seat.** This report (`.ufo/waves/round-62/w1/ExecutorCounterMutation7.md`) is the seat's only write outside scratch.
