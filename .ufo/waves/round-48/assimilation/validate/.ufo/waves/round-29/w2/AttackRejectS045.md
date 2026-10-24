# AttackRejectS045 — falsify the S045 rejection (jekyll/jekyll issue 332)

Seat: KakeR29.AttackRejectS045 (leaf critic, axis freshness). Attacked bytes at lane commit
7697990cbca20291f3b0367b8ff4220e93b38b03, in sandbox clone
/fast/scratch/hyaku/kake-r29/w2/AttackRejectS045/clone (TMPDIR inside the sandbox). No network
access, no installs, no lane mutation apart from this report.

## Item attacked
- `corpus/SOURCES.md:53`: the S045 row, rejected, with flip condition.
- `corpus/lessons/round-29.md:52`: the S045 lesson line and its single quote.
- Retained text `.ufo/waves/round-29/sources/screened/C3.txt` (one line) and its receipt.

## Commands (all exit 0)
1. `git clone -q <lane> clone && git -C clone checkout -q 7697990c…`, then `rev-parse HEAD` → 7697990cbca2….
2. `sha256sum screened/C3.txt` → 040620b6a2ccf00e3fd170f9d3eed2f140c15ba73ab8b1c4425902ccb38c7d0c. This matches `receipts.json` C3.textSha256.
3. `zcat screened/C3.html.gz | sha256sum`; `| wc -c` → e17cf2ce91f19aa5…eb12, 458345 bytes. This matches bodySha256 and bodyBytes.
4. A python3 check extracted the quote from round-29.md:52 and searched C3.txt for it. Result: substring True, count 1. Token counts in C3.txt: `user-name.github.com` 4, `base-url` 9, `baseurl` 14, `relative_url` 1, `github.io` 0, `29 remaining items` 1, `locked` 1.
5. grep for host and key names in S040–S043.txt: `github.io` appears 4/4/0/2 times, `*.github.com` Pages hosts 0, `baseurl` 0/1/4/0, `base-url` 0.
6. rg over corpus/ and SKILL.md for any statement that the github.com Pages host was retired or moved: no match outside the S045 row and lesson line themselves.

## Observed
- The quote is located and exact: “If you're not using a CNAME and hosting your Project Page on GitHub Pages it's served out of a "project-name" subfolder”. The text right after it is `http://user-name.github.com/project-name`.
- The issue body uses the old host and the `base-url` key: “The workaround I can think of for this is setting a "base-url:" in the _config.yml then put that in front of all href , src , url paths” and “e.g. <a href="{{ site.base-url }}/blog">blog</a>”.
- A 2013 maintainer comment (parkr, Member) is now contradicted by S042: “baseurl … doesn't interact with any of the links in your Jekyll source, nor is that configuration added to the site variable in Jekyll.” S042 says: “Prepend baseurl config value to the input to convert a URL path into a relative URL.”
- The thread is not only about `base-url`. It also uses `{{ site.baseurl }}` (halfninja 2011, andrewspiers 2011). Its last visible comment (whoisjorge 2017) gives the current fix: “<a href="{{ "/sitemap" | relative_url }}">sitemap</a>”. The thread was locked on 2017-08-26.
- “29 remaining items” are collapsed behind “Load more” and are not in the retained bytes.

## Verdict
**The rejection holds, with two defects to fix.**

The rejection is justified. The issue body and the 2013 maintainer reply describe a host (`user-name.github.com`) and a key (`base-url`) that no current primary source in this round uses. S040 gives the current location as `<owner>.github.io/<repositoryname>`, and S042 gives `baseurl` plus `relative_url`. The 2013 maintainer statement is directly superseded by S042. The flip condition is checkable.

Defect 1 (freshness): the quote does not show why the row was rejected. The kept sentence says a project page is served from a project-name subfolder, and that is still true today (S040, S041). The quote shows neither the old host nor the `base-url` key. Wave 1 had a second quote, `http://user-name.github.com/project-name` (`.ufo/waves/round-29/w1/ScreenRejectCandidates.md:50-51`), but it was dropped from round-29.md:52.

Defect 2: “retired host” is not grounded. No lane source says the github.com Pages host was retired. S040 shows only what the current host is, so the retirement is [INFERENCE]. The row's reason also says “the thread reasons about” `base-url`. That is too broad: the visible thread also uses `baseurl` and ends on `relative_url`.

Smallest safe correction (an edit to the lesson and row text only; status stays rejected):
- Lesson line 52: add the stale span as a second exact quote, either “http://user-name.github.com/project-name” or “<a href="{{ site.base-url }}/blog">blog</a>”. The parkr 2013 sentence above is optional extra support.
- Row and lesson: say “a host no current primary source uses (S040 lists `<owner>.github.io`)” instead of “retired host”. Alternatively, keep “retired” and add a source that documents the retirement.
- Row reason: say “the issue body and the 2013 maintainer reply” instead of “the thread”. The thread's later replies reach `baseurl` and `relative_url`, which S041 and S042 already cover, so the rejection is unchanged.

Impacted axis: freshness (how fully the rejection is evidenced). Operability is not affected.

## Not verified
- I did not open the live page, because this seat had no network grant. The judgment rests only on the retained bytes.
- I did not read the 29 collapsed thread items. They may hold maintainer guidance.
- I did not confirm when or whether github.com Pages hosts were retired.
- I did not check whether Liquid resolves `site.base-url` as a custom key.
