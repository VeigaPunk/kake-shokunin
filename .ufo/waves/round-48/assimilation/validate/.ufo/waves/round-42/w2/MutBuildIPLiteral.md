MET — the counter's catch power in the IP-literal/bracket area holds: 6 of 6 behaviour-changing one-member mutants were killed, and the single survivor is a provably equivalent mutant with no witness. No coverage hole found.

Tool under attack: `scripts/sitemap_audit.py` at lane tip 721310b19af88d3c43c01647d3ce29d51e6e3b96, build sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (copied to `/fast/scratch/hyaku/kake-r42w2/MutBuildIPLiteral/build.py`, same hash). Detector: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count_v3.py` sha256 `ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc`. Reference: `/fast/scratch/hyaku/kake-r42/shared/tip41.py` sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.

Scoring command, per tool (exit 0 = met, 1 = not met, 2 = cannot evaluate; no `--seed`):
`timeout 900 prlimit --as=8000000000 -- python3 -B …/c42_count_v3.py --root …/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w2/MutBuildIPLiteral/<tool> --label MutBuildIPLiteral-<tool> --out …/out/<tool>.json`
Runs: first batch `m1 m2 m3` in one shell with 3 background jobs, wall 60 s; second batch `m4 m5 m6`, wall 43 s; `m7` alone, wall 41 s. Every mutant file is a separate copy; the lane file was never opened for writing.

| tool | one-line change (lane `scripts/sitemap_audit.py` line) | sha256 | exit | equalRuns | ratios T1..T5 | caught by |
|---|---|---|---|---|---|---|
| m1_ip_drop_pct | line 124: `_IP_LITERAL_ASCII` drops the `%` member | 27c274739ff6b2a781a18b21a901c191db5a66b195c783183dc675654023206c | 1 | 6/10 | 1.112/1.339/1.284/1.245/1.315 | A, B, D, E |
| m2_ip_nonascii | line 130: `non_ascii=False` → `True` for `_TABLE_IP_LITERAL` | 48bf8f5528f77412d68f8649e1c1a739d7bfdaed9b925b8e6c819f934fd2057f | 1 | 8/10 | 1.205/1.340/1.351/1.140/1.197 | B, E |
| m3_ip_add_space | line 124: `_IP_LITERAL_ASCII` gains the space byte | 09798d9bc3b95ae1497599937a768c733027abdd865a20044ab34b3c43a40d79 | 1 | 9/10 | 1.096/1.370/1.313/1.291/1.083 | E only |
| m4_bracket_ge_gt | line 187: `close >= authority_end` → `close > authority_end` | c5371b525f61bb0d125463f8e19aab4ffe04944726943ee81337176ae388bc87 | 0 | 10/10 | 0.927/1.303/1.445/1.325/1.201 | — (survived, met=true) |
| m5_port_digit_top | line 198: port digit ceiling `0x39` → `0x38` | 591820e591b2564b2a9a3fd59b9c5bd77babba8517d4de37e2123c68985e485b | 1 | 6/10 | 1.020/1.378/1.337/1.241/1.243 | A, B, D, E |
| m6_ip_drop_underscore | line 124: `_IP_LITERAL_ASCII` drops the `_` member | 589821769db9995b054b1498aa094fbe9982805be5ec00553ddbf9ae06172b3e | 1 | 9/10 | 1.070/1.331/1.548/1.282/1.112 | E only |
| m7_ip_add_tab | line 124: `_IP_LITERAL_ASCII` gains the tab byte (one table byte) | 9be01591bcb29deaba1c32fdb19dfa5f88ba7c11a4de11396a1cc83e8d3f8dd0 | 1 | 8/10 | 0.854/1.322/1.437/1.179/1.256 | B, E |

Seeds: m1 201776976193692, m2 111415394375470, m3 192307454494476, m4 20126490570480, m5 175371702608137, m6 190837648476452, m7 232216209473597. REPS=5, ratio limit 2.0; every mutant also stayed under the cost limit, so each verdict was decided by output equality alone.

Witnesses, CLI level (each manifest: `sitemapUrl` `http://example.com/`, one `<loc>` holding the witness; build and tip41 outputs are byte-identical, sha256 of stdout prefix `bed2f840` = `loc_out_of_scope`, `f66984f0` = `loc_not_absolute`):
- m1 `http://[fe80::1%eth0]/x` — build/tip41 `loc_out_of_scope` (parsed as host `fe80::1%eth0`), m1 `loc_not_absolute`.
- m2 `http://[v1.é]/x` — build/tip41 `loc_not_absolute`, m2 `loc_out_of_scope` (urlsplit's IPvFuture path accepts it).
- m3 `http://[v1.a b]/x` — build/tip41 `loc_not_absolute`, m3 `loc_out_of_scope`.
- m5 `http://[::1]:9/x` — build/tip41 `loc_out_of_scope` (port 9), m5 `loc_not_absolute`.
- m6 `http://[v1.a_b]/x` — build/tip41 `loc_out_of_scope`, m6 `loc_not_absolute`.
- m7 `http://[v1.a<TAB>b]/x` — build/tip41 `loc_not_absolute`, m7 `loc_out_of_scope` (urlsplit strips the tab, host `v1.ab`).
- m4: no witness — `close` indexes a `]` byte while `authority_end` indexes a `/`, `?`, or `#` byte (or equals `len(raw)`, while `close < len(raw)`), so `close == authority_end` is unsatisfiable and `>=` / `>` agree on every input. Checked twice: 200,000 `bracket_value()` samples replayed from the counter's own generator and 180,000 random bracket-shaped values gave 0 `_parse_url` differences vs tip41 (build vs tip41 on the same 180,000: also 0).

Findings:
1. Holds — counter v3 kills every one-member change tested in `_TABLE_IP_LITERAL` / `_IP_LITERAL_ASCII` (`scripts/sitemap_audit.py:124`, `:130`) and in the bracket/port branch (`:187`, `:198`), including changes that only a urlsplit-tolerated byte makes observable (space, tab, non-ASCII, `_`, `%`).
2. Overstated if read as "run B carries this area": at m3's seed 192307454494476, 0 of the 1200 run-B bracket values were observable for the added-space member (replayed `cases_a` + `layout_cases` + `cases_b` with that seed). The kill came from run E only, whose slot alphabet enumerates all ASCII. Runs B for m3 and E for m1 also illustrate this: B's 60%-of-edits insertion picks one of ~150 units, so any single printable byte is generated a handful of times per run at best.
3. Holds with a caveat on granularity: the first divergence in every caught run reports `candExit` 2 (a `sitemapUrl` the mutant rejects, flipping the whole run to could-not-evaluate), so the receipts prove judgment equality — not which of the 1200/2000/4939 values flipped. The CLI witnesses above show the flips are genuine per-value judgments, not crashes.
4. m4's survival is not a counter gap: it is an equivalent mutant, so it cannot be a control under the kill rule.

Restoration: no build byte was mutated in place; `scripts/sitemap_audit.py` re-hashed after all scoring runs is still `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`, equal to the pre-run copy `build.py`. No installs or upgrades were made; host Python 3.14.8, counter run under `prlimit --as=8000000000` and `timeout 900`. Artifacts left under `/fast/scratch/hyaku/kake-r42w2/MutBuildIPLiteral/` (`build.py`, `m1..m7*.py`, `out/*.json`, `cli/`, `logs/`), ≈80 KB.
