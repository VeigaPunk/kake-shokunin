# SourceOpenS005 — S005 live reopen and the preflight inference

Seat: KakeR27.SourceOpenS005 (read-only leaf, no dispatch). Axis judged: freshness.
Milestone: r27-full-citing-set. Scope: reopen the single public URL in `corpus/SOURCES.md`
row S005, compare it with the round-27 retained capture, and test one grouped inference at
`corpus/knowledge/static-canonical-preflight.md:53-54` (the sentence starts at line 52:
"Prepare the / manifest over actual built/deployable HTML when that artifact exists, not over /
an assumed checkout served set (S001–S006, `ghp-served-set.md`).")

## Row apparatus (verbatim from `corpus/SOURCES.md` row S005)

- kind `docs`; tier A; status `mined`; opened `2026-10-19`; recheck `90d`;
  used-by `corpus/knowledge/ghp-custom-domain.md`.
- source cell, exactly one URL:
  `https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site`
- scope: "Custom-domain configuration for Actions-published Pages sites".
- anchor cell: "Configuring an apex domain step 4 and Configuring a subdomain step 4; fetched 2026-10-19".
- teaches: "An Actions-published site ignores a repository CNAME file; the domain is configured
  through Pages settings or the API".

## Live reopen (one public GET per URL; no credentials, cookies or auth)

| # | URL | HTTP | final URL | wire B | decoded B | sha256 (decoded body) | UTC window |
|---|---|---|---|---|---|---|---|
| 1 | row URL (HTML) | 200 | identical to row URL | 24,537 | 240,439 | `bf9ca81dfac68994dadab468e3fe82636d25efbd8f361dde3ac6024b442e299e` | 20:01:55Z → 20:01:55Z |
| 2 | same doc, `.md` form (cross-check only) | 200 | identical + `.md` | 11,805 | 26,789 | `85b813acf82cd02eb455f04e9a8ab301b8c3ca3e54b04fe2bc059c03e8c72ff1` | 20:04:45Z |

Headers (GET 1, response `Date: Wed, 21 Oct 2026 20:01:55 GMT`): `HTTP/2 200`,
`content-type: text/html; charset=utf-8`, `content-length: 24537`, `cache-control: public, max-age=60`,
`vary: x-user-version, accept, Accept-Encoding`, `x-cache: HIT, MISS`,
`x-github-request-id: 4D3C:1BBB7E:AC42DC:B7F419:6AD91670`. No `ETag`, no `Last-Modified`.
GET 2: `content-type: text/markdown; charset=utf-8`, `date: 20:04:45 GMT`. GET 2 is the markdown
source of the same document (the form used by `ghp-custom-domain.md`'s own recheck argv); it is
**not** a second S005 row URL and is not part of the retained r27 capture.

## Retained comparison (r27 capture vs r26 capture vs live)

- r27 `fetched/manifest.json` S005 idx 1: `fetchedAt 2026-10-21T19:59:56.085676+00:00`, 240,439 B,
  sha256 `6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4`
  (hash verified over the gunzipped body of `fetched/S005-1.raw.gz`, 33,557 B).
  Text view `fetched/text/S005-1.txt`: 14,701 B / 14,698 chars, sha256
  `b2a7d47d7193dd2f3d8303d32e7d2379b14e7908f26208115516237f6fd8d2ba`.
- r26 capture: `fetchedAt 2026-10-21T15:09:34.843922+00:00`, same 240,439 B, sha256
  `dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9` (receipt agrees).
- r27 vs live: 240,439 B in both; **104 differing bytes in 13 spans**, all inside Next.js
  script-src/buildId tokens (`webpack-5e180f68666d859a`→`1fbdc652d7b0357d`,
  `2137-5c2598d434944693`→`2137-1c30ccbb9981099f`, `4982-c25e321b45e9a868`→`4982-1e3d5bce25bc274d`,
  `buildId 3ojI2I6G4IdChWRIRpj5`→`gOeUVmJQ7z9zrUAITPynv`). No article byte differs.
- r26 vs r27: 108 differing bytes in 8 spans of the same kind (webpack chunk, build-manifest chunk,
  `buildId ndrfAHwVnt-w5Yffjl7I`→`3ojI2I6G4IdChWRIRpj5`).
- Asset-token-normalized page hash (Next.js `/_next/static/…` paths and `buildId` replaced with a
  fixed token) is identical for all three captures:
  sha256 `3d3cffd7851de74126a4fd817fc788c4a0e0c3c764517a646e62fc11d2ac95f0`, 239,572 normalized chars.
  Prose drift across 15:09:34Z, 19:59:56Z and 20:01:55Z is therefore **zero**; only build tokens rotate.
- Consequence for the C1 rule: the retained text view and the live HTML agree on every content
  sentence, so the text view is a faithful witness for this row's quote checks today.

## Anchor verification (raw offsets on retained/live bytes, which agree)

| element | apex section | subdomain section |
|---|---|---|
| heading | `<h2 id="configuring-an-apex-domain">` (tag offset 57,237) | `<h2 id="configuring-a-subdomain">` (tag offset 70,895) |
| ordered-step position | top-level `<ol>` item **4** | top-level `<ol>` item **4** |
| step-4 lead text | `Under "Custom domain", type your custom domain, then click Save.` | identical |
| quote occurrence | raw offset **61,968** | raw offset **75,623** |

The SOURCES anchor ("Configuring an apex domain step 4 and Configuring a subdomain step 4") is
observed exactly: the same conditional sentence is inside both step-4 list items, not in a note,
tip, warning or code block.

## Retained quote (22 words, ≤25; verbatim at both anchors)

> If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored

- Contiguous substring of the raw sentence (where `CNAME` is `<code>`-wrapped) and of the text
  view (where the backticks are absent). It occurs **2×** in the text view and 2× in raw HTML;
  the full sentence continues "and is not required".
- The markdown cross-check contains the backticked form twice; the words match.

## Inference test

Inference under test: "Prepare the manifest over actual built/deployable HTML when that artifact
exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)." It has two
separable parts.

- **P1 — the served/deployed set is not the checkout.** S005 contributes one documented instance:
  under a custom GitHub Actions workflow the repository `CNAME` "is ignored and is not required";
  the domain is set in Pages settings (step 4: type the domain, click Save). It also bounds the
  claim by mode: under branch publishing the same action "will create a commit that adds a `CNAME`
  file directly to the root of your source branch", so checkout membership matters only there.
- **P2 — the manifest should enumerate the built/deployable artifact.** S005 says nothing about
  HTML pages, build output, generator output, manifest population or enumeration boundaries. Its
  only build-related sentence (pull the CNAME commit locally after building with a static site
  generator) is about syncing a domain file, not about what a manifest measures.

Classification: **indirect contribution to P1; neither direct support nor contradiction of P2;
not irrelevant.** Direct support would require S005 to state the recommended manifest practice; it
does not. It is evidence that GitHub does not read deployment configuration from the checkout, not
evidence that built HTML differs from checkout HTML. The inferential step from "one config file is
ignored" to "measure the deployable set" is local synthesis, shared with the other five rows; this
row alone does not entail it.

Over-read hazard (must not be cited as support): "ignored" is scoped to domain configuration. S001's
archive exclusions are `.git`, `.github` and dot paths, so a checkout `CNAME` matches none of them
and may still ship as a static file; `corpus/knowledge/ghp-subpath-spotcheck.md:95` keeps "whether
Actions serves `/CNAME`" as an unverified prediction. Reading this quote as "checkout files are not
served" would be unsupported by both S005 and S001.

Weight in the grouped six, for the integration seat's honesty: S005 is the config-plane member only;
artifact-membership is S001/S004/S006, publishing mode S003, action-version change S002. The line's
`ghp-served-set.md` pointer does not itself cite S005 (that entry lists S001, S002, S003, S004, S006,
S008); S005 enters the preflight line only through the literal range `S001–S006`.

## Row teaching verdict

**HOLD at row scope.** The quote is verbatim and current at both anchors, and the row's first clause
("An Actions-published site ignores a repository CNAME file") is exactly what the bytes say. The
row's second clause is partly out of source: the article body contains **zero** `API` tokens (the
8 `API` strings in the live page are REST-version banners, footer/nav labels and code-example tab
labels in the i18n payload), so "or the API" rests on S003/S007, as round 26 already flagged (F3).
"fetched 2026-10-19" in the row is the historical open date; this reopen is 2026-10-21T20:01:55Z and
the r27 capture 2026-10-21T19:59:56Z. No status, recheck, used-by, teaches or opened cell was changed
by this read-only seat, and none needs changing for content.

## Pair record (existing obligation, not a new discovery)

- Pair: `S005` × `corpus/knowledge/static-canonical-preflight.md`, kind `source`, verdict **HOLD**
  (support at row scope; premise-level indirect contribution to the grouped inference, as argued above).
- This pair is already inside the frozen citing set: it appears in
  `c1-before.json` `missing` (one of the 16) because the literal range `S001–S006` expands it.
  It is **not** in `frozen/ledger.json`, which carries only S005 × `ghp-custom-domain.md`,
  `publish-channels.md` and `ghp-subpath-spotcheck.md`. No other citing form for S005 was found in
  the two files this seat read; the denominator is unchanged by this report.
- Adjacent observation, not judged here: the other S005 obligation in `c1-before.json`,
  `S005` × `corpus/knowledge/sitemap-orphan-audit.md`, comes only from the literal range in that
  file's metadata line ("r20 S001-S006 quote corrections 2026-10-19"); its substantive corrections
  cite S001/S002/S004/S006, so S005 has no content role there. That pair belongs to its own seat.
  Also, S005's `used-by` cell lists only `ghp-custom-domain.md` although three further files cite it;
  registry completeness is L1's call, not a content defect.
- Suggested `pairs.json` entry for L1 (not written by this seat):

```json
{"row":"S005","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD",
 "fetchIndex":1,
 "quote":"If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored",
 "anchor":"Configuring an apex domain top-level ordered step 4 and Configuring a subdomain step 4 (same sentence at both; h2 ids configuring-an-apex-domain / configuring-a-subdomain)",
 "reason":"Live 2026-10-21T20:01:55Z bytes and the r27 retained capture agree: under workflow publishing no CNAME file is created and any existing one is ignored and not required, at both step-4 anchors. Contribution to static-canonical-preflight.md:53-54 is premise-level indirect: deployment configuration is not read from the checkout. S005 does not address HTML/build artifacts, so it does not entail the built-HTML manifest rule; that step is local synthesis with S001/S004/S006. 'Ignored' is domain-config scope, not artifact membership (S001 excludes .git/.github/dot paths only)."}
```

## Uncertainties and limits

1. Living documentation page with no `ETag`/`Last-Modified` and `cache-control: max-age=60`; freshness
   is established by body comparison at the recorded instants, not by a validator. Drift after
   20:01:55Z is unobserved.
2. The `.md` fetch is the same document's markdown source, not a second row URL; it corroborates the
   sentence but is not retained r27 evidence.
3. The text view is lossy (14,701 B vs 240,439 B); the C1 quote rule checks the text view, and the
   chosen quote passes there and against raw markup.
4. "Step 4" is page structure (ordered list index), not a stable identifier; a restructure could
   renumber it. No claim is made here about HTML membership, artifacts, or whether `/CNAME` is served.
5. Round 26's report recorded raw offsets 62,011/75,666 for the same phrase; measured directly on
   the r26, r27 and live bytes the offsets are 61,968/75,623 in all three. My values are used above;
   the r26 figure appears to be from a different string representation and is not relied on.

## Verification performed

1. Read `corpus/SOURCES.md` row S005, `corpus/knowledge/static-canonical-preflight.md` lines 45-73,
   `corpus/knowledge/ghp-custom-domain.md` lines 1-40, `ghp-served-set.md` lines 1-45, and
   `grep -n` on the preflight sentence (authoritative line numbers 52-54).
2. One `curl` GET of the row URL and one of the same doc's `.md` form (public docs, no auth);
   headers and bodies retained under `/fast/scratch/hyaku/kake-r27/SourceOpenS005/`
   (`S005-live.html`, `S005-live.md`, `headers.txt`, `headers-md.txt`); sha256 over decoded bytes.
3. Gunzipped the r26 and r27 retained `S005-1.raw.gz`, verified both against manifest/receipt hashes,
   and byte-index diffed the three bodies (104 B/13 spans, 108 B/8 spans, 125 B/8 spans r26-live);
   normalized (asset-token-stripped) page hash identical across all three.
4. `html.parser` step parse to confirm top-level ordered step 4 under both h2 ids; raw-offset and
   occurrence counts for the quote; text-view sha256 and quote presence; `.md` sentence count = 2;
   `API` token count body vs text view.
5. No tool installs, no pacman/service changes, no browser/account/publication operations; writes
   limited to scratch and this report; no live-lane source/index/fleet/git edits; nothing committed.
