# ExecH4Probe — round-41 closure probe method, made reusable (r42 wave 1, leaf seat)

**Built** `/fast/scratch/hyaku/kake-r42w1/ExecH4Probe/h4_probe.py` — sha256 `e067e5d48653ecbd1a5d8b195511bee9eb3c3c9a5ac7bec6d11e5f422244fd4d`, 9,413 B; a generalisation of the closure probe `/fast/scratch/hyaku/kake-r42/shared/closure-probe/probe.py` (sha256 `01498b1b60d343f0eabb5ec5f342a3c358a56ce6c994b432a35aa2ec2f91a0b5`).
CLI: `python3 -B h4_probe.py --tool-file <cand.py> --base-file <base40.py> --seed N --out <json>` (`--count`, default 20000 = closure count; `--sitemaps`, default round-41 realrun sitemaps).
Method, the closure's verbatim: values = 0–3 random insertions (any position, ends included) / deletions / duplications of real `<loc>` values; units = ASCII 0x00–0x7F, broken percent units (`%`,`%4`,`%zz`,`%41`), delimiters (`@ # ? : //`), `[`, `]`, `é`, `:99999`; each side's `_parse_url` imported by path via `importlib`; oracle = vendored abnf 2.9.1 `rfc3986.Rule("URI").parse_all` + http(s) + non-empty host; "in-class" = the closure's own `out_of_class` rule (non-ASCII, `[` in host slot, port > 65535). Wheel pinned by sha256 (mismatch → exit 2).
Receipt `counts`: `validReject` = base accepts ∧ oracle accepts ∧ candidate rejects; `newAccept` = base rejects ∧ candidate accepts; `oracleDisagree` = candidate vs oracle, in-class only; plus `n`, `inClass`, `outOfClass`, `baseOracleDisagree`, accept-invalid/reject-valid split.

**Inputs (read-only)**: candidate `…/kake-r42/shared/tip41.py` `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; base `…/kake-r42/shared/base40.py` `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`; oracle wheel `…/shared/closure-probe/abnf-2.9.1-py3-none-any.whl` `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917`; loc pool `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/realrun/sitemaps/` (6 XML, 39,080 `<loc>` = closure's count).

**Commands** (cwd `/fast/scratch/hyaku/kake-r42w1/ExecH4Probe`, each `timeout 900 prlimit --as=8000000000 -- python3 -B h4_probe.py …`):
1. `--tool-file …/tip41.py --base-file …/base40.py --seed 924141 --out r42w1-ExecH4Probe/tip41-seed924141.json` → **exit 0** (121 s)
2. same, `--seed 42001 --out …/tip41-seed42001.json` → **exit 0** (127 s)
3. `--tool-file …/base40.py --base-file …/base40.py --seed 924141 --out …/base40-self-seed924141.json` → **exit 0** (125 s)
4. same, `--seed 42001 --out …/base40-self-seed42001.json` → **exit 0** (108 s)
5. `--help` → exit 0; missing `--tool-file` → exit 2 (`tool file not found`); `--count 50` smoke → exit 0.
Receipts: `tip41-seed924141.json` `c8644a996ab3ce11bdbc418985b0002ad2114d3f40356241406847301886aa51`; `tip41-seed42001.json` `8e6963f822ff05654ee366ea06ee28db2bf3daa938d4df82a19212786980d178`; `base40-self-seed924141.json` `c85ca59f50404b9d320083a0eebcff9f3afc6b529b44c00c4400c0b7618d1e04`; `base40-self-seed42001.json` `df96c14046740e1ba06840bd99931b3f1e3a1fb37b89c4267c8cf67e6e5ab183`.

**Counts**

| run | n | inClass | outOfClass | validReject | newAccept | oracleDisagree (cand, in-class) | baseOracleDisagree | out-of-class changed |
|---|---|---|---|---|---|---|---|---|
| tip41 vs base40, seed 924141 | 20,000 | 19,750 | 250 | **0** | **0** | **0** (0 accept-invalid, 0 reject-valid) | 4,015 (all accept-invalid) | 24 (all base-accept→tip-reject, all oracle-invalid) |
| tip41 vs base40, seed 42001 | 20,000 | 19,720 | 280 | **0** | **0** | **0** (0/0) | 3,989 (all accept-invalid) | 21 (all base-accept→tip-reject, all oracle-invalid) |
| base40 vs base40, seed 924141 | 20,000 | 19,750 | 250 | 0 | 0 | 4,015 (all accept-invalid) | 4,015 | 0 |
| base40 vs base40, seed 42001 | 20,000 | 19,720 | 280 | 0 | 0 | 3,989 (all accept-invalid) | 3,989 | 0 |

**Does tip41 reproduce the closure?** Yes — exactly, at the closure's own seed 924141 and its 20,000 values. The closure (`corpus/lessons/round-41-verifier-spotcheck.md:85-96`) recorded for base `4de35f8c…` vs tip `50287ac6…`: 19,750 in-class; base disagrees with the oracle 4,015, all accept-invalid; tip disagrees 0; tip rejects an oracle-valid value 0; tip accepts what base rejects 0; 250 out-of-class, 24 changed, all base-accept→tip-reject and all oracle-invalid. My run reproduces each number digit for digit (same loc pool, same RNG stream, same insertion table) — the method is reusable, not merely similar. The closure's **0/0** (reject-valid 0, new-accept 0) and **0 in-class disagreements** for the tip both hold: `validReject 0`, `newAccept 0`, `oracleDisagree 0` at 924141 and, independently, at 42001.
The base40-vs-base40 self-run controls the probe: `validReject 0`, `newAccept 0`, `outOfClassChanged 0`, and `oracleDisagree` = base's own 4,015 accept-invalid disagreements — the probe detects disagreement, does not manufacture it, and the oracle-side count is stable across seeds and orientations.

**Per checked statement (holds / overstated / wrong)**
- H4 harm clause — "the build rejects no value that both the round-40 tool and the oracle accept, and accepts no value the round-40 tool rejects" (`SCORECARD.md:2983-2987`) — on tip `50287ac6…` vs `4de35f8c…`: **holds** on this probe method (validReject 0, newAccept 0, two seeds, 40,000 values). Scope: the mutated-loc population of the retained sitemaps under the closure's in-class rule; not arbitrary URLs, IP-literal contents or ports above 65535 (excluded by that rule).
- "The closure's probe method is reusable for arbitrary candidate/base pairs": **holds** — one CLI, both tools imported by path, pinned wheel, JSON receipt, exit 2 on any precondition failure (missing tool, missing `_parse_url`, wheel sha mismatch, empty loc pool); reproduces the closure's own row.
- "The round-41 tip has 0 in-class oracle disagreements; the round-40 base has 4,015": **holds** — reproduced at 924141 (4,015) and 42001 (3,989), all accept-invalid.
- "The closure's method is complete evidence about URL judgment": **overstated** if read that way — a lexical URI check over 39,080 real loc values, with 250–280 of every 20,000 values out-of-class by construction; my receipts quantify that remainder.

**Risks / gaps**: closure reproduced only at its seed/count (924141 / 20,000; 42001 is my own second point); `out_of_class` copied verbatim, class boundary not re-derived; both tools share one interpreter (both guarded by `if __name__ == "__main__"`); no tools installed (python3 3.14.8 + vendored wheel sufficed).

**Scope**: read `.ufo/waves/round-41/realrun/sitemaps/`, `corpus/lessons/round-41-verifier-spotcheck.md`, SCORECARD.md round-42 C1 block, shared `tip41.py`/`base40.py`/wheel, closure probe; wrote this report and `/fast/scratch/hyaku/kake-r42w1/ExecH4Probe/{h4_probe.py, r42w1-ExecH4Probe/*.json, tmp/}`. No other lane file touched; no git/jj write.
