# Round 41 wave 1 — ReviewReferenceDiff (leaf seat)

Scope: L1 reference repair `ref_fix.diff` vs RFC 3986 Appendix A and c1-contract sentences 4/22.
Axes: operability (judged), freshness. No subagents, no lane mutation. Runtime: Python 3.14.8.

## Artifacts (sha256)
- base.py `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`
- ref_fix.py `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`
- ref_fix.diff `b608289c38ab84c1ffef4c79766ee051c8f4f9853c80d96167d87e671309b1b8` (66 lines)
- c1_count.py `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4` (matches SCORECARD)

## Official counter runs (canonical runtime; prlimit 4 GB; bwrap sandbox)
- `prlimit --as=4000000000 timeout 900 python3 -B .ufo/waves/round-41/c1_count.py --root <lane> --tool-file /fast/scratch/hyaku/kake-r41/shared/ref_fix.py --label ReviewReferenceDiff-refcopy-s41001 --seed 41001 --out refcopy-41001.json` → **exit 0, met, passed 1434/1434, loc 630/630, sitemapUrl 804/804**
- same with `--label ReviewReferenceDiff-refcopy-random` (fresh seed) → **exit 0, met, 1434/1434**
Receipts: `/fast/scratch/hyaku/kake-r41w1/ReviewReferenceDiff/refcopy-41001.json`, `refcopy-random.json`.

## Differential probe (ref vs base vs abnf 2.9.1 rfc3986 oracle; 20,441 cases incl. 20k random/mutated ASCII + non-ASCII)
- ASCII disagreements ref-vs-oracle: **2** — both ports > 65535 (`http://host.tld:99999/p`, `:65536/p`): oracle valid, ref invalid. Base also invalid → no regression.
- ASCII cases where base disagrees with oracle: 4,995 (base accepts interior C0/DEL/space/pct/misplaced gen-delims; ref agrees with oracle on all of them).
- Non-ASCII disagreements: 370 (targeted + random), all ref-accepts/oracle-rejects, only in userinfo / reg-name host / path / query / fragment; ref and base both reject non-ASCII in scheme, port, and bracket literals (identical behavior).
- Oracle-valid but ref-rejects among 3,000 random non-ASCII mutations: 0. Adversarial 2000-char near-misses parse in ≤ 0.0002 s (no backtracking blowup).

## Findings
- [Low, documented residual] `ref_fix.py:116-122` — `parts.port` raises ValueError for ports > 65535; caught → `None` → URL rejected, though RFC 3986 App A `port = *DIGIT` accepts any digits. Deviation from the claim sentence ("parses as RFC 3986 URI grammar … non-empty host"), but SCORECARD declares "ports above 65535 … outside the class" and the generator cannot produce one (`make_url`: port = `str(rng.randint(10,99))` + 1 inserted unit ⇒ ≤ 3 digits). Base behaves identically. No predicate impact; candidate for future in-class strengthening.
- [Info] `ref_fix.py:79,86,96-108` — IP-literal handling: `[^\]]*` capture then `ipaddress.IPv6Address` + hand-rolled IPvFuture `[vV][0-9A-Fa-f]+\.[A-Za-z0-9._~\-!$&'()*+,;=:]+`. Probed: `[::1]`, `[2001:db8::1]`, `[::FFFF:192.0.2.1]`, `[vF.x]`, `[v7.ch]`, `[invalid]`, `[::1%25eth0]` (zone id rejected per RFC 3986), internal space/C0, nested `[`, stray `]` — all agree with oracle. Generator never inserts into bracket literals (target==host always mutates a reg-name label), so this branch is unexercised by the counter; matches declared "IP-literal contents … outside the class".
- [Info] `ref_fix.py:76-85` — classes vs Appendix A: scheme `[A-Za-z][A-Za-z0-9+.\-]*` ✓; userinfo/reg-name = unreserved+sub-delims+pct ✓; `port = (?::[0-9]*)?` ✓ (empty port OK, defaults 80/443 downsteam — unchanged); path-abempty/query/fragment pchar sets ✓; `\A…\Z` anchored; `%` +P2 hexdig, case-insensitive ✓. No character class mismatch found in ASCII.

## Out-of-class choices in SCORECARD (round 41 section)
- "Code points U+0080 and above stay accepted where RFC 3986 allows `unreserved` … round-40 behaviour, unchanged" — **holds** (probe: identical accept/reject set to base on all non-ASCII positions; accepts only in unreserved positions).
- "IP-literal contents … outside the class" — **holds** (code reading + probe agreement).
- "ports above 65535 … outside the class" — **holds for the frozen predicate** (un-generatable), but the underlying grammar deviation above exists; not overstated as "grammar-following" in the general case.

## Other contract sentences
Diff touches only `_parse_url`'s guard; sole callers are `_evaluate_check` (sentence 4 → `check_invalid`, ref_fix.py:403) and `_audit_loc` (sentence 22 → `loc_not_absolute`, ref_fix.py:329). Downstream sentences 24-27 see identical tuples for every URL both base and ref accept; `_audit_loc` order (23 before 22) unchanged. No other sentence behaviour changes.

## Verification gaps
- Fresh-seed non-oracle crosscheck not rerun (pre-data crosscheck in SCORECARD; out of leaf scope).
- No LSP server for these loose scripts; review used `read`/`grep` plus direct module import + oracle execution, which is stronger than static analysis.

Conclusion: reference repair matches the frozen predicate on the canonical runtime (1434/1434, two receipts). No blocking finding; two declared out-of-class residuals (ports > 65535, IP-literal contents) and the IRI extension verified as claimed.
