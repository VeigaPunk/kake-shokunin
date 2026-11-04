# Round 79 — lessons (kake, attempt 1)

Base `0898085450ee1b65d910f1dcb7a0efc20b413b88`; frozen contract `.ufo/waves/round-79/contract.md`
at the freeze commit `e1a9a897`; terms-only amendment 1 at `43e0a9b7` (A1 adds `noarchive` to the
directive vocabulary, A2 pins the `none`/`all`/`index`/`follow` normalization wording; written before
any tool existed and before any case was scored, and it changes no case, oracle byte or predicate).
One v1 wave, fourteen requested seats. Axes: calibration 2 (the lowest non-retired axis) and
operability 10, with freshness 10 held. Scores are held; a claim moves evidence, not a scalar.

## Claims

**C1 — calibration: the receipt-rewrite disclosure ledger is current and the gate is standing.** The
disclosure surface is `.ufo/waves/round-58/receipt-rewrites.json`; the measured surface is every path
ever committed under `.ufo/waves/round-<N>/control/` or `.../controls/` on the measured revision's
first-parent line. At the base the standing counter prints
`C1v2 revision=0898085450ee1b65d910f1dcb7a0efc20b413b88 events=32 undisclosed=5 phantom=0 malformed=0 wrong_kind=0 unpointed=0 symlinks=0 round_rewritten=0 met=false`
(`.ufo/waves/round-79/controls/base-c1-receipt-ledger.txt:1`, exit 1); the five undisclosed events,
with their commits and blob pairs, are listed at `controls/base-c1-events.txt:3-7`. Counter:
`python3 -B .ufo/waves/round-79/c79_receipt_ledger.py --root . --revision <rev>`. Frozen predicate:

    met <=> undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0
           AND unpointed == 0 AND symlinks == 0 AND round_rewritten == 0

It imports the frozen round-58 counter for the event walk, ledger parsing, byte-level `classify()` and
note-pointer semantics, and generalizes only the predicate: the round-58 `new_receipts == 2` file-count
conjunct is dropped, and its round-scoped `new_rewritten` becomes `round_rewritten` under `--round`
(default 79). A ledger entry is admitted only when path, commit, status and `fromBlob`/`toBlob` equal
the event, its `kind` equals the classifier's reading of that blob pair, and its note names a
repo-relative `Path` that resolves at the measured revision
(`c79_receipt_ledger.py` re-uses `c58_receipt_rewrites.pointed()`, which tests `git cat-file -e
<tip>:<path>`). The carrier's after receipt and revision are recorded in `SCORECARD.md`
`## Round 79`; the frozen round-58 counter is the contract's cross-check at the same revision, not the
claim's counter. I re-derived the five byte-level kinds independently with the frozen classifier —
`content`, `append`, `content`, `content`, `content` (`w1/ScribeRecord/five-kinds-independent.txt`) —
so a wrong `kind` in any entry is a real `wrong_kind` failure, not a naming preference.

**C2 — operability (capability): offline X-Robots-Tag declaration audit.** `scripts/x_robots_tag_audit.py`
reads a version-1 manifest of recorded response header fields plus URLs, read-only and network-free,
and decides for every check the declared normalized global directive set, the global effective
restriction set and the per-bot sets, with the closed seven-id finding vocabulary and the 0/1/2/64
exit alphabet of contract §"C2 tool interface (frozen)". Counter:
`python3 -B .ufo/waves/round-79/c79_xrt_matrix.py --root . --tool-revision <rev> --cases
.ufo/waves/round-79/cases --expect .ufo/waves/round-79/expect/expect.json --consts
.ufo/waves/round-79/consts --work <scratch>` (the same CLI takes `--tool <path>` for pre-commit runs).
Frozen predicate:

    met <=> decided == cases AND wrong == 0 AND constants_failed == 4/4 AND selftest_ok

Per case the counter compares the exit code, the report's global finding-id list, and every check's
`directives`, `effective` and `bots` sets; it copies each manifest to its `--work` tree before the run,
so the tool receives payloads and never the oracle, which sits outside the case directories. At the
base the tool path does not exist (`git cat-file -e` rc 128, `controls/base-c2-tool-absent.txt`) and
the matrix prints `TOOL_ABSENT rc=128` with exit 2 (`controls/base-c2-matrix.txt`). The frozen case set
covers all seven finding ids (c09/c10 `xrt_mutually_exclusive`, c11 `xrt_unknown_directive`, c12
`xrt_empty_rule`, c13/c14/c17 `xrt_invalid_value`, c18 `xrt_bot_scope_empty`, c20
`xrt_indexifembedded_without_noindex`, c21 `xrt_duplicate_directive`), four input faults (c22
duplicate id, c23 check shape, c24 bad JSON, c25 schema) and clean/bot-scope/date/value/case variants
(c01–c08, c15, c16, c19, c26–c31). The carrier's matrix receipt, tool digest and real-input run are
recorded in `SCORECARD.md` `## Round 79`.

## Gate

Admit **S452** — MDN, *X-Robots-Tag header*,
`https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag`, accessed
2026-11-04 (fetch receipt `fetched_at 2026-11-04T09:39:04Z`, HTTP 200, 218,816 bytes, raw sha256
`c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38`, retained at
`.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.raw`). Located quote, retained text
`.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt:156`:

> An optional `<bot-name>:` specifies the user agent that the subsequent rules should apply to

That sentence grounds the bot-scope shape only. The declaration role is grounded separately at the
same page, line 136: "The X-Robots-Tag response header defines how crawlers should index URLs."; the
page states its own standing at line 137 ("While not part of any specification, it is a de-facto
standard method…"), so S452 is tier B and is cross-checked against S449 (tier A) for the vocabulary,
as the contract requires.

Reject **RFC 9309 as a row for the header carrier.** Candidate
`https://www.rfc-editor.org/rfc/rfc9309.txt`, retained at
`.ufo/waves/round-79/sources/reject-rfc9309.raw` (25,265 bytes, sha256 `f633915d…9fb207`). The silence
sweep: `grep -ci 'x-robots-tag'` on the retained text prints `0` and exits 1 (no match), while the
context control `grep -ci 'robots'` on the same file prints `42` and exits 0 (measured 2026-11-04,
`w1/ScribeKnowledge/rfc9309-sweep.txt`). The document is already held as S099 (`corpus/SOURCES.md:107`,
robots.txt REP behaviour), so a second row would duplicate a held document on a carrier it never
mentions. Flip: an RFC or update that defines header-level `X-Robots-Tag` processing (then a scoped row
is owed). No S453 row was written.

Rows touched, old→new:

- **S452 added** at `corpus/SOURCES.md:199` (kind `docs`, tier `B`, status `mined`, opened 2026-11-04,
  recheck 90d, used-by `corpus/knowledge/x-robots-tag-header.md`); registry 189 → 190 rows. The row's
  Gate quote is the bot-scope sentence above; its anchor names the frozen retained raw, not a seat tree.
- **S449 `used-by` cell changed** at `corpus/SOURCES.md:196`: old `corpus/knowledge/meta-robots-directives.md`,
  new `corpus/knowledge/meta-robots-directives.md, corpus/knowledge/x-robots-tag-header.md`. The other
  ten cells are byte-equal (cell-by-cell re-check 2026-11-04).
- The census is unchanged in warnings: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  kake` exits 0 with 19 `W04` lines before and after (`controls/census-before.txt`,
  `w1/ScribeKnowledge/census-after.txt`).

Screened and **deferred, not written**: a second row on S449's Google URL with a header scope. It is
mechanically admissible (census `E04` keys on the `(url, scope)` pair, so a different scope cell is a
`W04` warning; the scout measured `W04` 19 → 20 and no `E04` on a scratch copy) and it is the only
page that states the case rule, the multi-field combination sentence and the global default in clean
form — but the frozen contract admits S452 only. The drafted row is retained at
`w1/ScoutSources/row-deferred-google-xrt.txt` for a later round or for none.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| receipt-rewrite left undisclosed (mined; five instances) | `.ufo/waves/round-79/controls/base-c1-receipt-ledger.txt:1` (`undisclosed=5`, exit 1); the five events at `controls/base-c1-events.txt:3-7` — round 75 `controls/after-harm-battery.txt` at `3ae076ab3e01` and `0df52aed0b68`; round 78 `controls/base-c2-sweep.txt` at `c758904c15c2`, `controls/after-c1-population.txt` and `controls/after-c3-matrix.txt` at `406021c765fd` | the round-58 ledger gate existed but was not run at the round-78 carrier: re-running the frozen counter at the round-78 settle prints `C1 receipt-rewrites events=32 undisclosed=5 … met=False` with `EXIT=1` (`.ufo/waves/round-79/w1/ScribeRecord/c58-counter-at-r78-settle.txt`), and the round-78 non-author closure traced only the one event it had already followed (its R1, `after-c1-population.txt`). Nothing in the lane's process bound the check to a round that was not round 58 | C1: five entries with true blobs and byte-level kinds in the round-58 ledger, and a standing round-agnostic counter (`c79_receipt_ledger.py`) plus a `corpus/QUALITY.md` criterion and its one-green/four-red fixture control |
| freeze receipts print the exit line twice (fresh, cosmetic) | `controls/base-c1-receipt-ledger.txt:2-3`, `controls/base-c2-matrix.txt:2-3`, `controls/ctl-c2-constants.txt:6-7` each carry `exit=` twice; both counters already print it (`c79_receipt_ledger.py` summary, `c79_xrt_matrix.py` main) and the freeze-time wrapper appended a second copy | this seat's whole-line quoting discipline (round-76 criterion) | quote the whole line and count the exit once; no predicate reads the line. Reported, not edited — the receipts are frozen |
| contract control names do not resolve (fresh) | contract §C1 Controls names `controls/ctl-c1-fabricated.txt`, `ctl-c1-drop-one.txt` and `ctl-c1-cheap-note.txt`; the freeze shipped one combined `controls/ctl-c1-fixtures.txt` holding `## fabricated`, `## drop-one`, `## cheap-note` and `## round-rewrite` blocks beside the green variant | this seat's control inventory | reported, not amended: all five variants exist and are receipted, and a re-cut would itself be a rewrite of a frozen control |
| frozen-premise: the contract says the RFC 822/850 date branches are "pinned by cases" (fresh) | the frozen case set holds exactly two `unavailable_after` values — c16 `2025-12-31T23:59:59Z` (ISO) and c17 `tomorrow` (invalid); `grep -c 'GMT' expect/expect.json` prints `0` and no case carries a weekday-shaped value (measured 2026-11-04; `w1/ScoutSources.md` §10 D1) | the scout's source/grammar read, routed before the tool existed | reported, not amended: `correct=31` says nothing about the RFC 822 or RFC 850 branches; a later case set or a narrower claim |
| spec-tool mismatch: the grammar splits every field value on `,` first, so comma-bearing RFC 822/850 dates are unreachable | S452's own example `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (retained text line 239) yields `findings: ["xrt_invalid_value", "xrt_unknown_directive"]` with exit 1 (reproduced read-only 2026-11-04, `w1/ScribeRecord/f1-comma-date-repro.txt`; ReviewC2 F1, `w1/ReviewC2/`) | the frozen case set had no comma-bearing date case, so neither the oracle nor `correct=31` could see the conflict | next round: an amendment plus cases, never a post-data grammar change; the frozen tool, cases and receipts stay untouched |

## Corrections

1. **Round-78 closure R1 — the C1 receipt re-cut is disclosed.** The closure traced
   `after-c1-population.txt` (`020d8890c8f6` → `3e8b5b2efe85`, `kind=content`) and named the silent
   ledger. C1 discloses that event and the four the closure did not find, with the true blob pairs and
   the byte-level kinds, and appends `[r79-correction 2026-11-04]` rows to `corpus/lessons/round-75.md`
   (events at `3ae076ab3e01`, `0df52aed0b68`; section at line 154, rows 162-163) and
   `corpus/lessons/round-78.md` (`c758904c15c2`, `406021c765fd` ×2; section at line 95, rows 103-105).
   Each ledger note names the lesson path that records it, so the
   note is checkable at the revision rather than a claim about intent.
2. **Round-78 closure R2 — the landed-blob selftest receipt is closed.** The round-78 receipts bound the
   freeze blob `c2dc1cbf…`; on the landed counter bytes the selftest prints `selftest: 9/9 passed` with
   `exit=0`, and the receipt records the measured digest `c78_counter_sha256=c09651e43d7a3ffaa636f7683ad4bcb5b76deaf772ea1c1c9c3b0406dde43a3f`
   and `12238` bytes (`.ufo/waves/round-79/w1/ExecR2R3/c78-selftest-landed.txt`, landed in carrier
   `436f4429`).
3. **Round-78 closure R3 — plumbing and wording, closed.** The hard-coded `/fast/scratch/hyaku/kake-r78/l1`
   default (`.ufo/waves/round-78/c78_shonen_population.py:81` before the fix) is replaced at carrier
   `436f4429` by `tempfile.TemporaryDirectory(prefix="kake-c78-c77-")`, so the counter honours `TMPDIR`
   and the round-79 scratch discipline; the post-edit selftest is the R2 receipt above. The SCORECARD
   correction row below puts the `HOLD` token in the round-78 C1 cell text (append-only correction, not
   a rewrite), and the round-79 receipts carry an explicit `exit=` line.
4. **Coverage-map mis-attribution (ConnectorC defect).** `corpus/README.md:558-559` and
   `PROVINCE.md:580-581` attributed the `X-Robots-Tag` channel to `response_snapshot.py` /
   `header_audit.py`, and `corpus/knowledge/meta-robots-directives.md:123` said "Header instruments own
   it" — but `header_audit.py` audits only transport/security classes (content-type, HSTS, XCTO, CSP,
   singleton fields, field-name syntax) and parses no robots directive, and `response_snapshot.py` is a
   capture, not an audit. Evidence: `w1/ConnectorC.md` §"Coverage-map correction", re-checked read-only
   this seat (`grep -n -i robots scripts/header_audit.py` → no hit). The fix is append-only: a new
   `## Coverage — round 79 (2026-11-04)` section at `corpus/README.md:577`, a
   `[r79-correction 2026-11-04]` paragraph at `PROVINCE.md:592`, and one appended line at
   `corpus/knowledge/meta-robots-directives.md:140`; the three historical sentences stay verbatim and
   are named by the corrections.
5. **R4 (note, operator-owned) — unchanged.** The four `SHONEN.md` boxes keep their evidence pointers;
   box 2 stays an honest gap; promotion review is the operator's, never this lane's.

## Limits

- **The real-input run is a negative population.** The twelve recorded round-61 captures (2026-10-27,
  207 field lines) contain **0** `x-robots-tag` fields (independently re-read 2026-11-04; the scout's
  inventory in `w1/ScoutRealInput.md` §2 agrees). A clean audit over them proves manifest acceptance and
  empty-set rendering, never a positive grammar path on publisher ground; four of the twelve are 404
  records, and the manifest schema has no status field.
- **The grammar is a de-facto reading, not a specification.** S452 says the header is "not part of any
  specification" (retained text line 137; the page restates it at line 258). Directive-name precedence
  over a bot prefix, field-local scope, the bot-name charset, unknown-name handling, mutual exclusion
  as a *finding*, duplicate value directives, the deletion of `max-*` from `effective` under
  `nosnippet`, and the bot-name case rule each rest on a lane reading or on S449 sentences outside
  S452's scope (`w1/ScoutSources.md` §5 R1–R13). Marked `[INFERENCE]` in the knowledge entry.
- **Date branches: the grammar is ISO-only in practice.** `unavailable_after` names three shapes, but
  grammar rule 1 splits every field value on ASCII `,` before any directive is parsed, and every RFC 822
  and RFC 850 shape contains a comma (`Wed, 03 Dec …`, `Wednesday, 03-Dec-25 …`). Those branches are
  therefore **unreachable**: S452's own example `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT`
  (retained text line 239) yields `xrt_invalid_value` + `xrt_unknown_directive` and exit 1
  (reproduced read-only 2026-11-04, `w1/ScribeRecord/f1-comma-date-repro.txt`), and so does S449's
  `… 15:00:00 PST` example. `correct=31` exercises only an ISO date-time (c16) and an invalid value
  (c17); no case carries a comma-bearing date, so the matrix says nothing about the RFC branches. This
  is a stated limit of the frozen grammar, not a claim that the branches work. The round-78 meta
  instrument rejects RFC 850 outright — a lane-policy difference between two instruments, not a source
  difference.
- **Per-bot and cross-carrier work is out of scope.** `effective` is global-only; per-bot effective
  resolution, meta+header conflicts, and header inheritance across redirect hops are not decided. S452
  does describe a per-bot merge ("the search engine will use the sum of the negative rules"), so the
  exclusion is a stated lane limit, not source silence.
- **`xrt_input_unreadable` is unexercised** by the frozen cases: the four fault cases cover duplicate
  id, check shape, bad JSON and schema only.
- **The finite 31-case set is public.** The oracle sits outside the case directories and the counter
  copies each manifest to scratch, but that isolates labels, not semantics: fixture-fitting cannot be
  excluded by a green matrix.
- **C1's surface is the first-parent line of the measured revision.** A receipt re-added on a merge
  side line is outside the population, and the byte-level `kind` cannot say whether a run happened — a
  re-run that reproduces its result changes only the revision pin (`pin-only`). `round_rewritten`
  guards only the measured `--round` (79); the ledger has no chronological introduction cutoff (the
  connector named kama's rule), so a later correction entry could absorb a future round's rewrite
  without a bound. Report-only: the predicate is frozen.
- **The ledger is a disclosure, not a proof of intent.** An entry with true blobs, the right kind and a
  resolvable note can still describe a rewrite whose *reason* is only in the note's prose; the counter
  checks the pointer resolves, not that the prose is complete.

## Post-attack settlement (appended 2026-11-04)

The wave's attacks changed C2's measured bytes before the report, and the record is corrected here rather
than by rewriting an earlier line.

- **C2 carrier moved.** The first carrier `436f4429` measured tool `f06c47b5…` (18,053 B) with the matrix
  `met=true` (`controls/after-c2-matrix.txt`). SentinelC's F1–F6 and ReviewC2's F1 then exposed defects
  outside the frozen cases: an uncaught `ValueError` on integer caps beyond CPython's 4,300-digit limit
  (F1), an uncaught `RecursionError` on deeply nested JSON (F2), an unbounded read on `/dev/zero` and a
  FIFO open (F3), a duplicate-directive scan that missed `max-image-preview` and `unavailable_after`
  against contract §6 (F4), unescaped control characters in text-mode check ids (F5), and argparse usage
  errors exiting 2 instead of 64 (F6). The tool was repaired for all six, its selftest went 24 → 26, and
  the final carrier is `9cfa404dbed4dc7f0dca3784b01d33792fe684f0` with tool `dd83c2c8…` (19,680 B),
  matrix receipt `controls/after-c2-matrix-final.txt` (`correct=31 wrong=0 constants_failed=4/4
  met=true`), real-run receipt `controls/after-c2-realrun-final.txt` (`checks=12 findings=0`), C1
  receipts `controls/after-c1-receipt-ledger-final.txt` and `controls/after-c1-r58-crosscheck-final.txt`,
  and SHONEN population `controls/after-shonen-population-final.txt`. The frozen predicate, case set and
  oracle did not change; the earlier receipts stay as history. `[r79-correction 2026-11-04]`
- **Routed, not fixed.** The comma split precedes directive parsing, so RFC 822/850 `unavailable_after`
  values are unreachable (ReviewC2 F1; S452's own example is rejected) — a grammar change needs an
  amendment plus cases next round. MutC's counter survivors k3/k4/k5 (zeroing `wrong_kind`, `malformed`
  or `symlinks`) are killed only by isolated probes, not by the fixture battery; the QUALITY criterion
  states that limit. The freeze receipts print `exit=` twice (a shell echo plus the counter line) and the
  contract's three named C1 control files ship as one combined receipt.
- **Seats.** 14 seats settled; `ExecC2Tool` and `CriticC` returned empty output, and `ExecC1Ledger`,
  `ExecR2R3` and `ReviewC1` stopped after their first read with no deliverable, so the L1 completed the
  tool, the five ledger entries and lesson rows, the R2/R3 repairs and the C1 attacks itself; the
  independent C1 attack evidence is SentinelC's reproduction (base red, fixture verdicts, selftest), not
  a separate reviewer seat.
