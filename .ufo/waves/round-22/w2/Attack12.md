# Attack12 — frozen case `query_preserved` (round 22, wave 2)

Seat: `KakeR22.Attack12` (leaf, author-side falsifier). Not independent non-author closure.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Candidate under test:
`c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (observed lane HEAD; the shared-context base
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` is the BEFORE revision). Production source,
oracle, and fixture bytes were read only and are frozen; no production file edited, no
build/lint/test/formatter, no install, no package transaction, no network, no git/jj writes.
Scratch fixtures only under `/tmp/kake-r22-attack12/`; the only lane write is this report.

Frozen input digests (observed at test time):

```
35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7  scripts/canonical_audit.py
28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6  .ufo/waves/round-22/cases.json
6884ca0e94fce11687dd6adc99df30fbfbc089d8e22361ce066ce4d0ec83a568  .ufo/waves/round-22/fixtures/query_preserved/page.html
5a4099bc357981b9085929efff9f31bd1f55cb90d393cf0881cc7bd109fca46e  .ufo/waves/round-22/fixtures/query_preserved/manifest.json
```

`git status --porcelain scripts/ .ufo/waves/round-22/matrix.py .ufo/waves/round-22/cases.json
.ufo/waves/round-22/fixtures/query_preserved` was empty after all probes.

## 1. Frozen case inputs

`cases.json` record (input expectation, not an oracle by itself):

```json
{"caseId":"query_preserved","manifest":"fixtures/query_preserved/manifest.json","expectedExit":0,"expectedFindings":["clean"],"rationale":"Local publisher policy: retain and compare the complete query string."}
```

`fixtures/query_preserved/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html?x=1&y=2"}]}
```

`fixtures/query_preserved/page.html`:

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html?x=1&amp;y=2"></head><body></body></html>
```

Contract policy under test (`.ufo/waves/round-22/contract.json`): "Exactly one canonical link
in explicit head per page, rel ASCII case-insensitive token list; resolve href with first head
base href or document URL; compare WHATWG-like HTTP(S) normalized absolute URL to
expectedCanonical, **preserve query**, reject fragments and credentials." Exit map: `0` clean,
`1` failed policy, `2` could-not-evaluate input/unsupported shape.

## 2. Independent derivation (written before executing the case)

Derived from the contract policy plus HTML/URL semantics and the fixture bytes only — not from
the validator's output:

1. Head is explicit (`<head>`) and closed (`</head>`); document shape is supported, so no
   `html_unsupported`.
2. Exactly one `link` with `rel` token `canonical` sits inside that head: one canonical, so no
   `canonical_missing`, `canonical_multiple`, or `canonical_outside_head`.
3. `href` is present and non-empty at the HTML level, so no `canonical_href_missing`.
4. The attribute value contains `&amp;`, an HTML character reference that decodes exactly once
   to `&` in an attribute value (independent probe: `HTMLParser` yields
   `https://e.test/a?x=1&y=2` for `&amp;`, `&#38;`, and `&#x26;`). The decoded href is
   `https://example.test/project/a.html?x=1&y=2`.
5. The href is an absolute HTTP(S) URL with no `#` fragment and no credentials, so no
   `canonical_fragment` and no `canonical_url_invalid`.
6. Origin `https://example.test`, path `/project/a.html`, query `x=1&y=2` are all byte-equal to
   `expectedCanonical` after the same normalization; "preserve query" means the parameter
   string is retained and compared, not sorted, decoded, or dropped. So no `canonical_mismatch`.
7. No finding is produced → verdict `clean`, findings `[]`, exit `0`.

**Pre-registered prediction: exit `0`, finding id `clean`** (the matrix maps empty findings to
`clean`). `cases.json` agrees; it is corroboration, not the source of the prediction.

## 3. Frozen matrix execution

Command exactly as authorized:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case query_preserved
```

Exit: `0`. Stdout verbatim:

```
PASS caseId=query_preserved exit=0 findings=clean
SUMMARY selection=query_preserved accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

No stderr. Prediction matched observation exactly. The committed
`.ufo/waves/round-22/measure-after.json` independently records
`sourceCommit=c0fd6d53906a42dadfb997ddda2c8162f1adb78a`, `deterministic=true`,
`sameInstrumentAsBefore=true`, and two instrument runs exiting `0`.

Control: `python3 scripts/canonical_audit.py --selftest` exited `0` with
`{"selftest":{"passed":true,...}}` over 56 cases; the embedded `query_preserved`,
`empty_query_delimiter`, `relative_empty_query`, and `wrong_query` cases all matched their
declared expectations.

## 4. Nearest-neighbor fixture (same parser/policy boundary)

Built under `/tmp/kake-r22-attack12/order_swap/` — same absolute URL, same parameter multiset,
different serialized order, entity-encoded `&` exactly as the frozen case:

`manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html?x=1&y=2"}]}
```

`page.html`:

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html?y=2&amp;x=1"></head><body></body></html>
```

Independent prediction: "retain and compare the **complete** query string" forbids parameter
reordering or set-equality, so the `y=2&x=1` serialization must not match `x=1&y=2`; expected
exit `1`, finding `canonical_mismatch`.

Command and result:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-attack12/order_swap/manifest.json --json
```

Exit: `1`. Stdout verbatim:

```json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Prediction matched. The validator discriminates on query order; it does not normalize the
query into a parameter set.

## 5. Additional boundary probes (same query-preservation boundary)

All predictions were written from the source-observed normalizer (`quote` with safe set
`/?:@!$&'()*+,;=-._~%[]`, `query_delimiter_present` tracking, literal `#` rejected before
splitting) and the contract before each run. One table, actual = captured CLI result:

| # | probe (href vs expected) | predicted exit/id | actual exit/id | establishes |
|---|---|---|---|---|
| 1 | `?y=2&x=1` vs `?x=1&y=2` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | order is part of the query; no set/sort normalization |
| 2 | `?x=1&x=2&y=2` vs `?x=1&y=2&x=2` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | repeated-key position is preserved |
| 3 | `?x=1&#38;y=2` vs `?x=1&y=2` | 0 clean | 0 clean | numeric character reference decodes to the same retained query |
| 4 | `...a.html?` vs `...a.html` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | empty query delimiter is distinct from absent query (not dropped by `urljoin`) |
| 5 | `?x=1&y=2&` vs `?x=1&y=2` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | trailing empty parameter is retained, not trimmed |
| 6 | `?q=a+b%2Fc` vs same | 0 clean | 0 clean | literal `+` is not decoded to space; `%2F` not decoded |
| 7 | `?x=a%23b` vs same | 0 clean | 0 clean | only a literal `#` is a fragment; `%23` stays query data |
| 8 | unquoted `href=...?x=1&amp;y=2` vs `?x=1&y=2` | 0 clean | 0 clean | entity decode also holds for an unquoted attribute value |
| 9 | `?a=b?c` vs same | 0 clean | 0 clean | a `?` inside the query is retained |
| 10 | `?a=1;b=2` vs same | 0 clean | 0 clean | no `;` parameter splitting/rewriting |
| 11 | `?q=café` (literal UTF-8) vs `?q=caf%C3%A9` | 0 clean | 0 clean | UTF-8 query bytes normalized consistently on both sides |
| 12 | `?q=%7E` vs `?q=~` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | percent-encoded and literal tilde stay distinct (WHATWG-consistent) |
| 13 | `?q=%7Bv%7D` vs `?q={v}` | 0 clean | 0 clean | **WHATWG divergence (permissive):** implementation encodes literal `{}` to `%7B%7D`; WHATWG special-query leaves them literal |
| 14 | `?q=it's` vs `?q=it%27s` | 1 `canonical_mismatch` | 1 `canonical_mismatch` | **WHATWG divergence (strict):** implementation leaves `'` literal; WHATWG special-query serializes it as `%27` |

Verbatim capture for rows 1–14 (command per row:
`python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack12/<probe>/manifest.json --json`,
run with cwd = lane root):

```
order_swap	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
repeat_order	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
query_order_entity	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
empty_query_vs_absent	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
trailing_amp	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
plus_and_pct	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
encoded_hash	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
unquoted_amp	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
pct_quote	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
pct_brace	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
pct_tilde	rc=1	{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
literal_utf8	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
qmark_in_query	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
semicolon_params	rc=0	{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

WHATWG reference (Node's WHATWG `URL`, run as an external public oracle):
`?q=it's` → `?q=it%27s`; `?q=it%27s` unchanged; `?q={v}` → `?q={v}`; `?q=%7Bv%7D`
unchanged; `?q=~` unchanged; `?q=%7E` unchanged; `a?` → `a?`. The module's normalizer
(`normalize_http_url`) returns literal `'` unchanged, literal `{v}` → `%7Bv%7D`, and preserves
`%7B`/`%27`/`%7E`; equality probes: brace literal≡percent `True`, quote literal≡percent
`False`, tilde literal≡percent `False`.

Impact: the divergence is an equivalence-class difference in the query encode set, not a loss
of query bytes. No probe accepted a semantically different query (both divergent classes are
decode-equivalent: `{`↔`%7B`, `'`↔`%27`), the frozen `query_preserved` query `x=1&y=2` is
unaffected by either class, and the contract says "WHATWG-like" rather than exact WHATWG. It
should still be stated explicitly if strict WHATWG serialization parity is promised:
`'` is kept literal where WHATWG emits `%27`, while `{ } | ^ \`` are encoded where WHATWG
leaves them literal.

## 6. Verdict

- Frozen `query_preserved`: **claim survives.** Independent prediction (exit `0`, `clean`) =
  observed matrix result (`PASS ... exit=0 findings=clean`, matrix exit `0`), and the nearest
  neighbor that changes only query serialization order is correctly rejected with exit `1`
  `canonical_mismatch`. The instrument is not passing the case by accident: the same CLI
  distinguishes reordered, re-encoded, empty, and truncated queries in all 14 probes.
- Remaining unknowns: (a) the `'`/`{ } | ^ \`` query encode-set deviation from WHATWG described
  above, low severity and out of the frozen case's scope; (b) HTMLParser-vs-full-HTML5 tree
  construction limits are already declared by the contract and were not re-audited here;
  (c) this seat did not test search-engine selection, JS rendering, HTTP, redirects, or network
  freshness (declared non-claims).

## 7. Reproduction

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case query_preserved
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack12/order_swap/manifest.json --json
python3 scripts/canonical_audit.py --selftest
```

Scratch fixtures are disposable under `/tmp/kake-r22-attack12/`; the report above is the only
lane artifact produced by this seat.
