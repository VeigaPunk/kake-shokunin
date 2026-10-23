# ScoutReopenS011 — live re-open of S011 (RFC 9309) for C2 rule (k)

Access: `GET https://www.rfc-editor.org/rfc/rfc9309.html`, 2026-10-23T04:30:20Z, curl exit 0, HTTP
200, 82367 bytes, sha256 `bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87`, 0.185 s,
final URL = requested. Sandbox: `/fast/scratch/hyaku/kake-r38w1/ScoutReopenS011/`.

## Freshness / same bytes as retained
- Retained `.ufo/waves/round-37/sources/S011.html.gz` gunzips to 82367 bytes, sha256 `bbaa2806…dc1a87`,
  `cmp` exit 0 → **byte-identical to today's live fetch**.
- `receipts.json` S011: `accessedUtc 2026-10-23T02:50:49Z`, `bodySha256 bbaa2806…dc1a87`, status 200 →
  unchanged across ~1 h 40 m; rfc-editor serves a stable page (no errata overlay on it).
- Retained `S011.txt` sha256 `8e632e483ba4c6c9808a1436d3912079b1856e77d52ba2ca7245dc8d39259cf3` (3268
  words) = `receipts.textSha256`. Only delta vs live HTML text: citations render as `[ RFC3986 ]`
  where HTML has `[RFC3986]` (spacing only).

## Quotes (≤25 words each; live HTML lines in `rfc9309-live.html`)
- §2.2.2 l.1635: "The /robots.txt URI is implicitly allowed."
- §2.2.2 l.1637–39: "Octets in the URI … in the reserved range defined by [RFC3986], MUST be
  percent-encoded … prior to comparison."
- §2.2.2 l.1641: "If a percent-encoded ASCII octet is encountered in the URI, it MUST be unencoded
  prior to comparison, unless it is a reserved character …" (rest: "… or the character is outside the
  unreserved character range.")
- §2.2.2 l.1627: "The matching SHOULD be case sensitive."
- §2.3 l.1757–59: "The rules MUST be accessible in a file named "/robots.txt" (all lowercase) in the
  top-level path of the service."
- §2.3 l.1764: "scheme:[//authority]/robots.txt"
- §2.2.2 Figure 4 l.1654: path `/foo/bar?baz=quz` → path to match `/foo/bar?baz=quz` (query inside the
  matched path). §2.2.3 Figure 6 l.1648–52: `/path/file-with-a-%2A.html` ↔ `…/file-with-a-*.html`,
  `/path/foo-%24` ↔ `…/foo-$` (side finding below).

## Verdict on (k)
- **Percent-encoded spellings → FOLLOWS (high).** The unencoding MUST is stated "prior to comparison"
  with no restriction to rule matching, in the same subsection as the implicit-allow sentence. The
  round-37 raw compare (`scripts/robots_audit.py:530` at `2dab7f31`) denies `/robots%2Etxt`, which the
  RFC says must be unencoded to `/robots.txt` before comparison; (k) repairs it. The build-side excuse
  at `robots_audit.py:47-50` (sentence order) is not an RFC argument — cite "prior to comparison".
- **Case breaks it → FOLLOWS (high, and on a MUST).** §2.3's "(all lowercase)" is normative;
  `/ROBOTS.TXT` is not the robots.txt URI. Agrees with selftest `e11-robots-txt-exemption-is-exact`.
- **Non-empty query breaks it → FOLLOWS as inference (medium-high).** §2.3 gives the URI as
  `scheme:[//authority]/robots.txt` (no query) and Figure 4 puts the query inside the matched path.
  No single sentence says "query breaks it"; the reading is the conservative one and agrees with C2's
  clarification that `/robots.txt?` (empty query) is allowed (verified below).
- **Pin "normalized".** The RFC mandates only §2.2.2 octet normalization "prior to comparison"; it never
  mandates `remove_dot_segments` or case folding, so `/foo/../robots.txt` is not implicitly allowed under
  (k) as written. If a sealed case assumes full RFC 3986 normalization, the wording, not the RFC, decides.

## Differential demonstration (sandbox clone at 2dab7f31; one-line patch)
`diff tool_round37.py tool_k.py` → only l.530 `path` → `normalize(path)`; tool_k.py sha256
`3c8e928c5bd2e0d019e8eae34a13a3b16b322ad1c2e34db95338aac7b7245a70`. Fixture `user-agent: *` /
`disallow: /`; 11 URL variants, each `expect: allow`:
- round-37 tool: `blocked` for `/robots%2Etxt`, `/robots%2etxt`, `/%72obots.txt`, plus case, `?x=1`,
  `/robots.txt/`, `/foo/../robots.txt`, `%20`, `%2F`; exit 1.
- (k) tool: same minus the three encoded spellings (now allowed); exit 1.
- `--manifest explicit/manifest.json` (robots: `disallow: /robots.txt`, `disallow: /`) exit 1:
  `plain-allow`, `pct2E-allow` clean (explicit disallow does not override); `pct2E` with
  `expect: disallow` → `exposed`; `Robots.txt` → blocked. Reproduce from
  `/fast/scratch/hyaku/kake-r38w1/ScoutReopenS011/{demo,explicit}`.

## Harm instruments at the (k) build (tool-file mode)
- `python3 -B clone/scripts/robots_audit_selftest.py --tool tool_k.py` → exit 0, `137/137`,
  `verdict clean`, 2.9 s.
- `python3 -B clone/.ufo/waves/round-37/sealed_count.py --root clone --tool-file $PWD/tool_k.py
  --key-revision 424aa248` → exit 0, `cases 28`, `passed 28`, `met true`, `counterSha256
  2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3`.
- (k) is compatible with both instruments: no selftest case distinguishes raw from normalized, and the
  only implicit-allow cases (`e11` `/Robots.txt`, `e12` `/robots.txt`) are invariant under (k).

## Side finding (outside (k), same sources; advisory)
§2.2.2 ("reserved range … MUST be percent-encoded … prior to comparison") and §2.2.3 Figure 6 require a
raw `*`/`$` URI to compare equal to a rule's `%2A`/`%24`. `normalize()` keeps `%2A`/`%24` and leaves raw
`*`/`$` (`robots_audit.py:132-155`), so both Figure 6 rows evaluate **allow**: with
`disallow: /path/file-with-a-%2A.html` and `disallow: /path/foo-%24`, URLs `…/file-with-a-*.html` and
`…/path/foo-$` report `exposed` under `expect: disallow` (exit 1, `fig6/manifest.json`). Round-37 (e)
behaviour, unchanged by (k); no (k) case I tested is affected.
## Not verified
- The 20 sealed C2 cases (no key; not listed, read or searched; sealed trees untouched), the v3
  counter and the C2 `met` predicate (no key; not my seat).
- google/robotstxt implementation: S096 is the landing page text, not source. RFC errata list not
  fetched (page not named in my item). No tool installs or upgrades were made.
