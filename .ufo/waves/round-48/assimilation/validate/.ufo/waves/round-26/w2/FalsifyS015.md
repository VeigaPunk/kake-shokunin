# Falsify S015 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS015` (leaf member — no subagent dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S015.json` (verdict HOLD) and the SOURCES row `corpus/SOURCES.md:23`.

Goal: try to show the receipt is WRONG — (a) the quote does not ground this row's `teaches` (page chrome or a neighbouring clause instead), (b) `anchorObserved` is mislocated in the raw bytes, (c) content or version changed in a way the receipt missed.

**Verdict on the S015 receipt: AGREE.** It survives every falsification attempt I ran, on the receipt's own ground (retained bytes) and against a live re-GET of the same URL. Residual observation on the receipt: **low** (locator precision only).

**Separately, I found a real defect in the round's counter (`measure.py`), outside this item's target but load-bearing for the C1 evidence.** It does not change any count, exit code, or the S015 verdict; severity **medium** as an evidence/auditability defect. Details in §5; routed to the counter-owning seats `KakeR26-2.CounterCritic` and `KakeR26-2.MutateCounter` (neither had reported it).

---

## 1. The row and the receipt under attack

`corpus/SOURCES.md:23` — byte-identical at base `97404de4` and candidate `e28312b1` (md5 of the line: `95e2d611c22e90cc512c359ea662a7c5` at both revisions; the only `corpus/SOURCES.md` delta in the whole round is the appended round-26 note at `corpus/SOURCES.md:79`):

```
| S015 | GitHub Docs: GitHub Pages limits — https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | docs | A | Published-site size and platform usage limits | Usage limits; fetched 2026-10-19 | Published GitHub Pages sites are limited to 1 GB | queued | 2026-10-19 | 90d | — |
```

- teaches: *“Published GitHub Pages sites are limited to 1 GB”* → the **published-site** size cap, at **1 GB**.
- anchor: *“Usage limits; fetched 2026-10-19”* → the *Usage limits* section of the limits page.
- status `queued`, cadence `90d`, `used-by —` (no knowledge entry cites this row).

Receipt under attack — `rechecks/S015.json`, sha256 `3ac9f452885a2febc119fe37b65b1f819c51b628a4cd98433e46d4524fdf2039` in the worktree **and** at candidate `e28312b1` (identical blob); absent at base `97404de4`:

```json
{"id":"S015","verdict":"HOLD","fetchIndex":1,
 "quote":"Published GitHub Pages sites may be no larger than 1 GB.",
 "anchorObserved":"\"Usage limits\" section heading, bullet list of usage limits (single-line text view line 1)",
 "reason":"The re-fetched page still carries the 1 GB published-site cap in its Usage limits section, so the row's scope (published-site size and platform usage limits), anchor (Usage limits) and teaches all still hold; the neighbouring limits (10-minute deploy timeout, 100 GB/month soft bandwidth, 10 builds/hour) also persist.",
 "correction":null}
```

Retained bytes under test: `fetched/S015-1.raw.gz` → 88 733 B, sha256 `e5e9c38f4d09a286ed2d06609c678097da8771c322025b875ea50f41dc2f5014` (matches `fetched/manifest.json:297` and `population.json:352`). Text view `fetched/text/S015-1.txt` = 4 037 B, sha256 `64a9b04b9b5f79f3ee99876a0a01cff33f1bd6478ad71184100fb91e06845ff7`.

## 2. Attack A — does the quote ground THIS row's `teaches` (not page chrome, not a neighbouring clause)? → NO DEFECT

The `<li>` list under the `Usage limits` heading, extracted from the retained raw bytes (`<li><p>…</p></li>` items, in document order):

```
1. You can only create one user or organization site for each account on GitHub.
2. GitHub Pages source repositories have a recommended limit of 1 GB. For more information, see About large files on GitHub.
3. Published GitHub Pages sites may be no larger than 1 GB.      <== RECEIPT QUOTE
4. GitHub Pages deployments will timeout if they take longer than 10 minutes.
5. GitHub Pages sites have a soft bandwidth limit of 100 GB per month.
6. GitHub Pages sites have a soft limit of 10 builds per hour. This limit does not apply if you build and publish your site with a custom GitHub Actions workflow.
7. In order to provide consistent quality of service for all GitHub Pages sites, rate limits may apply. …
```

The **neighbouring-clause trap is live on this page and the quote avoids it**: bullet 2 is a *different* 1 GB claim with a *different* modality and a *different* subject — *source repositories*, “**recommended** limit of 1 GB”. The row teaches *published* sites “**limited to** 1 GB”. The receipt's quote is bullet 3 — the published-site cap — not the source-repo recommendation, and not the page chrome. A receipt that had quoted “1 GB” loosely (e.g. bullet 2) would have mis-grounded the row; this one did not.

- The quote is **verbatim**: byte-for-byte inside the raw HTML at offset 50 520 — `<li>\n<p>Published GitHub Pages sites may be no larger than 1 GB.</p>\n</li>`.
- It is **not chrome**: the chrome of this docs family (`Back to top Help and support Was this Doc helpful?`) is absent from the quote; the quote is a substantive usage-limit rule.
- **Word-bounded match** in the committed text view (the counter's own rule, `measure.py:273-275`): `re.search(r"(?<!\w)" + re.escape(normalize(quote)) + r"(?!\w)", text)` → match, span (2157, 2213) in `fetched/text/S015-1.txt` (1 occurrence).
- **Row-specific** (amendment rule “a decided quote must not occur in any other population row text outside its document group”; S015 is in no declared group, `measure.py:47`): I re-ran the counter's own text pipeline (`source_text.py` → `text_of` → `normalize`) over **all 34 retained bodies** and over **all 34 committed text views**: the quote occurs in `S015-1.raw.gz` and `S015-1.txt` **only**. No twin quote among the 32 receipts either.
- **Token/word rule** (`measure.py:386-390`): `tokens = len(re.findall(r"[^\W_]+", quote)) = 11 ≥ 6`; `words = len(quote.split()) = 11 ≤ 25` → passes.
- The receipt's three “neighbouring limits” claims are each literally present in the 2026-10-21 bytes: 10-minute deploy timeout (bullet 4), 100 GB/month soft bandwidth (bullet 5), 10 builds/hour (bullet 6). ✓
- **The only citing statement in the lane still holds.** `grep -rn "S015" corpus/` → `corpus/SOURCES.md:23`, the round-20 gate note, and `corpus/lessons/round-20.md:217`, whose quote `“Published GitHub Pages sites may be no larger than 1 GB.”` is the **same string** as the receipt's quote and is still word-bounded-present in the 2026-10-21 text view. `corpus/lessons/round-20.md` is byte-identical at base and candidate (md5 of line 217: `558dd3ce8d920d52fae91b467e42f3f2` at both). S015 has **no** `corpus/knowledge/*` entry, so `statements.json` `pairs` correctly contains no S015 entry (all 25 pairs point at `corpus/knowledge/*.md`), and no `[r26-recheck S015 STALE]` block is owed — nor does one exist (`grep -rn "r26-recheck S015" corpus/` → 0 hits, correct for HOLD).

**Conclusion:** the quote grounds the row’s `teaches` at its stated anchor. No mis-grounding, no chrome, no neighbouring clause.

## 3. Attack B — is `anchorObserved` correct in the raw bytes? → NO DEFECT

`anchorObserved` claims: *«"Usage limits" section heading, bullet list of usage limits (single-line text view line 1)»*.

| claim | raw-byte evidence (`fetched/S015-1.raw.gz`, decompressed) | verdict |
|---|---|---|
| “Usage limits” section heading | `<h2 id="usage-limits" tabindex="-1"><a class="heading-link" href="#usage-limits">Usage limits<span class="heading-link-symbol" aria-hidden="true"></span></a></h2>` at byte offset **49 254** | ✓ |
| the quote sits in that section’s bullet list | quote at **50 520**; the next `<h2 id="educational-exercises">` is at **51 772** → 49 254 < 50 520 < 51 772, i.e. the quote is inside the Usage-limits section and not in the neighbouring “Educational exercises” section | ✓ |
| “bullet list of usage limits” | lead-in `<p>GitHub Pages sites are subject to the following usage limits:</p><ul>` immediately precedes the `<li>` items quoted in §2 | ✓ |
| “single-line text view line 1” | `fetched/text/S015-1.txt` = 4 037 B with exactly **1** newline (trailing LF); content = `text_of(raw) + "\n"` — I re-derived the view from the raw bytes with the committed `.ufo/waves/round-26/source_text.py` and it is byte-identical to the committed view (`file == text_of + LF` → True, sha256 `64a9b04b…`) | ✓ |

**Residual (low, no correction required):** the string “Usage limits” occurs 5× in the raw bytes — sidebar nav (48 402), the `h2` heading (49 335 → 49 254 for the tag start), and three Next.js payload copies (75 762, 79 811, 86 149). The receipt names the *section heading*, which is the real one and is the one the row's anchor cell means; the anchorObserved does not spell out the `id="usage-limits"` disambiguator. Pure locator precision, not a mislocation.

## 4. Attack C — did content or version change in a way the receipt missed? → NO DEFECT

One plain public GET of the row URL (already listed in `corpus/SOURCES.md`; `curl 8.23.0` / `python3 urllib`, 2026-10-21 ~16:29–16:50 UTC; response **not** saved to disk):

- **HTTP 200**, `content-length: 88733` — identical to `manifest.json:294`.
- **Rendered text is byte-identical** to the retained view: normalizing live bytes and retained bytes with the committed `source_text.py` gives `live text len 4035`, `retained text len 4035`, `text identical: True`.
- **The Usage-limits section slice is byte-identical** live vs retained: `sha256 = 12cf4a0db38660e7b2da240cb159d632033e2eeba4fdb8ecba0e627481a29fee` for both.
- The whole-page sha differs (`0d4c8c83…` live vs `e5e9c38f…` retained). I characterised all 18 diff regions: **every one is a Next.js build artefact** — `/_next/static/chunks/*.js` content hashes, the `/_next/static/<buildId>/_buildManifest.js` path, and the `__NEXT_DATA__` `"buildId"` value (`PpWMQGxNtWl9_nwgOyDKU` retained → `RFHaKDekHOOUtf5ZK8clQ` live). No diff region touches prose, the heading, or any `<li>`. So the byte difference is a redeploy, **not** a content change — and the receipt’s content claim survives it.
- **No version/date marker to miss**: the page carries no “Last updated” line (`'last updated' in text.lower()` → False; `text.count('Updated')` → 0). The only dates in the payload are GitHub API-version dates (`2026-03-10`, `2022-11-28`) and an unrelated GHES deprecation date (`2026-10-16`) — none is a page-version stamp.
- The page’s set of headings is unchanged live vs retained: `GitHub Pages / GitHub Pages limits / Who can use this feature? / In this article / Usage limits / Educational exercises / Help and support / Was this Doc helpful? / Help us make GitHub Docs great! / Still need help?` — `live heads == retained heads: True`.
- **Corroboration of the row’s own history:** the base lesson line `corpus/lessons/round-20.md:217` records the identical quote and anchor from the 2026-10-19 open, and the identical quote is still present on 2026-10-21 → the taught claim is unchanged across the row’s whole life, so `HOLD` (not `STALE`) is the correct verdict and no `[r26-recheck S015 STALE]` block is owed.

**Conclusion:** no content or version change was missed.

## 5. Separate lane finding — the round counter drops its per-row output (not part of this item’s target; routed to the counter seats)

`.ufo/waves/round-26/measure.py:513` builds the per-row records into a **local** `rows` list (appended at `:519`) and `:528-529` returns **without assigning it to `output`**. The only `output["rows"] = …` is the early-exit path at `measure.py:495` (`receipts_absent`). `base_result()` (`:461`) initialises `"rows": []`, and on the success path nothing overwrites it.

Observed, running the committed counter read-only at both revisions:

```
$ python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de4ff73d6c8a4f87385cf5fdf36dca7f006   # base
exit=1  rows len 32  (early-exit path: all verdict null)   decided 0  findings ['receipts_absent']
$ python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e   # candidate
exit=0  rows len 0   decided 32  hold 32  stale 0  findings []
```

The committed verification artifacts show the same asymmetry: `verification/measure-before.json` → stdout `rows` length 32, while `verification/measure-candidate.json` and `verification/measure-candidate-reverify.json` → stdout `rows` length **0** with `decided 32`. A reader diffing before/after sees 32 rows *vanish* instead of 32 rows *decided*, and the per-row evidence for S015 (`{'id':'S015','decided':True,'verdict':'HOLD','findings':[]}`) exists nowhere in the counter output — it must be re-derived from the receipt files by hand.

Impact: **none on the C1 count.** `decided/hold/stale`, the statement ledger totals (276 / 8 / 8) and the exit code are all correct and match the round note at `corpus/SOURCES.md:79` (“HOLD 32, STALE 0, UNVERIFIABLE 0 at row level”). Impact: the per-row audit trail required to *see* that each of the 32 rows was decided is missing from the counter’s own output. Severity **medium** as an evidence/auditability defect; a selftest case that asserts the per-row records would have caught it (no case asserts them today — `run_case`, `measure.py:733-740`, checks exit, finding ids, decided count and local-population source only).

**Minimal correction (one line, before the return at `measure.py:529`):** `output["rows"] = rows`

Verified **in memory** (the committed `measure.py` was not modified; `git status --porcelain .ufo/waves/round-26/measure.py` is empty):

```
patched exit code: 0
patched rows len: 32
S015 row record: [{'id': 'S015', 'decided': True, 'verdict': 'HOLD', 'findings': []}]
decided/hold/stale: 32 32 0 | findings: []
patched selftest exit: 0 | passed 14 failed 0
```

## 6. Receipt-shape and counter agreement (for completeness)

- Receipt keys are exactly the 7 required by `measure.py:52` (`id, verdict, fetchIndex, quote, anchorObserved, reason, correction`); `id == "S015"`, `verdict == "HOLD"`, `fetchIndex == 1` is the row’s only population fetch (`population.json:347-357`), `reason` non-empty, `anchorObserved` non-empty, `correction: null` (required for HOLD by `measure.py:400-401`).
- All 32 receipts at candidate are `HOLD` (32/32 `HOLD`, 0 `STALE`, 0 `UNVERIFIABLE`), consistent with `corpus/SOURCES.md:79`.
- Counter at candidate: `decided 32, hold 32, stale 0, unverifiable 0, statements 276, statementsStale 8, statementCorrections 8, findings []`, **exit 0**; at base: `decided 0`, finding `receipts_absent`, **exit 1**. Population pin matches the counter’s own `POPULATION_SHA256` (`16330e1e…`) for both the worktree file and the committed blob.
- Corpus-wide STALE-tag census at candidate: `{S010: 2, S003: 2, S021: 1, S026: 1, S030: 2}` = 8 tags, matching `statements.json` `stale` sum 8; **S015: 0**, correct for a HOLD row with no knowledge entry.

## 7. Verification gaps / limits of this attack

- I could not re-derive the **2026-10-19** bytes: the lane retains no copy of the limits page from that date, so “unchanged since the row was opened” rests on (a) the corpus’s own 2026-10-19 record of the same sentence and anchor (`corpus/lessons/round-20.md:217`, byte-identical at base and candidate), (b) the identity of the live and retained Usage-limits section bytes on 2026-10-21, and (c) the absence of any version/date marker on the page. All three point the same way.
- The live page is a **living docs URL with no pin and no `etag`/`last-modified`** (`manifest.json:291-292` both `null`); my GET is a point-in-time observation, not a guarantee. This is the same limitation `w1/FetchCritic.md:37` recorded for the whole docs.github.com family, and the receipt does not over-claim beyond it.
- Freshness of *this* row is bounded by the 90-day cadence in the row; the recheck date is 2026-10-21, two days after the 2026-10-19 open — well inside cadence.
- Per the lane bounds I did not read, run, retry or re-route round-24 material; no property, site, browser, account, credential, publication or security probing; no corpus, script, fleet-repo, sibling-lane or lane Git-index/jj mutation.

## 8. Process / bound compliance

- **Tools used, none installed or updated**: `python3 3.14.8` (stdlib only: gzip, hashlib, html.parser via the committed `source_text.py`, difflib, urllib, re, json, subprocess, types), `curl 8.23.0` (OpenSSL 3.6.5), `gzip 1.15`, `sha256sum 0.8.0`, `git 2.56.0`. **No pacman / uv / cargo / npm transaction was performed**; the host-wide pacman pause was therefore untouched. No tool install or upgrade was needed for this falsification.
- **One plain public GET** of `https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits` (a documentation URL already listed in `corpus/SOURCES.md`), used only for the drift comparison; the response was held in memory and **not written to disk** (no copy retained anywhere). A second GET was used to characterise the build-hash diff regions, likewise in memory only.
- **Wave counter run read-only** at base and candidate revisions (`measure.py --root . --revision <sha>`); it writes nothing. The one-line fix in §5 was validated on an **in-memory copy** (`exec` of a patched source string) — the committed `measure.py` is unmodified (`git status --porcelain` clean for it).
- **Files written by me**: this report only (`.ufo/waves/round-26/w2/FalsifyS015.md`). Importing the committed `source_text.py` created untracked `__pycache__/` byte-code directories under `.ufo/waves/round-26/` and `.ufo/waves/round-26/before/`; I removed those regenerable byproducts. No corpus file, script, receipt, manifest, text view, population, statement ledger or Git index was touched.

```json
{"target":".ufo/waves/round-26/rechecks/S015.json","verdict":"AGREE","severity":"low"}
```
