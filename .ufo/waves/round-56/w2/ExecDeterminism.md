# ExecDeterminism

Seat ExecDeterminism, round-56 W2 falsify, lane kake-shokunin. Question attacked: do the two round-56 counters measure the
**committed bytes of `--revision`**, not the worktree they are pointed at? All runs in my own clone
`D=$(mktemp -d)` → `/tmp/tmp.HiLwYaNLzy`, `git clone -q --no-checkout <lane> $D && git -C $D checkout -q
a450e43e696d032e3ac308383f6b3394e0c92860`; `git -C $D rev-parse --show-toplevel` = `/tmp/tmp.HiLwYaNLzy` (equals `$D`),
`rev-parse HEAD` = `a450e43e696d032e3ac308383f6b3394e0c92860`. Lane tip at run time `7ad7db51…` — I wrote nothing in the lane
but this report; no lane git/jj mutation, no pacman, no tool install (nothing needed).

Counter commands (all from `$D`, absolute `--root "$D"`):
`python3 -B .ufo/waves/round-56/c56_selftally.py --root $D --revision <rev>` (C1) and
`python3 -B .ufo/waves/round-56/c56_quote_truth.py --root $D --revision <rev>` (C2).

Clean reference at `a450e43…` (worktree clean, `status --porcelain` empty):
C1 `tally_mismatches=0 rows_checked=10 met=True`, ten `OK` rows (claims 45/106/204/235/23/9/19/18/44/54), `EXIT=0`;
C2 `8/8 met=True`, C1–C8 all `PASS`, `EXIT=0`. Saved to `/tmp/execdet_clean_c1.txt`, `/tmp/execdet_clean_c2.txt`.

## DIRTY TREE RUNS:

Uncommitted worktree mutations in `$D` (HEAD still `a450e43…`, `git status --porcelain` = ` M SKILL.md`,
` D corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`):
1. `SKILL.md:726` (base-path-audit `Self-test` cell) `30 matrix fixtures plus 15` → `40 matrix fixtures plus 15` (claim 45 → 55);
2. `SKILL.md:1067` (source-recheck-audit `Self-test` cell) `(106 fixtures)` → `(999 fixtures)`;
3. deleted, uncommitted, the S419 entry `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (worktree `ls` count 0; the
   blob is still in the object store: `git show a450e43…:corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` prints its
   `source: S419 — https://info-search.yahoo.co.jp/archives/002856.php …` header).

Runs at `--revision a450e43e696d032e3ac308383f6b3394e0c92860`:
- C1: `tally_mismatches=0 rows_checked=10 met=True`, `base-path-audit: claim=45 observed=45/45 OK`,
  `source-recheck-audit: claim=106 observed=106/106 OK`, all ten `OK`, `EXIT=0`. The worktree cells (55, 999) were never read.
- C2: `8/8 met=True`, all eight `PASS`, `EXIT=0` — the entry deleted in the worktree still counts.
- `diff /tmp/execdet_clean_c1.txt /tmp/execdet_dirty_c1.txt` → empty (`IDENTICAL`); same for C2 → **both dirty-tree outputs are
  byte-identical to the clean runs**. The clean runs were re-taken after `git checkout -- SKILL.md
  corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (`status --porcelain` = 0 lines), so the comparison is same-root,
  same-revision, same host load.

Fourth probe (the one path where a worktree *could* leak — C1 runs the documented selftest in a clone of the root): worktree
`scripts/source_recheck_selftest.py` dirtied to end with
`_rc = main(); print("selftest: 999/999 passed"); raise SystemExit(_rc)`. Positive control: running that worktree script
prints `{"cases": 106, …, "passedOverTotal": "106/106"}` then `selftest: 999/999 passed` as its **last** line — exactly the
line `parse_tally` would take, i.e. a worktree-reading counter would report 999. C1 at `a450e43…` then printed
`tally_mismatches=0 rows_checked=10 met=True` and `source-recheck-audit: claim=106 observed=106/106 OK`, `EXIT=0`. Reverted
(`git checkout -- scripts/source_recheck_selftest.py`; `status --porcelain` = 0 lines).

No tree pollution: `git -C $D status --porcelain` is empty after the counter runs (C1 cleans its `c56-tally-*` clone in a
`finally` block).

## BROKEN COMMIT RUNS:

One commit in `$D` on top of `a450e43…`, `git -c user.name=selftest -c user.email=selftest@local commit` →
`6c5c59aa0a61df0a0624f767611475bbff65d4cb` ("selftest fixture: delete one C2 entry and corrupt one registry tally";
`SKILL.md | 2 +-`, `…/yahoo-japan-deleted-url-recrawl.md | 62 --------`). Contents: the S419 entry deleted **and**
`SKILL.md:1233` (readme-index-counter `Self-test` cell) `(44 fixtures, generated sandbox repos` →
`(45 fixtures, generated sandbox repos`.

- C2 at `6c5c59a` → `C2 quote-truth 5/8 met=False`, `EXIT=1`: `C1_entries_exist FAIL` (S419 entry absent at the measured
  revision), `C2_entry_provenance FAIL` (entry absent), `C7_validate_before_append FAIL` (validated scratch entry differs
  from the landed entry); C3/C4/C5/C6/C8 `PASS`. Not met, as required.
- C1 at `6c5c59a` → `tally_mismatches=1 rows_checked=10 met=False`, `EXIT=1`:
  `readme-index-counter: claim=45 observed=44/44 MISMATCH claim_ne_observed`; the other nine `OK`. Not met, as required.
  The same commit's deletion of a knowledge entry does not disturb any row (each row's selftest is fixture-built).

So the counters respond to committed content: the identical mutations are invisible when uncommitted (above) and decisive
when committed (here).

## REVISION FORMS:

State during these runs: HEAD = `6c5c59a` (the broken commit), worktree clean — so `HEAD` and the worktree were *wrong* and
only the `--revision` argument was right.

| form passed to `--revision` | `git rev-parse --verify <form>^{commit}` | C2 result | exit |
|---|---|---|---|
| `a450e43e696d` (12 hex, abbreviated) | `a450e43e696d032e3ac308383f6b3394e0c92860` | `8/8 met=True` | 0 |
| `selftest-attack` (tag at `a450e43`) | `a450e43e696d032e3ac308383f6b3394e0c92860` | `8/8 met=True` | 0 |
| `selftest-branch` (branch at `a450e43`) | `a450e43e696d032e3ac308383f6b3394e0c92860` | `8/8 met=True` | 0 |
| `broken-fixture` (branch at `6c5c59a`) | `6c5c59aa0a61df0a0624f767611475bbff65d4cb` | `5/8 met=False` | 1 |
| `HEAD` (later run, worktree detached at `a450e43`) | `a450e43e696d032e3ac308383f6b3394e0c92860` | `8/8 met=True` | 0 |

Abbreviated SHA, tag and branch all resolve to the same bytes and give the same verdict as the full 40-hex run; a ref name
pointing at a different commit gives that commit's verdict, so name resolution is faithful. C2's own resolution check is
`git rev-parse --verify --quiet <rev>^{commit}` (`c56_quote_truth.py:953`; `c56_selftally.py:491`), and an unresolvable form
prints `unevaluable: revision … does not resolve` with exit 2.

## FINDINGS:

1. **Committed-bytes-only holds for both counters (no defect; the assigned question is answered affirmatively).** Mechanisms:
   every content read is `git -C <root> show <rev>:<path>` (`c56_quote_truth.py:118-121`, used for the registry, lesson,
   three entries, receipts, validate receipts, mirror and every retained body; `c56_selftally.py:90-99` for `SKILL.md`), the
   page-uniqueness sweep is `git ls-tree` at the revision (`c56_quote_truth.py:357`), and C1's selftest execution path is
   `git clone -q --no-checkout <root> <tmp>` + `git checkout -q <rev>` (`c56_selftally.py:185-197`) with the command run
   inside that clone under a fixed environment (`c56_selftally.py:200-215`). Uncommitted edits, deletions and a doctored
   selftest script were all ignored; the same changes committed were decisive. Evidence: the four dirty-tree probes and the
   two byte-identical diffs above.
2. **The receipt records the caller's revision *string*, not the resolved commit** — attacks both counters' audit trail.
   `c56_quote_truth.py:973` prints `revision: {args.revision}` and `:961` puts the same raw string in `--json`;
   `c56_selftally.py:309`/`:497` do the same. Demonstrated: `--revision selftest-attack --json` →
   `{"schema": "kake-r56-c2-quote-truth-v1", "revision": "selftest-attack", "conditions_passed": 8, "exit": 0, "met": true}`.
   Consequence: a receipt taken with a branch name or a 12-hex abbreviation does not name the bytes measured; if the branch
   moves, the same command can later measure a different tree with a byte-identical label, and the committed receipts
   (`controls/base-c1-selftally-v2.txt`, `controls/base-c2-quote-truth.txt`, `w1/*`) cannot be re-anchored from their own text.
   The round's after-state statement should therefore carry full 40-hex revisions, or the counters should print the resolved
   commit beside the given string. Predicate not affected; the round-56 report and `contract.md` do quote full hashes.
3. **Nothing pins the measured revision to the claim's declared revision or to the lane tip** — `--revision` accepts any rev
   expression that resolves (`HEAD` measured 8/8 above; `HEAD~1`, `refs/heads/…`, tags all pass the same check at
   `c56_quote_truth.py:953` / `c56_selftally.py:491`). The label is honest about what was asked, so this is not a false
   receipt; it is a scope note: "measured at revision X" is a caller assertion, and only the string in the receipt ties the
   measurement to a commit. Same mitigation as finding 2 (resolve-and-print).
4. **A dirty worktree is invisible, by design, and therefore indistinguishable from a clean one** — the flip side of finding 1.
   Neither counter warns that `<root>`'s worktree differs from `<rev>` (no `git status` / `git diff --quiet` check anywhere).
   For the round's purposes that is correct (committed bytes only), but a receipt cannot show whether the seat measured from a
   dirty lane; a one-line warning would make the receipt self-describing. Not a predicate break; no claim is affected.
5. Nothing else diverged: the two counters agree with each other on the same tree (C2 `8/8` and C1 `0/10-mismatch` at
   `a450e43…`; both drop at `6c5c59a`), C2's failure set at the broken commit is exactly the three conditions the deletion
   touches, and C1's is exactly the corrupted row. I did not run either counter's `--selftest` (out of this seat's scope).

VERDICT: Both counters read committed bytes only — dirty SKILL.md cells, a deleted entry and a doctored selftest script left both verdicts byte-identical to clean, while the same edits committed at `6c5c59a` gave C2 5/8 exit 1 and C1 1-mismatch exit 1; 12-hex, tag and branch forms all resolve faithfully (defects found are receipt-level: the printed revision is the caller's string, never the resolved commit).
