# Round-54 w1 — ReviewerC1Noop: C1 do-nothing control falsification

Seat: `L1Kake54.ReviewerC1Noop` (leaf member; no subagents).
Scope: independent falsification of the C1 no-op control — run the named
read-only counter at round-open revision
`68228b2d74e7930ae4f07e90e382a0d03ab80c7b` and decide whether it reaches the
target. No writes other than this report; no installs.

## Command run (verbatim, cwd = lane root)

```
python3 -B .ufo/waves/round-54/c54_s374_calib.py --root . --revision 68228b2d74e7930ae4f07e90e382a0d03ab80c7b
```

## Exact stdout observed

```
  PASS C1.1_body: [] {'occurrences': 1}
  PASS C1.2_cells: [] {'suspect_cells': 1}
  FAIL C1.3_correction: ['no valid r54 correction block (exact quote + crawl token)'] {'block_offset': -1}
  FAIL C1.4_mismatch: ['mismatches=1'] {'mismatches': 1}
S374 qualifier: mismatches = rendered cells missing the crawl qualifier and not superseded by an r54 correction block; met when 0
mismatches=1 met=False
EXIT=1
```

Observed process exit status: **1**.

## Committed receipt comparison

Receipt `.ufo/waves/round-54/controls/base-c1-s374.txt` declares required
outcome `mismatches=1 met=False`, `EXIT=1` (contract.md kill rule: exit 1 if
not met). Live run matches on every load-bearing line:

- `mismatches=1 met=False` — identical.
- `EXIT=1` — identical, and the observed process returncode is 1.
- Check sequence PASS/PASS/FAIL/FAIL on C1.1–C1.4 — identical.

Cosmetic delta only: the receipt renders per-check notes/facts in abbreviated
`key=val` form (e.g. `no valid r54 correction block`, `occurrences=1`), while
the live script prints the full Python list/dict reprs shown above. No
semantic difference; receipt is a normalized transcription, not a raw capture.

## Independent fact-check at the pinned revision (read-only `git show`)

Did not trust the script's verdict; verified each underlying predicate input:

- `git show 68228b2d…:.ufo/waves/round-52/sources/S374.html` —
  grep count for `このリンク先のウェブページの巡回を推奨していない` = **1**
  (C1.1 pin confirmed).
- `git show 68228b2d…:corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` —
  two `(rendered: …)` cells. Cell 1 (line 13): "the site owner is taken to
  consider the link target's page one it does not recommend, or a link it
  cannot vouch for" — endorsement vocabulary (`recommend`, `vouch`), no
  `crawl`/`巡回` inside the cell → exactly **1 suspect cell**. Cell 2 (line 19)
  carries no endorsement vocabulary → not suspect.
- Same blob: no `[r54-correction 2026-10-25]` line exists → no valid
  correction block → the suspect cell is not superseded → mismatch = 1.
- Commit identity: `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`, subject
  "round-53 verifier spot-check (integrator, hyaku): non-author admit/reject",
  committer date 2026-10-25T09:27:37-03:00 — consistent with "lane master tip
  at round open" per contract.md.

## Verdict

**Control holds; the counter does not reach the claim target at base.**
At the round-open revision the counter reports `mismatches=1 met=False` and
exits 1 — the do-nothing run correctly refuses `met=True`. The counter is
observably discriminating (per-check PASS/FAIL varies with input facts), so
the observed behavior is inconsistent with a constant `met=True` junk
implementation on this input; formal junk-control attacks remain the
mutation-testers' lane.

## Residual risk / gaps

- Receipt formatting differs cosmetically from raw script output (noted
  above); downstream auditors diffing byte-for-byte should normalize.
- Falsification is single-input: base only. Discrimination on the *positive*
  side (an actual r54 correction block flipping the verdict to exit 0) is out
  of this seat's scope — selftest fixtures and any post-repair run cover it.
- Counter reads committed bytes via `git show` only; worktree state cannot
  influence the result, so the measurement is reproducible.

No installs performed. No files written other than this report.
