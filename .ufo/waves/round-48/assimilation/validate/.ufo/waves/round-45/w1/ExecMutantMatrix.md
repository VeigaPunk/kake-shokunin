# ExecMutantMatrix — C2(a) selftest coverage

Axes: **freshness** (the shipped selftest's detection boundary) and **operability** (reproducible local mutation evidence).

## Mutants implemented

Created `mutants/m1.py`–`m4.py` as copies of frozen `.ufo/waves/round-44/c44_audit.py`, then applied one behavioral mutation per copy. I followed the `## The four mutants` section in `.ufo/waves/round-44/w2/MutClassGate.md`, which states:

> == m1.py (revert to requiring EVERY caughtBy key be a class key)
> `< any(isinstance(key, str) and key in class_keys for key in caught))`
> `> all(isinstance(key, str) and key in class_keys for key in caught))`
>
> == m2.py (accept timing-only witnesses)
> `> TIMING_KEYS = ("T1", "T2", "T3", "T4", "T5")`
> `< any(isinstance(key, str) and key in class_keys for key in caught))`
> `> any(isinstance(key, str) and (key in class_keys or key in TIMING_KEYS) for key in caught))`
>
> == m3.py (treat a v4-run divergence as a class witness)
> `> V4_RUN_KEYS = ("A", "B", "C", "D", "E", "F")`
> `< any(isinstance(key, str) and key in class_keys for key in caught))`
> `> any(isinstance(key, str) and (key in class_keys or key in V4_RUN_KEYS) for key in caught))`
>
> == m4.py (witness when any run errors)
> `> if row.get("error"):`
> `>     return True`

Target locations: m1/m2/m3 each replace the return predicate at copied-source line 66 (m2/m3 use inline key tuples equivalent to the report's named tuples); m4 inserts its two-line error branch at line 64 of the copy, at the start of `semantic_witness`. Thus m1 rejects the real mixed `D,G3` selftest witness, m2 accepts timing-only caughtBy keys, m3 accepts the v4 `D` selftest row, and m4 reports an error row as a witness.

## Before — v1 shipped selftest

Commands run:

```text
python3 -B .ufo/waves/round-45/mutants/m1.py --selftest
python3 -B .ufo/waves/round-45/mutants/m2.py --selftest
python3 -B .ufo/waves/round-45/mutants/m3.py --selftest
python3 -B .ufo/waves/round-45/mutants/m4.py --selftest
```

Kill table (KILLED = selftest exits 1; SURVIVED = exits 0):

| Mutant | Result | Exit | Evidence |
|---|---|---:|---|
| m1 | KILLED | 1 | `before/m1.txt` — AssertionError at `assert semantic_witness(mixed_divergence, keys)` |
| m2 | SURVIVED | 0 | `before/m2.txt` — `SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail` |
| m3 | KILLED | 1 | `before/m3.txt` — AssertionError at `assert not semantic_witness(v4_divergence, keys)` |
| m4 | SURVIVED | 0 | `before/m4.txt` — `SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail` |

Observed before-state: **2/4 killed**, matching MutClassGate's shipped-selftest coverage result. Decisive command output, verbatim:

`m1`:
```text
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 226, in <module>
    main()
    ~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 122, in main
    selftest()
    ~~~~~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m1.py", line 94, in selftest
    assert semantic_witness(mixed_divergence, keys)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
SELFTEST_EXIT=1
```

`m2`:
```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_EXIT=0
```

`m3`:
```text
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 226, in <module>
    main()
    ~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 122, in main
    selftest()
    ~~~~~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/mutants/m3.py", line 95, in selftest
    assert not semantic_witness(v4_divergence, keys)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
AssertionError
SELFTEST_EXIT=1
```

`m4`:
```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_EXIT=0
```

Full captured output is also retained in the four `verification/selftest-coverage/before/mN.txt` files.

## After — v2 dependency absent

Attempted to read `.ufo/waves/round-45/c45_audit.py`; the repository read returned `Path 'kake-shokunin/.ufo/waves/round-45/c45_audit.py' not found`. Therefore no v2 mutant copies were created and no after selftests were run: **after-state is unmeasured (0/4 run), not a pass/fail result**. Required dependency: v2 driver file must be present before applying the same four mutations and running its shipped selftest.

## Files written

- `.ufo/waves/round-45/mutants/m1.py`
- `.ufo/waves/round-45/mutants/m2.py`
- `.ufo/waves/round-45/mutants/m3.py`
- `.ufo/waves/round-45/mutants/m4.py`
- `.ufo/waves/round-45/verification/selftest-coverage/before/m1.txt`
- `.ufo/waves/round-45/verification/selftest-coverage/before/m2.txt`
- `.ufo/waves/round-45/verification/selftest-coverage/before/m3.txt`
- `.ufo/waves/round-45/verification/selftest-coverage/before/m4.txt`
- `.ufo/waves/round-45/w1/ExecMutantMatrix.md`

No frozen file was edited; no tool install was performed. LSP was unavailable in the provided tool inventory; classifier and selftest locations were read directly.