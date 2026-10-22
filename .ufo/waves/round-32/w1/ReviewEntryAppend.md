ReviewEntryAppend — C2 "Retained copies (round 32, append-only)" section review
Scope: appended section at end of corpus/knowledge/render-web-services.md; diff a0b0dff..285abcad; sentence-level check (hash-object values, which sentences still need the external repo).
Tool note: no lsp device exists in this seat's tool inventory; review used git and file reads only (recorded per reviewer protocol). No network requests; no tools installed (pacman paused; none needed). ds4cc-marketplace read via `git show`/`ls-tree`/`rev-parse` only.

Commands run (all exit 0 unless noted):
- `git -C <lane> diff a0b0dff 285abcad -- corpus/knowledge/render-web-services.md` -> 13 insertions(+), 0 deletions; single `+` hunk. Pure addition: PASS.
- `git -C <lane> ls-tree -r 285abcad -- .ufo/waves/round-32/sources/` -> exactly 2 blobs: render.yaml d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252, apps-sdk/Dockerfile ee0b63819a9ce71e51469796541b9075e9676ae9.
- `git -C <lane> hash-object` on both working-tree copies -> same two ids. "byte-identical to the external blobs" VERIFIED.
- `git -C ~/Projects/ds4cc-marketplace rev-parse 1fbdb8ed` -> 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 (matches S062 URL pin).
- `ls-tree -r 1fbdb8ed` in external clone -> render.yaml d17ab7e5…, apps-sdk/Dockerfile ee0b6381… (match), apps-sdk/src/server.ts 649726dfcd4bead92195992ed23e03dacd2d23ba (entry's "649726df…" correct), .dockerignore d650445a62b723cb8331eb0159756d3cbfacc502.
- `git -C <lane> ls-tree -r 285abcad | grep -E '649726df|d650445a'` -> no match (rc=1): neither blob is anywhere in the lane tip tree.
- `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:apps-sdk/src/server.ts` lines 14/193/272 -> `PORT` parse `?? "3000"`, `app.get("/health",…)`, `listen(PORT,"0.0.0.0")`; cited lines correct.
- `git show 1fbdb8ed:.dockerignore` -> starts `*`, re-admits `!apps-sdk/…` and `!marketplace/…`; entry's description accurate.
- `git show 1fbdb8ed:apps-sdk/Dockerfile | grep -c ARG` -> 0 (rc=1, no matches); corrections bullet accurate.
- `git show tip:.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml | wc -l` -> 20 (matches S062 "20 lines").
- `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev 285abcad` -> {"met":3, c1/c2/c3 true, S062 cited 2x}.

FINDINGS (severity order):

1. MEDIUM — The appended final sentence under-lists which sentences still need the external repository. It names only "the sentence about the server's allow list", but the section above has at least four more sentences whose evidence is in files that are NOT retained:
   - healthCheckPath bullet: "The server answers `GET /health` with HTTP 200 (`server.ts:193`…)" — needs server.ts.
   - Port bullet: "the server reads `PORT` with fallback 3000 and listens on host `0.0.0.0` (`server.ts:14`, `server.ts:272`…)" — needs server.ts (repeated in the round-31 corrections bullet citing `server.ts:14`).
   - dockerContext bullet: "The repository's `.dockerignore` starts with `*` and re-admits only `apps-sdk/` sources and `marketplace/`" — needs .dockerignore (blob d650445a…, absent from lane tree); same for the corrections bullet "The lane's `.dockerignore` starts with `*`…".
   - dockerfilePath bullet: "the default would be the root Dockerfile, which this repository does not use" — a tree-level negative needing the external repo.
   A fresh session trusting "only the allow-list sentence still needs the external repository" would wrongly conclude those four sentences are offline-checkable.

2. LOW — Internal inconsistency between S062 and the entry it anchors. SOURCES.md:70 details cell says "also retained: apps-sdk/src/server.ts blob 649726dfcd4bead92195992ed23e03dacd2d23ba, .dockerignore blob d650445a62b723cb8331eb0159756d3cbfacc502", while the row's source cell defines "retained byte-identical at .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/" — a directory holding only two files, and neither blob id appears anywhere in the tip tree. If "retained" means byte-copies (as the same row's own source cell uses the word), the row overstates; the entry's "not retained" is tree-true but contradicts its cited row. "retained" has two meanings across the paired artifacts.

VERIFIED CLEAN: pure-addition diff; both `git hash-object` values in the appended text correct and equal to the upstream blobs; `649726df…` prefix correct; server.ts:14/193/272 and .dockerignore claims accurate in the external clone; S062 cited twice; counter met=3 at tip.

NOT VERIFIED: the live GitHub blob page (no network grant to this seat; the local clone at 1fbdb8ed is the defined offline ground). Sandbox clone not needed — all checks were read-only.
