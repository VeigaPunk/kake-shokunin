# MutLandedCheck

Target: `scripts/landed_check.py` at rev `a450e43e696d032e3ac308383f6b3394e0c92860` (clone `/tmp/mutlc.r8LvYO`, disposable mktemp).
Detector: `python3 -B scripts/landed_check.py --selftest` (14 checks), timeout 600s, run only inside the scratch clone.
Baseline (pristine, sha256 `b78ae52b889d838a1c8136f79fc1ae02ffb39d1b44a02c2a9b75fb163fdbeef8`): PASS, `selftest 14/14`, rc=0 — verdicts below are conclusive.
18 single-point mutants (10 named lanes + 8 derived). 10 KILLED, 8 SURVIVED. Every mutated file was restored and re-hashed after its run (18/18 `restored_ok=True`).

## MUTANTS:

| id | attack (landed_check.py) | verdict | detector evidence |
|----|--------------------------|---------|-------------------|
| M01 | ancestry verdict inverted, :107-110 | KILLED | FAIL honest-report: exit 1!=0, landed=0!=2, missing=2!=0 (+3 fixtures) |
| M02 | digest-label suppression disabled, :189 | KILLED | FAIL digest-label-ignored: cited=2!=1, unknown=1!=0 |
| M03 | 64-hex token skip removed, :122 | SURVIVED | 14/14; skip is dead code — see SURVIVORS |
| M04 | oid dedupe removed (`if oid in seen_commits`), :166 | KILLED | FAIL honest-report: cited=3!=2; duplicate-hash-counted-once: cited=3!=1 |
| M05 | token-string dedupe removed (`if key in seen`), :125 | SURVIVED | 14/14; observable only via suppressed counter — F05 kills |
| M06 | unknown unresolvable token counted as missing, :197-199 | KILLED | FAIL unknown-hash: exit 1!=0, missing=1!=0, unknown=0!=1 |
| M07 | exit-code map swapped 1<->2, :205-208 | KILLED | FAIL side-branch-hash: exit 2!=1; empty-report: exit 1!=2 |
| M08 | non-commit objects treated as citations (`kind != "commit"` gate), :184 | KILLED | FAIL non-commit-object-skipped: cited=2!=1, unknown=1!=0 |
| M09 | ancestry narrowed to `rev-list --first-parent`, :106-111 | SURVIVED | 14/14; no merge fixture — F09 kills |
| M10 | empty/no-citation report exits 0 (`landed == 0 or` dropped), :207 | KILLED | FAIL empty-report: exit 0!=2; prose-only-report: exit 0!=2 |
| M11 | branch resolution check removed, :157 | KILLED | FAIL branch-missing: cited=1!=0, unknown=1!=0 |
| M12 | MIN_HASH_LEN 7 -> 4, :51 | SURVIVED | 14/14; no sub-7 token fixture — F12 kills |
| M13 | USAGE_EXIT 64 -> 1, :50 | SURVIVED | 14/14; usage fixture compares against the same mutated constant — F13 kills |
| M14 | unknown-token dedupe removed (`seen_unknown`), :196 | SURVIVED | 14/14; second dedupe layer unreachable — see SURVIVORS |
| M15 | undetermined ancestry counted NOT-ANCESTOR (`state is not True`), :175 | SURVIVED | 14/14; no undetermined-ancestry fixture — F15 kills |
| M16 | ANCESTOR line emitted as NOT-ANCESTOR, :174 | SURVIVED | 14/14; counts unchanged, selftest never reads line content — F16 kills |
| M17 | line-text span collapsed (`line_end = line_start`), :129-130 | KILLED | FAIL digest-label-ignored: cited=2!=1, unknown=1!=0 |
| M18 | unknown token not counted as cited, :197-198 | KILLED | FAIL unknown-hash: cited=1!=2; short-hash-ambiguity: cited=1!=2 |

Mutated-file hashes (sha256[:12]): M01 3c8f12b9c295, M02 70f8ef6f84ab, M03 589ed073a5f2, M04 ee35ff4a5fe2, M05 627bc272ba19, M06 4dc3a2c884dd, M07 fa5df900cbf2, M08 d582fac06b6a, M09 9975f9746365, M10 5f1a455da1ac, M11 3c1113beaa3c, M12 8df64b85b1c9, M13 32dba5cb2998, M14 f7af6d71576e, M15 ba40fec08318, M16 7059766eede7, M17 43c18c34c626, M18 7e30f013b0e3.

## SURVIVORS:

1. **M03 (:122, `if len(token) == DIGEST_LEN`) — equivalent mutant.** HEX_RUN (:55-56) matches 7-40 chars with lookbehind/lookahead, so a token of length 64 can never be produced: probe `extract_tokens("digest <64-hex e3b0c4…855> and commit \`e3b0c442\` tail")` returned `['e3b0c442']` only (`len64_possible=False`). The skip is dead code; no fixture can kill its removal. Coverage finding: the 64-hex protection is the regex bounds, not this branch; the branch only guards a future MAX_HASH_LEN widening.
2. **M05 (:125, extract-level token dedupe) — killable, selftest lacks the fixture.** Only observable channel: `Result.suppressed_digests` (digest-suppressed tokens are counted per occurrence, resolvable ones are re-deduped by `seen_commits`). F05 below kills it (suppressed 1 -> 2, surfaced by main()'s stderr note, :414-416).
3. **M09 (:106-111, first-parent ancestry) — killable, selftest lacks the fixture.** All 14 fixtures are linear history, where first-parent == full ancestry. F09 below (merge commit) kills it.
4. **M12 (:51, MIN_HASH_LEN=7) — killable, selftest lacks the fixture.** No fixture cites a 4-6 hex token on a non-digest-labelled line ("sha256"/"digest" lines would mask it). F12 below kills it.
5. **M13 (:50, USAGE_EXIT=64) — killable, selftest check is self-referential.** usage-error fixture asserts `proc.returncode == USAGE_EXIT` against the same mutated module global, so 64->1 passes its own check (and collides with the real exit-1 "NOT-ANCESTOR" class for callers). F13 below pins the literal 64 and kills it.
6. **M14 (:196, `seen_unknown`) — equivalent mutant.** extract_tokens already yields each distinct (lowercased) token once (:124-127), so `seen_unknown` never fires. Demonstrated: report citing ghost `deadbeef00` twice -> pristine cited=2/unknown=1, mutant identical. No fixture can kill; the set is dead code.
7. **M15 (:175, `state is False`) — killable, selftest lacks the fixture.** No fixture produces undetermined ancestry. F15 below (resolvable cited commit, corrupted intermediate object -> merge-base exits 128) kills it.
8. **M16 (:174, classification line label) — killable, selftest never inspects line content.** `_expect` (:421-437) checks counts and summary shape only; result.lines are printed only on failure. F16 below (assert line0 starts with "ANCESTOR ") kills it.

## PROPOSED FIXTURES:

Validated in scratch: each fixture PASSES on pristine and FAILS on the mutant (pristine vs mutant observed via `check_report`).

1. **F05 kills M05** — repo 1 commit; report `sha256 \`2b146a72\` here and sha256 \`2b146a72\` again.`; assert suppressed_digests==1. Pristine: suppressed=1, cited=0, exit 2. Mutant: suppressed=2. (Add to `digest-label-ignored`-style fixture a repeated digest token; ideally also assert the stderr suppression note count.)
2. **F09 kills M09** — base; branch `feat`; commit S on feat; back to master; `merge --no-ff feat`; report cites S; assert code=0, landed=1. Pristine: ANCESTOR, exit 0. Mutant: NOT-ANCESTOR, exit 1, missing=1. (New `merge-commit-side-parent` fixture.)
3. **F12 kills M12** — repo 1 commit; report `Commit \`<oid>\`.\nStray cafe token.`; assert cited=1, unknown=0, code=0. Mutant: cited=2, unknown=1.
4. **F13 kills M13** — run script with no args; assert exit code == 64 (literal, not the module constant). Pristine rc=64; mutant rc=1.
5. **F15 kills M15** — commits a<-b<-c; delete loose object of b; report cites a; branch master; assert code=2, unknown=1, undetermined=1. Pristine: UNKNOWN + exit 2. Mutant: NOT-ANCESTOR + missing=1 + exit 1.
6. **F16 kills M16** — repo 1 commit; report cites HEAD; assert first result line starts with `ANCESTOR ` (and for side-branch fixture, `NOT-ANCESTOR `). Mutant emits the swapped label with unchanged counts.
7. **M03/M14 — no fixture can kill (equivalent mutants).** Proposed change instead: delete the dead `len(token) == DIGEST_LEN` skip (:122-123) and the dead `seen_unknown` set (:162, :195-198), or add a comment/contract note that dedupe+digest-length guards live solely in HEX_RUN/extract_tokens. Contract semantics unchanged.

Recommended selftest strengthening (coverage gaps behind all 6 killable survivors): one merge-commit fixture; one sub-7-hex token fixture; hard-coded usage exit 64; one corrupted-object undetermined fixture; line-content assertions for classification lines; repeated-token digest suppression count.

## Restoration evidence

- All runs in disposable clone `/tmp/mutlc.r8LvYO` checked out at `a450e43e696d032e3ac308383f6b3394e0c92860`; pristine copy kept beside target and sha-gated (`b78ae52b889d…beef8`).
- After every mutant the pristine bytes were written back and re-hashed: 18/18 `restored_ok=True`; final state hash equals pristine and a final detector run returned rc=0 `selftest 14/14`.
- During harness hardening one intermediate run left the scratch target mutated; it was restored from the sha-gated pristine copy (hash re-verified) before all conclusive runs. Lane repo, siblings, lane jj/git state: untouched; the only lane write is this report.

VERDICT: landed_check.py --selftest killed 10/18 single-point mutants; of 8 survivors 6 were killed by validated fixture proposals (merge-commit ancestry, sub-7-hex token, literal usage-exit 64, undetermined ancestry, classification-line content, digest-token dedupe) and 2 (M03 :122, M14 :196) are equivalent dead-code mutants — the selftest has real coverage gaps in non-linear history, line content, exit-code literal, and undetermined ancestry.
