# Round 50 wave 1 — ExecCensusMirror

Leaf seat report. Read-only execution; no file mutated.

## Frozen counting instruments (run verbatim)

### C1 quote_class @ base 9619af67c52939daac502ca7a24c9d714f3f51db

```
C1 classed 0/3 met=False
  FAIL S273: class ledger absent, lesson absent
  FAIL S274: class ledger absent, lesson absent
  FAIL S286: class ledger absent, retained blob absent, lesson absent, no live registry row, entry absent
```
Exit code: 1

### C1 quote_class @ pre-append 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1

```
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
```
Exit code: 1

### C2 durable @ base 9619af67c52939daac502ca7a24c9d714f3f51db

```
C2 durable 0/1 met=False
  FAIL order proof absent
  FAIL wave-cite proof absent
  FAIL LOG.md at measured revision does not cite the wave
  FAIL settlement absent
```
Exit code: 1

## Census runs

### 1) Mirror (pre-append assimilation)

Command:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md`

Full stdout:

```
file	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
file	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
file	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
file	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
file	W04	S110 duplicate url www.w3.org/TR/xml across scopes
file	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
file	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md
```

Exit code: **0**

### 2) Lane tip (kake via --root)

Command:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`

Full stdout:

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

Exit code: **0**

## Findings the mirror introduces beyond the lane tip

**None.** The two runs emit the identical 12 W04 rows (same IDs, same URLs, same order — only the lane label `file`/`kake` and the final `ok` path differ). `diff` between the mirror and the live `corpus/SOURCES.md` shows exactly one added line — the S286 registry row at line 151:

```
| S286 | Google for Developers — Troubleshoot Google Search crawling errors — https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors | docs | A | ... | mined | 2026-10-24 | 180d | corpus/knowledge/crawl-error-status-table.md |
```

That appended row produces zero new E or W findings: no duplicate id, no duplicate URL+scope, valid tier/kind/status, past opened date, valid `180d` recheck cadence. The pre-existing W04 set (cross-scope URL duplication) is unchanged and is a warning class that does not affect the `ok` verdict.

## E03 / E04 status

**Neither E03 nor E04 appears** in the mirror run (nor in the lane-tip run). No E-code of any kind is present — the mirror validates clean with warnings only (exit 0).

Report: .ufo/waves/round-50/w1/ExecCensusMirror.md
