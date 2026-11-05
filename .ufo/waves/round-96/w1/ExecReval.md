# ExecReval — C2 candidate `scripts/reval_exchange.py` (round 96, w1)

## Outcome

Candidate implemented and fully passing against the frozen population by
independent population probe; the frozen in-counter scoring path cannot run
because the counter itself is defective (details + routed defect below).

Verdict line: `EXEC-REVAL met=false rc=1` — met is `false` solely because
the frozen counter's `main()` raises `NameError` before printing a verdict;
the candidate's population verdict is met (hand 37/37, generated 112/112,
forgeries 6/6 refused, positive admitted, mutants 14/14, anti_table ok).

## Candidate file

`scripts/reval_exchange.py` (the single new lane-tree file this seat may
create; sha256 `192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212`,
135 lines). Pure stdin→stdout decision
over supplied values (no network, no clock, no storage): reads one JSON
document (`{"stored": {"exists", "etag", "last_modified"},
"received_status"}`), refuses raw duplicate keys at every nesting level
via `object_pairs_hook`, enforces contract clauses C1–C6 (construct /
cannot-revalidate / update-stored / may-reuse-stored / replace-stored;
when status null; refusal classes: non-object, unknown/missing keys,
non-bool exists, malformed etag per RFC 9110 8.8.3 etagc + obs-text,
negative/non-int last_modified, non-int / out-of-100..599 / 1xx status,
status without validator, validators with exists=false, duplicate keys).
Refusals exit 1 with `invalid_input: <reason>` on stderr; success prints one
decision object and exits 0.

## Frozen-instrument verification

- `c96_reval.py` sha256
  `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9`
  — matches `controls/instrument-sha256.txt` line 3 and the seat spec.
- `c96_selfassess.py` sha256
  `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134`
  — matches line 2.
- No instrument, counter, contract, or population file was edited
  (`git status` shows only the new `scripts/reval_exchange.py` plus
  untracked round-96 `w1/` / dispatch files; counter digest re-verified
  after all runs).

## Receipts (in `.ufo/waves/round-96/w1/ExecReval/`)

- `counter-run.txt` — exact seat-spec scoring command at lane tip
  `049e8eca2f0fa5e981232eb4efe367357dce578c` (freeze commit). The counter
  reports `candidate=absent … met=false` because it resolves the candidate
  via `git show <rev>:scripts/reval_exchange.py` and the freeze commit does
  not carry the (still uncommitted, untracked) candidate — see scratch
  rescoring below.
- `selftest.txt` — `--selftest` run: `selftest 7/7 fixtures scored as
  declared; mutants killed 14/14 survivors=none; anti_table=ok;
  generated-vs-reference seeded cases=37`, rc=0.
- `population-probe.txt` — independent population probe (counter's own
  `score_subject`/`mutant_cases`/`anti_table` functions driven directly,
  replicating `main()`'s scoring with the one missing variable supplied):
  candidate hand=37/37, generated=112/112 (112 = 120 generated minus
  8 reference-refused), forgeries 6/6 refused, positive admitted, mutants
  14/14 killed, anti_table ok. Full per-fixture lines in the file.
- `counter-defect.txt` — scratch-clone rescoring capture: the `NameError`
  traceback (kind, location, exact lines).

## Routed defect (NOT repaired — the counter is frozen)

The frozen counter `c96_reval.py` cannot complete `main()` when the
candidate is present: `mutants` is never assigned in `main()`
(`n_mut = len(load_mutants(...))` at line 561 discards the list; the sole
`mutants = load_mutants(...)` assignment lives in `selftest()` at line
511), yet line 624 passes `mutants` to `mutant_cases(...)`, raising
`NameError: name 'mutants' is not defined`. Any candidate that reaches
that point crashes the counter with rc=1 and a traceback instead of a
`met=true|false` verdict line — so `met=true` is unreachable on the frozen
bytes even for a perfect candidate. Exact case: scratch clone at
`30b2e7430c4a1d2f4f1f1c6a142717de23c5efdc` (tip + committed candidate)
scores hand/generated/forgeries/positive successfully, then dies at line
624 with the NameError. The counterpart `selftest()` path (line 511)
assigns `mutants` correctly and passes 14/14, so the defect is specific
to the `main()` scoring path. Reference decision per `reference()` (lines
97–144): no reference-decision disagreement was found — the defect is in
the counter's wiring, not in any decision. Route: round 97 counter
successor should load the mutant list once in `main()` (same expression
as line 561) before line 624. When the L1 integrates the candidate into a
commit and that one-line fix lands, the counting command should print
`candidate=present … mutants=14/14 … met=true rc=0`.

## Tooling

No tools installed. Scratch tree
`/fast/scratch/hyaku/kake-r96/ExecReval/` (one scratch clone
`lane-clone`, identity `ExecReval@example.invalid`, toplevel verified
before the commit; `--work` dirs `work/`, `work/score/`,
`work/selftest/`, `work/probe*/`) removed after receipts were copied into
`.ufo/waves/round-96/w1/ExecReval/`.
