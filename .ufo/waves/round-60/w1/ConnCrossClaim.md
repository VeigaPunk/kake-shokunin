# ConnCrossClaim

SEPARABILITY:
- Declared Status: contract.md (§Axis declaration, lines 41–46) asserts C1, C2, and C3 are causally separable: C1 reads SKILL.md/SCORECARD.md and runs the 28 historical/live population counters (rounds 48–59); C2 tests scripts/append_guard.py against synthetic fixtures K1–K22 and real-lane history fd6303ce..rev; C3 checks its new rows (S427–S429), receipts, and googlebot-verification.md correction.
- Operational Reality (Asymmetric Coupling):
  1. C3 is autonomous: c60_quote_truth.py evaluates only sources, receipts, registry mirrors, and condition C9. It executes neither C1's gate suite nor C2's guard cases. C3 can land and pass 9/9 independently of C1 and C2.
  2. C1 is causally dependent on C3: c59_quote_truth.py is a member of C1's 28-counter population. Its condition C8 requires registry rows to equal mirror rows (162) + 2 = 164. C3 appends S427–S429, raising registry rows to 167. On the round-60 measured tree, c59_quote_truth.py deterministically exits 1. At base, c59 is registered in SKILL.md as live (line 1309). If C3 lands, C1 will fail (live_not_green) unless SKILL.md simultaneously relabels c59 as historical with a valid ancestor pin. Conversely, if C1 relabels c59 as historical before C3 lands (or if C3 fails to land), c59 remains green at tip (164 rows), failing C1 with historical_but_green.
  3. C2 is causally exposed to C3 via case R1: c60_guard_cases.py runs append_guard.py across --base fd6303ce.. --revision <rev> on corpus/knowledge/**/*.md. This commit range encompasses C3's in-file insertion in googlebot-verification.md. If C3 introduces any base-line mutation, base-line deletion, CRLF conversion, untagged insertion, tag placed on line 2+ of the run, or tag inside backticks/comments, C2 case R1 detects changed or untagged_insertion and exits 1, failing C2 (23/24).
- Separability Verdict: C1 and C2 cannot be verified independently of C3 on the measured revision. C3 can land alone, but C1 and C2 succeed only if C3's mutations land with coordinated precision.

SHARED WEAKNESSES:
- Scratch & Subprocess Concurrency:
  1. C1 spawns 28 subprocesses, each executing git clone --shared in /fast/scratch/hyaku/ with an 1800s timeout per counter.
  2. C2 executes 22 git init scratch fixture repos plus 2 lane clones for cases R1/R2.
  3. All three claims execute under /fast/scratch/hyaku/. Scratch I/O saturation, clone locking, or disk contention during wave execution risks timeout (exit 124) or clone failure (exit 2).
- Environment Variable Leakage:
  All three counters rely on git subcommands and require scrubbing of inherited GIT_* variables (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE), as routed in round 58 defect D2. Any unscrubbed GIT_* variable causes tool commands to resolve the host repository instead of the scratch clone.
- Common Tracked Surfaces:
  1. corpus/knowledge/: modified by C3 (googlebot-verification.md, new entries), scanned by C2 (append_guard.py default scope), and parsed by C1 population gates (c55_readme_index, c58_quote_truth, c59_quote_truth).
  2. corpus/SOURCES.md: appended by C3, mirror-checked by C3, and parsed by C1 population counters (c56 through c59).
  3. SKILL.md: read directly by C1; tested as an out-of-scope negative control by C2 (case K17).
- Shared Tooling & Runtime:
  All three counters rely on stdlib python3 -B (hashlib, re, shlex, subprocess, json). Parsing divergences, regex discrepancies, or platform differences affect all three surfaces.
- Single-Commit Atomicity:
  All claims are measured at tip commit <rev>. A partial landing commit where C3 lands without C1's SKILL.md relabels, or C2 lands without C3's knowledge correction, breaks the integrated state.

INTERACTIONS:
- C3 -> C1 (Row Append vs Gate Status):
  c59_quote_truth.py checks C8: registry rows == mirror rows + 2. When C3 appends S427–S429, the row count becomes 167, causing c59 to fail (exit 1). SKILL.md row 1309 currently marks c59 as live. C1 requires 0 mismatches across 28 counters. C3's row append mandates that C1 relabel c59 to historical, pinned to the round-59 measured commit.
- C3 -> C2 (Knowledge Correction vs Append Guard):
  C3 condition C9 inserts an append-only block into googlebot-verification.md containing [r60-correction 2026-10-27] and quoting S428. C2 case R1 tests append_guard.py between round-58 spotcheck base fd6303ce and <rev>. If C3 alters any base line in googlebot-verification.md, misplaces the tag on line 2 of the run, or wraps the tag in backticks or HTML comments, C2 fails on R1.
- C2/C3 -> C1 Historical Gate Preservation:
  In round 59, the in-file correction in crawler-identity.md broke c55_readme_index.py's byte-prefix rule (head_changed=1, routed defect R59-D1). In round 60, C2's new append_guard.py validates tagged corrections to prevent future false positives, while C1 ensures c55 remains historical and does not turn red again.

PATTERN:
- Pattern to Avoid: Cascading Red Gates via Uncoordinated Cross-Claim Mutations.
- Evidence across Rounds 55–59:
  1. Round 56/57: Round 56 added S419/S420; Round 57's row growth broke c56_quote_truth.py (6/8 met=False, defect D3) because mirror rows were hard-pinned. It was carried forward as "red by design" without formal historical pinning.
  2. Round 58: c56_quote_truth.py remained failing at base and tip (6/8 met=False), but SKILL.md still claimed 0=met (stale premise mistake, line 113).
  3. Round 59: Claim C3's in-file correction in crawler-identity.md broke live gate c55_readme_index.py (head_changed=1, R59-D1). Attempt 1 landed without contract notes or pre-data relabeling, forcing an emergency mid-round retirement of c55 to historical.
  4. Rounds 55–58 Receipt Drift: Placeholder and post-commit receipt rewrites (r55 c1-selftest-v2, r56 §6.1 after-c1-selftally, r57 D1 after-c1-receipt-pins pending rewrite, r58 19 undisclosed receipt edits).
- Round 60 Application:
  Do not land C3's row additions or knowledge modifications in isolation. The round-60 build must atomically bundle C3's entries/appends, C1's honest relabeling of c59_quote_truth.py to historical with its 40-hex pin, and C2's compliance verification of googlebot-verification.md under append_guard.py, committing receipts once without placeholders.

VERDICT: C1, C2, and C3 are causally coupled through C3's mutations (C3 row appends require C1 c59 relabel; C3 in-file correction exercises C2 R1); cross-claim atomicity avoids the rounds 55-59 cascading gate-collision pattern.