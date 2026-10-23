# Round 42 — the round-41 URL rule priced: cost bound, declared zone-id behaviour, corrected harm rule

author: kake L1, round 42 attempt 1 (KakeR42)

Claim and rules: `SCORECARD.md` "Round 42 — C1 counter candidate" (pre-freeze, `d1c3f372`) and "Round 42 —
counter v2 replaces v1 before freeze" (`c23c145c`). Base `1ef7a0e9`. Outside check of round 41:
`corpus/lessons/round-41-verifier-spotcheck.md` (not edited here; every routed defect is answered below).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-42/sources/`, sums in `SHA256SUMS`
there; fetched 2026-10-23T11:24:53Z; each body equal to the wave-1 scouts' fetches).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S120 | https://www.rfc-editor.org/rfc/rfc3986.txt | 2026-10-23T11:24:53Z, HTTP 200, 141,811 bytes, sha256 `3102dae4…d683` (= S098, S117) | "URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]" (line 867) | admit — superseding row for S117 (routed defect 4) |
| S121 | https://pypi.org/pypi/abnf/2.9.1/json | 2026-10-23T11:24:53Z, HTTP 200, 8,215 bytes, sha256 `d1dab17e…d10d` (= round 41) | "Parsers for ABNF grammars." (`info.summary`); wheel digest `cdcac127…0917` | admit — superseding row for S118 |
| S122 | https://pypi.org/pypi/rfc3987/1.3.8/json | 2026-10-23T11:24:53Z, HTTP 200, 9,900 bytes, sha256 `f624f451…2e8d2e` (= round 41) | "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)" (`info.summary`); wheel digest `10702b1e…ce53` | admit — superseding row for S119 |
| S123 | https://docs.python.org/3/library/re.html | 2026-10-23T11:24:53Z, HTTP 200, 251,811 bytes, sha256 `1559698e…8f17e2` | "these do not allow back-tracking when the expression following it fails to match" (lines 357–373; "Added in version 3.11.") | admit — grounds the build technique |
| S124 | https://www.rfc-editor.org/rfc/rfc9844.txt | 2026-10-23T11:24:53Z, HTTP 200, 19,292 bytes, sha256 `7585b9a9…c4b135` | "This document completely obsoletes [RFC6874]" (line 192); obsoleting it "reverts the change that it made to the URI syntax" (195–196) | admit — grounds the declared zone-id behaviour |
| S125 | https://www.rfc-editor.org/rfc/rfc6874.txt | 2026-10-23T11:24:53Z, HTTP 200, 19,361 bytes, sha256 `5f54b04f…9380d5` | "ZoneID = 1*( unreserved / pct-encoded )" (line 200) | **reject** — obsoleted by RFC 9844 (S124); cannot ground current URI syntax |

Row changes this round (CORPUS.md §SOURCES.md rule 2: only `status`, `recheck`, `used-by` change in place; a
correction is a superseding row whose `teaches` opens `supersedes S0NN —`):

- S117 `anchor` and `teaches`, S118 `teaches`, S119 `teaches`: the in-place edits of round 41 (`2653b629`,
  `0c5ad2f6`) are reverted to the cells committed at `9e3c31d2`; the corrected text is carried by S120, S121,
  S122 (`w1/ScribeSupersedingRows.md`). `used-by` of S117–S119 stays `SCORECARD.md, corpus/lessons/round-41.md`
  (an allowed change, logged in round 41).
- S120–S125 added (5 admitted, 1 rejected). No other `status`, `recheck` or `used-by` change.

Rejects this round (each recorded before the build was scored):

- **Rejected: counter draft 1** (`draft1/c42_count_draft1.py`, `5478e4f3…`). Reason: the do-nothing tool met
  it (ratios 0.82–1.33): CPU was read from bwrap's `RUSAGE_CHILDREN` (1–2 ms per sample) and `/` every ~80
  characters bounded the round-41 regex's slow scan.
- **Rejected: counters v1 (`7bfc32c5…`) and v2 (`01d3fb8d…`) as C1's instrument.** Reason: wave-1 controls
  met v1 with witnesses (non-ASCII range ×3, `~` in a zone id, `\d` in a percent triplet, tail-window
  shape-keyed ×2, seed-keyed table, keyed manifest) or by forging CPU (`ctl_fake_timing`); v2 kept the same
  gaps. Counter v3 (`ce2d5a0c…`) was frozen instead; 86 control receipts, 3 meet, all three behaviour-equal
  by the frozen differential.
- **Rejected: RFC 6874 (S125) as the ground for zone-id behaviour.** Reason: obsoleted by RFC 9844 (S124).
- **Rejected: build `ExecBuildRegex`** (`8a30432d…`) as the landed build. Reason: `PASS 0/225` under
  Python 3.10.22 (possessive quantifiers need 3.11); the contract names no version floor.

## Routed defects of round 41 (closure `corpus/lessons/round-41-verifier-spotcheck.md`)

1. Harm-rule design → QUALITY (v) with a check red on round 41 and green on round 42; the round-42 harm rule
   declares "guards only" and a 2.0 cost bound before data.
2. Disposition of the URL rule `50287ac6…` → kept and declared (zone ids with non-ASCII or `|` rejected,
   grounded in S124), its cost repriced under C1, no-harm re-established under H1–H5 (SCORECARD round 42).
   Round 41 itself stays rejected-harmed; the 29/13 fixture split is a historical observation.
3. Tool comment → corrected at `scripts/sitemap_audit.py:67-74` in build `020bc457`.
4. S117–S119 → cells restored to `9e3c31d2`, superseding rows S120–S122 (Gate above).
5. Counter v2's known defects → fixed in this round's counters (absolute bwrap path and `OSError` caught,
   stdin `/dev/null`, stdout capped by `RLIMIT_FSIZE`, PATH-only environment); equivalence decided by a
   differential frozen at `d1c3f372`. Round-41 counter v2 itself is not frozen and decides nothing.
6. Open outside C1 → symlinked manifest `file` paths: reproduced, contract silent, fix outline recorded
   (`w1/ScoutSymlinkManifest.md`; next round's candidate). `source_recheck.py` Appendix-B reading: not
   worked this round.

## Mistakes

1. **Class: harm rule unmeetable by construction (round 41).** Evidence: `corpus/lessons/round-41-verifier-spotcheck.md:64-72,159-161`
   (13 of 42 new fixtures were guards, green on the base, under a rule demanding all red; cost unpriced).
   Captured-by: none in round 41 (the outside spot-check found it). Fix: QUALITY (v); able to fail —
   `harm_rule_check.py` exits 1 on round 41's SCORECARD bytes and 0 on round 42's
   (`.ufo/waves/round-42/verification/criteria/harm-rule-r4{1,2}.txt`).
2. **Class: counter weaker than the claim, three times in one round (this round).** Evidence: draft 1 met by
   the do-nothing tool (`draft1/donothing-tip-42001-draft1.json`, `met: true`); v1 met by nine wave-1
   controls with witnesses or a forged timing line (SCORECARD "Round 42 — counter v3 replaces v2").
   Captured-by: §9 / QUALITY (o) pre-freeze control rule — it worked: every gap was found before the build
   was scored. Fix: QUALITY (w) (timing channel the tool cannot write) and (x) (every repertoire unit and
   Unicode look-alike in every slot); able to fail — `ctl_fake_timing` meets v1 and fails v3; the five
   repertoire mutants meet v1 and fail v3 (`verification/w1v3/`).
3. **Class: in-place edit of committed SOURCES cells (round 41).** Evidence: closure lines 131–133;
   `git diff 9e3c31d2 0c5ad2f6 -- corpus/SOURCES.md`. Captured-by: CORPUS.md §SOURCES.md rule 2, not
   gated by the census. Fix: cells restored and superseding rows S120–S122 this round; able to fail — the
   restored cells equal `git show 9e3c31d2:corpus/SOURCES.md` field for field except `used-by` (checked by
   wave-2 `ReopenRFC3986Rows`, `ReopenPyPIRows`, `ReviewSourcesRule2`); no automated gate exists yet (open).
4. **Class: wrong clock read by the L1 (this round).** Evidence: `w1-dispatch-log.txt` settle line; a
   "deadline passed" notice went to five live seats at 11:41Z, 18 minutes early, corrected at 11:42Z.
   Captured-by: none. Fix: read `date -u` before any deadline message (applied for the rest of the round).
