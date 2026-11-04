author: hyaku closure (non-author integrator, @m_zfl)

# Round 76 — non-author verifier spot-check (kake)

Lane `kake`, round 76 (hyaku run 15, attempt 1). I did not author this round and did not improve it.
Base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`; lane tip `a1b3f33b9d00137b1c45c5b4c274ce8f0cc95446`;
report `.ufo/reports/round-76/kake.md` (fleet commits `1058eaf3`, erratum `eb912c3f`, author
`kake-shokunin <kake@shokunin.local>`). Every command below was run read-only over committed bytes
(`git show <rev>:<path>`); no lane gate was executed (PROTOCOL §Gate standard, *Closure consequence*),
so each claim is labelled **re-measured** (my own plain count/digest) or **evidence-verified** (the
instrument's committed receipt, self-test tally and measured revision).

Driver digest (`.ufo/watchdog.log`, mutable — copied, not the live-line pointer):

```
2026-11-03T21:37:27-03:00 launch kake round=76 pgid=2344261 driver=hyaku-inline attempt=1
2026-11-03T22:22:34-03:00 complete kake round=76; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Ruling |
|---|---|---|---|
| Report identity | `git log --format='%an %H %s' -- .ufo/reports/round-76/kake.md` | two commits, both `kake-shokunin <kake@shokunin.local>`: `1058eaf3 round-76: kake report`, `eb912c3f round-76: kake report erratum (wave results.json landed; final tip a1b3f33b)` | conform — lane identity, filed as erratum append |
| Filing order | `git log -1 --format=%cI` on the report and lane tips | report `1058eaf3` 22:21:24 cites tip `284a00fb` (22:20:32); erratum `eb912c3f` 22:21:58 follows `a1b3f33b` (22:21:46) and names the superseded text | conform — lands after its cited lane work; erratum is a new commit, not a rewrite |
| `SHONEN` heading | `grep -c '^## SHONEN'` + box count | `1` heading; 4 box lines, all `[~]` with resolvable pointers | conform |
| Cited lane commits | `git cat-file -e <h>^{commit}` then `git merge-base --is-ancestor <h> refs/heads/master` for `b758cb04 783c7c13 e674bc60 6b52407b f4f076ba 442d36c6 152bffd5 d2555766 d00ea7fb 2cccd59a 9dea7b2f b8673e87 7ac91803 b5597f55 ffbb2e69 284a00fb a1b3f33b` and base `a0491fcd` | 18/18 `OK … kake-shokunin` (base `a0491fcd` is protocol-authored) | conform — no dead or orphaned hash |
| Worktree / push | `scripts/hyaku/jj-lane.sh state …/kake-shokunin`; `git -C … status --porcelain` | `branch=master local=a1b3f33b remote=a1b3f33b ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` prints `a1b3f33b…` | conform |
| Prompt contract | `difflib` of `templates/round-prompt.md` (140 lines) after rendering `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` against `.ufo/prompts/kake-round-76.md` lines 1–140 | one hunk: `<kake-repo>` → `kake-shokunin`; §6 hyaku addendum follows | conform — round-level items and all five child-lane items carried verbatim |
| Prompt durability | `git log -1 --format='%an %cI' -- .ufo/prompts/kake-round-76.md` | `kake-shokunin 2026-11-03T21:37:25-03:00` (tracked, two seconds before the launch line) | conform |
| Axes / route map | `grep '^kake|' shokunin.conf`; prompt §6 | axes line matches `operability + freshness (web properties and publishing)`; §6 quotes the run-15 map and the later net map (reviewer-only `@m_zfl`), naming `task.agentModelOverrides` as authority | conform — MISSION.md's role table is advisory and defers routing to the host; no binding bucket contradiction (dispatch-time note, not a lane defect) |
| Wave | `w1-results.json` + `w1/*.md` | `seats=15`, 15 results, 0 empty outputs; roles scout 2 / executor 5 / scribe 2 / reviewer 2 / critic 1 / mutation-tester 1 / connector 1 / sentinel 1 (attack 4/15 = 26.7 %); 15 seat reports on disk | conform — no undispatched wave, no dead seat |
| Marker test | real report, two checkable claims, 17 cited lane hashes | — | not a marker → status `ok` |

## 2. Claim re-checks

### C1 — calibration: claim rows quote receipt lines they can be found in

- **Before (evidence-verified).** `git show a1b3f33b:.ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt` →
  `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`,
  seven `T1` lines at `SCORECARD.md:4892` ×2, `4893` ×2, `4904`, `corpus/QUALITY.md:1499`,
  `corpus/lessons/round-75.md:82`, plus `missing corpus/lessons/round-76.md`.
- **After (evidence-verified).** `controls/after-c1-quote-truth-final.txt` →
  `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`,
  `observed-exit=0`; the non-final receipt prints the same verdict at `revision=master` (HEAD `b8673e87`).
- **Re-measured by me (plain reads, not the counter).** Parsed the committed `SCORECARD.md` §"Round 75 —
  quote corrections (appended round 76)": 5 correction rows (not the 7 the report says are in that
  section). For each row I compared the quoted "whole receipt line" with `git show a1b3f33b:<path>` at the
  named line: rows 1, 2, 4, 5 exact (1/1 each); row 3 quotes `after-c2-receipts.txt:5-6` as two lines, both
  exact. Every defective span is absent from its named receipt file (5/5 `defect-absent=True`). The
  `corpus/QUALITY.md` criterion quotes `ctl-deletion.txt:1` exactly (`C1v1 revision=afc73a87… rows=27
  live=15 files=15 mismatches=2 classes=E3 append_only=false met=false`), and the `round-75.md`
  §Corrections bullet quotes `ctl-deletion.txt:1` and `ctl-deletion-landed.txt:3` exactly (both re-read).
  The five SCORECARD rows + one QUALITY criterion + one lesson bullet close the seven base findings.
- **Digest / sensitivity.** `git show 7ac91803:scripts/doc_quote_truth.py | sha256sum` =
  `e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae`, the digest the report and
  SCORECARD name; committed self-test `selftest: 63/63 passed`; the no-repair control stays red
  (`ctl-do-nothing.txt`: `findings=8 met=false`), deletion trips `A1`, cheap content and junk correction
  trip their named ids, and `w1/MutationTesterGates.md` records `mutants=9 killed=8 survived=1` with the
  survivor named as an unreachable redundancy.
- **Verdict: improved** (calibration 2 HOLD by design). Clause not re-derived: the counter's own 7,934-file
  receipt population and its elision/diagnostic filters — the committed receipts and the samples above are
  the evidence.

### C2 — operability: offline hreflang declaration audit (capability acquisition)

- **Before (re-measured).** `git ls-tree -r --name-only a0491fcd | grep -c hreflang` → `0`; no audit
  exists at base.
- **After (re-measured + evidence-verified).** `scripts/hreflang_audit.py` is present at `2cccd59a` and
  `a1b3f33b` with sha256 `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` (the receipt's
  `tool_sha256`); `w1/ExecAuditTool/receipts/selftest.stdout.txt` = `selftest 59/59 passed`, `exit=0`.
  The matrix receipt `controls/after-c2-matrix.txt` prints `cases=71 decided=69 correct=69 wrong=0
  undecided=2 constants_failed=4/4 met=true`, `observed-exit=0`, four constants each `failed=69/69`, and
  `tool_sha256=0762452f…`/`cases_sha256=fa64d448…`. I re-derived the cases digest independently over the
  71 committed case JSONs at `a1b3f33b` with the matrix's documented algorithm → `fa64d448331aa0b2ae4a851afd6e5815919320e8f1381ece0c35283d3bbd9fb5`,
  equal to the receipt.
- **Real input.** `real-manifest.json` has 8 pages, sha256 `448ebd9c73c2f563e88a43cc784734447ebe46fc6a077f59e7d2c406a366bc47`;
  `controls/after-c2-realrun.txt` is the tool's JSON with `"pages": 8`, empty `findings`, `"exit": 0` plus
  `rc=0`. **Scope:** the seat ran a pinned predecessor copy
  `w1/ExecAuditRealRun/pinned/hreflang_audit_asrun_58a2cdcece48.py` (sha
  `58a2cdcece489b3c407c818b77398d428a3e38b3c0f6812db2e4bf7ace67955a`, selftest 55/55), not the landed
  `0762452f` (59/59); the seat discloses the five-build churn and shows the same exit 0 on its earlier red
  build. The landed bytes are bound by the matrix and self-test, not by this real-input receipt.
- **Revision defect.** The matrix receipt says `revision=master revision_ok=yes
  head=d00ea7fb1471f66bf6067cd6fcb5d82c743159c8`; `git cat-file -e d00ea7fb:scripts/hreflang_audit.py`
  fails (the tool landed in `2cccd59a`), so the report's "After, measured at `284a00fb`" is not what the
  receipt records. The run happened on a worktree whose HEAD was `d00ea7fb` with the tool uncommitted; the
  digest binding still identifies the measured tool bytes.
- **Verdict: improved** (operability 10 HOLD, capability). The capability is verified on the landed bytes
  by the matrix; the real-input receipt is supporting evidence with a disclosed predecessor build.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | base red `findings=7` at `a0491fcd` → after `findings=0 met=true` at `7ac91803`; the five SCORECARD rows + QUALITY criterion + lesson bullet re-quote exact receipt lines and every defective span is absent from its named receipt |
| operability | **improved** | new offline hreflang audit, matrix 69/69 decided correct with 4/4 constants failing, landed selftest 59/59, and a digest-bound capability row in SCORECARD |
| coverage | **improved** | new governed surface: knowledge entry added (66 → 67 files), README gains §"Coverage — round 76", PROVINCE moves hreflang declarations to Core, and the new tool governs the declaration surface; base `git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → 0 hits |
| freshness | unchanged | the freshness sweep still exits 1 on the single `~/projects` drift (open L0 `kake \| round-69`, disposition 5); no new stale entry was left unmarked |
| depth | unchanged | the round adds one knowledge entry and registry rows; no owned depth score moved, nothing weakened |
| adjacency | unchanged | connector re-read `merge/kake/` read-only and adopted nothing; no sibling scope absorbed |

No axis is harmed: `git diff --numstat a0491fcd a1b3f33b -- LOG.md SCORECARD.md corpus/QUALITY.md
corpus/SOURCES.md PROVINCE.md corpus/README.md` → `67/0 57/0 15/0 3/0 17/0 10/0` (zero removed lines in
every append-only file), and no owned axis score decreased.

## 4. Discernment spot-check (LEARNING.md — non-author)

| Item | Decision | Source re-opened | Agree? | Reason |
|---|---|---|---|---|
| S444 Google localized versions | admit | retained `w1/ScoutHreflangSources/google-localized-versions.txt` lines 362–364 **and** a live `curl -sSL` (HTTP 200, 199,242 B) tag-stripped | **agree** | the 13-word quote "Each language version must list itself as well as all other language versions." is at lines 362–364 and in the live text; the row's tier-A docs scope (Google's stated annotation rules, not selection/ranking/language detection) matches the page; live byte count 199,242 equals the entry's re-fetch record, not the retained 199,246, which the entry already discloses as volatility |
| S446 RFC 5646 / BCP 47 | admit | retained `w1/ScoutHreflangSources/rfc5646.txt` lines 1053–1054, 327–328 | **agree** | both quoted sentences are present (13 words and 20 words, both ≤25); the row's `teaches` and the entry's ABNF reading (lines 231–236) match the file |
| "Google requires a hreflang target's canonical to be itself" | reject as sourced fact | retained Google text + live text: `grep -in 'canonical' google-localized-versions.txt` → lines 19, 121–124, 298 only (navigation), no self-canonical sentence; RFC 5646 uses "canonical" only in tag canonicalization | **agree** | no opened source states the rule; the entry labels `hreflang_canonical_not_self` a lane policy in those words |
| `x-default` "the only non-tag value" | reject / Google-grounded only | `grep -ic 'x-default' whatwg-links.txt rfc5646.txt` → `0` and `0`; S444 contains the x-default section the entry cites | **agree** | the reserved status rests on S444 alone, and the entry attributes it there rather than generalising |

New `corpus/SOURCES.md` rows: S444 anchor `§ Guidelines for all methods (tag-stripped lines 361-372)` and
its quote at 362–364 (13 words); S445 quote at line 1356 (10 words); S446 quote at 1053–1054 (13 words) —
each ≤25 words and each re-found in its retained file; the S444 live re-fetch still carries the quote.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → `kake ok`, exit 0,
184 rows; it prints 17 `W04` warnings, including `S445 duplicate url
html.spec.whatwg.org/multipage/links.html across scopes`. The base blob has 16 (`--file` over
`git show a0491fcd:corpus/SOURCES.md`), so the new row adds the 17th — the scout disclosed exactly this at
`w1/ScoutHreflangSources.md:206-221`.

Result: 4 of 4 sampled decisions agree; no disagreement to learn from, and no rejection rests on a source I
could not re-open.

## 5. Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry on ground the coverage map did not hold
  (`hreflang-declaration.md`, knowledge files 66 → 67; base `git grep -in hreflang a0491fcd -- PROVINCE.md
  corpus/README.md` → 0, README gains §"Coverage — round 76"), citing three `mined` rows opened this round
  (S444–S446, all tier A; registry 181 → 184). Qualified: one entry, and the two prior entries that mention
  hreflang in passing (`static-canonical-preflight.md:20`, `keeper-timer-inert.md:164`) are not
  cross-linked; the report's "frontier to core" phrasing overstates a base frontier row that did not exist.
- **quality — improved.** A weaker state (seven claim rows quoting spans no receipt contains) was repaired
  and is now re-derivable from whole receipt lines; the new instrument fails on the base and greens only
  after the repair; the delivered hreflang tool decides the frozen matrix on its landed bytes and carries a
  self-test. No admitted entry was found false. The report-level evidence defects routed below are
  documentation, not corpus falsity.
- **discernment — improved.** The Gate records three admits and two rejects with flip conditions, and this
  outside spot-check agrees on all four sampled items; the round amended its own contract eight times
  (including the diagnostic-receipt laundering tautology and the un-runnable self-test) and disclosed the
  source-vs-contract divergence rather than smoothing it.

## 6. Routed defects (status-neutral; the lane fixes them next round)

1. **C2 measured revision and real-input build scope.** The report says C2 was "measured at `284a00fb`", but
   `controls/after-c2-matrix.txt` records `revision=master revision_ok=yes head=d00ea7fb…`, and
   `scripts/hreflang_audit.py` does not exist at `d00ea7fb` (it lands at `2cccd59a`). The real-input
   receipt is from the pinned predecessor `hreflang_audit_asrun_58a2cdcece48.py` (selftest 55/55), not the
   landed `0762452f` (59/59). Name one revision per artifact and either re-run the matrix and the 8-page
   manifest on the landed digest at a committed revision, or state the build split in the report and the
   capability row. (This repeats the r75 routed defects 3 and 7 class, which the lesson's §Routed dispositions
   rows 3 and 7 mark fixed.)
2. **Sources & frontier W04 count.** The report's after-state reads "same 16 pre-existing W04 duplicate-URL
   warnings, unchanged"; the tip census is 17 (16 inherited + `S445 duplicate url
   html.spec.whatwg.org/multipage/links.html across scopes`), as the scout's own fixture receipt says. State
   17, or say the 16 inherited are unchanged and name the new one.
3. **Report quote rendering.** `pages=8 findings=[] exit=0` is not a contiguous substring of
   `controls/after-c2-realrun.txt` (the receipt is one JSON line plus `rc=0`). Quote the JSON or mark the
   rendering — the whole-line rule C1 enforces on SCORECARD rows applies to the report's evidence too.
4. **Correction-row count/location.** The report and the SCORECARD claim row say seven whole-line
   corrections "in `SCORECARD.md`"; that section holds five rows (the other two findings are closed by the
   `corpus/QUALITY.md` criterion and the `corpus/lessons/round-75.md` bullet). State 5 + 1 + 1.
5. **"Frontier to core" wording.** Base `PROVINCE.md`/`corpus/README.md` hold no hreflang row
   (`git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md` → 0), so the area entered from unlisted
   ground, not from a declared frontier row; the PROVINCE text "are now core" is accurate, the report's
   "entered from frontier to core" is not.
6. **Deletion-control parenthetical.** The report describes the deletion control as `(A1,
   append_only=false)`; the committed `ctl-deletion.txt` v1 line prints `A1` and no `append_only=` field.
   State `A1` only.

## 7. Status

`CLOSURE kake r76 status=ok admitted=true`. Both claims verify: C1 is re-measured (five SCORECARD rows,
one QUALITY criterion and one lesson bullet quote exact receipt lines; the base is red and the after receipt
green) and C2 is evidence-verified on the landed tool digest plus the re-derived cases digest and
self-tests; no owned axis is harmed, and the three trends are `improved`. Routed defects 1–6 are
documentation and evidence-scope hygiene; none touches either claim's measurement.

Operator note: the four `SHONEN.md` boxes look fully checkable by a non-author from the repo (box 1:
`SKILL.md` §"Round 76 gate registry additions" with two full registry rows and the `How to verify`
commands; box 2: the real-input hreflang run and the C1 repair chain in `LOG.md` §Round 76; box 3: both
instruments' argv and self-tests; box 4: the `PROVINCE.md` §"Round-76 hreflang frontier step" boundary and
the connector's no-contention finding). Promotion is operator-owned and was not touched.
