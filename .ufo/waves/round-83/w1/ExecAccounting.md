# ExecAccounting — round 83 wave w1

Scope executed: `.ufo/waves/round-83/make_accounting_v2.py` (new; round-82's `make_accounting.py`
untouched), plus receipts under `.ufo/waves/round-83/w1/ExecAccounting/`. No other lane file was
written; `git status --porcelain` shows the new tool and my own report/receipt paths only.

## Deliverable

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/make_accounting_v2.py`, 420 lines,
sha256 `14ddd368661769ceacb53f0ac52c5240415dee3b2567e7aaf4f164c1190093f3`, stdlib only (no installs;
pacman untouched).

Record keys emitted: `schema` (`kake-wave-accounting/v2`), `supersedes`, `lane`, `round`, `wave`,
`attack_roles`, `substantive_floor_bytes`, `bytes_basis` (`"utf-8"`), `requested`,
`requested_attack`, `requested_share`, `settled`, `settled_names` (sorted), `settled_attack`,
`settled_share`, `substantive`, `substantive_names`, `substantive_attack`, `substantive_share`,
`empty_output`, `seats` (`name`, `role`, `output_bytes` per results row), `rows_skipped`,
`spec_sha256`, `results_sha256`. Every v1 key is retained, so the diff below isolates the additions.

Derivation rules are byte-identical to the frozen C1 counter `c83_defect_queue.derive_population`:
`output_bytes = len(output.encode("utf-8"))` (never `len(output)`); settled = bytes > 0;
substantive = bytes >= 200; role comes from the spec item, an unmatched name is role `""`; shares
are `round(k/n, 4)` with an empty population yielding `0.0`; nameless/non-object rows are skipped and
counted in `rows_skipped`.

## Proof 1 — round-82 reproduction

`python3 -B .ufo/waves/round-83/make_accounting_v2.py --spec .ufo/waves/round-82/w1-spec.json
--results .ufo/waves/round-82/w1-results.json --out <receipt>/round82-accounting-v2.json` → exit 0,
stdout `requested=13 requested_attack=4 requested_share=0.3077 / settled=7 settled_attack=0
settled_share=0.0 settled_bytes=43152 / substantive=6 substantive_attack=0 substantive_share=0.0`.
Those are the committed `w1-accounting.json` values: 7 settled, attack settled `0/7`, share `0.0`,
substantive 6, sha256s `5a6e5b12…`/`08a020c6…` equal.

## Proof 2 — record diff (`round82-record-diff.txt`, exit 0)

20 shared keys: 18 identical (15 scalars plus the equal lists `attack_roles`, `substantive_names`,
`empty_output`), 1 order-only, 1 changed; 4 additive; 0 removed. Every assertion printed `True`.

- additive: `bytes_basis="utf-8"`, `seats` (13 rows), `rows_skipped=0`, `supersedes`.
- order-only: `settled_names` — same seven names, v2 sorts them as the seat spec requires.
- changed: `schema` `v1 -> v2`, the declared format marker; it is the only non-additive difference.
- per-seat bytes were independently re-derived from `w1-results.json` and match: ScoutRecon 4899,
  ScoutSources 7902, ExecCapture 92, ExecRegistry 0, ExecDelta 0, ScribeLesson82 6402,
  ScribeKnowledge 6669, ScribeRecord 3813, ReviewC1 0, ReviewC2 0, CriticClaims 0, MutC 0,
  ConnectorC 13375 (sum 43152). Note `ExecCapture` is 92 chars but 92 bytes; the non-ASCII rows
  (e.g. ScribeRecord +2) already show code-point counting would under-report.

## Proof 3 — selftest (`selftest-work.txt`, `selftest-tmpdir.txt`)

`--selftest --work /fast/scratch/hyaku/kake-r83/ExecAccounting/selftest` → exit 0,
`selftest: 13/13 passed`; the work dir is empty afterwards (the tool removes the `mkdtemp` subdir it
created). `TMPDIR=/fast/scratch/hyaku/kake-r83/ExecAccounting/tmpdir … --selftest` → exit 0, 13/13,
and `ls -A` on that TMPDIR prints 0 entries. Checks: empty row unsettled; 199-byte row settled but
not substantive; 200-byte row substantive (boundary); 150×`é` counted as 300 bytes, not 150 chars;
attack share 1/3 → 0.3333 and requested 2/4 → 0.5; `settled_names` sorted from reversed input;
`seats` one row per results row with the spec roles and `bytes_basis`/sha keys present; missing
results → exit 2 with no output file; malformed JSON → exit 2; `writes-only-out` (fixture dir holds
exactly `spec.json`, `results.json`, `accounting.json`); two runs byte-identical; missing flags →
64; `--help` → 0.

## Proof 4 — the frozen C1 counter accepts the record (`c1-counter-compat.txt`, exit 0)

Imported `c83_defect_queue.py` read-only and ran it on a scratch tree containing a v2-written
`w1-accounting.json`: `derive_population` equals my record field-for-field (settled 3, sorted names,
settled_attack 2, share 0.6667, identical `seats`), and `item_d1 -> (True, …)` / `item_d2 ->
(True, 'mismatched=[] log=yes')`. Negative controls on the same tree: `output_bytes + 1` → D2 False
(`mismatched=['Rev']`), dropped `bytes_basis` → D2 False, `settled_share=0.1` → D1 False,
`settled=2` → D1 False. The green path is therefore not vacuous, and C1's D1/D2 conjuncts can be
re-derived from this tool's output unchanged.

## Operational notes

`.ufo/waves/round-83/w1-results.json` does not exist while this wave is in flight (probe: exit 2,
`round83-missing-results.txt`), so no round-83 accounting record was fabricated. When the results
file lands, D1/D2 need exactly:
`python3 -B .ufo/waves/round-83/make_accounting_v2.py --spec .ufo/waves/round-83/w1-spec.json
--results .ufo/waves/round-83/w1-results.json --out .ufo/waves/round-83/w1-accounting.json`.
The round-83 roster must itself carry >= 2 settled attack seats and share >= 0.25 for D1 to pass;
the tool reports that population, it cannot manufacture it.

One incident handled: my first compatibility run imported the counter without `-B` and Python wrote
`.ufo/waves/round-83/__pycache__/c83_defect_queue.cpython-314.pyc`; I deleted the directory and
subsequent runs used `-B`. `find .ufo/waves/round-83 -name '__pycache__' -o -name '*.pyc'` is now
empty. Scratch `/fast/scratch/hyaku/kake-r83/ExecAccounting/` is removed after copying receipts
(verified absent).

## Verdict

Complete. `make_accounting_v2.py` re-derives the committed round-82 accounting exactly (settled 7,
settled_attack 0/7, share 0.0) while adding UTF-8 per-seat bytes and `bytes_basis`; the record diff
shows additive keys plus the declared schema bump and a sorted `settled_names`; `--selftest` is green
13/13 under both `--work` and `TMPDIR`; the frozen C1 counter's D1/D2 evaluators accept the emitted
record and reject doctored ones.
