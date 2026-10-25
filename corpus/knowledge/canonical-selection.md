source: S262 — https://developers.google.com/search/docs/crawling-indexing/canonicalization — § "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC) — fetched 2026-10-24
verified-at: 2026-10-24
recheck: 180d
ground: canonical selection — the half of the canonical signal the lane's held static preflight explicitly disclaims

# A declared canonical is a hint; Google selects

The lane's held `corpus/knowledge/static-canonical-preflight.md` validates the canonical a
site **declares** and says in its own words that it owns that job and not search-engine
selection. This entry is the other half: what the vendor does with the signals.

Google's own statement of the selection mechanism [S262], quoted from the section "What is
URL canonicalization":

> "indicating a canonical preference is a hint, not a rule."

The page then states what the hint is weighed against [S262] (collapsed-only quote, the
source breaks the sentence across lines):

> "There are a handful of factors that play a role in canonicalization: whether the page is
> served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and
> rel="canonical" link annotations."

and what the outcome is [S262] (collapsed-only quote):

> "Google then chooses the page that, based on the factors (or signals ) the indexing
> process collected, is objectively the most complete and useful for search users, and marks
> it as the canonical."

The page also says plainly [S262] (collapsed-only quote):

> "You can indicate your preference to Google using these techniques, but Google may choose a
> different page as canonical than you do, for various reasons."

## Why duplicates exist at all [S262]

The page lists the variant classes it recognises, each quoted raw from the page:

- "Device variants : for example, a page with both a mobile and a desktop version"
- "Protocol variants : for example, the HTTP and HTTPS versions of a site"
- "Site functions : for example, the results of sorting and filtering functions of a category
  page" (collapsed-only quote)
- "Accidental variants : for example, the demo version of the site is accidentally left
  accessible to crawlers" (collapsed-only quote)

and notes that the choice can follow the searcher rather than the declaration [S262]
(collapsed-only quote):

> "the search result will probably point to the mobile page if the user is on a mobile
> device, even if the desktop page is the canonical"

## Publisher-side consequences

1. **Declaration and selection are two different acts.** A declared canonical can be ignored,
   and a page with no declaration still gets one. Any check that treats the declared value as
   the indexed value is wrong by construction — which is exactly why the held preflight is a
   *preflight* and not a selection claim.
2. **The steering signals are the ones the lane already owns**: HTTPS, redirects, sitemap
   inclusion and the canonical element. The genuinely new ground here is that they are
   *weighed*, not obeyed, and that the outcome is described as "objectively the most complete
   and useful for search users" rather than as a declared preference.
3. **The selection set is the third canonicalization page.** With S021 ("how to specify") and
   S022 ("fix issues") the lane already held two of Google's three canonicalization pages;
   S262 supplies the frame those two assume.

## What this entry does not establish

- It does not establish the selection rule for any other engine. Baidu publishes a different
  account (a quality comparison); that is outside this row's scope.
- It does not establish that a declared canonical **will** be honoured for any particular
  page; only that it is one influence among several, and that the vendor may choose
  otherwise.
- It does not change the held preflight's scope: static validation of the declared value
  remains that entry's job.
- It is not a live measurement: no owned property was fetched, and no engine's selection was
  observed. The page's own revision line ("Last updated 2026-08-20 UTC") was read from the
  retained body this round.
