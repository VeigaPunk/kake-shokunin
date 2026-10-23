# ReopenS111 — Python urllib.parse (freshness)

Axes: freshness. No packages installed. No counter scored (source reopen, not a control).

Checked: row S111 (`corpus/SOURCES.md:119`), Gate quote (`corpus/lessons/round-40.md:16`), retained `.ufo/waves/round-40/sources/py-urllib-parse.html`, live GET, installed `urlsplit`.

Commands (exit codes):
- `sha256sum` retained HTML → `835af739560025f180c088c39dfae7806f1a5a859fa9f1ab650c8be59ab9ac16`, 119730 bytes, exit 0.
- `curl -fsSL -D …/headers.txt -o …/live-urllib-parse.html https://docs.python.org/3/library/urllib.parse.html` → first write failed exit 23 (sandbox dir missing); retry exit 0. HTTP/2 200, `content-length: 119730`, `last-modified: Fri, 23 Oct 2026 07:36:14 GMT`, `date: Fri, 23 Oct 2026 08:38:34 GMT`. Live sha256 **equal** to retained and to the row.
- `python3` 3.14.8 `urlsplit` probes, exit 0. `geturl()` drops the character: leading space/NUL/`\x1f`/`\x0b`; TAB/CR/LF at start, middle, and end (`http://h/a\tb` → `http://h/ab`). Unchanged: trailing space, interior space, interior NUL, interior VT. `\x7f` is not stripped.

Title in the retained page is “Python 3.15.1 documentation” (`py-urllib-parse.html:20`). The 3.15 note on `urlsplit` is only `missing_as_none` (`:445`), not the strip. Runtime checked is 3.14.8, which already has the 3.10 and 3.12 changes. Stdlib `/usr/lib/python3.14/urllib/parse.py:502-506` is `lstrip` of C0+space then `replace` of TAB/CR/LF; `:87`’s comment says “leading and trailing” but the code does not `rstrip` (matches the docs, not that comment).

## Clauses

- **Quote** (`round-40.md:16`): **holds.** After deleting tags and collapsing whitespace, the 25-word string is an exact substring (`py-urllib-parse.html:400-402`). Raw HTML breaks the line after “C0” and after “`\n,`”; the collapsed sentence matches the Gate.
- **Anchor** (`SOURCES.md:119`): **holds.** The paragraph is inside `urlsplit` (`id="urllib.parse.urlsplit"`, `:252`, body `:400-402`). Its notes are present: 3.10 “ASCII newline and tab characters are stripped from the URL.” (`:439`); 3.12 “Leading WHATWG C0 control and space characters are stripped from the URL.” (`:442`). SHA256 and HTTP 200 match this GET. Other 3.10 notes on the page are `parse_qs`/`parse_qsl`, not “its”.
- **`teaches`, stripping fact:** **holds.** Docs and 3.14.8: TAB/CR/LF anywhere, leading C0 or space, not trailing space and not other interior C0. Scope cell’s “not WHATWG or RFC 3986 conformance” matches the page’s own disclaimer (`:703-707`).
- **`teaches`, “must reject … before splitting (contract sentences 4, 21 and 22)”:** **wrong.** The page says `urlsplit()` does not validate (`:419`). Sentence 21 (`.ufo/waves/round-39/c1-contract.md:60-61`) removes leading and trailing XML whitespace (U+0020/0009/000D/000A) and nothing else; it does not reject them. A leading TAB on `loc` stays clean after that strip (SCORECARD U, `c1_count.py` comment). Citing 21 as a reject, and saying “anywhere” must be rejected before splitting, contradicts sentence 21. Sentences 4 and 22 require an absolute `http`/`https` URL as written; that obligation is the contract plus S102, which S111’s scope excludes.

Live copy: `/fast/scratch/hyaku/kake-r40w1/ReopenS111/live-urllib-parse.html` sha256 `835af739560025f180c088c39dfae7806f1a5a859fa9f1ab650c8be59ab9ac16`.
