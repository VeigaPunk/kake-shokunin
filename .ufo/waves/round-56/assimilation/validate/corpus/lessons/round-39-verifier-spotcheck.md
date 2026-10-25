# Round 39 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Lane round: kake 39 (attempt 3, L1 `KakeR39A3`). Base `2909f1dcf2a4e411394a5093c4ed811a81809895`,
tip `f841a48d8591b014dc706a3a47e44ce5c17454f4`. Report: fleet `.ufo/reports/round-39/kake.md`
(fleet commit `61d5d79e2788841749cd7e5c833ccbbf267f01e2`). Closed 2026-10-23 (checks 08:08–08:20Z).
Commands were run by this integrator or by six read-only closure seats it dispatched
(`HyakuCloseKake39.R39{PromptConf,CriticCopies,KillRule,BuildEvidence,Harm,SpotSources}`).
No lane gate, selftest or counter was executed (PROTOCOL §Gate standard, Closure consequence):
claim evidence below is evidence-verified against committed bytes, not re-run.

Driver digest (`.ufo/watchdog.log`, copied):

    2026-10-23T02:10:15-03:00 launch kake round=39 pgid=4010800 driver=hyaku-inline attempt=1
    2026-10-23T02:26:46-03:00 lane-dead-no-report kake round=39; retry same round (attempt 1: L1 died with the orchestrator process exit at 05:25:25Z)
    2026-10-23T02:26:48-03:00 launch kake round=39 pgid=2561054 driver=hyaku-inline attempt=2
    2026-10-23T03:40:36-03:00 lane-dead-no-report kake round=39; retry same round (attempt 2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z)
    2026-10-23T03:40:38-03:00 launch kake round=39 pgid=3140591 driver=hyaku-inline attempt=3
    2026-10-23T05:07:26-03:00 complete kake round=39; hyaku-inline attempt=3

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report identity | `git -C <fleet> log --format='%an %H %cI' -- .ufo/reports/round-39/kake.md` | `kake-shokunin 61d5d79e… 2026-10-23T05:06:59-03:00`; `show --stat` touches only the report (+154) | pass |
| Report after its commits | tip `f841a48d` committed 05:06:10-03:00 | report 49 s later | pass |
| SHONEN heading | report `## SHONEN` | 4 lines, one per box, all `[~]` with pointers | pass |
| Cited hashes | each 8-hex token in the report: `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` | 16 commits exist, all ancestors of `master` and descendants of the base; `16440f62`, `f3a0cd60`, `f4d057c4` are sha256 prefixes, not commits | pass |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain` | `local=remote=f841a48d… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | pass |
| Prompt contract | rendered `templates/round-prompt.md` (kake/39) vs `.ufo/prompts/kake-round-39.md` | only deltas: `<kake-repo>` rendered and the appended hyaku §6 addendum; 0 unrendered `{{`; round-level and five child-lane items present; no L2 route map quoted | pass |

Not a marker: 16 lane commits, 551 files changed (`git diff --stat 2909f1dc f841a48d`).

## Claim C1 — exploratory, operability (capability `scripts/sitemap_audit.py`)

### Frozen apparatus and kill rule (re-measured over committed bytes)

- Counter: `git show <rev>:.ufo/waves/round-39/sealed_count.py | sha256sum` at `ceecb1b1`, `4c080d3d`,
  `565ef4c9`, `f841a48d` → all `f3a0cd6053497cd0…6084593` = SCORECARD pin.
- Key: `git show aa73d919:.ufo/waves/round-39/sealed/cases.json | sha256sum` →
  `16440f62803e25fee5e17e77bae88636fa0c711b0fa26024ec78d4134767c10b` = pin `16440f62…4767c10b` in
  `ceecb1b1:SCORECARD.md:2374`.
- Predicate and contract: `met: passed >= 24 of 24 sealed cases` (`ceecb1b1:SCORECARD.md:2367`);
  `git diff ceecb1b1 f841a48d -- .ufo/waves/round-39/c1-contract.md` → empty; the "Round 39 — C1
  declared" block has additions only after it.
- Kill rule (1) is part of the declaration: `git log -S'Kill rule, frozen now' -- SCORECARD.md` →
  `ceecb1b 2026-10-23T02:40:00-03:00` (`SCORECARD.md:2394`, "if any control receipt meets the predicate,
  C1 is declared exploratory (no counter, verdict from a named non-author reviewer)"). One closure seat
  reported it first appearing at `57bdd802`; the pickaxe above refutes that.
- Fired before the build: `4c080d3d` (03:59:44-03:00, "kill rule (1) fired … before any build is
  dispatched") and `57bdd802` (04:01:41) precede the build `565ef4c9` (04:53:06).
- Tally: `jq -s 'map(select(.met))|length' .ufo/waves/round-39/verification/a3/w1a3-Mut*.json` → 15 of
  54 receipts; `w1a3-CtlRegexTweak.json` and `c1-keyrev-CtlRegexTweak.json` `met` true (24);
  `base-2909f1dc.json` false (0). 15 `w2a3/Verify*.md` each call one met mutant a valid control (1:1).
  Three met mutants diffed against `aa73d919:…/sealed/reference.py` are single localized changes
  (UrlAuthority M03, NamespaceBinding M09: one line; EntryNumbering M02: one loop, 5 lines).

The consequence was applied as frozen; no rule changed after data. Unlike rounds 37 and 38, the
round followed its own declaration.

### Critic transcriptions (control copies)

`HyakuCloseKake39.R39CriticCopies` compared committed bytes with each seat's returned text
(`w1a3/<Seat>.md` and transcripts): CtlEngineLenient, CtlStdlibConvenience, CtlHtmlParserReader (source
returned) and CtlGuessTweak, CtlRegexTweak, CtlXsdTweak (diffs returned; patch over the dead-seat base
reproduces the committed `.py`) are byte-identical. CtlValuesOnly and CtlHandTokenizer wrote their files
themselves; CtlStructureOnly is a leftover of a refused seat (met false). All 16 met receipts'
`toolSha256` equal the committed bytes. The 54 mutants were written directly by mutation-tester seats
(no transcription). **No control result depends on an unverified transcription.** The kill rule
fires on the 15 mutants alone, independent of the one transcribed control that meets
(`CtlRegexTweak`, itself verified byte-exact: diff `28f6f65a…`, tool `2d941dab…`).

### Build evidence (evidence-verified; not executed)

| Item | Committed evidence | Observed |
|---|---|---|
| Surface before→after | `git ls-tree -r --name-only <rev> scripts/ \| grep -c sitemap_audit` | 0 at `2909f1dc` → 2 at `565ef4c9` and `f841a48d` (tool + selftest) |
| Tool unchanged after build | `git diff 565ef4c9 f841a48d -- scripts/sitemap_audit*.py` | empty; tool sha256 `6d86c8ce…` = receipt pin |
| Selftest | `verification/build/selftest.txt` | `PASS 150/150`, exit 0; fixtures counted in source 131 `add(` + 19 `lastmod_case(` = 150 |
| Copy guard | `verification/build/copy-guard.txt` | max ratio 0.2868 vs reference, 0/22 pairs flagged |
| Contract witnesses | `resid/ReviewBuildWitnesses.md` | 18/18 identical |
| Real run (6 public sitemaps) | `verification/realrun/build-565ef4c9.json`, `reference-663e051e.json` | `jq -S . \| sha256sum` equal (`fd985a41…`), `cmp` exit 0; 4 clean, fsf.org 212 and nodejs.org 8 `loc_out_of_scope` |
| Contract review | `resid/ReviewBuildContract.md` | ~160 probes; 4 deviations + 1 ambiguity (D2 UTF-16 without BOM → false `clean`, MED) |
| Builder blindness | `w2a3/BuildSitemapAudit.md`; key revealed `aa73d919` after build `565ef4c9` | consistent |
| Registry | `SKILL.md:1118-1135` | row `sitemap-file-audit`, gate, verdict map 0/1/2/64, selftest spelling recorded |

### Non-author verdict on C1 (this integrator): **unprovable-but-better**

The lane's own `KakeR39A3.ExploratoryVerdictC1` is a lane-dispatched subagent and does not count
(LEARNING.md "A subagent the lane dispatched is still the lane"); this is the verdict of record.

Why unprovable: the frozen counter cannot separate the build from 16 controls (15 contract-breaking
mutants and a parser-free regex reader meet 24 of 24), so no count decides the claim.

Why better, with reasons:
1. The prior state had no sitemap-file auditor (0 at base); `robots_audit.py` ignores `Sitemap`
   records and PROVINCE listed sitemaps as open.
2. The tool is a coherent stdlib implementation of the frozen 34-sentence contract. Read here:
   `scripts/sitemap_audit.py:172-196` decodes UTF-8, enforces the declared encoding and refuses any
   DOCTYPE through an expat prescan *before* `ElementTree` parses (so no internal-entity expansion
   reaches the parser); `:199-224` dispatches on exact 0.9-namespace roots and counts entries;
   `:227-264` checks repeats and field values with skip rules; `:267-281` checks `loc` length,
   absoluteness and scheme/host/port/path scope. Unlike `CtlRegexTweak` (a token regex with no
   well-formedness gate), it rests on a real XML parser.
3. Independent reviewers agree with it beyond the thin key: 18/18 contract-decided witnesses, ~160
   contract probes, and on six live public sitemaps it equals the reference with findings a human can
   confirm (fsf.org http-vs-https).
4. Process integrity: frozen bytes unchanged, key-blind builder, copy guard clean.

Against (carried, not disqualifying): D2 UTF-16LE/BE without BOM reads `clean` (`:180-183` then the
re-sniff at `:193`), D1 XML 1.x accepted, D4 interior tab/newline in `loc` accepted (`urlsplit`
strips them), D5 duplicate id of an invalid check unflagged, D3 doctype-vs-malformed precedence
ambiguous. The real-run oracle is the L1's private reference, the same reading of the same contract,
so it confirms consistency, not independent truth. The tool is better than nothing and the defects
are named and bounded; that is "better", not "proven".

## Harm (no axis harmed)

- `git diff 2909f1dc f841a48d -- SCORECARD.md` → 207 insertions, 0 deletions; no axis score line
  changed; new capability row "Offline sitemap file audit (round 39, exploratory)" (`SCORECARD.md:199`,
  "pending closure").
- `git diff --numstat 2909f1dc f841a48d -- SKILL.md PROVINCE.md corpus/QUALITY.md corpus/README.md LOG.md`
  → 0 deletions in each; `git diff --diff-filter=DR --name-status 2909f1dc f841a48d` → empty.
- Robots tool sha256 `f4d057c4…` identical at base and tip; receipts `verification/harm/robots-selftest-
  {before,after}.txt` 194/194 → 204/204 (selftest +10 fixtures). source_recheck: diff read — fault
  branches now give one uncounted `check_invalid`, non-fault path untouched; receipts 106/106 →
  106/106, hardening 9/9 → 10/10.

Per-axis verdicts: operability **unprovable-but-better** (C1); freshness unchanged (S102–S104
re-opened, sha equal, no score move); depth, coverage, calibration, adjacency unchanged.

## Discernment spot-check

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` at 08:09:08Z →
exit 0, 6 W04 (S033, S088, S092, S098, S099, S102 duplicate URLs across scopes), `kake ok`. Rows
`grep -c '^| S[0-9]' corpus/SOURCES.md`: 101 at `2909f1dc` → 109 at `f841a48d`.

| Item | Decision | Re-opened source | Agree | Reason |
|---|---|---|---|---|
| S108 sitemaps.org FAQ (row + Gate quote) | admit, A, docs | `curl -sSL https://www.sitemaps.org/faq.html` → 200, 15,681 B (08:09Z, integrator) | agree | quote "Sitemaps should be no larger than 50MB (52,428,800 bytes) and can contain a maximum of 50,000 URLs." found verbatim in tag-stripped text; 17 words ≤25; grounds the limits in `teaches` |
| S105 XML 1.0 (row + Gate quote) | admit, A, spec | `curl https://www.w3.org/TR/xml/` → 200, sha256 = retained `xml-1.0.html` (seat) | agree | §2.3 S quote verbatim, 17 words; grounds the strip set |
| S107 XSD 1.1 Part 2 | admit, A, spec | `curl https://www.w3.org/TR/xmlschema11-2/` → 200, sha256 = retained (seat) | agree, caveat | quote present (11 words, markup spacing before the comma); `teaches` mis-attributes `24:00:00`/seconds to `xsd:date`, already corrected in the lesson only |
| S106 clause "'ignored' in sentence 14 comes from S102" | reject as wrong | live `https://www.sitemaps.org/protocol.html` (200, 45,292 B) and `https://www.w3.org/TR/xml-names/` (200): no `ignor` anywhere (integrator) | agree | S102's "Extending the Sitemaps protocol" only permits another namespace; S106's quote "The comparison is case-sensitive, and no %-escaping is done or undone." is verbatim (9 words) |
| Draft criterion-(o) checker | reject for adoption | `w2a3/MutCriterionO.md` adversarial table; `criteria/draft-o/check_control_inventory.py` | agree | 5 of the 7 adversarial SCORECARDs falsely accepted (code_only, after_declaration, no_summary_revision, comment_only, quoted_policy); the lesson's "5 of 15" denominator is loose |
| Sealed counter as C1's admission instrument | reject | receipts `verification/a3/w1a3-*.json` | agree | 16 controls meet the predicate (tally above) |

## Trend verdicts

- **expansion: unprovable-but-better.** A frontier area (sitemap files) entered with a capability
  admitted through this exploratory verdict and eight A-tier rows (S102–S109); no new
  `corpus/knowledge/` entry, so the LEARNING "improved" observable is not met.
- **quality: unprovable-but-better.** S102–S104 re-verified (sha equal), S102 supersedes S012's scope,
  robots selftest 194 → 204 and source_recheck g36 fixed red-then-green; but three rows admitted this
  round (S106, S107, S109) failed part of their wave-2 re-check and are marked only in the lesson, so
  "no admitted entry failing its re-check" does not hold. Not harmed: the errors are marked.
- **discernment: improved.** The spot-check agrees with the gate on every sampled admit and reject,
  and QUALITY gains (o) and (p), each grounded in lesson round-39 Mistakes with a check shown red.

## Report defects (status-neutral)

1. The "surface unmoved" command in the report says `grep -c sitemap_audit` gives 1 at `565ef4c9`;
   observed 2 (the selftest matches too). Use `grep -cx scripts/sitemap_audit.py`.
2. The report says seven critic seats returned source or diffs; six did (CtlValuesOnly and
   CtlHandTokenizer wrote files; CtlStructureOnly was refused).
3. The lesson's "5 false accepts in 15 adversarial samples" should read 5 of 7 adversarial samples.

## Routed defects (the lane must fix next round)

1. SOURCES append-only correction form (CORPUS.md §SOURCES rule 2): append superseding rows
   (`supersedes S106 —`, `S107`, `S109`) carrying the wave-2 corrections; S106's row still states
   the refuted "ignored … comes from S102".
2. Build deviations: fix D2 (UTF-16 without BOM → `encoding_invalid`/`xml_malformed`), D1, D4 and D5
   with red-then-green selftest fixtures; record D3 as a contract reading.
3. Append a SCORECARD correction marking the round-39 capability row admitted as
   `unprovable-but-better` with this file as the reviewer pointer (the row still says "pending closure").
4. Any later countable sitemap claim must first pass QUALITY (o): non-author mutant families and a
   tweaked shortcut scored below target before the declaration freezes the key.
5. Carried items stay open: (j) survivor M06, `MutRecheckOversize` boundary survivors, round-38 routed
   defect 6 items 2–10.

SHONEN: all four boxes `[~]` with pointers a non-author can check (SKILL "Sitemap file audit — round
39", LOG "Round 39" bullet 3, the selftest, PROVINCE boundary line); promotion is operator-owned.
