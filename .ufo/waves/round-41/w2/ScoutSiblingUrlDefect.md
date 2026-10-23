# ScoutSiblingUrlDefect — kake R41 wave 2

Axes: operability (does the cited site still decide URL validity by urlsplit acceptance), freshness (citations at build eae5ae2, not the pre-build tree). Defect = the C1 mismatch: validity by urlsplit acceptance instead of an RFC 3986 `URI` with authority and a non-empty host before the split.

Commands (all exit 0): `git rev-parse HEAD` = eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6; `git status --porcelain` on the nine scripts and the connector was empty; `git show eae5ae2^:scripts/sitemap_audit.py` (parent 9e3c31d, the connector commit) line 73 is `parts = urlsplit(value)`; `git blame -L 63,110 eae5ae2 -- scripts/sitemap_audit.py` puts lines 67–87 and 92–93 on eae5ae2. Sibling count: `rg -c -e 'urlsplit|urlparse'` over `/home/vgpnk/Projects/shokunin/*-shokunin/scripts` → kake 22, every other lane 0.

No tools installed.

## Per row

1. `scripts/sitemap_audit.py:73` YES — **refuted** (wrong at the build). Line 73 is `_UNRESERVED`, the repair's character class, not a judgment. `loc` is `_parse_url` at :308; `sitemapUrl` at :382. The gate at :92–93 returns None when `_URI_RE` fails, before `urlsplit` at :95. YES was true of parent 9e3c31d:73 and is false of eae5ae2. Severity: high for the table. Residual, not a restore of YES: IP-literal is `\[[^\]]*\]` (:80) and U+0080+ counts as unreserved (:69–73); comment :71–72 leaves IP-literal contents and port range to urlsplit. Low, documented.

2. `scripts/robots_audit.py:520` NO — **confirmed**. `parse_http_url` splits at :520 after `url_characters_ok` (:517; forbidden class :149, RFC 3986 §2 characters, not Appendix A). Lane reading :50–52: only scheme http(s) and a non-empty host; port, userinfo and further host syntax are not judged.

3. `scripts/link_preview_audit.py:151` NO — **confirmed**. `absolute_http_url` (:149–154) is urlsplit plus scheme plus hostname. Policy :15 and :22 is "absolute HTTP(S) URL with a host", stated as lane policy, not the sitemap RFC 3986 reading.

4. `scripts/live_snapshot.py:37` NO — **confirmed**. `safe_url` (:36–39): scheme, hostname, no userinfo. Module line 6 is a fetch safety guard, not a URI-grammar claim.

5. `scripts/receipt_replay.py:385` NO — **confirmed**. `safe_http_url` (:381–389) rejects controls, then scheme, hostname, no userinfo. Callers :425 and :431–432 are fetch-record guards. Header states no RFC 3986 URI grammar.

6. `scripts/source_snapshot.py:80` NO — **confirmed** for the defect. `valid_url` (:77–88) is a fetch-time http(s) guard with no userinfo. The table's "host" is slightly off: :85 tests `bool(parts.netloc)`, not hostname. "NO" holds; "host" is overstated.

7. `scripts/source_snapshot.py:171` NO — **confirmed**. Only `urlsplit(target).scheme in ("http", "https")`. A redirect-follow stop, not a validity claim.

8. `scripts/base_path_audit.py:376` NO — **confirmed**. `_parse_absolute` under the browser-like standard at :51 ("rather than bare RFC 3986").

9. `scripts/base_path_audit.py:421` NO — **confirmed**. `urlsplit(base_url).scheme` only. Scheme extraction, not a validity decision.

10. `scripts/canonical_audit.py:482,494` NO — **confirmed**. `normalize_http_url` rejects whitespace, controls, backslash and fragment (:474–478) before the splits, then `_host_and_port` (:382–443, called :505) checks IPv6, IPv4, DNS labels and port 0–65535. Stricter than urlsplit acceptance.

11. `scripts/source_recheck.py:516-523` NO — **confirmed**. No urlsplit in that file. `parse_uri_ref` is Appendix B (:92–106); the comment says the pattern always matches. `host_of` (:202–212) only strips userinfo and port. Analogous looseness, different parser.

## Other statements

- "Only `sitemap_audit.py:73` shares the defect": **wrong** at eae5ae2. That line is the repair; no remaining row shares the defect.
- "source_recheck does not use urlsplit": **holds**.
- "No sibling `scripts/` tree uses urlsplit": **holds** (0 outside kake).
- "20 urlsplit hits, all in kake": **overstated**. The build tree has 22 matches; the two added are comments at `sitemap_audit.py:72` and `:93`, not new call sites.
