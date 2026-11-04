# ExecReceipts — round 78, wave w1 (evidence hygiene: routed defects 4 and 5)

**Verdict:** All four artifacts are delivered. The quote-truth baseline is green at the freeze revision
(`findings=0`, exit 0) but must be re-cut after the round's own rows commit; SentinelC's F1 "closing" digest
`00cb4fb2…`/48,225 B **never committed** (committed bytes are `2d66e5af…`/48,343 B, selftest 26/26); the fleet
root carries **no** untracked path naming kake or round 78; and the instrument-receipt gate is red on two
round-76 rows (`scripts/doc_quote_truth.py`, `scripts/hreflang_audit.py`) that were already missing at the base —
the round-78 instruments are absent from the tree and not yet in the population.

## What ran (verbatim, with exit codes)

| # | command (cwd = lane root unless stated) | exit |
|---|---|---|
| 1 | `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/doc_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 78711a628ad7e1c23cefcb9f9e345a0cc240c25b --base fe50945399a386b48678b1f2051fdbe8a77b10bd --rounds 75,76,77,78` | **0** |
| 2 | `git show 78711a628ad7e1c23cefcb9f9e345a0cc240c25b:.ufo/waves/round-77/c77_shonen_ledger.py \| sha256sum` | 0 |
| 3 | `git rev-list --all -- .ufo/waves/round-77/c77_shonen_ledger.py` + per-commit `git show <c>:<path> \| sha256sum` | 0 |
| 4 | committed blob → scratch, `python3 -B $S/recut/c77_committed.py --selftest --work $S/st-c77` | **0** (26/26) |
| 5 | `grep -c _run_command` on the committed blob | 1 (grep: no match; printed count **0**) |
| 6 | `python3 -B scripts/instrument_receipts.py --root . --revision 78711a62… --check` | **1** |
| 7 | `python3 -B .ufo/waves/round-78/c78_shonen_population.py --selftest --work $S/st-pop` | **0** (9/9) |
| 8 | `python3 -B .ufo/waves/round-78/c78_sweep_truth.py --selftest` (on committed blob e49bb0f1 and on worktree 301921e2, digest checked before/after) | **0** (6/6 both) |
| 9 | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` | 0 |
| 10 | `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and `… status --porcelain -uall \| grep -iE 'kake\|round[-_ ]?78\|r78'` | 0 / **1** (no match) |
| 11 | `git merge-base --is-ancestor abfbfaac58bcee2514490940d1b16365027a07c9 HEAD` | 0 |
| 12 | `sha256sum` / `stat` on the five instrument paths | 0 |

No substitutions were needed: every flag the seat named (`--root`, `--revision`, `--base`, `--rounds`) exists in
`scripts/doc_quote_truth.py:1086-1092`; it also offers `--json`, `--selftest`, `--work`. The tool reads committed
bytes only, so the measured revision is the lane HEAD commit `78711a628ad7e1c23cefcb9f9e345a0cc240c25b` (full hash
in the receipt header). No tool was installed or upgraded; no network; no git/jj mutation.

## 1. Round-level quote-truth receipt (routed defect 5)

`.ufo/waves/round-78/controls/doc-quote-truth-r78.txt` — 1,094 B, sha256
`44fbcfe5dafd7def88492aebda9bc7c70b123b200d4febd276986cc56fdee7c2` (full stdout embedded verbatim; `diff` against
the captured stream: identical, rc 0). Header names revision `78711a628ad7e1c23cefcb9f9e345a0cc240c25b`, base
`fe509453…`, rounds `75,76,77,78`.

```
C1v2 revision=78711a62 rows=60 receipt_files=8453 spans=97 exempted=0 corrections=8 findings=0 met=true
  missing corpus/lessons/round-78.md
```

**Findings: none** (so no file:line list; nothing was fixed). The trailing line is the tool's diagnostic, not a
finding: `corpus/lessons/round-78.md` does not exist at this revision and no Round 78 claim rows are committed
(SCORECARD's last section is Round 77), so the round-78 share of the population is zero. **This receipt is a green
baseline, not the round's final yardstick** — it must be re-cut at the round's final revision once the ledger
populations, the lesson and the PROVINCE/README blocks are committed, or it proves nothing about the round's own
claims.

## 2. SentinelC F1 receipt re-cut (routed defect 4)

Committed counter digest, re-derived from git objects:

```
counter_sha256=2d66e5af30b90f50875ac820879430b55f0c344e3c4965b6bcc203a3567a4396 revision=78711a628ad7e1c23cefcb9f9e345a0cc240c25b
```

(bytes 48,343; identical at the round-77 carrier `3db64e09…` and the base `fe509453…`). Written to
`.ufo/waves/round-78/w1/ExecReceipts/sentinel-f1-recut.txt` (1,798 B, sha256
`5465a948f99b2acdc90cfe8856ba1d6fc8705347b53d9de0ff8805993f1fc12d`).

Two blobs of that path exist in the whole history — `7f35ad45abcd…` (commits `b1754c20`, `893b0f33`, `1fb696e2`)
and `2d66e5af30b9…` (commits `3db64e09`, `6f3518d3`, `fecf2b62`). Hash claims that **never committed**:

| claimed digest | claimed bytes | where claimed |
|---|---|---|
| `00cb4fb2dccc01268a21666ff58d94c636ff49313870c52d798a1bb74c63bd50` | 48,225 | `round-77/w1/SentinelC.md:22,26,33,56,62,354`; echoed in `round-77/w1-results.json:88` |
| `a9eef8bd278bfe436b1862d23882adb605b013251d53e898002f89733ebf047c` | — | `SentinelC.md:33`; `round-77/w1/CriticC.md:15` (intermediate v1) |
| `9612baac…` (8-hex prefix only) | — | `SentinelC.md:26,33,55` (intermediate; no committed digest begins with it) |

What transfers: the committed blob is still clean on F1's terms — `_run_command` occurrences **0**, and the blob
copied to scratch passes `selftest: 26/26 passed`, exit 0. So the defect is purely the citation (48,225 B vs the
committed 48,343 B), exactly as the routed defect says. `round-78/w1/MutC.md` did not exist at measurement time;
`round-77/w1/MutC.md:22` already records the correct scored digest `2d66e5af…`/48,343, so the correction belongs to
SentinelC's closing claim, not MutC's.

## 3. Inherited-state audit

Full verbatim snapshots are in `.ufo/waves/round-78/w1/ExecReceipts/state-audit.txt` (3,296 B, sha256
`2ec8aa91c14747e087c5a20a24560987ac4701c8a32c511de517a58db0120726`).

- Lane (`git -C …/kake-shokunin status --porcelain`, 23:41:03): `M c78_sweep_truth.py`, `M shonen-ledger.json`,
  plus untracked `contract-amendment-1.md`, `controls/base-instrument-receipts.txt`, `controls/doc-quote-truth-r78.txt`,
  `w1.ready`, `w1.ready.dispatched`, `w1/` — **all belong to this lane's round 78**.
- Fleet root (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, no pathspec): `M .scratch/goal-20261103-hyaku-run15.md`,
  `M .scratch/run15-state.json`, `?? .scratch/run13-state.json`, `?? .scratch/run15-kernel.py`, `?? after`.
- Untracked paths under the fleet root that name kake or round 78: **none** (filtered `-uall` grep rc=1). The three
  untracked entries are orchestrator run state (`{`, `# run-15 orchestrator helpers…`) and a 24-byte stray dump
  (`== SCORECARD diff base-`); none belongs to this lane's round. Nothing was moved or deleted — the misroot sweep
  is the L1's.
- `kake-shokunin` is ignored at the fleet root (the fleet root's `.gitignore` line 1 is `*-shokunin/`), so lane-local untracked files can
  never appear in the fleet snapshot; both commands are required and both are recorded.
- Sibling seats were editing during this audit (`c78_sweep_truth.py`, `freshness-pins.json`, `freshness-sidecar.json`,
  `shonen-ledger.json`; `w1/` gained `L1Sources/`, `ReviewC23/`, `ConnectorC/`, `ExecC1Population/`, `ExecC3Matrix/`,
  `ScoutCites/`). Recorded, not touched.

## 4. Instrument binding

`.ufo/waves/round-78/w1/ExecReceipts/instruments.txt` (2,655 B, sha256
`7cae64abc9081a0530f8b4f1058fd23101008a7f2a2cd0eca1abee851564bfcc`); close-time observation in
`instruments-close.txt` (863 B, sha256 `471dfccc3b5f6710d02dab1fd54e5cc1d3bc8dc53976db3ae2c4e69b23fff4a8`).

| path | measured sha256 | bytes | selftest mode | state |
|---|---|---|---|---|
| `.ufo/waves/round-78/c78_shonen_population.py` | `c2dc1cbf6cc1e860c87f77903b6ea865edbdc781b40ca537575eab958cde6673` | 11,827 | `--selftest --work <dir>` | committed at `78711a62`, identical; 9/9, exit 0 |
| `.ufo/waves/round-78/c78_sweep_truth.py` | `301921e2…` (23:41:15) → `46acb450…` (23:42:26) | 8,219 (at `301921e2`) | `--selftest` (no `--work`) | committed blob `e49bb0f1…`, 7,103 B; worktree **moved twice** while this seat ran (C2 seat); 6/6, exit 0 on both builds I ran |
| `.ufo/waves/round-78/c78_meta_robots_matrix.py` | ABSENT | — | contract: `--selftest` + `--work` | absent at `78711a62` and at measurement |
| `scripts/meta_robots_audit.py` | ABSENT | — | contract: `--selftest` ≥ 40 cases | absent at `78711a62` and at measurement |

Both present counters carry a real static `--selftest` registration (`add_argument("--selftest")` at
`c78_shonen_population.py:261`, `c78_sweep_truth.py:159`), so `instrument_receipts` would derive
`selftest_mode=true` if either entered the population. Round-78 amendment 1 (`contract-amendment-1.md`, untracked,
23:40) corrects the C3 *grammar* without changing the C3 predicate, so the C3 rows must be re-derived after the tool,
cases, consts and matrix are committed.

`instrument_receipts.py --check` at `78711a62` — stdout + exit in
`.ufo/waves/round-78/w1/ExecReceipts/instrument-receipts-check.txt` (2,528 B, sha256
`f4a28bf42467c980b1fcc606253a79c920ed2c96e308667e02f85c58826033a4`):

```
C2v1 revision=78711a628ad7e1c23cefcb9f9e345a0cc240c25b population=20 bound=18 mismatches=2 met=false
  finding: missing scripts/doc_quote_truth.py: receipt has no entry for this path
  finding: missing scripts/hreflang_audit.py: receipt has no entry for this path
EXIT=1
```

**Rows the receipt must gain (not edited here; `corpus/knowledge/instrument-receipts.json` is the L1's call):**

- `scripts/doc_quote_truth.py` — sha256 `e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae`, 49,077 B, `selftest_mode=true` (`add_argument` at `:1091`; the `:1055` subprocess argv list correctly does not register).
- `scripts/hreflang_audit.py` — sha256 `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`, 59,734 B, `selftest_mode=true` (`add_argument` at `:1543`).

A `--write --date 2026-11-03` at the final revision re-derives every row from committed bytes and is cheaper and
safer than hand-editing two rows. `declared_match=false` is expected (the receipt declares `abfbfaac…`, an ancestor:
`merge-base --is-ancestor` rc 0); the two mismatches are the missing entries. **No round-78 instrument is in the
derived population at this revision** — SKILL.md's last registry section is Round 76, so `c78_*.py` and
`scripts/meta_robots_audit.py` are invisible to the population rule. If the L1 appends a `### Round 78 gate registry
additions` section naming them, those paths enter the population and need receipt rows at the same time.

## Risks and carries (all L1-facing; none blocks this seat)

1. **The quote-truth receipt is revision-bound to the freeze commit.** It is green for rounds 75–77 only; re-cut it
   after the final commit (`--rounds 75,76,77,78`), otherwise the round's own rows are unmeasured.
2. **The instrument-receipt gate was red before the round and stays red** (`base-instrument-receipts.txt` shows the
   same `population=20 bound=18 mismatches=2` at `fe509453`). Round 78 must add the two missing round-76 rows if it
   wants this gate green; the round's own instruments cannot bind until they are committed.
3. **The worktree is moving under measurement** (`c78_sweep_truth.py` twice in one minute; `freshness-pins.json`,
   `freshness-sidecar.json`, `shonen-ledger.json` edited). Every binding row above names its instant; the L1 must
   re-derive from committed bytes, not from these worktree digests.
4. The SentinelC correction is citation-only: the committed `c77_shonen_ledger.py` already satisfies F1's substance
   (no `_run_command`, 26/26). Do not treat the re-cut as a re-opening of F1.
5. C3 was unevaluable for this seat (both paths absent); no C3 claim is made or implied here.

**Scratch:** `S=/fast/scratch/hyaku/kake-r78/ExecReceipts` (with `TMPDIR=$S/tmp`), used for the re-cut copy and all
`--work` dirs; receipts were copied into this wave directory first, then the tree was removed and verified absent.
