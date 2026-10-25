# Mutation report — C2 byte pin on retained source bodies

Seat: `L1Kake51.MutationSourceSha-2` (mutation tester, round 51 wave 1)
Scope: attack the freshness claim C2 (`met: conditions_passed == 8 of 8`) at the
behavior-bearing point `c51_quote_truth.py` calls "receipt pins": the sha256 of the
retained source bodies under `.ufo/waves/round-51/sources/`.
Scratch: `/tmp` only. Lane repo, lane jj state and lane git index untouched (read-only
git only). No subagents dispatched.

## Method

The counter reads committed bytes only (`git show <rev>:<path>`), so a mutation has to be
committed to be visible. I cloned the lane into scratch and worked there:

- `/tmp/r51-mut` — pristine clone of `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
- `/tmp/r51-mut-quote` — probe A (byte inside the S262 Gate quote).
- `/tmp/r51-mut-aside` — probe B (byte outside the S263 Gate quote).

Baseline reproduced on the clone before mutating:

```
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)   rc=0
```

Pristine committed bodies (grounding the "before" hash, `git show <base>:<path> | sha256sum`):

```
S262  792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
S263  6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
```

Both equal the `sha256` fields in `.ufo/waves/round-51/sources/receipts.json`, so the
mutant baseline is exactly the lane's committed body. `receipts.json` was NOT touched in
either mutant commit (kept, as tasked), and each mutant commit touches exactly one file,
one line (`1 insertion / 1 deletion` = one byte):

```
f458fc9 mutant: one byte inside S262 gate quote, receipt untouched
 .ufo/waves/round-51/sources/S262.html | 2 +-
76af961 mutant: one byte outside S263 gate quote, receipt untouched
 .ufo/waves/round-51/sources/S263.html | 2 +-
```

## Mutant A — one byte inside the quoted span

Byte at S262 offset **140660**: `i` -> `a`, turning the Gate quote
`"indicating a canonical preference is a hint, not a rule"` into `...a hant, not a rule`.
Length preserved: 174926 -> 174926 bytes, exactly **1** differing byte.

```
pristine 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
mutant   1c49660731329b67d66404d5654695fb233740484d5cd05437c5e9598a3e0ba7
```

`c51_quote_truth.py --root /tmp/r51-mut-quote --revision f458fc9a...` actual output:

```
C2 quote-truth 6/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth FAIL
    - S262: Gate quote is not a raw substring of the retained body
  C6_receipt_pins FAIL
    - S262: receipt sha256 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
             != body 1c49660731329b67d66404d5654695fb233740484d5cd05437c5e9598a3e0ba7
  C7_validate_before_append pass
  C8_append_after_mirror pass
  revision: f458fc9a038273781850f373c43e283280f4847e
```

**Exit 1. VERDICT: KILLED** by C5 (`gate-quote-truth`) and C6 (`receipt-pins`).

## Mutant B — one byte outside the quoted span

Byte at S263 offset **44**: `e` -> `x`, turning `lang="en"` into `lang="xn"` in the
`<html>` tag. Gate quote at offset 137363 stays intact; length 175561 -> 175561 bytes,
exactly **1** differing byte. This isolates C6 from C5: the quote still parses, so only the
receipt pin can catch it.

```
pristine 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
mutant   d613cd973ccdfc88a4419911f2885737766398e9efc92c65d2db86e51d555e90
quote_intact True
```

`c51_quote_truth.py --root /tmp/r51-mut-aside --revision 76af961...` actual output:

```
C2 quote-truth 7/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth pass
  C6_receipt_pins FAIL
    - S263: receipt sha256 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
             != body d613cd973ccdfc88a4419911f2885737766398e9efc92c65d2db86e51d555e90
  C7_validate_before_append pass
  C8_append_after_mirror pass
  revision: 76af96111b758753b8e23edda9618f382ad25f6c
```

**Exit 1. VERDICT: KILLED** by C6 alone. The two mutants together show C5 and C6 are
independently live: neither is riding on the other.

## Measurement boundary (checked, not assumed)

The counter's docstring claims it "opens no worktree file of the measured revision". Probe:
mutate S262 at the *same* offset 140660 in the clone worktree at the pristine revision and
run without committing.

```
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)   rc=0
```

Uncommitted drift does not move the verdict — the counter is commit-scoped, as documented.
This is a measurement fact, not a defect: the claim is about committed bytes, and a mutant
must be committed to exist.

## Coverage finding (not a contract change)

C6 compares only `sha256` and `url`. The receipt's `bytes` / `declaredBytes` (174926,
175561) are never compared against the body length, so both length-preserving mutants above
leave the size claim satisfied; the **whole body pin rests on sha256 alone**. That is
sufficient here (both mutants were killed), but it means a future reader should not assume
size is an independent guard. No change to C2's predicate is warranted or implied.

## Restoration evidence

Both mutated bodies were restored to their exact pristine bytes and re-verified:

```
/tmp/r51-mut       S262 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
/tmp/r51-mut       S263 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
/tmp/r51-mut-quote S262 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
/tmp/r51-mut-quote S263 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
/tmp/r51-mut-aside S262 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b
/tmp/r51-mut-aside S263 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de
```

Verdict restored to pristine at the base revision in every copy:

```
/tmp/r51-mut        rc=0  C2 quote-truth 8/8 met=True
/tmp/r51-mut-quote  rc=0  C2 quote-truth 8/8 met=True
/tmp/r51-mut-aside  rc=0  C2 quote-truth 8/8 met=True
```

In the two probe copies the worktree is one line off the *mutant commit* by construction
(`git diff --numstat` = `1 1`), and that diff is the exact byte reversal:

```
- indicating a canonical preference is a hant, not a rule.
+ indicating a canonical preference is a hint, not a rule.
-       lang="xn"
+       lang="en"
```

The slack copy `/tmp/r51-mut` is clean against the base commit (0 changes under
`.ufo/waves/round-51/sources`). The lane worktree bodies were never written by this seat and
still hash to the receipt values:

```
792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b  kake-shokunin/.ufo/waves/round-51/sources/S262.html
6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de  kake-shokunin/.ufo/waves/round-51/sources/S263.html
```

Lane git index, lane jj state and the fleet repo: no write, no `git add/commit/checkout/
switch/reset/stash/pull/push`, no `jj` mutation. This file is the only lane path written.

## Verdict

- Mutant A: **killed** (C5 + C6), exit 1.
- Mutant B: **killed** (C6), exit 1.
- C2's byte-level freshness pin on the two retained bodies is live and rejects a single-byte
  drift that keeps the receipt untouched. The claim text matches what the bytes prove; the
  residual is a coverage note (size field unchecked), not a defect in the predicate.

Tooling installed/upgraded: none (python3, git, coreutils only).
