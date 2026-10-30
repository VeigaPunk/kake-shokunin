# ExecLandedCheck — round 64

## Verdict
All three required commits exist and are ancestors of `master` at the checked lane tip. The round-64 T0 resolver run found **0 dangling IDs** (`unresolved` count 0). No repository files other than this assigned report were written.

## Evidence

- Repository: `/home/vgpnk/Projects/shokunin/kake-shokunin`; `git rev-parse --show-toplevel` output: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- Checked branch: `master`; `git rev-parse master` output: `cc8add1fa740b920ea5179a71152680ab220c70c`.
- Exact commands and results (run from the repository):
  - `git -C /home/vgpnk/Projects/shokunin/kake-shokunin merge-base --is-ancestor 1a48131577ba82c967650561be34e8dba909432a master` → exit `0` (`base`).
  - `git -C /home/vgpnk/Projects/shokunin/kake-shokunin merge-base --is-ancestor 4c8295fa5e3b628f1fdf3840299ae415c01849fb master` → exit `0` (`T0`).
  - `git -C /home/vgpnk/Projects/shokunin/kake-shokunin merge-base --is-ancestor cc8add1fa740b920ea5179a71152680ab220c70c master` → exit `0` (`receipts`).
  - `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb --fleet /home/vgpnk/Projects/shokunin/kake-shokunin/..` → `ids_cited=116 ids_resolved=116 dangling=0 owned_elsewhere=0 unowned=0` (exit `0`).
- Usage evidence read from `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py:11-19,33-36`: `--root`, `--revision`, and `--fleet` options; revision reads use the selected revision's tree/blob contents; exit 0 means dangling IDs are zero. `landed_check.py` usage read from `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/landed_check.py:4-7`; its report-based ancestry interface is available, and direct ancestry checks were used for these exact commits.
- No tools installed or updated.

## Limits
This check establishes ancestry of the requested commit IDs against `master` as resolved at run time and resolver status/count at T0. It does not make claims beyond those measured results.
