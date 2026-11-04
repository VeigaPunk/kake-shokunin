# Round 37 — offline robots.txt expectation audit on sealed cases

## Claims

Declared before any build in `SCORECARD.md` section "Round 37 — declared claims" (`202d625a`).
Base `621fb528ba9116b9f440b8332be6dfc0cad4e972` (round 36 admitted). Round 36 worked freshness on
`scripts/source_recheck.py`, so the round's claim moves to a new frontier surface: publisher-side
crawl rules (PROVINCE "Crawl hygiene per host").

- C1 (operability, capability): `scripts/robots_audit.py` reads a manifest of (robots status,
  local robots file, user agent, URL, expected allow/disallow) and reports where the robots rules
  disagree with the expectation (`blocked`, `exposed`), under RFC 9309 and the lane readings of the
  public contract (a)–(g). Frozen predicate `met: passed >= 25 of 28 sealed cases`. Before: 0 of
  28 at `621fb528`, `202d625a`, `4b089da6`, `ccc3b2b9` and `528a6d02` (tool absent). After: 28 of
  28 at the build commit `9dbc88bb` (`verification/c1-at-9dbc88bb.json` with the key file before
  the reveal; `verification/c1-keyrev-at-9dbc88bb.json` with `--key-revision 424aa248` after it).
  Measuring the reveal commit itself exits 2 (`c1-keyrev-at-424aa248….json`).
- The tool is wave-1 `ExecRobotsTool`'s file (sha256 `5eb767ec…cabae`), landed unedited. The
  seat never saw the cases; its report discloses one `test -e` of the sealed directory itself
  (existence only; nothing under it listed or read).
- C2 (declared at `202d625a`: the selftest fixture data kills the 32 round-36 mutants) was
  **withdrawn before any data**: a snapshot fixture set recorded from E1 on random inputs met its
  counter (32 of 32). Its fixture work continued as non-claim routed repair (below).

Pre-data history: declaration with counters, base receipts and 34 reference ablations
(`202d625a`); control call, receipts and C2 withdrawal (`4b089da6`); shortcut follow-up receipt
and disposition (`ccc3b2b9`); the build landed at `9dbc88bb` after all of them, and was measured
only after that. Neither counter, the key nor the predicate changed after the declaration.

## Gate

### Source openings

Opened with `.ufo/waves/round-37/fetch_sources.py` (one public GET each; receipts and retained
text in `.ufo/waves/round-37/sources/`) at 02:50:49Z–02:50:51Z, before the declaration. Each was
re-opened live by an independent wave-1 scout (`w1/ScoutReopenS011.md`, `S095`, `S096`, `S097`);
every retained visible text is byte-identical to the scout's live extraction. Quotes verified as
exact substrings of the retained text with `grep -cF` (1 match each).

- S011 — https://www.rfc-editor.org/rfc/rfc9309.html — accessed 2026-10-23T02:50:49Z, HTTP 200 —
  re-open of an existing row (admit, A, spec, mined): RFC 9309 grounds every rule of (a)–(e);
  quote “the crawler MUST assume complete disallow” (Section 2.3.1.4, "Unreachable" Status; 6
  words).
- S095 — https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt (301 to
  https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec) — accessed
  2026-10-23T02:50:49Z, HTTP 200 — admit, tier A, kind docs, status mined: Google's own reading
  of REP for its crawlers, cited where it agrees or differs from the lane readings; quote “The
  order of the groups within the robots.txt file is irrelevant.” (Order of precedence for user
  agents; 11 words).
- S096 — https://github.com/google/robotstxt — accessed 2026-10-23T02:50:50Z, HTTP 200 — admit,
  tier A, kind code, status mined: Google's released parser and matcher; settles how a production
  parser treats BOM, rule priority and normalization; quote “production code used by Googlebot”
  (README, About the library; 5 words).
- S097 — https://www.robotstxt.org/orig.html — accessed 2026-10-23T02:50:51Z, HTTP 200 — reject,
  tier C, kind community, status rejected: the 1994 consensus is superseded by S011 (no `Allow`,
  substring user-agent match, one `*` record); flip: RFC 9309 is withdrawn and this text becomes
  the operative specification; quote “It is not an official standard backed by a standards body”
  (Status of this document; 10 words).

Real reject with reason: S097 (superseded; contradicts the contract on seven points, wave-1
`ScoutReopenS097`). The scribe draft's first reject reason ("first-match semantics") was not in
the text and was replaced by the located one before the row landed.

Row changes logged old→new: S095, S096 `—` → `mined`, opened `2026-10-23`, recheck `90d`, used-by
`corpus/knowledge/robots-txt-rules.md`. S097 `—` → `rejected`, opened `2026-10-23`, recheck
`365d`, used-by `—`. S011 used-by `corpus/knowledge/crawl-scope-per-host.md` →
`corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/robots-txt-rules.md`; its status
(`mined`), opened (`2026-10-19`) and recheck (`365d`) are unchanged. S095 moved: the requested
Search Central URL now answers 301 to the crawling docs URL (row records the final URL).

Source-precision notes from the re-opens (carried as entry text or contract limits):
- S011 section 2.2.2 says octets "in the reserved range" MUST be percent-encoded before
  comparison; read literally, `%2F` and `/` compare equal. The contract follows Figure 4 instead
  (`ScoutReopenS011` D1); the knowledge entry now says so.
- The contract's "invalid bytes become U+FFFD" has no source: S011 is silent, S095 says Google may
  ignore such characters, S096 percent-escapes the raw byte (`ScoutContractVsGoogle` finding 2).
  No sealed case depends on it (MutRefPass M40 survives).
- S095 differs from the contract on 429 (Google treats it unlike other 4xx), on 5xx without a
  cached copy, on user-agent precedence (`googlebot/1.2` equals `googlebot`; specific and `*`
  groups never combine; the contract combines all `*` groups only when nothing matches, which
  agrees), and on path-only matching (`ScoutReopenS095`). The entry marks these as Google-only.
- S096 does not decode unreserved escapes, rewrites `/index.htm` allow rules, accepts misspelled
  keys and truncates user agents at the first invalid character (`ScoutReopenS096` K1–K7).

## Knowledge entry

`corpus/knowledge/robots-txt-rules.md`, drafted by wave-1 `ScribeKnowledgeEntry`, landed with two
L1 corrections: the RFC sentence on group selection (the draft said RFC 9309 requires "the most
specific matching group", which is S095's wording, not S011's) and the normalization paragraph
(reserved-range sentence vs Figure 4, S096 behavior). It cites S011, S095 and S096 per sentence
and marks every lane reading.

## Controls (all before any build was measured)

C1, frozen counter, passed of 28: base 0, constant clean 0, junk 0, no-reader 0, all-false 4,
stock `urllib.robotparser` 20, the L1 reference 28, 34 listed ablations 16–24. The shortcut
follow-up (stdlib parser plus six one-line patches, each a (b) or (e) rule) met 28; the
disposition recorded at `ccc3b2b9` before any build was measured: it does not skip the claimed
work, and the sealed cases do not separate the contract from the stdlib where they differ.
Mutation pass on the reference: 28 of 42 single-point mutants meet 25 (`ctl/MutRefPass.md`).

## Real-input run (evidence, not a claim)

Wave-1 `ExecLiveRobotsSnapshot` recorded the served `/robots.txt` of 12 hosts at
03:23:15Z–03:23:31Z (all HTTP 200; receipts `realrun/robots/receipts.json`) and wrote 55 checks
whose expectations each quote the robots line that justifies them. The landed tool:
`realrun/audit.json`, `clean`, 55 evaluated, exit 0. The stock-parser control gives the same
(`realrun/audit-stdlib-control.json`), so the live set does not separate them either; it shows
the tool runs on real files (BOM-led Wikipedia file, 165-record GitHub group, empty `Disallow:`),
not that it is more correct than the stdlib on them.

## Non-claim routed repairs

- Routed defect 3: five fixtures added to `scripts/source_recheck_selftest.py` (wave-1
  `ExecC2Fixtures`), each named for its contract sentence; the C2 counter, as evidence only,
  goes 27 → 32 of 32 (`verification/c2-at-621fb528.json` → `c2-evidence-at-528a6d02.json`; 106
  fixtures, all valid on E1 and E2). Wave-1 `RevengerSurvivors` independently found the same five
  distinguishing inputs and why each survived (no relative location on a second hop; `../` never
  in a Location; no comment holding `>`; no tag splitting a quote; no quote holding U+FEFF).
- Routed defect 8: `scripts/source_recheck.py` hardened (wave-1 `ExecRecheckHardening`, sha256
  `37a8a8ef…0e95`): a non-regular or over-64-MiB manifest gives `input_invalid`; `MemoryError`
  is caught; the body is opened at its resolved path; a raw-element start tag counts only where a
  tag can start. Contract (c) amendment sentence: "A raw-element start tag counts only where a tag
  can start, not inside another tag's attribute value." Six fixtures in the new
  `scripts/source_recheck_hardening_selftest.py`, red on `4d5b3d55`, green on the fix; the
  round-36 selftest 106/106 and the round-36 sealed counter 28 of 28 on the fixed tool (seat
  evidence). Carried: body reads are not size-capped; fixture g32 needs `strace`.
- Routed defect 7: `criteria/control_tree_check.py` v2, `polarity_check.py`, `bare_id_check.py`,
  each red and green (`criteria/receipts/`); QUALITY round-37 (e)–(g).
- Routed defects 1, 5, 6: "Round-36 routed corrections" below.
- Routed defect 2: every wave context named the seat's sandbox as its only deliverable path; the
  L1 checked `jj-lane.sh state` after each wave (below).

## Round-36 routed corrections (appended; drafted by wave-1 `ScribeR36Corrections`)

- (1) `bf9b2089` is not an object in lane history (`git cat-file -t bf9b2089` → exit 128). It is
  `bf9b20892d241a73648d04a37feea145a03efe77`, reachable only as `refs/heads/postfix` in
  `.ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle`; post-measurement, counts toward
  no claim. Read every round-36 citation of `bf9b2089` with that bundle path.
- (5) The round-36 junk control was **untested** (its seat ended on a provider policy filter);
  `SCORECARD.md` "Round 36 — wave-2 corrections" ("No do-nothing, junk, …") and
  `corpus/lessons/round-36.md` line 143 overstate it. Run this round: the junk tool scores 0 of 28
  under the round-36 counter with key `fd1fb723`, exit 1 (`verification/control-r36-junk.json`).
- (6) SOURCES notes (append-only; anchor and teaches cells are corrected by superseding rows only,
  CORPUS.md Rules 2, so the cells stay as landed): S091's quote is at Section 7 Design Goals item
  2, not Section 1.2; S093's rejected `teaches` lacks the `flip:` form — flip: a needed fact
  unavailable from any primary source is verified in the article; S094's reason should read
  "overbroad" (RFC 9110 15.4.5 does not require Location on 304; it does not forbid it), not
  "contradicts"; S088–S092 `used-by` names `scripts/source_recheck.py` where contract v1 asks for
  knowledge-entry or lesson paths — read them as `corpus/lessons/round-36.md`.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| an unrun control was reported with the measured controls as having failed the target | `corpus/lessons/round-36.md:143` and SCORECARD round-36 wave-2 corrections ("No do-nothing, junk, … control reached 25") while the junk seat produced no receipt (`round-36.md:105-109`); caught by the round-36 closure | none before the closure | `.ufo/waves/round-37/criteria/junk_control_receipt_check.py` (wave-1 `ScribeMistakeMine`): exit 1 at `1a16b8e3` ("no later correction says the round-36 junk control was untested"), exit 0 at `4b089da6` (correction backed by `control-r36-junk.json`, 0 of 28) |
| a fixture-set counter was declared before a recorded-oracle fixture set was scored against it | C2 at `202d625a`; `ctl/CtlC2FixtureSets.md` snapshot set 32 of 32, met | the pre-freeze control call (this round) | C2 withdrawn before data; QUALITY round-37 (h); red receipt `retained/controls/c2/c2-snapshot.json` (met true) |
| control seats' sandboxes sat beside the sealed key; key-blindness rested on instructions | `/fast/scratch/hyaku/kake-r37/ctl/*` next to `/fast/scratch/hyaku/kake-r37/private/` (wave-1 `ReviewRoutedDisposition` G2); every control report lists only its own tree, and `MutRefPass` was granted key access by design | none | QUALITY round-37 (i); wave-1 sandboxes moved to `/fast/scratch/hyaku/kake-r37w1/`. No check yet. |

## Holds and dead seats

- Control call: `CtlC1Shortcut` died at once on a provider quota error (HTTP 429
  `RESOURCE_EXHAUSTED`, route gemini-4-argon, "Individual quota reached … Resets in 59h"). Not
  replaced; the living `CtlC1NoReader` built the shortcut control as a disclosed follow-up.
- Wave 1: `CriticC1AxisFit`, `CriticDeclarationWording`, `CriticContractAmbiguity` and
  `CriticWithdrawal` died within 5 s on the same quota error. Not replaced; their attack topics
  are covered by wave-2 reviewer seats on the landed work.

## Carried open

- The sealed cases do not separate the contract from `urllib.robotparser` (substring user agent,
  non-final `$`, rule-length counting) nor from 28 single-point reference mutants (exact limit,
  trim set, `rfind('#')`, `splitlines`, casefold, `.+` for `*`, `re.search`, raw-length
  specificity, status edges, floats, symlink and sibling-prefix containment, 64 MiB edge,
  non-UTF-8 manifests, report version). 28 of 28 certifies the tested rules only.
- Counter limits (wave-1 `ReviewSealedCounter`, `SentinelCounterJail`): the jail's scratch is
  writable and shared across runs (a tool can keep state or rewrite its own file); files with the
  same base name would collide and subdirectories are not created (no sealed case has either; the
  two subdirectory-style robots paths, f2 and f3, expect `check_invalid` under every reading); a
  case with no runs would pass (none has); a tool crash of the counter exits 1, not 2. The C2
  counter takes REASONS from the selftest it counts and exits 1 on a missing mutant file
  (`ReviewC2Counter`, `MutC2Counter`: 2 of 13 counter mutants equivalent on tested inputs).
- The contract's U+FFFD sentence is unsourced; status 3xx is a check fault although S011 2.3.1.2
  describes following redirects.

## Wave-2 corrections (appended)

Wave 2 `kake-r37-w2` (34 seats, reports in `.ufo/waves/round-37/w2/`) attacked the landed work.
The declaration, counter, key and measured result stay as landed; SCORECARD "Round 37 — wave-2
corrections" lists the measured items.

- Reproduced byte for byte: C1 receipts at seven revisions, all controls, the independent
  implementation, the 34 ablations, the C2 evidence and the snapshot control, the junk receipt,
  the criteria receipts (with wave-1 fixtures, now committed under `criteria/fixtures/`).
- **Shortcut disposition contested** (`ReviewShortcutDisposition`, `ReviewTimeline`): the
  follow-up control delegates (c)/(d) to `urllib.robotparser`, which is wrong on 6 of 9 contract
  checks, and still met the predicate; the declared consequence ("fixed before any build") was
  replaced by a written judgment landed after the build seat was dispatched and before any
  measurement. C1: measured met, admission contested.
- Lesson text corrected: the S097 quote is 11 words, not 10; S095 says "most specific group" /
  "the group with the most specific user agent", not "most specific matching group" (the
  correction's point, that S011 does not say it, stands); "RFC 9309 grounds every rule of
  (a)–(e)" is overstated — the reserved-escape reading, the 3xx check fault and the U+FFFD rule
  are lane choices against or beyond S011; S096 "settles … normalization" is overstated — its
  README and code decline URL normalization; "every expectation quotes the line that justifies
  it" (real-input run) is overstated for 4 checks whose decision is "no rule matches"
  (`ReviewRealRun`), and check 33 is decided by Wikipedia's percent-encoded rule, not the raw
  `ö` line; "each of 28 cases has a holding and a failing check" fails for the (g) fault runs.
- The real-input set separates little: of 10 single-change mutants only one is caught by the 55
  checks; 8 extra checks on the same live files separate the tool from the stock parser on all 8
  and from the shortcut control on 2 (`ReviewRealRun`). Live files unchanged at 03:45Z, also
  under a Googlebot user agent (`ScoutRobotsRefetch`).
- Knowledge entry corrected after `ReviewKnowledgeEntry` and `ReopenGateS096`: Figure 4's
  reserved-character row, the `/robots.txt` lane-reading marker, the usage paragraph, the BOM as
  a Google-specific choice, "equivalent" not "equally specific", S095 cited for key case, code
  claims pinned to `22b355ff` and marked as not retained.
- Post-measurement repairs (no claim): linear wildcard matcher in `scripts/robots_audit.py`
  (backtracking hang, `SentinelRobotsInputs`, `ReviewRobotsTool`); quote opens only after `=` in
  `scripts/source_recheck.py` (`ReviewHardening` regressions R1–R7); three robots selftest
  fixtures (c12, c13, d17). The round-36 real-run S025 `quote_missing` was the attribute defect:
  the hardened tool drops it on both round-36 runs (`ReviewHardening`).
- Containment (`ReviewContainment`): no lane file outside reports, no landed fleet-root misroot;
  three attempted misroots by wave-1 scribes were refused by the edit tool. Eleven out-of-bounds
  actions, ten not recorded above: `/tmp` files by SimplifierCounters, ScoutPriorTools,
  ReviewC2Counter, ReviewRoutedDisposition, CtlC1NoReader and wave-2 ReviewSourcesRows,
  ReviewKnowledgeEntry, ReopenGateS097, ReviewLessonNumbers; six wave-1 seats replied to a stray
  broadcast from another lane's L1 (`MadoR24`, text "x") with status text only. L1 lane-state
  checks after each wave: wave 1 left only `w1/` reports untracked (`jj-lane.sh state`
  `untracked=1`, committed at `a5ae0280`); wave 2 likewise (`w2/`).
- Late results: `MutRefPassVsSelftest` — the selftest separates 41 of 42 reference mutants from the
  reference (M09 not); `DiffToolVsIndependent` — 8192 checks, 0 tool/independent disagreements;
  `MutSealedCounter` 13 of 14 counter mutants killed (1 equivalent); `ReviewRobotsSelftest` — all
  131 expectations follow the contract, write detection only sees new files in its temp tree.

### Mistakes (appended rows)

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| a control met the predicate and the L1 kept the claim by a written judgment instead of the declared consequence | SCORECARD `ccc3b2b9` section vs the declaration's "fixed before any build"; `w2/ReviewTimeline.md`, `w2/ReviewShortcutDisposition.md` | wave-2 review; none before | next declaration states, before any control runs, which control classes count as skipping work (any control that delegates a bullet's rules to a library counts as skipping that bullet unless the library is shown to implement the bullet on the selftest) and applies the consequence mechanically; QUALITY round-37 (j) |
| post-wave containment record named one out-of-bounds action of eleven | lesson "Claims" (one `test -e`); `w2/ReviewContainment.md` table | wave-2 review | the L1's per-wave containment line lists every seat-disclosed out-of-bounds action from the reports, and the wave context requires `/tmp`-free runs (TMPDIR in the sandbox) — already in the context, not followed; no check yet |
- Late: `MutRobotsTool` — 42 mutants of the landed tool, 23 meet the sealed target, 3 also pass
  the selftest (M04, M14, M15); fixtures b19, c14, c15 kill each (137/137 on the tool and the
  independent implementation; `verification/postfix/mutrobots-survivors/`). `RevengerToolReadings`
  — the tool's 12 open-point readings all hold; the L1 reference and the independent
  implementation crash on a lone-surrogate URL that the tool reports.
