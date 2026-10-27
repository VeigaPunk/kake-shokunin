# ReviewerC1Code
Code review of `.ufo/waves/round-58/c58_receipt_rewrites.py` (395 lines), code-before-data. All fixtures under
`/fast/scratch/hyaku/kake-r58/ReviewerC1Code/` (git 2.56.0); "confirmed" = reproduced in a fixture repo and/or via the CLI.
Contract cross-refs: `contract.md` (line 26 surface, line 36 predicate, line 41 exclusions).

FINDINGS:

- F1 [HIGH, confirmed by running] Receipts in a SUBDIRECTORY of `control(s)/` escape every count — `met=true` with an undisclosed round-58 rewrite.
  - Lines: 57 (`POP_RE = ^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$`), 102-103 (`events()` drops non-POP_RE paths before appending), 199 (`new_rewritten` sees only surviving `evs`), 59 (`NEW_RECEIPT_RE` likewise flat-only).
  - Failing input: fixture commits `.ufo/waves/round-58/controls/sub/after-c2-x.txt` ("ok"), then rewrites it post-commit ("rewritten undisclosed"), plus the two required flat receipts `after-c2-a.txt` / `after-c3-b.txt`. Observed CLI: `events=0 ... new_rewritten=0 new_receipts=2 met=True`, exit 0 (S7 via `measure`; Q2 via `python3 -B c58_receipt_rewrites.py --root <fixture> --revision HEAD`).
  - Contract conflict: line 26 freezes the surface as "every path ever committed **under** `.ufo/waves/round-<N>/control/` or `controls/` (all rounds)"; line 41 excludes only receipts *outside* `control(s)/` dirs. A nested path is under the dir, so it is in-surface, yet no count ever sees it.
  - Fix: line 57 `[^/]+$` → `.+` (any depth); align line 59 the same way (`.+\.txt$`) or document nested receipts as out of scope; add a selftest case for a nested rewrite.
  - Control: the same rewrite of a FLAT round-58 receipt is caught (`new_rewritten=1`, exit 1, Q3) — the hole is depth-specific.

- F2 [LOW, confirmed by running] A 0-byte ledger file is classified "absent" (exit 1, undisclosed) instead of "present but not JSON" (exit 2, unevaluable).
  - Lines: 163-164 (`raw = git(root, "show", f"{tip}:{LEDGER}", check=False)`; `ledger_present = raw != ""`).
  - Failing input: fixture tip commits an empty `receipt-rewrites.json` on top of one undisclosed fill. Observed: `ledger_present=false`, `undisclosed=1`, exit 1 (S6). Per the module docstring (line 30) and contract, exit 2 is for "ledger present but not JSON"; an empty file is present and `json.loads("")` raises. Inconsistency: a whitespace-only ledger hits the `json.JSONDecodeError` path → exit 2 (lines 167-170; code-read, not run).
  - Impact bounded: both outcomes are non-met; only the evidence-state class is wrong (mislabels a corrupt ledger as a mere failure to disclose).
  - Fix: test presence with `git cat-file -e {tip}:{LEDGER}` (or ls-tree), then parse; empty content then raises → exit 2.

- F3 [LOW, confirmed by running] `REVLINE_RE`'s `(?i)revision` substring (line 118, applied at line 142) turns prose into a "relabel", masking a met-flip rerun.
  - Failing input: `classify("M", "revision met=False\nnotes\n", "revision met=True\nnotes\n")` → `"relabel"` (observed, P1). Docstring (line 26-27 of the header) says relabel requires each changed line to carry "a 40-hex revision or a `revision` key"; "revision met=False" is prose, not a key.
  - Impact: (a) a genuine rerun disclosed with honest `kind="rerun"` is flagged `wrong_kind` (false accusation → claim blocked); (b) a lane can label a met-flipping rerun `relabel` and pass. Heuristic by design, so LOW.
  - Fix: require key shape, e.g. `(?i)\brevision\b\s*[:=]` as the word alternative (keep `\b[0-9a-f]{40}\b`). Note: `classify("M","met=False (<hex40>)\n","met=True (<hex40>)\n")` → relabel is docstring-conformant and NOT a defect (P1b).

NO-DEFECT CHECKS (each exercised; fixture refs in `/fast/scratch/hyaku/kake-r58/ReviewerC1Code/`, deleted after this report):

1. `-z` record shape is `\x01<hash>\0` + `\n` + `M\0<path>\0…`; `head`/`rest` parsing (lines 92-99) handles the stray `\n` on the first status token, and chunks from commits touching `.ufo/waves` but no `control(s)/` path parse to zero events (S0, P3).
2. Merges on git 2.56.0: `-m --first-parent` emits exactly ONE vs-first-parent diff per merge — no duplicate events for one commit, no cross-parent `fromBlob` mixing (S1, S2). A side-branch receipt state that survives into the tip is captured at the merge commit with correct pre/post blobs (S2). [Version-dependent: older git (<2.31 semantics) could emit pairwise diffs and duplicate events — INFERENCE, not tested.]
3. Path first added in a merge (absent from both parents): one `A` entry in the log, first-add skip applies, `events=[]` (S4) — the assignment's "first added in a merge" case is safe.
4. Merge resolution re-introducing a deleted receipt: faithful `A` event with `fromBlob=null` (S3) — a true re-add on the first-parent chain, matching the docstring's "A of a path that existed before".
5. Rename under `--no-renames` = D + A; the A of the new name is a first-add skip, the D is an event (selftest #8, and S3's delete leg).
6. Typechange `T` folded to `M` at lines 109-110 with correct blob ids; the ledger-facing status set {M,D,A} stays closed (S5). The first-add skip at line 105 runs before the fold, but a first-ever appearance as T cannot occur with `--full-history` [INFERENCE from history completeness, not separately fixture-proven].
7. Root commit: first-add skip (105-107) precedes the `{commit}^` resolution (111), so no rev-parse failure path is hit; `fromBlob=None` occurs only for genuine A/D events (fixtures throughout).
8. `blob_id` (76-84): ls-tree `-z` record `"<mode> <type> <sha>\t<name>"` split is correct, non-blob types skipped, failed rev → `None` via `check=False`; exercised on every fixture blob comparison.
9. Ledger matching (182-195): duplicate entries → second is phantom (selftest #5); a duplicate EVENT key cannot arise under one-diff-per-merge (see #2), so `ev_keys` set-collapse and one-entry-covers-two are unreachable; `None` blobs match `null` only on A/D as intended.
10. `pointed` (149-158): 12-hex resolving commit → True; a 41-hex run matches nowhere (boundary guards) → no false pointer; trailing `.` stripped from paths; absent path → False; existence enforced at the tip via `cat-file -e` (S8).
11. `new_receipts` (59, 197-198): the two required flat receipts counted; Q1 shows `new_receipts=2` + honest single-entry disclosure → `met=True`, exit 0 end-to-end. Edge note: a file literally named `after-c2-.txt` fails `[^/]+` while shell glob `*` matches empty — pathological name only, no impact on real receipt names.
12. Exit codes: 64 usage (missing `--revision`), 2 unresolvable revision, 2 non-JSON ledger, 2 top-level JSON list, 1 not-met, 0 met — all confirmed via CLI (P2, Q1).
13. Selftest: 18/18 PASS with `TMPDIR` pointed at the seat scratch (P4); `_repo` asserts toplevel identity before committing.

RESIDUAL RISK / VERIFICATION GAPS:
- Merge-diff semantics verified on the host's git 2.56.0 only; the counter's event model silently depends on `--first-parent` winning over `-m`. If the lane ever runs under a git where `-m` yields pairwise diffs, events can double-count merges (harmless direction: more undisclosed) — cite as an environment assumption in the counter docstring.
- F2's whitespace-only-ledger branch and #6's T-first-appearance claim are code-read, not fixture-run.
- Per seat scope (code-before-data) I did not run the counter against lane data or audit the real ledger/S423/S424 bodies; F1 means any `met=true` from this counter should not be trusted until line 57 is widened.
- No lane, fleet, or sibling files were modified; scratch fixtures were deleted after this report.

VERDICT: Core parser/matcher/exit-code behavior is sound on git 2.56.0, but F1 (subdir receipts invisible; met=true despite an undisclosed round-58 rewrite) must be fixed at line 57 before any C1 met=true is accepted; F2/F3 are low-severity polish.
