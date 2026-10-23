# ExecRobotsSelftest — kake r38 wave 1 (build), operability

Seat: `KakeR38.ExecRobotsSelftest`. Sandbox: `/fast/scratch/hyaku/kake-r38w1/ExecRobotsSelftest/`.
Deliverables (only write paths; L1 copies after review):
- extended selftest `/fast/scratch/hyaku/kake-r38w1/ExecRobotsSelftest/robots_audit_selftest.py`
  sha256 `bab98f444bdb6b10a375652977beb083c1d28adbed9b60b1857f36f0bec508c1` (1295 lines)
- blind mini implementation `/fast/scratch/hyaku/kake-r38w1/ExecRobotsSelftest/mini.py`
  sha256 `cb7ec732acf2a225d6c413eba40021d058560f459891acf00f37c609a5bfa8d2` (298 lines)

## Built
1. `robots_audit_selftest.py` = the 2dab7f31… selftest (137 fixtures) + 57 new fixtures, written
   blind from the SCORECARD contract text (r37 C1 (a)-(g) + r38 amendments (h)(i)(k)). 137
   originals verified unchanged (same-name comparison of the loaded fixture tables: zero missing,
   zero changed; indices 0-129 byte-equal; u01-u07 unchanged, just reordered). New contract keys
   `h`, `i`, `k`, `c-exact`, `d-match` quote the sentences; per-key minimums enforced at run
   time (h≥6, i≥20, k≥8, c-exact≥4, d-match≥4). 194 fixtures.
2. `mini.py` = from-scratch (a)-(g)+(h)(i)(k), same text, never reads the lane tool. Strict JSON
   via `parse_constant` rejection of NaN/Infinity/-Infinity; integers of any length via
   `parse_int` cap 4096 digits → out-of-range marker (linear, 64 MiB digits safe); 1e400 stays a
   float; URL character judge before parsing; implicit /robots.txt allow on the normalized path
   (empty-query clarification); ASCII-only group-name folding (Kelvin sign not folded); linear
   wildcard prefix matcher (no regex backtracking).

## New fixtures
- (h) 10: NaN/Infinity/-Infinity top-level (h01-h03) and in a check field (h04-h05) →
  `input_invalid`, null check, 0 evaluated; literals inside strings valid + 6000-digit unused
  number (h06); 5000-digit and −5000-digit status → `check_invalid`, other checks still evaluated
  (h07, h10); 6000-digit unused number changes nothing (h08); `1e400` status → `check_invalid`
  (h09).
- (i) 26: one per excluded ASCII class — space (path/leading/trailing/query/fragment/host,
  i01-i06), controls NUL/U+0001/TAB/LF/CR/U+001F (i07-i12), DEL (i13), `" < > \ ^ ` { | }`
  (i14-i22); non-ASCII kept + evaluated (i23); `%7C` kept and valid (i24); lone `%` not followed
  by two hex allowed (i25); full reserved set allowed (i26). i23-i26 pair the valid sentence-check
  with a space-URL check so base fails the fixture.
- (k) 9: `%2E`/`%2e`/`%72` spellings allowed (k01-k03); kept `%2F`, query, other case decided
  by rules, fragment not part of path, empty query normalizes to /robots.txt, 5xx disallows
  /robots.txt (k04-k09). k04-k09 pair with an escaped-dot allowance check so base fails them.
- (c)/(d) departure pins (12): substring UA both ways (c21, c22); ignored `crawl-delay` does not
  end a group (c23); same-name groups combined (c24); Kelvin-sign name not ASCII `k` (c25);
  matching group with no rules (c26); `*` ranked by rule length not matched length (d18);
  `/private/` beats `/*.html` (d19); equal-length tie allow (d20); non-final `$` literal (d21);
  final `$` anchors (d22); `*` matches empty (d23). Each maps to its sentence via `contract`.

## Results
All: `python3 -B robots_audit_selftest.py --tool <T>` in sandbox, TMPDIR set, `timeout 900`.
(exit 0 clean, 1 failed):

| tool | exit | passed | fails |
|---|---|---|---|
| `mini.py` (amendments) | 0 | 194/194 | — |
| base `af43a50f` (`clone/scripts/robots_audit.py`, sha256 `944d2f51…d3e5`) | 1 | 149/194 | exactly the 45 (h)/(i)/(k) (10+26+9); zero others |
| r37 shortcut `CtlC1Shortcut-followup-robots_audit.py` (sha256 `61724ead…6f7d`) | 1 | 150/194 | h06-h10, all 26 (i), c21, c25, d18-d21, + b09, b10, c10, c12, d07, d13, d17 |
| r37 independent `independent_robots_audit.py` | 1 | 149/194 | exactly the same 45 (h)/(i)/(k) |
| stock-urllib `CtlC1NaiveReader-robots_audit.py` (sha256 `fdc64538…13491`) | 1 | 155/194 | 5 (h), 10 (i), k05, k08, c21, c23, c25, d18-d21, + 17 pre-existing |

Result JSON in sandbox: `r38-mini.json` `f9bf41f0…`, `r38-base.json` `39996dad6d…`,
`r38-shortcut.json` `39b3107dd3…`, `r38-ind.json` `d211173ddb…`, `r38-naive.json`
`efc6e460ac…`.

## Findings (advisory)
- Base fails exactly the (h)/(i)/(k) fixtures (45/45) and passes all 12 new (c)/(d) fixtures:
  the selftest separates the three amendments from the r37 surface.
- (h): base accepts NaN/Infinity/-Infinity (evaluates) and treats 5000+/6000-digit integers as
  not-JSON (`input_invalid`) because `json.loads` hits the 4300-digit int limit; amendments
  require valid JSON + `check_invalid`. `1e400` already handled by base (float → check_invalid).
- (i): base accepts every excluded ASCII char everywhere (all probed clean), so all 26 fail.
  `%7C`, `%zz`, reserved chars already accepted/evaluated.
- (k): urllib 3.14 already implements the implicit allow on the normalized path
  (`normalize_uri` + `can_fetch` `/robots.txt`), so the shortcut passes all 9; (k) separates the
  base lane tool, not a stdlib delegator (naive k-fails = 2: k05, k08).
- stdlib departures confirmed: substring UA (c21), Kelvin-sign folding (c25), matched-length
  ranking (d18-d20), non-final `$` dropped (d21). c23 is fixed by the shortcut's non-record-key
  patch; c24 does not separate (3.14 merges same-name groups), it pins the contract rule.

## Risks / blockers
- The 5 long-integer (h) fixtures require the build to raise/bypass the int-conversion limit;
  default `json.loads` on a 6000-digit manifest gives `input_invalid` (measured — the base's
  defect).
- (c)/(d) fixtures are stdlib-separating on Python 3.14.8 (the lane's version).
- Did not run sealed counters (no key), did not touch sealed trees, did not read the builder's
  tool, wrote nothing outside sandbox + this report. No tool installs/updates performed.
