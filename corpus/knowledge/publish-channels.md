source: S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections; the entry's historical local sources are the ds4cc/plazir workflows, render.yaml, deploy-github-pages.sh and Kimi surface tools named below. Metadata authority only: S019, not live platform verification.
verified-at: 2026-09-26 (kimi-webbridge "not supported on Linux" check) and 2026-09-28 (round-1 commit cd5b381 that introduced this entry; wz1-ds4cc emptied 2026-09-28T21:42-03:00); round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed
recheck: local historical reading only: `git show 5009ecaa1cce10b895617a585ddd3f7c7c923a84:corpus/knowledge/publish-channels.md`; the external source trees are absent after the 2026-10-12 prune. Operator must restore and re-derive the dependent workflow/Render/Kimi claims or retire those sections.

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

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/publish-channels.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [publish-channels:c1] **STALE** — The current setup helper performs one push only and has a run-once guard. Surface: `GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/deploy-github-pages.sh`. Correction: As of 2026-10-21, the script has no run-once guard and executes `git push -u origin main` on every invocation, so the unit should describe the push as per-invocation rather than ‘once’.
- [publish-channels:c2] **UNVERIFIABLE** — The Kimi script still enforces the listed update precondition and one-fire confirmation gate, with the documented human publish and post-click verification sequence. Surface: `test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites/fleet/kimi-surface-ops.md; command -v kimi-webbridge; unauthenticated GET https://www.kimi.ai/apiv2/`. Unverifiable: The cited CLI and operations sources are absent, and the host's missing `kimi-webbridge` command does not establish the absence or behavior of every possible channel. An unauthenticated GET of the API root does not determine whether cookie-authenticated methods or the human-gated UI flow exist; those flows were not accessed under the no-auth/no-chat boundary.
- [publish-channels:c3] **HOLD** — The named historical project/workspace trees remain absent at their recorded local paths on this host. Surface: `for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e "$p"; then printf 'EXISTS %s\n' "$p"; else printf 'ABSENT %s\n' "$p"; fi; done`.
- [publish-channels:c4] **HOLD** — The ds4cc Pages workflow still triggers on main, performs the listed checks/build/test, uploads the checked-out project tree, and deploys it; its documented public domain currently serves the site and sitemap. Surface: `GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/.github/workflows/pages.yml; GET https://ds4cc.com/; GET https://ds4cc.com/sitemap.xml`.
- [publish-channels:c5] **HOLD** — The Plazir Pages workflow still triggers on main, uploads the project root (`.`), and its documented GitHub Pages URL currently serves the expected site and sitemap. Surface: `GET https://raw.githubusercontent.com/VeigaPunk/plazir-15-site/main/.github/workflows/pages.yml; GET https://veigapunk.github.io/plazir-15-site/; GET https://veigapunk.github.io/plazir-15-site/sitemap.xml`.
- [publish-channels:c6] **HOLD** — The Render configuration still names the Docker web service, Dockerfile, health path, APP_ORIGIN, and ALLOWED_ORIGINS as stated, and the public health endpoint currently reports healthy. Surface: `GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/render.yaml; GET https://app.ds4cc.com/health`.
- [publish-channels:c7] **HOLD** — The version-qualified action correction is current: v4 excludes hidden paths by default in addition to `.git`/`.github`, and v5 adds an `include-hidden-files` option defaulting to false while always excluding `.git`/`.github`. Surface: `GET https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml; GET https://raw.githubusercontent.com/actions/upload-pages-artifact/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml; GET https://raw.githubusercontent.com/actions/upload-pages-artifact/v3/action.yml; GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/.github/workflows/pages.yml`.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/publish-channels.md:69 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61). Each was judged against bytes re-fetched 2026-10-21 (`.ufo/waves/round-26/fetched/`, receipts `.ufo/waves/round-26/rechecks/S0NN.json`) and holds: S001 v4.0.0 and main exclude `.git`/`.github`, v4.0.0 excludes `.[^/]*`, main makes it conditional on `include-hidden-files`; the S002 v5.0.0 release lists “feat: add include-hidden-files input”; S005 says under a custom Actions workflow “any existing CNAME file is ignored and is not required”; S003 and S007 place the domain in Pages settings / the `cname` API field. Ledger pairs in `.ufo/waves/round-26/statements.json`; found by the falsify wave (w2/CounterCritic.md).
