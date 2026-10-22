# AttackRejectS044 — round 29 wave 2 (falsify), axis: freshness

Item attacked: rejected row S044 (Made Mistakes, "Jekyll's site.url and baseurl", Jul 19, 2021).
Bytes read at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03 in sandbox clone
`/fast/scratch/hyaku/kake-r29/w2/AttackRejectS044/clone` (SOURCES.md blob 855fa29, lessons/round-29.md blob 5f6b383).
Retained text C1.txt sha256 9e49199d…dae6e; C1.html.gz sha256 cbd5e09a…48ff. No network, no installs.

## Commands (all exit 0)
- `git clone -q … && git checkout -q 7697990…` — exit 0.
- Exact-substring check of 10 quotes against C1.txt (python3 inline) — all True, counts below.
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990…` — exit 0, `C1 4/4` (S044 is not part of that counter).
- `rg -c -i 'localhost:4000|JEKYLL_ENV|github-metadata|jekyll-github-metadata' corpus` — 0 files.

## Stated reason 1: stale version claim — HOLDS
- Quote is exact (1 hit): "GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locked at 3.9.0".
- S016 contradicts it: `corpus/lessons/round-20.md:218` records `"jekyll": "3.10.0"`; retained bytes `.ufo/waves/round-26/fetched/text/S016-1.txt` contain `"jekyll":"3.10.0"`.
- Second staleness point, also exact (4 hits): "4.2 (✨latest)"; S041/S042 retained text is from Jekyll "v4.4.1" docs.
- Caveat: S016 is status `queued` (SOURCES.md:24), not `mined`; it is tier A with bytes on disk, so it suffices as the contradicting source.

## Stated reason 2: raw baseurl concatenation — WEAK (preference, not a falsehood)
- Page: "This can be done by prefixing all links with {{ site.url }}{{ site.baseurl }} or by apply Jekyll's absolute_url or relative_url filters to them." and "The best option is the one that works for you!" So it does treat them as equals.
- But every concatenation example it marks ✅ yields the correct output (`/blog/about.html`, `/blog/images/pizza.jpg`), and the author says "Personally I tend to lean on the relative_url and absolute_url filters".
- S042 only *recommends* relative_url (knowledge/pages-base-path.md:33). The lane's own rule at :32 forbids "hard-coded paths", and `{{ site.baseurl }}` is not a hard-coded path. On its own, this reason is a style tradeoff, not a defect.

## Counterexample: a stronger current-bytes defect that the row does not cite
The page's own HTML (not an extraction artifact: the chroma `<span class=nt>` keys in C1.html.gz) tells readers to set:
- `_config.yml`: "website : https://mmistakes.github.io" and "basewebsite : /blog" (C1.txt, 1 hit each), plus "website: https://mademistakes.com" in the trailing-slash table.
- The author comment says "GitHub would automatically add basewebsite: /blog".
Meanwhile the prose and Liquid use `url`/`baseurl`. S042 says the filters prepend the "baseurl config value" (pages-base-path.md:33). [INFERENCE, not run] A reader who copies this config gets an empty `site.baseurl`, so every link loses `/blog`, which is the very breakage the page sets out to prevent. That makes the page unsafe to copy *today*, whatever its date.

## Is the flip condition checkable? PARTLY, and it is unsafe
- Branch 1, "a current tier-A source confirms the page's version claims": checkable against versions.json (S016), and currently false. Good.
- Branch 2, "refreshed to current GitHub Pages dependencies and restated in relative_url terms": "restated in relative_url terms" has no test. The page already names relative_url as its preferred option, so a reviewer cannot tell when this is met.
- Counterexample: if the author bumps "3.9.0" to "3.10.0" and "4.2" to "4.4" and leaves `basewebsite`, branch 2 can be argued met and the row flips while the broken config example remains.

## Could the page carry something true the lane lacks? YES, as leads only
Claims on the page that the lane corpus has nothing on (rg count 0):
1. "in older versions of Jekyll (v3.3 through 4.1) it would reset site.url to localhost:4000 when JEKYLL_ENV=development". Pages builds with 3.10.0 (S016), so a local `jekyll serve` build could emit `absolute_url` links to localhost, which is an out-of-base class relevant to `scripts/base_path_audit.py`. Unverified: tier C, no tier-A source opened.
2. "GitHub Pages automatically adds that value based on the repo and type of site" (baseurl set by Pages for project sites). The lane at pages-base-path.md:35 says baseurl must match and a local preview empties it, but not that Pages supplies it. Unverified, and in a comment that uses the broken key.
3. "Double forward slashes e.g., //minima/assets/style.css" is already covered: the audit handles protocol-relative input (`scripts/base_path_audit.py:402`, fixture `D5-protocol-relative-same-host`).
Leads 1 and 2 need tier-A grounding (Jekyll docs or changelog, pages-gem or jekyll-github-metadata docs) before use. They do not argue for admitting S044.

## Verdict: AGREE with the reject; the stated reasons and the flip condition need correcting
- Reason 1 holds with exact quotes and S016 bytes. Reason 2 is a preference, not a falsehood.
- The decisive defect (`website:` / `basewebsite:` config keys) is not cited, and the flip condition would let that defect survive.
- Impacted axes: freshness (stale versions), and operability, because copying the config example breaks subpath links.
- Smallest safe correction (for the L1 to decide): add the `basewebsite : /blog` quote to the SOURCES.md:52 reason and the round-29.md:51 line. Make the flip read: "versions.json-matching versions AND config example uses `url`/`baseurl` keys". Drop or soften the concatenation reason. Optionally queue leads 1 and 2 as questions for a tier-A source.

## Not verified
- No live fetch of the page or versions.json, and no Jekyll build to show that `basewebsite` leaves `site.baseurl` empty.
- Whether 3.9.0 was accurate on 2021-07-19 is unchecked. The site.url-reset version range and the Pages auto-baseurl claim are unchecked against any tier-A source.
- The C2 counter and selftest were not run (out of scope for this item).
