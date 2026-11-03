# ConnOverlap — round 73, w1 (connector)

Cross-claim overlap scan of the frozen round-73 contract (`contract.md`, base
`c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`). Read-only on the lane; every measurement below ran in
a scratch shared clone under `/fast/scratch/hyaku/kake-r73/ConnOverlap/` (deleted before yield).
No predicate, counter, corpus line or control was edited. Nothing was installed (host already had
`python3 3.14.8`, `node v24.21.0`, `git 2.56.0`; pacman untouched).

Clones (all `git clone --shared -q <lane> <scratch>/cloneN` + `checkout -q c1f3d8d4…`; toplevel
asserted for `clone`/`clone2` before the first commit and for `clone3`–`clone5` after the clean
repros — every one printed the scratch path):

```
clone -> /fast/scratch/hyaku/kake-r73/ConnOverlap/clone      (variant chain D/E)
clone2 -> …/clone2                                           (sweep / C3 pin / c66 tests)
clone3 -> …/clone3                                           (clean variant A)
clone4 -> …/clone4                                           (clean prose-only variant B)
clone5 -> …/clone5                                           (clean repo-rooted variant C)
```

## Summary matrix

| # | Claim pair | File(s) | Overlap found | Changes a predicate? |
|---|---|---|---|---|
| O1 | C1 correction tails × harm check “c70 exit 0 at tip” | `LOG.md`, `SCORECARD.md` | `controls/c1-tip.txt` is outside c70’s grammar (no new token). A repo-rooted spelling (`.ufo/waves/round-72/controls/c1-tip.txt`) creates a new **unannotatable** dangling token → c70 exit 1. LOG.md is never read by c70. | No — it decides whether the frozen c70 harm line can be met. |
| O2 | C2 SKILL.md registry row × C3 offline sweep | `SKILL.md`, `corpus/knowledge/freshness-sidecar.json` | Inserting after the “Owned freshness gate registry” last row (line 213) moves 22 of 25 SKILL.md-bound sidecar lines → sweep exit 2 `SKILL.md:365`. The contract requires the row “beyond line 935”; only an insertion after line 935/EOF is safe (measured exit 1, no `Error:`). | No — it decides whether C3’s “no `Error:`” conjunct can hold. |
| O3 | C3 SOURCES.md:140 pin × the SOURCES.md row that C2’s §2b.4 sourced claim opens | `corpus/SOURCES.md`, sidecar entry 140 | C1’s tails and C2’s SKILL.md row are inert here. The S440 row planned after S439 (line 185) leaves line 140 byte-identical (sha unchanged, sweep exit 1). Any insertion at/before line 140 shifts it → sweep exit 2 `corpus/SOURCES.md:140`. | No — it decides whether the single re-pin stays valid at the tip. |
| O4 | C2 SKILL.md row × harm check “c66 agreement ≥ 25” | `SKILL.md`, `.ufo/waves/round-66/c66_gate_status_hostportable.py` | c66’s population is fixed by a hardcoded 28-path map, not by registry rows: a new row cannot change `members=28`, and `.ufo/waves/round-73/c73_tmp_v3.py` is outside the population regex (round 48–59 only). But a row that mentions any frozen member path anywhere flips that member to `duplicate_row` (structural), which drops agreement 25→24. | No — but it can flip the c66 harm line red. |

---

## O1 — C1’s end-of-file correction tails × the frozen c70 pointer counter

### What c70 parses (read at base)

- `.ufo/waves/round-70/c70_pointer_audit.py` reads **only `SCORECARD.md`**: `audit()` line 192-193
  `text = read_scorecard(root, revision)`; `grep -n 'LOG' …/c70_pointer_audit.py` prints nothing
  (exit 0, no lines). The `LOG.md` tail cannot affect c70 at all.
- Token grammar (lines 54-62): repo tokens must begin with `.ufo/`, `corpus/`, `scripts/`,
  `handoffs/` or `considerthese/`; wave-relative `controls/…`, `sources/…`, `w1/…` are not tokens.
- Annotation locus (lines 148-177): only first cells of table rows **inside**
  `## Pointer calibration (round 70)`, and `annotation_cells()` breaks at the first heading after
  that section (line 171). That section closes at SCORECARD line 4765
  (`## Round 70 — declared and measured claims…`), so no appended tail line can annotate anything.
- Append-only conjunct (lines 181-190) is a line-prefix test of `SCORECARD.md` only.

### Baseline and the prescribed tail (variant A)

```
cd <clone> && python3 -B .ufo/waves/round-70/c70_pointer_audit.py \
  --root <clone> --revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
# exit 0
# pointers=359 dangling=17 annotated=17 unannotated=0 met=true
```

Variant A tail (the shape ScribeRow’s `LOG_TAIL`/`SCORECARD_TAIL` describe), appended to both files:

```
[r73-correction 2026-11-03] The round-72 close cited `controls/c1-tip.txt` and `controls/c2-tip.txt`;
both names are superseded. The committed receipt files are
`.ufo/waves/round-72/controls/c1-tip-final.txt` and `.ufo/waves/round-72/controls/c2-tip-final.txt`.
Historical record, not an executable instruction.
```

Clean repro from base (`clone3`, commit `992bf3a0d508659002ef52236af3277d2e65e868`):

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone3> --revision 992bf3a… \
  --base c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
# exit 0
# pointers=361 dangling=17 annotated=17 unannotated=0 append_only=true met=true
```

LOG-only intermediate in the chain clone (commit `56df40326806a5fb22fedcb53b76fa5034a240b5`):

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone> --revision 56df403… \
  --base c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
# exit 0
# pointers=359 dangling=17 annotated=17 unannotated=0 append_only=true met=true
```

**Answer to the seat question:** a tail line that repeats `controls/c1-tip.txt` creates **no new
c70 token** — the `controls/` prefix is not in the repo class and matches neither the home nor the
tmp class. The two corrected repo-rooted paths *are* new resolving tokens (pointers 359→361), which
does not change the predicate (`unannotated` still 0). Dangling stayed 17.

### Prose-only variant (variant B, clean from base)

Tail appended to `SCORECARD.md` naming only the superseded tokens, no corrected repo path
(`clone4`, commit `93fb786129811bc1488cbe2608b92d10b57caf1c`):

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone4> --revision 93fb786… \
  --base c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
# exit 0
# pointers=359 dangling=17 annotated=17 unannotated=0 append_only=true met=true
```

**c70 stays exit 0.** (Same result when the prose tail is stacked on variant A in the chain clone:
`pointers=361 … met=true`, exit 0.)

### The failure mode: a repo-rooted spelling of the superseded token

Tail appended to `SCORECARD.md` (`clone5`, commit `4d75d431dcccaaac3a4e0f98a87de71c77fdedfb`):

```
[r73-correction 2026-11-03] The dead repo path `.ufo/waves/round-72/controls/c1-tip.txt` was
superseded; the committed receipt is `.ufo/waves/round-72/controls/c1-tip-final.txt`.
Historical record, not an executable instruction.
```

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone5> --revision 4d75d43… \
  --base c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
# exit 1
# pointers=361 dangling=18 annotated=17 unannotated=1 append_only=true met=false
# repo unannotated line=4831 token=.ufo/waves/round-72/controls/c1-tip.txt
```

This new token is **structurally unannotatable by an append**:

- Appending an exact-token table row at EOF (`clone`, commit `97f2d9d9fd7444e06245d21cd5f1c22c5d229b20`):
  `pointers=362 dangling=18 annotated=17 unannotated=1 append_only=true met=false`, exit 1 — the
  row sits after the `## Round 73` heading, outside the round-70 calibration section.
- Inserting the same row inside the round-70 section (`clone`, commit
  `dc4e2b9dc7e0e3f0ec90b07cbeb5a9c0ba38ad97`): `pointers=362 dangling=18 annotated=18
  unannotated=0 append_only=false met=false`, exit 1 — annotation works, but the mid-file insert
  breaks the append-only conjunct.

**Conclusion for the integrator:** both C1 tails must keep the superseded names wave-relative
(`controls/c1-tip.txt`, `controls/c2-tip.txt`) and may cite the corrected files either wave-relative
or repo-rooted **only if they resolve** (`.ufo/waves/round-72/controls/c1-tip-final.txt` /
`c2-tip-final.txt` both resolve at base: `git cat-file -e` exit 0). Never write
`.ufo/waves/round-72/controls/c1-tip.txt` or any other repo-rooted spelling of a superseded path in
`SCORECARD.md`; that alone turns the frozen c70 harm line red at the tip.

---

## O2 — C2’s SKILL.md registry row × C3’s offline sweep (sidecar line bindings)

### Bound lines (base, `corpus/knowledge/freshness-sidecar.json`)

`entries` = 174. For `file == "SKILL.md"`: **25 entries**, `.line` values:

`16, 19, 20, 365, 424, 432, 442, 446, 449, 450, 451, 476, 477, 512–521 (10), 815, 935`.
Largest = **935**; all 25 hash-validate at base (0 failing).

`SKILL.md` is 1396 lines. The `### Owned freshness gate registry` table is lines 210-213 (header
210, separator 211, data rows 212-213); its **last data row is line 213**. The last gate-registry
table in the file is lines 1394-1396 (header 1394, separator 1395, single data row 1396).

### Measurements (clone2)

C3’s single re-pin applied first to isolate the SKILL.md placement (entry 142, `corpus/SOURCES.md:140`):

```
old lineSha256 b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47
new lineSha256 4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15
changed entries: 1 (only that field)
```

```
cd <clone2> && node scripts/freshness-sweep.mjs --offline
# exit 1, stderr empty
# VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)
```

Row inserted **after line 213** (literal “after the registry’s last row”), commit
`47c774bca42a9c603071fe3c5d3f86bccf8035e4`:

```
node scripts/freshness-sweep.mjs --offline
# exit 2
# stderr line 1: freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:365
```

Row appended at **EOF (line 1397**, i.e. the next data row of the last registry table), commit
`e0d159e84105693c9f6cefe951e532cc5a08f975`:

```
node scripts/freshness-sweep.mjs --offline
# exit 1, stderr empty
# §paths 191 files · 708 occurrences · 107 unique tokens
# VERDICT: DRIFT — … (identical to the pin-only state)
```

Mechanics: an insertion after line 213 shifts every later line by +1. **22 of the 25** SKILL.md
entries are at lines >213; for **22 of 22** the old line number would then hash a different line
(checked with the sweep’s split-on-`\n` / sha256 rule). An insertion at EOF moves none (max bound
935 < 1397), and line 935’s sha still equals its pinned value
`07d2e4313be3bd0fca4e5b7b7a370d16d8aec9c306375e897c4481daa9dc15b4`.

### Contradiction

`ExecRegistryRow` (item 1/3) says to use “the ‘Owned freshness gate registry’ table … its last
data row’s line number” (= 213), then “confirm the registry insertion point is after [the largest
sidecar `.line`]” (= 935). Those two sentences cannot both hold: 213 is not after 935. The frozen
contract’s C2 sentence (“one appended SKILL.md registry row beyond line 935”) is the satisfiable
one. **Recommendation: append the row after line 935 — concretely, as the next row of the last
gate-registry table (after line 1396)** — not after line 213.

---

## O3 — C3’s `corpus/SOURCES.md:140` re-pin × the other round-73 edits

- **C1’s LOG.md/SCORECARD.md tails:** different files; `corpus/SOURCES.md` is never written by C1.
  Inert for the pin (variant A/B/C runs above touched only LOG.md/SCORECARD.md).
- **C2’s SKILL.md row:** different file, and an insert after 935/EOF moves no SOURCES.md line.
  Inert for the pin.
- **The S440 row (C2 §2b.4 sourced claim / ScribeRow’s `ROW`)** is the only round-73 edit that can
  move SOURCES.md line 140. The registry is id-sorted (`S434…S439` at lines 180-185); S440 belongs
  after S439, i.e. at line 186 — after line 140. Measured (clone2, commit
  `771d42a2c59062bc7fd95bf89ab4eb789064c1f3`):

```
line140 sha before: 4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15
line140 sha after : 4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15
same: True
node scripts/freshness-sweep.mjs --offline   # exit 1, stderr empty (no Error:)
```

- **Negative control** (clone2, commit `2accc1ea8ccc42c8d7a6ce477db12d1799724074`): the same S440
  row inserted *before* line 140 shifts the S132 row to 141:

```
node scripts/freshness-sweep.mjs --offline
# exit 2
# freshness-sweep: Error: paths sidecar binding invalid: corpus/SOURCES.md:140
```

**Answer to the seat question:** neither C1’s tail nor C2’s SKILL.md row invalidates the pin. The
edit that would invalidate it is the S440/SOURCES.md row (or any other SOURCES.md insertion) placed
at or before line 140 — which is not the planned placement, because S440 sorts after S439 at line
185. No SOURCES.md sidecar entry sits beyond line 140, so shifting the notes region (lines 186+)
does not disturb any binding either.

Contract tension worth recording: C2’s separability sentence says C2 “touches
`.ufo/waves/round-73/` and one appended SKILL.md registry row beyond line 935”, but its §2b.4
sourced claim opens a `corpus/SOURCES.md` row (ScribeRow’s `ROW`). That row is a C2-adjacent edit
that lands in C3’s pinned file; it must stay after line 140 (id order does).

---

## O4 — C2’s SKILL.md row × the frozen c66 gate-status counter

### The population is fixed, not registry-derived (quotes at base)

`.ufo/waves/round-66/c66_gate_status_hostportable.py`:

- line 86: `EXPECTED_MEMBERS = 28`
- line 88: `POP_RX = re.compile(r"^\.ufo/waves/round-(\d+)/(?:[a-z0-9-]+/)?c(\d+)_[a-z0-9_]+\.py$")`
- line 113: `FROZEN = {` … 28 path→blob entries
- lines 221-224 (`population_candidates`):
  `return sorted(p for p in entries if (m := POP_RX.match(p)) and m.group(1) == m.group(2) and 48 <= int(m.group(1)) <= 59 and p != SELF_PATH)`
- line 682: `met = (len(present) == EXPECTED_MEMBERS and evaluated == EXPECTED_MEMBERS and held == 3 and structural == 0)`
- lines 505-522 (`eval_member`): rows are read **by name only to require registration and
  uniqueness** — `if not counted: res["classes"] = ["unregistered"]` (516-517) and
  `if len(counted) > 1 or others: res["classes"] = ["duplicate_row"]` (521-522); the member list
  itself comes from `sorted(frozen.items())`, never from rows.

Module-level check (import with the file’s `__main__` guard; no member executed):

```
EXPECTED_MEMBERS = 28 | FROZEN len = 28
.ufo/waves/round-73/c73_tmp_v3.py      => candidate: False | total candidates: 28
.ufo/waves/round-73/c73_wave_pointers.py => candidate: False | total candidates: 28
.ufo/waves/round-59/c59_d.py           => candidate: True  | total candidates: 29
.ufo/waves/round-66/c66_gate_status_hostportable.py => candidate: False | total candidates: 28
```

The round-73 counters are outside rounds 48–59, so the new `.ufo/waves/round-73/c73_tmp_v3.py`
blob is **not** an `extra_member` and **cannot** change `members` from 28. A SKILL.md registry row
is likewise inert for the count: `present` is built from `FROZEN` paths found in the tree.

The selftest confirms the semantics for in-range rounds (base source, lines 1100-1105):
`ck("E.extra_member", codeE == 1 and memE == 28 …)` — an out-of-registry round-59 file yields
`extra_member` while `members` stays 28, exit 1.

### The remaining c66 risk: a row that *mentions* a frozen member

Text-level check with c66’s own `md_tables`/`rows_mentioning` on base `SKILL.md` + one appended
row (no subprocess), member `.ufo/waves/round-52/c52_gate_registry.py`:

```
base        | counted rows: 1 | others: 0 | duplicate_row: False
safe-row    | counted rows: 1 | others: 0 | duplicate_row: False   (row names only .ufo/waves/round-73/…)
unsafe-row  | counted rows: 1 | others: 1 [line index 1396] | duplicate_row: True
```

`others` is any rendered data row anywhere in SKILL.md that mentions the member path outside its
entry row (lines 519-522); `counted` is rows whose **Entry command** cell contains it. A new row
that cites e.g. `.ufo/waves/round-52/c52_gate_registry.py` in its Self-test/Pinned cell therefore
sets that member to `duplicate_row`, which is a structural class (lines 105-110) → `met=false`,
exit 1 [INFERENCE from the code: also `agreement` 25→24 because that member gains a class, which
would breach the frozen harm line “agreement at tip ≥ 25”; I did not re-run the 28-member c66
suite — the base control reads `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0
agreement=25 scores_held=3/3 met=True`].

**Conclusion:** the C2 row cannot change c66’s member count (the seat’s question), but it must not
name any of the 28 frozen member paths, and it must have exactly 8 non-empty cells if it ever
becomes a counted row (line 528-529 `row_incomplete`). Naming only `.ufo/waves/round-73/…` paths
keeps c66 exactly at the base control.

---

## Predicate impact

None of O1–O4 changes a frozen predicate, corpus line, control or kill rule. Each overlap decides
whether a *frozen check on the tip* can be satisfied:

- O1: c70 exit 0 at tip is safe iff the C1 tails never spell a superseded round-72 path
  repo-rooted (wave-relative names + resolving corrected paths stay green).
- O2: C3’s `no Error:` conjunct is safe iff the C2 SKILL.md row is placed after line 935 (append at
  EOF); placement after line 213 makes the sweep exit 2.
- O3: C3’s single-entry re-pin stays valid iff the S440 SOURCES.md row lands after line 140 (id
  order, after S439 at line 185); an insertion at/before 140 re-creates the base failure.
- O4: the c66 harm line stays at `agreement=25` iff the new SKILL row names no frozen member path.

## Verification to run once, after integration (not run here)

1. `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <tip> --base
   c1f3d8d4…` → expect exit 0, `unannotated=0 append_only=true`.
2. `git show <tip>:SCORECARD.md | grep -c '\.ufo/waves/round-72/controls/c1-tip\.txt'` → expect 0
   (no repo-rooted dead spelling).
3. `node scripts/freshness-sweep.mjs --offline` at the tip → expect exit 0 or 1 and **empty
   stderr**; a `paths sidecar binding invalid: SKILL.md:<n>` line means the row was placed before
   line 935.
4. `python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root <clone> --revision <tip>
   --jobs 6 --work <scratch>` → expect `members=28 … agreement=25 … structural=0`.
5. `python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root <lane> --revision <tip>` (delivered
   counter) → expect `dead=2 unannotated=0 append_only=true met=true`; the tails above keep both
   dead tokens named wave-relative and add only resolving round-72 paths.

## Scratch

All five clones, `spec.txt`, `spec-wrapped.txt` and the captured sweep/c70 output files were under
`/fast/scratch/hyaku/kake-r73/ConnOverlap/` and were deleted before yield (`rm -rf`). The lane was
never mutated; no git/jj command ran in it.
