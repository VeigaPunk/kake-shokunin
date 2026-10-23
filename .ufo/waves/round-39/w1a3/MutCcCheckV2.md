# MutCcCheckV2 — r39-controls-a3
Axes: operability (mutation sensitivity); freshness held unchanged (no network or publishing).
Pinned source: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/criteria/control_consequence_check.py` at `72edf2123f92b9dc546494cbffcc777ed3c3cd3a`; SHA256 `39d6e4ed36d3a5b6a72bf53bd6dd954d921d5e9b324eec8f3f0298ef0af100a0`.
`S=/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2`; `C=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/sealed_count.py`. All fixture and log paths below are relative to S unless absolute.
Built 16 one-point mutants, copied all 14 authorized a3 receipts byte-for-byte into `S/rx/`, and authored 13 focused receipt fixtures; source/copy hashes are in manifest.json.
Verdict: selftest killed 8/16 and survived 8/16; adding the copied-receipt CLI detector kills M07 and M09, leaving 6 survivors. Focused fixtures killed all 16; no inconclusive baselines.
Restoration: every mutable `S/subjects/M*.py` ran pristine → mutated → restored, with identical commands, outputs, exits and SHA256 before/after; all 16 restored to the pinned SHA above. Immutable mutant artifacts remain under `S/mutants/`.
Pristine/restored output: `PASS 14/14` (exit 0); copied receipts: `receipts read 14; build receipts meeting 0; oracle-exempt 0; controls meeting 1; problems 0` (exit 1, ref.json).
Exact commands (cwd S; every subprocess has a 20 s process-group deadline; two workers; inherited 4 GB AS cap):
`timeout --kill-after=5s 300s prlimit --as=4000000000 python3 -B probe.py --phase init` → 0; same prefix with `--phase baseline`, `mutated`, `artifacts`, `restored` → 0 each.
For every artifact M: `python3 -B M --selftest` and `python3 -B M --root S/build-root --counter C --receipts S/rx`; actual absolute argv/stdout/stderr/exit for every run are retained in `*-results.json`.
Focused command substitutes `--receipts S/fx/F`; only F=same_bytes_build adds `--build-revision HEAD`. No command supplies --oracle-sha. Table exits are actual, not inferred.
Fixture Git initialization/add/commit/rev-parse all exited 0; exact argv in init-results.json. This synthetic, never-executed byte-identity file is not the claimed sitemap tool.
Columns: PASS = selftest output; rc = selftest exit; Rx = copied-receipt exit; F expected→mutant = pristine/restored exit versus mutant exit (all focused detectors killed).
| Mutant artifact (absolute path) | SHA256 | Single-point change (source line) | Selftest; rc; verdict | Rx | Killing F; expected→mutant |
|---|---|---|---|---|---|
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M01_name_build.py` | `47c7369b050012987424213041e306b8dc74187a57fc0ef3cb600f023082ef97` | filename build-* overrides tool bytes (:83) | PASS 13/14; 1; **killed** | 1 | `filename`; 1→0 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M02_label_build.py` | `1386fbe2ccd212e4a96d8b3fc2336e68a0dc7ec2ac9c5ad5b1ed9082521c10c5` | label build overrides tool bytes (:83) | PASS 12/14; 1; **killed** | 1 | `label`; 1→0 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M03_trust_met.py` | `5161afc68db05cd2576cfa2699dd6e4aecf04fb3b4fc7e57815e313226e81e62` | trust met rather than rows (:76) | PASS 12/14; 1; **killed** | 1 | `lying_met`; 2→0 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M04_ignore_counter.py` | `2bc9c238e8536d2d14c3cf35a3c44f5e414d4c71fb36ee31c531c96fc3cadb7f` | ignore counterSha256 (:66) | PASS 13/14; 1; **killed** | 1 | `foreign_counter`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M05_ignore_key.py` | `d4149777d30335cbf8be841be6cee13dade46b2c2b0c27888eb14c62aa18447a` | ignore keySha256 (:67) | PASS 14/14; 0; **survived** | 1 | `foreign_key`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M06_revision_identity.py` | `e82298819616da155fd9abd1309ac0595170bc775e34785b0ea3217751cfe896` | build identity is revision text, not bytes (:107) | PASS 14/14; 0; **survived** | 1 | `same_bytes_build`; 0→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M07_implicit_oracle.py` | `7ecde614390001142ff5f2a39885b88d2bb0ed03e27dc7d4bab1fb9d3b9fc64e` | ref exempt without --oracle-sha (:85) | PASS 14/14; 0; **survived** | 0 | `unnamed_ref`; 1→0 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M08_no_recursion.py` | `c4cd7719c89bbac2e6a29de02b1c61aac62fe8c28cae2fa16d0ab708eeb339c6` | visit only receipts root (:53) | PASS 13/14; 1; **killed** | 1 | `nested`; 1→2 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M09_swap_control_exit.py` | `4186f01ab2cc05a30a6081dffe664a7f8d8f9f56a82f8d79406f81d5c09223aa` | swap CLI control/clean exits (:120) | PASS 14/14; 0; **survived** | 0 | `unnamed_ref`; 1→0 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M10_problem_exit_one.py` | `8238207e1cb684c0c7cd30dc2bcefcb1328e1850e3e9cbb18237e6fd067dfc03` | CLI input error exits 1 instead of 2 (:119) | PASS 14/14; 0; **survived** | 1 | `foreign_key`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M11_rows_plus_one.py` | `76f3b6d3fff3b5e61c9e94f5a0f2fec550ad1b473ab3bfdb990549ed99f2ef43` | allow one extra row (:76) | PASS 14/14; 0; **survived** | 1 | `extra_row`; 0→2 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M12_ignore_target.py` | `b091b3f0a5f098bdee585ceaf93341dcc0ac939132192c015ac1d45884d689ae` | ignore receipt target pin (:68) | PASS 14/14; 0; **survived** | 1 | `foreign_target`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M13_truthy_pass.py` | `8d0959c78aa739a3c9aa0da9aa5790216377bbb246980d0ab2b6fface6e73fc3` | count truthy non-booleans as passes (:75) | PASS 13/14; 1; **killed** | 1 | `string_pass`; 0→2 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M14_ignore_passed.py` | `d69237b0b87eebf1bea365329507e6c8b45ff942a5238935f0e76c35793d7219` | ignore contradictory passed total (:77) | PASS 14/14; 0; **survived** | 1 | `wrong_passed`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M15_ignore_predicate.py` | `5a45ef5a24ac48654ea8cdf87c959e1fa08cb0eb3b17d3a32af419d931a08d40` | ignore predicate pin (:66) | PASS 13/14; 1; **killed** | 1 | `foreign_predicate`; 2→1 |
| `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/mutants/M16_strict_target.py` | `7cd76a75ec6407a7425cc1687f2e4dd45012e4e56b0505a73c8559e357bfd172` | reject exact target equality (:76) | PASS 6/14; 1; **killed** | 2 | `unnamed_ref`; 1→2 |
Killing fixture definitions (all actual files under S/fx, built from the authorized ref receipt, not the sealed key):
`foreign_key/r.json`: keySha256=64 zeroes; `foreign_target/r.json`: target=23; `wrong_passed/r.json`: passed=23 while all 24 rows pass.
`same_bytes_build/r.json`: matching SHA256 of synthetic `S/build-root/scripts/sitemap_audit.py`; pristine --build-revision HEAD recognizes identical bytes (0), M06 compares revision text (1).
`unnamed_ref/r.json`: unchanged meeting ref receipt, no oracle flag; this also exists as S/rx/ref.json. M07 prints EXEMPT; M09 prints CONTROL-MEETS but exits 0.
`extra_row/r.json`: 24 passing rows plus a 25th false row, passed=24, met=false; pristine ignores it as nonmeeting (0), M11 wrongly reports a met mismatch (2).
Other killing files: `filename/build-x.json`, `label/r.json`, `lying_met/r.json`, `foreign_counter/r.json`, `nested/sub/r.json`, `string_pass/r.json`, `foreign_predicate/r.json` (full contents packaged).
Findings (coverage only; checker/contract unchanged):
`.ufo/waves/round-39/criteria/control_consequence_check.py:162-164`: selftest calls evaluate and duplicates exit calculation, bypassing main/build lookup; M06/M09/M10 survive.
`.ufo/waves/round-39/criteria/control_consequence_check.py:149-154`: negative matrix omits foreign key/target, wrong passed total, long rows, and ref-label implicit exemption; M05/M12/M14/M11/M07 survive.
Evidence archive: `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/MutCcCheckV2-evidence.tar.gz`; SHA256 `c7dc6ae3a68d74264d8830508c6cc036e7e0de11d4a953556976a50720df020e`.
Detector: `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/probe.py`; SHA256 `d85df3286008b6d2476f08c310705711b99bdbf4e73b71d6d76d8e92ee847ae2`.
Manifest: `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/manifest.json`; SHA256 `d6513cb3976959d2cce343538755e5635fee4427048a2da1735dd21387f249a4`.
Verdicts/restoration: `/fast/scratch/hyaku/kake-r39a3w1/MutCcCheckV2/summary.json`; SHA256 `111b91e049332d3ff5eef42643b5ed0c7f484ad8572022293e80e055a6a2da71`.
Archive command `timeout 30s tar --sort=name -czf MutCcCheckV2-evidence.tar.gz pristine.py control_consequence_check.py probe.py manifest.json summary.json mutants subjects rx fx build-root init-results.json baseline-results.json mutated-results.json restored-results.json artifacts-results.json` → 0; `timeout 20s sha256sum ...` → 0 (hashes above).
Tools: Python 3.14.8, Git 2.56.0 (version commands exit 0); no installs/updates. No sealed key/reference implementation read, no counter execution, no lane mutation except this report, no running child processes remain.
Raw-read final-LF loss was reported to xd://report_issue; exact LF bytes were reconstructed only after hashes matched immutable source/receipt hashes, before any detector ran.
