# MutBaseRunnerLedger — pre-repair mutant ledger of the base citing-set runner

Seat: `KakeR30.MutBaseRunnerLedger` (mutation-tester, operability). Leaf seat, no
subagents. Lane read-only except this report. Sandbox:
`/fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger/`.

## What I attacked

Base revision `035668132250b75b38d399e86e540b0a0371efbc` (lane
`/home/vgpnk/Projects/shokunin/kake-shokunin`). The `scripts/` tree at that
revision is byte-identical to the tip commit `4580c78` (`git diff --name-only
0356681 4580c78 -- scripts/` → 0 lines), so the base gate is the gate the round
is about to repair.

Mutation: for every reason code the base gate can emit, rename it in a **copy**
of the exported tree (`"<code>"` → `"<code>_mutated"`, every double-quoted
occurrence), then run the **committed runner** `scripts/citing_set_selftest.py`
over that copy. Killed = runner exit ≠ 0. Survived = runner exit 0.

Reason codes enumerated by AST over `scripts/citing_set.py` (first argument of
every `InputInvalid(...)` call plus every `"reason":` dict value): **23**, not
22. The extra one over the seat brief's count is `not_a_regular_file`
(gate lines 294, 372, 377 — the corpus-side sibling of
`document_not_regular_file`). I ledgered all 23; no code was dropped.

| artefact | path | sha256 |
|---|---|---|
| exported base gate | `base/scripts/citing_set.py` | `d7e79ba102ff27761d830f95ad91e1970ebfcc942eea9728a0bdf3b0c3479d48` |
| exported base runner | `base/scripts/citing_set_selftest.py` | `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` |
| git blob of the gate at base | — | `d868b7dc668500c261b0eb595fc153685d3456dc` |
| fixture cases exported | `base/scripts/fixtures/citing-set/` | 29 directories |

## Result: 23 survivors, 0 kills

Every one of the 23 reason codes **survived**. The runner exits 0 with 29
cases and 0 failed on every mutated tree. Reason: the base runner compares the
exit code and the sorted multiset of **finding ids** only
(`citing_set_selftest.py:154-163` `finding_ids`, `:288-303` the two
comparisons); the `reason` field of a finding is never read. A renamed reason
code therefore leaves every fixture expectation satisfied.

| # | reason code | gate lines | renamed | runner exit | verdict | named by a committed fixture | probe changes output |
|---|---|---|---|---|---|---|---|
| 1 | absolute_path_not_allowed | 183 | 1 | 0 | Survived | — | yes |
| 2 | corpus_directory_missing | 255, 382 | 2 | 0 | Survived | — | yes |
| 3 | corpus_directory_unreadable | 258, 280 | 2 | 0 | Survived | — | yes |
| 4 | corpus_empty | 270 | 1 | 0 | Survived | — | yes |
| 5 | corpus_file_not_utf8 | 496 | 1 | 0 | Survived | — | yes |
| 6 | descending_range | 517 | 1 | 0 | Survived | 13-descending-range (id only) | yes |
| 7 | document_not_json | 419 | 1 | 0 | Survived | 15-invalid-json-population (id only) | yes |
| 8 | document_not_regular_file | 238 | 1 | 0 | Survived | — | yes |
| 9 | document_not_utf8 | 415 | 1 | 0 | Survived | — | yes |
| 10 | document_shape_invalid | 421, 428, 433, 436, 449, 453, 457, 459 | 8 | 0 | Survived | 16-invalid-population-shape (id only) | yes |
| 11 | document_unreadable | 234, 244 | 2 | 0 | Survived | — | yes |
| 12 | empty_path | 180, 188 | 2 | 0 | Survived | — | yes |
| 13 | git_command_failed | 355 | 1 | 0 | Survived | — | yes |
| 14 | git_unavailable | 323, 339, 353 | 3 | 0 | Survived | — | yes |
| 15 | not_a_directory | 266, 379 | 2 | 0 | Survived | — | yes |
| 16 | not_a_regular_file | 294, 372, 377 | 3 | 0 | Survived | — | yes |
| 17 | path_escapes_root | 186, 226 | 2 | 0 | Survived | — | yes |
| 18 | population_id_unreachable | 439 | 1 | 0 | Survived | — | yes |
| 19 | revision_not_found | 330, 341 | 2 | 0 | Survived | — | yes |
| 20 | root_not_a_directory | 711 | 1 | 0 | Survived | — | yes |
| 21 | root_not_repository_top_level | 325 | 1 | 0 | Survived | — | yes |
| 22 | span_too_large | 529 | 1 | 0 | Survived | 14-oversize-range (id only) | yes |
| 23 | symlink_rejected | 264, 288, 375 | 3 | 0 | Survived | — | yes |

**No equivalent mutants.** For each code I built a probe tree that provokes it
and ran the pristine and the mutated gate on it: all 23 probes provoked their
code (`probeProvokesCode: true`) and all 23 changed the gate's JSON output
(`probeOutputChanged: true`). So every survivor is a real behavioural change
that the committed runner does not catch, not a no-op mutation. Example
(`descending_range`, manual): the mutated gate emits
`"reason": "descending_range_mutated"` in the finding while the id stays
`citation_range_invalid` — the runner sees an unchanged id and passes.

## Controls (the detector is not broken)

| control | what | runner exit | meaning |
|---|---|---|---|
| K-baseline | pristine exported tree | 0 (clean, 29/0) | a non-zero exit on a mutant would be a real detection |
| K-positive | finding **id** renamed (`"input_invalid"` → `"input_invalid_control"`) | 1 (failed, 29 cases, 2 failed) | the runner does kill a mutation of the field it compares — the 23 survivors are a gap in the compared field, not a broken detector |

## Commands run (all inside the sandbox; exit codes shown)

| command | exit | observed |
|---|---|---|
| `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone` | 0 | clone at tip `4580c78` |
| `git archive 0356681 scripts/citing_set.py scripts/citing_set_selftest.py scripts/fixtures/citing-set \| tar -x -C ../base` | 0 | 120 files, 29 fixture cases |
| `python3 -B base/scripts/citing_set_selftest.py --root base --tmpdir scratch/base-tmp` | 0 | clean, 29 cases, 0 failed |
| `TMPDIR=$PWD/scratch python3 -B mutate.py` (the whole ledger) | 0 | 23 codes, 0 killed, 23 survived |
| `python3 -B ctrl/scripts/citing_set_selftest.py --root ctrl --tmpdir scratch/tmp-ctrl` | 1 | positive control, 2 failed cases |
| `uv run --no-project --offline --with jsonschema==4.25.1 python3 -B mte_report.py` | 0 | MTE report written, schema 3.9.0 validation OK |
| `node official_metrics.mjs` | 0 | official metrics: total 23, killed 0, survived 23, score 0 |

## Deliverables

- `/fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger/ledger.json` — the
  23-row ledger (schema `kake-mutant-ledger-v1`): per row the code, gate
  lines, occurrence count, pristine and mutant gate sha256, runner exit /
  cases / failed, verdict, the committed fixtures that name the code, the
  reproducible commands, the probe reasons before and after, and the
  equivalent-mutant flags. Top level carries the base metadata, the detector
  definition, both controls and the summary.
- `/fast/scratch/hyaku/kake-r30/w1/MutBaseRunnerLedger/ledger.mte.json` — the
  same ledger in the mutation-testing-elements report shape of
  `corpus/knowledge/mte-report-interop.md` (tameshi, revision `f4e8f7d8`):
  `schemaVersion "1"`, `thresholds {high 80, low 60}`, `framework`, one file
  entry `scripts/citing_set.py` with `language "python"`, the pristine source
  bytes and one mutant per code (`id`, `mutatorName`, `description`,
  `replacement`, `location`, `status`, `statusReason`). Validated against the
  vendored official schema 3.9.0 (`jsonschema` Draft-07) — **OK**. Official
  metrics via the vendored `mutation-testing-metrics` 3.9.0 library: total 23,
  killed 0, survived 23, `mutationScore` 0.
- Driver and evidence: `mutate.py`, `mte_report.py`, `official_metrics.mjs`,
  `vendor/` and `vendor-metrics/` (extracted from the integrity-pinned
  tameshi tarballs), `scratch/` (baseline, control and metric outputs).

## Restoration evidence

Each mutant ran in its own throwaway copy under `work/mut-<code>/`, removed
after the run. The exported base tree was never written: the gate sha256
before and after the whole ledger is identical
(`d7e79ba102ff…479d48` both times), as is the runner sha256
(`3c167895c7f3…62a1c`), and the fixture directory still holds 29 cases.

I wrote exactly one file inside the lane: this report. I did not write to
`scripts/` at any point. Note that `git status --porcelain scripts/` in the
lane is **not** empty as I finish: `scripts/citing_set.py`,
`scripts/citing_set_selftest.py`, four `expected.json` files and twelve new
fixture directories (30–41) are modified or untracked. Those are the
concurrent repair landed by the sibling executor seats
(`ExecGateFamilies`, `ExecRunnerReasonFixtures`), not my writes — my seat
never opened those paths for writing. I did not measure an after value against
that in-flight working tree, because it was still moving while I ran; the
after value must be taken from a landed commit.

## What this means for the L1 (advisory)

- The round-30 C1 repair is **necessary**, and this ledger is its measured
  before value: the base runner's detection power over the reason field is
  zero. The C1 counter's own `compared` sub-check already records the same
  thing at base — `.ufo/waves/round-30/verification/c1-before-0356681.json`
  shows `compared: false` with `mutantRunner.exit: 0` for all eight R-codes
  (R01–R08), which my rows 8, 7, 2, 4, 15, 18, 19, 21 reproduce
  independently.
- A surviving mutant is a coverage finding, not a licence to change the
  contract. The contract as declared already fixes the shape that makes these
  mutants killable: `expected.json` entries may be objects
  `{"id": …, "reason": …}` and the runner compares the sorted multiset of
  `(id, reason)` pairs. When that lands, each of these 23 mutants should be
  killed by a fixture that names its code. Codes that no fixture can reach
  (`empty_path`, `absolute_path_not_allowed`, `path_escapes_root` argument
  form, `corpus_directory_unreadable`, `not_a_regular_file`, `git_unavailable`,
  `git_command_failed`, `root_not_a_directory`, `revision_not_found`,
  `root_not_repository_top_level`) will stay surviving unless the runner
  gains a way to reach them — the sibling scout's gap list.
- Re-measuring the same 23 mutants after the repair lands is the natural
  after value for this ledger.

## Not verified

- I did not run either round-30 counter (`c1_reason_count.py`,
  `c2_quote_truth.py`): the C1 counter needs a landed commit, and running it
  here would grade bytes that are not the target of this seat.
- No network request was made; the vendored MTE schema and metrics library
  were read from the tameshi tarballs already on disk, not fetched.
- The MTE HTML consumer was not exercised (out of scope; the schema and the
  official metrics are the interop surface this seat needed).
- The after value (post-repair kills) is not measured here; the repair is
  still being built by sibling seats.
