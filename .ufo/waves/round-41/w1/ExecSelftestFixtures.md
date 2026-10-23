# R41 W1 — selftest fixtures for the RFC 3986 URL rule

Seat `KakeR41.ExecSelftestFixtures`. Lane `kake-shokunin` at tip abf457d0. Python 3.14.8.
Scope only: fixtures in a copy of the lane selftest; no lane file mutated, no counter scored.

## Artifacts
- Selftest copy: `/fast/scratch/hyaku/kake-r41w1/ExecSelftestFixtures/selftest.py`
  (1237 lines) sha256 `d8d2ba6cf3d8721e558cac42f44784101aaaddab8571a5364b8808cd4977c16d`.
- Lane selftest sha256 `d80302cbd5ef68715f83086e21c13af10815d79aed48652fe0cf3b1459aec319`.
- Unified diff (lane -> copy): `/fast/scratch/hyaku/kake-r41w1/ExecSelftestFixtures/selftest.diff`
  sha256 `00c20e4c00275085d5ed61874857c32662e2041f2dddb3f4f3c1632f60e67b73`;
  75 added lines, **0 removed** — old fixtures byte-identical.
- Logs in the same directory: `base.log`, `ref.log`, `r41-matrix.txt`, `map-new.txt`.

## Fixtures added (15, ids `r41_*`, one block before `return cases`, existing style)
Invalid, expect exit 1 / `failed-policy` / `(loc_not_absolute, 1)`:
`r41_loc_path_space`, `r41_loc_path_pipe`, `r41_loc_path_caret`,
`r41_loc_path_brace`, `r41_loc_path_del`, `r41_loc_fragment_second_hash`
(`.../a#x#y`), `r41_loc_path_bracket` (`.../a[b`), `r41_loc_bad_percent_triplet`
(`.../a%zz`), `r41_loc_userinfo_second_at` (`http://a@b@example.com/`),
`r41_loc_port_letter` (`http://example.com:80a/a`).
Manifest case, expect exit 2 / `could-not-evaluate` / error `check_invalid`:
`r41_manifest_url_c0_interior` (sitemapUrl `http://exam\x01ple.com/`).
Valid controls, expect exit 0 / `clean`: `r41_loc_path_sub_delims` (XML `&amp;`),
`r41_loc_path_pct_7e`, `r41_loc_ipv6_literal_host` (sitemapUrl is the same
IPv6 literal, so rule (h) holds), `r41_loc_userinfo_with_colon`.

## Commands (each `timeout N prlimit --as=4000000000 python3 -B`)
- `selftest.py --map` -> exit 0; `case count: 198`; `sentence coverage: 34/34`; no rule gap.
- `selftest.py --tool /fast/scratch/hyaku/kake-r41/shared/ref_fix.py` -> exit 0;
  `PASS 198/198`.
- `selftest.py --tool /fast/scratch/hyaku/kake-r41/shared/base.py` -> exit 1;
  `PASS 188/198`; 10 `FAIL` lines, all `r41_*`; `FAIL` lines not `r41_*`: 0.
- Driver over only `r41_*` cases -> exit 0: base 5/15, ref 15/15 (matrix file).
- Tool sha256: base `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`,
  ref `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`.

## Base behaviour behind the red lines
The 10 red invalid fixtures are clean/exit 0 on base except the manifest C0 case
(exit 1, `failed-policy`). Base's only textual guard is leading-char `<= " "` plus
tab/CR/LF (`shared/base.py:70`), then `urlsplit` (`:73`); it accepts interior
`\x01` in the host, space/`|`/`^`/`{`/DEL/`[`, `%zz`, a second `#` and a second `@`.
The ref gates on `_rfc3986_uri` (`shared/ref_fix.py:113-114`, regex `:76`, helper `:89`).

## Statement verdicts
- ">=12 fixtures with ids r41_*": holds (15, all listed categories covered).
- "each new fixture red on base": **overstated** for 1 of 11 invalid fixtures.
  `r41_loc_port_letter` is green on base too: `parts.port` (`shared/base.py:80`)
  raises ValueError for a non-digit port and base returns None, i.e. base already
  rejects it; no letter-in-port form can separate base from ref. Kept as a
  contract-correct regression guard; reported, not hidden.
- "green on ref": holds (198/198, including all 15).
- "183 old fixtures stay green on both": holds (base 188/198 = 183 old + 5 r41;
  ref 198/198; diff removes no old line).

## Risks / limits
- The letter-port fixture does not discriminate; effective new separation is 10/11
  invalid cases across 6 URL components plus 4 valid controls.
- No tool installs; no lane, jj, index or shared-path mutation; no counter run.
