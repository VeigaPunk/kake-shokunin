# R41 w2 — ReviewCounterV2Code (falsify, leaf seat). Axes: operability, freshness.

Reviewed the diff `c1_count.py` → `c1_count_v2.py` (60+/29−; every hunk) and the full 400-line v2,
against contract `.ufo/waves/round-39/c1-contract.md` sentences 4, 21, 22. Sandbox:
`/fast/scratch/hyaku/kake-r41w2/ReviewCounterV2Code/`. No tools installed (none needed).

## Checks (exact commands, exit codes)
- `diff -u .ufo/waves/round-41/c1_count.py .ufo/waves/round-41/c1_count_v2.py` → exit 1 (as expected).
- `python3 -B .ufo/waves/round-41/c1_count_v2.py --root . --revision eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 --seed 412776 --out <sb>/receipt_s412776.json` → exit 0; **met 1434/1434**, oracleInvalid 619, toolSha256 `0b485431…13edbf` == SCORECARD build sha.
- Same seed vs round-40 base (`git show 8eb121c8:scripts/sitemap_audit.py`, sha `4de35f8c…1460e` == SCORECARD base) → exit 1, passed **1068/1434**, 200 misses (userinfo `\x0b`, fragment `%2`, host `` ` ``…). v2 discriminates: it can fail, and fails on exactly the boundary units v1 missed.
- Independent RFC 3986 validator (written fresh from Appendix A; separate from abnf): 50-value adversarial truth table (all 5 ip_literal kinds incl. IPvFuture and case-insensitive `V1.a` per RFC 5234 §2.3; `a@@host`, empty userinfo/port/query/fragment/path-segment; `:80`; `%`,`%2`,`%4G`; scheme case) → **0 disagreements** with the oracle; 8604 generated cases over 6 seeds → **0 disagreements**.
- Leak scan of `layout()` output (seed 412776): manifest keys exactly `{file,id,sitemapUrl}`, 17 hex-named case files, **0 label tokens** (`"valid"`, `oracleValid`, `:true/:false`, …) in anything the tool sees.
- bwrap probes: v1-style (inherited env) → `/proc/1/environ` inside the sandbox contains the FULL operator env (marker `SECRET_LEAK_MARKER_ZZ=xyzzy` returned, plus OAuth tokens); v2-style (`env={"PATH": "/usr/bin"}`) → pid1 env reduced to `{PATH, _}`, child env `{LANG, PATH, PWD}`.
- Strip coverage, seeds 1–20: loc cases whose value changes under the sentence-21 strip: mean 2.1/630, one seed with **0** (seed 9).

## Findings
1. **Low — receipt can be silently skipped.** `c1_count_v2.py:378` `env={"PATH": "/usr/bin"}` narrows exec lookup (verified: `subprocess.run([...], env={"PATH":"/usr/bin"})` raises FileNotFoundError for a non-`/usr/bin` binary); the handler at `:381` catches only `TimeoutExpired`, so a host with bwrap outside `/usr/bin` crashes with a traceback, no exit in {0,1,2}, and **no receipt** — contradicting docstring `:7` ("a receipt is written in every case"). Latent here (`/usr/bin/bwrap` verified present). Catch `OSError` or invoke bwrap absolutely.
2. **Low (information for next round) — thin sentence-21 coverage.** `:211` strip is exercised by ~2 of 630 loc cases per run and can be 0 (seed 9/20): TAB/LF/CR/space must land at the value's very end. A run can meet 1434/1434 without ever testing the loc whitespace strip. Bias ws units toward value ends for `loc`.
3. **Info — dead parameter.** `maybe_empty` `:143` takes `target`, never uses it (AST-verified). Harmless (`insert("") == unit` is a legitimate case the oracle labels), but suggests an unimplemented exclusion.
4. **Info — docstring overstated.** `:26` "empty environment": child actually gets `{PATH, LANG, PWD}`, pid1 `{PATH, _}`. Wording only; no case data or operator env reaches the sandbox.

## Verified positives
- `:378` is a **genuine fix**: v1 runs (all 141 wave-1 receipts) exposed the operator's full env incl. secrets to the sandboxed tool via `/proc/1/environ`. Labels never travel through env, so past receipt integrity is unaffected — secret exposure only.
- Oracle = sentence 22 exactly (grammar + http/https ci + non-empty host), loc-only strip = sentence 21 exactly (`" \t\r\n"`, `:211`; sitemapUrl as written per sentence 4 being outside rules (g)–(k)). CR→LF XML normalization can't flip labels (both chars illegal/stripped alike).
- Boundary insertion (ends included), empty components, IP literals all live code: shape counts at seed 412776 — empty port 29, empty query 48, no-path 84, empty segment 122, empty fragment 27, empty userinfo 13, empty password 31, `?#` 29; ip-literal hosts 76; insertion is reg-name-only (`:152-156`), literals never targeted as documented.
- No new label leak: labels confined to the counter process; receipt written after tool exit; layout/judge unchanged from v1 apart from the diff hunks shown.

## Statement scorecard
- "judges loc (post-strip) / sitemapUrl as written against RFC 3986 URI + authority + non-empty host" — **holds**.
- "boundary insertion both ends; empty components; IP literals valid, never a target" — **holds**.
- "environment: bwrap's own /proc/1/environ" — **holds** (real fix, verified); "empty environment" — **overstated** (3 vars).
- "1434 cases; met at build; r40 base fails" — **holds** (630+804; exits 0 / 1 above).
- "no new label leak" — **holds**.

## Residual risk / gaps
- Oracle cross-checked against one independent implementation plus hand rules; a shared misreading (e.g. IPvFuture edge syntax) can't be fully excluded with two implementations.
- Out of generator scope (acknowledged): units inside IP-literal hosts, zone-ids, non-ASCII; tools mis-handling those pass v2.
- v1-inherited sandbox plumbing (bind-point parent dirs, bwrap argv) not re-verified; unchanged and proven by 141 receipts.
- Did not rerun the wave-1 tally or harm checks (other seats' scope).
