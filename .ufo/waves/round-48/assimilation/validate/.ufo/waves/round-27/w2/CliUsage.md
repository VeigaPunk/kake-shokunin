# Kake r27 — W2 falsification lane: CLI usage (operability)

Seat: `KakeR27.CliUsage` (leaf, read-only). Axis: operability. Milestone: r27-fresh-falsification.

## Authority read (frozen)
- Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; working tree identical for the measured source
  (`git diff ac46a74 -- scripts/` empty; `scripts/citing_set.py` blob `352a471abec08daa5…`, sha256
  `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`; selftest sha256 `3c167895c7f3a4ac…`).
- Contract `.ufo/waves/round-27/contract.json` → `gateInterface` (CLI, output schema, exits 0/1/2/64); also read
  `oracle-implementation-corrections.json`, `frozen-candidate.json`.
- No source edit, commit, registry/MANIFEST/state write; scratch only under `/fast/scratch/hyaku/kake-r27/cliusage/`
  (TMPDIR exported; no /tmp, no /dev/shm).

## Method (independent, expected-before-run)
Expectations were written to disk **before** any probe ran, then executed verbatim; no runner rewrites an expectation:
`expectations.json` (55 probes), `expectations2.json` (10), `expectations3.json` (2), plus a 10-case adversarial batch
declared inline in the runner source. Gate invoked as `python3 -B scripts/citing_set.py …` from the candidate root.
**77 probes, 0 Python tracebacks.** Exit codes observed: 0/1/2/64 exactly as documented for every non-defective case
(A01–A13, A15–A17, C01, C03–C08, D01–D14, E01/E02/E04/E05, F02–F04, F06, F07, F09, G02, H01–H10).
`--selftest` delegation reaches the sibling runner: 29 cases, 0 failed, exit 0 (E05).

## Findings by severity

**F1 — HIGH — a non-regular input document blocks the gate forever (no output, no timeout).**
`WorkingTreeSource.read_document` (scripts/citing_set.py:205-215) opens the population/ledger path with `open(…,"rb")`
and only catches `OSError`; it never checks that the path is a regular file. Corpus entries *are* checked
(`_walk` → `not_a_regular_file`, scripts/citing_set.py:238-259); the two input documents are not.
- F01 `--population <fifo>` → no stdout, no stderr, still running after 15 s (killed by timeout).
- G01 `--ledger <fifo>` → identical, killed after 12 s.
No JSON, no exit code, no diagnostic: violates “documented JSON + exit 64 or 2”; a CI wrapper that passes a substituted
path can hang the wave. Fix direction: `os.lstat` + `stat.S_ISREG` before opening (reuse the corpus rule) →
`input_invalid`/`not_a_regular_file`, exit 2.

**F2 — HIGH — repeated valued options are silently resolved by last-path-wins (never a usage error).**
`build_parser` (scripts/citing_set.py:575-586) uses plain argparse, so `store` options keep the last value; the lane
target requires “never … last-path-wins”. The contract is silent here, so this is a contract gap and a live fail-open,
because the discarded value can be the broken one:
- B01 `--population does-not-exist.json --population population.json` → **exit 0, verdict clean** — the unreadable path is
  dropped without a word; the gate certifies inputs it never opened.
- B02 reversed order → exit 2 (only the last value is read); B04 repeated `--ledger` → exit 2; F10 repeated
  `--population` → exit 2.
- B06 `--revision no-such-revision --revision HEAD` → **exit 0, clean**, `source:"git"` at HEAD: invalid revision discarded.
- B08 `--root /nonexistent-root-xyz --root <real>` → **exit 0, clean**. B05 (bad revision last) → exit 2, B07 → exit 2,
  B03 (same value twice) → exit 0 (accepted).
Fix direction: reject any repeated option with exit 64 + the documented usage JSON.

**F3 — MEDIUM-HIGH — an empty `--revision` silently degrades the pinned measurement to working-tree mode.**
`main` selects the source with the truthiness test `if arguments.revision:` (scripts/citing_set.py:650), so `""` is
treated as “not supplied”, while the adjacent blank `"   "` is an error (`GitSource._resolve` strips →
`revision_not_found`, exit 2, scripts/citing_set.py:272-283) — inconsistent handling of two adjacent blanks.
- C02 `--revision ""` → **exit 0, verdict clean, `source:"working-tree"`, `revision:null`** (measured the working tree).
- F08 `--revision=` (equals form) → identical.
The JSON discloses `source`/`revision`, but exit code and verdict do not distinguish it: a caller pinning a revision
through a variable that expands empty gets an unpinned “clean”. Fix direction: option present but empty →
`InputInvalid(revision_not_found)` → exit 2.

**F4 — MEDIUM — an absent corpus tree is certified as `clean` (exit 0, citingPairs 0).**
`WorkingTreeSource.corpus_files` returns `[]` when `corpus/knowledge` does not exist (scripts/citing_set.py:217-236);
`GitSource.corpus_files` returns `[]` when the path is absent at the revision (`git ls-tree` exits 0 with no output,
scripts/citing_set.py:303-321) — no diagnostic either way.
- C09 `--revision <commit with no corpus/knowledge>` → **exit 0, clean, citingPairs 0, corpusFiles 0**; F05 working tree
  without `corpus/knowledge` → **exit 0, clean, citingPairs 0**.
A pinned measurement over a revision where the corpus was deleted/not yet added is a false green; only `corpusFiles:0`
hints at it. Fix direction: absent corpus tree → `input_invalid` (exit 2), or a distinct “no corpus” verdict.

**F5 — LOW — `--help` emits no JSON and exits 0.** E03 → exit 0, stdout is argparse help text (`json.loads` →
JSONDecodeError). The docstring states “The JSON document is written to stdout in every mode”
(scripts/citing_set.py:75-77) and the contract maps exit 0 to `clean`; a consumer parsing stdout as JSON crashes on the
one invocation that cannot be parsed.

**F6 — LOW — undocumented option spellings are accepted (argparse prefix matching).** A14 `--popu population.json` →
accepted as `--population`, exit 0, clean, while A13 `--r` was correctly rejected as ambiguous: inconsistent near-misses.

**F7 — LOW — contradictory option sets are silently resolved.** E06 `--selftest --root <repo> --population
does-not-exist.json` → exit 0, selftest ran, the contradictory `--population` dropped (sibling uses `parse_known_args`,
scripts/citing_set_selftest.py:71). A18 `--root <scratch> --population … --ledger … --selftest` → `--root` silently
overridden by the selftest delegation, exit 2 with the sibling’s JSON reporting `root:"…/scratch"`, `cases:0`. The
modes are mutually exclusive but nothing says so.

**F8 — INFO — usage-error payload diverges from the documented schema.** The exit-64 payload adds an undocumented
`"error"` key and reports `verdict:"could-not-evaluate"` while exiting 64 (A01: `"error":"usage: missing required
option(s): --root, --population, --ledger"` + stderr line). The documented mapping is verdict→exit (2 =
could-not-evaluate), so a consumer mapping verdict to exit mis-handles usage errors; D03 `--population ""` is diagnosed
as “missing required option(s): --population” rather than an empty-path error (exit 64 — inside the lane’s 64-or-2 set).

## Contract vs optional strictness
- **Contract-required (contract.json → gateInterface), violated:** the “JSON document … in every mode” sentence (F5).
  The gateInterface’s silence about repeated/empty options is why F2/F3/F4 are *undetected* rather than *unforbidden*; a
  silent last-path-wins measurement is a false green for the C2 red condition, so I grade F2/F3/F4 contract-grade.
- **Optional strictness (not required by the frozen contract; recommended, each a clean cutover):** reject repeated options
  (F2), abbreviated spellings (F6), contradictory mode mixes (F7); treat an empty revision as a bad revision (F3);
  require a non-empty corpus tree (F4); check regularity of the input documents (F1). Each needs a contract line.

## Residual risk / verification gaps
- I exercised the gate only as a subprocess of the frozen candidate; no mutation seat was run by me (read-only seat).
- The 29 fixture expectations were observed passing (E05: 29/29, exit 0) but their semantics belong to other seats.
- `scripts/__pycache__/citing_set.cpython-314.pyc` (mtime 2026-10-21 19:03:01) appeared during my run; this seat never
  imported the module (always `python3 -B <script>`), so it is a sibling’s artifact — left untouched.
- Probes used synthetic roots under my scratch dir; the frozen oracle’s population/ledger
  (`.ufo/waves/round-27/frozen/expected.json`) was not re-run here.
