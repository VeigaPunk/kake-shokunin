# Scout — are S062's four retained render files still current at 7fc6aa2f?

Seat: KakeR33.ScoutRenderFilesStillCurrent (leaf, freshness axis; r33-build).
Question: do `render.yaml`, `apps-sdk/Dockerfile`, `apps-sdk/src/server.ts`, `.dockerignore`
(S062, retained at `.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/`) differ between upstream
`1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` and `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`?

## Verdict (observed)

No. All four files are byte-identical at both commits and byte-identical to the retained copies.

| file | blob @ 1fbdb8ed | blob @ 7fc6aa2f | retained-copy blob (lane rev bc6c4a8) | equal |
|---|---|---|---|---|
| `render.yaml` (mode 100644) | `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` | `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` | `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` | yes |
| `apps-sdk/Dockerfile` (100644) | `ee0b63819a9ce71e51469796541b9075e9676ae9` | `ee0b63819a9ce71e51469796541b9075e9676ae9` | `ee0b63819a9ce71e51469796541b9075e9676ae9` | yes |
| `apps-sdk/src/server.ts` (100644) | `649726dfcd4bead92195992ed23e03dacd2d23ba` | `649726dfcd4bead92195992ed23e03dacd2d23ba` | `649726dfcd4bead92195992ed23e03dacd2d23ba` | yes |
| `.dockerignore` (100644) | `d650445a62b723cb8331eb0159756d3cbfacc502` | `d650445a62b723cb8331eb0159756d3cbfacc502` | `d650445a62b723cb8331eb0159756d3cbfacc502` | yes |

Blob-id equality is byte equality (SHA-1 of `blob <len>\0<content>`), so no per-line diff is needed.
Mode and path are unchanged too: no rename, delete or mode change for any of the four paths.

## Commands run (exit codes)

Upstream clone `/fast/scratch/hyaku/kake-r33/ds4cc-upstream` (L1's read-only clone;
`origin https://github.com/VeigaPunk/ds4cc-marketplace.git`, non-bare, both commits present
as `commit` via `git cat-file -t`). `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset; git 2.56.0.

1. `git ls-tree -r 1fbdb8ed… | grep -E "render\.yaml|apps-sdk/Dockerfile|apps-sdk/src/server\.ts|dockerignore"`
   → the five rows above (the extra hit is `marketplace/plugins/spoderman/autoagent-weaver/.dockerignore`,
   blob `e00fae7f…`, also unchanged). exit 0.
2. `git ls-tree -r 7fc6aa2f… | grep …` → identical rows for all four targets. exit 0.
3. `git diff --stat 1fbdb8ed 7fc6aa2f -- render.yaml apps-sdk/Dockerfile apps-sdk/src/server.ts .dockerignore`
   → empty output. exit 0. `git diff --name-only … | wc -l` → `0`.
4. `git diff --name-status 1fbdb8ed 7fc6aa2f` → 12 paths, all `magga/**` (README.md, index.html,
   frostbite/ tree: 8 files + 2 covers) plus `M sitemap.xml`. No `D` or `R` anywhere; 3734 insertions,
   0 deletions.
5. `git merge-base --is-ancestor 1fbdb8ed 7fc6aa2f` → exit 0 (ancestor=yes);
   `git rev-list --count 1fbdb8ed..7fc6aa2f` → `1` (exactly one commit, as C2 declares).
   `git log -1 7fc6aa2f` → `2026-10-21 17:32:55 +0000 magga: Frostbite — Classic & Remastered at /magga/frostbite/`.
6. Lane side, at declared rev `bc6c4a8d435473f3c30903210be30d9d6e3ef750`:
   `git ls-tree -r bc6c4a8 -- .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/` → the four blobs in the
   "retained-copy" column, modes 100644, all tracked.
   `git cat-file blob bc6c4a8:<path> | git hash-object --stdin` per file → the same four ids.
7. Cross-check `git hash-object -- <retained path>` on the lane working tree (informational only,
   not landed-state evidence) → the same four ids, so the working tree copy did not diverge either.
8. Control on the new commit: `git show 7fc6aa2f:sitemap.xml | grep -c "<loc>"` → `100`, vs `97` at
   `1fbdb8ed` (+3, matching the C2 declaration). `git ls-tree -r --name-only 7fc6aa2f | grep -i render|docker`
   → still exactly `render.yaml`, `apps-sdk/Dockerfile`, `.dockerignore` at the paths S062 names
   (other hits are plugin-internal `src/render/*.ts` and weaver `Dockerfile*` copies, untouched here).

## render-web-services.md — does it need a change?

Not for content: every sentence in `corpus/knowledge/render-web-services.md` that cites S062 or the
`1fbdb8ed` blobs (`:50-67`, `:82-93`, `:97-101`) remains true at 7fc6aa2f, so no factual edit and no
new append-only correction is required. At most a one-line convenience edit: the existing drift-check
paragraph (`:102-108`) already records "the remote `main` is `7fc6aa2`, one commit ahead … touches only
`magga/**` and `sitemap.xml` (not re-checked by the L1)"; that hedge can now read "re-checked per-file:
all four blob ids equal at 7fc6aa2f (round-33 seat ScoutRenderFilesStillCurrent)". Optional, freshness
only — the entry is not stale without it.

## Unknowns / limits

- I did not fetch from github.com; I used the L1's clone whose `origin` is the named public repo and
  whose two commits resolve locally. Whether that clone matches github's `main` at scout time rests on
  the L1's fetch, not on my own GET. (Blob ids are content addresses, so any other clone of the same
  repo yielding these ids would agree.)
- Not verified: the live Render service, its dashboard settings, and whether `7fc6aa2f` is still the
  remote tip. Nothing about the deployed service was observed.
- No live request to any operator-owned property; no tool installs or updates were made.
- The extra `.dockerignore` at `marketplace/plugins/spoderman/autoagent-weaver/` is not in S062's scope
  and was only noted as unchanged, not analysed.
