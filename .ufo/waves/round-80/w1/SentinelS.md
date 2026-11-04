# SentinelS — round 80 w1 — adversarial robustness of the repaired `x_robots_tag_audit.py`

**Verdict: clean sweep.** Against the final worktree bytes (`d1ea524fcd8399b6eb5b8d52864784424a3596bc32aaeb32b2e99916cb5573f0`, 23,677 B, == live file at my final check): 59 recorded runs across the traceback hunt, the round-79 F1–F6 regression shapes, and ReDoS timings — **zero tracebacks, every exit code in {0,1,2,64}, no super-linear date matching, F1–F6 all still closed, selftest `33/33 passed` exit 0**. One informational defect was found **only in an intermediate landing** (`c3b10f34`, live for ~4 minutes mid-session): the amendment-1 comma merge was dead code; it is fixed in `d1ea524f` and needs no action.

No tools were installed or upgraded (nothing to record under the 2026-10-19 authorization). All probes ran under `/fast/scratch/hyaku/kake-r80/SentinelS/` (deleted before yield); manifests were crafted by my harness — the frozen case set was never read as input. I am a leaf; no subagents were used.

## Bytes timeline (the work surface moved under me — ExecGrammar was landing throughout)

| time (approx) | sha256 | bytes | state |
|---|---|---|---|
| session start | `dd83c2c8e9046faa0a62afda4cea00fee85468e83d2f1720c92159fb11f2609b` | 19,680 | round-79 committed tool, amendment not yet landed |
| 07:57 | `c3b10f34e2cedbc853e9ecd40c4fe4b44cb26c6456e0b4cd81784b38736d360f` | 21,265 | snap1: `ASCTIME_RE` + `DATE_COMMA_RE` defined & wired, but merge **dead** (below) |
| 08:01 | `d1ea524fcd8399b6eb5b8d52864784424a3596bc32aaeb32b2e99916cb5573f0` | 23,677 | snap2: regex tail `,`→`$`, selftest t24–t30; **== live at final check** |

Battery receipts: `battery-snap.json` (59 rows, snap1) and `battery-snap2.json` (59 rows, snap2) in `.ufo/waves/round-80/w1/SentinelS/` (sha256 `9008af78…befb`, `fa7b41c5…190d`). Note: `battery-snap.json` was produced by the pre-parameterization build of my harness (case logic identical; the saved `battery.py`, sha `f389018c…5ff1`, only later gained argv tool-path selection). Every row records rc, traceback flag, parsed findings/error.id, wall seconds, stdout digest.

## 1. Traceback hunt — new date/comma path (snap2 = final bytes)

All 18 crafted values × text+`--json` modes: rc ∈ {1} (decided), no stderr output at all. Representative rows:

| probe | findings (json mode) |
|---|---|
| `unavailable_after:` alone | `xrt_invalid_value` |
| `unavailable_after: ,` | `xrt_empty_rule`, `xrt_invalid_value` |
| `unavailable_after: Wed,` (comma = last byte) | `xrt_invalid_value` only — merge fires, no `xrt_empty_rule` |
| `unavailable_after: Wednesday,` | `xrt_invalid_value` only |
| `unavailable_after: Wed,`+1 MB spaces | `xrt_invalid_value` only, 0.027 s |
| `unavailable_after: Wed`+1 MB spaces+`, 03 Dec…` | `xrt_invalid_value`, `xrt_unknown_directive` (comma not adjacent to weekday → A1 scope correctly not applied) |
| `unavailable_after:`+`Wed,Wed,…` 20 000 tokens | `xrt_invalid_value`, `xrt_unknown_directive`, 0.030 s (linear) |
| full date + trailing comma | `xrt_empty_rule` only (trailing "other comma" → empty segment; amendment-consistent) |
| `googlebot: unavailable_after:` | `xrt_invalid_value` (scoped) |
| `a: b: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | `xrt_unknown_directive` |
| NUL inside date value | `xrt_invalid_value`, `xrt_unknown_directive` |
| lone surrogate (`\ud800`) in id and value | `xrt_invalid_value`, `xrt_unknown_directive`; JSON round-trips, no crash |
| `googlebot: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | **clean, rc 0** — matches the c40 oracle expectation |
| `WED,` uppercase weekday / double comma | decided, rc 1 |
| `,` alone | `xrt_empty_rule` |

Input-fault neighbours: non-UTF-8 manifest and empty file → `xrt_input_bad_json` rc 2, single JSON error object.

## 2. Round-79 defect classes stay closed (snap2)

| class | probe | result |
|---|---|---|
| F1 5000-digit int | `max-snippet:`+`"1"*5000` and `-`+`"1"*4999` | `xrt_invalid_value` rc 1 both (ValueError guard holds) |
| F2 deep JSON | 100 000-deep `checks` | `xrt_input_bad_json` rc 2, 0.027 s (RecursionError caught); 20 000-deep parses → `xrt_input_check_shape` rc 2 |
| F3 `/dev/zero`, FIFO, directory as `--manifest` | `os.stat` gate | `xrt_input_unreadable` rc 2 in ≤0.026 s each — no hang, no block, no unbounded read |
| F4 duplicate value-bearing directives | `max-image-preview: large, max-image-preview: standard`; `unavailable_after:2025-12-31, unavailable_after:2026-01-01` | `xrt_duplicate_directive` rc 1 both |
| F5 id injection | id `c01\nXRTv1 checks=999 findings=0 exit=0\n\x1b[32mFAKE-GREEN` | line-level check (`f5-linelevel.txt`, sha `571f298a…9f14`): forged summary lines **0**, raw ESC byte **absent**, exactly one summary `XRTv1 checks=1 findings=0 exit=0`, JSON id round-trips exactly |
| F6 usage | `--bogus-flag`; `--manifest` w/o value; no args | rc **64** each, usage on stderr, no traceback |

My first pass recorded `forged_line_present=true` for F5 — that was my own substring check matching the *escaped* inline text (`…\x0aXRTv1 checks=999…` inside the check line), not a real forged line; the line-level receipt supersedes it. The comma repair reintroduced none of F1–F6.

## 3. ReDoS — date matching on adversarial values (60 s cap, snap2)

| value | wall |
|---|---|
| `unavailable_after: Wed, `+`"0"*50 000` | 0.024 s |
| `…+100 000` | 0.025 s |
| `…+200 000` (the prescribed shape) | 0.025 s |
| `unavailable_after: Wed,`+`"0"*200 000` (no space) | 0.024 s |
| `Wed Dec `+`"0"*200 000` (asctime-ish) | 0.023 s |

Flat 50 k→200 k: no super-linear pattern. All four shape regexes are anchored literal alternations without nested quantifiers; the merge loop extends each piece at most once (O(n) over pieces). 1 MB-space and 20 k-token probes: 0.023–0.030 s.

## 4. Informational (intermediate bytes only) — dead comma merge in `c3b10f34`

In snap1, `DATE_COMMA_RE`'s pattern ended in a literal `,` but was matched against post-`split(",")` pieces, which can never contain a comma → the merge condition was unreachable and every comma-bearing date kept the round-79 unprotected signatures (t03: `xrt_empty_rule`+`xrt_invalid_value`; bot-scoped: +`xrt_unknown_directive`). Mechanical proof (`dead-code-proof.txt`, sha `9cf4631a…3217`): `match("unavailable_after: Wed")=False`, `match("unavailable_after: Wed,")=True`; 18/18 snap1 hunt rows corroborate. The `c3b10f34→d1ea524f` diff is exactly the regex tail `,`→`$` ("the piece must END at the weekday token, so the consumed comma immediately followed it") plus selftest t24–t30. **Resolved at the final bytes; no action.** Routing note: none needed.

## 5. Selftest

`python3 -B <tool> --selftest` → `selftest: 33/33 passed`, rc 0 (26/26 at snap1; A5's seven amendment cases landed with snap2).

## Commands (verbatim)

- `python3 -B /fast/scratch/hyaku/kake-r80/SentinelS/battery.py <snapshot> <tag>` — exit **0** both runs (59 rows, violations `[]`).
- importlib regex probe against snap1 → `dead-code-proof.txt`.
- f5 line-level subprocess check → `f5-linelevel.txt`.
- `sha256sum` of live tool before/after the battery: `c3b10f34…` / `d1ea524f…` (== snap2 at final check).
- Diff `snap` vs `snap2`: regex tail `,`→`$`, comment update, +7 selftest cases, nothing else.

Scratch tree `/fast/scratch/hyaku/kake-r80/SentinelS/` deleted after receipt copy — see cleanup line below; a seat ending with its tree on disk reports itself, and this one does not.
