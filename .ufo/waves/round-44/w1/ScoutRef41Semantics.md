# ScoutRef41Semantics

Round-41 reference tool finding codes for the six class shapes. Interpreter: CPython 3.14.8 (`python3`). No tools installed. No blocker.

## Tool identity

`REF41_REV` / `REF41_SHA` in `.ufo/waves/round-44/c44_count_v5.py` lines 88-89:

- rev `1ef7a0e95f6884dd113fe583a997c633fe330ddd`
- sha `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py
```

Written to `/fast/scratch/hyaku/kake-r44/ScoutRef41Semantics/sitemap_audit_ref41.py` (15061 bytes, 459 lines). sha256 of that file equals `REF41_SHA` (`sha_match True`).

Invocation (every run): `python3 -B <tool> --manifest <manifest.json>`. The tool prints one JSON line. Exit 0 = verdict `clean`, 1 = `failed-policy`, 2 = `could-not-evaluate`.

Manifests live under `/fast/scratch/hyaku/kake-r44/ScoutRef41Semantics/manifests/<shape>/`. Each check is one urlset file, one `<loc>`, sitemap namespace `http://www.sitemaps.org/schemas/sitemap/0.9`.

## Six shapes

SitemapUrl on (a)-(f) is parseable and, except (e), shares scheme, host, and normalized port with the loc, so the loc code is not an authority mismatch. (c) keeps the bad port off the sitemapUrl on purpose (see falsification 3).

### (a) `%` in the path, and non-ASCII in the path

These are not one code. Bare `%` is a grammar reject. Non-ASCII in the path is accepted.

`%` only. loc `https://example.com/dir/a%b`, sitemapUrl `https://example.com/dir/sitemap.xml`.

```
EXIT 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "a-pct", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}
```

Code: **`loc_not_absolute`**. `_URI_RE` does not match (`%` is not `%HH`). `_parse_url` is `None`.

U+00E9 only. loc `https://example.com/dir/café`, sitemapUrl `https://example.com/dir/sitemap.xml`.

```
EXIT 0
{"version": 1, "verdict": "clean", "checks": [{"id": "a-e9", "status": "clean", "error": null, "findings": []}]}
```

Code: **`clean`**. Parse `('https', 'example.com', 443, '/dir/café')`.

Same `clean` / exit 0 for path code points U+00A0, U+4E2D, U+1F600, U+212A (KELVIN SIGN), U+017F (LATIN SMALL LETTER LONG S), each against `https://example.com/dir/sitemap.xml`. Kelvin+long-s stdout:

```
EXIT 0
{"version": 1, "verdict": "clean", "checks": [{"id": "kelvin", "status": "clean", "error": null, "findings": []}, {"id": "longs", "status": "clean", "error": null, "findings": []}]}
```

A single manifest that contained both the `%` loc and the U+00E9 loc exited 1 with the `%` check `loc_not_absolute` and the U+00E9 check `clean`. Same codes.

### (b) zero-padded in-range 6-digit port `:000080`, clean path

loc `https://example.com:000080/dir/page`, sitemapUrl `https://example.com:000080/dir/sitemap.xml`.

```
EXIT 0
{"version": 1, "verdict": "clean", "checks": [{"id": "b-pad80", "status": "clean", "error": null, "findings": []}]}
```

Code: **`clean`**. `:000080` is port 80 (`urlsplit` port 80). It is not a defect. The path `/dir/page` is under directory `/dir/`.

### (c) out-of-range 6-digit port `:123456` on the loc only

loc `https://example.com:123456/dir/page`, sitemapUrl `https://example.com/dir/sitemap.xml` (parseable, port 443).

```
EXIT 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c-oor", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}
```

Code: **`loc_not_absolute`**. The grammar matches (`(?::[0-9]*)?`). `urlsplit` then raises `Port out of range 0-65535`, and `_parse_url` returns `None`.

### (d) no path, sitemapUrl at the host root

Reading used: the G3 string, which is also `segment_smu` of a pathless URL. loc `https://example.com`, sitemapUrl `https://example.com/sitemap.xml`.

```
EXIT 0
{"version": 1, "verdict": "clean", "checks": [{"id": "d-nopath", "status": "clean", "error": null, "findings": []}]}
```

Code: **`clean`**. Empty path is normalized to `/` (`path = parts.path or "/"`). Directory of `/sitemap.xml` is `/`. `/` startswith `/`.

### (e) loc port differs from the sitemapUrl port

loc `https://example.com:9443/dir/page`, sitemapUrl `https://example.com:8443/dir/sitemap.xml`. Path is under `/dir/`.

```
EXIT 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "e-portdiff", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

Code: **`loc_out_of_scope`**. Parsed ports 9443 vs 8443. Compared tuple is scheme, host, port (`parsed[:3]`).

### (f) implicit https port against sitemapUrl `:443`

loc `https://example.com/dir/page`, sitemapUrl `https://example.com:443/dir/sitemap.xml`.

```
EXIT 0
{"version": 1, "verdict": "clean", "checks": [{"id": "f-impl443", "status": "clean", "error": null, "findings": []}]}
```

Code: **`clean`**. Implicit https port and explicit `:443` both become 443. Path `/dir/page` is under `/dir/`.

## Assumptions the blueprints state, against this oracle

Hold:

- (a) a bare `%` in the path is `loc_not_absolute`. A padded in-range port does not change that: loc `https://example.com:000080/dir/a%b` against sitemapUrl `https://example.com:000080/sitemap.xml` is still `loc_not_absolute` (exit 1, one finding).
- (b) `:000080` with a clean in-directory path is `clean`. Zero-padding is not a finding.
- (c) `:123456` on the loc, sitemapUrl parseable, is `loc_not_absolute` (urlsplit range, not the grammar).
- (d) a pathless loc against `https://<host>/sitemap.xml` is `clean`.
- (e) a different explicit port is `loc_out_of_scope` even when the path is in the sitemap directory.
- (f) implicit https vs explicit `:443`, path in that directory, is `clean`.

Falsified:

1. **Non-ASCII in the path is not `loc_not_absolute`.** G1 says a `%` or a non-ASCII unit is rejected as `loc_not_absolute`. The fold brief says the same for U+212A / U+017F. Measured: those path code points are `clean`. The round-41 grammar keeps U+0080..U+10FFFF in `unreserved` (tool comment at the URI regex; `_parse_url` agrees). A class that plants only a non-ASCII path unit will not diverge from a control that also accepts it. The ASCII `%` (not two hex digits) is the defect that produces `loc_not_absolute`. Other `CASE_INVARIANT_DEFECTS` characters were not run.

2. **G3's "derived sitemapUrl is `https://<host>/sitemap.xml`" is not what `layout_f`'s `derived_smu` returns for a pathless value.** Executing that expression (`c44_count_v5.py` lines 569-571) on `https://example.com` yields `https://example.comsitemap.xml` (`find` returns -1, `-1+1` is 0, and `0 or len` keeps the whole string). The tool on that pair:

```
EXIT 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "x-derived", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

Code: **`loc_out_of_scope`** (host `example.com` vs `example.comsitemap.xml`), not `clean`. `segment_smu` of the same value (lines 532-543) is `https://example.com/sitemap.xml`, which is shape (d) and is `clean`. The clean result holds for that sitemap string. It does not hold for a `value`/`loc` unit, because `layout_f` calls `derived_smu` for those and `segment_smu` only for fold pairs and pairfiles. This scout did not run `layout_f` itself.

3. **An out-of-range port on the sitemapUrl is `check_invalid`, not `loc_not_absolute`.** `derived_smu("https://example.com:123456/dir/page")` is `https://example.com:123456/sitemap.xml`. Both sides fail `_parse_url`. The tool:

```
EXIT 2
{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "c-both", "status": "error", "error": "check_invalid", "findings": []}]}
```

Code: **`check_invalid`**. Findings empty. A class that expects `loc_not_absolute` when the bad port is also on the derived sitemapUrl is wrong.

4. **G2's "the pairfile's first value is the manifest sitemapUrl" is not `segment_smu`.** `segment_smu("https://example.com:443/sitemap.xml")` is `https://example.com:443/sitemap.xml/sitemap.xml` (no second slash, so it appends `/sitemap.xml`). loc `https://example.com/page` against that sitemapUrl:

```
EXIT 1
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "x-seg", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

Code: **`loc_out_of_scope`** (path `/page` is not under `/sitemap.xml/`), not `clean`. Shape (f) is the in-scope form: sitemap directory `/dir/`, loc path `/dir/page`, explicit `:443` only on the sitemapUrl. That one is `clean`. `derived_smu("https://example.com:443/sitemap.xml")` happens to equal the input; `derived_smu` is not what pairfiles use.

## Files

- Scratch tool and manifests: `/fast/scratch/hyaku/kake-r44/ScoutRef41Semantics/`
- This report: `.ufo/waves/round-44/w1/ScoutRef41Semantics.md`

Nothing under the lane repo was edited except this report. Controls were not run. Full counter was not run.
