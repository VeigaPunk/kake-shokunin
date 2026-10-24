# CriticMeasurementLimits — round 30, wave 2

Axes: operability and freshness. Advisory review only; no round judgment.
Attacked wave-1 items: C1 fixture/repair coverage at `71c6bfa`, and C2's
recheck instruction in `corpus/knowledge/render-static-sites.md` at `451e98f`.
Sandbox: `/fast/scratch/hyaku/kake-r30/w2/CriticMeasurementLimits/` (S below).

## 1. Operability: committed regression coverage stops before the repaired families do

Counterexample: five deliberately regressed gates still pass the committed
fixture runner, 41 cases, 0 failures, exit 0:

| Mutant under S/mut/ | Regression | Declared counter afterward |
|---|---|---|
| M1-repeat-last-wins | Remove StoreOnce's duplicate-option guard | 13/14, exit 1 |
| M2-no-onoctty | Remove input open's O_NOCTTY flag | 13/14, exit 1 |
| M3-depth-limit-50 | Raise RecursionError when directory stack exceeds 50 | 13/14, exit 1 |
| M5-dup-only-top-level-names | Detect duplicate keys only named rows/pairs | 13/14, exit 1 |
| M4b-only-NaN-and-overflow | Admit Infinity/-Infinity, retain NaN/overflow rejection | 13/14, exit 1 |

This is not evidence that the landed gate is broken: the counter catches all
five. It establishes an undisclosed boundary of the committed self-test:
14/14 does not mean these repaired behaviors have committed fixture protection.
Even F01/F02's fixture-and-rename conditions prove a reason code is compared,
not that each member of the family is represented in committed fixtures.
Fixture 38 covers a population top-level duplicate; 39 covers NaN; 41 covers
numeric overflow. Their successful rename tests cannot establish nested-key
or Infinity coverage. F04/F05/F06 have no committed fixture at all.

Evidence: `.ufo/waves/round-30/c1_reason_count.py:300-341,447-467`;
`scripts/fixtures/citing-set/38-document-duplicate-key/population.json:1`;
`39-document-nonfinite-number/population.json:1` and
`41-document-nonfinite-overflow/population.json:1` under the same fixture root.
The lesson's coverage caveat (`corpus/lessons/round-30.md:84-87`) names only
12 uncovered reason codes. The missing family cases emit already-covered
codes or usage outcomes; that list does not disclose them. SCORECARD's
notes (`SCORECARD.md:734-751`) describe strict checks, not this fixture gap.

Smallest safe correction: explicitly distinguish counter-built/strict-only
family checks from committed regression fixtures in the lesson and registry.
If committed regression coverage of these families is intended, add those
cases; do not silently reinterpret 14/14 as that stronger property.

## 2. Freshness: the entry's recheck command cannot detect a Render Docs change

`corpus/knowledge/render-static-sites.md:3` prescribes the frozen quote counter
as the action at 90 days or on a Render Docs change. Its only inputs are
committed bytes; it checks a literal registry date of 2026-10-22 and hashes of
retained text (`.ufo/waves/round-30/c2_quote_truth.py:81-114`). It performs no
fresh fetch, compares no current page, and evaluates no elapsed time.
[INFERENCE] The same retained revision will therefore retain its 4/4 after
any remote documentation change or passage of 90 days. Replaying this command
cannot renew the verified-at date or discover platform drift.

Disclosure check: SCORECARD's notes (`:752-765`) disclose quote/citation holes
and frozen-source identity, not that this prescribed recheck is only replay.
The lesson (`corpus/lessons/round-30.md:31-41`) records the two opening times
and body dynamics, not the invalid renewal procedure. SKILL.md:761-764 does
correctly require reopening the pages; the knowledge entry contradicts it.
This is a fixable instruction inconsistency, not a claim that 4/4 itself is
wrong or that current Render content differs. No live request was made here.

Smallest safe correction: label the counter command as historical evidence
replay; make the recheck field require authorized reopening and semantic
comparison of all four pages, then new dated receipts. Explicitly disclose
this distinction in the lesson. Preserve the frozen round counter.

## Commands and evidence

Commands below ran inside S with TMPDIR=S/tmp; no lane Git state was changed.
`git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin S/clone`; then
`git checkout -q 451e98f` inside that clone: exit 0.
`python3 -B mutants.py`: exit 0; script retained at S/mutants.py; all five
initial runner summaries were 41/41, exit 0. M4 was not a real regression
(post-parse checking still refused Infinity) and is excluded from findings.
For each table mutant: `python3 -B mut/<name>/scripts/citing_set_selftest.py --root mut/<name> --tmpdir tmp/run-<name>`: exit 0, 41 cases, 0 failed.
Sandbox-only clone/commit commands created mc/<name> revisions; then:
`python3 -B clone/.ufo/waves/round-30/c1_reason_count.py --root mc/<name> --revision HEAD --scratch S/tmp/cnt-<name>`: exit 1 for every table mutant.
Receipts: S/out-counter-<name>.json (revision, gate digest, counter result).
`sha256sum clone/scripts/citing_set.py clone/scripts/citing_set_selftest.py`: exit 0;
gate `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02`;
runner `0fc87d5b8134c841b02d0db33d8a3262fb774d0c8aacaefc6b6811f190b6530a`.
C2 finding is source inspection, not a new C2 execution or live comparison.
Did not verify all entry sentences, cross-version behavior, or live Render.
No tools installed or updated. No acceptance, integration, or shipment performed.
