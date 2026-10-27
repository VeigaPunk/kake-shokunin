# CriticC1Cheat

C1 counter (`c58_receipt_rewrites.py`, v1) attack: cheapest ledgers/commit sequences that reach `met=True` without a true disclosure. All runs: fixture repos under `/fast/scratch/hyaku/kake-r58/CriticC1Cheat/` (selftest identity, `git init -b main`, toplevel asserted), counter invoked `python3 -B c58_receipt_rewrites.py --root <d> --revision HEAD --json`; `--selftest` 18/18 PASS. Lane tip read-only run: `events=19 undisclosed=19 met=False exit=1`, ledger absent — matches frozen base.

Axes named: (a) every rewrite surfaces as an event; (b) disclosure matches event (blobs/kind/status); (c) note carries a resolvable evidence pointer; (d) surface covers all receipt locations; (e) cheapest false-green cost.

## CHEATS:

**CH1 rename-with-edit — the A of the new name is NOT an event. met=True.**
Commands: `controls/r57.txt` committed "v1"; one commit does `git mv` to `r57b.txt` and writes "v2"; ledger discloses only the `D` of the old path (+ `after-c2/c3` receipts at tip). Counter: `events=1` (only the D; `--no-renames` shows D+A, and the A is a first addition → skipped by the `seen` rule), `undisclosed=0 met=True exit=0`. The rewrite under the new name is invisible; the disclosed "delete" never mentions that the content lives on, rewritten. Fix: rename-pair detection (pair same-commit D→A by blob equality, or use `-M` and stop forcing `--no-renames`) and count both halves as events; additionally track any path that ever sat under `control(s)/` for life, so relocation does not drop it.

**CH2 subdir relocation / receipts outside `control(s)/` — invisible rewrites. met=True.**
`POP_RE = ^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$` excludes subdirs and everything else. (a) F3: `git mv controls/r57.txt controls/sub/r57.txt` (D disclosed), then rewrite inside `controls/sub/` → `events=1 met=True`. (b) F4: receipt *born* at `controls/sub/r57.txt` → zero events ever, any number of rewrites, no disclosure needed → `events=0 met=True exit=0`. Same class: moving a receipt out of `.ufo/waves` entirely (e.g. into `corpus/`) before rewriting. Fix: make the surface recursive (`control(s)/**`, allow `/`), and/or keep a lineage set of every path ever seen under `control(s)/`; a later M/D/A on a lineage path is an event wherever it sits.

**CH3 merge-second-parent / side-branch rewrites — transient rewrites vanish. met=True.**
With `--first-parent -m`, only the merge's diff vs its first parent is enumerated; side-branch commits never appear. (a) F5: side branch rewrites v1→v2, merged → exactly one `M` at the merge (v1→v2); disclose it → `met=True`. (b) F14: side branch v1→v2→v1 (rewrite then revert) then merge → `events=0 met=True` with NO disclosure; the post-commit rewrite existed and is gone without a trace. A full-history walk (drop `--first-parent`, keep `-m --full-history`) does enumerate both side M's (verified on the F5 and F14 fixtures) — fix: walk full history for receipt paths, or add explicit second-parent diffs at every merge. (c) F13 conflicted merge resolved to a third content: two events (pre-merge M + merge M); disclosing only one → `undisclosed=1 fail`; both → `met=True` — counter is sound here; a true disclosure just must list every M.

**CH4 note pointers: unrelated existing file or bare commit hash. met=True.**
`pointed()` accepts any repo-relative path that resolves at the tip, or any 7–40 hex resolving in the lane. (a) F6: note `"see .ufo/evidence.md"` (exists, unrelated to the event) → `unpointed=0 met=True`. (b) F7: note `"fixed in <hash>"` where hash is the rewriting commit (self-pointer) → `unpointed=0 met=True`. No event-specific information is disclosed. Contract states prose truth is reviewer-checked (stated limit), so the counter itself cannot tell; still a false-green relative to "disclosed with its true values". Fix: reject notes that are only a pointer (require non-pointer prose, e.g. ≥3 words outside the pointer); decide a reviewer gate for semantic truth.

**CH5 kind misnaming — caught when it disagrees with the classifier, but the classifier is shape-based.**
F12: `pending`→"met=True" is classified `fill`; ledger kind `rerun` → `wrong_kind=1 fail` (good). But any content placed into a disclosed kind matches: filling a `pending` receipt with *fabricated* values is still `fill` and meets (F1's fill content was arbitrary; no value-truth check). The classifier cannot distinguish an honest fill from a fabricated one; the kind taxonomy matches shapes, not semantics. Fix: reviewer check of values (already routed to the claim's reviewer); optionally require the note to name what was filled (prose, per CH4 fix).

**CH6 delete + readd identical bytes — sound: both are events.**
F8: delete commit then re-add commit with identical bytes → D + A(readd) events. Disclosing only the D → `undisclosed=1 fail`; disclosing both → `met=True`. No bypass; the counter correctly forces disclosure of the re-add even though bytes are unchanged (info-only burden). No fix needed; option: treat identical-byte re-adds as non-events (would weaken, not recommended).

**CH7 symlink indirection — zero events. met=True.**
Receipt committed as a symlink to a sibling file; rewriting the *target* changes receipt content with no path-level event: F9 → `events=0 met=True exit=0`. Fix: when walking, resolve symlink entries (`ls-tree` type `t`); flag receipt symlinks (new `malformed`/dedicated count) or track target blob changes.

**CH8 amend-folding — event erased from history. met=True.**
F10: add commit, then rewrite content and `git commit --amend` → history contains a single commit; `events=0 met=True exit=0`. The intermediate state never entered the committed lineage, so it is indistinguishable from an honest first commit (satisfies "committed once"). Fix: not fixable within git history semantics; record as boundary — the counter can only see states that entered history.

## LIMITS TO DISCLOSE:
- Receipts outside `control(s)/` dirs (incl. subdirs) are outside the observed surface — CH2 (contract-stated; demonstrated).
- Note prose truth is not checked, only pointer resolvability — CH4 (contract-stated; demonstrated).
- Value-level fabrication inside a kind the classifier assigns (fill with fake numbers) is indistinguishable from an honest disclosure — CH5.
- `--first-parent` hides side-branch/transient rewrites — CH3 (fix: full-history walk).
- States that never enter committed history (amend, `-s ours`, transient end-state cancellation) are invisible by nature — CH8, CH3b.
- Symlink targets are not tracked — CH7.
- A ledger auto-generated from git by the counter's own classifier would meet the counter; per contract that is a *true* disclosure, not a junk pass.
- C1 attests event disclosure, not the lane's prose assertions or the receipts' factual content beyond pointer existence.

## Evidence table (fixture → counter JSON)
| fixture | cheat | events | undisclosed | phantom | malformed | wrong_kind | unpointed | new_rewritten | new_receipts | met | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | control: true fill disclosure | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F2 | CH1 rename-with-edit (only D disclosed) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F3 | CH2 subdir relocate+rewrite | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F4 | CH2 subdir-native (no disclosure) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F5a | CH3 merge rewrite, no ledger | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | False | 1 |
| F5b | CH3 merge rewrite, disclose merge M | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F6 | CH4 note=unrelated existing file | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F7 | CH4 note=bare commit hash | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F8a | CH6 delete+readd, D only | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | False | 1 |
| F8b | CH6 delete+readd, both | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F9 | CH7 symlink indirection | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F10 | CH8 amend-fold | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| F12 | CH5 wrong kind | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | False | 1 |
| F13 | CH3 conflicted merge, one of two M disclosed | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | False | 1 |
| F14 | CH3 transient side rewrite reverted before merge | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | True | 0 |
| lane tip | read-only base run | 19 | 19 | 0 | 0 | 0 | 0 | 0 | 0 | False | 1 |

VERDICT: C1 v1 reaches met=True without true disclosure via rename-with-edit (CH1), subdir/outside-controls relocation (CH2), transient side-branch rewrites (CH3), pointer-only notes (CH4), symlink indirection (CH7) and amend-folding (CH8); the cheapest single fix is recursive control-surface + rename-pair/lineage tracking + full-history walk, with note-prose and value-truth left to reviewer gates.
