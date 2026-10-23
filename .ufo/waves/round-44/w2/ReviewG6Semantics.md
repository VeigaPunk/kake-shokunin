# ReviewG6Semantics — independent G6 witness-shape derivation (wrong-reason-witness guard)

Axes: operability (the four casememo controls' semantic witness). Freshness: untouched by this item.
Verdict: **FAIL against the item's named attack** — the file at `.ufo/waves/round-44/classes/g6_fold_pairs.py`
does **not** match the derivation; it is the pre-fix wave-1 file (ExecG6Fold's failing attempt, same 50+50
second-segment-marker shape; all 8 of its probes returned `equal:true`). sha256 at my runtime:

```
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  .ufo/waves/round-44/classes/g6_fold_pairs.py
b827ec1cd2b5e2144aa6c14ae3590b7ae6ff17488e9e93a9173b4bb63aea5f54  .ufo/waves/round-44/classes-placebo/g6_fold_pairs.py
```

The derivation below was written before inspecting those bytes, from the four frozen control sources and the
frozen counter layout only; the r43 witness record (`round-43/w1/CtlCaseMemo.md`) and live runs confirm it.

## Derivation

Three facts drive everything:

1. `_uri_ok_scan`/`_scan`/`_path_ok` are **byte-class scanners; every ASCII letter class admits both cases**, so
   `scan(v) == scan(v.lower())` on every input. The *only* fold-collapsible slot where the grammar forbids a
   non-ASCII code point is **inside the IP-literal `[ ]`** (`_TABLE_IP_LITERAL` is built `non_ascii=False`;
   scheme is too, but a folded scheme letter can never produce an http/https ASCII twin, so brackets are the
   only usable slot). A path/query swap therefore can **never** flip a `_uri_ok` verdict.
2. `layout_f` gives each `foldpair`/`pairfile` one file and `sitemapUrl = segment_smu(rng, member1)`: the smu's
   path is member-1's **first** path segment **as written** (`c44_count_v5.py:532-543`). The urlset scope check
   `parsed[3].startswith(directory_of(smu))` is case-sensitive, so only a swap inside the **first** segment can
   move the ref41 finding; a swap in a later segment leaves both members in-scope identically.
3. `len ≥ 2` path segments are needed on member 1: with one segment, `segment_smu` yields `a + "/sitemap.xml"`,
   directory `/x/`, and member 1's own path `/x` fails `startswith` — equal noise on both tools (verified).

### casememo-v3 (`_URI_MEMO[value.lower()] = verdict`, always consulted)
Witness unit: `("foldpair", a, b)` where **member a is the ASCII bracket form** `http://[::1%25k]/seg/tail`
and **member b carries U+212A KELVIN SIGN inside the brackets**: `http://[::1%25K]/seg/tail`.
`b.lower() == a.lower()`; `scan(a)=True` seeds True; `scan(b)=False` is suppressed by the hit.
ref41: `loc_not_absolute` entry 2. v3: clean. Order must be ASCII-first: `segment_smu` copies the bracketed
authority into the smu verbatim, so a K-first smu is itself `check_invalid` (equal on both tools).
U+212A is the only practical lower()→ASCII collapsible char (U+0130 lower()s to a 2-codepoint string; U+017F
does not collapse under lower()).

### casememo-v4 (same memo, consulted only `len(value) <= _MEMO_MAX = 64`)
Identical bracket-zone pair, with the added constraint **both members ≤ 64 code points** — the `len` gate wraps
both the lookup *and the store*, so an over-64 pair neither seeds nor hits. Verified live: the same pair padded
to 79 cp leaves v4 agreeing with ref41 while v3 still diverges.

### casememo-v7 (`_PARSE_MEMO[value.lower()]`, consulted only for non-ASCII values)
Witness unit: `("foldpair", a, b)`, **ASCII member first**, where the swap is in the **first path segment**:
`a = …/segk/x`, `b = …/segK/x` (U+212A). a stores `('http',host,port,'/segk/x')`; b hits the key and is judged
with `/segk/x` — in-scope under smu dir `/segk/` — while ref41 parses `/segK/x` → `loc_out_of_scope` entry 2.
(The r43 Éseg/éseg variant — non-ASCII first member — also works since the first member stores after a miss;
ASCII-first is the canonical form. A bracket-K pair also fires v7/v8, via the stored-tuple hit, but does not
discriminate the mechanism.)

### casememo-v8 (same memo, keyed on `value.casefold()`)
Same first-segment shape; **two markers wanted**: U+212A (casefold→'k', also hits v7) and U+017F long-s
(casefold→'s', lower()→unchanged). The long-s pair is the v8 discriminator: under v7 it is a non-collision and
the control agrees with ref41 — confirmed below. A G6 with only ſ pairs would miss v3/v4/v7; only-K pairs
witness all four but can't prove the casefold() key was exercised.

### Why each memo fires (one line each)
- v3: verdict memo answers True for `…[::1%25K]…` without scanning; the ref41 grammar's `non_ascii=False`
  IP-literal table is the only fold-distinguishing rejection, so the bracket is the only honest carrier.
- v4: same, and the 64-cp gate is the only thing separating it from v3 — an over-64 twin must be *absent* from
  any v4 witness pair.
- v7: tuple memo skips urlsplit+scope for the K-member; only a first-segment case diff changes a finding, and
  only `segment_smu` (foldpair/pairfile units) puts that case into the scope prefix.
- v8: same tuple memo under casefold(); 'ſ'→'ss'/'s' folding reaches keys lower() cannot.

## Landed file vs derivation — **MISMATCH on every axis**
`classes/g6_fold_pairs.py` (sha `f4f13a76…`) emits 100 foldpairs: ASCII member first with `k`/`s` in the
**second** path segment, marker U+212A/U+017F at that same slot in member 2, first segment identical.
- Wrong segment for v7/v8: stored-vs-written paths differ only in a later segment, so `startswith` agrees on
  both tools → clean/clean (the exact wave-1 failure).
- Wrong slot for v3/v4: the marker sits in the path, where the grammar admits non-ASCII — `scan(b)=True`, the
  fold collision is benign → no divergence. The required carrier is the `[ ]` zone id.
- Pair length (<64cp) and ASCII-first order are coincidentally fine, but moot given the position errors.

## Decisive output (verbatim, trimmed at 300 cols)
Manifests built in scratch `ReviewG6Semantics/`; ref41 extracted from
`git show 1ef7a0e9…:scripts/sitemap_audit.py` → sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (== REF41_SHA).

```
$ python3 -B <tool> --manifest <m>.json   # m ∈ {w34,w34long,w78,w78s,landed}
===== w34        (a=[::1%25k]/x/y, b=[::1%25K]/x/y, smu=[::1%25k]/x/sitemap.xml, len 20)
ref41      : {"findings": [{"code": "loc_not_absolute", "entry": 2}]}
casememo-v3: clean
casememo-v4: clean
casememo-v7: clean
casememo-v8: clean
===== w34long    (same pair, 79 cp — over the v4 cap)
ref41      : {"findings": [{"code": "loc_not_absolute", "entry": 2}]}
casememo-v3: clean            <- still diverges
casememo-v4: {"findings": [{"code": "loc_not_absolute", "entry": 2}]}   <- agrees: gate works
casememo-v7: clean
casememo-v8: clean
===== w78        (a=…/segk/x, b=…/segK/x, smu=…/segk/sitemap.xml)
ref41      : {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}
casememo-v3: {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}   <- agrees: verdict memo case-neutral
casememo-v4: {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}
casememo-v7: clean            <- stored /segk/x path judged in-scope
casememo-v8: clean
===== w78s       (a=…/segs/y, b=…/segſ/y, smu=…/segs/sitemap.xml)
ref41      : {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}
casememo-v3: {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}
casememo-v4: {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}
casememo-v7: {"findings": [{"code": "loc_out_of_scope", "entry": 2}]}   <- lower() no-collision
casememo-v8: clean            <- casefold() collision only
===== landed     (the g6 file's own shape: marker in second segment)
ref41 / v3 / v4 / v7 / v8 : clean  (all five agree — witnesses nothing)
```

Direct-function check (same scratch):
`v3._uri_ok_scan("http://[::1%25K]/x")` → False, `_uri_ok_scan("http://[::1%25k]/x")` → True;
after `_uri_ok(K-form)=False?` — no: ASCII-first seeds True, `_uri_ok(K-form)` then returns True (memo hit).
`v7._parse_url("…/segK/x")` → `('http','h.example.com',80,'/segk/x')` (stored tuple); `_parse_url_scan` would
return `/segK/x`. `v7._parse_url("…/segſ/x")` → `/segſ/x` (miss); `v8._parse_url("…/segſ/x")` → `/segs/x` (hit).

## Wrong-reason-witness guard for the L1 (what the landed fix MUST show)
- ≥1 foldpair `scheme://[…%25k]/seg/tail` then `scheme://[…%25K]/seg/tail` (U+212A **inside** the brackets),
  both members **≤ 64 code points**, ASCII member first, member 1 with ≥ 2 path segments.
- ≥1 foldpair with the swap in the **first** path segment: `…/segk/…` then `…/segK/…` (K, hits v7+v8).
- ≥1 foldpair `…/segs/…` then `…/segſ/…` (U+017F, hits v8 only — the casefold discriminator).
- If the landed file instead only moves the same markers into the first segment, v3/v4 stay unwitnessed; if it
  only adds bracket pairs without first-segment pairs, v7/v8's documented scope mechanism is unexercised
  (bracket pairs do flip their *findings*, but a reviewer should demand both).

## Files written
- `.ufo/waves/round-44/w2/ReviewG6Semantics.md` (this report)
- `/fast/scratch/hyaku/kake-r44/ReviewG6Semantics/` — `ref41.py`, `exp.py`, `exp78.py`, `w34.*`, `w34long.*`,
  `w78.*`, `w78s.*`, `landed.*` manifests (scratch only)

No tools installed. Frozen files read-only; lane file `classes/g6_fold_pairs.py` not edited (reviewer seat).
Report: .ufo/waves/round-44/w2/ReviewG6Semantics.md
