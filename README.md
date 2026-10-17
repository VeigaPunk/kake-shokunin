# kake-shokunin — 架け

**Web properties and publishing.** Audit the live surface, fix the
source, and stop at the operator-gated publish.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *is this property the bytes we think we shipped, on
the URL we think we own — and if not, where did the snapshot lie?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): the VeigaPunk property fleet —
ds4cc.com, kimi.page / kimi.pro mirrors, GitHub Pages deploys. Config
`status` is a **snapshot, not truth**; `SKILL.md` records the 2026-09-28
probe that found `lucario` marked `live` while never published.

Several `~/Projects/…` source dirs named in `SKILL.md` went absent in
the 2026-10-12 prune. Those rows stay as historical record. Re-probe
before acting; never publish from memory.

**Refuses** secrets (→ [kagi](https://github.com/VeigaPunk/kagi-shokunin)),
model endpoints (→ [kama](https://github.com/VeigaPunk/kama-shokunin)),
and browser *interaction* craft (→
[tabi](https://github.com/VeigaPunk/tabi-shokunin)). This lane publishes;
it does not drive a session against a third-party site.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | property map, probe-before-publish playbook, dead-slot recreation paths |
| [`PROVINCE.md`](PROVINCE.md) | domain boundary |
| [`scripts/freshness-sweep.mjs`](scripts/freshness-sweep.mjs) | re-verification battery over standing pins |
| [`scripts/probe-delta.mjs`](scripts/probe-delta.mjs) | probe-history event shape |
| [`corpus/`](corpus/) | knowledge, lessons, handoffs |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The gate

```sh
node scripts/freshness-sweep.mjs            # live re-verification of standing claims
node scripts/freshness-sweep.mjs --selftest # hermetic fixtures under /tmp/kake-r16/selftest
```

Exit `0` clean, `1` drift, `2` unreadable input. The normal path is
read-only and never writes under `~/Projects`.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
