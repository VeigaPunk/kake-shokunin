# Round-39 C1 contract — `scripts/sitemap_audit.py` (offline sitemap-file audit)

Written by the round-39 L1 (attempt 2) before any seat was dispatched. Sources: sitemaps.org
protocol page and its two XSDs, W3C Datetime note, all opened 2026-10-23 (`corpus/SOURCES.md`
S102–S104). Where the sources disagree the contract picks one reading and says so ("lane reading").
Every numbered sentence below is part of the rule of record; behaviour on inputs these sentences
do not cover is outside the contract.

## Usage

1. `python3 scripts/sitemap_audit.py --manifest <path>` reads the manifest and the files it names,
   writes one JSON document to stdout, writes nothing else, and uses no network. Python 3 standard
   library only.
2. Any other argument list is a usage error: exit 64, stdout ignored.

## Manifest (version 1)

3. The manifest is a JSON object `{"version": 1, "checks": [...]}`; `checks` is a non-empty array.
   Anything else (unreadable file, invalid JSON, not an object, `version` not the integer 1,
   `checks` missing, not an array or empty) is `input_invalid`: stdout
   `{"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []}`, exit 2.
4. Each check is an object with string members `id`, `file`, `sitemapUrl`. A check that is not an
   object, lacks one of them, has a non-string one, repeats an earlier check's `id`, has a `file`
   that is absolute or has a `..` path segment, or has a `sitemapUrl` that is not an absolute
   `http`/`https` URL with a host, is an error check with error `check_invalid`.
5. `file` is resolved against the manifest's directory. A file that cannot be read is an error
   check with error `file_unreadable`.

## Findings on one sitemap file (rules (a)–(k))

Findings are pairs `(code, entry)`. `entry` is the 1-based position of the entry among the root's
entries (rule (d)), or `null` for a file-level finding. Findings are compared as a set.

- **(a) Encoding.** 6. The file's bytes must decode as UTF-8; a leading UTF-8 byte-order mark is
  allowed. 7. If the XML declaration has an `encoding` pseudo-attribute, its value must be `UTF-8`,
  compared case-insensitively. Either failure gives `encoding_invalid` (file-level) and no other
  finding for that file (S102 "The file itself must be UTF-8 encoded").
- **(b) Well-formedness.** 8. The file must be well-formed XML 1.0 with namespaces; otherwise
  `xml_malformed` (file-level) and no other finding. 9. Lane reading (safety, not from a source):
  a document type declaration gives `doctype_present` (file-level) and no other finding.
- **(c) Root.** 10. The root element must be `urlset` or `sitemapindex` in the namespace
  `http://www.sitemaps.org/schemas/sitemap/0.9`, whatever prefix binds it; otherwise
  `root_invalid` (file-level) and no other finding (S102; S103).
- **(d) Entries.** 11. The entries are the root's child elements in the sitemap namespace named
  `url` (in a `urlset`) or `sitemap` (in a `sitemapindex`). 12. Zero entries gives `no_entries`
  (file-level). 13. Any other root child in the sitemap namespace gives `element_unexpected`
  (file-level). 14. Elements in any other namespace, at any level, are ignored (S102 "Extending
  the Sitemaps protocol").
- **(e) Entry children.** 15. An entry must have exactly one `loc` child in the sitemap namespace:
  none gives `loc_missing`, more than one `loc_repeated` (entry-level), and rules (g)–(h) are then
  skipped for that entry. 16. In a `urlset` entry, `lastmod`, `changefreq` and `priority` may each
  appear at most once; in a `sitemapindex` entry, `lastmod` at most once. A repeat gives
  `field_repeated` (entry-level) and that field's value rule is skipped. 17. Any other child of an
  entry in the sitemap namespace (including `changefreq` or `priority` in a `sitemapindex` entry)
  gives `element_unexpected` (entry-level). 18. Lane reading: child order is not checked (the XSD
  sequence orders them; the protocol text does not).
- **(f) Limits.** 19. A file larger than 52,428,800 bytes gives `too_large` (file-level) and no
  other finding. 20. More than 50,000 entries gives `too_many_entries` (file-level), in addition
  to entry findings (S102 "no more than 50,000 URLs and … no larger than 50MB (52,428,800 bytes)").
- **(g) `loc` form.** 21. Every element value in rules (g)–(k) is read after removing leading and
  trailing XML whitespace (U+0020, U+0009, U+000D, U+000A) and nothing else. 22. A `loc` must be an
  absolute URL whose scheme is `http` or `https` (case-insensitive) and whose host is non-empty;
  otherwise `loc_not_absolute`, and rule (h) is skipped for that entry. 23. Lane reading of a
  source conflict: a `loc` of 2,048 or more characters (Unicode code points) gives `loc_too_long`
  (S102 "must be less than 2,048 characters"; S103's `maxLength` 2048 would allow exactly 2,048).
- **(h) Scope.** 24. Scheme and host are compared case-insensitively; a missing port equals the
  scheme's default (80 for `http`, 443 for `https`). 25. In a `urlset`, a `loc` whose scheme, host
  or port differs from the `sitemapUrl`'s, or whose path (an empty path read as `/`) does not
  start with the `sitemapUrl`'s directory — its path up to and including the last `/` — gives
  `loc_out_of_scope`. 26. The path prefix is compared as written: case-sensitive, without
  percent-decoding and without dot-segment removal (S102 "can include any URLs starting with").
  27. In a `sitemapindex`, only scheme, host and port must match (S102 "can only specify Sitemaps
  that are found on the same site").
- **(i) `lastmod`.** 28. Allowed forms are the W3C Datetime levels with a complete date:
  `YYYY-MM-DD`, `YYYY-MM-DDThh:mmTZD`, `YYYY-MM-DDThh:mm:ssTZD`, `YYYY-MM-DDThh:mm:ss.sTZD`
  (`s` one or more digits; TZD is `Z` or `+hh:mm`/`-hh:mm` with hh 00–23, mm 00–59). 29. The date
  must exist in the Gregorian calendar (leap years included); hh 00–23, mm 00–59, ss 00–59.
  30. Lane reading: the year-only and year-month levels, and a time without TZD, are invalid
  (S102 "omit the time portion, if desired, and use YYYY-MM-DD"; S104). Otherwise
  `lastmod_invalid` (entry-level). Applies in both file kinds.
- **(j) `changefreq`** (urlset only). 31. The value must equal one of `always`, `hourly`, `daily`,
  `weekly`, `monthly`, `yearly`, `never`, case-sensitively; otherwise `changefreq_invalid`
  (entry-level) (S103 enumeration).
- **(k) `priority`** (urlset only). 32. The value must match the `xsd:decimal` lexical form
  `[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)` and lie in 0.0–1.0 inclusive as an exact decimal; otherwise
  `priority_invalid` (entry-level) (S103 `minInclusive`/`maxInclusive`).

## Output and verdict

33. stdout is one JSON object `{"version": 1, "verdict": V, "checks": [...]}` with one item per
    manifest check in manifest order:
    `{"id": <id or null>, "status": "clean"|"findings"|"error", "error": <code or null>,
    "findings": [{"code": C, "entry": N|null}, ...]}`. An error check has empty `findings`.
34. Verdict: any error check → `could-not-evaluate`, exit 2; otherwise any finding →
    `failed-policy`, exit 1; otherwise `clean`, exit 0.

## Limits

No live fetch, no gzip, no robots.txt `Sitemap:` cross-submission, no text or RSS/Atom sitemaps,
no XSD validation of extension namespaces, no check that a `lastmod` is true. Search engines may
read a sitemap more loosely than this contract (S102: "Support for these optional tags may vary
among search engines").
