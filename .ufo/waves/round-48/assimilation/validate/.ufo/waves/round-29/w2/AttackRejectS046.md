# Round 29 wave 2 — AttackRejectS046

Seat: KakeR29.AttackRejectS046 (leaf critic, freshness). Target: the rejected registry row S046 (Jekyll Talk thread "Relative URL and BaseURL", candidate C5) at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/AttackRejectS046/ (clone checked out at 7697990, TMPDIR inside the sandbox). No network, no installs, no lane mutation apart from this report.

## Verdict

- Quote located: **holds**. It appears exactly once in the retained text, and the check script passes.
- Rejection outcome (status `rejected`, tier C): **holds**. The thread never discusses a GitHub Pages project site, and its one current fact is already carried by S041 and S042.
- Stated reasons and flip clause: **broken in part**. Two of the four stated grounds are not in the bytes, and the flip condition is already met by the round's own admitted sources.

## Commands (all in the sandbox clone at 7697990)

1. `git clone -q <lane> clone && git -C clone checkout -q 7697990…`: exit 0.
2. `sha256sum .ufo/waves/round-29/sources/screened/C5.txt`: dd0cd1f1…63463b85, which matches receipts.json C5 textSha256. `zcat C5.html.gz | sha256sum`: 526cc1c4…cc76064, which matches bodySha256. Both have exit 0.
3. `cmp sources/screened/C5.txt verification/reject-path/cand/C5.txt`: exit 0 (identical).
4. Python substring count of the lesson quote in C5.txt: count 1, offset 2867.
5. `python3 -B .ufo/waves/round-29/verification/reject-path/reject_path_check.py --registry corpus/SOURCES.md --lesson corpus/lessons/round-29.md --entry corpus/knowledge/pages-base-path.md --screened-dir .ufo/waves/round-29/sources/screened --primary-dir .ufo/waves/round-29/sources --out <sandbox>/check.json`: exit 0. S046 shows `passed: true, problems: []`.
6. Keyword counts in C5.txt: "Gitlab" 2, "gitlab" 1, "netlify" 1, "localhost" 3, "GitHub" 0, "gh-pages" 1 (only in a related-topic title), "v4.0.0" 1, "Jekyll v3.x" 1, "jekyll serve" 0.
7. Post positions in the raw HTML: 1–9 and 11–13. Post 10 is missing from the retained bytes.

## Findings, checked against the S046 row (corpus/SOURCES.md:54) and the lesson line (corpus/lessons/round-29.md:53)

1. **Scope to GitLab Pages and localhost: holds.** Post 1: "I have deployed a site on gitlab pages … But when I deployed the same on netlify it works." Post 6: "Instead of having your site served at http://localhost:4000/ , you'll have it served at http://localhost:4000/blog/". Post 11: "I don't have a github site yet, just doing everything locally". The thread never mentions GitHub Pages ("GitHub" count 0).
   Two small wording problems. The thread never says "jekyll serve"; that is an inference from localhost:4000. The row also leaves out Netlify.
2. **"predates the Jekyll 4.0 link and post_url tag change": broken as written.** The thread runs to 2020-05, and post 13 (ijv, May 23 2020) states the change itself: "In v4.0.0 post_url tag now incorporates the relative_url filter within itself and therefore automatically prepends site's baseurl". Only the core answer (post 6, ashmaroli, 2018-08-14) predates 4.0.
   The 4.0 claim is not grounded in any retained primary source: neither S041.txt nor S042.txt contains "post_url" (S042 mentions "4.0" only for the where filters), and corpus/knowledge/pages-base-path.md has no 4.0 or post_url line. [INFERENCE] Jekyll 4.0.0 shipped in August 2019; I did not open a source for that date.
3. **"repeats Jekyll 3.x baseurl SCSS advice": broken.** Post 13 asks whether to remove the old variable: "What should I do in main.scss file with $baseurl variable? Remove it? (in Jekyll v3.x was $baseurl: "{{ site.baseurl }}"; )". Nobody repeats that as advice, and the question has no reply in the retained bytes.
4. **"Posts by ashmaroli and rdyar, 2018-08 to 2020-05": imprecise.** rdyar's only post is dated September 28 2019. The 2020-05 post is by ijv, and mmistakes and ginfuru also answered.
5. **The flip condition is already met (strongest counterexample).** The flip reads "a current primary source confirms the thread's guidance". The thread's guidance (post 6) is to use `{{ 'css/style.css' | relative_url }}` instead of prepending `site.baseurl`. Two of the round's own Jekyll v4.4.1 primary sources already say this:
   - S042.txt offset ~794: "Relative URL Prepend baseurl config value to the input to convert a URL path into a relative URL. This is recommended for a site that is hosted on a subpath of a domain."
   - S041.txt offset ~2030: "use the handy URL filters : … {{ 'assets/css/style.css' | relative_url }}".
   Read literally, the clause would flip the row today. So the guidance is current, not stale, and "pre-4.0 advice" is not a valid ground.
6. **The quote itself: located and accurate to the thread.** Post 6 (ashmaroli, 2018-08-14) reads "relative_url ensures proper links by: ensuring the url to have a single leading slash always ensuring there are no unnecessary slashes." The lesson quote is the first clause, an exact substring at offset 2867.
   Not verified: whether the current relative_url really removes repeated slashes for a value like '/blog// '. [INFERENCE] From memory of the Jekyll source, it strips only one trailing slash from baseurl and passes absolute inputs through unchanged. I did not read Jekyll source, so this is unverified.

7. **Peer input (AttackQueuedS047S048, 11:17Z), confirmed.** Registry row S016 (corpus/SOURCES.md:24, pages.github.com/versions.json, fetched 2026-10-19) says "At fetch time the dataset lists Jekyll 3.10.0". That row is `queued`, not mined.
   If GitHub Pages branch builds run Jekyll 3.10, the 3.x behaviour the thread describes, where post_url does not prepend baseurl, is what applies to them. So "predates 4.0" does not count against the thread for a GitHub Pages question, and the version split is one more reason to drop that clause.
   One reading supports it: for a 3.x build, post 11's `{{ site.baseurl }}{% post_url … %}` is the working form. The scope ground is unaffected.

## Impacted axes

- Freshness: the row says the thread is stale, but its bytes and S041/S042 show the core guidance is current. The flip clause is already satisfied, so the row's `rejected` status rests on scope and redundancy alone.
- Operability: none. The check script passes; it tests the quote, `REJECTED:`, `flip:` and status, not whether the stated reasons are true.

## Smallest safe correction

Rewrite the S046 teaches cell in corpus/SOURCES.md:54 and its copies (verification/reject-path/reg.md, and the mut/ fixtures that carry the row).

- Drop "predates the Jekyll 4.0 link and post_url tag change, and repeats Jekyll 3.x baseurl SCSS advice".
- Keep the scope ground: GitLab Pages, Netlify and localhost, with no GitHub Pages project site.
- Keep "the relative_url fact it states is already carried by S041 and S042".
- Replace the flip with a condition not yet met, for example: "flip: the thread gains a GitHub Pages project-site answer that S041 and S042 do not already carry".
- Optionally fix the authors cell to "mmistakes, ginfuru, ashmaroli, rdyar, ijv".

The lesson line at round-29.md:53 can stay as is; it is accurate apart from the inferred "jekyll serve".

## Side observation (outside my item, not investigated)

check.json reports `"rejectedRowsInRegistry": 5`, but only S044–S046 are rejected; S047 and S048 are queued. The counter's label does not match what it counts.

## Not verified

I fetched no live page, so post 10's content and any edits made after 10:34:14Z are unknown. I did not read Jekyll source or changelog, so the 4.0 release date and the current relative_url slash behaviour are unverified. Installs: none.
