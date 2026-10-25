source: operator-local webzites evidence cited in-entry — `~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md`, `~/Projects/webzites/src/speedrun.mjs`, `agents/webzites-speedrun.md`, `reports/keepers/speedrun-r1.md` (webzites-relative), `~/Projects/ds4cc-marketplace/speedrun/`; in-entry r18 absence flags (re-census 2026-10-14) cover SPEEDRUN-PROTOCOL.md, speedrun.mjs and ds4cc-marketplace/speedrun, while the keeper card and speedrun-r1 carry no absence flag; S001, S002, S004 (corpus/SOURCES.md) for the round-20 upload-artifact correction
verified-at: 2026-09-28 round-5 original evidence (commit 18537e9; LOG round-5); r20 correction base cb807bc (2026-10-17) — historical-not-live-reverified, not a domain recheck; metadata contract S019
recheck: on speedrun lane or webzites/ds4cc-marketplace source change — `for p in ~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md ~/Projects/webzites/src/speedrun.mjs ~/Projects/ds4cc-marketplace/speedrun; do test -e "$p" && echo "present $p" || echo "absent $p"; done`; paths absent since the 2026-10-12 prune: operator must restore the source tree or retire this entry

# Speedrun publish pipeline — ds4cc.com/speedrun

Source: `~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md` (operator runbook, <!-- r18 re-census 2026-10-14: ~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
r1 speedrun lane) + `~/Projects/webzites/src/speedrun.mjs` + <!-- r18 re-census 2026-10-14: ~/Projects/webzites/src/speedrun.mjs absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`agents/webzites-speedrun.md` keeper card + `reports/keepers/speedrun-r1.md`.

The board is **static JSON + `main.js` served by GitHub Pages** from
`ds4cc-marketplace/speedrun/` — there is **no HTTP upload API**. Authority:
`~/Projects/ds4cc-marketplace/speedrun/` ONLY; `plazir-15-site/speedrun/` <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace/speedrun absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
is a frozen `rel=canonical` copy — never stage into it. Keeper mission
root = `~/Projects/webzites`; `prep --write` refuses `--out` outside it. <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->

## Stages (keeper does 1–3, operator does 4–6)

1. `webzites speedrun record --run <n> --interval-ms 300000 --out
   state/speedrun/<n>` — NDJSON samples → `telemetry.jsonl`; `run.json`
   meta on exit. `--duration-s 0`/omit = until SIGINT. Sources degrade to
   `null`, never fatal (ai-usage cache, `omp usage --json` 30s cache,
   `omp stats.db`, `ps` lanes). Board pollers ran at 5min; Cursor-Ultra
   empirical median 181s.
2. `webzites speedrun report` — p50/p95 + sparklines → `graph.json`;
   reads only `telemetry.jsonl`, re-runnable.
3. `webzites speedrun prep` (dry) / `prep --write` — **fail-closed**
   schema check vs live-derived key-intersection of authority
   `speedrun/data/run-*.json` (18 keys; `budget_usd` nullable in 4/9 runs;
   embedded snapshot fallback if repo unreadable). Enums: `category` ∈
   seed|oneshot|debate|company|fleet|avalanche; `status` ∈
   closed|announced|live; `run.id` must not collide with an existing
   `run-<id>.json`. `--write` stages under `<out>/prep/`:
   `run-<id>.json` + `<id>-curve.json` → `speedrun/data/`,
   `manifest-entry.json` → append `data/run-<id>.json` to
   `manifest.json runs[]` (touch `featured_run_id`/`live_strip_run_id`
   only when featured), `receipt.json` sha256+bytes — **keeper-side only,
   never uploaded**.
4. Operator: `cp` the two bodies into the repo, edit `manifest.json`,
   `git commit && git push origin main` — Pages deploys the whole repo.
5. Operator verify: `curl ds4cc.com/speedrun/data/run-<id>.json` byte-diff
   vs staged file, `<id>-curve.json`, `manifest.json | grep run-<id>` —
   all three must pass; **a 200 with different bytes is failure — stop**.
6. `webzites speedrun post` — prints one deterministic X draft
   (`run <n> is live on ds4cc.com/speedrun — <duration> (<n> samples) ·
   meter <pct> on <meter> · p95 <pct> · Δ <pp> · peak <n> agent lanes ·
   $<usd> burned · <live-url>`; exit 1 if >280 chars). Writes `post.json`
   with `posted:false`; **operator posts from their own X session — never
   automated, never retried**; record status URL into `run.links.x_post`.

## Redaction (fail closed, enforced inside prep)

Bodies are **allowlist-built** — only fixed fields leave the keeper.
Denylist scan on every key+string: emails, `account_hint`-style keys,
absolute paths (`/home/…`, `C:\…`, `file://`), secret shapes (`sk-*`,
`ghp_*`, `AKIA…`, `Bearer`, `api_key:`), private hosts
(`localhost`/RFC-1918). Historical leaks exist in OLD receipts
(`account_hint` email, absolute `paper_attachment` path) — never copy
those fields forward. Public-safe: run id/title, runner handle,
provider/product, budget, meter %, lane counts, spend totals, `x.com` URLs.

## Failure handling

Fail closed on: missing telemetry, failing schema, redaction hits, `--out`
outside mission root, duplicate run id, probe mismatch, >280-char draft.
**Never smooth gaps, never invent a percentage, never retry a post.**

## Round-20 corrections (append-only; base `cb807bc`)

- Base `corpus/knowledge/speedrun-pipeline.md:36`: **[r20-correction 2026-10-19: the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default (v5 adds include-hidden-files) — S001, S002, S004]**

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/speedrun-pipeline.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [speedrun-pipeline:c1] **HOLD** — The previously flagged local runbook and implementation paths remain absent. Surface: `/home/vgpnk/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md; /home/vgpnk/Projects/webzites/src/speedrun.mjs`.
- [speedrun-pipeline:c2] **STALE** — The unflagged keeper-card and keeper-report references remain extant current source files. Surface: `/home/vgpnk/Projects/webzites/agents/webzites-speedrun.md; /home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/webzites/agents/webzites-speedrun.md` and `/home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md` are absent and should be marked unavailable rather than unflagged current sources.
- [speedrun-pipeline:c3] **HOLD** — The historically designated local authority path remains absent. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/speedrun`.
- [speedrun-pipeline:c4] **UNVERIFIABLE** — The live `prep --write` implementation refuses output paths outside the keeper mission root. Surface: `/home/vgpnk/Projects/webzites and /home/vgpnk/Projects/webzites/src/speedrun.mjs`. Unverifiable: Both the named mission root and the implementation path are absent, so no current CLI is available to execute this guard and decide the behavior.
- [speedrun-pipeline:c5] **UNVERIFIABLE** — The cited board poller currently runs on a five-minute cadence. Surface: `systemctl --user list-timers --all --no-pager; systemctl list-timers --all --no-pager; crontab -l`. Unverifiable: No current timer is identified as a speedrun/board poller, and the five-minute `ai-usage.timer` cannot be attributed to that poller from the available evidence.
- [speedrun-pipeline:c6] **HOLD** — The primary board's currently served run records still have 18 common top-level keys and `budget_usd` explicitly null in four of nine records. Surface: `GET https://ds4cc.com/speedrun/data/manifest.json and its nine `runs[]` JSON URLs`.
- [speedrun-pipeline:c7] **UNVERIFIABLE** — The public board is served from GitHub Pages and has no HTTP upload API. Surface: `GET https://ds4cc.com/speedrun/; GET https://ds4cc.com/speedrun/main.js; GET https://ds4cc.com/speedrun/data/manifest.json`. Unverifiable: The local source/authority tree is absent; public GETs show a JSON-backed page but cannot establish its GitHub Pages origin or prove that no separate upload endpoint exists.
- [speedrun-pipeline:c8] **HOLD** — The live Pages mirror declares `https://ds4cc.com/speedrun/` as its canonical URL. Surface: `GET https://veigapunk.github.io/plazir-15-site/speedrun/`.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/speedrun-pipeline.md:1 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/speedrun-pipeline.md:13 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/speedrun-pipeline.md:3 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/speedrun-pipeline.md:78 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.

- Additional round-23 correction [speedrun-pipeline:c7] at line 82: the mapped authority tree is present, but its reappearance alone does not establish the public hosting origin or an upload API (w1/R23ReceiptsDs4ccStale.md).

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). The round-20 correction lines in this entry cite S001, S002 and S004 (line 70). Each was judged against bytes re-fetched 2026-10-21 (`.ufo/waves/round-26/fetched/`, receipts `.ufo/waves/round-26/rechecks/S0NN.json`) and holds: S001 and S002 as in publish-channels.md; S004 uploads the configured path as the artifact. Ledger pairs in `.ufo/waves/round-26/statements.json`; found by the falsify wave (w2/CounterCritic.md).
