# ReviewS062Row — re-open S062 and check every cell

Seat: KakeR32.ReviewS062Row. Axis: freshness. Scope: the S062 registry row in
`corpus/SOURCES.md:70`, verified against `~/Projects/ds4cc-marketplace` (git
read-only) and the retained copies. No cell found wrong.

## Commands run (all read-only on the external clone)

- `git -C ~/Projects/ds4cc-marketplace rev-parse 1fbdb8ed` →
  `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (exit 0).
- `git ... log -1 --format='%H %ci %s' 1fbdb8ed` → same hash, dated
  2026-10-21 05:51:24 -0300.
- `git ... ls-tree 1fbdb8ed render.yaml apps-sdk/Dockerfile` →
  `blob d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252 render.yaml`,
  `blob ee0b63819a9ce71e51469796541b9075e9676ae9 apps-sdk/Dockerfile`.
- `git ... cat-file -p 1fbdb8ed:render.yaml` and `...:apps-sdk/Dockerfile`
  written to sandbox tmp; `cmp` vs retained copies → both exit 0
  (byte-identical). `wc -l -c`: render.yaml 20 lines / 565 B;
  apps-sdk/Dockerfile 17 lines / 380 B.
- Extra: `ls-tree` + `cat-file` + `cmp` for `apps-sdk/src/server.ts`
  (blob 649726dfcd4bead92195992ed23e03dacd2d23ba) and `.dockerignore`
  (d650445a62b723cb8331eb0159756d3cbfacc502) → both cmp exit 0.
- `git ... remote -v` → `origin https://github.com/VeigaPunk/ds4cc-marketplace.git`.

## Per-cell verdict (corpus/SOURCES.md:70)

- id S062 — present, unique. Accurate.
- source — URL embeds the full commit hash `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`;
  rev-parse confirms; remote path `VeigaPunk/ds4cc-marketplace` confirmed;
  "local clone ~/Projects/ds4cc-marketplace" exists and was read;
  "retained byte-identical" claim verified by cmp (exit 0). Accurate.
- kind `code`, tier `A` — operator-owned repo files at a pinned commit;
  consistent with registry convention for own/primary code rows (cf. S009). Accurate.
- scope — "content of the operator's own Blueprint file and Dockerfile at one
  commit, read offline; not a statement about the live Render service…":
  the re-open confirms content exists at that commit; the negative scope is
  appropriately bounded. Accurate.
- anchor — commit hash verified; both blob ids verified by ls-tree;
  "(20 lines)" for render.yaml verified by `wc -l` (20, trailing newline);
  "opened 2026-10-22 with git cat-file" reproduced this same way today. Accurate.
- teaches — "one Docker web service with dockerContext . , healthCheckPath
  /health and OPENAI_APPS_CHALLENGE as sync: false": render.yaml has exactly
  one service entry (`type: web`, `runtime: docker`), `dockerContext: .` (line 6),
  `healthCheckPath: /health` (line 7), and OPENAI_APPS_CHALLENGE with
  `sync: false` (lines 15-16). Accurate.
- status `mined`, opened `2026-10-22`, recheck `90d` — consistent with the
  row being opened and cited today; 90d matches the registry's fetched-doc
  convention and the round-32 census change at lane tip 285abcad. Accurate.
- used-by `corpus/knowledge/render-web-services.md` — file exists and cites
  S062 at lines 82, 88, 97. Accurate.

## Adjacent observation (not a row defect)

`corpus/knowledge/render-web-services.md:97` cites S062 for four retained
files while the S062 scope names only two (render.yaml, Dockerfile). The extra
two (`apps-sdk/src/server.ts`, `.dockerignore`) do exist at 1fbdb8ed and their
retained copies are byte-identical (cmp exit 0), so the citation is factually
supported but exceeds the row's stated scope. Advisory only.

## Not verified / evidence

- Did not fetch the github.com URL (owned-property/URL fetch not needed;
  commit object verified locally).
- Extracted blobs: `/fast/scratch/hyaku/kake-r32/w1/ReviewS062Row/tmp/{render.yaml,Dockerfile,server.ts,dockerignore}`.
- No tools installed this round.
