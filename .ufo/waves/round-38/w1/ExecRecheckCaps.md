# ExecRecheckCaps — round 38 wave 1 (operability, freshness)

Scope: the two carried round-37 read-cap defects in `scripts/source_recheck.py` at base
`2dab7f3114f3e9dcf072b524c88816ab05fdfcf1`. Sandbox only; the lane was read, never written except
this report. No round-38 sealed tree was listed, read, stat'ed or searched for; no round-38 counter ran.

## Built (smallest fix inside the round-36 contract, bullet (g))
- `MAX_BODY_BYTES = 16 * 1024 * 1024`, stated in the module docstring and at the constant
  (`scripts/source_recheck.py:10-13,52`). `evaluate_check` reads `MAX_BODY_BYTES + 1` (`:604-607`);
  an `OSError`/`MemoryError`/`ValueError` or a length over the cap is one `check_invalid` for that
  check and nothing else (`:608-613`). Over-cap is an input fault, never a crash, never a truncated
  quote test.
- Manifest reads stay capped at the existing 64 MiB; `raw.decode` and `json.loads` now catch
  `MemoryError` (`:670,679`), and `raw` is dropped before the parse (`:676`) to lower the peak. A
  ~60 MiB manifest that cannot be parsed in the address space is one `input_invalid` with a report.

Deliverables (L1 copies after review; all in `/fast/scratch/hyaku/kake-r38w1/ExecRecheckCaps/`):
- `clone3/scripts/source_recheck.py` sha256 `6629d8000ac661ef7340137dc026cbdcc79ab0c81d845ed499376b4c1b0f9c6b`
- `clone3/scripts/source_recheck_hardening_selftest.py` sha256 `2358206b5226648ffd8cfa2af1eb8dafbb49d7ebf2d99b4dba919664b9ac2a81`
- patch `source_recheck-caps.patch` sha256 `041b14d3a6643463c1d331ceb197b86a9dc20eedd002fa8089526f130a1e331d`
  (2 files, +76/−4; `git apply` onto a fresh base clone exit 0, applied hashes equal the above)
- base copy used for red: `base-source_recheck.py` sha256 `4f8adbc23d314bbae9280190a83a2f985bfddb22d94b6135b133222818d47179`

## Fixtures (existing hardening selftest, three added after g32)
`g33-body-over-cap` 16 MiB+8 body; `g34-body-1g` 1 GiB sparse body under 512 MiB address space;
`g35-near-cap-manifest` ~60 MiB manifest (inside the 64 MiB cap, ~7.9M small objects) under 512 MiB
(`scripts/source_recheck_hardening_selftest.py:64-69,88-95,223-238`). `checksEvaluated` is left
unpinned for g33/g34 (see risk 3); exit, verdict and findings are pinned.

| Command (in `clone3`, TMPDIR in sandbox) | exit | observed |
|---|---:|---|
| `python3 -B scripts/source_recheck_hardening_selftest.py --tool base-source_recheck.py` | 1 | 6/9, failures exactly `g33-body-over-cap`, `g34-body-1g`, `g35-near-cap-manifest` |
| `python3 -B scripts/source_recheck_hardening_selftest.py` | 0 | 9/9, verdict clean |
| `python3 -B scripts/source_recheck_selftest.py` | 0 | 106/106, verdict clean |
| `python3 -B .ufo/waves/round-36/sealed_count.py --root . --tool-file clone3/scripts/source_recheck.py --key-revision fd1fb723` | 0 | cases 28, passed 28, met true, toolSha256 `6629d800…9c6b` |
| base at same counter, `--tool-file base-source_recheck.py` | 0 | cases 28, passed 28, met true, toolSha256 `4f8adbc2…4179` |

Red failure reasons (stderr, `final-hardening-red.err`): g33 `exit mismatch: expected [2], observed 1`;
g34 and g35 `exit mismatch: expected [2]/[0,2], observed 1` with an uncaught `MemoryError` traceback.

## Blow-up receipts (`timeout 60 prlimit --as=… -- python3 -B <tool> --manifest manifest.json`)
Probes (`probe/`): `over` 16 MiB+1 text body; `body1g` 1 GiB sparse body; `near` 60 MiB manifest.

| probe / limit | base exit, stdout | fix exit, stdout |
|---|---:|---|
| over / 2 GiB | 1, `failed-policy` `quote_missing` (whole body read) | 2, `could-not-evaluate` `check_invalid` |
| body1g / 2 GiB | 1, **empty stdout**, `MemoryError` at `source_recheck.py:600` (`payload.decode`) | 2, `could-not-evaluate` `check_invalid` |
| near / 512 MiB | 1, **empty stdout**, `MemoryError` in `json/decoder.py:361 raw_decode` | 2, `could-not-evaluate` `input_invalid` (check null) |
| near / 2 GiB | 0, `clean` (parse fits) | 0, `clean` (parse fits) |

Boundary (`probe/exact`): body of exactly 16,777,216 bytes → fix exit 0 `clean`; 16,777,217 bytes →
fix exit 2 one `check_invalid`. No off-by-one.

## Observations / not verified
- The ~60 MiB `MemoryError` is address-space dependent: it reproduces under 512 MiB (fixture and
  probe) and not under the 2 GiB blow-up limit, where both tools parse and answer `clean`. g35 pins
  the 512 MiB condition deliberately.
- `.ufo/waves/round-37/sealed_count.py:47` sets `TOOL = "scripts/robots_audit.py"`; it is not an
  instrument for this tool. Scoring `source_recheck.py` with it gives 0/28 on base and fix alike
  (`base-r37-counter.json`, `green-r37-counter.json`) — instrument mismatch, not a regression.
- Did not verify: round-38 counters (no key), peak RSS, frames larger than 16 MiB against a real
  page (only synthetic probes), and a manifest whose `MemoryError` lands in `raw.decode`.
- No tools installed or updated. Every child process exited; no background jobs; no network.

## Risks
1. 16 MiB is a chosen cap, not a repository constant (largest committed body: 44 B in fixtures,
   1.7 KB tarball for the round-36 real run; largest sealed case 3,669 B). Changing it means the
   tool constant, the docstring and the fixture `BODY_CAP` move together; the 28/28 counter shows no
   sealed case is over it.
2. Catching `MemoryError` turns a manifest that might parse with more memory into `input_invalid`.
   That is contract (g) "unreadable" and the verdict is `could-not-evaluate` either way, but it is a
   judgment call for manifests just under the 64 MiB cap under address pressure.
3. Pre-existing, not changed and not pinned: contract (g) says `checksEvaluated` "counts the checks
   that are not check_invalid", yet `main` increments before `evaluate_check`, so an evaluate-time
   `check_invalid` (unreadable body, now also over-cap body) reports `checksEvaluated: 1`. The
   round-36 counter does not compare the field; the L1 may want to route this.
4. Bodies are still read whole up to 16 MiB and decoded/parsed in memory: bounded, not free.
