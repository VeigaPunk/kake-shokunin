# CriticC2Sufficiency — round 34, wave 2 (critic, freshness)

Target: the hollow commit `0cce15f0` scores C2 5/5. Does the landed entry show learning beyond what the counter measures?
Sandbox: /fast/scratch/hyaku/kake-r34/w2/CriticC2Sufficiency/ (clone at 24a1647, hollow bundle fetched to `refs/hollow/heads/hollow-c2`).
Scripts I wrote: `quote_check.py` (every curly quote followed by an Sxxx id, checked as an exact substring of the retained text after whitespace collapse) and `census_detail.py` (per-page recount of `html.tar.xz` with `html.parser`).

## Commands (all run in the sandbox clone; exit codes observed)
1. `python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision 9ef758c` exited 0 and printed `C2 5/5`. The same command with `--revision 0cce15f` also exited 0 and printed `C2 5/5`. Counter sha256 `ee7461b9…f892`.
2. `python3 -B quote_check.py clone 24a1647` gave `quotes=47 missing=0`, exit 0. At `9ef758c` it gave `quotes=45 missing=0`, and at `0cce15f` `quotes=0`. A count of `“` characters after line 8 also gives 47 and 45, so the regex caught every quote.
3. `python3 -B census_detail.py clone/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz` exited 0.
4. `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD refs/heads/main` exited 0. Both refs point to `7fc6aa2fc124…`, checked around 21:23Z.
5. Read-only checks: `git grep` at base `1e54c89` for og:/Open Graph across `corpus`; `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream` show/grep at 7fc6aa2f; greps over the round-23 `live/*/page.html` files.

## Findings
1. **The counter cannot tell the landed entry from the hollow one. The difference is real and I checked it outside the counter.** The hollow entry is 10 lines: `# junk`, seven `filler` lines, the four ids and the copied census line (sha256 `90895bbf…`). The landed entry at 9ef758c is 179 lines (sha256 `336ef643…`), and 222 lines at 24a1647. It has 45 platform quotes (47 at 24a1647), and every one is an exact substring of the retained S067–S070 and S073 text. The counter checks only one Gate quote per id, which is 4 of those 47.
2. **The census prose goes beyond the census line, and it is correct.** My recount reproduces all seven numbers (pages 102; og:title, og:type and og:url 87 each; og:image 1; all-four 1; og:url equals canonical 87). It also confirms every sub-claim the counter never reads:
   - 15 pages have none of og:title, og:type and og:url, and no page has only part of that set. 14 of the 15 have a canonical link; `benchmarks/benxshitter-frontier.html` has none (entry :133-137).
   - `omegag/index.html` is the only page with an image and the only page with all four properties, and its values match the entry (:138-141).
   - All 87 typed pages declare `website`, and no page has two og:type tags.
   - The 15 pages are the 11 under `burnerchrome/` plus `bloat.html`, `burnerchrome.html`, `exa.html` and the benxshitter page (:197-200).
   - No page uses `name="og:…"`.
   - At 7fc6aa2f, `pages.yml` uploads `./ds4cc-marketplace` as it is, and no js/mjs/py/sh/ts/rs file contains a quoted `og:title`, `og:type`, `og:image` or `og:url` string (:196-197).
   - The only raster images that look like a site default are three `logo-512.png` assets outside the site pages (:200-201).
3. **The wave-1 owned-property additions hold.** I spot-checked them against `.ufo/waves/round-23/live/*/{page.html,fetch.json}` (:216-222):
   - The ds4cc kimi.page mirror has og:url `./` and 0 canonical links.
   - The ds4cc.com root has og:title, og:type and og:url but no og:image.
   - The plazir-15 and charter roots have all four properties.
   - The lucario, burnerchrome-kimi, vault-kimi and ufo-fsd kimi.pro roots have none.
   - All snapshots carry a `fetchedAt` of 2026-10-21T06:33Z, which matches "one-day-old captured bytes".
4. **This is new knowledge for the lane.** At base `1e54c89` the corpus mentions og: only as observed data, in `drift-detection.md:80,109`, `publish-queue.md:38,181,270` and `lessons/round-16.md:58`. No entry held the required properties or any platform's crawler or cache behaviour. The parts with frontier value:
   - Facebook caches images by URL (S068).
   - Slack fetches with a Range request, caches globally for about 30 minutes, and ignores robots.txt (S069).
   - Discord takes a tag's key from `name` before `property` (S073).
   - The census shows that 101 of 102 pages have no og:image.
   - The entry turns these into an operator-gated fix plan (:147-159).
5. **Caveat on what is new: the census totals were known before the declaration.** The SCORECARD declaration's "Pre-declaration screening (2)" discloses 87 openings for og:title, og:type and og:url and 1 for og:image. So condition (e) confirms totals that were already known; what this round actually learned is the per-page breakdown in finding 2. This is disclosed, not hidden, and it is not a defect.
6. **Inference labels: 8 `[INFERENCE]` tags, and each one marks a real inference.** Three statements are wrong or overstated, all minor and fixable:
   - **Coverage line 6 claims "Slack's … tag preference".** S069 states no preference: `grep -i prefer S069.txt` exits 1. The body (:85-86) only says which tag families Slack reads. Smallest fix: replace "tag preference" with "tag families".
   - **Line :93-94 says the wrong thing.** "A corrected scrape can persist for about half an hour" should say the earlier cached response persists, so a correction can take about 30 minutes to show.
   - **Line :32-33 turns guidance into fact.** "is not untyped at the consumer" restates S067's "should be treated as og:type website" as a fact about consumers, without a label. Smallest fix: "should be treated as website (S067)".
7. **The ledger understates what the entry grounds.** SCORECARD.md:1276 at 24a1647 says "no opened source requires an absolute og:url". But the entry (:43-46) quotes S067's URL type definition, "All valid URLs that utilize the http:// or https:// protocols". In S067.txt that sentence follows "URL A sequence of Unicode characters that identify an Internet resource." The entry draws a labelled inference that a relative og:url fails that type. The entry's reading is the better-grounded one; the SCORECARD line should cite it as partial grounding rather than say no source exists. This affects calibration only, not the C2 count.
8. **Freshness fit is disclosed honestly, but it is weak.** Wave-1 `CriticDeclarationFit` 5 and `CriticFrontierNovelty` 8 already raised this; I am not reporting it as new. What I add:
   - QUALITY.md:145 says a freshness receipt counts only when at least one claim is decided against a live surface. In C2, that decision happened once, at fetch time: each page got one GET at 20:57Z with HTTP 200, recorded in `receipts.json`. The counter replays the retained bytes only, and the entry says so itself (:3, "cannot see a page change").
   - The census is of a commit, not of a live site. Upstream is still at 7fc6aa2f, so the census is current as of today.
   - The real freshness content: both pages' "Updated" dates are recorded (:165-167), the recheck triggers have a 90-day interval (:3), and S071 is rejected because its URL now redirects (:176-179).
   - My judgment: this fits freshness the same way rounds 29–31 were admitted, and it is not a misstatement. The closure should not give freshness credit for the census.

## Verdict recommendation (advisory): improved, with the C2 counter receipt alone unprovable
- From the counter alone, the result is unprovable: the hollow and landed commits get identical 5/5 receipts (command 1).
- From evidence outside the counter, it is improved. 47 of 47 quotes are exact (finding 1), every census sub-claim recounts (finding 2), the owned-property and workflow claims hold (finding 3), and the knowledge is new to the lane (finding 4).
- The defects in findings 6 and 7 are wording fixes. None of them changes a number or a source.
- The closure should base this verdict on independent checks like commands 2 and 3, not on `c2-at-9ef758c.json`.

## Not verified
- I did not re-fetch any source page; I made no live requests beyond `ls-remote` and touched no owned host. So whether S067–S073 still match their retained text today is unverified.
- I did not check that each quote is read in its source context, beyond the three contexts quoted above.
- I did not review S074–S077 rows or the C1 tool.

No tools were installed or updated.
