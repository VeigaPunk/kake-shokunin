#!/usr/bin/env python3
"""C2-m5 equivalence: exhaustive check over the counter's own met expression.

met_pristine = declared==3 and surfaces_a==3 and surfaces_b==3
               and receipts_ok and manifest_ok and order_ok and floor_ok
               and determinism and record_equal and selftest_ok
with receipts_ok derived exactly as the counter derives it:
receipts_ok = a_ok and b_ok and surfaces_a==declared and surfaces_b==declared

met_mutant  = the same expression with `surfaces_a == 3` removed.
Search every consistent assignment; report any in which the two differ.
"""
from __future__ import annotations

import itertools

def met(declared, surfaces_a, surfaces_b, a_ok, b_ok, manifest_ok, order_ok,
        floor_ok, determinism, record_equal, selftest_ok, drop_surfaces_a):
    receipts_ok = int(bool(a_ok and b_ok and surfaces_a == declared
                           and surfaces_b == declared))
    conjuncts = [declared == 3, surfaces_b == 3, receipts_ok == 1, manifest_ok == 1,
                 order_ok == 1, floor_ok == 1, determinism == 1,
                 record_equal == 1, selftest_ok == 1]
    if not drop_surfaces_a:
        conjuncts.insert(1, surfaces_a == 3)
    return all(conjuncts)


def main() -> int:
    domain = {
        "declared": range(0, 9),
        "surfaces_a": range(0, 9),
        "surfaces_b": range(0, 9),
        "a_ok": (0, 1),
        "b_ok": (0, 1),
        "manifest_ok": (0, 1),
        "order_ok": (0, 1),
        "floor_ok": (0, 1),
        "determinism": (0, 1),
        "record_equal": (0, 1),
        "selftest_ok": (0, 1),
    }
    keys = list(domain)
    total = differ = 0
    witness = None
    for values in itertools.product(*(domain[k] for k in keys)):
        row = dict(zip(keys, values))
        total += 1
        p = met(**row, drop_surfaces_a=False)
        m = met(**row, drop_surfaces_a=True)
        if p != m:
            differ += 1
            if witness is None:
                witness = (row, p, m)
    print(f"assignments={total} diverging={differ}")
    if witness:
        print(f"witness={witness}")
    print("EQUIVALENT" if differ == 0 else "NOT-EQUIVALENT")
    return 0 if differ == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
