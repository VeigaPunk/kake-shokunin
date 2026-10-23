# MutRefPass — 42 single-point reference mutants
Axes: operability and freshness; scoped to the public (h)/(i)/(k)/(c)/(d) contract.
Built M01–M42 as self-contained Python stdlib CLIs: 7 number, 9 URL-character, 6 implicit-allow, 10 group, 10 matching/ranking defects. Every mutant changes exactly one reference source line.
Manifest: /fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/manifest.json — sha256 4f82042ba17690b577399ecf908b6de75efa31d854b05f4e602114d949ec4400. Contains sentence, one-line diff, path/hash, and measured diff count for each mutant.
Detector/evidence: /fast/scratch/hyaku/kake-r38ctl/MutRefPass/local-results.json — sha256 d9a2be9d53b1dcb56a63663e59edd25173dafd3b82d8604a137d5708632bacef; complete argv, expected/actual JSON, stdout/stderr, exit codes and all stage hashes.
Harness: /fast/scratch/hyaku/kake-r38ctl/MutRefPass/generate_mutants.py — sha256 b1dec3639dd21fe4eed33be132735cc133af0bc5bf4a37c858fb121114ac0168. Uses only author-written manifests under the sandbox's probes/ directory, never the sealed counter.
Expected detector: identical `timeout 5s python3 -B <scratch> --manifest <own manifest>` on pristine, mutated and restored bytes; compare JSON plus exit code to the named contract sentence. Each probe includes an unaffected holding check unless the manifest itself is invalid.
Observed local verdict: killed 42; survived 0; inconclusive 0. All 42 pristine and restored probes passed; all 42 mutated probes returned valid JSON without crashing. Actual retained mutant files also passed the common CLI smoke, 42/42.
Observed outputs: M01–04 accepted a non-JSON constant (clean/0); M05/M07 rejected valid ignored integers (input_invalid/2); M06 accepted a long out-of-range status (clean/0); M08–15 accepted forbidden URL characters (clean/0); M16 rejected non-ASCII (check_invalid/2); M17–42 contradicted policy expectations (failed-policy/1). Full findings are in local-results.json.
Restoration: reference before = after = 7c07e969e5e2f6062b9fe1058a60e59516b382fc289ac7184554b408ad3c1414. The reference was never written. Every restoration/Mnn.py scratch copy was restored byte-for-byte to that hash, 42/42; intentionally retained mutants have the hashes below.
Commands/exits: `timeout 300s python3 -B generate_mutants.py` → 0; each `timeout 5s bash -o pipefail -c 'diff "$1" "$2" | wc -l' diff-count <reference> <mutant>` → 1 (expected diff status), stdout `4`; both sha256sum commands → 0; bounded read-only declaration git show → 0.
[INFERENCE] A sealed case exercising a mutant's named edge should reject it; exact sealed scores and predicate results are unknown and belong to L1. No round verdict. No sealed tree access, case search, counter execution, network, installs or upgrades; all spawned commands completed and were reaped. No lane writes except this report.
## Retained files — absolute path and SHA-256
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M01.py cff651bdaa6658c6f18dddd444b94fd3e61aeaf0f34933d26b56247104c3f516
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M02.py 25182a2b78dfb85a6c3fa846c7c70135c0a9d19767d26d310c3d57d00a4e2a93
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M03.py 11eeb211b1ad10ccd7a8e2d4e06653d34d4832463bd7555246d38c28a6705e0d
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M04.py 6073702f60f6fd202bd0fdcf29a717de6646a189286bf19b02fddb70818b766f
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M05.py 5f5f41f93024a0c08b5c037a7675844f5f7b36b1e93e5d69971d3882bf6dcb39
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M06.py 50aa7b0b3d04415e1cccc9d28a7fe7094281e543d0c9bae6309dd4ef9b4c6997
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M07.py b5acdec848ee92987d725fa9bcdec8b7f3956e747a43f6dd23eb4300d8b9bded
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M08.py 9e2a159cbaaf26034390d0b8e23d662cf5e795b7f104e842125c7d593267fcc6
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M09.py 68cfc67c0fd3d1e56cc4325c08b50285a7e29f9579efde7ed4624f7ac95f0f5f
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M10.py 0f4174e02b5b4a4233f4ed2a56c5aff0d15902e5b38c227adb645d6cf63a3f4c
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M11.py 4d1f3f2ab7c80b5178988a744bb53d576802308728b14a32cac4758dcdfda4dc
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M12.py 9ce7db397d8cd5c2f02bb2e86bfba6c2fb0177c42051f64a2af0973e1e66fa25
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M13.py 3058d78c93ec31e976efd22ff35b64e164e4c68611d04d7a2c6768db8e56afb9
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M14.py 7ee6c1681b5e30d6dfb838e70a8141279bfcae0ec877f51b5ba15cadbac49fd1
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M15.py 4adcac486742ab9ba8ca5e913bb6f889a99cd66da5183631bf3d8d8222e6aaca
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M16.py efdca30777b42c94b45e528bb7cdd46d74266d3a22f10412fee6bcf4093d64ac
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M17.py 1f2e69b3932f228c2852deab3c067410956dd911443f1c95c37feb0fdc35819c
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M18.py a54abd9d50c647f0a8d0808899d911eaf52330b639c03339a60678522b86b001
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M19.py f5ebf051b4fc6bec7bcd5caa4321935c649115ee68acd71cdd633dc816e765fc
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M20.py 2b80ce42d17701183bc730d93acffc57c183c2b23be74d7e820bca7206c22f39
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M21.py 53138065a81bfe9167909d9384c934953347c5143b28266b2f0da890f1b9f72e
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M22.py dd4fd900eb47f81f8662cc11613c8bba9dc7b4117540b726757bcd065942be8e
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M23.py 89803818ccdb106cc8082938eddfc568d12be590107d7b765ee7a5d6a6231bce
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M24.py 5323946b7184e65af42e6990ba6072db4cd48f330925df8cfcf9d4662be14507
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M25.py cc2ee7ca3b794885a25d4434a81a96d30519c3634255abdc58b6d5934628fe12
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M26.py ed5a3f47c57bea0bb4f04e5cbd3203d28c253e2f41f43f04c0eb85a5744885fe
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M27.py 734f10e5545b16d69ecaf8e9ae2fb2b3d29f9e43f1a7efb7bb5d24ebb320fc02
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M28.py 744d164eddf7886cd5e46f3f1bd7a0dbc1a444b159c60d0d011ee140aee8642f
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M29.py 4cef9878cd9c8e419fb81aa6cb2454e094c585a9073f16a29556364f28b92f7a
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M30.py 98cf5d594483d7550f0e3df675da3da02229c222d2e6e499de1df9adf5c88040
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M31.py f6add09814b79c2345e23e7e5c7814c0a57c55af4afc25c345ed8347e873f152
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M32.py f408eac27694946cfdca68137222e4d7bd72ab3d004de0c97419fceceb8c4f82
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M33.py 730bd892e778bfe40245b46214d6747405ebf63bc492cef9f5fde596255363a1
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M34.py 4ce3e32cc184faab656d59381e027da525cee3758d1a817d09c51ca3f7a5b87b
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M35.py 156c8898e3a31182020b43bbc8044bb5059a8dd93c8c26d9e33079c2d2133b88
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M36.py e88ff095b0ecfbf8cfa09dae7195e6ae9ecb3da917cc4fc4092be0f9298e231c
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M37.py 06aefabf007b2e925fc77d369cd0e4a6329465ddd9941f33bc568d50fe75103f
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M38.py 38583513b25a1f88de2e78df19227d7c3ac2efa2d9933d9176b580bcef9ff664
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M39.py b3e5e0c9454c2870b939f7dc16e8ad446ed0f618563e933657a999e97fb214ca
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M40.py fe60a4d46b1783d0a83a88631a6963b096b7afcd81c87e1a22a24cbddde80458
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M41.py 72ba10f60e41f78ed05a5b941160630bb77c2b0417723fc31a29054ec1d5ee9a
/fast/scratch/hyaku/kake-r38ctl/MutRefPass/mutants/M42.py dd76b59826a3b731c48de35f5e0935c64a08f60005c02b9dadecf705ed5871ab
