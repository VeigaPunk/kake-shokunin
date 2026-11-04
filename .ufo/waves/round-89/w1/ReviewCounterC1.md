# ReviewCounterC1 — adversarial review of the round-89 C1 counter

Seat: ReviewCounterC1 (leaf reviewer, no subagents). Target:
`.ufo/waves/round-89/c89_defect_queue.py`, sha256
`0ebea07f5f4db358566ea4562ca39737ba7bf327601b66dcef3c760cd7f6d803` (byte-identical to the
lane file; `receipts/sha256-inputs.txt`). Base tool `scripts/vary_match.py` at `76225160`,
sha256 `fdceef47…` (`receipts/tool-base-scripts-vary_match.py`). Lane tip read:
`2e700b9a94a3c8ce3c0d6b1cc9e84e7b17eee683`.

Receipts: `ReviewCounterC1/receipts/` (38 files, each opens with the exact command, the
exit code and the full stdout). Drivers: `ReviewCounterC1/drivers/`. Scratch
(`/fast/scratch/hyaku/kake-r89/ReviewCounterC1/`) is deleted before this yield; every
citation below is the copied receipt.

## Method and limits (read first)

- Lane access was read-only: `git show`, `log`, `ls-tree`, `cat-file`, `archive`, one
  `git clone` of the lane into scratch, and one `git status --porcelain` (read; I did not
  write anything in the lane).
- Experiments ran in two scratch repos, never the lane:
  - `g-git`: a green baseline built with the counter's own `green_tree()` writer (tool bytes
    from the frozen base), then one branch per attack. Each attack is a real commit, and the
    counter runs with `--root <g-git> --revision <branch>`. The baseline is therefore the
    counter's own notion of "closed", not an independent ground truth.
  - `e-git`: a separate repo for item E, because E reads history from the checked-out HEAD
    (see RC-1).
  - one clone of the lane, used only to reproduce the base control.
- No tools were installed or updated. No network access. No production file was touched.
- "Expected" is my reading of the frozen claim text in `freeze.md` and the docstring. Where
  the claim itself is ambiguous I say so, and I route it as a claim decision.

## Verdict per item

| Item | Broken? | Witness (receipt) |
|---|---|---|
| A selftest number | **yes**: 3 false green (tag exemption, scope, self-report) | A1, A2, A3, A4 |
| B gate sample | **yes**: false red and false green from a substring parse | B1, B2 |
| C receipt pointers | **yes**: 9 distinct false green/red routes, including 16 of 21 named receipts never checked at the lane tip | C1–C6, BR1–BR4, `short-form-audit-tip.txt` |
| D revision-pinned count | **no** for the recount itself; one design gap (pin may name an older revision) | `D-pin-old-extra-control.txt` (low, RC-15) |
| E freeze-before-dispatch | **yes**: reads HEAD, not `--revision`; post-dispatch edit passes; same-second false red | E-bad-order-rev-HEAD-good, E-root-rev-HEAD-good, E-good-order-rev-HEAD-bad, E-post-dispatch-edit-of-frozen-counter, E-realtime-correct-order, E-real-rebase-keeps-order |
| F lesson shape | **yes**: substring header match, tagged pointer does not point | F1, F2, F3 |
| (mirror mode, not a claim item) | **yes**: E is silently skipped | `mirror-mode-no-freeze.txt` |
| (do-nothing control) | **yes**: the base receipt reproduces only with HEAD at base | `base-revision-HEAD-at-base.txt`, `base-revision-HEAD-at-tip.txt` |

**Could not break:** E's ancestor-but-later-time check (`E-ancestor-but-later-time.txt`
prints the correct red); E's ordering when HEAD equals the measured revision
(`E-good-order-HEAD-good.txt` green, `E-bad-order-HEAD-bad.txt` red, both correct); D's
recount arithmetic (no mismatch went green at the pinned revision; D1 control red). I did
not probe duplicate-marker inputs (two `integrated-selftest:` lines, two `controls-count:`
lines) for A, B, C, D, so those are untested rather than proven safe.

## Experiments (every row is a receipt in `receipts/`)

Counter exit and open items are from the receipt. "Verdict" is against the frozen claim.

| Receipt | Attack | Counter | Verdict |
|---|---|---|---|
| A1-tagged-stale-stands | L88 line `22/22 [r89-correction: stands]` while tool prints 35/35 | exit 0, A closed | **false green** |
| A2-untagged-stale-round89-scorecard | untagged `22/22` in SCORECARD round-89 section | exit 0, A closed | **false green** |
| A3-untagged-stale-round89-lesson | untagged `22/22` in corpus/lessons/round-89.md | exit 0, A closed | **false green** |
| A4-selftest-self-report-99 | tool replaced by `print('selftest: 99/99 passed')`, markers updated to 99/99 | exit 0, A closed | **false green** (A trusts self-report) |
| B1-honest-reject-mentions-admit | four = `**reject** (not **admit**)`, markers truthful 2/2 | exit 1, B open | **false red** |
| B2-parser-matched-markers-false-counts | same row, markers set to parser output 3/1 | exit 0, B closed | **false green** |
| C1-trailing-char-truncates-receipt | names `base-c1.txt+missing` | exit 0, C closed | **false green** |
| C2-unbacked-claim-left-in-force | claim "A re-run at edcb2980 reproduces the round-88 selftest." left in L88, marker `retracted` | exit 0, C closed | **false green** |
| C3-rerun-receipt-is-existing-lesson | `r88-c-rerun: receipt=corpus/lessons/round-88.md` | exit 0, C closed | **false green** |
| C4-rerun-receipt-is-directory-git | `r88-c-rerun: receipt=.ufo/waves/round-88/controls/` (git mode) | exit 0, C closed | **false green** |
| C5-false-red-plus-in-real-receipt | real file `after+c1.txt`, named exactly | exit 1, C open | **false red** |
| C6-short-form-receipt-missing | SCORECARD names `controls/integrated-selftest.txt` (missing) | exit 0, C closed | **false green** |
| BR1-empty-brace-alt | `controls/{base-c1.txt,}` | exit 0, C closed | **false green** (empty alt → directory → passes) |
| BR2-brace-missing-alt-control | `controls/{base-c1.txt,nope.txt}` | exit 1, C open | correct red |
| BR3-trailing-dot-trim-to-other-name | `controls/base-c1.txt.` (file with dot absent) | exit 0, C closed | **false green** (rstrip yields base-c1.txt) |
| BR4-comma-prose-list-false-red | `controls/base-c1.txt,after-c1-carrier.txt` (both exist) | exit 1, C open | **false red** |
| D1-sanity-wrong-count | marker 9 vs recount 5 | exit 1, D open | correct red |
| D-pin-old-extra-control | extra file added after the pinned revision | exit 0, D closed | design gap (pin names older revision; low) |
| F1-header-substring-fix-in-prefix | header `Prefix` in place of `Fix` | exit 0, F closed | **false green** |
| F2-honest-captured-by-space | header `Captured by` | exit 1, F open | **false red** |
| F3-tagged-pointer-not-pointing | tagged line says "nothing moved" | exit 0, F closed | **false green** |
| E-good-order-HEAD-good | HEAD = rev, correct order | E closed | correct green |
| E-bad-order-HEAD-bad | HEAD = rev, reversed | E open (both sub-checks) | correct red |
| E-bad-order-rev-HEAD-good | rev = reversed commit, HEAD = correct commit | **E closed** | **false green** |
| E-good-order-rev-HEAD-bad | rev = correct commit, HEAD = reversed commit | **E open** | **false red** |
| E-root-rev-HEAD-good | rev = commit with no freeze, HEAD = correct commit | **E closed** | **false green** |
| E-ancestor-but-later-time | freeze ancestor, committer time later | E open | correct red |
| E-realtime-correct-order | back-to-back real commits, same second, correct order | E open | **false red** (second-granularity strict `<`) |
| E-real-rebase-keeps-order | `git rebase -f` onto root keeps order, same second | E open | **false red** (same cause) |
| E-post-dispatch-edit-of-frozen-counter | frozen c89_key.py edited after dispatch | **E closed** | **false green** |
| mirror-mode-no-freeze | `--mirror` on a tree with no freeze and no dispatch | E `[]` | **false green** for E |
| base-revision-HEAD-at-base | `--revision 76225160`, HEAD at base | open=6 closed=0 met=false, exit 1 | matches frozen control |
| base-revision-HEAD-at-tip | `--revision 76225160`, HEAD at 2e700b9a | **open=5 closed=1** met=false, exit 1 | **control not reproduced** |

Exact command shape for every receipt: `python3 -B <counter> --root <repo> --revision <rev> --work <dir>`
(E runs add a HEAD checkout, recorded in the receipt header as `HEAD=<sha8>`). The C/F/A/B
rows use `counters/c89_defect_queue.py` (sha256 above).

## Lane-tip finding for C (not a counter bug alone)

`short-form-audit-tip.txt` (script `drivers/short_form_audit.py`, run against
`2e700b9a`): 21 unique `controls/` receipt names in the round-88 section of SCORECARD.md and
the round-88 lesson. The counter's regex only matches the full `.ufo/waves/round-88/controls/`
prefix, so it checks 5 of them and never looks at the other 16. One of the 16 does not
resolve at all: `controls/integrated-selftest.txt` (SCORECARD.md:5469; the file on disk is
`integrated-selftests.txt`). At the lane tip the counter's C item would be green for that
broken pointer once the round-89 lesson exists. This is an L1 production fix, not mine.

## Routed defects (each with witness and proposed fix)

Severities are my judgement. "Claim decision" means the frozen claim text, not the counter's
code, has to change, so L1 decides.

**RC-1 (high) — E reads HEAD history, not `--revision`.** `item_e` calls `git log` and
`merge-base` against the checked-out HEAD (`c89_defect_queue.py` lines 246–258; the
`--revision` value is never passed). Witnesses: `E-bad-order-rev-HEAD-good` (E closed on a
reversed-order revision), `E-root-rev-HEAD-good` (E closed on a revision with no freeze),
`E-good-order-rev-HEAD-bad` (E open on a correct revision), `base-revision-HEAD-at-tip`
(base control prints open=5 instead of open=6; only `base-revision-HEAD-at-base` reproduces
the receipt). Fix: pass the resolved `rev` to every E git call
(`git log --format=%H --diff-filter=A <rev> -- <path>`, `merge-base --is-ancestor` on the
SHAs, committer times from the SHAs). Add a selftest mutant with HEAD ≠ rev. Re-record
`controls/base-c1.txt` after the fix, at both HEAD states.

**RC-2 (high) — E does not check the frozen counter's bytes after dispatch.** E only checks
which commit first adds `c89_key.py`. Witness `E-post-dispatch-edit-of-frozen-counter`
(edit after `w1.ready`, E closed). This is the same class as round 88's "freeze amended while
the wave was live" (round-88 L1 mistakes). Fix: require `rev:FREEZE_PATH` blob equal to
`freeze:FREEZE_PATH` blob, and no commit in `dispatch..rev` touching `FREEZE_PATH`. This adds a
requirement to the frozen E claim, so it is a **claim decision for L1**.

**RC-3 (med) — E's time clause is strict at second granularity.** Correctly ordered commits
in the same second are red: `E-realtime-correct-order` and `E-real-rebase-keeps-order`
(both `committer time … is not earlier than …` with equal timestamps). A rebase that keeps
order can therefore turn E red. Fix options (all **claim decisions**): drop the time clause
and rely on ancestry (already decisive for "earlier"); or state `<=` with ancestry as the
decider. Do not change the code until the claim wording is decided.

**RC-4 (med) — mirror mode silently skips E.** `item_e` returns `[]` when `ctx.mirror` is set
(line 243). `mirror-mode-no-freeze.txt`: E is green on a tree with no freeze and no dispatch
commit at all. The counting command in the freeze does not use `--mirror`, so this is latent
for the carrier, but it is a false green the selftest does not cover. Fix: in mirror mode
return `['E-freeze-before-dispatch not evaluable in mirror mode']`, so the item stays open.

**RC-5 (high) — A's tag exemption accepts any line containing `[r89-correction`.** `item_a`
exempts a stale `22/22` whenever the line contains the substring `[r89-correction`, without
checking that the line states the observed count. Witness `A1-tagged-stale-stands`: L88 line
`22/22 [r89-correction: stands]` with the tool printing 35/35, A closed. Fix: a stale line is
admissible only if the same line contains the observed count string `observed` and the
stale string appears as superseded (e.g. preceded by `was`/`stale`). Add mutant
"tagged-but-wrong-count" to the selftest.

**RC-6 (high) — A's scope skips the round-89 SCORECARD section and the round-89 lesson.**
`item_a` scans only the `## Round 88` section of SCORECARD.md and the round-88 lesson (lines
115–130). Witnesses `A2-untagged-stale-round89-scorecard`, `A3-untagged-stale-round89-lesson`:
untagged `22/22` in both, A closed. Fix: scan every line of SCORECARD.md and every
`corpus/lessons/round-8*.md` / `round-89.md` with the same tag rule.

**RC-7 (high) — A trusts the tool's self-reported count.** `item_a` takes the `selftest: N/M
passed` line printed by the tool and compares it with the prose. A tool that prints
`selftest: 99/99 passed` and checks nothing closes A (`A4-selftest-self-report-99`). This is
the same self-attested-banner limit as round-88 R88-5. Fix: bind the count to tool bytes —
the selftest receipt must record `sha256(scripts/vary_match.py)` at the revision, and the
counter must verify that sha against `rev`. Full fix needs a claim decision on what counts
as the tool's checks; at minimum disclose it.

**RC-8 (high) — B classifies rows by substring, `**admit**` checked before `**reject**`.**
`item_b` lines 161–164 count a reject whose decision cell mentions `**admit**` as an admit
and read the decision from `cells[1]` by position. Witnesses: `B1-honest-reject-mentions-admit`
(truthful markers, counter red: false red); `B2-parser-matched-markers-false-counts` (markers
set to the mis-parse, counter green: false green). Fix: take the verdict as the first bold
token of the decision cell (`re.match(r'\s*\*\*(admit|reject)\*\*', decision)`), fail any row
with neither or with both, and locate the Decision column by header name rather than index.

**RC-9 (high) — C checks only full-prefix receipt names.** `CTRL_RE` requires
`.ufo/waves/round-88/controls/`. At the lane tip, 16 of 21 unique round-88 receipt names are
short-form and unchecked; `controls/integrated-selftest.txt` (SCORECARD.md:5469) does not
resolve (`short-form-audit-tip.txt`; C6 shows the same miss in a scratch repo). Fix: resolve
`controls/X` under `.ufo/waves/round-88/` as well as the full prefix, and scan the round-88
lesson and round-88 section of SCORECARD for both forms. Route the broken pointer to L1 as
a production fix (`integrated-selftest.txt` → `integrated-selftests.txt`, or the file).

**RC-10 (high) — C's `r88-c-rerun: receipt=` accepts any existing object.** `item_c` checks
`ctx.read(path) is not None`. Witnesses `C3-rerun-receipt-is-existing-lesson` (a lesson file
closes C) and `C4-rerun-receipt-is-directory-git` (in git mode `git show rev:<dir>/` returns a
tree listing, not None). Fix: require the path to be a blob (`git ls-tree` type `blob`) under
`.ufo/waves/round-88/controls/`.

**RC-11 (high) — C's "unbacked re-run claim" is never checked as text.** `item_c` reads only
the `r88-c-rerun` marker. Witness `C2-unbacked-claim-left-in-force`: the round-88 lesson still
says "A re-run at edcb2980 reproduces the round-88 selftest." untagged, marker `retracted`,
C closed. The claim the defect names is still in force. Fix: scan SCORECARD.md and the
round-88 lesson for the `edcb2980` re-run phrase; each occurrence must carry `[r89-correction`
or be absent. The phrase must be pinned as a regex in the counter.

**RC-12 (med) — C's regex and brace handling are fragile.** The class
`[A-Za-z0-9._/,{}-]` stops at `+`, `=`, `@`, `(`, space and more. Witnesses:
`C1-trailing-char-truncates-receipt` (named `base-c1.txt+missing`, truncated to `base-c1.txt`,
closed: false green); `C5-false-red-plus-in-real-receipt` (real `after+c1.txt` truncated to
`after`, red: false red). Brace: `BR1-empty-brace-alt` (`{base-c1.txt,}` expands to
`controls/`, a directory that passes in git mode). Trailing punctuation: `BR3-trailing-dot-trim-to-other-name`
(`base-c1.txt.` rstripped to the existing `base-c1.txt`, closed: false green). Comma prose list:
`BR4-comma-prose-list-false-red`. Fix: stop tokens only at whitespace, backtick, quote and
closing paren; strip sentence punctuation only after confirming the exact token does not
exist; refuse empty brace alternatives; require blob type (RC-10).

**RC-13 (med) — F's column check is substring.** `item_f` tests `'fix' in joined` and
`'captured-by' in joined`. Witnesses `F1-header-substring-fix-in-prefix` (`Prefix` satisfies
`fix`: false green) and `F2-honest-captured-by-space` (`Captured by` fails the literal:
false red). Fix: split header cells, normalise (lowercase, strip non-alphanumerics), require
exact equality with `class, evidence, capturedby, fix, witness`.

**RC-14 (med) — F's pointer check accepts any line with the tag and `L1 mistakes`.** Witness
`F3-tagged-pointer-not-pointing`: the tagged line says the mistakes "stay under `## L1
mistakes`; nothing moved", and F closes. Fix: the tagged line must name `## Mistakes` and
`corpus/lessons/round-89.md`, and `## Mistakes` must be a heading in round-89 (the check
already exists for the heading; the pointer must reference it).

**RC-15 (low) — D's pin may name an older revision.** `D-pin-old-extra-control`: the marker
pins to the freeze commit, a control file is added afterwards, D stays closed. The count is
true at the pinned commit and does not describe the measured carrier. This is the frozen
design (pinned count), so it is not a false green against the claim as written. Fix (claim
decision): require the pin to equal the measured revision, or to be an ancestor with no
`*/controls/*` change between pin and measured revision.

**RC-16 (med) — the selftest covers none of the defects above.** The 12/12 selftest passes on
the current counter and does not exercise HEAD ≠ rev for E, tagged-wrong-count for A, Gate
rows that mention the other verdict for B, short-form or brace receipts for C, or header
substrings for F. Fix: one mutant per RC item, each asserting the item reopens.

**RC-17 (med) — the do-nothing control claim is HEAD-dependent.** The freeze says "committing
nothing prints `open=6 closed=0 met=false`". `base-revision-HEAD-at-base` reproduces that only
with HEAD at the base commit. At the lane tip, `base-revision-HEAD-at-tip` prints `open=5
closed=1`. The control receipt `controls/base-c1.txt` is therefore not a property of the
revision it names. Fix follows RC-1; re-record the control after the fix. Route to L1.

## Notes for L1

- Nothing in this report edits the frozen claim or any production file. RC-2, RC-3 and RC-15
  change claim wording and need L1's decision before any counter edit.
- The C-item and A-item defects are live at the lane tip only once round-89 files exist. At
  the tip itself, C is red for `round-89 lesson missing` and would be green for the broken
  `controls/integrated-selftest.txt` pointer once that file is present.
- The green baseline in `g-git` is produced by the counter's own writer, so "green" there
  means "closed by the counter's own rules". It is not evidence of a closed lane.
- No tool installs or updates. Python 3.14.8 and git 2.56.0 were already present.

- Lane HEAD moved during this review: `2e700b9a` (audited tip, pinned in every receipt) → `2177058662d8778f1d1a685613f57deccb51ef01` at yield. I did not commit or move any ref; the new commit is not mine and I did not read it. All findings above are about `2e700b9a` and are reproducible from that commit alone.
