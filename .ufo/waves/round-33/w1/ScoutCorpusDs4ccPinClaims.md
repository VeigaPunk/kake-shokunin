# Freshness inventory — corpus/SKILL statements at the ds4cc 1fbdb8ed → 7fc6aa2f move

Seat: KakeR33.ScoutCorpusDs4ccPinClaims (leaf, advisory evidence only). Inventory read at lane rev
`bc6c4a8d435473f3c30903210be30d9d6e3ef750` in a sandbox clone; the lane working tree was mid-edit by
the L1 and was not used as evidence except where labelled "in-flight".

## Established numbers (observed, `git cat-file`/`git show` on `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`)

| commit | `<loc>` count | sitemap.xml bytes | sha256 |
|---|---|---|---|
| `6e888784` (magga: Enduro) | 96 | — | — |
| `1fbdb8ed` | **97** | 7,614 | `18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d` |
| `7fc6aa2f` | **100** | 7,810 | `55cb947fa2d07f4a39f709b102f0133c94eb351501ec0b6d2263746f487006ef` |

`95dbeb69` is what added the 97th loc (`+<url><loc>https://ds4cc.com/gkeep/…`); `1fbdb8ed` did not touch
sitemap.xml (diff empty, exit 1). `7fc6aa2f` adds exactly three: `/magga/frostbite/`, `/classic/`, `/remastered/`.
Diff `1fbdb8ed..7fc6aa2f` = 12 files: 11 under `magga/` (3 `index.html`, 4 scripts, 2 covers, `magga/index.html`,
`magga/README.md`) + `sitemap.xml`; `magga/` tree entries 1,516 → 1,525. All four S062 blobs are byte-identical at
both commits (`render.yaml d17ab7e5`, `apps-sdk/Dockerfile ee0b6381`, `apps-sdk/src/server.ts 649726df`,
`.dockerignore d650445a`).
Local clone (read-only `git show`): HEAD `1fbdb8ed`, sitemap 97 locs / sha `18c51c45…`; `7fc6aa2f` is not an
object locally — so "one commit behind" is literally true.

## Inventory

| path:line | quoted claim (≤20 words) | status at 7fc6aa2f | correction if stale |
|---|---|---|---|
| `corpus/knowledge/sitemap-orphan-audit.md:145` | "byte-identical to checkout HEAD 1fbdb8ed: 7,614 bytes, SHA256 18c51c45…, 97 parsed loc elements" | **unaffected** (explicit pin; re-measured exact) | add qualifier: upstream `7fc6aa2f` is 100 locs / 7,810 B / `55cb947f…` |
| `corpus/knowledge/sitemap-orphan-audit.md:48-49` | "ds4cc.com/sitemap.xml → 404 live but exists at local HEAD (93 locs, unpushed)" | **stale** twice over: 404 falsified by its own c3 (live 200), 93 is the 2026-09-28 count | "live 200 since 2026-10-21 (c3); 1fbdb8ed staged 97 locs, upstream 7fc6aa2f 100" |
| `corpus/knowledge/sitemap-orphan-audit.md:70,74-76` | "staged `sitemap.xml` … 93"; "all 93 listed paths already serve 200" | **unaffected** as dated baseline; the *property* no longer holds | "pre-push preview held at 93 locs; the 3 frostbite locs of 7fc6aa2f are not yet served" |
| `corpus/README.md:28,62`; `SKILL.md:229`; `drift-detection.md:87-89`; `sitemap-orphan-audit.md:17` | "103 locs live-side / 102 source-side" (93 ds4cc + 8 + 2) | **unaffected** (dated r16 baseline) | optional: re-derivation today is 106 live / 109 source (see below, inference) |
| `corpus/knowledge/kimi-subpath-audit.md:24` | "ds4cc.com's `sitemap.xml` (93 locs) is the should-serve set" | **stale** — present tense, no date; denominator is now 100 | "the should-serve set is 100 locs at `7fc6aa2f` (97 at `1fbdb8ed`, 93 at `f3d2ecd`)" |
| `corpus/knowledge/kimi-subpath-audit.md:1-3` | "parity (93 locs; sitemap commit f3d2ecd)"; recheck "expect 93" | **unaffected** — the command reads `f3d2ecd`, not HEAD | none (c5 already notes that `f3d2ecd` now 404s upstream) |
| `corpus/knowledge/kimi-subpath-audit.md:30,44-46` | "93 canonical locs → 19 served, 74 missing"; "f3d2ecd adds 75 (18→93)" | **unaffected** (historical commit arithmetic) | none |
| `kimi-subpath-audit.md:96-97`; `sitemap-orphan-audit.md:135` | "live ds4cc.com sitemap contains 96 `<loc>` entries" | **unaffected** by the commit; **needs qualifier** — 96 is a deploy vintage | "96 = the `6e888784` deploy (lacks `/gkeep/`); source is 100 at `7fc6aa2f`" |
| `corpus/README.md:29`; `SKILL.md:230`; `free-read-verbs.md:215,465` | "75/93 canonical locs missing" | **needs qualifier** — ratio is 75-of-93, not of the current set | "75/93 at the 2026-09-28 baseline; source now 100, live canonical 96" |
| `corpus/knowledge/publish-queue.md:26` | PQ-2 "75 missing canonical paths (sitemap f3d2ecd: 18→93 locs)" | **needs qualifier** — ledger row is live readiness, denominator moved | "at 7fc6aa2f the source set is 100; unfired mirror delta grows by 4 (gkeep + 3 frostbite)" |
| `corpus/knowledge/publish-queue.md:92-96` | "`sitemap.xml` and `/robots.txt` are live 404"; "93-loc canonical URL list is working-tree-only, never on the wire" | **stale**, but not by this commit (its own c6 says live 200) | "live 200 since 2026-10-21 (c6); the wire list was then the 97-loc `1fbdb8ed` tree" |
| `corpus/knowledge/render-web-services.md:4-5,50,52,83-100` | "The lane's render.yaml at ds4cc-marketplace 1fbdb8ed" | **unaffected** (explicit commit pins; four blobs unchanged upstream) | none |
| `corpus/knowledge/render-web-services.md:103-106` | "remote `main` is `7fc6aa2`, one commit ahead … touches only `magga/**` and `sitemap.xml`" | **correct** — verified: 12 files, 11 under `magga/`, plus `sitemap.xml` | none |
| `corpus/SOURCES.md:70` (S062) | "render.yaml, apps-sdk/Dockerfile, apps-sdk/src/server.ts and .dockerignore at commit 1fbdb8ed" | **unaffected** — retention still valid at the new head | none |
| `corpus/SOURCES.md:73` (S065, **in-flight**, absent at bc6c4a8) | "the local clone ~/Projects/ds4cc-marketplace is one commit behind, at 1fbdb8ed" | **correct now**, but a relative claim | keep it paired with the absolute `7fc6aa2f` hash; refresh if upstream moves |
| 52 sidecar notes "checkout 1fbdb8ed" — `SKILL.md` ×10, `freshness-sidecar.json` ×26, `fleet-registry.md` ×5, `speedrun-pipeline.md` ×4, `origin-repos.md` ×3, `mirror-pitfalls.md`, `publish-channels.md`, `lessons/round-18.md`, `lessons/round-24.md` | "2026-10-21: … present (test -e exit 0; checkout 1fbdb8ed)" | **unaffected** — dated observations, still literally true | none |

## Adjacent, not caused by 7fc6aa2f (already stale on 2026-10-21 evidence)

- `corpus/knowledge/freshness-pins.json:36` `"sitemapStatus": 404` + `scripts/freshness-sweep.mjs:86` +
  `freshness-sweep.md:62` (armed A4: "`sitemapStatus` 404 → `200` → `LISTED-LIVE`"). Live is 200 per
  `sitemap-orphan-audit.md:135` and `publish-queue.md` c6, so this armed pin should already be reporting
  `LISTED-LIVE`; a source commit does not change it. Not repaired here (leaf bounds).

## Derived arithmetic [INFERENCE], for the L1 to use or discard

- Live-side today: 96 (ds4cc live) + 8 (plazir live) + 2 (charter live, r16 value, not re-measured) = **106**;
  source-side: 100 + 7 + 2 = **109**. The 103/102 decomposition changed shape, not just magnitude: ds4cc is now
  counted from live where r16 counted the staged copy.
- Live 96 matches `6e888784`'s count exactly while `95dbeb69` added `/gkeep/`; the r23 "96 entries" observation is
  therefore most likely the pre-`gkeep` deploy vintage, i.e. two pushes behind `1fbdb8ed` and four entries behind
  `7fc6aa2f`. Live-set identity was not checked (no live requests permitted to owned hosts).
- If no kimi mirror path changed, the PQ-2 delta grows from 77-of-96 to **81-of-100** missing (adds `/gkeep/` and the
  three frostbite locs). Every added path post-dates the ~Aug-29 mirror vintage, so the class stays "stale, 0 rot".

## Verification performed (all in sandbox; no tools installed or updated)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && git -C clone checkout -q bc6c4a8d…` → exit 0,
  HEAD `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
- `git grep -n '1fbdb8ed' -- corpus SKILL.md` at that rev; `git grep -c 'checkout 1fbdb8ed'` → 52 occurrences in
  9 files; `git grep -nE '\b(93|97|96|100|102|103)\b…(locs?|<loc>)'` for the count sweep.
- `git cat-file -p <rev>:sitemap.xml | grep -c '<loc>'` on 4 commits (96/97/97/100); `git cat-file -s` +
  `sha256sum` on two; `git diff --name-only 1fbdb8ed 7fc6aa2f`; `git rev-parse <rev>:<file>` on the four S062 files.
- Read-only `git show -s --format='%H %cI %s' HEAD` and `git show HEAD:sitemap.xml` in `~/Projects/ds4cc-marketplace`
  (no fetch, no write).

## Not verified

- No live request to any ds4cc host; the live 96-loc set, its identity with `6e888784`, and the 19/77 kimi split are
  taken from the corpus's 2026-10-21 corrections, not re-observed.
- The in-flight S065 row and the working-tree "Round-33 ds4cc source pin" section (absent at bc6c4a8) were read only to
  cross-check numbers; I make no statement about their landed form.
- Plazir/charter loc counts are the r16 values, not re-measured.
