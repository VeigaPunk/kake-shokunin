KILLED: both endian-only controls; neither meets the frozen predicate.
Axes: operability (assigned detector challenge); freshness (no intervention).
Scope: isolated one-line mutations of the reference repair; no round judgment or integration.
Sandbox S: `/fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/` (all short paths below are relative to S).

## Mutants and expected detector
- `little_endian_only.py:189`: replace the decoded-text NUL guard with `text[1::2] and all(c == "\x00" for c in text[1::2])`. Skips BOM-less UTF-16BE; expected rejection by E2/E4.
- `big_endian_only.py:189`: replace the guard with `text[::2] and all(c == "\x00" for c in text[::2])`. Skips BOM-less UTF-16LE; expected rejection by E1/E3/E5.
- Both retain the reference U/R repairs. Mutated probe bytes were preserved as the two rerunnable control tools before restoring the probes.

## SHA-256 and restoration
- H0 = `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b`: reference, both pristine probes, and both restored probes.
- HLE = `0ac183e41d18ba76178efc0c65d4486d0fcae6b1974b2d035ccf2c87a88376ff`: `little_endian_only.py`, identical to mutated `probe-le.py`.
- HBE = `05b5649bfc78c4e063dc93f4f6232741759655de9d0c55cf35168b3f2a4ec297`: `big_endian_only.py`, identical to mutated `probe-be.py`.
- Before → mutant → restored: LE H0 → HLE → H0; BE H0 → HBE → H0. Shared reference remained H0. Retained controls are intentional deliverables.

## Counter outputs (same detector, seed 40001)
| Scored tool / phase | Exit | passed | byClass E / U / R | selftest | met | Receipt |
|---|---:|---:|---|---|---|---|
| probe-le.py pristine | 0 | 30/30 | 9/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | true | receipt-pristine-le.json |
| probe-be.py pristine | 0 | 30/30 | 9/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | true | receipt-pristine-be.json |
| little_endian_only.py mutant | 1 | 28/30 | 7/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | false | receipt-le.json |
| big_endian_only.py mutant | 1 | 27/30 | 6/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | false | receipt-be.json |
| probe-le.py restored | 0 | 30/30 | 9/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | true | receipt-restored-le.json |
| probe-be.py restored | 0 | 30/30 | 9/9 / 13/13 / 8/8 | exit 0, PASS 150/150 | true | receipt-restored-be.json |

## Findings / attacked statements
- `c1_count.py:83-88`: holds for these controls. LE fails E2/E4; BE fails E1/E3/E5. Every failed row reports exactly `exit 0 != 1`; the required outcome was file-level `xml_malformed`, exit 1.
- `SCORECARD.md:2611-2614`: holds in this bounded attack: the little-endian-only partial repair is rejected, as is its big-endian counterpart. No broader rejection or build claim is inferred.
- Round-39 selftest alone does not kill either mutant (both PASS 150/150); the class-E witnesses supply the discrimination. Baselines passed, so these are killed mutants, not inconclusive baseline failures.

## Exact executed commands
```sh
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-le.py --label CtlELittleEndianOnly-pristine-le --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-pristine-le.json # exit 0
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-be.py --label CtlELittleEndianOnly-pristine-be --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-pristine-be.json # exit 0
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/little_endian_only.py --label CtlELittleEndianOnly-LE --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-le.json # exit 1
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/big_endian_only.py --label CtlELittleEndianOnly-BE --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-be.json # exit 1
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-le.py --label CtlELittleEndianOnly-restored-le --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-restored-le.json # exit 0
timeout --kill-after=5s 1200s prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-be.py --label CtlELittleEndianOnly-restored-be --seed 40001 --out /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/receipt-restored-be.json # exit 0
timeout --kill-after=5s 30s prlimit --as=4000000000 sha256sum /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-le.py /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/probe-be.py /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/little_endian_only.py /fast/scratch/hyaku/kake-r40w1/CtlELittleEndianOnly/big_endian_only.py /fast/scratch/hyaku/kake-r40/shared/ref_fix.py # exit 0
```
All bounded counter jobs exited; no background job or service was started. At most two counters ran concurrently. No network used; no tools installed or upgraded.
