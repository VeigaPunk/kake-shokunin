# Round 42 lesson review (KakeR42.ReviewLesson, wave 2 falsify)

Verdict: PASS — every pointer in `corpus/lessons/round-42.md` resolves and every quoted
line matches the cited source. No broken pointer found. Minor wording caveats below.

## Pointers verified

- Commit hashes all resolve to the stated commits: `9e3c31d2`, `0c5ad2f6`,
  `2653b629`, `d1c3f372`, `c23c145c`, `1ef7a0e9`, `020bc457`
  (`git rev-parse --short=8` each; messages match the lesson's description).
- `SCORECARD.md` sections exist at the cited commits: "Round 42 — C1 counter
  candidate" at `d1c3f372` (line 2907 there) and "counter v2 replaces v1" at
  `c23c145c` (line 2993 there); "counter v3 replaces v2" and C1 declared/tally at
  tip. "Equivalence differential (decided now)" text is at `d1c3f372`
  (line 2968).
- `corpus/lessons/round-41-verifier-spotcheck.md` exists; cited lines read as
  quoted: 64–72 (13/42 guards green on base, cost unpriced), 159–161 (routed
  defect 1), 131–133 (S117–119 `anchor`/`teaches` in-place edits at
  `2653b629`/`0c5ad2f6`, rule-2 append-only).
- `corpus/SOURCES.md` S117–S125: S117–S119 cells field-for-field equal
  `git show 9e3c31d2:corpus/SOURCES.md` except `used-by` (verified by Python
  comparison); S120/S121/S122 `teaches` open `supersedes S117/S118/S119 —`;
  S125 status `rejected`; `git diff 1ef7a0e9 HEAD -- corpus/SOURCES.md` touches
  only S117–S125 rows (+9/−3).
- Rule-2 quote matches `…/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`
  lines 114–119 ("Only `status`, `recheck` and `used-by` change in place … A
  correction is a new row whose `teaches` opens `supersedes S0NN —`").

## Gate quotes (all verbatim in the stored bodies; sha256 match SHA256SUMS)

- S120 rfc3986.txt line 867 `URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]`; body sha256 `3102dae4…d683` = S098/S117 pin; 141,811 bytes.
- S121 abnf PyPI: `info.summary` "Parsers for ABNF grammars."; wheel sha256 `cdcac127…0917`; 8,215 bytes.
- S122 rfc3987 PyPI: `info.summary` "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)"; wheel sha256 `10702b1e…ce53`; 9,900 bytes.
- S123 re.html: "these do not allow back-tracking when the expression following it fails to match" (lines 359–360, inside cited 357–373); "Added in version 3.11." at line 373; body sha256 `1559698e…8f17e2` = ScoutPythonRe fetch; 251,811 bytes.
- S124 rfc9844.txt: line 192 "This document completely obsoletes [RFC6874]"; 195–196 "reverts the change that it made to the URI syntax"; BOM present; 19,292 bytes; sha256 `7585b9a9…c4b135` = ScoutRFC6874.
- S125 rfc6874.txt line 200 `ZoneID = 1*( unreserved / pct-encoded )`; 19,361 bytes; sha256 `5f54b04f…9380d5` = ScoutRFC6874; info page Obsoleted by RFC 9844.

## Reject/counter bytes

- draft1 `5478e4f3…` = `draft1/c42_count_draft1.py` sha256; receipt
  `draft1/donothing-tip-42001-draft1.json` has `met: true`, ratios 0.824–1.333,
  counterSha256 `5478e4f3…`; draft1 code uses bwrap
  `RUSAGE_CHILDREN` and path-fill alphabet of 79 chars → `/` ≈ every 80 chars.
- v1 `7bfc32c5…`, v2 `01d3fb8d…`, v3 `ce2d5a0c…` = file sha256 of
  `c42_count{,_v2,_v3}.py`. v3 has absolute bwrap, OSError catch, stdin
  /dev/null, `RLIMIT_FSIZE` 256 MiB, PATH-only env.
- `ExecBuildRegex` tool `8a30432d…`: reproduced `PASS 0/235` exit=1 under
  Python 3.10.22 (current 235-fixture selftest; 225 at reject time) — quote
  "PASS 0/225 … possessive quantifiers need 3.11" holds. Final build tool
  `914ebdee…` = current `scripts/sitemap_audit.py`; tip41 `50287ac6…`,
  base40 `4de35f8c…` match shared paths.
- `harm_rule_check.py` behavior reproduced: `git show 1ef7a0e9:SCORECARD.md |
  harm_rule_check.py - 41` → exit 1, stdout byte-equal `harm-rule-r41.txt`;
  `harm_rule_check.py SCORECARD.md 42` → exit 0, byte-equal `harm-rule-r42.txt`.
- 86 v3 receipts in `verification/w1v3/`: 3 met (portpct, mutant_empty_host,
  mutant_port_letters); the five v1-witness tools (three non-ASCII, `~` zone,
  `\d` percent) and `ctl_fake_timing` are not met under v3 — matches
  SCORECARD tally ("Under v1, 9 receipts met …").

## Caveats (low severity)

1. Lesson line 28 "`used-by` of S117–S119 stays `SCORECARD.md, corpus/lessons/round-41.md`" is literal only for S117; S118/S119 `used-by` are `.ufo/waves/round-41/c1_count.py, SCORECARD.md` and `.ufo/waves/round-41/oracle_crosscheck.py, SCORECARD.md` (unchanged from round 41 apart from the dropped "Round 41" title). Shorthand, not a broken pointer.
2. Mistake 4's "notice went to five live seats" count is not evidenced in repo artifacts; `w1-dispatch-log.txt` confirms a deadline notice at 11:41Z (18 min before the 11:59Z settle line) corrected at 11:42Z.
3. At-typing: the 11:41Z notice was a "deadline passed" text, per the lesson; the log only says "deadline notice … misread the clock".

## Verification gaps

- HTTP status 200 and the 11:24:53Z fetch time of the L1's own fetches were
  not re-fetched (offline review); bodies/sizes/hashes match the recorded pins
  and the wave-1 scout notes (ScoutPythonRe, ScoutRFC6874).
- Constructor "5 live seats" detail above.
- Not judged: S123's admit framing ("grounds the build technique") vs the later
  rejection of the possessive-quantifier build — a decision question, outside a
  pointer/quote review (cf. ReopenPythonRe).
