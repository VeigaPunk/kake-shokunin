# MutCounters — round 99, w1 (mutation test of both frozen counters)

Seat: `MutCounters` (leaf, no subagents). Lane root `kake-shokunin`, read tip `master` = 7f5b1b7b.
Round base `cde408e5`, instruments `2345e309`, freeze `ab35eace`, C1 repair `9d341d1b`.
Deliverables: `w1/MutCounters/mutants.tsv`, `w1/MutCounters/survivors.md`, copies of the harness and results in `w1/MutCounters/`.

## Evidence

- Frozen digests: `sha256sum -c controls/instrument-sha256.txt` in the lane root, rc 0, all 11 entries OK
  (c99_registry.py, c99_fresh304.py, fresh304-contract.md, frozen/*.py). Read-only.
- Pristine reproduction: `harness.py repro` against a scratch clone (`git clone --shared`) with fixture
  commits (`git commit` with fixture identity) rebuilt exactly as `controls.sh` builds them. Every
  committed receipt reproduced: the registry selftest (20/20), pos, namesonly, fenced, falseselftest,
  junkprose, wrongowner, base-c1 (rc 1, unlisted=26); the fresh304 selftest, base-c2, pos-oracle and all seven negatives.
  Output: `REPRO ALL MATCH`. The counters were not modified; no lane git mutation; no commit in LANE.
- Mutants: 52 single-point string mutants (29 registry, 23 fresh304) generated in scratch by exact-string
  replacement asserting one occurrence each, each `ast.parse`d. Specs and line numbers are in `mutants.tsv`.
  Mutants were not written into the lane.
- Kill rule: a mutant is killed when, against its own `--selftest` or the committed control commands, the
  return code, the `met=` token, or a selftest case status changes. Detail-only changes are not kills.

## Results

- registry: **12/29** killed on the disk-safe rerun (selftest rc flips RG02, RG08, RG10, RG12–RG17, RG20–RG22).
  Confirmed survivors: 10 (RG01, RG03–RG07, RG09, RG11 equivalent, RG18, RG19). NOT-RUN: 7 (RG23–RG29).
- fresh304: **13/23** credible kills. 12 are reference-drift kills (rc 0->2, selftest), FR04–FR12, FR17, FR18, FR23,
  plus FR13 (neg-copyall rc 1->0). These came from the pre-fault batch and the resumed batch, not from a disk-safe
  rerun; the rc 2 signature cannot come from the disk-fault traceback (rc 1). Survived: 6 (FR15, FR16, FR19 equivalent,
  FR20, FR21, FR22). NOT-RUN/unverified: 4 (FR01, FR02, FR03, FR14).
- Separation probes (outside the control set, recorded as recipes in `survivors.md`): every survivor with a
  non-equivalent mutation has a verified separating fixture, including FR15 and FR16 (met flips).

Final verdict, as the seat spec requires: `MUT registry=12/29 fresh304=13/23`

## Incidents and corrections (affect how the numbers may be read)

1. `/fast` filled to 100 % host-wide (`ENOSPC`). My runs extract the full revision archive per
   `score()` call, which made my footprint transient but real. I removed the scratch clone's working tree
   (kept `.git`; the counters read only `git archive`/`ls-tree`) and ran with 2 workers.
2. Batch-1 kills that show an empty stdout and `met=None` (RG18, RG19, RG23, RG27, FR01–FR03) are disk-fault
   artefacts. Verified: RG23's falseselftest rerun is byte-identical to pristine, and RG18/RG19 survived on rerun.
   All registry kills were re-run in the disk-safe pass, except RG23–RG29, which are NOT-RUN. FR14's batch-1 kill is
   impossible for that mutation and is recorded as unverified.
3. The scratch fresh304 FR records were removed by my filter before the rerun; the FR verdicts above come from the
   batch output I printed (pre-fault FR04–FR14, resumed FR15–FR23). This is why they are labelled "credible", not "confirmed".
4. Stopped the staged batch when the L1 directive arrived ("stop launching new mutant runs"). Unrun mutants are marked NOT-RUN.

## Findings to route (counter behaviour, not repaired here)

- F1 (registry, exit-code contract): an uncaught `OSError` from `--work` (ENOSPC) gives a traceback and rc 1,
  identical in exit code to `met=false`. The counter only maps `RuntimeError` to rc 2. A fault can read as a verdict.
- F2 (registry, coverage): no committed control exercises `\|` inside a code span, a `No self-test` capitalisation,
  a `--x=path` entry, a `.mjs` population or dangling token, a `selftest` header alias, or a `\|`-escaped trailing cell.
  Survivors RG03–RG07, RG09, RG18, RG19 show these gaps; recipes are in `survivors.md`.
- F3 (fresh304, coverage): the hand table and grammar never use `!` in opaque tags, U+00FF, a lone `"`, a NUL in a
  header value, a refusal with stdout, or a judge rc 1 with a correct decision. FR01–FR03, FR20–FR22 survive/are unverified.
- F4 (fresh304, generator): the no-bad-cases mutant still emits 20/240 refusals through ambiguous ties (FR15), so
  refusal coverage is partly grammar-driven rather than from the kind-0..6 bad cases. Seed derivation (FR16) is not
  verdict-visible on the committed candidates.

## Tooling and footprint

- No tools installed. Python 3.14 from `/usr/lib/python3.14` was used as installed. pacman was not touched.
- Writes: scratch `/fast/scratch/hyaku/kake-r99/MutCounters/` (own seat dir); deliverables under this w1 tree.
  The Report trailer path is `w1/MutCounters.md`, which sits directly in `w1/`, not in `w1/MutCounters/`; I wrote it there as the trailer requires.
- Lane: no mutating git or jj commands. Read-only operations: `git show`, `rev-parse`, `ls-tree`, `archive`,
  `clone --shared` (a new scratch repository).
- Scratch seat directory removed at yield (after copying receipts into `w1/MutCounters/`).

MUT registry=12/29 fresh304=13/23
