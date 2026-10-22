# Round-30 C1 — citing-set gate families F01-F06 (seat ExecGateFamilies)

## What I built

Sandbox clone: `/fast/scratch/hyaku/kake-r30/w1/ExecGateFamilies/clone`
Commit: `1ebdc064b3380e4d8b12117f74a30d8c799d9068` (base `4580c78`), branch detached from the lane clone.
Gate sha256: `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02`
Diff stat vs base: 17 files changed, 297 insertions(+), 23 deletions(-) — `scripts/citing_set.py` plus 4 new fixture cases.
Lane tree untouched except this report; no lane git/jj command was run.

Gate changes (only `scripts/citing_set.py` was edited):

1. `document_duplicate_key` — `json.loads` now runs with `object_pairs_hook=_reject_duplicate_members`; a member name repeated inside one JSON object, at any depth, is refused as `input_invalid` (exit 2). Decided while parsing, before the shape checks (`scripts/citing_set.py:505`, `:560`, `:568`).
2. `document_nonfinite_number` — `parse_constant` refuses `NaN`/`Infinity`/`-Infinity`; `parse_float` refuses literals outside the finite double range (`1e999`) via `math.isfinite`; an iterative post-parse sweep checks every parsed float with `math.isfinite` (`:521`, `:526`, `:539`, `:570`).
3. Population ids — `re.fullmatch(r"S[0-9]{3,}")` (`:189`, `:598`): `S1`, `S01`, `X001`, `s001` and `"S001\n"` are `population_id_unreachable` (exit 2). `fullmatch`, not `match`, so a trailing newline is refused.
4. Repeated options — a store-once `argparse.Action` on `--root/--revision/--population/--ledger` (`:800`). Every spelling (`--x v` twice, `--x=v` twice, mixed, abbreviated `--pop/--led/--rev/--roo`) exits 64 with the usual usage JSON object; a single occurrence, abbreviated or not, is unchanged.
5. Iterative corpus walk — `WorkingTreeSource` keeps its own stack of directory frames, no Python recursion (`:311`, `:332`). Git mode was already recursion-free (`git ls-tree -r`, `:439`) and is measured too.
6. `O_NOCTTY` — every `os.open` of an input document adds `getattr(os, "O_NOCTTY", 0)` beside `O_NONBLOCK`/`O_CLOEXEC` (`:285-289`).
7. Module docstring — reason list, accepted JSON profile, usage rule, safety note and the `S` + three-or-more-digits id rule (`:35-124`).

New fixtures (plain files, no setup step, object form `{"id": ..., "reason": ...}`): `38-document-duplicate-key`, `39-document-nonfinite-number`, `40-population-id-short-digits`, `41-document-nonfinite-overflow`. Cases 30-37 belong to the runner seat; legacy 01-29 untouched by me.

## Commands run (exit codes and observed output)

| Command (in the clone/sandbox) | Exit | Observed |
| --- | --- | --- |
| `python3 -B smoke.py` (14 hand-built cases) | 0 | 14/14 OK: dup top-level, dup nested, NaN, Infinity, -Infinity, 1e999, `S01`, `S001\n`, repeat `--population`, repeat `--population=`, repeat abbreviated `--rev`, single abbreviated `--pop` (clean), 1000-deep corpus (exit 1, one finding), clean tree (exit 0) |
| `python3 -B checkers/c1_reason_count.py --root clone --revision HEAD --scratch $PWD/count` | 1 | `C1 4/14 at 1ebdc06 (controls True, constant gates rejected True)` |
| `python3 -B checkers/c1_strict_checks.py --root clone --revision HEAD --scratch $PWD/strict` | 1 | `C1 strict 5/6 {'S1': True, 'S2': False, 'S3': True, 'S4': True, 'S5': True, 'S6': True}` |
| `python3 -B scripts/citing_set_selftest.py --root . --tmpdir $PWD/tmp` (base runner) | 1 | 33 cases, 4 failed: only 38-41, each `expected.json "findings" must contain only strings`; the 29 legacy fixtures pass |
| `python3 -B scripts/citing_set.py --selftest` (gate delegates to the base runner) | 1 | same summary: 33 cases, 4 failed, verdict `failed` |
| `python3 -B contract_runner.py …` (sandbox runner with the round-30 contract: strings compare ids, objects compare (id, reason)) | 0 | 33 cases, 0 failed |
| git-mode 1000-deep corpus (`--root gitdeep --revision HEAD`) | 1 | verdict `failed`, one `unadjudicated_citing_pair`, row `S001`, full `corpus/knowledge/d/d/…/entry.md`, stderr empty |

Counter detail (`.ufo/waves/round-30/c1_reason_count.py`): every **behaviour** part is true for all eight R codes, `document_duplicate_key` and `document_nonfinite_number`. F03 (short ids), F04 (repeated options), F05 (deep walk), F06 (O_NOCTTY) **PASS**. F01/F02 and R01-R08 fail only on the `fixture`/`compared` parts: no committed fixture names those codes yet, and the committed runner compares finding ids only, so the baseline runner exits 1 and the rename check cannot be graded.

Strict checker detail: S1 passes for all ten codes (each refusal returns exactly one finding `(input_invalid, code)`); S3 passes for all 16 repeated-option spellings plus "each option once"; S4 passes (row `S001`, full deep path); S5 passes (device opened through `os.open` with flag 526592 = O_NOCTTY|O_CLOEXEC|O_NONBLOCK, tty_nr 0); S6 passes for all five nested duplicate/nonfinite cases. S2 passes for the three codes a committed fixture names (`population_id_unreachable`, `document_duplicate_key`, `document_nonfinite_number`) and fails for the seven R codes with no fixture yet.

## Risks, blockers, not verified

- **Blocker outside my seat:** the counter's `compared` parts and the strict S2 need the runner seat's reason-aware runner and fixtures 30-37 naming the seven remaining R codes. Until then the counter reads 4/14 and the strict checker 5/6; the behaviour of the gate itself is complete for all ten codes.
- The base runner rejects object-form `expected.json`, so my four fixtures fail under it by design of the contract, not by a gate defect; the contract-shaped runner passes all 33.
- Fixture numbering checked with the runner seat: 30-37 theirs, 38-41 mine, no collision; I converted no legacy fixture.
- I did not run the lane's post-integration gate, and did not test the gate against live or owned web properties (none involved). No tooling was installed or upgraded (none needed).

## Observation for the closure (from the mutation seat, advisory)

On the merged tree (my gate bytes + the runner seat's runner + both fixture sets) the counter reads 14/14 with 41 cases and a clean runner baseline, and `diff -r` against the lane working tree `scripts/` is identical (mutation seat, commit 1ebdc06 + 9bf6896). One structural note worth carrying into the non-author closure: the counter's `compared` condition only bites for a code whose committed fixture exercises the reason through a per-case setup step. A runner that quietly skips setup cases keeps four of the ten codes ungraded (mutation row W3 killed R01, R04, R07, R08 only). The parse-time reasons (duplicate key, non-finite number, unreachable population id — my cases 38-41, plain files, no setup) are well covered; the setup-shaped ones (a FIFO or device document, an empty corpus, an unknown revision, a nested repository root — runner seat cases 30-37) are the ones a setup-skipping runner would lose.
