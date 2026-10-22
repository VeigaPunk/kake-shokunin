# DraftSourcesRowsLog — round 29 SOURCES.md registry rows, Paths line, Search log

Seat: KakeR29.DraftSourcesRowsLog (scribe, freshness axis). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
No lane file was modified by me; no git or jj command ran in the lane. All editing happened in the sandbox
/fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/ on a clone at e58b66c203bed4e38f89afeaa9573d980344ab64.

## What I built

1. Four registry rows S040-S043 for `corpus/SOURCES.md`, cells from `.ufo/waves/round-29/sources/receipts.json`
   and the retained visible texts S040.txt ... S043.txt.
2. One Paths line, `Project-site base paths — S040 → S043 → S041 → S042`, with a one-sentence route.
3. One Search log paragraph: bounded question, where, date, identified 10, opened 9, screened 9, included 9,
   excluded 0 opened candidates, reject count 3, the never-opened candidate, and the counting basis.
4. Recommended lesson Gate quotes, one curly-quoted span per `- S0NN — ` line, each an exact substring of the
   retained text and each 25 words or fewer.
5. One optional one-cell change to S024's `used-by`, as a separate patch so it can be taken or dropped.

## Lane state observed at the end of my run

The L1 landed the registry rows while I worked. I diffed the lane's rows S040-S043 against my sandbox rows
cell by cell: identical in all 11 cells of all four rows, including `status=mined`, `opened=2026-10-22`,
`recheck=90d` and `used-by=corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md`. The lane's Paths
line and Search log paragraph are present, written by the L1 with its own wording and the same counts
(identified 10, opened 9, screened 9, included 9, excluded 0 opened candidates, rejected rows S044-S046, queued
rows S047 and S048). `corpus/knowledge/pages-base-path.md` exists in the lane and cites S040-S043 in its body.

Read-only census on the landed lane file:
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md --today 2026-10-22`
— exit 1, output `W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` (pre-existing, also
on the unmodified clone) and four `E11 S040..S043 missing used-by corpus/lessons/round-29.md` lines.
`corpus/lessons/round-29.md` does not exist in the lane yet; until the lesson seat lands it the lane census
stays at exit 1. The landed entry's base-element sentence names no S024, so the optional S024 change is not
needed for the entry as it stands.

## Deliverables (absolute paths)

- /fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/DRAFT-sources-rows-and-log.md — rows, Paths line,
  Search log paragraph, Gate quotes, optional S024 change. sha256 41cc8b3c4fb2e226952c8f0ee6f3e303d7b3e38be63c90552dac9eef890c219f
- /fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/SOURCES-round29.patch — the four rows, the Paths line
  and the Search log paragraph. sha256 f73d3671e35f0c2d7ac725ab8bb87242536b2f2e95d745079154c96d1f29a5a9
- /fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/SOURCES-round29-S024-usedby.patch — the optional S024
  used-by change alone. sha256 f056d033f009917e2b8e45320c69bb989d8c2568a8a2ff68931a2b6b0b398c56
- /fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/fleet/kake-shokunin/corpus/SOURCES.md — the patched copy
  the checks ran against; rows at lines 49-52, Paths line at line 67, Search log paragraph at line 99.

## The drafted rows

| S040 | GitHub Docs: What is GitHub Pages? — https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages | docs | A | The two GitHub Pages site types and the default location each one is served from | Types of GitHub Pages sites table, the Default site location row; fetched 2026-10-22, the requested URL redirects to https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages | A project site is served at http(s)://<owner>.github.io/<repositoryname> while a user or organization site is served at http(s)://<owner>.github.io, so a root-relative reference written for one kind does not stay inside the other | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
| S041 | Jekyll Docs: GitHub Pages — https://jekyllrb.com/docs/github-pages/ | docs | A | The branch-published project-page URL structure in Jekyll's own GitHub Pages documentation: the project-page subpath, the relative_url template filter, and the gh-pages branch; the page says nothing about absolute_url or about Actions publishing | Project Page URL Structure, Deploying Jekyll to GitHub Pages and its Project Pages paragraph, Running and Testing Locally; Jekyll v4.4.1 docs, fetched 2026-10-22 | A Jekyll project page is published under a subpath of the user pages subdomain such as username.github.io/project unless a custom domain is set, and the documentation writes template URLs through the relative_url filter so they resolve from that subpath | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
| S042 | Jekyll Docs: Liquid filters — https://jekyllrb.com/docs/liquid/filters/ | docs | A | What the relative_url and absolute_url filters prepend, for Jekyll sites served from a subpath | Standard filters table, the Relative URL and Absolute URL rows; Jekyll v4.4.1 docs, fetched 2026-10-22 | relative_url prepends the baseurl config value to a path and is the filter recommended for a site hosted on a subpath of a domain, while absolute_url prepends the url and baseurl values | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
| S043 | Vite Docs: Deploying a Static Site — https://vite.dev/guide/static-deploy.html | docs | A | The build-time base value a Vite site published on GitHub Pages needs; a bundler configuration rule, not a statement about how GitHub Pages serves paths | GitHub Pages section, the Update Vite Config step; Vite v8.3.4 docs, fetched 2026-10-22 | A project site at https://<USERNAME>.github.io/<REPO>/ needs base set to /<REPO>/, while a user site or a custom domain uses base /, which is also the default when base is omitted | mined | 2026-10-22 | 90d | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |

Paths line:
`- Project-site base paths — S040 → S043 → S041 → S042: learn which location each GitHub Pages site kind is served from, then the build-time base a project site needs, then how a Jekyll project page is published under a subpath, then the filters that prepend that base to a path.`

Search log paragraph (verbatim in the deliverable file): bounded question; where (four primary pages opened by
GET and retained, plus six secondary candidates); date 2026-10-22; identified 10, screened 9, included 9,
excluded 0 registry candidates, reject count 3; one Stack Overflow candidate never opened because it answered
a 403 bot challenge; counting basis; stop rationale.

Gate quotes (one curly-quoted span each, exact substrings of the retained texts, word counts in brackets):
S040 “Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>” [10];
S041 “the output will become available under a subpath of your user pages subdomain, such as username.github.io/project (unless a custom domain is specified)” [22];
S042 “Prepend baseurl config value to the input to convert a URL path into a relative URL.” [16];
S043 “If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .” [19].
The S040 quote contains angle brackets; put the backticks outside the curly quotes so the quoted span stays exact.

## Commands run, with exit codes

All ran inside the sandbox clone, with the clone root as the working directory, except the last item.

1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone` — exit 0; HEAD e58b66c203bed4e38f89afeaa9573d980344ab64.
2. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <sandbox>/fleet <sandbox>/fleet/kake-shokunin`
   — exit 1 on the first run, printing eight `E11 ... missing used-by corpus/knowledge/pages-base-path.md` and
   `corpus/lessons/round-29.md` lines for S040-S043, plus the pre-existing `W04 S033 duplicate url`. Cause:
   the two used-by files did not exist in the sandbox copy at that moment.
3. The same command after creating stub `corpus/knowledge/pages-base-path.md` and `corpus/lessons/round-29.md`
   in the sandbox copy — exit 0, output only `W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`
   and `kake-shokunin ok <path>`. The W04 line is present on the unmodified clone too, so it is not mine.
4. The same command after adding the Paths line and the Search log paragraph — exit 0, same two lines.
5. Frozen census commands from the CORPUS.md contract on the patched copy — all exit 0: rows `43`; malformed
   rows `0`; tier histogram `A=41 C=2`; status histogram `mined=39 queued=2 rejected=2`; duplicate ids printed
   nothing; the enum and tier-inflation check printed nothing.
6. Cell-count check, the acceptance criterion: `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {print NF-2, $2}' corpus/SOURCES.md | awk '$1!=11 {print "BADCELLS", $0}'`
   — exit 0 with no output: every registry row, including S040-S043, has exactly 11 cells.
7. Counter parity check in python against the row parsing of `.ufo/waves/round-29/c1_quote_truth.py`: for each
   of S040-S043 the split gives 11 cells, cells[7] = `mined`, cells[8] = `2026-10-22`, and the receipt `url`
   string is inside cells[1]. All four pass those three conditions.
8. Quote truth check in python: every quoted span listed above was collapsed the way the counter collapses and
   tested with `in` against the collapsed retained text. All true, all within 25 words.
9. `git apply --check` on fresh clones: main patch exit 0, optional S024 patch exit 0, both applied in sequence
   on one clone exit 0. Against the lane as it now stands the main patch no longer applies (exit 1), because
   the L1 already landed the same rows.
10. Read-only census on the landed lane file — exit 1 with the four remaining E11 findings above.

## Findings for the L1

- **The lesson file is the last E11.** `corpus/lessons/round-29.md` does not exist yet; four E11 findings
  remain and the lane census exits 1 until the lesson seat lands it. The entry side is already satisfied.
- **Optional S024 used-by change.** The landed entry's base-element sentence names no S024 row, so the patch
  is not needed as the entry stands. If the entry later cites S024, apply
  /fast/scratch/hyaku/kake-r29/w1/DraftSourcesRowsLog/SOURCES-round29-S024-usedby.patch and log the change
  old to new in the round lesson.
- **S040 redirect.** The requested URL `.../about-github-pages` redirects to `.../what-is-github-pages`; the
  receipt records both. The row keeps the requested URL in the source cell because the C1 counter requires the
  receipt url string there, and records the final URL in the anchor cell. The page title is "What is GitHub Pages?".
- **recheck cadence.** I used `90d` on all four rows as the assignment specified. The S042 and S043 source
  seats proposed `on-release` because the Jekyll page carries no per-page date and the Vite page carries a
  version marker (v8.3.4) whose sample workflow pins action SHAs. The census accepts either.
- **S041 scope.** The source seat warns that the Jekyll page mentions `absolute_url` zero times and covers
  branch publishing only. The S041 scope cell says both, so no reader can extend it to Actions publishing.

## Not verified

- I did not run the C1 counter `c1_quote_truth.py`; it needs a commit containing the rows, the entry and the
  lesson, and the lesson does not exist yet. Items 7 and 8 replicate its two row-level conditions. I did not
  open any URL. Every claim here comes from the retained texts and receipts committed at e58b66c. No install
  was performed and no tooling was needed.
