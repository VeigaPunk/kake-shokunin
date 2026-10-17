# kake-shokunin

Web properties and publishing for the VeigaPunk sites: audit a live
surface, fix the source, and publish only through the operator's gate.

The playbook in `SKILL.md` is a property map with a live URL, a source
directory, and a publish path for each site. Several of those directories
were measured absent after the 2026-10-12 projects prune. The skill keeps
the old rows and marks them historical in place. Verify current state
with the probe commands in the skill, not with the table from memory.

## The job

`PROVINCE.md` scopes the lane to web properties and publishing — ds4cc.com,
kimi.page/pro mirrors, Pages deploys — and to the knowledge, playbooks,
error patterns, and checklists for that work. Anything outside the domain
is reported back to the orchestrator.

Two detectors live in `scripts/`:

| Script | What it does |
|---|---|
| `scripts/probe-delta.mjs` | Reads `probe-history.jsonl` and reports `violated[]` movement between full sweeps. Spot probes (`total: 1`) are not diffed against full sweeps. Alert delivery stays with the probe owner; this script is the detection half. |
| `scripts/freshness-sweep.mjs` | Freshness sweep over the property set. Read the header before pointing it at a tree. |

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — the one-paragraph boundary.
2. [`SKILL.md`](SKILL.md) — the property map, including which rows are historical.
3. [`corpus/README.md`](corpus/README.md) — the coverage map and the known gaps the scripts were written against.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Property map and publish playbook. |
| `PROVINCE.md` | Domain and refusal. |
| `scripts/` | Probe-delta and freshness sweep. |
| `corpus/` | Knowledge and lessons. |
| `plans/` | Round plans. |
| `SHONEN.md` | Promotion checklist. Rank is shonen. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
Roster id `kake`, rank **shonen**.
