# Publish channels (verified)

## GitHub Pages — push to `main` is the publish verb

- `ds4cc-marketplace/.github/workflows/pages.yml`: on push to main → validate
  (`scripts/validate-agent-payloads.mjs`, `check-opencode-install.mjs`), build
  Kimi archives (`build-kimi-marketplace.py` + unittest), `cargo test` on
  `marketplace/validator`, `upload-pages-artifact` repo root → `deploy-pages`.
  `CNAME` file pins `ds4cc.com`.
- `plazir-15-site/.github/workflows/pages.yml`: same shape, uploads `.` whole,
  no custom domain → `veigapunk.github.io/plazir-15-site/`.
- `deploy-github-pages.sh` (ds4cc) is a one-time *setup* script: writes CNAME,
  adds origin, pushes once, prints the DNS records (apex A/AAAA, www CNAME).
  Not the deploy path.
- Agent-side shipping when push is gated: `git format-patch` +
  `publish/APPLY.md`, verified by `git am --check` on a fresh clone
  (wz1-ds4cc isolation protocol, `~/Projects/ephemeral/wz1/ds4cc` — emptied
  2026-09-28T21:42-03:00; recipe stands for re-created workspaces).

## Render — app.ds4cc.com

`ds4cc-marketplace/render.yaml`: Docker web service `ds4cc-marketplace-app`,
`apps-sdk/Dockerfile`, health `/health`, `APP_ORIGIN=https://app.ds4cc.com`,
`ALLOWED_ORIGINS=https://chatgpt.com` (ChatGPT Apps SDK host).

## Kimi surface — kimi.page / kimi.pro

No non-GUI channel exists on this host (kimi-webbridge: "not supported on
Linux", observed 2026-09-26). Verified verbs in
`~/Projects/webzites/scripts/kimi-surface.mjs`:
> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing line is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*

| Verb | Precondition | Metered? |
|---|---|---|
| `sync-check [id]` | — | free (pure HTTP) |
| `kimi-map` | signed-in lane | free (in-page RPC reads) |
| `update <id> --chat=<uuidv8>` | chat bound to live URL | `--fire --confirm=<id>` = 1 fire |
| `recreate <id> --chat=<vessel>` | dead slot + EMPTY chat | same gate |
| `recreate <id> --new-chat` | dead slot, no chat | same gate |
| `rebuild <id> --chat=<uuid>` | dead slot + existing unpublished chat w/ versions | same gate |

Publish gate: the version-card **Publish / Share→Update click is human**.
`AppService/PublishApp`, `OKCService/PublishDeployment` exist on
`www.kimi.ai/apiv2/` (recon-verified, cookie-session auth) but are recorded as
capability only — banned from fleet code. `DuplicateApp` is state-changing,
not allowlisted, never called.

Post-click verify (free): live URL 200 → `GetWebsiteByChatID` publishedUrl +
PUBLISHED → `sync-check` marker → `kimi-map` refresh.
Source: `~/Projects/webzites/fleet/kimi-surface-ops.md` rounds 1–4. <!-- r18 re-census 2026-10-14: ~/Projects/webzites/fleet/kimi-surface-ops.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->

## Round-20 corrections (append-only; base `cb807bc`)

- Base `corpus/knowledge/publish-channels.md:8`: **[r20-correction 2026-10-19: the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default (v5 adds include-hidden-files) — S001, S002]**
- Base `corpus/knowledge/publish-channels.md:9`: **[r20-correction 2026-10-19: a repo CNAME sets the domain only for branch publishing; under Actions it is ignored and the domain is a Pages setting (`cname` in the REST API) — S005, S003, S007]**
- Base `corpus/knowledge/publish-channels.md:10`: **[r20-correction 2026-10-19: the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default (v5 adds include-hidden-files) — S001, S002]**
- Base `corpus/knowledge/publish-channels.md:12`: **[r20-correction 2026-10-19: under Actions the repository CNAME is ignored for domain configuration; the domain is the Pages setting — S003, S005]**
