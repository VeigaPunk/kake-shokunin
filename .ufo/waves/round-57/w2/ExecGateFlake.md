# ExecGateFlake

Artifact under test: `.ufo/waves/round-57/c57_idresolver_gate.py` at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (read via `git show <rev>:<path>`; the gate file in the scratch checkout was
diffed byte-identical to that blob). Tool under test: `scripts/id_resolver.py` @ same revision (722 lines, 33-case selftest).
Scratch clone `/tmp/egf-lane` (`git -C /tmp/egf-lane rev-parse --show-toplevel` = `/tmp/egf-lane`, checked out at the pinned
revision); junk commits `45e91ad…3bffb8b` exist only there. Fleet `/home/vgpnk/Projects/shokunin` read-only. Host load
average 37.5 on 32 cores. No tool installed, no pacman, nothing written outside this report and `ExecGateFlake.files/`.

## FLAKE TABLE:

Command per run (cwd `/tmp/egf-lane`):
`python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root /tmp/egf-lane --revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f --fleet /home/vgpnk/Projects/shokunin`

| run | exit | G1 | G2 | G3 | G4 | G5 | G2 note | G3 summaries (dirty/clean) | G4 summary | G5 summary |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 02 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 03 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 04 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 05 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 06 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 07 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 08 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 09 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |
| 10 | 0 | PASS | PASS | PASS | PASS | PASS | 33/33 | (12,3,9,6,3)/(3,3,0,0,0) | (99,94,5,5,0) | (106,106,0,0,0) |

Per-condition tally over 10 runs: G1 10/10 PASS, G2 10/10, G3 10/10, G4 10/10, G5 10/10; `met=True` 10/10; exit 0 10/10.
Flake rate against the shipped tool: **0/10**, and the stdout of all ten runs is byte-identical (the `secrets`-seeded fixtures
produce the same reference summaries because the fixture classes, not the ids, fix them). Raw outputs:
`/tmp/egf-flake/run{01..10}.txt`; the same table body re-produced as `gate-*.txt` for the junk runs in `ExecGateFlake.files/`.

Extra determinism probes (all `confirmed by running`):
- 3 gate runs started simultaneously: all exit 0, all 5/5 (`/tmp/egf-conc{1,2,3}.txt`) — the `secrets` fixtures and the
  `/tmp` dirs do not collide.
- `PYTHONHASHSEED=random TMPDIR=/var/tmp`: exit 0, 5/5, same summaries (`/tmp/egf-hs.txt`).
- `--root` = the real lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (instead of a clone): exit 0, 5/5, same notes
  (the G4 owner column changes internally — defect D1).
- Stale-snapshot probe (scratch fleet `/tmp/egf-fleet`, a second sibling `zzz-shokunin` holding `S367`, tool unchanged):
  exit **2**, `C2 id-resolver-gate unevaluable: Unevaluable: live sibling ownership {'S367': ['kotodama-shokunin',
  'zzz-shokunin'], …} differs from the committed snapshot (sibling heads: kotodama-shokunin=, zzz-shokunin=)` — defect D2.
- Temp hygiene: 0 `/tmp/c57-gate-*` / `/tmp/c57-fixture-*` dirs from my 14 runs; the 9 `/tmp/c57-*` dirs present are other
  seats' harnesses (`c57-diff*`, `c57-pins-*`, `c57-qt-*`, older `c57-fixture-clean-*`), not this gate's leak.

## JUNK RESULTS:

Seven tools derived from the shipped candidate by `make_junk.py` (each replacement asserted to match exactly once; every
variant keeps `--selftest` unchanged except where noted), committed in `/tmp/egf-lane` and measured with
`--revision <that commit>`; logs `ExecGateFlake.files/gate-<tool>.txt`.

| tool (commit) | defect | G1 | G2 | G3 | G4 | G5 | met | what caught it |
|---|---|---|---|---|---|---|---|---|
| `junk_const.py` (45e91ad) | constant printer: red block + fixed `(105,100,5,5,0)`, exit 1 | PASS | PASS (33/33) | FAIL | FAIL | FAIL | **2/5** | G3 `summary (105,100,5,5,0) != reference (12,3,9,6,3)`; G4 `!= (99,94,5,5,0)`; G5 `!= (106,106,0,0,0)`, exit 1 |
| `junk_worktree.py` (1c90d6c) | CLI passes `revision=None` (working tree read) | PASS | PASS (33/33) | PASS | FAIL | PASS | **4/5** | G4 `summary (106,106,0,0,0) != reference (99,94,5,5,0)`, exit 0 vs 1 |
| `junk_nofleet.py` (cb6b9fb) | CLI passes `fleet=None` (parent of `--root`) | PASS | PASS (33/33) | PASS | FAIL | PASS | **4/5** | G4 `(99,94,5,0,5) != (99,94,5,5,0)` — G3 cannot see it (D3) |
| `junk_unsorted.py` (37537d4) | DANGLING line order, cited-by, owners, url-match all reversed | PASS | PASS (33/33) | PASS | PASS | PASS | **5/5** | nothing — sets, as required (D6) |
| `junk_nourl.py` (216e1bc) | `url-match=-` always | PASS | PASS (33/33) | FAIL | PASS | PASS | **4/5** | G3 `S193 … url-match [] != ['e5888fa-shokunin']` (only G3 compares url-match) |
| `junk_offbyone.py` (27ab4ce) | prints `owned_elsewhere=owned+1` | PASS | FAIL (32/33) | FAIL | FAIL | FAIL | **1/5** | tool's own selftest case "exact DANGLING and summary lines"; gate: `summary identities fail: (12,3,9,7,3) with 9 DANGLING lines` (gate `parse`, lines 122-123) |
| `probe_defaultfleet.py` (3bffb8b) — *extra probe, not one of the six* | returns 64 when `--fleet` is omitted (documented default not implemented) | PASS | PASS (33/33) | PASS | PASS | PASS | **5/5** | nothing (D7) |

Reading of the matrix: the five expected outcomes hold (const fails G3+G4+G5; worktree fails G4 only; nofleet fails G4 only;
unsorted passes; url-match always `-` fails G3 only; the off-by-one is rejected by the summary-identity check before any
comparison, plus its own selftest). The two failures of interest are the ones nothing caught: reversed output ordering and
the unimplemented default `--fleet`.

## TIMING:

- One full gate run, shipped tool, warm, load ~37/32 cores: 1.31 s, 1.36 s, 1.39 s (three solo runs,
  `--root /tmp/egf-lane --revision 4b8c730…`). Inside the ten-run batch under heavier contention: 1.83–2.72 s.
- Breakdown: the tool's `--selftest` alone is 0.12 s (33 cases), so ~90 % of a gate run is the gate's
  own process work. `cProfile -s tottime`: `select.poll` 0.923 s (subprocess waits), `posix.unlink` 0.102 s and
  `shutil._rmtree_safe_fd_step` 0.173 s (fixture cleanup), `registry_rows` 0.121 s (161 calls).
- Subprocess scale: **359 `git` invocations per gate run**, counted with a `git` shim on `PATH` (`/tmp/egf-gitcount`).
  Sources: `read_lane` at RED_REV/the measured revision issues 1 `ls-tree` + one `show` per knowledge file (51 at the measured
  revision) + 1 registry `show` per revision, and `read_siblings` issues one `show` per sibling lane (21 with a clone root),
  twice (G4, G5).
- Junk-matrix runs: 7 variants × ~1.6 s each = 11.6 s total; no run needed a retry, no timeout (tool timeout is 300 s).

## GATE DEFECTS:

D1 **G4's owner column is root-dependent and not pinned to kotodama.** Gate `c57_idresolver_gate.py:323` removes
`kake-shokunin` only from the *snapshot* comparison; `read_siblings` (lines 168-181) and therefore both the reference and the
tool still name the lane itself when `--root` is a clone outside the fleet. `confirmed by running`:
`--root /tmp/egf-lane` → `DANGLING S367 … owners=kake-shokunin,kotodama-shokunin`; `--root` = the real lane →
`owners=kotodama-shokunin`. Both invocations score 5/5, so the contract's "each owned by kotodama-shokunin" is only
enforced as "kotodama ∈ owners" (line 328), and a tool that hard-codes "skip the lane's own name" fails with a clone root
while passing with the real-lane root: the verdict depends on how the operator invokes the gate.

D2 **The verdict is not a function of the measured revision: any fleet change flips met → exit 2.** The live check
(lines 318-326) compares every sibling HEAD registry (21 with a clone root) against `sibling-snapshot.json`. `confirmed by running`: a scratch
fleet with one extra sibling holding `S367` turns the correct tool's 5/5 into exit 2 with no condition table. Transient
forms of the same channel (a sibling mid-rewrite whose HEAD momentarily lacks `corpus/SOURCES.md`, a new `*-shokunin`
directory adopting one of the five ids) are `[INFERENCE]` from lines 171-178 and 323. The message also prints empty heads
(`kotodama-shokunin=`) whenever a sibling is not a git repo, so the diagnostic is degraded exactly in the copied-fleet case.

D3 **G3 cannot see a tool that ignores `--fleet`.** `build_fixture` (line 226) puts the lane at
`<fleet>/demo<nonce>-shokunin`, so the documented default (parent of `--root`) *is* the fixture fleet, and G3 passes
`--fleet` explicitly (line 268) with the same value. `confirmed by running`: `junk_nofleet.py` passes G3 and is caught only
by G4. Any fixture with the lane outside the fleet (or a second fixture fleet) would close this.

D4 **url-match is compared only on punctuation-free fixture rows, and the shipped tool disagrees with the reference on
punctuated ones.** G3 is the only `with_urls=True` call (line 268); fixture rows are written as `t — {url} |` (line 233), so
no URL ever ends in `. , ; :`. The tool strips those characters (`scripts/id_resolver.py:98`, `url.rstrip(".,;:")`) while
the reference matches verbatim (gate line 198). `confirmed by running` on a hand-built fleet whose sibling row is
`| S777 | t — https://a.example/777. |`: tool `url-match=alpha-shokunin`, reference `url-match=[]`. No live registry row
currently triggers it (scan of all 21 lane HEAD registries: 0 rows with a URL followed by punctuation), and G4/G5 pass
`with_urls=False`, so this is a coverage hole, not a live false pass.

D5 **Reference and tool disagree on a git sibling whose HEAD has no `corpus/SOURCES.md`; G3 builds only the non-git
variant.** Gate lines 175-178 omit such a sibling (it "owns nothing", per the contract); the tool falls back to the
worktree file (`scripts/id_resolver.py:194-202`). The fixture's registry-less sibling (line 250) is a plain directory, which
both sides read through the same fallback. `confirmed by running` on a scratch fleet with a git sibling whose worktree holds
the row but whose HEAD does not: tool `owners=alpha-shokunin` (exit 1), gate reference `owners=[]` (summary
`(1, 0, 1, 0, 1)`). Here the *tool* is the one off the frozen rule and the gate cannot say so.

D6 **Output order is never checked, although the CLI contract requires it.** The contract (gate docstring line 26) says the
DANGLING lines are "sorted by id"; `compare` (lines 209-214) sorts the id keys and compares cited-by/owners/url-match as
frozensets. `confirmed by running`: `junk_unsorted.py` reverses the line order and all three lists and scores 5/5. Set
semantics for owners is the intent; applying them to the line order and to cited-by silently drops two contract clauses.

D7 **Large parts of the CLI contract are never exercised.** The gate invokes the tool exactly four ways: `--selftest`
(line 295), fixture runs with no `--revision` (line 268), and two real-revision runs (lines 327, 331). Consequences:
`confirmed by running` — `probe_defaultfleet.py`, which refuses to run without `--fleet` and returns 64, scores 5/5, so the
documented default fleet is untested and a tool that breaks the round-58 `--root`-only invocation passes. `[INFERENCE]` from
the same invocation set: the exit-2 paths (unresolved revision, registry absent, no knowledge file) and exit 64 (usage) are
untested, so a tool that returns 0 there passes.

D8 **[INFERENCE] G2 proves nothing about correctness by design, and the gate never cross-checks it.** Line 298 accepts any
tool whose last `--selftest` line is `selftest: N/N`, N ≥ 16, with no `Traceback` on stderr; a tool that prints
`selftest: 33/33` without running anything passes G2. The contract already calls G2 "a smoke test, not evidence", so this is
recorded only because the junk matrix confirms 6 of 7 variants ride G2 for free.

Non-defects checked: summary identities (line 122) are enforced, so an off-by-one in `owned_elsewhere` is rejected before
comparison (junk_offbyone); the gate rejects extra stdout lines and duplicate DANGLING ids (lines 111-117), so a tool cannot
smuggle verbose or repeated output past the parser; `PYTHONHASHSEED=0` is set for the tool (line 99) and the reference is
set-based, so hash order is not a flake channel; fixtures and sandbox clones are removed in the `finally` (line 337-339),
verified by the zero leftovers above.

VERDICT: version-2 C2 gate is deterministic (10/10 identical 5/5 runs for the shipped tool, 0 % flake; three concurrent runs and a random-hashseed/alt-TMPDIR run also 5/5) and it kills 5 of the 6 junk tools it is supposed to kill (const 2/5, worktree 4/5, nofleet 4/5, nourl 4/5, offbyone 1/5) while correctly passing the unsorted-owners tool, but it has five confirmed holes — G4's owner column includes the lane itself when `--root` is a clone (D1), fleet state outside the measured revision can flip a correct tool to exit 2 (D2), G3 cannot see an ignored `--fleet` (D3), url-match is only tested on punctuation-free rows where the shipped tool diverges from the reference (D4), and reversed output order plus an unimplemented default `--fleet` pass 5/5 (D6, D7).
