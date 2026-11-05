# CriticClaims — round 97 (kake) attack on C1 and C2 as frozen

Seat: CriticClaims (leaf critic, no dispatch). Lane tip read: `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`
(`git -C LANE rev-parse master`). Round base `36d148f5c60100021304903c30e5663207c72f4f`.
Frozen digests verified before attack (`sha256sum`): `c97_index.py` 8535150e…aa008 OK;
`c97_reval.py` f3895a32…39266 OK; `frozen/neg-lookup-table.py` 898df9a2…460cc OK.
All counter runs below went through the public CLI (`--root … --revision … --work …`) on committed
revisions in clones of the lane (`git clone --shared`, toplevel asserted, identity `CriticClaims@example.invalid`).
Lane tree: not written by this seat (`git -C LANE status --porcelain` shows only pre-existing SKILL.md
and round-97 untracked files; see `receipts/lane-state.txt`). No tool installed or upgraded.

Scratch incident (disclosed, observed): ConnectorScope-23 deleted the round parent scratch dir at ~18:14Z,
including this seat's scratch. Every run below was re-created and re-run after that; the receipts in this
directory were regenerated from the re-created scratch. No frozen input was touched.

## Verdict basis (one line per claim, command and rc)

| claim | command | observed | rc |
|---|---|---|---|
| C1 control: base README | `c97_index.py --revision 36d148f5…` (controls/base-c1.txt, lane receipt) | `entries=84 indexed=46 unindexed=38 mismatches=38 met=false` | 1 |
| C1 tip | `c97_index.py --revision 9e27ce0b…` (lane receipt repair-c1.txt) | `mismatches=0 met=true` | 0 |
| C1 M1 one mega-row | `c97_index.py --root fx-c1-m1-megarow --revision 5ee564e3…` | `entries=84 indexed=84 unindexed=0 mismatches=0 met=true`, `index_rows 130` | 0 |
| C1 M2 per-entry scope copy | `c97_index.py --root fx-c1-m2-scopecopy --revision 2c6beec0…` | `entries=84 indexed=84 unindexed=0 mismatches=0 met=true`, `index_rows 213` | 0 |
| C1 shuffle (lane receipt, not re-run) | controls/ctl-c1-forgery-shuffle.txt | `mismatches=0 met=true` | 0 |
| C2 control: predecessor at base | `c96_reval.py` (controls/c2-predecessor-at-base.txt, lane receipt) | NameError `mutants`, no verdict | 1 |
| C2 tip, successor | `c97_reval.py --revision 9e27ce0b…` (receipts/c2-tip-successor.txt) | `candidate=present hand=37/37 generated=104/104 heldout=56/56 forgeries_refused=7/7 positive=admitted mutants=14/14 survivors=none anti_table=ok population=ok met=true` | 0 |
| C2 K1 5xx enumerated | `c97_reval.py --root fx-c2-k1-5xx-enumerated --revision 270de0c0…` | `hand=37/37 generated=104/104 heldout=54/54 … met=true` | 0 |
| C2 K2 etag control-char-only | `… fx-c2-k2-etag-control-only --revision c29fd622…` | `hand=37/37 generated=104/104 heldout=55/55 … met=true` | 0 |
| C2 K3 bool last_modified accepted | `… fx-c2-k3-bool-lastmod --revision eab7fe4e…` | `hand=37/37 generated=104/104 heldout=55/55 … met=true` | 0 |
| C2 K4 only 100 refused as 1xx | `… fx-c2-k4-1xx-only-100 --revision 5210393d…` | `hand=37/37 generated=104/104 heldout=55/55 … met=true` | 0 |
| C2 K5 all four | `… fx-c2-k5-all-four --revision a227d62d…` | `hand=37/37 generated=104/104 heldout=56/56 … met=true` | 0 |

Probe-level proof that K1–K5 break contract v1 (`direct.py`, `receipts/direct-probes.txt`, run as `python3 -I` on the
candidate file alone; the contract text is `.ufo/waves/round-96/reval-contract-v1.md`):

| probe | contract v1 says | real candidate 9e27ce0b | K1 | K2 | K3 | K4 | K5 |
|---|---|---|---|---|---|---|---|
| status 502 | C4: 500–599 → may-reuse-stored | may-reuse-stored | replace-stored (WRONG) | may-reuse | may-reuse | may-reuse | replace (WRONG) |
| etag `"a"b"` | C6: etagc excludes DQUOTE → refuse | refuse | refuse | construct (WRONG) | refuse | refuse | construct (WRONG) |
| etag `"a\x7fb"` | C6: etagc excludes DEL → refuse | refuse | refuse | construct (WRONG) | refuse | refuse | construct (WRONG) |
| last_modified `true` | C6: non-negative integer → refuse | refuse | refuse | refuse | construct, if_modified_since=true (WRONG) | refuse | construct (WRONG) |
| status 101 | C6: 1xx refused → refuse | refuse | refuse | refuse | refuse | replace-stored (WRONG) | replace (WRONG) |

Every K-variant differs from the real candidate by a few-line edit (`receipts/c2-variant-diffs.patch`).

## C2 — findings

**F-C2-1 (falsifies C2 as frozen).** The frozen predicate is satisfied by a candidate that treats only
500, 503 and 599 as 5xx (K1). Cause: `generate()` draws statuses from {200,204,302,304,404,410,499,500,503,599};
hand cases use 500/503/599 only. No 501, 502, 504 or any other 5xx is exercised anywhere in the population.
C4 is a universal clause ("500–599"); the population enumerates three points of it. Counter met=true, exit 0.

**F-C2-2 (falsifies C2 as frozen).** Etag grammar is tested by one control byte (0x01) and one unquoted
string (hand cases `refuse/etag-quoted-control`, `refuse/etag-unquoted`). A candidate that rejects only
control characters and accepts DQUOTE and DEL inside the quotes (K2) passes all 37 hand cases, all 104
generated and all held-out cases. C6 names the etagc grammar (RFC 9110 §8.8.3) as a universal refusal.
Counter met=true, exit 0.

**F-C2-3 (falsifies C2 as frozen).** No case in the hand, generated or held-out population sends a boolean
`last_modified`. `_is_int` excluding bool is therefore untested. K3 accepts `true` as a timestamp and emits
`if_modified_since: true`. Contract: "non-negative integer". Counter met=true, exit 0.

**F-C2-4 (falsifies C2 as frozen).** 1xx refusal is tested at 100 (hand), 99 and 600 (hand). 101–199 are not.
K4 refuses only 100 and decides 101 as replace-stored. Counter met=true, exit 0.

**F-C2-5.** K1–K4 composed (K5) is still met=true, exit 0. The counter has no clause that can see any of the four.

**F-C2-6 (sizing: silent denominator shrink).** `main()` builds `gen_expected` with `except Invalid: continue`
(c97_reval.py lines ~634–639), and the held-out list the same way. The reference refuses 16 of the 120 seed-97
generated inputs and 1 of 30 selftest-seed inputs (`receipts/direct-probes.txt` first lines). Those refusals are
never scored against any candidate, so the printed `generated=104/104` is a denominator of valid inputs only.
The contract text (reval-contract-v1 "met predicate") says "all 120 seeded generated cases match". The counter
therefore reports a population that disagrees with its own contract prose; the refusal leg of generated input is
untested. Held-out drawn count is always 60; scored count varies by revision (54–56), by the same mechanism.

**F-C2-7 (sizing: a clause that does not measure the candidate).** `mutant_cases` is fed `base_src` read from
`MUTANT_BASE` = the frozen positive control (`main()` line ~689), never the candidate. `mutants=14/14` is therefore a
harness self-check that is identical for every candidate. It is observed identical across the tip and K1–K5
(all `mutants=14/14`). The predicate phrase "every scored mutant killed" reads as a candidate test and is not one.

**F-C2-8 (sizing / attribution, not a falsification).** The candidate blob is byte-identical at base and tip
(`192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212` at both `36d148f5` and `9e27ce0b`; `receipts/lane-state.txt`).
The round's C2 credit therefore lands on a candidate that landed in round 96, scored by an instrument that changed
this round. This is consistent with the r96 flip rule ("round 97's successor counter reaching met=true on the landed
candidate"), but the capability move is an instrument credit, not new capability work. Recorded so the SCORECARD row says so.

**F-C2-9 (minor instrument hygiene; fail-closed, not a false green).** `main()` does `shutil.rmtree(work/tree)` and
writes `work/tree/mut-*.py`. Two concurrent scorings sharing one `--work` collide. I observed it: `FileNotFoundError`
at `mutant_cases` line 433, rc=1, traceback, no verdict line. The verdict is not green; the failure mode is a crash.

**C2 causal separability (holds).** `c97_reval.py` reads only `scripts/reval_exchange.py`, the round-96 pins file
and fixtures, the round-96 mutant population and base, and `round-97/frozen/neg-lookup-table.py`. It does not read
`corpus/`. Verified by grep of the counter's path constants (PINS_FILE, POSITIVE, FORGERIES, MUTANTS_JSON, MUTANT_BASE,
CANDIDATE). C2 can be verified without C1.

**Anti-table and forgery route (for completeness).** All five K-variants pass `anti_table=ok`, `forgeries_refused=7/7`,
`heldout` at its (reduced) denominator. The frozen lookup-table forgery is refused via heldout as designed; I did not find
a memorizing candidate that survives heldout, because held-out seeds derive from the scored commit id and a
memorizer cannot enumerate the 2×5×10⁶×11 input space. Positional/seed-order tables and oracle import remain
frozen-tested; I did not build new variants for them (budget spent on the five above).

## C1 — findings

**F-C1-1 (falsifies the counter leg of C1).** One row can index all 84 entries. M1 appends a single table row whose
Entry cell holds all 84 `knowledge/…md` tokens, whose coverage cell holds every source id in the population and two
6+-letter words drawn from each entry's body (168 words). The counter's rule is "an entry is indexed iff ≥1 row
carries its token, its source ids, ≥8 other words and ≥2 shared 6+-letter words". M1 satisfies all four for every
entry. `mismatches=0 met=true`, exit 0. This is the declared shuffle known-limit's family, but one step past it:
the rows are not shuffled per entry, they are one non-judgment row for the whole population.

**F-C1-2 (falsifies the predicate's review leg as written).** The frozen predicate requires "every row of the round-97
index section judged agree" and "agree count equals the section's row count". The verdict format is one line per row:
`<entry>\t<agree|disagree>\t<reason>`. A row that names 84 entries has no single `<entry>`. If it is judged agree once,
the predicate's count condition holds (1 row, 1 agree) with zero per-entry judgment. The predicate's unit (row) and the
counter's unit (entry, any-row) do not match, and the frozen text does not say which governs when they diverge.

**F-C1-3 (counter measures presence, not accuracy; the review leg is the only accuracy check).** M2 writes 84 rows, one
per entry, each copying the entry's first prose line verbatim, with its ids. `mismatches=0 met=true`, exit 0, `index_rows 213`.
Copied scope is accurate by construction, and the freeze admits quoting the scope sentence by design. So "calibration"
as the counter reads it is satisfied by a mechanical copy. The axis definition ("self-assessment vs observed state")
is met only through reviewer judgment on the rows, which the counter does not supply. AXES.md is not in the lane tree
(`find . -name 'AXES*'` empty); the definition used here is freeze.md's and CORPUS.md's quote "An index row is a claim".

**F-C1-4 (the calibration measure is blind to superseded failing claims).** The repair appends 38 rows and keeps the
earlier rows "above as filed history" (corpus/README.md, the new section's preface). `receipts/stale-rows.txt`: 129 index
rows at the tip; 33 entries carry more than one row; **29 rows still fail the counter's own per-row test** (missing source
ids, or fewer than 8 words of coverage, or fewer than 2 shared words). The counter reports per-entry, so these 29 rows
are invisible to `mismatches`. The predicate reviews only the round-97 section. A README that carries 29 self-assessment
rows failing the counter's own standard is recorded as calibrated.

**F-C1-5 (minor: vacuous id gate for three entries).** `gate-agreement-metadata.md`, `gate-status-ledger.md` and
`kimi-subpath-audit.md` have no `S###` id in the first 15 lines' `source:` line (own-work or non-S provenance). For these,
`need = {}`, so the id conjunct is vacuous and any row with the token and 8 words passes. Current rows happen to cite
no ids either, so no tip result changes; the gate is simply empty for them.

**F-C1-6 (sizing: undefined denominator).** "The round-97 index section" is not a construct the counter can see. It is a
README heading ("## Coverage index — round 97 (calibration repair)"). The review denominator is therefore defined by a
human reading of the README, not by the counter. Predicate and counter can disagree about what was reviewed.

**F-C1-7 (sizing: the do-nothing control does not cover the claimed attack).** The frozen do-nothing control (base README,
`mismatches=38`) fails, as stated. But the cheap non-work controls M1 and M2 pass the counter. The control set in
freeze.md names the zero-work tree and the path-only/fenced junk rows; it does not name a multi-entry row or a copied-scope
generator. The §9 do-nothing check discriminates against doing nothing, not against the work-skipping class.

**C1 causal separability (holds).** `c97_index.py` reads only `corpus/README.md` and `corpus/knowledge/*.md` at the
revision (README, KDIR constants; `git ls-tree` of KDIR). It does not read the C2 candidate, pins or fixtures. C1 can be
verified without C2.

## Q3 — r34-class junk-row route: is it closed?

**No.** The shuffle known-limit plus the row-review conjunct do not close the route, for three reasons, each shown above:
(a) the counter admits a single junk row for the whole population (F-C1-1) and a mechanical per-entry copy (F-C1-3);
(b) the review unit is the row and the verdict format is per entry, so a multi-entry row either cannot be judged per entry
or is counted once (F-C1-2); (c) nothing in the predicate requires one judged row per entry, so "agree count equals row
count" is satisfiable without per-entry work. The route is closed only by reviewer discipline, not by the frozen predicate.
The minimal correction is a per-entry predicate (every entry has ≥1 row judged agree, and no judged row names more than one
entry), which is an instrument change and so is routed to round 98, not made here.

## Q2 — C1 sizing and axis

- Named by the surface it changes: yes (`corpus/README.md` vs `corpus/knowledge/*.md`).
- Axis: calibration as "self-assessment vs observed state" is the right axis only with the review leg doing the accuracy
  check; the counter alone measures presence, identifiers and word overlap (F-C1-1, F-C1-3).
- Do-nothing control fails the target: yes (base 38 mismatches). It does not fail the work-skipping class (F-C1-7).
- Universal clause unenumerated: "every knowledge entry has a row that describes it" is enumerated per entry by the counter
  but "describes" is not checked; "every row is a claim" is not enumerated (F-C1-4).

## Q2 — C2 sizing and axis

- Named by the surface it changes: yes (candidate `scripts/reval_exchange.py`).
- Axis: freshness, capability row enters on met. The credited artifact is r96's (F-C2-8).
- Do-nothing control fails the target: yes (predecessor crash). The instrument-set rule holds.
- Universal clauses unenumerated: C4 (5xx), C6 etagc grammar, C6 integer (bool), C6 1xx range, C5-as-status-set, and the
  "all 120 generated" prose (F-C2-1..6). The mutant clause is candidate-independent (F-C2-7).

## Findings count

C1: 7 (F-C1-1..7). C2: 9 (F-C2-1..9). Total 16. Of these, falsifying as frozen: F-C1-1, F-C1-2, F-C2-1..F-C2-4
(the K-variants are the decisive ones; F-C2-5 is their composition). Sizing and minor: the rest.

## Verdicts

C1 = **falsified** (the frozen counter admits a one-row, zero-judgment control (F-C1-1); the predicate's review unit cannot
judge a multi-entry row (F-C1-2); the 38 per-entry rows are genuine work but the frozen measure does not require it).
C2 = **falsified** (the frozen counter reports met=true for candidates that violate contract v1 on C4, C6 etag, C6 integer and
C6 1xx; probes in `receipts/direct-probes.txt`).

Both falsifications are of the frozen predicates, not of the repairs' content as far as this seat can see. The 38 C1 rows are counter-passing (tip `mismatches=0`) but this seat did not judge them; the review verdicts belong to the reviewers. The C2 candidate at `192b3bf7` passes the frozen positive control and the tip scoring; this seat did not re-derive its contract behaviour beyond the probes above. The defects are in what the counters can
see, and the fixes are instrument changes (routed, not made).

CRITIC C1=falsified C2=falsified findings=16

## Receipts

`receipts/` (copied from scratch before yield):
- `drive.py`, `variants.py`, `stale.py`, `direct.py` — the scripts that produced every number above (python3 stdlib + git only).
- `variants-results.json` — rc, line 1, fixture path and revision for all K/M variants and the tip run (`python3 -B variants.py`, rc 0).
- `c2-tip-successor.txt` — `c97_reval.py --root <LANE> --revision 9e27ce0b… --work <scratch>` rc 0 (`cat` line shows rc=0).
- `direct-probes.txt` — generate() dropped counts and candidate probes (`python3 -B direct.py`, rc 0).
- `stale-rows.txt` — per-row failing list (`python3 -B stale.py`, rc 0).
- `c2-variant-diffs.patch`, `c1-variant-stats.txt` — the exact edits behind K1–K5 and M1/M2.
- `lane-state.txt` — candidate blob shas at base and tip; `git status --porcelain` at the lane (read-only).

Tools: none installed or upgraded. Interpreters used: system `python3` (stdlib only), `/usr/bin/git`.
