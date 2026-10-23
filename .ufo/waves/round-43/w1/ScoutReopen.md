CHURN: S126's live page differs from the round-42 retention by a five-byte docs-footer clock only; S127 is byte-equal. Both quoted sentences still locate.

Fetched 2026-10-23T19:53:08Z (response `Date`). No tools installed. Scratch: `/fast/scratch/hyaku/kake-r43/kake-r43-w1-ScoutReopen/`.

## Commands (exit codes)

- `timeout 120 curl -fsS -D re.headers -o re.html -w 're_http=%{http_code} re_size=%{size_download}\n' https://docs.python.org/3/library/re.html` → exit 0, `re_http=200`, `re_size=251811`. Header: `HTTP/2 200`, `content-length: 251811`, `last-modified: Fri, 23 Oct 2026 19:42:40 GMT`, `etag: "6adbb8b0-3d7a3"`. No `-L` (no redirect followed).
- `timeout 120 curl -fsS -D rfc.headers -o rfc9844.txt -w 'rfc_http=%{http_code} rfc_size=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9844.txt` → exit 0, `rfc_http=200`, `rfc_size=19292`. Header: `HTTP/2 200`, `content-type: text/plain;charset=utf-8`.
- `sha256sum re.html rfc9844.txt` → exit 0 (hashes below).

## S126 — https://docs.python.org/3/library/re.html

- Status 200. Bytes 251811. Live sha256 `c5771cb13c076a0bf9413c0a9632ff7d3273bc703a889845c4d4eadaa261c231`.
- Retention `.ufo/waves/round-42/sources/docs.python.org_3_library_re.html` sha256 `1559698e711ec65be18bd2a3bae3328206c248fba490633c139617c97a8f17e2` (matches `SHA256SUMS:1`). Same length, not equal.
- Relation: churn-only. One differing line, `re.html:2360`: live `Last updated on Oct 23, 2026 (19:41 UTC).` vs retention `… (09:57 UTC).` (bytes 251557–251562, `19:41` vs `09:57`). Every earlier line is identical. Round-42 reopen (`.ufo/waves/round-42/w2/ReopenPythonRe.md`) recorded etag `"6adb3018-3d7a3"` and `last-modified` 09:59:52 GMT; those header fields moved with the footer.
- Quotes located: yes. `as many times as possible` at `re.html:358`. `do not allow back-tracking when the expression following it fails to match` across `re.html:359-360` (newline between `allow` and `back-tracking`; absent as one raw line; present when whitespace is joined). `are equivalent to` at `re.html:370` (`x*+`, `x++`, `x?+` … `(?>x*)`, `(?>x+)`; `(?>x?)` continues at `re.html:371`; `>` stored as `&gt;`). `Added in version 3.11.` at `re.html:373`, `:408`, `:581` (spans 357–373, 396–408, 569–581 hold). A fourth hit at `:986` is a different feature, same as the round-42 reopen.

## S127 — https://www.rfc-editor.org/rfc/rfc9844.txt

- Status 200. Bytes 19292. Live sha256 `7585b9a9ed2e6d350ac4e79d0bbb722e5ab3d22c93fb2a40ad03d832cdb4b135`.
- Retention `.ufo/waves/round-42/sources/www.rfc-editor.org_rfc_rfc9844.txt` and `SHA256SUMS:6` are that same digest. Byte-equal, including leading BOM `EF BB BF`. 418 newline-lines.
- Quotes located: yes. `This document completely obsoletes [RFC6874]` at `rfc9844.txt:192` (sentence continues through `:194`). `reverts the change that it made to the URI syntax` across `:195-196` (`the` / `URI` split by the newline; absent as one raw line; present when joined). The sentence finishes at `:196-197` with `so [RFC3986] is no longer updated by [RFC6874].` Cited span 192 and 195–197 holds.

## Checked statements

- S126 anchor spans 357–373, 396–408, 569–581 and the three possessive/atomic quotes in `corpus/SOURCES.md:134`: holds (live and retention).
- S126 row hash `1559698e…8f17e2` "bytes equal" at the 12:13:37Z reopen: holds of the retained file; overstated if read as the 19:53Z page (footer clock only).
- S127 obsolescence and syntax-revert quotes and hash `7585b9a9…c4b135` "bytes equal" in `corpus/SOURCES.md:135`: holds. Live bytes equal the retention.
- No quote missing, no substantive sentence change. Not a defect.
