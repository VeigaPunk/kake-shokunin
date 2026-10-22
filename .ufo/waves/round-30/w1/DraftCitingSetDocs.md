# DraftCitingSetDocs — C1 support: reason-code registry and fixture format drafts

Seat: `KakeR30.DraftCitingSetDocs` (leaf, docs only). Lane HEAD read at `4580c78cca1185d059efa6970722bbcf2f9c1b0f`.
Deliverable draft: `/fast/scratch/hyaku/kake-r30/w1/DraftCitingSetDocs/docs.md`
(sha256 `4bf658c3d5bc4d686d1b2488d7e7bac795efece5a541ece77ad7f24beb4a5375`).
No lane file was edited except this report; no live request was made; no tool was installed.

## What I built

`docs.md` holds four parts:

- **Part A** — paste-ready `SKILL.md` addition: a new subsection "Citing-set reason-code registry —
  round 30" with a table of all 25 reason codes the gate can emit after C1 (23 today plus
  `document_duplicate_key` and `document_nonfinite_number`), each with its finding id, exit/verdict and
  fixture case (`30-…` to `37-…` for the eight round-28 codes, `38-document-duplicate-key`,
  `39-document-nonfinite-number`), with codes that have no fixture marked "no fixture (uncovered)"; plus
  the fixture-format block (legacy string entries versus object entries `{"id","reason"}`, one form per
  case, sorted multiset of `(id, reason)` compared exactly, exit comparison unchanged) and the round-30
  counter command. A.2 offers the optional amendment to the existing `citing-set` row (`SKILL.md:616`).
- **Part B** — two conditional rewrites of `corpus/QUALITY.md:396-401` "Status of the first bullet
  today": B.1 for a 14/14 counter result, B.2 for a shortfall, plus the wording rules (no claim of gate
  correctness, no claim of coverage beyond the named fixtures, counter exit 2 is a broken measurement).
- **Part C** — the reason codes still without a fixture, split into codes a committed case can produce
  with the runner as it stands, and codes that need a runner extension.
- **Part D** — four decisions for the L1 (case 38-40 numbering, per-case `argv`/`setup` in the runner,
  which counts to print, whether fixtures 13/14 are upgraded to the object form).

## Reason codes still without a fixture (after cases 30-40), 17 of 25

Assertable now, uncovered: `document_shape_invalid`, `document_not_utf8`, `corpus_file_not_utf8`,
`symlink_rejected`, `descending_range`, `span_too_large`.
Not reachable without a runner extension: `corpus_empty`, `revision_not_found`,
`root_not_repository_top_level`, `absolute_path_not_allowed`, `empty_path`, `path_escapes_root`,
`root_not_a_directory`, `not_a_regular_file`, `document_unreadable`, `corpus_directory_unreadable`,
`git_unavailable`, `git_command_failed`.

## Commands I ran (sandbox copy of `scripts/` under `.../DraftCitingSetDocs/before/`)

| Command | Exit | Observed |
|---|---|---|
| `grep -n "InputInvalid(\|reason\"" scripts/citing_set.py` | 0 | 23 distinct reason strings |
| `python3` extraction of those strings (AST-free regex over the file) | 0 | 23 codes listed in Part 0.1 |
| `python3 -B scripts/citing_set.py --root <case> --population population.json --ledger ledger.json --json` (no `corpus/`) | 2 | `corpus_directory_missing` |
| same, `corpus/knowledge` as a regular file | 2 | `not_a_directory` |
| same, malformed `ledger.json` | 2 | `document_not_json` |
| same, `population.json` a directory | 2 | `document_not_regular_file` |
| same, population row id `X001` | 2 | `population_id_unreachable` |
| same, population ids `S01`,`S02` | 0 | verdict clean — F03 gap |
| same, `--population` given twice | 0 | last value used, no usage error — F04 gap |
| same, corpus 1000 levels deep | 1 | `RecursionError` traceback on stderr, empty stdout — F05 gap |
| same, duplicate `"rows"` member | 1 | no duplicate detection — F01 gap |
| same, `"w": NaN` | 1 | no non-finite detection — F02 gap |
| `grep -c O_NOCTTY scripts/citing_set.py` | 0 matches | F06 gap |
| `python3 -B scripts/citing_set.py` on fixture cases `13`, `14`, `15`, `16` | 1, 1, 2, 2 | reasons `descending_range`, `span_too_large`, `document_not_json`, `document_shape_invalid` — asserted as ids only today |

## Findings for the L1 (advisory)

1. **Three of the eight round-28 codes cannot be committed as working fixtures with the runner as it
   stands** (`corpus_empty`, `revision_not_found`, `root_not_repository_top_level`). The runner's argv is
   fixed (`scripts/citing_set_selftest.py:214-221`): no `--revision`, and Git stores no empty directory, so
   an empty `corpus/knowledge` cannot exist in a committed tree. The counter's `fixture` and `compared`
   conditions (`.ufo/waves/round-30/c1_reason_count.py:438-461`) require a working fixture for each of
   R01-R08 and a runner baseline that exits 0, so this is load-bearing. A per-case `argv` plus a
   `setup` that runs on a scratch copy under `--tmpdir` (never in the lane tree) would close 33 and 36;
   case 37 additionally needs a disposable Git repository with the case root nested below its top level,
   because the counter exports `scripts/` with `git archive` into a non-repository tree where any
   `--revision` resolves as `revision_not_found`. I told `KakeR30.ExecRunnerReasonFixtures` this.
2. **Duplicate keys and non-finite numbers are invisible to plain `json.loads`** (observed above:
   exit 1, no detection). The new codes need a pair hook and `parse_constant` at any depth, and the
   non-finite check must run before the shape checks or `document_shape_invalid` wins. I told
   `KakeR30.ExecGateFamilies` this.
3. **Case numbering.** `KakeR30.ExecRunnerReasonFixtures` confirms 30-37 for the eight round-28 codes and
   that 38-40 belong to the gate seat; my draft uses 38 and 39 and leaves 40 free.
4. **Fixture format.** The runner today rejects any non-string entry
   (`scripts/citing_set_selftest.py:181`); the object form needs that check relaxed to "every entry is a
   string or every entry is an object", with a mixed case rejected as a malformed oracle.

## Evidence pointers

`scripts/citing_set.py:113-114,141-156,180-189,226-246,255-270,279-294,323-355,372-382,415-421,428-459,
496,517,529,711` (sha256 `d7e79ba102ff27761d830f95ad91e1970ebfcc942eea9728a0bdf3b0c3479d48`);
`scripts/citing_set_selftest.py:50,167-181,214-221,269-277` (sha256
`3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`);
`.ufo/waves/round-30/c1_reason_count.py:60-88,391-405,434-461` (sha256
`be2a1287ab7f2abdca8695d8274504d14b9e1c6b0afe95e940c890bfb8bcc53e`);
`corpus/QUALITY.md:396-401` (sha256 `2b6a6748732e2b863a967e3e4cd256997a5df28964d80d9f1101916760985684`);
`SKILL.md:616` (sha256 `b43c27cb2668882fc43921be126a85aee58eef266add50b1e229fa285ce55f6e`).

## Not verified

- I did not run the round-30 C1 counter: the gate has no C1 implementation at `4580c78`, so 14/14 is not
  reachable yet, and running it would only reproduce the recorded before receipt.
- I did not apply Part A or Part B to `SKILL.md` or `corpus/QUALITY.md`; the L1 integrates.
- I did not verify the per-case `argv`/`setup` runner extension; it is a proposal, and whether the runner
  may grow a per-case key is the L1's decision.
- I did not test `document_unreadable` and `corpus_directory_unreadable` under a privileged reader: the
  lane runs as a user that bypasses the permission bits, so those two codes stay classified as uncovered.
