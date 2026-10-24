# ReopenS040 — attack seat: S040 row + pages-base-path.md S040 lines (kake r29 w2)

Item attacked: corpus/SOURCES.md row S040 (line 48) and every S040-citing line of
corpus/knowledge/pages-base-path.md (lines 1, 2, 19, 20, 27, 31, 46, 48), against one
fresh public GET of the declared URL on 2026-10-22. Bytes read at commit
7697990cbca20291f3b0367b8ff4220e93b38b03 via sandbox clone
/fast/scratch/hyaku/kake-r29/w2/ReopenS040/clone (HEAD verified = 7697990). No tool
installs needed; curl + python3 stdlib only. No pacman transactions.

## Commands and observed outputs

1. `curl -sL -o about-pages-live.html -w '...' 'https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages'` → exit 0;
   `HTTP 200 | final_url=https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages | bytes=94214 | type=text/html; charset=utf-8`.
   The declared URL redirects to the renamed page, exactly as the row's anchor cell discloses.
2. `sha256sum clone/.ufo/waves/round-29/sources/S040.txt` → exit 0;
   `625f2b0783a129d2492669d1761329b6b3a5262455aa314dc6900b9143d56eab` — matches the
   declared prefix in pages-base-path.md:2 and the C1 claim.
3. Independent visible-text extraction of my live HTML (script/style removed, entities
   decoded, whitespace collapsed — same rule as receipts.json textRule), diffed against
   retained S040.txt: whitespace-normalized equality, both 3266 chars, zero differences.
4. `gzip -dc clone/.ufo/waves/round-29/sources/S040.html.gz` vs my live HTML: byte-identical
   (True). Receipts.json S040: status 200, bodyBytes 94214 (== my curl size_download),
   finalUrl = the what-is-github-pages redirect target, accessedUtc 2026-10-22T10:29:37Z.
5. Page title tag: `<title data-next-head="">What is GitHub Pages? - GitHub Docs</title>`
   — matches the row's source-cell name "GitHub Docs: What is GitHub Pages?".

Freshness is genuine, not counter-shaped: the retained text and even the saved raw bytes
are what docs.github.com serves today.

## SOURCES row S040 cells (corpus/SOURCES.md:48)

- source/kind/tier "docs | A": title and kind match the live page; tier-A per header rule
  ("scoped to the row's stated topic") is defensible for official vendor docs. OK.
- anchor: "Types of GitHub Pages sites table, the Default site location row; fetched
  2026-10-22, the requested URL redirects to ...what-is-github-pages" — redirect
  reproduced verbatim by my GET. Table and row exist on the live page. OK as far as it
  goes; see F1 for what it omits.
- teaches, first half: "A project site is served from http(s)://<owner>.github.io/<repositoryname>
  while a user or organization site is served from http(s)://<owner>.github.io" — both cells
  verified in raw HTML (`<code>http(s):/<wbr/>/<wbr/>&lt;owner&gt;.github.io</code>` and the
  `/<wbr/>&lt;repositoryname&gt;` variant) in the Default site location row. OK.
- teaches, second half: "so a root-relative reference written for one leaves the other" —
  not page content; the page contains no statement about references or base paths. See F2.
- status/opened/recheck/used-by (mined, 2026-10-22, 90d, pages-base-path.md +
  lessons/round-29.md): consistent with receipts and entry header. OK.

## Per-line verdicts, pages-base-path.md

- :1 (source header) — supported. Declared URL resolves today, HTTP 200 via the disclosed
  redirect to "what-is-github-pages"; page title matches the row name.
- :2 (verified-at, S040 part) — supported. "all four opened this round with one public GET
  each, HTTP 200" (13 words): S040 hash recomputed identical; my GET returned 200 with the
  same body size and final URL as the receipt. The GET-count itself is process, not provable.
- :19 (two quotes) — supported. "a static site hosting service that takes HTML, CSS, and
  JavaScript files straight from a repository on GitHub" (16 words) and "There are two types
  of GitHub Pages sites..." both verbatim in live and retained text. Caveat: the first
  quote's topic sits outside the row's declared scope; see F1.
- :20 (Default site location) — supported. "http(s)://<owner>.github.io/ <repositoryname>"
  with "(the retained text collapses that cell's spacing)" — accurate and honestly
  disclosed: the collapse comes from `<wbr/>` splits inside `<code>` cells; the rendered
  cells match the claimed locations, user/org site is the host alone in the same row.
- :27 (collective "None of S040–S043 discusses the base element") — supported for the S040
  half: no "base element", "<base", "baseurl" or "base path" anywhere in retained or live
  S040 text. (S041–S043 halves are sibling seats' scope.)
- :31 (build process) — supported. "optionally runs the files through a build process" (8
  words) verbatim in live text ("...straight from a repository on GitHub, optionally runs
  the files through a build process, and publishes a website."). Scope caveat: F1.
- :46 (custom domain sentence) — supported. "You can host your site on GitHub's github.io
  domain or your own custom domain." (15 words) verbatim, under heading "Hosting on your
  own custom domain". Scope caveat: F1.
- :48 ("S040 itself states only that a custom domain is possible") — supported. The page's
  custom-domain content is that one sentence plus links; it says nothing about project-site
  paths or base paths under a custom domain.

(Line :3 names the counter, not a citation — excluded.)

## Findings

- F1 (low, registry hygiene, not a freshness break): the S040 scope cell — "The two GitHub
  Pages site types and the default location each one is served from" — and the anchor cell
  under-declare what the entry trusts S040 for. Three of five S040 citation topics come from
  the page's intro paragraph ("static site hosting service..." :19, "optionally runs ... build
  process" :31) and the "Hosting on your own custom domain" section (:46), none named in
  scope or anchor. Sibling row S041 (same batch, same day) enumerates scope exhaustively,
  including absence claims, so lane convention supports widening S040's cells to name the
  intro paragraph and the custom-domain section. All the extra content is verbatim on the
  page (verified today), so widening the cells is the fix; nothing needs retraction.
- F2 (minor, wording): the teaches cell appends "so a root-relative reference written for one
  leaves the other" — a lane consequence the page does not state. The two location halves of
  the cell are verbatim-supported; the derivation should be marked as inference or moved to
  the entry, which already carries it as a cited claim.

## Verdict

Item holds. Retained S040.txt is the live page's visible text (normalized-equal; saved raw
HTML byte-identical to today's fetch); the row's redirect disclosure reproduces exactly; all
eight S040-citing entry lines are supported as quoted, with :20's spacing artifact disclosed
in-line. Two low/minor registry findings (F1 scope/anchor under-declaration, F2 teaches
synthesis clause) — neither breaks freshness, quote truth, or any cited claim.

Residual / not verified: the "one public GET each" count in :2 is receipt-consistent
(accessedUtc 2026-10-22T10:29:37Z) but not independently provable; the redirect's status
code (301 vs 302) was not captured (single GET with -L, final URL only); S041–S043 halves of
line :27 and the lessons file's S040 usage were out of my assignment's Change.
