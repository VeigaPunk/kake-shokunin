# ScribeC1Text — round 69 W1 drafts (kake lane, base `4d188f94`)

Prose drafts only. No repo file written except this report; no tracked lane file
edited; no tool installed (git/grep sufficed). Base bytes read with
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4d188f94:<path>`.

## QUALITY addendum draft

Append at end of `corpus/QUALITY.md` (append-only; earlier criteria untouched).
Scope: the publishing evidence this lane commits for its own gates and property
records — corpus lesson/ledger records and the control receipts under
`.ufo/waves/` that a published claim rests on. A count or receipt about work
outside that evidence base is neither admitted nor rejected here.

| Criterion | Admit | Reject | Grounding |
|---|---|---|---|
| **A recorded integer count re-derives at the revision it names, or is cleared by a correction row.** | The count is reproduced by the command the record names, run against the committed bytes of the path it names at the revision it names — `git show <rev>:<path> \| grep -c '<pattern>'` — and the reproduced integer equals the recorded integer; or the count is cleared by a correction row appended to `corpus/lessons/round-69.md` §Corrections naming the pair id and the re-derived value. | A count measured on an uncommitted worktree state; a recorded pre-value carried from an earlier round and re-measured at no revision; a count "relabelled" by editing the original record line; a correction row that names a round but not the pair id and the re-derived value. | `corpus/lessons/round-69.md` §Mistakes row M1 (class record/observed drift). `corpus/lessons/round-67.md:54` records the ledger wording count as "5 → 1"; the count re-measures 2 at `099923320` and at `396128196` (`corpus/lessons/round-68-verifier-spotcheck.md` §2 C1 table; `LOG.md:2319`; D-2 at `corpus/lessons/round-67-verifier-spotcheck.md:180-186`), and §7 item 2 routes the pre-value as unreproduced. Falsifier: `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --selftest --work <scratch>` prints `selftest 4/4` and exits 0. |
| **A committed receipt names no `/tmp` path it reads.** | Every path the receipt reads is committed in the lane (or a retained source under `.ufo/waves/<round>/sources/`), and the receipt's transcript reproduces from committed bytes alone. | A committed receipt whose transcript reads an absolute `/tmp` path — including one ending in a `FileNotFoundError` on such a path, which is a broken read, not evidence; a re-run executed but left uncommitted. | `corpus/lessons/round-69.md` §Mistakes row M2. `.ufo/waves/round-68/controls/wordcounts-d3-r68.txt` ends in a traceback on `/tmp/q133.txt`; `corpus/lessons/round-68-verifier-spotcheck.md` §7 item 3 routes the block as non-reproducible. Falsifier: `grep -c '/tmp' .ufo/waves/round-68/controls/wordcounts-d3-r68.txt` = 1 (red) and `grep -c '/tmp' .ufo/waves/round-69/controls/wordcounts-r68-rerun.txt` = 0 (green). |

Base observations for the two falsifiers, measured at `4d188f94`:
`grep -c '/tmp' .ufo/waves/round-68/controls/wordcounts-d3-r68.txt` → `1`;
`git show 4d188f94:corpus/knowledge/gate-status-ledger.md | grep -c "not adjudicated here\|candidate mechanism"`
→ `1` at the base, `2` at `099923320` and at `396128196`, against the recorded
"5 → 1". The counter `c69_recorded_counts.py` and the round-69 re-run receipt do
not exist at the base revision (both absent at `4d188f94`); they are round-69
deliverables, named here as the checks that decide the two criteria — not
reported as run.

## Lesson sections draft

For `corpus/lessons/round-69.md`.

### Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| record/observed drift — a recorded integer count that does not re-derive at the revision it names (pre-value unreproduced) | `corpus/lessons/round-67.md:54` records the ledger wording count `grep -c "not adjudicated here\|candidate mechanism" corpus/knowledge/gate-status-ledger.md` as "5 → 1"; the count re-measures **2** at `099923320` and at `396128196` (`corpus/lessons/round-68-verifier-spotcheck.md` §2 C1 table; `LOG.md:2319`; D-2 at `corpus/lessons/round-67-verifier-spotcheck.md:180-186`), and no r68 control re-measures a 5 (§7 item 2). The recorded post-value 1 does re-derive at the base (`4d188f94`). | none — the count was carried forward without re-measurement; no "recorded count re-derives at a named revision" check existed at either landing | the C1 counter `.ufo/waves/round-69/c69_recorded_counts.py` re-derives every frozen pair at its own named revision and prints `unrelabelled=0` (red on the base record, shown by the base run); a mismatching pair is cleared only by a correction row in §Corrections below, and the r67/r68 record lines are never edited. |
| record/observed drift — a committed receipt reads a `/tmp` path it cannot resolve, so the receipt is not reproducible evidence | `.ufo/waves/round-68/controls/wordcounts-d3-r68.txt` ends in `FileNotFoundError: [Errno 2] No such file or directory: '\\tmp\\q133.txt'` after `pathlib.Path('/tmp/q133.txt').read_text(...)`; `grep -c '/tmp'` on that receipt = 1; routed as non-reproducible at `corpus/lessons/round-68-verifier-spotcheck.md` §7 item 3. | none — the receipt was committed with the broken read left in place; no "receipt names no scratch path" check existed | the D-3 receipt is re-run against committed bytes at `4d188f94` and committed under `.ufo/waves/round-69/controls/`; the able-to-fail check is `grep -c '/tmp'` = 1 on the round-68 receipt vs 0 on the round-69 re-run. The round-68 receipt's bytes are not edited. |

### Corrections

Append-only. The round-67 and round-68 records are history and are not rewritten
(round-20 append-only ruling). A mismatching pair is cleared here and only here,
by a row that names the pair id and the re-derived value at the revision the
pair names. The C1 counter reads the correction at the measured revision
(`correction_locus` = `corpus/lessons/round-69.md`, `correction_id` = the pair
id) and counts a pair as relabelled only when this section contains that id.

| Pair id | Recorded value | Revision | Re-derived value | Re-derived by | Note |
|---|---|---|---|---|---|
| `<pair id>` | `<recorded value>` | `<revision>` | `<re-derived value>` | `<command>` | `<one line: what did not re-derive and why the re-derived value is the accepted one>` |

The known pair of this round is the round-67 ledger pre-value "5 → 1"
(`corpus/lessons/round-67.md:54`): the recorded pre-value 5 re-measures 2 at
every revision the round named, and the recorded post-value 1 re-measures 1 at
the base. Its pair id is the one the frozen pair set
`.ufo/waves/round-69/c1/pairs.json` assigns; the L1 fills the row above with
that id, the re-derived value, and the revision the value was measured at. Rows
for further mismatching pairs are appended in the same shape, one row per pair
id; a pair discovered after the pair set was frozen is a round-70 item and is
not recorded here.

### Verification exercised by this seat

| Command (lane `/home/vgpnk/Projects/shokunin/kake-shokunin`, base `4d188f94`) | Output | Exit |
|---|---|---|
| `git show 4d188f94:.ufo/waves/round-68/controls/wordcounts-d3-r68.txt \| grep -c '/tmp'` | `1` (M2 red side confirmed) | 0 |
| `git show 4d188f94:corpus/knowledge/gate-status-ledger.md \| grep -c "not adjudicated here\|candidate mechanism"` | `1` at base | 0 |
| same, at `099923320` / at `396128196` | `2` / `2` | 0 |
| `git cat-file -e 4d188f94:<path>` for `c69_recorded_counts.py`, `c1/pairs.json`, `controls/wordcounts-r68-rerun.txt`, `corpus/lessons/round-69.md` | all ABSENT at base | 1 each |
| `git show 4d188f94:LOG.md \| sed -n '2319p'` | "count re-measures 5 → 2 at every r67 revision while every record says 5 → 1;" | 0 |

Not run by this seat: the `c69_recorded_counts.py` selftest (counter not yet
delivered) and the round-69 receipt re-run (not yet delivered). Both are named
as the deciding checks; neither is reported as passing.

Scratch tree `/fast/scratch/hyaku/kake-r69/ScribeC1Text/` was created for the
lesson-row extraction and removed on exit.
