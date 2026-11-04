# kake round 80 — frozen contract (author L1, before any seat ran)

Lane: kake. Round: 80 (attempt 1). Base measured revision: `9998dc7a586b9fe76379014c8123aa3606f2d8b9`
(the lane tip at freeze time; the round-79 settle). Axes owned: operability, freshness; calibration is
the lowest non-retired axis (score 2). Scores are HOLD unless a claim says otherwise; a claim moves
evidence, not a scalar.

Two claims, causally separable: C1 (calibration) is verifiable with C2 unlanded, and C2 (operability)
with C1 unlanded. Each has one counting command, one frozen predicate and its own controls.

## C1 — calibration: the round-79 routed-defect queue closes to zero open

Surface: the eight routed defects the non-author round-79 closure filed in
`corpus/lessons/round-79-verifier-spotcheck.md` §6. The two medium work items (R79-6 fixture
mutants, R79-7 date grammar) belong to C2 and are **not** in C1's population; C1's population is
the six report/receipt-accuracy items **R79-1, R79-2, R79-3, R79-4, R79-5, R79-8**.

Counter: `python3 -B .ufo/waves/round-80/c80_defect_queue.py --root <tree> [--revision <rev>]`.
It prints one line per item (`R79-N closed|open <detail>`) and a summary
`C1v1 revision=<label> items=6 open=<k> closed=<m> met=<true|false>`, exit 0 met / 1 not met / 2
unevaluable / 64 usage. With `--revision` it exports the paths it reads from that revision into a
TMPDIR scratch tree and evaluates there, so the verdict is over committed bytes.

Frozen predicate, one sentence, repeated verbatim as the counter's label:

    met <=> open == 0 for the six items R79-1, R79-2, R79-3, R79-4, R79-5, R79-8

Per-item closure conditions (each is what "closed" means; the counter implements exactly these):

| Item | Closed iff |
|---|---|
| R79-1 | `corpus/SOURCES.md` carries an `S453` row whose `source` cites RFC 9110 and not RFC 9309, **and** `corpus/lessons/round-80.md` records the erratum naming `R79-1`, the withdrawn sentence's subject and `S453` |
| R79-2 | `scripts/ledger_append_guard.py` exists, its `--selftest` exits 0 and prints one non-prefix append fixture as failed, and its run over the lane reports the receipt ledger's byte prefix preserved |
| R79-3 | `.ufo/waves/round-80/controls/c80-selftest.txt` holds a `selftest: N/N passed` line and `exit=0`, and re-running the tool's `--selftest` at the measured revision prints the identical line |
| R79-4 | `.ufo/waves/round-80/c80_ledger_fixtures.py --root <tree> --json` reports `killed == 3` with the three survivors isolated (k3 `wrong_kind`, k4 cheap-note, k5 `symlinks`), the cheap-note fixture red through `undisclosed == 1`; `controls/c80-cheap-note.txt` records that run; `corpus/QUALITY.md` carries a criterion clause naming `R79-4` with `undisclosed=1` |
| R79-5 | `corpus/lessons/round-80.md` withdraws the sentence in a row naming `R79-5`, and no lane self-assessment file (`SCORECARD.md`, `SKILL.md`, `LOG.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/**`) repeats it |
| R79-8 | `.ufo/waves/round-80/defect-queue.json` records every round-79 seat whose output was empty, with the `output_bytes` and `output_sha256` values re-derived from `.ufo/waves/round-79/w1-results.json` |

Kill rule: any of the six open at the carrier fails C1. A counter that meets at the base fails its
own premise (it is redone before data). A junk tree that merely asserts closure must still report
every item open.

## C2 — operability: `unavailable_after` accepts the date shapes its source names

`scripts/x_robots_tag_audit.py` (round 79) splits every field value on ASCII comma before parsing,
so every comma-bearing date shape is unreachable: S452's own example,
`unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT`, yields `xrt_invalid_value` plus
`xrt_unknown_directive` (`corpus/lessons/round-79.md` §Limits; routed as R79-7). The frozen round-79
grammar is amended by `amendments/amendment-1.md` (terms only, written before any case was scored
and before the tool was touched): a comma that follows a leading weekday token inside an
`unavailable_after` value belongs to the value, and the asctime shape joins the accepted set.

Counter: `python3 -B .ufo/waves/round-80/c80_measure.py --root <lane> --revision <rev> --work <scratch>`.
It runs the frozen round-79 matrix counter (`c79_xrt_matrix.py`) twice over the same tool revision —
once over the frozen 31-case set, once over this round's 12-case set (`cases/`, oracle
`expect/expect.json`, the four frozen constants of `.ufo/waves/round-79/consts`) — and prints one
summary line.

Frozen predicate, one sentence, repeated verbatim as the counter's label:

    met <=> frozen wrong=0 and a2 wrong=0 and constants_failed=4/4 in both runs and selftest_ok=true in both runs

Before state: at the base the same command prints `frozen wrong=0` (the round-79 capability stands)
and `a2 wrong=10` (ten of twelve date-shaped cases decided against the source-derived oracle).

Kill rule: any a2 case wrong at the carrier, or the frozen 31-case set regressed, or any of the four
degenerate constants surviving on either set, or the tool's own `--selftest` failing, fails C2. The
oracle is derived from the grammar and the two named sources (S452 retained bytes, S453 live fetch),
never from a green run of the tool; the counter copies each manifest to scratch before the run, so
the tool receives payloads and never the oracle.

## Case set (frozen inventory, 12 cases, c32–c43)

| id | field value | expected |
|---|---|---|
| c32 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (S452's own example) | clean, directive kept |
| c33 | `unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` (RFC 850 shape) | clean |
| c34 | `unavailable_after: Sun Nov  6 08:49:37 1994` (asctime shape, two-space day) | clean |
| c35 | `unavailable_after:2025-12-31` (ISO date only) | clean |
| c36 | `unavailable_after:2025-12-31T23:59:59-03:00` (ISO offset) | clean |
| c37 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 PST` (comma date, wrong zone) | `xrt_invalid_value` only |
| c38 | `noindex, unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, noarchive` | clean, three directives |
| c39 | two comma-bearing dates | `xrt_duplicate_directive` |
| c40 | `googlebot: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | clean, per-bot token |
| c41 | comma date then `frobnicate` | `xrt_unknown_directive` only |
| c42 | `max-snippet: 20, unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` | clean, two directives |
| c43 | `unavailable_after: Sun Nov 16 08:49:37 1994, noindex` | clean, two directives |

The oracle is `expect/expect.json` (`schema: xrt-expect/v1`), generated by the committed authoring
record `make_cases.py` from the grammar, before any tool run. The case set and the oracle are frozen
with this contract; a case may not be added, removed, or re-scored after any seat has run.

## Controls (committed before data)

- `controls/base-c80-defect-queue.txt` — C1 counter at the base revision: `open=6 met=false`, exit 1.
- `controls/base-c80-a2.txt` — C2 counter at the base revision: `a2 wrong=10`, `met=false`, exit 1.
- `controls/ctl-c80-junk-queue.txt` — the C1 counter over a scratch tree that fabricates the closure
  artifacts (lesson asserting all six closed, a receipt with the right words) and holds no source
  evidence: it must still print `open=6`.
- `controls/ctl-c80-consts.txt` — the four frozen degenerate constants over the new case set: each
  must fail at least one case.

## Scope of the round

Write scope: the lane repo and this wave directory; the report on the fleet repo. No publishing, no
deploy, no live-property fetch beyond source openings (one public GET per opened source). The frozen
round-79 contract, case set, oracle and receipts are never edited: this round amends the grammar by a
new amendment and adds a new case set beside the old one.
