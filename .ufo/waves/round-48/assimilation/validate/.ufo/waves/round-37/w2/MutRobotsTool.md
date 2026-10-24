# MutRobotsTool — round 37, wave 2
Axes: **operability** (scored); freshness (lane context only). Attack: single-point contract defects in the landed robots tool versus both behavioral detectors.
Pinned tool: `9dbc88bb:scripts/robots_audit.py`, byte-identical at `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`. No lane source/index changes; no network; no tools installed.
Let `S=/fast/scratch/hyaku/kake-r37w2/MutRobotsTool`; evidence paths below are relative to S. Each mutant changes exactly one source line; contract sentence anchors and exact old/new bytes: `mutants.json:1`, `mutations.patch:1`; retained tested sources: `mutated-bytes/Mxx.py`.
Before/restored SHA-256 (all 42 targets): `5eb767ec68a649145102619ed13754428bef489e432ed50eb20e9e50542cabae`. Every distinct mutant SHA-256 is in `mutants.json` and its detector receipts; actual restored hashes are in `evidence/restored/Mxx.{sealed,selftest}.json`.
Expected detectors: sealed kills iff <25/28 (exit 1); selftest kills iff <131/131 (exit 1). Table survival uses these declared predicates, not an invented perfect-sealed threshold; all other table exits are 0.
All 42 pristine and all 42 restored targets: sealed 28/28, selftest 131/131, every exit 0. Thus no baseline failures/inconclusive mutants. 252 controlled detector runs; zero timeouts; all child processes reaped.
Exact orchestration commands (cwd S; each exited 0; 180-second deadline per child, one sealed and one selftest concurrently, process ceiling 8):
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/MutRobotsTool/tmp timeout --kill-after=10s 900s python3 -B run_probe.py pristine` → 0.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/MutRobotsTool/tmp timeout --kill-after=10s 900s python3 -B run_probe.py mutated` → 0 (individual detector failures below).
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/MutRobotsTool/tmp timeout --kill-after=10s 900s python3 -B run_probe.py restored` → 0.
Actual child argv, exit codes, stdout/stderr and SHA-256s: `evidence/{pristine,mutated,restored}/Mxx.{sealed,selftest}.{json,stdout,stderr}`; full summaries: each `summary.json:1`. Child commands are the unchanged sealed counter (`--root S/clone --tool-file TARGET --key-revision 424aa248`) and `python3 -B scripts/robots_audit_selftest.py --tool TARGET`.
Counter SHA-256: `2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3`; selftest SHA-256: `0c5b1131afd25dc6052205fd6952f6c39a9500d0a259a091ab6368a7fb25e80f`. Key pin: `93ad9ee64db63b661b408e678f2c6f3d665b7f5c88ef1f977433dbceee8c0a90`.

| Mutant · change (contract; tool line) | Sealed passed | Selftest passed | Survived which |
|---|---:|---:|---|
| M01 · Read byte 512001 too (b; L85) | 28/28 | 130/131 | sealed |
| M02 · Stop at byte 511999 (b; L85) | 28/28 | 130/131 | sealed |
| M03 · Keep leading BOM (b; L169) | 24/28 | 130/131 | neither |
| M04 · Drop invalid UTF-8 bytes (b; L171) | 28/28 | 131/131 | both |
| M05 · LF-only line endings (b; L104) | 24/28 | 129/131 | neither |
| M06 · Comment starts at last hash (b; L179) | 28/28 | 130/131 | sealed |
| M07 · Trim Unicode whitespace in keys (b; L185) | 28/28 | 130/131 | sealed |
| M08 · Trim Unicode whitespace in values (b; L186) | 28/28 | 130/131 | sealed |
| M09 · Unicode rather than ASCII casefold (c; L120) | 28/28 | 129/131 | sealed |
| M10 · Never merge adjacent agent names (c; L188) | 24/28 | 129/131 | neither |
| M11 · Substring user-agent matching (c; L257) | 28/28 | 130/131 | sealed |
| M12 · Keep only last exact-match group (c; L259) | 24/28 | 130/131 | neither |
| M13 · Always include wildcard groups (c; L262) | 24/28 | 129/131 | neither |
| M14 · Only first wildcard group (c; L263) | 28/28 | 131/131 | both |
| M15 · Empty exact group falls back to star (c; L258) | 28/28 | 131/131 | both |
| M16 · Empty rules match (d; L201) | 24/28 | 129/131 | neither |
| M17 · Star requires at least one character (d; L283) | 28/28 | 129/131 | sealed |
| M18 · Trailing dollar loses anchor semantics (d; L226) | 20/28 | 125/131 | neither |
| M19 · Literal rules match anywhere (d; L291) | 28/28 | 130/131 | sealed |
| M20 · Specificity excludes star and dollar (d; L225) | 26/28 | 130/131 | sealed |
| M21 · Last matching rule wins equal-length tie (d; L303) | 26/28 | 129/131 | sealed |
| M22 · No matching rule denies (d; L297) | 4/28 | 110/131 | neither |
| M23 · Omit query from path (e; L448) | 20/28 | 130/131 | neither |
| M24 · Empty URL path stays empty (e; L447) | 24/28 | 130/131 | neither |
| M25 · Include URL fragment (e; L450) | 24/28 | 130/131 | neither |
| M26 · Remove implicit robots.txt allow (e; L517) | 24/28 | 130/131 | neither |
| M27 · Decode reserved escaped slash (e; L144) | 24/28 | 130/131 | neither |
| M28 · Do not decode unreserved escapes (e; L144) | 24/28 | 128/131 | neither |
| M29 · Preserve escaped hex letter case (e; L147) | 24/28 | 129/131 | neither |
| M30 · Use Latin-1 rather than UTF-8 octets (e; L155) | 24/28 | 127/131 | neither |
| M31 · Reject valid status 599 (f; L480) | 27/28 | 130/131 | sealed |
| M32 · Accept float status (f; L479) | 28/28 | 130/131 | sealed |
| M33 · 4xx unavailable denies (a; L522) | 24/28 | 124/131 | neither |
| M34 · 5xx unreachable allows (a; L524) | 24/28 | 125/131 | neither |
| M35 · Accept duplicate check ids (f; L473) | 24/28 | 130/131 | neither |
| M36 · Accept user-agent with invalid suffix (f; L486) | 25/28 | 129/131 | sealed |
| M37 · Use string-prefix path containment (f; L413) | 28/28 | 130/131 | sealed |
| M38 · Reject exactly 64 MiB manifest (g; L362) | 28/28 | 130/131 | sealed |
| M39 · Replace invalid manifest UTF-8 (g; L380) | 28/28 | 130/131 | sealed |
| M40 · Accept boolean/float manifest version 1 (g; L390) | 26/28 | 130/131 | sealed |
| M41 · Emit report version 2 (usage; L76) | 28/28 | 7/131 | sealed |
| M42 · Overcount checksEvaluated by one (f; L560) | 28/28 | 7/131 | sealed |

**Survivors:** sealed **23/42** (18 at 28/28; M20/M21/M31/M36/M40 pass only through the frozen tolerance); selftest **3/42**; both **M04, M14, M15**. Sealed kills 19; selftest kills 39. The table enumerates every sealed survivor; there are no selftest-only survivors.
Positive controls establish all three joint survivors are non-equivalent defects, not harmless rewrites. Same manifest run on pristine/mutated/restored bytes; all pristine/restored outputs were exit 0, clean, one evaluated check, no findings:
- M04 (`SCORECARD.md:1817-1818`): robots bytes `User-agent: *\nDisallow: /\xffprivate\n`, URL `/private`, expect allow. Ignoring the invalid byte yields exit 1, failed-policy, `blocked`; replacement correctly allows.
- M14 (`SCORECARD.md:1829-1830`): two wildcard groups deny `/one` and `/two`; URL `/two`, expect disallow. Keeping only the first yields exit 1, failed-policy, `exposed`; combined groups correctly deny.
- M15 (`SCORECARD.md:1827-1830`): `User-agent: bot\nDisallow:\nUser-agent: *\nDisallow: /\n`, URL `/private`, expect allow. Empty exact group must suppress wildcard fallback; mutant yields exit 1, failed-policy, `blocked`.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w2/MutRobotsTool/tmp timeout --kill-after=5s 180s python3 -B survivor_witness.py` → 0; nine concrete tool invocations, all expected. Inputs, exact argv, reports and hashes: `survivor_witness.py:15-20`, `witnesses/{M04,M14,M15}/{manifest.json,robots.txt,pristine.json,mutated.json,restored.json}`, `witnesses/summary.json:1`.
**Verdicts:** published pristine pass results **hold**. Treating either detector as exhaustive contract-defect coverage is **overstated**: three demonstrated (b)/(c) defects survive both. This is a coverage finding, not a defect in the unchanged production bytes, a contract change, or a round-admission verdict.
Restoration evidence: `evidence/restored/summary.json:1` records all 84 restored detector successes and reaped children; per-target receipts record the exact original hash above. Reproducible complete score/hash bundle: `result.json:1`.
Scope note: two preliminary standalone pristine preflights used implicit TMPDIR and are excluded from the controlled evidence; every counted run explicitly used S/tmp. No tool installations or updates.
