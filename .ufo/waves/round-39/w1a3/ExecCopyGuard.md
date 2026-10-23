# ExecCopyGuard — R39 W1 A3: copy guard for the future build

Deliverable: `/fast/scratch/hyaku/kake-r39a3w1/ExecCopyGuard/copy_guard.py` — 355 lines, 13148 B,
stdlib only, py3.14.

## What it does
`copy_guard.py --candidate <py> --against <file|dir|glob>...` normalises each file (ast parse; drop
module/class/function docstrings; rename every identifier to `vN` by first use in source order —
`copy_guard.py:140`; `ast.unparse`; tokenise, dropping layout/comment tokens and unquoting strings —
`copy_guard.py:184`), then prints per pair the difflib ratio, the longest common contiguous
normalised token run and the matched-token count. Exit 0 clean, 1 hit, 2 could-not-evaluate; a hit is
`ratio>=0.60 (default) AND matched>=40`, or `run>=200` (`copy_guard.py:282-285`). `--ratio`, `--run`,
`--min-matched`, `--json` are overridable; `--help` exits 0.

## Commands and exit codes (all executed; cwd = the sandbox dir above)
| command | exit |
|---|---|
| `python3 copy_guard.py --candidate fx/orig.py --against fx/renamed.py` | **1** (ratio 0.9945, run 178, matched 180) |
| `python3 copy_guard.py --candidate fx/indep_a.py --against fx/indep_b.py` | **0** (ratio 0.3378, run 8, matched 50) |
| `python3 copy_guard.py --candidate fx/indep_b.py --against fx/indep_a.py fx/orig.py fx/renamed.py` | **0** (max 0.3446) |
| `python3 copy_guard.py --candidate fx/mutant_findings.py --against .../a3-controls/dead-w1/` | **1** vs `CtlConstFindings.py`: 1.0000 / run 237 / 237 matched; next best 0.3257 |
| `python3 copy_guard.py --candidate fx/mutant_xsd.py --against .../a3-controls/dead-w1/` | **1** vs `CtlXsdDelegate.py`: 0.9976 / run 1528 / 2451 matched; next best 0.2786 |
| `python3 copy_guard.py --candidate fx/indep_a.py --against .../a3-controls/dead-w1/` | **0** (0/12 pairs, max 0.1317) |
| `python3 copy_guard.py --candidate copy_guard.py --against .../a3-controls/dead-w1/` | **0** (0/12, max 0.1309) — the guard is not derived from a control |
| `python3 fx/pairwise.py .../a3-controls/dead-w1/` | **0** — 12 files, 66 pairs, max ratio 0.4408 (`CtlConstError :: CtlNoReader`), max run 26 |
| timed `mutant_xsd` vs the 12 controls (~16k corpus tokens) | exit 1, 464 ms wall |
| error paths: syntax error, missing candidate, empty glob, undecodable bytes | **2** each, message on stderr (no traceback) |
| degenerate: empty/empty, docstring/docstring, `x = 1`/`y = 2` | **0** each + `floor` note; pre-floor they scored 1.0, 1.0, 0.6667 — three false hits |

Fixtures: `orig.py` + `renamed.py` (same logic, every identifier renamed, comments rewritten,
statements re-wrapped); `indep_a.py`/`indep_b.py` (edit distance — full DP matrix vs two rolling
rows); `mutate.py` (independent token-level relabeller: reverse first-use numbering, comment bodies
replaced, builtins/keywords protected — it does **not** use copy_guard's normaliser, so the two
control hits are not an artefact of the guard's own mapping); `pairwise.py` (corpus baseline sweep).

```
0e1b9d2c0d1f7abb030ae97db9b719efe1f26e78fb7005441519ed94e6bf21b1 copy_guard.py   1a6a3ca9276e6558d4fd16be1b115f6651cf8e2195e7945684bbd96dc91d27cc fx/orig.py   2a43c59197e1e39e993adc5d9e99b06795b2f17400cc07d79300a6fdacc7874f fx/renamed.py
592d32f65ceec5a2b985e066240593028048ad49b523487bffc440bd84ffa7c5 fx/indep_a.py  cbade4da1d2c4a297c2724764ea47b7593431aa079077d16620695528f031b18 fx/indep_b.py  21671a7d748e0665f55760f7f98c63875613a8d67edde2669136439a98462e11 fx/mutate.py
075b683b7c7d3bf7ae3abe1d5fa6a8c9a88a3d60674827fa27ae2495397fe0b9 fx/pairwise.py  b127c85cc9855fc61cc9a09168314f1cc1cd717f1f7a7ba2dbe9be12cfcfc101 fx/mutant_findings.py  c2517b7eec3a080570a74c42010b606eddb5c6a9da5ce6679205d2da649b7315 fx/mutant_xsd.py
```

## Findings
- `copy_guard.py:282` (floor added after test): difflib ratios are meaningless on tiny inputs —
  `x = 1` vs `y = 2` scored 0.6667 and two empty files 1.0000, i.e. both were HITs before the floor.
  `--min-matched 40` demotes them to notes; any consumer computing its own ratio must repeat it.
- `pairwise.py` baseline: unrelated controls peak at ratio 0.4408 / run 26, so the 0.60 and 200
  thresholds sit 0.159 away from the corpus's own idiom overlap; a build at ≥0.60 is outside it.
- Relabelled controls are caught at 1.0000 and 0.9976, so renaming, comment and docstring changes do
  not hide a copy — but a *semantic* reimplementation sharing no token sequence is invisible by
  construction: this complements, never replaces, the behavioural diff against the controls.
- `mutant_xsd.py` scored 0.9976 not 1.0 (2451/2457 matched): relabelling a name that collides with a
  protected builtin (`id`, `type`, `next`, `bytes`, `input`) shifts the mutant's numbering; run rule fired at 1528.
- `copy_guard.py:188`: reading via `tokenize.open` honours PEP 263 cookies (latin-1 + coding line
  exits 0); undecodable bytes exit 2 instead of comparing mojibake.

## Risks / blockers
- No blocker; no network, no installs, no lane writes (control corpus listed/read only). Sandbox 120 KB.
- Threshold is policy, not proof: a legitimate build reusing a control's schema and flow vocabulary
  could approach 0.60 — raise `--ratio` (e.g. 0.75) for a stricter gate or read the per-pair table
  rather than the exit code alone. Python only; non-Python and unparsable inputs exit 2 by design.
