# Wave-2 ReviewCriteriaChecks — the four round-36 criteria checks and their receipts

Attacked `.ufo/waves/round-36/criteria/{ablation_floor_check,control_tree_check,version_bump_check,hash_resolve_check}.py`
and the nine `verification/criterion-*.txt` receipts at `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e`.
All nine receipts reproduce exactly; then one false pass per check was constructed and run — all four succeeded.
Sandbox clone `/fast/scratch/hyaku/kake-r36w2/ReviewCriteriaChecks/clone` (rev-parse = f3a38bf…; criteria scripts,
receipts, r35-shape fixtures, ctl reports and sealed_count_v1/v2/v3 all tracked there, so reruns used exactly the
landed bytes), `TMPDIR=…/tmp`, GIT_* unset, every process under `timeout` ≤300 s, ≤4 parallel. Fixtures under
`/fast/scratch/hyaku/kake-r36w2/ReviewCriteriaChecks/tmp/`. No tools installed (python3/git sufficed); no pacman use (host-wide pause honored).

## 1. Reproduction — 9/9 exact

| Receipt | Command (from clone root; `python3 -B .ufo/waves/round-36/criteria/…`) | Recorded | Rerun | Match |
|---|---|---|---|---|
| ablation-floor-r36 | `ablation_floor_check.py --target 25 --receipts .ufo/waves/round-36/verification/ablations` | PASS 36 scored, exit=0 | identical | yes |
| ablation-floor-r35-shape | `ablation_floor_check.py --target 22 --bullets a,b,c --receipts .ufo/waves/round-36/criteria/r35-shape-receipts` | FAIL c_skip met 22/24, exit=1 | identical | yes |
| control-tree-r36-controls | `control_tree_check.py --report …/ctl/{CtlAllFalse,CtlConstantClean,CtlNaiveReader,CtlNoReader,CtlShortcut}.md --pattern /fast/scratch/hyaku/kake-r36/.k --pattern .ufo/waves/round-36/sealed/` | 5×PASS "ls; 3 listed paths", exit=0 | identical | yes |
| control-tree-r35-report | `control_tree_check.py --report .ufo/waves/round-35/w2/CriticC2Sufficiency.md --pattern .ufo/waves/round-35/sealed/` | FAIL no listing, exit=1 | identical | yes |
| version-bump-r36-v1-v2 | `version_bump_check.py .ufo/waves/round-36/sealed_count_v1.py .ufo/waves/round-36/sealed_count_v2.py` | SAME, exit=0 | identical (sha256s match receipt) | yes |
| version-bump-r36-v2-v3 | same, v2→v3 | DIFFERENT KEY_SHA256 pin, exit=1 | identical | yes |
| version-bump-r35-v1-v2 | `.ufo/waves/round-35/sealed_count_v1.py`→`sealed_count.py` | DIFFERENT C2_MAX_WORDS 1500→2200, exit=1 | identical | yes |
| hash-resolve-r36-decl | `hash_resolve_check.py --root . --revision 3555f63f --heading "## Round 36 — declared claims (before implementation lands)"` | FAIL b720d79976a1…, exit=1 | identical | yes |
| hash-resolve-r35-decl | same, `--revision cd321279`, Round 35 heading | hashes 1, unresolved 0, exit=0 | identical | yes |

## 2. Per-check verdicts and constructed false passes

**ablation_floor_check.** Failing receipt (r35-shape) fails for the stated reason: `ablation-c_skip.json` has
`met=true, passed=22 ≥ target 22` — the exact round-35 routed-defect-3 slack pattern the fixture encodes; the
fixture JSONs say so verbatim. Passing receipt (r36) passes for the right reason, independently verified from the
receipt contents: 36 ablation-named files, per-bullet a:3 b:5 c:7 d:4 e:4 f:6 g:5 (+2 `s_*` scored but not
required), max `passed`=24 < 25, zero `met=true`, zero malformed, zero stale-`target` warnings; reference-private
correctly skipped with its met=true noted.
**False pass (ran, exit 0):** `--target 25 --bullets c --receipts tmp/fp-ablation/dir1` → `PASS: 1 ablation
receipts scored … bullets c each covered`, where dir1 holds the REAL met=true receipt renamed
`ablation-c-skip.json` (dash, so `NAME_RE` `[^-_]+_` skips it — stderr note only) plus fabricated
`ablation-c_ok.json` `{"passed":0,"met":false}`. Second variant: dir2 with only the fabricated receipt → PASS.
Root cause: receipt↔bullet binding is filename-only; content is never tied to any run, and a one-character rename
unscores a real receipt while exit stays 0.

**control_tree_check.** Failing receipt (r35) fails for the stated reason: CriticC2Sufficiency.md quotes no
`ls`/`git ls-tree` output. Passing receipt (r36) is honest output but passes for a weaker reason than criterion
(d) (`corpus/QUALITY.md:864-866`) claims: the five ctl reports list `ls -la` of each control's own work directory
(e.g. `ctl/CtlConstantClean.md:71-81`), which cannot contain the key by construction; the check verifies only
"a listing exists and shows no key path" — never that the listing covers the tree the control was built from.
**False pass (ran, exit 0):** `tmp/fp-control/report.md` quotes a root `ls -la` of a tree that provably holds
`.ufo/waves/round-36/sealed/key.json` (`find` printed it immediately before the run); verdict text is
`PASS: … records a tree listing (ls; 3 listed paths) and shows no key path.` — byte-for-byte the shape and
"3 listed paths" of the landed receipts. Same-class variants (by code reading): one `git ls-tree` line satisfies
the listing requirement; `ls -la` with no path argument yields bare unmatched names; ACL `+` entries fall outside
`LS_ENTRY_RE`. Root cause: presence of *a* listing, not coverage or tree identity. (Lane working tree also holds
two untracked companions, `criteria/r35-0b7779dc-parent-tree-report.md` +
`verification/criterion-control-tree-r35-keypath-listing.txt`, showing the keypath-listing failure mode; not part
of f3a38bf, noted only.)

**version_bump_check.** Failing receipt r35-v1-v2 fails for the stated reason (the routed defect 2 cap change).
Failing receipt r36-v2-v3 fails for the right reason (only `KEY_SHA256` moved) and the demanded named control
exists: `SCORECARD.md:1681-1698` names CtlShortcut/key-version-2 as forcing the pin change, version 3 landed at
`cd321279` before any build (`SCORECARD.md:1712-1713`). Passing receipt r36-v1-v2 passes for the right reason:
raw diff v1→v2 is +26/−4, entirely the bwrap jail fix, its guard, and the docstring note that says the cases, pin,
projection, judge and predicate are unchanged — nothing scored moved.
**False pass (ran, exit 0):** `tmp/fp-version/{old,new}.py` — old computes `met = _meets(passed_count)` with
`_meets` = `passed >= TARGET`; new changes the helper body to `passed >= TARGET - 5`. `--list` shows identical
inventory (same constants, judge literals, met expression) and the verdict is `SAME - no target, threshold, cap,
pin or predicate differs`. Root cause: the inventory covers module constants, docstring predicate lines,
*string* literals inside `judge`/`project`/`*_judge`, and the literal text of the `met` assignment — numeric or
relational logic in function bodies and lowercase non-string variables are unscored. The real counter computes
`met` inline (`.ufo/waves/round-36/sealed_count.py:231`), so today a loosening there is caught; a refactor to a
helper followed by a body edit would not be.

**hash_resolve_check.** Failing receipt (r36 decl) fails for the stated reason: the section at 3555f63f contains
exactly one 40-hex hash, `b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07`; `git cat-file -e <h>^{commit}` exits 128
("Not a valid object name") while the intended base `b720d799ae99c19a7c97f2b1391d4fe928be0e11` resolves as a
commit — a declaration typing error, correctly caught. Passing receipt (r35 decl) passes for the right reason:
its single hash `16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a` is the round-34 verifier spot-check commit and resolves.
**False pass (ran, exit 0):** the same unresolvable hash written UPPERCASE in a scratch repo's declaration section
(`tmp/attack-up/SCORECARD.md`, committed) → `hashes 0, unresolved 0`, exit 0; the lowercase twin
(`tmp/attack-low/`) exits 1. Root cause: `hash_resolve_check.py:40` scans `[0-9a-f]{40}` only and there is no
"section must contain ≥1 hash" floor, so case (or any 41+-hex embedding, e.g. inside a sha256 token) hides a bad
hash entirely. Caller-chosen `--heading` on a hash-free section also trivially exits 0 (code-read, not run).

## 3. Severity (advisory)

- **High — control_tree_check:** the only positive evidence for criterion (d)'s listing requirement certifies
  work-dir listings that cannot show the key; an identical-shaped report over a key-holding tree passes (demonstrated).
  The check operationalizes neither "listing covers the build tree" nor "control built from that listed tree".
- **Medium-high — ablation_floor_check:** filename-only binding; fabricated clean receipts pass, and a one-dash
  rename unscores a real met=true receipt with exit 0 (stderr note only).
- **Medium — version_bump_check:** logic-level predicate loosening is invisible (demonstrated); the landed r36
  verdicts themselves are honest and the v3 pin change is properly named.
- **Low-medium — hash_resolve_check:** case blindness plus no minimum-hash floor; landed FAIL receipt genuine.

## 4. Residual risk / not verified

- Exit-2 paths (unreadable report/revision, heading not found) verified by code reading only, not run.
- Did not audit whether the 36 ablation receipts' `passed` values are truthful (counter ground — other seats);
  internal consistency only.
- Did not verify the ctl reports' claimed sandbox commits/bundles or that controls were key-blind in fact; the
  check cannot and I did not independently.
- The 7-bullet full-fabrication variant of the ablation false pass was not run (mechanical generalization of the
  bullet-c demo); the `git ls-tree`-one-line and ACL variants of the control-tree pass were not run.
- Criteria (a) knowledge-control, (b-polarity/f) sealed-polarity checks are other seats' items; untouched.
- No lane files written except this report; no network; no pacman.

Artifacts (deletable): `/fast/scratch/hyaku/kake-r36w2/ReviewCriteriaChecks/{clone,tmp}`
(clone at f3a38bf; fixtures `tmp/fp-ablation/`, `tmp/fp-version/`, `tmp/fp-control/`, `tmp/attack-low/`, `tmp/attack-up/`).
