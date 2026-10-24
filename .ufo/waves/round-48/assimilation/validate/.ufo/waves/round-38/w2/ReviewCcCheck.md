# ReviewCcCheck — operability

## Findings (severity order)

1. **Low — name-based false pass (documented limitation).** `control_consequence_check.py:128-137` classifies controls by path/name; `:95` and `:254-258` only count non-control receipts named `c<N>-*` or `claim-*` as violations. Using identical 20/20, `met:true`, counter-`a` JSON:
   - `timeout 30 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --verification /fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/fixtures/canonical` → exit 1; `VIOLATION: c2-at-run.json`.
   - Same command with `fixtures/renamed-control` (control renamed `shortcut.json`) → exit 0; no control recognized.
   - Same command with `fixtures/renamed-claim` (claim renamed `measurement-c2.json`) → exit 0; reports `met (not a claim receipt)`.
   Verdict: **overstated** if interpreted as name-independent; it holds for the declared naming convention and the current tree. This escape is explicitly disclosed in `corpus/QUALITY.md:945-947`.

2. **Low — `met`/tally disagreement (conditional on inconsistent receipt data).** C2 declares `met: passed >= 20 of 20` (`SCORECARD.md:2218-2221`); v3 sets `met = len(rows)==20 and passed>=20` (`sealed_count_v3.py:64-66,270-274`). The check only type-checks `met` (`control_consequence_check.py:159-166`) and trusts it (`:251-258`), despite `passed/cases/target` being present.
   Exact fixture command template (substituting `DIR`): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/tmp; set +e; timeout 30 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --verification /fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/fixtures/DIR; rc=$?; printf 'EXIT=%s\n' "$rc"; exit 0`. `DIR` results: `canonical`→1, `renamed-control`→0, `renamed-claim`→0, `control-met-false-high`→0, `control-met-true-low`→1, `claim-met-true-low`→1, `claim-met-false-high`→0.
   Verdict: **overstated** as an independent predicate check; these fixtures contradict the producer invariant, and I found no such mismatch in the sampled committed receipts. Wave-1 author report already records no `met`/`passed`/`target` cross-check (`w1/ExecQualityJCheck.md:75-77`).

## Executed checks

- Sandbox checkout: `mkdir -p /fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/clone && git -C /fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/clone checkout -q adab4c7e9ec2178657395f49346f18800ff4796f`; confirmed `git rev-parse HEAD` → `adab4c7e9ec2178657395f49346f18800ff4796f`.
- `export TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/tmp; timeout 120 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --selftest` → exit 0, `selftest: 10/10 ok` (matches `criteria/receipts/ccc-selftest.txt:1-12`).
- Ran these three commands separately (same `TMPDIR` export): `timeout 120 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --root . --revision 99357694f68886d3175fc6c386979c350be789bc --verification .ufo/waves/round-36/verification` → exit 0 (`PASS`, tainted 0); `timeout 120 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --root . --revision 99357694f68886d3175fc6c386979c350be789bc --verification .ufo/waves/round-37/verification` → exit 1 (`FAIL`, two named violations); `timeout 120 python3 .ufo/waves/round-38/criteria/control_consequence_check.py --root . --revision 99357694f68886d3175fc6c386979c350be789bc --verification .ufo/waves/round-38/verification` → exit 0 (`PASS`, tainted 1, violations 0). Outputs match `criteria/receipts/ccc-r36-at-99357694.txt`, `ccc-r37-at-99357694.txt`, and `ccc-r38-at-99357694.txt`.
- R38 output: 143 receipts, 18 controls, one skipped; v2 counter `52da…` is tainted by four controls, while met mutant/reference receipts are not violations; v3 counter `28b1…` has four 20/20 `v3/Ctl*` notes, not taints. The real C2 receipt is 20/20, target 20, met true (`verification/c2-at-3ed8e15c.json:3-11`). Current result therefore follows the check's declared name/class rules; whether C2's `v3` class disposition is valid is not decided here.
## Residual risk and verification gaps

- Selftest gap: its “violation list names the claim receipt” assertion filters parsed `Receipt` objects (`control_consequence_check.py:377-381`) rather than captured report text. Direct canonical fixture run did print the violation line; future output regressions could still pass this selftest.

## Evidence and limits

- LSP unavailable: `read xd://lsp` returned “No such tool” (mounted devices were `ast_edit`, `debug`); reviewed source line evidence directly. No network requests or tools installed.
- Checker SHA-256 `d8415484cb39b55c9347ad2b94e0b6d097fcb6e2544a7c94f99d2d267edf6ee2`; `ccc-selftest.txt` `d63fce2dfd3c73e1a27fa7c4f2e60b71ef968127476cccc76cb8d3ec18cee33d`; r36/r37/r38 receipt hashes respectively `f4fcbcf347d6f03b8081c326b670008b359860391a2f10fecaa9bb2af006ce8c`, `b157d67b350aa5997cd6fcd078781addfa384a4177746e346096fcc6528dafa1`, `f1d8111be6e2dad051791470c1570a29c72a209c7649a4a6a6d3bb5f7cef42ab`.
- Fixture directory: `/fast/scratch/hyaku/kake-r38w2/ReviewCcCheck/fixtures/`. Identical 20/20 `met:true` JSON files: SHA-256 `87ea9bbfaad315bab0ac205ddc255f2e743b3b88b705c36e204c9c5cce37e265`; 19/20 `met:true`: `534a60bca7b1d097d02750a16c13ac5aace9568a956662691f87d3599950eb89`; 20/20 `met:false`: `bdd371d606a18168a2f8718e3ee6e5103f8a9c318d6648cef47f8535f95834fa`.
