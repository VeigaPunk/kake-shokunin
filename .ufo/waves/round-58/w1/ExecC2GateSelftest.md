# ExecC2GateSelftest

Scope: claim C2 counter hardening, before data. Built a selftest for
`.ufo/waves/round-58/c58_resolver_cases.py` (v1 `selftest()` was a stub returning 2) in the patched copy
`.ufo/waves/round-58/w1/ExecC2GateSelftest.files/c58_resolver_cases.py`. The counter at its own path and the
lane tool `scripts/id_resolver.py` are untouched (that tool is unchanged from BASE_REV at lane tip `cc8da16`,
verified by diff against `git show 0440485:scripts/id_resolver.py`).

## DIFF

File: `.ufo/waves/round-58/w1/ExecC2GateSelftest.files/c58_resolver_cases.py` vs `.ufo/waves/round-58/c58_resolver_cases.py`
— `git diff --no-index --stat` = **1 file changed, 342 insertions(+), 2 deletions(-)**; the only deleted lines are
the two stub lines (`print("... version 1 has none ...")` / `return 2`).

`measure()` and `case_results()` are byte-identical to v1: no case expectation, fixture, regex, kill rule or exit
code was changed, so the gate's semantics for the lane's after-run are unchanged. Additions, all after the
`measure()` block:

- `BASE_REV = 044048597d62f3199494b63b36e90dd57825e350` + comment block stating what the selftest scores.
- `CONST_STUB` — control (a): prints the constant line `ids_cited=1 ids_resolved=1 dangling=0 owned_elsewhere=0 unowned=0`, exit 0.
- `MINI_STUB` — one minimal resolver used as a template, with four injected flags: `FENCE_DROP` (fence-aware but
  drops every line after the first fence), `ALWAYS_EXIT_ONE`, `BLANKET_DANGLING` (DANGLING for every cited id),
  `TALLY` (own `--selftest` tally string, or none). It reads knowledge at a revision via `git ls-tree -z` (so
  quoted/CJK paths are not dropped), parses only the `## Registry` section outside fences, honours the 0–3-space
  row rule, reads sibling registries at sibling `HEAD`, and emits the tool's `DANGLING … cited-by=… owners=… url-match=…`
  and `ids_cited=… ` lines.
- `_stub()` (flag injection), `_lane_root()` (walk up for `.git` + `corpus/SOURCES.md`, env fallback `C58_LANE_ROOT`),
  `_base_tool()` (`git -C <lane> show <BASE_REV>:scripts/id_resolver.py`; read-only), `_fixture_lane()` (commits a fixture
  lane holding the control tool at `scripts/id_resolver.py`, a 106-row `## Registry`, and one knowledge file citing all
  106 ids; `repo()` provides the `rev-parse --show-toplevel` assertion), `_control()` (scores one tool through the
  unchanged `measure()`, then checks score, exit code and named must-pass / must-fail cases), and the rewritten
  `selftest()`.

P7 is selftested without the lane's real revision: each control is committed as the tool of the fixture lane above, so
P7's `ids_cited >= 106` floor is satisfiable in scratch, and it still discriminates (a constant-green tool fails P7;
relaxing the floor to `>= 1` is caught — see below).

## SELFTEST RUN

Command (scratch root `/fast/scratch/hyaku/kake-r58/ExecC2GateSelftest`, now deleted; receipts in `.files/`):

    TMPDIR=<scratch> python3 -B .ufo/waves/round-58/w1/ExecC2GateSelftest.files/c58_resolver_cases.py --selftest

Result: **exit 0**, `selftest: ok (7 controls; P7 satisfied on a fixture lane)` — receipt `.files/selftest-run.txt`.

| control | score | exit | failing cases |
|---|---|---|---|
| (a) `const_green` | 1/12 | 1 | K1–K5, P2, P3, P4, P5, P6, P7 (P1 only) |
| (b) `blanket_dangling` | 3/12 | 1 | K1–K3, P1, P2, P4, P5, P6, P7 |
| (c) `fence_drop` | 9/12 | 1 | K1, P2, P6 |
| (d) `always_exit_one` (both defects closed, exit always 1) | 8/12 | 1 | P1, P2, P6, P7 |
| (e) `near_miss_p6` (correct, own tally 48/48) | 11/12 | 1 | P6 |
| (f) `full_green` (correct, own tally 49/49) | 12/12 | 0 | — |
| (d′) `base_tool` (`git show 0440485:scripts/id_resolver.py`) | 7/12 | 1 | K1–K5 (P1–P7 pass) |

Also run, read-only, with the patched counter against the real lane at BASE_REV — receipt `.files/gate-at-base-rev.txt`:

    python3 -B …/c58_resolver_cases.py --root <lane> --revision 044048597d62f3199494b63b36e90dd57825e350
    -> C2 resolver-cases 7/12 met=False; K1–K5 FAIL, P1–P7 PASS, P7 ids_cited=106; EXIT=1

That reproduces the contract's before-state (7/12) with the patched file, i.e. the added selftest changed no measured value.

Selftest-sensitivity probes (scratch mutants of the patched copy, receipts `.files/mutation-probes.txt`, `.files/k4k5-forbid-probe.txt`;
each probe ran from scratch, so the base-tool control reports `unrun base_tool_git_show: lane root not found above the
counter path` there — the unrun path is itself exercised, and the selftest exits 1):

- P7 floor `>= 106` → `>= 1`: caught — `FAIL const_green: score=2/12 expected=1/12; wrong-case P7_real_lane_green`.
- P6 floor `>= 49` → `>= 1`: caught — `FAIL near_miss_p6: score=12/12 expected=11/12; wrong-case P6_tool_selftest`.
- Adding `[r"^DANGLING S001 "]` to K4/K5 (proposed fix, see below): `blanket_dangling` falls 3/12 → 1/12, `base_tool` stays
  7/12, `full_green` stays 12/12 — the tightened gate is satisfiable and the selftest flags that the blanket control's
  expected set must move to 1/12 in the same patch.

Tooling: nothing installed (no `pacman`/`uv`/binary fetch); Python 3.14.2 (`sys.executable`) and git only.

## GATE DEFECTS FOUND

1. **K4 and K5 carry no forbid list** (`check(..., 1, [want])`, no `forbid_re`), and P3 forbids nothing either. Verified
   consequence: the `blanket_dangling` control — a tool that prints `DANGLING` for *every* cited id — **passes K4, K5 and P3**
   and scores 3/12. So K4/K5 prove the cited-by path is *named* (which does require reading the non-ASCII / `"`-bearing
   path at the revision), but they do not prove resolution survives for the registered S001 in the same run. Suggested
   patch (verified in the probe above, **not applied** — case semantics are the parent's): pass
   `[r"^DANGLING S001 "]` as `forbid_re` in K4/K5 and change the blanket control's expectation to 1/12 in the same patch.
2. **`url-match=` is never asserted.** `grep -n "url-match"` in the counter (v1 and patched) matches nothing; no fixture
   cites a URL, so every case runs with `url-match=-`, and `full_green` scores 12/12 while emitting only `-`. A fix that
   dropped the field (or its computation) entirely would still score 12/12. Only the tool's own selftest covers it, and P6
   checks the tally floor, not which cases ran. Suggested patch (not built): give P4's knowledge file a line quoting the
   sibling's S004 URL and require `url-match=alpha-shokunin` (or forbid `url-match=-`) on that case.
3. **P6 is a count floor only.** The base tool — fence-blind and `--revision` quote-blind — prints `selftest: 49/49`, so
   **P6 PASSes for the unfixed tool** (observed in `.files/gate-at-base-rev.txt`). P6 therefore cannot evidence that the
   shipped fix's own selftest covers D1/F1; only K1–K5 do. Suggested (decision for the parent, since it changes the kill-rule
   input): raise the floor to the fix's own tally (base 49 + its new cases) once the fix lands; any floor above 49 is
   satisfiable by the fixture controls here (they report 49/49 and 48/48).
4. Minor, same family as (1): no case forbids a spurious `DANGLING` line for a resolved id in the positive cases
   (`P1`, `P2` check only the summary line; `P4` only the S004 line). A tool that resolves correctly *and* emits extra red
   lines still scores 12/12. Fixing (1) covers K4/K5; covering P1/P2 would need `forbid_re=[r"^DANGLING "]`.

Not defects, stated limits: P7's floor is proved against a gate-built fixture (106 cited ids), not the lane; the
`--work` tree, `p6` copy and fixture repos are all created under `TMPDIR` and removed by `shutil.rmtree`.

## Files / evidence

- `.ufo/waves/round-58/w1/ExecC2GateSelftest.files/c58_resolver_cases.py` — patched counter (selftest added; `measure()`/`case_results()` unchanged).
- `.files/selftest-run.txt` — `--selftest` run, exit 0, 7 controls.
- `.files/gate-at-base-rev.txt` — patched counter at BASE_REV on the real lane: 7/12, EXIT=1.
- `.files/mutation-probes.txt` — P7-floor and P6-floor mutants caught.
- `.files/k4k5-forbid-probe.txt` — K4/K5 forbid probe: blanket 3/12 → 1/12, base 7/12 and full-green 12/12 unaffected.
- Scratch `/fast/scratch/hyaku/kake-r58/ExecC2GateSelftest` deleted; no lane jj/git index touched, no writes outside this report and `.files/`.

VERDICT: selftest written and green (7 controls, exit 0; base tool 7/12, near-miss 11/12, full green 12/12 reproduced on fixtures) and it catches relaxed P6/P7 floors — left for the parent: K4/K5 lack a forbidden-resolved-id check (blanket-red scores 3/12), `url-match` is never asserted, and P6 passes for the unfixed tool at 49/49.
