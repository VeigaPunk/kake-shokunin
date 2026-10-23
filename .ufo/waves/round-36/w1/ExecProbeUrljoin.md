# ExecProbeUrljoin — round 36, wave 1

Seat `KakeR36.ExecProbeUrljoin`; axes operability/freshness; milestone r36-build.
Hypothesis: "`urllib.parse.urljoin` gives the RFC 3986 section 5.4 results for every normal and
abnormal example". No sealed key opened; nothing under `/fast/scratch/hyaku/kake-r36/` read or
searched; no network fetch (item names no URL) — table from the retained S089 body in the lane.

**Verdict: false as stated, but only one table row fails and that failure is RFC-blessed.**
`urljoin` reproduces every 5.4.1/5.4.2 example except `http:g`, where it returns the RFC's
*backward-compatibility* answer rather than its *strict* answer (5.4.2 prints both). All other
divergences are **outside** the 5.4 table and bite the C1 bullet-(b) rule ("resolved ... by
RFC 3986 section 5.2").

Table source `.ufo/waves/round-36/sources/S089.html.gz`: the `.txt` twin flattens the table onto
one line with padded spaces inside the quoted targets (`" g" = " http://a/b/c/g "`), so expectations
come from the HTML body where each `= "..."` is on its own line. Base for every row
`http://a/b/c/d;p?q`; 42 rows (23 normal + 19 abnormal) + 20 extra probes = 62.

```
$ timeout 120 python3 -B probe_urljoin.py ; echo EXIT=$?
TABLE+EXTRA rows: 62
urljoin mismatches: 5
  MISMATCH[divergence] base='http://a/b/c/d;p?q' ref='//host/a/../b' expected='http://host/b' urljoin='http://host/a/../b'
  MISMATCH[divergence] base='http://a/b/c/d;p?q#f' ref='' expected='http://a/b/c/d;p?q' urljoin='http://a/b/c/d;p?q#f'
  MISMATCH[divergence] base='http://a/b/c/d;p;q' ref='g:h/../x' expected='g:/x' urljoin='g:h/../x'
  MISMATCH[divergence] base='http://a/b/c/d;p;q' ref='g:h/./x' expected='g:h/x' urljoin='g:h/./x'
  MISMATCH[divergence] base='http://a/b/c/d;p;q' ref='HTTP:g' expected='HTTP:g' urljoin='http://a/b/c/g'
resolver mismatches: 0
EXIT=1
```

The single table-row divergence, same run: `OK 'http:g' expected='http:g' urljoin='http://a/b/c/g'
resolver='http:g'`. RFC 3986 5.4.2 prints `"http:g" = "http:g" ; for strict parsers /
" http://a/b/c/g " ; for backward compatibility` — `urljoin` takes the second. The other 41 rows
match byte for byte, including every abnormal one (`../../../g`, `../../../../g`, `/./g`, `/../g`,
`g.`, `.g`, `g..`, `..g`, `./../g`, `./g/.`, `g/./h`, `g/../h`, `g;x=1/./y`, `g;x=1/../y`,
`g?y/./x`, `g?y/../x`, `g#s/./x`, `g#s/../x`). The assignment's extra probes (https base
`https://a/b/c/d;p?q`) all agree: `//host/path`→`https://host/path`; `?q`→`https://a/b/c/d;p?q`;
`../../../../g`,`../../../../../g`→`https://a/g`; `""`→`https://a/b/c/d;p?q`; `..`→`https://a/b/`.

**Resolver** `/fast/scratch/hyaku/kake-r36w1/ExecProbeUrljoin/rfc3986_resolve.py` — 47 lines (34 code;
docstring 1-7), stdlib `re` only, sha256 `b71f7d6c825461854fff4fcb1c4bde255a4e0a838f6e4fa38284bf945269d87c`.
5.2.2 `resolve` (line 40), 5.2.4 `rds` (15), 5.2.3 `merge` (30), 5.3 `compose` (34); `strict=True`
keeps a reference scheme equal to the base scheme (strict column), `strict=False` the other.
Passes **all 62 rows** (`resolver mismatches: 0`, `RES-BAD` count 0) plus both RFC 5.2.4 worked
examples (`rds("/a/b/c/./../../g")=="/a/g"`, `rds("mid/content=5/../6")=="mid/6"`).

Cross-check with `rfc3986` 2.0.0 (PyPI via `uv` into a seat-local venv: `uv venv .venv` +
`uv pip install --python .venv/bin/python rfc3986`; CPython 3.15.0 in venv; no system package
touched, no `pacman` call, no service restart, no downgrade):

```
$ timeout 120 .venv/bin/python -B cross_check.py ; echo EXIT=$?
BAD  'http:g'  expected='http:g'  mine='http:g'  lib='http://a/b/c/g'  urljoin='http://a/b/c/g'
table rows: 42   rows where mine!=expected or lib!=expected: 1
EXIT=0
```

The library is non-strict so it also lands on `http:g`'s backward-compat answer; it agrees with the
resolver on the other 41 rows. A 336-case sweep (6 bases × 56 refs) gave `urljoin==resolver: 283`,
`resolver==rfc3986 lib: 315`, all three equal 279 — every difference is one of the five classes:

1. **Authority-relative ref not dot-cleaned.** `//host/a/../b` → `urljoin` `http://host/a/../b`,
   RFC `http://host/b`. `urljoin` splits the netloc off and never dot-cleans the rest
   (`/usr/lib/python3.14/urllib/parse.py`, `urljoin`, the `if netloc:` branch returns
   `_urlunsplit(...)` with `path` untouched); RFC 5.2.2 requires `remove_dot_segments` there.
   Redirect-relevant: `Location: //cdn.example/x/../y` → `https://cdn.example/x/../y` under
   `urljoin`, `https://cdn.example/y` under RFC 3986.
2. **Base fragment inherited on an empty ref.** base `http://a/b/c/d;p?q#f`, ref `""` → `urljoin`
   keeps `#f`; RFC 5.2.2 sets `T.fragment = R.fragment`, undefined for an empty ref, so no
   fragment. (S088 10.2.2 HTTP fragment inheritance is a different layer, out of C1 scope.)
3. **Ref with its own scheme not dot-cleaned.** `g:h/../x` → `urljoin` `g:h/../x`, RFC `g:/x`;
   `g:h/./x` → `urljoin` `g:h/./x`, RFC `g:h/x`. 5.2.2's `defined(R.scheme)` branch still calls
   `remove_dot_segments(R.path)`; `urljoin` returns the ref verbatim when the scheme differs.
4. **Scheme case lost.** `HTTP:g` → `urljoin` `http://a/b/c/g`; RFC strict `HTTP:g`. `urljoin`
   lower-cases at split time; `rfc3986` agrees with the resolver here.
5. **Same-scheme short ref takes the non-strict branch.** `http:g` → `urljoin` `http://a/b/c/g`;
   RFC 5.4.2 strict `http:g`. RFC-sanctioned, but a *choice*.

Classes 1, 3, 4 are **silent**: `urljoin` returns a plausible well-formed URL, no exception, so a
tool built on it would report a wrong `moved` target with no signal. Chain simulation (C1
bullet-(b) shape: each `location` resolved against the URL that hop answered — check `url` for
hop 1, then the previously resolved location; 6 chains, 22 hops) differs in exactly 2 hops:

```
$ timeout 120 python3 -B chain_sim.py ; echo EXIT=$?
DIFF base='https://example.com/a/b' loc='//cdn.example/x/../y' urljoin='https://cdn.example/x/../y' resolver='https://cdn.example/y'
DIFF base='https://example.com/a/b' loc='https:rel'            urljoin='https://example.com/a/rel'      resolver='https:rel'
EXIT=0
```

**Answer, plainly.** Mismatch list for `urljoin` vs the RFC 3986 5.4 table: **one row, `http:g`**
(`urljoin`→`http://a/b/c/g`; RFC strict→`http:g`; RFC also sanctions `urljoin`'s answer as the
backward-compatible column); the other 41 rows match. The resolver passes every example, 62/62
rows including all 42 table rows.

**C1 relevance (advisory for the L1, not a verdict).** `urljoin` is not an RFC 3986 5.2 resolver:
it passes the 5.4 table, so a table-only spot-check would not catch it, yet it diverges on
authority-relative dot segments, on refs carrying their own scheme, and on scheme case. A tool
using `urljoin` would fail a sealed case with `Location: //host/x/../y` or `Location: https:rel`.
`rfc3986_resolve.py` is a drop-in replacement satisfying the contract wording; advisory only.

**Files** (seat sandbox; only this report written to the lane) under
`/fast/scratch/hyaku/kake-r36w1/ExecProbeUrljoin/`: `rfc3986_resolve.py` (`b71f7d6c…269d87c`) ·
`probe_urljoin.py` (`1e84f53b…09d504`) · `cross_check.py` (`89bbaa43…d545f`) · `sweep.py`
(`389f0c5d…d96f`) · `divergence_oracle.py`, `chain_sim.py`; transcripts `out_probe.txt`,
`out_cross.txt`, `out_sweep.txt`, `out_chain.txt`.

**Commands / exit codes.** `timeout 120 python3 -B probe_urljoin.py` → 1 (non-zero = urljoin
mismatches found, by design) · `timeout 120 .venv/bin/python -B cross_check.py` → 0 ·
`timeout 120 .venv/bin/python -B sweep.py` → 0 · `timeout 120 python3 -B chain_sim.py` → 0 ·
`timeout 60 python3 -B -c "<rds worked-example check>"` → 0. System CPython 3.14.8
(`/usr/lib/python3.14/urllib/parse.py`); venv CPython 3.15.0.

**Risks / not verified.** (a) Not verified against the sealed cases — no key, counter not run;
whether any sealed case exercises classes 1/3/4/5 is unknown. (b) `http:g` strict-vs-non-strict
is a contract ambiguity, not a bug: C1 says "RFC 3986 section 5.2" and 5.2.2 offers both
readings, and the L1's reference may pick either; resolver defaults to `strict=True`.
(c) `rfc3986` 2.0.0 is non-strict, so it cannot settle `http:g`; used only as an independent check
on the other 41 rows. (d) `g:h/../x` is the one row where resolver and `rfc3986` differ (resolver
`g:/x`, library `g:x`); I hand-traced RFC 5.2.4 step by step against the retained text and kept
the RFC-literal answer — the library's segment-stack variant differs on a rootless path. Not in
the 5.4 table, so the table verdict is unaffected, but it is an unresolved interpretation
difference worth the L1's attention if rootless-scheme refs ever appear. (e) No system-wide tool
install: `rfc3986` 2.0.0 came from PyPI via `uv` into a seat-local venv.
