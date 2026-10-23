ReviewBuildDiffFresh — round 41 wave 2, axis: operability. Fresh non-author review.

# Reviewed bytes
- Build: `scripts/sitemap_audit.py` @ eae5ae2c, sha256 `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf` — matches claim.
- Base: same file @ 8eb121c8, sha256 `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` — matches claim.
- Diff: single hunk. Adds `_UNRESERVED/_SUB_DELIMS/_PCT/_PCHAR/_URI_RE` (lines 68–86) and replaces the old whitespace guard with `if _URI_RE.match(value) is None: return None` (line 92). Callers: `_audit_loc` line 308 (→ `loc_not_absolute`), `_evaluate_check` line 382 (→ `check_invalid`).

# Method (commands, all exit 0)
- `git diff 8eb121c8 eae5ae2c -- scripts/sitemap_audit.py`; both blobs extracted to my sandbox and hashed.
- Differential harness (`/fast/scratch/hyaku/kake-r41w2/ReviewBuildDiffFresh/difftest.py`): 39,904 composed `scheme://[userinfo@]host[:port][path][?query][#frag]` values + directed edge cases; compared `base_tool._parse_url` vs `build_tool._parse_url`. Independent RFC oracle: `abnf.grammars.rfc3986.Rule("URI").parse_all` from the shipped wheel `.ufo/waves/round-41/oracle/abnf-2.9.1-py3-none-any.whl` (sha256 `cdcac127…0917` verified, matches c1_count.py's pin), labelled "URI with authority + non-empty host" (7,277 oracle calls). Python 3.14.8.

# Results
- Divergences base≠build: 3,253 + 4. Every one oracle-checked.
- RFC-valid & base-accepted but build-rejected: **0**. RFC-valid but `_URI_RE`-rejected (3,000-sample + all composed): **0**. Differing non-None tuples: **0** (same post-guard code).
- Base-rejected but build-accepted: 4 (bounded exhaustively to 12 slot×char combos — see F1).

# `_URI_RE` vs RFC 3986 Appendix A, class by class
scheme `ALPHA *(ALPHA/DIGIT/"+"/"-"/".")`, userinfo `*(unreserved/pct/sub-delims/":")`, reg-name `1*(unreserved/pct/sub-delims)` (non-empty ✓), port `*DIGIT`, path-abempty `*("/" segment)`, query/fragment `*(pchar/"/"/"?")`, pchar incl. pct-encoded `% HEXDIG HEXDIG`, single `@` after userinfo, `//` mandatory — all faithful. Two supersets, both documented in the comment (lines 68–71): `\u0080–\U0010ffff` admitted wherever `unreserved` is (not RFC 3987 conformance, verbatim-comment behaviour, kept); IP-literal contents `[^\]]*` deferred to urlsplit — verified urlsplit rejects invalid literals (`'a b'`, `''`, `[::1\x0b]`, `[ ]` all → ValueError → None). `\A…\Z` anchors confirmed (`'http://h/\n'` → None).

# Findings
- **F1, low** — `scripts/sitemap_audit.py:81`: the `\[[^\]]*\]` host alternative admits tab/LF/CR inside an IP literal; urlsplit strips those three characters before validating, so RFC-invalid input normalizes to a valid literal and is accepted: `'http://[2001\tt:db8::1]/'` → `('http','2001:db8::1',80,'/')`, `'http://[v1.f\te80]/'` → host `v1.fe80`. Base rejected these (old guard caught `\t\r\n` anywhere). This is the only class where the build accepts values the base rejected — the "judged as written" claim is defeated exactly for urlsplit's strip-set inside brackets. Reachable via a literal TAB inside `loc` brackets (sentence-21 strip is leading/trailing only) or JSON `\t` in `sitemapUrl`. Wrong-direction acceptance (a missed `loc_not_absolute`/`check_invalid`), narrow exotic class. All other bytes inside `[...]` are consistent-reject: they either fail the regex or trip urlsplit's IP-literal validation.

# Per checked statement
- "Judges `loc`/`sitemapUrl` as written against RFC 3986 `URI` with authority + non-empty host, before urlsplit": **holds** for every RFC-valid value tested (superset judge, zero false rejections); **overstated** for the F1 bracket-whitespace class, which is judged by urlsplit's normalized form, not as written.
- "Every caller keeps behaviour for values the base accepted and RFC 3986 accepts": **holds** — 0 regressions in ~47k differential cases; all 3,253 tightenings are RFC-invalid values (spaces, `{}`, `|` `^` `` ` `` `\` `"` `<>` in path/query/fragment, `%`-misencodings, stray `@`, `#` inside fragment) that urlsplit had silently tolerated.
- Build sha256 `0b485431…13edbf`: **holds** (recomputed).

No installs needed (reused the shipped abnf wheel). Sandbox: `/fast/scratch/hyaku/kake-r41w2/ReviewBuildDiffFresh/`.
