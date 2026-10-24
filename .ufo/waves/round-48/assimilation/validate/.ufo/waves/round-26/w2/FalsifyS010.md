# FalsifyS010 — author-side falsification of receipt S010 (verdict HOLD)

Seat: KakeR26-2.FalsifyS010 (leaf member — no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S010.json` (verdict HOLD).
Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Row: `corpus/SOURCES.md:18`.

**Verdict: AGREE (severity: low).** The HOLD survives every falsification attack I ran and must **not** be
flipped. The one actionable defect is *not in the receipt* — it is a stale text-view digest/size asserted in the
row's own evidence trail, `.ufo/waves/round-26/w1/RowS010.md:4`. The receipt itself carries no digest or size
claim and is internally sound against the committed artifacts. This is the same defect class as sibling
`w2/FalsifyS024.md` (stale text-view numbers, graded AGREE/low) and `w2/FalsifyS027.md` (stale numbers promoted
into the receipt's own `anchorObserved`, graded DISAGREE/low). For S010 the stale numbers never entered the
receipt, so AGREE/low is the consistent label.

---

## Axes named

1. **Grounding** — does the receipt's quote ground *this* row's `teaches` (both clauses), not page chrome and not a
   neighbouring clause?
2. **Anchor identity** — is `anchorObserved` correct in the retained raw bytes `fetched/S010-1.raw.gz`?
3. **Drift** — did the live document change after the 2026-10-21 fetch in a way the receipt missed?
4. **Locator fidelity** — do the offsets/sizes/digests asserted anywhere in this row's evidence trail describe the
   committed artifacts at `e28312b`?
5. **Counter consistency** — does the receipt satisfy the counter's own gates, and is the row's decision coherent
   with its corpus entry?

---

## 1. Grounding — PASS (both clauses of `teaches`)

Row `corpus/SOURCES.md:18`:

```
| S010 | RFC 9110: HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 | spec | A | HTTP validator semantics for entity tags | Section 8.8.1 Weak versus Strong and 8.8.3 ETag; published June 2022 | Entity tags are opaque validators, and a strong validator can change for metadata reasons without representation-data changes | mined | 2026-10-19 | 365d | corpus/knowledge/ghp-etag-anatomy.md |
```

`teaches` has two conjuncts; the receipt claims both and both are verbatim in the retained raw bytes.

**Clause 1 — "Entity tags are opaque validators"** → `fetched/S010-1.raw.gz` raw lines 6620–6629, §8.8.3 ¶1:

```
6620           <p id="section-8.8.3-1">
6621     The "ETag" field in a response provides the current entity tag for
6622     the <a href="#selected.representation" class="xref">selected representation</a>, as determined at the conclusion of handling
6623     the request.
6624     An entity tag is an opaque validator for differentiating between
6625     multiple representations of the same resource, regardless of whether
6626     those multiple representations are due to resource state changes over
6627     time, content negotiation resulting in multiple representations being
6628     valid at the same time, or both. An entity tag consists of an opaque
6629     quoted string, possibly prefixed by a weakness indicator.<a href="#section-8.8.3-1" class="pilcrow">¶</a></p>
```

**Clause 2 — "a strong validator can change for metadata reasons without representation-data changes"** →
raw lines 6416–6422, §8.8.1 ¶3:

```
6416 <p id="section-8.8.1-3">
6417    A strong validator might change for reasons other than a change to the
6418    representation data, such as when a
6419    semantically significant part of the representation metadata is changed
6420    (e.g., <a href="#field.content-type" class="xref">Content-Type</a>), but it is in the best interests of the
6421    origin server to only change the value when it is necessary to invalidate
6422    the stored responses held by remote caches and authoring tools.<a href="#section-8.8.1-3" class="pilcrow">¶</a></p>
```

The receipt's own `quote` is the leading sentence of §8.8.1 ¶3 — the clause that carries the claim, not chrome and
not a neighbouring clause:

- `raw.count(b'A strong validator might change')` → **1**; `raw.count(b'An entity tag is an opaque validator')` → **1**.
- Committed text view `fetched/text/S010-1.txt`: each string occurs exactly **1**×; offsets 147062 and 155118.
- The counter's own gate passes on the committed artifacts, not only on a recomputation:
  `measure.quote_in_text(source_text, quote, view)` → **True** against the committed view; **True** against
  `text_of(gunzip(S010-1.raw.gz))`.
- Token/word limits: 15 tokens / 15 words (limits: ≥6 tokens, ≤25 words). ✓
- Row-specificity: the same sentence also occurs in `S028-1.txt` and `S033-1.txt`, but those are the RFC 9110
  **text** twin and are in the same `DOCUMENT_GROUPS = {S010, S028, S033}` set; the three quotes are distinct, so
  `quote_not_row_specific` does not fire. Verified by running the counter (§5).

**No defect.**

## 2. Anchor identity — PASS, with one wording nit

`anchorObserved` (receipt line 6):

> `§8.8.1 "Weak versus Strong", paragraph defining a strong validator; earlier in §8.8.3 "ETag": "An entity tag is an opaque validator" (single-line text view line 1)`

Verified in the raw bytes:

| Claim | Raw evidence | Verdict |
|---|---|---|
| §8.8.1 "Weak versus Strong" | 6398 `<section id="section-8.8.1">`; 6399 `<h4 id="name-weak-versus-strong">`; 6400 `8.8.1. … Weak versus Strong` | ✓ |
| §8.8.3 "ETag" | 6612 `<section id="section-8.8.3">`; 6613 `<h4 id="name-etag">`; 6614 `8.8.3. … ETag` | ✓ |
| "An entity tag is an opaque validator" | 6620–6624 (§8.8.3 ¶1) — the **first** paragraph of §8.8.3, so "earlier in §8.8.3" is accurate | ✓ |
| "single-line text view line 1" | committed `fetched/text/S010-1.txt`: 450,533 B, **1** newline (trailing), 448,451 chars → one line | ✓ |

**Wording nit (low, no verdict impact).** The receipt describes the §8.8.1 location as the *"paragraph defining a
strong validator"*. The paragraph that **defines** a strong validator is §8.8.1 ¶2 (raw 6412–6415:
`A "strong validator" is representation metadata that changes value whenever a change occurs to the representation
data that would be observable in the content of a 200 (OK) response to GET.`). The quoted sentence is the **next**
paragraph, §8.8.1 ¶3. The section is right and the `reason` field disambiguates by quoting the full ¶3 clause
through "(e.g., Content-Type)", so nothing is mis-grounded — but the anchor descriptor is off by one paragraph.
Optional fix, prose only:

```
anchorObserved: "§8.8.1 \"Weak versus Strong\", ¶3 (the paragraph after the strong-validator definition in ¶2);
earlier in §8.8.3 \"ETag\" ¶1: \"An entity tag is an opaque validator\" (single-line text view line 1)"
```

## 3. Drift — PASS (no content or version change)

One plain public GET of the recorded row URL (2026-10-21 16:29:40 GMT; body piped to a hasher, never saved):

```
HTTP/2 200
date: Wed, 21 Oct 2026 16:29:40 GMT
content-type: text/html
etag: W/"0d9f5fb8eb38d3c08b055f9b0671d68b"
link: <https://www.rfc-editor.org/info/rfc9110/>; rel="canonical"
```

- Live body sha256 = `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5`, **byte-identical** to the
  retained bytes, to `fetched/manifest.json` (row S010, index 1) and to `population.json`.
- Live `etag` = `W/"0d9f5fb8eb38d3c08b055f9b0671d68b"` = the etag recorded in the manifest. **No drift at all.**
- The row's date anchor holds: raw 1237–1239 `<dt class="label-published">Published:</dt> … <time
  datetime="2022-06" class="published">June 2022</time>`; 1235–1236 `Category: Standards Track`; 1232–1234
  `Updates: 3864`.
- No obsoleting/updated-by status line in the page: the only `Obsoleted by` hits are the §1.4 heading
  (`"Specifications Obsoleted by This Document"`, raw 124576 / TOC 32837); `Updated by` does not occur in the page.
  The only `Errata ID` tokens in the document belong to RFC 2978 references; `eid9110` does not occur.
- Cross-format corroboration (the RFC's canonical text, also a corpus URL — `corpus/SOURCES.md:36`, `:41`): live
  `rfc9110.txt` sha256 = `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` = the retained
  `S028-1`/`S033-1` bytes = the digest recorded in the row (`plain text sha256 21c1cdce…7232a`).
- The receipt's `reason` claim *"RFC 9110 is a published immutable spec"* is **slightly overstated** as a general
  property: the rfc-editor HTML is a rendering that can be re-emitted, and RFCs can carry errata. It happens to
  hold today (byte-identical live fetch, identical ETag), and the row's two clauses are unaffected either way —
  flagged as a caveat, not a defect.

**No defect.**

## 4. Locator fidelity in this row's evidence trail — **one stale artifact (the actionable item)**

The receipt contains **no** sha256 and **no** byte-size claim, and its only locator ("single-line text view
line 1") is true of the committed view. But the row's own report does assert one, and it is stale:

`.ufo/waves/round-26/w1/RowS010.md:4`

```
… body sha256 `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5` (1,187,554 B),
text view `fetched/text/S010-1.txt` sha256 `c345bef6c9e101e8ee6c0971d8ff0cf002d5cfc26602249db139c8cd0fa9bc13`
(450,208 B, complete through Authors' Addresses).
```

Committed artifact at `e28312b` (verified via `git cat-file`):

```
fetched/text/S010-1.txt  →  450,533 B  sha256 675f66255175fcefa118d5fd96762bbaa41c269149282d6ac08e1e40d3f4a492
```

The asserted digest `c345bef6…` matches **no committed artifact** in the wave. It is exactly the output of the
**superseded pre-amendment normalizer** `before/source_text.py`:

```
before/source_text.py  output : 450,208 B  c345bef6c9e101e8ee6c0971d8ff0cf002d5cfc26602249db139c8cd0fa9bc13   ← the asserted (stale) value
committed source_text.py output: 450,533 B  675f66255175fcefa118d5fd96762bbaa41c269149282d6ac08e1e40d3f4a492
```

Cause (the `contract-amendment.json` change, `diff -u before/source_text.py source_text.py`):

```diff
-    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)\]])', r'\1', text))   # old: also strips space before ']'
+    return re.sub(r'(\()\s+', r'\1', re.sub(r'\s+([,.;:)])', r'\1', text))     # new: ']' spacing rule removed
```

and the single-entity-decode change (`html.unescape` removed, `HTMLParser(convert_charrefs=True)` now decodes
once). On the S010 body this flips 325 sites: old view has **0** `X ]` and **445** `X]`; new view has **325** `X ]`
and **120** `X]`; 448,125 → 448,450 chars (+325). The committed view is the *new* one, so `w1/RowS010.md:4` reports
a digest and size that were superseded in the same commit that produced the candidate. The "complete through
Authors' Addresses" part of that sentence remains true (new view still ends
`…julian.reschke@greenbytes.de URI: https://greenbytes.de/tech/webdav/`).

Wave-level note (not a second S010 defect): three w1 row reports assert a digest with no committed artifact —
`RowS010.md` (`c345bef6…`, this one), `RowS033.md` (`93a20ab9…` — also a pre-amendment `before/source_text.py`
output, reproduces exactly) and `RowS016.md` (`77b2ab6…`, a different artifact entirely — S016 is the
`versions.json` JSON body; that digest is not the raw, the view, the view-minus-LF, or the pre-amendment view, so
it is unexplained and worth a second look by the S016 seat). The contract amendment's own claim, *"18 text views
regenerated and all 32 receipt quotes re-found"*, is true for the **views** (I reproduced the regeneration set
exactly: S006, S007, S010, S011, S012, S017, S020, S023, S024, S025, S026, S027, S028, S029, S030, S031, S033,
S034 = 18 rows) and for the **quotes** (all 32 re-found, counter exit 0) — but the w1 row-report digests were not
carried forward with them.

**Minimal correction (append/edit of one line in a w1 artifact; no receipt, corpus, or SOURCES change):**

```
w1/RowS010.md:4 — replace
  text view `fetched/text/S010-1.txt` sha256 `c345bef6c9e101e8ee6c0971d8ff0cf002d5cfc26602249db139c8cd0fa9bc13` (450,208 B, complete through Authors' Addresses).
with
  text view `fetched/text/S010-1.txt` sha256 `675f66255175fcefa118d5fd96762bbaa41c269149282d6ac08e1e40d3f4a492` (450,533 B = 448,450 chars + trailing LF, complete through Authors' Addresses).
```

The receipt itself needs **no** change for this. (The §2 wording nit is optional and prose-only.)

## 5. Counter consistency and corpus coherence — PASS

- Counter at the candidate: `python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b1…` →
  `{"decided":32,"expected":32,"findings":[],"hold":32,"stale":0,"unverifiable":0,"statements":276,
  "statementsStale":8,"statementCorrections":8,"populationSha256":"16330e1e…"}`, **exit 0**. No finding is
  attributable to S010.
- Counter at the base: same command with `97404de4…` → `{"decided":0,…,"findings":[{"id":"receipts_absent",…}]}`,
  **exit 1** — the base has no round-26 receipts, so the "0/32 before" half of the claim holds.
- `python3 -B .ufo/waves/round-26/text_selftest.py` → `passed: true, failed: []` (73 cases) — the committed views
  equal `text_of(gunzip(raw))` + one trailing LF for their effective fetch, so the committed `S010-1.txt` is the
  *current* helper's output and the stale digest in §4 is the anomaly, not the view.
- Receipt file at the candidate is byte-identical to the worktree file (`git diff e28312b1 -- …/rechecks/S010.json`
  → empty); the embedded JSON block in `w1/RowS010.md` parses to exactly the same object as the receipt file.
- Receipt schema: keys `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}` — exactly
  `RECEIPT_KEYS`; `verdict: HOLD` ⇒ `correction: null` ✓; `fetchIndex: 1` is the only fetch in `population.json`
  for S010, and its `sha256`/`file` match the manifest.
- Corpus coherence for the row: `corpus/knowledge/ghp-etag-anatomy.md` carries **2** `[r26-recheck S010 STALE]`
  markers (lines 62 and 64) against `statements.json` pair S010 `stale: 2` ✓, and the base 3,304 bytes are an exact
  prefix of the candidate 4,905 bytes (append-only preserved). The C2 correction's quoted clause is verbatim in
  the committed view: `…might be a weak validator if it is possible for the representation to be modified twice
  during a single second and retrieved between those modifications` (raw 6471; `grep -o` on the committed view → 1).
- `corpus/lessons/round-20.md:212` cites S010 with both strings still verbatim in the re-fetched bytes:
  `"An entity tag is an opaque validator"` (1×) and `"A strong validator might change for reasons other than a
  change to the representation data"` (1×) — so that lesson row leaves no stale claim behind. (It is not listed in
  S010's `usedBy` cell; that is the wave-wide convention for `round-20.md` — 18 rows cite it the same way — not an
  S010 defect.)

## Residual risk / verification gaps

1. **Residual risk (accepted).** "RFC 9110 is a published immutable spec" is true of the *document* but not of the
   *rendering* or of errata. The live GET today is byte-identical with the same weak ETag, and the rfc-editor
   `.html` carries no "Updated by" line, so a later RFC that updates RFC 9110 would not be visible in these bytes.
   I did not fetch `rfc-editor.org/info/rfc9110` or the errata page (lane bounds allow one plain GET of a recorded
   documentation URL; I used it on the row URL plus the RFC text twin, both corpus URLs). Status after the
   2026-10-21 fetch is therefore asserted by the w1 pair report, not by me.
2. **Gap.** No 2026-10-19 (row `opened`) bytes for S010 exist in the lane, so byte identity with the original
   opening read is unproven; the row's `verified-at: 2026-10-19` in `ghp-etag-anatomy.md:2` remains the historical
   date, superseded for S010 by the 2026-10-21 re-fetch (the w1 pair flagged it; the corpus keeps it as history).
3. **Gap.** `w1/RowS016.md`'s orphan digest `77b2ab6…` is not reproducible from any artifact I could construct
   (raw, view, view-minus-LF, pre-amendment view). Out of my scope (S016), but it is the one unexplained member of
   the §4 defect class and should not be waved through on the strength of the other two.
4. **Not checked (out of scope).** The other 31 receipts, the S009 pair, and the 22 rejected statement seats; the
   counter was run read-only twice (base and candidate) and no corpus, script, fleet, sibling-lane or Git state was
   mutated.

## Reproduction commands (read-only; the live body was never saved)

```bash
# retained bytes, anchor lines
gzip -dc .ufo/waves/round-26/fetched/S010-1.raw.gz | sed -n '6398,6422p;6612,6629p;1230,1240p'
gzip -dc .ufo/waves/round-26/fetched/S010-1.raw.gz | grep -c 'A strong validator might change'      # 1
gzip -dc .ufo/waves/round-26/fetched/S010-1.raw.gz | grep -c 'An entity tag is an opaque validator'  # 1

# committed view vs the digest asserted in the row report
git cat-file -p e28312b1:.ufo/waves/round-26/fetched/text/S010-1.txt | wc -c          # 450533
git cat-file -p e28312b1:.ufo/waves/round-26/fetched/text/S010-1.txt | sha256sum      # 675f6625…
# reproduce the asserted (stale) digest from the superseded helper
python3 - <<'PY'
import gzip,hashlib,importlib.util
s=importlib.util.spec_from_file_location('old','.ufo/waves/round-26/before/source_text.py')
o=importlib.util.module_from_spec(s); s.loader.exec_module(o)
raw=gzip.open('.ufo/waves/round-26/fetched/S010-1.raw.gz','rb').read()
b=(o.text_of(raw,'text/html')+'\n').encode()
print(len(b), hashlib.sha256(b).hexdigest())   # 450208 c345bef6…  ← the stale value
PY

# live GET of the row URL, bytes hashed in the pipe only
curl -sS -D- "https://www.rfc-editor.org/rfc/rfc9110.html" | tee >(sha256sum >&2) >/dev/null

# counter, read-only, base and candidate
python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de4ff73d6c8a4f87385cf5fdf36dca7f006  # exit 1
python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e  # exit 0
```

## Tooling

No tools installed, upgraded or removed — `python3` 3.14.8 (stdlib only: `gzip`, `hashlib`, `json`, `re`,
`importlib.util`, `os`, `difflib`, `subprocess`) and `curl` 8.23.0 were already present. Per the operator
directive, no package transaction was performed (host-wide pacman pause respected; no host service or system
change). Three plain public GETs of already-recorded corpus documentation URLs: the row URL
`https://www.rfc-editor.org/rfc/rfc9110.html` (twice — headers, then a piped hash) and its text twin
`https://www.rfc-editor.org/rfc/rfc9110.txt` (also in `corpus/SOURCES.md:36,41`). No credentials, no browsing, no
site probing, no file written outside this report, no `/tmp` use, no corpus/script/fleet/sibling-lane/Git mutation.

```json
{"target":".ufo/waves/round-26/rechecks/S010.json","verdict":"AGREE","severity":"low"}
```
