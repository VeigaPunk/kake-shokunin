# ExecControlPair — round 83 wave w1

## Scope

Built the C2 control pair at
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/capture-control/{a,b}/`.
`a/` is a verbatim copy of `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/capture`
(7 files: three surfaces × body+receipt, plus `manifest.json`). `b/` is the same copy with exactly
one flipped body byte per declared surface (`bytes`/`sha256` re-derived from the retained body) and
one changed `ETag` value on `ds4cc-primary`. Nothing else was touched in either tree.

Declared surface order read from
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture-expectations.json`:
`ds4cc-primary`, `ds4cc-robots`, `ds4cc-sitemap`.

## Build mechanics

- Copy: `shutil.copytree(<round-82 capture>, control/{a,b})`; byte-for-byte, no edits to `a/`.
- `b/` body flip: last byte of each `body.bin`, XOR `0x01` (`0x0A` → `0x0B`), length unchanged.
- `b/` receipt: `bytes` and `sha256` rewritten from the retained body; `fetchedAt`, header order,
  `headerCount`, `contentType`, `Content-Length`, status, method, truncated and the manifest left
  byte-identical. `Content-Length` therefore remains truthful (length unchanged).
- `b/` primary `ETag`: `"6addaff5-13431"` → `"6addaff5-13432"` (validator class).
- First build attempt produced a malformed ETag (`"6addaff5-113432`, closing quote lost). I deleted
  `b/` and rebuilt it from the source tree; the retained `b/` is the corrected second build. Only
  the final build record exists (`pair-build.json`).
- Receipts: `pair-build.json`, `pair-verify.json`, `tree-manifest.txt` (sha256 of all 14 files),
  `classifier.txt`, `classifier.run2.txt`, `classifier.json.txt`, `classifier.stderr.txt`,
  `classifier-negative.txt`, `counter-control-probe.txt`, all under
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/w1/ExecControlPair/`.

## Per-surface numbers

| surface | bytes a=b | flip offset | byte | sha256 a | sha256 b | header change | surface line |
|---|---|---|---|---|---|---|---|
| ds4cc-primary | 78897 | 78896 | 0x0A→0x0B | `f2c5d2b3…e8342e93` | `35873219…24824dc2` | ETag `"6addaff5-13431"`→`"6addaff5-13432"` | diffs=1 validator=1 verdict=representation-changed |
| ds4cc-robots | 62 | 61 | 0x0A→0x0B | `70f9ea28…d0264c05` | `7e08c44f…358a42120` | none | diffs=0 verdict=representation-changed (body digest) |
| ds4cc-sitemap | 7810 | 7809 | 0x0A→0x0B | `55cb947f…487006ef` | `65a21fb0…4567318b4` | none | diffs=0 verdict=representation-changed (body digest) |

## Commands run and exit codes

1. `python3 -B scripts/header_change_class.py --a .ufo/waves/round-83/capture-control/a --b .ufo/waves/round-83/capture-control/b --declared .ufo/waves/round-81/capture-expectations.json`
   → exit 0, stderr empty. Output (`classifier.txt`):
   `summary surfaces=3 diffs=1 per_request=0 validator=1 representation=0 policy=0 unknown=0 verdict=representation-changed`
   with per-surface `verdict=representation-changed` on all three surfaces.
2. Same command a second time → exit 0; `cmp classifier.txt classifier.run2.txt` identical
   (deterministic bytes).
3. Same command with `--json` → exit 0; stdout identical to the plain run (the frozen grammar says
   `--json` adds nothing the counter reads).
4. Negative control `--a …/a --b …/a` → exit 0, `summary surfaces=3 diffs=0 … verdict=same-object`
   (`classifier-negative.txt`): the pair discriminates, the control is not trivially passing.
5. Independent verifier (own code, not the tool) over both trees: for every one of the six receipts
   `method == GET`, `status` int in 100..599 (200), `bytes == len(body)`,
   `sha256 == sha256(body)`, `truncated is False`, `bodyFile` resolves → all pass
   (`pair-verify.json`, `all_ok = True`). Whole-tree diff `a` vs `b` is exactly six files:
   three `body.bin` + three `response.json`; both `manifest.json` files are identical.
   `headerCount == len(headers)` and `Content-Length == body length` on all six receipts.
6. `python3 -B .ufo/waves/round-83/c83_drift_class.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --work /fast/scratch/hyaku/kake-r83/ExecControlPair/work`
   → exit 0; `control_ok=1` and `# control=verdict=representation-changed validator=1`
   (`counter-control-probe.txt`, full line below). This was read-only over the lane.
7. `git status --porcelain -- .ufo/waves/round-82` in the lane → `0` lines: the frozen round-82 tree
   is unmodified.

Counter probe line:

    C2v1 revision=worktree declared=3 surfaces_a=3 surfaces_b=3 receipts_ok=1 diffs=14 validator=0 representation=0 unknown=0 verdict=same-object record_equal=1 determinism=1 control_ok=1 tool_offline=1 selftest_ok=1 tool_absent=0 met=true

## Write scope and hygiene

- Wrote only `.ufo/waves/round-83/capture-control/`, `.ufo/waves/round-83/w1/ExecControlPair/` and
  this report inside the lane.
- No writes or mutations to the fleet repo `/home/vgpnk/Projects/shokunin`: the dirty entries
  reported there (`.scratch/run15-state.json` 13:24:49Z, `.ufo/l0-questions.md` 09:46Z, three
  `.scratch/closure-*` at/ before 13:15Z) all pre-date this seat's first write (~13:26Z).
- No VCS mutation (read-only `git status` only), no network, no installations, no subagents.
- Scratch `/fast/scratch/hyaku/kake-r83/ExecControlPair/` removed; verified absent before yield
  (`ls` → "No such file or directory").

## Risks and notes

- `b/manifest.json` is the verbatim round-82 manifest, identical in `a` and `b`; its `source` paths
  still name the round-82 capture. It carries no body digests and is read by neither the frozen tool
  nor the counter, so it contributes no classification signal. I did not rewrite it because step 1
  mandates a copy and no frozen artifact consumes it; if an auditor wants the control tree
  self-describing, that rewrite must land in both sides and be disclosed.
- Coverage shape: the pair exercises a body-digest change on all three surfaces and one
  validator-header change. It does not exercise representation-class or unknown-class header
  changes. The frozen control predicate (`verdict=representation-changed`, `validator >= 1`,
  receipts verifiable) is satisfied; this note prevents reading the control as coverage of those
  classes.
- The counter probe also reported `met=true` on the current tree. That is advisory output from a
  read-only run by this seat, not a C2 after-state claim and not a substitute for C2's own
  executor receipt.

## Verdict

PASS — the control pair at `.ufo/waves/round-83/capture-control/{a,b}` is built as specified; the
frozen classifier exits 0 printing `diffs=1 validator=1 representation=0 unknown=0
verdict=representation-changed` (all three surfaces representation-changed); all six synthetic
receipts verify against their retained bodies (GET, bytes, sha256, status, not truncated); the a
vs a negative control reads `same-object diffs=0`; two classifier runs are byte-identical; and the
frozen C2 counter reads `control_ok=1` with `# control=verdict=representation-changed validator=1`.
