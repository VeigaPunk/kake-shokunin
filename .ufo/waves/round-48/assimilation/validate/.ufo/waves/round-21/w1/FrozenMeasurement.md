# FrozenMeasurement — round-21 wave-1 report

## Files changed (scoped writes only, no commits)

| File | Status |
|---|---|
| `.ufo/waves/round-21/measure.mjs` | new, executable |
| `.ufo/waves/round-21/replay-proof.mjs` | new, executable |

No other files touched; no tree mutations; no commits. No test/lint/verification
runs performed per lane bounds (parent wrapup: no runs; L1 executes before/after).

## measure.mjs — independent frozen measurer
- **C1 (provenance trio):** each of `source:`, `verified-at:`, `recheck:`
  matched by `/^<field>:[ \t]*\S/` — exact lowercase, case-sensitive —
  against the **first 8 lines** of every `corpus/knowledge/*.md`; prose
  `Source:` in legacy entries does not count (FieldSemantics fix applied:
  legacy `Source:` prose would otherwise inflate complete count above the
  declared 4/21 baseline). 21 expected; list embedded, mirroring
  `.ufo/waves/round-21/initial.json` (baseline 5009ecaa).
- **C2 (lane lesson gates):** exact population regex
  `/^round-\d+(?:-recensus)?\.md$/` (excludes `round-1-aggregator-audit`,
  `round-20-verifier-spotcheck`, `round-8-aggregator-box3-coldrun`, etc.),
  gate regex is the **exact line** `/^## Gate$/m` per parent correction —
  `## Gate — round-20 resume` does NOT satisfy it (round-20 still passes via
  its bare `## Gate` at line 41).
- **Denominators:** legacy lesson population fixed at 15. A fresh working
  tree enumerates 16 (`corpus/lessons/round-21.md` exists in this tree);
  `population.lessons.found` reports 16 while `expected` stays 15 and the
  extra is listed under `population.lessons.extra`. Extras are evaluated
  like members — their own missing gates still fail — but a complete extra
  never fails the run (per parent: do not fail merely due to round-21).
  `populationDeviation` is informational, not an exit driver.
- **Modes:** default working-tree reads (`readdirSync`/`readFileSync`);
  `--revision <commit-ish>` resolves via `git rev-parse --verify
  <ish>^{commit}`, enumerates via `git ls-tree -r --name-only`, reads via
  `git show <sha>:<path>` — argv-form `execFileSync` only, no shell, no pipes.
  `--root` override supported; `DEFAULT_ROOT` is `../../..` from the script
  (parent correction applied — `.ufo/waves/round-21` → repo root).
- **JSON output:** `source.mode`/`revision`, `criteria` (exact regexes),
  `semantics` note (missing metadata = absent provenance record, NOT absent
  live verification; no domain reads performed), `population` per set with
  expected/found/absent/extra, per-file rows listing each missing field or
  `## Gate`, flat `missing` strings `file: item`, `errors`, `exitCode`.
- **Exit:** 0 complete · 1 any missing field/gate/absent expected file ·
  2 read errors (unreadable file/dir, unresolvable revision, git failure) ·
  64 usage. Usage header documents all of the above.

## replay-proof.mjs — digest-first frozen replay

- Verifies all 36 SHA-256 digests in
  `.ufo/waves/round-21/frozen/before/expected.json` **before** any execution;
  any mismatch/unreadable member → `REPLAY_PROOF: snapshot_tampered`, exit 2,
  gate never runs.
- Runs `node scripts/corpus-contract.mjs --root <frozen> --json` **twice**
  on the unchanged snapshot; asserts both exits equal `expected_exit` (1)
  and both stdouts are byte-identical (stable ID set, no ordering drift).
- Extracts `missing_metadata*`/`missing_gate*` IDs from raw stdout;
  asserts: metadata IDs cover `knowledge − metadata_complete` = 17 files,
  gate IDs exactly `lessons − gates_complete` = 14 and one per un-gated
  lesson, every extracted `corpus/...` path inside the frozen populations
  (`corpus/knowledge/*`, `corpus/lessons/round-\d+(?:-recensus)?.md`).
  Gate stdout must parse as JSON (contract violation otherwise).
- Re-verifies all 36 digests **after** execution — proves the unchanged
  snapshot ran and was not mutated by gate or proof.
- Exit: 0 PASS · 1 FAIL (contract assertions) · 2 could_not_evaluate /
  snapshot_tampered. Same convention as `.ufo/round-20/replay-proof.mjs`.

## Evidence retained

- Population oracle = `initial.json` lists embedded verbatim (21 knowledge,
  15 legacy lessons); `expected.json` observed: knowledge=21,
  metadata_complete=4, lessons=15, gates_complete=1, expected_exit=1,
  revision=5009ecaa1cce10b895617a585ddd3f7c7c923a84.
- Working tree currently shows `round-21.md` present in `corpus/lessons/`
  (observed via directory listing) → found=16 path is exercised, not
  hypothesized.
- `corpus/lessons/round-20.md:41` has exact `## Gate`; `:182` `## Gate —
  round-20 resume` correctly rejected by `/^## Gate$/m`.

## Risks / blockers

- `scripts/corpus-contract.mjs` is a sibling deliverable (MetadataCheck) and
  was absent at write time — replay-proof exits 2 `could_not_evaluate` with
  a clear message until it lands; ID-count assertions assume IDs embed
  `corpus/...` paths (they must, to name missing members).
- `measure.mjs` exit-2 aggregates any unreadable member; spec wording
  "each missing field/gate" satisfied via per-file `missing` arrays.
- Not run, per operator wrapup — syntax/behavior unverified by execution;
  L1 before/after run is the first execution.
- No tool installs performed.
