# MutC1Counter

ATTACKS:
- C1 counter v1 at the frozen bytes `1ea305904933ac0f57e84ac1e7a8207e486f577d`; generated 25 one-point mutants in isolated scratch copies.
- Axes: C1 structural detection (member census/registry/command/labels), calibration score, revision verdicts, selftest sensitivity.

MUTANTS:

Commands run per mutation (from scratch clone; output captured by the harness):
- `python3 -B <mutant> --selftest --work /fast/scratch/hyaku/kake-r60/MutC1Counter/work`
- `python3 -B <mutant> --root /fast/scratch/hyaku/kake-r60/MutC1Counter/clone --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --work /fast/scratch/hyaku/kake-r60/MutC1Counter/work --jobs 24 --json`
- Same command with revision `97cdc122379711c2b02a8970752c8782da3ac81d`.

Pristine controls: `--selftest` → exit 0, `selftest 76/76 passed`; B1 → exit 0, `members=28 mismatches=0 scores_held=3/3 met=True`; base → exit 1, `members=28 mismatches=14 scores_held=3/3 met=False`.

`selftest` exit 1 = detected (killed); exit 0 = survived. B1/base columns are actual process exit codes. A survivor may leave the overall revision verdict unchanged because other defects continue to fail the predicate.

| Mutant | Behavior point changed | Selftest | B1 | Base | Mutant SHA-256 |
|---|---|---:|---:|---:|---|
| M01 | Predicate forces `met=True` | 1 | 0 | 0 | `293a3a7b83af56232d9c7b27eb4acb55d266adc51bc30d979d668ffd27bdb3e2` |
| M02 | Member count accepts any count | 0 | 0 | 1 | `d82eb4d02fce006c97717fd7f20a6e6c7f074aaaef17c0ab456d019d8fa409bf` |
| M03 | Frozen member blob-id mismatch ignored | 1 | 0 | 1 | `0c856889cdc4590a016b28561bdc0427679fbd0df16a67955311226614d3c78b` |
| M04 | Non-regular member mode accepted | 1 | 0 | 1 | `213d96a94e8a7939cbff800349fef19d293f709a7d37cf67fa1431ba3cae113a` |
| M05 | Extra population members ignored | 1 | 0 | 1 | `f20aadf7ce6832d1a294a5ee1577593221c485a56dbfc12ac48e8d35e8b234c1` |
| M06 | Missing registry row falls through | 1 | 0 | 1 | `d7ca69d16335dea01575c9d09ed9808d53b2a6cc4b4f0ec28a2551d7531dec94` |
| M07 | Duplicate registry rows ignored | 1 | 0 | 1 | `4f1b84d7ad4f81845ab57b168a07f00534513d1f83ef36a09788631990bcc4d7` |
| M08 | Row cell count requirement removed | 1 | 0 | 1 | `d2dae667b6fe8f15c195cfd74eb405f25bc45c45ae430c8c0701779b0aa58a84` |
| M09 | Verdict-map requirement removed | 0 | 0 | 1 | `940a393badac80ee18c049887de20153c05a7902990e448fcc82d1e5d1b2ae8f` |
| M10 | Historical label never recognized | 1 | 1 | 1 | `e5bbd0a48419eb503ce7e264201aa5d9a6dede7b44e0636d1558c143e34acf33` |
| M11 | `never met` label never recognized | 1 | 1 | 1 | `f354747023b9527d6bb81add72c0c489bd6e0a5119f46f4f4a262afb8888ca20` |
| M12 | Pin ancestry check always succeeds | 1 | 0 | 1 | `207f432db3afad68556b1d11a78e2f81d521edfa5e48f40e2367ecf590f1ab72` |
| M13 | Live exit never mismatches | 1 | 0 | 1 | `fc04fadb7cbf9beecf0737ed4d01e35513eb396873285ef14063b5c6e526ab92` |
| M14 | Historical green-tip mismatch suppressed | 1 | 0 | 1 | `e7254d760690234a2e63be7187126350444792f5d0d39b23011c919d3da19c42` |
| M15 | Historical pin-exit mismatch suppressed | 1 | 0 | 1 | `ff072a14537b4dc9ea0dfb1be568e9c28fdae88566b9d79149c006559798787f` |
| M16 | Multiple scorecard axis tables accepted | 1 | 0 | 1 | `19b6af210c722bbe417db1db45d281e6964e4a4e1dde1ba9a5a0fc26c36b8709` |
| M17 | Duplicate axis rows accepted | 1 | 0 | 1 | `50ffe6b24e3e2683cf24e1732a54ae35d003557cc6484eaa5e8f017c0d8674a3` |
| M18 | Any score value accepted | 1 | 0 | 1 | `527aeffc87d2aee7422910d902bd5087e7bddc689a71c33479758d20ec91fa04` |
| M19 | Axis name casefold removed | 1 | 0 | 1 | `e1dae20c73afcd91f30ff4d120936c0a2e66bcdca62bdc734b4a773d860f9f5d` |
| M20 | Command environment validation removed | 1 | 0 | 1 | `3ab5288c469b479aa172f1fbd8af5a35d56cec4f90ea1f111cbfa62d6967d23a` |
| M21 | Revision placeholder accepted only if absent from allowed tuple | 1 | 1 | 1 | `4c02563b26a1ea727b0a05be7c965c53e6654052c5f36057a43af35ee0db1c8c` |
| M22 | `--selftest` permitted in documented command | 1 | 0 | 1 | `97095564c1d0288cbf5b3626591457ddd98f247e21441e54ba4784989bc8db6c` |
| M23 | Invalid `--root` value accepted | 1 | 0 | 1 | `cd4d692ec45b29d6c0d3300d2562823765492493aac09e4ab73d4903b3f3ca44` |
| M24 | Git/Python/KAKE environment scrub removed | 1 | 0 | 1 | `4116eae095050b75582681bc9dfef3ebe8f80c9459abfbdcad169a16fa67afa` |
| M25 | Timeout extended from 1800 to 18000 seconds | 0 | 0 | 1 | `33fc9c0d06f24251ab08880545dae80fc13d9c21693dccbb5b9581cb67190415` |

M06 and M21 selftests exited 1 by raising exceptions rather than printing the normal tally: M06 `IndexError: list index out of range` after removing the unregistered early return; M21 `KeyError: 'tip'` after its documented command becomes unparsable. Both are detected, though the fixture assertion is not exception-safe. For all other killed mutants, the selftest returned its normal failure status. Survivors are M02, M09, M25; their actual B1/base exits remain 0/1 respectively.

SURVIVORS:
- **M02 — member-count predicate blind spot.** Counter selftest exit 0 despite changing the final cardinality condition to `len(present) >= 0`. Its D fixture has 27 members, but the missing member also contributes `member_missing`, so the aggregate mismatch independently keeps exit 1; it never isolates the cardinality gate. B1/base exits 0/1.
- **M09 — verdict-map blind spot.** Counter selftest exit 0 when the `0=`/`1=` requirement is removed. The junk-row fixture used for `row_incomplete` has only seven non-empty cells, so the cell-count condition still catches it. B1/base exits 0/1.
- **M25 — timeout policy blind spot.** Counter selftest exit 0 when timeout is increased 10x. No fixture member hangs or times out; B1/base exits 0/1.

CASES TO ADD:
- M02: fixture with all 28 frozen member blobs present and unchanged, all rows/labels/commands valid, then force `present` to 27 by deleting one frozen path; assert exit 1 specifically because `members != 28` while there are zero member-level structural mismatches. Or factor predicate testing and assert the 27 count fails independently.
- M09: exactly eight non-empty registry cells, one valid command and all otherwise valid data, but the `Verdict map` cell contains neither `0=` nor `1=`; assert `row_incomplete`.
- M25: invoke a synthetic member that sleeps beyond a test-injected short timeout; assert observation returns 124 and is classified as a mismatch. Use an injectable short timeout in selftest, not a 30-minute wait.

FINDINGS:

| Severity | Target file:line | Issue | Evidence command | Fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/c60_gate_status.py:903-915` | The 27-member case asserts `member_missing`, making the aggregate failure independent of `len(present) == 28`; M02 survives. | `python3 -B <M02 mutant> --selftest --work <scratch>` → exit 0 (`76/76`); M02 B1/base exits 0/1. | Add isolated cardinality assertion/case with no other mismatch classes. |
| medium | `.ufo/waves/round-60/c60_gate_status.py:435-439` | The malformed-row test's seven-cell failure masks removal of verdict-map validation; M09 survives. | `python3 -B <M09 mutant> --selftest --work <scratch>` → exit 0 (`76/76`); M09 B1/base exits 0/1. | Add an eight-cell row with an empty/invalid verdict map. |
| low | `.ufo/waves/round-60/c60_gate_status.py:392-409` | No selftest exercises the timeout return/classification; a 10x timeout mutant survives. | `python3 -B <M25 mutant> --selftest --work <scratch>` → exit 0 (`76/76`); M25 B1/base exits 0/1. | Exercise with a configurable short test timeout and sleeping fixture. |

Restoration: the lane counter and frozen counter were never edited. Before/after SHA-256 of the pristine scratch-clone counter was `613cc4bb6ebf9572d50f4d1060a1522e80288d8a8084d89a4c693873108fffc3`; it matched `git show 1ea305904933ac0f57e84ac1e7a8207e486f577d:.ufo/waves/round-60/c60_gate_status.py`. Mutations were separate files, not applied over the pristine bytes. Scratch cleanup performed after copying cited results into this report.

VERDICT: C1 v1 selftest kills 22/25 mutants; three survivors expose missing isolated coverage for member-count gating, verdict-map-only validation, and timeout behavior; pristine controls match B1 met/base not met.
