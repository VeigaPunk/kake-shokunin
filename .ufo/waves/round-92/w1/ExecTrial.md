# ExecTrial — heuristic freshness instrument on recorded domain bytes (round 92 w1)

seat: ExecTrial-6 (executor, leaf)
lane: /home/vgpnk/Projects/shokunin/kake-shokunin
lane head at run: f0b2dc635e34cc1c593655d926af74f19bd21034; freeze a5640ca02c20f94a0fa03af41b977b46ae99808e (verified ancestor)
subject: scripts/heuristic_freshness.py sha256 7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c (22985 B, uncommitted worktree bytes at run time, digest-bound)

VERDICT: trial complete — 18/18 recorded surfaces decided at exit 0, 18/18 match the
frozen contract's decision order derived before the run; no instrument defect observed
on the exercised branches; one coverage finding and one contract-shape finding routed.

## What was run (exact commands, from LANE)

1. `python3 -B .ufo/waves/round-92/w1/ExecTrial/build_inputs.py` → exit 0, `inputs=18`.
   Builds each contract input from the recorded status/headers only (Date,
   Last-Modified, Expires, Cache-Control, Vary when present — never invented),
   HTTP-dates → decimal-integer strings (clause 3+5 adapter convention, cross-checked
   vs GNU date 3/3), `now` = recorded fetchedAt epoch, `shared` omitted.
2. `python3 -B .ufo/waves/round-92/w1/ExecTrial/run_trial.py` → recorder exit 0;
   `outputs/summary.json`: `exit0=18 refused=0 surfaces=18`.
3. `python3 -B .ufo/waves/round-92/w1/ExecTrial/make_table.py` → exit 0,
   `agree=18/18 refused=0` vs the clause-cited derivation in `EXPECTED`,
   authored before any instrument execution (attested; the file's mtime was
   later bumped by a cosmetic post-run edit — Notes.md §5/F2).

First run (my misbuilt inputs, Date as JSON number): all 18 refused, exit 1,
`invalid_input: header name or value is not a string` — clause 3 firing correctly;
rebuilt; retained receipt `outputs/validation-refusal-clause3.txt`.

## Results (full table: w1/ExecTrial/trial.txt)

| Decision | n | Surfaces | Recorded basis |
|---|---|---|---|
| not-storable | 4 | r61 burnerchrome-kimi, ds4cc-kimi, ufo-fsd-kimi-pro, vault-index-kimi | `Cache-Control: no-store` (c9) |
| explicit, lifetime 600, heuristic false | 10 | r61 charter-ghp, ds4cc-primary, lucario-ghp, plazir15-ghp; r81+r82 ds4cc-primary/-robots/-sitemap | `max-age=600` shadows `Expires` (c10) |
| heuristic-undecided | 4 | r61 charter-kimi, lucario-kimi, plazir15-kimi, plazir27-kimi (404) | no explicit freshness; 404 heuristically cacheable; `Last-Modified` absent (c11+c13) |

Population: 12 × round-61/capture + 3 × round-81/capture + 3 × round-82/capture —
all present, none substituted. Per-surface stdin: `w1/ExecTrial/inputs/`; raw
stdout/stderr/rc: `w1/ExecTrial/outputs/`; provenance incl. response.json sha256,
verbatim recorded headers, absent fields, combined field lines:
`w1/ExecTrial/inputs.index.json`.

## What the trial proves / does not prove

Proves: the instrument runs end-to-end on real recorded header sets; on every branch
the corpus exercises its decisions and lifetimes follow the frozen contract
(c2-contract.md v1, clauses 9–13; source decision order skimmed post-run, lines
202–235, and matches); clause-3 type validation fires on real-shaped malformed input.

Does not prove: anything about a live cache or deployed property; that the recorded
headers were correct at capture time; and — **coverage limit** — nothing about the
clause-12 heuristic branch: no recorded surface reaches it (every Last-Modified-bearing
200 also carries max-age=600; every 404 lacks Last-Modified), and the `Expires−Date`
arm never decides (always shadowed; on r81/r82 ds4cc-primary the recorded Expires
precedes Date, −1072 s / −4394 s, moot under shadowing). This trial must not be cited
as clause-12 evidence; that branch is witnessed only by the counter's synthetic cases.

## Findings (routed; no frozen file touched)

- **F1 coverage:** the recorded round-61/81/82 corpus exercises 3 of 5 decisions and
  never clause 12; a future real-byte heuristic witness needs a captured surface with
  `Last-Modified` and no explicit freshness.
- **F2 self-defects, fixed:** (a) first input build used JSON-number dates →
  18/18 clause-3 refusals; builder corrected to decimal-integer strings; both
  facts retained (`outputs/validation-refusal-clause3.txt`). (b) cosmetic
  post-run edit to `make_table.py` destroyed the mtime witness of `EXPECTED`'s
  pre-run authorship; ordering attested narratively (Notes.md §5).
- **F3 contract shape vs HTTP:** 7 of 12 r61 surfaces carry two `Vary:` field lines;
  the contract's JSON header object cannot represent repeated names and clause 1
  refuses duplicates, so the adapter must combine per RFC 9110 §5.2 before the
  contract boundary — the contract nowhere declares this. My combination
  (`Accept-Encoding, Origin`) is recorded per surface in `inputs.index.json`. A
  successor contract should state the combination rule.

## Honest notes

- Instrument uncommitted at run time; the sha256 above is the binding. After the wave
  lands, re-hash against the committed blob before citing.
- `run_trial.py` is a recorder and always exits 0; per-surface exit codes are in
  `outputs/<surface>.rc`.
- `now` is validated but no exercised contract clause consumes it (clauses 9–13 read
  status/headers only); recorded Date-vs-fetchedAt skew up to +2 s passed through.
- No network GET, no tool install, no git mutation, no clone (0 ≤ 1 allowed); scratch
  `/fast/scratch/hyaku/kake-r92/ExecTrial/` removed before yield; nothing cited from
  /tmp or scratch.

## Files written (all inside my seat scope)

`w1/ExecTrial/{trial.txt, Notes.md, trial.env, build_inputs.py, run_trial.py,
make_table.py, seat-inventory.txt, inputs.index.json, inputs/ (18), outputs/
(18×3 + summary.json + validation-refusal-clause3.txt)}` and this report `w1/ExecTrial.md`.
