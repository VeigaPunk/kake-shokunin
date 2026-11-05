# ExecC2Mutants — round 94 C2 mutant kill count (v1 vs v2)

VERDICT: C2 not met as frozen: v1 killed 31/40 (matches the round-93 receipt, survivors M11 M18 M19 M24 M28 M29 M32 M37 M40); v2 killed 39/40 against the frozen target 40/40. The sole v2 survivor, M11, is a semantically equivalent mutant (115200/115200 exhaustive input cases agree), so no counter over this population can kill it; the target is unattainable as written. Base candidate scores met=true under both counters.

## Scope and what was run

- Lane revision: `ba667b245f26125c13885958498b3b4999756d04` (freeze commit). LANE was not written; no git mutation in LANE.
- Scratch clone (`git clone -q --shared`, detached at ba667b24, `rev-parse --show-toplevel` = clone path, verified before every commit). Clone and scratch dir deleted before yield; the receipts below are copies.
- Mutant base: the patch list (`.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`, `base.sha256` 0fe018a8…868e4) names `.ufo/waves/round-93/frozen/pos-good.py` as the base source for `scripts/conditional_eval.py`. The clone commit at ba667b24 does not carry that file (see Defect D1), so I created one clone-only baseline commit `6d75ee0c2d893b67315cdef42855f68a48606707` = ba667b24 tree with `scripts/conditional_eval.py` replaced by pos-good bytes (sha256 verified 0fe018…). Each of the 40 mutants is a detached child of that baseline commit (one file changed, per mut94.py).
- Driver: `receipts/mut94.py` (adapted from round-93 `mut.py`: COUNTERS = {v1: c93_conditional.py, v2: c94_conditional.py}, both scored for every applied mutant, `--work` per run `works/<v>/w-<id>`). Command: `CAND_REV=ba667b24… JOBS=6 python3 -B mut94.py mutants-posgood.json <clone> 6d75ee0c… <works> <out>` → exit 0, log `receipts/run.log` (`v1 killed=31/40`, `v2 killed=39/40`, `applied=40 rejected=0`), wall 295 s.
- Every find string applied exactly once on the base (`base_find_count=1`, 40/40 APPLIED; zero PATCH-NOT-UNIQUE, zero COMMIT-FAILED).
- Killed = counter exit nonzero. Records: `mutants-v1.json`, `mutants-v2.json` (per mutant: id, clause, status, rev, base/candidate find counts, exit, line 1, killed, first failing case, stderr head).

## Base candidate (ba667b24, no mutation) — `base-candidate.txt`

- `python3 -B .ufo/waves/round-93/c93_conditional.py --root <clone> --revision ba667b24… --work <w>` → exit 0; line 1: `C2v93 revision=ba667b24… candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true`
- `python3 -B .ufo/waves/round-94/c94_conditional.py --root <clone> --revision ba667b24… --work <w>` → exit 0; line 1: `C2v93 revision=ba667b24… candidate=present hand=53/53 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true`
- Both match the frozen controls `controls/base-c2-v1.txt` (44/44) and `controls/base-c2-v2.txt` (53/53) line 1. Candidate sha256 in the counter detail: d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e (`receipts/base-v{1,2}.stdout`).
- Observed instrument digests: `c94_conditional.py` 357d8cd1…d2a750a (matches freeze); `c93_conditional.py` fee28ea0…dd55a3 (not pinned by the freeze; `receipts/instrument-sha256-observed.txt`).

## Results (`summary.txt`)

```
v1 killed=31/40
v2 killed=39/40
v2 not killed: M11
```

v1 survivors: M11 M18 M19 M24 M28 M29 M32 M37 M40 — identical to the freeze's list of surviving classes.
v2 kills the eight non-equivalent survivors (M18, M19, M24, M28, M29, M32, M37, M40) via the nine v2 successor cases, and kills all 31 v1 kills again.

Per mutant (v1 exit / v2 exit; v2 first failing case, from JSON detail):

| id | clause (short) | v1 | v2 | v2 first failing case |
|---|---|---|---|---|
| M01 | 5/8 If-Match uses weak | 1 | 1 | ifmatch/weak-tag-no-strong-match |
| M02 | 5/10 If-None-Match uses strong | 1 | 1 | inm/weak-member-matches-strong-current |
| M03 | 5 strong ignores current weakness | 1 | 1 | ifmatch/strong-vs-weak-current |
| M04 | 5 strong ignores request weakness | 1 | 1 | ifmatch/weak-tag-no-strong-match |
| M05 | 4/8/10 `*` always present | 1 | 1 | ifmatch/star-without-representation |
| M06 | 4/10 `*` never matches | 1 | 1 | ifmatch/star-with-representation |
| M07 | 10/11 IMS evaluated with INM | 1 | 1 | inm/precedes-if-modified-since |
| M08 | 8/9 IUS evaluated with If-Match | 1 | 1 | ius/ignored-when-if-match-present |
| M09 | 7 cache: If-Match not skipped | 1 | 1 | ifmatch/skipped-for-cache |
| M10 | 7 cache: IUS not skipped | 1 | 1 | ius/skipped-for-cache |
| M11 | 9 IUS not ignored w/o last_modified | 0 | 0 | — survives (equivalent, see D2) |
| M12 | 11 IMS not ignored w/o last_modified | 1 | 1 | ims/ignored-when-last-modified-absent |
| M13 | 10 304/412 always 304 | 1 | 1 | inm/match-post-412 |
| M14 | 10 method test inverted | 1 | 1 | inm/match-get |
| M15 | 11 IMS gate widened to POST | 1 | 1 | ims/ignored-for-post |
| M16 | 3 quoting not required | 1 | 1 | refuse/etag-unquoted |
| M17 | 3 etagc not checked | 1 | 1 | refuse/etag-bad-char |
| M18 | 3 lowercase `w/` accepted | 0 | 1 | refuse/ifmatch-lowercase-weak-prefix |
| M19 | 3 empty opaque-tag refused | 0 | 1 | inm/empty-opaque-tag-matches |
| M20 | 4 empty member tolerated | 1 | 1 | refuse/empty-member |
| M21 | 4 `*` mixed tolerated | 1 | 1 | refuse/star-mixed |
| M22 | 4 empty value tolerated | 1 | 1 | refuse/empty-value |
| M23 | 1 bool accepted as int | 1 | 1 | refuse/last-modified-bool |
| M24 | 1 negative accepted | 0 | 1 | refuse/negative-if-modified-since |
| M25 | 1 string date coerced | 1 | 1 | refuse/date-as-string-not-int |
| M26 | 1 exists not bool-checked | 1 | 1 | refuse/exists-not-bool |
| M27 | 2 etag with exists=false | 1 | 1 | refuse/absent-with-etag |
| M28 | 2 last_modified with exists=false | 0 | 1 | refuse/absent-representation-with-last-modified |
| M29 | 6 IUS skipped under If-Match | 0 | 1 | refuse/unmodified-since-malformed-under-if-match |
| M30 | 7 unknown role as origin | 1 | 1 | refuse/role-unknown |
| M31 | 1 unknown top key tolerated | 1 | 1 | refuse/unknown-top-key |
| M32 | 1 extra key in current | 0 | 1 | refuse/current-extra-key |
| M33 | 5 etag null equals any tag | 1 | 1 | inm/ignored-when-current-etag-absent (subject traceback) |
| M34 | 9 IUS strict instead of <= | 1 | 1 | ius/equal-passes |
| M35 | 11 IMS strict instead of <= | 1 | 1 | ims/equal-304 |
| M36 | 1 method token not checked | 1 | 1 | refuse/method-not-token |
| M37 | 1 method case-insensitive 304/412 | 0 | 1 | inm/lowercase-method-is-not-get |
| M38 | 8 `*` needs current tag | 1 | 1 | ifmatch/star-with-representation |
| M39 | 5 weak needs equal weakness | 1 | 1 | inm/weak-member-matches-strong-current |
| M40 | 4 HTAB not accepted | 0 | 1 | inm/htab-around-list-members (subject refuses a valid list) |

Note on M33 and M40: v2 kills these through a subject-side error path (a TypeError traceback in the mutant; a valid HTAB-separated list refused as `invalid_input`), not through a semantic mismatch. The kill rule counts this as a kill; it is recorded so the L1 can weigh it.

## Equivalence of M11 (the one v2 survivor)

- M11 changes `elif ... and stamp is not None: if stamp > ius` into `elif ... ius is not None: if (stamp or 0) > ius`.
- Reasoning: ius is validated as an integer >= 0 before evaluation (clause 1), so `0 > ius` is always false; when stamp is None the mutant never returns 412 and falls through identically to the base.
- Measured: `receipts/equiv_m11.py receipts/base-posgood.py receipts/m11.py` → `cases=115200 differing=0`, exit 0. Exhaustive product over method (4), exists (2), etag (3), last_modified (4), if_match (4), if_none_match (4), IMS (5), IUS (5), role (3). Diff of the two files: `receipts/`-copies of base and M11 (two lines changed).
- Consequence: no counter can kill M11 on this population. The v2 "one new case per surviving class" rule included M11 (`ius/unbounded-when-last-modified-absent`, c94 line 306), but that case is a behaviour check the mutant satisfies, so it cannot kill M11 by construction. Under the freeze's kill rule the count stays honest: 39/40, with the survivor named and proved equivalent. The 40/40 target is unattainable without changing the population, which is frozen and was not changed.

## Defects and limits (findings, not edits)

- D1 (population base mismatch, material): every one of the 40 find strings matches the frozen pos-good base (count 1) and matches the candidate at ba667b24 zero times (`candidate_find_count=0` for all 40, recorded in both JSON files). The "mutants of scripts/conditional_eval.py" are therefore mutants of the round-93 positive control's bytes, not of the candidate. Kill counts measure counter sensitivity on pos-good-shaped code, which is what the freeze's claim says ("instrument sensitivity"), but it is not a mutation of the scored candidate. Round 93 had the same base (`base.sha256` 0fe018…).
- D2 (target infeasible as frozen): 40/40 is not reachable because M11 is equivalent (above). The freeze does not mention equivalence; it should have been checked before the target was written.
- D3 (label): the v2 counter still prints `C2v93` and reads round-93 pins and contract (`.ufo/waves/round-93/c2-contract.md`, `c2-population.sha256`). The base receipt therefore does not identify which counter produced it; I attribute by the file path only.
- D4 (pin gap): `c93_conditional.py` digest is not in the freeze's instrument digests. Observed fee28ea0…dd55a3 (`receipts/instrument-sha256-observed.txt`); if the L1 relies on the v1 counter as a fixed predecessor, that digest should be recorded.
- D5 (clone commit): the mutant base commit `6d75ee0c…` and the 40 mutant commit revs in the JSON files exist only in the deleted scratch clone. They are reproducible from the bytes: ba667b24 tree + pos-good bytes (sha 0fe018…) + the single patch per mutant in `mutants-posgood.json`; the commit hashes will not reproduce exactly (identity `mut`, timestamps).
- Limits: one run per counter per mutant, default seed 93, generated=120; no seed sweep. Exit codes are the only kill signal; a crash-as-kill (M33, M40) is included. No subagent was spawned; no tool was installed or upgraded; no network access; no host sysctl changed.

## Receipts (under `.ufo/waves/round-94/w1/ExecC2Mutants/`)

- `mutants-v1.json`, `mutants-v2.json` (40 entries each), `summary.txt`, `base-candidate.txt`
- `receipts/`: `mut94.py`, `mutants-posgood.json`, `posgood-base.rev`, `run.log`, `run.err` (empty), `base-v{1,2}.stdout` / `.stderr` (base run JSON detail), `base-posgood.py`, `m11.py`, `equiv_m11.py`, `instrument-sha256-observed.txt`
- Scratch `/fast/scratch/hyaku/kake-r94/ExecC2Mutants/` removed after copying.
