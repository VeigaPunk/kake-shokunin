# MutationC2HeaderNames

- Scope: scratch clone `/fast/scratch/hyaku/kake-r61/MutationC2HeaderNames/lane`; no lane source files changed. No tools installed.
- Pristine `scripts/header_audit.py` SHA-256: `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`.
- Detector: `python3 -B .ufo/waves/round-61/c61_header_cases.py --root <scratch-clone> --revision <commit> --work <scratch-work> --seed 61 --json`.
- Pristine output: H1–H18 `cases_passed=18`, `ncases=18`; counter `met=False`, exit 1 because R3 fails with `ambiguous manifests` (committed round-61 tree contains additional version-1 manifests under w1 seat `.files` directories). Thus the full predicate baseline fails and is **inconclusive**; H1–H18 case deltas are the bounded detector. This R3 issue is observed, not attributed to header_audit.
- Malformed-name probe against pristine tool: exit 1, `checks=1 findings=10`; `field_name_syntax` emitted for `X Bad Name`, leading-space ` X`, tab `X\tY`, `X:Bad`, `Bad:Name`, raw obs-text `X\x80Name`, UTF-8 non-ASCII `naïve`, empty name, and `Content Type`. Valid control `ok-name` was accepted. It also reported the intentionally absent Content-Type expectation. Finding details are sanitized by `token()`.

## Mutants and results

- **M1 — remove header-name case folding:** changed `lowered = [name.lower() for name, _ in headers]` to preserve original case. Scratch commit `578eca71c02aee78dc45ed944c28707661762063`. Detector: `cases_passed=6/18`; H1 and H3 among failures (capitalized names treated absent). **Killed** by H1/H3 presence expectations.
- **M2 — allow whitespace in field-name token grammar:** added a space to `FIELD_NAME` character class. Detector: `cases_passed=17/18`; H12 fails because `X Bad Name` is accepted (no `field_name_syntax`). Malformed-name probe with mutant flags only the remaining malformed forms; whitespace cases are accepted. **Killed** by H12.

The frozen H fixtures exercise whitespace via H12, but do not exercise colon, obs-text, or empty field names. Therefore corresponding grammar-weakening mutants (allow colon, allow `\x80-\xff`, or change `+` to `*`) are **not tested by a frozen case** and are expected survivors/coverage gaps; the pristine malformed-name probe establishes those forms are currently rejected. No such additional mutants were committed/run.

## Restoration

Reset the scratch clone to pristine base `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`. Post-reset tool SHA-256 is again `01abd8d4ff628907713b4300adf26b5962924d85132d1f330a33b70110c1d1d4`, matching pristine exactly; scratch HEAD is the base revision. No mutation remains.

VERDICT: KILLED — case-folding and whitespace-token mutants. Colon, obs-text, and empty-name mutant coverage gaps remain unprobed by H1–H18; full counter baseline is inconclusive because of independent R3 ambiguity.
