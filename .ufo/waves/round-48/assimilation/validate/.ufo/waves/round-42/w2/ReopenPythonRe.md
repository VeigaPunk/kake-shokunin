OVERSTATED: S123's page, digest, and syntax quotes hold; `used-by` is not honest, and the Gate does not ground the landed build.

Axes: freshness (live bytes vs the row), quote fidelity, used-by honesty. No tools installed.

## Fetch

`curl -sS -D /fast/scratch/hyaku/kake-r42w2/ReopenPythonRe/re.headers -o /fast/scratch/hyaku/kake-r42w2/ReopenPythonRe/re.html -w … --max-time 60 -L https://docs.python.org/3/library/re.html` at 2026-10-23T12:13:37Z. Exit 0. HTTP/2 200, 0 redirects, `content-type: text/html`, `content-length: 251811`, `last-modified: Fri, 23 Oct 2026 09:59:52 GMT`, `etag: "6adb3018-3d7a3"` (same etag and last-modified as wave-1 `ScoutPythonRe`). Body 251811 bytes, sha256 `1559698e711ec65be18bd2a3bae3328206c248fba490633c139617c97a8f17e2`. Equal to the row's `1559698e…8f17e2`, to `.ufo/waves/round-42/sources/SHA256SUMS`, and to `sources/docs.python.org_3_library_re.html` (byte-identical). Title line 20: Python 3.15.1. `python3 --version` → 3.14.8, exit 0.

## Quotes (whitespace-joined HTML; `>` is `&gt;` in the raw file)

| Claim | Verbatim | Where |
|---|---|---|
| Gate / teaches: "these do not allow back-tracking when the expression following it fails to match" | yes, across a newline (`allow` ends line 359, `back-tracking` starts 360); not one source line. Inside the claimed span 357–373 | holds |
| "Added in version 3.11." on `*+`/`++`/`?+`, `{m,n}+`, `(?>...)` | yes | lines 373, 408, 581 (spans 357–373, 396–408, 569–581 hold). Other "Added in version 3.11." notes at 879 and 986 are different features |
| teaches: possessive quantifiers "match as many repetitions as possible" and then that back-tracking clause | the clause is the `*+` paragraph, which says "as many **times** as possible" (line 358). "as many **repetitions** as possible" is `{m,n}+` (line 397), and that paragraph says "backtracking" with no hyphen (398) | overstated |
| teaches: `` `x*+` equals `(?>x*)` `` | page says "are equivalent to" (line 370), not "equals" | supported as a paraphrase, not verbatim |
| scope: stdlib `re` possessive quantifiers and atomic groups; not a claim that a rewrite keeps judgments | page documents both; it makes no judgment-preservation claim | supported |
| host 3.14.8; syntax since 3.11 | version note plus `python3 --version` | holds |

## Used by this round?

Not by the landed build. `scripts/sitemap_audit.py:76-81` is a byte-table scanner and says possessive quantifiers are not used. The only `*+` bytes in that file are the sub-delim class `()*+` (`:71`, `:119`), not a possessive quantifier. No `++`, `?+`, or `(?>`. The comment cites S124, not S123.

`used-by` is `SCORECARD.md, corpus/lessons/round-42.md` (`SOURCES.md:131`; CORPUS.md:103-108: mined means cited by a path in `used-by`, and `used-by` is knowledge entries or lessons that cite the row).

- `SCORECARD.md`: **wrong**. No `S123`, no `re.html`, no `1559698e`. Lines 3084–3093 and 3101 name possessive quantifiers only as rejected `ExecBuildRegex` (`8a30432d…`, information only, fails H5). The scored build is the byte-table tool.
- `corpus/lessons/round-42.md:19`: the id is cited, so the path is a real citation. The decision "admit — grounds the build technique" is **wrong**. The same lesson rejects that technique (`:43-44`: `ExecBuildRegex` `PASS 0/225` under Python 3.10.22). Wave-1 `w1/ExecBuildRegex.md:6` cites seat `ScoutPythonRe`, not row S123.

sha256 equal: yes. Scope: supported. Teaches: overstated (times/repetitions glued; "equals" is a paraphrase). Gate "grounds the build technique": wrong. `used-by`: not honest.
