# kake-shokunin

**Web properties and publishing** — audit the VeigaPunk property fleet,
fix the source, publish only when the operator gates it.

Kake's playbook is `audit → source fix → operator-gated publish`. Every
claim cites a file or a verified report. State is re-probed, never
remembered. Config `status` is a snapshot, not truth.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**.

## The craft

- Property map: live URL, source dir, publish path (GitHub Pages, Kimi
  surfaces, Render). Dead rows stay `pruned` / `queued` — never deleted.
- Freshness: what the live URL actually serves vs what the source tree
  (or last known source tree) claims.
- Probe discipline: `expect` tripwires, status histograms, keeper-bot
  parity (`fleet.config.json` vs `grokbots.json`) as recorded in
  [`SKILL.md`](SKILL.md).
- Publish path is operator-gated. This lane does not silently ship.

**Host note (recorded, not a re-scope).** The 2026-10-12 `~/Projects`
prune removed several source trees this skill still cites
(`ds4cc-marketplace`, `origin-work/charter-ufo-fsd`, `webzites/fleet`).
Those citations are historical records. Re-probe before acting; do not
treat a stale `status:live` as a live site.

## Province

Owns: web properties & publishing — scopes historically `ds4cc.com`,
kimi.page / kimi.pro mirrors, Pages deploys.

**Refuses:** secrets (→ kagi; session material is shape-only), model
endpoints (→ kama), model quality (→ kengaku), orchestration (→
kumitate), browser *interaction* craft (→ tabi). Report, never absorb.

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
kake-shokunin/
├── SKILL.md            property map, probe rules, publish discipline
├── PROVINCE.md         domain boundary
├── SHONEN.md           promotion checklist
├── LOG.md              append-only trail
├── SCORECARD.md        per-axis verdicts
├── AGENTS.md           operating rules
├── plans/
├── scripts/
│   ├── freshness-sweep.mjs
│   └── probe-delta.mjs
└── corpus/
    ├── knowledge/      sourced notes
    ├── lessons/        per-round lessons
    └── handoffs/       packets sent to other lanes
```

## Start here

Read [`SKILL.md`](SKILL.md) §Property map first — it is the operating
picture, including which rows are historical-absent. Then:

```sh
# hermetic; the only writes are scratch fixtures under /tmp
node scripts/freshness-sweep.mjs --selftest
```

The live path (`node scripts/freshness-sweep.mjs`) is read-only against
the host and will `drift` where cited trees are gone — that is the
correct answer. `scripts/probe-delta.mjs` compares recorded probe
events; it does not publish.

Never fire into the vault-index Kimi chat named in `SKILL.md` (it
hot-swaps the live vault). Never treat a kimi.page 404 as "unpublished
on purpose" without a source citation.

## How a round works

One axis-move on operability / freshness (and any other live axis in
`SCORECARD.md`). Lane identity: `kake-shokunin <kake@shokunin.local>`.

## Fleet

[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin) ·
[kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin)
