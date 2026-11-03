# Round-74 controls — provenance

The three claim controls were frozen in commit `b35dd4d7` before any seat ran:

- `base-c1-registry.txt` — C1 base census at `ced2878a` (7 of 8 unregistered, `met=false`, exit 1).
- `base-c2-sidecar.txt` — C2 base sidecar census at `ced2878a` (174 entries, 144 contradictions,
  `met=false`, exit 1).
- `base-c2-sweep.txt` — the standing sweep at base: `--selftest` 36/36, `--offline` exit 1 with the
  single `~/projects` drift and no mention of the 144 contradictions (the blindness control).

The four `base-harm-*.txt` receipts were produced by the L1 (`KakeR74`) at 2026-11-03T20:15:45-03:00,
after the freeze commit and before any after-state, as supplementary base readings for the harm
battery; they are not part of the frozen claim controls. Commands (cwd = the lane at `ced2878a`):

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root . --revision ced2878a --base ced2878a
python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane . --revision ced2878a
python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root . --revision ced2878a
python3 -B .ufo/waves/round-73/c73_tmp_v3.py --lane . --revision ced2878a --work <scratch>
```

Each file's last line is the shell's recorded exit (`c70=0`, `c72=0`, `c73p=0`, `c73tmp=0`); the
lines above it are the counter's own output. Disclosed under `## Mistakes` in
`corpus/lessons/round-74.md` and in the round report.
