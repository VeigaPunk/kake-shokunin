# SimplifierV2 — YAGNI review of the driver-v2 receipt-validity gate (round-45 wave 1)

Seat: `kake-r45.SimplifierV2` · role simplifier · axis operability · 2026-10-24.
Report-only item: the L1 owns the instrument bytes; nothing outside this report and
`/fast/scratch/hyaku/kake-r45/SimplifierV2/` was written. No tools installed (python3
present; pacman paused; nothing needed).

## What was reviewed

The v2 mechanism spec (`.ufo/waves/round-45/make_w1_spec.py:182-201`, identical text in
`w1-spec.json`/`w1-plan.json`/`w1-taskcall.json` "ExecDriverV2"): one receipt-validity
gate, `receipt_validity(receipt, exit_code, mtime_bounds, counter_sha)`, valid iff
receipt parses ∧ `receipt['counterSha256'] == invoked counter sha` ∧ receipt mtime in
`[started_ns-eps, finish_ns+eps]` ∧ "receipt exit recorded in {0,1}" ∧
`receipt.get('note') != 'tool absent'` ∧ receipt has a recorded seed; invalid rows join
`errors[]` as `counter_error / tool_absent / stale_receipt`; plus v2-only behaviors
outside the gate (v2 creates the outdir cohort itself and refuses a non-empty one;
writes `run-manifest.json {started_ns, counter_sha256, nonce}` before spawning).

Ground truth read: frozen v1 driver `.ufo/waves/round-44/c44_audit.py` (sha
`8ee2c8bf…`; `run_counter` :49-61 reads whatever JSON parses at the out path
regardless of returncode; row `exit` = subprocess returncode :158; `note` dropped
:157-160; `rec=None` → error row), frozen counter `.ufo/waves/round-44/c44_count_v5.py`
(seed + `counterSha256` written at receipt assembly :995-1003; tool-absent note :1113
**still carries the seed**; `finish(2)` on CannotEvaluate :1114-1119 with "a receipt in
every case"), `.ufo/waves/round-44/w2/ReviewCounterContract.md` defects
1a/1b/1c (+2, +3), a real receipt
`.ufo/waves/round-44/verification/claim/after-final/tools/repeat-len-band.json`
(`seed: 187926495163792`, `counterSha256: 5cedaa3b…` = the counter's own declared sha,
`note: null`, no top-level exit field), and the frozen C1 claim sentence
(`SCORECARD.md:3639-3657`): refuse witness **and** not-met credit for receipts that
(i) record a counter exit other than 0/1, (ii) record note "tool absent", (iii) were
not written inside the driver's run window **over the invoked counter bytes**.

`c45_audit.py` did not exist on disk at review time (ExecDriverV2 in flight); this is
the itemed spec-level review, so that is expected, not a blocker.

## Per-check verdict (staged shapes: 1a counter-error, 1b tool-absent, 1c stale-planted)

Staged facts: 1a = real receipt copy, own-sha, in-window, seeded, note "cannot
evaluate…", process exit 2. 1b = own-sha, in-window, **seeded** (v5 :997/:1113), note
"tool absent", exit 1. 1c = planted byte-exact real receipts (real-v5 sha ≠ invoked
fake sha, mtime before the run, seeded, honest note), counter SIGKILLs → driver-observed
exit −9.

| Spec check | Deleted solo → which class regresses? | Verdict |
|---|---|---|
| exit set {0,1} | **1a counter-error** (its only failing clause) | KEEP — unique discriminator for class 1a |
| note ≠ "tool absent" | **1b tool-absent** (its only failing clause; 1b exits 1 and is seeded, so exit and seed do not back it up) | KEEP — unique discriminator for class 1b |
| seed presence | **none** — 1a falls to exit, 1b to note, 1c to sha+mtime+exit | **DELETION CANDIDATE** |
| sha binding | none solo (1a→exit, 1b→note, 1c→mtime ∧ exit −9) | KEEP (claim clause iii "over the invoked counter bytes"; unique catch: in-window receipt over *different* bytes, e.g. a touched cross-counter plant) |
| mtime window | none solo (1a→exit, 1b→note, 1c→sha ∧ exit −9) | KEEP (claim clause iii "inside the run window"; unique catch: same-bytes staleness — the organic 1c rerun trigger of defect 1c, where sha *matches* and only mtime tells) |

## Decisive evidence (verbatim)

Command: `python3 -B /fast/scratch/hyaku/kake-r45/SimplifierV2/gate_truth_table.py`
(scratch probe modelling the three staged receipt shapes and the gate clauses exactly as
specified; full script retained in scratch):

```
== full 5-part gate (spec) ==
spec gate: parse+sha+mtime+exit+note+seed invalid_accepted=0 all refused
== solo deletion of each part ==
delete seed presence                   invalid_accepted=0 all refused
delete exit set {0,1}                  invalid_accepted=1 REGRESSION: counter_error(1a)
delete note check                      invalid_accepted=1 REGRESSION: tool_absent(1b)
delete sha binding                     invalid_accepted=0 all refused
delete mtime window                    invalid_accepted=0 all refused
== multi-deletion / variant probes ==
delete sha+mtime (exit-only byte/window shadow) invalid_accepted=0 all refused
delete exit+sha+mtime (note+seed only) invalid_accepted=2 REGRESSION: counter_error(1a),stale_plant(1c)
trap: 1a with exit read from receipt internals  -> ACCEPTED (claim regress)
== minimal gates ==
minimal closing all 3 staged classes: parse+exit+note invalid_accepted=0 all refused
claim-faithful minimal: parse+sha+mtime+exit+note (seed dropped) invalid_accepted=0 all refused
```

Supporting v1/v5 bytes (read, not mutated):
`c44_count_v5.py:995` `seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")`;
`:1003` receipt init carries `"seed": seed` and `counterSha256`;
`:1113` `rec["note"] = None if "cand" in paths else "tool absent"` (seeded either way);
`:1114-1119` CannotEvaluate → `rec["note"] = "cannot evaluate: %s"` + `finish(2)`;
`c44_audit.py:56-60` receipt read whenever it parses regardless of `p.returncode`;
`:158` row `exit=code` (subprocess returncode); ReviewCounterContract 1c end-to-end:
SIGKILL counter with planted receipts → `"exit": -9` rows yet `"ok": true`.

## Findings

1. **Deletion candidate: seed presence (5 parts → 4).** No staged class regresses; the
   frozen claim sentence does not name it; the spec's own named invalid classes
   (counter_error/tool_absent/stale_receipt) do not include a seedless class; the
   spec's selftest addition list has **no seedless fixture**, so the clause ships
   unexercised; and real tool-absent receipts *are* seeded (v5 :997/:1113), so it does
   not even strengthen 1b. Residual if deleted: a seedless but otherwise in-window,
   own-sha, exit-{0,1}, honest-note receipt counts valid — only the invoked counter can
   write that file (fresh-outdir rule), and `row['seed']=None` still surfaces in the
   summary for C2 re-derivation to flag. If the L1 wants the guard anyway, fold it into
   the parse/error-row path (v1 already emits seed-less error rows without crashing),
   not into the validity gate.
2. **Simplification shown: one check closes two of the three classes.** The
   driver-observed exit check alone refuses both 1a (exit 2) and the staged 1c (SIGKILL
   → −9). The minimal gate closing all three staged classes is
   `parse ∧ exit_code∈{0,1} ∧ note≠"tool absent"` (probe: `invalid_accepted=0`).
   **Tradeoff, and why I do not recommend it:** that gate implements claim clause (iii)
   only through the process shadow (the fixture's SIGKILL); it accepts a clause-(iii)
   receipt *property* violation — e.g. a no-op counter that exits 0 over a planted
   same-window receipt, or the organic rerun staleness of defect 1c. The
   **claim-faithful minimum is 4 parts: parse ∧ sha ∧ mtime ∧ exit ∧ note, seed
   dropped.** sha and mtime are cross-masked in staging (each solo-deletion is caught by
   the other plus exit), which means the before/after fixture matrix can never
   individually falsify them — they are kept on claim text and on their unique organic
   catches (wrong-bytes-in-window for sha; same-bytes-out-of-window for mtime), not
   because the matrix proves them.
3. **Spec trap to pin (would regress 1a silently):** "receipt exit recorded in {0,1}"
   must mean the **subprocess returncode** (v1 `row['exit']`, the gate signature's
   `exit_code`), not any receipt-internal field — real receipts have no top-level exit
   (only per-run `candExit`), and 1a's receipt is copied from a real receipt with honest
   `candExit` values, so an internal reading accepts it (probe line "trap"). The
   in-memory selftest would stay green unless it pins explicit `exit_code=2` and
   `exit_code=-9` variants; the spec's selftest list pins counter_error only via the
   receipt fixture — name the exit_code variants explicitly.
4. **Interaction note (not a defect):** v2's create-and-refuse-non-empty outdir rule
   already structurally refuses the stale-planted fixture *as staged* (plants precede
   the run), so class 1c's after-stage refusal may come from the outdir rule, the exit
   check (−9), sha, and mtime — four independent layers. The matrix's
   `invalid_accepted=0` for class 3 therefore cannot distinguish which layer fired; if
   the L1 wants clause (iii) itself exercised (not its SIGKILL/outdir shadows), that is
   an ExecMatrixRunner/staging decision, outside this item.
5. Untouched by design: the gate's invalid-set feeding both `witnessed` and `not-met`
   counting (closes ReviewCounterContract defect 2), and the build-row count pin
   (defect 3) — both are separate from the five parts and are defect-2/3 fixes, not
   YAGNI targets.

## Pass/fail against the item's named question

**PASS (partial).** The three defect classes close with fewer than five checks in two
senses: (a) one part, **seed presence, is a clean deletion** with zero regressing
classes (5→4, the claim-faithful minimum); (b) a 3-check gate
(parse+exit+note) closes all *staged* classes, shown by probe, but it degrades claim
clause (iii) to a process shadow and is not recommended. Checks with no *solo*
regressing class other than seed: sha binding and mtime window — deletion candidates
only under a claim amendment; retained here because the frozen sentence names both
conjuncts ("inside the driver's own run window **over the invoked counter bytes**").

## Exact commands run

- `python3 -B /fast/scratch/hyaku/kake-r45/SimplifierV2/gate_truth_table.py` (output above)
- `grep -n "seed\|note\|tool absent\|candExit\|CannotEvaluate" .ufo/waves/round-44/c44_count_v5.py`
- `grep -n "sys.exit\|json.dump\|with open" .ufo/waves/round-44/c44_count_v5.py`
- reads: `make_w1_spec.py:140-205`, `c44_audit.py:60-214`, `c44_count_v5.py:1105-1140`,
  `ReviewCounterContract.md`, `SCORECARD.md` (round-45 declaration), real receipt
  `after-final/tools/repeat-len-band.json`, `w1-spec.json`/`w1-plan.json` items.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/SimplifierV2.md` (this report)
- `/fast/scratch/hyaku/kake-r45/SimplifierV2/gate_truth_table.py` (scratch probe)

## Blockers

None. `c45_audit.py`/`c45_matrix.py` absent at review time — spec-level item, v1 bytes
and the frozen declaration were sufficient; no sibling artifact awaited (independent
leaf, no waits).
