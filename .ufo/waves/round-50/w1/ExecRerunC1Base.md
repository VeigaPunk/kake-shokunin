# C1 base-revision control rerun (do-nothing)

Seat: leaf (freshness axis), wave 1 of round 50.
Claim under test: **C1 (freshness, capability) — quote class, committed bytes only.**
Predicate: `met: classed == 3 of 3 declared ids` (S273, S274, S286).
Control revision (do-nothing base): `9619af67c52939daac502ca7a24c9d714f3f51db`
Expectation: this control must NOT be met.

## Exact command

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/c50_quote_class.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 9619af67c52939daac502ca7a24c9d714f3f51db
```

## Exact stdout

```
C1 classed 0/3 met=False
  FAIL S273: class ledger absent, lesson absent
  FAIL S274: class ledger absent, lesson absent
  FAIL S286: class ledger absent, retained blob absent, lesson absent, no live registry row, entry absent
```

## Exit code

`1`

## Classed count

`0/3` — `met=False` (control behaves as required: the predicate is not satisfied at the do-nothing base).

## Per-id failure reasons

- **S273** — class ledger absent; lesson absent. (2 of 5 signals missing; no retained-blob / live-registry / entry checks listed for this id at base.)
- **S274** — class ledger absent; lesson absent. (Same profile as S273.)
- **S286** — class ledger absent; retained blob absent; lesson absent; no live registry row; entry absent. (All 5 signals missing — this id additionally requires a retained blob and a live registry row that S273/S274 do not.)

## Read of the result

At base, the instrument distinguishes the three ids by how much evidence is missing: S273/S274 fail on the two-quote-class core (ledger + lesson), while S286 — the newly declared id — fails every check including the retained blob, the live registry row, and the entry. Any committed move that flips C1 to `met` must therefore land all three ledger/lesson pairs **plus** S286's retained blob, live registry row, and entry — committed bytes only.

Report: .ufo/waves/round-50/w1/ExecRerunC1Base.md
