# ReviewSelftest — `scripts/source_recheck_selftest.py` vs the C1 contract

Seat: KakeR36.ReviewSelftest (wave-2 falsify). Target: `scripts/source_recheck_selftest.py`
(917 lines, sha256 `0ad5623b…5e419`) at lane `f3a38bf`, incl. the L1's f08 change; contract =
SCORECARD.md:1598-1657 "C1 contract". Sandbox `/fast/scratch/hyaku/kake-r36w2/ReviewSelftest/`
(clone at f3a38bf, TMPDIR=`.../tmp`). No lane file touched except this report.

## Verdict

No contract-breaking fixture found. 90 of 101 fixtures audited line-by-line (all of a, b, c, d,
e, f, verdict, usage, output-shape; 10 of 28 g); every expectation follows from the contract
sentence it quotes. The f08 change is **correct and necessary** (details below). Selftest runs
clean on the landed tool and discriminates wrong tools. Findings are all low-severity
tolerance/coverage issues, none changing the landed tool's result.

## Runs (exit codes observed)

| command (cwd=clone, TMPDIR set, `timeout 300 python3 -B`) | output | exit |
|---|---|---|
| `scripts/source_recheck_selftest.py --tool scripts/source_recheck.py` | `passedOverTotal 101/101, verdict clean` | 0 |
| `scripts/source_recheck_selftest.py` (default tool resolution) | `101/101 clean`, resolved to `scripts/source_recheck.py` | 0 |
| `… --tool /fast/…/kake-r36w1/ExecSelftest/reference.py` | `101/101 clean` | 0 |
| `… --tool /fast/…/kake-r36w1/ExecSelftest/toy_wrong.py` | `verdict failed, 42/101, 59 failures` (matches w1/ExecSelftest.md §B verbatim) | 1 |
| `… --tool toys/const_clean.py` (recreated; /tmp copy gone) | `failed 0/101` | 1 |
| `… --tool toys/junk.py` (non-JSON stdout) | `failed 0/101` | 1 |
| `… --tool toys/noreader.py` (status rules only) | `failed 44/101` | 1 |

Seat sha `9db94fec…` for its original file confirmed against w1 sandbox copy.

## f08 change (SCORECARD f, S090) — verified correct

- Original fixture (`/fast/…/ExecSelftest/source_recheck_selftest.py:487`) used
  `charset=utf-16` and demanded `charset_unsupported`/exit 2. Wrong: the WHATWG label table
  maps `utf-16` → UTF-16LE — sealed `ref.py:17` lists `"utf-16"` under `"utf-16le"` labels, and
  the contract says the tool "supports the labels of UTF-8, UTF-16BE, UTF-16LE and
  windows-1252". A conforming tool would have failed the old fixture.
- Landed fixture (selftest:486-492) uses `charset=shift_jis`, a label valid in the WHATWG
  table whose encoding is outside the supported set → `charset_unsupported` is the only
  contract outcome. Sealed `cases.json` itself carries a `charset=shift_jis` case, so the fix
  aligns the selftest with the sealed key, not away from it.

## Findings (all low)

1. **a08 under-tolerates** (selftest:283-286). Docstring says a check with a redirect last hop
   "may be reported as check_invalid … or evaluated on its last hop", but the only accepted
   alternative is `http_error` alone. A lenient tool that also honours (b)'s leading-permanent
   rule would emit `moved` (target `https://example.com/x`) plus `http_error` and be rejected.
   The L1 reference resolves it as `check_invalid` (ref.py:102), so the sealed key is safe;
   only the documented tolerance is narrower than advertised.
2. **g22 over-tolerates** (selftest:598-601). Alternative `alt(0,"clean",[])` accepts an
   outcome no contract reading produces: hops=[200,200] with no `contentType`/`body` leniently
   "evaluated on last hop" still requires `contentType`/`body` for a 200 → `check_invalid`
   (cf. g23). Masked in practice because g23 forces that rule anyway.
3. **Docstring overclaim** (selftest:63-66): "Every fixture therefore carries a location on
   every hop" — `chk()`'s default `[{"status":200}]` (line 236) has no location; used by
   g06,g13-g15,g23,g24,v03 and the bad check of g25/g26. All still expect `check_invalid`, so
   no wrong verdict; the claim is false and those hops violate the manifest's hop shape.
4. **f07/f08 duplicated** (selftest:481-492): after the fix both probe `charset=shift_jis`
   with identical bodies and expectations. f08 could use another valid-table unsupported label
   (`gbk`, `euc-kr`, `koi8-r` — all present in sealed cases.json) to widen discrimination.
5. **`checksEvaluated` unjudged on 6 fixtures** (e04:438, e08:454, f07:485, f08:492, v02:640,
   v04:648 all `evaluated=None`): contract implies 1 (findings are not `check_invalid`).
   Matches the sealed counter, which never compares `checksEvaluated`, but the selftest is
   stricter elsewhere — an inconsistency, not a defect.

## Ambiguity audit vs sealed reference (ref.py)

All three documented ambiguities: ref.py picks the selftest's **primary** expectation each
time — redirect-hop `location` required (ref.py:102 → g19/g28), malformed chain →
`check_invalid` (ref.py:104-105 → a08/g22), missing manifest → `input_invalid` exit 2
(ref.py:123-128 → g05 primary, 64 tolerated). Tolerances only widen where the sealed key is
strict, so no conforming-to-ref tool can fail these fixtures. Note the sealed counter judges
only exit/verdict/findings; these tolerances sit on selftest-only surfaces anyway.

## Residual risk / not verified

- Write-detection snapshots only the selftest's temp tree (selftest:731-732,759-774); a tool
  writing to $HOME or global /tmp escapes it.
- No-write/network prohibitions are enforced only by the file snapshot — no syscall or network
  monitoring (same as the sealed counter).
- g-fixtures audited: g01-g09,g13,g18-g23,g25,g27,g28 (the rest by report map only).
- The c09 case-insensitive-start-tag reading and NBSP/NFKC equivalence (d07) rely on standard
  HTML/Unicode semantics, not literal contract text; both readings are the reasonable ones.
- Did not re-run the sealed counter or touch `/fast/scratch/hyaku/kake-r36/`; no installs
  needed (no tool installed or updated).
