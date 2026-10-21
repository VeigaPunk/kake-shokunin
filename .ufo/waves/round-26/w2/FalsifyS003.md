# FalsifyS003 — receipt `rechecks/S003.json` (verdict HOLD), row `corpus/SOURCES.md:11`

- Seat: KakeR26-2.FalsifyS003 (reviewer, leaf). Axis: freshness. Milestone: r26-recheck-falsify. Checked 2026-10-21.
- Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Target under attack: `.ufo/waves/round-26/rechecks/S003.json` (HOLD) and the SOURCES.md row line it certifies.
- Verdict: **AGREE** on the row verdict HOLD and on the quote/anchor/no-drift findings. One **low-severity** internal-consistency finding on the receipt's prose (Finding 1). Nothing in scope overturns HOLD.

## 0. What the receipt claims, and whether it survives

Receipt (`rechecks/S003.json`, committed at candidate, `git show e28312b…:.ufo/waves/round-26/rechecks/S003.json`):

- `verdict` HOLD, `fetchIndex` 1
- `quote` "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site."
- `anchorObserved` "'About publishing sources' section, first paragraph (directly after the 'In this article' nav); matching CNAME note retained at the end of 'Creating a custom GitHub Actions workflow to publish your site'"
- `reason` "...returned 200 today with both row anchors intact... Scope and teaches hold; both citing claims (ghp-custom-domain.md:22 CNAME note, ghp-served-set.md:28 source folder) are still supported."
- `correction` null

Row `corpus/SOURCES.md:11` (verified byte-identical between base and candidate; `git diff 97404de… e28312b… -- corpus/SOURCES.md` touches only the appended round-26 paragraph at line 79):

`teaches` = "GitHub Pages can publish from a selected branch or from a GitHub Actions workflow"; `anchor` cell = "About publishing sources and note under Creating a custom GitHub Actions workflow; fetched 2026-10-19".

## 1. Does the quote ground THIS row's teaches, or only page chrome / a neighbouring clause?

**It grounds the teaches, in body prose, not chrome.** Evidence from the retained raw bytes `fetched/S003-1.raw.gz` (decompresses to 154,136 bytes; sha256 `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`, equal to `fetched/manifest.json` S003 `sha256`/`bytes` and to `population.json` S003 fetch 1):

- The quote is a real rendered paragraph, not navigation or a sidebar entry:
  `gzip -dc fetched/S003-1.raw.gz | grep -c '<p>You can publish your site when changes are pushed'` → the exact plain-HTML block is present at byte offset 51837:
  `<p>You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.</p>` (`exact plain <p> block present: True`).
- It sits inside the article region, after the section heading the row names: `<h2 id="about-publishing-sources"` at 51638, the quote `<p>` at 51837, next `<h2 id="publishing-from-a-branch"` at 53830. So the quote is the **first paragraph of the "About publishing sources" section** — exactly the row's anchor cell.
- Not page chrome: the same sentence also occurs in the escaped Next.js payload (offset ~116507 and ~149390 as `\u003cp\u003eYou can publish…`), but `source_text.py` strips `script`, so the text view contains exactly one occurrence — `text/S003-1.txt` count = 1, and it comes from the plain `<p>`. The minitoc nav (`<nav … Minitocs_miniToc`, 49234–51422) contains only section titles, not this sentence.
- Not a neighbouring clause: the section's *second* paragraph is the separate "recommend that you publish your site when changes are pushed to a specific branch… source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch" sentence (raw offset ~52277). The receipt's quote is the first paragraph and does not straddle the two.
- The quote is also row-specific: `grep -l "publish your site when changes are pushed to a specific branch" .ufo/waves/round-26/fetched/text/*.txt` matches **only** `S003-1.txt`. No boilerplate collision, and `source_text.normalize` word-bounded substring test passes (`quote_in_text: True`).
- Contract-amendment word budget: 25 tokens / 25 whitespace words (limit ≥6 tokens, ≤25 words) — at the ceiling but inside it.

**Finding 1 (low severity, prose only): the receipt's `reason` contradicts the same commit's own adjudication of `ghp-served-set.md:28`.**
`rechecks/S003.json` asserts "both citing claims (ghp-custom-domain.md:22 CNAME note, ghp-served-set.md:28 source folder) are still supported". The candidate's committed corpus file says the opposite about the same line:

`git show e28312b…:corpus/knowledge/ghp-served-set.md` line 87:
`- [r26-recheck S003 STALE] The S003 bullet at lines 28-29 is not a verbatim quote. The 2026-10-21 bytes read: "the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch."`

and the wave's own rule (`.ufo/waves/round-26/statements.json:4`) is `STALE = the statement is wrong or unsupported at its own stated scope against the 2026-10-21 bytes (content, attribution, quote fidelity, version semantics)`. Under that rule the `:28` statement is **not** supported — the corpus bullet at lines 28-29 presents the wording as a quotation and the 2026-10-21 bytes read differently (`raw: "the source folder can either be the root of the repository (<code>/</code>) on the source branch or a <code>/docs</code> folder on the source branch."`). `statements.json` records S003 × ghp-served-set as `stale: 2`.
The clause is imprecise, not verdict-bearing: the *substance* (root-or-/docs) is unchanged, which is exactly what `w1/RowS003.md` caveat 4 already discloses ("semantics are identical") and what `w1/PairS003GhpServedSet.md` K6 records as "STALE (quote fidelity; teaching HOLD)". The row verdict HOLD is unaffected and the corpus bytes are correct. Minimal correction (single clause, receipt prose only — the corpus stays append-only):
> `Scope and teaches hold; the CNAME-note citation (ghp-custom-domain.md:22) is verbatim today; the source-folder citation (ghp-served-set.md:28) holds in substance but its quoted wording is not verbatim (quote-fidelity correction appended at corpus/knowledge/ghp-served-set.md:87).`

**Finding 2 (residual, non-blocking): the S003 row's own date cells still read 2026-10-19.** `corpus/SOURCES.md:11` keeps `fetched 2026-10-19` inside the anchor cell and `opened 2026-10-19`; the round-26 re-fetch is 2026-10-21. This is consistent with the contract's append-only rule (only status/recheck/used-by cells are mutable) and is disclosed at file level by the appended round-26 paragraph (`corpus/SOURCES.md:79`, "Re-fetched every recorded URL with one public GET … Retained gzip bytes and sha256 under round26 `fetched/`") and by the per-file EOF blocks. Not a defect; recorded as residual risk only.

## 2. Is the anchor observed correct in the raw bytes?

Yes, both halves, checked in the retained bytes and re-checked live.

- "About publishing sources" — heading `<h2 id="about-publishing-sources" tabindex="-1">` at raw 51638; heading ids present in the page: `['about-publishing-sources', 'publishing-from-a-branch', 'troubleshooting-publishing-from-a-branch', 'publishing-with-a-custom-github-actions-workflow', 'creating-a-custom-github-actions-workflow-to-publish-your-site', 'troubleshooting-publishing-with-a-custom-github-actions-workflow', 'survey-title']`.
- "directly after the 'In this article' nav" — the minitoc nav block spans raw 49234→51422; the `About publishing sources` h2 follows at 51638 and its first `<p>` at 51837. The h2 is the first thing after the nav closes, and the quoted sentence is that section's first paragraph.
- "CNAME note retained at the end of 'Creating a custom GitHub Actions workflow to publish your site'" — the h3 `creating-a-custom-github-actions-workflow-to-publish-your-site` opens at raw 67840; the plain-HTML note `<p>\nA <code>CNAME</code> file in your repository file does not automatically add or remove a custom domain…` is at raw 70227; the next h3 `troubleshooting-publishing-with-a-custom-github-actions-workflow` opens at 70793. The note is therefore **inside** that h3 and at its end (2441 of 2953 bytes into the section; the only text after it is the same paragraph's continuation). Text after the note: "Instead, you must configure the custom domain through your repository settings or through the API. For more information, see Managing a custom domain … REST API endpoints for GitHub Pages."
- The note occurs exactly once in rendered text (`text/S003-1.txt`: `CNAME` count 1; the other two raw hits are the escaped payload copies), so it is one note, not two.
- The h3 title in the receipt's `anchorObserved` ("Creating a custom GitHub Actions workflow to publish your site") is the exact page title; the SOURCES anchor cell's shorter "Creating a custom GitHub Actions workflow" is a prefix of it and unambiguously denotes the same h3, not the parent h2 "Publishing with a custom GitHub Actions workflow".

## 3. Did content or version change in a way the receipt missed?

**No prose drift; the only live differences are Next.js build artifacts.** One plain public GET of the row URL (no save, nothing written outside this report) at 2026-10-21, `https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site` → HTTP 200, 154,136 bytes, same URL. Diff of retained vs live:

- 20 diff hunks in 154,136 bytes, every one of them either a `/_next/static/chunks/…-<hash>.js` filename or the `"buildId"` field. Examples: `chunks/webpack-091b7f339815a268.js` → `chunks/webpack-5e180f68666d859a.js`; `static/ndrfAHwVnt-w5Yffjl7If/_buildManifest.js` → `static/3ojI2I6G4IdChWRIRpj5c/_buildManifest.js`; `"buildId":"ndrfAHwVnt-w5Yffjl7If"` → `"buildId":"AZNqItOm5dutcdHoWp04P"`.
- Extracted article region (`<h2 id="about-publishing-sources">` … `</article>`) is 102,454 bytes in both, differing only in the three `buildId` occurrences inside the trailing JSON island.
- Rendered text views are **identical** (retained 8,310 chars derived vs live 8,310; retained file 8,311 bytes with trailing newline). Live text contains the receipt quote and the CNAME note verbatim; live text also carries the current folder sentence "the source folder can either be the root of the repository ( / ) on the source branch or a /docs folder on the source branch".

So no version/content change is being missed by HOLD. The receipt's own scope caveat ("living page, no commit/tag pin") is the right one, and `w1/RowS003.md` caveat 1 correctly records that no prior S003 byte copy exists (confirmed: `find .ufo/waves -name '*.raw.gz' -not -path './.ufo/waves/round-26/*'` returns nothing outside round 26; no S003 bytes under round-25). Consequently the receipt's "returned 200 today" is a content/anchor-presence judgement, not a byte-drift comparison — and it does not claim to be one.

## 4. Counter-checks (none overturn HOLD)

1. *Is the quote actually in the text view the counter will use?* `source_text.normalize(receipt.quote) in source_text.normalize(text)` → `True`; `quote_in_text: True`; and `normalize(quote) in normalize(live_text)` → `True`.
2. *Does the quote collide with another row (contract-amendment specificity)?* Only `S003-1.txt` contains it; `S003` is not in `DOCUMENT_GROUPS` (`{S010,S028,S033}`), so no group exception is needed.
3. *Receipt schema / counter gate:* `RECEIPT_KEYS = {id, verdict, fetchIndex, quote, anchorObserved, reason, correction}` — the receipt has exactly those 7 keys, `correction` is `null` (required for HOLD), `fetchIndex` 1 is a population fetch of S003. `python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e` → `{"decided": 32, "expected": 32, "findings": [], "hold": 32, "stale": 0, "statementCorrections": 8, "statements": 276, "statementsStale": 8, "unverifiable": 0}`, exit 0. All 32 receipts are HOLD (`Counter({'HOLD': 32})`).
4. *Does the CNAME note really belong to this row's second anchor, or to a different S00x?* The note text is unique to this page's custom-workflow section and is what `corpus/knowledge/ghp-custom-domain.md:22-24` quotes; it matches the row's anchor cell verbatim ("note under Creating a custom GitHub Actions workflow").
5. *Could the receipt be quoting a page that has since changed such that the teaches are now narrower?* The page still carries the unqualified dual-mode statement as its own lead sentence; the only qualification present ("Your GitHub Pages site will always be deployed with a GitHub Actions workflow run") sits in the troubleshooting section and does not narrow the publishing-source distinction — the same distinction `w1/PairS003GhpServedSet.md` C1 already cites in the STALE correction at `corpus/knowledge/ghp-served-set.md:85`.

## 5. Residual risk / verification gaps

- **Unpinned living doc.** S003 has no commit/tag pin; a docs edit between the 2026-10-21 fetch and any later reading would invalidate HOLD without detection. The wave's 90d `recheck` cell plus the appended round-26 block is the only guard.
- **No pre-round byte baseline.** No S003 bytes exist under round-21/22/23/24/25 (`find` above). The 2026-10-19 wording in the corpus cannot be replayed against retained bytes, so whether "on the source branch" was added by GitHub or omitted by the corpus is unresolved — the wave records this as [INFERENCE] in `w1/PairS003GhpServedSet.md` K6 and it remains unresolved here.
- **Receipt prose is not counter-checked.** `measure.py` validates receipt schema, quote presence/specificity, anchor presence and STALE markers — it does not read `reason`. Finding 1 therefore cannot be caught by the counter and needs a human correction.
- **Disclosure.** The item allows one plain GET of the row URL; several GETs of that same documentation URL were issued while cross-checking the live text and diffing hunks (all read-only, same URL, nothing saved to disk, no other host contacted, no property probing).

## 6. Housekeeping

- No tool installed, upgraded or removed; no pacman/uv/npm/cargo use.
- Only file written: this report. No corpus, script, fleet-repo, sibling-lane, Git-index or jj mutation; `git status --porcelain` shows only pre-existing untracked round-26 wave artifacts (`__pycache__/` byte-compiled caches of the read-only `source_text.py`, `w2/`, `verification/`, dispatch JSONs), none of them staged or committed by this seat.
- Commands run: `git show/diff/log/status`, `gzip -dc`, `sha256sum`, `python3 -c` (in-memory only), `grep`, `find`, `awk`, `curl`/`urllib` GET of the single documentation URL. Counter run with `-B` (no bytecode written).

```json
{"target":".ufo/waves/round-26/rechecks/S003.json (HOLD) + corpus/SOURCES.md:11","verdict":"AGREE","severity":"low"}
```
