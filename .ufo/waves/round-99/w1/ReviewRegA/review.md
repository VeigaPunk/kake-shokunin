# ReviewRegA — C1 row-review conjunct (round 99, repair commit 9d341d1b)

## Scope and trees
- Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. Lane `master` read with `git rev-parse master` -> 7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916 (later than the repair; see Tip check).
- Judged revision: 9d341d1b46f16dbfbb41af75dd6d4966808dfa5d (the C1 repair commit).
- Read-only extraction: `git -C LANE archive 9d341d1b... | tar -x -C <scratch>/tree` (no LANE write).
- Scratch clone: `git clone --shared -q LANE <scratch>/fx`; `git -C fx checkout -q --detach 9d341d1b...` rc=0; `git -C fx rev-parse --show-toplevel` = fx path (asserted); HEAD = 9d341d1b (asserted).
- Diff of the repair: `git -C LANE diff ab35eace... 9d341d1b... -- SKILL.md` rc=0; section `## Round 99 — tool registry completion` at SKILL.md:1700+; 26 rows parsed by splitting on unescaped `|` (rows-extracted.json, 26 rows, 7 cells each, owner all `kake`).
- Row set equals the 26 tools in scripts/ that the counter lists as unlisted at base (cde408e5). rows-not-on-disk = [].

## Method per row
1. Kind: docstring head of scripts/<tool> (first 5 lines) compared with the Kind cell.
2. Entry command: each flag named in the cell grepped in the source (add_argument / argv parsing); the stdin or argv form exercised with probes (probes.json). Failing forms are recorded as observed rc.
3. Verdict map: each exit path grepped (sys.exit / return N / process.exit / ap.error / SystemExit) and read at the cited line; observed rc for usage and bad-input probes.
4. Self-test: the command in the cell run in the clone at the repair rev with TMPDIR set to a per-row scratch dir, cwd = clone, timeout 900 (selftest-rc.tsv; outputs under scratch, not kept). Placeholders (`<dir>`, `<path>`, `--work <dir>`) replaced with scratch paths. Tallies quoted in cells checked against stdout/stderr.
5. Write scope: grep for file/dir/tempfile writes (open 'w', write_text, mkdir, makedirs, mkstemp, mkdtemp, os.replace, unlink, rmtree) and the stated destinations read at the cited lines.

Verdict rule applied: a cell is `false` when the code or an observed rc contradicts it. Cells that are incomplete within the stated location (a file written in the named directory but not named) are recorded as notes under `agree`.

## Commands and rc (summary; full list in selftest-rc.tsv and probes.json)
- Counter (orientation only, not scored here): `python3 -B .ufo/waves/round-99/c99_registry.py --root <fx> --revision 9d341d1b... --work <scratch>/c1work` -> rc=0, stdout `tools=54 rows=152 listed=54 unlisted=0 dangling=0 exec_fail=1 mismatches=0 met=true`; `exec_fail 1104 scripts/robots_audit.py rc=2` (line 1104 is an older robots-expectation-audit row, not a repair row). Full output: c1-counter-stdout.txt.
- Counter selftest, not run here (out of assignment).
- Self-tests of the 26 rows: 18 ran and returned rc=0 (base_path_selftest, citing_set --selftest, citing_set_selftest --selftest, citing_set_hostile_selftest, conditional_eval --selftest, header_change_class --selftest, knowledge_metatext_lint --selftest, landed_check --selftest, ledger_latest_check --selftest, link_preview_selftest, quote_class --selftest, robots_audit_selftest, sidecar_reobserve --selftest, sitemap_audit_selftest --tool, source_recheck_hardening_selftest, source_recheck_selftest, stale_extensions --selftest, and robots_audit's self-test command). 8 rows have cell `no self-test` and were not run (cache_key, cache_key_conformance, live_snapshot, probe-delta.mjs, response_snapshot, reval_exchange, source_snapshot, wave_seat_record); for each, grep found no selftest mode in the file.
- Digests: `sha256sum` of each committed blob at ab35eace equals instrument-sha256.txt (11/11 OK).
- Probes (probes.json): usage and bad-input forms with observed rc, for example: quote_class.py no args rc=2; quote_class.py classify ... --json rc=2; wave_seat_record.py no args rc=2; wave_seat_record.py results missing rc=2, happy path rc=0; header_change_class.py no args rc=64; landed_check.py no args rc=64; live_snapshot.py no args rc=64; response_snapshot.py --bogus rc=64; robots_audit.py no args rc=64; citing_set.py no args rc=64; citing_set.py missing population rc=2; cache_key.py empty/bad stdin rc=1; conditional_eval/reval/stale with [], 1, null, "x", {}, duplicate keys rc=1 with invalid_input and no traceback; probe-delta --bogus rc=64, --since bad rc=64, --hole-hours 0 rc=64, empty file rc=2, nonexistent file rc=2, one valid row rc=0; knowledge_metatext_lint nonexistent root rc=2, repo rc=0; ledger_latest_check --root clone rc=0; sidecar_reobserve --check rc=0 wrote=false; sitemap_audit_selftest --fault-injection rc=0, --map rc=0; robots_audit_selftest/source_recheck_selftest/source_recheck_hardening --list rc=0; cache_key.py valid payload with vary as a string rc=0.

## Row verdicts
See verdicts.tsv: 24 agree, 2 disagree.
- quote_class.py disagree: Entry `classify ... [--json]` rc=2 observed (quote_class.py:112 defines --json on top-level only); Verdict `64 usage` false: ap.error exits 2 (:142), `return 64` (:143) unreachable; observed rc=2.
- wave_seat_record.py disagree: Verdict `64 usage` false: no 64 return; argparse error exits 2 (:45), observed rc=2.

## Tip check
- SKILL.md at master still has the `## Round 99 — tool registry completion` heading once and 26 table rows (awk count). Tip differs from the repair commit in 6 files (`git diff --stat 9d341d1b... master`: 414 insertions). Tip rows were not re-judged; the freeze says the C1 score is at the repair commit.

## Observations routed (not repaired)
1. SKILL.md:1104 (robots-expectation-audit row, older, not a repair row): its self-test cell `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` carries literal bracket tokens; the counter reports exec_fail rc=2 for it. The counter still prints met=true because the repair row for scripts/robots_audit.py passes (listed set is any-row). Routed to L1: the freeze control 'exec_fail -> met=false' holds only when no row for the tool passes.
2. The counter does not check Entry flags; the quote_class.py `--json` defect passes the counter (met=true at 9d341d1b). This is the declared limit that the review conjunct covers.
3. Frozen instrument digests: instrument-sha256.txt is committed in ab35eace (freeze), not in 2345e309; all 11 listed blobs match at ab35eace.
