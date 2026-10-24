# MutationC1Row — C1 registry-row removal probe

Seat: mutation-tester (leaf). Scope: assigned mutant only, disposable scratch clone of committed
bytes. Lane repo read-only throughout; no lane production file, index, ref or bookmark touched.

## Detector

`python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision REV`
(sha256 `4065b1cb52908102efc56e4508149842c837d24aec44883916a192983f00d3b6`, identical at
`714e707`, `766f461` and in the lane worktree).

Row predicate, `.ufo/waves/round-47/c47_registry_count.py:113-115`:
`needle = f"scripts/{tool}"`; `rows[tool] = any(line.lstrip().startswith("|") and needle in line ...)`
over `git show REV:SKILL.md`. Verdict/exit: `:128-130`, `:148` (`0=C1_MET`, `1=C1_NOT_MET`,
`2=could-not-evaluate`, `64=usage`).

Registry row under test: `SKILL.md:1197` (841 bytes incl. newline,
sha256 `63e8725cc3406faabcee71fa2ee441dd2b9e284e924a68bb81827650ad7323dc`), head
`| redirect-expectation-audit | gate (offline; no network) | \`python3 -B scripts/redirect_a…`,
tail `…| reads the manifest; writes only an optional \`--json\` report path | kake |`.
`awk '/^\|/ && /scripts\/redirect_audit\.py/' SKILL.md` → exactly line 1197 at `766f461`
(line 1202 prose mentions `redirect_audit.py::_witnesses()` but does not start with `|`).
Sibling gate row: `SKILL.md:1198` (`commit-citation-lint`, `scripts/citation_lint.py`).

## Baselines (pristine bytes, same clone)

| revision | output | exit |
|---|---|---|
| `cd42e3c310ba442e89dde638ba6401adaefaf3e8` (frozen base) | `registry_rows=0/2 receipts=0/2 C1_NOT_MET` | 1 |
| `714e7074110469a9ed2a3594677197baa0890905` (claimed after tip) | `registry_rows=2/2 receipts=2/2 C1_MET` | 0 |
| `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (lane HEAD) | `registry_rows=2/2 receipts=2/2 C1_MET` | 0 |

Baseline is green; the kill below is therefore interpretable.

## Mutant M1 (assigned): delete the redirect-audit registry row

Scratch clone: `/fast/scratch/hyaku/kake-r47/MutationC1Row/c1clone` (`git clone --no-hardlinks`,
origin path only, nothing pushed). Worktree at `766f461`; line 1197 removed; committed as
`63054913d69e0fbfa678daa5b6204de93fd42f5b` (parent `766f461`).

`git diff --numstat 766f461 6305491` → `0	1	SKILL.md` (1 file, 1 deletion, no additions).
`SKILL.md` in mutant: 1202 lines, sha256
`1ecd714a50736c5702f434913059e21b4b7ca2a247dcdd4cca5766496b4534e5`.

Detector output:

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision 63054913d69e0fbfa678daa5b6204de93fd42f5b
registry_rows=1/2 receipts=2/2 C1_NOT_MET
exit=1
```

`--json -` detail: `registry_row_detail = {"citation_lint.py": true, "redirect_audit.py": false}`,
`selftest_receipt_detail = {"citation_lint.py": true, "redirect_audit.py": true}`,
`registry_rows="1/2"`, `verdict="C1_NOT_MET"`.

**Verdict: KILLED.** Row count falls 2/2 → 1/2, verdict `C1_MET` → `C1_NOT_MET`, exit 0 → 1.
Receipts stay 2/2 at the mutant revision, so the failure is attributable to the row and not to
collateral receipt breakage or revision-resolution failure. The counter cannot return
`C1_MET` once every `|`-prefixed SKILL.md line naming `scripts/redirect_audit.py` is gone:
the row is load-bearing in this instrument.

## Control M2 (predicate strength, not the assigned mutant): non-gate table mention

Same clone, row 1197 replaced (not removed) by
`| redirect-audit-mention | informational (no gate semantics) | \`scripts/redirect_audit.py\` referenced only |`;
commit `cae48fb49316ff4ce7575a9c900d0cf2a4d1d121`, `SKILL.md` sha256
`c69692c3475b2f2b10801dc60cc908fdfef2422faa932279cd3c5ed640ad1a04`.

```
$ python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision cae48fb49316ff4ce7575a9c900d0cf2a4d1d121
registry_rows=2/2 receipts=2/2 C1_MET
exit=0
```

**Verdict: SURVIVED — coverage finding.** `:115` tests only "table line contains
`scripts/<tool>`"; it carries no gate-cell semantics (no column/command/exit-code assertion).
Any future table that merely mentions the path — e.g. a residual-defect table — would satisfy
the "gate-registry row" half of C1 without registering a gate. This does not falsify the shipped
C1 claim (line 1197 is a genuine gate row), and I do not propose changing the contract; it bounds
what the predicate proves: row *presence*, not row *meaning*. Recorded as a detector gap for a
later round, not a C1 failure.

## Restoration (exact bytes) and honest procedure note

- First restore attempt `git checkout -- SKILL.md` was a **no-op**: `git commit -a` had already
  written the mutant blob into the index, so `--` re-materialized the mutant
  (post-command sha256 stayed `1ecd714a…`). No detector result above depends on it; recorded
  because a silent no-op restore is itself a hazard for this workflow.
- Correct restore: `git checkout 766f4610… -- SKILL.md` → sha256
  `a40a37d1fa10d27d75a88e9da3fe9c54bc32ce561fc5e81d80a7189b922385e6`;
  `git diff 766f4610… -- SKILL.md` empty. Then `git reset --hard 766f4610…` → HEAD `766f4610…`,
  `git status --porcelain` empty, worktree sha256 `a40a37d1…` (equals pristine committed blob).
- Post-restore controls: pristine `766f461` → `registry_rows=2/2 receipts=2/2 C1_MET`, exit 0;
  base `cd42e3c` → `registry_rows=0/2 receipts=0/2 C1_NOT_MET`, exit 1. Detector unharmed.
- Mutant commits `6305491` / `cae48fb` remain addressable in the scratch object db (evidence
  retained); scratch clone never pushed (`git remote -v` = origin path only).
- Lane checkout unchanged: HEAD `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` before and after;
  `SKILL.md` sha256 `a40a37d1…`, 1203 lines, line 1197 intact; counter script sha256 unchanged.
  `git status --porcelain` shows only sibling-owned artifacts (`M .ufo/waves/round-47/w1/swarm-registry.json`,
  `?? .ufo/waves/round-46/residual/`, `?? .ufo/waves/round-47/w1/{CriticReasonFidelity,ExecBaseC1,ExecReceiptReplay,MutationC1Receipt,MutationC2R3,MutationC2R5,MutationC2R6,ScoutS136Quote}.md`;
  none written by this seat; this report is the only lane write from this seat).

## Tooling

No installs or updates; `python3`, `git`, coreutils only. Pacman not invoked.

## Bottom line

C1's row half is genuinely exercised by the shipped counter: deleting `SKILL.md:1197` costs
exactly one row and deterministically yields `C1_NOT_MET` (exit 1). Residual, non-blocking:
the row test is substring-based, so "registry row" is proven as presence, not as gate semantics.
