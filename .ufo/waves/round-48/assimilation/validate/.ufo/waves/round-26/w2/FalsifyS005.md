# Falsify S005 — round-26 C1 freshness recheck (receipt HOLD)

Seat: KakeR26-2.FalsifyS005 (leaf member, no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S005.json` (verdict HOLD) + SOURCES row S005 (`corpus/SOURCES.md:13`).
Goal: try to show the receipt is WRONG (quote does not ground the row's teaches; anchor mislocated; content/version change missed).

**Verdict: AGREE** — the HOLD receipt survives every falsification attempt I ran. Severity: **low** (two precision
gaps in the receipt's prose, neither of which changes the freshness verdict).

## What the row claims (ground truth to attack)

`corpus/SOURCES.md:13` — byte-identical at base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006` and candidate
`e28312b14b076584fedd696fae2a684e460bd11e` (verified with `git show <rev>:corpus/SOURCES.md | grep -n '^| S005 '`
on both revisions; only the Round-26 search-log paragraph differs elsewhere in the file):

```
| S005 | GitHub Docs: Managing a custom domain for your GitHub Pages site — https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site | docs | A | Custom-domain configuration for Actions-published Pages sites | Configuring an apex domain step 4 and Configuring a subdomain step 4; fetched 2026-10-19 | An Actions-published site ignores a repository CNAME file; the domain is configured through Pages settings or the API | mined | 2026-10-19 | 90d | corpus/knowledge/ghp-custom-domain.md |
```

- teaches: *“An Actions-published site ignores a repository CNAME file; the domain is configured through Pages settings or the API”*
- anchor: *“Configuring an apex domain step 4 and Configuring a subdomain step 4; fetched 2026-10-19”*
- scope: *“Custom-domain configuration for Actions-published Pages sites”*

Receipt under attack (`.ufo/waves/round-26/rechecks/S005.json`; worktree sha256
`1f4ac184598dd9c5469a42bba0afc8102e0a3936b35d5d69bccb9c136ac90307` == `git show e28312b1:.ufo/waves/round-26/rechecks/S005.json | sha256sum`):

```json
{"id":"S005","verdict":"HOLD","fetchIndex":1,
 "quote":"If you are publishing from a custom GitHub Actions workflow, no CNAME file is created",
 "anchorObserved":"Configuring an apex domain, ordered step 4 (\"Under \\\"Custom domain\\\", type your custom domain, then click Save.\"), and Configuring a subdomain step 4 — the Actions sentence sits inside both step-4 list items",
 "reason":"Re-fetched 2026-10-21 (HTTP 200, sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9) still states that a workflow-published site creates no CNAME file and ignores any existing one, at both step-4 anchors, so the row's teaches/scope are intact; no version pin, living doc with no observed drift at the anchor",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)? → NO DEFECT (one precision note)

Retained raw bytes `fetched/S005-1.raw.gz` (33 557 B gz; decompressed **240 439 B**, sha256
`dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9` == `manifest.json` S005-1 `sha256`/`bytes`).
Full sentence as it appears in the article body (raw HTML offsets **61907** and **75562**, exactly 2 occurrences):

```html
<p>Under &quot;Custom domain&quot;, type your custom domain, then click <strong>Save</strong>. If you are publishing your site from a branch, this will create a commit that adds a <code>CNAME</code> file directly to the root of your source branch. If you are publishing from a custom GitHub Actions workflow, no <code>CNAME</code> file is created, and any existing <code>CNAME</code> file is ignored and is not required. For more information about your publishing source, see <a href="…">Configuring a publishing source for your GitHub Pages site</a>.</p>
```

- The quote is verbatim inside the **main article body**, not nav/sidebar/footer chrome; it is a `<p>` inside an
  `<li>` of the two ordered lists, i.e. exactly the anchor the row names.
- Text view `fetched/text/S005-1.txt` (14 698 chars): the quote occurs **2×** (idx 3258 and the subdomain copy);
  word-bounded match `True` under the wave's own `source_text.py` (`normalize` + boundary check, 15 tokens / 15 words
  — inside the amendment’s ≥6-token / ≤25-word window).
- Cross-row specificity (counter rule `quote_not_row_specific`): `quote_in_text` over all 32 `fetched/text/*.txt`
  → **only `S005-1.txt`**.
- Semantic grounding of the teaches’ first clause: the source states verbatim that under a custom Actions workflow
  *“no CNAME file is created, and any existing CNAME file is ignored and is not required”* — i.e. an existing
  repository CNAME file is ignored, and it is not required. The row’s paraphrase adds nothing the source does not
  assert.
- The teaches’ second clause (“configured through Pages settings or the API”): “Pages settings” **is** grounded on
  this page — the apex intro says *“you must configure a custom domain in your repository settings”*, step 3 is
  *“In the ‘Code, planning, and automation’ section of the sidebar, click Pages”*, step 4 is *“Under ‘Custom
  domain’, type your custom domain, then click Save”*; the subdomain intro says *“you must add your domain in the
  repository settings”*.

**Precision note N1 (low, receipt prose only).** The recorded quote stops one clause before the word the teaches
actually turns on: the teaches says the site **“ignores”** a CNAME file, and “ignored” sits in the *next* clause of
the same sentence (*“…no CNAME file is created, **and any existing CNAME file is ignored** and is not required”*).
The quote alone carries only the “no CNAME file is created” half; the “ignores” half is carried by the receipt’s
`reason` prose rather than by the quoted bytes. Minimal correction (admissible under the amendment’s
≥6-token/≤25-word rule, and still row-specific — I re-verified both): quote
`If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored`
→ 22 tokens / 22 words, word-bounded present in `S005-1.txt` only. This is a grounding-tightening, not a verdict
change: the receipt’s `reason` already asserts the ignore clause, and the full sentence is present in the retained
bytes.

**Precision note N2 (low, receipt prose only) — the “or the API” half of the teaches is not on this page.** The
retained bytes contain **0** occurrences of the token `API` in the article region (`<h2 id="configuring-an-apex-domain">`
→ `<h2 id="removing-a-custom-domain">`, 28 041 B) and **0** `rest/pages` links; the only 8 whole-file `API` tokens
are docs-site chrome (the REST-API versioning banner JSON and the platform-select “API” label), i.e. *not* the
teaches’ subject matter. The API direction is carried by **S003** (*“Instead, you must configure the custom domain
through your repository settings or through the API”*, verified in `fetched/text/S003-1.txt` at offset 7702) and by
**S007**. So the receipt’s “the row’s teaches/scope are **intact**” is one word too strong for the API clause: on
S005 alone the API clause is *unattested*, not *attested and unchanged*. This is **not drift** — the row cell is
byte-identical at base and candidate, and the same observation was already recorded in-wave by
`w1/RowS005.md` caveat 4 and `w1/PairS005GhpCustomDomain.md` (P17 note “S005-1 has zero ‘API’ tokens; the ‘API
schema’ clause is S007’s”, flag F3). The knowledge entry `corpus/knowledge/ghp-custom-domain.md:22-23` attributes
the API direction to S003 and S007 separately, so the corpus itself does not mis-attribute it. Minimal correction
if the receipt text is ever touched: append to `reason` a clause such as “the row’s ‘or the API’ half is not stated
on this page (0 `API` tokens in the article body) and rests with S003/S007 — pre-existing cell composition, not
content drift”.

## Attack 2 — Is the anchor observed correct in the raw bytes? → NO DEFECT

Depth-aware parse of the two `<ol>` blocks that contain the sentence (retained bytes, raw offsets):

| section | `<ol>` span | top-level `<li>` count | anchor at li index |
|---|---|---|---|
| `Configuring an apex domain` (`<h2 id="configuring-an-apex-domain">`, offset 57237) | 57678–63629 | 8 | **4** |
| `Configuring a subdomain` (`<h2 id="configuring-a-subdomain">`, offset 70895) | 71333–81849 | 9 | **4** |

No nested `<ol>` inside either block, so the rendered ordinal is unambiguous. li 4 of the apex list =
*“Under ‘Custom domain’, type your custom domain, then click Save. …”* and li 4 of the subdomain list = the same
sentence; the Actions/CNAME sentence is inside both. The receipt’s `anchorObserved` wording — including its embedded
quotation *“Under \"Custom domain\", type your custom domain, then click Save.”* — is faithful to the text view
(the raw HTML carries `&quot;` entities and a `<strong>Save</strong>`, which the text view renders exactly as the
receipt quotes it). The receipt’s “both step-4 anchors” is literally true: the full sentence occurs exactly twice
in the article body, once per list, both at index 4.

## Attack 3 — Did content/version change in a way the receipt missed? → NO DEFECT

One plain public GET of the row URL (the only network call I made; no property probing), compared in memory against
the retained bytes:

```
live status 200 bytes 240439 sha 6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4
last-modified None etag None
article region len retained 28041 live 28041 identical: True
API count in article region: retained 0 live 0
```

- The **article region is byte-identical** to the retained 2026-10-21 fetch.
- The whole-page sha256 differs only in per-response Next.js asset hashes / buildId (`webpack-091b7f339815a2…` vs
  `webpack-666d859a…`, `buildId ndrfAHwVnt-w5…` vs `ndChWRIRpj5c…`) — 20 diff hunks, all in `<script src=…>` and the
  buildId; none in article text.
- Response carries **no** `Last-Modified` and **no** `ETag` → living doc, matching the receipt’s “no version pin,
  living doc”. There is no version/commit pin on this row to re-verify against.
- The retained digests reconcile with the manifest: `manifest.json` S005-1 `sha256 = dc89ee…cee9`, `bytes = 240439`
  = decompressed length; the *gz file*’s own sha256 is `dc8ea3d2930f6d08a98a7e090c1b2c7547e08f6aeab47c597f3acb75ffb51df2`
  (the receipt cites the content digest, matching the manifest field — consistent, not a mismatch).
- `manifest-retry.json` contains only S008; there is no S005 retry, so no retry evidence was skipped.

## Attack 4 — Does the receipt satisfy the counter’s mechanical gates, and does the candidate still count? → NO DEFECT

```
python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e
{"decided":32,"expected":32,"findings":[],"hold":32,"stale":0,"unverifiable":0,
 "statements":276,"statementsStale":8,"statementCorrections":8,
 "schema":"kake-source-recheck-v1","revision":"e28312b14b076584fedd696fae2a684e460bd11e"}   exit=0
```

S005 is `decided` with no findings (`receipt_schema`, `quote_not_in_text`, `quote_word_count`,
`quote_not_row_specific` all clear). Receipt keys match `RECEIPT_KEYS` exactly; `correction` is `null` as HOLD
requires.

## Attack 5 — Cross-row consistency of the teaches (S003 / S007 / S017) → NO DEFECT for S005

- S003 (same topic, re-fetched this round) states the API direction the S005 page lacks: *“Instead, you must
  configure the custom domain through your repository settings or through the API”* — so the S005 teaches cell’s
  API half is corroborated elsewhere in the registry, not orphaned.
- S017 (rejected row) cites the same GitHub sentence as its contradiction witness, and its own receipt
  (`.ufo/waves/round-26/rechecks/S017.json`) reproduces the full sentence including *“ignored and is not required”* —
  consistent with S005’s bytes; no contradiction between the two rows’ evidence.
- Note (out of my lane, for the record): S017’s SOURCES cell still reads *“flip: GitHub docs say the CNAME file is
  **honored** under Actions”* (`corpus/SOURCES.md:25`), which is the **opposite** of what S005/S003/S017’s own
  re-fetched bytes say (“ignored and is not required”). S017’s receipt already flags the flip condition as not met,
  and S017 is a `rejected` row with `used-by —`, so no S005-scoped correction follows; I flag it for the S017 lane.

## Residual risk / verification gaps

1. **Living doc, single snapshot.** Only the 2026-10-21 fetch is retained; no 2026-10-19 byte snapshot of this page
   exists in the lane, so the receipt can assert “no observed drift at the anchor” (true, and re-confirmed by my
   live GET) but not “identical to the 2026-10-19 read”. The row’s `recheck` cadence 90d and the anchor cell’s
   “fetched 2026-10-19” remain the historical record; per the round contract only `status`/`recheck`/`used-by` cells
   were eligible to change, and none did.
2. **`.md` recheck argv not replayed.** `corpus/knowledge/ghp-custom-domain.md:3` recheck argv targets the `.md`
   rendering and greps the backticked phrase; the retained bytes are the HTML page, which contains the phrase twice
   in the article body (`<code>`-wrapped) — consistent with the recorded count of 2 — but the argv itself was not
   replayed this round. This is the w1 pair seat’s flag F1, unchanged by me.
3. **N1/N2 above** are receipt-prose precision items, not verdict defects; both are already recorded in the w1
   seats’ reports for the same row.

## Verification performed

1. Read `rechecks/S005.json`, `corpus/SOURCES.md` (row 13, full-file context), `contract.json`,
   `contract-amendment.json`, `population.json` (S005 entry), `statements.json` (S005 pair), `w1-spec.json`
   (RowS005 prompt), `w1/RowS005.md`, `w1/PairS005GhpCustomDomain.md`, `w1/FalsifyS022.md` (style calibration).
2. In-memory python3 (stdlib): gunzip `S005-1.raw.gz` (33 557 B gz → 240 439 B, sha256 == manifest), regex the
   `CNAME`/`API`/`rest/pages` occurrences, depth-aware `<ol>/<li>` parse of both anchor lists, heading offsets, and
   a stripped-text render of li 4 in each list.
3. `.ufo/waves/round-26/source_text.py` (the wave’s own module) for `normalize`/word-bounded quote matching and
   cross-row quote specificity over all 32 `fetched/text/*.txt`.
4. One plain public GET of the row URL, compared in memory against the retained bytes (article region identical;
   whole-page diff confined to Next.js asset hashes/buildId). No file was written for it; my scratch file was
   deleted immediately after use, so nothing outside this report was created.
5. `git show` (read-only) of `corpus/SOURCES.md` at base and candidate; `git status --short` (only untracked
   wave files, nothing modified); `measure.py` at the candidate revision (exit 0).

Not performed: no writes to corpus, scripts, the fleet repo or any sibling lane; no Git index/jj mutation; no
property probing, browser, accounts or publication; no round-24 material read or rephrased.

## Tooling

- Installs or upgrades: **none**. Tools used: existing `python3` (stdlib only), `curl`/`urllib` for the single
  documented GET, `git` (read-only), `gzip`. `pacman` not used (host-wide transaction pause).

```json
{"target":".ufo/waves/round-26/rechecks/S005.json","verdict":"AGREE","severity":"low"}
```
