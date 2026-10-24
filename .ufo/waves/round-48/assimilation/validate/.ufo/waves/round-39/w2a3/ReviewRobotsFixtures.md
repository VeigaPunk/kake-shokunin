# ReviewRobotsFixtures — r39 w2 attack on ExecRobotsDeclaredFixtures (operability)

Target: `/fast/scratch/hyaku/kake-r39a3w1/ExecRobotsDeclaredFixtures/robots-selftest.patch`
(sha256 `f4f1685c149ef2335b57328d256e66f60a9596c6b89fb81fc82307893bc997b2` — matches report :8).
Sandbox: `/fast/scratch/hyaku/kake-r39a3w2/ReviewRobotsFixtures/` (clone of lane tip bb4a1e1).

## Commands / exits (all `TMPDIR=/dev/shm timeout 400 prlimit --as=4000000000 --`)
- `git apply --check <patch>` → 0; applied `scripts/robots_audit_selftest.py` sha256
  `ea069396f560297200a472b7944d39520401c3ffad7bdd582baae21a19f48622` — matches report :10-11.
  `git status --porcelain`: only ` M scripts/robots_audit_selftest.py`.
- `scripts/robots_audit.py` sha256 `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace` (pre- and post-apply) — "untouched" confirmed.
- Extended selftest, pristine: `python3 scripts/robots_audit_selftest.py` → exit 0, `{"passed":204,"cases":204}`, 5.7 s.
- Baseline selftest (`git show HEAD:scripts/robots_audit_selftest.py` → `/tmp/st_base.py`, sha
  `bab98f44…c508c1` = report :11), pristine `--tool` → exit 0, 194/194.
- Mutants (`--tool`): extended-run totals/failures; baseline-run totals:
  | mutant (sha256 verified = report :44-45,:18) | ext 204 | kills | base 194 |
  | m_emptyq `ed00b962` | 201/204 exit1 | e03,k05,+k10 | 192/194 (e03,k05) |
  | m_barepct `f20d1bf8` | 202/204 exit1 | i25,+i27 | 193/194 (i25) |
  | m_explicit `e11073ae` | 197/204 exit1 | k04-k09,+k11 | 188/194 (k04-k09) |
  | m_unguarded `e7907567` | 203/204 exit1 | h11 TimeoutExpired 20 s | 194/194 exit0 |
  | H03 `8f8add5a` (abs) | 203/204 exit1 | h12 exit0≠2 | 194/194 |
  | H04 `f50ab442` (%1000) | 203/204 exit1 | h13 exit0≠2 | 194/194 |
  | I13 `78616821` (`_` in forbidden RE) | 203/204 exit1 | i28 exit2≠1 | 194/194 |
  | I16 `a51f8068` (isprintable) | 203/204 exit1 | i29 exit2≠1 | 194/194 |
  | K08 `d3fcdc23` (scheme==https) | 203/204 exit1 | k12 exit1≠0 | 194/194 |
  | K09 `b30ef0a1` (endswith) | 203/204 exit1 | k13 exit0≠1 | 194/194 |
  Each mutant fails **exactly** its mapped new fixture (+ pre-existing kills retained). Confirmed.
- Mutant diffs vs pristine tool verified one-line each: H03 `abs(int(token))`, H04 `%1000`,
  I13 adds `_` to `_URL_FORBIDDEN_RE`, I16 `isprintable()`, K08 `and parts.scheme=="https"`,
  K09 `path.endswith(IMPLICIT_ALLOWED_PATH)` — mutation descriptions accurate.

## Expected values vs contract (`git show 2909f1dc:SCORECARD.md`; `corpus/knowledge/robots-txt-rules.md`)
- h11 (:895): 64 MiB = cap boundary, not "larger than 64 MiB" ((g), :1854); 20 s = counter bound
  (:2150-2151,:2253); "unread" field + giant int → "changes nothing" (:2150). Holds; exit0/eval0/timeout20 correct.
- h12 (:898) −200, h13 (:904) 1200: integer status outside 2xx/4xx/5xx → that check
  `check_invalid`, "other checks still evaluated" (:2148-2151) → exit2, eval1. Holds.
- i27 (:965): `%` + trailing `%` kept by (i)/(e) (:2255); robots `/a%` blocks URL `/a%` → k1
  blocked (expect=allow default :269), k2 space → check_invalid; exit2. Holds.
- i28 (:971): `_` in allowed list (:2154); pristine exit1 blocked. Holds.
- i29 (:975): non-ASCII "kept" (:2153); NBSP written raw UTF-8 into rule+URL → rule matches →
  blocked; expect "judged as written" is exactly what pristine does. Holds.
- k10 (:1034): `/robots.txt?` empty query → path `/robots.txt` allowed (:2255-2256); `disallow: /`
  → exit0 eval1. Holds (overlaps k05/e03 by design — report :47-48 discloses).
- k11 (:1038): explicit `Disallow: /robots.txt` does not override implicit allow (:2256-2257);
  exit0. Holds.
- k12 (:1042): implicit allow is on normalized path, scheme-agnostic (:2158-2160); manifest
  "absolute http(s) URL" (knowledge :67) makes http input valid → exit0. Holds.
- k13 (:1046): only *exactly* `/robots.txt` (:2159); `/nested/robots.txt` decided by `disallow: /`
  → blocked exit1. Holds.
- Mechanism: `timeout=` param (applied :234,:256) → `run_case` uses `fixture["timeout"]` (:1203);
  CONTRACT keys h-bound/i-clar/k-clar (:193-206) quote clarifications verbatim vs :2253-2257;
  MIN_BY_CONTRACT 1/1/2 (:75-79) — confirmed in perContract output.
- Coverage note: `git apply --check` and file sha verified; report's `cmp`-identical claim
  corroborated by identical post-apply sha256.

## Per attacked statement
holds — every table row (fixtures :30-39), mutant-kill mapping, baseline totals (:16-19), 204/204
(:20), hash claims, "exactly one new fixture" (:45), disclosure that only h11+m_unguarded and six
survivors were genuinely uncovered (:47-50), citation line numbers (±1-2 lines, region-accurate).
overstated — patch docstring :10-13 says "each one kills the reference mutant that breaks exactly
it" (reads as exclusivity; e03/k05/i25/k04-k09 also kill the m_* mutants) — report's own finding (1)
discloses this, so mild. No wrong statement found.

Residual risk: per-run JSON receipt shas not re-hashed (regenerated equivalent runs instead);
h11 uses subprocess-level timeout (no in-tool watchdog needed — contract bounds the counter's
invocation). No installs, no lane mutation beyond this report.
