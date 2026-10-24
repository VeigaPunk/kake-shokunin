# ScribeFreshnessKnowledge — round 24, lane kake, claim C1 (freshness)

Seat: scribe (author side, leaf). Base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Observed 2026-10-21T11:46Z. Scratch: `/tmp/kake-r24-ScribeFreshnessKnowledge-Nc0g/`. No lane file was edited; `corpus/knowledge/freshness-sweep.md` is unchanged (sha256 `9e22fd12a7d0147e1f98a8df2cc9b9f376790bfd3874a41e3522d6e36954f7a7`, 188 lines).

## Verdict

The draft section is below (§ Draft) and is ready for the L1 to integrate once the sidecar and the C1 counter land. It was tested in a fixture copy of the corpus: appending it changed no drift set, no newMissing set and no recovered set. Its one new cite (the sidecar example line) is self-annotated. The draft is a description of rules that the executors and the counter must implement; it is not yet a claim that they work.

Main facts behind it: the `~/Projects/ds4cc-marketplace` tree reappeared on 2026-10-21 (directory birth 05:19:01 -03). The four pinned misses for that tree (T16 to T19) are stale. Twelve newMissing tokens (T04 to T15) are unpinned. Three drift targets (T01 to T03) have four unannotated cites. Current exit of the paths section is still 1.

## Findings

### F1 — P2 (freshness): pinned miss set is stale in both directions

Exact command and output:

```
$ node scripts/freshness-sweep.mjs --section=paths --json   # exit=1
counts {'resolve': 19, 'declaredAbsent': 60, 'declaredAbsentIndirect': 4, 'drift': 3, 'unresolved': 10, 'newDrift': 0, 'newMissing': 12}
setDelta.recovered ['~/Projects/ds4cc-marketplace', '~/Projects/ds4cc-marketplace/CNAME', '~/Projects/ds4cc-marketplace/burnerchrome', '~/Projects/ds4cc-marketplace/speedrun']
pinned 55 observed 63   (55 - 4 + 12 = 63)
```

Impacted claim: C1 "pins.pathsMissSet equals the observed missSet". Smallest fix: the re-pin in draft §2 (remove the 4 recovered tokens; add the 12 newMissing tokens, each only after its round-24 receipt observes it absent; set `round` 24 and `updated` 2026-10-21 in `corpus/knowledge/freshness-pins.json`). Not done here; lane production files are read-only for this seat.

Recovered tokens (exact state observed by `stat`/`test -e`): `~/Projects/ds4cc-marketplace` present, `.../CNAME` present (content `ds4cc.com`, 9 bytes), `.../burnerchrome` present, `.../speedrun` present. All 15 other population targets (T01 to T15) are absent.

### F2 — P2 (freshness, measured): a restoration note with an absence word creates a false green

The paths gate applies its absence regex to a ±2-line window around every cite (`scripts/freshness-sweep.mjs:317-336`). Fixture reproduction (scratch dir `fixture-*` under the tmp root; copies, no git):

```
== bleed-plain             (restoration line without absence word)
exit=1
drift [('~/Projects/zz-r24-fixture-missing/a.md', ['corpus/knowledge/doc.md:4'])]
declaredAbsent []
== bleed-with-absence-word (restoration line contains "gone", two lines above the miss cite)
exit=0
drift []
declaredAbsent [('~/Projects/zz-r24-fixture-missing/a.md', ['corpus/knowledge/doc.md:4'])]
```

Impacted claim: C1 "every unannotated cite carries a dated absence annotation" is satisfied by accident. Smallest fix: the C1 counter (`measure_c1`) rejects any restoration note containing an absence word, and the sweep selftest gets this fixture as a case. No restoration note has been written yet; this finding is preventive.

### F3 — P2 (operability/freshness): sidecar predicate as briefed checks less than the contract

The executor brief for the sidecar (`ExecSweepSidecar`, `.ufo/waves/round-24/w1-taskcall.json`) checks: non-author file, token on the line, line sha256 matches, note matches the absence regex. The contract additionally requires, for every absence annotation: the date `2026-10-21`, the event, and the phrase `historical record, not an executable instruction`. The brief does not check these. Smallest fix: the round-24 counter `measure_c1` checks all three for every `absent` entry and every inline absence annotation. The sweep keeps the predicate as briefed.

### F4 — P2 (freshness): armed pins for the ds4cc tree were not evaluated

`pins.pq2Dir` / `pq2Remote` (`e6bd071…`) / `pq2Unpushed` (20) describe the tree as it was before the reappearance. The PQ-2 check runs `git ls-remote origin main` (network) and `rev-list --count origin/main..HEAD`. The local count now is 0 (`git -C ~/Projects/ds4cc-marketplace rev-list --count origin/main..HEAD` → `0`). I did not run `ls-remote` (network read outside this seat's bounds), so whether the remote moved is undetermined. Smallest fix: the integrating seat runs `node scripts/freshness-sweep.mjs --section=armed` once and records the PQ-2 verdict before re-pinning `pq2*`.

### F5 — P3 (freshness, informational): `projectsChildrenSet` drifted outside the population

`projectsChildrenDelta.added` = `BTVREV, TPSnCONC, audio-shokunin-publish, ds4cc-marketplace, gkeep, kaidoku-r21-battery, kaidoku-r21-compare, kaidoku-r21-coverage, kimi-code, xsnapshot` (10 added, 0 removed). These are outside the 19-target population and the sweep never gates on them. Not re-pinned, per draft §2 rule 5. Smallest fix: a separate receipt-backed decision in a later round.

### F6 — P3 (process disclosure): one git call in a domain tree that is not strictly read-only

I ran `git -C ~/Projects/ds4cc-marketplace status --porcelain=v1` once (output discarded). `git status` can refresh `.git/index`. Afterwards `.git` shows mtime `2026-10-21T08:43:26` (local -03). I changed no tracked file and made no commit, stage or checkout. The `.git` mtime change is mine. Other git calls in that tree were `log`, `rev-parse`, `remote -v`, `branch --show-current`, `rev-list --count`, `ls-tree`, `ls-files --error-unmatch`.

### F7 — P3 (implementation hint for the executor): corpus-contract predicate is broader

`scripts/corpus-contract.mjs:73` uses `EXCLUDE_RE = /verifier|aggregator|operator/i`. The brief's "reuse the predicate" would also exclude any `operator-*` lesson. The contract's non-author set is the two globs only. Both predicates give the same result on all 10 non-author lessons present in the corpus (listed under Checked and held), so this does not change C1 today. Use the explicit globs.

## Draft: appended section for `corpus/knowledge/freshness-sweep.md`

Insert after the current last line (188). Tested in a fixture copy: the paths gate result did not change except for the sidecar example line, which is self-annotated (see Checked and held).

````markdown

## Round-24 reconciliation and sidecar

Scope: the paths gate of `node scripts/freshness-sweep.mjs --section=paths` on 2026-10-21. Population: `.ufo/waves/round-24/c1-population.json` (19 targets: 3 drift, 12 newMissing, 4 recovered). Round-open snapshot: `.ufo/waves/round-24/paths-before.json` (exit 1). The rules below are the operating rules; the numbers belong to the round that records them.

### 1. The 2026-10-21 ds4cc-marketplace reappearance (stale pinned misses)

- The directory `~/Projects/ds4cc-marketplace` has birth time 2026-10-21 05:19:01 -03. Its `CNAME` (born 05:19:05 -03) reads `ds4cc.com`. Its `origin` is `https://github.com/VeigaPunk/ds4cc-marketplace.git`, and `origin/main` is `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (committed 05:51:24 -03). The cause of the reappearance was not observed; its event is recorded as `unknown`.
- The round-23 receipts under `.ufo/waves/round-23/receipts/` were written between 04:23 and 04:58 -03, before the directory existed. Their absence observations were correct for that time. They stay historical; they are no longer the current state of this tree.
- Four pinned misses in `corpus/knowledge/freshness-pins.json` (`pins.pathsMissSet`) are now stale: `~/Projects/ds4cc-marketplace`, `~/Projects/ds4cc-marketplace/CNAME`, `~/Projects/ds4cc-marketplace/burnerchrome`, `~/Projects/ds4cc-marketplace/speedrun` (population T16 to T19). The sweep reports them under `setDelta.recovered`. Recovery is informational, so it never fails the gate by itself.
- Arithmetic at observation: observed miss set 63 (60 declaredAbsent + 3 drift); pinned set 55; newMissing 12; recovered 4; 55 - 4 + 12 = 63.
- The armed pins for this tree (`pq2Dir`, `pq2Remote`, `pq2Unpushed`, PQ-2) were written against the pre-reappearance tree. The PQ-2 check needs `git ls-remote origin main`, a network read, so it is not evaluated by the paths section. Run `--section=armed` before trusting those pins.

### 2. Re-pin rule

1. Only targets observed in this round by a receipt may change `pins.pathsMissSet`. A pinned miss observed `present` is removed (re-arm). A newMissing token observed `absent` with every cite annotated is added.
2. Drift tokens are never re-pinned to hide unannotated cites. A drift token is already pinned; its unannotated cites are fixed by annotation (lane-authored files inline, non-author files through the sidecar). This is the round-20 rule: do not re-pin existing misses to hide newly visible unannotated occurrences.
3. The pin must equal the observed miss set after the corrections, with the same set on both sides: `pathsMissSet` = `declaredAbsent` plus `drift` (63 entries here).
4. Re-pin stamp: `round` 24 and `updated` 2026-10-21, in the same commit as the corrected prose.
5. Informational sets are outside this rule. `projectsChildrenSet` shows 10 added children under `~/Projects` (including `ds4cc-marketplace`); it is recorded, not re-pinned, because no round-24 receipt covers it.
6. A removed recovered token that vanishes again becomes a newMissing (exit 1) until a receipt re-pins it. That is the re-arm.

### 3. Restoration corrections (no absence words)

A lane-authored cite of a recovered token gets an appended restoration note. The 25 distinct lane-authored cite lines are the population's recovered cites (T16 to T19). The non-author cite (`corpus/lessons/round-1-aggregator-audit.md:30`) uses the sidecar `restored` kind instead.

Required form, appended at the end of the line (or inside the row as an HTML comment):

```
<!-- r24 restoration 2026-10-21: ~/Projects/ds4cc-marketplace/CNAME observed present (CNAME reads "ds4cc.com", 9 bytes; directory birth 05:19 -03). The earlier clause on this line stays historical/unverified for the restored tree. -->
```

Rules:
- Must contain none of: `absent`, `gone`, `vanished`, `emptied`, `no longer`, `dangling`, `no such file`, `never published`, `missing` (case-insensitive, so `newMissing` counts too). The paths gate applies its absence regex to a +/-2-line window around every cite, so a restoration note with an absence word silently annotates other cites of missing tokens near it.
- Measured side effect: in a fixture, a note containing `gone` two lines above an unannotated miss cite changed the result from exit 1 (drift for the fixture token, unannotated at `doc.md:4`) to exit 0 (that token moved to `declaredAbsent`), with no pin changed.
- Must start with `*[r24 restoration 2026-10-21:` or `<!-- r24 restoration 2026-10-21:`, name what was observed present, and say which part of the earlier line stays historical or unverified.
- Append only. Existing text stays, including the r18 and r20 absence notes on those lines. They become stale for a present token, and the restoration note records that.

### 4. Non-author sidecar (schema `kake-paths-sidecar-v1`)

Non-author files are `corpus/lessons/*aggregator*.md` and `corpus/lessons/*verifier-spotcheck*.md`. They are never edited. Their citations are annotated through `corpus/knowledge/freshness-sidecar.json`, which binds each entry to the exact line bytes.

Shape (the executor defines the top-level wrapper; the entry fields are fixed by this section):

```json
{"schema":"kake-paths-sidecar-v1","entries":[{"file":"corpus/lessons/round-6-aggregator-audit.md","line":48,"token":"~/Projects/webzites/scripts/kimi-surface.mjs","lineSha256":"<64 lowercase hex>","kind":"absent","date":"2026-10-21","note":"absent since the 2026-10-12 ~/Projects prune/migration (event per the r20 citation-local note at corpus/knowledge/free-read-verbs.md:325, not re-derived here); historical record, not an executable instruction."}]}
```

- `file`: lane-relative path. `line`: 1-based line number. `token`: the canonical `~` spelling, exactly as it occurs on that line.
- `lineSha256`: lowercase hex SHA-256 of the UTF-8 bytes of the line text, without the newline.
- `kind`: `absent` or `restored`. `date`: `YYYY-MM-DD`. `note`: free text.

Rules:
1. An `absent` entry annotates (file, line, token) only if the file is non-author, the token occurs on that line, the line's current SHA-256 equals `lineSha256`, and `note` matches the absence regex.
2. A `restored` entry is informational. It is printed and never changes the exit code.
3. A malformed sidecar, an unknown schema, a missing field, or an entry for a lane-authored file exits 2 (fail closed).
4. A changed line breaks its binding. The annotation then no longer applies, the cite is unannotated, and the gate exits 1. This is intended. The sweep should print the reason ("sidecar sha mismatch") so the cause is visible.
5. Sidecar annotations are exact: one file, one line, one token. They never use the +/-2-line window, so they cannot bleed into neighbouring cites.
6. Absence notes keep the round-20 style: the date, the event (or `unknown`), and the phrase `historical record, not an executable instruction`. The sweep checks only the absence regex. The date, event, and phrase are checked by the round-24 counter `measure_c1`, not by the sweep.

### 5. Checks for the integrating seat (not run by the scribe)

- `node scripts/freshness-sweep.mjs --section=paths`: expect exit 0 after the annotations land, the 12 new misses are pinned, and the 4 recovered tokens are removed.
- `node scripts/freshness-sweep.mjs --selftest`: must stay green with the sidecar cases added.
- `python3 .ufo/waves/round-24/measure_c1.py --root . --revision <commit>`.
- `node scripts/freshness-sweep.mjs --section=armed`: re-evaluate PQ-2 against the reappeared tree before trusting the armed pins.

### 6. Limits

- Filesystem truth at the observation time. A later restore or prune is new drift for a later round.
- The cause of the 2026-10-21 reappearance was not observed.
- The armed section was not run. It needs network reads.
- Restoration of domain trees is operator-owned and was not attempted.
````

## Checked and held

- Population states, observed by `test -e` / `stat` / `cat` on 2026-10-21 (read-only):
  - Absent (15): T01 `~/Projects/plazir-15-site`; T02 `~/Projects/webzites/bin/webzites.mjs`; T03 `~/Projects/webzites/scripts/kimi-surface.mjs`; T04 `~/Projects/lucario/site/README.md`; T05 `~/Projects/plazir-15-site/.github/workflows/pages.yml`; T06 `~/Projects/plazir-15-site/speedrun`; T07 `~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs`; T08 `.../fleet/vault-properties.json`; T09 `~/Projects/shokunin/kake-shokunin/kimi-surface.mjs`; T10 `~/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review`; T11 `~/Projects/webzites/agents/webzites-speedrun.md`; T12 `~/Projects/webzites/fleet/grokbots.json`; T13 `~/Projects/webzites/repos/ds4cc-marketplace`; T14 `~/Projects/webzites/state/probe-latest.json`; T15 `~/Projects/webzites/state/rebuild-charter-fire.log`. (`~/Projects/webzites` itself is absent.)
  - Present (4): T16 `~/Projects/ds4cc-marketplace`; T17 `.../CNAME`; T18 `.../burnerchrome`; T19 `.../speedrun`.
- Birth times: `stat -c '%n birth=%w mtime=%y' Projects/ds4cc-marketplace Projects/ds4cc-marketplace/CNAME` → `birth=2026-10-21 05:19:01.033916520 -0300` and `birth=2026-10-21 05:19:05.036234032 -0300`. `burnerchrome` 05:19:05.038621636, `speedrun` 05:19:05.120101209.
- `origin/main` = `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`, `log -1` → `2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 …`. `remote -v` origin = `https://github.com/VeigaPunk/ds4cc-marketplace.git`.
- Round-23 receipt timestamps: `.ufo/waves/round-23/receipts/*.json` mtimes 04:23:36 to 04:58:19 -03, all before the 05:19:01 birth. `property-map.json` `observedAt` = `2026-10-21`.
- Pin arithmetic: pinned `pathsMissSet` 55 entries (`corpus/knowledge/freshness-pins.json`); observed `declaredAbsent` ∪ `drift` = 63; `newMissing` = 12 (exactly T04–T15 tokens); `recovered` = 4 (exactly T16–T19 tokens).
- Draft in fixture (`/tmp/kake-r24-ScribeFreshnessKnowledge-Nc0g/fixA` vs `fixB`, `fixB` = corpus copy + draft appended): both exit 1. `counts` identical except none. `newMissing` identical (12). `recovered` identical. `drift` identical (3 targets, same unannotated cites). Only cite-set change: `~/Projects/webzites/scripts/kimi-surface.mjs` gains `corpus/knowledge/freshness-sweep.md:234` (the sidecar example line, annotated by its own `absent` word). Before the fix to the draft, an unannotated fixture path in the draft prose produced `newMissing` 13 vs 12; that cite was removed.
- Restoration template and absence-word list: the restoration template contains no word from `ABSENT_RE` (`/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i`).
- Non-author set: `corpus/lessons/*aggregator*.md` and `*verifier-spotcheck*.md` match 10 files: round-1-aggregator-audit, round-20-verifier-spotcheck, round-21-verifier-spotcheck, round-22-verifier-spotcheck, round-4-aggregator-audit, round-5-aggregator-audit, round-5-aggregator-mirror-pathless-cli-invocation, round-6-aggregator-audit, round-8-aggregator-box3-coldrun, round-9-aggregator-corpus-verdict. Population non-author cites: `round-6-aggregator-audit.md:48` (T03, unannotated → sidecar `absent`); `round-1-aggregator-audit.md:30` (T17, recovered → sidecar `restored`); `round-4-aggregator-audit.md:31,32`, `round-5-aggregator-mirror-pathless-cli-invocation.md:11,13`, `round-6-aggregator-audit.md:145` (annotated already).
- Lane-authored unannotated cites (for the inline annotations, not in this seat's scope): `corpus/knowledge/drift-detection.md:77` (table row, needs an HTML-comment form), `corpus/knowledge/fleet-registry.md:57`, `corpus/knowledge/free-read-verbs.md:321`.
- Lane-authored recovered cites (restoration list, 25 distinct lines): T16 `SKILL.md:16,19,364,445,448,449,450`, `corpus/knowledge/fleet-registry.md:49,50,64`, `corpus/knowledge/origin-repos.md:11,19,70`, `corpus/knowledge/publish-channels.md:69`, `corpus/lessons/round-18.md:55`; T18 `SKILL.md:20,423,431`, `corpus/knowledge/fleet-registry.md:51,66`; T19 `corpus/knowledge/mirror-pitfalls.md:63`, `corpus/knowledge/speedrun-pipeline.md:1,3,13,78`. Several of these lines say `absent` about this tree in prose (for example `SKILL.md:423`, round-23 correction), and those statements are now stale for a present token.
- `scripts/freshness-sweep.mjs` ABSENT_RE (`:122`) and window logic (`annotate`, `:314-338`): read and confirmed by the fixture above.
- `scripts/corpus-contract.mjs:73` EXCLUDE_RE (`/verifier|aggregator|operator/i`) differs from the contract's glob set; no population file is affected (F7).
- Sidecar file `corpus/knowledge/freshness-sidecar.json` does not exist yet; the scan covers `SKILL.md` and `corpus/**/*.md` only (`scanCitations`, `:346-357`), so a JSON sidecar adds no `pathsFiles` change.
- P1 scan set: the draft's own cites are present tokens (`~/Projects/ds4cc-marketplace/CNAME`, `~/Projects`) or the self-annotated sidecar example. No other missing-token cite appears in the draft.

## Limits

- Observations are filesystem and git reads at 2026-10-21T11:46Z. They are not a measurement of a later state.
- The cause of the ds4cc reappearance is unobserved. The event field is `unknown` in the draft. I did not query the remote (no `ls-remote`), so whether the origin remote changed is undetermined.
- The draft describes the sidecar and the counter as designed by the briefs (`ExecSweepSidecar`, `ExecPathsCounter`). Neither exists in the lane yet; their behaviour is not verified. The draft's claims about them are requirements, not results.
- The draft's top-level sidecar wrapper (`{"schema":…,"entries":[…]}`) is my choice; the brief names only the entry fields.
- The fixtures are plain copies under `/tmp`, not git clones. No commit was needed for this seat, so no clone HEAD is recorded.
- I did not run the sweep's `--selftest`, `--section=armed`, or `--section=history`. The armed section performs network reads and was outside this seat's bounds.
- Restoration of domain trees (ds4cc, plazir, webzites) is operator-owned. Nothing was restored.

## Tooling

No tools were installed or upgraded. Used existing binaries only: `node` (sweep, read-only `--section=paths --json`), `git` (read-only subcommands, see F6), `python3` (JSON reads), `stat`/`test`/`cat`, and the fixture copies. `pacman` was not invoked.
