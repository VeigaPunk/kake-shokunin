MET: three lookup-only normalization controls meet 30/30 + selftest 150/150 while missing exact repeated string ids after an invalid check.
Axes: operability (attacked); freshness (unchanged). No round judgment or integration is made here.
All artifacts below are under `S`; all controls start from read-only reference `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b`.
`R=/home/vgpnk/Projects/shokunin/kake-shokunin; S=/fast/scratch/hyaku/kake-r40w1/CtlRCaseFold`
Exact-command aliases (expansions match executed commands; full commands/receipts also in `S/evidence.json`):
`C="timeout 1200 prlimit --as=4000000000 -- python3 -B $R/.ufo/waves/round-40/c1_count.py --root $R"`
`D="timeout 240 prlimit --as=4000000000 -- python3 -B $S/identity_probe.py"`
Each counter selftest below is `{exit:0, summary:"PASS 150/150"}`; class order is E,U,R; seed is 40421.
| Tool under S | sha256 | Receipt under S | passed; E,U,R | met; exit; verdict |
|---|---|---|---|---|
| `control_casefold.py` | `424ae8cac4a9756f822c8eabf6d7e09ef4112942718f7635b282056d1e463750` | `receipt-casefold.json` | 29/30; 9/9,13/13,7/8 | false; 1; killed |
| `control_lower.py` | `f4fddb3ef0f72ad87cbeb93c246e0ae0db2c38bf5dcd1f9859b8f3b242188002` | `receipt-lower.json` | 29/30; 9/9,13/13,7/8 | false; 1; killed |
| `control_nfkc_casefold.py` | `0d13623ce8584b187348897d1cf681440bb92ae1c9dfe2b6492adc1614d4d1a8` | `receipt-nfkc-casefold.json` | 29/30; 9/9,13/13,7/8 | false; 1; killed |
| `control_nfkc.py` | `fe2a8651591252568450e45088273dee1618d9baf7171f6b9edf235fa26a7573` | `receipt-nfkc.json` | 30/30; 9/9,13/13,8/8 | true; 0; survived |
| `control_lookup_casefold.py` | `02fc6b602f7155bb9bf21f88e3e2405206f22fe2980a6272ed40f688294096e2` | `receipt-lookup-casefold.json` | 30/30; 9/9,13/13,8/8 | true; 0; survived |
| `control_lookup_lower.py` | `a1801de1c0300b2238a5e8f5ab41dedc9492b4f38f2a12ad52ef5173029ffd2b` | `receipt-lookup-lower.json` | 30/30; 9/9,13/13,8/8 | true; 0; survived |
| `control_lookup_nfkc.py` | `da201fc85bbe6ff80e54c4828f4f4bcf246695884b58113f20d98d3710449956` | `receipt-lookup-nfkc.json` | 30/30; 9/9,13/13,8/8 | true; 0; survived |
Per-tool skipped work and catching witnesses:
- `control_casefold.py:339-340`: replaces exact string identity with casefold identity; R8 caught it: second check `error/check_invalid`, expected `clean/null`.
- `control_lower.py:339-340`: lowercased identity instead of exact string identity; R8 caught the same over-rejection.
- `control_nfkc_casefold.py:340-341`: NFKC+casefold identity instead of exact identity; R8 caught the same over-rejection.
- `control_nfkc.py:340-341`: NFKC identity collapses distinct strings; no frozen witness caught it. Diagnostic `distinct-nfkc` caught `Ａlpha`/`Alpha`. Harm-only caveat: this retains positive E/U/R repairs, so SCORECARD.md:2616-2618 may exclude it as a C1 control; not relied on for the finding.
- `control_lookup_casefold.py:339`: casefolds lookup but reserves raw ids; skips exact uppercase/Unicode repeats after invalid checks; no frozen witness caught it; meets.
- `control_lookup_lower.py:339`: lowercases lookup but reserves raw ids; skips those exact repeats; no frozen witness caught it; meets.
- `control_lookup_nfkc.py:340`: NFKC+casefold lookup with raw reservations; skips those exact repeats; no frozen witness caught it; meets.
Executed counter commands (aliases above; every output is retained in its receipt):
`$C --tool-file "$S/probe.py" --label CtlRCaseFold-pristine --seed 40421 --out "$S/receipt-pristine.json"` -> exit 0.
`$C --tool-file "$S/control_casefold.py" --label CtlRCaseFold-casefold --seed 40421 --out "$S/receipt-casefold.json"` -> exit 1.
`$C --tool-file "$S/probe.py" --label CtlRCaseFold-mutated --seed 40421 --out "$S/receipt-mutated.json"` -> exit 0.
`$C --tool-file "$S/control_lower.py" --label CtlRCaseFold-lower --seed 40421 --out "$S/receipt-lower.json"` -> exit 1.
`$C --tool-file "$S/probe.py" --label CtlRCaseFold-restored --seed 40421 --out "$S/receipt-restored.json"` -> exit 0.
`$C --tool-file "$S/control_nfkc_casefold.py" --label CtlRCaseFold-nfkc-casefold --seed 40421 --out "$S/receipt-nfkc-casefold.json"` -> exit 1.
`$C --tool-file "$S/control_nfkc.py" --label CtlRCaseFold-nfkc --seed 40421 --out "$S/receipt-nfkc.json"` -> exit 0.
`$C --tool-file "$S/control_lookup_casefold.py" --label CtlRCaseFold-lookup-casefold --seed 40421 --out "$S/receipt-lookup-casefold.json"` -> exit 0.
`$C --tool-file "$S/control_lookup_lower.py" --label CtlRCaseFold-lookup-lower --seed 40421 --out "$S/receipt-lookup-lower.json"` -> exit 0.
`$C --tool-file "$S/control_lookup_nfkc.py" --label CtlRCaseFold-lookup-nfkc --seed 40421 --out "$S/receipt-lookup-nfkc.json"` -> exit 0.
Pristine/mutated/restored counter runs all passed 30/30, E9/9,U13/13,R8/8, selftest 150/150, met=true; the frozen detector therefore survived the one-line mutation.
Executed diagnostic commands (same bwrap runner/judge; 60-second child timeout; actual stdout/stderr retained):
`$D --tool /fast/scratch/hyaku/kake-r40/shared/ref_fix.py --out "$S/identity-pristine.json"` -> exit 0, 3/3.
`$D --tool "$S/probe.py" --out "$S/identity-mutated.json"` -> exit 1, 1/3 (before restoration).
`$D --tool "$S/probe.py" --out "$S/identity-restored.json"` -> exit 0, 3/3 (after restoration).
`$D --tool "$S/control_nfkc.py" --out "$S/identity-nfkc.json"` -> exit 1, 2/3.
`$D --tool "$S/control_lookup_casefold.py" --out "$S/identity-lookup-casefold.json"` -> exit 1, 1/3.
`$D --tool "$S/control_lookup_lower.py" --out "$S/identity-lookup-lower.json"` -> exit 1, 1/3.
`$D --tool "$S/control_lookup_nfkc.py" --out "$S/identity-lookup-nfkc.json"` -> exit 1, 1/3.
Actual lookup-mutant output for two `ReportKey` checks, first missing `file`: check statuses `[error/check_invalid, clean/null]`, exit 2; expected `[error/check_invalid,error/check_invalid]`. `Straße` repeated exactly fails identically.
Why it escapes: `.ufo/waves/round-40/c1_count.py:50,126-139` generates lowercase ASCII positive repeat ids; R8 only tests an uppercase-first/lowercase-second distinct pair, which the asymmetric lookup also accepts.
Attacked statement: rejection of symmetric case-insensitive R proxies — holds (R8 kills all three).
Attacked statement: frozen predicate establishes the full declared earlier-invalid exact-string repeat behavior — overstated (three omissions meet).
Attacked statement: every R-skipping control fails the predicate — wrong for the three lookup-only controls. No contract change is proposed.
Expected detector: frozen R witnesses should expose missing invalid-earlier repeats; actual verdict: survived, not inconclusive. Added exact-uppercase/unicode diagnostic kills them with pristine/restored passing.
Restoration: `probe.py` before/after sha256 `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b`; mutated `02fc6b602f7155bb9bf21f88e3e2405206f22fe2980a6272ed40f688294096e2`; exact byte equality with read-only reference true. Mutant bytes retained as `control_lookup_casefold.py` for rescoring.
Original/shared/lane source bytes were never written; requested standalone controls intentionally retained. All started detector processes exited; no tool installs/updates; no network.
Detector sha256 `0d328298d6fc172ae4c1ba4dbbe66a88e682708561bdedde4895992348ed922f`; frozen counter sha256 `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8`.
