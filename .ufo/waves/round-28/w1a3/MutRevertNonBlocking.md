# MutRevertNonBlocking — C1 counter sensitivity probe (round 28, wave 1a3)

Role: UFO-FSD mutation tester (leaf). Target claim C1 (operability, repair-first).
Probe: restore the round-27 blocking `open(target, 'rb')` read in `WorkingTreeSource.read_document`
and show the C1 counter catches it.

## Mutation
- Sandbox: `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r28a3/w1/MutRevertNonBlocking/clone`
- One mutation in `clone/scripts/citing_set.py::WorkingTreeSource.read_document` (lines 213–238 at b5d423f):
  replaced the repaired non-blocking `os.open(..., O_NONBLOCK)` + `S_ISREG` check + `os.fdopen`
  body with the round-27 blocking version:
  ```python
  def read_document(self, relative):
      target = os.path.join(str(self.root), relative)
      if not is_inside(self.root, target):
          raise InputInvalid("path_escapes_root", relative, "document")
      try:
          with open(target, "rb") as handle:
              return handle.read()
      except OSError as exc:
          raise InputInvalid(
              "document_unreadable", relative, "document", detail=exc.strerror or type(exc).__name__
          )
  ```
  Diff: 1 insertion, 16 deletions in `scripts/citing_set.py` only (verified via `git diff` before commit).
- Commit in clone: `git -c user.name=mut -c user.email=mut@invalid commit -qam mut` → `42174e01ebf1dd8c554acdcc5382ea178ecfd942`.
- Hashes of `scripts/citing_set.py`: pristine b5d423f `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415`; mutated HEAD `d757565317e79ab27fcb9c8783c6dc3b4360eeac95ff33046f0649924cb317d0`. Pristine bytes remain intact in the clone history at b5d423f (reference run below re-exported them). Scratch clone is the disposable mutant artifact; no lane files touched.

## Counter runs (exact commands, exit codes)
Commands (both with `TMPDIR=/fast/scratch/hyaku/kake-r28a3/w1/MutRevertNonBlocking`):
1. Mutated: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py --root /fast/scratch/hyaku/kake-r28a3/w1/MutRevertNonBlocking/clone --revision HEAD --scratch /fast/scratch/hyaku/kake-r28a3/w1/MutRevertNonBlocking/count` → **exit 1** (wall 41.3 s; FIFO cases each timed out at 20 s).
2. Reference: same with `--revision b5d423fc02057f67a6f3a255808313ce40d29069` → **exit 0** (wall 1.3 s).

Outputs (JSON saved at `count-mutated.json`, `count-ref.json` in the scratch dir; `path:line` for source of checks = `c1_interface_count.py:176-258`):

| Run | passed/total | defect | control | Exit |
|---|---|---|---|---|
| Mutated HEAD 42174e0 | **13/15** | 9/11 | 4/4 | 1 |
| Reference b5d423f | 15/15 | 11/11 | 4/4 | 0 |

Mutated failing checks:
- `U1-population-fifo`: `['timed out after 20s', 'exit None, want 2', 'stdout is not one JSON object']`
- `U2-ledger-fifo`: same.
Controls K1 (valid-clean-working-tree), K2 (valid-clean-git), K3 (valid-failed-missing-pair), K4 (fixture-selftest) all passed in the mutated run, confirming the gate still works on valid input; only the FIFO refusal regression is exposed.

## Verdict
**Mutant killed.** The counter drops 15/15 → 13/15 (exit 1) with exactly U1 and U2 failing; controls K1–K4 stay green. The blocking-read regression is detected; no counter gap observed in this probe. Not verified: deep-JSON (U3/U4) and corpus-surface (A1–A7) sensitivity under this mutation (unaffected by the change; reference run confirms they pass at b5d423f).

## Tooling
No installs/updates made (no pacman, uv, or binaries needed; plain python3/git used). Scratch root: `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertNonBlocking/`.
