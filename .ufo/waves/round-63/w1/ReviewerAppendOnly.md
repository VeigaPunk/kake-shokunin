# ReviewerAppendOnly — round-63 w1: append-only discipline verification

Seat: leaf reviewer. Scope: append-only discipline of the two corpus files edited
between base `13d4519818db28cd0aa912e49020659140d7b9fa` and measured revision
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, verified with the lane's own tool
`scripts/append_guard.py` plus independent cross-checks. No installs performed;
no subagent dispatch; no git/jj mutation anywhere; fixture battery ran in a
throwaway repo under `/fast/scratch/hyaku/kake-r63/ReviewerAppendOnly/` and was
deleted after use.

## Verdict

**Append-only discipline: VERIFIED (no violation found).** Both edited corpus
files are byte-level pure appends at EOF; the lane guard reports green and is
independently shown to bite on real bytes. One tool-coverage finding (scope gap
for `corpus/QUALITY.md`, F-1) — closed by an extended-scope rerun and manual
proof; it does not change the verdict for this round's edits.

## 1. Frozen counting command — output (verbatim)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin   # script path is lane-relative; --root is absolute
$ python3 -B scripts/append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --base 13d4519818db28cd0aa912e49020659140d7b9fa --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
files=58 findings=0
exit=0
```

Note: the literal command `python3 -B scripts/append_guard.py …` resolves only
from the lane root — `/home/vgpnk/Projects/shokunin/scripts/` exists at the
fleet root but contains no `append_guard.py`. Running it with `cwd` = lane root
and the absolute `--root` is the faithful realization of the seat command.

## 2. What the guard actually checked

- `git diff --name-status 13d4519..05b0d7f` shows exactly two modified corpus
  files: `M corpus/QUALITY.md` (+4/−0) and
  `M corpus/knowledge/response-header-expectations.md` (+29/−0); 19 paths added
  (`.ufo/waves/round-63/**`, `corpus/lessons/round-63.md`,
  `scripts/quote_class.py`, `scripts/fixtures/quote-class/**`); nothing else
  touched.
- Default scope `corpus/knowledge/**/*.md` matches exactly 58 regular blobs at
  base (`git ls-tree -r 13d4519 --name-only | grep -c '^corpus/knowledge/.*\.md$'`
  → 58 of 19,324 paths), so `files=58` covers every pre-existing knowledge file.
  Only `corpus/knowledge/response-header-expectations.md` changed among them;
  a rewrite of any of the 58 would have produced a finding (tool proven to
  bite, §4). Guard semantics enumerate base-tree paths only (new files are
  unchecked by design — selftest K11), which is why the new
  `corpus/lessons/round-63.md` is not in scope.

## 3. Findings

### F-1 (Medium, tool coverage — does not affect this round's verdict): default scope is blind to `corpus/QUALITY.md`

`scripts/append_guard.py:DEFAULT_SCOPE = ["corpus/knowledge/**/*.md"]`
(`scripts/append_guard.py:17`) does not match `corpus/QUALITY.md`, yet the seat
item says "on the two edited corpus files" and the contract's no-harm clause
("Append-only edits to existing files") includes QUALITY.md's round-63 criteria
block. Empirical proof of blindness (fixture battery, §4, T6): an untagged
mid-file insertion into `corpus/QUALITY.md` passes default scope with
`files=1 findings=0` exit 0.

Closure performed here (reviewer-side, no repo edits):

- Extended-scope rerun on the real revisions, run from lane root:
  `python3 -B scripts/append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --base 13d4519818db28cd0aa912e49020659140d7b9fa --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f --scope 'corpus/knowledge/**/*.md' --scope 'corpus/QUALITY.md'`
  → `files=59 findings=0`, `exit=0` (58 knowledge blobs + `corpus/QUALITY.md`;
  fixture-equivalent T2 printed `files=2 findings=0` for the two-file fixture).
- Byte-prefix proof, independent of the tool: `git cat-file blob
  05b0d7f:corpus/QUALITY.md | cmp - <(base blob)` reports
  `EOF on <base> after byte 126927` (cmp exit 1, zero differing bytes) — the
  revision blob is a strict byte-extension of the base blob. Same for the
  knowledge file: `EOF on <base> after byte 13782`.
- Diff shape: `corpus/QUALITY.md` hunk `@@ -1410,3 +1410,7 @@` — one EOF hunk,
  4 added lines (`## Round-63 criteria` + blank + criterion bullet), 0
  deletions. `response-header-expectations.md` hunk `@@ -219,3 +219,32 @@` —
  one EOF hunk, 29 added lines, 0 deletions; the committed round-62 correction
  paragraph appears as unchanged context directly above the new block
  (no-harm: "round-62 held correction preserved verbatim" holds).
- Tagging reading: both runs are EOF appends, which the guard's own semantics
  admit without a `[rN-correction]` tag (selftest K1; `first_untagged_run`
  skips runs after the last matched base line). The knowledge-file block
  carries a visible `[r63-correction 2026-10-27]` tag on the second line of the
  appended run (plain text, not inside a code span or HTML comment); the
  QUALITY.md criteria bullet carries no tag, mirroring the committed round-62
  criteria block's shape.

### F-2 (Info): the guard tool itself is not sha-frozen in the round-63 contract

The contract freezes `c63_calibration.py`, `c63_quote_tool.py`,
`scripts/quote_class.py` and `quote-classes.json`; `append_guard.py` is only
named in the seat item. Identity pinned by this seat: worktree sha256
`141b7cac57a7ec8373f69d0f430b65a3239ab1afd02ddc1bbb73ff3e24040827`; git blob
oid `e9657e23120316828ed0b00be7c3669e55ac2581` identical at base, at revision,
and in the worktree (`git rev-parse 13d4519:scripts/append_guard.py
05b0d7f:scripts/append_guard.py` + `git hash-object`), and
`git status --porcelain scripts/append_guard.py` is clean. So the tool that
printed the verdict is byte-identical at base and measured revision — no
mid-wave tool mutation.

## 4. Tool-soundness battery (anti-false-green, on the real base bytes)

Round-62's routed defect was a false-green counter family, so the guard itself
was attacked before trusting `findings=0`. Fixture: throwaway repo
`/fast/scratch/hyaku/kake-r63/ReviewerAppendOnly/gf`, `git init -q`, toplevel
asserted equal to the dir, base = the two real base blobs, commits with
throwaway identity `r63-scratch <r63-scratch@invalid>` only; deleted after.

| T | Mutation (from real blobs) | Scope | Output | exit |
|---|---|---|---|---|
| T1 | real revision blobs | default | `files=1 findings=0` | 0 |
| T2 | real revision blobs | + `corpus/QUALITY.md` | `files=2 findings=0` | 0 |
| T3 | 1-byte in-place flip, untagged (knowledge) | extended | `changed corpus/knowledge/response-header-expectations.md` `files=2 findings=1` | 1 |
| T4 | untagged mid-file insertion (knowledge) | extended | `untagged_insertion corpus/knowledge/response-header-expectations.md:10` | 1 |
| T5 | untagged mid-file insertion (QUALITY.md) | extended | `untagged_insertion corpus/QUALITY.md:3` | 1 |
| T6 | same as T5 | default | `files=1 findings=0` (blind — F-1) | 0 |

Selftest: `python3 -B scripts/append_guard.py --selftest` →
`append_guard selftest: 54/54`, exit 0.

Interpretation of the frozen command's `files=58 findings=0`: every
pre-existing knowledge file, including the one edited, satisfies the
append-only predicate at the measured pair; the predicate is demonstrably able
to fail (T3/T4/T5, selftest K3–K14), so the green is not vacuous.

## 5. Residual risk / verification gaps

- New files (`corpus/lessons/round-63.md`, `.ufo/waves/round-63/**`,
  `scripts/**`) are outside append-only discipline by design (guard checks
  base-tree paths only, K11); nothing here attests their content.
- `append_guard.py` is not sha-frozen by the round-63 contract (F-2); future
  rounds relying on its verdicts should freeze it or re-pin identity as done
  here.
- Default-scope blindness to `corpus/QUALITY.md` (F-1) remains in the tool;
  any later seat citing `files=N findings=0` as covering QUALITY.md without
  `--scope` extension is over-claiming.
- Verification bounds: base/revision assumed to be the contract's measured
  pair (both resolve; base is ancestor of revision — checked via
  `git merge-base --is-ancestor`, exit 0).
