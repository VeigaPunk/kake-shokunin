# FalsifyS027 — author-side falsification of receipt S027 (verdict HOLD)

Target receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S027.json`
Candidate: `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`)
Row: `corpus/SOURCES.md:35` — S027 · Python: urllib.parse · https://docs.python.org/3/library/urllib.parse.html
Axis: freshness · Milestone: r26-recheck-falsify

**Verdict: DISAGREE (severity: low).** The HOLD verdict itself survives every attack I ran and must **not** be flipped; the disagreement is confined to the receipt's `anchorObserved` locator string, which (a) states three numbers that describe **no committed artifact** — they reproduce the superseded pre-amendment normalizer output — and (b) misplaces the warning structurally ("immediately after the urlsplit() signature", when it is 5,027 characters later, at the end of that entry). Minimal correction below — verdict and `correction` stay `HOLD`/`null`.

---

## Axes named

1. **Anchor identity** — does the quoted sentence and the cited section exist in the retained bytes (`fetched/S027-1.raw.gz`) and in the committed text view at `e28312b`?
2. **Grounding** — does the quote ground *this* row's `teaches` (not page chrome, not a neighbouring clause)?
3. **Locator fidelity** — do the offsets/character counts in `anchorObserved` describe the artifact they name at the reviewed revision?
4. **Drift since fetch** — did the live page change after the 2026-10-21 fetch in a way the receipt missed?
5. **Cross-lane consistency** — is the same locator pattern present in sibling receipts (wave-level signal)?

---

## 1. Anchor identity — PASS

Retained bytes: `fetched/S027-1.raw.gz` → 119,730 bytes, sha256 `a27468b3a18380e3f0b86b9326217bfee865d2c81523d0849927dd2b8542d9f1` — identical to `fetched/manifest.json` (row S027, index 1) and to `population.json` (`"sha256": "a27468b3…42d9f1"`, `"file": "fetched/S027-1.raw.gz"`).

Raw HTML carries the quoted sentence, split by markup exactly as Sphinx emits it (double space after the period, the link text wrapped across a newline):

```
raw 34168: <div class="admonition warning">\n<p class="admonition-title">Warning</p>
raw 34298: <p><code class="xref py py-func docutils literal notranslate"><span class="pre">urlsplit()</span></code>
           does not perform validation.  See <a class="reference internal" href="#url-parsing-security">
           <span class="std std-ref">URL parsing\nsecurity</span></a> for details.</p>
raw 65002: <section id="url-parsing-security">  →  <h2>URL parsing security …
```

The receipt's `quote` is a *normalized* rendering of that sentence; it is **not** a raw-byte substring (raw has `validation.  See` and `URL parsing\nsecurity`). That is the lane's own convention — `measure.py:273-276` normalizes the quote and searches the normalized text, and `source_text.text_of` produces exactly `"urlsplit() does not perform validation. See URL parsing security for details."` at normalized offset 7,274. `quote_in_text` therefore passes, and the quote is verbatim in the canonical view. **Not a defect.**

Normalized view of the security section (text offsets), all verified present:
- 16,660 `The urlsplit() and urlparse() APIs do not perform validation of inputs.`
- 17,295 `code defensively.` / 17,313 `Do some verification within your code before trusting a returned component part.`
- 17,640 `the living WHATWG spec describes what user facing web clients such as a web browser require.`
- 17,765 `These functions incorporate some aspects of both, but cannot be claimed compliant with either.`
- 15,203 `it is generally not secure to use urljoin with an attacker-controlled url.` (raw 59,763)
- title at offset 0: `urllib.parse — Parse URLs into components — Python 3.15.1 documentation`; TOC entry `URL parsing security` at 166; footer `Last updated on Oct 21, 2026 (13:02 UTC).`

The `urljoin` Warning is a *separate* admonition (raw 59,445) from the `urlsplit` one (raw 34,168) — the receipt does not conflate them. **PASS.**

## 2. Grounding — PASS

Row `teaches`: «URL components must be validated by the caller; stdlib parsing is not exact browser URL equivalence».
Row `anchor`: «urlsplit warning **and** URL parsing security» — a two-part anchor, and both parts are present and located.

- «validated by the caller» ← `code defensively. Do some verification within your code before trusting a returned component part.` (17,313) — direct.
- «not exact browser URL equivalence» ← `the living WHATWG spec describes what user facing web clients such as a web browser require` (17,640) + `cannot be claimed compliant with either` (17,765, i.e. neither WHATWG nor RFC 3986) — direct, not an inference.
- The `resolution` half of the row's `scope` («URL splitting and resolution are not validation») rests on the `urljoin` Warning, **not** on the security section (which names only `urlsplit()`/`urlparse()`), and the receipt says so explicitly. Correct scoping.

The quote is the page's own `urlsplit()` admonition, not chrome and not a neighbouring clause. **PASS.**

## 3. Locator fidelity — **FAIL (the finding)**

`rechecks/S027.json:6` (`anchorObserved`) states:

> "fetched/text/S027-1.txt is one **30,322-char** line; … 'Warning urlsplit()' admonition at offset **7,261** … body heading 'URL parsing security ¶' at offset **16,630**"

All three numbers are wrong for the file the receipt names, at the reviewed revision:

```
$ git show e28312b:.ufo/waves/round-26/fetched/text/S027-1.txt   →  30,329 chars (30,442 bytes), 1 line
   'Warning urlsplit()'          at  7,266      (receipt says 7,261  → 5 chars early)
   'URL parsing security ¶'      at 16,637      (receipt says 16,630 → 7 chars early)
   committed[7261:7301]  = "='') Warning urlsplit() does not perform vali"
   committed[16630:16680]= 'anges. URL parsing security ¶ The urlsplit() and u'
```

The receipt's numbers are reproducible **only** from the superseded pre-amendment normalizer, `before/source_text.py`:

```
OLD (before/source_text.py) : len=30321  Warning@7261  heading@16630   ← receipt's numbers
NEW (source_text.py)        : len=30328  Warning@7266  heading@16637   ← committed view
```

Root cause, precisely: the contract amendment changed `normalize()` — it dropped `]` from the trailing-punctuation rule (`re.sub(r'\s+([,.;:)\]])', r'\1', text)` → `re.sub(r'\s+([,.;:)])', r'\1', text)`). That **keeps 7 spaces** that the old view collapsed, at normalized positions 5,583 / 5,640 / 5,728 / 5,785 / 5,919 / 16,089 / 16,094 (the `[ 1]` / `[ 3]` footnote markers). Five of them precede the Warning ⇒ +5; all seven precede the section heading ⇒ +7; total length 30,321 → 30,328 (+1 trailing LF ⇒ 30,329). Diff of the two views:

```
('insert', 5583, 5583, 5583, 5584) '' -> ' '      … 7 such inserts
```

`contract-amendment.json` required "18 text views regenerated and all 32 receipt quotes re-found" — the **quotes** were re-found, the **locators** were not. The stale numbers were carried over from the w1 drafts, which were computed against the old view (`w1/PairS027StaticCanonicalPrefl.md`: "Text view `fetched/text/S027-1.txt`: 30322 characters", "URL parsing security" pos 16630; `w1/RowS027.md` carries the identical JSON blob).

Timing shows this is not a benign "written before the file existed" race:

```
$ stat -c '%n %y' .ufo/waves/round-26/{source_text.py,before/source_text.py,fetched/text/S027-1.txt,rechecks/S027.json}
source_text.py            2026-10-21 13:02:13.677
before/source_text.py     2026-10-21 13:02:13.676
fetched/text/S027-1.txt   2026-10-21 13:02:14.133   ← regenerated view already on disk
rechecks/S027.json        2026-10-21 13:04:31.603   ← receipt written 2m17s later, still with old offsets
```

### 3b. Structural locator — also inaccurate ("immediately after the urlsplit() signature")

The same `anchorObserved` string asserts the warning sits **"(immediately after the urlsplit() signature)"**. It does not. The `urlsplit()` signature is at text offset **2,239** and the warning at **7,266** — **5,027 characters apart**, with the `SplitResult` description, the `netloc` attribute table and two doctest examples in between. The warning is the **last** admonition of the `urlsplit()` entry, sitting immediately *before* `Changed in version 3.2: Added IPv6 URL parsing capabilities`:

```
text[7266-120:7266]  = "cheme = 'http') SplitResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', query='', fragment='') "
text[7266:7266+140]  = "Warning urlsplit() does not perform validation. See URL parsing security for details. Changed in version 3.2: Added IPv6 URL parsing capabil"
```

Raw structure confirms the same: `<dt class="sig sig-object py" id="urllib.parse.urlsplit">` at raw 16,677, the warning `<div class="admonition warning">` at raw 34,168 (17,491 bytes later, still inside the same `<dd>` — zero `</dd>`/`</dl>` between them), and the next `<dt>` (`urllib.parse.parse_qs`) at raw 36,518. The warning is therefore at the **end** of the `urlsplit()` entry, not at its head. This defect is independent of the numeric drift in §3 (it is wrong under the old view too) and it is the part an auditor is most likely to act on.

Both locator defects are consequences of the receipt inheriting the w1 draft's prose without re-measuring against the regenerated view.

Also: **no committed artifact ever had 30,322 chars.** Both wave commits carry the same 30,442-byte text file:

```
$ git show cada1a4:.ufo/waves/round-26/fetched/text/S027-1.txt | wc -c   →  30442
$ git show e28312b:.ufo/waves/round-26/fetched/text/S027-1.txt | wc -c   →  30442
```

Impact: an auditor who follows the receipt's offsets into the committed file lands 5 and 7 characters *before* the named anchors — the anchor phrases are still recoverable in the neighbourhood, so no wrong section is cited and the HOLD conclusion is untouched. That is why severity is **low**, not medium. But as pushed, the receipt misstates where its anchors are, and the w1 pair report carries the same stale locators ("pos 16653", "pos 16803", "pos 17306", "pos 17758", "pos 15198", "pos 14303", "pos 4054", "pos 2239", "pos 30238" — all pre-amendment).

## 4. Drift since fetch — PASS (no change)

One plain GET of the row URL (documentation GET, permitted) — content byte-identical to the retained bytes, and headers identical to the manifest:

```
status 200 · content-length 119730 · sha256 a27468b3a18380e3f0b86b9326217bfee865d2c81523d0849927dd2b8542d9f1
last-modified: Wed, 21 Oct 2026 13:04:29 GMT   etag: "6ad8b85d-1d3b2"   content-type: text/html
```

(The GET was issued twice — once via `urllib` to compare normalized text, once via `http.client` to read raw headers; both reads returned the identical 119,730 bytes. No content was saved to disk.)

The version claim in the receipt's `reason` is exact: the page self-labels `Python 3.15.1 documentation` (family 3.15, as the anchor cell records) and its footer reads `Last updated on Oct 21, 2026 (13:02 UTC).`; `Last-Modified 2026-10-21T13:04:29Z` in the receipt matches the manifest header. The corpus-level version-label change is already carried at `corpus/knowledge/static-canonical-preflight.md:188` (`[r26-recheck S026 STALE] … The page now labels itself Python 3.15.1 documentation (S026 and S027 alike)`), and `statements.json` carries the S027 pair with `stale: 0` and the disposition "version label/date only; relied-on warnings unchanged (note in S026 block)" — consistent with a row-level HOLD whose anchor cell is append-only and whose "Python 3.15" label is a historical access record (ledger rule: "Historical dates and base-scoped pointers are not stale"). The receipt's `reason` is also careful to attribute the resolution half to `urljoin`'s own Warning. **PASS.**

## 5. Cross-lane consistency — wave-level signal (not my scope to fix)

The same stale-locator pattern is present in sibling receipts, all recomputed against `before/source_text.py` and all shifted in the committed view:

| receipt | stated offset | what is actually at that offset in the committed view | shift |
|---|---|---|---|
| S024 | 8,390 | `erface. 4.2.3 The base element ✔ MDN Element/base Suppo` (old view: `4.2.3 The base element ✔ …`) | +8 |
| S025 | 62,596 | `content attribute is a boolean attribute. The template ` (old view: `The template contents of a template element are not chi`) | +30 |
| S027 | 7,261 / 16,630 | see §3 | +5 / +7 |
| S034 | 8,863 | ` The names within an object SHOULD be unique. object = ` (old view: `The names within an object SHOULD be unique. object = b`) | +1 |

`measure.py` does not validate offsets (`measure.py:370` only requires a non-empty `anchorObserved`), which is why the counter reports 32/32 exit 0 while the locators are wrong. The S025 case is the most misleading (the stated offset no longer sits on the quoted sentence at all); S027 is the least divergent. Sibling lanes FalsifyS024 / FalsifyS025 / FalsifyS034 are the right owners of those; I flag the shared root cause so it is fixed once, not four times.

---

## Minimal correction (S027 only — verdict and `correction` unchanged)

In `rechecks/S027.json`, `anchorObserved` only, replace:

- `one 30,322-char line` → `one 30,328-char line (30,329 chars including the trailing LF)`
- `at offset 7,261` → `at offset 7,266`
- `at offset 16,630` → `at offset 16,637`
- `(immediately after the urlsplit() signature)` → `(last admonition of the urlsplit() entry, after the SplitResult description, the netloc attribute table and the two doctest examples, immediately before "Changed in version 3.2: Added IPv6 URL parsing capabilities")`

No change to `verdict` (HOLD), `quote`, `reason` or `correction` (`null`). The offsets above are reproducible with the committed helper:

```
$ python3 -B -c "
import gzip,importlib.util,pathlib
s=importlib.util.spec_from_file_location('st','.ufo/waves/round-26/source_text.py');st=importlib.util.module_from_spec(s);s.loader.exec_module(st)
t=st.text_of(gzip.decompress(pathlib.Path('.ufo/waves/round-26/fetched/S027-1.raw.gz').read_bytes()),'text/html')
print(len(t), t.find('Warning urlsplit()'), t.find('URL parsing security ¶'))"
30328 7266 16637
```

Optionally, in the same edit, tighten `reason`'s citation sentence: it says `corpus/lessons/round-22.md L50 quotes the identical warning sentence`, but L50 quotes only the first sentence (`urlsplit() does not perform validation.`) of the two-sentence warning the receipt's `quote` field carries. "Identical" is loose; the lesson's fragment is a prefix of the receipt's quote.

## Residual risk / verification gaps

- **Residual risk (accepted):** the anchor is a living `/3/` URL, unpinned; the 3.15→3.15.1 label move is recorded only inside the S026-tagged correction block (`static-canonical-preflight.md:188`), so a reader auditing S027 alone sees no S027-tagged correction and the SOURCES row cell still reads "Python 3.15 documentation accessed 2026-10-20". That is consistent with the append-only rule and with `statements.json` (`stale: 0`), so I do not call it a defect — but it is the weakest link in the S027 chain.
- **Gap:** no 2026-10-20 bytes for S027 exist in the lane, so the 3.15 → 3.15.1 delta cannot be diffed; my verification of the version claim rests on the page's own title/footer plus the S026 receipt's independent observation of 3.15.0 earlier the same day.
- **Gap:** the receipt cites `corpus/knowledge/static-canonical-preflight.md (~L74-77)`; the cited sentence is actually at L74-75. Immaterial to the verdict.
- **Consistency note for the coordinator:** sibling leaf `FalsifyS024.md` reached `AGREE / low` on the same stale-offset class (S024's offsets are stale by +8). My S027 finding is graded DISAGREE only because S027's stale numbers are *exactly* reproducible from the retained `before/source_text.py` and because of the additional structural misplacement in §3b — the underlying defect class is identical. If the coordinator prefers one uniform label for the class, treat S027 as `AGREE` with the same low-severity locator correction; the substantive HOLD conclusion is unaffected either way, and the minimal correction is the same four-field edit.
- **Not checked (out of scope):** the other 31 rows, the knowledge-entry statement ledger beyond S027's pair, and the counter's own exit code — which I did not re-run, since my assignment is the S027 receipt, not the counter.

## Tooling

No tools installed or upgraded (Python 3 stdlib only: `urllib`, `http.client`, `gzip`, `importlib.util`, `json`, `re`, `subprocess`; `git` for revision reads). Two plain public GETs of the documented URL `https://docs.python.org/3/library/urllib.parse.html` (documentation GET, within bounds); no credentials, no browsing, no site probing, no file written outside this report.

```json
{"target":".ufo/waves/round-26/rechecks/S027.json (S027 receipt, verdict HOLD)","verdict":"DISAGREE","severity":"low"}
```
