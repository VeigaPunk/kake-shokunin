MET — 3 of 4 controls of the caching/precomputation class met the predicate (10/10 equal, ratios ≤ 1.771), each with a witness where base42 = tip41 and the control differs, so each is a control; under kill rule (2) a control that meets means C1 is not met (L1 to rule).

Seat KakeR42.CtlFreshCache, round-42 wave 2, lane `kake-shokunin`. Tools built from the scored build
(`scripts/sitemap_audit.py` @020bc457, sha256 914ebdee…) — only `_parse_url` is wrapped by a cache.
Counter `.ufo/waves/round-42/c42_count_v3.py` sha256 ce2d5a0c…, scored **without `--seed`** (seed drawn
from `os.urandom`, recorded in each receipt). At most 3 counters at once; every run capped as instructed.

Command (per tool): `timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-42/c42_count_v3.py --root <repo> --tool-file <tool> --label CtlFreshCache-<name> --out /fast/scratch/hyaku/kake-r42w2/CtlFreshCache/<name>.json`

| tool (path under /fast/scratch/hyaku/kake-r42w2/CtlFreshCache/) | sha256 | one-line change |
|---|---|---|
| `v1_commonprefix.py` | `9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4` | `_parse_url` memoised on the value with ASCII letters folded to lower case |
| `v2_userinfocache.py` | `eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f` | `_parse_url` answered from a table keyed on the first 32 code points of the value |
| `v3_querycache.py` | `6afc89f8248c4ee4e6f62e11b9491766c342d7aafc2df57798fd3be52cb58b0d` | `_parse_url` answered from a per-host cache of the whole first result (scheme, host, port, path) |
| `v4_uriokmemo.py` | `dc8b6ecdcc638d20d34f66aaeadd8aa8ba798f5307c2fa8d80a876d2ae16ece7` | `_parse_url` answered from a static table of common hosts, URI check skipped |

Receipts (seed; equalRuns; ratios T1/T2/T3/T4/T5; met; counter exit; which run caught it):
- `v1_commonprefix`: 235657414196257; **10/10**; 1.235/1.771/1.736/1.349/1.347; **met true**; exit 0; nothing caught it.
- `v2_userinfocache`: 247978936813490; **10/10**; 1.035/1.33/1.592/0.714/1.142; **met true**; exit 0; nothing caught it.
- `v3_querycache`: 187784835162308; **3/10**; 1.063/1.567/1.739/0.749/1.056; met false; exit 1; caught by **A, C, D, E, T1, T3, T4**.
- `v4_uriokmemo`: 155356302814098; **10/10**; 1.04/1.189/1.612/1.362/1.178; **met true**; exit 0; nothing caught it.

Witnesses (`witness.py`, exit codes and stdout compared; `base42` was run on every witness and is byte-equal to
tip41, so the divergence is the cache's, not the build's):
- `v1`: locs `http://h.example/ABdir/x`, `http://h.example/abdir/x`, sitemapUrl `http://h.example/ABdir/sitemap.xml`
  → tip41/base42 exit 1 `loc_out_of_scope entry 2`; control exit 0 `clean`. `_parse_url('http://h.example/abdir/x')`:
  tip41 `(http,h.example,80,'/abdir/x')`, control `(http,h.example,80,'/ABdir/x')`.
- `v2`: locs `http://h.example/`+40×`a`+`%zz` then `…ok`, sitemapUrl `http://h.example/sitemap.xml` → tip41/base42
  exit 1 one `loc_not_absolute entry 1`; control exit 1 **two** `loc_not_absolute` (entries 1 and 2).
  `_parse_url` of the second value: tip41 a tuple, control `None`.
- `v3`: locs `http://h.example/a/x`, `http://h.example/b/y`, sitemapUrl `http://h.example/a/sitemap.xml` → tip41/base42
  `loc_out_of_scope entry 2`; control exit 0 `clean` (path of the first reused).
- `v4`: loc `http://localhost/%zz`, sitemapUrl `http://localhost/sitemap.xml` → tip41/base42 exit 1
  `loc_not_absolute entry 1`; control exit 0 `clean`. `_parse_url`: tip41 `None`, control `(http,localhost,80,'/')`.

Checked statements (holds / overstated / wrong):
- "the predicate (equal on every generated run, ratios ≤ 2.0) certifies that the tool keeps every round-41 judgment"
  — **WRONG**: three caching controls meet it and judge ordinary values differently (witnesses above).
- "caching/precomputation that survives random seeds cannot meet the predicate" — **WRONG**: v1, v2, v4 met at
  `os.urandom` seeds; their divergences need only repeated structure (case-variant value, two values sharing 32 code
  points, a host from a static table), which no generator of the counter produces (`analyze.py`: 0 case-variant pairs,
  0 distinct-value 32-prefix collisions over seeds 4242/991/20261023/7; the one seed-4242 group is an identical duplicate).
- "the corpus distinguishes a per-host cache" — **HOLDS**: v3 was caught on 7/10 runs; generated hosts do repeat
  (≈28–36 hosts per run carry two different ports), so a whole-result per-host cache diverges inside the corpus.
- "values are distinct (a random token leads every path), so caching by value cannot help" (`c42_count_v3.py:33`) —
  **OVERSTATED as a defence**: exact-value memo cannot help, but the retained real run repeats 32-code-point prefixes at
  **99.2 %** (38 772 hits / 39 080 loc values, 308 distinct prefixes), so v2 skips the URL check on T4 and lands at
  **0.714× round-40** (~43 % below the build's own T4 ratio 1.264) while staying output-equal.
- "a meeting tool must be a behaviour-equal rewrite" — **WRONG** for this class: v1/v2/v4 each have a CLI-level and a
  `_parse_url`-level witness, i.e. they satisfy the frozen rule "a meeting tool is a control iff a witness value is
  shown" (their witnesses lie outside runs A–E, so the counter's own equality cannot see them).

Files: four tools + `analyze.py` + `witness.py` + `witness/` + `<name>.json` receipts + `<name>.log` under
`/fast/scratch/hyaku/kake-r42w2/CtlFreshCache/`; this report. No tool installed or upgraded; no repo, lane-jj or git
write; no network. Risk: each verdict is one `os.urandom` seed per tool (v1/v4 are seed-independent by construction;
v2 needs two distinct values to share 32 code points, measured 0 over four seeds; v3 is deterministic).
