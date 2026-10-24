# Round-33 w1 — ScribeEntrySectionDraft (freshness: C2 entry text)

Leaf scribe. Clone at `bc6c4a8d435473f3c30903210be30d9d6e3ef750`; deliverable
`/fast/scratch/hyaku/kake-r33/w1/ScribeEntrySectionDraft/section.md`, sha256
`f134a69a37fef56d997b14374ae39c91cbb7cc1686a3d6dafbc622497cd11469`, 18 lines. Nothing installed or
upgraded; no live fetch of any owned property; no lane file touched except this report; no lane git/jj state.

## Draft — paste at EOF as a REPLACEMENT, never a second copy

At `bc6c4a8` the heading is absent, but the lane working tree holds an in-flight section with the same
heading; the counter's `section()` needs `headingCount == 1`, so a second copy turns c3 false. I did not
read that text as evidence — the numbers below come from the upstream bytes I read myself.

```
## Round-33 ds4cc source pin 7fc6aa2f

Upstream `ds4cc-marketplace` moved one commit past the corpus' pin `1fbdb8ed` (S062): `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, 2026-10-21T17:32:55Z, "magga: Frostbite — Classic & Remastered at /magga/frostbite/".
The commit adds nine files under `magga/frostbite/` — three pages (the hub, `classic/`, `remastered/`), four scripts and two cover images — links all three from one DLC card in `magga/index.html`, adds a README section, and inserts three `<url>` entries at lines 15–17 of the new `sitemap.xml`, between the `magga/v2/` and `magga/enduro/` blocks.
It touches none of the four files S062 retains (`render.yaml`, `apps-sdk/Dockerfile`, `apps-sdk/src/server.ts`, `.dockerignore`), so S062's content statements still describe those files at the new pin; only the pin moves.
Read on 2026-10-22 through a sandbox clone of the public repository (S065); every number below comes from the retained bytes under `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/`, whose blob ids S065 lists.

The count statements earlier in this entry are historical for their dates and commits and are not re-measured here: the 93-loc staged copy (lines 48, 74–76), round-16's decomposition of 103 (78–86), round-23's live observation of 96 locs (135), round-24's snapshot of `1fbdb8ed` (145).
Round-24's 7,614 bytes and SHA-256 `18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d` reproduce exactly from the source blob at `1fbdb8ed`, so that line is confirmed rather than superseded; the live 96-loc observation is a different surface and no order between it and this commit is established, so nothing here reconciles the two.
This commit is a sitemap change, one of the three events the front matter's recheck line names; no workflow or action file is in it.

sitemap-locs: N
canonical https://ds4cc.com/magga/frostbite/: <verdict>
canonical https://ds4cc.com/magga/frostbite/classic/: <verdict>
canonical https://ds4cc.com/magga/frostbite/remastered/: <verdict>

Limits: source-side only. Nothing was fetched from ds4cc.com, so whether this commit is deployed, and what the live sitemap lists today, is not known from this section; each verdict is `scripts/canonical_audit.py`, an offline static check of the page's explicit head `rel=canonical` link, not a search-engine selection, render or redirect observation.
The front matter's `source:` and `verified-at:` lines still name the 2026-09-28 baseline and are not rewritten: this section is an append.
```

Fill `N` → `100` and each `<verdict>` → `clean` (both observed below; the counter re-derives them). Keep
those four lines bare: the counter matches `^sitemap-locs: (\d+)$` and `^canonical <url>: (\S+)$`, one each.

## Commands (exact, with exit codes)

| # | command | exit | observed |
|---|---|---|---|
| 1 | `git clone -q <lane> clone && git -C clone checkout -q bc6c4a8d…` | 0 | clone at declared rev; section absent at it (`grep -c` 0) |
| 2 | `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream log --format='%h\|%ci\|%s' 1fbdb8ed..7fc6aa2f` | 0 | exactly one commit `7fc6aa2f` \| `2026-10-21 17:32:55 +0000` \| `magga: Frostbite — Classic & Remastered at /magga/frostbite/` |
| 3 | `git … diff --name-status 1fbdb8ed 7fc6aa2f` | 0 | 9 `A` under `magga/frostbite/` (3 `index.html`, 4 `*.js`, `covers/classic.png`, `covers/remastered.jpg`), `M magga/README.md`, `M magga/index.html`, `M sitemap.xml`; no `.github/` path |
| 4 | `git show <rev>:sitemap.xml` → `grep -c '<loc>'`, `xmllint`-free XML parse, `sha256sum` | 0 | `1fbdb8ed` 97 locs / 7,614 B / `18c51c45…823e53d`; `7fc6aa2f` 100 locs / 7,810 B / `55cb947f…7006ef`; blob `f6e254a`→`67d8c7a50dc3a3734ce4be97ffa4810e1e257e12` |
| 5 | `git show 7fc6aa2f:sitemap.xml \| grep -n frostbite` | 0 | new locs at new-file lines 15, 16, 17, after the `magga/v2/` block and before `magga/enduro/` |
| 6 | `git … diff --stat 1fbdb8ed 7fc6aa2f -- render.yaml apps-sdk/Dockerfile apps-sdk/src/server.ts .dockerignore` | 0 | empty → the four S062 paths are byte-identical at the new pin |
| 7 | `python3 -B clone/scripts/canonical_audit.py --manifest pages/manifest-{0,1,2}.json` (manifest in pages root, relative `file`) | 0 ×3 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` for hub, `classic/`, `remastered/` |
| 8 | `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev HEAD --repo <scratch>` on a scratch C2 package with the draft filled | 0 | `met 4 of 4`; `headingCount 1`; `rowCells 11`; `sitemapLocs 100`; canonical observed = stated `clean` ×3 |
| 9 | same counter with `N` / `<verdict>` left unfilled | 0 | `met 3 of 4`, `c4_truth false`, `statedLocs []` → placeholders must be filled |

Manifest gotcha, #7: an absolute `file` yields `input_invalid` / `could-not-evaluate` (exit 2); `file` is
resolved against the manifest's directory (the counter already writes it beside the retained root).

## Evidence map (sentence → evidence)

1. One commit past `1fbdb8ed` (S062), subject/time — #2; `corpus/SOURCES.md:70` at `bc6c4a8`.
2. Nine files, three pages/four scripts/two covers — #3 + `git ls-tree -r 7fc6aa2f -- magga/frostbite/` (9 blobs, all 100644).
3. One DLC card links all three — #3; the diff carries `href="./frostbite/classic/"`, `"./frostbite/remastered/"`, `"./frostbite/"` in a single `article.dlc-card`.
4. README section — #3 (`+## Frostbite — bonus cartridge (DLC shelf)` in `magga/README.md`).
5. Locs at lines 15–17 between `magga/v2/` and `magga/enduro/` — #5.
6. Four S062 files untouched — #6.
7. Read 2026-10-22 via sandbox clone, S065 — this report; the S065 row is the L1's to write (dry run only proved `c2_row` on my scratch row).
8. Historical pointers 48, 74–76, 78–86, 135, 145 — read at `bc6c4a8`; each is self-evidencing in the entry.
9. "7,614 bytes and SHA-256 reproduce exactly" — #4 at `1fbdb8ed`, exact match to entry line 145.
10. "no workflow or action file" — #3.
11. Offline-policy wording — `scripts/canonical_audit.py:2-8` docstring.
12. Front matter still names 2026-09-28 — entry lines 1–3 at `bc6c4a8`.

## Not verified / out of scope

- No live `ds4cc.com` request: deploy state and today's live loc count are unknown here; the 96-loc figure
  is quoted only as the entry's own r23 record.
- The brief named round-17/20 corrections; this entry has no round-17 block (`grep -rln 'Round-17' corpus/`
  empty). Used r20 (118–127), r23 (129–141), r24 (143–145), r26/r27.
- The S065 row, the retained-copy commit and any lane-rev counter run are the L1's surfaces. My dry run lived
  only in `/fast/scratch/…/dryrun` (scratch commit `6d88557`); I ran no counter against the lane at any rev.
