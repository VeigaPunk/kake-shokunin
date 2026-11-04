VERDICT: C2 frozen predicate not contradicted (numbers 70/120/3/6 and all checklist expectations reproduce), but the gate's sandbox claim is falsified: a stdlib `_posixsubprocess.fork_exec` launcher that delegates to the gate's own `reference()` is admitted `met=true`, exit 0, `sandbox=ok`.

Seat ScoutGround (agent id ScoutGround-2), round 90 wave 1. Read-only recon; no production edits, no git mutation, no network. Lane HEAD at reading: `79e1aac2`. Python 3.14.8 (`/usr/bin/python3`). No tools installed.
Receipts: `.ufo/waves/round-90/w1/ScoutGround/` (paths below are relative to that dir unless absolute). Scratch `/fast/scratch/hyaku/kake-r90/ScoutGround/` was created, passed as `--work`/`TMPDIR`, and deleted before yield. Any `/fast/scratch` path echoed inside a receipt is not evidence.

## F1 — Sandbox bypass: delegation admitted (DEFECT, high)

`SANDBOX` (scripts/cache_key_conformance.py:284-330) denies `subprocess.Popen`, `os.exec*`, `os.posix_spawn`, `os.fork` and other events. The private stdlib module `_posixsubprocess` is in `sys.stdlib_module_names`, so its import passes the import check, and `_posixsubprocess.fork_exec` raises no audit event. The child interpreter it starts has no audit hook.

| Probe candidate | Delegates to | Result | Receipt |
|---|---|---|---|
| `neg-forkexec-delegate.py` (15 lines) | `/usr/bin/python3 scripts/cache_key.py` | `advisory=2/3 … clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=9090 met=true`, exit 0 | `probe-neg-forkexec-delegate.txt` |
| `neg-forkexec-gate-reference.py` | `python3 -c` imports `cache_key_conformance` and calls its `reference()` | `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=9090 met=true`, exit 0 | `probe-neg-forkexec-gate-reference.txt` |

Command (run from the lane root): `python3 -B scripts/cache_key_conformance.py --candidate .ufo/waves/round-90/w1/ScoutGround/<probe>.py --work <scratch> --seed 9090 --verbose`

Statements this falsifies:
- The gate docstring (lines 7-10) says the candidate may "spawn no process".
- Knowledge entry `corpus/knowledge/cache-key-conformance-gate.md:35`, Sandbox row: "no process".
- `:46`, error pattern "Delegating to the counter's reference … sandbox (exit 97, uncatchable)". That holds only for in-process import or exec, not for a spawned process.
- `round-90.md` Mistakes row 4 and the L1 draft `PROVINCE.md` wording "with an execution-time sandbox against delegation".

Limits of this finding:
- It does **not** falsify the C2 counter predicate, which is scored over the frozen 57+4 population. Neither probe is in that population, and the gate still refuses `neg-oracle-path-import` (`pattern-neg-oracle-path-import.txt`: `SANDBOX_VIOLATION import c89_key`, `sandbox=violation met=false`, exit 1).
- The entry's own Limits line (`:60-61`, "evidence against delegation, not a security boundary") partly hedges this. Even as evidence against delegation, though, the sandbox misses a two-call stdlib route.

Candidate fixes for L1 (not applied):
- deny import of `_posixsubprocess`, plus `_ctypes` and `_socket` for symmetry;
- or set `RLIMIT_NPROC=0` in a `preexec_fn` on the candidate subprocess, so the kernel enforces it rather than the audit hook;
- then add both probes as standing negatives.

## F2 — Crashes are reported as `sandbox=violation` (DEFECT, medium: misattribution)

Any uncaught exception in a candidate makes the traceback printer (linecache) open `<work>/sandbox.py`. That path is not under the stdlib roots, so the hook kills the process with exit 97.

- `pattern-adv-bad-json.txt`: `FAIL refusals/malformed-json: violation`, `SANDBOX_VIOLATION open …/sandbox.py`, then `sandbox=violation met=false`.
- `probe-neg-crash-traceback.txt`: a naive `json.loads`/`obj["uri"]` script gives `sandbox=violation`, `hand=3/70`.

Consequences:
- The verdict stays correct.
- The `sandbox=` field no longer separates delegation from crashing.
- The entry's error-pattern row (`:45`), "Crashing on malformed JSON … caught by `malformed-json`, `empty-input`", is mis-described: those cases fail as `violation`, not on the refusal shape.

Fix: allow opening the gate's own sandbox path, or install the hook after `runpy` resolves its frames.

## F3 — Numbers in the knowledge entry against the source and checklist runs

| Stated (entry) | Source / run | Match |
|---|---|---|
| 70 hand cases | `hand_cases()` lines 151-246: 7 worked + 18 members + 7 names + 12 values + 6 escaping + 6 layout + 14 refusals = 70; run prints `hand=70/70` | yes |
| 120 generated | `--generated` default 120 (line 405); run `generated=120/120` | yes |
| 3 advisory | `advisory_cases()` lines 378-382; `advisory=1/3` | yes |
| 6 clauses | tags layout, members, names, values, escaping, refusals; `clauses=6/6` | yes |
| Checklist 1: `advisory=1/3 outside-contract-gaps=utf8-required,nul-in-value`, `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok met=true`, exit 0 | `checklist-cache_key.txt`: identical, seed 2102391599, exit 0 | yes |
| Checklist 2: adv-cr-only `met=false`, exit 1 | `checklist-adv-cr-only.txt`: `clauses=5/6 hand=68/70 generated=117/120 … met=false`, exit 1 (fails cr-only, cr-unnominated) | yes |
| Checklist 3: neg-exec-source `sandbox=violation met=false`, exit 1 | `checklist-neg-exec-source.txt`: `SANDBOX_VIOLATION open …/round-89/c89_key.py`, `clauses=0/6 … sandbox=violation met=false`, exit 1 (also `advisory=0/3`, not stated) | yes |
| Error-pattern table (`:41-47`) | `pattern-*.txt`, seed 9090:<br>- adv-raw-sort fails sort-lowered-a-B/B-a (+Zb)<br>- adv-no-name-escape fails name-percent-present/absent<br>- adv-cr-only fails cr-only and cr-unnominated<br>- M23 fails cr-only, lf-only, cr-unnominated, lf-unnominated-novary<br>- M24 fails lf-only, lf-unnominated-novary<br>- adv-missing-headers fails headers-missing(-vary)<br>- M37 fails name-percent-absent<br>- neg-oracle-path-import gives exit-97 import violation | yes, except adv-bad-json (F2) and the reference-delegation row (F1) |
| RFC lines | retained bodies `.ufo/waves/round-90/L1/src/` (sha256s match the entry):<br>- 9110 "invalid and dangerous" spans 1606-1607<br>- 9111 "cache key" at 251, method/URI at 252, Vary at 258-261, §4.1 title at 526<br>- 8259 §7 at 429-431, §8.1 at 485-486 | yes, but entry `:16` says "lines 1606–1609" for a quote ending on 1607 (lesson says 1606–1607): minor imprecision |
| Wide run | `wide-seed90-gen2000.txt`: shipped candidate `generated=2000/2000 met=true`, exit 0 (no reference/candidate drift at 2000 cases, seed 90) | consistent |

Observation, not a defect: RFC 9111 lines 254-256 ("many HTTP caches in common use today only cache GET responses and therefore only use the URI as the cache key") directly supports the R90-4 method-omission limit. The entry and lesson could cite it.

## F4 — Existing material: what the gate duplicates and what is new

Method: text grep (no LSP; these are Markdown and stdlib scripts). Relevant hits:

- `scripts/cache_key.py:2`, `corpus/knowledge/cache-key-construction.md:1-5,138-168,188-196`. The construction entry's Limits say the round-89 counter "does not establish the whole contract" and admits seven violating variants. The gate is the instrument those lines lacked: it **newly covers** per-clause cases and generated cases decided by its own reference.
- `.ufo/waves/round-89/c89_key.py` (SKILL.md row "c89 key capability"). The gate **duplicates** its role: a contract reference, seeded generation, scoring of one candidate. `reference()` (lines 76-117) is the third independent implementation of the contract (c89 reference, `cache_key.py`, gate). It supersedes c89_key functionally; the c89 row remains as history.
- `corpus/knowledge/vary-matching.md:5,262-264,296-300,317-320` and `scripts/vary_match.py:22-34`. This is the match half; it explicitly disclaims key construction and conformance. No overlap. `:317` treats "CR, LF and NUL never enter a field name" as an adapter convention; the gate **newly covers** CR/LF in *values* on every header (S466).
- `corpus/README.md:705-713` (round-88 frontier step) lists "the CR/LF/NUL rule" as remaining frontier. Round 90 moves CR/LF into the contract's refusal clause on S466 ground and routes NUL (R90-2). That paragraph is now partly historical and has no appended note yet.
- Sandbox prior art: `corpus/QUALITY.md:1007-1019` (r40 (r) "A counter's sandbox exposes no witness identity"; r41 SentinelSandbox) and `:1060-1064` (r42 CpuHide). These confine the *tool under a counter* against witness leaks. The gate's audit hook is the lane's first candidate-confinement sandbox, so this is new. It does not reuse the r41/r42 process-level containment lessons, and F1 is the gap a process-level limit would have closed.
- Field-value validity: `SKILL.md:1568` (cache_control_effective, "bounded field-value decoder") has no CR/LF/NUL rule. S466 is the first field-value-validity row (`corpus/SOURCES.md:212`).
- Registry: `corpus/SOURCES.md:212-214`, S466-S468 (205 rows, base 202).

Residual from the D89-3 closure:
- S467 `used-by` lists `corpus/knowledge/cache-key-construction.md`, but that entry does not cite S467. Its `source:` line still names S463 as construction ground (grep: S467 appears only in the gate entry and the lesson).
- `used-by` is routing data (`SKILL.md:599`), so this is a tension, not a false entry. An appended `[r90-correction]` tail on the construction entry naming S467 would reconcile it.

## F5 — Registry rows for L1 (in the lane's formats)

The L1 has already drafted uncommitted rows (`git diff HEAD`: SKILL.md +3, README +1, PROVINCE +10, QUALITY +23). I checked them against code and neighbours and propose these amendments.

**SKILL.md.** Neighbours are the round-88 table header `| Name | Kind | Entry command | Verdict map | Selftest | Pinned values | Write scope | Owner |` (SKILL.md:1605) and `| c89 key capability | gate | … | 0 clean/met; 1 failed/not-met | … --selftest (43/43) | seed 89089; 16 frozen cases … | --work scratch only | kake |`. Round 89 appended to the round-88 table without its own heading; the draft continues that pattern.

```
| cache_key_conformance | gate | `python3 -B scripts/cache_key_conformance.py --candidate <script> --work <explicit-scratch> [--seed N] [--generated N]` | 0 clean/met; 1 failed/not-met; 2 usage, missing candidate or reference self-check failure; the `advisory=` line is never scored; `sandbox=violation` also fires on any uncaught candidate exception, and `sandbox=ok` does not exclude delegation through `_posixsubprocess.fork_exec` (round-90 w1 ScoutGround) | built-in reference self-check against the contract's seven worked examples and every hand case (exit 2 on drift) | `.ufo/waves/round-89/c2-contract.md`; 6 clauses, 70 hand cases, 120 generated (seed printed), 3 advisory (S466, S468) | `--work` scratch only; candidate runs under an in-process audit hook | kake |
| c90 defects | gate | `python3 -B .ufo/waves/round-90/c90_defects.py --root . --revision <rev> --work <explicit-scratch>` | 0 clean/met; 1 failed/not-met (open items named in the JSON line); 2 argparse usage; D1 carries one live working-tree conjunct | none in the counter; pre-freeze controls `.ufo/waves/round-90/controls/ctl-c1.txt` (do-nothing, 7 forgeries, 1 positive) | sha256 462224f6…; inherited sha256 4046c204…; c89 blob 0dee1dc8; rfc9111 sha256 aeb52adb… | `--work` scratch only (scratch clone for the c89 re-run) | kake |
| c90 gate capability | gate | `python3 -B .ufo/waves/round-90/c90_gate.py --root . --revision <rev> --work <explicit-scratch> [--seed N]` | 0 clean/met; 1 failed/not-met (gate absent, false admits, errors, anti-table hits, population drift); 2 unresolved revision or argparse usage | none in the counter; pre-freeze controls `.ufo/waves/round-90/controls/ctl-c2.txt` (no gate, blanket refuse/admit, hash- and name-table gates) | sha256 703b0058…; 4 positives + 57 negatives pinned in `.ufo/waves/round-90/frozen/c2-population.sha256` (a57f8985…) | `--work` scratch only; nonce copies beside the extracted subjects | kake |
```

Changes from the draft:
- exit 2 for c90 gate (`c90_gate.py:108-110` returns 2 on an unresolved revision; the draft omits it);
- missing-candidate exit 2 for the gate (`cache_key_conformance.py:415-417`);
- the F1/F2 sandbox caveats;
- counter sha256 pins from `freeze.md:15-16,35-38`.

Proposed prose under the table: "From round 90, `scripts/cache_key.py` is gated by `scripts/cache_key_conformance.py`; the `cache_key` row's Selftest cell (`c89_key.py --selftest`) is historical."

**corpus/README.md frontier table.** Header `| Frontier ground | Entered in round | Entries | Rows |`. Neighbour row: `| Cache-key construction (Vary-nominated stored-response key; key only, not storage or reuse) | r89 (lands this round, instrument not admitted) | knowledge/cache-key-construction.md + scripts/cache_key.py | S463 S465 |`. Proposed row:

```
| Cache-key conformance (does a key constructor implement the contract; field-value validity; JSON text encoding) | r90 (lands this round, gate not admitted) | `knowledge/cache-key-conformance-gate.md` + `scripts/cache_key_conformance.py` | S466 S467 S468 |
```

The only change from the draft is the Entered cell, which follows the r89 pattern because outside closure owns admission. Proposed appended note after the round-88 frontier paragraph: "Round 90: CR/LF in any field value is now a contract refusal grounded on S466; NUL stays routed (R90-2); field-specific normalisation stays frontier." The preamble's "measured at the final revision (N rows, S… added)" convention stops at round 60 (README:93-98), so no sentence is required.

**PROVINCE.md.** Neighbour: `## Round 89 — cache-key construction only` … "so the ground is recorded as held-but-unadmitted." Proposed ground paragraph:

```
## Round 90 — cache-key conformance gate

`scripts/cache_key_conformance.py` and `corpus/knowledge/cache-key-conformance-gate.md`
(S466, S467, S468) decide whether a key constructor implements the round-89 key
contract: per-clause hand cases, seeded generated cases decided by the gate's own
reference, an in-process audit hook that catches stdlib-external imports and file
opens (not a process boundary: a `_posixsubprocess` spawn is not caught), and an
advisory line for inputs the contract leaves undecided (non-UTF-8 input, NUL in a
value, raw control characters in JSON). S467 supersedes S463 as the construction
ground (RFC 9111 §2, §4.1). Still outside: storability, reuse, revalidation,
freshness, serving and browser behaviour; the request method is not part of the
lane's key (adapter limit). Held, unadmitted until the outside spot-check.
```

## Honest limits
- C1 (`c90_defects.py`) was not re-run or attacked by this seat; only D89-3's residual `used-by` tension (F4) was observed.
- Probes ran against the working tree at HEAD `79e1aac2` with the system Python 3.14.8. `_posixsubprocess.fork_exec` arity is version-specific, and the probe was exercised only here.
- Generated-case agreement was checked for one wide seed (90, 2000 cases), plus seeds 9090, 2102391599, 1843433862 and 584909056 on single runs; this is not exhaustive.
- The c90_gate counter was not re-run with the two new probes (they are not in its frozen population, by design).
