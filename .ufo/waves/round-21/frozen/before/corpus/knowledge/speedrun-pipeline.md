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
