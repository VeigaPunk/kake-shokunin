# kake-shokunin

Web properties and publishing — the sites, the mirrors, and the Pages
deploys this lane is willing to stand behind.

The province names the scope in one line: `ds4cc.com`, the kimi.page/pro
mirrors, and Pages deploys. The craft record is a freshness instrument
that re-executes standing claims against the live filesystem and records
which pins still hold.

Rank: **shonen**. `SHONEN.md` is still here. Registered in the fleet
`MANIFEST.json` roster since 2026-09-28.

## Province

**Owns.** Knowledge, playbooks, error patterns, and checklists for those
web properties and their publishing path.

**Hands off.** Anything outside that domain. Cross-domain evidence goes
back to the orchestrator. The province file is six lines; the surfaces
and the pin ledger live in `SKILL.md` and `corpus/`.

## Start here

1. `PROVINCE.md` — the one-line boundary.
2. `corpus/README.md` — the coverage map.
3. `SKILL.md` — the playbook.
4. `corpus/knowledge/freshness-sweep.md` — what the standing instrument
   last caught.
5. `SCORECARD.md` — read the banner before the numbers. The card says the
   numeric ratings are legacy round-17/18 assessments, and that round 20
   is a blocked attempt whose admission did not advance a score.

## Run the sweep

From the repository root:

```sh
node scripts/freshness-sweep.mjs --selftest
node scripts/freshness-sweep.mjs
```

The script header is the contract: exit 0 clean, 1 drift, 2 unreadable
input, 64 usage. The normal path is read-only; writes exist only inside
the `--selftest` region, under a temp directory. A live exit 1 can be the
expected outstanding pin rather than a new surprise — the scorecard names
PQ-14 (`plazir-live-source-gap`) as the live exit-1 that remained. Read
the sweep output before you repair prose.

`scripts/probe-delta.mjs` is the companion for probe-history shape.

## The tree

| Path | What it is |
|---|---|
| `scripts/` | The freshness battery |
| `corpus/knowledge/` | Pins, sweep notes, publishing claims |
| `corpus/lessons/` | Per-round lessons |
| `corpus/handoffs/` | Patches staged for the owner of a surface this lane does not write |
| `plans/` | Round plans |

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin).
