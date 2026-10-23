# ProbeUrlsplit — R38 w1, ASCII × urlsplit × base tool (af43a50f)

Hypothesis tested: `urllib.parse.urlsplit` silently removes tab/CR/LF anywhere, strips leading
C0 controls and spaces, and every other ASCII character outside RFC 3986 passes unchanged.

Verdict: **confirmed**, with three corrections that matter to the build:
1. The strip is **leading only** (`parse.py:502` comment "Only lstrip url ... would strip both").
   A space or NUL at the *end* of the URL stays in `parts.path` (e.g. `http://h.example/a ` →
   path `"/a "`), so trailing controls/spaces are not silently removed.
2. `?` and `#` are not "kept unchanged": they delimit. In the path they move the character into
   `query`/`fragment`; at the end of the URL they consume themselves into an empty component.
3. `[` and `]` raise `ValueError: Invalid IPv6 URL` only in the **netloc**; in path/query they are
   kept without error.

## Method (sandbox only: /fast/scratch/hyaku/kake-r38w1/ProbeUrlsplit)
- Base tool: checkout 2dab7f31.., `scripts/robots_audit.py` sha256 `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`
  (same hash as the lane file), Python 3.14.8, `/usr/lib/python3.14/urllib/parse.py:89,92,502-506`.
- 128 ASCII chars × 3 assigned positions + 2 supplementary = **640 rows**:
  `start` = `<ch>http://h.example/a`; `middle` = `http://h.example/a<ch>z`;
  `end` = `http://h.example/a<ch>` (the URL named in the assignment);
  `host` = `http://h.exam<ch>ple/a`; `query` = `http://h.example/a?q=1<ch>`.
- Each row ran the real CLI on its own one-check manifest: `robotsStatus 200`, `userAgent probe`,
  `robots.txt` = `User-agent: *` / `Disallow: /a`, `expect allow`. Row dirs: `rows/<position>/<code>/`.
- `timeout 600 python3 probe_table.py` → exit 0, 640 rows in 1.55 s wall.
- Note on reading the base verdict: `Disallow: /a` is a prefix rule, so every *evaluated* row is
  `blocked`. The discriminators are `reason=check_invalid` + `checksEvaluated 0` (URL rejected)
  versus `blocked` + `checksEvaluated 1` (URL accepted and evaluated) versus `clean`.

## Table summary — what urlsplit does
| class | chars | where |
|---|---|---|
| dropped anywhere | 0x09 `\t`, 0x0a `\n`, 0x0d `\r` | start, middle, end, host, query (removed from the whole URL before splitting) |
| stripped, leading only | 0x00–0x1f and 0x20 space (33 chars) | vanish at `start` (`url.lstrip`); kept at middle/end/host/query |
| kept raw in path | 123/128 at `middle`, 123/128 at `end` | includes NUL, space, `"`, `<`, `>`, `\`, `^`, `` ` ``, `{`, `\|`, `}`, DEL |
| moved | `?` → query, `#` → fragment (middle); both consumed at end | `host`: `/`, `?`, `#` shorten the netloc |
| raises | `[` 0x5b, `]` 0x5d in netloc only | `ValueError: Invalid IPv6 URL`; base → check_invalid |
| non-ASCII (control) | U+00E9 kept in path; base accepts; `normalize` → `%C3%A9` | confirms kept + rule (e) encoding |

`normalize()` changed none of the 640 paths (no valid `%xx` sequences were generated), so raw
control/punctuation bytes reach rule matching unchanged: `middle 0x00` → path `'/a\x00z'`,
normalized `'/a\x00z'`.

## Base-tool verdict per class (af43a50f)
- **middle**: 128/128 accepted and evaluated (`failed-policy`, exit 1, `blocked`, evaluated 1).
- **end**: 128/128 accepted and evaluated (same). Includes NUL (`path '/a\x00'`), space
  (`'/a '`), DEL, `"`, `\`, `|`.
- **query**: 128/128 accepted and evaluated.
- **start**: 33 stripped chars accepted and evaluated; 95 → `check_invalid` (exit 2, evaluated 0)
  because `parse_http_url` sees scheme `''`/`<ch>http` instead of `http`.
- **host**: 123 accepted (NUL, space, `"`, `<`, `>`, `\`, `^`, backtick, `{`, `|`, `}`, DEL in the
  hostname all pass `parse_http_url`), 3 accepted-clean (structural `/`, `?`, `#`), 2 check_invalid
  (`[`, `]`).
- **Outside RFC 3986 (43 chars: 0x00–0x20, 0x22, 0x3c, 0x3e, 0x5c, 0x5e, 0x60, 0x7b–0x7d, 0x7f)**:
  **43/43 accepted at middle, end, host and query; 33/43 at start.** The base tool has no ASCII
  character validation at all; only `urlsplit`'s own lstrip/remove and the `[`/`]` netloc error
  ever reject anything. This is the hole rules (i) and (h) must close.

Concrete counterexamples (evidence rows, base exit 1 `blocked`, `checksEvaluated 1`):
- `rows/end/000/manifest.json` URL `http://h.example/a\u0000` → tool path `'/a\x00'`.
- `rows/middle/092/manifest.json` URL `http://h.example/a\z` → tool path `'/a\\z'`.
- `rows/host/000/manifest.json` URL `http://h.exam\u0000ple/a` → hostname `h.exam\x00ple`.
- `rows/host/032/manifest.json` URL `http://h.exam ple/a` → hostname `h.exam ple`.

## Advisory for the implementer (not a verdict)
- Rule (i) must scan the raw `url` string before `urlsplit`; after `urlsplit` the stripped
  leading 33 chars and removed tab/CR/LF are unrecoverable.
- Rule (i)'s RFC set admits `[ ]` in path/query; only netloc raises today, so (i) must not reject
  `[`/`]` in a path while keeping today's check_invalid for bracketed hosts.
- Prefix `Disallow: /a` cannot distinguish `/a\x00` from `/a`; reveal the character with `/a$`.

## Evidence
- `/fast/scratch/hyaku/kake-r38w1/ProbeUrlsplit/table.json` sha256 `f733964776e6b3a31c1844b4a3844c3fd2cfa52a9bff967ebe3326fd0077b3c4` (640 rows, raw components + CLI report)
- `.../summary.json` sha256 `238216b937112258e2f9eeac888b8053faa9279bddb20041e847ed9034ad055d` (128-row per-char matrix)
- `.../probe_table.py` sha256 `a1b419e73e5b87791e6db006284153fb7dc60fc7a909f07d3863072308caea68`
- stdlib: `/usr/lib/python3.14/urllib/parse.py:89` C0 set, `:92` tab/CR/LF list, `:502-506` lstrip+replace.

## Not verified
- R38 sealed cases/counters not run, not looked for (no key; sealed trees untouched); round-37
  counter (424aa248) and `robots_audit_selftest.py` not run (no build to gate). No tools installed.
