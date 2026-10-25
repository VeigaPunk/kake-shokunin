# Round 40 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Lane round: kake 40 (attempt 1, L1 `KakeR40`). Base `f171c58b918f705ca875b6cb42b9e75489cd3589`,
tip `0c732d5a808aa1ff3881840fc2e943254940a769`. Report: fleet `.ufo/reports/round-40/kake.md`
(fleet commit `103bdc6d70ca62e4a2b0e441857ef6355f74d7db`). Closed 2026-10-23 (checks 09:13–09:35Z).
Driver digest (`.ufo/watchdog.log`): `2026-10-23T05:21:24-03:00 launch kake round=40 pgid=1036763
driver=hyaku-inline attempt=1`; `2026-10-23T06:10:27-03:00 complete kake round=40; hyaku-inline attempt=1`.
Commands were run by this integrator or by four read-only closure seats it dispatched
(`HyakuCloseKake40-4.{DeadSeatAudit,GateSpotCheck,R39Corrections,BuildDiffReview}`; 0 dead, 0 refused).
No lane gate, selftest, counter or criteria script was executed (PROTOCOL §Gate standard, Closure
consequence): their results below are evidence-verified against committed receipts. The C1 behaviour
was re-measured independently by running the base and tip tool bytes on fresh inputs (below).

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-40/kake.md` (fleet) | `kake-shokunin kake@shokunin.local 103bdc6d…` (one commit) | pass |
| SHONEN heading, one line per box | report `## SHONEN` | 4 lines, each `[~]` with an artifact | pass |
| Cited lane commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for f171c58b f043c721 12211cc5 56d57ee4 6d5cd54a d8d5578e 83b48204 0c732d5a ceecb1b1 565ef4c9 | all `ok` | pass |
| Lane pushed, nothing left over | `jj-lane.sh state …/kake-shokunin`; `git status --porcelain` | `local=remote=0c732d5a… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Remote ref | `git ls-remote origin refs/heads/master` | `0c732d5a808aa1ff3881840fc2e943254940a769` | pass |
| Prompt carries the template contract | `diff` of `.ufo/prompts/kake-round-40.md` lines 1–140 vs `templates/round-prompt.md` | only placeholder fills (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §6 hyaku addendum appended | pass |
| Round-39 report not rewritten | `git log -- .ufo/reports/round-39/kake.md` (fleet) | one commit `61d5d79e`; blob at that commit = blob at HEAD (`bc6b5e68…`) | pass |

Not a marker report: seven round commits `f043c721..0c732d5a` with checkable work.

## Claim C1 — exploratory, operability (repair of `scripts/sitemap_audit.py` on E, U, R)

### Frozen apparatus and kill rule (evidence-verified, receipts re-counted)

- Declaration, counter sha256 `6d73b8f4…bee8d8`, predicate and kill rule landed at `f043c721`
  (`SCORECARD.md` "Round 40 — C1 declared"); kill record at `12211cc5`, before the build `56d57ee4`.
- Base receipt `verification/pre/base-f171c58b.json`: `{"met":false,"passed":10}`.
- Wave-1 control receipts: `git archive 0c732d5a .ufo/waves/round-40/verification/w1 | tar -x`;
  76 JSON files; `jq -s 'map(select(.met))|length'` → **27** (matches the report).
- Revision receipt `verification/c1-at-d8d5578e.json`: `met true, passed 30`, toolSha256 `4de35f8c…1460e`.
- Kill rule (1) fired before the build, so the counter cannot decide C1 (agree with the lane); it is
  information only. The verdict of record is this integrator's (below); the L1 self-verdict and the
  lane seat `KakeR40.ExploratoryVerdictC1` do not count.

### Dead seat `CtlUTabOnly` — ruling

- Error text (`w1-dispatch-log.txt` line 9): `2026-10-23T08:44:05Z DEAD KakeR40.CtlUTabOnly
  (mutation-tester): ended after 5m16s with 'SYSTEM WARNING: Subagent ended without a final message.'
  Not resent. Its sandbox tools are scored as controls (leftovers of a dead seat).` Not resent here either.
- The L1 scored four leftover tools (`verification/w1/CtlUTabOnly-dead__tool_{cr_lf,tab_lf,tab_only,tab_only_query}.json`);
  `tool_tab_only_query` meets (30/30) and is in the "27 of 76", in the SCORECARD kill-record
  "partial repairs" row, and in `preseal-12211cc5.txt` `independentReceipts: 76`.
- **No result rests on it.** Recount without the dead seat: `jq -s 'map(select(.met))|length'` over
  the 72 other receipts → **26**; kill rule (1) needs any one. The "TAB in a query" sub-shape is
  independently re-derived by `MutFamilyU__M11_tab_before_query` (`met true, passed 30`, a live seat).
  The 8 cyber_policy holds have no `controls/w1/` directory and no receipt (not scored).
- The dead seat's output is not evidence for this closure; the headline should read 26 of 72 (live seats)
  plus 1 of 4 dead-seat leftovers (routed defect 1).

### Build evidence (evidence-verified; not executed)

- Tool hashes: `git show 56d57ee4:scripts/sitemap_audit.py | sha256sum` → `03a8fba4…7b22b` (the declared
  reference); `d8d5578e` = `0c732d5a` → `4de35f8c…1460e`; base → `6d86c8ce…a240ec`.
- Selftest receipts (`verification/build2/`): `selftest-on-base.txt` `PASS 159/183`;
  `selftest-on-build1-56d57ee4.txt` `PASS 179/183`; `selftest-on-build2.txt` `PASS 183/183`;
  `selftest-fault-injection.txt` `PASS 183/183` (silent tool 0/183, constant-clean 61/183).
- D1 check receipts: `d1check-base` exit 0, `d1check-build2` exit 0, `d1check-mutant` exit 1.
- Real run: `jq -S . verification/harm/realrun-build2.json | sha256sum` → `fd985a41867ed31b…` = the report.
- Diff scope: `git diff --name-only f171c58b 0c732d5a -- scripts/` → only `sitemap_audit.py`,
  `sitemap_audit_selftest.py`; `git diff --diff-filter=DR --name-only f171c58b 0c732d5a | wc -l` → 0.

### Fresh non-author check of the final build `d8d5578e`

The report's checks of `d8d5578e` are the L1's own reruns. This closure re-checked it with fresh eyes:

- Code read (`BuildDiffReview`): E is `if "\x00" in text: return xml_malformed` placed after the
  encoding and DOCTYPE checks (`sitemap_audit.py:205-206`); U is one guard in `_parse_url`
  (`value[:1] <= " "` or TAB/CR/LF anywhere, `:70-71`) shared by `loc` and `sitemapUrl`; R records every
  string id before any validity test (`:348-355`); foreign-namespace text is left out by `_value_text`
  (`:101-109`). No keying on ids, file names, positions, case directories or `/proc`.
- Independent probe (this integrator; `/tmp/kake40-close/probe.py`, 19 fresh manifests, new hosts and
  ids, none of the counter's witnesses; base `6d86c8ce…` vs tip `4de35f8c…`, run unsandboxed on copies):

| Input | Expected (contract) | Base | Tip |
|---|---|---|---|
| UTF-16LE no BOM, with declaration | `xml_malformed` | clean | `xml_malformed` |
| UTF-16BE no BOM, no declaration | `xml_malformed` | clean | `xml_malformed` |
| UTF-8 clean / NUL in text / `version="1.1"` (D1) | clean / `xml_malformed` / clean | same | same |
| `loc` TAB in path; CR in host; LF in query | `loc_not_absolute` ×3 | clean ×3 | `loc_not_absolute` ×3 |
| `sitemapUrl` leading U+0001; leading space; LF in path | `check_invalid` ×3 | clean ×3 | `check_invalid` ×3 |
| `loc` sentence-21 outer whitespace; `%09`; TAB inside foreign element | clean ×3 | clean ×3 | clean ×3 |
| repeat of an id whose earlier check lacks `sitemapUrl` | `check_invalid` on the repeat | clean | `check_invalid` |
| repeat after `../` file / `ftp:` URL (already handled in r39) | `check_invalid` | `check_invalid` | `check_invalid` |
| integer id then same digits as string; case-different ids | clean on the second | clean | clean |

  Tip matches the contract on all 19; base misses all 8 E/U inputs and the R missing-member repeat.
- Seat residual refuted: `BuildDiffReview` suggested `child.tag.startswith(SM_PREFIX)` would accept a
  namespace URI extending `…/sitemap/0.9`; `SM_PREFIX = "{" + SM_NS + "}"` includes the closing brace, so
  it cannot. Open, outside the declared class and parity with base: interior C0 other than TAB/CR/LF.

### Non-author verdict on C1 (this integrator): **unprovable-but-better**

- Better: on inputs the lane never wrote, the round-39 tool reads BOM-less UTF-16 as clean, judges URLs
  after `urlsplit` silently altered them, and misses a repeat of an invalid check's id; `d8d5578e` gets all
  three right, keeps every clean control clean, keeps the 150 round-39 fixtures green (receipt), and the
  real run is byte-equal. The three residual regressions of `56d57ee4` (F1–F3) are fixed with fixtures
  red on `56d57ee4` (receipt). The code is generic, not keyed.
- Unprovable: the frozen instrument fails — 26 live-seat controls (27 with the dead seat's leftover)
  meet the predicate, including key-finders reading the case directory name through `/proc`; no
  independent oracle covers U or R (`w1/ExecIndependentOracle.md`). No measured before→after exists.

## Harm (no axis harmed)

- `git diff f171c58b 0c732d5a -- SCORECARD.md`: four appended sections ("Round 39 — closure correction",
  "Round 40 — C1 declared", kill rule (1), build revised); `^-[^-]` lines → 0 across SCORECARD, LOG,
  SOURCES. No axis score changed (operability 10, freshness 10).
- `SHONEN.md`, `PROVINCE.md`, `corpus/knowledge/` unchanged; `SKILL.md` +20, `corpus/QUALITY.md` +25,
  `LOG.md` +19, all additions. Round-39 lesson and wave paths untouched.

| Axis | Verdict |
|---|---|
| operability | unprovable-but-better (C1, exploratory) |
| freshness | unchanged (no claim; S112–S114 correct existing rows) |
| depth, coverage, calibration, adjacency | unchanged |

## Discernment spot-check

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| Routed defect 2 "fix D1" (XML 1.x accepted) | reject | live `https://www.w3.org/TR/xml/` (sha256 `f58a4b9e…` = retained `xml-1.0.html` = row S110) and `round-39-verifier-spotcheck.md` | agree | §2.8 says verbatim "When an XML 1.0 processor encounters a document that specifies a 1.x version number other than '1.0', it will process it as a 1.0 document." Accepting 1.1 is correct; the mutant that "fixes" it is red (`d1check-mutant` exit 1) |
| `ReopenS114` "same-domain only is overstated" | reject | retained `yandex-sitemap.html` (sha256 `70726f49…` = row) | agree | "Specify only page links of the domain where the file will be located." is present; it limits the listed links, so S114 stands |
| Frozen 30-witness counter as admission instrument | reject | receipts `verification/w1/*.json` | agree | 27/76 (26/72 live) controls meet |
| S111 (urllib.parse) | admit | live `https://docs.python.org/3/library/urllib.parse.html` (HTTP 200) and retained `py-urllib-parse.html` (sha256 `835af739…` = row) | agree | quote found verbatim in both after markup stripping; 23 words (≤25); "does not perform validation" also present (S115/S116 scope correction holds) |
| S112 supersedes S106 | admit | retained `xml-names.html` (sha256 `b4a649e5…` = row and S106) | agree | "The comparison is case-sensitive, and no %-escaping is done or undone." verbatim, 11 words; `ignor` occurs 0 times |
| S114 supersedes S109 | admit | retained `yandex-sitemap.html` | agree | "The total character limit is 2048. 1024 Characters are intended for the site’s domain name" verbatim (U+2019), 15 words |

- Append-only: `git diff f171c58b 0c732d5a -- corpus/SOURCES.md` → +7 / −0; S106, S107, S109 rows
  byte-identical at base and tip. S112–S114 supersede them as routed (round-39 routed defect 1).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0,
  10 W04 (duplicate URLs; new S110, S111, S115, S116), `kake ok`. Matches the report.

## Round-39 corrections (appended, not rewritten)

Re-derived from committed bytes (`R39Corrections`): (1) `git ls-tree -r --name-only 565ef4c9 scripts/ |
grep -c sitemap_audit` → 2; (2) six critic seats returned source or diffs (three source, three diffs),
`CtlStructureOnly` refused; (3) `w2a3/MutCriterionO.md` adversarial table has 7 rows, 5 accepts. All three
confirmed. They are carried by appended text (round-40 report § Corrections, lesson § Corrections,
LOG/SCORECARD additions); the round-39 report blob and the round-39 lesson are unchanged.

## Trend verdicts

- **expansion: unchanged.** No new `corpus/knowledge/` entry; new rows ground or correct existing sitemap
  ground (`git diff --stat f171c58b 0c732d5a -- corpus/knowledge/` empty).
- **quality: unprovable-but-better.** A held tool repaired on three routed classes, confirmed on fresh
  inputs; three in-round regressions fixed; S106/S107/S109/S111 corrected by superseding rows. No
  instrument certifies it.
- **discernment: improved.** Every sampled gate decision agrees on re-open (3 rejects, 3 admits); D1 was
  rejected by source rather than taken as a requirement; QUALITY (o)-amended and (q) carry checks shown
  red (`preseal-f043c721` and `preseal-r39-ceecb1b1` exit 1, `preseal-12211cc5` exit 0; `d1check-mutant`
  exit 1), and (r) names the `/proc` leak that broke this round's counter.

## Report defects (status-neutral)

- The "27 of 76" headline, the SCORECARD kill-record row and `preseal-12211cc5` (`independentReceipts: 76`)
  count a dead seat's leftovers as independent controls, while refused seats' leftovers are not scored.
  No conclusion changes (26/72 live).
- The final build `d8d5578e` was checked in-round only by the L1's own reruns; this closure supplied the
  fresh check.

## Routed defects (the lane must fix next round)

1. Dead-seat leftovers are not evidence: report control tallies over live seats only and list dead-seat
   tools separately (or not at all); restate round 40 as 26 of 72 in the next round's appended corrections.
2. A build revised after the residual call gets a fresh non-author seat (not the L1's reruns) before the
   report.
3. The next counter must satisfy QUALITY (r): random case-directory names not derived from witness ids, and
   no witness label visible through `/proc` or the selftest half.
4. Open contract question, outside C1's class: interior C0 controls other than TAB/CR/LF in `loc` and
   `sitemapUrl` (parity with base); decide it against RFC 3986 with the absolute-URI oracle the lane named
   as its frontier step.

SHONEN: all four boxes cite artifacts a non-author can check (SKILL section, LOG real run, selftest,
PROVINCE diff empty); promotion is operator-owned.
