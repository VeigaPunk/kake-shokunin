# ReviewRegB — C1 row-review of the 26 round-99 repair rows (SKILL.md)

Seat: ReviewRegB (reviewer, leaf — no subagents). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
Scope: judge every cell of every row the C1 repair adds (`## Round 99 — tool registry completion`,
26 rows), against the tool bytes at the C1 repair commit.

## Method

For each row and each cell (Kind, Entry command, Verdict map, Self-test, Write scope, Owner):

1. Read the tool at 9d341d1b46f16dbfbb41af75dd6d4966808dfa5d (scratch extraction via
   `git archive`, plus a read-only `git clone --shared` pinned to the same commit for runs —
   a "clean checkout" as the Self-test cells claim). Cell truth judged against the code:
   argparse/manual flag parsing, every `return`/`sys.exit`/`process.exit` site, every write site.
2. Ran every Self-test cell command that the cell claims exists, from the pinned clone, with
   `TMPDIR` pointed at my scratch and explicit `--tmpdir`/`--work` where the cell names them.
   `no self-test` cells verified by `grep -c -- "--selftest"` (0 refs) and reading the parser.
3. Exercised entry forms and usage/edge exits that decide verdict-map truth (observed rc below).
4. Owner `kake`: convention of the lane registry (all 26 rows identical); nothing in code
   contradicts it.

A row is `agree` only if no cell is false; wording I would improve is noted on an `agree` line.

## Instrument verification (before attacking)

`controls/instrument-sha256.txt` (11 entries): recomputed sha256 of each working-tree file AND of
`git show 2345e309640adac6c36e41eca87409085ba3a276:<path>` — all 22 digests equal the frozen
values (c99_registry.py 0f39bbbc…, c99_fresh304.py d13bba5d…, fresh304-contract.md 2be46b4d…,
8 frozen control files). No mismatch; no repair license needed or used.

## Environment

- Scratch root: /fast/scratch/hyaku/kake-r99/ReviewRegB/ (tree extraction, shared clone pinned to
  9d341d1b verified via `git rev-parse HEAD`, w/ tmp dirs, st/ results). Deleted before yield.
- No mutating git/jj command was run in the lane or fleet repo; LANE touched only via
  show/archive/ls-tree/clone --shared (all read-only). Identity: no commits made at all.
- Tooling installed: none. python3 3.x system, node system — no installs to record.

## Self-test cell runs (command from the cell, observed rc)

| Row | Command (from cell, cwd=clone at 9d341d1b) | rc |
|---|---|---|
| base_path_selftest.py | python3 -B scripts/base_path_selftest.py | 0 (`45/45 fixtures passed`, stderr, scripts/base_path_selftest.py:310) |
| citing_set.py | python3 -B scripts/citing_set.py --selftest | 0 |
| citing_set_selftest.py | python3 -B scripts/citing_set_selftest.py --selftest --tmpdir <scratch>/cit | 0 |
| citing_set_hostile_selftest.py | python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir <scratch>/hostile | 0 |
| conditional_eval.py | python3 -B scripts/conditional_eval.py --selftest | 0 (`selftest 99/99`) |
| header_change_class.py | python3 -B scripts/header_change_class.py --selftest | 0 (`selftest: 6/6 passed`) |
| knowledge_metatext_lint.py | python3 -B scripts/knowledge_metatext_lint.py --selftest | 0 (`selftest 13/13`) |
| landed_check.py | python3 -B scripts/landed_check.py --selftest | 0 (`selftest 14/14`) |
| ledger_latest_check.py | python3 -B scripts/ledger_latest_check.py --selftest | 0 (`selftest: 2/2 passed`) |
| link_preview_selftest.py | python3 -B scripts/link_preview_selftest.py | 0 (`"passedOverTotal": "46/46"`) |
| quote_class.py | python3 -B scripts/quote_class.py --selftest | 0 (`selftest 4/4`) |
| robots_audit.py | python3 -B scripts/robots_audit_selftest.py | 0 (verdict clean) |
| robots_audit_selftest.py | python3 -B scripts/robots_audit_selftest.py | 0 (same command as robots_audit.py row's cell; one run covers both) |
| sidecar_reobserve.py | python3 -B scripts/sidecar_reobserve.py --selftest --work <scratch>/sidecar | 0 (`tests=10 failures=0`) |
| sitemap_audit_selftest.py | python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py | 0 (`PASS 271/271`) |
| source_recheck_hardening_selftest.py | python3 -B scripts/source_recheck_hardening_selftest.py | 0 (`10/10`) |
| source_recheck_selftest.py | python3 -B scripts/source_recheck_selftest.py | 0 (`106/106`) |
| stale_extensions.py | python3 -B scripts/stale_extensions.py --selftest | 0 (`cases=113 passed=113`) |

`no self-test` rows (cache_key.py, cache_key_conformance.py, live_snapshot.py, probe-delta.mjs,
response_snapshot.py, reval_exchange.py, source_snapshot.py, wave_seat_record.py): 0
`--selftest` references each — claim true. Scored-by references checked to exist at 9d341d1b:
`.ufo/waves/round-89/c89_key.py`, `.ufo/waves/round-97/c97_reval.py`.

## Observed entry/exit evidence (decides verdict-map cells)

- cache_key.py: valid stdin rc=0 `{"key": ...}`; invalid stdin rc=1 `invalid_input: …` stderr.
- reval_exchange.py: invalid stdin rc=1 `invalid_input: body is not JSON`.
- conditional_eval.py: invalid stdin rc=1; refusal contract matches cell (empty stdout asserted by selftest).
- stale_extensions.py: invalid stdin rc=1 `invalid_input: …`.
- probe-delta.mjs: 2-sweep history rc=0; `--bogus` rc=64; empty history rc=2 (`zero usable rows`).
- citing_set.py: missing --population/--ledger rc=64 with JSON `could-not-evaluate` usage verdict.
- knowledge_metatext_lint.py: `--root . --revision HEAD` on clone rc=0, `gate_findings=0
  review_hits=146` (review-tier allowed, exactly as the `0` cell says).
- ledger_latest_check.py: `--root .` on clone rc=0, `3 figures, 0 mismatches`.
- sidecar_reobserve.py: `--check --root .` on clone rc=0, `wrote=false` (read-only confirmed).
- live_snapshot.py: no args rc=64; `--help` rc=0.
- response_snapshot.py: `--bogus` rc=64 (SystemExit translation); defaults run hits its own
  committed capture leaves -> collision path rc=2 (no writes occurred; check precedes makedirs).
- source_snapshot.py: no args rc=2 (argparse; row claims no 64 — consistent).
- header_change_class.py: no args rc=64 (explicit usage return).
- landed_check.py: no args rc=64 (explicit usage return).
- cache_key_conformance.py: no args rc=2 (argparse; row maps 2 to usage/self-check — consistent).
- wave_seat_record.py: no args rc=2; fixture run (results/spec in scratch, --out in scratch) rc=0,
  record written, `seats=1 empty=0 not_settled=0`.
- quote_class.py: no args rc=2 (NOT the claimed 64).
- sitemap_audit_selftest.py: `--bogus` rc=64; tool-not-found path returns 64
  (scripts/sitemap_audit_selftest.py:1549-1550). No exit-2 path exists in the runner.

## Disagreements (false cells; path:line + observed rc)

1. **quote_class.py — Verdict map cell `64` usage.** scripts/quote_class.py:142 calls
   `ap.error("one of --selftest or classify is required")`, which raises SystemExit(2); the
   `return 64` at :143 is unreachable. Observed: `python3 -B scripts/quote_class.py` (no args)
   rc=2. The tool's own docstring states "Exits: 0 …; 2 unreadable input or usage fault".
   No code path yields 64.
2. **sitemap_audit_selftest.py — Verdict map cell `2` setup fault.** The runner exits only
   0/1/64: usage errors and tool-not-found return 64 (:1538-1550), coverage gaps or case
   failures return 1 (:1585). The only `return 2` sites (:1332, :1337) are inside the
   `CONSTANT_CLEAN_TOOL` generated-fake-tool string (fault-injection payload), not the runner.
   Observed: `--bogus` rc=64.
3. **wave_seat_record.py — Verdict map cell `64` usage.** scripts/wave_seat_record.py:45 is a
   plain `ap.parse_args()` with no SystemExit translation, so usage faults exit 2 (argparse
   default) and nothing returns 64. Observed: no-args rc=2. The row mirrors the tool's docstring
   ("Exit 0 …, 2 unreadable input, 64 usage"), but the docstring contradicts the code.

## Agree-with-note rows (cell not false; wording I would improve)

- header_change_class.py: exit 1 also occurs on `--selftest` failure (:296); row maps 1 only to
  unevaluable input.
- probe-delta.mjs: 64 also returned for invalid `--hole-hours`/`--since` values (:48-53); cell
  names only "unknown flag".
- ledger_latest_check.py / knowledge_metatext_lint.py / robots_audit_selftest.py: argparse usage
  faults exit 2 and selftest failure exits 1 (secondary meanings of mapped codes, unmapped).
- source_snapshot.py: also writes `receipts.json` next to the manifest (:297); write-scope cell
  names only "the manifest and body files it names". All writes stay in declared output locations.
- source_snapshot.py / cache_key_conformance.py: optional flags shown unbracketed / `--work`
  falls back to TMPDIR when omitted; forms run as written.
- response_snapshot.py / live_snapshot.py: default `--population`/`--out` point inside the lane
  tree (round-23/round-61 wave dirs) — relevant when run without explicit args.

## Verdict file

`verdicts.tsv` — 26 lines, `<row name>\t<agree|disagree>\t<reason>`, same order as the repair
table. Count: agree=23, disagree=3.

REVIEW rows=26 agree=23 disagree=3
