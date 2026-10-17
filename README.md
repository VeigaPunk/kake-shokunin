# kake-shokunin

**Web properties and publishing — audit, then source-fix, then
operator-gated publish.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. Kake owns the
VeigaPunk property fleet: GitHub Pages fronts, kimi.page / kimi.pro
mirrors, and the probe scripts that refuse to trust memory.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/kake-shokunin?branch=master)

## Domain

From `PROVINCE.md` and `SKILL.md`: scopes `ds4cc.com`, kimi.page / pro
mirrors, and Pages deploys. Every live-URL claim in the skill cites a
file or a verified report and must be re-probed — `updatedAt` in config
can lag live state, and several source trees named in the 2026-09-28
property map were recorded **absent** after the 2026-10-12 prune
(historical cites retained in `SKILL.md`).

The playbook is:

```
audit → source fix → operator-gated publish
```

Never fire into the vault-index kimi surface
(`https://veigapunk.kimi.page/`) — `SKILL.md` records that it hot-swaps
the live vault.

## What it refuses

Anything outside web properties and publishing. Secrets →
[kagi](https://github.com/VeigaPunk/kagi-shokunin). Browser interaction
craft → [tabi](https://github.com/VeigaPunk/tabi-shokunin). Endpoint
identity → [kama](https://github.com/VeigaPunk/kama-shokunin). CDP
chrome-profile ownership is contested with kagi and is reported, not
absorbed.

## In this repository

```
PROVINCE.md     domain boundary
SKILL.md        property map + publish playbook
SHONEN.md  SCORECARD.md  LOG.md
corpus/         knowledge/, lessons/, QUALITY.md, handoffs/
scripts/
  freshness-sweep.mjs    property freshness probe
  probe-delta.mjs        probe-to-probe delta
```

## Probe, don't remember

```bash
node scripts/freshness-sweep.mjs
node scripts/probe-delta.mjs
```

Treat script output as the current claim. The skill's URL table is a
sourced map, not a liveness oracle.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
