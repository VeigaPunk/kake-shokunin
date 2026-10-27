# ExecSwappedLabel — round-63 w1 seat report

**Item.** Build the swapped-label control the round-50 criterion names: a
scratch repo whose ledger records the S432 span as `raw-substring` while the
blobs derive `collapsed-only`. Run `c63_calibration.py` (expect `met=false` via
`class_match=0`). Then swap the other way (record `collapsed-only` for a span
that IS a raw substring) and run the lane tool's `classify` on it directly.
Scratch under `/fast/scratch/hyaku/kake-r63/ExecSwappedLabel/`.

**Verdict.** Both halves of the item behave as the round-50 criterion
requires. The one-token label swap (ledger `collapsed-only` →
`raw-substring`, blobs untouched) turns C1 red through `class_match=0` while
`blobs_match=1` and `derived=collapsed-only` — the counter detects the swap
against its own committed blobs, not against the ledger's wording. The
other-way swap (ledger records `collapsed-only` for a span that IS a raw
substring) is likewise caught: the counter re-derives `raw-substring` and goes
red via `class_match=0`, and the lane tool's `classify` independently derives
`raw-substring` for the same span. The counter's label check is exact-string,
not a prefix/loose match: `"collapsed-only "` (trailing space) also fails.

**No C1/C2 kill-rule breach found.** The after receipts reproduce (`met=true`
for C1, `present=1 selftest=4/4 frozen_cases=ok met=true` for C2), the two
committed controls still print `met=false`, and no fixture in this seat
reproduced a marker-only green. No frozen claim, counter, receipt, registry
row, corpus file or ledger was edited; the fleet repo working tree is
unchanged; scratch deleted at end of wave.

**Tooling.** None installed. No pacman transaction, no `uv`/`npx`/binary
install. Everything below uses pre-existing `git` and `python3`.

---

## 1. Objects under test (unmodified, frozen)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-63/c63_calibration.py \
             .ufo/waves/round-63/c63_quote_tool.py \
             scripts/quote_class.py \
             .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All four match the contract's frozen values
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md:22-28`).
The counters and the tool were run **as committed**; nothing in the fleet repo
was edited.

Reference greens (the real measured commit, unmodified tree), so the reds
below are attributable to the fixtures and not to an always-red counter:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

These match the committed receipts
`.ufo/waves/round-63/controls/after-c1.txt` and `after-c2.txt` byte for byte.

---

## 2. The label the counter compares against

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py:130-145`
(re-read verbatim):

```python
    if raw_blob is not None and text_blob is not None and ledger_err is None:
        row = ledger.get("S432")
        if row:
            blobs_match = int(
                row.get("rawSha256") == hashlib.sha256(raw_blob).hexdigest()
                and row.get("textSha256") == hashlib.sha256(text_blob).hexdigest()
                and row.get("quote") == FROZEN_QUOTE
            )
            if blobs_match:
                derived = classify(FROZEN_QUOTE,
                                   raw_blob.decode("utf-8", errors="replace"),
                                   text_blob.decode("utf-8", errors="replace"))
                class_match = int(derived == "collapsed-only"
                                  == row.get("matchClass"))

    quote_correction = int(correction and blobs_match and class_match)
```

and the inlined derivation at `c63_calibration.py:59-68`:

```python
def classify(quote: str, raw: str, text: str) -> str:
    """Round-50 class semantics, inlined so C1 is verifiable without the
    scripts/quote_class.py tool (claim separability; the tool re-derives the
    same class as C2 evidence, never as a C1 gate)."""
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"
```

`class_match` is a chained equality — `derived == "collapsed-only" ==
row["matchClass"]` — so it holds only when **both** the re-derived class and
the recorded label are exactly the string `collapsed-only`. The ledger's
wording is never taken as evidence of the class; the class is re-derived from
the two retained blobs and the ledger is only compared against it.

The criterion this implements is `corpus/QUALITY.md:1100-1108` (round 50):
"a span that is a substring of the retained HTML is `raw-substring`, a span
that survives only whitespace collapse is `collapsed-only` … a collapsed-only
span is never described as a raw substring nor the reverse — the two classes
are different facts and a swapped label fails the check."

---

## 3. Fixture construction (shared across all fixtures below)

Source of truth for every corpus byte copied into a fixture: the fleet repo at
the measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, extracted
read-only with `git show <rev>:<path>`. Every fixture is an independent git
repo with a throwaway identity set **inside that repo only** — the global
identity was never touched (`git config --global --list` still shows the
pre-existing `user.name=probe`).

```
$ D=/fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapA
$ mkdir -p "$D" && git -C "$D" init -q
$ TL=$(git -C "$D" rev-parse --show-toplevel); echo "$TL"
/fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapA
$ test "$TL" = "$D" && echo TOPLEVEL_OK
TOPLEVEL_OK
$ git -C "$D" config user.name "r63 swaplabel fixture"
$ git -C "$D" config user.email "swaplabel-fixture@example.invalid"
```

The top-level assertion `git rev-parse --show-toplevel == $D` was checked and
printed `TOPLEVEL_OK` for **every** fixture before its first commit (swapA,
swapB, swapC, swapD, swapE, swapF, swapG, swapH, swapI, swapJ).

Fixture-local identities, confirmed after the fact:

```
$ for d in swapA swapB swapC swapD swapE swapF swapG swapH swapI swapJ; do
    printf "%-7s " "$d"; git -C /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/$d config user.name; done
swapA   r63 swaplabel fixture
swapB   r63 swaplabel fixture
swapC   r63 swaplabel fixture
swapD   r63 swaplabel fixture
swapE   r63 swaplabel fixture
swapF   r63 swaplabel fixture
swapG   r63 swaplabel fixture
swapH   r63 swaplabel fixture
swapI   r63 swaplabel fixture
swapJ   r63 swaplabel fixture
```

---

## 4. Baseline control — the fixture greens before the swap

To show the reds below come from the label and not from a fixture missing
bytes, `swapA` was first committed with the **pristine** measured-commit
blobs and the pristine ledger, then run:

```
$ git -C "$D" add -A && git -C "$D" -c commit.gpgsign=false commit -q -m "r63 control: pristine measured-commit blobs (collapsed-only label)"
$ REV=$(git -C "$D" rev-parse HEAD); echo "fixture_rev=$REV"
fixture_rev=6ec7a7640c8a32c07703b28fead8117cdee36595
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"
revision=6ec7a7640c8a32c07703b28fead8117cdee36595 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

The pristine fixture reproduces the fleet's own `met=true` line exactly. The
fixture is complete; only the label changes below.

---

## 5. HALF 1 — label swapped to `raw-substring` while the blobs derive `collapsed-only`

The swap is a **one-token** change to the ledger. Byte-exact diff between the
green baseline commit and the swapped commit:

```
$ git -C "$D" diff 6ec7a7640c8a32c07703b28fead8117cdee36595 6a28b7615e3d8413a5aa1cbbeac3ecadd439c8fc -- .ufo/waves/round-63/quote-class/quote-classes.json
diff --git a/.ufo/waves/round-63/quote-class/quote-classes.json b/.ufo/waves/round-63/quote-class/quote-classes.json
index 7b2a907..7398de8 100644
--- a/.ufo/waves/round-63/quote-class/quote-classes.json
+++ b/.ufo/waves/round-63/quote-class/quote-classes.json
@@ -6,7 +6,7 @@
   {
    "id": "S432",
    "quote": "The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.",
-   "matchClass": "collapsed-only",
+   "matchClass": "raw-substring",
    "textPath": ".ufo/waves/round-63/quote-class/S432.txt",
    "rawPath": ".ufo/waves/round-61/sources/S432.html",
    "textSha256": "8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69",
```

```
$ git -C "$D" diff --stat 6ec7a7640c8a32c07703b28fead8117cdee36595 6a28b7615e3d8413a5aa1cbbeac3ecadd439c8fc
 .ufo/waves/round-63/quote-class/quote-classes.json | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Both blobs are **untouched** — the sha256 pins still match, so `blobs_match`
stays `1`, and the counter re-derives the class from the very same bytes:

```
$ git -C "$D" add -A && git -C "$D" -c commit.gpgsign=false commit -q -m "r63 swapped-label control: ledger records raw-substring, blobs derive collapsed-only"
$ REV=$(git -C "$D" rev-parse HEAD); echo "swapped_rev=$REV"
swapped_rev=6a28b7615e3d8413a5aa1cbbeac3ecadd439c8fc
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"
revision=6a28b7615e3d8413a5aa1cbbeac3ecadd439c8fc disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

**Result — exactly the predicted failure mode.** `blobs_match=1` (the pins are
honest), `derived=collapsed-only` (the blobs say so), `class_match=0` (the
ledger disagrees with them), `quote_correction=0`, `unresolved=1` (the S432
disagreement is restored), `met=false`, exit 1.

The counter is not fooled by the ledger's wording in either direction: it
re-derives `collapsed-only` from the committed blobs and then finds the
recorded `raw-substring` false. The round-50 "swapped label fails the check"
sentence holds for the round-63 counter.

---

## 6. HALF 2 — the other way: `collapsed-only` recorded for a span that IS a raw substring

Two fixtures, because there are two distinct ways to state the other-way swap.

### 6a. `swapC` — the S432 span itself is a raw substring, the ledger still says `collapsed-only`

The retained HTML is made to carry the frozen span verbatim (so the span
genuinely *is* a raw substring of the HTML), and the ledger's `rawSha256` is
re-derived from that doctored blob so the pin still holds. The recorded class
stays `collapsed-only` — the swap.

```
$ python3 - <<'PY'   # appends the frozen span verbatim to the retained HTML,
...                   # then re-derives the ledger's rawSha256 from the new bytes
PY
swapC rawSha256: ad5857c5ceee02a5731fb2f8424063869e623da09c177a09de1fa94e3a0ce79e
swapC textSha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
```

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py --root "$D" --revision 34ab842294258eb13c9c38876873e8f3797b2a53
revision=34ab842294258eb13c9c38876873e8f3797b2a53 disagreements=1 quote_correction=0 blobs_match=1 derived=raw-substring class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

`derived=raw-substring` — the counter re-derives the class from the blobs and
finds the recorded `collapsed-only` false. `blobs_match=1`, so this is a pure
label mismatch, not a missing-blob artefact.

### 6b. `swapB` — a second ledger row claims `collapsed-only` for a raw-substring span

Pristine committed blobs (both sha256 pins unchanged from the measured
commit); the ledger additionally carries an `S432-ALT` row whose quote is
verifiably a raw substring of the retained HTML, recorded as `collapsed-only`.
The span was chosen by scanning the committed HTML for a plain-text run
present in the raw bytes:

```
$ python3 -c "..."
in_raw: True
in_text: True
```

### 6c. The lane tool's `classify`, run directly on the swapped span

This is the item's second half — the tool invoked on the span directly, not
through any counter. `scripts/quote_class.py` was run **unmodified** from the
fleet root (its sha256 is the frozen `431e75e8…` above):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B scripts/quote_class.py --json classify \
    --quote "the response of a redirect has to be set if it was set for previous responses in the redirect chain," \
    --raw   /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapB/.ufo/waves/round-61/sources/S432.html \
    --text  /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapB/.ufo/waves/round-63/quote-class/S432.txt
{"derived": "raw-substring"}
exit=0
```

The tool derives `raw-substring` for the very span the ledger records as
`collapsed-only` — the same fact the counter re-derives, reached by a
different code path (`scripts/quote_class.py:32-38`, byte-identical logic to
the counter's inlined `classify`).

Control on the same invocation path, with the *correctly* labelled S432 span
against the *same* pristine blobs:

```
$ python3 -B scripts/quote_class.py --json classify \
    --quote "The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request." \
    --raw   /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapB/.ufo/waves/round-61/sources/S432.html \
    --text  /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapB/.ufo/waves/round-63/quote-class/S432.txt
{"derived": "collapsed-only"}
exit=0
```

Same blobs, same tool, same invocation — only the span differs, and the
derived class differs accordingly. The tool's answer is a function of the
span and the blobs, not of any recorded label.

And the tool against `swapC`'s doctored blobs, for the S432 span itself:

```
$ python3 -B scripts/quote_class.py --json classify \
    --quote "The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request." \
    --raw   /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapC/.ufo/waves/round-61/sources/S432.html \
    --text  /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapC/.ufo/waves/round-63/quote-class/S432.txt
{"derived": "raw-substring"}
exit=0
```

Tool and counter agree independently on the same bytes.

---

## 7. Supplementary probes (same fixture family)

These are not required by the item; they bound how the label check behaves.
All are `met=false` / exit 1.

| Fixture | What was changed | Counter output (key fields) | Exit |
|---|---|---|---|
| `swapD` | ledger's two sha256 pins exchanged (`textSha256`←raw, `rawSha256`←text); blobs byte-identical to the measured commit | `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| `swapE` | ledger `textPath`/`rawPath` repointed at nonexistent round-62 paths; sha256 pins and label unchanged | `quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true` | 0 |
| `swapF` | retained HTML made to carry the span verbatim **and** the flat-text rendering stripped of it; both sha256 pins re-derived from the committed blobs | `quote_correction=0 blobs_match=1 derived=raw-substring class_match=0 … met=false` | 1 |
| `swapG` | C1 tree built with **no** `scripts/quote_class.py` at all (separability clause) | C1: `… class_match=1 … met=true` / C2: `present=0 selftest=unevaluable met=false` | C1 0, C2 1 |
| `swapH` | label written as `"collapsed-only "` (trailing space) | `blobs_match=1 derived=collapsed-only class_match=0 … met=false` | 1 |
| `swapI` | ledger file is malformed JSON | `blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |
| `swapJ` | ledger is valid JSON but has no `classes` key | `blobs_match=0 derived=unevaluable class_match=0 … met=false` | 1 |

Raw outputs for the non-obvious ones:

```
=== swapD blob-role swap ===
revision=6e6b8700ac81ac98ca06c6bc07d48111ccc0c8c2 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== swapH near-miss label 'collapsed-only ' ===
revision=423b1993cca9a7c953e36cfaf1c252b51b1354e2 disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== swapI malformed ledger ===
revision=5e78b41f761385fb838586a33259fba3dc2704a4 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== swapJ ledger without classes key ===
revision=bcac39547b2ff5a37d938af2c97ec9611322780c disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== swapF raw-only span, sha pins re-derived ===
revision=7b5a279db7b32884a350fced30321653a620b420 disagreements=1 quote_correction=0 blobs_match=1 derived=raw-substring class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

`swapH` confirms the check is an exact-string comparison, not a prefix or
loose match: `"collapsed-only "` does not satisfy `derived == "collapsed-only"
== row["matchClass"]`.

`swapG` confirms the contract's Separability clause
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md:75-82`)
in the direction the fixture was built to test: **C1 greens on a tree where
`scripts/quote_class.py` never landed**, because C1 re-derives the class
inline (`c63_calibration.py:59-68`) and never gates on the tool, while **C2
correctly reds on the same tree** (`present=0 selftest=unevaluable met=false`).
The two claims do not couple.

`swapE` is the one green in that table and is reported as an observation, not
a claim defect: the counter never reads the ledger's `textPath`/`rawPath`
fields — it reads the two blobs from its own `QUOTE_REL`/`TEXT_REL`
constants (`c63_calibration.py:42-44`) and compares only the sha256 pins and
the label. Repointing the ledger's *path* fields at nonexistent files
therefore does not change the class that is derived, and the derived class is
still `collapsed-only` from the real blobs, so `met=true` is correct for that
tree. The paths are descriptive; the sha256 pins are the binding part, and
those are enforced (see `swapD`). No C1 predicate in the contract mentions the
path fields.

---

## 8. Claim-separability re-check under a swapped ledger

A tree carrying a swapped ledger label must not flip C2 (C2's counter reads
only the tool and its selftest — `c63_quote_tool.py:60-95`):

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py --root "$SWAPB" --revision a40a80611a44f2a5fd3b4daccd0249fa215b52ff
revision=a40a80611a44f2a5fd3b4daccd0249fa215b52ff present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

C2 is unaffected by the ledger's label (it never reads the ledger), while C1
on the same tree is red whenever the *S432* row's own label is swapped
(§5, §6a). The claims stay independently verifiable, as the contract's
Separability clause requires.

The tool's own selftest was also run from inside the fixture root, confirming
its cwd-bound fixture resolution behaves as the contract's freeze note
describes:

```
$ cd /fast/scratch/hyaku/kake-r63/ExecSwappedLabel/swapB && python3 -B scripts/quote_class.py --selftest --json
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": true, "passed": 4, "total": 4}
exit=0
```

---

## 9. Ground truth for the S432 span (why `collapsed-only` is the correct label)

The span is carried across inline markup in the retained HTML, so it is not a
raw substring there; it survives whole in the flat-text rendering. From the
retained raw bytes at
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html`
lines 6150-6154 (`git show 05b0d7f4:.ufo/waves/round-61/sources/S432.html`):

```html
  <h3 class="heading settled" data-level="3.6" id="x-content-type-options-header"><span class="secno">3.6. </span><span class="content">`<code>X-Content-Type-Options</code>` header</span><a class="self-link" href="#x-content-type-options-header"></a></h3>
  <p>The
`<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>`
response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used to require checking of a <a data-link-type="dfn" href="#concept-response" id="ref-for-concept-response④①">response</a>’s
`<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">header</a> against the <a data-link-type="dfn" href="#concept-request-destination" id="ref-for-concept-request-destination①⓪">destination</a> of a
<a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.

</p>
```

The `<code>`, `<dfn>` and `<a>` elements sit inside the sentence, so the
quoted span is not contiguous in the HTML; the flat-text rendering
(`.ufo/waves/round-63/quote-class/S432.txt`, recipe
`.ufo/waves/round-63/quote-class/extract_text.py`) does carry it contiguously.
Hence `collapsed-only` is the correct derivation, and the committed ledger's
label is correct — the round-61 S432 disagreement is genuinely resolved by
admitting this span as `collapsed-only` (round-50 rule), which is what the
measured commit's ledger says.

---

## 10. No-harm / scope check

* Fleet repo working tree unchanged. `git status --porcelain` in
  `/home/vgpnk/Projects/shokunin/kake-shokunin` shows only the wave's own
  untracked wave-control files (`?? .ufo/waves/round-63/w1.ready`,
  `?? .ufo/waves/round-63/w1.ready.dispatched`, `?? .ufo/waves/round-63/w1/`)
  — all created by the orchestrator, none by this seat;
  `git diff --stat HEAD` is empty. HEAD is `15eb965c1d0f23ce2a522c651e9306a0952da7d3`
  (the wave-spec commit, not a mutation by this seat).
* No commit, no push, no branch, no tag, no `git config --global` change, no
  jj invocation, no pacman transaction, no tool install.
* Nothing written outside this seat's report path and its own scratch tree
  under `/fast/scratch/hyaku/kake-r63/ExecSwappedLabel/`. No file under
  `considerthese/`, `.ufo/state`, `scripts/`, `templates/`, `corpus/`,
  `MANIFEST.json`, `LOG.md` or `SCORECARD.md` was created, edited or deleted.
* The frozen claim, the frozen counters, the frozen tool, the committed
  class ledger, the committed receipts and the S432 registry row were read and
  run, never edited. The committed receipts in
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls/`
  are byte-unchanged (`after-c1.txt`, `after-c2.txt`, `base-c1.txt`,
  `base-c2.txt`, `control-marker-fixture.txt`, `control-junk-fixture.txt`).
* Scratch tree deleted after the evidence above was captured.

---

## 11. Findings

1. **C1's swapped-label gate works in the direction the round-50 criterion
   names.** A one-token ledger change (`collapsed-only` → `raw-substring`)
   with untouched blobs turns the counter red via `class_match=0`, with
   `blobs_match=1` and `derived=collapsed-only` proving the counter
   re-derived the class from the committed bytes and then rejected the
   ledger's wording. `met=false`, exit 1.
2. **The gate is symmetric.** Recording `collapsed-only` for a span that IS a
   raw substring is equally fatal: the counter re-derives `raw-substring`
   (`swapC`, `swapF`) and goes red via `class_match=0`.
3. **The lane tool agrees with the counter, independently.**
   `scripts/quote_class.py classify` derives `raw-substring` for both
   swapped spans and `collapsed-only` for the genuine S432 span, from the
   same blobs, on the same invocation. Two independent code paths, one
   answer.
4. **The label check is exact.** `"collapsed-only "` fails (`swapH`).
5. **C1 and C2 remain separable.** C1 greens on a tree with no
   `scripts/quote_class.py` (`swapG`); C2 reds on that same tree; a swapped
   ledger label does not move C2 (`swapB`).
6. **Observation, not a defect.** The ledger's `textPath`/`rawPath` fields are
   not read by the counter (`swapE`): it resolves the two blobs from its own
   `QUOTE_REL`/`TEXT_REL` constants and binds them by sha256 only. Repointing
   the path fields at nonexistent files leaves `met=true`, and correctly so,
   since the class is still derived from the real blobs. The sha256 pins —
   which are what actually bind blob identity — are enforced (`swapD`).

**Recommendation.** None required: the frozen counters and the frozen tool
behave as the round-50 criterion and the round-63 contract require. The
`swapE` observation concerns the ledger's descriptive path fields only; it is
reported for the record and does not bear on either frozen predicate.

---

## 12. Artifacts

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py` | C1 counter under test, frozen sha256 `bcd16f68…`, unmodified |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py` | C2 counter, frozen sha256 `9fcbfad0…`, unmodified |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py` | lane tool, frozen sha256 `431e75e8…`, unmodified |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/quote-classes.json` | committed class ledger, frozen sha256 `5f48e26b…`, unmodified |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/contract.md` | frozen contract |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:1100-1108` | round-50 quote-class criterion |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecSwappedLabel.md` | this report |

Scratch (created, exercised, then deleted):
`/fast/scratch/hyaku/kake-r63/ExecSwappedLabel/{swapA,swapB,swapC,swapD,swapE,swapF,swapG,swapH,swapI,swapJ}`.

**Blockers.** None.
