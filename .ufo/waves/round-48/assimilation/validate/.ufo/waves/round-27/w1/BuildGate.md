# BuildGate — round-27 C2 citing-set completeness gate (operability)

Seat: KakeR27.BuildGate (executor, axis: operability, milestone: r27-full-citing-set).

## Changed path (exact, single file)

- `/fast/scratch/hyaku/kake-r27/writer-gate/scripts/citing_set.py` (new, 694 lines, mode 755)
- Worktree: `/fast/scratch/hyaku/kake-r27/writer-gate`, branch `kake-r27-gate`, HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (observed base; worktree clean before this edit).
- **Not committed** (L1 integrates). No other source file, no fixture, no selftest runner, no corpus/ledger file, no manifest/state/index/jj/Git mutation was made.

## Interface implemented (from `.ufo/waves/round-27/contract.json` → `gateInterface`)

```
python3 -B scripts/citing_set.py --root <dir> [--revision <commit>] \
    --population <relative-json> --ledger <relative-json> [--json]
python3 -B scripts/citing_set.py --selftest [extra args]
```

- stdout is always the JSON document `{"verdict","citingPairs","ledgerPairs","findings",...}`; `--json` is accepted as a no-op so a runner that omits it still gets machine-readable output.
- `--root` resolves every input; the run is cwd-independent. `--population` / `--ledger` must be relative paths that resolve inside `--root` (absolute paths, `..` escapes and symlinks pointing outside the root are rejected as `input_invalid`).
- `--revision` resolves the revision to one commit object once (`rev-parse --verify <rev>^{commit}`) and then reads blobs (`git show`, `git ls-tree`); without it, working-tree files are read. No network, no execution of corpus content, no writes outside the process.
- `--selftest` delegates to the sibling `scripts/citing_set_selftest.py` (resolved next to the gate itself) with an explicit `--root` (the user's `--root`, else the gate's repo root) and cwd=root; a user-supplied `--root` is stripped from the forwarded flags so it is never duplicated; if the sibling rejects `--root` the delegation is retried once without it. Missing sibling → `could-not-evaluate`, exit 2.
- Exit codes: 0 clean, 1 failed, 2 could-not-evaluate, 64 usage. Usage errors emit the JSON document on stdout plus a one-line stderr message and exit 64; **no Python traceback is ever printed** for invalid input.

## Implementation decisions

1. **Citation token**: `S` + ≥3 ASCII digits, delimited by non-word characters (`(?<!\w)S([0-9]{3,})(?!\w)`). Consequently `S024S025` inside `w2/UncoveredS024S025.md` is *not* a citation — it is part of a longer word. Whole-file text is scanned, so front-matter `source:` / `verified-at:` metadata lines and the round-26 EOF prose are in scope exactly like in-body citations.
2. **Range**: two ids joined by hyphen-minus, en dash U+2013, em dash U+2014, `..`, `to` or `through`; any whitespace (newlines included) may surround the separator and the separator may abut the digits; the left endpoint needs only a word boundary before its `S`, the right endpoint a word boundary after its digits. Ranges are scanned by an independent regex, literals by the standalone-token rule. A valid range expands inclusively. **Descending** (`end < start`) or **span > 200** → one `citation_range_invalid` finding; the range is *not* expanded and its endpoints stay literal citations when they are standalone tokens. The evaluation still completes, so this finding yields `failed` / exit 1 (it is a corpus defect the gate reports, not an unusable input). `input_invalid` is reserved for unusable inputs and forces `could-not-evaluate` / exit 2.
3. **Population**: only ids present in the population document are part of the citing set. Ids are compared numerically when they look like `S<digits>` (`S001` == `S0001`), otherwise as exact text. Ids cited outside the population are counted in the extra key `outsidePopulation` and never become findings.
4. **Ledger comparison**: a citing pair is adjudicated when the ledger contains the same (row-key, file). A ledger pair not in the citing set → `ledger_pair_not_cited` (this also covers a ledger row outside the population and a ledger file that cites nothing). A ledger pair occurring more than once → **one** `ledger_duplicate_pair` finding carrying `occurrences`; a repeated pair still counts as adjudicated, so it produces no `unadjudicated_citing_pair`.
5. **Finding multiplicity**: one finding per distinct object — one `unadjudicated_citing_pair` per distinct (row, file) of the expanded citing set. Findings are emitted sorted by (id, row, file) for deterministic output.
6. **Symlink / non-regular policy** (per the L1 instruction): `corpus/knowledge` itself may not be a symlink; no knowledge file may be a symlink; any non-regular entry (fifo, socket, device) is rejected. Both cases are `input_invalid` → exit 2. A *missing* `corpus/knowledge` directory is not an error (nothing to read → empty citing set); a wrong root is still caught by the ledger side (`ledger_pair_not_cited`).
7. **Independence**: the scanner is a hand-written token walk (delimiter matching, separator table, explicit range expansion), not a reuse of the frozen oracle's regex pair in `.ufo/waves/round-27/count_c1.py`; the frozen oracle was read as the claim to satisfy, not copied.
8. **Extra JSON keys** (beyond the four required): `populationRows`, `corpusFiles`, `outsidePopulation`, `source` (`working-tree`|`git`), `revision` (null in working-tree mode). The frozen harness `c2_count.py` reads only `findings`, so extras are inert for it.

## Evidence (observed) and expectations (inference)

Observed, read-only, before implementation:

- `.ufo/waves/round-27/c2-oracle.json`: `expectedCount: 16`, `expectedExit: 1`, `expectedFinding: "unadjudicated_citing_pair"`, `falsePositives: 0`, and 16 explicit (row, file) pairs (S001–S006 grouped pairs in `static-canonical-preflight.md`, `sitemap-orphan-audit.md`, `publish-channels.md`; S008 in four files; S022/S023 in `static-canonical-preflight.md`).
- `.ufo/waves/round-27/frozen/expected.json`: pins 25 `corpus/knowledge` files + `population.json` + `ledger.json` by sha256, exit 1, finding `unadjudicated_citing_pair`, count 16; `c2_count.py` materialises exactly that snapshot into a temp dir and runs the gate **without** `--revision` (so the working-tree source is the measured path), then requires `run.returncode == 1`, the (row, file) set to equal the oracle's, and `len(findings) == 16`.
- `frozen/ledger.json` pairs (41) are byte-identical in membership to `.ufo/waves/round-26/statements.json` `pairs` (41) — the r26 ledger is what the gate is measured against.
- Running the **frozen C1 counter** (`count_c1.py --root . --revision 83528f7…`, a read-only oracle already in the tree, not my gate) reports at that base: `citingPairs 57`, `decided 41`, `missing 16`, and those 16 are exactly the oracle's `expectedPairs`. That fixes the target the gate must hit: 57 expanded pairs, 41 adjudicated, 16 unadjudicated, zero false positives.
- Corpus range forms actually present (grep over `corpus/knowledge/*.md`): `S001-S007`, `S001-S006`, `S020-S027`, `S028-S029`, `S001–S006` (en dash). No `..`, `to` or `through` form and no descending/over-wide range exists in the corpus, so `citation_range_invalid` cannot fire on the frozen snapshot.

Inference, **not executed**: with the rule set above the gate should report `citingPairs: 57`, `ledgerPairs: 41`, 16 `unadjudicated_citing_pair` findings, no `ledger_pair_not_cited` / `ledger_duplicate_pair` / `citation_range_invalid`, `verdict: "failed"`, exit 1 — i.e. the frozen oracle's expectation. This is derived from the frozen counter's own numbers and the corpus text, not from a run of my code.

## Not run (deliberate)

Per the L1 instruction "no checks mid-flight" and the wave bound "writers only author, L1 runs after integration", **I did not execute the new gate, did not run the fixture runner or the selftest, and did not run any build/lint/formatter**. The gate is therefore *unexecuted*: its behaviour above is a derivation, not a measurement. No tool was installed or updated in this seat (no pacman/uv/cargo/npm action; nothing was needed).

## Risks / blockers for L1

- **Unmeasured implementation risk**: a first execution may surface a defect (the file was reviewed line by line but never run). The L1 should run, in order: (1) `python3 -B scripts/citing_set.py --root <tmp> --population population.json --ledger ledger.json --json` against the frozen snapshot copy (`c2_count.py` does this) — expect exit 1 and exactly 16 `unadjudicated_citing_pair` findings matching `c2-oracle.json`; (2) the fixture runner (`scripts/fixtures/citing-set/*`) — expect ≥12 cases, nonzero on mismatch; (3) `python3 -B scripts/citing_set.py --selftest` — expects the sibling runner to exist and to accept `--root`.
- **Convention coupling** (not an interface change): exit 1 vs 2 for `citation_range_invalid`, and "one finding per distinct object" multiplicity, are my reading of the contract. Both were communicated to `KakeR27.BuildSelftest` and `KakeR27.BuildFixtures` so their `expected.json` encodes the same rules; if either seat reads the contract differently, the gate must change (the CLI interface stays fixed).
- **Field naming**: findings carry `row` (population id) and `file` (corpus-relative path); `input_invalid` findings carry `reason`/`scope`/`path` instead of `row`/`file`.

## Interface alignment with the sibling seats (observed, same wave)

- `KakeR27.BuildSelftest` (selftest runner writer) confirmed the invocation, the JSON report shape and the exit+id-multiset comparison need **no change** on their side; my `--selftest` delegation (`--root <repo-root>`, cwd=repo-root, stdout/stderr forwarded, child exit code returned) was confirmed compatible. I declined their optional per-case `pairs` field so the frozen fixture interface (`expected.json {exit, findings:[ids]}`) stays as contracted; the (row, file) pinning of the 16 oracle pairs is done by the frozen harness `c2_count.py` itself.
- `KakeR27.BuildFixtures` (fixture producer) confirmed the five semantics they queried: `input_invalid` → exit 2; an invalid range is **not expanded** while its endpoints stay literal citations; the standalone-token rule; the six separators; the recursive `corpus/knowledge` scan set; and the population intersection (a cited id outside the population is never a citing pair and never a finding). Multiplicity and the `row`/`file` field semantics were sent to both seats and are recorded in the gate docstring.
- Resolved (no blocker): the selftest runner derives its own defaults from its own location — root = `<repo>/` (the gate's parent directory), gate = `<root>/scripts/citing_set.py`, fixtures = `<root>/scripts/fixtures/citing-set`. My delegation passes exactly that `--root` with cwd=repo-root, so no `--fixtures`/`--gate` argument is needed; their stdout is one JSON summary object (`kake-citing-set-selftest-v1`) forwarded verbatim, stderr empty, their exit code (0 matched / 1 mismatch / 2 could-not-evaluate) becomes the gate's.

## Pre-integration correction (L1 instruction, same file, no checks run)

L1 instruction: the frozen RANGE grammar (contract + `count_c1.py`) allows `\s*` around the separator (newlines included) and `to`/`through` without mandatory surrounding spaces (`S001toS006`); my hand lexer only skipped space/tab and required token word-boundaries there; align the range scanner with the declared grammar, keep the literal regex, the range scanner may be an independent regex, do not change the frozen oracle, report the exact delta.

Exact delta (only `scripts/citing_set.py` touched; `count_c1.py`, the contract and every oracle file are untouched):

- **Added** `_RANGE_RE = re.compile(r"\bS([0-9]{3,})\s*(?:-|–|—|\.\.|through|to)\s*S([0-9]{3,})\b")`.
- **Replaced** the hand-written range lexer (the `match_separator` helper and the token-driven range detection inside `scan_text`) with one independent regex pass: `scan_text` now runs two independent `finditer` scans — literals via the unchanged `_TOKEN_RE`, ranges via `_RANGE_RE`.
- **Deleted** the now-dead `is_word_char`, `match_separator`, `_DASHES`, `_WORD_SEPARATORS`.
- **Behavioural effect**: (a) any whitespace, newlines included, is allowed around the separator; (b) `to`/`through` may abut the digits, so `S001toS006` is a range; (c) the left endpoint of a range needs only a word boundary before its `S` (not a standalone token), so in `S001toS006` the endpoints are *not* literal tokens — the range alone supplies them. (d) unchanged: the literal token rule, the population intersection, expansion/validation (descending or span>200 → `citation_range_invalid`, not expanded), every finding id, every exit code, and the whole CLI interface.
- **Equivalence to the frozen grammar**: same separator set, same `\s*`, same trailing word boundary on the right endpoint, same greedy digits, same left-to-right non-overlapping match order. The only textual differences from the frozen regex are `[0-9]` instead of Unicode `\d` (immaterial for this ASCII corpus and consistent with my literal rule) and the order of the `through`/`to` alternatives (equivalent — `"th"` never matches `"to"`).
- **Effect on the frozen measurement (inference, nothing executed)**: the corpus range forms are `S001-S007`, `S001-S006`, `S020-S027`, `S028-S029`, `S001–S006` — all recognised identically by the old lexer and the new regex — so `citingPairs` stays 57, `ledgerPairs` stays 41, the 16 unadjudicated pairs stay 16, and no `citation_range_invalid` is produced.
- **No tests, no fixtures, no selftest, no execution** were performed after the change, per the L1 instruction.

Peer notification: `KakeR27.BuildFixtures` and `KakeR27.BuildSelftest` were told that the range grammar now admits newline-spanning and digit-abutting separators, and that a glued form such as `S001toS006` yields the range expansion without literal endpoint pairs — fixture `expected.json` files must encode that.

## Boundary semantics (raised by `KakeR27.BuildFixtures`, answered as implemented)

- **Range with an endpoint outside the population**: the range is still validated. Descending (`end < start`) or span > 200 emits `citation_range_invalid` (exit 1) whatever the population contains — validation is a property of the range text. Such a range is not expanded and contributes no pairs. A *valid* range expands over its whole numeric span and every interior id that **is** in the population becomes a pair; endpoints outside the population contribute nothing. Example: population `{S092}` + corpus `S090-S095` → one pair `(S092, file)`; population `{S092}` + corpus `S090-S995` → `citation_range_invalid` only, no pairs (span 905 > 200, nothing expanded).
- **Numeric id comparison**: ids are compared numerically, so `S001`, `S0001` and `S00001` are one row id and `S1234` is its own. If one population lists two spellings of one id they collapse to one comparable id: the citing set holds one pair for it, reported under the first id in `population.rows`; a ledger pair spelled `S0001` for the same file matches the `S001` pair (same id), and a ledger listing both spellings for one file yields **one** `ledger_duplicate_pair` (the same row adjudicated twice), not two. 4+ digit ids are ordinary row ids; literal tokens need `S` + ≥3 ASCII digits, so `S1234` is a literal and `S123-S1240` is a range whose interior ids match numerically.
- Disclosure: the frozen counter formats an id as `S%03d` before intersecting the population, so it would not match a non-canonical population spelling such as `S0001`. My gate keeps such a row citable (denominator never shrinks silently). The frozen 32-row population uses canonical 3-digit ids only, so this difference cannot change the 16-pair measurement.
- Fixture producer's case set is unaffected by this correction; both seats confirmed alignment (their `expected.json` files encode the corrected range grammar: glued `S001toS006`, separator across a line break, em dash, `..`, `to`, `through`, descending, span>200). Their set reached **29** self-contained cases, of which three pin the boundary semantics above and were checked against my implementation line by line: 27-range-endpoint-outside-population (one interior-row pair), 28-ledger-row-numeric-spelling (clean exit 0 via numeric identity), 29-ledger-pair-two-numeric-spellings (one `ledger_duplicate_pair`, pair still adjudicated, exit 1).

## Scope statement

Only `scripts/citing_set.py` was written. No corpus, ledger, population, oracle, manifest, registry or state file was touched; no sibling seat's file was modified; no commit, push or deployment was performed.
