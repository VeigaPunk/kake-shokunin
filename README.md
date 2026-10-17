# kake-shokunin — web properties & publishing

**Audit → source fix → operator-gated publish.** Every claim cites a
file or a verified report. Verify state with the probe commands, never
with memory.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane for the
VeigaPunk property fleet: `ds4cc.com`, kimi.page / kimi.pro mirrors, and
GitHub Pages deploys. Rank: shonen.

Kake owns *publishing surfaces*. It does not own browser-driving craft
([tabi](https://github.com/VeigaPunk/tabi-shokunin)), secrets
([kagi](https://github.com/VeigaPunk/kagi-shokunin)), or model endpoints
([kama](https://github.com/VeigaPunk/kama-shokunin)). The shared word
"probe" carries no scope.

## Province

**Owns:** the property map (live URL, source dir, publish path); freshness
and delta probes over those surfaces; the domain knowledge, playbooks,
error patterns, and checklists in this repo.

**Refuses:** anything outside web properties & publishing. Report
cross-domain evidence back to the orchestrator.

Host fact, recorded in `SKILL.md` (r18 re-census, 2026-10-14): several
source trees named on the property map
(`~/Projects/ds4cc-marketplace`, `~/Projects/origin-work/charter-ufo-fsd`)
were gone after the 2026-10-12 `~/Projects` prune. Those rows stay as
historical record. Do not treat a cited source dir as live until a
same-round probe says it is.

The CDP / Chrome-profile lease is contested with kagi — kake does not
adjudicate custody. Full boundary: [`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — property map and the audit → fix → publish playbook.
2. [`PROVINCE.md`](PROVINCE.md) — owned domain and refusals.
3. [`scripts/`](scripts/) — freshness and delta probes.

## Probes

```
node scripts/freshness-sweep.mjs --selftest
node scripts/freshness-sweep.mjs --offline
node scripts/probe-delta.mjs
```

These are read-only toward live properties. They do not publish. A
publish path named in the property map is operator-gated — this lane
prepares the source fix and reports the deploy surface; it does not
push a property because a probe went green.

The vault index at `https://veigapunk.kimi.page/` is a live Kimi surface.
`SKILL.md` forbids firing into that chat: it hot-swaps the live vault.

## What's in the repo

```
kake-shokunin/
├── SKILL.md          property map + playbook
├── PROVINCE.md       domain boundary
├── SHONEN.md         promotion checklist
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── scripts/          freshness-sweep.mjs, probe-delta.mjs
├── plans/            round plans
└── corpus/           knowledge/, lessons/, QUALITY.md
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
