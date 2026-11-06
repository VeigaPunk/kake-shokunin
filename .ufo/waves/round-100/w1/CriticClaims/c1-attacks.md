# Round 100 C1 critic attacks — CriticClaims seat (kake r100, hyaku run 15)

Instrument attacked: `.ufo/waves/round-100/c100_registry.py`
(sha256 `c25d981ec110e7d7676f55f1e494db159c6c2bbe71d40fc5d88d0d746132ae48`, verified against
`controls/instrument-sha256.txt` before attacking; `sha256sum -c` reported no mismatch line).
Surface: the C1 claim at repair commit `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` (lane tip;
`git -C <lane> rev-parse master` → same).

Method: scratch clone of the lane (`git clone --shared`), one fixture commit per attack, each
fixture editing ONLY `SKILL.md` (plus the tool for A5) on top of the repair commit; counter run per
fixture rev: `python3 -B .ufo/waves/round-100/c100_registry.py --root <clone> --revision <rev>
--work <scratch>/work/<run>`. The clone is deleted after receipt copying; every inserted row text is
reproduced verbatim below, and every rev id is recorded.

Baseline reproduction at the repair commit (matches `controls/after-c1.txt`):

```
revision=e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f
tools=55 rows=146 listed=55 unlisted=0 dangling=0 duplicated=0 probe_mismatch=0 exec_fail=0 mismatches=0 met=true
rc=0
```

Observed ground truth for `scripts/cache_key.py` (the duplicated tool): unknown-flag exit is 1
(`python3 -B scripts/cache_key.py --zz-bogus-r100 </dev/null` → rc=1 "invalid_input"; same for
`--definitely-bogus-other-flag`; the tool ignores argv entirely and reads stdin JSON). Its current
registry row's verdict map names 0 and 1 — correct.

## Escapes: met=true while the registry is wrong outside the declared limits

Every fixture inserts a SECOND registry row for `cache_key.py` inside the live 7-column registry
table (`| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |`,
SKILL.md:1705-1707), cell-count conformant, owner `kake`, verdict map claiming
`` 127`` for unknown flags (false; true code 1). The original row stays. The counter's
`invoked()` grammar strips leading `VAR=` words and — only when the first word is
`python3`/`python`/`node` — the interpreter and consecutive `-flag` words. Any wrapper whose first
word is not in that set, or a flag-with-value pair (`-X dev`), leaves the tool path unreached, so
the row is never recorded in `invoking`: D1 never sees the duplicate and D2 never checks its map.

| id | fixture rev (clone) | inserted Entry command cell | counter first line (abridged) | rc | why invisible |
|---|---|---|---|---|---|
| A1 | `073f80e2fe354857112349e1dcb5d588056fe50c` | `` `env python3 -B scripts/cache_key.py` `` | `tools=55 rows=147 listed=55 unlisted=0 dangling=0 duplicated=0 probe_mismatch=0 exec_fail=0 mismatches=0 met=true` | 0 | `invoked()` → `["env"]` ∉ population |
| A2 | `b05f5cda50f06ee405a13adbedda10718524a92f` | `` `bash -c 'python3 -B scripts/cache_key.py'` `` | `tools=55 rows=147 … duplicated=0 probe_mismatch=0 … mismatches=0 met=true` | 0 | `invoked()` → `["bash"]` |
| A3 | `b53e88f920739acec3dea77c518d3bf1611e5ac1` | `` `uv run scripts/cache_key.py` `` | `tools=55 rows=147 … duplicated=0 probe_mismatch=0 … mismatches=0 met=true` | 0 | `invoked()` → `["uv"]` |
| A4 | `40ef90b83d46b9342777eea3f8e4095032cf8cdc` | duplicate row in a **separate** table whose header omits `Write scope` (entry `` `python3 -B scripts/cache_key.py` ``, map claims `64`) | `tools=55 rows=146 … mismatches=0 met=true` | 0 | header misses a REQUIRED column → `tables()` drops the whole table: rows=146 (the row is not even counted), no invocation, no dangling |
| A5 | `ff33b8630f759e6a4fa2c750ce027d01a9a57e8d` | **tool edit, SKILL.md unchanged**: `main()` gains `if len(sys.argv)==2 and sys.argv[1]=="--zz-bogus-r100": print("usage: …"); return 0` | `tools=55 rows=146 … duplicated=0 probe_mismatch=0 … mismatches=0 met=true` | 0 | D2's probe uses the literal magic flag; the tool special-cases it to exit 0, which the row's map names; the map's `1 refusal` prose is now false for the probe path — the counter certifies a manufactured exit |
| A7 | `d7a50a4d298895048c69e3ff393cc8d6a34c8b09` | `` `python3 -X dev scripts/cache_key.py` `` | `tools=55 rows=147 … duplicated=0 probe_mismatch=0 … mismatches=0 met=true` | 0 | `invoked()` pops `-X`, stops at the VALUE word `dev`, reports `["dev"]` — built as a negative control, observed as an escape |

Inserted row (A1/A2/A3/A7 form, Entry command cell varying per row above):

```
| cache_key.py | probe (CriticClaims A<n> fixture: …) | <entry cell> | `0` key printed on stdout; `1` refusal; `127` unknown flag, usage fault | no self-test (no `--selftest` mode; scored by `.ufo/waves/round-89/c89_key.py`) | stdin/stdout/stderr only | kake |
```

A4's broken-header table (inserted after SKILL.md:1731 with a blank-line separator):

```
| Name | Kind | Entry command | Verdict map | Self-test | Owner |
|---|---|---|---|---|---|
| cache_key.py | probe (CriticClaims A4 fixture: duplicate row in a table whose header lacks the Write scope column) | `python3 -B scripts/cache_key.py` | `0` key printed on stdout; `1` refusal; `64` unknown flag, usage fault | no self-test (no `--selftest` mode) | kake |
```

A6 negative control (the one form the counter does catch):

| id | fixture rev | Entry command cell | counter line | rc |
|---|---|---|---|---|
| A6 | `29139af0ab02824b40d9d5a180e8b71bb46c6457` | `` `python3 -B ./scripts/cache_key.py` `` | `tools=55 rows=147 … duplicated=1 probe_mismatch=0 … mismatches=1 met=false` / `duplicated scripts/cache_key.py 1707,1708` | 1 |

`invoked()` strips a leading `./`, so the relative path reaches the tool and D1 fires. The
selftest's `v2-assignment-prefix-invocation` case (`X=1 python3 -B -I scripts/a.py`) survives only
because `-B -I` are consecutive flag words; any flag-with-value (`-X dev`, `-W ignore`) hides the
tool. A process-run note: a first A4 launch accidentally resolved an OLD lane commit via
`git log --grep=A4` (scoring `a26fd6a5…`, rows=59, met=false — not my fixture); it was re-run pinned
to `40ef90b8…` above. The mis-run is evidence only of my own tooling, not of the counter.

## Declared-limit boundary (honesty)

- The freeze/docstring DECLARE: false-but-well-formed prose passes; a map naming extra codes passes
  D2; the review conjunct covers that limit. My A-rows' false `127` codes ride exactly that limit —
  what is NOT declared is that D1's invocation grammar silently excludes wrapper prefixes and
  flag-value pairs, and that the review conjunct judges only 8 fixed units at the repair commit, so
  a false-map duplicate row at any OTHER location of the registry is covered by nothing. A1/A2/A3/A7
  are escapes of that undeclared gap; the same fixture checked against the review conjunct would
  need a reviewer looking at line ~1708, which the frozen 8 units do not include.
- A4 relies on the counter's surface definition (a table without the full header is not a registry
  table) — structural, but the effect is that visible, unfenced, non-history registry-shaped content
  escapes both D1/D2 and the review units; it is weaker than A1/A2/A3/A7 and reported for
  completeness.
- A5 shows the one execution the counter performs (D2's probe) is steerable by the tool via a
  literal argv comparison. The docstring declares "the probe checks only the usage-fault path"; it
  does not declare that the flag itself is a magic value any tool can detect.

## Framing defects (item 3 of the assignment)

- **FD1 (claim quantifier):** the claim says "every row's verdict map naming the exit code the tool
  returns for an unknown flag". The instrument checks that predicate only for rows its
  `invoked()` grammar recognizes, at one magic flag, and the review conjunct only for 8 named
  units. A1/A2/A3/A5/A7 all print met=true while a registry row visible in a registry table names a
  wrong unknown-flag code. "Calibration" is point-in-time at the repair commit (there it is honest —
  baseline met=true reproduced), not a property the instrument enforces against nearby edits.
- **FD2 (cheaper controls):** no do-nothing or cheaper control reaches either target honestly:
  C1 base `3989618d` → `met=false` exit 1 (`controls/base-c1.txt`), `deleteall` → `met=false`
  (`controls/ctl-c1-deleteall.txt`); C2 base blob → `hand=72/91 … met=false`
  (`controls/base-c2.txt`). But the cheapest control that DOES reach met=true is not a repair: for
  C1 it is any of my A1/A2/A3/A7 one-row edits (escape above); for C2 it is a reformatted copy of
  the published reference (see c2-attacks.md, F2-capability). The instruments measure conformance to
  their own surface, not truth of the claim sentence.
- **FD3 (calibration vs execution):** C1 is self-assessment-vs-observed-state only in the
  population/unlisted/dangling dimensions (those are real: git population vs registry rows). The
  verdict-map dimension is executed at exactly one input; the review dimension is scoped to 8 units.
  Calling the composite "calibration, score 3 → 4" is fair ONLY under the declared limits — and the
  declared limits do not include the D1 grammar gap or the probe magic-value gap demonstrated above.

## Routed findings (for the L1; nothing repaired)

1. Extend `invoked()` to resolve wrapper prefixes (`env`, `bash -c`, `sh -c`, `uv run`,
   `python3 -X <value> …`, `-W <value> …`) or declare the grammar limit in freeze.md; the selftest
   should gain a flag-value case (A7).
2. Consider a surface rule that a near-registry table (header superset/variant of the required
   columns) is reported rather than silently dropped (A4).
3. Consider making the D2 probe flag non-greppable-per-tool (e.g. random per run) or double-probing
   with a second unknown flag, so A5-style special-casing shows a contradiction between the two
   probes.
