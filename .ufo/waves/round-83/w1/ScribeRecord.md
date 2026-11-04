# ScribeRecord — round 83 wave w1

Seat: scribe. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`, base
`826b0061f233ce1dffb9bd6874abc1342a864247`, freeze commit
`64b7199281e5457df0e08652977f698c4f34f46e`. Two deliverables: close C1's D6 by appending one
criterion line to `corpus/QUALITY.md`, and draft the four record appends for the L1. No other
production file was read-modified-written; no VCS mutation; no network; no tool installed.

## D6 — behavior

The frozen conjunct (`c83_defect_queue.py::item_d6`) is two-part: a `corpus/QUALITY.md` line that
carries `corpus/lessons/round-82.md`, `Gate` and `round-83` **on one physical line**, plus a `D6`
line in `corpus/lessons/round-83.md` carrying `§Gate` and `corpus/QUALITY.md`. I appended one
criterion section — `## Round 83 criterion — a Gate summary cites the lesson section it
summarises` — and one bullet, written unwrapped at 1,323 characters because the counter iterates
`splitlines()`. The criterion states the rule the round-82 report prose got wrong: a Gate summary
cites the lesson section it summarises, and a report's prose does not name a category where the
lesson has a row; the reject example is the round-82 report's "the `merge/kake` package" against
`corpus/lessons/round-82.md` §Gate's two S455 anchor rejects and the package's assimilation
non-adoption. Grounding cites `.ufo/waves/round-83/contract.md` §C1 D6 and
`corpus/lessons/round-82-verifier-spotcheck.md` §6 item 6. The stated limit is textual: the
counter reads one line, so a non-contradicting paraphrase passes and the non-author closure is
what catches a mis-transcription.

## Commands and exit codes

1. `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root .` (pre-edit) → exit 1;
   `D6 open criterion=no log=no`, `C1v1 revision=worktree items=6 open=6 closed=0 met=false`.
2. Same counter after the QUALITY append but before the lesson landed → exit 1;
   `D6 open criterion=yes log=no` (only the lesson-row conjunct was missing).
3. Token self-check over the appended line → exit 0; `lines=1701 criterion_hits=[(1701, 1323)]`,
   `Gate`×7, `corpus/lessons/round-82.md`×2, `round-83`×2, `.ufo/waves/round-83/contract.md`×1,
   `round-82-verifier-spotcheck.md`×1.
4. Same counter after `corpus/lessons/round-83.md` landed (ScribeLesson, same wave) → exit 1;
   **`D6 closed criterion=yes log=yes`**, `D3 closed`, `D4 closed`, `D5 closed`,
   `C1v1 revision=worktree items=6 open=2 closed=4 met=false` (D1, D2 still open — not this seat).
5. `python3 -B .ufo/waves/round-83/c83_drift_class.py --root .` → exit 0;
   `met=true` in worktree mode (`diffs=14 validator=0 representation=0 unknown=0
   verdict=same-object`, `# control=verdict=representation-changed validator=1`). Read only as
   context; the carrier-revision line is the L1's to paste.
6. `git diff --numstat -- corpus/QUALITY.md` → `4 0` (four insertions, zero deletions); the only
   tracked modification in the tree from this seat.
7. `sha256sum` over the four drafts, this report and `corpus/QUALITY.md` → recorded in
   `w1/ScribeRecord/receipts/draft-sha256.txt` (QUALITY.md
   `43ff73f935c2d92a1dc9b912599b39111344180eb0f170a704370bbd9f934291`).
8. Read-only reads: `controls/base-c83-defect-queue.txt` (`open=6 … met=false`, `base_c1_exit=1`),
   `controls/base-c83-drift-class.txt` (`tool_absent=1 met=false`, `base_c2_exit=1`),
   `controls/c83-selftest-c1.txt` (`selftest: 9/9 passed`), `controls/c83-selftest-c2.txt`
   (`selftest: 9/9 passed`), `controls/ctl-c83-junk-queue.txt` (`open=6 … met=false`),
   `controls/ctl-c83-control-class.txt` (`control_ok=0 met=false`),
   `controls/after-c2-classes.txt` (3 surfaces, `diffs=14`, all `per_request`, `same-object`),
   `controls/after-c83-instrument-check.txt` (`population=30 bound=30 mismatches=0 met=true`).

## Gates

- D6's own conjunct is falsifiable: the frozen selftest case `d6-missing-criterion` builds a tree
  whose `QUALITY.md` says `# QUALITY\n\n- no provenance criterion\n` and opens the item, and case
  `junk-prose-only` keeps the junk tree at `open=6` even with prose claiming closure. I read both
  case names in `controls/c83-selftest-c1.txt`; I did not re-run the selftest.
- The D6 row is only half the frozen item; the lesson half landed from ScribeLesson inside this
  wave and cites `corpus/QUALITY.md:1701` verbatim (`corpus/lessons/round-83.md:107`). The line
  number is stable under appends after it.
- C1 as a whole is **not met at this instant**: `open=2 closed=4 met=false`. D1 (wave accounting
  from spec+results) and D2 (UTF-8 `output_bytes` from `w1-accounting.json`) were still open when
  this report was written; that is other seats' work, not a D6 regression.

## Drafts for the L1 (paths under `w1/ScribeRecord/`)

- `scorecard-block.md` — round-83 measured-claims header, the two claim rows, the round-83 move
  log, the `Header-change classifier` capability row, and a stated-limits paragraph. Base lines
  are copied byte-exactly from the frozen receipts; after-state is `<<after-c1>>` / `<<after-c2>>`,
  with `<<carrier>>`, `<<verdict-c1>>`, `<<verdict-c2>>` also placeheld and listed in the draft's
  comment legend. Axes held: operability 10 HOLD, freshness 10 HOLD, calibration 2 HOLD.
- `log-entry.md` — `## Round 83 — 2026-11-04 (attempt 1; Linux host; …)` with contract,
  motivating evidence, wave shape (14 requested seats: scout 2, executor 4, scribe 3, reviewer 2,
  mutation-tester 2, critic 1; requested attack share 5/14 = 35.7 %), C1, C2, frontier/sources,
  mined mistakes, routed and not-done bullets. `<<settled-wave>>`, `<<sources-line>>`, `<<mined>>`
  and `<<assimilation>>` stay placeholders — WAVE-DONE is the L1's measurement.
- `province-append.md` — `## Round 83 header-change classification ground`: the class table
  (per-request / validator / representation / policy / unknown), the verdict rule, the committed
  record `controls/after-c2-classes.txt` (`summary surfaces=3 diffs=14 per_request=14 …`), the
  counter's re-derivation, and the stated limits (names not values; `unknown` decisive; no origin
  proof).
- `readme-row.md` — `## Coverage — round 83 (2026-11-04)` table row, sources line and frontier
  line. The entry `corpus/knowledge/header-change-classes.md` was absent when this seat first
  wrote the draft and landed at 180 lines later in the same wave (`S456` in its `source:` field),
  so the draft now cites it and keeps a presence guard rather than a warning.

## Touched surfaces

- Modified (tracked): `corpus/QUALITY.md`, +4/−0 lines (blank line, section header, blank line,
  criterion bullet). Nothing else tracked changed. The `??` entries at this instant are other
  seats' wave evidence and production files (`corpus/lessons/round-83.md`,
  `corpus/knowledge/header-change-classes.md`, `killers/`, `capture-control/`,
  `make_accounting_v2.py`, the control receipt, per-seat dirs) plus this seat's own files; this
  seat wrote none of the former.
- Created (untracked): `.ufo/waves/round-83/w1/ScribeRecord.md` (this report);
  `w1/ScribeRecord/{scorecard-block,log-entry,province-append,readme-row}.md`;
  `w1/ScribeRecord/receipts/{c1-queue-worktree-after-d6.txt,d6-line-check.txt,draft-sha256.txt}`.
- Not touched: `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `corpus/README.md`,
  `corpus/lessons/round-83.md`, the frozen counters/tool/controls, `.ufo/waves/round-82/` and
  earlier, the fleet repo, sibling repos, `considerthese/`, `corpus/SOURCES.md`.
- Scratch: none created; `/fast/scratch/hyaku/kake-r83/ScribeRecord` does not exist, so there is
  nothing to delete.

## Out of scope (not done, not claimed)

D1/D2/D3/D4/D5 production work and their after receipts; any commit, push or VCS mutation; the
carrier revision selection; the `S456` row and `corpus/knowledge/header-change-classes.md`; the
round-83 lesson (ScribeLesson); the SCORECARD/LOG/PROVINCE/README integration; the non-author
closure. I also did not re-run either counter's `--selftest` (I read the committed receipts) — that
is the L1's gate, not this seat's.

## Findings

1. **A criterion that spans two physical lines is invisible.** The frozen D6 conjunct matches per
   `splitlines()`; a naturally wrapped Markdown bullet fails even when every required token is
   present in the rendered paragraph. The line had to be written unwrapped (1,323 chars, still
   below the file's existing 1,422-char maximum). A future re-wrap of that bullet would silently
   reopen D6.
2. **D6 is a two-file item and the two halves landed independently.** My QUALITY append took the
   counter from `criterion=no log=no` to `criterion=yes log=no`; the item only read `closed` after
   ScribeLesson's D6 row landed. Had either seat been empty, D6 would have stayed open with the
   other half green — the counter's detail string distinguishes the two, which is why the row's
   conjuncts must not be collapsed into one.
3. **The round-82 defect is reproduced as a rule, not as a quotation.** The criterion names the
   exact misfile ("the `merge/kake` package" among Gate rejects vs the lesson's two S455 anchor
   rejects and the package's assimilation non-adoption) so a later Gate summary can be checked
   against it; the reject clause is prose because the defect was prose (D6's contract note).
4. **C2's committed classifier record is internally consistent with the frozen class table.**
   `after-c2-classes.txt` reports `diffs=14`, `per_request=14`, all other classes `0`,
   `verdict=same-object` on all three surfaces. That is the expected shape for two captures of a
   static object four minutes apart: `date`, `x-cache`, `x-fastly-request-id`, `x-served-by`,
   `x-timer` moved; nothing representation-bearing did.
5. **Draft hazards are marked, not smoothed over.** The knowledge entry landed mid-wave (finding
   6); the registry counts are not yet measurable; the wave's settled/attack counts arrive with
   WAVE-DONE; and the assimilation status must be re-derived. Each remaining placeholder is a
   named slot rather than a plausible number, per the "no invented numbers" instruction.
6. **Source scope is grounded for the L1.** The ScoutSources receipt (`w1/ScoutSources/fetch.txt`)
   records one GET of `https://www.rfc-editor.org/rfc/rfc9111.txt`, HTTP/2 200, 84,477 bytes,
   sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`; `quotes.tsv` locates
   §4 at L466, §4.2 at L581 and §4.3 at L801 of that retained copy. After the knowledge entry
   landed I replaced the drafts' `<<rfc>>` placeholder with the entry's own six-section scope
   (§3.1, §3.2, §4, §4.2, §4.2.3 and §4.3.1); no `<<rfc>>` token remains in any draft.

## Verdict

**D6 closed** — `corpus/QUALITY.md:1701` carries the criterion and `corpus/lessons/round-83.md:107`
carries the pairing row; the frozen counter reads `D6 closed criterion=yes log=yes`. All four
integration drafts are written with explicit placeholders for the after-state; no other production
file was touched. C1 overall remains `open=2 closed=4 met=false` pending D1/D2, which is outside
this seat.
