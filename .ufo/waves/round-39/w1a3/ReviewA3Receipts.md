# Round 39 attempt 3 — control receipt audit (seat ReviewA3Receipts, wave 1)

Scope: all 14 receipts `.ufo/waves/round-39/verification/a3/*.json` at `72edf2123f92b9dc546494cbffcc777ed3c3cd3a` (lane tip, verified `rev-parse HEAD`) plus the 12 copies `.ufo/waves/round-39/a3-controls/dead-w1/*.py`, checked by content against the frozen counter at `ceecb1b1f9093471eb0b17d2c9190e78bceb0b78`. The counter was never run; the key was never opened or read; `shared/reference.py` was only hashed, never opened. No tools installed (tooling directive: nothing needed).

Anchors, independently computed:
- counter sha256 at `ceecb1b1` = at `72edf212` = worktree = `f3a0cd6053497cd05b6a57ab712552146960c1efe2f8fb50eee36bace6084593`; every receipt's `counterSha256` matches.
- `KEY_SHA256` pin inside the counter = `16440f62803e25fee5e17e77bae88636fa0c711b0fa26024ec78d4134767c10b`; every receipt's `keySha256` matches. `PREDICATE = "met: passed >= 24 of 24 sealed cases"`, `CASES = TARGET = 24` — every receipt's fields match.
- reference original `/fast/scratch/hyaku/kake-r39w1/shared/reference.py` sha256 = `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8` (matches SCORECARD pin `663e051e…2d69f8`).
- `scripts/sitemap_audit.py` absent at `915e9e87dd64cbcf8bad107e476520707efe4d27` and at `72edf212` (`git ls-tree` empty for both).

Per-receipt verdicts (all checks: toolSha vs scored bytes; counterSha; keySha; predicate/cases/target; 24 rows k01–k24; passed = count of `pass:true`; `met == (len(rows)==24 and passed>=24)`; `.exit` vs counter semantics; worktree == blob; copy == /fast original):

| receipt | label | toolSha | rows | passed | met | exit | copy==orig | verdict |
|---|---|---|---|---|---|---|---|---|
| c1-at-915e9e87.json | at-915e9e87 | null + rev `915e9e87dd64…`, tool absent, toolFile null | 24 | 0 | false | 1 | n/a | holds |
| ref.json | ref | == sha(`shared/reference.py`) | 24 | 24 | true | 0 | n/a | holds |
| dead-CtlCodeGuess.json | dead-CtlCodeGuess | == copy == orig | 24 | 23 | false | 1 | yes | holds |
| dead-CtlXsdDelegate.json | dead-CtlXsdDelegate | == copy == orig | 24 | 19 | false | 1 | yes | holds |
| dead-CtlRegexOnly.json | dead-CtlRegexOnly | == copy == orig | 24 | 19 | false | 1 | yes | holds |
| dead-CtlShallowStdlib.json | dead-CtlShallowStdlib | == copy == orig | 24 | 13 | false | 1 | yes | holds |
| dead-CtlFirstFinding.json | dead-CtlFirstFinding | == copy == orig | 24 | 12 | false | 1 | yes | holds |
| dead-CtlLabelIds.json | dead-CtlLabelIds | == copy == orig | 24 | 7 | false | 1 | yes | holds |
| dead-CtlConstClean_manifest_only.json | dead-CtlConstClean_manifest_only | == copy == orig | 24 | 6 | false | 1 | yes | holds |
| dead-CtlNoReader.json | dead-CtlNoReader | == copy == orig | 24 | 5 | false | 1 | yes | holds |
| dead-CtlConstClean.json | dead-CtlConstClean | == copy == orig | 24 | 5 | false | 1 | yes | holds |
| dead-CtlConstError.json | dead-CtlConstError | == copy == orig | 24 | 4 | false | 1 | yes | holds |
| dead-CtlJunk.json | dead-CtlJunk | == copy == orig | 24 | 2 | false | 1 | yes | holds |
| dead-CtlConstFindings.json | dead-CtlConstFindings | == copy == orig | 24 | 1 | false | 1 | yes | holds |

`passed` of every dead control equals the SCORECARD pre-wave record (CodeGuess 23 … ConstFindings 1); none meets the predicate.

Copy == original, full sha256 (committed copy at `72edf212` is byte-identical to its `/fast/scratch/hyaku/kake-r39w1` original; worktree copy also equals the blob):
CodeGuess `1d0a5d9f1ff859b1b7ba403b4ee4e5e775306de24103902bb27c10b590958448`; ConstClean `46ea5079e7b5428d489a86c68de2fb5797d6f9f090eb99ae63d0f412962574a6`; ConstClean_manifest_only `b68ba5c6dddb320371fae3cde91a4dc144368348be253c8b3c675f26723ca819` (orig `CtlConstClean/control_manifest_only.py`); ConstError `e22e179e540ab347974cd77da21657476d793d87b9f98698dd054231e67e2670`; ConstFindings `9c2d48248440e6df66710e8da23e73bde3ff3c031e49fb235f0934bb377a4e16`; FirstFinding `59a31e22ff6d433c326d49c90fe734f8b746d6b0f83c39a71177a35e2c32c018`; Junk `fc7b986da7f613e072a9bc7e7f2776c0b3e57708ff645ccf58ee5b5303a5545c`; LabelIds `dab8a8824229d288be94898bef4ac9449e9e1f774f13ec8d630420b06dd167be`; NoReader `fad57c529e440aa783ff0bb941da93206fbeb94fe6211c44386ece08e3d16808`; RegexOnly `b7667eaf223caf1045f2e5298f8759205dc5703f7a8bfea1cf66930b93d21871`; ShallowStdlib `0aee6bca740cb23f8130013dc10451606b8f4d017120ec3bfc3c0cd67541c3c5`; XsdDelegate `72a614fc9adf992877cd40f24ee8d59e8bd46f4a4071ae968d5250dfaa5bfa14`.

Commands (exit codes): `git ls-tree -r --name-only 72edf212… -- .ufo/waves/round-39/verification/a3/ .ufo/waves/round-39/a3-controls/ .ufo/waves/round-39/sealed_count.py` → 0; `git show ceecb1b1…:.ufo/waves/round-39/sealed_count.py | sha256sum` (and same at `72edf212…`) → 0; `timeout 300 python3 /fast/scratch/hyaku/kake-r39a3w1/ReviewA3Receipts/verify.py` → 0, output ends `ALL CHECKS HOLD for every receipt.` (first run exited 1 from two script-side misreads only — receipts record `toolFile` as a lane-relative path to the copy, and the counter's tool-absent path exits 1, not 2; script fixed, no receipt affected); `sha256sum` of the 12 copies and 12 originals → all pairs identical (exit 1 only because the glob also hit `CtlSandboxProbe`, `MutRootEntries`, `shared`, which have no `control.py` and no receipts — expected).

Findings: none. Two non-defect observations: (1) every `dead-*.json` names the committed copy via lane-relative `toolFile`, i.e. the counter scored the committed copy bytes; the sha256 identity with the `/fast` originals closes that chain. (2) `c1-at-915e9e87.json` has `note="tool absent"` with `.exit` 1 — exactly the counter's `finish(1)` tool-absent path (`finish(2)` is reserved for cannot-evaluate notes); its `toolSha256` is null and the tool is verified absent at that revision.

Residual risk / gaps: the counter was not re-run (forbidden — needs the key), so row-level `pass`/`why` values are taken as counter output and checked only for internal consistency, exit-file consistency, and agreement with the SCORECARD record; `ref.json` rests on `/fast/scratch/hyaku/kake-r39w1/shared/reference.py` still being the bytes scored (sha matches the receipt and the SCORECARD pin). No LSP was applicable (data-only audit).
