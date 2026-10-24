MET — three of five port-length-gate controls met counter v4's predicate (exit 0) while disagreeing with the round-41 tool; the counter cannot see this control class, so the round's kill rule ("any live-seat control meeting v4 -> C1 NOT MET") fires.

Seat `CtlPortLen` (control class: port-length gates). Axis: operability. Sandbox: `/fast/scratch/hyaku/kake-r43/CtlPortLen/` (all artefacts). No network, no tool installs.
Counter: `.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab` (matches `verification/freeze/counter-v4.sha256`).
Base for every variant: `git show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py`, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (r42 fast build). Python 3 stdlib only.

## Scoring command (one per tool, no `--seed`; seed drawn from os.urandom and recorded in the receipt)
`timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-43/c43_count_v4.py --root <repo> --tool-file <tool> --label CtlPortLen-<name> --out <sandbox>/receipts/<name>.json`

| tool (path under `tools/`) | sha256 | one-line skip | receipt | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | exit | run that caught it |
|---|---|---|---|---|---|---|---|---|---|
| `v1_skip_grammar_6plus.py` | `752a8de5baba3d14f8edb8e77052c0f8dd164f814c4c74c2922283abda5d7df6` | skip the grammar scan `_uri_ok` when the authority's port has >=6 digits (urlsplit + port-range check still run) | `receipts/v1_skip_grammar_6plus.json`, `.seed2.json`, `_rerun.json` | 20206143012247 / 127771515288693 / 256939862227786 | **11/11** (x3) | 1.049/1.291/1.294/1.182/1.131; 1.064/1.256/1.283/1.195/1.146; 1.012/1.196/1.321/1.240/1.295 | **true** (x3) | **0** (x3) | **nothing — it met on 3 independent seeds** |
| `v4_cache_portlen_with_path.py` | `1b34f83d4b45346dd22628064ffb5cda451ea9922b1168933b781648262df58b` | process-global parse cache keyed on (scheme, host, path, port-digit count): the port digits are dropped from the key | `receipts/v4_cache_portlen_with_path.json`, `.seed2.json`, `.seed3.json` | 242546727411566 / 32164737160471 / 169042992976497 | **11/11** (x3) | 1.124/1.190/1.601/1.476/1.277; 1.252/1.254/1.582/1.511/1.238; 1.100/1.203/1.516/1.378/1.126 | **true** (x3) | **0** (x3) | **nothing — it met on 3 independent seeds** |
| `v5_abbrev_window_6plus.py` | `e55e3bfb9a6e9f3523a9c1393e14a2defdadd2ae7c2b4104e12cd717a51e76f5` | judge only the first 64 code points of a value whose authority carries a >=6-digit port | `receipts/v5_abbrev_window_6plus.json`, `.seed2.json`, `.seed3.json` | 38050045368543 / 177141853874895 / 164371636714392 | **11/11** (x3) | 1.082/1.271/1.440/1.286/1.047; 1.080/1.274/1.321/1.288/1.106; 0.946/1.172/1.340/1.367/1.199 | **true** (x3) | **0** (x3) | **nothing — it met on 3 independent seeds** |
| `v2_skip_grammar_and_port_6plus.py` | `2a176ebb47ac09316f5149207519f4fd42b870aab55e5060fad5f0872fc72bbc` | skip grammar **and** port-range check for a >=6-digit port; read the port as its first five digits | `receipts/v2_skip_grammar_and_port_6plus.json` | 75177356262882 | 6/11 | 1.020/1.259/1.354/1.290/1.210 | false | 1 | **F, T1, T2, T3, T5** |
| `v3_cache_portlen.py` | `edc60507310d7a9f3210ff7cc145684e2b5fb7ee5b66cc513588284222c99a4c` | process-global parse cache keyed on (scheme, host, port-digit count): path **and** port digits dropped from the key | `receipts/v3_cache_portlen.json` | 175271011686483 | 4/11 | 1.152/0.945/1.111/0.751/1.220 | false | 1 | **A, C, D, E, F, T2, T3** |
| `M8-port-five-digits.py` (round-42 control, re-scored here) | `391608309640431acfc873d48e33189cf71a399faaa410ce6d65b910282bbb1f` | read at most five port digits (upstream) | `receipts/M8-port-five-digits.json` | 236183745249029 | 9/11 | 1.012/1.218/1.314/1.251/1.108 | false | 1 | **F, T3** (agrees with the L1 freeze receipt) |

Baseline: the untouched r42 build scored `equalRuns 11/11, met true` at seed 43922329937609 (`receipts/sanity.json`) — the counter itself works.

## Witnesses: the three meeting controls differ from the round-41 tool
`_parse_url` level (round-41 tool = `refs/ref41.py`, sha256 `50287ac6…`):
- `v1`: `http://h.example:000080/a b` -> round-41 **None**, v1 `('http','h.example',80,'/a b')`. Also `…/a%zz`, `…/a|b`, `…/a^b`, `…/0000123/a b` -> round-41 None, v1 a tuple.
- `v4`: `http://h.example:000081/x` -> round-41 `('http','h.example',81,'/x')`, v4 `('http','h.example',80,'/x')` (the cache answers from the `:000080` sibling).
- `v5`: `http://h.example:000080/` + `a`*100 + `|` -> round-41 **None**, v5 `('http','h.example',80,'/a'*40)`.

CLI level (`python3 -B cli_witness.py <tool>`; one manifest, one sitemap, `sitemapUrl = http://h.example:000080/sitemap.xml`):
- `v1`, loc `http://h.example:000080/a b`: round-41 exit **1**, finding `loc_not_absolute` entry 1; v1 exit **0**, `"verdict":"clean"`.
- `v5`, loc `http://h.example:000080/` + `a`*100 + `|`: round-41 exit **1**, `loc_not_absolute` entry 1; v5 exit **0**, `clean`.
- `v4`, two locs `http://h.example:000080/x` and `http://h.example:000081/x`: round-41 exit **1**, `loc_out_of_scope` entry 2; v4 exit **0**, `clean`.
So all three are genuine controls (they change a judgment on an ordinary value), not honest rewrites — and the counter scored them `met`.

## Why the counter is blind here (measured, not inferred)
`probe_blindspot2.py` / `probe_timing.py` replay the counter's own generators and ask the only question that matters: does the corpus ever contain a value that (a) carries a port of >=6 digits **and** (b) is rejected by the round-41 grammar check? Measured over the equality corpus (runs A-F) at seeds 20206143012247 / 256939862227786 / 127771515288693 / 32164737160471: 240 values per seed carry a 6+-digit port, ~66-80 of them in range, and **0** are grammar-rejected. Over the timing shapes at seed 20206143012247: T1 395 long-port values (0 witness cells), T2 22 (0), T3 542 (0), T5 3 (0). The pairing that would expose a port-length gate is simply absent.
`probe_collision2.py` (the v4 cache): at the three seeds where v4 met, the corpus contains 1-3 cache keys shared by >1 distinct value, but **0** of those groups changes an accept/reject answer in the same process (the collisions sit in different runs/manifests, i.e. different processes).
- `.ufo/waves/round-43/c43_count_v4.py:395-403` — "Zero-padded in-range forms exercise the port loop **without an output difference of their own**." Holds as a statement about the corpus, and is exactly the hole: a 6+-digit port never co-occurs with a grammar defect, so skipping the grammar check for long-port authorities is invisible.
- `c43_count_v4.py:465,467` — run F pairs `long_port` only with otherwise-clean `short_url` values (no `defect=True`), so no corpus value exercises "long port AND something else wrong".
- `c43_count_v4.py:569-583` — `with_long_port` always inserts an **out-of-range** port (`out_of_range=True`), whose verdict is fixed by the port-range check that every variant here keeps; v2 is caught precisely because it drops that check.
- `c43_count_v4.py:1027,1055-1062` — equality is byte-comparison of outputs on the generated runs only; a class of disagreement absent from the corpus cannot be observed.

## Checked statements
- "the counter rejects a control that skips the URL check when the port has >=6 digits" — **WRONG**: v1 met on three independent random seeds (exit 0, 11/11).
- "run F's 6+-digit ports make the port-length gate visible" — **OVERSTATED**: F exercises the port *loop*, but never the port *gate* (0 grammar-rejected long-port values per seed); only the port-range half is visible (v2 and M8 are caught there).
- "keying a cache on the port length is caught" — **WRONG** for a key that keeps the path (v4 met 3/3 seeds); **holds** for a key that drops the path (v3 caught by A, C, D, E, F, T2, T3).
- "the counter's equality runs decide 'every judgment' of the round-41 tool" — **WRONG beyond the generated runs**, as in round 42: equalRuns 11/11 and equalValues 11889 say nothing about `http://h.example:000080/a b`.
- "the round-42 control M8-port-five-digits is not met" — **holds** (re-scored here: 9/11, caught by F and T3; same runs as the L1 freeze receipt).
- "the counter is seed-robust for these controls" — **holds, and this differs from round 42's CtlCache finding**: these controls are not corpus-harvested, so they met on every seed tried (3 seeds x 3 controls, 9/9 met).

## Risks
- The meeting verdicts are seed-robust for the three controls above (9/9 met over independent os.urandom seeds), but the blind spot is a property of the *generators*, not of a seed: any seed that keeps long ports away from grammar defects reproduces it. I did not exhaustively search seeds.
- v1/v5 are unsound on values the corpus never builds; they are not fast (their ratios match the honest build), so the hole is in the equality half of the predicate only.
- The port-length gate family has not been exhausted: a gate that skips the grammar check only for **in-range** 6+-digit ports, or one keyed on the first five port digits, were not built (v2 approximates the latter and is caught).

## Recommendation to the L1
Add one equality cell that pairs a 6+-digit **in-range** port with an otherwise-defective value (e.g. `http://h.example:000080/a b`, or a long in-range port with a defect at a code point past any window a control might keep) — that single cell would have caught v1 and v5; a cell with two values sharing scheme/host/path and differing only in their port digits (e.g. `:000080/x` and `:000081/x`) in the same file would have caught v4. A cheaper alternative is to restate the predicate as "equal on the generated runs", as round 42's CtlShapeKeyed recommended.

## Files written by this seat
- This report only: `.ufo/waves/round-43/w1/CtlPortLen.md`.
- Everything else under `/fast/scratch/hyaku/kake-r43/CtlPortLen/` (`build_variants.py`, `tools/`, `receipts/`, `refs/`, `find_witness.py`, `cli_witness.py`, `probe_blindspot.py`, `probe_blindspot2.py`, `probe_collision.py`, `probe_collision2.py`, `probe_collision3.py`, `probe_timing.py`).
- No fleet-repo file other than this report; no `git`/`jj` mutation; no network request; no tool installed or upgraded.
