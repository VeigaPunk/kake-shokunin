# Round 38 W2 — source_recheck caps review

Axes: operability; freshness. Scope: the 16 MiB body cap and MemoryError handling, reviewed against the round-36 C1 contract. Sandbox clone: `/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/clone` at `adab4c7e9ec2178657395f49346f18800ff4796f`.

## Findings

- **P2 — Oversized-body error output violates contract (g).** `source_recheck.py:604-613` emits `check_invalid` inside `evaluate_check`; `main` increments `evaluated` before calling it (`:750-755`). A 16,777,217-byte body with a valid permanent redirect + 200 produced exit 2, `checksEvaluated: 1`, and both `moved` and `check_invalid`. Round-36 SCORECARD lines 1649-1653 require one `check_invalid`, no other finding for that check, and exclude invalid checks from `checksEvaluated`. The new selftest explicitly leaves this field unpinned (`source_recheck_hardening_selftest.py:218-222`); the round-36 counter does not compare it (`sealed_count.py:23-26`). Thus the counter pass does not close this defect.

## Attacked statements and verification

- **Bounded body read / large-body handling — holds for bounded consumption; overstated for full contract output.** Hardening selftest: 9/9, exit 0; includes g33 and sparse 1 GiB g34. Code reads at most `MAX_BODY_BYTES + 1` (`source_recheck.py:603-613`). The reproducer above falsifies the claimed single-finding / zero-evaluated result. Exact-cap 16,777,216-byte body was processed (exit 1, `moved` + `quote_missing`), consistent with “larger than” cap.
- **MemoryError while parsing a near-cap manifest — holds in the tested constrained run.** 62,914,607-byte manifest under 512 MiB `RLIMIT_AS` returned JSON `input_invalid`, exit 2; source catches `MemoryError` from decode/`json.loads` (`source_recheck.py:669-680`).
- **Round-36 functional behavior — holds on the sealed counter, with the field gap above.** Functional selftest 106/106, exit 0; round-36 counter 28/28, `met: true`, exit 0.

Commands (run from the sandbox clone; each explicitly unset inherited Git variables):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/tmp timeout 900s prlimit --as=4000000000 python3 -B scripts/source_recheck_hardening_selftest.py  # exit 0; 9/9
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/tmp timeout 900s prlimit --as=4000000000 python3 -B scripts/source_recheck_selftest.py  # exit 0; 106/106
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/tmp timeout 900s prlimit --as=4000000000 python3 -B .ufo/waves/round-36/sealed_count.py --tool-file scripts/source_recheck.py --key-revision fd1fb723  # exit 0; 28/28
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60s prlimit --as=4000000000 python3 -B scripts/source_recheck.py --manifest /fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/oversize-redirect.json  # exit 2; checksEvaluated=1, moved + check_invalid
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180s prlimit --as=536870912 python3 -B scripts/source_recheck.py --manifest /fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/near-cap.json  # exit 2; JSON input_invalid
```

Evidence hashes: tested `source_recheck.py` `6629d8000ac661ef7340137dc026cbdcc79ab0c81d845ed499376b4c1b0f9c6b`; hardening selftest `2358206b5226648ffd8cfa2af1eb8dafbb49d7ebf2d99b4dba919664b9ac2a81`; repro manifest `/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/oversize-redirect.json` `ec82edacdb6ee6dffe0e4f386d922ddb2f85fbf9b4af4f99337ddf3fa3dc2b30`; sparse body `/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/oversize.bin` (16,777,217 bytes) `1003b1b5dc078189799a1216ce0f9fbcebb94e8b6b83c58c4b03345f07f94ced`; near-cap manifest `/fast/scratch/hyaku/kake-r38w2/ReviewRecheckCaps/near-cap.json` `70dfff9864241dd760d3f2e0759a4b07f699d441f65c7adcbad86a5dd24305df`.

## Residual risk / gaps

No `lsp` device/server was available (`read xd://lsp` reported “No such tool”; only `ast_edit` and `debug` were mounted), so no LSP status/references/definition/diagnostics were possible. Used direct source and SCORECARD line reads; the literal grep only located the contract heading. No network was used; the audited tool is offline. The sealed counter and its 28-case predicate do not verify `checksEvaluated`.

Report: `.ufo/waves/round-38/w2/ReviewRecheckCaps.md`
