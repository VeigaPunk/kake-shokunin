# Round 21 — ScopeOverlap (kake-shokunin)

Seat: `KakeR21.ScopeOverlap` (connector, leaf). Scope: sibling overlap of lane-local metadata gates vs protocol ownership, and the publishing boundary. Read-only; no target files edited; no commits; no network; no domain or source-tree reads; no git subcommands; no installs or upgrades.

## Ownership map (grounded)

| Surface | Owner | Evidence |
|---|---|---|
| Corpus contract (trio, `## Gate`, SOURCES v1, append-only rules) | Fleet protocol, read-only to the lane | `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` lines 18–20, 53–60, 64–74, 162–171 |
| `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md` | L1 (per wave contract) | wave spec Contract paragraph |
| `corpus/knowledge/*.md`, `corpus/lessons/round-<N>.md` (lane-authored) | Lane (kake) | CORPUS.md lines 54–56 ("Lanes own `lessons/round-<N>.md`") |
| `corpus/lessons/*-aggregator-*.md`, `round-20-verifier-spotcheck.md` | Aggregator / verifier, not lane | CORPUS.md lines 54–56; wave Contract "no altering verifier/aggregator/operator lessons" |
| `scripts/freshness-sweep.mjs`, `scripts/probe-delta.mjs`, `corpus/knowledge/freshness-pins.json` | Lane | PROVINCE.md lines 17–18 |
| Publishing (`git push`, Pages deploy, kimi publish click, PublishApp RPCs) | Operator | SKILL.md lines 121–132, 375–377; PROVINCE.md line 18 |

## Findings

### F1. The metadata trio is protocol-mandated but not gated by the lane's own instrument
- CORPUS.md lines 162–165 say "Freshness sweeps read these fields, not provenance buried in prose." The lane's instrument does not. `scripts/freshness-sweep.mjs` has no reader for `source:`, `verified-at:` or `recheck:`; the only `source` hits are the human label at lines 225/227/230/931 and the `source:` field of the pins loader at 1055.
- Consequence: C1's "honest historical metadata" is a convention, not a gate. Any claim that the trio is "checked" must be scoped to the reviewer's read, not to `freshness-sweep`. A real trio gate would be a new lane gate and is out of this round's stated scope unless assigned.

### F2. S019 is the trio's cited authority, and the row now present is not verifiable
- At my first read of `corpus/SOURCES.md` (registry lines 9–26) the registry ended at S018. At a re-read later in this session, a row S019 exists at line 27. Its content is "own-work: publishing corpus contract audit — `scripts/corpus-contract.mjs`", tier A, status `mined`, used-by `corpus/lessons/round-21.md`.
- `scripts/corpus-contract.mjs` does not exist (`scripts/` holds only `freshness-sweep.mjs` and `probe-delta.mjs`). The row's own "teaches" text says the gate is "first-working round 21", so it is a promised gate, not one run.
- SOURCES tier rule (`SOURCES.md` definition of A, and CORPUS.md line 93–97 in the protocol): tier A for own-work means "the lane's own re-runnable gate output." A tier-A row whose gate does not exist breaks the tier rule. This is grounded; whether it is intended is L1's call.
- The protocol `CORPUS.md` Contract-v1 section (lines 64–171, read this session) does not define S019. The metadata contract cited by ~18 knowledge entries is therefore a lane-local row, not a fleet-ratified id.
- Seat reports disagree on S019 state. `w1/Knowledge05.md` says the row is "confirmed present". `w1/Knowledge02.md`, `Knowledge03.md`, `Knowledge06.md`, `Knowledge09.md`, `Knowledge10.md` each say it was absent when they looked. These are timing differences, not necessarily errors, but L1 should reconcile them before the entries are cited as admitted.
- `w1/Knowledge09.md` states "`corpus/CORPUS.md` does not exist". `corpus/knowledge/publish-queue.md` line 1 (prefix) says "corpus/CORPUS.md registered by L1 this round". No `corpus/CORPUS.md` exists in the glob of `corpus/*.md` at my read. The prefix's registration claim is unsupported by the tree.

### F3. Prefix additions move every line number in a lane file; the citation-local gate is shift-invariant, but the ledgers are not
- Gate behaviour: `scanCitations` keys citations as `${rel}:${i+1}` (freshness-sweep.mjs line 404), annotates a ±2 window relative to the citing line (413), and pins hold target and file sets only (`pathsMissSet`, `pathsFiles`, `pathsCitedSet`), not line numbers. A uniform prefix therefore does not change the gate verdict. It changes the reported coordinates.
- Historical pointers that will go stale on a prefix insert, all of which are append-only history and must not be rewritten: `corpus/lessons/round-20.md` ledger rows (lines 336–367) cite `freshness-sweep.md:102–145`, `publish-channels.md:49–50`, `probe-delta-alerting.md:78–79`, `fire-journal-codes.md:4–5`, `free-read-verbs.md:352–353`, `round-17.md:14–21`, `round-4.md:5–6`; `.ufo/round-20/acceptance.json:46,58,69` and `citation-debt.json:42,112` point at the same spots.
- QUALITY.md lines 31–39 (post-review append-only ruling): an adjacent note requires "an inbound-anchor movement census and corrections for moved pointers; otherwise leave the location uncleared." That census is not in the wave and is not present for any of the 21 entries. Either the census is run for each prefixed file, or the prefixes must be shown not to move any inbound pointer.

### F4. The 4/21 baseline in the wave spec cannot be reproduced from the working tree
- The working tree already shows `source:` as line 1 in many knowledge entries, and several seat reports (`w1/Knowledge02.md`, `Knowledge05.md`, `Knowledge09.md`) describe prefixes they wrote. Current counts therefore mix base and in-flight writes.
- The base count needs `git show 5009ecaa…:corpus/knowledge/<f>.md | head -1` per file. That is a git read, outside this seat's allowed activity, so I did not run it. `MetadataCheck` is the owner of that count.

### F5. Historical `## Gate` sections (C2) must stay EOF-only and avoid new unannotated absent cites
- CORPUS.md line 19 requires `## Gate` per lesson; `round-20.md` already has `## Gate` (line 41) and `## Gate — round-20 resume` (line 182). Adding a historical gate must not duplicate or edit those.
- QUALITY.md line 9–16 bar: "Admission authority" rejects treating self-review as promotion; "Platform mechanism" requires tier-A cites. A historical gate for a lane-authored lesson must record that no independent non-author spot-check was run. It must not state that one passed.
- The paths gate scans `SKILL.md` and `corpus/**/*.md` (freshness-sweep §paths). Any new `~/Projects/...` cite in a gate section that resolves to nothing is `drift` unless annotated with the named target, dated absence event, and non-executable wording (QUALITY.md line 14). An annotation word inside ±2 lines is not enough.
- Scope count check: the 15 lane-authored lessons are `round-1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 17, 18, 19-recensus, 20`. Excluded by the ownership rule: `round-1-aggregator-audit`, `round-5-aggregator-audit`, `round-5-aggregator-mirror-pathless-cli-invocation`, `round-6-aggregator-audit`, `round-8-aggregator-box3-coldrun`, `round-9-aggregator-corpus-verdict`, `round-4-aggregator-audit`, `round-20-verifier-spotcheck`. `round-21.md` is this round's lesson and is not historical.

### F6. Publishing boundary is unchanged by any round-21 move
- Hard rule (SKILL.md 375–377): never `git push`, never click publish, never call publish RPCs from fleet code. This round's C1/C2 are local markdown prefixes and EOF additions. Nothing in the wave requires or authorizes a push, a Pages deploy, or a kimi fire.
- `freshness-pins.json` pins `round: 18` and says re-pin happens only in the same commit as corrected prose. C1/C2 change no pinned value; no re-pin is implied.
- The S019 row says "not verification of historical platform claims". Trio `source:` fields therefore must not carry platform mechanism claims without a tier-A row (QUALITY.md line 15). The kimi-shokunin protocol file is a fleet document, not platform authority, and must not be cited as one.
- Sibling boundaries: no cross-domain cite is needed. Kagi (secrets), tabi (crawler discipline), chousa (method) and kama (local serving) are not touched by this scope (PROVINCE.md 30–37).

## Scope constraints (what the round's writers must respect)

1. Prefix additions only at line 1 of knowledge files; never reflow or edit an existing line. Run an inbound-pointer census for each file before claiming it is "pure", or record the moved pointers in a correction block at EOF.
2. Trio `source:` may cite S019 only as "metadata format authority, not platform authority" and must say the row's gate (`scripts/corpus-contract.mjs`) is absent until it exists. Do not claim any round-21 gate ran.
3. Historical `## Gate` sections go to EOF of the 15 listed lessons only. They name no admissions or rejections that the base record does not already contain, and no independent review.
4. No edits to SOURCES, QUALITY, README, SCORECARD, LOG, SKILL, `freshness-pins.json`, any aggregator or verifier lesson, or the protocol CORPUS.md.
5. Any new cite to an absent path needs the QUALITY.md line 14 annotation form.
6. No push, no commit by the seat, no publish action.

## Open items for L1 / integrator (not decided here)

- Register or retire S019. The `scripts/corpus-contract.mjs` it names does not exist, and its tier-A own-work status outruns the gate.
- Reconcile the seat reports on S019 and on `corpus/CORPUS.md` existence before the prefixes are called admitted.
- Decide whether a movement census is required for the 21 prefixes (QUALITY.md 31–39).
- `MetadataCheck` to produce the base-commit count for the trio.

## Verification

- Read only: `PROVINCE.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `AGENTS.md`, `scripts/freshness-sweep.mjs` (selected ranges), `corpus/knowledge/freshness-pins.json`, `SKILL.md` (grep), kimi-shokunin protocol `CORPUS.md` and `PROTOCOL.md`/`PROTOCOL-APPENDIX.md` (grep), wave spec and registry JSON (ranges), several `corpus/knowledge/*.md` header lines, and `w1/Knowledge*.md` seat reports (grep).
- Globs and greps only. No build, test, lint, or sweep was run. No git subcommand was run. No network reads. No credential or auth files touched.
- Installs or upgrades: none.
- Limitations: F4 base-commit count is unverified. F2 reflects the SOURCES.md state at the times read; the file is being written concurrently.
