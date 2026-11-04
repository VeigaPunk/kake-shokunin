# Round 69 — lessons (kake, attempt 1)

Base `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4` (lane master at round open). Frozen contract
`.ufo/waves/round-69/contract.md` (commit `dbcfef0b`), with its dated Amendment 1 recorded after the W1
attacks and before any after-state measurement. Two claims: C1 calibration (2 → 2, HOLD), C2 operability
(10 → 10, HOLD). Wave shape: W1, one v1 wave of 12 seats (3 attack seats, 25 %), plus the residual
falsifiers named in the report.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 — record/observed drift: a recorded post-value does not re-derive at the revision it names | `LOG.md:2304-2305`, `corpus/lessons/round-67.md:53-54`; pair C1-02 in `.ufo/waves/round-69/c1/pairs.json` (record: 1 at `4b03efe1`; `grep -c 'not adjudicated here\|candidate mechanism'` observes 2). Pre-value 5 at `6ff73edd` (C1-01) re-derives. | none at the round-67 landing; the round-68 spot-check caught it by re-running the command | C1 counter `.ufo/waves/round-69/c69_recorded_counts.py` (frozen 20-pair set; base exit 1 on C1-02; selftest 6/6 includes a wrong-integer row and an id-substring row) plus the QUALITY criterion in `corpus/QUALITY.md` (Round-69 addendum) and the correction row below |
| M2 — a committed receipt reads a `/tmp` path and is not reproducible from committed bytes | `.ufo/waves/round-68/controls/wordcounts-d3-r68.txt`: the quote-truth block ends in a `FileNotFoundError` on `\tmp\q133.txt` (line mid-file; the file continues after it); `grep -c '/tmp'` = 1 | none (round-68 spot-check §7.3 routed it) | re-run against committed bytes at `.ufo/waves/round-69/controls/wordcounts-r68-rerun.txt` (`grep -c '/tmp'` = 0; S133 10 words collapsed-only, S434 full 26 words raw-substring, S434 sub-quote 22 words raw-substring; all three re-derived at `4d188f94`); QUALITY criterion; the original receipt is kept unmodified |

## Corrections

Correction rows for the C1 relabel rule (`c69_recorded_counts.py`, Amendment 1). The counter reads a
line of this file matching `^\|\s*<pair id>\s*\|\s*<re-derived integer>\s*\|`. The record lines it
corrects are not edited (append-only).

| Pair | Re-derived value | Note |
|---|---|---|
| C1-02 | 2 | round-67 record (`LOG.md:2304`, `corpus/lessons/round-67.md:53-54`) says 1 for `grep -c 'not adjudicated here\|candidate mechanism' corpus/knowledge/gate-status-ledger.md` at `4b03efe1`; the command re-derives 2 there (`ScoutC1Pairs.md`, C1-02). The round-68 record already states the later value 1 at `ce2ba654`; the ledger is unchanged. |

## Gate

Candidates considered this round, with decisions:

- **Admit — C1 counter** `c69_recorded_counts.py`: exact-token relabel, frozen pair set, base exit 1, selftest 6/6. Able to fail: the base run is red on C1-02; the selftest cases (e) and (f) are red.
- **Admit — C2 patch and counter** (`scripts/freshness-sweep.mjs`, `c69_tmp_honour.py`): the R15 snapshot default and the selftest default no longer carry a `/tmp` path literal; the selftest default is `os.tmpdir()`. Base: `tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=true`, exit 1.
- **Admit — S436 row** (Node.js `os.tmpdir()`): quote 23 words, class collapsed-only (raw `grep -cF` 0; collapsed 1), sha256 `0d31bf3c…b6245b`, opened 2026-11-03.
- **Admit — S437 row** (Python `tempfile`): quote 19 words, class collapsed-only (raw 0; collapsed 1), sha256 `4a9695c5…9beec`, opened 2026-11-03. The row teaches only the environment knob this span states.
- **Admit — QUALITY criteria M1 and M2** (addendum in `corpus/QUALITY.md`).
- **Reject — S437 named span** ("gettempdir() three environment items as rendered prose"): class absent; the three names sit in three `<li>` items (tag-inclusive span 51 words; rendered prose 24 words raw 0, collapsed 0). Discarded; the deviation from the spec's named span is recorded here, not rescued by a stripped-tag class.
- **Reject — S437 precedence claim** (TMPDIR before TEMP before TMP): the admitted quote does not state an order. The precedence claim rests on S436 alone.
- **Reject — counter reading HOME as TMPDIR** (critic attack C): a fixture under HOME would pass a counter that set both to one directory; the frozen predicate now requires distinct fresh directories and a not-under-HOME check.
- **Reject — scribe correction-table shape** (`| Pair id | Recorded | … | Re-derived |`): the counter reads the re-derived integer in the second cell (ConnW1 finding 1); the rows above use that shape.
- **Reject — `offline_exit=0` in the C2 predicate**: unsatisfiable at base on this host (ReviewerDesign F2; see Known residuals). Replaced by `offline_unchanged` in Amendment 1.
- **Reject — "every count the records attribute"** as a C1 scope: the sentence quantified beyond the frozen set (ReviewerDesign F5). Scope is the 20-pair set.
- **Reject — assimilation this round**: none admitted (see report, Sources & frontier).

Discernment spot-check: seats in this wave are the lane's own (`corpus/LEARNING.md`: a subagent the lane dispatched is still the lane). A lane-side sample of this round's gate decisions gives 3 admits, 2 rejects, with the reasons above. The non-author spot-check is owed to the hyaku closure and is not claimed here.

## Sourced claims

- **C2 rests on S436** (Node.js `os.tmpdir()`, https://nodejs.org/api/os.html, opened 2026-11-03, one GET, HTTP 200, 90,518 bytes, sha256 `0d31bf3c15787b15bcddd8e380dd67c9505d7d47d8892ff4ce69b2ceebb6245b`). Located quote (23 words, collapsed-only): "On non-Windows platforms, TMPDIR, TMP and TEMP environment variables will be checked to override the result of this method, in the described order." Source: `.ufo/waves/round-69/w1/ScoutSources/sources/S436-node-os.html`.
- **S437 supports the knob, not the order** (Python `tempfile`, https://docs.python.org/3/library/tempfile.html, opened 2026-11-03, HTTP 200, 75,198 bytes, sha256 `4a9695c51c513c70dcd4e1bd51ee836b0e5ace45ed95bc9c493b264ca019beec`). Located quote (19 words, collapsed-only): "the user of the application can control the directory location by setting the TMPDIR, TEMP or TMP environment variables."
- **What the sources do not prove.** A documented precedence is not the tool's behaviour. C2's counter tests the tool itself (selftest fixture location under a fresh TMPDIR, against a fresh HOME), not the documentation.

## Frontier

- `corpus/SOURCES.md`: registry 173 → 175 (S436, S437 appended inside `## Registry`; both `mined`; used-by this lesson). Census at base and after: exit 0 (W04 warnings unchanged).
- No new PROVINCE frontier ground. The round touches operability of the lane's own gate.

## Measurements (counting commands; receipts under `.ufo/waves/round-69/`)

- C1: `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root <lane> --revision <rev> --pairs .ufo/waves/round-69/c1/pairs.json`. Base `4d188f94`: `pairs=20 mismatches=1 relabelled=0 unrelabelled=1 met=false`, exit 1.
- C2: `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <dir>`. Base `4d188f94`: `tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=true`, exit 1.

After-state values are in the report (measured at the round tip).

## Known residuals (named, not closed)

- `--offline` is red at base on this Linux host: lowercase `~/projects` citations at `corpus/lessons/round-66-verifier-spotcheck.md:101-102` and `corpus/lessons/round-66.md:69`, unannotated and absent from `pins.pathsMissSet`. The round-67 record's offline exit 0 was host-relative (case-insensitive filesystem). Routed to L0 (`.ufo/l0-questions.md`); not C2's to cure.
- `offline_unchanged` is a no-regression reading, not a green gate. MutC2Base M5 (removing the r15 absent branch) is indistinguishable from the honest fix on this host.
- TMPDIR unset falls back to `os.tmpdir()`, which is `/tmp` on POSIX (S436 names this fallback in its body). The patch takes its default from `os.tmpdir()`; the fallback is documented behaviour, not a literal.
- SKILL.md cites `/tmp/kake-r11`, `/tmp/kake-r12` and a `/tmp/probe-latest.backup.json` procedure step (lines 95, 356, 359). Those are historical or procedure paths outside `scripts/freshness-sweep.mjs`; C2 does not cover them.

## Amendment 1 (recorded in `contract.md`)

Recorded after the W1 attacks and before any after-state. Terms only: the frozen C1 pair set and its relabel rule; `tmp_literals` as quote-adjacent path literals; `offline_unchanged` in place of `offline_exit=0`; distinct fresh TMPDIR and HOME; the M2 wording. The unamended counters' base receipts are kept as history.
