# Round 36 — source re-check audit on sealed cases

## Claims

Declared before any build in `SCORECARD.md` section "Round 36 — declared claims" (`3555f63f`).
Base `b720d799ae99c19a7c97f2b1391d4fe928be0e11`. One claim. Rounds 34 and 35 were rejected
because cheap controls met knowledge-entry counters; this round makes no knowledge-entry claim
and works a different surface: a new tool that re-checks a registry row's quote against a
recorded fetch of its source.

- C1 (freshness, capability): `scripts/source_recheck.py` meets the public contract (a)–(g).
  Frozen predicate `met: passed >= 25 of 28 sealed cases`. Before: 0 of 28 at `b720d799`,
  `3555f63f`, `9d81c75c` and `cd321279`. After: 28 of 28 at the build commit `4d5b3d55`
  (`verification/c1-at-4d5b3d55.json` with the key file before the reveal;
  `verification/c1-keyrev-at-4d5b3d55.json` with `--key-revision fd1fb723` after it). Measuring
  the reveal commit itself exits 2 (`c1-keyrev-at-fd1fb723.json`).
- The tool came from wave-1 `ExecToolBuild` (sha256 `577b2d7d…0d48`, landed unedited); the seat
  never saw the cases. An independent implementation written by wave-1 `ExecSelftest` from the
  same contract, also blind, scores 28 of 28 too (`verification/independent-selftest-reference.json`),
  so the cases follow the contract rather than one reader of it.

Pre-data history (all before the build existed): counter v1 (`3555f63f`); v2 jails the tool
(`9d81c75c`, the L1's own review: a tool could read the counter's command line through /proc);
the control wave found that key v1 let a body-blind shortcut pass every (e) and (f) case
(17 of 28 under v2), so key v2 and counter v3 (pin only) landed at `cd321279`. All receipts were
rescored under v3 before the build.

## Gate

### Source openings

Opened with `.ufo/waves/round-36/fetch_sources.py` (one public GET each; receipts and retained
text in `.ufo/waves/round-36/sources/`) at 01:08:56Z–01:09:01Z, before the declaration. Each
source was re-opened live by an independent wave-1 scout (`w1/ScoutReopenS088.md` … `S094.md`);
every retained body is byte-identical to the scout's fetch. Quotes were verified as exact
substrings of the retained text by wave-1 `ScribeGateLines` (commands in `w1/ScribeGateLines.md`).

- S088 — https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4 — accessed 2026-10-23T01:08:56Z, HTTP 200 — admit, tier A, kind spec, status mined: RFC 9110 normatively defines permanent-status URI semantics, anchoring redirect classification and final-status rules; quote “the target resource has been assigned a new permanent URI” (Section 15.4.2, 301 Moved Permanently; 10 words).
- S089 — https://www.rfc-editor.org/rfc/rfc3986.html#section-5.2 — accessed 2026-10-23T01:08:57Z, HTTP 200 — admit, tier A, kind spec, status mined: RFC 3986 supplies the normative relative-reference resolution algorithm required for each Location hop; quote “For each URI reference (R), the following pseudocode describes an algorithm for transforming R into its target URI (T):” (Section 5.2.2, Transform References; 19 words).
- S090 — https://encoding.spec.whatwg.org/ — accessed 2026-10-23T01:08:57Z, HTTP 200 — admit, tier A, kind spec, status mined: WHATWG defines byte-order-mark precedence and charset labels, including the contract's legacy Windows-1252 aliases; quote “A byte order mark has priority over a label” (Section 8.1.1, UTF-8 decoder; 9 words).
- S091 — https://www.unicode.org/reports/tr15/ — accessed 2026-10-23T01:08:59Z, HTTP 200 — admit, tier A, kind spec, status mined: UAX #15 defines compatibility equivalence, supporting the contract's NFKC quote matching; quote “If two strings are compatibility equivalents, then toNFKC(x) = toNFKC(y)” (Section 1.2, Normalization Forms; 10 words).
- S092 — https://html.spec.whatwg.org/multipage/syntax.html#elements-2 — accessed 2026-10-23T01:08:59Z, HTTP 200 — admit, tier A, kind spec, status mined: The HTML Standard classifies script and style as raw text elements for the contract's HTML-text removal; quote “Raw text elements script” (Section 13.1.2, Elements; raw text classification list; 4 words).
- S093 — https://en.wikipedia.org/wiki/HTTP_301 — accessed 2026-10-23T01:09:00Z, HTTP 200 — reject, tier C, kind community, status rejected: Tertiary encyclopedia summary repeats older RFC-era guidance and cannot ground current normative status behavior; quote “the HTTP status code used for permanent redirecting” (opening paragraph, HTTP 301 description; 8 words).
- S094 — https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections — accessed 2026-10-23T01:09:01Z, HTTP 200 — reject, tier B, kind docs, status rejected: it restates S088's permanent/temporary split and its Principle section says every redirect response has a Location header, which S088 contradicts for 300 and 304 (wave-1 `ScoutReopenS094`, both quotes located there); the scribe draft proposed admit, the L1 rejects; quote “These redirections are meant to last forever.” (Permanent redirections, first paragraph; 7 words).

Real rejects with reasons: S093 (tertiary; quotes RFC 2616, never mentions 308; wave-1
`ScoutReopenS093` found an Apache example that 301-redirects onto `http://`) and S094 (secondary
restatement that contradicts S088 on Location for 300 and 304).

Row changes logged old→new: S088–S092 `—` → `mined`, opened `2026-10-23`, recheck `90d`,
used-by `scripts/source_recheck.py`. S093, S094 `—` → `rejected`, opened `2026-10-23`, recheck
`90d`, used-by `—`. No existing row's status, recheck or used-by cell changed.

Source-precision notes from the re-opens (carried as contract limits, not row changes):
- S088 section 15.4.4 never calls 303 temporary; the contract's "302, 303 and 307 are temporary"
  is lane reading for 303 (`ScoutReopenS088` F1). 404 does not mean permanent (F3).
- S090: the windows-1252 index maps every byte 0x80–0xFF, so Python's `cp1252` codec differs on
  0x81, 0x8D, 0x8F, 0x90 and 0x9D (`ExecProbeCp1252`). The landed tool and the L1 reference use
  Python `cp1252`; no sealed case uses those bytes.
- S089: `urllib.parse.urljoin` passes every RFC 3986 section 5.4 example except the strict `http:g`,
  but does not remove dot segments in an authority-relative reference (`ExecProbeUrljoin`). No
  sealed case depends on it.

## Real-input run (evidence, not a claim)

`scripts/source_snapshot.py` recorded live fetches of 90 Gate quotes (one per row id; input
`realrun/input.json` built from wave-1 `ExecGateQuoteExtractor` output plus the new rows; no
operator-owned host), and the landed tool audited them (`realrun/audit.json`, exit 1,
`failed-policy`, 90 evaluated). Findings: `quote_missing` 9 (S004, S005, S006, S007, S008,
S017, S025, S065, S068), `moved` 2 (S040 → `…/what-is-github-pages`, S068 →
`…/docs/sharing/webmasters/`), `gone` 1 (S087, already rejected), `unsupported_type` 2 (S016,
S066, JSON endpoints). Each finding is re-opened by hand in wave 2 before any row changes.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| a declaration wrote a full commit hash that names no object | `git show 3555f63f:SCORECARD.md` "Base `b720d79976a1fb8f…`"; the real base is `b720d799ae99c19a…` (seen when the counter refused the long form) | none | `.ufo/waves/round-36/criteria/hash_resolve_check.py`: exit 1 on that section (`verification/criterion-hash-resolve-r36-decl-at-3555f63f.txt`), exit 0 on the round-35 declaration. QUALITY round-36 (e). Corrected by append in SCORECARD. |
| a sealed key whose body-reading checks all expected a hold, with one fixed contentType on the c and d checks, so a body-blind shortcut passed two bullets | key v1 (`sealed/cases-v1.json`); `verification/v2/control-CtlShortcut.json` (17 of 28, every (e) and (f) case passed) | the pre-freeze control wave (`ctl/CtlShortcut.md`); none of the L1's 34 v1 ablations skipped reading | key v2 adds `quote_missing`-polarity checks and rotates contentTypes; shortcut 9 of 28 under v3; ablations `s_ctkey` 13 and `s_unsure` 24. QUALITY round-36 (f). |
| two wave-1 seats wrote their deliverable into the lane, outside their report path | `ExecCriterionAblation` and `ExecCriterionControlTree` reports say they landed files under `.ufo/waves/round-36/criteria/`; the wave context allowed only the report | the wave context's bounds sentence; no check | the L1 verified each file's sha256 against the seat's sandbox copy and committed them as wave evidence; next round's context names the sandbox path as the only deliverable path and the L1 checks `git status` before integration |
| a seat's selftest fixture contradicted the contract it quoted | `scripts/source_recheck_selftest.py` fixture f08 used `charset=utf-16`, which the WHATWG table lists as a UTF-16LE label (S090), and expected `charset_unsupported` | the landed tool (exit 1 against the fixture) | the L1 changed the label to `shift_jis` with a comment (101/101 after); the change is to the selftest, not to the tool or counter |

Round-35 routed mistakes mined by wave-1 `ScribeMistakeMine` (`w1/ScribeMistakeMine.md`) are the
round-35 closure's routed defects 2–5; their fixes are QUALITY round-36 (a)–(d) and the appended
corrections, each check shown able to fail:
- (b) `criteria/version_bump_check.py`: exit 1 on round-35 v1→v2 (`C2_MAX_WORDS` 1500 → 2200),
  exit 0 on round-36 v1→v2, exit 1 on v2→v3 naming the pin (`verification/criterion-version-bump-*.txt`).
- (c) `criteria/ablation_floor_check.py`: exit 1 on the round-35 shape (skip (c) = 22 of 24),
  exit 0 on the 36 round-36 ablations (`criterion-ablation-floor-*.txt`).
- (d) `criteria/control_tree_check.py`: exit 1 on round-35 `CriticC2Sufficiency.md` (no listing),
  exit 0 on the five round-36 control reports (`criterion-control-tree-*.txt`). Limit
  (`w1/ExecCriterionControlTree.md`): a listing of the control's own commit tree passes even when
  the build tree held the key.

## Round-35 routed defects — disposition

| # | Item | Disposition |
|---|---|---|
| 1 | Seal what the claim names; a bare id line must not satisfy cites | No knowledge-entry claim this round. QUALITY round-36 (a) carries the rule for the next one. |
| 2 | Do not loosen a counter in a version bump | v2 (jail) and v3 (pin) change no target, cap or predicate; `version_bump_check.py` receipts. |
| 3 | Target slack: every bullet must move the target | 4 cases per bullet, one check per rule; 36 ablations at most 24 of 28; QUALITY (c). |
| 4 | Control key-blindness | Controls built from public text by seats told never to touch the key tree; listings in `ctl/*.md`; `control_tree_check.py`. |
| 5 | Gate-line nits (S084 coverage, S079 cite) | Corrections appended to `corpus/lessons/round-35.md` and to the entry. |

## Holds

- Control wave `CtlJunk` and `CtlCounterExploit` ended at once on a provider cyber-policy filter
  (`code=cyber_policy`). Not retried, rerouted or rephrased; no findings used. The declared junk
  control therefore has no receipt.

## Carried open

- Rule (d) deletes every whitespace character, so 1612 of 1891 single-space corruptions of the
  22 round-34/35 Gate quotes still hold (`w1/ExecProbeQuoteMatch.md`); `clean` means the recorded
  quote occurs in the recorded text, not that it is reader-visible.
- The counter compares exit, verdict and projected findings only: `checksEvaluated`, `version`
  and usage paths are not measured by it (`w1/CriticAxisFit.md`); the selftest checks them.
- Counter defects from `w1/ReviewCounterV2.md`: an unhashable `check` value crashes the run
  (D1); duplicate check ids split (D2, no sealed case has one); a missing `--tool-file` exits 1.
  Earlier case directories are visible to later cases inside the jail (`w1/ReviewJailIsolation.md`).
- 18 contract points are undecided by the text (`w1/CriticContractAmbiguity.md`).
