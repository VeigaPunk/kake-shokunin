# kake-shokunin

Web properties and publishing for the VeigaPunk fleet: ds4cc.com, the
kimi.page and kimi.pro mirrors, and GitHub Pages deploys.

Rank: **shonen**. [`SHONEN.md`](SHONEN.md) is the promotion checklist;
its boxes are open.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> What is actually live on this property right now, and which source
> directory publishes it?

The playbook in `SKILL.md` is audit → source fix → operator-gated
publish. Config `status` is a snapshot. The skill's own rule is to
re-probe before acting. Several source directories named in the property
map are marked absent after the 2026-10-12 projects prune; those rows are
historical records, kept in the table with the re-census note.

## Boundary

**Owns:** the property map, freshness pins, probe history, and the
publish-path knowledge for these sites.

**Hands off:** anything outside web properties and publishing. Cross-domain
evidence goes back to the orchestrator. The shared word "probe" does not
make an endpoint-health question (kama) or a research question (kengaku)
into a publishing task.

Full boundary: [`PROVINCE.md`](PROVINCE.md).

## Where the work lives

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | property map, decision tables, publish rules |
| [`corpus/knowledge/`](corpus/knowledge/) | sourced notes, including freshness pins |
| [`corpus/handoffs/`](corpus/handoffs/) | cross-lane handoffs |
| [`scripts/freshness-sweep.mjs`](scripts/freshness-sweep.mjs) | re-executes the quantified standing claims |
| [`scripts/probe-delta.mjs`](scripts/probe-delta.mjs) | `violated[]` movement over `probe-history.jsonl` |
| [`LOG.md`](LOG.md), [`SCORECARD.md`](SCORECARD.md) | rounds and axis verdicts |

`freshness-sweep.mjs` re-checks cited filesystem paths, probe-history
shape, and the armed pins (charter beat, kimi dead slot, push gate,
sitemap). `probe-delta.mjs` detects coverage and violation movement; alert
delivery stays with the webzites owner, as that file's header says.

```sh
node scripts/freshness-sweep.mjs
node scripts/probe-delta.mjs
```

Read each file's header for flags. A green run is a pin check against the
tree you have, and several historical source directories are already
recorded absent.

## How a round lands

One axis-move. Non-author verifier. `LOG.md` plus `SCORECARD.md`. The
corpus is append-only: a stale URL stays in the record with the date it
was last true.
