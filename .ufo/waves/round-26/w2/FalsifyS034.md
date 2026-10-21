# FalsifyS034 — round-26 C1 freshness falsification of receipt S034 (HOLD)

Seat: `KakeR26-2.FalsifyS034` (leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Milestone `r26-recheck-falsify`, judged axis **freshness**.
Target artifact: `.ufo/waves/round-26/rechecks/S034.json` (verdict HOLD), row line `corpus/SOURCES.md:42`.
Pushed candidate under test: `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`).

**Verdict: DISAGREE — severity low.** The HOLD verdict itself is **confirmed correct** and is not overturned: the quote grounds this row's teaches, the live bytes are byte-identical to the retained bytes and to the digest recorded at row open, and all four cited sections are present with the relied-on sentences verbatim. What I can show is wrong is narrower and is about the receipt's *evidence pointers* and its *supersession argument*: the anchor offset it cites does not resolve against the committed artifact it names, and the supersession evidence it offers is tautological. Both are correctable without changing the verdict.

---

## 1. What the receipt claims, and what I re-verified independently

`rechecks/S034.json:3-7` (blob `d1a4bae217c35c960f21eb5319788120ae8cd320` at the candidate):

- `"verdict": "HOLD"`, `"fetchIndex": 1`
- `"quote": "The names within an object SHOULD be unique."`
- `"anchorObserved": "RFC 8259 Section 4 (Objects), raw line 322; fetched/text/S034-1.txt is whitespace-collapsed onto line 1 (offset 8863), where the sentence still sits under the '4. Objects' heading"`
- `"reason"`: live GET 200, body sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`, byte-identical to the digest recorded at open (`corpus/lessons/round-24.md:33`); "Header still reads December 2017 and 'Obsoletes: 7159' with no 'Obsoleted by'"; all four cited sections exist; §4/§6/§3 content quoted; "Duplicate rejection stays local policy because §9 requires parsers to accept all grammar-conforming texts."

Independent re-verification (commands and outputs in §5):

| Receipt claim | Result |
|---|---|
| Quote is in §4 Objects | **CONFIRMED** — raw line 322 of `fetched/S034-1.raw.gz` is exactly `   name.  The names within an object SHOULD be unique.`; quote occurs once in raw and once in the committed text view. |
| Anchor "raw line 322" | **CONFIRMED** — `gunzip -c S034-1.raw.gz \| grep -n` gives `322:   name.  The names within an object SHOULD be unique.` |
| Live GET today = 200, sha256 `61a5378f…5cd2d7`, byte-identical to retained bytes and to the open-time digest | **CONFIRMED** — live GET returned `http=200 size=28360`, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`; `gunzip -c fetched/S034-1.raw.gz \| sha256sum` = same digest; `corpus/lessons/round-24.md:33` records the same digest. |
| Four cited sections exist (3 Values, 4 Objects, 6 Numbers, 9 Parsers) | **CONFIRMED** — TOC raw lines 126–135; section headings at raw lines 296, 316, 362, 541. |
| §4 "SHOULD uniqueness" + "unpredictable" | **CONFIRMED** — raw 322 and 333–336. |
| §6 "as Infinity and NaN) are not permitted" | **CONFIRMED** — present verbatim once in raw and in the committed text view. |
| §3 false/null/true as literal names distinct from number | **CONFIRMED** — raw 296–310 (`false`/`null`/`true` literal names; `value = false / null / true / object / array / number / string`). |
| §9 "A JSON parser MUST accept all texts that conform to the JSON grammar." | **CONFIRMED** — raw 543–544, verbatim. |
| Quote is row-specific (not boilerplate shared with another population row) | **CONFIRMED** — the string occurs in no other `fetched/text/*.txt` and in no other retained raw `.gz`. |
| Receipt schema | **CONFIRMED** — keys exactly `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}`; anchorObserved non-empty; quote 8 words / ≥6 alphanumeric tokens. |

So the **freshness outcome (HOLD) is correct**: the cited document is unchanged byte-for-byte at the anchor, the anchor sections still exist, and every sentence the row's teaches depend on is still present verbatim in the retained bytes. Nothing here supports a STALE verdict.

---

## 2. Finding A — the anchor offset in the receipt does not resolve against the committed candidate (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S034.json:6` — "fetched/text/S034-1.txt is whitespace-collapsed onto line 1 (offset 8863), where the sentence still sits under the '4. Objects' heading".

**Evidence.** At the pushed candidate, the committed text view is:

```
$ git show e28312b:.ufo/waves/round-26/fetched/text/S034-1.txt | sha256sum
8b3b71a46be7000929bee04395a3c8574c2b89b55b6dedec34c64c306582e076   # 23,053 bytes
$ python3 -c "t=open('...S034-1.txt').read(); print(t.find('The names within an object SHOULD be unique.'))"
8864
$ git show e28312b:...S034-1.txt | python3 -c "import sys; b=sys.stdin.buffer.read(); print(repr(b[8863:8870]))"
b' The na'          # offset 8863 is a SPACE; the quote starts at 8864
```

Offset **8863** is the offset in the *superseded* pre-amendment text view. The amendment `.ufo/waves/round-26/contract-amendment.json:15` records the change: "source_text.py: single entity decode (HTMLParser convert_charrefs) and no `]` spacing rule; before copy retained at before/source_text.py; **18 text views regenerated** and all 32 receipt quotes re-found". The RFC 8259 ABNF contains eight `]` tokens (`ws %x5D ws;`), so removing `]` from the spacing class lengthened this view by 8 characters. Reproducing the pre-amendment extractor from the committed `before/` blob yields exactly the offset the receipt cites:

```
$ python3 - <<'EOF'   # source_text.py taken from the committed before/ blob
import gzip, importlib.util
src = subprocess.run(['git','show','e28312b:.../before/source_text.py'],capture_output=True).stdout
mod = types.ModuleType('b'); exec(compile(src,'b','exec'), mod.__dict__)
raw = gzip.decompress(open('fetched/S034-1.raw.gz','rb').read())
tb = mod.text_of(raw,'text/plain;charset=utf-8')
print(len(tb), tb.find("The names within an object SHOULD be unique."))
EOF
23044 8863
```

and the same blob produces the 23,045-byte view whose digest the sibling report still quotes:

```
before-view + "\n" -> 23045 bytes, sha256 80a181c35a15c4108d2d2e70aaa91e7391e4f84d1b92924cd20e012841dcbc24
committed view      -> 23053 bytes, sha256 8b3b71a46be7000929bee04395a3c8574c2b89b55b6dedec34c64c306582e076
```

**Timeline shows the receipt was written after the regeneration and was not re-derived.** File mtimes in the lane:

```
2026-10-21 12:37:32  w1/PairS034StaticCanonicalPrefl.md     (states 23,045 B / 80a181c3 — correct for the then-current view)
2026-10-21 13:02:13  before/source_text.py, source_text.py  (amendment)
2026-10-21 13:02:14  fetched/text/S034-1.txt               (regenerated view)
2026-10-21 13:04:31  rechecks/S034.json                    (still cites offset 8863)
```

So the receipt (13:04) cites a coordinate that became stale two minutes earlier (13:02) and was carried forward from the 12:37 pair seat.

**Scope.** This is systemic to the 18 regenerated views, not S034-specific. Auditing every numeric offset cited in all 32 receipts' `anchorObserved` against the committed views yields four receipts whose offsets resolve in the *before* view only (S024 `10160`, S025 `62596`, S027 `7261`, S034 `8863`); the S034 pair report's own eight cited offsets (@8232, @8242, @8434, @9176, @10717, @11127, @16229, @16355) are likewise before-view offsets (deltas −1 … −7 against the committed view). S034 is additionally the only pair report that states a **digest** for the committed text view that contradicts the committed blob: `w1/PairS034StaticCanonicalPrefl.md:11` says "Text view `fetched/text/S034-1.txt`: 23,045 B, sha256 `80a181c3…`" while the committed file is 23,053 B / `8b3b71a4…`.

**Why this is not caught by the counter.** `measure.py` validates a receipt's quote as a *word-bounded normalized substring* of the text view (`measure.py:273-276`, used at `:391-392`); it never checks a numeric offset and never checks `anchorObserved` for accuracy beyond being a non-empty string (`measure.py:365-370`). The candidate's exit 0 (`.ufo/waves/round-26/verification/measure-candidate.json`: `decided 32, findings [], exit 0`) therefore certifies quote presence, not the anchor locator. The stale offsets pass silently.

**Minimal correction (row receipt only).** In `rechecks/S034.json`, change the `anchorObserved` clause "(offset 8863)" to "(offset 8864)" and, to keep the locator self-checking, append the committed view digest: "fetched/text/S034-1.txt is whitespace-collapsed onto line 1 (offset 8864; view sha256 8b3b71a4…, 23,053 B)". The raw-byte half of the anchor ("raw line 322") is correct and needs no change.

---

## 3. Finding B — the receipt's supersession evidence is tautological (severity: low, verdict-affecting: no)

**Claim under test:** `rechecks/S034.json:7` — "Header still reads December 2017 and 'Obsoletes: 7159' with no 'Obsoleted by'." Read as a freshness argument, this asserts the absence of a supersession marker in the fetched bytes.

**Evidence that the marker cannot appear.** A published RFC `.txt` is frozen at publication; obsoletion and update relationships live on the RFC Editor info page and the datatracker, never in the RFC body. The lane's own retained corpus proves this without any external inference: RFC 3339 **is** updated by RFC 9557 — the lane records that itself at `corpus/knowledge/static-canonical-preflight.md:194` ("the RFC Editor info page reports RFC 3339 (S032) as updated by RFC 9557") and at `corpus/SOURCES.md:79` — yet the retained RFC 3339 bytes contain none of the markers the receipt greps for:

```
$ python3 - <<'EOF'   # fetched/S032-1.raw.gz
raw = gzip.decompress(open('fetched/S032-1.raw.gz','rb').read()).decode()
for p in ['Obsoleted by','Updated by','Updates:','9557']: print(p, raw.count(p))
EOF
Obsoleted by -> 0
Updated by -> 0
Updates: -> 0
9557 -> 0
```

So a receipt for RFC 3339 using the identical check would equally report "no 'Obsoleted by'" while the document is, in fact, updated. The S034 check therefore cannot distinguish "current" from "superseded"; it is satisfiable by construction.

**Also uncovered by the byte-equality argument.** "Byte-identical … so there is no drift to test" holds only for the frozen `.txt`. RFC 8259 carries verified errata that live *outside* the `.txt` — the sibling seat enumerates verified errata 5210 (boilerplate), 5318 (§7 ABNF), 7383 (§3 ABNF hex case), 7600 (§6 leading-zero sentence), 7603 (§1) at `w1/PairS034StaticCanonicalPrefl.md` ("Freshness of the cited version and anchors"), and notes the retained text still predates them ("it still reads 'Leading zeros are not allowed.'" — raw line 368 of the retained gz reads `fraction part and/or an exponent part.  Leading zeros are not`). The receipt mentions no errata channel at all, so its "no drift to test" claim is true of the bytes and silent about the document's current version.

**Effect on the verdict: none.** I checked whether any known RFC 8259 erratum could touch what the row teaches. The taught clauses are (i) object names SHOULD be unique (§4), (ii) NaN/Infinity are not JSON numbers (§6's "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."), (iii) explicit duplicate rejection is local receipt-integrity policy (§4 unpredictability + §9 MUST-accept). Verified erratum 7600 changes the §6 *leading-zero* sentence and 7383 the §3 *ABNF hex case*; neither touches (i), (ii) or (iii). Erratum 8622, which proposed replacing the very §4 SHOULD sentence, was rejected (per the pair seat's errata reading). So HOLD remains the right verdict — but on the *documented* errata and datatracker checks, not on the receipt's own header grep.

**Minimal correction (row receipt only).** Replace the header-grep clause with a check that can actually fail, e.g.: "RFC 8259 remains the current JSON RFC — RFC Editor info page lists it as Internet Standard / STD 90 with no obsoleting or updating action, and datatracker history shows no supersession; verified errata 5210, 5318, 7383, 7600, 7603 touch §1, §3 ABNF hex case, §6 leading-zero sentence and §7 ABNF, none of them the sentences this row's teaches rely on; rejected erratum 8622 (proposed replacement of the §4 SHOULD sentence) does not change it." If the receipt is not to carry the errata inventory, the supersession clause should at least cite the info-page/datatracker observation (which the pair seat already made) instead of a body grep that cannot fail.

---

## 4. Non-defects I checked and cleared (so the integrator does not re-open them)

- **Quote grounds THIS row's teaches, not page chrome or a neighbouring clause.** "The names within an object SHOULD be unique." is the normative sentence of §4 Objects (raw line 322, inside the §4 body starting at raw 316), not the TOC entry (raw 126–135 lists only section titles) and not a page footer (the footers "Bray / Standards Track / [Page N]" are the only chrome in the view and the quote does not touch them). The other two teach clauses are grounded elsewhere inside the same cited anchor set: §6 for "NaN and Infinity are not JSON numbers", §4 unpredictability + §9 MUST-accept for "explicit duplicate rejection is local receipt-integrity policy" — all verified verbatim above. The one-quote-per-receipt shape is what `measure.py` requires; the reason field legitimately carries the rest.
- **Quote uniqueness across the population.** `grep` over all 34 committed text views and over every retained raw `.gz`: the quote occurs only in S034. `measure.py:407-422` (quote_not_row_specific) is satisfied.
- **Verdict HOLD vs STALE.** No drift in the source: live GET today is byte-identical to the retained gz and to the open-time digest; the sections exist; the sentences are verbatim. STALE is not supportable for this row.
- **No change to `corpus/SOURCES.md:42`** in the candidate diff — the round-26 paragraph at `corpus/SOURCES.md:79` is the only SOURCES.md change (`git diff 97404de e28312b -- corpus/SOURCES.md` shows one added paragraph), so the "no row cell changed" claim in that paragraph holds for S034.
- **Duplicate-rejection inference.** The row's teach ("explicit duplicate rejection is local receipt-integrity policy") is consistent with §4 (SHOULD, not MUST) and §9 (MUST accept all grammar-conforming texts). Strictly, §9's MUST-accept also means a duplicate-name text — which conforms to the RFC 8259 grammar — must be accepted by a conforming parser, so the local rejection is a *stricter local deviation*, not merely an unspecified area. The receipt's conclusion is right; its wording ("§9 requires parsers to accept all grammar-conforming texts" ⇒ local policy) understates it. Recorded as wording-only, no correction required.

---

## 5. Commands and outputs (reproduction)

```
$ curl -sS --max-time 60 -o /dev/null -w "http=%{http_code} size=%{size_download}\n" https://www.rfc-editor.org/rfc/rfc8259.txt
http=200 size=28360
$ curl -sS --max-time 60 https://www.rfc-editor.org/rfc/rfc8259.txt | sha256sum
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  -
$ gunzip -c .ufo/waves/round-26/fetched/S034-1.raw.gz | sha256sum
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  -
$ gunzip -c .ufo/waves/round-26/fetched/S034-1.raw.gz | grep -n "SHOULD be unique"
322:   name.  The names within an object SHOULD be unique.
$ gunzip -c .ufo/waves/round-26/fetched/S034-1.raw.gz | grep -n -E "^3\.  Values|^4\.  Objects|^6\.  Numbers|^9\.  Parsers|Obsoletes:"
9:Obsoletes: 7159                                            December 2017
296:3.  Values
316:4.  Objects
362:6.  Numbers
541:9.  Parsers
$ git show e28312b:.ufo/waves/round-26/fetched/text/S034-1.txt | sha256sum
8b3b71a46be7000929bee04395a3c8574c2b89b55b6dedec34c64c306582e076   # 23,053 bytes
$ git show e28312b:.ufo/waves/round-26/fetched/text/S034-1.txt | python3 -c "import sys;b=sys.stdin.buffer.read();print(repr(b[8863:8870]), b.decode().find('The names within an object SHOULD be unique.'))"
b' The na' 8864
$ stat -c '%n %s %y' .ufo/waves/round-26/{before/source_text.py,source_text.py,fetched/text/S034-1.txt,w1/PairS034StaticCanonicalPrefl.md,rechecks/S034.json}
.../before/source_text.py  1301  2026-10-21 13:02:13
.../source_text.py         1301  2026-10-21 13:02:13
.../fetched/text/S034-1.txt 23053 2026-10-21 13:02:14
.../w1/PairS034StaticCanonicalPrefl.md 9861 2026-10-21 12:37:32
.../rechecks/S034.json    1083  2026-10-21 13:04:31
$ grep -n "8863\|23,045 B\|80a181c3" .ufo/waves/round-26/w1/PairS034StaticCanonicalPrefl.md .ufo/waves/round-26/w1/RowS034.md
w1/PairS034StaticCanonicalPrefl.md:11: …23,045 B, sha256 `80a181c35a15…`
w1/PairS034StaticCanonicalPrefl.md:24: …"The names within an object SHOULD be unique." (@8863, 8 w)…
w1/RowS034.md:9: …23,044-char line… (offset 8863)
$ python3 -c "import gzip;raw=gzip.decompress(open('.ufo/waves/round-26/fetched/S032-1.raw.gz','rb').read()).decode();[print(p,raw.count(p)) for p in ['Obsoleted by','Updated by','Updates:','9557']]"
Obsoleted by 0 / Updated by 0 / Updates: 0 / 9557 0
```

---

## 6. Residual risk and verification gaps (not actionable by this seat)

1. **Supersession of RFC 8259 is verified second-hand here.** My own network access was one documentation URL already in `corpus/SOURCES.md` (`https://www.rfc-editor.org/rfc/rfc8259.txt`) — two GET requests to that same URL (one for status/size, one for the digest); nothing was saved, no other host was contacted, no probing of properties. The RFC Editor info page and datatracker history were **not** fetched by me; the "still current / STD 90 / no obsoleting action" statement rests on `w1/PairS034StaticCanonicalPrefl.md` ("Freshness of the cited version and anchors") and on the lane's own `corpus/SOURCES.md:79` note about RFC 9557. That is a documented, in-lane, same-round observation, but it is not my own independent check, and I flag it as the one place where a reviewer might want a fresh GET of the info page.
2. **Errata inventory is likewise second-hand.** I verified errata *impact* by reading the retained raw bytes against the taught sentences (no taught sentence is affected by 7600 or 7383) but the erratum list and their status come from the pair seat's errata pages. If the integrator wants the receipt to carry errata, re-verify the list at the source before writing it in.
3. **Systemic stale offsets.** Four receipts (S024, S025, S027, S034) carry offsets that resolve only in the pre-amendment view, and S034's pair report additionally publishes a text-view digest that contradicts the committed blob. The counter cannot see any of this (`measure.py` checks quote presence, not offsets). If L1 wants offsets to be trustworthy evidence, they need either re-derivation after every text-view regeneration or an explicit view digest in each `anchorObserved`; today the field is prose the counter never verifies.
4. **Bound interpretation disclosed.** I read `corpus/lessons/round-24.md` lines 25–40 only to check the cross-reference the receipt itself cites for its digest (`corpus/lessons/round-24.md:33`, which does record `61a5378f…5cd2d7`). I did not open, run, retry, rephrase or reroute any round-24 assignment, probe, counter, or `.ufo/waves/round-24/` material; nothing from round 24 was reused as evidence beyond that single cited corpus line.

## 7. Tooling

No tool was installed, updated or removed. Everything used was already present: `python3` 3.14.8 (stdlib only: `gzip`, `hashlib`, `re`, `types`, `subprocess`), `git` 2.56.0, `grep`/`sed`/`curl` (system). No builds, tests, linters or counters were run; `measure.py` was read but not executed (its output is quoted from the lane's committed `verification/measure-candidate*.json`). No file was written except this report; no corpus file, script, fleet repo, sibling lane, or Git index/jj state was mutated.

```json
{"target":".ufo/waves/round-26/rechecks/S034.json","verdict":"DISAGREE","severity":"low"}
```
