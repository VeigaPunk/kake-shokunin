# ExecC1Tool2

Claim C1, **second independent implementation** of `scripts/receipt_lineage.py`, built from
`contract.md` § Claim C1 only. No coordination with the first implementation; no counter
touched; no after-state scored.

Retained artifact (my deliverable):
`.ufo/waves/round-61/w1/ExecC1Tool2.files/receipt_lineage.py` — 871 lines, stdlib only,
`sha256 3144246aa9f6a94a660f38591262424f7bfa2a7199d76ab70076c855c7313c6a`.

Path collision, stated plainly: I wrote my implementation to `scripts/receipt_lineage.py`
first and ran it there (selftest 23/23); at 06:18:36Z the peer seat's independent
implementation (1040 lines, its own selftest 68/68) replaced that path. I did not overwrite
it back — two seats racing on one path is not a decision a leaf may make, and the seat item
asks for an artifact to *compare*, so mine is retained under `.files/` and the choice of
which lands at the lane path is the L1's.

## DESIGN:

- **CLI** — `--root --revision [--disclosures] [--json]` and `--selftest`; exits 0 clean,
  1 findings, 2 could-not-evaluate, 64 usage (argparse `error()` overridden to 64). Findings
  one per line `<kind> <path> <commit>`, then
  `receipts=<n> events=<k> undisclosed=<m> met=<bool>`; `--json` carries the same numbers plus
  `population_source`, `population_by_rule`, `receipt_grammar_members`, `members_missing`,
  `disclosures`, `notes`.
- **Read-only / committed bytes only** — `git rev-parse` (toplevel + `--verify --end-of-options
  REV^{commit}`), `git rev-list --first-parent --reverse`, `git ls-tree -r -z --full-tree`,
  `git cat-file`. The worktree is never read; the only file opened is the disclosure registry,
  which is a CLI path, not a revision-scoped blob. `git_env()` rebuilds the environment with
  every `GIT_*` key removed, then sets `GIT_OPTIONAL_LOCKS=0`, `GIT_TERMINAL_PROMPT=0`,
  `LC_ALL=C` (proved by S18: `GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY` poisoned to
  `/nonexistent/*`, run still clean).
- **Population** — `(?i)^(?:.*/)?control(?:s)?/(?:.*/)?[^/]+\.(?:txt|json)$` over regular
  blobs only (`mode in {100644,100755}`; a symlink is a blob with mode 120000, so the mode is
  checked and a symlink/submodule population path is skipped with a `note:` on stderr).
  Measured: at base `9f07731a` the rule selects **exactly the 144 frozen paths**; at
  `eaa9177e` it selects **146** = the 144 + `.ufo/waves/round-61/controls/census-before.txt`
  + `.ufo/waves/round-61/controls/population-144.txt`.
- **Frozen list** — when a `\.ufo/waves/round-<N>/controls/population-<n>\.txt` blob is
  committed at the revision, the walk is bounded by that list (highest round, then highest
  count); rule-only extras get a stderr `note:` (`population_rule_extra ...`) and are *not*
  walked. Rationale: contract R2 freezes `receipts=144`, which is the frozen-list size; the
  path rule alone gives 146 at any revision past `eaa9177`. Member drift
  (`member_changed`/`member_missing`/`extra_member`) stays counter-level, as the contract
  says, and `members_missing` is reported for information.
- **`receipts=`** — population members examined (not grammar matches). Base and `eaa9177e`:
  `receipts=144`; grammar-matching members at those revisions: 95.
- **Rules implemented verbatim**: receipt grammar `(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:`
  on the **first committed version**; result-span regex copied character for character;
  event candidate = different blob than the commit's first parent, after the first-added
  commit, through the revision under test; a path absent at a commit and present again is a
  new lineage (the re-add is a first-added commit, like a rename's new path).
- **Event classification** — one kind per commit: `pending_filled` when the first version's
  span contains `(?i)\bpending\b` and this is the earliest later version whose span does
  not; every other span-differing candidate is `rewrite`. A fill commit is therefore *not*
  also an `undisclosed_rewrite` (contract L7 expects exactly one finding).
- **Disclosure** — entries matched on equal `path` and `commit`; a hex commit of ≥7 chars also
  matches as a prefix, so a 40-hex registry and an abbreviated registry both work. Missing
  registry file = empty registry. Malformed JSON, non-object top level, non-list `entries`,
  non-string `path`/`commit`, or a `schema` that is present and not
  `kake-receipt-disclosures-v1` → exit 2.
- **`met` = `undisclosed == 0`** (frozen definition). Exit code follows findings, so a
  `phantom_disclosure` alone exits 1 while printing `met=True` — see LIMITS.
- **Performance** — the (path × chain) blob matrix goes through one `git cat-file
  --batch-check` process (372 commits × 144 paths); a real-lane run takes ~1.0 s.

## SELFTEST:

`TMPDIR=… python3 -B …/receipt_lineage.py --selftest` → **23/23 PASS, exit 0**
(`.files/selftest.txt`). Every fixture is a fresh `git init` under `$TMPDIR`, toplevel
verified, committed only with `-c user.name=selftest -c user.email=selftest@local`; the tool
runs as a black box through its CLI, so exit codes and env handling are exercised, not
internals. Cases map onto the frozen counter table:

| case | counter case | asserts |
|---|---|---|
| S01 clean untouched | L1 | 0 findings, `receipts=1` |
| S02 revision relabel | L2 | 1 `undisclosed_rewrite` at that commit, `met=False`, exit 1 |
| S03 same, disclosed | L3 | 0 findings, `undisclosed=0`, exit 0 |
| S04 non-result body line | L4 | 0 findings |
| S05 non-receipt member | L5 | 0 findings |
| S06 `met=False`→`met=True` | L6 | 1 `undisclosed_rewrite` |
| S07 `EXIT=pending`→filled | L7 | 1 `undisclosed_pending_filled` (exactly one finding) |
| S08 same, disclosed | L8 | 0 findings |
| S09 two rewrites, one disclosed | L9 | 1 `undisclosed_rewrite` (the second) |
| S10 rewrite after the tested rev | L14 | 0 findings |
| S11 empty population | L16 | `receipts=0 events=0`, exit 0 |
| S12 malformed registry | L12 | exit 2 |
| S13 registry entry with no event | L13 | 1 `phantom_disclosure`, exit 1 |
| S14 unresolved revision | L15 | exit 2 |
| S15 root = subdirectory; S16 missing `--root` | `--root` rule / usage | exit 2 / exit 64 |
| S17 symlink population path | non-blob note | `skipped_non_blob` note, 0 findings |
| S18 poisoned `GIT_*` | env scrub | clean run, `receipts=1` |
| S19 frozen list bounds walk | L11 shape | `receipts=1`, `population_rule_extra` note, extra rewrite not walked |
| S20 same input twice | determinism | byte-identical stdout and exit |
| S21 delete then re-add | first-added rule | 0 findings (re-add = new lineage) |
| S22 `--json` | report shape | `receipts=1`, `met=True`, resolved `revision` |
| S23 default registry path | CLI default | registry found at the lane root with `cwd=/` |

Real-lane evidence (`.files/real-lane.txt`, `.files/events-empty-registry.txt`), instrument
runs only — no counter was run, no after-state scored:

- `--revision 9f07731a…` (base) → `receipts=144 events=12`; empty registry → 12
  `undisclosed_rewrite`, exit 1.
- `--revision eaa9177e…` (contract commit) → same 12 events; stderr
  `note: population_rule_extra …census-before.txt`, `…population-144.txt`.
- The 12 events are real, spot-checked by hand: e.g. `.ufo/waves/round-56/controls/after-c1-selftally.txt`
  at `ad06cb8` shows `-  revision: f8438a28…` / `+  revision: 4cb225fb…` (the r56 relabel of
  the contract's motivation); `.ufo/waves/round-52/control/c1-ledger-real.txt` at `a4a890c`
  likewise; `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` at `20217f2` gains its
  whole `met=True` result line in a later commit.
- The r57 case is classified `rewrite`, not `pending_filled`: its first version's result span
  carries no literal `pending` (the receipt was committed empty of results), so the frozen
  `pending_filled` rule does not fire on it. `[INFERENCE]` a round that commits the word
  `pending` inside a result line would be the first true `pending_filled` in this history.
- **Cross-seat corroboration**: `.ufo/receipt-disclosures.json` exists in the lane (written by
  another seat at 06:19Z, still untracked) with exactly 12 entries; its (path, commit) set is
  identical to my 12 events (set equality checked), so a run with the default registry gives
  `receipts=144 events=12 undisclosed=0 met=True`, exit 0 — contract R2's shape is reachable
  once the L1 commits that registry.

## LIMITS:

- **`receipts=` is the one reading where the two implementations disagree, and it decides R2.**
  Mine: 144 (population members; matches the frozen string `receipts=144` at base *and* past
  `eaa9177`, via the frozen list). Peer tool at `eaa9177`: `receipts=95` (grammar matches).
  A third reading (path rule only) gives 146. The L1 must pick before the counter freezes R2
  (`.files/differential.txt`).
- **Explicit `--disclosures` that does not exist**: mine treats it as an empty registry
  (contract names only *malformed* → exit 2); the peer tool exits 2
  (`not found at the revision or on disk`). Fixtures L3/L8/L13 pass registries that exist, so
  neither behaviour is exercised there, but the choice is visible in `--json`/exit codes.
- **`phantom_disclosure` exits 1 while `met` stays `True`**, because `met` is frozen as
  `undisclosed == 0`. If the counter asserts `exit == met` this case (L13) diverges.
- Text is decoded `utf-8` with `errors="replace"`; population paths containing whitespace,
  `:`, NUL or a newline are not walked (`note:`), an inexpressible `cat-file` spec.
- Version comparison is within a presence run: a delete/re-add starts a fresh receipt test,
  and a *rename* ends the lineage (no rename following, per contract).
- A new population file outside the frozen list is not walked (stderr note): `extra_member`
  is the counter's, per the contract.
- Not tested here, by scope: disclosed-note prose truth (reviewer), whether the population
  regex misses a receipt shape the lane never used (scout), symlinks/submodules beyond S17,
  and any behaviour at a revision past the wave (no after-state exists yet). Nothing was
  built, linted or formatted in the lane; no `git add/commit/checkout/stash/reset` and no jj
  call was made in the lane; no pacman transaction and no install was needed.
- Scratch `/fast/scratch/hyaku/kake-r61/ExecC1Tool2/` was deleted after the cited evidence was
  copied into `.files/`.

VERDICT: Independent C1 tool implemented, retained and green (23/23 selftest; 144 receipts, 12 real rewrite events at base and at eaa9177; disclosed run exit 0, undisclosed=0, met=True); the decisive divergence is `receipts=` (144 population vs 95 grammar vs 146 rule) plus missing-registry exit 2 vs empty — the L1 must freeze one reading before the counter is frozen.
