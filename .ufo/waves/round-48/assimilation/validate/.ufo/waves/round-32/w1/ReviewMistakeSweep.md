# ReviewMistakeSweep — errata the lane has not yet mined (r32 w1)

Seat: KakeR32.ReviewMistakeSweep (leaf, reviewer). Axes: operability (lesson mining) and
freshness (the errata ledger reflects what wave reports actually say). No subagents, no
installs (pacman paused; none needed), no lane mutation except this file. Sandbox
/fast/scratch/hyaku/kake-r32/w1/ReviewMistakeSweep/ created but unused (read-only sweep).

## Scope and method

Targets: `corpus/lessons/round-3*.md` (round-3, round-30, round-30-verifier-spotcheck,
round-31, round-31-verifier-spotcheck, round-32) and `.ufo/waves/round-31/a2-w2/*.md`
(38 reports). Comparison set: every `## Mistakes` row in round-30.md, round-31.md,
round-32.md, plus the lane's other tracking surfaces (spotcheck "Routed defects",
round-31.md "Carried open (attempt 2)", QUALITY.md wave-2 corrections) so items are not
called unmined when they are tracked elsewhere.

Sweep greps (grep tool, all exit 0):

- `\b(HIGH|MEDIUM)\b` (case-insensitive) over round-3*.md → matches only round-30.md:76-80
  (the Mistakes table quoting round-29 findings: "finding 1, HIGH, process"). Mined.
- `\b(HIGH|MEDIUM)\b` over a2-w2/*.md → exactly 5 files: CriticQualityCriteria (F1-F4),
  ReviewCensusAfter (F1), ReviewHostileSelftestCode (F1 HIGH, F2 MEDIUM),
  ReviewPartialReportsList (MEDIUM), ReviewProvinceReadme (F1 HIGH, F2 MEDIUM).
- `not repaired|unrepaired|left open|uncarried|\bcritical\b` over both targets →
  round-30.md:77,79 (quoting round-29 "Open after wave 2 (not repaired)"; mined as the
  unattributed-evidence and vacuous rows), round-31-verifier-spotcheck.md:170 ("left
  unrepaired by the freeze"), CriticOpenItemsCarried.md:34 (the grep text of that seat).
  No CRITICAL marks anywhere.

## Unmined items (absent from every lesson ## Mistakes row)

U1. CriticQualityCriteria F2 (HIGH) and F3 (MEDIUM) — checks shipped in QUALITY that
    cannot fail (F2: closure-command step 1 is a git-diff tautology; step 2 passes for the
    round-30 directory command) or fail the round's own wave 1 (F3: five-status reality vs
    four statuses named; count equality hides swaps).
    `.ufo/waves/round-31/a2-w2/CriticQualityCriteria.md:55-70`.
    Patched in corpus/QUALITY.md:517-545 ("Round-31 wave-2 corrections", labeled F2, F3),
    but no Mistakes row in any lesson records "we declared criteria whose checks could not
    fail / failed our own data". F4 got a partial row anchor (round-31.md row 6 cites the
    criterion-4 extension); F2/F3 got none.

U2. CriticQualityCriteria F1 (medium) — the criterion-1 reviewer check does not test what
    the criterion asks (still exits 1 with 4 of 5 specs deleted; never runs the selftest
    against the claimed runner; no spec-count check).
    `.ufo/waves/round-31/a2-w2/CriticQualityCriteria.md:46-53`.
    The QUALITY corrections are "Grounded in ... (F2–F5)" (QUALITY.md:519) — F1 is the one
    finding the corrections skip. Unpatched and unmined; the per-name-class bullet
    (from CriticSymlinkCases) covers only part of it.

U3. ReviewProvinceReadme F1 (HIGH) — PROVINCE.md:118-119 "nothing live was fetched" false
    as written (the round's C2 ground was five live GETs, S057-S061); F2 (MEDIUM) —
    PROVINCE.md:121-122 parenthetical names the checker, not the runner holding the
    refusals. `.ufo/waves/round-31/a2-w2/ReviewProvinceReadme.md:28-47`.
    Repaired (PROVINCE.md "Round-31 wave-2 narrowing" paragraph citing F1/F2/F4; README.md
    clarifier at corpus/README.md:299-301), but no Mistakes row and no routed item records
    the overclaim. Repaired-but-unmined: the lesson carries no trace that PROVINCE stated
    a falsehood about the round's own evidence.

U4. ReviewCensusAfter F1 (medium) — `census-before.txt` and `census-after.txt` are
    byte-identical validate transcripts (sha256 6ba6b789…), insensitive to registry size,
    so they cannot witness the 56→61 change they are named after; no census-mode receipt
    exists anywhere under `.ufo/waves/round-31/`.
    `.ufo/waves/round-31/a2-w2/ReviewCensusAfter.md:49-60`.
    Absent from every Mistakes row, from routed defects, and from Carried open. round-31.md
    row 7 mentions census-after.txt only as attempt-1 debris (an untracked path), not the
    receipt-quality defect. Through round-32 the receipts stand as committed (the committed
    census-before.txt still carries sha 6ba6b789…), and `.ufo/waves/round-32/verification/`
    holds no census-mode receipt either. Unpatched and unmined.

U5. Round-31 routed defect 3, three of four sub-items — the only explicit "not repaired"
    marker in scope ("`ReviewRunnerDiff` LOW/INFO items left unrepaired by the freeze",
    round-31-verifier-spotcheck.md:170-172): `OSError` from `fstat`/`read` in
    `read_expected` escapes the handler; stray regular files, FIFOs and sockets at the
    fixture root are skipped silently; option tables hand-duplicate the gate parser.
    Still unrepaired at tip: confirmed by my read of scripts/citing_set_selftest.py:403-414
    (only `os.open` is in the try/except; fstat/read sit in try/finally) and by
    `.ufo/waves/round-32/w1/ReviewRoutedItemsStatus.md` item 3 ("OPEN (all four
    sub-items unrepaired)"). The fourth sub-item (symlink docstring wording) was repaired —
    scripts/citing_set_selftest.py:80-81 now says "never a silent skip" truthfully.
    Mining gap: none of the three open items is in a Mistakes row, and round-31.md
    "Carried open (attempt 2)" lists mutants m2/m4/m5, fifo-on-.gitattributes, gate-git
    timeouts and Git pins — but not these three. They survive only in the spotcheck routed
    list and a wave-1 report; the next round's lesson will not see them from the lessons.

U6. ReviewPartialReportsList MEDIUM — the round-30 partial-reports list's evidence pointers
    are dead (history://KakeR30:*, agent://KakeR30.* unresolvable) and the scout's
    independent corroboration `.ufo/reports/round-30/kake.md:64` was never committed, so
    the 15/5 classification rests on one author and one measurement pass.
    `.ufo/waves/round-31/a2-w2/ReviewPartialReportsList.md:57-66`.
    Partially tracked: routed defect 6 (round-31-verifier-spotcheck.md:175) captures the
    class and round 32 discharged it prospectively (no new history:// refs; ReviewRoutedItemsStatus
    item 6 ADDRESSED), but no Mistakes row records the round-30 list's decayed evidence.

U7. ReviewHostileSelftestCode F2 (MEDIUM) — a spec-valid case name with an embedded NUL
    crashed the selftest (uncaught ValueError from copytree, whole run lost).
    `.ufo/waves/round-31/a2-w2/ReviewHostileSelftestCode.md:29-31`.
    Repaired in code — scripts/citing_set_hostile_selftest.py:137-139 rejects "\0" in case
    names and :243-244 now catches ValueError — but no Mistakes row and no routed item
    records the defect or the repair; the repairing commit is not cited anywhere I could
    find (I did not bisect it). Same repaired-but-unmined shape as U3.

Adjacent, outside the severity filter (one line each, for the L1's discretion):
- ReviewHostileSelftestCode F3/F4 (LOW): a symlinked spec dir is silently skipped and
  `citing-set-hostile` itself may be a symlink out of `--root` — the same silent-skip shape
  the lane repaired at case level, unmined (a2-w2/ReviewHostileSelftestCode.md:33-40).
- Round-32 w1 `ReviewRunnerDocstringPins.md` findings 1-3 (stale/wrong runner docstring
  sentences after P6) are not yet in any Mistakes row — expected, the round is in flight.

## Mined, for contrast (the filter's negatives)

- ReviewHostileSelftestCode F1 (HIGH) → round-31.md Mistakes row "selftest trusts the
  reported names" + routed defect 1. Mined.
- Round-29 "Open after wave 2 (not repaired)" defects 3 and 5 (quoted at round-30.md:77,79)
  → round-30.md Mistakes rows unattributed-evidence and vacuous. Mined.
- NoHarmExistingGates HIGH process finding → round-30.md Mistakes row "boundary". Mined.
- CriticQualityCriteria F4 → patched in QUALITY.md:543-545 and partially anchored by
  round-31.md row 6's fix cell. Partially mined.

## Suggested smallest correction (for the closure to weigh)

One appended round-32 wave-2 Mistakes row (or a carried-open line) naming U1-U7 by report
and line, or a single "unmined wave findings" register row, would close the pattern: four
of the seven were repaired but leave no lesson trace, two are still open, one (U4) leaves
committed receipts that do not evidence what they are named after.

## Not verified

- I did not run the C1/C2 counters or any selftest; this is a text/ledger sweep.
- I did not pin the commit that added the NUL guard (U7) or the PROVINCE narrowing commit.
- I did not audit Mistakes-row accuracy (a2-w2/ReviewMistakesRows.md owns that) and did not
  check round-29 or earlier waves, other lanes, or `.ufo/waves/round-30/**/*.md`.
- grep is literal evidence only; I read each cited finding in full before classifying it.
