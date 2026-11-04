# ExecC1Derive — round 84 wave w1

Read-only over the lane except this report and `ExecC1Derive/`; scratch
`/fast/scratch/hyaku/kake-r84/ExecC1Derive/` deleted before yield. No production
file written. No tools installed. The counter was run only for steps 2–3 (plus a
clearly-labelled `--revision` cross-check); every step-1 conjunct below is my own
derivation from committed bytes.

## 1. State conjuncts re-derived at the freeze `f358022f`

**D1 (retention side verified; lesson side impossible at freeze).** Retained
RFC bytes `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`: sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, 84,477
bytes, 1,956 lines — identical to the digest the round-83 spot-check recorded,
and the freeze blob equals the worktree file (`git rev-parse
f358022f:…rfc9111.txt` = `git hash-object` = `cef95c761dfcbc6f649019efa2cf5f97dc5f9020`).
All four heading strings are raw substrings, at 1-based lines 97, 98, 106, 117
(TOC) and 1081, 1111, 1203, 1408 (body). `corpus/lessons/round-84.md` is absent
at the freeze (`git cat-file -e` → absent) and absent at HEAD `87cbfd99`, so no
`[r84-correction` line exists: **D1 open at the freeze**, retention conjunct
already true.

**D2 (my own count: 66).** Boundary printed and used: 0-based slice
`lines[837:844]` == physical lines 838–844 inclusive, joined with `\n`, tokens
`re.findall(r"\S+")`. Count = **66**; two independent tokenizers (`str.split()`
and per-line split sum) also give 66. Line 837 (excluded) is blank; line 845
(excluded) is blank; span runs "Another validator is the entity tag…" → "…the
listed entity tags)." So the only value a lesson can truthfully transcribe is
`D2 count=66 span=838-844 measure=words-full-span`. With the lesson absent at
the freeze, **D2 open at the freeze**; nothing to check against yet.

**D3 (spec arrived post-freeze; results still missing).** At the freeze neither
`w1-spec.json` nor `w1-results.json` is tracked (`git ls-tree -r f358022f --
.ufo/waves/round-84` lists neither). At HEAD `87cbfd99` the spec exists; my role
census: scout 2, executor 3, scribe 3, reviewer 2, critic 1, mutation-tester 1,
**connector 1** — the `connector >= 1` half holds from `87cbfd99` on.
`w1-results.json` exists nowhere (not at HEAD, not in the worktree). **D3 open;
missing exactly: a results file with ≥ 1 row `agent=="connector"` and non-empty
output** (contract adds a prose row conjunct — see finding F1).

**D4 (state conjunct HOLDS already).** My parser, written from the contract's
prose rule alone (0–3 leading spaces; `## Registry` section; 11-cell pipe rows,
separator rows skipped; `S\d{3,}` ids; first `https?://[^\s|]+` in the source
cell; normalize = strip fragment, strip one trailing `/`, strip scheme,
lowercase host-before-first-slash; collide when URL seen before and `(url,
scope)` pair new) re-derives **22** W04 collisions. Sorted set equality vs
`controls/census-before.txt` (22 rows, `census_exit=0`, ok line naming
`…/kake-shokunin/corpus/SOURCES.md`): **set_equal=true** over the worktree, the
freeze blob, the base `fe42ad11` blob and the HEAD blob — `corpus/SOURCES.md`
is byte-identical across base→freeze→HEAD (`git diff --quiet` = same, all three
blobs 181,343 bytes). So at the freeze only D4's prose row conjunct (lesson
naming `controls/census-before.txt`) is uncarriable; its state conjunct is
already green. Exit 0 on all four comparisons.

## 2. Records-only junk control (step 2)

Tree `/fast/scratch/hyaku/kake-r84/ExecC1Derive/junk/` contains exactly one
file, `corpus/lessons/round-84.md`, asserting all four items closed in prose —
including a `[r84-correction` line naming `round-83.md` §Gate, a D2 prose
sentence stating a measurement was taken, a D3 prose sentence naming the
connector seat, and a D4 sentence naming `controls/census-before.txt`. A
stronger probe than the frozen control, whose lesson carries no correction line
at all.

```
python3 -B $CTR --root $S/junk     → junk_exit=1
item=D1 closed=0 state=0 row=0 heading not cited-or-retained: '5.2.  Cache-Control'
item=D2 closed=0 state=0 row=0 retained RFC 9111 absent
item=D3 closed=0 state=0 row=0 w1-spec.json or w1-results.json absent
item=D4 closed=0 state=0 row=0 census receipt or SOURCES.md absent
C1v1 revision=worktree items=4 open=4 closed=0 met=false
```

**No item can be closed by prose alone.** D1 needs the four headings both in the
line and in retained RFC bytes (absent here); D2 needs RFC bytes to re-derive
the count; D3 needs spec+results files; D4 needs the receipt agreeing with the
registry. The verdict matches the frozen `ctl-c84-junk-queue.txt` (open=4,
exit 1), so the frozen kill rule — counter must not reach `met` on its junk
control — holds; my run reproduces it.

## 3. Counter over the lane (step 3, exact output)

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/c84_defect_queue.py --root /home/vgpnk/Projects/shokunin/kake-shokunin
item=D1 closed=0 state=0 row=0 no [r84-correction line
item=D2 closed=0 state=0 row=0 no `D2 count=<n> span=838-844 measure=words-full-span` line
item=D3 closed=0 state=0 row=0 w1-spec.json or w1-results.json absent
item=D4 closed=1 state=1 row=1 receipt_w04=22 derived_w04=22
C1v1 revision=worktree items=4 open=3 closed=1 met=false
lane_exit=1
```

Open now, and why: **D1** — `corpus/lessons/round-84.md` does not exist yet
(ScribeLesson produces it), so no correction line; the retention half is already
satisfied. **D2** — same missing lesson; when it lands it must carry exactly
`count=66` (my count), any other number reopens. **D3** — `w1-results.json` does
not exist anywhere yet; the spec half (1 connector) is already satisfied at
HEAD. Closed already: **D4**, from files alone. A `--revision f358022f…` run
gives the identical item states (exit 1, open=3). Counter selftest rerun in my
scratch: 8/8 passed, exit 0 — equals the frozen `c84-selftest-c1.txt`.

## 4. Do-nothing reachability (step 4)

**The path: fabricate D3's two files.** The counter closes D3 from
`w1-spec.json` (a role list) plus `w1-results.json` (any row with
`agent=="connector"` and a non-empty `output` string). Nothing cross-references
`w1-dispatch.json`, timestamps, or any accounting; a two-file after-state with a
hand-written connector row closes D3 with no connector seat ever having run.
Combined with D4 already green from files and D1/D2 being one lesson line, the
queue can reach `met=true` on paper-work alone.

**Does the frozen control catch it? No — worse, the selftest certifies the
path.** The junk control omits the files entirely (open=4), and the committed
selftest's green fixture IS a fabricated row: `good_results()` returns
`{"name": "C", "agent": "connector", "output": "done"}`; its `junk-prose-only`
fixture (all state files, prose lesson) reads open=2, i.e. D3 and D4 close from
files with zero prose. No frozen artifact distinguishes a real connector run
from an invented row; only the non-author closure re-reading the wave transcript
can.

**Second path (bonus): D2 in worktree mode.** The count is re-derived from the
RFC *at the measured tree* with no digest conjunct; appending words to lines
838–844 of the retained file in a worktree would make any claimed count "true".
In `--revision` mode `git show` reads committed bytes and closes this; no frozen
control pins the RFC hash (the round-83 digest lives in prose only). The bytes
are intact today (blob equality above).

**Findings (defects reported, not patched — the counter is frozen):**
- **F1.** The code never implements the contract's D3/D4 prose row conjuncts:
  `item_d3` row = `settled >= 1` and `item_d4` row = `claimed==derived and
  derived>0`; neither reads the lesson or `SCORECARD.md`. This is exactly what
  makes the D3 fabrication silent, and it makes lane-run D4 "closed" mid-wave
  before any lesson exists.
- **F2.** Cosmetic: contract §C1 D2 writes `"".join(lines[837:844])`, the code
  joins with `"\n"` — identical under `\S+` counting (both = 66 here).

## Commands and exit codes

| cmd (absolute paths elided to `$LANE`, `$S`) | exit |
|---|---|
| my D1/D2 derivation (python3, headings + span count + file existence) | 0 |
| my census parser vs receipt: worktree / freeze / base / HEAD blobs | 0 / 0 / 0 / 0 |
| `python3 -B $CTR --root $S/junk` | 1 (expected: met=false) |
| `python3 -B $CTR --root $LANE` | 1 (open=3: D1, D2, D3) |
| `python3 -B $CTR --selftest --work $S/selftest` | 0 (8/8) |
| `python3 -B $CTR --root $LANE --revision f358022f…` | 1 (open=3) |
| git reads: `rev-parse`, `cat-file -e`, `ls-tree -r`, `diff --name-status`, `show` | 0 |

Receipts in `ExecC1Derive/`: `d1d2-d3-derivation.txt`, `census-{worktree,freeze,
base,head}.txt`, `junk-run.txt`, `lane-run.txt`, `lane-run-freeze.txt`,
`selftest-run.txt`, and the three compared `SOURCES.*.md` blobs.

## Verdict

At the freeze, D4's state conjunct is already true (my parser reproduces the
frozen receipt's 22-row W04 set exactly over base/freeze/HEAD/worktree); D1's
retention half and D2's true count (66) verify from committed bytes; D1, D2, D3
are open for want of the not-yet-written lesson and results files. The counter
does not close any item on prose alone (junk control open=4, exit 1 — kill rule
holds), but it can read `met=true` without the connector work ever running: a
fabricated `w1-results.json` connector row closes D3, the frozen selftest itself
certifies that path, and no frozen control catches it (F1: the code drops the
contract's D3/D4 prose row conjuncts). Admission must re-derive D3 from the wave
transcript, and D2 from a pinned RFC digest if the lane wants worktree-mode runs
to be trustworthy.
