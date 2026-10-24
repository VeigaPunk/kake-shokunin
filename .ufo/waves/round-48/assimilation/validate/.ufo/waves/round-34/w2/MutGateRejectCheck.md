# Round 34 W2 — MutGateRejectCheck

Axes: operability (Gate decision/reason/scope detection) and freshness (whether the retained criterion receipts identify checker changes).

Built six lesson fixtures and committed them only in sandbox clone `/fast/scratch/hyaku/kake-r34/w2/MutGateRejectCheck/clone`, commit `f953ff52dc3b28a09dc22eefcc96849ae9f6ffe6`. Expected exit 1 = reject input; expected exit 0 = accepted reject. The checker command was `set +e; export TMPDIR=/fast/scratch/hyaku/kake-r34/w2/MutGateRejectCheck/tmp; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; python3 -B /fast/scratch/hyaku/kake-r34/w2/MutGateRejectCheck/clone/.ufo/waves/round-34/criteria/gate_reject_check.py --repo /fast/scratch/hyaku/kake-r34/w2/MutGateRejectCheck/clone --rev f953ff5 --lesson corpus/lessons/gate-reject-mutation-variants/<fixture>; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"; exit 0`. Ran that same command on each fixture with pristine, mutated and restored checker bytes.

| Variant (committed fixture lines) | Expected | Pristine | Mutated | Restored | Observed output |
|---|---:|---:|---:|---:|---|
| Fenced-block reject (`fenced-reject.md:5-9`) | 1 | 0 | 0 | 0 | `MATCH ...:8` — false pass in all states |
| “rejected” in plain prose, not a decision (`prose-rejected.md:5`) | 1 | 1 | 1 | 1 | `NO MATCH` |
| Table reject with empty reason (`empty-reason.md:5-7`) | 1 | 1 | 0 | 1 | `NO MATCH`; mutant `MATCH ...:7` |
| Reject only in `## Notes`, after Gate (`outside-gate.md:3-9`) | 1 | 1 | 1 | 1 | `NO MATCH` |
| Reasoned table-row reject (`table-reject.md:5-7`) | 0 | 0 | 0 | 0 | `MATCH ...:7` |
| Reasoned list-line reject (`list-reject.md:3-5`) | 0 | 0 | 0 | 0 | `MATCH ...:5` |

No false failures. Baseline false pass: fenced Markdown is not excluded before table parsing (`gate_reject_check.py:124-149`); it reports the row inside the fence. The prose-only and out-of-Gate negatives, reasoned table and list positives behaved as expected.

Mutation: one-line edit at checker line 94, `return bool(inline_reason or clean_cell(separate_reason))` → `return True` (empty decision reasons accepted). Pristine SHA-256 `35d0bba359ddbfaba242236cf45e5983f1add5136d1cd0c23c151e5e05972a84`; mutated `e90e6c90ceafe229105f4de04393cede762f5454333198b91edcad1520c9ddab`; restored `35d0bba359ddbfaba242236cf45e5983f1add5136d1cd0c23c151e5e05972a84`. The empty-reason witness detects the mutant (1→0→1). Overall six-case detector is **inconclusive as a clean mutation score** because pristine already false-passes the fenced case; specifically, the reason-focused witness flags this mutation.

Receipt check: reran the historical round-33 negative and round-29 positive with pristine, mutated and restored bytes. Every state returned round 33 `NO MATCH`, exit 1, and round 29 `MATCH` at line 56, exit 0; outputs match the retained receipts at `.ufo/waves/round-34/verification/criterion-gate-reject-r33-at-93359ff.txt:1-2` and `criterion-gate-reject-r29-at-a2fe31b.txt:1-2`. These receipts contain output and exit only, no checker hash, so this single-line mutant leaves both receipts apparently valid. Commands used the same invocation above with `--rev 93359ff0924bf622acc51eb15c2afa3cd2743022 --lesson corpus/lessons/round-33.md` and `--rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --lesson corpus/lessons/round-29.md`; observed `EXIT_CODES=1,0` for pristine, mutated and restored.

Sandbox operations/exit: cloned the lane and checked out `24a16474ee73e20453f3e1be9d2f33573c5196d9` (0); `mkdir -p /fast/scratch/hyaku/kake-r34/w2/MutGateRejectCheck/clone/corpus/lessons/gate-reject-mutation-variants` (0); committed the six fixtures with `git -C <clone> -c user.name=MutGateRejectCheck -c user.email=mut-gate-reject-check@example.invalid commit -m 'Add isolated Gate reject parser fixtures'` (0; six files); `git -C <clone> rev-parse f953ff5` (0); `sha256sum <clone>/.ufo/waves/round-34/criteria/gate_reject_check.py` returned the pristine/mutated/restored hashes above (0 each). The edit was restored and the pristine hash matches wave-1's reported final hash (`.ufo/waves/round-34/w1/ExecGateRejectCheck.md:3,27`). No tools installed. All fixture/checker mutation and runs were in scratch; only this report was written in the lane.

Process note: my initial inspection accidentally read the lane worktree copy of the checker; I made no lane edits or other lane writes. Subsequent inspection and all execution used the pinned scratch clone.
