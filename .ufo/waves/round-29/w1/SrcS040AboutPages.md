# SrcS040AboutPages — S040 (GitHub Docs, About/What is GitHub Pages?) base-path extraction

Seat: `KakeR29.SrcS040AboutPages` (leaf scribe, read-only). Axis named: **freshness**.
Scope: only what the S040 page says about user/organization sites versus project sites, the default site location of each, custom domains, and publishing sources.

No product-code edit, no registry edit, no commit, no install, no build/test. No tracked lane file other than this report was written.

## Target and retained bytes

| field | value |
|---|---|
| source id | S040 |
| requested URL | `https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages` |
| final URL after redirect | `https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages` (page h1: "What is GitHub Pages?") |
| retained text | `.ufo/waves/round-29/sources/S040.txt`, 3268 bytes, 1 line, 528 words |
| retained text sha256 | `625f2b0783a129d2492669d1761329b6b3a5262455aa314dc6900b9143d56eab` |
| receipt (`sources/receipts.json`) | status 200, accessed 2026-10-22T10:29:37Z, bodyBytes 94214, bodySha256 `fac40d86c4907bee0119443a19a1cab9e8e786f63b723518e7dd667a5547fbda`, textSha256 `625f2b07…` |

## Freshness re-open (one public GET, no browser, no headless tool)

```
curl -sS -L --max-time 60 -o live-S040.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  -A 'Mozilla/5.0 (X11; Linux x86_64) kake-source-check' \
  'https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages'
exit=0
http_code=200 size=94214 url=https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
```

```
sha256sum live-S040.html                      -> fac40d86c4907bee0119443a19a1cab9e8e786f63b723518e7dd667a5547fbda
sha256sum .ufo/waves/round-29/sources/S040.txt -> 625f2b0783a129d2492669d1761329b6b3a5262455aa314dc6900b9143d56eab
python3 -B live_text.py   (strip script/style, comments, tags; unescape; collapse whitespace; compare)
exit=0
live extracted words 528 / retained words 528 / identical to retained: True
```

**Today's live body is byte-identical to the retained body** (same 94214 bytes, same body sha256 as the receipt), and the live derived visible text is byte-identical to the retained text string. No drift since the round's fetch. The page carries no visible "last updated" stamp, so freshness rests on the identical-byte re-open; the receipt `accessedUtc` is 2026-10-22T10:29:37Z.

Sandbox copies: `/fast/scratch/hyaku/kake-r29/w1/SrcS040AboutPages/live-S040.html`, `verify_final.py`.

## Statements and verified quotes

Check command (run in the sandbox, exit 0):

```
python3 -B verify_final.py
```

It reads the retained file, collapses whitespace with `re.sub(r"\s+"," ",…)`, and for each quote prints the substring test against the collapsed text, against the raw file bytes, the word count, and the counter's own flip-letter control (first letter flipped to `q` must NOT occur). Result: `ALL PASS: True` for all six; every quote is ≤25 words and the flip control is clean for every one.

**S1 — The page names two kinds of GitHub Pages site: one bound to a user or organization account, one bound to a specific project.**
Quote (14 words): `Sites associated with a user or organization account, and sites for a specific project.`
Also true: `There are two types of GitHub Pages sites.` (8 words).

**S2 — A user or organization site's files must live in a repository named `<owner>.github.io`.**
Quote (18 words): `Must be stored in a repository named <owner>.github.io , where <owner> is the personal or organization account name`

**S3 — A project site's files live in a folder inside the repository that holds the project code.**
Quote (12 words): `Stored in a folder within the repository that contains the project's code`

**S4 — The default site location differs by kind: `<owner>.github.io` for the user/organization site, `<owner>.github.io/<repositoryname>` for the project site.**
Quote (10 words): `Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>`
The live HTML table confirms the column mapping the flattened text loses: header `Property | User and organization sites | Project sites`; row `Default site location | http(s)://<owner>.github.io | http(s)://<owner>.github.io/<repositoryname>`. This is the frontier row: a project site is served one path segment below the owner domain.

**S5 — A site may be hosted on GitHub's `github.io` domain or on a custom domain.**
Quote (14 words): `You can host your site on GitHub's github.io domain or your own custom domain.`

**S6 — Publishing is from a repository; a build step is optional.**
Quote (21 words): `GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub`
Companion verified quote (12 words), usable outside the single-quote gate line: `optionally runs the files through a build process, and publishes a website.`
Limits row, also verified: `Maximum of one pages site per account` (7 words) and `Maximum of one pages site per repository` (7 words).

## Proposed SOURCES row (11 cells)

```
| S040 | GitHub Docs: What is GitHub Pages? (About GitHub Pages) — https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages | docs | A | GitHub Pages site types, where each kind of site's files live, and the default served location of each kind | Types of GitHub Pages sites section: the two-types sentence, the Source files, Limits and Default site location table rows, and the Hosting on your own custom domain subsection; opened 2026-10-22 | A user or organization site is served at <owner>.github.io from a repository named <owner>.github.io, while a project site is served at <owner>.github.io/<repositoryname> from a folder inside the project repository | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
```

Sent to `KakeR29.DraftSourcesRowsLog` (row drafter) as well.

## Findings and cautions for the L1

1. **Gate-line shape.** The C1 counter takes the line starting `- S040 — ` inside the `## Gate` section of `corpus/lessons/round-29.md`, requires exactly one curly-quoted span in it, and requires that span to be an exact substring of the collapsed retained text. Suggest the S4 quote for that line; the other five quotes belong in `corpus/knowledge/pages-base-path.md`.
2. **Angle brackets.** The S4 quote contains `<owner>` and `<repositoryname>`. In markdown a renderer may swallow them as a tag. Put the curly-quoted span inside a code span with the backticks outside the quotes: `` `“Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>”` `` — the quoted text itself stays byte-exact.
3. **Spacing artifact.** The retained text shows `http(s):/ /` and `<owner>.github.io ,` because tag stripping left a space. Any quote must reproduce that spacing exactly; do not "repair" it to `http(s)://`.
4. **Scope limit — publishing sources.** S040 does not define publishing-source modes (branch versus GitHub Actions workflow); it only says Pages publishes from a repository, optionally through a build process, and links to "Configuring a publishing source for your GitHub Pages site" under Further reading. Publishing-mode claims stay with the existing row S003. Do not let the S040 row carry a publishing-source teaching.
5. **Scope limit — custom domain.** S040 names custom domains as an option and points to the configuration page; it does not describe CNAME handling or Actions-published CNAME behaviour (existing rows S005 and S017 cover that). The S040 teaches cell above stays on site kinds and default locations.
6. **Overlap.** S006 (About GitHub Pages and Jekyll) covers the Jekyll build side; S040 covers the site-kind and location side. They are disjoint and both may be cited.
7. **Redirect.** The requested URL redirects to `what-is-github-pages`. The receipt records `url` as the requested address and `finalUrl` as the redirect target. The registry source cell must contain the requested URL string verbatim, because the counter compares it against the receipt `url`.
8. Freshness note: the page is a living doc with no revision stamp; today's re-open proves no change today, not stability going forward. The 90-day recheck cell matches the other 2026-10-22 docs rows.

## Out of scope, not done

- No registry, knowledge, or lesson file was edited; the S040 row and the six statements are proposals for the L1.
- No live probe of any owned web property; no browser; no headless tool; no bot challenge touched. The C1 counter was not run against a revision (the row is not landed, so it would report 0/4 for S040 regardless); I did not create a commit.
- S041, S042, S043 were not opened by me; S042 and S043 have their own seats.
- Tooling: no install was needed. Python 3 and curl only, both already present; no pacman transaction, no service restart.

Report: .ufo/waves/round-29/w1/SrcS040AboutPages.md
