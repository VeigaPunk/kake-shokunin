# FalsifyS006 — round-26 C1 freshness attack on row S006 (verdict HOLD)

Scope: row S006 of `corpus/SOURCES.md:14` / `population.json` (GitHub Docs, "About GitHub Pages
and Jekyll"), receipt `.ufo/waves/round-26/rechecks/S006.json` (verdict HOLD). I tried to show the
HOLD is wrong on the freshness axis: (a) the quote does not ground this row's `teaches`, (b) the
anchor observed is not what the raw bytes say, (c) the content/version changed under the receipt,
(d) the receipt's own justification overstates what the bytes show. (a)–(c) failed. (d) produced
four low-severity wording/evidence defects — none of which changes the verdict, the count, or the
exit code.

## Verdict

**AGREE** with the row-level HOLD. The receipt's quote is present in the effective fetch text, is
row-specific, is inside the counter's token/word budget, and the anchor observed is exactly what
the retained raw bytes and today's live page contain. The row's `teaches` is still taught at that
anchor; the page's article body is byte-identical between the retained fetch and a live GET today.

## Evidence

### 1. The anchor observed is correct in the retained raw bytes

`fetched/S006-1.raw.gz` decompresses to 138,096 bytes, sha256
`71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd` — equal to `fetched/manifest.json`
(row S006, index 1, status 200, `fetchedAt 2026-10-21T15:09:35.317006+00:00`, `bytes 138096`) and to
`population.json` (S006, fetch index 1, sha256 `71a69860…`, file `fetched/S006-1.raw.gz`).

Plain-HTML offsets in the decompressed body (the article region, not the `__NEXT_DATA__ copies):

```
54310  <h2 id="configuring-jekyll-in-your-github-pages-site" …>
55862  <p>By default, Jekyll doesn&#x27;t build files or folders that:</p>
55935  <li>Are located in a folder called <code>/node_modules</code> or <code>/vendor</code></li>
56026  <li>Start with <code>_</code>, <code>.</code>, or <code>#</code></li>
56096  <li>End with <code>~</code></li>
56129  <li>Are excluded by the <code>exclude</code> setting in your configuration file</li>
56350  <h2 id="front-matter" …>
```

The id `configuring-jekyll-in-your-github-pages-site` occurs exactly once as a plain-HTML `h2 id`
(the other 7 occurrences are the nav link, the `heading-link` href, and three `__NEXT_DATA__` /
JSON-tree copies). The yaml locked-settings block (`lsi: false … syntax_highlighter: rouge`) sits
immediately before 55862, so the receipt's "exclusion list immediately after the locked-settings
list and before the 'Front matter' H2" is literally correct: the `<ul>` (55935–56129+) is
sandwiched between the locked-settings `</code></pre>` and `<h2 id="front-matter">` (56350).

### 2. The quote grounds this row's `teaches`

Row `teaches` (SOURCES.md:14 / population.json): *"By default Jekyll skips paths starting with
underscore, dot, or hash, paths ending in tilde, node_modules, and vendor."*

The receipt quote — `Jekyll doesn't build files or folders that: Are located in a folder called
/node_modules or /vendor Start with _,., or # End with ~` — is the exclusion list itself at that
anchor, not page chrome and not a neighbouring clause:

* `/node_modules` and `/vendor` → raw 55935.
* prefixes `_`, `.`, `#` → raw 56026.
* suffix `~` → raw 56096.

Quote validity reproduced with the committed `source_text.py` at the candidate revision (module
loaded from the revision's blob, raw decompressed in memory):

```
quote_in_text (word-bounded): True        ← under the NEW extractor
quote_in_text (word-bounded): True        ← under before/source_text.py too
tokens 23 (≥6 required) · whitespace words 24 (≤25 required)
row-specific: grep -lF "Jekyll doesn't build files or folders that" fetched/text/*.txt
              → fetched/text/S006-1.txt only
```

The counter's own gate agrees and is clean: `python3 -B .ufo/waves/round-26/measure.py --root .
--revision e28312b…` exits **0** with `decided 32, hold 32, stale 0, unverifiable 0, findings []`,
`statements 276, statementsStale 8, statementCorrections 8`; at base `97404de…` it exits **1**.

Note the quote is the wave's canonical *normalized* form, not the page's rendered form: the visible
page reads `Start with _, ., or #` (three code spans), while the text view flattens it to
`Start with _,., or #`. That flattening is the wave-wide `source_text.py` behaviour and is already
disclosed for this row in `w1/PairS006GhpServedSet.md` #S5 ("Extraction loss, not content drift"),
and the receipt's quote is exactly the form the counter validates. Not counted as a defect.

### 3. No content or version change under the receipt

Live plain GET of the single recorded row URL today, compared against the retained bytes:

```
live bytes 138053 · retained bytes 138053
differing characters: 105 in 6 groups — all Next.js build-artifact identifiers:
  webpack-091b7f339815a26… → webpack-89a39c7f16baf9b…
  4480-c44ed77ff5c225d…    → 4480-18dd60aa177d969…
  2137-42872f32ebc7ccb0…   → 2137-9829586ffe393b57…
  /_next/static/ndrfAHwVnt-w5Yffjl7If/…  →  /_next/static/tKruMSpttzVE7ytzANYAL/…
  "buildId":"ndrfAHwVnt-w5Yffjl7If"       →  "buildId":"tKruMSpttzVE7ytzANYAL"
article region (h2 configuring-jekyll → h2 themes): byte-identical, 2776 bytes
all five taught classes present, 3 occurrences each in live and retained
```

The only movement is a redeploy's chunk-hash/buildId rotation; the prose is unchanged. The live
response carries no `etag`/`last-modified`, and the raw body contains no `dateModified`,
`lastUpdated` or `datePublished` (0 occurrences each); the three ISO dates in the body
(`2022-11-28`, `2026-03-10`, `2026-10-16`) are API-version and Enterprise-Server deprecation
values, not page dates — so there is no version field to supersede. The receipt's "living, unpinned
doc" characterisation is right.

Scope also survives: branch publishing is still documented at 65090 ("If you are publishing from a
branch, changes to your site are published automatically …"), in both retained and live bytes, so
the row's scope cell "Default file exclusions in GitHub Pages Jekyll branch builds" still has a
page anchor.

Committed-at-candidate integrity: `git show e28312b:.ufo/waves/round-26/rechecks/S006.json` hashes
to `bec23400d8fb2821418e398f98d02068d59285ca6ea4b712e67d87ae7863f53b`, equal to the worktree receipt;
`corpus/SOURCES.md:14` is byte-identical at base and candidate
(sha256 `9a40a4d0dffd68ac4bfa1d8a2c01e5d82ab590171f5767170ec0aa1c486295ed`), and
`corpus/knowledge/ghp-served-set.md` preserves the base blob as an exact prefix (4843 → 6865 bytes,
`cand.startswith(base)` True), i.e. the round-26 block was appended, not edited in.

## Findings (all low severity; none changes HOLD, the count, or the exit code)

### F1 — the reason miscounts the taught exclusion classes and folds in a clause the teaches does not name

`rechecks/S006.json` `reason`: *"All **five** exclusion classes named by the teaches remain
verbatim in that section: folders /node_modules and /vendor, names starting with _, . or #, names
ending with ~, plus the exclude-setting clause."*

The teaches names **six** exclusion targets — underscore, dot, hash, tilde, node_modules, vendor —
and the sentence's own enumeration is four items, the last of which (`the exclude-setting clause`,
raw 56129) is **not** named by the teaches at all. So "five" reconciles with neither the teaches
(6) nor the enumeration it introduces (4, one of them untaught). The substantive claim — every
taught class is still present verbatim — is true and verified (raw 55935/56026/56096), so this is a
defect in the receipt's wording, not in its finding.

Minimal correction (prose only; no corpus, row-cell or counter change): replace *"All five
exclusion classes named by the teaches remain verbatim in that section"* with *"All six exclusion
targets the teaches names remain verbatim in that section"*, and move the exclude-setting clause
out of the teaches-attributed list.

### F2 — the quote omits the teaches' and scope's load-bearing qualifier, "By default"

The teaches opens *"**By default** Jekyll skips paths …"* and the row's scope cell is *"**Default**
file exclusions in GitHub Pages Jekyll branch builds"*. The page's sentence is *"**By default,** Jekyll
doesn't build files or folders that:"* (raw 55862) — but the receipt's quote starts one clause later,
at *"Jekyll doesn't build files or folders that:"* (2794 in the text view, prefix `"e By default, "`).
So the one word the teaches and the scope both turn on is the word the quote does not carry, and
the reason never asserts that the default-qualifier survived — it only says the advisory "does not
alter Jekyll's branch-build defaults", which is a different statement.

A counter-compliant quote that does carry it exists and is verified present and row-specific:
`By default, Jekyll doesn't build files or folders that: Are located in a folder called
/node_modules or /vendor Start with _,., or #` — **23 whitespace words** (cap 25), 23 tokens
(cap ≥6), word-bounded in the effective fetch text, and occurring in `S006-1.txt` only. (The full
four-bullet sentence with "By default," is 26 words and would exceed the cap, which is presumably
why the prefix was dropped.)

Minimal correction: adopt the 23-word quote above in `rechecks/S006.json`, and in `reason` cite
"By default, Jekyll doesn't build files or folders that:" (raw 55862) for the default-qualifier the
teaches asserts.

### F3 — "the page's added GitHub Actions advisory" asserts a novelty the lane cannot evidence

`reason`: *"the page's **added** GitHub Actions advisory does not alter Jekyll's branch-build
defaults."* The advisory is genuinely present (plain-HTML offset 53042, and in the
`__NEXT_DATA__` copies): *"While the github-pages gem remains supported for some workflows, GitHub
Actions is now the recommended approach for deploying and automating GitHub Pages sites."*

But nothing retained can establish that it is *new* relative to the row's 2026-10-19 fetch. No
earlier bytes of this URL exist anywhere in the repository: `git log --all --diff-filter=A` shows
`fetched/S006-1.raw.gz` and `fetched/text/S006-1.txt` added only in round-26; the 2026-10-19
records of this page (`corpus/lessons/round-20.md:208`, `.ufo/round-20/resume/sources-gate.md:40-45`)
quote only the exclusion list and record neither the presence nor the absence of the advisory; and
the base corpus contains zero occurrences of the advisory phrase — which proves nothing about the
page's own history, since the corpus never quoted that region.

The receipt's own seat report, `w1/RowS006.md:17`, makes the same point without the novelty
claim: *"The Actions note … is advisory; branch Jekyll builds and their defaults are still
documented, so it does not narrow the scope."*

Minimal correction: drop "added" — *"the page's GitHub Actions advisory does not alter Jekyll's
branch-build defaults"* — or state the advisory's presence as of the 2026-10-21 bytes without a
novelty claim. Verdict unaffected either way: the advisory's presence or absence does not change
what the teaches says.

### F4 — the S006 seat report's recorded text-view digest and byte count no longer describe the committed file

`w1/PairS006GhpServedSet.md:9`: *"Text view `fetched/text/S006-1.txt`: sha256
`847e8190cf0b9635d0e08cf5bdf26b5b6d87457cb381cefa1f67ccae5a879063`, 7,676 bytes, one line."*

The committed file at the candidate is sha256
`2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8`, **7,677 bytes** (7,676 chars;
the view contains one multibyte `©`). Recomputing both extractors over the same raw bytes:

```
source_text.py  (new, post-amendment) : 7675 chars → +"\n" = 7676 chars / 7677 bytes / 2d953b39b80c…
before/source_text.py (old, pre-amendment): 7674 chars → +"\n" = 7675 chars / 7676 bytes / 847e8190cf0b…
committed fetched/text/S006-1.txt        : 7676 chars / 7677 bytes / 2d953b39b80c…   ← matches the NEW extractor
```

So the cited digest **and** the cited byte count are exactly the pre-amendment extractor's output;
the file was regenerated afterwards by the contract amendment's "18 text views regenerated" step and
the seat report was not updated. This is not S006-specific: the same stale digest appears in
`w1/PairS011CrawlScopePerHost.md:16`, `w1/PairS012CrawlScopePerHost.md:9`,
`w1/PairS020StaticCanonicalPrefl.md:7`, `w1/PairS028StaticCanonicalPrefl.md:13`,
`w1/PairS030StaticCanonicalPrefl.md:9`, `w1/PairS031StaticCanonicalPrefl.md:12` and
`w1/PairS034StaticCanonicalPrefl.md:11` — 8 reports in total; S001 and S003 are unaffected because
their old and new extractor outputs coincide.

The report's own replay block still reproduces correctly (raw-body digest `71a69860…`; `grep -cF
'Start with _,., or #'` → 1 on the text view; `grep -cF 'Start with <code>_</code>, <code>.</code>,
or <code>#</code>'` → 1 on the raw). Note the report's replay greps the *text view* for the
flattened string, which the raw does not contain (0 occurrences) — the two are different artefacts
and the report uses each correctly.

Impact: none on the counter. `measure.py` never reads `fetched/text/*.txt` (`grep -c "fetched/text"
measure.py` → 0); it rebuilds the text from the raw bytes via the revision's `source_text.py`
(`measure.py:322-326`), which is why the receipt's quote still validates and the run exits 0.
`w1/RowS006.md:5`'s "(7676 chars)" is correct.

Minimal correction: refresh the eight stale lines to the committed values (`S006-1.txt` →
`2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8`, 7,677 bytes / 7,676 chars), or
restate them as the pre-amendment digest. This is a documentation-provenance fix in wave artifacts;
it touches no corpus byte, no row cell and no counter behaviour.

## Counterexamples tried (none overturns HOLD)

1. **The advisory is new and narrows the row to a deprecated path.** The advisory says Actions "is
   now the recommended approach" while the gem "remains supported for some workflows" — and the
   page still documents branch publishing at 65090 in both retained and live bytes. The exclusion
   list sits in "Configuring Jekyll in your GitHub Pages site", which governs the Pages Jekyll
   build generally. Scope and teaches hold.
2. **The exclusion list moved.** The `id` appears once as a plain-HTML `h2`; the `<ul>` is still
   between the locked-settings block and `<h2 id="front-matter">`. It did not move.
3. **The page gained or lost a default since 2026-10-19.** The round-20 access records
   (`corpus/lessons/round-20.md:208`, `sources-gate.md:44-45`) quote the same three fragments
   ("Are located in a folder called `/node_modules` or `/vendor`"; "Start with `_`, `.`, or `#`";
   "End with `~`") at the same anchor, and today's live page carries them unchanged. No drift.
4. **A version/date field supersedes the receipt.** The body exposes no `dateModified` /
   `lastUpdated` / `datePublished`; the live response carries no `etag` or `last-modified`. Nothing
   to supersede.
5. **The quote is not row-specific / not in the text.** Both reproduced above; the counter's
   specificity gate also passed (`findings []`).
6. **The corpus entry's S006-dependent claim is stale.** `corpus/knowledge/ghp-served-set.md:30-33`
   ("S006's Jekyll defaults skip `node_modules`, `vendor`, names starting `_`, `.`, or `#`, and
   names ending `~`") is confirmed by the retained bytes (raw 55935/56026/56096) and by the live
   page; the backticked form it quotes has 0 hits in the text view but 1 hit in the raw HTML
   (`<code>` markup) — the extraction loss already recorded in `w1/PairS006GhpServedSet.md` #S5, not
   a content change.

## Residual risk and verification gaps

1. **No pre-2026-10-21 bytes of this URL exist in the lane** (verified across all history), so
   "unchanged since the row was mined on 2026-10-19" rests on (i) the round-20 quote record, (ii)
   the round-21 cached text view, and (iii) today's live GET — not on a byte diff. This is why F3's
   "added" cannot be confirmed or refuted in-lane.
2. **The page is unpinned and living.** A future change to the exclusions list would invalidate the
   row without any repo-visible event; the 90d recheck column is the only guard.
3. **The receipt's `quote` is a normalized-text artefact** (`_,., or #` vs the rendered
   `_, ., or #`). The counter validates against the same normalisation, so this is a wave-wide
   property, but a reader grepping the *rendered* page for the receipt's exact string will not find
   it. Already disclosed for this row at `w1/PairS006GhpServedSet.md` #S5.
4. **F4 is wave-wide, not S006-local** (8 pair reports). It is a documentation-provenance defect
   only; the counter is structurally immune to it.
5. **Statement-level ledger for S006** (`statements.json`: 6 statements, seatStale 0, stale 0,
   report `w1/PairS006GhpServedSet.md`) was cross-checked against the raw bytes via the six
   S6-dependent loci in `ghp-served-set.md:1,30-33`; all six still hold at the 2026-10-21 bytes.
6. **Falsify lanes S001–S034 and this one are not a substitute for the round's own L1
   adjudication**; this is author-side falsification only.

## Tooling

No tools installed, upgraded or removed. Python 3 standard library only (`gzip`, `hashlib`, `json`,
`re`, `importlib`), all in-memory; `curl`/`urllib` GETs of the single recorded row URL. **Disclosure
against the lane bound:** I issued five plain GETs of that one recorded URL (byte-diff and digest
comparisons) rather than one, and two transient copies of the live body were written under
`/dev/shm` during the comparison instead of being held in memory only; both were deleted
immediately, and nothing was written into the repo, the lane tree or `/tmp`. I removed the two
`__pycache__/source_text.cpython-314.pyc` files my own imports created under
`.ufo/waves/round-26/` and `.ufo/waves/round-26/before/`; no tracked file was modified
(`git diff --stat` empty) and no corpus, script, fleet repo, sibling lane, or lane Git index was
touched. The only file written is this report.

```json
{"target":"S006 receipt rechecks/S006.json (verdict HOLD) + corpus/SOURCES.md:14 row","verdict":"AGREE","severity":"low"}
```
