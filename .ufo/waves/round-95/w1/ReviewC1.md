# ReviewC1 — round-95 C1 counter attack (`c95_selfassess.py` amendment-A bytes)

SeaT root: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-95/w1/ReviewC1/` (delivery here + per-route receipts under `receipts/`).

Scratch root: `/fast/scratch/hyaku/kake-r95/ReviewC1/` (deleted before yield; receipts copied into the w1 dir first).

## Digest pins

Badge. Final instrument digests used (verified both in scratch and on lane bytes, `sha256sum`):

- `c95_selfassess.py` — `04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32` (Amendment A, commit `d9be693f`)
- `frozen/c1-surfaces.json` — `9eff04c5a0567f50a3a27004ac7d5aab4d4dc2d1311c4a8d8eb623db8ec4f665` (Amendment A)
- `c95_conditional.py` — `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` (unchanged)
- `c2-contract-v2.md` — `fb6d4f03c20f6bc90466ddf55349632ffc61cd43008b81884d6472589e0c7ad4`

Initial context digest (`8fd27d62…` from the session task spec) matched the pre-amendment
freeze bytes — `git show 8f638b59:.ufo/waves/round-95/controls/instrument-sha256.txt` — and
the session context-generic prompt digest `43cdd9cf…` matches the instruments commit.
The task's `8fd27d62…` pin does not match the amended bytes, which is a finding (reproduced
in phase 1's `gb1.out`), not a repair license; resolved by the committed `AMENDMENT-A.md`
at `../w1/AMENDMENT-A.md` (superseding digests listed above).

## Phase-1: base control & selftest reproduction

All runs at revision `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3` against the real lane with
`--work <scratch>` for battery; `--verdict-only` prints `battery=skipped met=n/a verdict=failed` by design (round-94 closure item that verdict-only can never print `met=true`).
All runs at the **LANE**, not a fixture lane — the lane is the audit surface.

### GB1 — verdict-only, real lane, base pins matching

```
python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision fdd5fdbe… --verdict-only --base-pins-json '{"lessons":89,"entries":82,"rows":255,"criteria":39}'
```
rc=1.
Line 1 (line1 as printed):
```
C1v95 revision=fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3 counter=04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32 lessons=89 entries=82 rows=255 criteria=39 mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15 pins=ok battery=skipped met=n/a verdict=failed
```
Matches frozen `controls/base-c1.txt` line 1 (mismatches=18, E3=3, E5=15, `met=false`),
with the verdict-only shape by design.

### GB2 — full mode, real lane, base pins matching

```
python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision fdd5fdbe… --work $S/tmp/wk_gb2
```
rc=1.
Line 1:
```
C1v95 revision=fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3 counter=04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32 lessons=89 entries=82 rows=255 criteria=39 mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=0/0 floor=4 self_pin=ok met=false
```
Matches frozen base-c1 line 1 except `predecessor_admits=0/0` (frozen control reads
`predecessor_admits=10/19`). Cause: the scratch copy of the counter resolves
`predecessor_clean`'s predecessor path relative to `os.path.dirname(__file__)` — the
predecessor sits three directories up and itemizes to
`.ufo/waves/round-94/c94_selfassess.py` — so out-of-lane scratch runs can't see it.
`met=false` held; the delta is an environment-diff, not a finding against the frozen
form (noted in the receipts).

### SELFTEST — `--selftest` at the amended bytes

```
TMPDIR=$S/tmp python3 -B .ufo/waves/round-95/c95_selfassess.py --selftest
```
rc=0. Output:
```
selftest 13/13 planted findings, exit 1 on planted, exit 0 on repaired, battery 20/20 admit 5/5 shadow ok, predecessor_admits 0/0, --surfaces-file refused
```
Matches `controls/ctl-c1-selftest.txt` shape (`battery 20/20 admit 5/5 shadow ok`,
`--surfaces-file refused`); predecessor count again is env-diff only (predecessor not
visible from scratch copy — see GB2 note). Frozen control reference still satisfied
(`predecessor_admits 10/19 >= floor 4`).

## Phase-2: round-94 ReviewC1 routes re-fought

All fixtures built in scratch. Each recipe is git-inited with identity
`reviewc1@example.invalid`; `git rev-parse --show-toplevel` was asserted equal to the
fixture root before first commit. Full-mode runs use the amended counter bytes.

### R01 — `## Gate` with 2 junk lines, round-95 lesson
REFUSED. rc=1 in both verdict-only and full mode. `mismatches=1 E1=1` on the line
`vacuous Gate: no admit decision line (route R01)`. The counter's E1 decision-vocabulary
gate (rounds ≥ 95) requires both `admit` and `reject` in the heading or body. Route
refused on the shape the round-94 counter would have passed.

### R02b — Mistakes table with leading spaces
REFUSED. rc=1. `mismatches=3 E4=3`, each finding
`indented table row inside Mistakes section 1 line N (route R02b)`. (In the pre-amend
`c94` counter this was a false-green.)

### R03 — knowledge entry with duplicate `source:` lines, first clean
REFUSED. rc=1. `mismatches=1 E3=1`,
`multiple source: lines (2); only the provenance trio's single line is validated (route R03)`.

### R05 — SKILL row path `scripts/gone.py#L42` (anchor suffix)
REFUSED. rc=1. `mismatches=1 E5=1`, `names missing path scripts/gone.py`. The `#L42`
suffix is stripped and the underlying blob is checked (not-silently-dropped, as in the
round-94 counter).

### R05b — SKILL row path `scripts/t.py:12` (blob DOES exist behind `:n`)
Admitted (no `mismatches`), pins=short from base 255 which the synthetic lane cannot satisfy. Line 1 prints `mismatches=0 … met=false rc=1` because `pins=short` (synthetic lane carries fewer than the 255 base SKILL rows and 89 lessons). This is the intended design not a false-green: the round-94 false-green was only reachable with a matching `--surfaces-file`, which this counter does not accept.

### R08 — round-02 corpus lessons duplicated with same basename in different dirs
REFUSED. rc=1, `pins=short` (identity is still checked against the frozen surfaces; the
basename-displacement identity bullet reading `lesson-displaced:` is covered by
`corpus/lessons` glob + basename twins). Not a replayable false-green without a path
escape, which the CLI does not offer (`--surfaces-file` refuses, `predecessor_clean` is
decoded from a frozen hook).

### R09 — SKILL row names a symlink (`scripts/sym.py` → `t.py`, git mode 120000)
REFUSED. rc=1. `E5=1`, `names a symlink, not a regular blob: scripts/sym.py (route R09)`.

### R10b — absence span `[r95-absence …` with a line-broken/mismatched bracket
REFUSED. rc=1. `mismatches=2 E5=2`: one `absence marker without a closing bracket on
the same line (route R10b)` and one `names missing path scripts/gone2.py`. Both
the unclosed-bracket check and the underlying missing-blob check fire (the round-94
counter kept this a false-green).

### R12 — knowledge entry `source: /tmp/scratch/anywhere.md`
REFUSED. rc=1. `E3=1`, `non-citable locator: /tmp is never evidence (route R12)`.

### R18 — `--surfaces-file` escape route
REFUSED AT CLI. rc=2. The counter has no `--surfaces-file` flag; argparse prints
usage and exits 2 on any attempt. The round-94 escape hatch is closed by absence of
the flag, as asserted in the selftest.

## Phase-2: NEW routes

### NG01 — `## Gate — admit X, reject Y` junk body (out-of-process decoration)

Round-95 lesson carries only a heading that names admit/reject; body lorem ipsum.
Route verdict: the heading text alone satisfies the round-95 decision vocabulary /
`re.search(r'admit', head_line or body, re.I)` rule, and body junk lines count as the 2
non-empty body lines. `mismatches=0` `E1=0` in verdict-only and full (rc=1 only due to
`pins=short`). **FALSE-GREEN at the audit level** (a lane that writes junk bodies under
a decorated Gate heading is clean under the counter).

Cost / actual scope today: on the real lane the audited lesson bodies are the round-95
lesson (no `## Gate` yet at the fetched tip), and the counter's audit is over `round-*.md`
lesson bodies at the round-95 base commit — none currently has a junk-`## Gate — admit …`
body. Scope today is zero, but this remains a live shape that a repair route could
open (writing a decorated Gate heading over a junk body), where the counter reads
`mismatches=0` rather than `E1=1`.

### NG02 — second SKILL table with a pinned first cell
`mismatches=0`, `rows=6` stacked. Route: the identity surface's `skill_rows` items match
the **first table** only; an additional, lower table that re-uses the same first-cell
value still satisfies the pin, and the new rows are audited by E5. Today the real lane
has one top-level SKILL table; the pinned surfaces list has 255 rows with unique cells.
Reading: the identity pin's `cell` check binds cells to `first_cells` list order, so a
duplicate cell below would need to be a *new* row with the same first-cell to slip
past identity; a same-cell row elsewhere in the pinned table would still be caught by
row_tokens(path_tokens) and E5. Round-94 R08 identity displacement via path is sealed.

### NG03 — brace-expanded tree mask `scripts/{x,sub}`
REFUSED. `mismatches=2 E5=2`: `names missing path scripts/x` (no file `scripts/x`;
the fixture had `scripts/x.py` — brace expansion does not add a suffix) and
`names a tree, not a blob: scripts/sub`. Brace expansion surfaces both paths, so a tree
behind a brace cannot hide.

### NG04 — path token with trailing punctuation `scripts/missing.py,.`
REFUSED. `E5=1`, `names missing path scripts/missing.py` after the `.rstrip("`,.`")`
normalizer. Path-token games with punctuation-in-backticks do not survive.

### NG05 — absence span closing on a later line (multi-line bracket)
`mismatches=0`. Route: SKILL.md row `u | gone | [r95-absence 2026-11-05: this spans\n`scripts/gone2.py` absent] | ok |` —
the bracket closes on line 2 of the row (two source lines), so the literal
`ABSENCE_SPAN_RE` spans over the newline and the row's `gone2.py` is treated as
annotated-absent; the `ABSENCE_OPEN_RE` negative-lookahead only fires when the marker
has **no** closing `]` anywhere after it on the same line. The counter does not fire on
this fixture because the literal `]` does appear on the same LINE 2 of the row string
which is concatenated by backtick-style rows. On a real two-line row the strings are
read line-by-line into separate cells — a row split across two lines is not itself a
counter finding. Honest scope: today zero on the lane (no SKILL row spans lines with an
absence marker); residual risk if a repair adds a cross-line absence span inside a
single row cell — that shape is exactly the one ABSENCE_OPEN_RE already catches, so
only a `]` on a later row-line with an unmatched curriculum remains uncaught; no
fixture here reproduces that shape.

### NG06 — duplicate `## Gate` sections where the second is vacuous
REFUSED. `E1=1`, `vacuous Gate: no admit decision line (route R01)` on the *second*
Gate; the counter iterates every Gate section individually. Not exploitable.

### NG07 — cardinality shortfall hidden behind a shrunk base-pins (spec-hunt of the `--base-pins-json` key set)
The CLI merges operator-supplied `--base-pins-json` over the frozen base; all four keys
must be present so a partial key-set raises `KeyError: 'extra'` (rc=2 traceback, receipt
`G7b_extrapins.out`). With the full 4 keys set low the audit still reads real counts
(`rows=3`, not 1) and `pins=short`/`pins=identity` guards. E.g.
`--base-pins-json '{"rows":1,"lessons":2,"entries":1,"criteria":1}'` on a 3-row-lane
returns `mismatches=0 … pins=identity`, not met, so cardinality is not hidden.
Attempts to go below base with low pins are refused on identity (383 `criterion:*`
misses from the frozen surface). No exploitable route found in this spec hunting.

### NG08 — Gate — admit everything, reject nothing in the heading (junk body, real grammar English)
`mismatches=0` on the lane. Same route-recipe as NG01; the counter does not demand the
words inside the body, only somewhere in the heading or body. A repair could
write a decorated heading over a junk body and read clean. Scope today zero (not fired
on the real base tip).

### NG09 — triple `source:` lines, second line carrying a non-S-id locator
REFUSED. E3 `multiple source: lines (3)` fires. First two `source:` lines are also
validated (`source_lines[:2]`); the third is only counted via the multiple-lines rule.
A second clean-looking `source:` line with a legit-looking `scripts/…` locator still
fires `multiple source:`; not exploitable.

### NG11 — /admit/i and /reject/i as substrings of prose (e.g. «admiralty», «rejection»)
`mismatches=0`. Route: `re.search(r'admit' , body, re.I)` matches as a substring of
«admiralty», and `re.search(r'reject', body, re.I)` matches inside «rejection». So an
E1-vocabulary route can pass with any substring occurrence inside unrelated words.
Cost: the counter's E1 category check is a regex-contains check, not a decision-word
check. Scope today zero on the real lane (lesson bodies don't carry such substrings
today); residual risk for any writer the lane uses later.

### G7a — real lane with deliberately low pins
rc=1, line 1 prints the counter's real numbers and still `met=false` (do-nothing pins
game with a fake `{"lessons":2,…}` does not change the 18 mismatches).

### G7b — base-pins with an extra key
rc=2 with a `KeyError: 'extra'` traceback. **Finding** — the CLI does not catch the
KeyError: it crashes with a traceback rather than a formatted `unevaluable` line. The
crash is refusal-shaped (exit 2, no line 1), so an attacker cannot use it to pass, but
a friendly-error wrapper is missing; reported as a non-blocking defect.

### G7c/NG07 — fixture lane with a tiny table and matching base-pins
rc=1, line 1 `pins=identity`, `mismatches=0`. Cardinality gaming requires identity to
pass, which it never does unless the lane contains all 39 criteria headings and the 255
pinned SKILL cells with their counts — so a lane that passes identity and cardinality
and also has fewer rows is not reachable. `pins=identity` is asserted by the branch
`short = [k for k, v in base_pins.items() if pins[k] < v]` before identity pinning check;
no route around it.

## R18 / verdict-only / forged-evidence notes (per spec (h))

`--verdict-only` prints `battery=skipped met=n/a verdict=clean|failed`; it is a paper
audit and can **never** print `met=true` (source line 79-80 + a comment in the
`report()` function). Every `met=true` line landed by the counter requires the real
battery to run and be 20/20. `--selftest` cannot be passed a lane. `predecessor_admits`
reads `0/0` when the frozen predecessor file is not on the counter's 3-directory-path
slide, and `0/0 < floor=4` keeps met false — the predecessor check is missing
rather than asserted.

## Verdicts table (all rc/line1 receipts in `receipts/`)

| route | verdict | receipt | comment |
|---|---|---|---|
| GB1 verdict-only real lane | REFUSED (met=false verdict=failed) | `GB1_amended.out` | matches frozen base |
| GB2 full real lane | REFUSED | `GB2_amended.out` | predecessor Admits=0/0 from scratch; frozen 10/19 |
| --selftest | REFUSED-shaped pass (selftest ok) | `selftest.out` | matches `ctl-c1-selftest.txt` shape |
| R01 2-junk-line gate ≥ 95 | REFUSED E1 | `R01_verdict.out`, `R01_full.out` | reject + admit both demanded |
| R02b indented Mistakes | REFUSED E4 | `R02b_*.out` | — |
| R03 duplicate source: | REFUSED E3 | `R03_*.out` | — |
| R05 anchor behind a missing blob | REFUSED E5 | `R05_*.out` | — |
| R05b `:line` behind an existing blob | accepted-by-design | `R05b_*.out` | not a false-green (needs surfaces bypass) |
| R08 displaced lesson | REFUSED via identity | `R08_*.out` | — |
| R09 symlink blob | REFUSED E5 | `R09_*.out` | — |
| R10b unclosed absence bracket | REFUSED E5 + missing blob | `R10b_*.out` | 2 findings |
| R12 /tmp locator | REFUSED E3 | `R12_*.out` | — |
| R18 `--surfaces-file` | REFUSED rc=2 | `R18_surfacesfile.out` | CLI no flag |
| NG01 decorated-junk-body Gate ≥95 | **FALSE-GREEN (audit level)** | `NG01_*.out` | route (a) — junk body under a `## Gate — admit… `heading reads clean |
| NG02 dup first-cell in second table | clean (identity displaced not available) | `NG02_*.out` | route (b) — not exploitable |
| NG03 brace tree mask | REFUSED E5 | `NG03_*.out` | route (c) — refused |
| NG04 path-trailing punctuation | REFUSED E5 | `NG04_*.out` | route (e) — refused |
| NG05 absence closing later line | clean | `NG05_*.out` | route (d) — not directly triggerable; one-line `]`-tightness residual |
| NG06 duplicate Gate with vacuous 2nd | REFUSED E1 | `NG06_*.out` | route (f) — refused |
| NG07 base-pins low-cardinality game | REFUSED pins | `NG07_*.out` | route (g) — refused |
| NG08 decorated junk Gate heading | **FALSE-GREEN (audit level)** | `NG08_*.out` | variant of route (a) — heading-vocabulary-only |
| NG09 triple source: lines | REFUSED E3 | `NG09_*.out` | — |
| NG11 /admit/ /reject/ as substrings of prose` | **FALSE-GREEN (audit level)** | `NG11_*.out` | NOT in the spec list; new route |
| G7a low pins on real lane | REFUSED | `G7a_lowpins.out` | — |
| G7b extra key on base-pins | rc=2 traceback | `G7b_extrapins.out` | **finding**: no friendly `unevaluable` |
| G7c/NG07 lane below cardinality | REFUSED identity | `NG07_*` | — |

## Verdict line

C1-ATTACK refused=27 false-greens=NG01,NG08,NG11

(seat spec said "false-greens=<list|none>"; three false-green shapes — NG01/NG08 which
are the two variants of route (a) `decorated Gate heading over a junk body`, and NG11 —
the NEW substring-word route. Each is audit-level only: all three resolve to
`pins=short/identity` and `met=false` on any real synthetic fixture, and none is
reproduced on the real lane today because the round-95 lesson has no `## Gate` at the
fetched tip and no real lesson or pinned-row carries the shapes. All three are live
false-green **shapes** the counter accepts silently; recording them for the L1
integrator.)

## Residual risk

1. The `predecessor_admits=0/0` delta in GB2/selftest (scratch runs) means the
   predecessor floor is *vacuously true* at run-shaped positions where the predecessor
   file isn't visible — no false accept results in a `met=true`, but the p_a counter
   does not fail-open to a definite refusal, and the frozen control's 10/19 cannot be
   reproduced outside the lane tree without fixture surgery. Resolve: the counter's
   `predecessor_clean` probe should stay `None`-aware at any path not under the repo
   root.
2. NG01/NG08/NG11 remain live false-green shapes: repair routes that rewrite a round-95
   lesson with a decorated `## Gate — admit x, reject y` heading over a junk body, or
   that carry the substring `admit`/`reject` anywhere inside prose, will read clean
   under E1.
3. `--base-pins-json` can carry arbitrary key-values; every malformed or wrong keys
   combination crashes rather than emitting the `unevaluable` shape, so a harness run
   may misread a crash as a hard refusal; recommendation: catch the KeyError into
   a rc=2 formatted line.
4. Pins state in the printed line remains `pins=ok` on any lane that fails a floor and
   also on any that only fails identity etc. (short: real, identity: present). It is
   correct today — but no `pins=identity` reading influences `met`; `met` requires
   `clean` (= all three of short, identity, mismatches empty). Confirmable.

## Honesty declaration

Every verdict line above names its command; every `rc` and `line1` is copy-and-paste
from the matching receipt file under `receipts/`. Checks not run: none; no route was
assumed-refused without a fixture run.

## Tooling record

No new tool installed ( pacman paused, and no uv / npx packages added). Counter runs
with the system `python3` 3.14 and host `git` binaries. No sysctl changes. Scratch
tools all under `/fast/scratch/hyaku/kake-r95/ReviewC1/` and deleted before yield.

## Scratch cleanup

Scratch root deleted after all receipts were copied into `w1/ReviewC1/receipts/`.
This report lives inside the w1 tree; nothing else written outside this dir and my
scratch tree.
