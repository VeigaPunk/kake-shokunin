# Kake round 60 — contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, the round-59 non-author spot-check):
`97cdc122379711c2b02a8970752c8782da3ac81d`. Round opened 2026-10-27 00:56 -03:00 (attempt 1, L1 `KakeR60`); the three source
fetches ran 2026-10-27T04:03Z, so the **access date** of every new row, Gate line, `verified-at:` and correction tag is
`2026-10-27` (UTC). This file and `contract.json` are committed before any wave seat is dispatched and before any counter scores
anything. The predicate sentence of each claim below is the sentence the counter's code carries (`PREDICATE`) and every receipt
label repeats.

Round shape: two v1 waves — `w1` build (counters, tool, entries, rows, recon, first falsifiers; 32–64 seats) and `w2` falsify (fresh
reviewer/critic/mutation-tester/scout/sentinel seats on what w1 produced; 32–64), round total 64–128, plus at most one residual call
of <= 8 reviewer/critic seats. The counters are written by wave-1 seats to the conditions frozen here, integrated by the L1, frozen
as version 1 with their base controls **before any after-state is scored**; wave 2 attacks version 1; a version 2 may only tighten
(every loosening is named in § Counter versions) and is frozen before the after-state is measured. The L1 holds the canonical §3
planner seat (the validator rejects `planner`). Seats are read-only except their own report and `<Seat>.files/` directory.

Receipt rule (round 58, kept): a receipt under `.ufo/waves/round-60/controls/` is committed once, after the run it records, and never
rewritten; a re-run lands under a new name. No placeholder receipt is committed.

## Routed defects of the round-59 spot-check (`corpus/lessons/round-59-verifier-spotcheck.md` §6)

- **R59-D1** (c55 byte-prefix rule vs append-only in-file corrections) → claim **C2** (a lane tool whose append-only rule accepts a
  tagged in-file correction and still catches rewrites/deletions) and claim **C1** (a live-labelled gate that a round turns red is a
  counted mismatch until relabelled with its pin).
- **R59-D2** (C1 counter never checks the calibration score) → claim **C1** term `scores_held == 3`: all three axis-table scores,
  calibration included, must equal the base values (10, 10, 2) — this round declares no score change; shown able to fail by a
  selftest mutant that moves only the calibration score.
- **R59-D3** (C2 P6 printed-tally trust, fixture-sniff composite, C3 footer `Last updated`) → C3 footer read fixed forward in
  `c60_quote_truth.py` (the `Last updated` text must sit inside `<devsite-content-footer`); P6 / fixture-sniff / Q1–Q8 carried (one
  operability claim per round; this round's is R59-D1), recorded as carried in the lesson.
- **R59-D4** (S425 `scope` overstates robots.txt posture for user-triggered fetchers) → claim **C3**: superseding row S427 (same URL,
  `teaches` opens `supersedes S425 —`) and row S428, the user-triggered fetchers page that does state that posture.
- **R59-D5** (dead seats, no planner seat) → status-neutral; dead seats are recorded from `w*-results.json`, never re-spawned.

## Axis declaration

Prompt-declared lane axes: operability + freshness; the scorecard also carries the round-54 bounded sub-axis **calibration**
(score 2, lowest non-retired), so the lowest-axis obligation lands on C1 (ownership still open for the operator, L0 row of round 59).
Three claims on three distinct axes: C1 calibration, C2 operability, C3 freshness (sourced). No exploratory claim.

Causal separability: C1 reads `SKILL.md` registry rows, `SCORECARD.md` rows 15–19 and runs the 28 population counters (it does not
include any round-60 counter, so C2/C3 landing or failing changes no C1 member); C2 reads only `scripts/append_guard.py` at the
revision and gate-built fixture repos plus the real lane history `fd6303ce..rev`; C3 reads only its entries, the correction file,
rows S427–S429, the lesson Gate and the round-60 sources/receipts. C3's appended rows may turn a population counter red; C1 then
requires that counter's honest relabel — C1 is judged on whichever tree is measured.

## Claim C1 — calibration: the gate registry's status labels match observed verdicts (population: round 48–59 counters)

Surface: `SKILL.md` gate-registry rows — the lane's self-assessment of which frozen round counters are live and which are historical.
Population: every committed path at the measured revision matching `^\.ufo/waves/round-(N)/(?:[a-z0-9-]+/)?c(N)_[a-z0-9_]+\.py$`
with the same N twice and 48 <= N <= 59 — 28 files at base (c48 ×2, c49 ×2, c50 ×2, c51 ×2, c52 ×4, c53 ×1 under
`exec-quality-gate/`, c54 ×2, c55 ×2, c56 ×2, c57 ×3, c58 ×3, c59 ×3). Rounds 40–47 counters are outside the population (not claimed).

Per member m:
- **row**: a rendered Markdown table row of `SKILL.md` (not inside fenced/indented code or an HTML comment) in a table whose header's
  first three cells are `Name`, `Kind`, `Entry command`, whose `Entry command` cell contains m's path. 0 rows → `unregistered`;
  more than 1 → `duplicate_row`. The row needs 8 non-empty cells and a `Verdict map` cell containing `0=` and `1=` → else
  `row_incomplete`.
- **label**: `historical` if the `Kind` cell contains the word `historical`; `never-met` if it contains `never met`; else `live`.
  `historical` and `never-met` need a 40-hex revision in the `Kind` cell (the first one is the pin) → else `unpinned`; the pin must
  be an ancestor of the measured revision → else `pin_not_ancestor`.
- **command**: the first backtick span of the `Entry command` cell that contains m's path. Placeholders `<commit>`, `<rev>`,
  `<revision>`, `<tip>` → the revision under test; `<scratch>` → a fresh scratch dir; `<fleet root>` → `/home/vgpnk/Projects/shokunin`;
  a `[...]` segment is kept (brackets removed) when every `<...>` inside it is one of those placeholders, else dropped; leading
  `NAME=value` words are environment assignments. Not shlex-parsable, or not running m with `python3` → `command_unparsable`.
- **observation**: the command runs with cwd = a fresh `git clone --shared` of the lane detached at the measured revision (`--root .`
  is that clone), inherited `GIT_*` scrubbed, `TMPDIR` = scratch, timeout 1800 s (timeout → exit 124). Exit at the measured revision
  = `e_T`; for `historical` / `never-met` members the same command also runs with the pin substituted = `e_P`.
- **mismatch** when: `live` and `e_T != 0` (`live_not_green`); `historical` and `e_T == 0` (`historical_but_green`); `historical` and
  `e_P != 0` (`historical_not_green_at_pin`); `never-met` and (`e_T == 0` or `e_P == 0`) (`never_met_but_green`); plus every
  structural class above. The counter's own file is not a member.
- **scores_held**: the `SCORECARD.md` axis table (`| Axis | Score | Evidence pointer | Last change |`) rows operability, freshness,
  calibration have scores 10, 10, 2 (the base values; this round declares no score change).

Counter: `python3 -B .ufo/waves/round-60/c60_gate_status.py --root <lane> --revision <rev> [--work <scratch>] [--jobs N] [--json]`.
- Predicate (frozen): **met: members == 28 AND mismatches == 0 AND scores_held == 3**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable (revision unresolved, SKILL.md/SCORECARD.md unreadable, clone failure); 64 usage.
- Before (L1 probe at base, 2026-10-27, to be re-derived by the version-1 counter as a committed receipt): 12 members unregistered
  (c48 ×2, c49 ×2, c50 ×2, c51 ×2, c52_gate_registry, c52_mutation_ladder, c54 ×2); `c53_gate_truth.py` labelled live, exit 1;
  `c57_idresolver_gate.py` labelled live, exit 2 without `--fleet`.
- Do-nothing control: base (>= 13 mismatches). Junk rows (path only, empty cells) fail `row_incomplete`; labelling green counters
  historical fails `historical_but_green`; a fake pin fails `historical_not_green_at_pin` / `pin_not_ancestor`; a calibration score
  moved 2 → 10 fails `scores_held`.
- What the counter does not test: whether a row's verdict-map text is true beyond `0=`/`1=`; whether a pin is the round's own
  measured revision (reviewer-checked); counters outside rounds 48–59.

## Claim C2 — operability: an append-only correction guard for knowledge files (`scripts/append_guard.py`, new)

Surface: a new lane tool, `scripts/append_guard.py` — read-only, stdlib Python, committed bytes only (`git cat-file`/`git ls-tree`,
never the worktree; inherited `GIT_*` scrubbed; `--root` must be a repository toplevel).
CLI: `python3 -B scripts/append_guard.py --root <lane> --base <rev> --revision <rev> [--scope <glob> ...] [--json]` and `--selftest`.
Default scope: `corpus/knowledge/**/*.md` (recursive). Exits: 0 clean, 1 findings, 2 could-not-evaluate (revision unresolved, base
not an ancestor of revision, root not a toplevel), 64 usage. One finding per line, `<kind> <path>[:<line>]`, then a summary line
`files=<n> findings=<k>`.
Rule, for every path P in scope that is a regular blob at base:
- P missing at revision, or not a regular blob there (symlink, submodule, tree) → `deleted P`.
- B = base lines, R = revision lines, split on `\n` as bytes (no decoding, no normalisation). If B is not an ordered subsequence of R
  → `changed P`.
- Otherwise, inserted lines (R positions not matched) form maximal runs. A run after the last matched base line is an end-of-file
  append (allowed). Every other run must begin with a line holding a **visible correction tag** — the regex
  `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` matched outside an HTML comment and outside a backtick code span. P gets
  `untagged_insertion P:<line>` iff **no** alignment of B into R exists in which every non-EOF run begins with a tagged line.
- Paths new at revision are not checked; paths outside scope are not checked.

Counter: `python3 -B .ufo/waves/round-60/c60_guard_cases.py --root <lane> --revision <rev> [--work <scratch>] [--seed N]` — runs the
tool **as committed at the revision** over gate-built fixture repos (each `git init` in its own scratch dir, ids drawn from the
seed) and over the real lane. 24 cases; a case passes only on the expected exit **and** the expected finding kind + path on stdout:

| id | fixture change (base → revision) | expected |
|---|---|---|
| K1 | lines appended at EOF | 0 |
| K2 | a 3-line run inserted mid-file whose first line carries `**[r60-correction 2026-10-27]**` | 0 |
| K3 | an untagged 2-line run inserted mid-file | 1 `untagged_insertion` |
| K4 | one byte of a base line changed | 1 `changed` |
| K5 | a base line deleted | 1 `changed` |
| K6 | the file deleted | 1 `deleted` |
| K7 | the file renamed | 1 `deleted` (old path) |
| K8 | a 2-line run mid-file, tag on its second line | 1 `untagged_insertion` |
| K9 | run's first line is `<!-- [r60-correction 2026-10-27] -->` | 1 `untagged_insertion` |
| K10 | run's first line holds the tag only inside a backtick code span | 1 `untagged_insertion` |
| K11 | a new knowledge file added | 0 |
| K12 | two base lines swapped | 1 `changed` |
| K13 | trailing space added to a base line | 1 `changed` |
| K14 | file converted to CRLF | 1 `changed` |
| K15 | base `a,"",b` → revision `a,TAG,"","",b` (an alignment with the run `TAG,""` exists) | 0 |
| K16 | base `a,b,c` → revision `a,b,b,c` (untagged duplicate mid-file) | 1 `untagged_insertion` |
| K17 | an out-of-scope file (`SKILL.md`) rewritten, knowledge untouched | 0 |
| K18 | a knowledge file replaced by a symlink | 1 `deleted` |
| K19 | bytes `\xff\xfe` appended at EOF | 0 |
| K20 | `--base` not an ancestor of `--revision` | 2 |
| K21 | `--base` missing | 64 |
| K22 | a file under `corpus/knowledge/sub/` rewritten | 1 `changed` |
| R1 | real lane: `--base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision <rev>` (holds the round-59 tagged in-file correction that `c55_readme_index.py` reads as `head_changed`) | 0 |
| R2 | real lane clone at `<rev>` + one byte of a base line of `corpus/knowledge/crawler-identity.md` changed, committed in the scratch clone | 1 `changed corpus/knowledge/crawler-identity.md` |

- Predicate (frozen): **met: cases_passed == 24 of 24**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base (no tool) → 0/24. Counter selftest controls (before data): no tool, always-exit-0, always-exit-1, the
  c55 byte-prefix rule port (must fail K2, K15, R1), a reference implementation (24/24).
- What the counter does not test: whether a tagged run is a *faithful* correction (reviewer-checked); files outside the scope.

## Claim C3 — freshness (sourced): the S425 scope overstatement corrected on rows opened this round, and the robots.txt posture of user-triggered fetchers re-verified

Surface: registry row S425's `scope` cell claims "the three crawler categories and their robots.txt posture"; the overview page (re-opened
2026-10-27 as S427, retained `sources/S427.html`) states a robots.txt posture for common crawlers ("They always respect robots.txt rules
for automatic crawls.") and special-case crawlers (the AdsBot example) only. The lane's `corpus/knowledge/googlebot-verification.md`
quotes S426 (`Last updated 2026-03-20 UTC`): "these fetchers ignore robots.txt rules"; the user-triggered fetchers page (S428,
`Last updated 2026-08-19 UTC`) reads "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules."
- Rows (all opened 2026-10-27, retained bodies + `sources/receipts.json`):
  - **S427** = re-open of the S425 URL; `teaches` opens `supersedes S425 —`; corrected scope; `used-by` = `corpus/lessons/round-60.md`.
  - **S428** = `https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers` (lane-found: linked
    from the S426 page's category table); `used-by` = `corpus/knowledge/google-user-triggered-fetchers.md`,
    `corpus/knowledge/googlebot-verification.md`.
  - **S429** = `https://developers.google.com/search/docs/crawling-indexing/robots/intro` (staged S415 of `merge/kake/`, renumbered
    by document); `used-by` = `corpus/knowledge/robots-txt-limits.md`.
- Entries: `corpus/knowledge/google-user-triggered-fetchers.md` (S428), `corpus/knowledge/robots-txt-limits.md` (S429; staged
  `google-robots-txt-limits.md` re-grounded, staged name not carried); an append-only `[r60-correction 2026-10-27]` run in
  `corpus/knowledge/googlebot-verification.md` after its S426 user-triggered quote, citing S428.
- Counter: `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root <lane> --revision <rev> [--json]`, generated by
  `derive_c60_quote_truth.py` from `.ufo/waves/round-59/c59_quote_truth.py` (version 2). Conditions:
  - C1 both entries exist at their paths; the staged name `corpus/knowledge/google-robots-txt-limits.md` does not.
  - C2 each entry opens with `source:` / `verified-at:` / `recheck:` in its first 8 lines; `source:` names its row id and URL; the id
    is cited again below the header.
  - C3 rows S427, S428, S429 well formed (11 cells, no pipe inside a cell, status `mined`, opened 2026-10-27, recheck normalised), each
    carrying its page URL, all three absent from the base registry; S427 `teaches` opens `supersedes S425 —`; S427 `scope` does not
    contain `their robots.txt posture` and does contain `common crawlers` and `special-case crawlers`.
  - C4 used-by exactly as listed above.
  - C5 quote truth (round-59 rules): the lesson `## Gate` line per id carries URL, access date, body sha256 and byte count and >= 1
    double-quoted span of 6..25 units, <= 160 characters, a substring of one whitespace-collapsed text node of the retained body's
    article block (`class="devsite-article-body` .. `<devsite-content-footer`), page-unique; every double-quoted span of 2+ units in
    each entry obeys the same rules against its row's body; each entry carries >= 3 distinct page-unique spans, one carrying the
    row's subject (S428 `generally ignore`, S429 `cannot enforce`; S427's Gate quote carries `automatic crawls`); the body carries
    the row's `<title>` text before ` | `, the anchor heading (an `<h2>`/`<h3>` of the article block) and the printed revision
    `Last updated <date> UTC` **inside `<devsite-content-footer`** (R59-D3 fix); body sha256 equals the frozen digest.
  - C6 receipts pin each body (sha256, bytes, HTTP 200, fetchedAt on 2026-10-27 UTC, userAgent tagged `round60`); receipt URL =
    row URL.
  - C7 the append block was census-validated before the append (round-60 paths, `validate_append.sh`).
  - C8 the pre-append mirror equals the base registry (164 rows, pinned sha256), its add-commit is a strict ancestor of the measured
    revision, and the measured registry minus the three new rows reproduces the mirror bytes.
  - C9 append-only correction: `corpus/knowledge/googlebot-verification.md` differs from base by inserted lines only; the base line
    holding `these fetchers ignore robots.txt rules.` is still present; an inserted line within the 6 base lines after it carries
    `[r60-correction 2026-10-27]`, cites S428 and holds a double-quoted span passing C5 against S428 that carries `generally ignore`.
- Predicate (frozen): **met: conditions_passed == 9 of 9**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base → 0/9.
- What the counter does not test: whether entry prose is faithful beyond quote truth (reviewer/critic-checked).

## Frontier step and assimilation (inside the claim cap)

Census at round start: exit 0, 164 rows, 14 W04 (`controls/census-before.txt`, `.exit`). Collision check (0–3-space pattern, guard
proven on a scratch `  | S002 |` registry → `S002`): reg 164, staged 129, collisions 8 (S312 S329 S367 S372 S373 S374 S390 S409); staged
S415 does not collide; renumber map by document S415 → S429. Quarantine slice: 12 rows, byte-identical to round 59; held (the
round-58 L0 question is unanswered) — nothing from it is appended. Assimilation theme: `robots.txt posture and limits per Google
crawler category` (`merge/kake/`): admit candidate `google-robots-txt-limits.md` (S415 → S429), screen-reject candidate
`common-crawlers-japanese.md` (staged S337, Japanese edition). Considerthese: `considerthese/2026-10-26.md` proposal 5 (historical-gate
list) — carried by C1. Mistakes to mine (each to be shown able to fail): R59-D1 gate collision (C2 R1 under the c55 rule port), R59-D2
counter-scope gap (C1 `scores_held` mutant), R59-D4 row precision (C3 condition C3 on the S425 scope cell).

## Amendments before any data (counters not yet frozen; no seat has scored)

- **A1 (2026-10-27, during w1; raised by `w1/EntryUserTriggered`):** C3 condition C5's "anchor heading (an `<h2>`/`<h3>` of the
  article block)" becomes "the nearest article-block `<h1>`, `<h2>` or `<h3>` that precedes the row's Gate quote, and the row's
  anchor cell names it". S428's robots sentence sits in the page intro under the article `<h1>` "List of Google user-triggered
  fetchers" with no `<h2>` before it; the old rule would force an anchor on an unrelated per-fetcher `<h2>` (understating the row's
  scope, the R59-D4 class). The amendment admits `<h1>` (a loosening) and binds the heading to the quote's position (a tightening).
- **A2 (C1, disambiguation; `w1/ExecC1Registered`, `w1/CriticD1Collision`):** a `[...]` segment of an Entry command is kept (brackets
  removed) only if it holds >= 1 placeholder and every placeholder in it is `<scratch>` or `<fleet root>`; a segment with a revision
  placeholder (`[--base <rev>]`) or with no placeholder (`[--seed N]`, `[--json]`) is dropped. The original rule kept `[--base <rev>]`
  and substituted the revision under test — a self-comparison the round-59 counters reject — and kept `[--seed N]` verbatim (exit 64).
- **A3 (C1, tightening; `w1/CriticC1Cheat` T1/T2, `w1/CriticAxisLabels`):** after env words the command must be exactly
  `python3 -B <member path> <args...>`; the only env word allowed is `TMPDIR=<scratch>`; args contain `--revision` followed by a
  revision placeholder, never `--selftest`, and `--root` (if present) is `.`; a shell-metacharacter token → `command_unparsable`.
  The command runs without a shell (`sys.executable`), env exactly `{PATH=/usr/bin:/bin, HOME, TMPDIR = scratch, LANG=C.UTF-8}`.
- **A4 (C1, tightening; T3):** the 28 member paths and their base blob ids are frozen in the counter; at the measured revision each
  must be the same regular blob (`member_missing` / `member_changed`), and a population-regex file outside the frozen set is
  `extra_member`. `members` counts frozen paths present unchanged.
- **A5 (C1, tightening; T4):** `historical` needs `e_T == 1` and `e_P == 0`; `never-met` needs `e_T == 1`, `e_P == 1`, a strict-ancestor
  pin at which the member file exists; a Kind cell holding both labels → `label_invalid`; label words are ASCII words.
- **A6 (C1, tightening; T7):** the member path in any other rendered table row anywhere in `SKILL.md` → `duplicate_row`; cells split
  honouring `\|`; exactly 8 non-empty cells.
- **A7 (C1, tightening; T8):** `SKILL.md` / `SCORECARD.md` read through git at the revision only; exactly one axis table; exactly one
  row per axis; the score cell, `**` and backticks stripped, equals 10 / 10 / 2 digit-exact.
- **A8 (C2, tightening; `w1/CriticC2Semantics` CR8):** a case passes only on an exact finding set — a finding case needs exactly one
  finding line with the expected kind and path and exactly one summary line with `findings=1`; a clean case needs no finding line
  and exactly one summary line with `findings=0`. The counter selftest gains an always-clean constant control (prints
  `files=1 findings=0`, scores 7/24); always-exit-0 with no output now scores 0/24.
- **A9 (C3, tightenings; `w1/CriticC3Conditions` T1–T8):** S427's scope also must not match
  `/robots\.txt[^.]{0,60}(user-triggered|three|all|every|each)/i`; C9's tagged line itself carries the tag, the S428 citation, the
  base wording `ignore robots.txt rules` and the `generally ignore` span; all inserted lines in `googlebot-verification.md` form one
  run starting at a block boundary within 6 base lines after the stale line; fenced code and HTML comments are stripped before every
  tag/citation/quote search; `verified-at:` equals the access date; the receipt's `effectiveUrl` equals the row URL and
  `sources/receipts.json` is pinned to blob `b9b56713713523ed9bec1c769313fd9cb0d52e6d`; the validate receipt's add-commit is a strict
  ancestor of the first commit holding an S427–S429 row; `Last updated` is read between `<devsite-content-footer` and its close tag
  with `<template>`/`<script>`/`<style>` stripped.

No predicate sentence changed: C1 `met: members == 28 AND mismatches == 0 AND scores_held == 3`, C2 `met: cases_passed == 24 of 24`,
C3 `met: conditions_passed == 9 of 9`.

## Stated limits carried from wave 1 (not fixed by version 1)

- C1: whether a historical pin is the round's own measured revision (`w1/CriticC1Cheat` T5 not adopted: `c57_receipt_pins.py` is red at
  its round's measured revision `32754df7` and green only from `20217f23`, so pin = measured revision would make an honest label
  impossible); whether a verdict map's text is true beyond `0=`/`1=`; `c57_idresolver_gate.py` reads live sibling registries
  (`--fleet`), so its live label is not hermetic; rounds 40–47 counters (17 files, `w1/CriticC1Population`) are outside the population.
- C2: existential alignment can park an untagged line inside a tag-led run when the inserted lines duplicate base lines
  (`w1/CriticC2Semantics` CR1) and, with a base older than an existing tag, a new untagged line next to that tag rides in its run
  (`w1/RevengerC55Intent` P5; a rolling base — the previous round's tip — closes it); a tag inside a fenced block, link title or heading
  counts as visible (CR2); the regex is the strict `[rNN-correction YYYY-MM-DD]` form, so the older `[r20-correction DATE: …]` and
  `[r23-correction]` spellings do not qualify (CR3, `w1/ScoutTagForms`); an empty base blob reads `x` (no newline) as `changed` (CR4);
  the default scope skips the three machine-written `.json` files under `corpus/knowledge/` (CR5, P6); the guard does not reproduce
  c55's frozen round-55 window (P7).
- C3: quote truth, not semantic support (reviewer-checked).

Amendment A3a (C1, before freeze; `w1/ExecC1Data52`): `c52_mutation_ladder.py` reads its own checkout and exits 2 on any argument, so
A3's `--revision` requirement cannot hold for it; the counter freezes it as the one `SELF_CHECKOUT` member, whose documented command
must be exactly `python3 -B <path>` (no arguments) — the clone it runs in is detached at the revision under test. Every other member
keeps A3. Collision disclosed before data (`w1/ExecC1Data53`): `c54_ops_debt.py`'s registry check requires the c53 row's Kind cell to
read literally `gate`, so the honest `never met` relabel of c53 turns c54_ops_debt red; it is then relabelled historical at its
round-54 measured revision `a631cc0246b97f2a949d61186c7466468faf94d6`.

## Counter versions — version 2 (after wave 2, before the after-state is measured)

Wave 2 (38 attack seats, `w2/`) attacked build B1 `8b33fd24` and the version-1 counters. Version 1 stays committed at `1ea30590`; the
claims are judged on version 2. No predicate sentence changed; both changes tighten.

- **C1** (`c60_gate_status.py` v2): text inside an inline HTML comment is no longer a rendered table cell (`w2/ReviewerC1Counter`
  high: a row whose Entry command existed only inside `<!-- … -->` registered a member). Selftest 76/76 (`controls/c1-selftest-v2.txt`).
  Not adopted, stated limits: no process-group containment, timeout reported through the label classes, `--work` prefix cleanup,
  exception → exit 1, no sandbox for member argv values (`w2/SentinelC1Exec`); a non-CommonMark fence closer `` ```python `` ends a
  fence (`w2/ReviewerC1Counter` medium; a false red, not a false green).
- **C2** (`c60_guard_cases.py` v2): eight cases carry extra sub-fixtures and pass only if all pass (K3, K8, K9, K10, K17, K18, K20; K22
  uses a non-ASCII file name) — from `w2/MutGuardTool` (16/33 mutants survived v1), `w2/SentinelGuard` (git-quoted paths silently out
  of scope) and `w2/ReviewerGuardCode` (code spans across line ends; unequal closers). Selftest: 6 controls, reference 24/24, c55 port
  7/24 (`controls/c2-selftest-v2.txt`). The B1 tool scores 22/24 under v2 (K10, K22 fail; `controls/c2-b1-tool-under-v2.txt`), so
  the tool was fixed in the build (NUL-delimited `ls-tree`, paragraph-level code spans, zero-coverage scope → exit 2, validated root,
  unchanged blobs skipped; tool selftest 38 → 51).
- **C3** (`c60_quote_truth.py`): unchanged (version 1). `w2/MutC3Counter`'s two survivors are killed by the selftest.
