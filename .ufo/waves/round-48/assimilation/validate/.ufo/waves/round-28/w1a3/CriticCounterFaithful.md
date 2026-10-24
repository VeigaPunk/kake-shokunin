# KakeR28a3.CriticCounterFaithful — is the C1 counter faithful to round-27 routed defect 1?

Seat: leaf critic, operability. Read-only in the lane; this report is the only lane write. Sandbox: `/fast/scratch/hyaku/kake-r28a3/w1/CriticCounterFaithful/` (TMPDIR there). Gates exported with `git archive` from a sandbox clone: base `22c1669` `scripts/citing_set.py` sha256 `3a361a00…ffc228` (the same blob as the round-27 candidate `ac46a74`), and repair `b5d423f` sha256 `28ba9965…f8f415`. No installs. No network.

## Verdict
The 11 defect checks are faithful but they are a subset. All 11 match a real round-27 failure. Every round-27 variant they skip that sits in the same code path (a FIFO reached through a symlink, other nesting depths, deep JSON in Git mode, reduced stack, `--revision=`, a Git `corpus` symlink) also holds at `b5d423f`. **Three round-27 variant families still fail at `b5d423f`.** The counter cannot see any of them:
1. **CLI-SCOPE-FALSE-GREEN, exact replay of round-27 probe P22** (CliJson F1): population `S01`,`S02`, corpus `See S01 and S02 for details.`, empty ledger. Result: **exit 0, `clean`, citingPairs 0**, the same as at base. The repair keys reachability on `_NUMERIC_ID_RE = ^S([0-9]+)$` (citing_set.py:125 at b5d423f). The scanner, however, needs `S` plus 3 or more digits (`_TOKEN_RE`, :116). So `S01` and `S1` pass the new `population_id_unreachable` check (:422) even though their own spelling is never scanned. Counter A5 tests only `X001` (c1_interface_count.py:223), a shape that has no `S` prefix and therefore cannot catch this. One mitigating fact: if the corpus spells the id as `S001`, it does count (exit 1, two `unadjudicated_citing_pair`). Treating the alias spelling as making `S01` "reachable" is a judgment the canonical judge has to make. The round-27 declared expectation (an unsupported population must not be green) still fails.
2. **Repeated options, last value wins** (CliUsage F2, B01/B04/B06/B08). Round-27 record CLI-SCOPE-FALSE-GREEN cites CliUsage as evidence. On a clean tree each of these exits **0 with `clean`** and silently drops the unusable value: `--population does-not-exist.json --population population.json`, the same pattern with `--ledger`, `--revision no-such-revision --revision HEAD` (Git source at HEAD), and `--root /nonexistent-root-xyz --root <real>`. `build_parser` (:622-630) is unchanged. One caveat on scope: the record's one-line summary names unreachable ids, absent or empty corpus, blank revision and nested root, and does not mention repeats. Repeats are inside the cited report and match the routed-defect wording ("unusable input documents must yield … exit 2").
3. **JSON-PROTOCOL "duplicate/nonfinite acceptance remains an undeclared profile"** (CliJson F8). This is still accepted silently, and the docstring still says nothing about it (`grep` finds no `NaN`, `Infinity` or duplicate-member text outside `ledger_duplicate_pair`). Observed: a duplicate `rows` member keeps the last value (exit 1 from that side effect alone); `NaN` and `Infinity` members give exit 0 `clean`; duplicate population rows give exit 0 `clean` with populationRows 3; `S001` plus `S0001` gives exit 0 `clean`. The record allows either fix: reject these inputs, or declare the profile. Neither has been done.

## Commands (all exit codes observed)
- `python3 -B variants.py gate/scripts/citing_set.py work-after > after.json` exit 0: **23/33** pass, sha256 `5f737789…7b06`.
- `python3 -B variants.py base/scripts/citing_set.py work-before > before.json` exit 0: **6/33** pass, sha256 `585b8a46…6224`. This confirms the variants are genuine failures at base.
- `cd clone && python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision b5d423f… --scratch <sandbox>/count` exit 0: **15/15** (defect checks 11/11), sha256 `65acffdf…1cd90`. This is an independent reproduction of the claimed after value.
- A direct replay of B01/B04/B06/B08 and P22 on a clean tree with the `b5d423f` gate: each run exits 0 with `clean`. Respelling the P22 corpus as `S001` gives exit 1.
- The harness, `variants.py` (sha256 `2ddae583…2960`), declares each expectation before running it. "strict" is the counter's own defect predicate (exit 2, JSON, `could-not-evaluate`, an `input_invalid` finding). "not-clean" means not exit 0 and not `clean`.

## Variant table (each variant is a round-27 probe or failure; result at b5d423f)
| Variant (round-27 source) | Counter | Base 22c1669 | b5d423f |
|---|---|---|---|
| Population FIFO / ledger FIFO, working tree (CliUsage F01/G01, CliPaths W15/W17) | covered U1/U2 | hang | exit 2 (counter) |
| Population FIFO through an in-root symlink | not covered | hang | **holds** `document_not_regular_file` |
| Ledger FIFO through an in-root symlink | not covered | hang | **holds** |
| FIFO at a subdirectory path | not covered | hang | **holds** |
| Unix socket as a document ("other special file") | not covered | exit 2 | holds `document_unreadable` |
| In-root symlink to `/dev/zero` (device class) | not covered | exit 2 | holds `path_escapes_root` |
| Deep JSON, arrays at depth 200000, population and ledger (P46) | covered U3/U4 | exit 1, traceback | exit 2 (counter) |
| Deep JSON at depths 60000/100000/150000/400000 (P46, "stack-dependent") | not covered | exit 1, traceback | **holds** `document_not_json` |
| Deep JSON, objects at depth 200000 | not covered | exit 1 | **holds** |
| Deep JSON in Git mode (`--revision HEAD`) | not covered | exit 1 | **holds** |
| Deep JSON with `ulimit -s` 256 KiB / 1 MiB / 64 MiB | not covered | exit 1 / exit 1 / exit 2 | **holds**: exit 2 all three (64 MiB parses, then `document_shape_invalid`) |
| Duplicate JSON member `rows` (P24) | not covered | exit 1, silent | **FAILS**: exit 1, silent, last value wins |
| `NaN`/`Infinity` members (P25) | not covered | exit 0 clean | **FAILS**: exit 0 clean |
| Duplicate population row (P23) | not covered | exit 0 clean | **FAILS**: exit 0 clean |
| `S001` + `S0001` alias (P36) | not covered | exit 0 clean | **FAILS**: exit 0 clean |
| Unreachable id `X001` | covered A5 | clean | exit 2 (counter) |
| `A01`,`B02` (P22b) | not covered | exit 0 clean | holds `population_id_unreachable` |
| Whitespace id `" S001 "` (P40) | not covered | exit 0 clean | holds |
| **`S01`,`S02` exact replay (P22)** | not covered | exit 0 clean | **FAILS: exit 0 clean** |
| `S1` (short digits) | not covered | exit 0 clean | **FAILS: exit 0 clean** |
| Absent corpus, working tree / Git (F5, W22, C09, P21b, P32) | covered A1/A2 | clean | exit 2 (counter) |
| Empty corpus directory (P21b "empty") | covered A3 | clean | exit 2 (counter) |
| Absent corpus with a non-empty ledger (W21) | not covered | exit 1 | holds, exit 2 |
| `corpus/knowledge` blob in Git mode (CliPaths F2 G04, P60b) | covered A4 | exit 1 | exit 2 (counter) |
| `corpus` committed as a symlink, Git mode (CliPaths G13) | not covered | **exit 0 clean** | **holds** `corpus_directory_missing` |
| `corpus/knowledge` committed as a symlink, Git mode | not covered | exit 2 | holds `not_a_directory` |
| `--revision ""` (C02, P47) | covered A6 | working tree measured | exit 2 (counter) |
| `--revision=` equals form (F08) | not covered | working tree measured | **holds** `revision_not_found` |
| `--revision HEAD --revision ""` | not covered | working tree measured | holds |
| `--revision "   "` | not covered | exit 2 | holds |
| Nested Git root, wrong corpus (AttackCase01 F3 P) | covered A7 | wrong surface | exit 2 (counter) |
| Nested root, top-level population differs (P/AE: documents read relative to the top level) | not covered | **exit 0 clean** | **holds** `root_not_repository_top_level` |
| **Repeated `--population`/`--ledger` (B01/B04)** | not covered | exit 0 clean | **FAILS: exit 0 clean** |
| **Repeated `--revision` bad,HEAD (B06)** | not covered | exit 0 clean | **FAILS: exit 0 clean** |
| **Repeated `--root` bad,real (B08)** | not covered | exit 0 clean | **FAILS: exit 0 clean** |
| (my extension, not a round-27 probe) Corpus holding only an empty `.gitkeep`, empty ledger | not covered | clean | exit 0 clean (the gate counts 1 file) |

Not counted against the repair, because each is a different routed defect or outside defect 1: `--help` with no JSON (CliUsage F5), prefix abbreviations (F6), mixing `--selftest` (F7), the `error` key on exit 64 (F8), Git mode dropping `path` (CliJson F5), mode asymmetry for a symlinked document (CliPaths F3; at base it already exits 2, not a false green). IDENTITY-PATHS and ORACLE-GRANULARITY are routed separately.

## Impacted axes and smallest safe corrections
- Operability: the C1 claim of "15/15" holds for the counter but is a **subset count**. Do not read it as "routed defect 1 closed".
- The counter's A5 tests a shape without the `S` prefix only, which is the easier case. The faithful round-27 replay (`S01`) still fails.
- Gate fix: require population ids to match the scanner's own token, `^S[0-9]{3,}$`, otherwise `population_id_unreachable`. Reject any repeated valued option with exit 64 (for example, `GateParser` checks `argv` for a repeated `--root`, `--revision`, `--population` or `--ledger`). Either `object_pairs_hook` and `parse_constant` reject duplicate and non-finite input, or the docstring declares the accepted profile.
- Counter fix: add P22 (`S01`), B01, B06 and B08 on a clean tree, plus P24 and P25, as defect checks, and keep the existing controls.

## Not verified
- Character devices other than via a `/dev/zero` symlink (I had no unprivileged mknod).
- A writer-held FIFO.
- Time-of-check races.
- Any machine other than this host (Python 3.14.8).
- The 29-fixture selftest beyond the counter's K4 check (which passed).
- I did not re-run `c1-before.json` at base. My base numbers come from my own harness only.
