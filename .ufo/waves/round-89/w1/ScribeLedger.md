# ScribeLedger — round 89, wave 1 (bookkeeping drafts)

Seat: ScribeLedger (leaf; no subagent dispatch). Lane `kake-shokunin` (LANE). Measured at lane HEAD
`acc69ba59af9ddff84a704331087b9147cc0aa1b`; the lane was moving during this seat (HEAD went
`1b0f1008` → `acc69ba5` while I worked), so every number below names its revision. L1 must re-measure
at its own final carrier.

## Behavior and axes

Axes: calibration (lowest owned, 2 HOLD) and freshness (10 HOLD), as declared. This seat claims no score
change, no counter success, and no outside admission. It wrote drafts only. Its findings are that the
landed round-89 bookkeeping overstates two claims, and that the round's own instruments are defective in
the ways the wave review (ReviewCounterC1, ReviewCounterC2, CriticClaims, MutKey, ExecControls) already
routed. This seat re-derived those findings from receipts; it did not add new counter attacks.

## Outputs (all under my own paths)

Drafts, in `.ufo/waves/round-89/w1/ScribeLedger/`:

- `scorecard-round-89.md` — full replacement for the landed `## Round 89` section: claims table (axis,
  before→after, counting command, evidence), `integrated-selftest: 35/35` marker (exactly one), move-log
  pair, `### Demonstrated repertoire — round 89` row for the cache-key capability, `### Planned — after
  round 89` paragraph.
- `log-round-89.md` — replacement for the landed LOG entry (`LOG.md:3029`) in the round-88 entry's shape:
  motivation, claims, counter integrity, wave shape, actual domain work, assimilation, adjacency, tools.
- `skill-round-89.md` — new `## Round 89` section with its own header and three registry rows (`cache_key`,
  `c89 defect queue`, `c89 key capability`), plus the landing note to move the landed rows out of the
  round-88 table.
- `readme-round-89.md` — `## Coverage — round 89` row and `## Round-89 frontier step` paragraph; keeps the
  landed frontier-map row.

Receipts, in `.ufo/waves/round-89/w1/ScribeLedger/receipts/` (checksums in `SHA256SUMS`):
`c1-at-acc69ba5.txt`, `c1-base-revision-control-at-acc69ba5.txt`, `c1-selftest-run.txt`,
`c2-v2-at-acc69ba5.txt`, `c2-frozen-v1-at-acc69ba5.txt`, `c2-selftest-run.txt`, `candidate-identity.txt`,
`candidate-selftest-mode.txt`, `trial-committed-run.txt`, `trial-committed-results.json`,
`corpus-contract-at-acc69ba5.json`, and `c1-at-1b0f1008-superseded.txt` (an earlier C1 measurement, kept
and labelled).

Not written: no `corpus/`, `scripts/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`; no commit, no push,
no mutating git or jj command, no write to the fleet repo, sibling lanes or any source tree.

## Commands run and exits

All run from LANE, with `--work` under my scratch root, or read-only.

| Command | Exit | Result |
|---|---|---|
| `git archive 08ab46a1 .ufo/waves/round-89 \| tar -x -C <scratch>/v1` | 0 | frozen v1 counter tree extracted |
| `python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision acc69ba5… --work <scratch>` | 1 | `items=6 open=1 closed=5 met=false` (A open) |
| `python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision 76225160… --work <scratch>` | 1 | `items=6 open=5 closed=1 met=false` (E reads HEAD; RC-1) |
| `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision acc69ba5… --candidate scripts/cache_key.py --work <scratch>` | 0 | `frozen=16/16 props=200/200 refuse=9/9 controls=5/5 met=true` |
| `python3 -B <v1>/c89_key.py --root . --revision acc69ba5… --candidate scripts/cache_key.py --work <scratch>` | 0 | same line, `met=true` (frozen v1 counter) |
| `python3 -B .ufo/waves/round-89/c89_defect_queue.py --selftest` | 0 | `selftest: 12/12 passed` |
| `python3 -B .ufo/waves/round-89/c89_key.py --selftest` | 0 | `selftest: 43/43 passed` |
| `python3 -B scripts/cache_key.py --selftest < /dev/null` | 1 | `invalid_input: input is not valid JSON` (the tool has no selftest) |
| `python3 -B .ufo/waves/round-89/w1/ExecTrial/driver/trial.py scripts/cache_key.py <scratch>/trial-committed <LANE>/.ufo/waves` | 0 | 12 cases; key, exit and stderr equal ExecTrial's reference `results-reference.json` on all 12 (compared by script) |
| `python3 -B .ufo/waves/round-89/w1/L1/cache_key.py --selftest` | 0 | `selftest: 20/20 passed` (the L1 reference draft, not the lane candidate) |
| `node scripts/corpus-contract.mjs --json` | 1 | `ok:false`, 3 findings, all `missing_metadata:corpus/knowledge/meta-robots-directives.md`; that file has no round-89 commit, so the finding predates this round |
| `python3 -B .ufo/waves/round-89/c89_defect_queue.py --selftest` (run as the counter's own check) | 0 | 12/12 |

Reads: the freeze, contract, counters, frozen cases, both base receipts, the landed SCORECARD, LOG,
SKILL, README and PROVINCE rows, the round-88 SCORECARD and lesson, the round-89 lesson, and the seat
reports on disk (read in part; every seat figure I cite is attributed to its own receipt, and I did not
re-run those batteries). Note: my earlier pipe-based `exit=0` for the corpus contract was the status of `head`, not
of the tool; the corrected exit is the one in the table.

## Findings — the landed bookkeeping overstates or misstates (corrected in the drafts)

1. **C1 numbers are stale.** Landed SCORECARD and LOG state `open=5 closed=1` at `f62e7954`. At `acc69ba5`
   the counter prints `open=1 closed=5`, because the round-89 lesson markers landed afterwards. The draft
   states the carrier value.
2. **The C1 base control does not reproduce.** The frozen predicate says the same counter at `76225160`
   prints `open=6 closed=0`. With HEAD past dispatch it prints `open=5 closed=1` (item E reads HEAD, not
   `--revision`; RC-1, reproduced here). Only the freeze-time receipt `controls/base-c1.txt` shows
   `open=6`. The draft says so.
3. **Item E's "closed" is closed only on the frozen predicate.** The C2 counter changed after dispatch
   (`46a43e94` after `2e700b9a`), and E cannot see it (RC-2; CriticClaims §2.4). The draft states this next
   to the E verdict, not only in the lesson.
4. **The C2 instrument's admitted set is understated.** Landed text says "seven non-conforming stubs also
   score met". The reviews support more: a URI without escaping and values stripped of all whitespace
   (CriticClaims, four seeds); a 421-entry table over the committed seed (CriticClaims); runtime, alias,
   `file://` and environment imports, a hybrid literal table, and a guard bypass (ReviewCounterC2); 7 real
   survivors in 37 mutants (MutKey). The draft lists them.
5. **The planned C2 fix ("one frozen item per clause") is insufficient.** The guard is textual and
   bypassable, and the property classes compare key relations, not the key string. The draft names the
   needed change: key-string assertions against a declared oracle, plus a behavioural guard or none.
6. **C2 axis label is disputed.** The contract disclaims freshness; the critic places it under operability or
   coverage (D89-C2-6). The draft keeps the declared axis, keeps the score at 10 HOLD, and flags the label as
   a claim decision.
7. **SKILL rows sit inside the round-88 table** (added to its end), so a filed table changed and round 89 has
   no heading. The `cache_key` row's Selftest cell also implied the tool had one. The draft moves the three
   rows into a `## Round 89` section and states that `--selftest` is not a recognised argument (verified
   above).
8. **Trial count.** The landed LOG says six real cases (R1–R6). ExecTrial's table has seven (R2b is real);
   five synthetic refusals; twelve in total. The draft says seven and twelve.
9. **Wave settlement is not verifiable from disk.** There is no results JSON and no wave-done receipt (round 88
   had both). Ten seat reports are on disk; ScoutRFC has receipts only; ScribeEntry's directory is empty;
   ScribeLesson has no output on disk. The landed LOG's "one v1 wave, 14 seats" is kept with that stated.
10. **Contract and reference gaps that the prose must not hide** (ReviewCounterC2 6, 9; ExecTrial D1): the
    duplicate-`Vary` line combination is unspecified (the driver joins with `, `); U+001D is escaped by the
    reference but is not one of the contract's named separators; the contract's GS (U+001C) is FS in ASCII;
    duplicate JSON keys and CTL bytes in non-nominated values are unaddressed.

## Defects in the round's own instruments (reported, not repaired)

- C1 item E: reads HEAD (RC-1); blind to post-dispatch amendment (RC-2); same-second false red (RC-3); mirror
  skips E (RC-4).
- C1 item C: regex sees 5 of 21 named receipts (RC-9). Item A: tag exemption and scope gaps and self-reported
  count (RC-5, RC-6, RC-7). Item B: substring classification (RC-8). Item F: substring header match (RC-10).
- C2 counter: textual guard bypassed by runtime-built paths, `file://` reads and environment paths
  (ReviewCounterC2 2); relations-only properties (3); substring refusal reasons (5); uncovered clauses (ExecControls
  1–7); guard rejection prints one character per line (ReviewCounterC2 8; the reason is lost).
- C2 committed candidate: no selftest; `--selftest` is not recognised.

## Honest limits

- The drafts pin `acc69ba5`. L1's carrier may differ; every revision-bearing number must be re-measured.
- The mutation, adversarial and reviewer figures are cited from their seats' receipts; I did not re-run those
  batteries. The numbers I measured myself are the C1 and C2 runs, the trial comparison, the selftests and the
  corpus-contract exit.
- The trial comparison used the committed candidate's bytes at blob `13ea9374` (sha256 `3a658326`); the
  candidate's identity is in `receipts/candidate-identity.txt`.
- No claim about storage, reuse, freshness or serving appears in any draft.
- Adjacency and assimilation were taken from the landed ConnectorScope and round-88 records. I did not re-run
  the 20-lane sweep.

## Tools

None installed or upgraded. Only `git`, `python3` and `node` (already on the host) were used. No pacman, no
network GET, no credentials. Nothing written to `~/.local/bin` or any PATH directory.

## Scratch

`/fast/scratch/hyaku/kake-r89/ScribeLedger/` held the frozen-v1 archive, the trial output, the scored
receipts and one parallel-copy mistake (an empty corpus-contract copy, caught and recopied sequentially). Its
receipts were copied into `receipts/`; the directory is deleted before yield. No file under `/tmp` was used,
and no `/tmp` path is cited as evidence.
