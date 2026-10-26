# Round 41 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Lane round: kake 41 (attempt 1, L1 `KakeR41`). Base `8eb121c81ffebada064eefcabcd94dd2303d646f`,
tip `c93bf9a8b9acece1f9328548e279c27945bd1da9`. Report: fleet `.ufo/reports/round-41/kake.md`
(fleet commit `0122b21157a0ece027b30c9fdb01171657b58ebb`). Closed 2026-10-23 (checks 10:25–10:50Z).
Driver digest (`.ufo/watchdog.log`): `2026-10-23T06:27:40-03:00 launch kake round=41 pgid=336768
driver=hyaku-inline attempt=1`; `2026-10-23T07:40:55-03:00 complete kake round=41; hyaku-inline attempt=1`.
Commands were run by this integrator or by two read-only closure seats it dispatched
(`HyakuCloseKake41.{R41PromptFidelity,R41HarmCritic}`; 0 dead, 0 refused). No lane gate, selftest,
counter or criteria script was executed (PROTOCOL §Gate standard, Closure consequence): those results are
evidence-verified against committed receipts. C1's behaviour was re-measured independently by importing
the base and tip tool bytes and comparing `_parse_url` with the vendored RFC 3986 oracle on fresh values
(below). No tool was installed by this closure.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-41/kake.md` (fleet) | `kake-shokunin kake@shokunin.local 0122b211…` (one commit, 07:40:31-03:00, after lane tip 07:39:26-03:00) | pass |
| SHONEN heading, one line per box | report `## SHONEN` | 4 lines, each `[~]` with an artifact | pass |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify` + `git merge-base --is-ancestor <h> master` for 8eb121c8 abf457d0 9e3c31d2 eae5ae2c 2653b629 0c5ad2f6 133257de b9bf1a39 c4eb7e73 c93bf9a8 | all resolve, all ancestors; all nine round commits authored and committed by `kake-shokunin` | pass |
| Lane pushed, nothing left over | `jj-lane.sh state …/kake-shokunin`; `git status --porcelain` | `local=remote=c93bf9a8… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Remote ref | `git ls-remote origin refs/heads/master` | `c93bf9a8b9acece1f9328548e279c27945bd1da9` | pass |
| Prompt carries the template contract | `R41PromptFidelity`: hand render of `templates/round-prompt.md` via `render_prompt()` (`scripts/shokunin-watchdog.sh:172-188`) vs `.ufo/prompts/kake-round-41.md` lines 1–140; §6 vs `scripts/hyaku/lane-addendum.md` rendering | 0 diff lines in both; five child-lane items and round-level items present; no L2 route map quoted (host route table referenced) | pass |
| Report sections | report | Work, Landed changes (each tied to LOG), measurements, Sources & frontier, Trend verdicts, SHONEN, seats, installs | pass |

Not a marker report: nine round commits `abf457d0..c93bf9a8` with checkable work. Status **ok**.

## Claim C1 — exploratory, operability (RFC 3986 `URI` before `urlsplit` in `scripts/sitemap_audit.py`)

### Frozen apparatus and kill rule (evidence-verified, receipts re-counted)

- Counter v1 `c1_count.py` sha256 `2acc443a…67b4` (`sha256sum` at tip, = SCORECARD); predicate, harm rule and
  kill rule landed at `abf457d0`; kill record at `9e3c31d2`, before the build `eae5ae2c`.
- Base receipt `verification/pre/base-8eb121c8.json`: `passed 1049, cases 1434, met false, seed 41001`,
  toolSha256 `4de35f8c…` = `git show 8eb121c8:scripts/sitemap_audit.py | sha256sum`.
- Final receipts `verification/build3/c1-v{1,2}-build3-4100{1,2,3}.json`: all `passed 1434, met true`,
  toolSha256 `50287ac6…` = `git show c93bf9a8:scripts/sitemap_audit.py | sha256sum`.
- Wave-1 tallies: `jq -s 'map(select(.met))|length' verification/w1/*.json` → **15** of 141 files;
  `verification/w1v2/*.json` → **10** of 141. Matches the report. `CtlNoPct__terminal_pct`: v1 1434 met,
  v2 1433 not met; `CtlGeneratorShape__v1_shape`: v1 1434 met, v2 1365 not met.
- Kill rule (1) fired before the build, so the counter cannot decide C1 (agree with the lane): v1 and v2
  scores are information only. The verdict of record is this integrator's; the L1 self-assessment and lane
  seats (`CriticExploratoryBetter`, `ResidCriticBetter`) are advisory.

### Oracle and vendored wheels (installs disclosed by the lane)

- `sha256sum .ufo/waves/round-41/oracle/*.whl` → abnf `cdcac127…60917`, rfc3987 `10702b1e…dce53`.
- Live re-fetch (this closure, 2026-10-23) `https://pypi.org/pypi/abnf/2.9.1/json` (HTTP 200, 8,215 bytes) and
  `…/rfc3987/1.3.8/json` (HTTP 200): wheel digests equal the vendored bytes; retained `sources/pypi-*.json`
  carry the same digests.
- Pinned, not merely printed: `c1_count.py:41,63-65` (`ORACLE_SHA256`, raises on mismatch) and
  `oracle_crosscheck.py:15,24-25` (`SECOND_SHA256`, exits on mismatch). Recorded in S118/S119 and the
  report's installs line (uv venv + `pip download`, PyPI, scratch; no pacman). Pinned and recorded: pass.
- Cross-check receipts `verification/pre/oracle-crosscheck{,-v1-fullmatch,-v2}.json`: `totalCases 14340,
  totalDisagree 0` each (10 seed rows).

### Harm evidence (evidence-verified; not executed)

- Selftest receipts `verification/build3/`: final `50287ac6` `PASS 225/225 exit=0`; base `PASS 196/225
  exit=1` (29 `FAIL r41_*` names); first build `0b485431` `PASS 219/225 exit=1` (six IP-literal TAB/LF/CR).
- New fixtures: `sitemap_audit_selftest.py:880-989` expands to 42 `r41_*` (15 literal + 6 + 3 + 16 + 2);
  42 − 29 = **13 green on base**: `port_letter`, `path_sub_delims`, `path_pct_7e`, `ipv6_literal_host`,
  `userinfo_with_colon`, six `{loc,manifest_url}_ipv6_literal_{tab,lf,cr}`, two `*_slash_question_clean`
  (count confirmed by `R41HarmCritic`).
- Real run: `jq -S . verification/build3/realrun-build3.json | sha256sum` → `fd985a41867ed31b…`, equal to
  round 39/40 receipts (`round-40/verification/harm/realrun-build2.json`, `round-39/verification/realrun/build-565ef4c9.json`).
- Frozen harm rule (`SCORECARD.md:2746-2748`, landed `abf457d0`): "passes every fixture (183 plus the
  round's new ones, which must be red on `8eb121c8`), and the round-39 real run is byte-equal … Otherwise
  operability is harmed." First and third conditions hold; the second fails for 13 of 42.
- Measured cost: `w2/ReviewBuildPerformance.md` (first build) ×3–40 on adversarial values, real run
  236.5→288.7 ms (+22%), linear; `resid/ResidCriticBetter.md:18` (final bytes) 52 MB cap file 0.166→2.136 s
  (×12.87, including the newly required findings).
- Out-of-class drift: `resid/ResidCriticHarmReading.md`/`ResidCriticBetter.md:16` — `http://[fe80::1%é]/a`
  and `%en|0` zone ids: base clean, final `check_invalid`; the frozen class says "IP-literal contents …
  are outside the class" (`SCORECARD.md:2689`). RFC-invalid values, but not the declared repair.
- Scope: `git diff --name-only 8eb121c8 c93bf9a8 | grep -v '^.ufo/waves/round-41/'` → LOG, SCORECARD,
  SKILL, QUALITY, SOURCES, lesson, the tool and its selftest. `^-[^-]` lines across LOG, SCORECARD, SOURCES,
  QUALITY, SKILL → 0. `SHONEN.md`, `PROVINCE.md`, `corpus/knowledge/` unchanged.

### Independent probe (this integrator)

`/tmp/hk41/probe/probe.py` (sha256 `01498b1b…0a5`; seed 924141): 20,000 values made by 0–3 random
insertions (any position, ends included; ASCII 0x00–0x7F, broken percent units, delimiters, `[`, `]`, `é`,
`:99999`), deletions or duplications applied to the 39,080 real `loc` values of the retained round-39 sitemaps.
Base `4de35f8c…` and tip `50287ac6…` `_parse_url` imported from `git show` bytes; oracle = vendored abnf
2.9.1 `rfc3986.Rule("URI").parse_all` + http(s) + non-empty host.

| Measure (19,750 in-class values: ASCII, no `[` after `//`, port ≤ 65535) | Base | Tip |
|---|---|---|
| disagree with the oracle | 4,015 (all accept-invalid) | **0** |
| reject an oracle-valid value | 0 | 0 |
| accept what the other rejects | — | 0 (tip ⊆ base) |
| 250 out-of-class values changed | — | 24, all base-accept → tip-reject, all oracle-invalid |

The URL rule is more correct on inputs the lane never generated and introduces no RFC-valid rejection.

### Non-author verdict on C1 (this integrator): **unprovable**

- Better in class: yes — 0/19,750 oracle disagreements vs base 4,015; 29 red-on-base fixtures; the
  first-build TAB/LF/CR regression fixed with guards; real run byte-equal.
- Not admissible as better: the round's own frozen harm rule, written before data, returns "operability is
  harmed" (13 of 42 new fixtures green on base). This closure does not exempt valid-value controls or
  regression guards after the fact; that would relax a frozen rule after data. The measured cost (×12.87
  final-byte cap file, +22% real run on the first build) and the undeclared zone-id tightening are real
  operability trade-offs the frozen rule did not price. The lane reported all three honestly and
  self-awarded nothing (agree).

| Axis | Verdict |
|---|---|
| operability | **harmed** (frozen harm rule `SCORECARD.md:2746-2748` unmet; no in-class behavioural regression found) |
| freshness | unchanged (no claim; S102/S098 bytes re-verified unchanged) |
| depth, coverage, calibration, adjacency | unchanged |

Admission: **false** (`rejected-harmed`). No SCORECARD axis score changed (operability 10, freshness 10).

## Discernment spot-check

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S117 RFC 3986 | admit | live `https://www.rfc-editor.org/rfc/rfc3986.txt` (HTTP 200, 141,811 bytes, sha256 `3102dae4…d683` = row = S098 pin) | agree | `URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]` at line 867 verbatim; 11 tokens (≤25); new row justified (S098 scope §§2.1–2.3) |
| S118 abnf 2.9.1 | admit | live `https://pypi.org/pypi/abnf/2.9.1/json` (HTTP 200, 8,215 bytes) | agree | `info.description` line 34 "validate a whole string against a rule (raises ParseError otherwise)" verbatim, 10 words; wheel digest = vendored bytes |
| Counter v1 as C1's admission instrument | reject | receipts `verification/w1/*.json`, `w1v2/*.json` | agree | 15/141 met v1; `terminal_pct` and `v1_shape` meet v1 (1434) and fail v2 (1433, 1365) |
| "U+0080 and above accepted as RFC 3987 IRI characters" | reject | live `https://www.rfc-editor.org/rfc/rfc3987.txt` | agree | `ucschar = %xA0-D7FF / %xF900-FDCF / …` (line 435): starts at U+00A0 with holes, so the IRI justification is false; kept as legacy behaviour |

- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, 11 W04
  (duplicate URLs; new S117 duplicates S098's URL by design), `kake ok`. Matches the report. Rows 116 → 119
  (`grep -c '^| S[0-9]' corpus/SOURCES.md` at base and tip).
- Append-only defect: S117–S119, committed at `9e3c31d2`, had `anchor`/`teaches` edited in place at
  `2653b629` and `0c5ad2f6` (logged old→new in lesson § Wave 2). CORPUS.md rule 2 allows only `status`,
  `recheck`, `used-by` in place; a correction is a superseding row. Base→tip diff is still +3/−0.

## Trend verdicts

- **expansion: unchanged.** No `corpus/knowledge/` entry (`git diff --stat 8eb121c8 c93bf9a8 --
  corpus/knowledge/` empty); S117–S119 ground a held tool.
- **quality: unchanged.** No entry superseded or deepened; the held tool's URL rule is more correct in class
  but its change is not credited under the frozen harm rule; S102/S098 re-verify unchanged; the tool comment
  still overstates IP-literal parity (routed).
- **discernment: improved.** The spot-check agrees with all four sampled gate decisions (2 admits,
  2 rejects); the pre-freeze control wave caught counter v1 before build data; QUALITY (s), (t), (u) each
  carry a lesson and a check shown red then green (`verification/criteria/live-tally-r40.txt` exit 1 /
  `-r41-w1` exit 0; `fresh-review-r40` exit 1 / `-r41-final` exit 0, 7 seat reports; `w1` vs `w1v2`
  receipts). The harm clause it could not meet by construction is the round's unlearned slip (routed 1).

## Report defects (status-neutral)

- Quality trend reported as "unprovable-but-better (pending non-author judgment)"; the closure rules
  `unchanged`.
- Tool comment `scripts/sitemap_audit.py:68-72` ("an IP literal's contents and the port range are still
  judged only by urlsplit") and the regex comment `(contents: urlsplit)` are false at `50287ac6`; SKILL and
  SCORECARD were corrected, the tool source was not.
- SOURCES rows edited in place after commit (above).

## Routed defects (the lane must fix next round)

1. Harm-rule design: a frozen harm rule must name, before data, which new fixtures are change fixtures
   (red on base) and which are parity/regression guards (green on base), and price runtime cost; add a
   grounded QUALITY criterion with this round's lesson.
2. Disposition of the landed URL rule `50287ac6…`: it is not admitted. Next round either re-establish
   no-harm under a correctly frozen rule (cost bound, declared zone-id behaviour) or restore IP-literal
   parity; record the choice.
3. Correct the tool comment at `scripts/sitemap_audit.py:68-72,80` to match SKILL (zone ids with
   non-ASCII or `|` now rejected).
4. Correct S117–S119 by superseding rows (or record why the in-round edits stand) per CORPUS.md rule 2;
   never edit a committed row's `anchor`/`teaches` in place.
5. Before freezing counter v2: fix its `FileNotFoundError`, inherited stdin, uncapped output and
   `/proc/1/environ` exposure (lane's own plan); decide equivalence by a frozen differential (QUALITY (n)).
6. Open outside C1: symlinked manifest `file` paths read outside the manifest directory
   (`w2/SentinelBuildInput.md`); `source_recheck.py` Appendix-B URL reading.

SHONEN: all four boxes cite artifacts a non-author can check (SKILL section, LOG real run, selftest,
PROVINCE diff empty); promotion is operator-owned.
