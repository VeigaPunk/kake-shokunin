HOLDS (with a reach caveat): counter v3 caught both of my behaviour-bearing scheme-area mutants (2/2, killed on 9–10 of 10 runs); the other 8 single-point scheme mutants met and are provably behaviour-equal, so their survival is not a counter gap.

Attack: one-member changes of the LANDED build (tool sha256 `914ebdee…`, copy `/fast/scratch/hyaku/kake-r42w2/MutBuildScheme/build.py`, same sha) in `_SCHEME_ASCII` (build.py:132), `_TABLE_SCHEME` (:133), first-char check (:219), `://` check (:225). tip41 `50287ac6…`, base40 `4de35f8c…`, counter v3 `ce2d5a0c…`. Scoring command (per mutant, no `--seed`):
`timeout 900 prlimit --as=8000000000 -- python3 -B <lane>/.ufo/waves/round-42/c42_count_v3.py --root <lane> --tool-file $PWD/<mutant>.py --label MutBuildScheme-<mutant> --out $PWD/<mutant>.json` (exit 0 met / 1 not met). Receipts in `/fast/scratch/hyaku/kake-r42w2/MutBuildScheme/M*.json`.

| tool | sha256 (12) | one-line change | seed | equalRuns | ratios T1..T5 | met |
|---|---|---|---|---|---|---|
| M1_drop_minus | 3710ecb9e3d3 | `-` dropped from `_SCHEME_ASCII` | 12293878160583 | 10/10 | .99 1.33 1.28 1.23 1.17 | yes |
| M2_drop_plus | 4bc61375608f | `+` dropped from `_SCHEME_ASCII` | 178816950276102 | 10/10 | 1.03 1.37 1.41 1.21 1.19 | yes |
| M3_allow_underscore | e0ed35a5da2f | one table byte: `_` (0x5F) admitted | 77630085874261 | 10/10 | 1.00 1.39 1.42 1.34 1.13 | yes |
| M4_scheme_non_ascii | bf4a222f9544 | `_class_table(..., non_ascii=True)` | 268005352187647 | 10/10 | 1.05 1.42 1.38 1.13 1.12 | yes |
| M5_first_digit_ok | 849563920ee4 | first char may be `0-9` (:219) | 176542076761970 | 10/10 | 1.02 1.37 1.36 1.20 1.19 | yes |
| M6_scheme_len_ge2 | 917d76284ed0 | `colon < 1` → `colon < 2` (:218) | 223177824812708 | 10/10 | 1.02 1.48 1.39 1.21 1.22 | yes |
| M7_allow_tilde | 94a41b0915f7 | `~` added to `_SCHEME_ASCII` | 159661200866756 | 10/10 | 1.02 1.30 1.15 1.32 1.51 | yes |
| M10_single_slash | 5f703e9dd871 | `!= b"//"` → `!= b"/"` (:225) | 261718967747252 | 10/10 | .99 1.31 1.28 1.31 1.16 | yes |
| M8_drop_t | 35c6c59671d4 | `t` dropped from `_SCHEME_ASCII` | 95765027587783 | 0/10 | .06 .05 .06 .06 .87 | no |
| M9_first_lower_only | a216a985fa1a | uppercase head branch removed (:219) | 110554234923086 | 1/10 | .92 1.14 1.21 1.31 1.19 | no |

Killed, which run caught it: M8 output sha differs on all ten runs (A–E,T1–T5), exits also differ on T1–T4 (ref 1, cand 2 — http(s) no longer recognised); M9 unequal on A,B,C,D,E,T1,T2,T3,T5, only T4 (round-39 real run, lowercase schemes) stayed equal. So the counter's scheme-case churn (`rcase`, 30% upper) and its all-ASCII unit sweeps are what make these detectable.

Witness search for every meeting tool (`_parse_url` vs tip41, both imported; plus CLI). None found:
- 60,000 scheme-directed values (`fuzz_scheme.py`, seed 424242: scheme heads/tails over 0x00–0x7F + non-ASCII, delim variants, `rcase` http(s)): 0 differing values for M1–M7, M10; M8/M9 differ immediately (e.g. `HtTP://h.example/x`: None vs `('http','h.example',80,'/x')`).
- Delimiter corpus 1,832 + 394 random one-char edits: 0 diffs for M10.
- CLI corpus `cli/s.xml` (12 scheme-directed locs: `ht_tp://`, `h+ttp://`, `ht-tp://`, `h~ttp://`, `httpé://`, `3http://`, `a://`, `HTTP://`, `http:/`) run as `python3 -B <tool> --manifest cli/m.json`: tip41, build, M1–M7, M10 all `exit=1`, stdout sha256-12 `77614d6f90ca`; M8 `exit=2` `518173259842`; M9 `exit=1` `217b4c350eba`.

Mechanism (why 8 of 10 are behaviour-equal, not undetected defects): `_uri_ok` is called only from `_parse_url` (build.py:290; the only other users are `_audit_loc` :506 and `_evaluate_check` :580, both via `_parse_url`), and `_parse_url` returns None unless `urlsplit` scheme ∈ {http, https} (:293–295). Any value that can possibly yield a parsed URL therefore has `raw[0:colon]` made only of the letters of http/https — every mutated table accepts those, the head is `h`/`H`, and `colon` is 4/5 (> 2). Where a mutant *widens* scheme acceptance (`_`, `~`, non-ASCII, digit head, single-slash `/`), `urlsplit` rejects the scheme downstream, so no judgment changes. Sanity: pristine build vs tip41 on the same 60,000 values → 0 diffs.
Statement "the counter can catch one-member changes of the build's scheme scanning": holds for behaviour-bearing changes (2/2), overstated if read as "the scheme table's contents are exercised" — only the bytes of `http`/`https` are; the rest of the scheme breadth (`+ - .`, first-char rule, `://` arity) is unreachable-in-effect for every output. That is dead breadth in the build, not a rule-2 control: none of M1–M7, M10 has a witness, so each is a rule-2 "not a control" (behaviour-equal rewrite), as wave 1 found for `MutRegexPct/portpct`.

Restoration: I only ever wrote under `/fast/scratch/hyaku/kake-r42w2/MutBuildScheme/` plus this report; no lane file was touched. `sha256sum scripts/sitemap_audit.py` after all work = `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (= before, = my `build.py` copy). All spawned python/bwrap processes have exited (`timeout 900` per run; receipts written). No tool installed or upgraded this item.
