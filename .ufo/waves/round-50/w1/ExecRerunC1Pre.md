# C1 re-run at pre-append revision

## Command

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/c50_quote_class.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1
```

## Exact stdout

```
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
```

## Exit code

`1`

## Per-id outcome

- **S273** — NOT classed. Reason: `lesson absent`.
- **S274** — NOT classed. Reason: `lesson absent`.
- **S286** — NOT classed. Reason: `lesson absent, no live registry row, entry absent` (three sub-conditions listed by the instrument: the lesson file is absent, there is no live registry row for S286, and the committed entry is absent).

## Summary

At the pre-append revision `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` (mirror committed, live registry still without S286), the C1 instrument classed **0 of 3** declared ids. The predicate `met: classed == 3 of 3 declared ids` evaluated **met=False**. None of S273, S274, or S286 reached the classed state; S286 additionally lacked both a live registry row and the committed entry.

Report: .ufo/waves/round-50/w1/ExecRerunC1Pre.md
