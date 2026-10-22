# R29 w1 — SrcS043ViteDeploy

Scope: extract only the GitHub Pages part of the Vite static-deploy guide (source S043)
for the round-29 project-site base-path claim. No product code, corpus entry, lesson or
registry file was written by this seat.

## Source and receipt

- URL: https://vite.dev/guide/static-deploy.html (final URL identical, HTTP 200)
- Retained visible text: `.ufo/waves/round-29/sources/S043.txt`, 13360 bytes, 2164 words,
  sha256 `d665dd23b193b0a416e9d2e9b15e65e30b5644e5b513a9c834c0c2535b52dcba`, equal to
  `receipts.json` `S043.textSha256` (recomputed and compared).
- Receipt: accessed 2026-10-22T10:29:37Z, body sha256 `be274bde…302b4b80`, bodyBytes 93983.
- The GitHub Pages section is the text between `GitHub Pages ` and
  `GitLab Pages and GitLab CI `, 2457 characters.

## Freshness re-check (my own GET, same extraction rule)

Re-fetch of https://vite.dev/guide/static-deploy.html into
`/fast/scratch/hyaku/kake-r29/w1/SrcS043ViteDeploy/refetch/` (body + visible text):
HTTP 200 at 2026-10-22T10:33:28Z, bodyBytes 93983,
bodySha256 `be274bde3c2b6b0932e92f09e044d9dc7f24682ff443aef4a7bfc399302b4b80`,
textSha256 `d665dd23b193b0a416e9d2e9b15e65e30b5644e5b513a9c834c0c2535b52dcba`,
`full_text_equal: True`, `ghp_section_equal: True` (2457 = 2457 characters). The retained
text is therefore the current live text; nothing drifted since the L1 opening. Page version
marker in the retained nav: `v8.3.4` (1 occurrence).

## Statements (5) with re-checked quotes

Each quote was checked by script as an exact substring of the retained file, of the
whitespace-collapsed retained text, and of the GitHub Pages segment, with at most 25 words,
and with the counter's flip-letter control holding (the flipped quote is not a substring).
All checks passed.

S1. A user site (`https://<USERNAME>.github.io/`) or a custom domain through GitHub Pages is built with `base` set to `/` (23 words):
> If you are deploying to https://<USERNAME>.github.io/ , or to a custom domain through GitHub Pages (eg. www.example.com ), set base to '/' .

S2. `base` may simply be left out because it defaults to `/` (14 words):
> Alternatively, you can remove base from the configuration, as it defaults to '/' .

S3. A project site served from `https://<USERNAME>.github.io/<REPO>/` is built with `base` set to `/<REPO>/`, because the site lives under the repository path (19 words):
> If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .

S4. The publishing source is GitHub Actions and deployment runs through a GitHub Actions workflow, which the guide calls necessary because Vite needs a build step (14 and 23 words):
> Under Build and deployment , open the Source dropdown, and select GitHub Actions .

> GitHub will now deploy your site using a GitHub Actions workflow , which is necessary since Vite requires a build step for deployment.

S5. The workflow lives at `.github/workflows/deploy.yml` in the repository (10 words):
> Create a new file in your repository at .github/workflows/deploy.yml .

Supporting short quotes also verified: `Set the correct base in vite.config.js .` (7), `In your repository, go to Settings → Pages .` (9), headings `Update Vite Config`, `Enable GitHub Pages`.

## Proposed S043 row for `corpus/SOURCES.md`

Eleven-cell pipe row in the existing shape (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by). It satisfies the C1 counter checks `cells[7] == "mined"`, `cells[8] == "2026-10-22"`, and `url in cells[1]`.

```
| S043 | Vite: Deploying a Static Site — https://vite.dev/guide/static-deploy.html | docs | A | Build-time `base` value for a Vite site published on GitHub Pages; a Vite configuration rule, not a statement about how GitHub Pages serves paths | GitHub Pages section: Update Vite Config and Enable GitHub Pages steps; Vite docs v8.3.4, opened 2026-10-22, text sha256 d665dd23…52dcba | A project site at https://<USERNAME>.github.io/<REPO>/ needs base '/<REPO>/', while a user site or custom domain uses base '/', which is also the default when base is omitted | mined | 2026-10-22 | on-release | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
```

Recheck cadence suggestion: `on-release` rather than `90d`, because the page is versioned by the Vite documentation release (`v8.3.4` in the nav) and its sample workflow pins action commit SHAs (checkout v7, setup-node v7, configure-pages v6, upload-pages-artifact v5, deploy-pages v5) that move with each documentation update.

## Recommended gate line for the lesson

The C1 counter accepts exactly one curly-quoted span in the single `- S043 — ` line of the lesson `## Gate` section, and that span must be a substring of the retained text. Suggested line (one quote only, 19 words, verified substring):

```
- S043 — https://vite.dev/guide/static-deploy.html — accessed 2026-10-22, section GitHub Pages: “If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your repository is at https://github.com/<USERNAME>/<REPO> ), then set base to '/<REPO>/' .”
```

Only one bullet in the whole Gate section may start with `- S043 — `; the remaining quotes
can go in a backtick table like round-28 used, which the counter does not read.

## Out of scope and limits

- Not verified: how GitHub Pages itself serves a project site, and whether any owned property is affected. The page is a build-tool instruction only; the serving-side claim rests on the other three sources.
- The GitLab Pages section repeats the same base pattern for GitLab; outside this seat's scope, and no quote from it is offered. Quotes S1 to S5 were confirmed to lie inside the GitHub Pages segment only.
- No corpus, lesson, registry or product file was modified by this seat.

## Evidence pointers

- `.ufo/waves/round-29/sources/S043.txt` (retained visible text, sha256 d665dd23…52dcba), `.ufo/waves/round-29/sources/receipts.json` (S043 receipt)
- `/fast/scratch/hyaku/kake-r29/w1/SrcS043ViteDeploy/check_quotes.py` and `cands.json` (quote checker; `verify_out.txt` holds its output)
- `/fast/scratch/hyaku/kake-r29/w1/SrcS043ViteDeploy/refetch/S043.txt` and `refetch_out.txt` (freshness re-fetch and comparison)
- No tool was installed or upgraded; the host pacman channel is paused and no install was needed, so the tooling directive had nothing to record.
