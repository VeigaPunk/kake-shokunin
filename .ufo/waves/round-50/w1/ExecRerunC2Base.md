# ExecRerunC2Base — C2 durable control at base revision

Round 50 wave 1 leaf seat. Do-nothing control rerun of the frozen C2
(operability) counting command against the base revision
`9619af67c52939daac502ca7a24c9d714f3f51db`.

## Command

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/c50_durable.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 9619af67c52939daac502ca7a24c9d714f3f51db
```

## Exact stdout

```
C2 durable 0/1 met=False
  FAIL order proof absent
  FAIL wave-cite proof absent
  FAIL LOG.md at measured revision does not cite the wave
  FAIL settlement absent
```

## Exit code

`1`

## Result

- Durable count: **0/1**
- `met=False` — the control is not met at the base revision, as required.
- Reasons (all four checks FAIL):
  1. `FAIL order proof absent`
  2. `FAIL wave-cite proof absent`
  3. `FAIL LOG.md at measured revision does not cite the wave`
  4. `FAIL settlement absent`

The instrument correctly reports the do-nothing base as unmet: no order
proof, no wave-cite proof, no wave citation in LOG.md at the measured
revision, and no settlement artifact are present at
`9619af67c52939daac502ca7a24c9d714f3f51db`.
