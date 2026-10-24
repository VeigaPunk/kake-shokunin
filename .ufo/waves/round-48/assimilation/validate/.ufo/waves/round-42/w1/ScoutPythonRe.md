# ScoutPythonRe — Python `re` possessive quantifiers and atomic groups

Axes: freshness (docs date and version vs host), quote fidelity, SOURCES-row fit. No tools installed. SOURCES.md not edited (draft only).

## Fetch

- GET `https://docs.python.org/3/library/re.html` at 2026-10-23T11:14:27Z. HTTP/2 200, no redirect (`url_effective` same). `content-type: text/html`, `content-length: 251811`, `last-modified: Fri, 23 Oct 2026 09:59:52 GMT`, `etag: "6adb3018-3d7a3"`.
- Body sha256 `1559698e711ec65be18bd2a3bae3328206c248fba490633c139617c97a8f17e2` (251811 bytes, identity encoding). Retained at `/fast/scratch/hyaku/kake-r42w1/ScoutPythonRe/re.html`.
- Title (line 20): `re — Regular expression operations — Python 3.15.1 documentation`. Nav: `3.15.1 Documentation`. RST: `https://github.com/python/cpython/blob/3.15/Doc/library/re.rst`.

## Host

- `python3 --version` → `Python 3.14.8` (main, Oct 2 2026). Exit 0.
- `python3 -c "import re; print(re.compile('a*+').pattern)"` → `a*+`. Exit 0. Extra: `a*+` `fullmatch('aaaa')` is `None`; `a*` matches. Host is older than the 3.15.1 page and newer than the 3.11 addition.

## Located quotes (≤25 words), section `#regular-expression-syntax`

1. `*+`, `++`, `?+` (lines 357–373): "However, unlike the true greedy quantifiers, these do not allow back-tracking when the expression following it fails to match." (19). "These are known as possessive quantifiers." (6). "`x*+`, `x++` and `x?+` are equivalent to `(?>x*)`, `(?>x+)` and `(?>x?)` correspondingly." (12). Then "Added in version 3.11." (line 373).
2. `{m,n}+` (lines 396–408): "This is the possessive version of the quantifier above." (8). "Added in version 3.11." (line 408). Spelling here is "backtracking" (line 398), not the hyphenated "back-tracking" of quote 1.
3. `(?>...)` (lines 569–581): "once exited, the expression, known as an atomic group, has thrown away all stack points within itself." (17). "Added in version 3.11." (line 581).

Other "3.11" notes on this same page are not these features: line 528 (inline flags, changed), line 879 (`-` added to `__all__`), line 986 (`re.NOFLAG`).

## Draft SOURCES row (not inserted; next free id S120)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S120 | Python 3.15.1 documentation: re — Regular expression operations — https://docs.python.org/3/library/re.html | docs | A | Possessive quantifiers `*+` `++` `?+` `{m,n}+` and atomic group `(?>...)` in the standard-library `re` syntax; not a claim that a rewrite preserves round-41 URL judgments | `#regular-expression-syntax` `*+`/`++`/`?+` (lines 357–373), `{m,n}+` (396–408), `(?>...)` (569–581), each "Added in version 3.11."; title Python 3.15.1; fetched 2026-10-23T11:14:27Z, HTTP 200, 251811 bytes, SHA256 `1559698e711ec65be18bd2a3bae3328206c248fba490633c139617c97a8f17e2`, last-modified 2026-10-23T09:59:52Z | Possessive quantifiers match as many times as possible and do not backtrack when the following expression fails; `x*+` equals `(?>x*)`; an atomic group discards its stack points on exit; all three forms were added in 3.11 and are still documented on the 3.15.1 page | queued | 2026-10-23 | on-release | — |

## Checked statements

- The live `/3/library/re.html` page documents `*+`, `++`, `?+`, `{m,n}+` and `(?>...)` with "Added in version 3.11." — holds.
- That page is current 3.15.1 docs (last-modified the same UTC day as the fetch), not a frozen 3.11 snapshot — holds. Calling the page "the 3.11 docs" would be wrong.
- Host `re.compile('a*+')` works — holds on Python 3.14.8. Not checked: whether 3.15.1 changed matching vs 3.14.8.
