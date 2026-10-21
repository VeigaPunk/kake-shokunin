# Round 24 axis-harm pre-mortem and gate baseline

## Verdict

Recorded the requested baseline in a no-hardlinks clone pinned to the frozen base. Baseline is not an all-green set: `paths` is expected to fail at the round-24 open state; `history` exits 0 while explicitly suspended; `armed` below was run offline and exits 0 only as a partial, non-pass. The remaining measured gates pass at this base.

The full online `armed` section was not run: the lane bounds allow only read-only GET/HEAD of public documentation pages, while that section would fetch live publication surfaces and run `git ls-remote`. I ran its `--offline` mode so no such requests occurred; it cannot establish the online result.

## Findings

- **P1 — C1/freshness regression surface is broader than the 19-target receipt population.** Exact baseline: `node scripts/freshness-sweep.mjs --section=paths --repo=/tmp/kake-r24-CritAxisHarm-XFWF/clone` exits 1 with 3 unannotated drifts, 12 misses absent from `pins.pathsMissSet`, and 4 recovered targets; it scanned 55 files / 531 occurrences / 92 unique tokens. The round-24 counter's 19 targets are not the complete set of the sweep's cited-path tokens. A new citation or a restoration note containing an absence word can affect unrelated nearby citations and change the sweep result. **Impacted:** C1 / freshness. **Smallest safe correction:** preserve cite-local annotations (especially absence-free restoration corrections), reconcile the pinned miss set from observed misses, and compare the full paths section after integration—not only the 19 receipts.
- **P1 — Zero exit is not equivalent to complete freshness coverage.** Exact baseline outputs below show history `SUSPENDED` by `probeHistoryAbsent` and armed `skipped(offline)`, each returning exit 0. The armed invocation is also explicitly partial. **Impacted:** freshness/operability interpretation. **Smallest safe correction:** L1 must treat the emitted suspended/skipped/`complete=false` states as incomplete, not as green coverage; keep the full online armed comparison explicitly held until allowed.
- **P2 — Round-23 counters are historical authorities, not the round-24 acceptance counter.** At the frozen revision the old C1 runner reports 17/17 accepted and the old C2 runner 12/12; these results do not test the new 19-path C1 population or malformed-case C2 matrix. **Impacted:** C1 freshness and C2 operability. **Smallest safe correction:** preserve round-23 runner bytes and use the round-24 counters/populations for round-24 acceptance; compare these baseline counts only as regression checks on historical artifacts.
- **P2 — Corpus and publisher regression guards are distinct.** `corpus-contract` passes at 22 knowledge / 18 lesson files, but a new lane-authored round lesson still needs a non-empty `## Gate`, and a new knowledge pointer needs the provenance trio. `canonical_audit --selftest` and the frozen round-22 matrix pass independently; changes to receipt replay should not redefine the publisher-policy oracle or case set. **Impacted:** C2 operability and publishing gate. **Smallest safe correction:** keep `receipt_replay.py` and its pointer isolated from `canonical_audit.py` / the frozen matrix; satisfy corpus shape when adding the pointer/lesson.

## Checked and held

Clone: `git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-CritAxisHarm-XFWF/clone`, then detached checkout of the frozen base. Observed `git rev-parse HEAD` output:

```text
f7de3ab4e9f030a15a857a5a08631bd8e690f436
```

All commands below ran against that clone. Where shown, `[exit N]` is the wrapper's captured exit status after the command. `TMPDIR` / `KAKE_SELFTEST_DIR` keep selftest scratch under `/tmp/kake-r24-CritAxisHarm-XFWF`.

### 1. Corpus shape gate

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
node scripts/corpus-contract.mjs --json; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```json
{"tool":"corpus-contract","contract":"S019","root":"/tmp/kake-r24-CritAxisHarm-XFWF/clone","ok":true,"code":0,"counts":{"knowledgeChecked":22,"lessonsChecked":18,"skipped":10},"findings":[],"skipped":[{"file":"corpus/lessons/round-1-aggregator-audit.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-20-verifier-spotcheck.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-21-verifier-spotcheck.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-22-verifier-spotcheck.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-4-aggregator-audit.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-5-aggregator-audit.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-5-aggregator-mirror-pathless-cli-invocation.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-6-aggregator-audit.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-8-aggregator-box3-coldrun.md","reason":"not-lane-author"},{"file":"corpus/lessons/round-9-aggregator-corpus-verdict.md","reason":"not-lane-author"}],"errors":[]}

[exit 0]
```

### 2. Freshness sweep selftest

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
KAKE_SELFTEST_DIR=/tmp/kake-r24-CritAxisHarm-XFWF/selftest TMPDIR=/tmp/kake-r24-CritAxisHarm-XFWF node scripts/freshness-sweep.mjs --selftest; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```text
freshness-sweep --selftest
fixtures: /tmp/kake-r24-CritAxisHarm-XFWF/selftest (hermetic; re-runnable)
  PASS  a annotated-missing -> declaredAbsent, exit-neutral
        expect: exit 0 · declaredAbsent contains selftest-missing.md · drift [] · resolve contains selftest-present.md
        got:    exit 0 · declaredAbsent ["~/Projects/webzites/selftest-missing.md"] · drift [] · resolve ["~/.kake-freshness-selftest-921900/selftest-present.md"]
  PASS  b unannotated-missing -> drift, exit 1
        expect: exit 1 · drift contains selftest-gone.md
        got:    exit 1 · drift ["~/Projects/webzites/selftest-gone.md"]
  PASS  f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent
        expect: exit 0 · declaredAbsent contains selftest-unrelated.md · drift [] — spec-mandated window semantics
        got:    exit 0 · declaredAbsent ["~/Projects/webzites/selftest-unrelated.md"] · drift []
  PASS  g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict)
        expect: exit 1 · setDelta.newMissing contains selftest-missing.md · drift []
        got:    exit 1 · newMissing ["~/Projects/webzites/selftest-missing.md"] · drift []
  PASS  h1 spec-literal ±2 window: trailing annotation -> declaredAbsent, exit 0
        expect: exit 0 · declaredAbsent has trailing+named · drift []
        got:    exit 0 · declaredAbsent ["~/Projects/webzites/selftest-named.md","~/Projects/webzites/selftest-trailing.md"] · drift []
  PASS  h2 strict pin (pathsAbsenceStrictSameLine): unnamed trailing annotation -> drift, exit 1
        expect: exit 1 · drift has trailing · declaredAbsent has named · evidence.direct/mentions recorded
        got:    exit 1 · drift ["~/Projects/webzites/selftest-trailing.md"] · declaredAbsent ["~/Projects/webzites/selftest-named.md"]
  PASS  m cross-citation leak -> drift, exit 1; annotated dup control stays declaredAbsent
        expect: exit 1 · canonical leak target · unannotatedCites ['SKILL.md:3'] · cites lists both locations · annotated duplicate stays declaredAbsent
        got:    exit 1 · drift [["~/Projects/webzites/selftest-leak.md",["SKILL.md:3","corpus/knowledge/note.md:1"],["SKILL.md:3"]]] · declaredAbsent [["~/Projects/webzites/selftest-dup.md",["SKILL.md:6","corpus/knowledge/note.md:3"]]]
  PASS  c malformed JSONL -> exit 2
        expect: exit 2 · error names malformed JSONL
        got:    exit 2 · stderr/stdout "{\n  \"generatedAt\": \"2026-10-21T11:44:00Z\",\n  \"node\": \"v24.21.0\",\n  \"repoRoot\": \"/tmp/kake-r24-CritAxisHarm-XFWF/clone\",\n"
  PASS  j probeHistoryAbsent + canonical default missing -> SUSPENDED, exit 0
        expect: exit 0 · historySuspended true · file is selftest-rebound canonical
        got:    exit 0 · suspended true · file /tmp/kake-r24-CritAxisHarm-XFWF/selftest/canonical-absent-history.jsonl
  PASS  k probeHistoryAbsent + explicit missing KAKE_PROBE_HISTORY -> exit 2 (fail-closed)
        expect: exit 2 · error cannot read · not historySuspended
        got:    exit 2 · suspended undefined · error cannot read /tmp/kake-r24-CritAxisHarm-XFWF/selftest/explicit-missing-history.jsonl
  PASS  l probeHistoryAbsent pin is known/consumed (not listed unused)
        expect: pins._unused excludes probeHistoryAbsent
        got:    unused []
  PASS  i malformed pins JSON -> exit 2 (never silent defaults)
        expect: exit 2 · stderr names pins file invalid and parse error
        got:    exit 2 · "freshness-sweep: pins file invalid — /tmp/kake-r24-CritAxisHarm-XFWF/selftest/bad-pins.json: Unexpected end of JSON input"
  PASS  d unknown flag -> exit 64
        expect: exit 64
        got:    exit 64 · "freshness-sweep: unknown flag: --bogus-flag"
  PASS  e write-API call sites confined to SELFTEST-WRITES region
        expect: 0 call sites outside balanced region(s)
        got:    0 outside · errors 0 (regions B1154,E1225,B1515,E1517)
  PASS  e2 write confinement mutation proof (in memory)
        expect: every out-of-region top-level function mutant caught; every covered API name caught; marker errors, anchoring and identifier boundary pinned; positive/decoy controls pass
        got:    caught 26/26 mutants · apis 31/31 pin=match · regions B1154,E1225,B1515,E1517 · controls positive=PASS decoy=PASS unbalanced=error nested=error loneEnd=error junkMarker=rejected suffix=clean inSelftest=yes
selftest: 15/15 passed

[exit 0]
```

### 3. Freshness `paths`

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
node scripts/freshness-sweep.mjs --section=paths --repo=/tmp/kake-r24-CritAxisHarm-XFWF/clone; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```text
freshness-sweep — kake-shokunin freshness axis
generated 2026-10-21T11:43:59Z · node v24.21.0 · repo /tmp/kake-r24-CritAxisHarm-XFWF/clone
pins: file /tmp/kake-r24-CritAxisHarm-XFWF/clone/corpus/knowledge/freshness-pins.json (round 18, updated 2026-10-14)
pins not evaluated by this instrument (informational): charterGhpDeploy, plazirUrl, vaultBytes, vaultSha, vaultUrlBearing, vaultDeadLinks, fleetSites, fleetStatus, grokbotsRows, reposClones
§paths  55 files · 531 occurrences · 92 unique tokens
  resolve 19 · declaredAbsent 60 · drift 3 · unresolved 10
  !! DRIFT 3 cited path(s) missing with unannotated citation(s):
     ~/Projects/plazir-15-site  (2 of 19 cites unannotated: corpus/knowledge/drift-detection.md:77, corpus/knowledge/fleet-registry.md:57)
     ~/Projects/webzites/bin/webzites.mjs  (1 of 16 cites unannotated: corpus/knowledge/free-read-verbs.md:321)
     ~/Projects/webzites/scripts/kimi-surface.mjs  (1 of 28 cites unannotated: corpus/lessons/round-6-aggregator-audit.md:48)
  declaredAbsent  ~/.config/systemd/user/webzites-keeper.service  SKILL.md:342 (+3)
  declaredAbsent  ~/.config/systemd/user/webzites-keeper.timer  SKILL.md:342 (+6)
  declaredAbsent  ~/.config/systemd/user/webzites-probe.service  SKILL.md:342 (+1)
  declaredAbsent  ~/.config/systemd/user/webzites-probe.timer  SKILL.md:342 (+2)
  declaredAbsent  ~/.grok/agents/grokbot-lucario.md  SKILL.md:27 (+1)
  declaredAbsent  ~/.local/bin/grokbot-lucario  SKILL.md:27 (+1)
  declaredAbsent  ~/DIRMAP.md  SKILL.md:311 (+5)
  declaredAbsent  ~/Projects/bounties  corpus/knowledge/publish-queue.md:218 (+1)
  declaredAbsent  ~/Projects/ephemeral/wz1  SKILL.md:118 (+1)
  declaredAbsent  ~/Projects/ephemeral/wz1/ds4cc  corpus/knowledge/publish-channels.md:21 (+2)
  declaredAbsent  ~/Projects/lucario  SKILL.md:26 (+4)
  declaredAbsent  ~/Projects/lucario/site  SKILL.md:27 (+3)
  declaredAbsent  ~/Projects/lucario/site/README.md  SKILL.md:458
  declaredAbsent  ~/Projects/origin-work/charter-ufo-fsd  SKILL.md:18 (+6)
  declaredAbsent  ~/Projects/origin-work/open-bug-bounties  corpus/knowledge/publish-queue.md:237 [indirect: "vanished" @238, no token mention]
  declaredAbsent  ~/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl  corpus/knowledge/keeper-timer-inert.md:118 (+2)
  declaredAbsent  ~/Projects/plazir-15-site/.github/workflows/pages.yml  SKILL.md:461
  declaredAbsent  ~/Projects/plazir-15-site/speedrun  corpus/knowledge/mirror-pitfalls.md:63 [indirect: "absent" @64, no token mention]
  declaredAbsent  ~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs  corpus/knowledge/vault-properties.md:100
  declaredAbsent  ~/Projects/shokunin/kake-shokunin/fleet/vault-properties.json  corpus/knowledge/vault-properties.md:100
  declaredAbsent  ~/Projects/shokunin/kake-shokunin/kimi-surface.mjs  corpus/knowledge/vault-properties.md:100
  declaredAbsent  ~/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review  corpus/knowledge/mirror-pitfalls.md:64
  declaredAbsent  ~/Projects/ufofsdbeta  SKILL.md:50 (+1) [indirect: "absent" @48, no token mention]
  declaredAbsent  ~/Projects/ufofsdbeta-kimi-review  SKILL.md:51 (+2)
  declaredAbsent  ~/Projects/ufofsdbeta/.ufo  SKILL.md:371 (+1)
  declaredAbsent  ~/Projects/webzites  SKILL.md:333 (+17)
  declaredAbsent  ~/Projects/webzites/agents/webzites-speedrun.md  corpus/knowledge/speedrun-pipeline.md:77
  declaredAbsent  ~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md  SKILL.md:157 (+5)
  declaredAbsent  ~/Projects/webzites/fleet/fleet.config.json  SKILL.md:30 (+11)
  declaredAbsent  ~/Projects/webzites/fleet/fleet.dedupe-report.md  corpus/knowledge/publish-queue.md:288 (+1)
  declaredAbsent  ~/Projects/webzites/fleet/grokbots.json  SKILL.md:429
  declaredAbsent  ~/Projects/webzites/fleet/kimi-surface-ops.md  corpus/knowledge/publish-channels.md:54 (+1)
  declaredAbsent  ~/Projects/webzites/package.json  corpus/lessons/round-5-aggregator-mirror-pathless-cli-invocation.md:13
  declaredAbsent  ~/Projects/webzites/reports  corpus/lessons/round-6-aggregator-audit.md:81
  declaredAbsent  ~/Projects/webzites/reports/dead-slot-recreate-readiness-r9.md  SKILL.md:282
  declaredAbsent  ~/Projects/webzites/reports/keepers  corpus/knowledge/keeper-timer-inert.md:18 (+1)
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r1.md  corpus/knowledge/origin-repos.md:1 (+3)
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r2.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r3.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r4.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r5.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r6.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r7.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/repos-r8.md  corpus/lessons/round-5.md:5
  declaredAbsent  ~/Projects/webzites/reports/keepers/speedrun-r1.md  corpus/knowledge/speedrun-pipeline.md:77 (+1)
  declaredAbsent  ~/Projects/webzites/reports/r9-publish-queue.md  corpus/knowledge/publish-queue.md:288 (+3)
  declaredAbsent  ~/Projects/webzites/reports/r9-stale-markers.md  corpus/README.md:83
  declaredAbsent  ~/Projects/webzites/repos  corpus/knowledge/origin-repos.md:3 (+6)
  declaredAbsent  ~/Projects/webzites/repos/ds4cc-marketplace  corpus/knowledge/origin-repos.md:82
  declaredAbsent  ~/Projects/webzites/scripts  corpus/lessons/round-10.md:41 [indirect: "absent" @43, no token mention]
  declaredAbsent  ~/Projects/webzites/src/cli.mjs  corpus/knowledge/free-read-verbs.md:1 (+5)
  declaredAbsent  ~/Projects/webzites/src/fleet.mjs  corpus/knowledge/free-read-verbs.md:1 (+1)
  declaredAbsent  ~/Projects/webzites/src/probe.mjs  corpus/knowledge/drift-detection.md:7 (+5)
  declaredAbsent  ~/Projects/webzites/src/reconcile.mjs  corpus/knowledge/free-read-verbs.md:1 (+8)
  declaredAbsent  ~/Projects/webzites/src/speedrun.mjs  corpus/knowledge/speedrun-pipeline.md:1 (+4)
  declaredAbsent  ~/Projects/webzites/state  corpus/knowledge/fire-journal-codes.md:84 (+5)
  declaredAbsent  ~/Projects/webzites/state/probe-history.jsonl  corpus/knowledge/ops-automation.md:136 (+9)
  declaredAbsent  ~/Projects/webzites/state/probe-latest.json  corpus/knowledge/ops-automation.md:141
  declaredAbsent  ~/Projects/webzites/state/rebuild-charter-fire.log  corpus/knowledge/fire-journal-codes.md:86
  declaredAbsent  ~/projects  SKILL.md:308 (+13)
  unresolved (not existsSync-checkable): ~/ [placeholder] · ~/.config/systemd/user/webzites-*.timer [glob] · ~/.grok/agents/grokbot- [placeholder] · ~/Projects/**/ufofsdbeta-kimi-review [glob] · ~/Projects/webzites/reports/dead-slot- [placeholder] · ~/Projects/webzites/reports/keepers/grokbot-*.log.md [glob] · ~/Projects/webzites/state/rebuild-*.json [glob] · ~/Projects/webzites/state/recreate-*.json [glob] · ~/Projects/webzites/state/recreate-plazir15-*.json [glob] · ~/Projects/webzites/state/update-*.json [glob]
  citation base: 92 targets · missSet 63 · files 55
  relative-form cites (outside PATH_RE, not resolve-checked): 856 — e.g. SKILL.md:27 fleet/grokbots.json · SKILL.md:34 fleet/grokbots.json · SKILL.md:36 src/cli.mjs · SKILL.md:42 src/cli.mjs · SKILL.md:43 src/cli.mjs
  set-delta miss: !! NEW MISS ~/Projects/lucario/site/README.md · ~/Projects/plazir-15-site/.github/workflows/pages.yml · ~/Projects/plazir-15-site/speedrun · ~/Projects/shokunin/kake-shokunin/fleet/kimi-surface.mjs · ~/Projects/shokunin/kake-shokunin/fleet/vault-properties.json · ~/Projects/shokunin/kake-shokunin/kimi-surface.mjs · ~/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review · ~/Projects/webzites/agents/webzites-speedrun.md · ~/Projects/webzites/fleet/grokbots.json · ~/Projects/webzites/repos/ds4cc-marketplace · ~/Projects/webzites/state/probe-latest.json · ~/Projects/webzites/state/rebuild-charter-fire.log · recovered: ~/Projects/ds4cc-marketplace · ~/Projects/ds4cc-marketplace/CNAME · ~/Projects/ds4cc-marketplace/burnerchrome · ~/Projects/ds4cc-marketplace/speedrun
  set-delta files: +15 / -0 — added: corpus/QUALITY.md · corpus/SOURCES.md · corpus/knowledge/crawl-scope-per-host.md · corpus/knowledge/ghp-custom-domain.md · corpus/knowledge/ghp-etag-anatomy.md · corpus/knowledge/ghp-served-set.md · corpus/knowledge/static-canonical-preflight.md · corpus/lessons/round-19-recensus.md · corpus/lessons/round-20-verifier-spotcheck.md · corpus/lessons/round-20.md · corpus/lessons/round-21-verifier-spotcheck.md · corpus/lessons/round-21.md · corpus/lessons/round-22-verifier-spotcheck.md · corpus/lessons/round-22.md · corpus/lessons/round-23.md
  ~/Projects children: 24 (informational) — added: BTVREV · TPSnCONC · audio-shokunin-publish · ds4cc-marketplace · gkeep · kaidoku-r21-battery · kaidoku-r21-compare · kaidoku-r21-coverage · kimi-code · xsnapshot
VERDICT: DRIFT — §paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet (exit 1)

[exit 1]
```

### 4. Freshness `history`

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
node scripts/freshness-sweep.mjs --section=history --repo=/tmp/kake-r24-CritAxisHarm-XFWF/clone; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```text
freshness-sweep — kake-shokunin freshness axis
generated 2026-10-21T11:43:59Z · node v24.21.0 · repo /tmp/kake-r24-CritAxisHarm-XFWF/clone
pins: file /tmp/kake-r24-CritAxisHarm-XFWF/clone/corpus/knowledge/freshness-pins.json (round 18, updated 2026-10-14)
pins not evaluated by this instrument (informational): charterGhpDeploy, plazirUrl, vaultBytes, vaultSha, vaultUrlBearing, vaultDeadLinks, fleetSites, fleetStatus, grokbotsRows, reposClones
§history  SUSPENDED — probe-history source absent by declaration (pins.probeHistoryAbsent): /home/vgpnk/Projects/webzites/state/probe-history.jsonl — section suspended until a history source is re-anchored
skipped(offline): §history (probe-history source absent — pin-declared) — complete=false, never counted as pass
VERDICT: OK (exit 0)

[exit 0]
```

### 5. Freshness `armed` (offline only)

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
node scripts/freshness-sweep.mjs --section=armed --repo=/tmp/kake-r24-CritAxisHarm-XFWF/clone --offline; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```text
freshness-sweep — kake-shokunin freshness axis
generated 2026-10-21T11:43:59Z · node v24.21.0 · repo /tmp/kake-r24-CritAxisHarm-XFWF/clone · OFFLINE
pins: file /tmp/kake-r24-CritAxisHarm-XFWF/clone/corpus/knowledge/freshness-pins.json (round 18, updated 2026-10-14)
pins not evaluated by this instrument (informational): charterGhpDeploy, plazirUrl, vaultBytes, vaultSha, vaultUrlBearing, vaultDeadLinks, fleetSites, fleetStatus, grokbotsRows, reposClones
§armed
  all remote checks skipped(offline) — NOT counted as pass (complete=false)
skipped(offline): §armed (all remote checks) — complete=false, never counted as pass
VERDICT: OK (exit 0, partial: offline)

[exit 0]
```

### 6. Canonical audit selftest

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
TMPDIR=/tmp/kake-r24-CritAxisHarm-XFWF python3 scripts/canonical_audit.py --selftest; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout (JSON selftest record; all 82 returned cases have matching actual/expected exit+finding IDs and `ok:true`):

```json
{"selftest":{"cases":[{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"absolute_match","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"selfclosing_link","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"title_text_decoy","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"relative_same_dir","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"relative_parent","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"root_relative","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"scheme_relative","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"network_path_empty_authority","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"network_path_empty_authority_four","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"first_base","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"second_base_ignored","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"empty_base","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"rel_token_list","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"rel_uppercase","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"attr_uppercase","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"rel_non_ascii_separator","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"duplicate_attrs_first_wins","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"entity_href","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"query_preserved","ok":true},{"actual":{"exit":1,"id":"canonical_mismatch"},"expected":{"exit":1,"id":"canonical_mismatch"},"name":"empty_query_delimiter","ok":true},{"actual":{"exit":1,"id":"canonical_mismatch"},"expected":{"exit":1,"id":"canonical_mismatch"},"name":"relative_empty_query","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"missing_link","ok":true},{"actual":{"exit":1,"id":"canonical_multiple"},"expected":{"exit":1,"id":"canonical_multiple"},"name":"duplicate_same","ok":true},{"actual":{"exit":1,"id":"canonical_multiple"},"expected":{"exit":1,"id":"canonical_multiple"},"name":"duplicate_different","ok":true},{"actual":{"exit":1,"id":"canonical_outside_head"},"expected":{"exit":1,"id":"canonical_outside_head"},"name":"body_link","ok":true},{"actual":{"exit":1,"id":"canonical_href_missing"},"expected":{"exit":1,"id":"canonical_href_missing"},"name":"href_absent","ok":true},{"actual":{"exit":1,"id":"canonical_href_missing"},"expected":{"exit":1,"id":"canonical_href_missing"},"name":"href_empty","ok":true},{"actual":{"exit":1,"id":"canonical_href_missing"},"expected":{"exit":1,"id":"canonical_href_missing"},"name":"href_ascii_whitespace","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"href_c1_control_path","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"href_c1_control_query","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"invalid_url","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"javascript_url","ok":true},{"actual":{"exit":1,"id":"canonical_url_invalid"},"expected":{"exit":1,"id":"canonical_url_invalid"},"name":"data_url","ok":true},{"actual":{"exit":1,"id":"canonical_fragment"},"expected":{"exit":1,"id":"canonical_fragment"},"name":"fragment_url","ok":true},{"actual":{"exit":1,"id":"canonical_fragment"},"expected":{"exit":1,"id":"canonical_fragment"},"name":"empty_fragment","ok":true},{"actual":{"exit":1,"id":"canonical_mismatch"},"expected":{"exit":1,"id":"canonical_mismatch"},"name":"wrong_host","ok":true},{"actual":{"exit":1,"id":"canonical_mismatch"},"expected":{"exit":1,"id":"canonical_mismatch"},"name":"wrong_path","ok":true},{"actual":{"exit":1,"id":"canonical_mismatch"},"expected":{"exit":1,"id":"canonical_mismatch"},"name":"wrong_query","ok":true},{"actual":{"exit":1,"id":"base_url_invalid"},"expected":{"exit":1,"id":"base_url_invalid"},"name":"base_invalid","ok":true},{"actual":{"exit":1,"id":"base_url_invalid"},"expected":{"exit":1,"id":"base_url_invalid"},"name":"base_empty_authority","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"comment_decoy","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"script_decoy","ok":true},{"actual":{"exit":1,"id":"canonical_missing"},"expected":{"exit":1,"id":"canonical_missing"},"name":"template_decoy","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"template_selfclose","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"noscript_canonical","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"foreign_content","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_svg_after_head","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_math_after_head","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"body_void_selfclose","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_svg_selfclose_link","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"head_svg","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_nonvoid_selfclose","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_svg_unclosed","ok":true},{"actual":{"exit":1,"id":"canonical_outside_head"},"expected":{"exit":1,"id":"canonical_outside_head"},"name":"body_svg_then_body_canonical","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"body_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"foreignobject_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"svg_head_breakout_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"svg_mismatched_end_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"svg_title_hidden_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"svg_style_hidden_base","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"svg_script_hidden_base","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"svg_title_text_clean","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"foreign_stray_end","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"processing_instruction","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"missing_head","ok":true},{"actual":{"exit":2,"id":"html_unsupported"},"expected":{"exit":2,"id":"html_unsupported"},"name":"head_body_child","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"manifest_traversal","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"symlink_html","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"symlink_parent","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"fifo_html","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"manifest_symlink","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"manifest_dir_caller_prefix","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"empty_manifest","ok":true},{"actual":{"exit":2,"id":"input_invalid"},"expected":{"exit":2,"id":"input_invalid"},"name":"duplicate_pages","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_missing_mode","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_unknown_flag","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_missing_manifest_path","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_conflicting_modes","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_json_with_selftest","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_abbreviated_manifest","ok":true},{"actual":{"exit":64,"id":"usage_json"},"expected":{"exit":64,"id":"usage_json"},"name":"cli_repeated_manifest","ok":true},{"actual":{"exit":0,"id":null},"expected":{"exit":0,"id":null},"name":"cli_help","ok":true}],"passed":true},"tool":"canonical_audit.py"}

[exit 0]
```

### 7. Round-23 C1 replay counter at base

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
TMPDIR=/tmp/kake-r24-CritAxisHarm-XFWF python3 .ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-CritAxisHarm-XFWF/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```json
{
 "accepted": 17,
 "claimVerdicts": {
  "HOLD": 79,
  "STALE": 55,
  "UNVERIFIABLE": 42
 },
 "revision": "f7de3ab4e9f030a15a857a5a08631bd8e690f436",
 "total": 17,
 "units": [
  {
   "claims": {
    "HOLD": 5,
    "STALE": 3,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "drift-detection"
  },
  {
   "claims": {
    "HOLD": 2,
    "STALE": 0,
    "UNVERIFIABLE": 4
   },
   "pass": true,
   "problems": [],
   "unit": "fire-journal-codes"
  },
  {
   "claims": {
    "HOLD": 4,
    "STALE": 4,
    "UNVERIFIABLE": 1
   },
   "pass": true,
   "problems": [],
   "unit": "fleet-registry"
  },
  {
   "claims": {
    "HOLD": 3,
    "STALE": 2,
    "UNVERIFIABLE": 3
   },
   "pass": true,
   "problems": [],
   "unit": "free-read-verbs"
  },
  {
   "claims": {
    "HOLD": 4,
    "STALE": 2,
    "UNVERIFIABLE": 1
   },
   "pass": true,
   "problems": [],
   "unit": "ghp-subpath-spotcheck"
  },
  {
   "claims": {
    "HOLD": 1,
    "STALE": 7,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "keeper-timer-inert"
  },
  {
   "claims": {
    "HOLD": 2,
    "STALE": 3,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "kimi-subpath-audit"
  },
  {
   "claims": {
    "HOLD": 2,
    "STALE": 1,
    "UNVERIFIABLE": 3
   },
   "pass": true,
   "problems": [],
   "unit": "mirror-pitfalls"
  },
  {
   "claims": {
    "HOLD": 0,
    "STALE": 4,
    "UNVERIFIABLE": 3
   },
   "pass": true,
   "problems": [],
   "unit": "ops-automation"
  },
  {
   "claims": {
    "HOLD": 3,
    "STALE": 3,
    "UNVERIFIABLE": 2
   },
   "pass": true,
   "problems": [],
   "unit": "origin-repos"
  },
  {
   "claims": {
    "HOLD": 5,
    "STALE": 1,
    "UNVERIFIABLE": 2
   },
   "pass": true,
   "problems": [],
   "unit": "probe-delta-alerting"
  },
  {
   "claims": {
    "HOLD": 5,
    "STALE": 1,
    "UNVERIFIABLE": 1
   },
   "pass": true,
   "problems": [],
   "unit": "publish-channels"
  },
  {
   "claims": {
    "HOLD": 3,
    "STALE": 3,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "publish-queue"
  },
  {
   "claims": {
    "HOLD": 3,
    "STALE": 5,
    "UNVERIFIABLE": 0
   },
   "pass": true,
   "problems": [],
   "unit": "sitemap-orphan-audit"
  },
  {
   "claims": {
    "HOLD": 4,
    "STALE": 1,
    "UNVERIFIABLE": 3
   },
   "pass": true,
   "problems": [],
   "unit": "speedrun-pipeline"
  },
  {
   "claims": {
    "HOLD": 4,
    "STALE": 5,
    "UNVERIFIABLE": 1
   },
   "pass": true,
   "problems": [],
   "unit": "vault-properties"
  },
  {
   "claims": {
    "HOLD": 29,
    "STALE": 10,
    "UNVERIFIABLE": 18
   },
   "pass": true,
   "problems": [],
   "unit": "property-map"
  }
 ]
}

[exit 0]
```

### 8. Round-23 C2 replay counter at base

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
TMPDIR=/tmp/kake-r24-CritAxisHarm-XFWF python3 .ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-CritAxisHarm-XFWF/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```json
{
 "accepted": 12,
 "revision": "f7de3ab4e9f030a15a857a5a08631bd8e690f436",
 "surfaces": [
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "plazir15-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "charter-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "ds4cc-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "burnerchrome-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "vault-index-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "plazir27-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "ufo-fsd-kimi-pro",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-ghp",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "plazir15-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
 ],
 "total": 12,
 "validatorSha256": "23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4"
}

[exit 0]
```

### 9. Frozen round-22 canonical matrix

Command (`cwd=/tmp/kake-r24-CritAxisHarm-XFWF/clone`):

```sh
TMPDIR=/tmp/kake-r24-CritAxisHarm-XFWF python3 .ufo/waves/round-22/matrix.py --root /tmp/kake-r24-CritAxisHarm-XFWF/clone; rc=$?; printf '\n[exit %s]\n' "$rc"
```

Exact stdout:

```text
PASS caseId=absolute_match exit=0 findings=clean
PASS caseId=relative_same_dir exit=0 findings=clean
PASS caseId=relative_parent exit=0 findings=clean
PASS caseId=root_relative exit=0 findings=clean
PASS caseId=scheme_relative exit=0 findings=clean
PASS caseId=first_base exit=0 findings=clean
PASS caseId=second_base_ignored exit=0 findings=clean
PASS caseId=rel_token_list exit=0 findings=clean
PASS caseId=rel_uppercase exit=0 findings=clean
PASS caseId=attr_uppercase exit=0 findings=clean
PASS caseId=entity_href exit=0 findings=clean
PASS caseId=query_preserved exit=0 findings=clean
PASS caseId=missing_link exit=1 findings=canonical_missing
PASS caseId=duplicate_same exit=1 findings=canonical_multiple
PASS caseId=duplicate_different exit=1 findings=canonical_multiple
PASS caseId=body_link exit=1 findings=canonical_outside_head
PASS caseId=href_absent exit=1 findings=canonical_href_missing
PASS caseId=href_empty exit=1 findings=canonical_href_missing
PASS caseId=invalid_url exit=1 findings=canonical_url_invalid
PASS caseId=javascript_url exit=1 findings=canonical_url_invalid
PASS caseId=data_url exit=1 findings=canonical_url_invalid
PASS caseId=fragment_url exit=1 findings=canonical_fragment
PASS caseId=wrong_host exit=1 findings=canonical_mismatch
PASS caseId=wrong_path exit=1 findings=canonical_mismatch
PASS caseId=wrong_query exit=1 findings=canonical_mismatch
PASS caseId=base_invalid exit=1 findings=base_url_invalid
PASS caseId=comment_decoy exit=0 findings=clean
PASS caseId=script_decoy exit=0 findings=clean
PASS caseId=template_decoy exit=0 findings=clean
PASS caseId=missing_head exit=2 findings=html_unsupported
PASS caseId=manifest_traversal exit=2 findings=input_invalid
PASS caseId=symlink_html exit=2 findings=input_invalid
SUMMARY selection=all accepted=32 total=32 executed=32 discrepancies=0 tool_missing=0

[exit 0]
```

## Limits

- The `armed` baseline is only the offline partial result; a full live armed comparison remains unobserved and must not be fabricated from that exit 0.
- Initial counter invocations from the fleet-root working directory used relative script paths that did not resolve (`python3: can't open file '/home/vgpnk/Projects/shokunin/.ufo/waves/round-23/measure_c1.py'` / `measure_c2.py`, and the round-22 matrix equivalent; exit 2). I corrected the working directory to the clone and recorded the successful outputs above. Those initial path errors are invocation mistakes, not baseline gate results.
- No tools were installed or updated. No lane production files, git index, or jj state were changed; all executed selftest scratch is under the fresh `/tmp/kake-r24-CritAxisHarm-XFWF` workspace.
