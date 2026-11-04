# ExecQueue — kake round 80, wave w1 (C1 calibration, seat ExecQueue)

**Verdict: both deliverables landed — `.ufo/waves/round-80/defect-queue.json` (R79-8) is written and re-derived; my independent six-predicate re-implementation agrees with `c80_defect_queue.py` at the base (`open=6 met=false`) and at a same-moment worktree snapshot (`open=2 met=false`, both sides), and I found 10 latent reading divergences between the contract text and the counter (6 where the counter is stricter than the contract, 4 where it is looser).**

Tooling: no installs or upgrades (nothing needed; pacman host-wide pause noted, no transaction attempted).

## (A) `defect-queue.json` — built and re-derived

File: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/defect-queue.json`
(sha256 `989fa3028e9c413bf13383aae08be55f03bf365f91bfc1020aade2310c897f0a`).

Exactly two of the 14 round-79 seats have an empty `output`: `ExecC2Tool` (results index 2) and `CriticC` (index 10). Schema per seat spec, top level `{"schema": "kake-defect-queue/v1", "round": 79, "seats": {...}}`:

| seat | status | output_bytes | output_sha256 | evidence |
|---|---|---|---|---|
| ExecC2Tool | `null` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `…/round-79/w1-results.json:2` |
| CriticC | `null` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `…/round-79/w1-results.json:10` |

How the bytes were re-derived: `python3` `json.load` of `.ufo/waves/round-79/w1-results.json` (sha256 `120844dc76d7d56ba27c22f4e5369f76cff3684ef2a6c4e20fcdf84b1817e27b`), iterate `results`, select entries with `output == ""`, then `len(output.encode("utf-8"))` and `hashlib.sha256` over those UTF-8 bytes. `sha256(b"")` = `e3b0c442…b855` (cross-checked independently). Both seats: 0 bytes.

Two honest findings about the source file, reflected in the record:

1. **No seat entry carries a `status` field.** All 14 entries parse with exactly the keys `agent, name, note, output` (verified programmatically over the whole file), so `status` is recorded as JSON `null` — the results file's status value is absent, and `null` is the faithful encoding of absence.
2. **No seat entry carries any error field** (`note` is also `null` for both dead seats), so `last_error` is the sentence "the results file carries no error field for this seat" — which is itself the R79-8 finding (the round-79 template asked for last-error text the harness never recorded).

The counter's `p_r79_8` closes R79-8 on this file (verified live below).

## (B) Independent re-implementation: `w1/ExecQueue/indep_queue.py`

Written from the contract's per-item closure table only (docstrings quote the contract sentence; no import from or shared code with `c80_defect_queue.py`). Runs:

- **Base `9998dc7a586b9fe76379014c8123aa3606f2d8b9` (`--revision`, own `git show` export into scratch):** `open=6 closed=0 met=false exit=1` — per-item: all six open, matching the frozen control `controls/base-c80-defect-queue.txt` (same verdict and same per-item reasons). Receipt: `w1/ExecQueue/indep-base-9998dc7a.txt` (sha256 `dd0279a097376a01e919f89ac766993fe1467455e510e26e30ef63bb4041a31b`).
- **Carrier worktree, same moment as the official counter:** indep `open=2 closed=4 met=false exit=1`; counter `open=2 closed=4 met=false exit=1`. Identical per-item verdicts: R79-1, R79-3 (receipt `selftest: 33/33 passed` == tool re-run), R79-5, R79-8 closed; R79-2 (`scripts/ledger_append_guard.py` absent — ExecGuard not yet landed) and R79-4 (harness reports `killed=2` — ExecFixtures mid-flight) open. Receipts: `w1/ExecQueue/indep-worktree.txt` (`7bd735d5…`), `w1/ExecQueue/counter-worktree.txt` (`573e67b0…`). Snapshot caveat: the worktree moved during this seat (R79-3's receipt landed between my first and second look); these receipts pin one moment.

### Reading divergences vs `c80_defect_queue.py` (all latent — both sides agreed at base and at the snapshot)

**Counter STRICTER than the contract text (adds conjuncts):**

1. **R79-1 used-by resolution** (`c80_defect_queue.py:124-128`): counter requires the S453 row's used-by cell (index 10) to resolve to an existing file that itself cites `S453`. Contract names no used-by conjunct. Contract text supports the literal reading (a row whose source cites RFC 9110 and not 9309); the extra check is defensible registry hygiene and is exercised by the counter's own `--selftest` (`:243-277`, "unresolved-open"), but it is extra-textual — a contract-closed tree with a dangling used-by stays counter-open.
2. **R79-1 census row-shape** (`:63-82`, applied `:129-131`): 11 cells, closed enums, no community-tier-A, no empty cells. Not in the contract sentence. Same judgment as #1 (counter selftest "twelve-open" proves it bites).
3. **R79-1 lesson proxy** (`:122-123`): counter requires the literal token `RFC 9309` in the round-80 lesson. The contract requires the erratum to name **the withdrawn sentence's subject** (the kept rejected `S453` row — `round-79-verifier-spotcheck.md:130,153-156`) and `S453`. The token neither implies nor is implied by naming the subject: a lesson can name the subject without writing "RFC 9309" (contract-closed, counter-open) or quote "RFC 9309" while never naming the subject (counter-closed, contract-open). Contract text supports the subject-named reading; note the counter's own selftest lesson line (`:253-254`) is thinner than the contract wording yet passes its own check.
4. **R79-2 run exit code** (`:149`): counter requires the `--root <tree> --json` run to exit 0. Contract: "its run over the lane reports the receipt ledger's byte prefix preserved" — no exit conjunct stated. Minor; contract text supports not gating on exit (I record `rc2` in the detail but don't gate on it).
5. **R79-3 re-run exit code** (`:164`): counter requires the tool `--selftest` re-run to exit 0. Contract: "re-running the tool's `--selftest` at the measured revision prints the identical line" — the line, not the exit. Contract text supports my reading (rc recorded, not gated).
6. **R79-8 population premise + emptiness width** (`:217-219`): counter (a) treats whitespace-only *and missing* `output` as empty (via `(r.get("output") or "").strip()`), and (b) refuses to close if zero empty-output seats exist ("population premise lost"). The contract says seats "whose output was empty"; `""` is the literal reading, and no at-least-one conjunct is stated. At round 79 the difference is moot (exactly two seats, both exactly `""`), but a whitespace-only seat would be counter-mandatory and literally optional. Contract text supports the strict reading on both points.
7. **R79-8 duplicate names** (`:217`): counter collapses the population into a dict keyed by seat name; two same-named empty seats would be checked once. Contract says "every seat". My implementation iterates by results index.

**Counter LOOSER than the contract text (omits conjuncts):**

8. **R79-4 survivor identity** (`:186-210`): the counter checks only `killed == 3`, `len(fixtures) == 3`, and the `cheap_note` entry (`ledger_red is True`, `undisclosed == 1`) — it never verifies the three survivors are **k3 `wrong_kind`, k4 cheap-note, k5 `symlinks`** as the contract names them. Any three fixture keys, e.g. three renamed stubs, pass. Contract text supports my reading (I require all three kinds identifiable in the harness output).
9. **R79-5 withdrawal semantics** (`:212-214` area; `WITHDRAWN` at `:42`): the counter closes on any lesson line containing both `R79-5` and the sentence fragment — a line *asserting* the sentence ("R79-5: passed 31/31 before the tool existed") passes it. The contract says the lesson "withdraws the sentence"; my implementation also requires a withdrawal verb on the row. Contract text supports my side. (Both sides closed at the snapshot only because the scribe's row genuinely withdraws.)
10. **R79-1/R79-5 erratum semantics**: related to #3/#9 — neither predicate requires the lesson to perform an erratum/correction (mine does for both). Contract text supports requiring it ("records the erratum").

Shared limitation (not a divergence): both implementations substring-scan for the sentence fragment `passed 31/31 before the tool existed`, so a self-assessment file repeating the sentence re-worded (e.g. "the pre-tool 31/31 scratch run") evades both.

### Cheapest lazy-author shortcut per item — and whether the counter rejects it

| Item | Cheapest fake closure | Counter rejects? |
|---|---|---|
| R79-1 | Hand-write the S453 row citing RFC 9110 (source never opened) + one lesson line carrying the tokens `R79-1`/`S453`/`RFC 9309` | **No** — all greps pass (used-by resolves: the landed knowledge file cites S453, verified 18 hits). Its extra shape/used-by checks reject only malformed rows, not fabricated ones |
| R79-2 | Do-nothing guard: `--selftest` prints any `non-prefix … failed` line, exits 0; `--json` constant-prints `{"prefix_preserved": true, "files": 1}` | **No** — the predicate is behavioral-over-the-lane only as real as the guard's code; nothing re-derives the prefix independently |
| R79-3 | Hand-write the receipt to match whatever the tool prints (fabricating the run itself is undetectable; the predicate only enforces receipt==re-run agreement) | Partially — it rejects receipt≠re-run, missing `exit=0`, re-run rc≠0, but cannot detect a never-made run |
| R79-4 | Canned harness: print `{"killed": 3, "fixtures": {a:…, b:…, cheap_note: {"ledger_red": true, "undisclosed": 1}}}` + hand-written receipt with the two magic words + one QUALITY sentence | **No** — this is the weakest item (divergence #8): the counter never checks the survivors are k3/k4/k5, and the receipt is grepped, not re-run |
| R79-5 | One lesson line *asserting* the sentence while naming R79-5 (no withdrawal) — tokens co-occur, nothing withdraws | **No** (divergence #9). My independent reading rejects it (no withdrawal verb) |
| R79-8 | Pad the queue with extra seat entries, or omit a whitespace-only seat | Extra entries: **no** (counter checks coverage only). Whitespace-only seat: the counter *does* catch the omission (its `.strip()` widening, divergence #6) where the contract-literal reading would not |

None of these shortcuts is open to me: my deliverable (A) is the honest re-derivation, and the junk control `controls/ctl-c80-junk-queue.txt` independently shows a fabricating tree still scoring `open=6`.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/defect-queue.json` (deliverable A; sha256 above)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/w1/ExecQueue/indep_queue.py` (deliverable B)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/w1/ExecQueue/indep-base-9998dc7a.txt`, `indep-worktree.txt`, `counter-worktree.txt` (run receipts)

Scratch (`/fast/scratch/hyaku/kake-r80/ExecQueue/`) deleted at end of seat; no fixture repos created. No commits, no git mutations. No message to L1 needed — no blockers. Risks: the worktree continues to move under the wave (R79-2 guard and the R79-4 `killed=3` state are sibling-owned); the validator should re-run the frozen counter over the carrier at integration time, not rely on my snapshot.
