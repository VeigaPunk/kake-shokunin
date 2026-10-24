# ReopenS133 — S133 continued truth

Axis: **freshness**. Source re-opened at `2026-10-24T03:56:49Z`.

**Named attack verdict: FAIL to falsify S133's quoted sentence. Re-open procedure: PASS.** The exact 15-word sentence remains at [Popen.returncode, paragraph 3](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.returncode). Confidence: high for the fetched response and retained-byte comparison.

## Observed findings

- Live GET: **HTTP 200**, `text/html`, **208,624 bytes**, sha256 **`b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355`**.
- Retained `.ufo/waves/round-45/sources/subprocess.html`: **208,624 bytes**, sha256 **`eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd`**.
- **Page bytes changed**, despite equal byte sizes. The complete diff contains only line 2037: footer `Last updated` changed from `00:13 UTC` to `03:37 UTC`, both on October 24. Both pages still identify themselves as **Python 3.15.1 documentation**. The entire `Popen.returncode` entry is unchanged.
- At HTML anchor `subprocess.Popen.returncode` (line 1184), paragraph 3 in both responses reads exactly: **“A negative value -N indicates that the child was terminated by signal N (POSIX only).”** This is exact visible text after removing inline markup and collapsing HTML whitespace, not a contiguous raw-HTML substring: `<code>` tags and a newline interrupt the raw sentence in both copies. No wording, punctuation, case, or symbol substitution was used.
- Response headers: `last-modified: Sat, 24 Oct 2026 03:40:00 GMT`; `etag: "6adc2890-32ef0"`; `date: Sat, 24 Oct 2026 03:56:49 GMT`; `content-length: 208624`.
- Registry `corpus/SOURCES.md:141` records S133 as `mined`, opened `2026-10-24`, recheck `on-release`. Its retained digest remains accurate for the retained file; it is not the current live-page digest.

## Is an on-release re-open due?

**No missed release-triggered re-open is established.** The advertised version is unchanged (`3.15.1` in both copies). A documentation rebuild/publication is observed, so a freshness re-open was warranted and **has now been performed**; the anchored quote still holds. A digest change alone is not a stale-claim finding: lane `SKILL.md:578-583` explicitly judges living documents by quote at anchor, not sha equality.

**Inference / remaining gap:** `../CORPUS.md:105-106` lists `on-release` as a cadence but does not define whether a same-version documentation rebuild counts as a release. A Python release-history check was not run. Therefore this evidence establishes neither a missed Python release nor a universally satisfied release schedule; it establishes the quoted claim's continued truth at this fetch. No registry or retained-source update was made.

## Exact commands and decisive output

Working directory for every command below: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

### Fetch, status, sizes, and digests

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/ReopenS133 && curl --location --silent --show-error --connect-timeout 20 --max-time 90 --dump-header /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.headers --output /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html --write-out 'HTTP=%{http_code}\nBYTES=%{size_download}\nURL=%{url_effective}\nCONTENT_TYPE=%{content_type}\n' https://docs.python.org/3/library/subprocess.html && sha256sum .ufo/waves/round-45/sources/subprocess.html /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html && wc -c .ufo/waves/round-45/sources/subprocess.html /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html && date -u '+FETCHED_AT=%Y-%m-%dT%H:%M:%SZ'
```

Exit 0; verbatim output:

```text
HTTP=200
BYTES=208624
URL=https://docs.python.org/3/library/subprocess.html
CONTENT_TYPE=text/html
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  .ufo/waves/round-45/sources/subprocess.html
b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355  /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html
208624 .ufo/waves/round-45/sources/subprocess.html
208624 /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html
417248 total
FETCHED_AT=2026-10-24T03:56:49Z
```

### Complete byte-change diff

```sh
diff -u .ufo/waves/round-45/sources/subprocess.html /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html
```

Exit 1 (files differ, not a failed fetch); verbatim output:

```diff
--- .ufo/waves/round-45/sources/subprocess.html	2026-10-24 00:42:33.818156641 -0300
+++ /fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html	2026-10-24 00:56:49.601928113 -0300
@@ -2034,7 +2034,7 @@
 <a href="https://www.python.org/psf/donations/">Please donate.</a>
 <br>
     <br>
-      Last updated on Oct 24, 2026 (00:13 UTC).
+      Last updated on Oct 24, 2026 (03:37 UTC).
     
       <a href="/bugs.html">Found a bug</a>?
     
```

### Located exact-visible-text check

The scratch helper uses Python's standard-library `HTMLParser`, starts at the exact `<dt id="subprocess.Popen.returncode">`, collects only its `<dd>` paragraphs, and compares each paragraph to the complete requested sentence. It additionally prints both byte digests, titles, update footers, raw-substring results, and changed-line positions. It writes nothing.

```sh
python3 -B /fast/scratch/hyaku/kake-r45/ReopenS133/check_source.py
```

Exit 0; verbatim output:

```text
retained: bytes=208624 sha256=eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd
retained: title=subprocess — Subprocess management — Python 3.15.1 documentation
retained: last_updated=Oct 24, 2026 (00:13 UTC).
retained: anchor=subprocess.Popen.returncode line=1184 paragraphs=4
retained: exact_visible_quote_paragraphs=[3]
retained: raw_contiguous_quote=False
retained: paragraph_3=A negative value -N indicates that the child was terminated by signal N (POSIX only).
refetched: bytes=208624 sha256=b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355
refetched: title=subprocess — Subprocess management — Python 3.15.1 documentation
refetched: last_updated=Oct 24, 2026 (03:37 UTC).
refetched: anchor=subprocess.Popen.returncode line=1184 paragraphs=4
refetched: exact_visible_quote_paragraphs=[3]
refetched: raw_contiguous_quote=False
refetched: paragraph_3=A negative value -N indicates that the child was terminated by signal N (POSIX only).
PAGE_BYTES_CHANGED=True
LINE_COUNTS=2048,2048
CHANGED_LINE_NUMBERS=[2037]
QUOTE_AT_ANCHOR=PASS
```

## Scope and written files

Every file written by this seat:

1. Lane report: `.ufo/waves/round-45/w2/ReopenS133.md`.
2. Scratch fetched body: `/fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.html`.
3. Scratch response headers: `/fast/scratch/hyaku/kake-r45/ReopenS133/subprocess.headers`.
4. Scratch analysis helper: `/fast/scratch/hyaku/kake-r45/ReopenS133/check_source.py`.

No other lane file was modified. No installs/updates, builds, test suites, mutations, commits, pushes, or subagent dispatches. LSP was not applicable: this assignment inspected documentary HTML and its literal anchor, not repository symbol definitions or callers.
