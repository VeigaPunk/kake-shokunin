# RerunC2Sealed — round 35 wave 2 (falsify)

Attacks C2's measured values: re-ran the sealed C2 counter (v2 at four revisions, v1 at
95abec21) in a fresh clone at 7deacc4629c1d05a34fb919d8095e99efc7b712f and compared
field-by-field against the lane receipts. Result: **no deviation — claims reproduce exactly**.

## Sandbox
- Clone: /fast/scratch/hyaku/kake-r35/w2/RerunC2Sealed/clone (git clone of the lane,
  checkout 7deacc4629c1d05a34fb919d8095e99efc7b712f; EXIT=0)
- TMPDIR: /fast/scratch/hyaku/kake-r35/w2/RerunC2Sealed/tmp
- Runs output: tmp/c2-at-<rev>.run.json, tmp/c2-v1-at-95abec21.run.json (no stderr bytes)
- Span tool: tmp/probe_spans.py (mirrors sealed_count.py run_c2 load/clean/normalize)
- No tool installs needed (python3 present; no channel-use recorded)

## Commands and exit codes (all run from clone root, `python3 -B` with key-revision
4c6be2bdec5630166c4013e53c226b1119ec63cc)
| rev | v2 exit | met | probesPassed | receipt match |
|---|---|---|---|---|
| 16a6b8b8 | 1 | false | 0/12 | EQUAL |
| bd14096a | 1 | false | 0/12 | EQUAL |
| b1cbbc39 | 1 | false | 0/12 | EQUAL |
| 95abec21 | 0 | true | 12/12 | EQUAL |
| 95abec21 (v1 sealed_count_v1.py) | 0 | true | 12/12 | EQUAL |

Field-by-field diff of run JSON vs verification/c2-at-<rev>.json and
c2-v1-at-95abec21.json: the only differing key is `keySource` (`revision 4c6be2bd` in
receipt vs `revision 4c6be2bdec...` in run — verbatim CLI arg spelling, same revision).
All other fields identical: revision hash, counterSha256 (v2 1b4d9d…, v1 c4d58d…),
entrySha256 0b5ac7e83a622045a3c1a528e25c042ecb400b46309a09660ac0b500e6c0c397, words 1388
(v2) / 1298 (v1), copiedShare 0.0, pinnedTextsIntact true, 11 citedIds, 8 goodCites
(S078-S080, S082-S086), all five conditions, perProbe all true at 95abec21. Exit-2 guards
(unresolved rev, key sha256 pin 111bceea…, key visible at measured rev) never triggered.

## Per-probe match spans at 95abec21 (normalized text, len 8692; P01-P12 all PASS)
- P01 span=(154,179) `'/.well-known/security.txt'`; lines 1/16/21
- P02 (regex[1]) span=(3165,3213) `well-known copy must be used (s078), so the root`; line 28
- P03 span=(3506,3635) `text/plain` with default charset `utf-8` (s078)… bytes are utf-8`
  (crosses line boundary; no single-line hit)
- P04 span=(3885,3906) `contact` is mandatory`; line 44
- P05 span=(4173,4208) `expires` is mandatory, exactly once`; line 48
- P06 span=(4243,4262) `shorter than a year`; line 120
- P07 span=(4213,4221) `rfc 3339`; line 48
- P08 span=(4118,4139) `ordered by preference`; lines 47/118
- P09 span=(4805,4818) `never the key`; line 57
- P10 span=(4872,4889) `openpgp cleartext`; line 59
- P11 span=(5290,5319) `not its parents or subdomains` (crosses lines; no single-line hit)
- P12 span=(6039,6061) `include: [".well-known"`; line 81

## Findings
1. [CONFIRMED] C2 measured values at all four revisions reproduce byte-identical JSON vs
   the receipts (modulo the cosmetic keySource arg spelling). Exit codes match (1,1,1,0,0).
2. [CONFIRMED] v1 and v2 agree on met=true at 95abec21 and on all probe outcomes; word
   counts differ per the v1/v2 counting rule (1298 vs 1388), both under their caps (1500/2200).
3. [IMMATERIAL] P03/P11 only match across line boundaries in normalized text, so no single
   entry line satisfies them in isolation; the global spans above are the evidence.

## Not verified / gaps
- Did not run with --key-file or against any other revision set (out of scope of the item).
- Probe spans are from my mirror script, not from the counter itself (the counter emits only
  passed/not); the mirror copies the counter's load/clean/normalize logic exactly and its
  pass/fail per probe agrees with the counter's perProbe in all five runs.
- No live network or owned-site access used; all data read via git show in the sandbox clone.
