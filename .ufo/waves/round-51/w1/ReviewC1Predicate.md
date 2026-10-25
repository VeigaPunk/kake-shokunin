# ReviewC1Predicate — C1 predicate vs counter text and semantics

Scope: `contract.json` C1 (lines 17–28) vs `.ufo/waves/round-51/c51_wave_ledger.py`
(docstring 3–33, `PREDICATE` 42, `check_l1` 97–142, `check_l2` 145–197,
`check_l3` 200–257, `main` 260–293). Read-only; no lane mutation.

## 1. Verdict on the three questions

**Predicate sentence — identical, byte for byte.**
- `contract.json:18` → `"predicate": "met: ledger_checks_passed == 3 of 3"`
- `c51_wave_ledger.py:42` → `PREDICATE = "met: ledger_checks_passed == 3 of 3"`
- `c51_wave_ledger.py:29` → the same sentence on its own line inside the docstring.

Verified programmatically (string equality `True`; the sentence occurs exactly once
in the docstring and exactly once in the contract).

**Threshold — 3 of 3 in both, and the code's "3" is genuinely "three checks".**
The check tuple at `c51_wave_ledger.py:269` is exactly `("L1", check_l1), ("L2",
check_l2), ("L3", check_l3)`, so `passed` can only take 0..3. The threshold is
re-encoded at `:280` (`"met": passed == 3`), `:285` (stdout `met=`), `:293`
(`return 0 if passed == 3 else 1`). No divergence.

**Condition sentences — NOT word for word. All three diverge.**

| check | contract | docstring | verbatim | same after stripping backticks |
|---|---|---|---|---|
| L1 | `contract.json:23` | `c51_wave_ledger.py:11-16` | No | No |
| L2 | `contract.json:24` | `c51_wave_ledger.py:17-20` | No | No |
| L3 | `contract.json:25` | `c51_wave_ledger.py:21-25` | No | No |

Token-level deltas (contract-only → docstring-only):

- **L1** `accounting:` → `accounting —`; `the committed seat-report count` →
  `the number of committed seat reports`; `the settlement's reports_written` →
  `the count the committed settlement receipt records as written`; `the payload's
  seat count` → `the seat count of the committed dispatch payload`; `every seat
  marked` → `every seat the settlement marks`. **Docstring adds a clause the
  contract does not have** (`:15-16`): `(and every committed report file belongs
  to a seat the settlement knows)`. Round-trips to the same predicate, but it is
  not the frozen sentence.
- **L2** `with an integer HTTP status` → `that names an HTTP status code` (the word
  *integer* is dropped); `a failing receipt carries a body excerpt` →
  `names an HTTP status code and a body excerpt` (**scope widened from failing
  receipts to all receipts**); `is not used by a role` → `is never used as a
  role's model`; `the route map` → `the committed route map`.
- **L3** `aggregate seat seconds`/`dead-seat seconds` → `aggregate seat time`/
  `dead-seat time`; `the same figures` → `the same three figures`; `LOG.md` →
  `the lane's LOG.md`; `duration matches its recorded reason` → `recorded duration
  is consistent with its recorded reason`.

## 2. Findings

### HIGH

**H1 — L3 enforces a condition that appears nowhere in the frozen contract.**
`c51_wave_ledger.py:252-256` requires the committed `wave-grant.txt` to exist and
to contain `granted lane=kake`. `contract.json` never mentions a grant (grep for
`grant` hits only `L3`/`separability`/`r50-3`, and none of them name it), and the
docstring's L3 sentence (`:21-25`) does not name it either.
Evidence — a fully valid synthetic wave with every L3-named artifact committed but
no grant file scores 2/3:
```
--- mutant A (drop wave-grant.txt) exit=1
C1 ledger 2/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L3 FAIL
    - wave grant file absent at the measured revision
```
Under `contract.json:28` ("a miss on any of L1, L2 or L3 is an honest stop for C1")
this turns an unwritten extra file into an honest stop. `wave-grant.txt` is present
in the worktree today but **uncommitted**, so unless the wave lead commits it the
wave will stop on a condition the frozen predicate never declared.

### MEDIUM

**M1 — L2 requires an integer HTTP status from receipts the wave never used.**
`c51_wave_ledger.py:182-185` loops over *all* committed receipts; `contract.json:24`
scopes "an integer HTTP status" to "every route the wave used".
```
--- mutant B (unused receipt, string httpStatus) exit=1
L2 FAIL - probe receipt for alias-unused carries no integer httpStatus
```
The route map binds only `alias-ok`; the offending receipt belongs to an unused
route. Condition text satisfied, counter still fails.

**M2 — L2's "recorded as a deviation" is a substring test over prose.**
`c51_wave_ledger.py:192-196` concatenates every role's `probe` field and does
`if alias not in recorded`. An alias that merely occurs inside another route's
probe string is treated as recorded. Mutant: a failing receipt for alias `alias`
(`ok:false`, `httpStatus:500`) is never named as a deviation, but the role probe
text `route-probes/alias-ok.json` contains it:
```
--- mutant C (failing alias never recorded, substring collision) exit=0
C1 ledger 3/3 met=True
```
False accept: an unrecorded deviation passes. (The live `route-map.json` relies on
this: its `probe` values are prose paragraphs, so any alias mentioned anywhere in
any role's prose satisfies the check.)

**M3 — L3's "every dead seat's duration matches its recorded reason" is only
checked for two reason prefixes.** `c51_wave_ledger.py:230-235` tests
`timeout-*` (exact seconds) and `exit-*` (≤ timeout); every other reason is
unconstrained. Mutant: dead seat with `reason:"killed-by-operator"`, `seconds:600`
(= `timeout_seconds`) passes 3/3. Condition satisfied on paper, not enforced.

**M4 — L1 adds two gates absent from the frozen L1 sentence.**
`c51_wave_ledger.py:124-125` requires the payload's own `counts.spawn` to equal its
task count, and `:128-129` requires `settled_count + dead_count == len(settled) +
len(dead)`. `contract.json:23` states neither. Both are plausible integrity checks,
but they are extra pass/fail gates on a claim whose conditions were frozen without
them. Both are internally consistent with the settlement the wave itself writes,
which is why this is MEDIUM rather than HIGH — but they are still pass/fail gates
the frozen sentence does not carry.

### LOW

(F = finding; `L1`/`L2`/`L3` stay reserved for the check names.)

**F1 — the docstring's route-receipt claim is stronger than the code and than the
contract.** `:17-18` says every receipt "names an HTTP status code **and a body
excerpt**". The code checks an excerpt only when `ok is False` (`:186-189`), and
`contract.json:24` scopes the excerpt to failing receipts. Mutant: a used route with
`{"alias":"alias-ok","httpStatus":200,"ok":true}` and no `bodyExcerpt` scores 3/3.
Contract satisfied; docstring over-claimed.

**F2 — the documented exit-code table is unreachable.** `:31-32` documents `2 the
evidence cannot be evaluated` and `64 usage error`. No code path returns 2 or 64:
missing evidence returns `False` + notes (`:107-108, 149, 207-213`) and `main`
returns only 0/1 (`:293`). `--root`/`--revision` are `required=True`
(`:262-263`), so a usage error exits **2** via argparse:
`python3 c51_wave_ledger.py` → exit 2, `error: the following arguments are
required: --root, --revision`.

**F3 — the LOG wall-clock check is a substring test.** `:242`
`str(wall) not in log_text` accepts `600` inside `1600`/`6000`. Bounded (the value
is also cross-checked against the accounting artifact at `:240`), but it does not
prove LOG.md "names the wall-clock figure".

**F4 — the frozen counting command is cwd-dependent.** `contract.json:19` uses
`--root .`; the dispatcher's form (`--root /home/vgpnk/.../kake-shokunin`) is not
the frozen text. Both work; only the dispatcher's runs from any cwd.

**F5 — freeze provenance.** `contract.json` and `c51_wave_ledger.py` entered in the
same commit (`19a99bd`), so the pair cannot witness that the predicate was frozen
before the counter was written; `declaredBeforeScoring` is supported only in the
sense that no wave evidence existed at that commit.

**F6 — every artifact path is code-only.** The frozen C1 text names *what* to read
("the settlement", "the payload", "the route map", "the committed settlement and
wave-timing bytes", "the committed time-accounting artifact", "LOG.md") but never a
filename. The paths exist only as constants at `:46-53` (`settlement.json`,
`w51-taskcall.json`, `route-map.json`, `route-probes/`, `wave-timing.json`,
`round-time-accounting.json`, `wave-grant.txt`). A wave that names any of them
differently fails with "absent at the measured revision" (`:104-106`, `:148`,
`:207-213`), which reads as a claim failure rather than a path mismatch. Same
defect class as H1, mitigated only by the wave lead writing these exact names.

**F7 — the seat-name to report-stem mapping is unstated.** `:109-114` derives each
committed report's identifier as the `w1/<stem>.md` path stem and compares it, as a
sorted list, against the settlement's seat `name` fields. Neither `contract.json:23`
nor the docstring (`:11-16`) says a report must be named after its seat, so a seat
`ScoutCensusBefore` that commits `w1/scout-census-before.md` fails "exactly one
committed report file" while having exactly one.

## 3. Measured state at dispatch (what the counter actually printed)

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768…
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL  - settlement receipt absent at the measured revision
  L2 FAIL  - route map absent at the measured revision
  L3 FAIL  - settlement receipt absent at the measured revision
exit=1
```
Base `007d66e` prints the identical block (exit 1), matching the committed control
`controls/c1-before-base.txt`. `git ls-tree -r HEAD -- .ufo/waves/round-51/w1`
returns no files. Every other input the counter reads is also absent at the
measured revision — `git cat-file -e HEAD:…` reports ABSENT for all six:

```
settlement.json              ABSENT      route-map.json          ABSENT
wave-timing.json             ABSENT      wave-grant.txt          ABSENT
round-time-accounting.json   ABSENT      w51-taskcall.json       ABSENT
```

In the worktree `route-map.json`, `route-probes/`, `wave-grant.txt`,
`w51-taskcall.json` and `w1/` all exist but are untracked (`git status` `??`), so
none of them is visible to the counter yet. The worktree payload declares
`counts.spawn = 48` with 48 tasks, so L1 can pass only once the 48 seats' reports
are committed and the settlement's `reports_written`/`settled_count`/`dead_count`
agree with them.

## 4. Residual risk and verification gaps

- The 3/3 path is proven only on synthetic fixtures under `/tmp/c51probe`. I did
  **not** observe the counter reach 3/3 on the real wave evidence: it does not
  exist yet. Whether the real settlement satisfies `reports_written`,
  `settled_count + dead_count` and the wall-clock figure is unverified by me.
- H1 is the one finding that can flip the verdict against a wave that satisfies the
  frozen words. Of the rest, M1, M4, F6 and F7 can fail a wave that satisfies the
  frozen words, while M2, M3 and F3 can pass a wave that does not.
- Verified positive: `git`/`show`/`show_json`/`list_paths` (`:56-84`) use only
  `git show <rev>:<path>` and `git ls-tree`, so the docstring's "it opens no
  worktree file of the measured revision" holds — the 0/3 reading at the tip is
  not an artifact of the untracked worktree evidence.
- Not exercised: C2's counter (out of this seat's scope); `--json` mode beyond its
  shape (`:276-281`); behaviour on a revision where `git show` fails mid-loop.
- No tooling installed; no network; no lane writes other than this file.
