# SimplifierBuild

Revision read: `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show`). The working tree is byte-identical to it for every file below (`git status --porcelain <paths>` prints nothing), except `make_spec_w2.py`, which does not exist at that revision and was read at HEAD `51921b9` (it emits the tracked `w2-spec.json`). All experiments ran on copies under `/tmp`; the originals were not edited. No tool installs (vulture 2.16 preinstalled, no pacman).

CANDIDATES:

- `c57_quote_truth.py:59` — `from datetime import datetime, timezone`; `timezone` has zero uses (vulture, 90% confidence). Verdict: DELETE. Evidence: `confirmed by running` — selftest 101/101 with the import narrowed.
- `c57_quote_truth.py:81` + `:324` + `:540` + `:546-548` — the held-row machinery: `PRIOR_USED_BY: dict = {}` is never mutated; `PRIOR_USED_BY.get(sid, [])` and `if sid in PRIOR_USED_BY ...` are therefore unreachable. Round 56 carried `{"S367": [NOFOLLOW]}` (`c56_quote_truth.py:81`), so this is the derive script's blanked remnant. Deleting it cascades: `mlines = row_lines(...)` becomes unused, hence `row_lines()` (`:142-155`) too. Verdict: DELETE constant, both branch sites, and `row_lines`. Evidence: `confirmed by running` — 101/101 after; real run identical (below).
- `c57_quote_truth.py:366` + `:371` — `all_texts = dict(texts)` is a pure alias. In round 56 it held extra bodies scanned from `SOURCES_DIR` (`c56_quote_truth.py:356-363`); the wave-1 derive deleted that block but kept the alias. Verdict: DELETE alias, read `texts` directly. Evidence: `confirmed by running` — 101/101 after.
- `c57_quote_truth.py:307-315` — C3 held-row branch (`else: base = base_rows.get(sid); ... row[:10] != base[:10]`). `ADOPTED` keys equal `NEW_ROWS` (`S421`,`S422`), so every iteration takes the new-row arm; the comparison arm is unreachable. Verdict: DELETE the arm, keep `if sid in base_rows: already in base`. Evidence: [INFERENCE] for unreachability (static: the two constants); `confirmed by running` for neutrality — 101/101 and identical real run.
- `c57_quote_truth.py:362` — `if sid in NEW_ROWS and row and len(row) > 5:`; the first conjunct is always true for the same reason. Verdict: DELETE the conjunct. Evidence: `confirmed by running`.
- `c57_receipt_pins.py:394` — `r1 = sb.commit(...)`; the return value is never read (vulture, 60%). Verdict: DELETE the assignment, keep the call. Evidence: `confirmed by running` — 48/48 after.
- `c57_receipt_pins.py:392` + `:431` — `honest(extra_files=...)` is accepted and merged (`files.update(extra_files or {})`) but no `scenario(...)` call passes it. Verdict: DELETE parameter and merge line. Evidence: `confirmed by running` — 48/48 after.
- `scripts/id_resolver.py:50-56,73,240` — `Result.registry` is assigned in `__init__`, filled with `{}` by `_err`, and set by `evaluate`, but has zero readers (`grep -n "\.registry"` returns only the assignment; selftests read `cited`, never `registry`). Verdict: DELETE slot, constructor parameter, and the two constructor arguments. Evidence: `confirmed by running` — selftest 33/33; real run at the build revision identical.
- `derive_c57_quote_truth.py:131` — `sub('"schema": "kake-r56-c2-quote-truth-v2"', ...) if ... in body else None`. The pinned BASE blob carries `kake-r56-c2-quote-truth-v1`, so the condition is false and the call never executes (`git show BASE:.ufo/waves/round-56/c56_quote_truth.py | grep -c 'kake-r56-c2-quote-truth-v2'` = 0). Verdict: DELETE. Evidence: `confirmed by running` — deletion, then full derive pipeline reproduces `4b8c730:...c57_quote_truth.py` byte-for-byte.
- `derive_c57_quote_truth.py:213` — `body.replace('"schema": "kake-r57-c2-quote-truth-v1"', '"schema": "kake-r57-c3-quote-truth-v2"')` can never match: at that point `main()` still says `kake-r56-...`; the name becomes `kake-r57-...` only in the blanket rename at `:226`. Stage-1 output already carries `kake-r57-c2-quote-truth-v1` (checked). Verdict: DELETE. Evidence: `confirmed by running` — pipeline output identical to the built file.
- `c57_idresolver_gate.py`, `derive_c57_selftest.py`, `make_spec_w1.py`, `make_spec_w2.py` — no dead code found: vulture (min-confidence 0) flags only the `_`-named fixture functions (registered by decorator side effect) and no unused variable/import; every `def` has a reference. Verdict: no change.

VERIFIED DELETIONS (all deletions for a file applied together to a scratch copy; originals untouched):

| artifact | selftest before | selftest after | real-run check |
|---|---|---|---|
| `c57_quote_truth.py` (import, held-row block, `row_lines`, `all_texts`, C3 arm, C5 guard) | 101/101 | 101/101 | `--root . --revision 4b8c730...` exit 0, `C3 quote-truth 8/8 met=True`, stdout byte-identical (`diff`) |
| `c57_receipt_pins.py` (`r1`, `extra_files`) | 48/48 | 48/48 | `--root . --revision 4b8c730...` exit 1, `met=False`, stdout byte-identical |
| `scripts/id_resolver.py` (`Result.registry`) | 33/33 | 33/33 | `--root . --revision 4b8c730... --fleet <fleet>` exit 0, `ids_cited=106 ids_resolved=106 dangling=0`, stdout identical |
| `derive_c57_quote_truth.py:131,213` | n/a | n/a | `derive_c57_quote_truth.py` + `derive_c57_selftest.py` in a scratch dir → `diff` against `git show 4b8c730:...c57_quote_truth.py` = identical |

Baseline runs were made against the unmodified files in the lane before the copies were edited; `python3 -m py_compile` on every mutant copy passes, and vulture on the mutated `c57_quote_truth.py` is clean afterwards.

KEEP LIST (looks removable, is load-bearing):

- `derive_c57_quote_truth.py:93,98,170-171` — the `HELD_BODY_SHA256` strings are match/insertion anchors for the round-56 source text and for the v1→v2 replacement chain. Removing them breaks `sub(...)` assertions; with them the pipeline reproduces the built counter byte-for-byte (`confirmed by running`).
- `derive_c57_quote_truth.py:84-116` — the v1 `ARTICLE_START`/`content_window` insertions are overwritten by the v2 block, but they are the `body.index()` anchors the v2 edits locate; collapsing them means re-anchoring the v2 block, not deleting text.
- Cross-file `git`/`blob`/`show`/`parse_registry` helpers (`scripts/id_resolver.py:65-81`, `c57_receipt_pins.py:83-91`, `c57_quote_truth.py:127-147`, `c57_idresolver_gate.py:78-114`) — each file is a frozen standalone artifact that a receipt/gate runs from its own revision; the gate's `reference()` is a deliberate independent oracle against the shipped tool, so sharing code would destroy the oracle.
- `c57_quote_truth.py` selftest (95 cases, 89 kill-matrix rows, `unit_checks`) — the suite itself rejects untabled/orphaned fixtures; every case is a killed mutant class (including the v2 attacks). Not scaffolding to trim.
- `c57_receipt_pins.py:367,497,529-538` — round-56 receipt paths are the fixture population for rename/relabel/deletion scenarios, not stale scratch.
- `scripts/id_resolver.py` `Result.cited` — read by five selftest cases; only `registry` was dead.
- `c57_quote_truth.py` `set_used_by()` — after the C8 restore branch is deleted it is still used by selftest fixtures; keep.
- `make_spec_w1.py` / `make_spec_w2.py` — one-shot generators, but both reproduce the tracked `w1-spec.json` / `w2-spec.json` byte-for-byte in a scratch copy (`confirmed by running`). The `GODSPEED` constant duplicates the first line of `CONTEXT` in each prompt; it is artifact redundancy already dispatched, not dead code, and changing it would change tracked spec bytes.

VERDICT: 10 dead spots found in 4 files; deleting them keeps 101/101, 48/48, 33/33 and the derive/real-run outputs byte-identical.
