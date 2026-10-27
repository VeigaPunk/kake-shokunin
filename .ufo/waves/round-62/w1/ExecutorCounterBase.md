# ExecutorCounterBase — round-62 C1 frozen-counter base-control verification

Seat item: independently run the frozen counter `c62_calibration.py` against the base revision
`c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` and confirm the recorded output. Advisory only: no claim,
counter, criterion, score, or lane-file mutation was performed. All work below is read-only against
the lane plus a disposable scratch fixture under `/fast/scratch/hyaku/kake-r62/ExecutorCounterBase/`.

## VERDICT

**Base control CONFIRMED.** The frozen counter, run from the lane root against the frozen base
revision, reproduces the wave-recorded base-control exactly, on every repeat run, and exits 1.

```
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Wave-recorded base-control was `unresolved=1 quote_correction=0 criterion=0 lesson_gate=0
source_row=1 met=false exit 1`. Every one of the six fields matches, and the exit code matches.
The counter is additionally shown below to discriminate correctly (met=false at base, met=true only
when all four required artifacts land), so it is a live predicate rather than a constant.

## Counter identity (frozen artifact integrity)

Counter path: `.ufo/waves/round-62/c62_calibration.py` (lane
`/home/vgpnk/Projects/shokunin/kake-shokunin`).

```
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

Expected (from the round-62 brief): `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`
— **identical**. Size 2488 bytes; mtime `2026-10-27 08:55:30.046849951 -0300` unchanged before and
after every run below (the counter is read-only and was never rewritten).

Base revision confirmed present and current in the lane:

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kake-shokunin
$ git -C ... cat-file -t c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
commit
$ git -C ... log --oneline -3 c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
c341a7a round-61 verifier spot-check (integrator, hyaku): non-author admit/reject
51ef86c round-61: harden capture ingress and record HTTPS probe
7b3d8c5 round-61: record verdicts, source measurements, C2 counter v2 and capture hardening
```

## Exact command and output — base control

Run from the lane root (`cwd=/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

### Determinism

The identical output line and `exit=1` were produced on **five** consecutive invocations
(runs 1–4 as separate shell calls plus the final re-run), and identically when invoked with an
absolute `--root` from an unrelated cwd (`/fast/scratch/hyaku/kake-r62/ExecutorCounterBase`), and
identically when `--revision` was omitted (the script's `BASE` default resolves to the same
revision):

```
$ cd /fast/scratch/hyaku/kake-r62/ExecutorCounterBase
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root .
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Interpreter: `Python 3.14.8 (main, Oct 2 2026, 10:23:31) [GCC 16.2.1 20260810]`.

## Component-by-component derivation (independent recomputation)

Rather than trusting the counter's summary line, each of its five inputs was recomputed directly
from the committed Git blobs at the base revision with an independent script, reading the same five
paths the counter reads:

```
$ python3 - <<'EOF'
import subprocess
ROOT="/home/vgpnk/Projects/shokunin/kake-shokunin"
REV="c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13"
PATHS={"spot":"corpus/lessons/round-61-verifier-spotcheck.md",
       "knowledge":"corpus/knowledge/response-header-expectations.md",
       "quality":"corpus/QUALITY.md","lesson":"corpus/lessons/round-62.md",
       "sources":"corpus/SOURCES.md"}
QUOTE="response header can be used to require checking of a response’s Content-Type header against the destination of a request"
CRITERION="substantive located quote"
def blob(p):
    r=subprocess.run(["git","-C",ROOT,"show",f"{REV}:{p}"],capture_output=True)
    return "" if r.returncode else r.stdout.decode("utf-8",errors="replace")
d={k:blob(p) for k,p in PATHS.items()}
print("blob present:",{k:bool(v) for k,v in d.items()})
dis=[(i+1,l) for i,l in enumerate(d["spot"].splitlines()) if "S432" in l and "Disagree" in l]
print("disagreement count:",len(dis))
print("QUOTE in knowledge:",QUOTE in d["knowledge"])
print("'S432 §3.6' in knowledge:","S432 §3.6" in d["knowledge"])
print("'Round-62 correction' in knowledge:","Round-62 correction" in d["knowledge"])
print("CRITERION in quality:",CRITERION in d["quality"])
print("'round-61-verifier-spotcheck.md' in quality:","round-61-verifier-spotcheck.md" in d["quality"])
print("source_row ('| S432 |' in SOURCES):","| S432 |" in d["sources"])
EOF
```

Output:

```
blob present: {'spot': True, 'knowledge': True, 'quality': True, 'lesson': False, 'sources': True}
disagreement count: 1
  line 33 -> | S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body `.ufo/waves/round-61/sources/S432.html` | D
QUOTE in knowledge: False
'S432 §3.6' in knowledge: True
'Round-62 correction' in knowledge: False
correction = 0
CRITERION in quality: False
'round-61-verifier-spotcheck.md' in quality: False
criterion = 0
lesson_gate = 0
source_row ('| S432 |' in SOURCES): True
```

All five components reconcile with the counter's printed line:

| Counter field | Value at base | Independent basis |
|---|---|---|
| `disagreements` | 1 | `corpus/lessons/round-61-verifier-spotcheck.md` line 33 is the only line containing both `S432` and `Disagree` (case-sensitive). Lines 36, 41, 42, 46 mention S432 but not the capitalized `Disagree` marker. |
| `unresolved` | 1 | `resolved` is False (three of four artifact flags are 0), so `unresolved = disagreements = 1`. |
| `quote_correction` | 0 | Requires all three of: the 120-char `QUOTE` string, the literal `S432 §3.6`, and the literal `Round-62 correction` in `corpus/knowledge/response-header-expectations.md`. `S432 §3.6` is already present (knowledge lines 75/83/86); the other two are absent. |
| `criterion` | 0 | Requires `substantive located quote` AND `round-61-verifier-spotcheck.md` in `corpus/QUALITY.md`. Neither is present at base. |
| `lesson_gate` | 0 | `corpus/lessons/round-62.md` does not exist at the base revision (`git cat-file -e` → missing), so all four tokens (`## Gate`, `S432`, `Agree`, `Reject`) are absent. |
| `source_row` | 1 | `corpus/SOURCES.md` line 178 begins `\| S432 \|`. This flag is already satisfied at base and is a *regression guard*, not a work item. |
| `met` | false | `unresolved == 0 and resolved` → False. Exit 1. |

## Predicate discrimination — the counter is live, not constant

Measured in a disposable fixture (never in the lane). The fixture was built by
`git archive` of the base revision into `/fast/scratch/hyaku/kake-r62/ExecutorCounterBase/repo`,
then `git init` + one commit, giving an independent SHA namespace (`24ebd479…`) so no lane Git state
was touched. Fixture root asserted before every mutation:

```
$ git -C /fast/scratch/hyaku/kake-r62/ExecutorCounterBase/repo rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r62/ExecutorCounterBase/repo
```

Cumulative build-up (each row is the fixture HEAD after that commit):

| Fixture state | Counter output | exit |
|---|---|---|
| base snapshot only | `disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 |
| + knowledge correction appended | `disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 |
| + QUALITY criterion appended | `disagreements=1 unresolved=1 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 met=false` | 1 |
| + `corpus/lessons/round-62.md` gate written | `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` | 0 |

The counter therefore gates on all four artifacts: none → false, three of four → false, all four
→ true. It is not satisfiable by a do-nothing edit, and it is not permanently false.

## Mutation sensitivity — how each flag can be knocked back to 0

Every mutation below was applied to the *satisfied* fixture state (all four flags 1) and reverted
afterwards. Each one alone flips `met` back to `false` (exit 1). This is the practical guidance
for the implementing seat.

**Quote corrections (`quote_correction` → 0):**

| Mutation | Result |
|---|---|
| `destination of a request` → `destination of the request` | `quote_correction=0 … met=false`, exit 1 |
| `response’s` → `response's` (straight ASCII apostrophe) | `quote_correction=0 … met=false`, exit 1 |
| wrap the quote across a markdown line break (`against the\ndestination of a request`) | `quote_correction=0 … met=false`, exit 1 |
| wrap `Content-Type` in backticks (``a response’s `Content-Type` header``) | `quote_correction=0 … met=false`, exit 1 |
| `## Round-62 correction` → `## Round 62 correction` (hyphen dropped) | `quote_correction=0 … met=false`, exit 1 |
| `S432 §3.6` → `S432 3.6` (section sign dropped) | `quote_correction=0 … met=false`, exit 1 |

The `QUOTE` constant is byte-exact and **must be copied from the source text, not retyped**:
it contains U+2019 (`’`), a literal `Content-Type` with no backticks, and it must appear on one
logical line. `S432 §3.6` must use U+00A7 (§), and `Round-62 correction` must use U+002D (hyphen).
Case matters throughout: `round-62 correction` in lowercase prose does **not** satisfy the flag.

**Criterion (`criterion` → 0):**

| Mutation | Result |
|---|---|
| replace `corpus/lessons/round-61-verifier-spotcheck.md` with `corpus/lessons/other.md` | `criterion=0 … met=false`, exit 1 |

Both substrings are required — the literal phrase `substantive located quote` *and* the file path
reference `round-61-verifier-spotcheck.md`.

**Lesson gate (`lesson_gate` → 0):**

| Mutation | Result |
|---|---|
| `## Gate` → `## Gates` (still contains `## Gate` as a prefix — note this **passed**, `lesson_gate=1`) | met=true — see caveat below |
| `Agree` → `Agreex` (still contains `Agree` — **passed**, `lesson_gate=1`) | met=true — see caveat below |
| `## Gate`/`Agree`/`Reject` all removed from the lesson | `lesson_gate=0 … met=false`, exit 1 |
| `Agree` → `Approve` (literal removed) | `lesson_gate=0 … met=false`, exit 1 |
| `Reject` → `Approve` (literal removed) | `lesson_gate=0 … met=false`, exit 1 |
| `S432` absent from the lesson | `lesson_gate=0 … met=false`, exit 1 |

Caveat worth flagging to the integrator: the `lesson_gate` test is a plain substring test, so
`## Gates` and `Agreex` satisfy it. The gate is satisfied by *presence of the tokens*, not by their
correct semantic role. That is a property of the frozen counter (which must not change) and not a
defect to fix — but it means the lesson file's prose quality is on the integrator, not the counter.

**Source row (`source_row` → 0):**

| Mutation | Result |
|---|---|
| `\| S432 \|` → `\| S432\|` (space dropped) | `source_row=0 … met=false`, exit 1 |
| delete the S432 row from `corpus/SOURCES.md` | `source_row=0 … met=false`, exit 1 |

`source_row` is already 1 at base and acts as a **no-deletion guard** on `corpus/SOURCES.md`. It
is satisfied by keeping the existing row exactly as-is (`| S432 |` with both spaces). It does not
require any new SOURCES work.

## The `Disagree` row is preserved, not flipped — counter confirms this is safe

The contract states the existing S432 row in `corpus/lessons/round-61-verifier-spotcheck.md` is
kept and must **not** be marked rejected. The counter is consistent with that instruction: the
`Disagree` marker on the row is what *creates* the `disagreements=1` reading, but `unresolved` is
governed by `resolved` (all four artifact flags), not by `disagreements`. Verified:

| Fixture state | Counter output | exit |
|---|---|---|
| full fix, `Disagree` row **kept** (contract shape) | `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` | 0 |
| full fix, `Disagree` row **removed** | `disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` | 0 |
| full fix, marker flipped `Disagree` → `Reject` | `disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` | 0 |

The counter is indifferent between these dispositions, so the *contract instruction* (keep the row
as `Disagree`) is not enforced by the counter but is not contradicted by it either. **Recommendation
to the integrator: keep the row exactly as it is at base, per the contract — do not edit, do not
flip the marker.** The counter's `disagreements=1` at the after-state is expected and correct, not a
failure signal; `unresolved=0` is the field that carries the resolution.

## Committed-blob-only semantics (the counter reads Git, not the working tree)

`blob()` in the counter is `git -C <root> show <rev>:<path>`. Verified that a dirty working tree
does not influence the measurement: two junk lines appended to
`corpus/knowledge/response-header-expectations.md` and `corpus/QUALITY.md` in the fixture, with the
same `--revision` passed, still produced the identical base line and `exit=1`:

```
revision=24ebd47922bb91ae4c546afc37160f073645241a disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Practical consequence for the implementing seat: the after-state must be **committed** for the
counter to see it. The contract already requires measurement "at the measured committed revision";
this confirms the counter enforces that mechanically.

## Error paths (counter robustness)

| Condition | Output | exit |
|---|---|---|
| `--revision deadbeef…` (nonexistent) | `could-not-evaluate: missing verifier spot-check` (stderr) | 2 |
| spot-check file removed from the tree at that revision | `could-not-evaluate: missing verifier spot-check` (stderr) | 2 |

Exit code 2 is the distinct "could not evaluate" code, distinct from 1 ("evaluated, not met").
The base control's exit 1 is therefore a genuine negative evaluation, not a harness failure.

## Source grounding for the `QUOTE` constant (independent verification)

The counter's `QUOTE` constant must be a faithful, de-marked-up rendering of S432 §3.6. Verified
against the retained round-61 body at `.ufo/waves/round-61/sources/S432.html`, which is committed at
the base revision:

```
$ git -C . cat-file -e c341a7a4...:.ufo/waves/round-61/sources/S432.html   # -> committed
$ git -C . log --oneline -1 -- .ufo/waves/round-61/sources/S432.html
d2da25de round-61: integrate sourced header audit, rechecks, and w2 hardening; C1 withheld
$ git -C . show c341a7a4...:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
$ sha256sum .ufo/waves/round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
```

Working-tree copy is byte-identical to the committed blob. §3.6 spans lines 6149–6156 of the
retained body (contract cites 6151–6154 as the substantive body lines):

```
6149:    <h3 class="heading settled" data-level="3.6" id="x-content-type-options-header">…`<code>X-Content-Type-Options</code>` header…
6150:    <p>The
6151: `<dfn …><code>X-Content-Type-Options</code></dfn>`
6152: response <a …>header</a> can be used to require checking of a <a …>response</a>’s
6153: `<code>Content-Type</code>` <a …>header</a> against the <a …>destination</a> of a
6154: <a …>request</a>.
6155:
6156: </p>
```

De-marking the §3.6 segment (strip tags, strip backticks, collapse whitespace) yields exactly:

```
'response header can be used to require checking of a response’s Content-Type header against the destination of a request.'
```

and this **starts with** the counter's `QUOTE` constant (120 chars, containing U+2019). Cross-check
on the whole file: the quote is present in the tag-stripped + backtick-stripped + whitespace-
normalized text (`True`), but **not** in the raw HTML (`False`) and **not** in the tag-stripped text
with backticks retained (`False`) — the backtick around `Content-Type` is what breaks it.

This is the one place where a copy error is easy: the quote as rendered in the HTML source has
`` `Content-Type` `` in backticks and the sentence is broken across lines by markup. The counter
requires the **de-marked-up single-line** form with U+2019 and no backticks. The round-61 knowledge
entry currently quotes only the fragment `> "can be used to require checking of a"` and the generic
lead-in `> "Web developers and conformance checkers must use the following"` (knowledge entry line
79) — which is exactly the lead-in the round-61 spot-check rejected, and exactly what the contract's
correction must replace/supersede.

## Lane and artifact integrity

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain
?? .ufo/waves/round-62/
$ git -C ... rev-parse HEAD
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

- Lane HEAD is unchanged at the base revision; the only untracked entry is the wave's own
  `.ufo/waves/round-62/` directory (pre-existing, holds the frozen counter + spec; not created by
  this seat). No lane Git/jj/index mutation was performed. `jj` log shows the working-copy change id
  `lumzmpwnqmkm` / commit `1108744228b5`, untouched.
- The frozen counter file was not modified: identical sha256 and identical mtime
  (`2026-10-27 08:55:30.046849951 -0300`) before and after all runs.
- No claim, criterion, score, `corpus/` file, or contract file was written or altered.
- Only this seat's report file and its scratch directory were written. Scratch
  `/fast/scratch/hyaku/kake-r62/ExecutorCounterBase/` was removed before yield.
- No installs were performed; no pacman transaction was run; no tool beyond stock
  `python3` (3.14.8), `git`, `sha256sum`, `stat`, `awk`/`grep` was needed.

## Evidence index

| Evidence | Location |
|---|---|
| Frozen counter (unmodified) | `.ufo/waves/round-62/c62_calibration.py`, sha256 `ba7b7737…548d` |
| Contract | `.ufo/waves/round-62/contract.md` |
| Base revision | `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` (`master`, remote-verified per contract) |
| S432 disagreement row (the one `Disagree` hit) | `corpus/lessons/round-61-verifier-spotcheck.md` line 33 |
| S432 harm statements | same file, lines 36, 41, 42, 46 |
| S432 SOURCES row (source_row=1, guard) | `corpus/SOURCES.md` line 178 |
| Knowledge entry, existing generic lead-in quote | `corpus/knowledge/response-header-expectations.md` line 79 (`> "Web developers and conformance checkers must use the following"`); existing `S432 §3.6` location markers at lines 75, 83, 86 |
| Retained S432 body (source of truth for the quote) | `.ufo/waves/round-61/sources/S432.html` lines 6149–6156, sha256 `63b0a018…911b`, committed at `d2da25de` |
| Scratch fixture (deleted after run) | `/fast/scratch/hyaku/kake-r62/ExecutorCounterBase/repo`, fixture root asserted via `git -C … rev-parse --show-toplevel` |

## Risks / blockers

- **None blocking.** The base control is confirmed and the counter's discrimination and mutation
  sensitivity are fully characterised.
- Two soft risks for the implementing seat, both informational:
  1. The `QUOTE` constant must be pasted from the de-marked-up §3.6 text (single line, U+2019
     apostrophe, `Content-Type` unwrapped). Six distinct single-character/single-marker edits each
     silently drop `quote_correction` to 0 — the failure mode is a *quiet* `met=false`, not an error.
  2. `lesson_gate` is satisfied by substring presence (`## Gates` and `Agreex` both pass), so it
     cannot be used as evidence that the round-62 lesson actually records the Agree/Reject decision
     paths. That quality rests with the implementing seat, not the counter.
- The counter is **not** the mechanism that enforces "keep the S432 row, do not mark it rejected";
  it is indifferent to that disposition. The contract instruction must be honored by hand.
