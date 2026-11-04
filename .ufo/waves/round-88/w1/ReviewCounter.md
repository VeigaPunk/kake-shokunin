# ReviewCounter — round 88, C1 counter `c88_defect_queue.py`

Seat: reviewer (leaf). Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Scope: attack the C1 counter `LANE/.ufo/waves/round-88/c88_defect_queue.py` with independent
mirror fixtures; confirm the repaired-tool mirror closes all three items; audit the counter's
read surface. No production edits, no commits, no delegation.

Bytes measured (sha256, before and after the seat):

| object | sha256 |
|---|---|
| `.ufo/waves/round-88/c88_defect_queue.py` | `1d550923261bb8e68859fcab48e1fdca61913d790ec288d4947ecffd47db0aa5` |
| `frozen/base-cache_current_age.py` | `d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a` |
| `frozen/base-cache-current-age.md` | `8bbbeb9edf7e595b2e3edabb39d44c9f0716091bea441b44ece79265c3f07eef` |
| `frozen/base-gate-agreement-ledger.json` | `ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506` |
| `vary-cases.json` | `c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d` |

Freeze integrity checked: the three frozen blobs equal the bytes at `f4479c14` for
`scripts/cache_current_age.py`, `corpus/knowledge/cache-current-age.md`,
`corpus/knowledge/gate-agreement-ledger.json` (sha256 MATCH each). The C1 counter is
byte-identical to freeze v2 (`8063739`) and to current HEAD `52e41d2d`.

Command template for every mirror attack (run from my scratch, `TMPDIR` explicit):

```
TMPDIR=/fast/scratch/hyaku/kake-r88/ReviewCounter/work \
python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py \
  --mirror /fast/scratch/hyaku/kake-r88/ReviewCounter/fixtures/<case> \
  --work /fast/scratch/hyaku/kake-r88/ReviewCounter/work
```

Raw receipts (one file per case, exact stdout/stderr/exit) are in
`.ufo/waves/round-88/w1/ReviewCounter/receipts/`; `results.json` holds exit + detail per case;
`build_fixtures.py` and `run_attacks.py` reproduce every fixture and run.

## 1. Attack results (a)–(e)

| # | fixture | intent | exit | JSON detail | survives? |
|---|---|---|---|---|---|
| a | `a-records-only` | all prose fixed, frozen base tool kept | 1 | `{"D1-…": [], "D2-diagnostic-type": ["float input diagnostic does not name float (or still says boolean)"], "D3-…": []}` | no — D2 reopens alone |
| b | `b-ledger-row-newdigest` | only one ledger row `"agree"`→`"disagree"`, companion digest updated to the changed bytes | 1 | `{"D1-ledger-companion": ["ledger bytes differ from the frozen base copy"], "D2-…": [], "D3-…": []}` | no — D1 reopens alone |
| b′ | `b-ledger-row-staledigest` | same row change, companion keeps the frozen digest | 1 | `{"D1-ledger-companion": ["ledger bytes differ from the frozen base copy"], …}` | no |
| b″ | `b-ledger-whitespace` | single no-op byte change (`"admit",`→`"admit" ,`) | 1 | `{"D1-ledger-companion": ["ledger bytes differ from the frozen base copy"], …}` | no |
| c1 | `c1-truncated-digest` | companion quotes only `ef58f9092c32179de6e6` (20 hex) | 1 | `{"D1-ledger-companion": ["companion does not quote the ledger sha256"], …}` | no |
| c2 | `c2-wrong-digest` | companion quotes `f…f` (64 hex) | 1 | `{"D1-ledger-companion": ["companion does not quote the ledger sha256"], …}` | no |
| c3 | `c3-path-suffix-trap` | `source:` names `corpus/knowledge/gate-agreement-ledger.json.bak` (does not exist) + correct digest | 0 | `{"D1-ledger-companion": [], "D2-…": [], "D3-…": []}` | **YES — false green (F4)** |
| c4 | `c4-path-other-dir` | `source:` names `archive/corpus/knowledge/gate-agreement-ledger.json` (does not exist) | 0 | `{"D1-ledger-companion": [], …}` | **YES — false green (F4)** |
| c5 | `c5-truncated-path` | `source:` names `corpus/knowledge/gate-agreement-ledger` (no `.json`) | 1 | `{"D1-ledger-companion": ["companion source: line does not name the ledger path"], …}` | no |
| c6 | `c6-trio-after-seven-junk-lines` | 5 junk lines, then the trio | 0 | all `[]` | **YES — false green (F9, lenient window)** |
| c7 | `c7-trio-at-line-9` | 6 junk lines, trio starts at line 7–9 | 1 | `{"D1-ledger-companion": ["companion head lacks a filled source: line", … "companion does not quote the ledger sha256"], …}` | no — pins the window at 8 lines |
| d1 | `d1-insert-contradicting-claim` | recheck fixed + an inserted line asserting the opposite of the entry's claim | 0 | all `[]` | **YES, but contract-permitted** (pure insertion) — see §3 |
| d2 | `d2-plain-claim-rewrite` | one claim line rewritten in place | 1 | `{"D3-recheck-path": ["history-preservation violation at base line 30 (replace)"], …}` | no — in-place rewrite is caught |
| d3 | `d3-crlf-line-endings` | every line terminator LF→CRLF (entry 5662→5741 bytes, 79 CRLF lines) | 0 | all `[]` | **YES — false green (F5)** |
| d4 | `d4-stale-recheck-moved-to-body` | stale r87 recheck text (with `/fast/scratch` and `TMPDIR=`) kept as an inserted body line | 0 | all `[]` | **YES, contract-permitted** (token rule is recheck-line only) |
| e0 | `e0-offbyone-caught` | repaired diagnostics, `current_age + 1` | 1 | `{"D2-diagnostic-type": ["valid input did not emit the six expected integer terms", "tool selftest is not green"], …}` | no — the tested payload's arithmetic is checked |
| e1 | `e1-hardcoded-valid-output` | correct diagnostic words, constant output table for every accepted input | 0 | all `[]` | **YES — false green (F1)** |
| e2 | `e2-wrong-arith-age-omitted` | correct diagnostics, `max()` dropped when `age_value` is omitted; tool's real selftest kept | 0 | all `[]` | **YES — false green (F2)** |
| e3 | `e3-float-terms` | six `float` terms, real selftest | 1 | `{"D2-diagnostic-type": ["tool selftest is not green"], …}` | no — only because the real selftest crashed on the `10**5000` fixture (`OverflowError`), not because of a type check |
| e3b | `e3b-float-terms-stub-selftest` | same float terms, stub `--selftest` printing `selftest: 61 isolated CLI fixtures passed` | 0 | all `[]` | **YES — false green (F3)** |
| r0 | `r0-nonnumeric-cadence-control` | `recheck: soon or source change` | 1 | `{"D3-recheck-path": ["recheck line does not open with a cadence or ISO date"], …}` | no |
| r1 | `r1-bare-number-cadence` | `recheck: 5` | 0 | all `[]` | **YES — false green (F6)** |
| r2 | `r2-year-only-cadence` | `recheck: 2026` | 0 | all `[]` | **YES — false green (F6)** |
| r3 | `r3-bare-tmp-path` | `recheck: 180d; the command runs under /tmp` | 0 | all `[]` | **YES — false green (F10)** |
| r4 | `r4-shell-var-no-equals` | `recheck: 180d; run with $TMPDIR set by the operator` | 0 | all `[]` | **YES — false green (F10)** |
| d5 | `d5-negated-mktemp-command` | negated mktemp line inserted directly after the recheck line | 1 | `{"D3-recheck-path": ["history-preservation violation at base line 3 (replace)"], …}` | no — rejected for the positional reason in F7, not the negation |
| d5b | `d5b-negated-mktemp-in-body` | same negated line inserted in the body | 0 | all `[]` | **YES — false green (F8)** |
| d6 | `d6-neutral-insert-after-recheck` | neutral inserted line directly after the recheck line | 1 | `{"D3-recheck-path": ["history-preservation violation at base line 3 (replace)"], …}` | **false red (F7)** |
| d7 | `d7-neutral-insert-in-body` | same line inserted in the body | 0 | all `[]` | control for F7 |

## 2. Surviving mutants

### F1 [HIGH] D2 accepts a hardcoded output table
`item_d2` runs exactly one accepted payload (`VALID`, `age_value: 5`) and compares to the
constant `VALID_OUT`. `e1` validates types/ranges exactly like the repaired tool, then
`print(json.dumps(OUT))` — the same six values for every accepted input.
Evidence: counter exit 0, all items closed; on the entry's own alternate valid case
(`{"date_value":95,"request_time":90,"response_time":100,"now":130}`) the mutant returns
`{"apparent_age":20,"response_delay":10,"corrected_age_value":15,"corrected_initial_age":20,"resident_time":30,"current_age":50}`
where the base tool returns `{"apparent_age":5,"response_delay":10,"corrected_age_value":10,"corrected_initial_age":10,"resident_time":30,"current_age":40}`.
The item's "valid input still emits the six integer terms" cannot distinguish a calculator
from a lookup table keyed on the one scored payload.

### F2 [HIGH] D2 accepts wrong arithmetic on the Age-omitted branch, with the tool's own real selftest green
`e2 = repaired_tool()` with `corrected_initial_age = max(apparent_age, corrected_age_value)` →
`... if age_value else apparent_age`. Diagnostics are correct, and the tool's real selftest is
green (`selftest: 61 isolated CLI fixtures passed`, exit 0 — none of the 61 covers
"Age omitted **and** transit > Date-based age").
Evidence: counter exit 0, all items closed, while:
- entry checklist item 2 (`Date60/request45/response60/now75`, Age omitted): base emits
  `current_age 30`, mutant emits `15` (`corrected_initial_age 0`);
- divergence case (`Date95/req90/res100/now130`): base `current_age 40`, mutant `35`.
This is the exact failure mode the contract's D2 sentence is meant to exclude, and the
counter's single payload (`age_value: 5`) never reaches it.

### F3 [MEDIUM-HIGH] D2's term-type gate is `==`, and the selftest gate is a printed string
`obj != VALID_OUT` uses Python equality, so `20.0 == 20`; the counter never checks
`type(value) is int`. `e3b` emits six floats and a stub `--selftest` that prints
`selftest: 61 isolated CLI fixtures passed` and exits 0. Counter exit 0, D2 closed.
Direct evidence: `float_terms_equal_VALID_OUT=True types=['float']`.
The only barrier to a float-emitting tool is the candidate's own selftest, and the counter
accepts that on `p.returncode == 0 and 'selftest' in p.stdout.lower()` — a string any
candidate can print. `e1` also relies on this.

### F4 [MEDIUM] D1's ledger-path binding is a substring test
`item_d1` accepts any `source:` line containing `corpus/knowledge/gate-agreement-ledger.json`
as a substring. `c3` names `…/gate-agreement-ledger.json.bak`; `c4` names
`archive/corpus/knowledge/gate-agreement-ledger.json`. Neither path exists (`ls`: "No such
file or directory"; no `archive/` directory). Counter exit 0, D1 closed. The item's purpose is
that the companion *names the ledger path*; a look-alike that binds nothing passes, and only
`c5` (path missing the `.json` suffix entirely) is rejected.

### F5 [MEDIUM] D3's "byte-identically" is a per-split-line identity
`item_d3` compares `str.splitlines()` output, which strips `\r\n` terminators. `d3` rewrites
all 79 line endings to CRLF: entry 5662 → 5741 bytes, `splitlines()` equal, counter exit 0,
D3 closed. The contract says "preserve every other base line byte-identically"; every
preserved line's bytes changed. The same mechanism would accept any line-terminator
normalization that `str.splitlines()` folds.

### F6 [MEDIUM] D3's cadence test accepts any digit-leading recheck line
Predicate: `rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())`.
The second disjunct is true for any 1–4 digit prefix, so `recheck: 5` (`r1`) and
`recheck: 2026` (`r2`) both close D3 (exit 0), while the non-numeric control `r0` is rejected.
A line that names no cadence and no date passes.

### F7 [MEDIUM] D3 is over-strict: a contract-permitted insertion next to the recheck line is a violation
`d6` inserts a neutral line immediately after the fixed `recheck:` line. difflib merges that
insertion into the recheck `replace` opcode, making it 1→2 lines, which fails the special case,
and D3 opens with `history-preservation violation at base line 3 (replace)`. The identical line
inserted in the body (`d7`) passes. The contract permits "pure insertions"; an honest repair
that appends a note to the metadata block is rejected. This is a false red, not a false green,
but it is a counter defect against the stated predicate.

### F8 [LOW-MEDIUM] D3's mktemp requirement is token presence
`d5b` inserts `4. Never run \`mktemp -d\`; use a fixed path for scripts/cache_current_age.py --selftest.`
in the body: all three tokens present, instruction negated, counter exit 0, D3 closed.
(`d5` places the same line next to the recheck line and fails only for the F7 positional reason.)

### F9 [LOW] D1's "opens with" is a first-8-lines window
`c6` (5 junk lines then the trio) closes D1; `c7` (6 junk lines, `source:` at line 7,
`recheck:` at line 9) opens it. The window is exactly `splitlines()[:8]`, so the trio need not
open the file.

### F10 [LOW] D3's ephemeral-token list is literal
`r3` (`… /tmp` without trailing slash) and `r4` (`$TMPDIR` without `=`) close D3. The
contract enumerates the three literal tokens `/fast/scratch`, `TMPDIR=`, `/tmp/`, so this is a
contract-level limit rather than a deviation from its letter — but the same ephemeral class the
item removes is admitted by spelling it differently.

### F11 [INFO] Counter selftest: 11 checks, 10 distinct mutants
`junk_prose()` and `base_tool()` write byte-identical trees (both install
`frozen/base-cache_current_age.py`). The contract's "one mutant per item, a junk-prose tree" is
satisfied, but the junk-prose check adds no independent mutation, and no selftest case covers
F1–F10. The selftest is self-confirming at 11/11 (verified, matches the committed
`controls/c1-selftest.txt` line for line).

## 3. Attack (d) precisely

The literal attack — "a claim line rewritten in a way an insertion could mask" — does **not**
survive for a real byte edit: `d2` rewrites one claim line in place and D3 opens
(`history-preservation violation at base line 30 (replace)`). difflib matches whole lines only,
so a deletion or in-place change always yields `delete`/`replace`; a rewrite can only be
"masked" by leaving the original line in place and *adding* a contradicting line (`d1`) or
moving stale text into the body (`d4`). Both are pure insertions, which the contract explicitly
permits ("other differences must be pure insertions"), so they are contract-permitted and not
counter false greens. The real D3 defects are F5 (byte identity not enforced), F6 (cadence
vacuous), F7 (positional false red), F8 (negated command accepted).

## 4. Converse: the repaired mirror does close all three

| case | exit | predicate |
|---|---|---|
| independent green built from frozen bytes + my own companion/entry/tool repair (`A0-green`) | 0 | `C1v1 revision=mirror:… items=3 open=0 closed=3 met=true`, detail all `[]` |
| the counter's own `mirror_tree()` green (`A0-green-counter-mirror`, generated by importing the module) | 0 | same |
| counter selftest | 0 | `selftest: 11/11 passed`, identical PASS list to `controls/c1-selftest.txt` |
| base tree (`A0-base`, pure frozen bytes) | 1 | `open=3 closed=0 met=false` with the exact three detail strings of `controls/base-c1.txt` |
| `--root LANE --revision f4479c14…` | 1 | stdout byte-identical to `controls/base-c1.txt` (`diff` exit 0) |
| repaired tool's own selftest | 0 | `selftest: 61 isolated CLI fixtures passed` |

So the green/converse direction is sound *for the mutations the counter models*: all three
items close on a genuine repair, and the base reopens all three. What fails is the attack
surface in §2.

## 5. Read-surface audit (must read lane bytes only)

Static: the only data reads in the source are `FROZEN/*` (three frozen lane blobs), the
`--mirror` tree the caller names, and `git -C <root> show/rev-parse` on `--root` (lane bytes at
a revision). No `controls/`, no `.ufo/waves/*/w1` receipt, no fleet path, no URL, no network
import. The docstring's claim ("No receipt, fleet input or other claim is read") is accurate.

Dynamic: `strace -f -e trace=openat` over the green mirror run. Lane paths touched:
`.ufo/waves/round-88` (directory), `frozen/base-cache-current-age.md`,
`frozen/base-gate-agreement-ledger.json`. Everything else was `/usr/lib/python3.14`,
`/usr/bin/python3`, `/etc/{ld.so.cache,localtime,ssl/openssl.cnf}` interpreter startup, or my
fixture/work dirs. `strace -f -e trace=socket,connect,sendto` returned no lines: no network.

Limits of this audit: `item_d2` executes *candidate bytes* via `sys.executable` with inherited
cwd/env, so the candidate (not the counter) can read anything; the counter itself is confined,
but it does not sandbox what it runs. Also `_run_tool` writes a fixed filename
(`work/cache_current_age.py`) and unlinks it, so two counter runs sharing one `--work` would
race; the carrier uses a dedicated work dir.

## 6. Defects in the round's own bookkeeping (outside C1 admission; reported, not judged)

While this seat ran, LANE advanced `f60a852a` → `52e41d2d` **"round-88: freeze amendment v3 —
validation precedes the wildcard rule"** (2026-11-04 15:58:05 -0300; wave dispatched 15:52:15).
The commit changed:

- `c88_vary.py` (5 lines): `if star: return 'mismatch'` moved after the header-map
  normalization/validation, so a malformed map is `invalid` even with `*`;
- `contract.md`: freeze history and the C2 profile/control-score sentences;
- `controls/base-c2.txt`: frozen `random_sha256` `004a8eb7…` → `52714a5f…`;
- `controls/ctl-c2-constant-{match,mismatch,invalid}.txt` and the contract's own numbers
  (`9/20 + 112/200` → `9/20 + 109/200`; `4/20 + 21/200` → `4/20 + 24/200`);
- new `w1/L1/vary_match.py`, `controls/c1-selftest.txt`, `controls/c2-selftest.txt`.

Two factual points:
1. The C1 surface is untouched: `c88_defect_queue.py`, `vary-cases.json` and the contract's C1
   section are byte-identical to freeze v2, so every finding above holds at both v2 and HEAD.
   (The contract file hash changed `b8f7db94…` → `639035d3…`; the only C1-mentioning line in
   the diff is the freeze-history sentence.)
2. The v3 history paragraph says "No item, case, threshold, control or target moved", but the
   same commit rewrote the C2 control receipts and the contract's C2 control scores, and the
   contract's C2 kill rule says "the case set, the seed, the generator and the reference are not
   edited after scoring". The reference was edited after the base C2 control had been measured
   (`controls/base-c2.txt` first committed at `f60a852a`). Whether any *candidate* had scored
   before 15:58 is L1's call; any C2 receipt printed before that carrying
   `random_sha256 004a8eb7…` is stale against the current counter. I do not adjudicate C2.

## 7. Residual risk and verification gaps

- D1/D3 are textual by the contract's own statement; F4/F5/F6/F8/F9 are the false greens that
  survive in that space, and the non-author closure (a human/independent tree that writes the
  real files) remains the only catch for them, exactly as the contract's "Limits" says.
- D2 is behavioural but bounded to three payloads (valid, float, bool) and a candidate-printed
  selftest banner. F1/F2/F3 mean a tool can pass D2 with wrong arithmetic off the scored
  payload or with non-integer output. If D2 is to be the diagnostic-type item only, the
  contract should say so; as written ("the valid input still emits the six integer terms") the
  predicate is weaker than its wording.
- I did not run the carrier (no production edits) and did not score C2; `--mirror` receipts
  carry `revision=mirror:<path>`, so they are evidence about behaviour, not carrier predicates.
- The counter's own selftest never exercises the F1–F10 shapes; its 11/11 is a lower bound on
  what the counter enforces, not a measure of the false-green space.
- Candidate code executed by `item_d2` is unconstrained; a future carrier that runs counters
  over a tree written by an adversary inherits that.

## 8. Environment / tooling

No tool was installed or upgraded (PACMAN untouched). Used: `/usr/bin/python3` 3.14.8,
`git` 2.56.0, `strace` 7.2. No network access beyond none; no credentials used.

Scratch `/fast/scratch/hyaku/kake-r88/ReviewCounter/` held one fixture tree per case plus the
receipts; receipts, `results.json`, both scripts and the strace logs were copied into
`.ufo/waves/round-88/w1/ReviewCounter/` and the scratch directory was deleted before yield.
No production byte was written; the only lane writes are this report and that directory.
