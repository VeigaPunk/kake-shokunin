## Verdict

**Counterexample found.** D5 rejects inconsistent totals, duplicate populations, forged status, and forged matrix exit codes. However, it accepts rows marked PASS with oracle-matching values even when the matrix reports `executed: 0` and never invokes the validator. A fully self-consistent fake with `executed: 32` is likewise accepted; the frozen replay digest check rejects the changed matrix.

D6 behaves as intended in the tested paths.

## Findings

### P2 — `executed: 0` is accepted alongside 32 PASS rows

The hostile matrix only reads `cases.json`; it does not invoke `scripts/canonical_audit.py`. Its rows copy `expectedExit` and `expectedFindings` into the actual fields.

**Command:**
```text
R22_PROBE_MODE=executed-zero python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/measure.py --root /tmp/kake-r22a2-ResRevCounter-Pnjk/clone --revision 3ee9dcc65e1bcf724fb2e0f891ab78799c3540b
```

**Observed:** exit `0`; top-level `accepted=32`, `total=32`, `available=true`, `acceptedDerivedFromRows=true`, `error=null`. Embedded `matrixStdout` reports `accepted=32`, `total=32`, `executed=0`, `discrepancies=0`. The first row is `PASS`, `actualExit=0`, `actualFindings=["clean"]`.

**Impact:** C1 operability/verifiability; `reconcile_rows` accepts `executed=0` because it checks only that it is within `0..len(results)`.

**Smallest fix:** reject `executed < derived` (or at least fewer executed cases than PASS rows). Do not require `executed == len(results)`: the real matrix can emit failure rows for errors before a subprocess is run.

### P2 — A fully self-consistent fake matrix is indistinguishable to `measure.py` alone

With the same stub but `executed=32`, the validator is still never run, yet the command exits `0` with `accepted=32`, `available=true`, `matrixExitCode=0`, and no error. Its `actualFindings` are copied from the oracle’s `expectedFindings`.

This is inherent to trusting matrix-produced rows: the count runner cannot prove execution from self-reported fields. The existing replay digest gate bounds this reliance: replay on the hostile clone exited `2` with `{"verdict":"could-not-evaluate","id":"snapshot_tampered","error":"snapshot member digest mismatch"}`. Treat measure output as authoritative only alongside the frozen-input digest check; otherwise the runner would need to execute the validator itself.

## Checked and held

- **Pre/post counter probe:** `counter-probe.py` against the pre-fix runner (SHA-256 `329f45b67b3610c5ac132ef53f3428ad8dc9c2dd065ec0a96834a08b71ab9c49`) reported `passed=false`: the FAIL-row stub was accepted (`exit=0`, `accepted=32`) and the unvalidated baseline also exited `0`. Against the post-fix runner it reported `passed=true`: the stub was rejected (`exit=1`, `accepted=0`; error says declared accepted `32` differs from derived `0`) and the unvalidated baseline exited `2` with `instrumentValidated=false`.
- **Duplicate rows:** `R22_PROBE_MODE=duplicate` — exit `1`, `accepted=0`; error: `matrix results case population mismatch: duplicates=absolute_match; missing=symlink_html`. Rejected.
- **Extra keys:** `R22_PROBE_MODE=extra-keys` — exit `0`, `accepted=32`. An extra row key is preserved in `results`; unknown keys do not affect the derived count. Accepted, but no acceptance forgery demonstrated.
- **Discrepancy-consistent forged status:** `R22_PROBE_MODE=status-forged` — exit `1`, reported/derived accepted `31`; error: `absolute_match: status 'PASS' disagrees with oracle comparison`. Rejected.
- **Forged matrix exit:** `R22_PROBE_MODE=exit-forged` — exit `1`, reported/derived accepted `32`, `matrixExitCode=1`; error: `matrix exit 1 != 0 implied by rows`. Rejected.
- **Malformed oracle expectation:** a cases row with string `expectedFindings` was rejected, exit `1`, with `.ufo/waves/round-22/cases.json row 'absolute_match' lacks expectedExit/expectedFindings`.
- **Baseline:** the legitimate baseline command (`--revision 7c61c8cc791bde36dd5e3688bdfea2678d90146c --cases-root /home/vgpnk/Projects/shokunin/kake-shokunin`) exited `0` with `accepted=0`, `total=32`, `available=false`, `instrumentValidated=true`. An incomplete cases root exited `2`.
- **Runner digest:** the post-fix result reports `runnerSha256=a08ac6a38b6b213485f79c6caf1deb633a530b477c92c02b01df6d498924a1eb`, matching the post-fix file’s SHA-256. The frozen input list does not pin `measure.py`; this field records runner identity but does not authenticate it.
- All hostile commits and probe files were confined to `/tmp/kake-r22a2-ResRevCounter-Pnjk`; the lane was not modified.

## Limits

No LSP device was mounted (`xd://lsp` returned “No such tool”), so I could not run references, definition, or diagnostics. No builds, linters, formatters, or installs were run.