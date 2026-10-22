# C2 truth sampling: Dockerfile sentences vs retained bytes (KakeR32.ReviewEntryDockerfileTruth)

Scope: every sentence in `corpus/knowledge/render-web-services.md` stating a fact about
`apps-sdk/Dockerfile`, checked against
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/apps-sdk/Dockerfile` (17 lines, 380 bytes).
Axes: freshness (does the retained-bytes citation actually hold). Leaf seat; no lane mutation.

## Grounding runs (all in /home/vgpnk/Projects/shokunin; exit codes shown)

- `git hash-object .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/apps-sdk/Dockerfile .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml` → exit 0:
  `ee0b63819a9ce71e51469796541b9075e9676ae9`, `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`.
- `git -C ~/Projects/ds4cc-marketplace rev-parse 1fbdb8ed:apps-sdk/Dockerfile` → exit 0:
  `ee0b63819a9ce71e51469796541b9075e9676ae9` (same id).
- `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:apps-sdk/Dockerfile | cmp - <retained>` → exit 0, `cmp-identical` (byte-identity shown directly, not only via hash).
- `git -C ~/Projects/ds4cc-marketplace cat-file -e 1fbdb8ed:Dockerfile` → exit 128, `fatal: path 'Dockerfile' does not exist in '1fbdb8ed'` (no root Dockerfile).
- grep `ARG` (case-sensitive) on the retained Dockerfile → no matches (0 lines).
- grep `^(FROM|WORKDIR|COPY|RUN|ENV|EXPOSE|USER|CMD)\b` on the retained file → 16 directives + 1 blank line, numbered below.

Retained Dockerfile inventory: L1 `FROM node:22-alpine AS build`; L2 `WORKDIR /app/apps-sdk`; L3 `COPY apps-sdk/package*.json ./`; L4 `RUN npm ci`; L5 `COPY apps-sdk/ ./`; L6 `RUN npm run build`; L8 `FROM node:22-alpine`; L9 `ENV NODE_ENV=production`; L10 `WORKDIR /app/apps-sdk`; L11 `COPY apps-sdk/package*.json ./`; L12 `RUN npm ci --omit=dev`; L13 `COPY --from=build /app/apps-sdk/dist ./dist`; L14 `COPY marketplace /app/marketplace`; L15 `EXPOSE 3000`; L16 `USER node`; L17 `CMD ["node", "dist/server.js"]`.

## Verdicts (entry line numbers are `corpus/knowledge/render-web-services.md` lines)

Supported — 6:

1. L53–54 "the Dockerfile is blob `ee0b63819a9ce71e51469796541b9075e9676ae9`" — retained file hash-objects to exactly that id; external blob has the same id; `cmp` identical.
2. L61 bracketed inference "the Dockerfile copies only `apps-sdk/` and `marketplace` paths" — context-sourced COPYs are L3 (`apps-sdk/package*.json`), L5 (`apps-sdk/`), L14 (`marketplace`); L13 is stage-internal (`--from=build`), so every context source is under `apps-sdk/` or `marketplace`. Supported.
3. L65 "The image says `EXPOSE 3000`" — L15 of the retained file, verbatim.
4. L72 "`EXPOSE 3000` in the image does not change that" — the Dockerfile constituent (`EXPOSE 3000`) is present (L15); the rest of the sentence is about Render/server, not the image.
5. L73 "`apps-sdk/Dockerfile` at `1fbdb8ed` has no `ARG` instruction … prints 0" — 0 matches for `ARG` in the retained bytes; the substring `ARG` occurs nowhere, so the cited `grep -c` result reproduces exactly.
6. L85–86 retained Dockerfile "(`ee0b63819a9ce71e51469796541b9075e9676ae9`)" — hash-object confirms; also `cmp`-identical to `git show 1fbdb8ed:apps-sdk/Dockerfile`.

Wrong — 0. No sentence about the Dockerfile contradicts the retained bytes.

Not checkable against the retained bytes — 2 (with what external evidence exists):

1. L60 "the default would be the root Dockerfile, which this repository does not use" — a repo-layout fact, not a bytes-of-the-file fact. Corroborated externally: `cat-file -e 1fbdb8ed:Dockerfile` exit 128 (no root Dockerfile at that commit). Confirmed true, but a fresh re-check needs the marketplace clone; the retained pair cannot show it.
2. L28 "The container starts with the Dockerfile's own command unless a Docker Command is set" — a Render-docs claim (S059), not a claim about this file's bytes; out of scope for the retained Dockerfile (its truth lives with the round-31 S059 text retention). Incidentally consistent: the image does define `CMD ["node", "dist/server.js"]` (L17), so the default path exists.

Residual caveats:

- L73's trailing "the build never reads `OPENAI_APPS_CHALLENGE`" is flagged `[INFERENCE]` by the entry itself; the no-`ARG` premise is verified above, but the Docker-semantics premise (undeclared build args are unused) is not evidenced by any retained document in the lane — the inference is plausible and labeled, not sourced.
- The entry makes no line-count claim for the Dockerfile (the "20 lines" on L53 is render.yaml), so there is no count to check; the Dockerfile is 17 lines/380 bytes.
- Incidental: retained `render.yaml` also hash-objects to `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` as claimed (render.yaml sentences are the sibling seat's scope; recorded here only as evidence the retention mechanism holds).

## Bottom line

Every checkable Dockerfile fact in the entry is byte-true against the retained copy, and the retained copy is byte-identical to the external blob at `1fbdb8ed` (hash + `cmp` both confirm `ee0b63819a9ce71e51469796541b9075e9676ae9`). Tally: 6 supported, 0 wrong, 2 not checkable from retained bytes alone (one of those confirmed via the read-only marketplace checkout). No repair needed.

Tooling: no installs were needed (git, cmp, grep, wc only). No pacman use. No live requests; marketplace read only via `rev-parse`/`cat-file`/`show`.
