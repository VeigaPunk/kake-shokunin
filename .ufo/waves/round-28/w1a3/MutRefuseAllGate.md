# MutRefuseAllGate — round-28 constant-gate mutation probe

- Axes: **operability attacked**; freshness unchanged and not evaluated.
- Both tested constants were **KILLED** by the assigned C1 counter. Neither reached 15/15.
- Scope: only `scripts/citing_set.py:678` (`main`) changed, in this seat's sandbox clone. Each mutant was committed there before measurement. No lane source, index, or Git state was changed.
- Scratch root `S=/fast/scratch/hyaku/kake-r28a3/w1/MutRefuseAllGate`; clone `R=$S/clone`; counter `C=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py`.

## Mutants and expectations

1. Refuse all: replace `main` with unconditional `emit({"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,"findings":[{"id":"input_invalid","reason":"mutant_constant_refuse_all"}]})`; return `EXIT_CANNOT_EVALUATE` (2). No input or CLI argument is consulted.
2. Always clean: same unconditional structure, verdict `clean`, counts 0, findings `[]`; return `EXIT_CLEAN` (0).
3. Expected detector: refuse all passes the 11 defect checks but fails K1–K4, hence exit 1. Always clean fails all defect checks, passes K1/K2, fails K3/K4, hence exit 1. Pristine and exact-restored bytes must pass all 15; a failing baseline would make the probe inconclusive.

## Exact behavioral commands and outputs

Environment for every counter: `TMPDIR=$S TMP=$S TEMP=$S`; Python bytecode disabled by `-B`. Pristine, clean, and restored also set `PYTHONDONTWRITEBYTECODE=1`.
Actual execution order was refuse all, pinned pristine baseline, always clean, restored. The baseline measured the immutable repair commit, not the then-mutated working tree.

```sh
# Refuse-all HEAD eab579d0bc7a70ff6a7704f0473bd43427f3b3d7; exit 1
python3 -B "$C" --root "$R" --revision HEAD --scratch "$S/count"
# Pristine repair; exit 0
python3 -B "$C" --root "$R" --revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch "$S/count"
# Always-clean HEAD 611af42461bdd4f11a37301342f69fe30cdd5e7c; exit 1
python3 -B "$C" --root "$R" --revision HEAD --scratch "$S/count"
# Restored HEAD e20e770d775a5951aacc75f093db158c0eaf631f; exit 0
python3 -B "$C" --root "$R" --revision HEAD --scratch "$S/count"
```

| Stage | Counter exit | Total | Defects | Controls | K4 fixture result |
|---|---:|---:|---:|---:|---|
| Pristine | 0 | 15/15 | 11/11 | 4/4 | exit 0; 0/29 failed |
| Refuse all | 1 | 11/15 | 11/11 | 0/4 | exit 1; 27/29 failed |
| Always clean | 1 | 2/15 | 0/11 | 2/4 | exit 1; 24/29 failed |
| Restored | 0 | 15/15 | 11/11 | 4/4 | exit 0; 0/29 failed |

Refuse-all K1/K2 reported `exit 2, want 0`; K3 reported `exit 2, want 1`; K4 reported `selftest exit 1`. Always-clean defect checks reported `exit 0, want 2`, wrong verdict, and no `input_invalid` finding; K3 reported `exit 0, want 1` and no `unadjudicated_citing_pair`. All counter stderr files were empty; no case timed out.

## Setup, commits, and restoration evidence

Setup command (exit 0): `mkdir -p /fast/scratch/hyaku/kake-r28a3/w1/MutRefuseAllGate && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r28a3/w1/MutRefuseAllGate/clone`.
Each source mutation/restoration used the edit tool. In `$R`, these exact commit commands each exited 0:
```sh
git add scripts/citing_set.py && git -c user.name=MutRefuseAllGate -c user.email=mutrefuseallgate@invalid commit -q -m "mutant: refuse-all constant main (could-not-evaluate exit 2)"
git add scripts/citing_set.py && git -c user.name=MutRefuseAllGate -c user.email=mutrefuseallgate@invalid commit -q -m 'mutant: always-clean constant main exit 0'
git add scripts/citing_set.py && git -c user.name=MutRefuseAllGate -c user.email=mutrefuseallgate@invalid commit -q -m 'restore: exact pristine citing-set main after mutation probes'
```
`git rev-parse HEAD` and `sha256sum scripts/citing_set.py` exited 0 at the recorded stages. Restoration additionally compared the whole restored file with bytes from `git -C "$R" show b5d423fc02057f67a6f3a255808313ce40d29069:scripts/citing_set.py` (exit 0): **exactBytesEqual=true**, 27,458 bytes.

| Source stage | SHA-256 |
|---|---|
| Pristine and restored | `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415` |
| Refuse all | `a2db60310c09b681b4d319730d6c50ce7653388fa1f5fc243d47c468729d4171` |
| Always clean | `5e52d258ddf52ad76e1cf4f8f4968181f7fba76ccad9251ff0ca261ed098721f` |

## Retained evidence

Paths below are under `$S/count`; complete counter JSON, stderr, and command metadata are retained. The counter deletes its temporary exported trees itself.
- `pristine-counter.json:1` — SHA-256 `65acffdf77237841e76daf6cb8cd382af1657139879a9df8fae748fd2bf1cd90`.
- `refuse-all-counter.json:1` — SHA-256 `861795070d2e8fd6eee61f29603ecd6b152bfd83e5c8e4adbeb5d5f06007d564`; K1/K2/K3/K4 start at lines 177/196/215/234.
- `always-clean-counter.json:1` — SHA-256 `c44db28bf7d694fb899606c7120ea4022bdc253924b50cf64c5f1a63295a0baf`; K1/K2/K3/K4 start at lines 199/212/225/242.
- `restored-counter.json:1` — SHA-256 `152295c42559c0d8b582d915b987cb944809b985c45c88dfac3c3b193ef3bb15`.
- `restoration.json:1` and `probe-summary.json:1` record byte equality, hashes, resolved commits, execution order, and exits; `*-command.json:1` records each counter argv and environment.
- Counter SHA-256 at completion: `a30d9d945e90727e704ac99aa2b41a5705b6317ea4037fdb64803e16a8739395`. Contract/control implementation: lane counter lines 119–162, 247–279, 317–331.

Verdict is limited to these two constant-main mutants. No claim about all possible constants, general correctness, freshness, or round admission is made. No additional suites, builds, network operations, installs, upgrades, or other runtime were invoked. No tools were installed or updated.
