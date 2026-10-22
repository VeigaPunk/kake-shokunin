# Round 35 sealed-counter mutation probe

Axes: operability (counter refusal and verdict gates); freshness (pinned texts and sourced-citation gates). I used the 318561efa base in my own clone and a private synthetic Git repo with fake C1 cases/C2 probes; patched only scratch copies' SHA pins. The prohibited `/fast/scratch/hyaku/kake-r35/sealed/` was never accessed. No tools installed.

## Commands and fixture

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/clone && git -C /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/clone checkout -q 318561efa67206699fdaf259ffb86e39f2d916a8` — exit 0.
- `timeout 90s python3 -B /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/prepare_fixtures.py` — exit 0; built fake C1/C2 JSON keys, a scripted fake audit tool, and candidate revisions.
- `timeout 60s python3 -B /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/update_shared_fixture.py` — exit 0; unified C1 cases (24 total) to one pinned fake key: SHA-256 `108510f55f444b626e55350648511e3d7b8191345811708a6c4f904629260b66`. C2 key SHA-256 `f8959be94be714edaf7b43fe741783eabcab601a9f046bcec353c9aab501696e`; fake source hashes/revisions: `fixture-scenarios.json:1-31`.
- First `timeout 300s python3 -B /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/run_matrix.py` — exit 2, inconclusive: two distinct C1 fake keys did not match the one patched C1 pin. The shared-key fixture fixed this; the final run below is authoritative.
- Final `timeout 300s python3 -B /fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/run_matrix.py` — exit 0. It ran the same bounded CLI detector on pristine, mutated, then byte-restored copies for each mutant.

`ROOT=/fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/fixture-repo`; `D=/fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/mutants`; C1 base revision `92ae67815f3a29d0e53b188c5b95a438d4b34f37`; visible-key revision `681a5b87f5dfd29bdb79a57ff09a86b4d6c3f361`; C2 pinned/used-by/fenced revisions `f78eea92c05a073e9aa44bc1f73d6caff2f8901e` / `8816a9c9e54c55c6f423f9d7d4a2737b1ace04cc` / `c035cadf2f51e6e244899ae0eafa3625bff276e8`. Exact argv, stdout, stderr, and exits for all three runs per mutant are in `/fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/matrix-results.json` (SHA-256 `00f9e14c0560a648795b835018f7fe12fe9946b02de2e6727651f5c63ab34f0c`).

## Mutant table

The command column is the mutated invocation; pristine/restored runs used identical arguments with `pristine.py` instead of the mutant file. `K1=/fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/keys/c1-all.json`; `K2=/fast/scratch/hyaku/kake-r35/w1/MutSealedCounter/keys/c2-probes.json`.

| Mutant | Detected | Observed output (pristine → mutant) | Mutant SHA-256 | Command |
|---|---|---|---|---|
| Drop key-visible refusal | Yes | exit 2, visible-key refusal → exit 1, C1 21/24, no refusal | `9b034fa52e6e8c02a04e66ab52a4b569a9f91a9550449ed5989a28324ca4afe5` | `/usr/bin/python3 -B $D/key-visible.py c1 --root $ROOT --revision 681a5b87f5dfd29bdb79a57ff09a86b4d6c3f361 --key-revision 681a5b87f5dfd29bdb79a57ff09a86b4d6c3f361` |
| Drop pinned-text check | Yes | exit 1, pinned/copy false → exit 0, pinned/copy true, met | `1adce11789310b730d8a1ac5184e439039e84aae5f54ea179dea93b9f52d1a43` | `/usr/bin/python3 -B $D/pinned-check.py c2 --root $ROOT --revision f78eea92c05a073e9aa44bc1f73d6caff2f8901e --key-file $K2` |
| Compare findings as set | Yes | exit 1, 21/24 → exit 0, 22/24, met | `132f9757dc3211febd71bef36261df09724ffe8dfce4ad4d1d8f069c9d7132e3` | `/usr/bin/python3 -B $D/findings-set.py c1 --root $ROOT --revision 92ae67815f3a29d0e53b188c5b95a438d4b34f37 --key-file $K1` |
| Skip verdict compare | Yes | exit 1, 21/24 → exit 0, 22/24, met | `d693ec5744c18ee13d700a3d8f365f261005a984a87c66007b5783172cbc52c4` | `/usr/bin/python3 -B $D/verdict.py c1 --root $ROOT --revision 92ae67815f3a29d0e53b188c5b95a438d4b34f37 --key-file $K1` |
| Accept any exit | Yes | exit 1, 21/24 → exit 0, 22/24, met | `53e41ee7414229314a693126f896a9590e2a4b6010bbbe288f6a76bdc719d073` | `/usr/bin/python3 -B $D/exit-check.py c1 --root $ROOT --revision 92ae67815f3a29d0e53b188c5b95a438d4b34f37 --key-file $K1` |
| Count cites without used-by | Yes | exit 1, 2 good cites/cites false → exit 0, 3 good cites/cites true | `86e8972626c3ae0906ab8aa98641454784284b64f66586a177e9336549a37ecf` | `/usr/bin/python3 -B $D/used-by.py c2 --root $ROOT --revision 8816a9c9e54c55c6f423f9d7d4a2737b1ace04cc --key-file $K2` |
| Count fenced registry rows | Yes | exit 1, 2 good cites/cites false → exit 0, 3 good cites/cites true | `15721240c5b68e993ddacdef05dd570f87466681253b1100414ea16f93ebe666` | `/usr/bin/python3 -B $D/fenced-row.py c2 --root $ROOT --revision c035cadf2f51e6e244899ae0eafa3625bff276e8 --key-file $K2` |
| Invert C2 probe threshold (`>=` to `<`) | Yes | exit 0, 9/12 probes/met → exit 1, probe condition false | `608969c12cd883e799363909e84f50b3bf96bc42db50be5ea0c477f28e772006` | `/usr/bin/python3 -B $D/threshold.py c2 --root $ROOT --revision 92ae67815f3a29d0e53b188c5b95a438d4b34f37 --key-file $K2` |

## Verdict and restoration

All eight mutants were detected; survivors: none. Each pristine baseline and restored run matched its fixture oracle. Pristine/before and restored SHA-256 for every probe: `dbba80692cd361c1e4d25b465e58bacf674846dace7d986b3a1d90e86a1afd3d`; all eight `restored_exact` values are true. Per-mutant outputs and before/mutant/restored hashes: `matrix-results.json:24-217,218-532,533-934,935-1336,1337-1738,1739-2051,2052-2364,2365-2670`. No project build, tests, lint, or formatting were run; only the assigned counter matrix was exercised.

Report: `.ufo/waves/round-35/w1/MutSealedCounter.md`
