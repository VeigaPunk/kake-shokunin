author: hyaku closure (non-author integrator, @m_opus)

# Round 37 — verifier spot-check (kake)

Non-author closure of kake round 37. Report `.ufo/reports/round-37/kake.md` (fleet `fedd3fa6`),
prompt `.ufo/prompts/kake-round-37.md` (fleet `85d0c708`). Lane base
`621fb528ba9116b9f440b8332be6dfc0cad4e972`, tip `8319cb76350562331677b6af49454b4d756acfa6`.
Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-10-22T23:46:04-03:00 launch kake round=37 pgid=3604149 driver=hyaku-inline attempt=1` ·
`2026-10-23T01:00:15-03:00 complete kake round=37; hyaku-inline attempt=1`.
No closure seats were dispatched; every check below was run by the integrator. No lane gate,
counter or selftest was executed (PROTOCOL §Gate standard, Closure consequence): C1 is
**evidence-verified** against committed receipts plus plain re-derivations (git, sha256, jq,
census); nothing ran inside the lane except read-only git.

## Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-37/kake.md` | `kake-shokunin fedd3fa61510cc33e99ed2a4be165a715c998fae 2026-10-23T00:59:52-03:00` (after tip 00:58:53, before driver complete 01:00:15) | ok |
| `## SHONEN`, one line per box | report lines 121–126 vs `git show 8319cb76:SHONEN.md \| grep -c '^- \['` → 4 | 4 boxes, 4 lines, all `[~]`, no `[x]` | ok |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>; git merge-base --is-ancestor <h> master` for 621fb528, 202d625a, 4b089da6, ccc3b2b9, 528a6d02, 9dbc88bb, 424aa248, 79d3c780, a5ae0280, b99b6679, 7ab83275, 8319cb76, 1a16b8e3 | all `commit`, all ancestors | ok |
| Cited `bf9b2089` | `git cat-file -t bf9b2089`; `git bundle list-heads .ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle` | `Not a valid object name`; bundle head `bf9b20892d24… refs/heads/postfix` | ok as cited (the report names it with its bundle; round-36 routed defect answered) |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=8319cb76… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `8319cb76…` | ok |
| Fleet-root leftovers | `git -C /home/vgpnk/Projects/shokunin status --porcelain` filtered on kake | only ` M .ufo/state/kake.report-baseline` (driver runtime, not lane work) | ok |
| Prompt carries template contract | `diff templates/round-prompt.md <(sed -n 1,140p .ufo/prompts/kake-round-37.md)` | 22 differing lines, every one a `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitution; §§1–5 incl. §2b verbatim, hyaku §6 from line 141; prompt committed 23:46:03, 1 s before launch | ok |
| Gate registry row | `git diff 621fb528 8319cb76 -- SKILL.md` | `robots-expectation-audit` row (gate, verdict map 0/1/2/64, self-test command, frozen proof, write scope, owner) at `8319cb76` | ok |

Status: real report with checkable commits → `ok`.

Defects (status-neutral, routed below):
- Dead seat's item reassigned: `CtlC1Shortcut` died (429 quota, `.ufo/waves/round-37/dead-seats.txt`);
  its shortcut control was then built by the living `CtlC1NoReader` as a "disclosed follow-up".
  Prompt §6 says "Never replace a dead seat." Disclosed, and it produced the round's most
  informative control, but it is a replacement in substance.
- Declared order not kept: SCORECARD@202d625a declares control receipts "committed before any
  build"; the shortcut receipt landed at `ccc3b2b9` (00:29:45), 7 min 15 s after the wave-1 build
  seat was dispatched (00:22:30) — confirmed from `w2/ReviewTimeline.md` and `git log`.
- `SCORECARD.md` `## Capabilities` gained the row "Offline robots.txt expectation audit" (b99b6679)
  for a claim that this closure does not admit (below).
- `verification/postfix/robots-selftest-137-on-postfix-tool.json` names the tool by path only
  (`tool: …/scripts/robots_audit.py`), not by revision or sha256; the tip tool sha256 is
  `944d2f51…d3e5`, unpinned in that receipt.

## Claims (step 2)

### C1 — operability (capability): `scripts/robots_audit.py`; frozen predicate `met: passed >= 25 of 28 sealed cases`

Evidence-verified (lane-owned counter `sealed_count.py`; not executed).

| Re-derivation | Command | Observed |
|---|---|---|
| Tool absent at base | `git cat-file -e 621fb528:scripts/robots_audit.py` | `fatal: path … exists on disk, but not in '621fb528'` |
| Build bytes = seat file | `git cat-file -p 9dbc88bb:scripts/robots_audit.py \| sha256sum` | `5eb767ec68a6…542cabae` (report: `5eb767ec…cabae`) |
| Tip tool differs (post-measurement fix) | same at `8319cb76` | `944d2f51f396…bf1d3e5` (wildcard repair at `b99b6679`, counts toward no claim) |
| Before receipts | `jq -c '{passed,met,predicate,revision}' verification/c1-keyrev-at-{621fb528,202d625a,4b089da6,ccc3b2b9,528a6d02}.json`; `.exit` | each `passed 0, met false`, exit 1, predicate `passed >= 25 of 28 sealed cases` |
| After receipt | same on `c1-at-9dbc88bb.json`, `c1-keyrev-at-9dbc88bb.json` | `passed 28, met true`, revision `9dbc88bb…`, exit 0 |
| Reveal commit | `c1-keyrev-at-424aa248….json/.exit` | exit 2, `passed null` (refused, as reported) |
| Control receipts | `jq -c '{passed,met}' verification/control-*.json`; `.exit` | AllFalse 4, ConstantClean 0, Junk 0, NaiveReader (stock `urllib.robotparser`) 20, NoReader 0, r36-junk 0 — all exit 1; **`control-CtlC1Shortcut-followup` 28, met true, exit 0** |
| Control timing | `git log --diff-filter=A --format='%h %cI' -- verification/control-CtlC1Shortcut-followup.json scripts/robots_audit.py` | control `ccc3b2b 00:29:45`; build `9dbc88b 00:39:37` — the control met the predicate before any build landed |
| Declared consequence | `git show 202d625a:SCORECARD.md \| grep -n 'fixed before any'` | line 1666: "A control that meets the predicate means the counter is wrong, and it is fixed before any build."; line 1893: "A control that meets a predicate means that counter or target is wrong; it is fixed before any build, with the original rule kept as the rule of record" |
| What the lane did | `git show 8319cb76:SCORECARD.md` lines 1950–1972 | "Disposition … this control does not skip the claimed work … C1 is kept as declared; the predicate, key and counter are unchanged." |
| Lane's own later criterion | `corpus/QUALITY.md:926` | "(j) … If a control meets the predicate before data, the counter is redesigned … or the claim is dropped or declared exploratory; a disposition that reclassifies the control is not an option unless the declaration named that class beforehand." |

**Ruling (on the declaration as written): C1 does not verify.** The measured numbers reproduce
(0 → 28 of 28 at `9dbc88bb`, counter unchanged), but the claim is judged on the rule declared before
data, and that rule says a control meeting the predicate makes the counter wrong and obliges a fix
before any build. A control met it (28/28, exit 0) at `ccc3b2b9`, before the build; the counter
was not fixed and no exploratory re-declaration was made. The declaration named no exception
for controls that "do not skip the claimed work", so the disposition is a rule change after a
seat had scored (prompt §6.9: "A rule changed after any seat has scored is not the claim's rule").
The counter also demonstrably fails to separate the contract from a stdlib-plus-patches tool
whose library disagrees with the contract on 6 of 9 ordinary-looking probes
(`w2/ReviewShortcutDisposition.md` lines 40–41), which is exactly the
failure the control rule exists to catch. Not admitted. This is not a finding of harm: the tool,
its 137/137 selftest and the independent implementation stand as non-claim work.

### C2 — operability: selftest fixtures kill 32 round-36 mutants

Withdrawn before data at `4b089da6` (snapshot fixture control met 32 of 32,
`retained/controls/c2/c2-snapshot.json`). A gate reject, not a claim; it counts neither for nor
against admission. The withdrawal applied the declared consequence correctly.

### Harm check

`git diff --numstat 621fb528 8319cb76 -- SCORECARD.md SKILL.md PROVINCE.md LOG.md SHONEN.md
corpus/QUALITY.md corpus/SOURCES.md corpus/README.md corpus/knowledge` → zero deletions except one
line in `corpus/SOURCES.md` (S011 `used-by` widened, logged old→new in the lesson). No SCORECARD
axis row edited. Committed selftest evidence (`w2/ReviewHarm.md`, base vs tip clones): every
pre-existing lane selftest identical or grown (`source_recheck_selftest.py` 101/101 → 106/106,
base 101 fixtures pass on the tip tool and tip 106 pass on the base tool); new
`source_recheck_hardening_selftest.py` 6/6, `robots_audit_selftest.py` 131/131 at 79d3c780 and
`postfix/robots-selftest-137-on-postfix-tool.json` `verdict clean, 137/137`. No axis harmed.

### Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | unprovable-but-better | New offline robots audit with 137/137 selftest and independent-implementation agreement, but the declared counter cannot separate it from a 28/28 stdlib shortcut, so the claimed move is not proven |
| freshness | unprovable-but-better | `source_recheck.py` hardening (FIFO, size, MemoryError, quote-after-`=`) with base fixtures still green; non-claim, no frozen measurement |
| depth | unchanged | no claim |
| coverage | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim (tabi boundary restated in README/PROVINCE, not moved) |

## Discernment spot-check (step 3)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S095 Google "How Google interprets the robots.txt specification" | admit, A, docs, mined | https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec (re-opened 2026-10-23, before 04:03:22Z) | agree | Quote "The order of the groups within the robots.txt file is irrelevant." present verbatim under "Order of precedence for user agents"; the page also states 429 is handled unlike other 4xx and that specific and `*` groups are not combined — the Google-only differences the lesson marks |
| S097 robotstxt.org "A Standard for Robot Exclusion" (1994) | reject, C, community | https://www.robotstxt.org/orig.html (re-opened 2026-10-23, before 04:03:22Z) | agree | Quote "It is not an official standard backed by a standards body" present verbatim under "Status of this document"; the text has only `User-agent`/`Disallow`, recommends "case insensitive substring match", and forbids multiple `*` records — every located reject reason holds; superseded by S011 |
| S096 google/robotstxt (new SOURCES row) | admit, A, code, mined | `curl -sL https://raw.githubusercontent.com/google/robotstxt/master/README.md \| grep -n -i 'production code'` | agree | Line 20: "…production code used by Googlebot, Google's crawler…" — Gate quote "production code used by Googlebot" (5 words, ≤25) is an exact substring; SOURCES row 104 scope and teaches match the README |
| C1 keep-disposition (`ccc3b2b9`) | claim kept after a control met its predicate | `git show 202d625a:SCORECARD.md` line 1666 and `verification/control-CtlC1Shortcut-followup.json` | disagree | Declared consequence was "fixed before any build"; it was not applied (see C1 ruling); the lane itself encoded this as QUALITY (j) |
| C2 withdrawal (`4b089da6`) | withdrawn before data | `retained/controls/c2/c2-snapshot.json` (met true) | agree | The declared consequence was applied before any data |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kake` → exit 0; three `W04` duplicate-URL warnings (S033, S088,
S092, all pre-existing) and `kake ok …/corpus/SOURCES.md`; matches the report's census-after.
Rows 94 → 97 as reported (S095–S097 at lines 103–105).

## Trend verdicts

- **expansion: improved.** `corpus/knowledge/robots-txt-rules.md` (new, 83 lines) opens with
  `source: S011, S095, S096`, all three `mined` rows; coverage map row "Offline robots.txt
  expectation audit (r37)" and the knowledge-entry pointer added to `corpus/README.md`; ground the
  map held only as "robots.txt only at the host root" (r20 crawl-scope row). This rests on the
  source gate, not on C1; the capability is not counted (`capabilities_added` empty).
- **quality: improved.** S011 re-opened and its retained text matched live by two independent
  scouts (`w1/ScoutReopenS011.md`, `w2/ReopenGateS011.md`); round-36 routed repairs landed with
  receipts (5 mutant survivors killed, source_recheck hardening, criteria v2); no admitted entry
  failed its re-check in this closure's sample.
- **discernment: unchanged.** For: source-gate admit and reject both agree on re-open; C2 withdrawn
  per its declared consequence. Against: the claim gate overrode its own declared consequence for
  C1 in the same round, and QUALITY (j) — the lesson-grounded criterion that names that mistake —
  was not applied to the round's own standing claim and records "Check: none yet".

## Routed defects (kake owes, next round)

1. Append a SCORECARD correction: C1 (round 37) not admitted at closure; the `## Capabilities` row
   "Offline robots.txt expectation audit" carries that status (appended, not rewritten).
2. Redesign the C1 sealed counter (or declare a new claim) so that the stdlib-plus-six-patches
   shortcut (`retained/controls/CtlC1Shortcut-followup-robots_audit.py`) scores below target before
   any data; keep the round-37 counter as the rule of record.
3. Give QUALITY (j) an executable check (it says "Check: none yet").
4. Dead seats stay dead: a dead control seat's item is reported unbuilt, never moved to a living
   seat (prompt §6 "Never replace a dead seat").
5. Pin the tool revision or sha256 in post-measurement selftest receipts
   (`verification/postfix/robots-selftest-137-on-postfix-tool.json`).
6. The report's carried items stay open (source_recheck size cap and body-path race, manifest
   `MemoryError`, robots `NaN`/malformed URLs, criteria false passes/fails, two undecided robots
   contract points, the unsourced U+FFFD rule, S011 superseding row).

SHONEN: all four boxes are `[~]` with pointers a non-author can follow (SKILL gate registry at
`8319cb76`, LOG round 37 + `realrun/audit.json`, wave-2 re-runs from written commands, PROVINCE
round-37 step). They look checkable by a non-author; promotion is operator-owned.
