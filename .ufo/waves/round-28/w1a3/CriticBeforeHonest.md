# CriticBeforeHonest — is the C1 before value (4/15 at 22c1669) honest?

Seat: KakeR28a3.CriticBeforeHonest (critic, leaf, read-only on the lane). Axis: operability.
Scratch: `/fast/scratch/hyaku/kake-r28a3/w1/CriticBeforeHonest/` (TMPDIR set there). Python 3.14.8, git 2.56.0, `ulimit -s` 8192.

## Verdict
The before value is honest on this host. 0 of 11 defect checks and 4 of 4 controls reproduce exactly, and all 11 base failures are real behaviour of the base gate rather than counter artifacts. Each one is a hang, a traceback or a wrong-surface/empty-surface clean. Three caveats narrow what some "false green" labels mean (A1–A4, A5, A7). One caveat is load-bearing for the after value (U3/U4 depend on the stack size). Details follow.

## Provenance (git metadata, read-only)
- Counter `.ufo/waves/round-28/c1_interface_count.py`: sha256 `a30d9d94…8739395`. Its only commit is the declaration commit `84ea5b1`, and the working tree is unmodified. The declared before value "4/15 (0/11 defect, 4/4 controls)" is at `84ea5b1:SCORECARD.md:585`, landed before the repair `b5d423f`. `c1-before.json` itself was committed in `b5d423f`.
- Base gate blob `22c1669:scripts/citing_set.py` = `352a471a…` is byte-identical to the round-27 falsified candidate `ac46a74` and the round-27 final head `62aeddf`. The whole `scripts/` tree is identical too (`6742bb45…`). `git log 22c1669..b5d423f -- scripts/` lists only `b5d423f`. So the base is the exact round-27 gate, with no partial repair mixed in.

## Re-run of the counter
`python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision 22c1669c1fec83d1a0769de6b9ce686c75657e66 --scratch $S/counter > $S/c1-before-rerun.json` exited 1 after 41.3 s.
Result: passed 4/15, defect 0/11, control 4/4. Every case matches `.ufo/waves/round-28/verification/c1-before.json` on id, passed, reasons and observed fields (stderr tail aside, which differs only in "used 8144/8140 kB"). Re-run sha256 `c43fe144…`; recorded `ce4103ed…`. The byte difference comes only from the stderr tails.

## Hand reproductions (my own inputs, base gate extracted to `$S/gate-22c1669.py`, sha256 `3a361a00…`)
Script `$S/repro.sh`, log `$S/repro.log`. The script exited 0 and every case ran. Its elapsed-seconds column is broken because `bc` is absent, so I took durations from `timeout` exit 124 and wall time. Population/ledger were `pop.json`/`led.json` with ids S010/S011/S099/R-7/src10, entries `a.md`/`b.md`. All gate line numbers below refer to `22c1669:scripts/citing_set.py`.

| Case | Counter says | My input and result | Mechanism | Call |
|---|---|---|---|---|
| U1 population FIFO | timeout 20 s | FIFO `pop.json`: `timeout 60` exit 124, 0 stdout bytes; repeat with `timeout 30`: exit 124, 30.2 s wall | `open(...).read()` blocks with no writer, :210-211 | confirm: real hang |
| U2 ledger FIFO | timeout 20 s | FIFO `led.json`: exit 124 at 60 s, 0 bytes | same, :414→:210 | confirm: real hang |
| U3 population deep | exit 1, traceback | nested objects, depth 100000: exit 1, `RecursionError: Stack overflow … JSON object`, empty stdout | only `ValueError` caught, :356 | confirm (8 MiB stack); see caveat 4 |
| U4 ledger deep | exit 1, traceback | arrays, depth 100000: exit 1, `RecursionError … JSON array` | same | confirm (8 MiB stack); see caveat 4 |
| A1 corpus absent, worktree | clean exit 0 | no `corpus/`, empty ledger: exit 0 clean, corpusFiles 0 | `FileNotFoundError → []`, :221-222 | confirm; caveat 1 |
| A2 corpus absent, git | clean exit 0 | commit holding only README plus docs, `--revision HEAD`: exit 0 clean, corpusFiles 0 | `ls-tree` over a missing path is empty and exits 0, :304 | confirm |
| A3 corpus empty dir | clean exit 0 | empty `corpus/knowledge/`: exit 0 clean | empty walk, :234-236 | confirm |
| A4 corpus is a blob, git | clean exit 0 | uncited blob at `corpus/knowledge`: exit 0 clean, corpusFiles 1. Same tree in worktree mode: exit 2 `not_a_directory`. Cited blob (A4b): exit 1 `unadjudicated_citing_pair` file=`corpus/knowledge` | Git mode reads the blob as a corpus file; worktree mode refuses it (:232-233 vs :304-320) | confirm: real mode asymmetry |
| A5 unreachable ids | clean exit 0 | population `R-7`,`src10`, entry cites S010/R-7/src10: exit 0 clean, citingPairs 0, outsidePopulation 1 | token grammar is `S\d{3,}` only, :108 | confirm per round-27 record; caveat 2 |
| A6 blank revision | clean exit 0 | HEAD cites S010 unadjudicated, worktree edited to cite nothing. `--revision HEAD`: exit 1 failed. `--revision ''`: exit 0 clean, source working-tree. `--revision ' '`: exit 2 `revision_not_found` | `if arguments.revision:` treats `''` as absent, :650; the blank guard at :273 is never reached | confirm, with a stronger false green than the counter's case |
| A7 nested Git root | clean exit 0 | top `b.md` uncited, `inner/b.md` cites S010, empty ledgers. Git mode on `inner`: exit 0 clean. Worktree mode on `inner`: exit 1 failed | file list from `ls-tree` is cwd-relative (:304), blob read `REV:path` is top-relative (:301) | confirm; caveat 3 |
| K1/K2/K3 | pass | valid clean in worktree exit 0, in Git exit 0; missing pair exit 1 `unadjudicated_citing_pair` | — | confirm |

## Caveats (each is a fixable defect or a disclosure need, not a reason to change 4/15)
1. **A1–A4 are false greens only with an empty ledger.** With a non-empty ledger (A1b), an absent corpus gives exit 1 `failed` with `ledger_pair_not_cited`, not clean. That is still not the contracted exit 2, so the defect check correctly fails. The counter discloses the empty-ledger choice at `c1_interface_count.py:190-192`. The lane's real ledger is non-empty, so for the real lane the base harm is a mislabelled verdict, not a green.
2. **A5 contradicts the base gate's own docstring.** `:33-38` declares that non-`S<digits>` ids compare as exact strings and that outside-population citations "never become findings", and the base obeys that. A5 is a defect because the round-27 record names it (`.ufo/waves/round-27/unresolved-acceptance.json`, CLI-SCOPE-FALSE-GREEN: "Unreachable population ids …"), not because the base breaks its contract. It is a contract tightening, so the repaired docstring must say so.
3. **A7's green needs colliding top-level paths.** With no colliding top-level corpus file (A7b), exit 2 `git_command_failed`. With no top-level `pop.json` (A7c), exit 2 `git_command_failed` on `show <rev>:pop.json`, which proves the input documents are also read top-relative. The counter builds that collision on purpose (`:234-245`). The defect is real, but the base fails closed when paths do not collide.
4. **U3/U4 depend on the stack size, for the base and for the repair** (load-bearing for the after value, not the before value). Input: valid population, depth-200000 array, cited entry, matching ledger (`$S/hand2/d200k-valid`):
   - base, `ulimit -s 8192`: exit 1 RecursionError
   - base, `ulimit -s unlimited`: exit 0 clean
   - `b5d423f`, 8192: exit 2 `document_not_json`
   - `b5d423f`, unlimited: exit 0 clean

   The repair only adds `RecursionError` to the except clause (`b5d423f:scripts/citing_set.py:401`) and has no depth limit. Under an unlimited stack the counter would score the repair U3/U4 failed (13/15). The base scores 0/11 either way, so the before value stays sound. Smallest correction: declare and enforce an explicit nesting limit in the gate, so the input is refused independent of the stack. Alternatively, the counter could record and pin `ulimit -s` in its output.

## Commands run (all inside scratch or read-only git; exit codes)
- `git show/log/rev-parse/diff --stat` on pins `22c1669`, `84ea5b1`, `b5d423f`, `ac46a74`, `62aeddf`: all 0.
- Counter re-run as above: exit 1 (expected, because 4/15 is less than 15/15).
- `bash $S/repro.sh`: exit 0 in 121.0 s wall; the two 60-second FIFO timeouts account for almost all of it. Per-case gate exits are listed in the table.
- Probes in `$S/hand2/`: A7c exit 2; deep arrays at depths 10000/20000/50000 exit 0 clean (the overflow threshold on this host lies between 50000 and 100000); FIFO `timeout 30` exit 124; stack probes as in caveat 4.

## Not verified
- I did not run the K4 selftest by hand; I rely on the counter re-run (exit 0, 29 cases).
- I did not re-run the after value, except the single deep-JSON probe in caveat 4.
- No other Python version or OS stack default was tried.
- No tool was installed or updated. `bc` is absent and was not needed.
- No lane file other than this report was written.
