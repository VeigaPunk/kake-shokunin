# ExecCensusModeReceipt — round 33 wave 1

Axes: freshness (current registry count) and receipt quality (census-mode evidence).

## Commands and evidence

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --help` → exit 0. Help documents `census` mode and TSV row, tier, status, and missing metrics. Saved output: `/fast/scratch/hyaku/kake-r33/w1/ExecCensusModeReceipt/help.out`; stderr: `help.err` (empty).
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → exit 0; stdout saved as `/fast/scratch/hyaku/kake-r33/w1/ExecCensusModeReceipt/census-current.out`; stderr empty (`census-current.err`). This selects `kake` from the root roster and reads its current working-tree `corpus/SOURCES.md` without writing to the lane.
- Exact census stdout:

```text
kake\trows\t65
kake\ttier.A\t54
kake\ttier.B\t1
kake\ttier.C\t10
kake\tstatus.mined\t50
kake\tstatus.queued\t6
kake\tstatus.rejected\t9
FLEET\trows\t65
FLEET\ttier.A\t54
FLEET\ttier.B\t1
FLEET\ttier.C\t10
FLEET\ttier.invalid\t0
FLEET\tstatus.queued\t6
FLEET\tstatus.mined\t50
FLEET\tstatus.rejected\t9
FLEET\tstatus.invalid\t0
FLEET\tmissing\t0
```

- `sha256sum /fast/scratch/hyaku/kake-r33/w1/ExecCensusModeReceipt/census-current.out /fast/scratch/hyaku/kake-r33/w1/ExecCensusModeReceipt/census-current.err` → exit 0; stdout hash `b1e5605e918b39a78201b787fb86445ac6987d25be7d8e272cf6ff0654b93159`; empty stderr hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Round-end receipt command

Run the same census command against the root roster at the round-end working tree, saving stdout and exit status separately; use the same invocation for the baseline before edits to make a comparable before/after pair:

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake > census-after.txt 2> census-after.err
```

The current output above is this run's working-tree reading, not an independently preserved pre-edit baseline. No tests, builds, or other checks were run; no tools were installed. No lane file was changed except this assigned report.

Evidence: `/fast/scratch/hyaku/kake-r33/w1/ExecCensusModeReceipt/census-current.out` and `help.out`; script help/mode contract: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` lines 10–38.
