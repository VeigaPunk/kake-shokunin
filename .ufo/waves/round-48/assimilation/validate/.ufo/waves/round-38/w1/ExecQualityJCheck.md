# QUALITY (j) — executable control-consequence check (round-38 wave 1)

Built the missing executable check for QUALITY (j) (round-37 closure routed defect 3): a
control that meets the predicate taints its counter, and a claim measured on a tainted counter
is caught without a human reading receipts.

## Deliverable

`/fast/scratch/hyaku/kake-r38w1/ExecQualityJCheck/control_consequence_check.py`
sha256 `c69ab476f5dd1402d59b1bea2ff78d2dc3a3a29aac6b65525277380f817d44d3`, 452 lines, stdlib
only (`argparse io json os re shutil subprocess sys tempfile pathlib`), writes nothing. Nothing
installed or upgraded (python3 and git 2.56.0 already present). To land as
`.ufo/waves/round-38/criteria/control_consequence_check.py`.

Rule encoded: group every JSON receipt by `counterSha256`; a control receipt with `met: true`
taints its counter; every non-control receipt with `met: true` under a tainted counter is a
violation (exit 1 with the list); none → exit 0; unreadable/unevaluable input → exit 2. Naming
convention documented in the module docstring (lines 22-40): control = basename starts
`control-`/`control_`, or sits under a path component `controls`/`pre` and bears a control name
(`control`/`ctl`/`critic`, optional `rNN-` tag). Control-seat names outside those directories
(round-38 `v3/Ctl*`, `v3/Critic*`) are **not** controls for the verdict — round-38 C2's
declaration pre-registers the full-rule tools as builds — and print as `note:` only.

## Runs (TMPDIR in sandbox, `GIT_*` unset, all `timeout`-capped)

| command | exit | observed |
|---|---|---|
| `--selftest` | 0 | `selftest: 10/10 ok`: compliant 0, tainted 1, violation named, seat-name noted-not-tainting 0, `pre/Ctl…` 1, malformed 2, control-without-met 2, no-receipts 2 |
| `--verification .ufo/waves/round-37/verification` | 1 | `tainted_counters=1 violations=4` |
| `--root LANE --revision 2dab7f31… --verification .ufo/waves/round-37/verification` | 1 | same 4; receipt census identical to filesystem (54 receipts, 7 controls, 13 skipped) |
| round-36 dir, filesystem / git at `2dab7f31` | 0 / 0 | `RESULT: PASS … tainted_counters=0` |
| round-38 dir, filesystem / git at `2dab7f31` | 1 / 1 | `tainted_counters=1 violations=30` |
| `fixtures/compliant` / `fixtures/tainted` (constructed) | 0 / 1 | PASS / names `c1-at-aaaaaaa.json` |
| missing dir / empty dir / bad revision / `/tmp` outside root | 2 / 2 / 2 / 2 | named one-line errors, no traceback |
| two identical r37 runs | — | byte-identical output (`cmp` clean) |

Red run, round 37: `control-CtlC1Shortcut-followup.json:4,11` (counter `2ebb39b5…f0e3`,
`met: true`, 28/28) and `c1-at-9dbc88bb.json:4,11` (same counter, `met: true`, 28/28) →
`VIOLATION: c1-at-9dbc88bb.json`. Same counter also lists `ablations/reference.json`,
`c1-keyrev-at-9dbc88bb.json`, `independent-selftest-reference.json` (load-bearing pair is the
control plus `c1-at-9dbc88bb`).

Green runs: round 36 (all 15 controls `met: false`; its `met: true` receipts sit on untainted
counters) and the constructed compliant directory (control `met:false` + claim `met:true`).

Round 38 as-is: **exit 1**. Tainted counter is `52daff55…6e7b` (v2, C1's withdrawn counter),
tainted by `control-CriticPredicate-rulepatch{,_pct}`, `control-CtlBaseWrapper-care`,
`control-CtlLabelShortcut-delegate_ceiling` (all 20/20 `met:true`). The 30 violations are
`pre/reference.json` (20/20) and 29 `mutref/M*.json` survivors. The live v3/C2 counter
`28b120a5…f9e4` is **untainted under the declared naming rule**; it carries four non-verdict
`note:` lines (`v3/CtlBaseWrapper-care`, `v3/CtlLabelShortcut-delegate_ceiling`,
`v3/CriticPredicate-rulepatch{,_pct}`, all 20/20), which match the round-38 declaration's
pre-registered builds. Under the narrow reading ("non-control receipt" = `c<N>-` claim
measurement, as the assignment's parenthetical suggests) round 38 exits 0: no `c1-*`/`c2-*`
receipt is `met:true` under a tainted counter (one-off scan, tool unchanged).

Evidence files in `/fast/scratch/hyaku/kake-r38w1/ExecQualityJCheck/`: `ev-r37-fs.txt`
`7018384c…36db`, `ev-r37-git.txt` `54bb9888…e416`, `ev-r36-fs.txt` `88f23039…2060`,
`ev-r36-git.txt` `0bb61e39…9e83`, `ev-r38-fs.txt` `989e58fc…ce5b`, `ev-r38-git.txt`
`0fe8c3a4…8082`, `fx-compliant.txt` `8f9d2830…5860`, `fx-tainted.txt` `9d581ce0…fe19`,
`det1.txt` `7018384c…36db`, `ev-missing.txt` `718306ac…c573`, `ev-empty.txt` `59fb45a7…420a`.

## Finding for the L1 (advisory, not a verdict)

QUALITY (j) fires on round 38 only through the already-withdrawn v2 counter, so this check does
not by itself reopen C2. The four v3 receipts at 20/20 are control-named tools the C2
declaration pre-registered as builds; the check cannot judge that class, and round-37's
after-scoring reclassification is not reproduced. If one is later treated as a control, v3 is
tainted and C2's predicate is met before the build.

## Not verified / limits

- Did not read or stat the sealed key trees, did not run a round-38 counter (no key); no network.
  Round 38 compliance is untested against a future receipt set (shown on round 36 + a fixture).
- Classification is name-based: a control receipt renamed outside the documented prefixes escapes
  taint (docstring states it). No check of `counterSha256` against the counter file, nor of `met`
  against `passed`/`target`.
- No lane file, index or jj state touched; read-only git only (`rev-parse`, `ls-tree`,
  `cat-file`); selftest/fixture temp dirs under the sandbox TMPDIR.
