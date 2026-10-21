# Round 23 — FixProbeWitnesses

## Verdict

**No actionable finding in the assigned fixes.** The added `foreign_stray_end` selftest now detects removal of the foreign end-tag mismatch rejection, and both new relaxation attacks independently make the probe fail when their corresponding guard is removed.

## Findings by severity

None.

## Review and mutation evidence

Compared the working-tree changes against frozen `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` (working-tree `HEAD` `1b309c93fb0b2007ef15587100e7a1cdb9ef5573`). The diff adds `foreign_stray_end` to `scripts/canonical_audit.py`'s selftest and adds `foreign_canonical` plus `foreign_stray_end` to `.ufo/waves/round-23/relaxation_probe.py`. The former has a valid head canonical and a mismatched `</bad>` followed by matching `</g></svg>`, so the mismatch is not masked by an unclosed foreign stack or an unrelated forbidden token. The probe's foreign canonical attack uses a self-closing canonical-looking link in SVG; its stray-end attack uses the same balanced-after-mismatch shape.

Created a private clone at `/tmp/kake-r23res-witnesses-jT7W/clone` from the current checkout with `git clone --no-hardlinks --no-checkout`, then detached at `1b309c93fb0b2007ef15587100e7a1cdb9ef5573`. Copied the working-tree validator and relaxation probe into it. Their SHA-256 values matched the checkout: validator `23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4`; probe `a0ef673effec1cdeadd7909fbd92a43edc576c6625b90d79d9683e8a513dda60`.

Exact detector commands, run at pristine state and after each restoration:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kake-r23res-witnesses-jT7W python3 /tmp/kake-r23res-witnesses-jT7W/clone/scripts/canonical_audit.py --selftest
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/kake-r23res-witnesses-jT7W python3 /tmp/kake-r23res-witnesses-jT7W/clone/.ufo/waves/round-23/relaxation_probe.py --validator /tmp/kake-r23res-witnesses-jT7W/clone/scripts/canonical_audit.py
```

Pristine and restored runs: selftest exit 0 with `passed: true`; relaxation probe `passed: true`, `met: 13`, `total: 13`. The selftest's `foreign_stray_end` row expected and observed exit 2 / `html_unsupported`. The probe's two controls remained `clean` in every phase.

1. **Mismatch rejection mutant:** in the clone only, replaced `self.unsupported = True` with `pass` in the foreign-stack mismatch `else` branch (`scripts/canonical_audit.py:318`; guard at `310-319`). The relaxation probe exited 1, `passed: false`, `met: 12/13`; `foreign_stray_end` was exit 0 / `clean` / `ok: false`. The built-in selftest exited 1 / `passed: false`; `foreign_stray_end` observed exit 0 / null ID versus expected exit 2 / `html_unsupported`. Restored the original line and reran both detectors successfully before the next mutation.
2. **Foreign canonical-link guard mutant:** in the clone only, changed `_foreign_token`'s condition to `if tag in {"base", "head"}:`, disabling just the canonical-link term while preserving base/head checks (`scripts/canonical_audit.py:206-210`). This is the isolated guard mutation identified in `ReviewQualityCriteria.md:27-49`. The relaxation probe exited 1, `passed: false`, `met: 12/13`; `foreign_canonical` was exit 0 / `clean` / `ok: false`, while `foreign_stray_end` remained non-clean. The built-in selftest also exited 1: `body_svg_selfclose_link` observed exit 1 / `canonical_missing` instead of expected exit 2 / `html_unsupported`. Restored the original condition and reran both detectors successfully.

After restoration, the clone validator hash again matched the checkout hash; the relaxation probe hash remained unchanged. No live source or probe files were edited. Mutations were confined to the private clone.

## Comparison to prior reports

- `w2/MutateGuards.md:21-28` documented M3 (mismatch rejection removed) surviving the old 81-case selftest and 11-case probe, and recommended a uniquely mismatched-but-balanced selftest plus an equivalent relaxation attack. The added selftest/probe case has that shape; the one-line M3 mutant now fails both.
- `w2/ReviewQualityCriteria.md:27-49` found that removing the foreign canonical-link guard left the old probe green. The new self-closing foreign canonical attack makes the same isolated guard removal produce a clean verdict and therefore a failing probe. It exercises the same `_foreign_token` guard; the test uses a direct SVG link rather than the earlier report's `foreignObject` example.

## Residual risk and verification gaps

This was a targeted parser/selftest mutation review, not a browser-runtime or public-page test; it establishes detector sensitivity to these two source-guard regressions, not search-engine behavior. `ReviewQualityCriteria.md` also contains a separate C1 gone-surface/HOLD finding, outside this assignment. No build, lint, or formatter was run. LSP was unavailable: the initial `read xd://lsp` returned `No such tool`, so LSP status/references/definition/diagnostics could not be queried. Literal grep was used only to locate targets; conclusions above come from source reads and the isolated CLI mutations. No tools were installed or updated.