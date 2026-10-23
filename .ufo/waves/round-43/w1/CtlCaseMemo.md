MET — four case-fold-memo controls met the v4 predicate (11/11, ratios <=1.48) while their CLI output differs
from the round-41 tool on a supplied witness: counter v4 cannot see this class. Kill rule ("a control that meets
-> C1 NOT MET") therefore fires on this class; the L1 decides (this seat does not).

Built from the frozen build `020bc457` (`git show 020bc457:scripts/sitemap_audit.py` =
`914ebdee7bcb...`, byte-equal to the working file), one memo added per tool; base kept otherwise intact.
Counter `.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b9661...` matches the frozen counter.

Command (one per tool, no `--seed`, seed drawn from os.urandom):
`timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-43/c43_count_v4.py --root <repo> --tool-file /fast/scratch/hyaku/kake-r43/CtlCaseMemo/<v>.py --label CtlCaseMemo-<v> --out /fast/scratch/hyaku/kake-r43/CtlCaseMemo/<v>.json`

| tool (dir `/fast/scratch/hyaku/kake-r43/CtlCaseMemo/`) | sha256 | skip (one line) | seed | equalRuns | ratios T1..T5 | met | caught by |
|---|---|---|---|---|---|---|---|
| v1_memo_value_lower.py | `cb7f3315...` | full `_parse_url` result memoized under `value.lower()` | 275182798613458 | 10/11 | 1.086 1.195 1.312 1.344 1.285 | false | **run F** |
| v2_memo_authority_lower.py | `0ea6be18...` | full parse memoized under the lower-cased authority component | 278057045964480 | 2/11 | 1.065 0.930 1.028 0.734 1.171 | false | A,C,D,E,F,T1,T2,T3,T4 |
| v3_memo_validity_lower.py | `bec3fd0c...` | only the `_uri_ok` verdict memoized under `value.lower()` | 177976386450790; rerun 99779124184620 | 11/11; 11/11 | 1.096 1.253 1.388 1.302 1.255; 1.065 1.136 1.435 1.383 1.281 | **true**; **true** | — |
| v4_memo_validity_lower_short.py | `5c9158fb...` | as v3, gated to values <=64 code points | 253324364115530; rerun 48234740188413 | 11/11; 11/11 | 1.048 1.211 1.463 1.331 1.140; 1.001 1.212 1.472 1.328 1.113 | **true**; **true** | — |
| v5_memo_value_casefold.py | `5c55af22...` | full parse memoized under `value.casefold()` | 183151114290059 | 9/11 | 1.182 1.217 1.453 1.280 1.227 | false | **F, T2** |
| v6_memo_path_casefold.py | `a4f57dbe...` | full parse memoized under `casefold()` of the path component | 44659963718528 | 3/11 | 1.146 1.314 1.512 1.461 1.197 | false | A,B,C,D,E,F,T3,T4 |
| v7_memo_value_lower_nonascii.py | `d41f0f1b...` | full parse memoized under `value.lower()`, consulted only for values carrying a non-ASCII character | 145800555643649; rerun 127410521958092 | 11/11; 11/11 | 1.107 1.254 1.416 1.282 1.282; 1.062 1.195 1.466 1.362 1.372 | **true**; **true** | — |
| v8_memo_value_casefold_nonascii.py | `29070eed...` | as v7 but keyed on `value.casefold()` | 182719331353519; rerun 261082027567851 | 11/11; 11/11 | 1.109 1.256 1.437 1.292 1.297; 1.118 1.263 1.479 1.377 1.314 | **true**; **true** | — |
| reference: the r42 build itself | `914ebdee...` | none (no memo) | 113649863528153 | 11/11 | 1.010 1.151 1.264 1.237 1.174 | true | — |

Witnesses (meeting tools; round-41 tool = `ref41.py`, `git show 1ef7a0e9:...` sha256 `50287ac6...`; both
tools run on the same manifest, same cwd; the memo is process-global so both values share one run):
- v3/v4 — `/fast/scratch/hyaku/kake-r43/CtlCaseMemo/witness/w6_kelvin_zone/m.json` (sitemapUrl
  `http://[::1%25k]/sitemap.xml`; loc 1 `http://[::1%25K]/x` with U+212A KELVIN SIGN, loc 2 ASCII
  `http://[::1%25k]/x`). `loc2.lower()==loc1.lower()`. ref41: `loc_not_absolute` entry 1 only, exit 1.
  v3/v4: `loc_not_absolute` entries 1 **and 2**, exit 1. `_parse_url`: ref41(loc2)=`('http','::1%25k',80,'/x')`,
  v3(loc2)=`None`.
- v7/v8 — `witness/w2_fold_nonascii/m.json` (sitemapUrl `http://h.example.com/Éseg/sitemap.xml`; loc 1
  `.../Éseg/x`, loc 2 `.../éseg/x`). ref41: `loc_out_of_scope` entry 2, exit 1. v7/v8: `clean`, exit 0 (loc 2
  answered from loc 1's cached tuple, so its path prefix is judged with the wrong case). Also reproduces when
  the two values sit in separate files of one manifest (`witness/w5_split_files/m.json`).

Findings (holds / overstated / wrong):
- `.ufo/waves/round-43/c43_count_v4.py:428-440` (`fold_pair`) — HOLDS as written ("fold to one key under
  upper-to-lower folding") but the pair differs by `seg[j].upper()` on a lowercase ASCII token (`:435`): the
  fold class is ASCII-only. Same at `:443-455` (`prefix_pair`) and `:458-490` (`cases_f`).
- `.ufo/waves/round-43/c43_count_v4.py:5` (run-F class list, "case-fold pairs") and `:509-512` ("a case-fold
  cache answers it in-scope") — OVERSTATED: true only for a memo over the parse result under an ASCII-only fold (v1 caught by F,
  v5 caught by F+T2). A memo that stores only the validity verdict (v3/v4) or that is keyed on a fold reaching
  non-ASCII (v7/v8) passes all 11 runs while disagreeing with round-41.
- `.ufo/waves/round-43/c43_count_v4.py:319` `LOOKALIKE` carries `\u212a`, `\u0130`, `\u017f` — HOLDS as a unit
  pool, but `:328-372` (`e_units`, `slot_value`, `cases_e`) insert one unit into one value, so no two generated
  values ever share a folded form: run E never exercises a folded-key collision.
- `scripts/sitemap_audit.py:130` (`_TABLE_IP_LITERAL` built `non_ascii=False`) with `:287-306` (`_parse_url`) and
  `:502-516` (`_audit_loc`) — HOLDS: the grammar keeps a non-ASCII/ASCII pair distinguishable (Kelvin vs `k`
  inside the brackets), which is what makes the v3/v4 witness a real divergence rather than a rewrite.
- Sandbox/harm: all 8 tools are the frozen build plus one memo; no other edit (diff inspected). `base_r42.py`,
  `ref41.py`, every variant's sha256 above; build tools in `/fast/scratch/hyaku/kake-r43/CtlCaseMemo/`
  (`build_variants.py`, `build_variants3.py`, `sanity.py`, `witness.py`, `witness2.py`, `hunt_v3.py`).

Calibration: the four meeting tools are not do-nothing/constant tools — each returns the round-42 verdict for
every value whose folded form is unseen and skips re-judgment only on a collision (a real but narrow skip).
Untested / not claimed: no second seed for the reference build row; v2/v6 catch sets read from one receipt
each; the witnesses are hand-built manifests, not counter runs; no RSS claim. No tool installed or upgraded.
Wrote only `/fast/scratch/hyaku/kake-r43/CtlCaseMemo/` and this report; no mutating git/jj command (read-only
`git show`/`git rev-parse`), no lane file touched; all processes finished under `timeout`.
