# ReviewerNoHarm

No-harm check: the six earlier lane gates were run against a shared clone at the build
`ab6e100e442046006fa039315f5bd33bb516940b` (fresh clone under
`/fast/scratch/hyaku/kake-r59/ReviewerNoHarm/clone`, `git checkout --detach`, `rev-parse HEAD`
= `ab6e100e…`, scratch removed after transcripts were copied beside this report). Invocation
shape matches the wave-1 baseline: `python3 -B <counter> --root <clone> --revision ab6e100e…`
from inside the clone, `c58_resolver_cases` with `--work <scratch> --seed 58`, `c57_idresolver_gate`
with `--fleet /home/vgpnk/Projects/shokunin`. Base values are from
`.ufo/waves/round-59/w1/ExecHistoricalGates.md` (all six green at `fd6303ce`). Saved transcripts:
`ReviewerNoHarm.files/out-*.txt`.

## RUNS:

| gate | base (fd6303ce) | build (ab6e100e) | verdict |
|---|---|---|---|
| c58_resolver_cases.py (`--seed 58`) | exit 0, `14/14 met=True` (P6 59/59, P7 ids 108/108) | exit 0, `C2 resolver-cases 14/14 met=True` (P6 72/72, P7 ids 110/110 dangling=0) | green → green, NO HARM; all P1–P5 worktree-mode fixtures still behave, so H6 did not materialize |
| c58_receipt_rewrites.py | exit 0, `events=19 … new_receipts=2 met=True` | exit 0, `C1 receipt-rewrites events=19 undisclosed=0 … new_receipts=2 met=True` | green → green, NO HARM (H5 did not materialize; no receipt rewritten) |
| c58_quote_truth.py | exit 0, `8/8 met=True` | exit 1, `C3 quote-truth 6/8 met=False` — C7 `validated scratch registry is not byte-equal to the landed registry`, C8 `registry rows 164 != mirror rows 160 + 2` | green → red, but the row is marked `historical from round 59` in SKILL.md at the build (line ~1295), exactly the pinned condition (registry now 164 = 160 + 2 + the two round-58 S423/S424 rows). NOT a harm by the seat rule — historical by design (H2, as predicted) |
| c57_idresolver_gate.py (`--fleet /home/vgpnk/Projects/shokunin`) | exit 0, `5/5 met=True` (selftest 59/59; G5 ids_cited=108) | exit 0, `C2 id-resolver 5/5 met=True` (selftest 72/72; G4 `(99,94,5,5,0)`; G5 `(110,110,0,0,0)` ids_cited=110) | green → green, NO HARM (H3 did not materialize; the hardened tool source does not trip the G2 judge-word check) |
| c55_readme_index.py | exit 0, `index_mismatches=0 knowledge_files=56 met=True` | exit 1, `C1 readme-index index_mismatches=1 knowledge_files=58 met=False` — `head_changed=1: crawler-identity.md`; unindexed=0 multi=0 thin=0 duplicate=0 deleted=0 dangling=0 coverage_rows=60 | green → red, HARM by the seat rule: row is NOT marked historical at the build (SKILL.md:1233 still reads `gate (offline, committed bytes only; no network)`). This is the predicted, unavoidable H1: the c59 C9 predicate requires the correction inserted mid-file (line ~35), which breaks the byte-prefix invariant on a file unchanged since c55's base. Needs either a `historical` marking naming `head_changed: crawler-identity.md` or an explicit recorded decision — the seat rule reports it as a harm |
| c56_selftally.py | exit 0, `tally_mismatches=0 rows_checked=10 met=True` | exit 0, `C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True` (all ten tallies claim=observed, same claims as base) | green → green, NO HARM (H4 did not materialize; no `scripts/fixtures/` change, no pre-existing *.py touched, no duplicate SKILL row name) |

sources-census run (required): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ exit 0; last line `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, preceded by
14 `W04 duplicate url … across scopes` warnings on S033/S088/S092/S098/S099/S102/S110/S111/S115/S116/S117/S127/S416/S417
— all pre-existing rows, none on the new S425/S426 (registry at build = 279-line SOURCES.md, 164 S-rows per C8).

## HARMS:

- `c55_readme_index.py` / `readme-index-counter`: green at base, red at build (`head_changed:
  crawler-identity.md`, exit 1), and the row carries no `historical` marking at `ab6e100e`. Harm by
  the seat rule — unavoidable consequence of the mandated mid-file C9 correction (H1 reproduced
  exactly as predicted in `w1/ExecHistoricalGates.md`); the L1 must mark the row historical or record
  an explicit waiver.
- `c58_quote_truth.py`: red at build but already `historical from round 59` per SKILL.md at the build —
  reported for completeness, not a harm.
- No other harms: the five remaining gates are green at the build, several materially stronger than
  at base (P6/G2 selftest 72/72 vs 59/59; P7/G5 ids_cited 110 vs 108 — the two new rows resolve).
- Sources census: clean (`kake ok`, exit 0); the 14 `W04` warnings cite only pre-build S-ids.

VERDICT: 5/6 gates hold at ab6e100e (c58 resolver 14/14, c58 receipts met, c57 gate 5/5, c55→red, c56 met); c58 quote-truth red is historical by design (marked at build); the only true harm is c55 readme-index `head_changed: crawler-identity.md` — the predicted unavoidable H1 — and no skill marking covers it yet.
