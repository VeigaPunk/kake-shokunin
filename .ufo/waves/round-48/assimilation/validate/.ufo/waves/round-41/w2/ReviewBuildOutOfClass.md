# Wave 2 — ReviewBuildOutOfClass: build out-of-class statements

Seat `KakeR41.ReviewBuildOutOfClass`, axis operability. Build `eae5ae2` landed; tool sha256
`0b485431…13edbf` verified equal to worktree; base `8eb121c8` tool sha256 `4de35f8c…1460e` verified.

## Method

`git show 8eb121c8:scripts/sitemap_audit.py > base.py`, `git show eae5ae2:… > build.py` (exit 0; sha256
above). Driver `/fast/scratch/hyaku/kake-r41w2/ReviewBuildOutOfClass/run.py`, Python 3.14.8:
per value, a manifest with `sitemapUrl=https://example.com/s.xml` + `s1.xml` whose `<loc>` is the
value (check `c_loc`), and `sitemapUrl`=value + valid `s2.xml` (check `c_url`). `rej` =
`loc_not_absolute`/`check_invalid`. Oracle column = `c1_count.py`'s logic (abnf 2.9.1 `Rule("URI")`
from the vendored wheel + scheme http/https + authority + non-empty host). Driver run: exit 0, 2.08 s.
A second pass covered whitespace (`<loc>` sentence-21 strip vs unstripped `sitemapUrl`).

## Table (name — base loc/url — build loc/url — RFC 3986 URI+http(s)+host)

| value | base | build | oracle |
|---|---|---|---|
| `hétp://example.com/` (scheme) | rej/rej | rej/rej | invalid |
| `http://é@example.com/` (userinfo) | acc/acc | acc/acc | invalid |
| `http://éxample.com/` (host) | acc/acc | acc/acc | invalid |
| `http://example.com:8é/` (port) | rej/rej | rej/rej | invalid |
| `http://example.com/é` (path) | acc/acc | acc/acc | invalid |
| `http://example.com/?é` (query) | acc/acc | acc/acc | invalid |
| `http://example.com/#é` (fragment) | acc/acc | acc/acc | invalid |
| `…/\U0010ffff`, `…/\x80` | acc/acc | acc/acc | invalid |
| `…/%é0` | acc/acc | rej/rej | invalid |
| `http://[fe80::1%eth0]/` (raw zone) | acc/acc | acc/acc | invalid |
| `http://[fe80::1%25eth0]/` | acc/acc | acc/acc | invalid (no ZoneID in 3986) |
| `http://[v1.fe80]/` lower `v` | acc/acc | acc/acc | valid (IPvFuture) |
| `http://[V1.fe80]/` upper `V` | acc/acc | acc/acc | valid (ABNF literals case-insensitive) |
| `http://[not-ipv6]/`, `[]/`, `[é]/`, `[v]/` | rej/rej | rej/rej | invalid |
| `http://example.com:65535/` | acc/acc | acc/acc | valid |
| `http://example.com:65536/`, `:99999/` | rej/rej | rej/rej | valid (port = *DIGIT) |
| `http://example.com:/` (empty port) | acc/acc | acc/acc | valid |
| `http://h?`, `http://h#`, `http://h`, `http://h/` | acc/acc | acc/acc | valid |
| `http://example.com/a?b#c` | acc/acc | acc/acc | valid |
| `…/a b`, `…/a\x7fb` | acc/acc | rej/rej | invalid |
| `  http://example.com/p  ` | acc loc / rej url | acc loc / rej url | invalid as written |
| `\xa0http://h`, tab, CRLF inner | rej/rej | rej/rej | invalid |

`acc` = judged absolute (findings such as `loc_out_of_scope` follow, never `loc_not_absolute`).

## Differences base → build (all listed)

Only `…/%é0`, `…/a b`, `…/a\x7fb` — exactly the claimed in-class repair (bad percent triplet, space,
DEL). No out-of-class value changed verdict in either direction, as `loc` or as `sitemapUrl`.

## Per checked statement

- **"code points U+0080 and above are still accepted wherever RFC 3986 allows `unreserved`"** — holds:
  userinfo, host, path, query, fragment all accept é/\x80/\U0010ffff identical to base; scheme and
  port reject identically (they can't take unreserved anyway). `%é0`'s change is the claimed
  pct-encoded rule, not non-ASCII drift.
- **"IP-literal contents … still judged by `urlsplit`"** — holds on Python 3.14.8: junk `[not-ipv6]`,
  `[]`, `[é]`, `[v]` are rejected and IPvFuture `[v1.fe80]`/`[V1.fe80]` and both zone-id forms are
  accepted, all identical to base (the build regex's `\[[^\]]*\]` defers to urlsplit's bracket check).
- **"ports above 65535 … judged by `urlsplit`"** — holds: 65536/99999 rejected by both (urlsplit
  `.port` ValueError), though RFC 3986 `port = *DIGIT` and the oracle call them valid; empty port and
  65535 accepted by both.
- **`http://h?`, `http://h#`, `http://h`** — accepted by both, oracle-valid; parity holds.
- **"`loc` after sentence-21 strip; `sitemapUrl` as written"** — holds: outer whitespace on `loc` is
  stripped (accepted) while the same string as `sitemapUrl` is rejected by both; NBSP/inner tab/CRLF
  rejected identically.

## Findings

None actionable in scope. Residual note (informational, severity low): the IP-literal parity relies
on the interpreter — urlsplit's bracketed-host validation exists since Python 3.9.5; on older
interpreters `[not-ipv6]`/`[é]` would pass both tools, still parity, just a different out-of-class
answer. Tooling: no installs needed (abnf 2.9.1 wheel vendored in repo was reused).
