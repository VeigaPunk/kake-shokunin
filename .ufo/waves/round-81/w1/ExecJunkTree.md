# ExecJunkTree — R80-5 junk-control re-run (kake round 81, wave w1)

**Verdict: R80-5's condition closes — the frozen builder is deterministic, round-80's own counter re-runs over the rebuilt tree to `open=5 closed=1 met=false` exit 1, the builder's path guards hold, and the tree is bound to its predicate. After-receipt committed at `.ufo/waves/round-81/controls/after-r80-5-junk-rerun.txt`.**

Frozen condition re-tested (contract §C1, item R80-5): `junk_tree_build.py` rebuilds the junk tree from `junk-tree.json` deterministically (two runs, identical file set and digests), and `.ufo/waves/round-80/c80_defect_queue.py` over the rebuilt tree prints `open=5 closed=1 met=false`, exit 1.

## 1. Determinism — PASS

Two runs of `python3 -B .ufo/waves/round-81/junk_tree_build.py --spec .ufo/waves/round-81/junk-tree.json --out <scratch>/build-{a,b}`: both exit 0, both print `wrote 1 files to ...`. `diff -r build-a build-b` silent, rc=0. Sole file `corpus/lessons/round-80.md`, sha256 `f32ae6a609f182c13c9cc813f5e4a1f94afcc76838ec596f7855dc8ed71b0693` in both; aggregate digests of the sorted (path, sha256) listings identical: `c2cc56360ae367312eccee6221866482dbd3d6654f66226d1ae1270083f0c049`. Receipt: `.ufo/waves/round-81/w1/ExecJunkTree/determinism.txt`.

## 2. Round-80 counter over the rebuilt tree — PASS (required shape reproduced)

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/c80_defect_queue.py --root <scratch>/build-a --work <scratch>/work-c80` → stdout:

```
R79-1 open no S453 row in corpus/SOURCES.md
R79-2 open scripts/ledger_append_guard.py absent
R79-3 open receipt c80-selftest.txt lacks a `selftest: N/N passed` line or `exit=0`
R79-4 open .ufo/waves/round-80/c80_ledger_fixtures.py absent
R79-5 closed withdrawal recorded; no self-assessment file repeats the sentence
R79-8 open round-79 results unreadable: Expecting value: line 1 column 1 (char 0)
C1v1 revision=worktree items=6 open=5 closed=1 exported=0 met=false
exit=1
```

exit=1. Exactly the required `open=5 closed=1 met=false` + exit 1. Recorded verbatim as `$`-echo + stdout + `exit=1` at `.ufo/waves/round-81/controls/after-r80-5-junk-rerun.txt` (the R80-5 receipt; sha256 `306c63fe4ce1b2461c251b759920ae7c72dd730896a9474481db1d8dd386ccac`, identical bytes copied to `w1/ExecJunkTree/c80-over-rebuild.txt`).

Line-for-line comparison with the committed round-80 receipt `.ufo/waves/round-80/controls/ctl-c80-junk-queue.txt` (full labeled diff: `w1/ExecJunkTree/receipt-comparison.txt`):

- **Agree exactly:** R79-2, R79-4, R79-5, R79-8 item lines; the summary line `C1v1 revision=worktree items=6 open=5 closed=1 exported=0 met=false`; the counter's own trailing `exit=1`.
- **Cannot agree (stated, with cause):** (a) the command echo — the old run names the deleted `/fast/scratch/hyaku/kake-r80/l1/junk` and carries a comment; (b) R79-1's *reason* — the old scratch tree held a decoy S453 row citing RFC 9109, while the committed `junk-tree.json` deliberately supplies no SOURCES.md ("supplies nothing else"), so the same `open` verdict reads `no S453 row in corpus/SOURCES.md`; (c) R79-3's *reason* — the rebuilt tree fails one conjunct earlier (missing `c80-selftest.txt` receipt vs missing tool file); verdict `open` either way; (d) the receipt's final `exit=1` line is a recorder-appended trailer, re-added as the trailer of the after-receipt. All six verdicts and the aggregate state are identical.

## 3. Builder negative controls — PASS

- Spec `{"files": {"../escape.md": ...}}` → exit 2, stderr `unsafe path: ../escape.md`, stdout empty; `--out` dir never created; `find` sweep over the whole scratch tree found no `escape.md`. Receipt: `w1/ExecJunkTree/neg-escape.txt`.
- Spec `{"files": {"/fast/scratch/hyaku/kake-r81/ExecJunkTree/abs-escape.md": ...}}` (absolute path) → exit 2, stderr `unsafe path: /fast/.../abs-escape.md`, stdout empty; target file absent. Receipt: `w1/ExecJunkTree/neg-abs-path.txt`.

Nothing was written inside or outside `--out` in either run.

## 4. Predicate-binding control — PASS

Extended spec (derived from the committed `junk-tree.json`) adding exactly the S453 closure apparatus: a valid 11-cell S453 row in `corpus/SOURCES.md` (`RFC 9110 dates - https://example.test/rfc9110.txt`, kind `spec`, tier `A`, status `mined`, used-by `corpus/knowledge/x.md`), a `corpus/knowledge/x.md` citing S453, and an `R79-1 erratum` line in the lesson (the R79-5 withdrawal line retained). Builder exit 0 (`wrote 3 files`); round-80 counter over it:

```
R79-1 closed S453 = RFC 9110 row present, used-by resolves (corpus/knowledge/x.md), row shape ok, erratum recorded
...
C1v1 revision=worktree items=6 open=4 closed=2 exported=0 met=false
exit=1
```

exit=1 — exactly one item flips. The junk tree is bound to the predicate, not to a word. Receipt: `w1/ExecJunkTree/ctl-overbuilt.txt` (sha256 `a2f940db710213700f9a313c7ff917e39af6c9bad56622bd8b9f9eddad85cc8b`).

## Instruments

Builder, spec, and both counters were tested read-only; **no defects found** in any of them. The two reason-string deltas in §2 are inherent to reconstructing the tree from committed bytes + predicates instead of the uncommitted round-80 scratch tree (the spec's `_note` documents exactly this), and do not touch any verdict.

## Notes for the L1

- `c81_defect_queue.py` re-derives R80-5 itself (its `p_r80_5` runs the builder twice and re-runs `c80_defect_queue.py`; grep finds no reference to `after-r80-5-junk-rerun.txt` in the C1 counter), so this seat's after-receipt is the evidence artifact; the binding check remains machine-decided at measurement.
- Receipt digests: determinism `a71adebf…`, receipt-comparison `0cf7a538…`, neg-escape `d236c0a0…`, neg-abs-path `bb66cd72…`, ctl-overbuilt `a2f940db…`, after-r80-5 / c80-over-rebuild `306c63fe…`.
- No tools installed or upgraded. No network use. No subagents spawned (labrat allowance unused — nothing to probe). Scratch tree `/fast/scratch/hyaku/kake-r81/ExecJunkTree` deleted before yield (`test ! -e` rc=0). No blockers.
