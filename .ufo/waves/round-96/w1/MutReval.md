# MutReval — round-96 w1 seat report (mutation tester, leaf; no subagent dispatch)

Date: 2026-11-05. Target: prove the frozen 14-mutant revalidation population live and find the clause variants it misses.

## Verdict

**MUT frozen=14/14 new=12 newsurvivors=N05,N06,N07,N08,N11**

## Evidence (each verdict names its command and observed rc)

- Main counting command at wave HEAD `049e8eca2f0fa5e981232eb4efe367357dce578c` (freeze commit): `TMPDIR=<seat scratch> python3 -B .ufo/waves/round-96/c96_reval.py --root . --revision $(git rev-parse HEAD) --work <seat scratch>/reval-main` → `candidate=absent hand=0/37 generated=0/120 forgeries_refused=0/6 positive=refused mutants=0/14 survivors=none anti_table=ok population=ok seed=96 met=false`, `{"detail": "candidate absent"}`, **rc=1**. Line-identical to `controls/base-c2.txt` except the revision field — the candidate `scripts/reval_exchange.py` is absent at HEAD (`git show HEAD:scripts/reval_exchange.py` → rc=128), so the main path scores no subjects; the committed control was reproduced, not re-stamped.
- Counter's own population path: `python3 -B .ufo/waves/round-96/c96_reval.py --work <seat scratch>/reval-selftest --selftest` → `selftest 7/7 fixtures scored as declared; mutants killed 14/14 survivors=none; anti_table=ok; generated-vs-reference seeded cases=37`, **rc=0** — line-identical reproduction of `controls/ctl-c2-selftest.txt`. **The frozen population is live: 14/14 killed, no survivor.**
- Per-mutant receipts via the counter imported as a module (never edited): counter's own `mutant_cases()` under its own SANDBOX, gen_limit=40 (= the counter's mutant rule), plus a full-generated-set pass (seed 96: 120 raw, 112 decided, 8 reference-refused). **Pristine control admitted first (hand=37/37, gen=112/112)**; lane bytes before==after across the whole probe (`w1/MutReval/receipt-pristine-driver.txt`).

## Findings

1. **Frozen 14-mutant population: LIVE** — 14/14 killed under the counter's own scoring, reproduced twice (selftest + per-mutant receipts). No instrument defect surfaced; all five frozen digests match `controls/instrument-sha256.txt` and the frozen round-95 counter `8fd27d62…` is verified present and untouched.
2. **Coverage gaps → survivor recipes (route to the C2 population owner for the successor round; not implemented here):**
   - **N05** `etag: ""` accepted — recipe: hand case `C("refuse/etag-empty", True, "", None, None, None)`.
   - **N06** `last_modified: true` accepted — recipe: hand case `C("refuse/lm-bool", True, None, True, None, None)`; note `refuse/lm-negative` still refuses under this mutant, so frozen M13's kill does not transfer.
   - **N07** `exists=false` + validator + `received_status=304` accepted — recipe: status-bearing validators-without-representation hand case (the current one is construction-stage only; generated inputs never pair exists=false with a validator).
   - **N08/N11 (vacuous survivors) — refusal-coarseness class:** `score_subject` accepts any rc≠0/empty/non-JSON stdout as a refusal, so mutants that swap one C6 refusal for another (non-object clause dropped; dup-key scoping no-op) are invisible. If the successor wants these clauses killable, it must pin refusal diagnostics or refusal classes — instrument-design decision, routed.
3. **Dup-key kill-path nuance:** `refuse/raw-dup-bytes` kills dup-key acceptance only through a collateral C6 status-without-validator refusal (the duplicated `received_status: 304` lands on a validator-less stored response); `refuse/raw-nested-dup` is the load-bearing kill for both frozen M11 and new N09. Keep both cases in any successor population.

## Deliverables (all inside `.ufo/waves/round-96/w1/MutReval/`)

`mutants-report.md` (full report, verdict line, per-mutant tables, recipes) · `new-mutants.json` (12 find/replace defs + outcomes + pristine/restoration metadata) · `receipt-frozen-M01.txt`…`receipt-frozen-M14.txt` · `receipt-new-N01.txt`…`receipt-new-N12.txt` · `receipt-pristine-driver.txt` · `receipt-counter-main.txt` · `receipt-counter-selftest.txt` · `receipt-digests.txt`.

## Bounds

Writes scoped to `w1/MutReval/` + `w1/MutReval.md` + seat scratch `/fast/scratch/hyaku/kake-r96/MutReval/` (deleted before yield, receipts copied first). No mutating git/jj command anywhere (read-only `rev-parse`/`show`/`log`/`status` only); no clone or fixture repo needed; no sysctl touched; no tool installed (stock python3/git sufficient). Frozen files read-only; `c96_reval` imported, never edited.
