# SrcS041JekyllPages — S041 source extraction (round 29, wave 1)

Seat: KakeR29.SrcS041JekyllPages (leaf scribe). Axis: freshness. No subagents, no installs, no network fetch, no lane mutation; the only lane file I wrote is this report. Sandbox: `/fast/scratch/hyaku/kake-r29/w1/SrcS041JekyllPages/`.

## Axes

- freshness (primary): does the retained S041 text still support a base-path statement, with quotes that are true substrings.
- operability (secondary): does the page give an actionable way to keep template URLs correct under a project-site subpath (the `relative_url` filter plus an empty-baseurl local preview).

## Source identity

- URL `https://jekyllrb.com/docs/github-pages/`; receipt: HTTP 200, `accessedUtc` 2026-10-22T10:29:37Z (`.ufo/waves/round-29/sources/receipts.json`).
- Retained text `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/sources/S041.txt`, sha256 `86a77ee24f7e01d56cc3de44d0bc07b37d68e00713f694b027611bd4527f4969` (equals `receipts.json` `textSha256`), 5551 bytes, 876 words, 2 lines; all page prose sits on line 1, so offsets below are char offsets on line 1.
- Version marker: the docs nav shows `v4.4.1` (offset 98); the footer shows `© 2026`. I did **not** re-fetch the URL (this seat was not told to open it), so live-page state is unverified.

## Statements (5) with checked quotes

**St1 — GitHub serves project pages with a subdirectory-like URL structure, and that structure is what breaks naive URL resolution; the published output lands under a subpath of the owner subdomain such as `username.github.io/project`.**
- Q1 (15 words, offset 1765): "The subdirectory-like URL structure GitHub uses for Project Pages complicates the proper resolution of URLs."
- Q6 (22 words, offset 3569): "the output will become available under a subpath of your user pages subdomain, such as username.github.io/project (unless a custom domain is specified)."

**St2 — The page says to route template URLs through its URL filters, showing `relative_url` on a static asset name and on a page URL that can change.**
- Q11 (14 words, offset 1874): "In order to assure your site builds properly, use the handy URL filters :"
- Q3 (9 words, offset 1989): `<link href=" {{ 'assets/css/style.css' | relative_url }} " rel="stylesheet">`
- Q4 (15 words, offset 2120): `[ {{ page . title }} ](" {{ page . url | relative_url }} ")`

**St3 — With those filters applied you can preview the site from its root on localhost, and the same URLs resolve when GitHub builds from the `gh-pages` branch you would push.**
- Q5 (24 words, offset 2180): "This way you can preview your site locally from the site root on localhost, but when GitHub generates your pages from the gh-pages branch"
- Q2 (16 words, offset 1669): "Sometimes it’s nice to preview your Jekyll site before you push your gh-pages branch to GitHub."

**St4 — The project site's content lives in a specially named `gh-pages` branch (or a `docs` folder on master) of the project repository, not in a separate pages-only repository.**
- Q7 (20 words, offset 3413): "the website content is stored in a specially named gh-pages branch or in a docs folder on the master branch"

**St5 — To preview locally against the production-level settings you serve with an empty baseurl; the server then runs on `http://localhost:4000`.**
- Q10 (16 words, offset 4618): "it’s quite hard to switch back and forth with the local settings and the production-level settings"
- Q8 (7 words, offset 4792): `bundle exec jekyll serve --baseurl = ""`
- Q9 (14 words, offset 4832): "This will run the jekyll server on your local machine i.e. on http://localhost:4000 ."

## Proposed S041 registry row (11 cells, tested)

`| S041 | Jekyll Docs: GitHub Pages — https://jekyllrb.com/docs/github-pages/ | docs | A | GitHub Pages URL structure and the Jekyll preview workflow on the branch-published path: project-page subpath, the relative_url template filter, baseurl local preview, and the gh-pages branch; the page is silent on absolute_url and on Actions publishing | Project Page URL Structure, Deploying Jekyll to GitHub Pages and its Project Pages paragraph, Running and Testing Locally; Jekyll docs version marker v4.4.1; fetched 2026-10-22 | Project pages are published under a subpath of the owner subdomain such as username.github.io/project, template URLs stay correct under that subpath when the relative_url filter is used, the site content sits in a gh-pages branch, and jekyll serve with an empty baseurl previews the site locally on http://localhost:4000 | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |`

Recommended Gate line for `corpus/lessons/round-29.md` (must start `- S041 — ` and carry exactly one curly-quoted span; Q1 shown with straight quotes here, curly in the file):

`- S041 — https://jekyllrb.com/docs/github-pages/ — accessed 2026-10-22, section Project Page URL Structure: "The subdirectory-like URL structure GitHub uses for Project Pages complicates the proper resolution of URLs."`

## Verification actually run

1. `python3 -B /fast/scratch/hyaku/kake-r29/w1/SrcS041JekyllPages/check_quotes.py` → **EXIT 0**, `RESULT: PASS`: 11 quotes (Q1–Q11 above) each an exact substring of the raw file and of the whitespace-collapsed text, each 1–25 words, and the counter's letter-flip control string absent for every quote. Script: `/fast/scratch/hyaku/kake-r29/w1/SrcS041JekyllPages/check_quotes.py`.
2. Counter simulation on a sandbox clone (`git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r29/w1/SrcS041JekyllPages/clone`, HEAD e58b66c2) where I added only my S041 row plus a stub entry and stub lesson: `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 9cde172168119763e751bf19ffa21f66b38902b7` → counter exit 1 overall (S040/S042/S043 rows absent by design) with **S041 `passed: true`** and `a_row`, `b_entry_body_cites`, `c_gate_quote`, `d_quote_in_retained_text` all true, `controlBroken: false`. Same S041 result with the Q6 gate quote at revision 5cf379320b25f7bab10e75d18998734a887a754d.
3. Negative control: changing one word in the Gate quote (`subpath` → `sub-path`) at the next sandbox commit makes `d_quote_in_retained_text` false and S041 fail — the check is not vacuous. Weaker control noted: dropping only the trailing full stop still passes, because the counter matches substrings.

## Limits, conflicts, not verified

- `absolute_url` occurs **0 times** in S041.txt (only `relative_url`, 2 times). This page must not be cited for `absolute_url`; S042 covers that filter. `baseurl` occurs once, only as the `--baseurl` CLI flag — the page does not define a `baseurl` configuration key or `site.baseurl` semantics.
- The page describes classic branch publishing (`gh-pages` branch, or a `docs` folder on master) and never mentions Actions or artifact publishing; keep the scope cell's "branch-published path" wording so the row is not read as a claim about current Pages defaults.
- The retained text is a whitespace-collapsed rendering of the HTML, so the code-sample quotes (Q3, Q4) contain the extraction's inserted spaces. They are exact substrings of the retained file, but they are not literal HTML.
- Not verified by me: the live page as of today (no fetch authorized for this seat), the L1's final entry text and Gate line, the S040/S042/S043 rows, and the counter run at the landed lane commit.
- Freshness risk for the recheck column: the Jekyll docs site version marker is v4.4.1 and the page's `gh-pages` wording may change when the docs are refreshed; 90d with the version marker in the anchor cell is the conservative choice.

## Tooling record

No installs or upgrades were made or needed (operator rule: none expected; `python3`, `git`, `grep` were already present). All writes stayed in `/fast/scratch/hyaku/kake-r29/w1/SrcS041JekyllPages/` except this report in the lane.
