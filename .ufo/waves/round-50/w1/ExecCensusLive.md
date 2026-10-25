# ExecCensusLive — round 50 wave 1 leaf report

Date: 2026-10-24. Seat: leaf (freshness). Scope: run the frozen instruments verbatim, count the live registry, check S286 presence.

## Command outputs (verbatim)

### `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`

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

Exit code: `0` (census passes; the W04 lines are warnings, not failures).

### Live registry row count

`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → **142**

### S286 in live registry

`grep -nE '^ {0,3}\|[[:space:]]*S286' corpus/SOURCES.md` → no match (exit 1). **S286 is NOT in the live registry at this moment.**

## Instrument readings (run verbatim, no reasoning applied)

### C1 quote-class counter

Base revision `9619af67c52939daac502ca7a24c9d714f3f51db` (exit 1):

```
C1 classed 0/3 met=False
  FAIL S273: class ledger absent, lesson absent
  FAIL S274: class ledger absent, lesson absent
  FAIL S286: class ledger absent, retained blob absent, lesson absent, no live registry row, entry absent
```

Pre-append revision `33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` (exit 1):

```
C1 classed 0/3 met=False
  FAIL S273: lesson absent
  FAIL S274: lesson absent
  FAIL S286: lesson absent, no live registry row, entry absent
```

Delta between revisions: at the pre-append revision, the S273/S274 class ledgers now exist (their "class ledger absent" flags cleared) and the S286 retained blob now exists — but the mirror commit did not add a live S286 registry row, the entry, or any lesson. Both revisions still read `met=False`, `0/3`.

### C2 durability counter

Base revision `9619af67c52939daac502ca7a24c9d714f3f51db` (exit 1):

```
C2 durable 0/1 met=False
  FAIL order proof absent
  FAIL wave-cite proof absent
  FAIL LOG.md at measured revision does not cite the wave
  FAIL settlement absent
```

## Findings for the frontier

- C1 remains unmet at both frozen revisions. The gap is uniform: all three declared ids (S273, S274, S286) lack `corpus/lessons/round-50.md` coverage, and S286 additionally lacks a live registry row and a `corpus/SOURCES.md` entry. The pre-append mirror proves the class-ledger and retained-blob bytes exist at `33eec7f` — the residual misses are exactly the lesson file, the live S286 row, and the entry.
- C2 is entirely unmet: no order proof, no wave-cite proof, no LOG.md wave citation at the measured revision, no settlement artifact. All four sub-checks are open work for this wave.
- Live census: 142 registry rows, exit-0 validate with twelve pre-existing W04 duplicate-URL warnings (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127) — none involving the three declared ids.
- S286 has no live registry row, consistent with the C1 counter's `no live registry row` flag at both revisions.
