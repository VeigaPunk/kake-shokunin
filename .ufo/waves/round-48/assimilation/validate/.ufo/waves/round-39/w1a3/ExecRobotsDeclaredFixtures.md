# ExecRobotsDeclaredFixtures — round-39 wave 1 (leaf, operability)

Built: named fixtures for the round-38 declared-but-untested sentences (defect 3,
`corpus/lessons/round-38-verifier-spotcheck.md:174-176`) in the robots selftest only; `scripts/robots_audit.py`
untouched (sha256 `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace` before and after).

Deliverable: `/fast/scratch/hyaku/kake-r39a3w1/ExecRobotsDeclaredFixtures/robots-selftest.patch`
sha256 `f4f1685c149ef2335b57328d256e66f60a9596c6b89fb81fc82307893bc997b2` (156 lines,
standard `a/` `b/` prefixes; `git apply --check --reverse` in the clone exit 0).
Applied selftest bytes: `/fast/scratch/hyaku/kake-r39a3w1/ExecRobotsDeclaredFixtures/clone/scripts/robots_audit_selftest.py`
sha256 `ea069396f560297200a472b7944d39520401c3ffad7bdd582baae21a19f48622` (was `bab98f44…c508c1`, 194 fixtures; now 204).
Patch applies clean: `patch --dry-run -p1 -d patchcheck < robots-selftest.patch` exit 0; applied file `cmp`-identical.

Commands (all with `TMPDIR=/dev/shm timeout 300 prlimit --as=4000000000 --`):
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone` (GIT_* unset) → 0.
- unchanged selftest, pristine tool: 194/194 clean, exit 0.
- unchanged selftest, four reference mutants (`/fast/scratch/hyaku/kake-r38w2/CriticKeyExpectations/mutants/`,
  hashes equal the published `ed00b962/f20d1bf8/e11073ae/e7907567`): m_emptyq 192/194, m_barepct 193/194,
  m_explicit 188/194 (all exit 1); m_unguarded 194/194, exit 0 — the only genuine survivor.
- extended selftest (204), pristine tool: 204/204 clean, exit 0 (9.0 s wall).
- extended selftest (204), ten mutants: each exit 1, each failing exactly its mapped new fixture below.
  Per-run JSON: `/fast/scratch/hyaku/kake-r39a3w1/ExecRobotsDeclaredFixtures/runs/ext/{pristine,m_emptyq,m_barepct,m_explicit,m_unguarded,H03,H04,I13,I16,K08,K09}.json`
  (sha256 e.g. pristine `567c93c7…3896`, m_unguarded `f246e551…38ef`); baseline runs in `runs/base/`.

New fixtures (194→204; pristine passes all ten; each mutant fails its mapped new row — the three
mutants already caught by old cases also keep those failures; observed reason in quotes):

| fixture (selftest line) | contract citation | expected | pristine | mutant it kills |
|---|---|---|---|---|
| h11-64mib-integer-literal-within-20s (:895) | SCORECARD.md:2150-2151,2253 — "manifest within the 64 MiB cap … within 20 s"; unread numbers change nothing | exit 0 clean, eval 0, own 20 s timeout | pass (~0.10 s) | m_unguarded "tool could not run: TimeoutExpired" at 20 s |
| h12-negative-short-status-check-invalid (:898) | SCORECARD.md:2148-2149 — status outside ranges is check_invalid | exit 2, bad check_invalid, eval 1 | pass | H03 (abs) exit 0 "exit mismatch … observed 0" |
| h13-four-digit-status-truncation-check-invalid (:904) | same (h) sentence, "however many digits" | exit 2, bad check_invalid, eval 1 | pass | H04 (%1000) exit 0 |
| i27-bare-percent-kept-and-matched (:965) | SCORECARD.md:2152-2157,2255 — bare `%` allowed by (i), kept by (e) | exit 2, k1 blocked, k2 check_invalid, eval 1 | pass | m_barepct k1 check_invalid |
| i28-underscore-in-path-valid (:971) | SCORECARD.md:2154 — `_` an allowed character | exit 1, blocked, eval 1 | pass | I13 exit 2 |
| i29-nbsp-valid-and-normalized (:975) | SCORECARD.md:2152-2157 — non-ASCII kept, judged as written | exit 1, blocked, eval 1 | pass | I16 exit 2 (isprintable) |
| k10-empty-query-empty-path-rule (:1034) | SCORECARD.md:2255-2256 — `/robots.txt?` path to match is `/robots.txt` | exit 0 clean, eval 1 | pass | m_emptyq exit 1 |
| k11-explicit-disallow-robots-txt-does-not-override (:1038) | SCORECARD.md:2256-2258 — explicit Disallow does not override | exit 0 clean, eval 1 | pass | m_explicit exit 1 |
| k12-implicit-allow-http-scheme (:1042) | SCORECARD.md:2158-2161 — implicit allow is path-based, not scheme-based | exit 0 clean, eval 1 | pass | K08 exit 1 |
| k13-nested-robots-txt-not-implicit (:1046) | SCORECARD.md:2159-2161 — only exactly `/robots.txt` | exit 1, blocked, eval 1 | pass | K09 exit 0 |

Mechanism: `add()` gains `timeout=TIMEOUT_SECONDS` (:234, stored :256) and `run_case` uses
`timeout=fixture["timeout"]` (:1203); CONTRACT gains quoted clarification keys `h-bound`, `i-clar`,
`k-clar` (:193-206) with coverage minimums 1/1/2 (:75-79), so the new cases cannot be dropped silently.
All six `MutBuildTool` survivors (H03 `8f8add5a`, H04 `f50ab442`, I13 `78616821`, I16 `a51f8068`,
K08 `d3fcdc23`, K09 `b30ef0a1`) passed all 194 old fixtures and now fail exactly one new fixture each.

Findings/risks: (1) three of the four reference mutants were already caught incidentally by old
fixtures (e03 and k05 for the empty query, i25 for the bare `%`, k04-k09 for the explicit disallow), so
only the 20 s bound (m_unguarded, 194/194) and all six survivors were genuinely uncovered; the new
fixtures make each clarification its own isolated case with a quoted citation, and k10/k11 pin the
clarification text rather than a rule-side effect. (2) h11 holds one 64 MiB
bytes object and materialises 64 MiB per run (plus the two pre-existing 64 MiB manifests; ~192 MiB peak
temp, removed by existing `cleanup()`); the 20 s timeout includes ~15 ms interpreter start, pristine
margin ~200x. (3) Reference-mutant tools come from `/fast/scratch/hyaku/kake-r38w2/…` because the lane
copy holds only zero-byte `.err` stubs; hashes match the published ones.

No installs, no network, no lane/jj/index change; all evidence under
`/fast/scratch/hyaku/kake-r39a3w1/ExecRobotsDeclaredFixtures/` (`runs/` 128 KB). Lane run gate left to main.
