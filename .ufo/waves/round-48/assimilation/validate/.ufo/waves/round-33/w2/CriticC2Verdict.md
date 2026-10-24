# KakeR33.CriticC2Verdict — does C2 verify, and do the round-33 prose sections overclaim?

Seat: critic (leaf), axis freshness. Clone `/fast/scratch/hyaku/kake-r33/w2/CriticC2Verdict/clone` at `0a0acfb1`; upstream read only through the L1 clone `/fast/scratch/hyaku/kake-r33/ds4cc-upstream` (git show/ls-tree/rev-parse). The wave-1 reports are not tracked at `0a0acfb`, so I read them read-only at the lane path `.ufo/waves/round-33/w1/*.md`. No network reads, no installs, no lane mutation except this file.

## Verdict
**C2 verifies as declared: met 4 of 4 at `0a0acfb`, 0 of 4 at base.** Every number I checked in the four prose sections and the entry is exact. **One overclaim:** PROVINCE.md:146-147 says "The round's only network reads were the public GitHub repository clone and two GitHub API run listings." That is false. The round's own LOG.md and at least six wave-1 reports record more network reads. **One provenance defect:** the corpus cites `w1/*.md` reports that are not committed at the claimed revision.

## C2 counter (exit codes)
- `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev <r>` at 5777d5a, bc6c4a8, b1752a2, e490381, 1cf452e, 0a0acfb: all exit 0; met 0, 0, 4, 4, 4, 4. My outputs are byte-identical (`cmp`) to all five committed receipts `verification/c2-*.json`. My receipts: `/fast/scratch/hyaku/kake-r33/w2/CriticC2Verdict/receipts/c2-*.json`.
- The counter is unchanged since its freeze: `git diff bc6c4a8 0a0acfb -- .ufo/waves/round-33/c2_pin_count.py` is empty. The C2 inputs (SOURCES.md, the sitemap-orphan entry, the retained sources, canonical_audit.py) are unchanged from 1cf452e to the tip.
- Independent blob check: `ls-tree 7fc6aa2f` gives sitemap.xml `67d8c7a5`, frostbite hub `e0d9ee29`, classic `12c58e2d` and remastered `4e6d70ae`, all mode 100644. These equal the retained files under `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/` at the tip.
- Known counter weakness, already disclosed at SCORECARD.md:1153-1157: a junk S065 row can also score 4 (`MutC2HollowCommit`). I checked the landed row and section by hand instead (below).

## Numbers checked (all hold)
- 7fc6aa2f: committed 2026-10-21T17:32:55Z, parent 1fbdb8ed, so one commit. It adds 12 files, all under magga/ plus sitemap.xml, and `magga/index.html` gains 9 lines. The frostbite links are at magga/index.html:371.
- Sitemap: XML-parsed loc counts are 97 (1fbdb8ed) and 100 (7fc6aa2f). The three new locs are lines 15–17. 86 locs end in `/` and 14 are explicit files.
- The old sitemap is 7,614 bytes with sha256 `18c51c45…53d`, matching sitemap-orphan-audit.md:145.
- The four S062 paths have identical blobs at both commits (render.yaml `d17ab7e5`, apps-sdk/Dockerfile `ee0b6381`, apps-sdk/src/server.ts `649726df`, .dockerignore `d6504456`). This supports the entry's "changes none of the four files" and SKILL's "empty this round".
- `pq2Remote` is `e6bd0718` (freshness-pins.json:34): `rev-list --count e6bd0718..7fc6aa2f` = 29. `sitemapStatus` is 404 (line 36).
- Retained JSON sha256 values match S066: `92bd3b31…ce1c` and `f2056e8b…67e4`.
- Run 39644779773 (Pages deploy): success, started 17:32:59Z, updated 17:33:42Z. Run 39644779805 (apps-sdk test): failure.
- The apps-sdk list holds six runs, all failures, on 7fc6aa2f, 1fbdb8ed, 95dbeb69, 6e888784, 9ec6e919 and 480dd05f. The 480dd05f run was 2026-10-14T21:32:49Z.
- magga/frostbite/index.html:208 declares `width="1280" height="960"`. The PNG IHDR of covers/classic.png reads 960×768.
- The entry's "lines 48–49" and kimi-subpath-audit.md:24 both say "93 locs", as cited.
- LOG.md:1405 says 35 wave-1 seats with a given role split. It matches the 35 `.md` reports, grouped by name prefix.
- The local checkout `~/Projects/ds4cc-marketplace` HEAD is `1fbdb8ed` (read-only rev-parse).
- PROVINCE.md:140-145 (one commit, three pages, 97 → 100, S065/S066, source-side and forge-record only), corpus/README.md:307 and SKILL.md:930-947 make no numeric claim beyond the ones above.

## Overclaim 1 — PROVINCE.md:146-147, "only network reads"
Counterexamples. All are against public github.com or api.github.com. None touched an owned property, so the sentence just before it ("no operator-owned property was fetched") holds as far as these reports show.
- The L1 also ran `git ls-remote` at round start (LOG.md:1393: "(`git ls-remote` at round start)"). SKILL.md:940 cites that result as its round-33 evidence.
- Five wave-1 seats cloned from github.com instead of the L1's local clone:
  - ExecRecountSitemapAt7fc6.md:9
  - ExecSitemapTreeParity.md:13
  - ExecNewPagesRefIntegrity.md:35
  - ScribeProvinceReadme.md:19 (its line 78 says "one network git clone")
  - ScribeS065RowDraft.md:8,25, a `--filter=blob:none` clone. Its later `git show` calls lazily fetch blobs [INFERENCE].
- CriticC2FreshnessFit.md:40-42 made more reads:
  - `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git`
  - two unauthenticated `curl` requests to api.github.com (`actions/runs`, `deployments`), both HTTP 403
  - three authenticated `gh api` reads: `actions/runs?head_sha=…`, `deployments?environment=github-pages` and `actions/workflows`. Deployments and workflows are not run listings.
- ScribeS065RowDraft.md:7: a `curl` GET of the github.com commit page (HTTP 200 at 20:02:31Z).

Tally, from reports only: 6 Git clones (L1 plus 5 seats), 2 `ls-remote`, 5 `gh api` reads (the L1's 2 plus 3 from a seat), 2 unauthenticated API GETs and 1 web-page GET. The sentence names 1 clone and 2 listings. This repeats the round-31 pattern that ScoutProvinceLiveFetchWording.md:17-26 corrected, where an "only live fetches" claim had to rest on a complete fetch record.

Impacted axes: freshness and calibration (provenance of what was read). No owned-site breach is shown.

Smallest safe correction: append, without rewriting, under PROVINCE "Round-33 frontier step": "Correction: all network reads this round were against the public github.com repository VeigaPunk/ds4cc-marketplace and its API: 6 Git clones (L1 and five wave-1 seats), 2 `git ls-remote`, 5 authenticated `gh api` reads (runs, deployments, workflows), 2 unauthenticated API requests that returned 403, and 1 commit-page GET. No operator-owned property was contacted."

## Defect 2 — corpus cites wave-1 reports that are not committed at 0a0acfb
- `git ls-tree -r 0a0acfb .ufo/waves/round-33/` contains no `w1/` path.
- These sections cite them anyway:
  - sitemap-orphan-audit.md:220 ("reports under `.ufo/waves/round-33/w1/`") and lines 222-253
  - SKILL.md:935, 941, 944
  - SCORECARD.md:1131-1163
  - README.md:307, where "sitemap-to-tree parity" rests only on `ExecSitemapTreeParity.md`
- Round 32 committed its wave-1 reports by its measured-results commit (`96d49d6`, also `e9283ec`). Rounds 30, 31 and 32 have 35, 17 and 36 tracked w1 files.
- Fixable: commit the 35 reports, or state that they land at closure. Until then, the parity, reference-integrity and anatomy facts in the wave-1 additions section have no in-repo evidence at the claimed revision.

## Not overclaimed (checked)
- The claim's wording "the pin advances" was flagged in wave 1 as a parallel pin. SCORECARD.md:1161-1164 and the entry at lines 245-249 disclose that freshness-pins.json was flagged, not re-pinned, so the wording is disclosed and bounded.
- README.md:307 and PROVINCE.md:140-145 keep the "live serving not observed" limit.

## Not verified
- Whether 7fc6aa2f is still the upstream tip now. I made no network read; ScoutUpstreamHeadNow owns that.
- The contents of the wave-1 seats' own sandboxes. I read their reports only, so the tally above is a lower bound.
- The 1fbdb8ed "97 of 97 mapped" and "21 references" figures. I did not rerun the parity or reference walks.
- The "103 across three GHP rows" figure at sitemap-orphan-audit.md:209.

Tools: none installed or updated.
