# RerunC1Base — C1 before-measurement re-run (advisory)

## What was done

Independent re-run of the C1 counter at the declared "before" revision, from a
fresh clone at `bc6c4a8d435473f3c30903210be30d9d6e3ef750`, comparing field by
field against the L1 receipt
`.ufo/waves/round-33/verification/c1-before-5777d5a.json`.

## Exact commands and exit codes

Sandbox: `/fast/scratch/hyaku/kake-r33/w1/RerunC1Base/` (`tmp/` created,
`export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/RerunC1Base/tmp`; `GIT_DIR`,
`GIT_WORK_TREE`, `GIT_INDEX_FILE` unset).

1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/RerunC1Base/clone` — exit 0.
2. `git -C clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750` — exit 0;
   `git rev-parse HEAD` = `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
3. `python3 -B .ufo/waves/round-33/c1_code_probe.py --repo /fast/scratch/hyaku/kake-r33/w1/RerunC1Base/clone --rev 5777d5af79cac1ebf9144b348a9d274099e77338`
   (cwd = clone, stdout → `c1-rerun.json`, stderr → `c1-rerun.stderr`) —
   **exit 0**, wall ~4 s, stderr 0 bytes.
4. Field-by-field flatten-and-diff of rerun vs receipt (67 flattened keys) —
   **0 diffs**, exit 0.
5. `sha256sum` both files — identical:
   `999801a475d773576292ff1bde66c74a8fe677c36345e1e24eeac24a933caf16`;
   `cmp -s` reports identical (both 2161 bytes). The rerun output is
   **byte-for-byte identical** to the L1 receipt.

## Acceptance fields

- Exit: probe exit 0 (receipt implies a successful run; my run also 0).
- `met`: **2 of 4** — matches receipt (`"met": 2`, `"of": 4`).
- `guard_ok`: **true** — matches.
- `guardMatches`: 1; `runnerSha256`
  `7a6365e0e72fa513136d433b4dc3d382c8ca4812076e52a49836668f1c68827f`;
  `hostileSha256`
  `1d326e160274711031c566e81e2d1207edab1fa81e62c3465cfd1f17d4a32a95` — all match.
- `benign`: exit 0, timedOut false, cases 45, failed 0 — matches.
- Per-variant:
  - `pristine`: applicable, exit 0, `failing: []` — matches.
  - `reworded`: applicable, exit 1, `failing: ["P6-commit-before-init"]`,
    sha256 `8d114395…2504f0b` — matches.
  - `m3`: applicable, exit 1, `failing: ["P6-commit-before-init"]`, sha256
    `bd18bc8f…13ed8a7` — matches.
  - `recoded`: `applicable: false` — matches (at 5777d5a there is no code
    literal to recode, so the variant does not apply).
- `expectations`: pristine_passes true, reworded_passes false, m3_killed true,
  recoded_killed false — matches; `met` = 2 consistent with them.
- Fields that differ from the receipt: **none** (0/67 flattened values; byte
  identical).

## Findings

- **Confirmed, not falsified.** The C1 "before" measurement reproduces
  exactly: at base 5777d5a the hostile selftest keys P6 on message text, so
  `met` = 2 (pristine passes, m3 killed; reworded fails P6; recoded
  inapplicable) with `guard_ok` true. The counter is deterministic across
  clones — identical runner/hostile digests, identical JSON bytes.
- No evidence of flakiness, environment dependence, or overstatement in the
  L1 receipt. The declared-before state stands as a valid baseline for the
  claimed 2 → 4 improvement.

## Not verified

- I did not re-derive the probe's internal spec rows beyond the emitted JSON
  (the receipt's `specs` arrays matched verbatim — they are part of the 67
  compared keys, all 26 case rows per variant identical).
- I did not run the probe against bc6c4a8 (that is the C1 "after" measurement,
  outside this item's scope; covered by sibling/critic seats).
- Lane tree was never touched; all writes stayed in the sandbox except this
  report file. No installs needed (python3 already present).
