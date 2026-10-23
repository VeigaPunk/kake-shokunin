# ReviewSkillAmendment — SKILL.md "Sitemap file audit — round-41 URL rule" (SKILL.md:1157-1170)

Reviewed the worktree text of the section (it is modified, uncommitted, tracking build `50287ac6…`;
during review HEAD moved eae5ae2c → 0c5ad2f6, a mid-flight revision of the very sentences under review).
Method: ran `scripts/sitemap_audit.py` vs the round-40 base (git archive 8eb121c8, sha `4de35f8c…1460e`)
and first build (archive eae5ae2c, `0b485431…13edbf`) on ~70 small manifests in
`/fast/scratch/hyaku/kake-r41w2/ReviewSkillAmendment/` (harness.py; exit codes recorded below).

## Commands / exit
- `python3 scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → `PASS 204/204`, exit 0.
- Same on base tool → `PASS 194/204`, 13 `r41_*` FAIL lines (all red fixtures are `r41_*`).
- `jq -s 'map(select(.met))|length' verification/w1/*.json` → 15; file count 141.
- `sha256sum scripts/sitemap_audit.py` → `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` ✓ the new text's `50287ac6…1dde7d`.
- Harness: build gives `loc_not_absolute`/`check_invalid` for interior space, `"<>\^`{|}`, DEL, interior
  TAB (loc), all of \x00/\x01/\x0b/\x1f/\x7f/TAB (sitemapUrl), `]`/`[` in path, second `#`, `a@b@host`,
  `%zz`/`%`/`%2`; base gives `loc_out_of_scope`/`clean`/`check_invalid` as recorded per case.

## Per sentence (numbering = sentences of the section, in order)
S1 sha `50287ac6…1dde7d` + "(revised … TAB/LF/CR inside an IP literal stays invalid)": **holds.**
  `http://[::\t1]/a` parses to `loc_out_of_scope` on `0b485431…` (regression corroborated) and is
  `loc_not_absolute`/`check_invalid` on `50287ac6…`; `http://[fe80::1%eth0]/x` still parses (zone-id
  acceptance kept via urlsplit), matching SCORECARD:2835-2837.
S2 "judged as written against RFC 3986 `URI` with an authority and a non-empty host … only then does
  `urlsplit` split it": **holds.** `_URI_RE` matches before `urlsplit` in `_parse_url`
  (scripts/sitemap_audit.py:71-92); loc gated at :308 (after `_text_of` strip, :305 — leading WS clean,
  verified) and sitemapUrl at :382. S102 quote verified in retained bytes
  (.ufo/waves/round-39/sources/sitemaps-protocol.txt:276); S117 = RFC 3986 Appx A (SOURCES.md:125).
S3 character list → `loc_not_absolute`/`check_invalid` "where the round-40 tool accepted them" (204
  fixtures): **overstated** (two carve-outs; all build-side error codes correct).
S4 "U+0080+ still accepted wherever RFC 3986 allows `unreserved` (broader than `ucschar`); IP-literal
  contents and ports >65535 still judged by `urlsplit` (it rejects >65535, RFC 3986 does not)":
  **holds.** `\x85` (a ucschar hole) and NBSP/CJK accepted; `[2001:db8::zz]`, `:99999` rejected only via
  the urlsplit `ValueError` path; `port = *DIGIT` (SOURCES.md:125).
S5 proof status "exploratory — counter met by 15 of 141 wave-1 controls … use the selftest, treat the
  counter as information": **holds.** Recount 15/141; `c1_count.py` header imports `abnf.grammars.rfc3986`
  (S118, SOURCES.md:126); matches SCORECARD kill-rule section and "v1 score is information only".

## Findings
- LOW SKILL.md:1162-1163 — S3's "where the round-40 tool accepted them" overgeneralizes: `[`/`]` **in the
  host** already gave `loc_not_absolute`/`check_invalid` on round-40 (urlsplit bracket check); the new
  behavior is only `[`/`]` in path/query/fragment (verified `a]b`/`a[b` clean on base). Either fix the
  example ("a `[` or `]` outside the authority") or keep the scope note.
- LOW SKILL.md:1162 — "any C0 control" is exact only for `sitemapUrl`; for `loc`, non-XML-legal C0s
  (`&#1;`) give `xml_malformed`, not `loc_not_absolute`, and edge TAB/LF/CR are stripped by sentence 21.
  Behavior is stronger than the sentence; wording is imprecise.
- LOW freshness — "(selftest `r41_*`, 204 fixtures)" is true at write time; SCORECARD:2858-2864 already
  records a committed selftest of 225 fixtures (`18752057…`) not yet landed in the worktree → the count
  will be stale the moment that lands. (Selftest count discrepancy at review time, not a behavior defect.)

## Residual risk / gaps
- Oracle cross-check (abnf wheel) not re-run by this seat; counter claims taken from receipts + source.
- r40 `PASS 194/204` lists 13 FAIL names vs arithmetic gap of 10 — not reconciled here (three names may
  be multi-assert or coverage fails); SCORECARD:2844 says 16 of 21 red at that commit.
- Fixture numerator left vague: 204 total = 183 + 15 + 6 ipv6 fixtures; SKILL says "selftest `r41_*`"
  which is accurate for all named sets.

No installs performed (no new tools needed); git used read-only (archive/diff/log/status).
