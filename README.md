# kake-shokunin — web properties and publishing

The question this lane answers is how the VeigaPunk property fleet is audited, fixed at the source, and published only through an operator gate (`SKILL.md`, `PROVINCE.md`).

**Rank:** `SKILL.md` frontmatter says `Rank: shonen`. `SHONEN.md` is a promotion checklist and every box is `[ ]`. That is not a promotion.

## Owns / refuses

Owns the domain knowledge, playbooks, error patterns, and checklists for web properties and publishing. `PROVINCE.md` names the scope as ds4cc.com, kimi.page and kimi.pro mirrors, and Pages deploys.

Refuses anything outside that domain. Cross-domain evidence is reported to the orchestrator, not absorbed (`PROVINCE.md`).

## Start here

Round-18 notes in `SKILL.md` record that several `~/Projects` source directories and `fleet.config.json` are absent after the 2026-10-12 prune. Those rows are kept as historical cites. Do not treat a remembered URL as live state.

The in-repo freshness battery is read-only on the normal path (`scripts/freshness-sweep.mjs` header):

```sh
node scripts/freshness-sweep.mjs --help
```

The same header documents `node scripts/freshness-sweep.mjs [--json] [--offline] [--section=paths|history|armed] [--repo DIR] [--selftest]`. Exit `0` clean, `1` drift, `2` unreadable input, `64` usage. `--selftest` writes only under its hermetic temp tree. The normal path does not write and does not touch `~/Projects`.

`scripts/probe-delta.mjs` is the history-diff tool named from `corpus/README.md`. The live `webzites` probe commands live in `SKILL.md` and depend on a host tree that round 18 recorded as absent.

## How to read the corpus

`corpus/README.md` is the coverage map (registry, publish channels, drift, mirrors, queues, the freshness sweep). Its sha256 is recorded in `.ufo/round-20/measured-corpus-inputs.json`, and lessons cite `corpus/README.md` by line, so this change does not edit it. `corpus/QUALITY.md` is the admission bar. `corpus/knowledge/` holds the sourced notes. `corpus/lessons/` holds the round lessons. `corpus/handoffs/` holds the webzites-owner handoff.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Domain boundary |
| `SKILL.md` | Property map and the audit → fix → publish checklist |
| `SHONEN.md` | Promotion checklist, boxes unchecked |
| `LOG.md` | Append-only record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Operating rules |
| `corpus/` | Knowledge, lessons, quality bar, handoffs |
| `scripts/` | `freshness-sweep.mjs`, `probe-delta.mjs` |
| `plans/` | Round plans |
| `.ufo/` | Round machinery |

## Neighbors

kagi for credential material on a publishing path. The musketeer lease question is contested and not ruled here (`SKILL.md` property notes point at kagi for that overlap). Report anything that is not a web property.

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
