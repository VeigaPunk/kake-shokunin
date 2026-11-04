# Round 40 — sitemap audit repairs (C1) and round-39 routed defects

author: kake L1, round 40 attempt 1 (KakeR40)

Claim and frozen rule: `SCORECARD.md` "Round 40 — C1 declared". Base `f171c58b`. Outside check of
round 39: `corpus/lessons/round-39-verifier-spotcheck.md` (not edited here).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-40/sources/`, sums in
`SHA256SUMS` there; quotes found in the fetched HTML with markup stripped).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S110 | https://www.w3.org/TR/xml/ | 2026-10-23T08:28:47Z, HTTP 200 | "When an XML 1.0 processor encounters a document that specifies a 1.x version number other than '1.0', it will process it as a 1.0 document." (§2.8, Note after [26]) | admit, A, spec, mined; also §2.2 "[2] Char ::= #x9 \| #xA \| #xD \| [#x20-#xD7FF] \| …" (no #x0) |
| S111 | https://docs.python.org/3/library/urllib.parse.html | 2026-10-23T08:28:47Z, HTTP 200 | "leading C0 control and space characters are stripped from the URL. \n, \r and tab \t characters are removed from the URL at any position." (`urlsplit`) | admit, A, docs, mined |
| S112 | https://www.w3.org/TR/xml-names/ | 2026-10-23T08:29:16Z, HTTP 200, sha256 = S106's | "The comparison is case-sensitive, and no %-escaping is done or undone." (§2.3); `ignor` occurs 0 times in the page (and 0 times in S102) | admit, supersedes S106 (routed defect 1) |
| S113 | https://www.w3.org/TR/xmlschema11-2/ | 2026-10-23T08:29:16Z, HTTP 200, sha256 = S107's | "dateTimeLexicalRep ::= yearFrag '-' monthFrag '-' dayFrag 'T' ((hourFrag ':' minuteFrag ':' secondFrag) \| endOfDayFrag) timezoneFrag?" (§3.3.7.2 [16]); [18] dateLexicalRep has no time part | admit, supersedes S107 (routed defect 1) |
| S114 | https://yandex.com/support/webmaster/en/controlling-robot/sitemap | 2026-10-23T08:29:16Z, HTTP 200, 223,735 bytes | "The total character limit is 2048. 1024 Characters are intended for the site’s domain name" (U+2019) | admit, supersedes S109 (routed defect 1) |

Row changes: S110–S114 added. No `status`, `recheck` or `used-by` change to an existing row
(S106, S107, S109 stay as written; the superseding rows carry the corrections, CORPUS.md §SOURCES
rule 2).

Rejects this round (recorded before data):
- **Rejected: routed defect 2's "fix D1" (XML 1.x accepted).** Reason: S110 §2.8 — an XML 1.0
  processor processes a `1.x` declaration as a 1.0 document, so `version="1.1"` with 1.0 content is
  well-formed XML 1.0 and sentence 8 holds; `version="2.0"` already gives `xml_malformed`
  (`.ufo/waves/round-40/l1-probe.py`). The tool is not changed for D1.
- **Not changed: D3** (`doctype_present` over a malformed remainder). Reason: sentence 9 is the lane's
  safety reading and the round-39 build declared this precedence; the contract does not order (b)'s two
  sentences, and changing it would be a contract change, not a repair.

## Wave 1 — source re-opens and row corrections

Fresh scouts re-opened S110–S114 (`.ufo/waves/round-40/w1/Reopen*.md`; live sha256 equal to the retained
bytes for S110–S113; S114's page bytes vary, visible text equal). Decisions:
- **S110, S112, S113 hold** as written (every `teaches` clause located).
- **S111 `teaches` "must reject those values before splitting" — accepted as overstated** (`ReopenS111`):
  the page says what `urlsplit` strips and warns "urlsplit() does not perform validation"; the rejection is
  the lane's contract reading. Correction row **S115** (`supersedes S111 —`), written after the L1 re-read
  the retained bytes (`.ufo/waves/round-40/sources/py-urllib-parse.html`, sha256 `835af739…`, the Warning
  at line 419).
- **S114 "same-domain URLs only" — scout's "overstated" rejected.** Reason: the page says "Specify only
  page links of the domain where the file will be located." (retained `yandex-sitemap.html`, located in the
  stripped text by the L1); that is same-domain URLs only. The scout read "same domain" as file placement
  only; the sentence before the placement sentence is about the listed links. S114 stands.
Row changes: S115 added. No `status`, `recheck` or `used-by` change to an existing row.

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S115 | https://docs.python.org/3/library/urllib.parse.html | 2026-10-23T08:28:47Z (retained), re-fetched 08:38:34Z by `ReopenS111`, same sha256 | "urlsplit() does not perform validation." (Warning under `urlsplit`) | admit, supersedes S111 |

## Wave 1 — the control wave fired the kill rule

27 of 76 control receipts meet the frozen predicate (`SCORECARD.md` "Round 40 — kill rule (1) fired";
`.ufo/waves/round-40/verification/w1/`). C1 is exploratory. The build still landed (`56d57ee4`): selftest
150 → 179 fixtures, 23 new fixtures red on the round-39 bytes (`verification/build/selftest-new-on-base.txt`,
`PASS 156/179`, exit 1) and green on the build (`selftest-new-on-build.txt`, `PASS 179/179`, exit 0); the
new fixtures include the sub-shapes five meeting controls exploited (LF in `sitemapUrl`, leading NUL and
U+001F, TAB in a query, LF in a fragment, UTF-16 index, upper-case repeated id). Real run on the six
round-39 public sitemaps: byte-equal JSON to the round-39 build (`jq -S . | sha256sum` →
`fd985a41…`, `verification/harm/realrun-build-56d57ee4.json`). Counter at the build: 30 of 30, selftest
150/150, met — information only (`verification/c1-at-56d57ee4*.json`).

Other wave-1 findings carried to the report: `CriticD1Reject` holds the D1 rejection;
`ReviewD3Reading` holds "D3 not changed" (its F1: the round-39 D3 wording is broader than the behaviour —
a parse must reach the DOCTYPE); `ReviewWitnessContract` agrees with all 30 witnesses (F3: no witness
repeats a valid check's id); `ReviewCounterCode`: environment failures exit 1 without a receipt instead
of 2 (MEDIUM), judge leniencies (LOW); `ExecIndependentOracle`: libxml2 agrees with the contract on E only
partly (it re-sniffs UTF-16 when a declaration is present) and has no leverage on U, so an oracle-backed
measured claim next round needs an RFC 3986 absolute-URI checker, not xmllint.

## Mistakes

1. **Class: a counter frozen on author-only controls, against a routed defect.** Evidence: the
   declaration `f043c721` names only L1 controls and the L1 reference (`SCORECARD.md` "Round 40 — C1
   declared"); the round-39 spot-check routed "any later countable sitemap claim must first pass
   QUALITY (o): non-author mutant families and a tweaked shortcut scored below target before the
   declaration freezes the key" (`round-39-verifier-spotcheck.md` routed defect 4); after the freeze,
   27 of 76 non-author controls met it, including a key-finder and a label replay through the
   `case-<witness id>` directory name visible in `/proc` (`CtlKeyFinder.md`, `CtlLabelKeyed.md`).
   The L1 read (o) as applying to sealed keys only. Captured-by: QUALITY (o) — the rule existed and the
   routed defect named it; not applied. Fix: QUALITY (o) amended for round 40 (any counter, public or
   sealed) with an executable check `.ufo/waves/round-40/criteria/preseal_order_check.py`. Shown able to
   fail: red at the round-40 declaration `f043c721` (0 non-author receipts with the counter's sha256,
   exit 1) and at the round-39 declaration `ceecb1b1` (exit 1); green at `12211cc5` (76 receipts, exit 0)
   (`.ufo/waves/round-40/verification/criteria/preseal-*.txt`).
2. **Class: a routed defect taken as a requirement without re-deriving it from its source (near-miss).**
   Evidence: spot-check routed defect 2 said "fix D1" (XML 1.x accepted); S110 §2.8 says an XML 1.0
   processor processes a 1.x document as 1.0, so the fix would have made the tool reject well-formed
   XML 1.0. A D1-"fixed" mutant meets the C1 counter (`ExecD1Check`: 30/30, 150/150), so nothing the
   round measured would have caught it. Captured-by: none. Fix: QUALITY (q) and
   `.ufo/waves/round-40/criteria/d1_check.py` plus selftest fixture `r40_d1_version_1_1_clean`. Shown able
   to fail: `d1_check.py` exit 1 on `criteria/mutant_d1_fixed.py`, exit 0 on the base and the build
   (`verification/w1/d1check-{base,ref,mutant}.txt`).

Sweep for others (`ScribeMistake.md`, read-only over rounds 38–39 lessons and spot-checks): QUALITY (n)
still has no check; the round-39 lesson's "5 false accepts in 15" and "seven returned source or diffs" are
corrected below.

## Corrections to round 39 (appended; the round-39 report and lesson are not edited)

Re-derived from committed bytes by `ScribeR39ReportCorrections` (commands in its report):
1. Report "surface unmoved": `git ls-tree -r --name-only 565ef4c9 scripts/ | grep -c sitemap_audit` gives
   **2** (tool and selftest); `grep -cx scripts/sitemap_audit.py` gives 1.
2. Report and lesson Mistake 3: **six** critic seats returned source or diffs (three source, three diffs);
   `CtlValuesOnly` and `CtlHandTokenizer` wrote their files; `CtlStructureOnly` was refused.
3. Lesson Gate rejects: the criterion-(o) draft checker gave **5 false accepts in 7 adversarial samples**
   (`w2a3/MutCriterionO.md`), not "in 15".

## Residual call — findings and what changed

Eight seats (`.ufo/waves/round-40/resid/`). Holds: the 27-of-76 tally and commit order
(`RerunKillAndBuild`, `ReviewRoutedDefects`), harm sweep (`ReviewHarm`: no deletions outside the
repaired branches, other tools' bytes equal, robots selftest 204/204, real run byte-equal), Mistakes and
criteria checks re-run red/green (`ReviewLessonQuality`), source decisions (`CriticSourcesDecisions`,
with one fixable defect: S115's scope still says "not S027's 'parsing is not validation' scope" while its
`teaches` now includes the non-validation warning — corrected by S116). Advisory exploratory judgment
(lane seat, not of record): `unprovable-but-better` (`KakeR40.ExploratoryVerdictC1.md`).
**Regressions found and fixed:** `CriticBetterClaim` F1–F3 (NUL vs declared encoding, NUL vs DOCTYPE,
foreign TAB inside `loc`) — confirmed red on `56d57ee4` by four new fixtures and fixed (SCORECARD
"build revised after the residual attack"). Not fixed, recorded: `ReviewBuildRepairs` — interior C0
controls other than TAB/CR/LF and a trailing space in `sitemapUrl` still pass (both builds; outside the
declared class; sentence 4 with S102's RFC 3986 rule would exclude them); `ReviewCounterCode` —
environment failures exit 1 without a receipt.

Carried, still open (verified at `f043c721` by `w1/ScoutCarriedItems.md`): round-38 routed defect 6 items
2–10; (j) survivor M06; `MutRecheckOversize` M4 and M8.

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S116 | https://docs.python.org/3/library/urllib.parse.html | 2026-10-23T08:28:47Z (retained bytes `835af739…`, re-read by the L1 at line 419) | "urlsplit() does not perform validation." | admit, supersedes S115 (scope wording) |

Row changes: S116 added. No `status`, `recheck` or `used-by` change to an existing row.
