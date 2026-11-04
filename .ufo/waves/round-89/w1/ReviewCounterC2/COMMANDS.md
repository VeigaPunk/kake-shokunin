# ReviewCounterC2 — experiment log

Scratch root (deleted after copying): /fast/scratch/hyaku/kake-r89/ReviewCounterC2/
Receipts: runs/ (one file per counter run, with exact command, env, exit, stdout, stderr).
Counter copies: head = freeze commit 08ab46a1 (v1 guard, sha256 a72d5efc...);
wt = lane HEAD v2 counter (committed in 46a43e94, sha256 d4588d4b...).
Fixture: a fresh `git init` repo in scratch (toplevel asserted before each commit); one commit per candidate. Commit map: meta/fixture-commits.json.
Candidates: cands/ (sources, copied here verbatim).

## Setup (read-only on lane)
- `git ls-tree -r --name-only 08ab46a1 -- .ufo/waves/round-89` -> meta/freeze-files.txt; each file `git show 08ab46a1:<path>` into scratch head/.
- `git archive` was attempted first and produced an empty tree; discarded, replaced by the per-file extraction above.
- `git show HEAD:scripts/cache_key.py > scratch/work/committed_cache_key.py`; sha-checked the committed v2 counter against the wt copy.

## Selftests
- `cd head/.ufo/waves/round-89 && python3 -B c89_key.py --selftest` -> exit 0, `selftest: 43/43 passed` (selftest/head-selftest.txt)
- `cd wt/round-89 && python3 -B c89_key.py --selftest` -> exit 0, `selftest: 43/43 passed` (selftest/wt-selftest.txt)

## Counter runs (command template)
`python3 -B <counter> --root <root> --revision <rev> --candidate scripts/cache_key.py --work <dir> [--seed N]`

| run (runs/<tag>.txt) | counter | candidate | seed | result |
|---|---|---|---|---|
| head_ref | head | verbatim REFERENCE | 89089 | 16/16 200/200 9/9 met=true |
| head_const / _seed1/_seed2/_seed4242/_seed89089 | head | ctl-constant-key | 89089,1,2,4242 | props=100/200 every seed, met=false |
| head_ref_seed1/_seed2/_seed4242 | head | REFERENCE | 1,2,4242 | 16/16 200/200 9/9 met=true |
| head_plain_import | head | ctl-oracle-import (literal import) | 89089 | guard rejects; output prints `fail: s`, `fail: h`, ... (report bug) |
| head_runtime_import | head | importlib, path from concatenated fragments | 89089 | 16/16 200/200 9/9 met=true |
| head_aliased_import | head | sys.path + import_module('c89'+'_key') | 89089 | met=true |
| head_fileurl_exec | head | urllib file:// + exec, no __file__ | 89089 | 0/16 — candidate bug: NameError __file__ |
| head_fileurl_exec2 | head | same, with __file__ set | 89089 | met=true |
| head_env_import | head | importlib path from $KAKE_R89_REF, env unset | 89089 | 0/16 |
| head_env_import_with_env | head | same, env KAKE_R89_REF set | 89089 | met=true |
| head_no1d | head | REFERENCE minus the U+001D escape | 89089 | met=true |
| head_hybrid_table | head | 12 literal frozen key strings + JSON-list encoding otherwise | 89089 | met=true |
| head_lf_nominated_only | head | CR/LF refused only for nominated headers | 89089 | met=true |
| head_dup_nominated_only | head | case-duplicate refused only for nominated names | 89089 | met=true |
| head_composite_reason | head | every refusal prints all nine keywords | 89089 | refuse=9/9 met=true |
| wt_* (ref, plain_import, runtime_import, fileurl_exec2, aliased_import, hybrid_table, no1d) | wt (v2) | same candidates | 89089 | same as head for each |
| wt_base_lane | wt (v2) | none (lane base 76225160) | 89089 | candidate absent, met=false, ctl-table names 'c2-cases' |
| base_lane_head_counter | head (v1) | none (lane base 76225160) | 89089 | candidate absent, met=false, ctl-table names '.ufo/waves' |

## Carrier reproduction (lane HEAD candidate, read-only --root)
- v2 counter on 9784ad54 (`carrier/v2-on-committed-9784ad54.txt`): frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true; matches controls/c2-carrier-v2.txt.
- v1 counter on 9784ad54 (`carrier/v1-on-committed-9784ad54.txt`): same counts, met=true; matches controls/c2-carrier-frozen-v1.txt.

## Hand derivation and independent check
- Seven worked examples derived by hand; `meta/indep_check.py` (independent code from prose) and the reference both equal the hand expectations for all seven (`meta/indep_check.out.txt`).
- Probes (run inline, outputs recorded in the review):
  - raw U+001D value: REFERENCE -> `u\x1fa\x1ex%1Dy`; no1d -> `u\x1fa\x1ex\x1dy`.
  - duplicate JSON member `"a":"1","a":"2"` -> exit 0, key ends `\x1e2` (silent last-wins).
  - NUL in non-nominated value -> exit 0, key `u` (contract silent on non-CR/LF CTLs).

## Seed population
- Population size is 200 at every seed (by construction: 20 matched draws per class). Seed 89089 and seed 1 yield 198 and 199 distinct left inputs, 4 shared.

## Host and network
- No package was installed or upgraded. No pacman, no ~/.local/bin write.
- No network access; URL-based candidates used file:// on local scratch paths only.
- No writes to the lane except this wave directory; counters wrote only to scratch work dirs.

## Wave-tree read gap (added)
| run | counter | candidate | result |
|---|---|---|---|
| head_wave_read_pathlib | v1 | fragment-built path to c2-contract.md read via pathlib | met=true (v1 also blind to concatenated paths) |
| wt_wave_read_pathlib | v2 | same | met=true |
| head_wave_read_literal_v1 | v1 | literal `.ufo/waves/round-89/c2-contract.md` via pathlib | met=false, guard rejects (garbled fail lines) |
| wt_wave_read_literal_v2 | v2 | same literal | met=true (v2 admits literal wave-tree reads) |
