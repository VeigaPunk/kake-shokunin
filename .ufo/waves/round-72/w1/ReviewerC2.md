# Round-72 w1 — ReviewerC2 — attack on the frozen C2 counter `c72_tmp_v2.py`

c2_verdict=survives

The frozen predicate verifies end-to-end on this host: selftest `11/11` exit 0; on the J3 control commit
`7966a320` c71 accepts (exit 0) and c72 rejects (exit 1); c72 is red at round-71 base `cc6b4e0b` (exit 1)
and green at tip `3c68645a` (exit 0). No leg is defeated, so C2 as frozen is provable. The attack found real
gaps around the predicate: (1) a `${TMPDIR:-/tmp}` fallback repoint — the exact F2 class the counter's own
docstring claims to kill — escapes both regexes; (2) command-form lines whose verb is outside the frozen
17-word list take the phrase-only annotation and pass, demonstrated end-to-end (commit `193fa3d5`,
met=True exit 0); (3) two basename-collision shapes redden legitimate dated-absence rows. All findings are
routed/note severity, none blocking.

## Evidence (commands → observed exit codes)

1. Frozen-bytes check: `git show a19d38ea:.ufo/waves/round-72/c72_tmp_v2.py | cmp - <worktree file>` → identical.
2. `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` → `C2v2 selftest 11/11`, exit 0.
3. `sh .ufo/waves/round-72/controls/j3-control.sh` → `J3_CONTROL_COMMIT=7966a32029826d3f25bf4fe9e72a5b1651c29c87`;
   c71 printed `met=True`, `c71_exit=0`; c72 printed `command_findings=1 findings=[(27,0,1,0)] met=False`;
   script exit 1 — but see finding C3 below: `set -e` aborts before `c72_exit=1` is printed.
4. `c72_tmp_v2.py --revision cc6b4e0b...` → exit 1, findings lines 27,95,227,356,356,359,463,464 (red-before holds).
5. `c72_tmp_v2.py --revision 3c68645a...` → exit 0, `met=True` (tip green holds).
6. Attack driver `attack.py` (importlib load of the frozen counter by path, `python3 -B`, function-level
   fixtures + scratch clone `/fast/scratch/hyaku/kake-r72/ReviewerC2/clone`, commits as kake-scratch with
   `rev-parse --show-toplevel` asserted) → all results below, driver exit 0.

## Fixture table (line → counter (brace,command,prose) → classification → judgment)

| id | counter | class | judgment |
|---|---|---|---|
| T1 `\| r11 \| artifacts under /tmp/kake-r11/ \| 2026-11-02: absent; historical record, not an executable instruction \|` | (0,0,0) | clean | accept — correct |
| T2 `see the artifacts under /tmp/kake-r12/live/` | (0,0,1) | prose | reject — correct |
| T3 `copy the snapshot first \`cp state/probe-latest.json /tmp/kake-r12/live/backup.json\` (historical record, …)` | (0,1,0) | command | reject — correct (J3 kill works for `cp`) |
| T4 `cp state/probe-latest.json /tmp/kake-r12/live/backup.json` (imperative) | (0,1,0) | command | reject — correct |
| T5 `run the tool with TMPDIR=${TMPDIR:-/tmp/scratch} first` | (1,0,0) | brace | reject — by design (F2, with-slash spelling) |
| T6 `run the tool with BK="${TMPDIR:-/tmp}/kake-r12" first` | (0,0,0) | clean | **FALSE GREEN** (brace class evades) |
| T7 `rsync -a /tmp/kake-r12/live/ backup/ (historical record, not an executable instruction)` | (0,0,0) | clean | **FALSE GREEN** (command form, annotated) |
| T8 `TMPDIR=/tmp/kake-r12 python3 -B scripts/tool.mjs (historical record, …)` | (0,0,0) | clean | **FALSE GREEN** (env-prefixed command, annotated) |
| T9 ``elevate first: `sudo cp state/x /tmp/kake-r12/live/x.json` (historical record, …)`` | (0,0,0) | clean | **FALSE GREEN** (`sudo` prefix defeats span first-word check) |
| T10 ``run ``cp state/… /tmp/kake-r12/live/backup.json`` (historical record, …)`` (double-backtick span) | (0,0,0) | clean | **FALSE GREEN** (`SPAN_RE` matches empty spans; CommonMark ` `` ` spans unsupported) |
| T11 `` `cd /tmp/kake-r12/live && cp …` (historical record, …) `` | (0,0,0) | clean | **FALSE GREEN** (`cd` not in frozen word list) |
| T12 `` \| r12 \| artifacts under `/tmp/kake-r12/test` \| 2026-11-02: absent; … not an executable instruction \| `` | (0,1,0) | command | **FALSE RED** (span basename `test` collides with command word; dated-absence row reddened) |
| T13 ``ensure `BK="$(mktemp -d)"` then write `"$BK/probe-latest.backup.json"` …`` (repaired recipe) | (0,0,0) | clean | accept — correct (vacuously: no `/tmp/` token present) |
| T14 `rm -rf /tmp/kake-r12/ (historical record, …)` | (0,0,0) | clean | **FALSE GREEN** (`rm` not in word list) |
| T15 ``run `cp` state/probe-latest.json /tmp/kake-r12/live/backup.json (historical record, …)`` | (0,0,0) | clean | **FALSE GREEN** (command word backticked alone, bare args) |
| T16 `/tmp/kake-r12/sh wrapper output (2026-11-02: absent; … not an executable instruction)` | (0,1,0) | command | **FALSE RED** (line-initial path, basename `sh` → "imperative") |
| T17 `cp state/probe-latest.json "$(mktemp -d /tmp/kake-r12.XXXXXXXX)/probe-latest.backup.json"` | (0,1,0) | command | **FALSE RED candidate** — fresh-dir `mktemp -d /tmp/…` recipe cannot be a stale citation |

17 candidate lines; 8 false greens, 3 false reds/candidates, 6 correct classifications.

## Counterexamples (severity)

**C1 — routed (attack item a, brace class).** `${TMPDIR:-/tmp}` (closing brace before the slash) matches
neither `BRACE_TOKEN_RE` (requires `${TMPDIR:-/tmp/`) nor `TOKEN_RE` (requires literal `/tmp/`), so a
fallback repoint — the docstring's own "`${TMPDIR:-/tmp}` repoint kill (ReviewContract F2)" — is invisible
to findings AND to the guard (T6, G6: guard_ok=True met=True). Guard hole: such lines can be added freely.

**C2 — routed (attack item a, verb class).** The phrase-only kill covers only the frozen 17-word list as
line-initial or span-initial word. `rsync`, `rm`, `sudo cp`, `cd … &&`, env-prefixed `TMPDIR=/tmp/… python3`,
double-backtick spans, and lone-backtick command words all take the phrase and pass (T7–T11, T14, T15).
End-to-end proof: commit `193fa3d5dd488a19a3be8bf0f7c87511f37b5144` (clone, off tip) replaced line 27 with
T7 and appended T6 → `c72_tmp_v2.py --revision 193fa3d5` → `met=True`, exit 0, guard ok. The same M5/J3
shape with a different verb is accepted; the frozen cp-specific J3 control still holds, so C2's predicate
is untouched.

**C3 — routed (control script, not the counter).** Frozen `j3-control.sh` runs `set -eu`; c72 exits 1, so
errexit aborts the script before `echo "c72_exit=$?"`. Observed: `c71_exit=0` printed, then script exit 1
with no `c72_exit=` line. The contract receipt spec (`controls/c2-j3-control.txt` → `c71_exit=0` and
`c72_exit=1`) is not literally producible by the frozen script; the rejection is still evidenced by the
counter's own `met=False` line and the script exit code. L1 should describe the receipt accordingly.

**C4 — note (attack item b, false reds).** T12/T16: a dated-absence annotated row citing a path whose last
component equals a command word (`/tmp/kake-r12/test`, `/tmp/kake-r12/sh`; a bare-clone dir named `git` is
equally exposed) is classified command and reddened despite the phrase — command beats annotation by
design. The claim requires dated-absence prose annotations to be accepted; the lane's actual rows (tip
lines 27/227/356/359) are accepted, so C2 holds, but future rows citing such paths would false-red.

**C5 — note.** T17: `mktemp -d /tmp/kake-r12.XXXXXXXX` (fresh unique dir, cannot be a stale citation) is
reddened as a command finding. The lane's repaired convention `${BK:=$(mktemp -d)}` (T13) is accepted and
is what the contract demands, so this is a model limitation, not a contract breach.

## (c) Guard semantics — verified via evaluate()

- G1 added token line without phrase → guard_ok=False, met=False (required to fail ✓); also prose finding.
- G2/G5 annotated addition / annotate-in-place → guard_ok=True, met=True (annotated additions tolerated ✓).
- G3 removed token line → guard_ok=True, met=True: a removed line carries no obligation ✓.
- G4 de-annotate-in-place → guard_ok=False (annotation may never silently vanish ✓).
- E3 end-to-end: added unannotated token line → exit 1, guard=fail.
- E4 end-to-end: token line deleted → exit 0, met=True (removal required nothing).
- E5 end-to-end: removal + annotated addition → exit 0.
- Caveat: guard shares `TOKEN_RE` with findings, so C1's brace spelling is invisible to the guard too (G6).

## (d) `--revision` passed after `--end-of-options`

Code: `["git","-C",lane,"show","--end-of-options", f"{rev}:{PATH}"]` — revision argument placed after
`--end-of-options` ✓. Empirical (git 2.56.0): `git show --end-of-options 3c68645a:SKILL.md` → exit 0,
190536 bytes. Without mitigation, `git show --ext-diff 3c68645a:SKILL.md` → exit 0 (option silently
absorbed before the rev — the dangerous parse). With mitigation, `git show --end-of-options
--ext-diff:SKILL.md` → exit 128 fatal (treated as a revision, never an option). Counter on option-shaped
`--revision --ext-diff` → exit 2 unevaluable (no option parsing, clean failure). Placement and behavior
correct.

## (e) Selftest expected values vs code intent

All 8 line cases and 3 guard/ability cases match the code's actual behavior; `11/11` matches the
contract's required count. Two coverage gaps: the `mktemp_line_ok` case contains no `/tmp/` token and so
passes vacuously (real repaired-recipe acceptance is exercised by the tip-green leg, line 95's repaired
recipe); `brace_default_is_finding` only tests the `${TMPDIR:-/tmp/` with-slash spelling — the `${TMPDIR:-/tmp}`
spelling of C1 is untested and fails.

## Residual risk

C2's guarantee is the four named controls, not "no /tmp regressions": a crafted revision can carry
command-form `/tmp` references with verbs outside the frozen list, `${TMPDIR:-/tmp}` fallbacks, and
double-backtick spans, and still passes green (`193fa3d5`). A v3 would need: brace regex `\$\{TMPDIR:-/tmp\}`,
span parsing that handles ` `` ` and sudo/env prefixes, and either a wider verb list or a "command-shaped
line" heuristic. Counter is frozen this round — route, do not patch.

## Housekeeping

No tools installed (python3 3.x / git 2.56.0 sufficient; pacman untouched). Lane untouched (read-only git
show; counter run with `-B`, no bytecode writes). Scratch tree `/fast/scratch/hyaku/kake-r72/ReviewerC2/`
(incl. clone with branches e2–e5) deleted before yield; j3-control scratch self-cleaned via its trap.
