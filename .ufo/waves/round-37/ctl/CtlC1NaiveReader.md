# Control Report — `CtlC1NaiveReader`

- **Control**: `CtlC1NaiveReader` (C1 naive-reader control).
- **What it skips**: Implements CLI usage, (a) status ranges (`200–299`, `400–499`, `500–599`), (f) check validation, (g) manifest validation, and the verdict rule faithfully, but skips the contract's (b)–(e) parser/normalizer for `200–299` and delegates to Python's standard `urllib.robotparser.RobotFileParser` (`parse(lines)` + `can_fetch(userAgent, url)`).
- **Tooling installs/updates**: None (`python3` 3.14 standard library only).
- **Score**: Scored by L1 against the sealed key (seat never accessed `/fast/scratch/hyaku/kake-r37/private/`).

## Deliverables (absolute paths & SHA-256)

- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/robots_audit.py`
  `fdc64538c3b9cc889e659f24798529218a871295a24c0dfa4d4e11da2db13491`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/run_own_manifests.py`
  `2c58027632a202856f3c0e6f4998e523c45b98b1203bc2c66bb305039a2b0467`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/manifests/manifest_divergences.json`
  `0233f2e23d337babce203dc0b05c7182c878818e6cd3a1fbabdc7bb28b6ba061`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/manifests/manifest_af.json`
  `619be7d0d79a72457b6bc01dd781765e68313522b2aa8940dadbccc78748c6b9`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/manifests/manifest_g_fault.json`
  `17427f799e3b5c749790b0a8b611ba51b781c69835c90863f6fb38cfbcbdf2d5`

## Contract (b)–(e) vs. `urllib.robotparser.RobotFileParser` Divergences Verified

1. **(b) No 500 KiB limit**: `RobotFileParser` parses rules past byte 512,000 (`b1_over_512000_bytes` -> `blocked`).
2. **(b) Leading UTF-8 BOM (`EF BB BF`) not stripped**: `\ufeffuser-agent` fails to match `"user-agent"`, dropping the group (`b2_utf8_bom_first_line` -> `exposed`).
3. **(b)/(c) `crawl-delay` / `request-rate` split consecutive `user-agent` lines**: `RobotFileParser.parse()` sets `state = 2` on `crawl-delay`/`request-rate`, so a following `user-agent` starts a new group instead of sharing rules (`b3_crawldelay_splits_group` -> `exposed`).
4. **(b) Line splitting on non-CR/LF Unicode breaks**: `.splitlines()` splits on `\x0b`, `\x0c`, `\x85`, `\u2028`, `\u2029` inside `#` comments (`b4_formfeed_in_comment_splits_line` -> `blocked`).
5. **(c) Substring `user-agent` match**: `Entry.applies_to` checks `agent in useragent` before falling back to `*`, so `User-agent: bot` matches `mybot` (`c1_ua_substring_match` -> `blocked`).
6. **(d) Mid-pattern `$` rejected**: `RuleLine` raises `ValueError` when `$` appears before the end of a rule and `parse()` silently drops the rule instead of matching `$` literally (`d1_mid_dollar_dropped` -> `exposed`).
7. **(d) Wildcard match length uses matched target slice (`m.end()`) instead of rule octet length**: `Disallow: /*` (2 octets) on `/page/index.html` scores `17`, beating `Allow: /page` (5 octets, score `6`) (`d2_star_matched_len_vs_rule_len` -> `blocked`); conversely, `Disallow: /*a*b*` (6 octets) on `/ab` scores `4`, tying `Allow: /ab` (3 octets, score `4`) and losing on tie-break (`d4_wildcards_longer_than_target_path` -> `exposed`).
8. **(d) Trailing `$` stripped before length check**: `Disallow: /a$` (3 octets) and `Allow: /a` (2 octets) both get `len("/a") + 1 = 3`, so `Allow: /a` wins on tie-break (`d3_anchor_dollar_excluded_from_len` -> `exposed`).
9. **(e) Reserved percent-escapes conflated**: `urllib.parse.unquote` + `quote(safe='/')` decodes `%2F` to `/` (`e1_pct2f_decoded_to_slash` -> `blocked`) and encodes literal `:` in URL paths to `%3A` (`e2_reserved_colon_encoded_to_pct3a` -> `blocked`).
10. **(e) Trailing `?` (empty query) preserved**: `_urlsplit` + `_urlunsplit` turns `https://example.com/page?` into `/page?` instead of `/page`, missing `Disallow: /page$` (`e3_trailing_question_empty_query` -> `exposed`).

## Commands Run & Exit Codes

- `timeout 60 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/run_own_manifests.py` -> exit `0`
  - Invoked `robots_audit.py` with no args -> exit `64`
  - Invoked `robots_audit.py --manifest manifests/manifest_g_fault.json` -> exit `2` (`could-not-evaluate`, `input_invalid`)
  - Invoked `robots_audit.py --manifest manifests/manifest_af.json` -> exit `2` (`could-not-evaluate`, `checksEvaluated: 2`)
  - Invoked `robots_audit.py --manifest manifests/manifest_divergences.json` -> exit `1` (`failed-policy`, 12/12 divergence findings)

## Sandbox Directory Listing (`ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1NaiveReader/`)

```
total 28
drwxr-xr-x 3 vgpnk vgpnk    74 Oct 23 00:08 .
drwxr-xr-x 9 vgpnk vgpnk   157 Oct 23 00:07 ..
drwxr-xr-x 2 vgpnk vgpnk  4096 Oct 23 00:09 manifests
-rwxr-xr-x 1 vgpnk vgpnk  8464 Oct 23 00:07 robots_audit.py
-rwxr-xr-x 1 vgpnk vgpnk 10529 Oct 23 00:09 run_own_manifests.py
```
