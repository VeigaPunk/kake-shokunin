# Round 80 — lesson draft (ScribeRecord seat, prose only)

Draft for the L1 to land as `corpus/lessons/round-80.md`. Every value below is either quoted from a
file this seat read (path and line given) or marked `[pending receipt: <path>]`. Nothing here is a
claim that an unrun check passed. Where a value moved while this seat was drafting, the measurement
that supersedes the earlier one is the one printed.

## Gate

Admit **S453** — RFC 9110, *HTTP Semantics*, §5.6.7 *Date/Time Formats*,
`https://www.rfc-editor.org/rfc/rfc9110.txt`, opened 2026-11-04. Two public GETs on the same day are
byte-identical: the wave scout's (HTTP 200, final URL identical, 502,941 bytes, sha256
`21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, fetched 2026-11-04T10:44:33Z —
`.ufo/waves/round-80/w1/ScoutSources/fetch-receipts.json`) and the knowledge seat's own
(`.ufo/waves/round-80/w1/ScribeKnowledge/gate-quote.md`; that seat's two records give the fetch time as
`10:44:53Z` in the entry's `source:` line and `10:45:05Z` in `gate-quote.md` — the digests agree, the
two timestamps do not, and the record keeps both). Retained: `.ufo/waves/round-80/sources/rfc9110.txt`
and `.ufo/waves/round-80/w1/ScribeKnowledge/rfc9110.txt`, same digest, 502,941 bytes (this seat read
both). Located quote, retained text lines 1855-1856 (the normative sentence wraps; 17 words when
joined):

> A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats.

The three shapes the sentence binds are at line 1848 (`Sun, 06 Nov 1994 08:49:37 GMT    ; IMF-fixdate`),
line 1852 (`Sunday, 06-Nov-94 08:49:37 GMT   ; obsolete RFC 850 format`) and line 1853
(`Sun Nov  6 08:49:37 1994         ; ANSI C's asctime() format`); the ABNF follows at 1873-1911, and line
1914 reads `HTTP-date is case sensitive.  Note that Section 4.2 of [CACHING] relaxes this for cache
recipients.` The knowledge seat's quote locator reports every span it used present in the retained
bytes, `quotes=19 found=19 missing=0` (`w1/ScribeKnowledge/quote-receipts.json`; its own run, not this
seat's). Tier A: an Internet Standards Track document with a normative `MUST` on the recipient. The row's
scope is the HTTP-date grammar and the comma rule that lets such a value survive field segmentation —
not the header's declaration role (S452/S449 ground), not crawler behaviour, not robots.txt.

The row is `corpus/SOURCES.md:200` (`spec`, tier `A`, `mined`, opened 2026-11-04, recheck `365d`,
used-by `corpus/knowledge/http-date-grammar.md`). It is a second scoped row on a document the registry
already holds: S028 carries the same plain-text file under empty-host URI validity with the recorded
digest `21c1cdce…7232a`, which equals the digest above, so the census takes a duplicate-URL warning
rather than an error. Measured on the lane worktree after the row and entry landed (2026-11-04):

- `sources-census.sh census --file <lane>/corpus/SOURCES.md` → `rows 191`, `tier.A 167`, `tier.B 7`,
  `tier.C 17`, `status.mined 161`, `status.queued 8`, `status.rejected 22` (base: 190 / 166 / 7 / 17 /
  160 / 8 / 22).
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, 20 `W04` lines
  (base 19), the new line being `W04 S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across
  scopes`.

Rejected / not written, with reasons:

- **RFC 9309 for the header carrier.** The round-79 rejection stands unchanged: the retained document
  carries no `x-robots-tag` occurrence and is already held as S099 (`corpus/lessons/round-79.md`,
  §Gate). No row was written for it in round 79 either — correction R79-1 below.
- **A second row on S449's Google URL with a header scope.** Carried from round 79, still unwritten: it
  is mechanically admissible (a `W04` only) but outside the frozen contract, which admits S453 only. The
  drafted row stays at `.ufo/waves/round-79/w1/ScoutSources/row-deferred-google-xrt.txt`.

Spot-check slot — **filled by the non-author closure, not by this lane.** Empty at draft time; until it
is filled this Gate has no non-author review, and the following four checks are what it owes:

1. Re-open `https://www.rfc-editor.org/rfc/rfc9110.txt`; record HTTP status, byte count, sha256 and
   fetched-at; compare against `21c1cdce…47232a` and 502,941 bytes as retained.
2. Locate the quoted sentence in §5.6.7 and agree or disagree with `tier A`, the scope cell and the
   duplicate-URL disposition.
3. Re-derive the C1 six-item verdict at the carrier with `python3 -B .ufo/waves/round-80/c80_defect_queue.py
   --root <tree> --revision <carrier>` — citing the counter's post-amendment-2 digest `ccb05318…`
   (`amendment-2.md`), not the freeze digest `90649c08…`.
4. Re-derive C2's two runs at the carrier with `python3 -B .ufo/waves/round-80/c80_measure.py --root
   <lane> --revision <carrier> --work <scratch>`.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **unsatisfiable predicate conjunct**: the C1 counter's R79-1 `used-by` read `row[11]` on an eleven-cell row, so no shape-valid row could ever resolve | `c80_defect_queue.py` at the freeze `f20163c1` (sha256 `90649c08…`): `used = row[11] if len(row) > 11 else ""` under `row_shape`'s `len(cells) != 11` check; the base control could not see it because the row is absent at the base (`controls/base-c80-defect-queue.txt:2` reads `R79-1 open no S453 row in corpus/SOURCES.md`), so the failure was masked by an earlier branch | the wave's `ScoutSources` seat, at the freeze bytes and **before any after-state** (`amendment-2.md`; `w1/ScribeKnowledge/r79-1-counter-probe.txt` shows freeze `(False, 'S453 used-by resolves to no file that cites S453')` vs HEAD `(True, …)` on the same eleven-cell row) | `amendment 2` (terms-only; predicate and item conditions unchanged): `used = row[10] if len(row) > 10 else ""` plus a three-case `--selftest` that shows the conjunct able to pass, able to fail, and able to reject a twelve-cell row (`selftest: 3/3 passed`, exit 0, `controls/ctl-c80-queue-selftest.txt`); counter digest `ccb05318…` at `de65ec21` |
| **same-round receipt rewrite**: the base and junk control receipts were re-cut in place by that fix, one added `exit=1` line each, disclosed only in amendment 2's prose | `git diff f20163c1..HEAD -- .ufo/waves/round-80/controls/`: `base-c80-defect-queue.txt` blob `d46bd610` → `dad8fb81` and `ctl-c80-junk-queue.txt` `a265d23a` → `b72e4af0`, each `+exit=1`; the verdicts did not move (re-run against the amended counter reproduces the rewritten base receipt body byte-for-byte — `w1/ScribeRecord/base-c80-defect-queue-rerun-diff.txt`) | this seat's byte diff; amendment 2 states "Regenerated controls after the fix" | a receipt of the round's own round is re-cut as a new file or carries an in-file marker naming the re-cut, never a bare in-place edit — the round-79 QUALITY `round_rewritten` rule applied to this round's own controls. Report-only here: `f20163c1` and `de65ec21` are both committed |
| frozen-premise: the round-79 contract called the RFC 822/850 `unavailable_after` branches case-pinned when no case carried them | `corpus/lessons/round-79.md:114`; the frozen 31-case set holds exactly two `unavailable_after` values, c16 `2025-12-31T23:59:59Z` and c17 `tomorrow` (`grep -rho 'unavailable_after[^"]*' .ufo/waves/round-79/cases`), and `grep -c 'GMT' .ufo/waves/round-79/expect/expect.json` prints `0` (this seat, 2026-11-04) | the round-79 scout's grammar read, routed before the tool existed; the defect is now measured, not argued: this round's base receipt prints `a2: cases=12 decided=12 wrong=10` (`controls/base-c80-a2.txt:3`) | a branch is never called covered without a case carrying it; c32-c43 now carry the comma-bearing IMF-fixdate, RFC 850 and asctime shapes, and the base receipt records the failure they were written against |
| spec-tool mismatch: the grammar splits every field value on ASCII `,` first, so S452's own example is rejected | `corpus/lessons/round-79.md:115` and `:165`; S452 retained text `.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt:239` (the page's own example, unchanged between rounds — the round-80 re-open is byte-identical, `w1/ScribeKnowledge/gate-quote.md`); this round's base prints `a2 wrong=10` and exit 1 (`controls/base-c80-a2.txt:3,6`) | ReviewC2 F1 (round 79) named it after the green matrix; the frozen case set could not see it | amendment 1 (A1 comma-after-weekday belongs to the value, A2 asctime joins the accepted shapes, A3 no new finding id) written before any case was scored and before the tool was touched; the frozen 31-case set stays a no-regression conjunct |
| criterion overclaimed a fixture's mechanism | `corpus/QUALITY.md:1631` renders the cheap-note control as `cheap-note (`malformed=1`)`; MutC reads the same fixture as red through `undisclosed` — `cheap-note stays red only via `undisclosed=1`` (`.ufo/waves/round-79/w1/MutC.md:57`), F2 at `:73` | the round-79 mutation-tester, whose k4 survivor row is the counterexample | the R79-4 correction below renames the mechanism, and the round-80 QUALITY clause requires each survivor to be killed by an isolated fixture |
| control expectation is not what the committed control prints | contract §Controls says a junk tree that fabricates the closure "must still print `open=6`" (`.ufo/waves/round-80/contract.md:97-99`); the committed receipt prints `C1v1 revision=worktree items=6 open=5 closed=1 exported=0 met=false` (`controls/ctl-c80-junk-queue.txt:8`) with `R79-5 closed withdrawal recorded; no self-assessment file repeats the sentence` (`:6`) | this seat's read of the frozen control; the cause is R79-5's closure being purely textual — a lesson line quoting the withdrawn sentence satisfies it, with no pointer that must resolve | reported, not edited. The control still gates: it exits 1 and reports `met=false`. R79-5's textual predicate is recorded as its own limit — a later round should require the withdrawal row's evidence pointer to resolve at the measured revision |
| contract control not shipped | `contract.md:100` names `controls/ctl-c80-consts.txt` (the four frozen degenerate constants over the new case set); the wave's controls directory holds no such file and nothing else references it — the measurement exists only inside `controls/base-c80-a2.txt` (`constants_failed=4/4` on both runs) | this seat's control inventory; the same class as the round-79 lesson's "contract control names do not resolve" row | reported, not amended: the constants conjunct is decided by the C2 predicate on both sets, so no claim rests on the missing file; a later round ships the named receipt or stops naming it |
| cosmetic: `exit=` is echoed more than once in the control receipts | `controls/base-c80-a2.txt:6,8,9` (`grep -c 'exit='` prints `3`: the nested round-79 matrix `c79_xrt_matrix.py:231`, `c80_measure.py:90`, and the freeze wrapper) and `controls/base-c80-defect-queue.txt` now prints it twice | this seat re-ran both commands in scratch on 2026-11-04; each receipt body reproduces byte-identically (`w1/ScribeRecord/a2-rerun-diff.txt`, `base-c80-defect-queue-rerun-diff.txt`), so the repeats are a rendering convention, not a defect | quote the whole line and count the exit once; nothing reads the line |

## Corrections

1. **R79-1 — erratum: the rejected `S453` row was never written, and the conjunct that was to close it
   could not pass.** The round-79 report says "One rejected row is kept (`S453`, RFC 9309, tier A,
   `status=rejected`, 0 `x-robots-tag` occurrences in its text)"
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-79/kake.md:143`), and the non-author closure
   measured `grep -c 'S453' corpus/SOURCES.md` = 0
   (`corpus/lessons/round-79-verifier-spotcheck.md` §6.1; re-measured this seat at the base:
   `git show 9998dc7a…:corpus/SOURCES.md | grep -c 'S453'` prints `0`). Erratum: no rejected row was
   written and none should be — **RFC 9309** stays held as S099 for robots.txt and its disposition for
   the header carrier is unchanged. `S453` is instead this round's **RFC 9110** row (§5.6.7
   `HTTP-date`), admitted in the Gate above (`corpus/SOURCES.md:200`; rows 190 → 191, `tier.A`
   166 → 167). The closure also needed the counter's `used-by` index repaired first (amendment 2, at
   `de65ec21`), because at the freeze bytes no shape-valid row could satisfy that conjunct.

2. **R79-4 — the precise MutC finding, and the two sentences harmonized.** k4 (the mutant that zeroes
   the `malformed` conjunct) survives the frozen battery because the cheap-note entry is counted under
   `undisclosed` as well: the k4 row reads "all 5 scenarios unchanged (cheap-note stays red only via
   `undisclosed=1`)" (`.ufo/waves/round-79/w1/MutC.md:57`), and F2 states an empty-note entry is counted
   as both `undisclosed` and `malformed` (frozen receipt `undisclosed=1 malformed=1`), so dropping
   `malformed` flips nothing (`:73`). The fixture *co-fires* `malformed` but never *isolates* it, and the
   round-79 QUALITY sentence that renders cheap-note as `malformed=1` (`corpus/QUALITY.md:1631`) is
   withdrawn as a mechanism claim while its row stands. Round 80's closure condition:
   `python3 -B .ufo/waves/round-80/c80_ledger_fixtures.py --root <tree> --json` reports `killed == 3`
   with k3 (`wrong_kind`), k4 (cheap-note) and k5 (`symlinks`) each killed by its own fixture and the
   cheap-note fixture red through `undisclosed == 1`; the run is recorded at `controls/c80-cheap-note.txt`;
   and the QUALITY clause naming `R79-4` with `undisclosed=1` is appended.
   `[pending receipt: .ufo/waves/round-80/c80_ledger_fixtures.py, controls/c80-cheap-note.txt]`

3. **R79-5 — the "31/31 before the tool existed" sentence is withdrawn.** Keep the next line as one
   physical line: the C1 counter's R79-5 predicate matches a single line carrying both the item id and
   the sentence.

   R79-5 withdrawal: `passed 31/31 before the tool existed` is withdrawn for want of a committed reference run.

   The round-79 report says "an L1 scratch reference passed 31/31 before the tool existed"
   (`.ufo/reports/round-79/kake.md:29`); no committed reference run exists and the scratch tree is gone,
   so the sentence is withdrawn. What the round actually rests on is unaffected and named instead: amendment 1's readings (A1 `noarchive`; A2 `none`
   replaced, `all` dropped, `index`/`follow` kept), the frozen 31-case set, and the matrix receipt. No
   lane self-assessment file repeats the sentence — the only lane occurrence is the non-author closure
   quoting it as the routed defect (`corpus/lessons/round-79-verifier-spotcheck.md:170`).

4. **R79-8 — the empty-output seats, and what the results file does and does not record.**
   `.ufo/waves/round-79/w1-results.json` holds 14 records, each with exactly four fields — `agent`,
   `name`, `note`, `output` — under top-level keys `lane, round, wave, seats, results`. Exactly two
   records carry an empty `output` string: `ExecC2Tool` (executor) and `CriticC` (critic), 0 bytes each,
   `output_sha256` of the empty string
   `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The file records **no** status,
   exit, timestamp or error text for any seat — `note` is `null` in all 14 — and
   `.ufo/waves/round-79/w1-dispatch.json` records `kind`, `agentId` (`null`), `role` and the item text
   only. The "last error text" template §2 asks for is therefore not recoverable from committed bytes;
   `.ufo/waves/round-80/defect-queue.json` records the two seats with their re-derived
   `output_bytes`/`output_sha256` and states that limit instead of inventing a message. Three further
   seats are non-empty but stopped after their first read — `ExecC1Ledger` (347 B), `ExecR2R3` (195 B),
   `ReviewC1` (241 B); their outputs are reading-progress notes with no deliverable and no
   `w1/<seat>.md` report, so they are recorded as thin, not as empty-output seats.
   `[pending receipt: .ufo/waves/round-80/defect-queue.json]`
