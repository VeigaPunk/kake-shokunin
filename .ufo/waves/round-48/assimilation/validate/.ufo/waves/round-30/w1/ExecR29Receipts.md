# Round-30 wave 1 — round-29 receipts re-run with provenance (ExecR29Receipts)

Seat: KakeR30.ExecR29Receipts (leaf executor, operability axis). Lane repo touched only for this
report; no round-29 file was edited. Sandbox: `/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/`.

## 1. What I attacked

Round-29 routed defect 3: the receipts `.ufo/waves/round-29/verification/selftest-lane-final.json`
and `.ufo/waves/round-29/real-input/out/summary.json` name no revision and no tool digest, so a
reader cannot tell which bytes produced the numbers. I re-ran both round-29 demonstrations against
the committed bytes of the lane revision and wrote receipts that name what they measured
(revision, script digests, interpreter, commands with exit codes, outputs).

## 2. Revision and digests (provenance of the re-run)

- Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`, HEAD `4580c78cca1185d059efa6970722bbcf2f9c1b0f`
  ("round-30: declaration before implementation", 2026-10-22T08:52:57-03:00); sandbox clone `clone/`
  at the same revision, working tree clean (`git status --porcelain` empty).
- `scripts/base_path_audit.py` sha256 `c5a13a32e7a232e1a3079ed4275333339d6c197ac42b5fbdfbbb08e1e4ba1dc0` (29312 bytes)
- `scripts/base_path_selftest.py` sha256 `e6f21acb654119bf17175632eaf3bcc4a27bdd8965b1e19b7aa13b1148317e4b` (12336 bytes)
- `.ufo/waves/round-29/real-input/real_input_run.py` sha256 `324be40fd47e050f41cd2a65e7b4026ba3a52df8fc1ef8f131beffeeaa8d4bd0` (4908 bytes)
- Fixture tree `scripts/fixtures/base-path`: 45 case dirs, tree sha256 `a0dafac3b0ec033b91271450345747d77ee3b9037597d59beed3d7df53a52dad`
- Real-input site tree sha256 `b2c194c7f9f4b68fcc95b038cb5fb8c1d34af2c1f4936f711559f363c963986d`; page digests
  charter-ghp `7c243a1d…3aba`, lucario-ghp `bee2d9f5…6cff`, plazir15-ghp `d82af77a…2af18e` (byte-identical
  to `.ufo/waves/round-23/live/<site>/page.html` in the same clone).
- Python: CPython `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`, `/usr/bin/python3`,
  Linux 7.2.11-arch1-1 x86_64, `TMPDIR=/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/tmp`. The lane
  working copy of both scripts hashes the same as the committed bytes at 4580c78 (no drift today).
  No network: only committed local snapshots were read.

## 3. Commands, exit codes, outputs

```
python3 -B scripts/base_path_selftest.py                                    # exit 0, "45/45 fixtures passed"
python3 -B .ufo/waves/round-29/real-input/real_input_run.py \
  --tool scripts/base_path_audit.py --sites .ufo/waves/round-29/real-input/sites \
  --out <sandbox>/out/round-30/r29-rerun/real-input                          # exit 0
```
Runner table (exit 0): `charter-ghp 1 failed-policy 1 page 67 refs 3 findings | lucario-ghp 0 clean 1 1 0 |
plazir15-ghp 1 failed-policy 1 46 1 | totals sites=3 pagesChecked=3 referencesChecked=114 findings=4 failedSites=2 contractProblems=0`

## 4. Old vs new numbers

| number | round-29 committed | round-30 re-run | equal |
|---|---|---|---|
| selftest cases / passed / failed | 45 / 45 / 0 | 45 / 45 / 0 | yes |
| selftest verdict, case-name list | clean, 45 names | clean, identical list | yes |
| sites | 3 | 3 | yes |
| pages checked | 3 | 3 | yes |
| references checked | 114 | 114 | yes |
| findings | 4 | 4 | yes |
| failed sites | 2 | 2 | yes |
| contract problems | 0 | 0 | yes |
| site exits (charter / lucario / plazir15) | 1 / 0 / 1 | 1 / 0 / 1 | yes |

No numeric difference. Per site the whole row object, the tool `result` object, the tool stdout and
the tool stderr are byte-equal to the committed `real-input/out/<site>.json` (exits 1 / 0 / 1,
findings 3 / 0 / 1). Totals object equal.

## 5. Provenance difference found (the routed defect, confirmed)

- Committed `selftest-lane-final.json` (sha256 `0bc3ebb1211971836af3910c8e13f2a399ac7cc6765885b38ff8010d23db7fbb`,
  authored at d8cd2e4) carries no revision, no tool digest and no interpreter version.
- Committed `real-input/out/summary.json` (sha256 `f04238dbeae56180b22f187a0ebe8fca3061ac2e48e484ff25177dab4025ba0d`,
  authored at 98dbab2) carries the same three gaps; the three per-site files name an interpreter path
  inside the recorded `argv` but no version and no digest.
- Consequence found by re-running: the committed real-input receipts were authored at 98dbab2, when
  `scripts/base_path_audit.py` still hashed `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`.
  The tool changed at d8cd2e4 (cross-scheme handling, new --help text) and now hashes `c5a13a32…1dc0`.
  Because the receipts name no digest, a reader could not tell the committed numbers came from the
  older tool bytes. The numbers are nevertheless identical under the current tool: the three snapshots
  hold no `http://` reference, so the changed branch never fires. The committed selftest receipt and the
  current tool agree on all 45 fixture names, so the 45-case floor added at d8cd2e4 holds.

## 6. Receipt paths (sandbox, absolute)

- Main receipt `/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/out/round-30/r29-rerun/receipt.json`
  (sha256 `a6d43778560b0bf63554a450cb99721260d50e214176163a9170b1df2e7f7993`): provenance, both commands
  with exit codes and outputs, parsed summaries, old-vs-new table, per-site comparison, provenance gap.
- Selftest stdout JSON `…/r29-rerun/selftest.stdout.json` (`13fe8821ca893d2a…7861b`), stderr
  `…/r29-rerun/selftest.stderr.txt` (`ad88ba50cf24f98…db94c`).
- Real-input outputs under `…/r29-rerun/real-input/`: `summary.json` (`ca22884d8bb65235…f637`),
  `charter-ghp.json` (`71c9dc1578a1bd07…f3ad`), `lucario-ghp.json` (`dc573132059b7343…5f0`),
  `plazir15-ghp.json` (`234356f504ec6b56…337`); stdout `…/r29-rerun/real-input.stdout.txt` (`1e8bc03f…b0232`).
- Machine-readable old-vs-new diff `…/r29-rerun/compare-r29.json` (`e5c46c836eb17400…b061`); generators
  `/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/make_receipts.py` and `compare_r29.py`; clone
  `/fast/scratch/hyaku/kake-r30/w1/ExecR29Receipts/clone`.

## 7. Not verified / risks

- I did not run the round-29 C1/C2 counters, the C2 matrix counter, `citing_set*`, or any freshness or
  live-probe script; nothing was fetched from the network and no owned web property was contacted.
- The receipts do not prove the committed round-29 receipts were produced by the tool bytes that carry
  digest `e3264615…`; that digest comes from the round-29 wave-2 seat reports, not from the receipts.
  My own receipts are byte-tied to `c5a13a32…1dc0` at 4580c78.
- The re-run used the clone's committed copies of the site snapshots; I verified their digests against
  the round-23 live copies in the same clone, not the round-23 originals on disk. No package was installed
  or upgraded (pacman paused host-wide); the run used the preinstalled CPython 3.14.8.
Report: .ufo/waves/round-30/w1/ExecR29Receipts.md
