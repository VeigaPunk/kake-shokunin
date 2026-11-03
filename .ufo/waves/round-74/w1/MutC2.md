# MutC2 — mutation check of the C2 counter and repair tool

Round 74, wave w1, seat `MutC2` (mutation-tester, leaf). Measured revision for the frozen fixture:
`ced2878a1e77f57afb4ee3baebf1021e5130399b`; freeze commit `b35dd4d7`. The lane checkout was read-only
throughout; every mutation is a patched copy under scratch.

**Artifacts measured**

| Artifact | Path | sha256 | size / mtime |
|---|---|---|---|
| Counter | `.ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py` | `62b3d9e8188ce88bfecd30dbd2076a5b3f3edb6396f6187023bb964c8b7df285` | 9010 B, 2026-11-03 20:16:10 |
| Tool | `.ufo/waves/round-74/w1/ExecC2Tool/sidecar_reobserve.py` | `1284bd17d0f0e8c41ac37d27598d8cc623e39ee89866b950ad5a5f1f4e8d0c28` | 11474 B, 2026-11-03 20:17:58 |

Both files were present when measured; no contract-described reconstruction was used for the verdicts.
`bin/counter_ref.py` and `bin/tool_real.py` in the receipts are byte-identical copies of the two files
(same sha256); every mutant is a copy with one rule removed or inverted. The pristine copies passed every
detector, so no verdict is inconclusive.

Receipts: `.ufo/waves/round-74/w1/MutC2-assets/` — `counter_matrix.json`, `tool_matrix.json`,
`integration.json`, `mutations.diff`, `base-control-vs-counter.diff`, `stat-probe.txt`,
`delivered-hashes.txt`, `base-run.txt`.

## Question

Can the counter's `--selftest` and the frozen fixtures kill a detector missing one rule?

**Short answer.** All seven counter mutants and all three tool mutants were killed, but not by the two
frozen instruments alone:

- the counter's `--selftest` kills M1–M6 and misses **M7** (working tree instead of revision bytes);
- the frozen base receipt kills only **M3** and **M6**;
- **M1, M2, M4, M5, M7** reproduce the frozen base receipt exactly and survive it;
- the tool has no frozen receipt at all; its `--selftest` kills M8–M9 and misses **M10**
  (non-deterministic write);
- M7 and M10 are killed only by constructed fixtures. Those two gaps are routed as defects below.

## Method and detectors

Mutations are single-rule edits applied by exact string replacement; `mutations.diff` carries the full
unified diffs. Fixtures were built in one `git clone --shared --no-checkout` of the lane plus sparse
checkout of `corpus/`, so the counter's hardcoded `BASE_REVISION` resolves; `git rev-parse --show-toplevel`
inside the clone printed the clone root before the first commit. One commit per fixture case; the working
tree was synchronised to the committed revision for f1–f6/f8 and deliberately diverged for f7.

Detectors, run on every variant:

1. **D1 — counter selftest**: `python3 -B <counter> --selftest`; killed if exit ≠ 0 or fewer than 6/6.
2. **D2 — frozen base receipt**: `python3 -B <counter> --root <lane> --revision ced2878a…`; killed if
   stdout differs from the frozen numeric line or exit ≠ 1.
3. **D3 — constructed fixtures** f1–f9 (below), run with `--json`; killed if any specified field/exit or
   `annotation_findings` differs.
4. **Tool cross-check**: the counter is run over a commit containing the tool's written sidecar; the tool
   output must be accepted (`met=true`, exit 0) when correct and rejected (`exit 2`,
   `restored_unevaluable=1`) when it claims `stat ok` for an unevaluable token.

Fixture definitions and the pristine counter's results (all matched the specification; this is the
baseline, not a failure):

| Fixture | Sidecar state | Pristine result |
|---|---|---|
| f1 | `kind=absent`, token present | `absent_present=1`, `contradictions=1`, met false, exit 1 |
| f2 | `kind=restored`, token absent | `restored_absent=1`, exit 1 |
| f3 | `kind=restored`, token under a `chmod 000` dir (EACCES) | `restored_unevaluable=1`, met false, exit 2 |
| f4 | `kind=restored`, token present, note contains `missing` | exit 0, `annotation_findings=[{index:0,issue:restored-note}]` |
| f5 | base identity `SKILL.md:512` (`kind=absent` at base) now `kind=restored`, token present, no history | exit 0, `annotation_findings=[{index:0,issue:prior-history}]` |
| f6 | `kind=restored`, token `~/present` resolvable only from `HOME`, not from `--root` | exit 0, `restored_present=1`, met true |
| f7 | committed bytes are a contradiction; working tree sidecar is empty | exit 1, `absent_present=1` (committed bytes win) |
| f8 | `kind=absent`, token is a dangling symlink | `absent_absent=1`, exit 0 |
| f9 | `kind=restored`, token is a symlink loop (ELOOP) | `restored_unevaluable=1`, exit 2 |

Stat probe (`stat-probe.txt`): dangling symlink → `os.stat` `absent(FileNotFoundError)`,
`os.path.exists` `False` (non-discriminative); symlink loop → `os.stat` `unevaluable(OSError errno=40)`,
`os.path.exists` `False` (discriminative); present file → both present/True.

## Counter mutants — results

| Mutant | Rule changed | D1 selftest | D2 frozen base | D3 fixtures | Verdict |
|---|---|---|---|---|---|
| M1 | `except OSError: return 'absent'` (was `unevaluable`) | **g3 FAIL**, 5/6, exit 1 | matches exactly (survives) | f3 `ra=1` exit 1; f9 `ra=1` exit 1 | **killed (D1, D3)** |
| M2 | `os.path.exists()` instead of `os.stat` try/except | **g3 FAIL**, 5/6, exit 1 | matches (survives) | f3 `ra=1` exit 1; f9 `ra=1` exit 1 | **killed (D1, D3)** |
| M3 | contradiction = `absent_absent + restored_absent` (inverted) | **g1 FAIL**, 5/6, exit 1 | **`contradictions=4`** vs 144 (mismatch) | f1 met true exit 0; f7 met true exit 0; f8 met false exit 1 | **killed (D1, D2, D3)** |
| M4 | restored-note absence vocabulary check dropped | **g4 FAIL**, 5/6, exit 1 | matches (survives) | f4 `annotation_findings=[]` (expected `restored-note`) | **killed (D1, D3)** |
| M5 | prior-history check dropped | **g5 FAIL**, 5/6, exit 1 | matches (survives) | f5 `annotation_findings=[]` (expected `prior-history`) | **killed (D1, D3)** |
| M6 | `~` expanded from `--root` instead of `HOME` | **g6 FAIL**, 5/6, exit 1 | **`ap=0 aa=148 rp=0 ra=26`** vs `ap=144 aa=4 rp=26 ra=0` | f1 met true exit 0; f6 `ra=1`; f7 met true; f9 `ra=1` | **killed (D1, D2, D3)** |
| M7 | sidecar read from working tree, not `<rev>:path` | **6/6 pass**, exit 0 (survives) | matches (survives; tree clean) | f5 `annotation_findings=[]`; f7 **`entries=0`, met true, exit 0** | **killed (D3 only)** |

Exact evidence samples:

```
M1/M2 selftest: g1 ok g2 ok g3 FAIL g4 ok g5 ok g6 ok / selftest 5/6 (exit 1)
M3  frozen:     …absent_present=144 absent_absent=4 … contradictions=4 met=false (exit 1)
M6  frozen:     …absent_present=0 absent_absent=148 … restored_absent=26 … contradictions=26 met=false
M7  selftest:   selftest 6/6 (exit 0); frozen byte-equal to the receipt
M7  f7 --json:  entries=0, met=true, exit=0  (committed fixture: absent_present=1, exit=1)
```

M3 is the strongest case: the inverted rule changes a count that the frozen receipt names, so the frozen
base alone kills it. M1/M2/M4/M5/M7 are invisible to the frozen base because the base corpus has no
non-ENOENT `OSError` among its 174 tokens, its 26 restored notes are absence-vocabulary-clean, there are
no flips at base, and the lane worktree equals the revision.

### Kill channel per detector (counter)

| Detector alone | Kills | Misses |
|---|---|---|
| D1 `--selftest` | M1, M2, M3, M4, M5, M6 | **M7** |
| D2 frozen base | M3, M6 | **M1, M2, M4, M5, M7** |
| D3 constructed f1–f9 | all seven | — |

Caveat on D3 for M4/M5: f4/f5 differ from the faithful run only in the JSON `annotation_findings` array;
the summary, `met` and exit stay `0/true` in both. A gate that grades only the exit code or the summary
line would let M4 and M5 through (see routed defect 2).

## Tool mutants — results

The delivered tool's selftest is 8 unittest cases (`sidecar_reobserve tests=8 failures=0 errors=0
passed=true`, exit 0). Fixtures tf1–tf10 were built on synthetic roots with valid `lineSha256` entries;
tf4 and tf5 are assertions folded into tf1 (exact history bytes, no absence vocabulary).

| Mutant | Rule changed | Tool selftest | Fixtures | Verdict |
|---|---|---|---|---|
| M8 | refusal on unevaluable removed; `unevaluable` added to the flip predicate | **FAIL 1/8** (`test_unevaluable_refuses_entire_write`: `(0,1) != (2,1)`) | tf3 exit 0, `flipped=1`, `wrote=true`, bytes changed (expected exit 2, unchanged) | **killed (selftest, tf3)** |
| M9 | prior observation not appended to `history` | **ERROR+FAIL** (`test_flip` `KeyError: 'history'`; `test_history_preservation` `[] != [{…}]`) | tf1 written entry has no `history` key | **killed (selftest, tf1)** |
| M10 | `datetime.now()` added to every new note (non-deterministic write) | **8/8 pass** (survives) | tf8: two identical roots produce **different bytes** | **killed (tf8 only)** |

Cross-check: M8's written sidecar (`kind=restored` for a `chmod 000` token, note claims `stat ok`) was
committed into the fixture clone and read by the pristine counter:
`restored_unevaluable=1`, `met=false`, **exit 2**. The counter rejects the mutant tool's output.

## Positive control (delivered bytes, real corpus)

The delivered tool was run on an unmodified copy of the base sidecar (`--write --date 2026-11-03
--host linux-x64`, `HOME=/home/vgpnk`):

- `flipped=144`; `absent_left=4`; `absent_left_present=0`; prior-note/history problems `0`; deterministic
  across two independent roots `true`; exit 0.
- The result was committed in the scratch clone (`4d18d166…`) and read by the delivered counter:
  `entries=174 absent=4 restored=170 absent_present=0 absent_absent=4 absent_unevaluable=0
  restored_present=170 restored_absent=0 restored_unevaluable=0 contradictions=0 met=true`,
  `annotation_findings=[]`, **exit 0**.

This exercises the whole after-state path (144 flips, history preservation, vocabulary, HOME expansion,
revision-bound read) and passes.

## Routed defects (survivors / coverage findings)

1. **Counter selftest never exercises `read_entries` (D1 misses M7).** M7 reads
   `corpus/knowledge/freshness-sidecar.json` from the working tree and passes 6/6; it also reproduces the
   frozen base receipt because the lane worktree equals the revision. A working-tree reader therefore
   survives both shipped instruments. Add a g7 fixture: a two-revision fixture repo (or a stubbed
   `git show`) where the working tree differs from `<rev>:path`; the committed bytes must win.
2. **Exit code / `met` ignores `annotation_findings` (D2 and the summary miss M4/M5).** C2 conjuncts 2
   (history bytes) and 3 (absence vocabulary) are checked only into the JSON array; a sidecar with a
   missing history or an absence word in a restored note still prints `met=true` and exits 0. The seat
   item freezes `met` to the stat formula, so this cannot be fixed inside the counter without an L1
   decision; the landing validator must assert `annotation_findings == []`, or the contract must fold
   those findings into `met`. The sweep binding catches vocabulary structurally but does not check
   history preservation.
3. **Tool selftest has no determinism fixture (D3 misses M10).** The delivered selftest passes 8/8 with a
   `datetime.now()` in the note; two identical `--write` runs produce different bytes. Add a fixture that
   writes two identical copies and compares bytes, plus a second-run idempotence check.
4. **Frozen receipt format is not reproduced exactly.** `controls/base-c2-sidecar.txt` is 14 lines
   (divided summary, six `sample` tuples, three `absent_token` lines); the delivered counter emits one
   line. The numeric conjunction matches exactly, but the contract's "MUST reproduce … exactly" clause
   cannot pass byte-for-byte (`base-control-vs-counter.diff`). Either the control must be the one-line
   summary or the counter must print the sample/genuinely-absent block; L1 owns that choice.
5. **Prior-history lookup is keyed on `(file, line, token)`.** If a flip re-pins the cited line (the
   round-64 re-pin map shows line numbers moving), `prior.get(identity)` misses, the loop `continue`s,
   and history preservation is silently unenforced for that entry. The tool as delivered does not move
   lines, but the check is fragile against any future re-pin.
6. **Frozen-receipt kill surface is narrower than it appears.** Because the base corpus has no
   EACCES/ELOOP token, no vocabulary-matching restored note, no flipped entry and a clean worktree,
   M1/M2/M4/M5/M7 all reproduce it. The receipt pins the `144/4/26` stat contradiction, not the
   unevaluable, vocabulary, history or revision-binding rules.
7. **The "broken-symlink class" in the seat wording is only half-discriminative.** A dangling symlink is
   `absent` under both `os.stat` and `os.path.exists` (f8 passes for M2). The discriminating members of
   that family are ELOOP (f9) and EACCES (f3); both kill M2.
8. **Minor robustness/observations.** (a) `measure()` always reads the hardcoded `BASE_REVISION`; in a
   shallow or unrelated clone that commit is absent, so every run — including `--check`-equivalent base
   runs — returns exit 2 `Unevaluable`. (b) The tool's `--check` exits 0 with pending flips (its
   docstring: "exit 0: observation completed"); a gate that wants a pending signal must read
   `absent_present` from `--json`. Neither breaks the frozen predicate as written.

## Restoration and cleanup

- No lane file was written, created or deleted; no git/jj mutation was run in the lane. The only commits
  were in the scratch `--shared` clone, with an explicit fixture identity and a toplevel assertion.
- Delivered-byte hashes were identical before and after the probe (see `delivered-hashes.txt`).
- Scratch tree `/fast/scratch/hyaku/kake-r74/MutC2/` (clone, fixture homes, mutant copies) was copied
  into `MutC2-assets/` and then deleted (`chmod -R u+rwX` first, then `rm -rf`, exit 0; the path is
  gone). No tool installs or upgrades were made.
