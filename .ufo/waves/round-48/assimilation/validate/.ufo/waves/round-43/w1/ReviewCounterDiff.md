CONFORMANT — v4 transform reproduces the frozen counter byte-exactly; run F is well-formed and the claimed trap classes are real; one docstring placement claim is overstated (non-blocking).

Scope: build_v4.py transform applied to c42_count_v3.py; runs A–E / sandbox unchanged; run-F
XML-legality for `loc`; generator bugs that could make a correct tool fail or a wrong tool pass.

## Commands / evidence
- sha256 c43_count_v4.py = 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab (frozen hash — matches SCORECARD).
- Rebuilt via patched build_v4.py (SRC/DST repointed to sandbox) → rebuilt_v4.py sha256 identical; `diff -q` → BYTE_IDENTICAL. Transform is faithful.
- diff -u v3→v4 = 7 hunks: (1) docstring head, (2) "Five→Six equality runs" line, (3) +260-line run-F block before cases_d, (4) shape_t1 body, (5) shape_t2 deleted+replaced (moved into F block) + shape_t3 body, (6) shape_t5 loop, (7) main() runs list + F-branch. Every claimed change appears exactly once.
- ref41 tool (rev 1ef7a0e…, sha 50287ac6…) parsed for port/scope semantics.

## Per-invariant verdicts
- Anchor uniqueness / single-occurrence: HOLDS. Each `assert … in s` + `s.replace(…,1)`; byte-identical rebuild proves no silent over/under-match.
- Runs A–E generators, layout_cases, write_single, RUNNER, Sandbox._limits, Sandbox.run, main accounting (equal/values/ratios/met): byte-unchanged. HOLDS.
- Predicate sentence, RATIO_LIMIT=2.0, REPS=5, refs/shas, sandbox constants: unchanged. HOLDS.
- Run-F `loc` XML-legality: HOLDS. layout_f.urlset escapes via xml_text (unconditional for `&<>"'`; other non-alnum escaped p=0.3 but are XML-legal raw). write_scoped uses fast_xml (`&<>`). CASE_INVARIANT_DEFECTS `"` `\` tab `|` `%` `[` `]` `{` `}` `^` `` ` `` are XML-legal in content. No `&` in any defect list → no raw-`&` hazard. Well-formed for the round-41 ElementTree parser.
- Run-F `sitemapUrl` XML-legality: n/a — sitemapUrl lives in the JSON manifest, not XML; ref41 json.loads it. HOLDS.
- Long-port trap: HOLDS. urlsplit(…):port raises ValueError for ≥100000 (verified) → ref41 check_invalid/loc_not_absolute; zfill in-range (≤065535) parses. A 5-digit-truncating tool diverges → real trap.
- Case-fold pair (foldpair/pairfile, segment_smu): HOLDS. smu path = first value's first segment cased as written; ref41 `_directory_of` compare is case-sensitive → second (lowercase-seg) member = loc_out_of_scope; a fold cache answers in-scope. Deterministic.
- prefix_pair shared-prefix trap: HOLDS. `bad`/`good` share base[:cut] (cut 36–44, base padded ≥50); both in-scope by authority; `bad` carries defect → not_absolute vs `good` clean. Return order randomized.
- T1/T2/T3/T5 additions (with_long_port, scoped t2, block/common/prefix t3, t5 port-smu): deterministic; port insertion placed correctly after authority (first `/`/`?`/`#` boundary; `?`/`#` bodies never precede the path slash).
- main() F wiring: `("F", None)` in runs, `elif key=="F"` calls cases_f+layout_f, `n` from units — counted in equalValues only when equal. Correct.

## Finding (non-blocking)
1. OVERSTATED docstring — c43_count_v4.py:422-424 (`short_url`): defect insert index is
   `rng.randrange(v.find("/")+1, len(v))`. `v.find("/")` is the first `/` of `://`, so the defect
   can land at index 5-7, i.e. inside the scheme/authority boundary (e.g. `hTTp://<host/…`), not
   strictly "after the path start" as documented. Still a deterministic ref41 finding (loc_not_absolute),
   so no wrong-tool-pass — but the advertised placement is wrong; the "case-invariant defect" class
   sometimes lands in the authority rather than the path body. Severity: low.

## Residual risk
- write_single smu derives `https://{values[0].split("/")[2]}/sitemap.xml`; for T3 short_url first-values the loc scheme is rcase'd and may be http while smu is hardcoded https → whole file loc_out_of_scope. Pre-existing v3 behavior (long_value had the same scheme split); deterministic, not a v4 defect — but it means a fraction of T3 files are uniformly out_of_scope regardless of the new classes.
- 240 long-port run-F units all collapse to check_invalid under ref41 (sitemapUrl unparseable), so the block exercises one code path heavily — intended, deterministic.

Verification gap: semantic trace only; the frozen counter was not executed (leaf seat reviews diff, not scores). No file in the lane was mutated; analysis ran in /fast/scratch/hyaku/kake-r43/ReviewCounterDiff/.
