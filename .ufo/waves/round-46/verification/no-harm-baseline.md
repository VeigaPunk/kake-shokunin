# Round 46 no-harm baseline

Axis: operability.

Working directory for all commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

## Ledger latest check

Command: `python3 -B scripts/ledger_latest_check.py`

Exit: `0`

Verbatim output:

```text
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3581
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1705
ledger-quotes: 3 figures, 0 mismatches
EXIT_CODE=0
```

## Freshness sweep selftest

Command: `node scripts/freshness-sweep.mjs --selftest`

Exit: `0`

Verbatim output:

```text
freshness-sweep --selftest
fixtures: /tmp/kake-r16/selftest (hermetic; re-runnable)
  PASS  a annotated-missing -> declaredAbsent, exit-neutral
        expect: exit 0 · declaredAbsent contains selftest-missing.md · drift [] · resolve contains selftest-present.md
        got:    exit 0 · declaredAbsent ["~/Projects/webzites/selftest-missing.md"] · drift [] · resolve ["~/.kake-freshness-selftest-2656727/selftest-present.md"]
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
        got:    exit 2 · stderr/stdout "{\n  \"generatedAt\": \"2026-10-24T04:59:10Z\",\n  \"node\": \"v24.21.0\",\n  \"repoRoot\": \"/home/vgpnk/Projects/shokunin/kake-shoku"
  PASS  j probeHistoryAbsent + canonical default missing -> SUSPENDED, exit 0
        expect: exit 0 · historySuspended true · file is selftest-rebound canonical
        got:    exit 0 · suspended true · file /tmp/kake-r16/selftest/canonical-absent-history.jsonl
  PASS  k probeHistoryAbsent + explicit missing KAKE_PROBE_HISTORY -> exit 2 (fail-closed)
        expect: exit 2 · error cannot read · not historySuspended
        got:    exit 2 · suspended undefined · error cannot read /tmp/kake-r16/selftest/explicit-missing-history.jsonl
  PASS  l probeHistoryAbsent pin is known/consumed (not listed unused)
        expect: pins._unused excludes probeHistoryAbsent
        got:    unused []
  PASS  i malformed pins JSON -> exit 2 (never silent defaults)
        expect: exit 2 · stderr names pins file invalid and parse error
        got:    exit 2 · "freshness-sweep: pins file invalid — /tmp/kake-r16/selftest/bad-pins.json: Unexpected end of JSON input"
  PASS  d unknown flag -> exit 64
        expect: exit 64
        got:    exit 64 · "freshness-sweep: unknown flag: --bogus-flag"
  PASS  e write-API call sites confined to SELFTEST-WRITES region
        expect: 0 call sites outside balanced region(s)
        got:    0 outside · errors 0 (regions B1199,E1270,B1557,E1623,B1628,E1630)
  PASS  e2 write confinement mutation proof (in memory)
        expect: every out-of-region top-level function mutant caught; every covered API name caught; marker errors, anchoring and identifier boundary pinned; positive/decoy controls pass
        got:    caught 27/27 mutants · apis 31/31 pin=match · regions B1199,E1270,B1557,E1623,B1628,E1630 · controls positive=PASS decoy=PASS unbalanced=error nested=error loneEnd=error junkMarker=rejected suffix=clean inSelftest=yes
  PASS  sidecar valid absence
        expect: exit 0
        got:    exit 0
  PASS  sidecar stale line digest
        expect: exit 2
        got:    exit 2
  PASS  sidecar outside corpus file
        expect: exit 2
        got:    exit 2
  PASS  sidecar wrong token
        expect: exit 2
        got:    exit 2
  PASS  sidecar no absence word
        expect: exit 2
        got:    exit 2
  PASS  sidecar invalid calendar date
        expect: exit 2
        got:    exit 2
  PASS  sidecar no historical wording
        expect: exit 2
        got:    exit 2
  PASS  sidecar malformed JSON
        expect: exit 2
        got:    exit 2
  PASS  sidecar valid restoration is not absence
        expect: exit 1
        got:    exit 1
  PASS  sidecar restoration cannot annotate
        expect: exit 2
        got:    exit 2
  PASS  absence vocabulary absent
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary gone
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary vanished
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary emptied
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary no longer
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary dangling
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary no such file
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary never published
        expect: exit 0, annotated target
        got:    exit 0
  PASS  absence vocabulary missing
        expect: exit 0, annotated target
        got:    exit 0
  PASS  recovered list is exact and informational
        expect: exit 0, recovered [~/.kake-freshness-selftest-2656727/selftest-present.md]
        got:    exit 0 · ["~/.kake-freshness-selftest-2656727/selftest-present.md"]
selftest: 35/35 passed
EXIT_CODE=0
```

## Frozen write-bounds check

Attempted command: `bash .ufo/waves/round-46/build/frozen-check.sh`

Exit: `127` (failure finding). The required script was absent at the time of the attempt.

Verbatim output:

```text
bash: .ufo/waves/round-46/build/frozen-check.sh: No such file or directory
EXIT_CODE=127
```
