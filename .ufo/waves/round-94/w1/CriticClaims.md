# CriticClaims — round 94 (kake, hyaku run 15, attempt 1), wave w1

VERDICT: claims do not hold as declared. (a) C2 "40/40" is unreachable: M11 is a semantically equivalent mutant, so the ceiling is 39/40 and the frozen kill rule makes C2 an honest unmet 1. (b) C1 "mismatches 0, met=true, exit 0" is reachable by two non-repair SKILL.md edits (prose-ifying the 13 directory paths, or annotating them as absent) that leave identity pins and battery intact; the freeze's own repair rule is not enforced by the counter. (c) The C2 population is not "mutants of scripts/conditional_eval.py": all 40 find strings match the frozen positive control `pos-good.py` and match the lane candidate zero times, so the "before 31/40 at base" is measured on a different base. (d) `c94_selfassess.py --skip-battery` prints `met=true` with `battery=0/8 predecessor_admits=0/0`.

Scope and state at my last check: `w1/ExecC1Repair/` is empty (no `skill.diff`), so the C1 row-by-row review in section 3 is a pre-registered rule applied to the base rows, not a verdict on a repair. `w1/ExecC2Mutants.md` exists and agrees with every C2 number below. `corpus/SOURCES.md` is modified in the working tree (ExecSourceRows, in progress); I did not assess S477/S478.

Lane is `ba667b245f26125c13885958498b3b4999756d04` (freeze), base `0f7d9bbcdd6a9ed36f5bc62b2116ddd040e871a8`. No LANE file was edited; no LANE git mutation. Scratch clone (`git clone -q --shared`, toplevel asserted, throwaway identity `critic-fixture`, commits only in the clone) was used for the SKILL.md experiments; the clone and scratch are deleted before yield. No tool was installed or upgraded. No network GET was made.

## 1. Claim-by-claim: before/after re-derivable, do-nothing control, kill rule

### C1 (calibration)

| Check | Command | Result | Receipt |
|---|---|---|---|
| Before (base) | `TMPDIR=… python3 -B .ufo/waves/round-94/c94_selfassess.py --root <lane> --revision 0f7d9bbc --work <scratch>` | line 1: `mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=8/8 predecessor_admits=7/7 floor=2 self_pin=ok met=false`; rc=1 | `w1/CriticClaims/c1-base-0f7d9bbc.out` |
| HEAD re-run | same, `--revision ba667b24` | identical line 1, rc=1 | `w1/CriticClaims/c1-head-ba667b24.out` |
| Instrument selftest | `python3 -B c94_selfassess.py --selftest` | `selftest 9/9 planted findings, exit 1 on planted, exit 0 on repaired`, rc=0 | `w1/CriticClaims/c1-selftest-rerun.out` |
| Digest | `sha256sum .ufo/waves/round-94/c94_selfassess.py` | `58028584…8306a` = freeze | `w1/CriticClaims/git-and-digests.out` |
| Surfaces digest | `sha256sum .ufo/waves/round-94/frozen/c1-surfaces.json` | `b911321d…e4e6`, matches the constant in the counter | same |

Do-nothing control: rc=1, met=false. The do-nothing route cannot reach the target. **Holds.**

But the target is reachable without the repair the freeze describes (section 3): see X4/X5.

### C2 (instrument capability, v1 vs v2)

| Check | Command / source | Result |
|---|---|---|
| v2 counter digest | `sha256sum .ufo/waves/round-94/c94_conditional.py` | `357d8cd1c2dd04f609518e785616c4f9e54e348b954266a137078dd1ed2a750a` = freeze; `git show ba667b24:` equal |
| v1 counter digest | `sha256sum .ufo/waves/round-93/c93_conditional.py` | `fee28ea0…` (not pinned in the freeze's digest table; last touched by commit `bb8012fe`, `git log -1 -- …` → unchanged since freeze) |
| population pins | `sha256sum .ufo/waves/round-93/frozen/c2-population.sha256` | `9c45db5c…` = `PINS_SHA` |
| base candidate | `git show 0f7d9bbc:scripts/conditional_eval.py \| sha256sum` | `d3bac7de…` = receipt `candidate_sha256` |
| v1 HEAD | `python3 -B c93_conditional.py --root <lane> --revision ba667b24 --work <scratch>` | `hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted … met=true`, rc=0 (`w1/CriticClaims/c2-v1-head-ba667b24.out`) |
| v2 HEAD | `python3 -B c94_conditional.py --root <lane> --revision ba667b24 --work <scratch>` | `hand=53/53 generated=120/120 … met=true`, rc=0 (`w1/CriticClaims/c2-v2-head-ba667b24.out`) |
| selftest | `python3 -B c94_conditional.py --selftest` | `selftest 7/7 fixtures scored as declared; drifted-reference cases=4`, rc=0 (`w1/CriticClaims/c2-selftest-rerun.out`) |
| do-nothing (unmutated positive control) | `score_subject` of `pos-good.py` under v1 and v2 (`w1/CriticClaims/c2-kill-drive.py`) | v1 hand 44/44 gen 120/120 fails 0; v2 hand 53/53 gen 120/120 fails 0 → admitted by both (the control does not kill) |
| kill table | `python3 -B c2-kill-drive.py` (imports both counters read-only; mutants = the frozen 40-patch list applied to `pos-good.py`) | v1 killed **31**, v2 killed **39** (`w1/CriticClaims/c2-kill-table-pos-good-base.json`, `c2-kill-run.txt`) |

"Before" and "after" are **not** one command: the C2 numbers require the mutant driver (40 committed mutant trees in a scratch clone, each scored by the counter). The round-93 base revision `191dd0ed` cited by the round-93 receipts is absent from the lane (`git cat-file -t 191dd0ed` → `fatal: Not a valid object name`, rc=128). **Fails the one-command rule** (see D1, D14).

### Kill rules: freeze sentence vs counter

- C1 freeze sentence: `met <=> pins ok AND zero mismatches AND battery refused 8/8 AND predecessor admits >= 2/7`. Counter `met = (not short) and (not ident) and (not mismatches) and (skip_battery or (b_r == b_t and p_a >= floor))`. The `skip_battery or` term makes `met` true without the battery or predecessor clauses (D5). The identity pin covers only the SKILL row first cell (D4). The battery has an uncovered route set (D3) and one tautological route (D6).
- C2 kill rule (any v2 survivor = honest unmet) is implemented by the external driver (exit code of the counter per mutant), not by the counter. It matches in outcome (see section 2) but is not a single command.

## 2. C2: arithmetic, equivalence, population, and the nine new cases

### 2.1 40/40 is unreachable (D2)

M11 (`elif ... ius is not None: if (stamp or 0) > ius`) differs from the base only when `last_modified` is null, where it compares `0 > ius`. Both the positive control's `integer()` (`pos-good.py`) and the counter's reference (`c94_conditional.py` `reference()`: `is_int(v) and v >= 0`) admit only ints >= 0 for `if_unmodified_since`, so `0 > ius` is always false, and the mutant falls through identically. Evidence:

- Analytic argument above (uses only the counter's own validation).
- My grid: `python3 -B c2-m11-equivalence.py` → `grid inputs 28512 differences 0`, rc=0 (`w1/CriticClaims/c2-m11-equivalence.out`).
- Executor's exhaustive product: `cases=115200 differing=0` (cited in `w1/ExecC2Mutants.md`, not re-run by me).

The v2 counter's hand case `ius/unbounded-when-last-modified-absent` expects 200 (contract clause 9: "ignored when `current.last_modified` is null") and the mutant also returns 200, so no input can kill M11. v2 therefore has a ceiling of 39/40. The freeze's target `killed=40/40` cannot be met by any candidate or counter; under its own kill rule C2 is an honest unmet 1. The freeze does not mention equivalence.

### 2.2 Each mutant's first failing case vs its class (population as applied to pos-good.py)

| Mutant | Class (patch list) | v1 | v2 | v2 first failing case | Class match |
|---|---|---|---|---|---|
| M11 | 9 IUS not ignored w/o last_modified | S | S | — (equivalent, D2) | — |
| M18 | 3 lowercase `w/` accepted | S | K | `refuse/ifmatch-lowercase-weak-prefix` | yes |
| M19 | 3 empty opaque-tag refused | S | K | `inm/empty-opaque-tag-matches` | yes |
| M24 | 1 negative integer accepted | S | K | `refuse/negative-if-modified-since` (also `refuse/unmodified-since-malformed-under-if-match`) | yes |
| M28 | 2 last_modified allowed when absent | S | K | `refuse/absent-representation-with-last-modified` | yes |
| M29 | 6 IUS skipped when If-Match present | S | K | `refuse/unmodified-since-malformed-under-if-match` | yes |
| M32 | extra key in `current` tolerated | S | K | `refuse/current-extra-key` | yes |
| M37 | method compared case-insensitively | S | K | `inm/lowercase-method-is-not-get` | yes |
| M40 | HTAB around list members not accepted | S | K | `inm/htab-around-list-members` | yes |

Cross-kills of the nine new cases (from `kill-table.json` `all_hand_failing`):
- `inm/empty-opaque-tag-matches` also fails M14 and `inm/htab-around-list-members` also fails M14 (method inversion; GET-based cases). M14 is already killed in v1 by `inm/match-get`. Same clause family (10); incidental.
- `inm/lowercase-method-is-not-get` also fails M13 (always-304). Same method family; old kill already present.
- `ius/unbounded-when-last-modified-absent` fails **no** mutant: a dead case (see 2.1).

Kills by crash: M33 (`current.etag` null treated as any tag) fails as `rc=1 Traceback` on `inm/ignored-when-current-etag-absent` in v1 and v2 (the mutant crashes instead of answering). It counts as a kill; it is a crash-kill, not a clause decision (D8 below lists it as a limit).

### 2.3 Population base mismatch (D1)

- `git show 0f7d9bbc:scripts/conditional_eval.py` sha = `d3bac7de…` (candidate); `pos-good.py` sha = `0fe018a8…`. They differ.
- For all 40 mutants, `find` count in the base candidate = 0 (`python3 -B -c` over `mutants-posgood.json` vs `git show 0f7d9bbc:scripts/conditional_eval.py`); count in `pos-good.py` = 1. A driver that applies the patch list to the candidate yields 40× `PATCH-NOT-UNIQUE` and kills nothing.
- The round-93 receipts (`w1/recovered-partial/MutConditional/posgood-out/mutants.json`) state `base_rev 191dd0ed…` with `base.source = pos-good.py`. That revision is not in the lane. The executor's clone-only base commit `6d75ee0c` is the same "pos-good bytes" substitution.
- Therefore "31/40 at base" and "40 mutants of scripts/conditional_eval.py" are both mis-described. The numbers reproduce on the pos-good base (section 2.2). The C2 claim is an instrument test over mutants of a correct implementation, which is legitimate, but the freeze must say so.

### 2.4 Citation conflict: RFC 9110 §5.6.1 (D10)

The freeze cites §5.6.1 for M40 and §9.1 for M37. Checked in the scout's copy `rfc9110.txt` (sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, 502941 bytes; I did not re-fetch):
- §9.1 (line 3748): "The method token is case-sensitive." Supports M37. Holds.
- §5.6.3 defines OWS = `*( SP / HTAB )` (line 9802). §5.6.1 points to §5.6.3 for OWS. The freeze's "§5.6.1" for HTAB is a loose citation; §5.6.3 is the source.
- §5.6.1.2 (lines 1699-1700): "a recipient MUST accept lists that satisfy `#element => [ element ] *( OWS "," OWS [ element ] )`" and "MUST parse and ignore a reasonable number of empty list elements." The frozen contract refuses empty members (`refuse/empty-member`, a round-93 case, `"1", , "2"` → refusal). That contradicts a MUST in the very section the freeze cites. M20 (empty member tolerated) is therefore an RFC-conforming behaviour that the instrument kills. The freeze does not disclose this; it may belong to the contract-v2 routing (R93-9/10), but it must be stated.

## 3. C1: repair review rule (claim 2) and the strict-counter gaps

### 3.1 The 15 base findings (`w1/CriticClaims/e5-base-tree-rows.txt`)

The 15 E5 findings are 15 SKILL rows naming 13 distinct directories (`.ufo/waves/round-85/w1/ExecRegistry/` appears in 3 rows, the round-87 row also contains a brace list). Lines at base: 617, 720, 726, 1046, 1253, 1254, 1350, 1359, 1431, 1506, 1535, 1536, 1537, 1539, 1588. A repair must, for each row: keep the row's first cell (identity pin), name one concrete non-empty blob that the row's entry describes, and not annotate a present path as absent. The three `ExecRegistry` rows (1535-1537) must name three blobs that match their own entries, not the same tree or the same file.

### 3.2 The counter accepts non-repair edits (D3)

Experiments in the scratch clone (commits in clone only; receipts `w1/CriticClaims/e5-routes-*.json`, driver `e5-routes-driver*.py`):

| Variant | Edit | Result (line 1) | rc |
|---|---|---|---|
| X0 | none (base) | `mismatches=15 E5=15 pins=ok battery=8/8 predecessor_admits=7/7 met=false` | 1 |
| X1 | de-backtick one directory path | `mismatches=14 … met=false` | 1 |
| X2 | annotate one directory as a fabricated absent file `[r94-absence …: scripts/fixtures/citing-set/none.md absent]` | `mismatches=14 … met=false` | 1 |
| X3 | annotate a present directory as absent | `mismatches=15` (E5 "annotated absent but present" reported) | 1 |
| X4 | de-backtick **all** 13 directory paths (no blob named, rows and first cells intact) | `mismatches=0 E1..E5=0 pins=ok battery=8/8 predecessor_admits=7/7 met=true` | **0** |
| X5 | replace all 13 with `[r94-absence …: <path>/none.md absent]` (fabricated absences) | `mismatches=0 … met=true` | **0** |

X4 and X5 satisfy every counter predicate and fail the freeze's stated repair rule. The counter does not distinguish them from a real repair (the row count, first cell, and battery are unchanged). The freeze's identity pins are first-cell-only and do not pin row content. The battery's eight routes (section 3.3) do not include either route.

### 3.3 Battery issues (D6)

- F2 (canned wrapper) is refused by construction: `refused_f2 = ("counter=%s" % true_digest) not in first`, where `first` is the wrapper's own constant line. The counter under test is never executed for F2. So "battery 8/8" is 7 real routes plus one tautology.
- F1, F3, F4, F5, F6, F6b, Fv run the counter or predecessor on real fixture repos (code read in `c94_selfassess.py` lines 437-562; the per-route detail is in the base receipts' line 2 JSON, `battery` key; I did not re-run each route separately).

### 3.4 `--skip-battery` reports met=true (D5)

`python3 -B c94_selfassess.py --root <lane> --revision <X4 commit 2b5a49e6…> --skip-battery --work <scratch>` → line 1 `mismatches=0 … battery=0/8 predecessor_admits=0/0 floor=2 self_pin=ok met=true`, rc=0 (`w1/CriticClaims/c1-skip-battery-on-X4-variant.out`). The freeze's met sentence requires battery 8/8 and predecessor >= 2; the flag bypasses both. Any receipt that cites `--skip-battery` is a false green.

### 3.5 E4 gap (D7)

The docstring says "each blank-line gap is reported". The code reports a gap only when both neighbouring lines are table rows (`lines[i].startswith("|") and lines[i+1] == "" and lines[i+2].startswith("|")`). Probe (`w1/CriticClaims/e4-gap-probe.out`): a table row, a blank, a prose line, a table row → `mismatches=[]`; a table row followed by two blank lines and a row → `mismatches=[]`. Base E4=0, so this is a false-negative risk, not a base route.

### 3.6 Non-idempotent `--work` (D8)

Running the C1 counter twice with the same `--work` directory crashes in the battery: `FileExistsError: …/F1_shadow_subprocess/shadow` (`os.makedirs(shadow_dir)` without `exist_ok`), exit 1, no line-1 receipt. Exit 1 is the "unmet" code, not the "unevaluable" code 2 the docstring promises. A re-run with the same `--work` looks like a red measurement.

### 3.7 Provisional read of the in-progress repair (working tree, not committed)

At my read, `git diff -- SKILL.md` (working tree, mtime 12:11) changed 7 of the 15 rows (lines 617, 720, 726, 1046, 1253, 1254, 1350); the other 8 (1359, 1431, 1506, 1535-1537, 1539, 1588) were unchanged. Each changed row keeps its first cell (identity holds). Every new target is a non-empty file (no tree, no fabricated absence). Provisional row findings, to be re-checked on the final diff:

- 617 citing-set: `scripts/fixtures/citing-set/` → `…/01-single-literal-clean/expected.json`. One case of 29; the row's sentence now says the selftest delegates "over" that one file while the same row still says "29 independent consumer-input cases". Scope of the entry changed; **weak**.
- 720 round-29 real-input: `…/out/` → `…/out/summary.json` (950 B). Plausible if summary.json is the 4-finding summary the row describes; **needs check**.
- 726 base-path: `scripts/fixtures/base-path/` → `…/D1-root-relative-stylesheet/expected.json`. The row describes 30+15 fixtures; one file is named and the sentence says the selftest runs "over" it; **weak**.
- 1046 link-preview: `scripts/fixtures/link-preview/` → `…/canonical_first_mismatch/expected.json`. The row describes 45 fixture directories; one is named; **weak**.
- 1253 selftest-tally: `scripts/fixtures` → `scripts/fixtures/quote-class/inline.raw.html`, with the prose rewritten ("tree" removed, a new clause inserted). The row's entry is about the whole audited tree; **weak, and prose changed beyond the path**.
- 1254 yahoo-crawl: `…/sources/` → `…/sources/S367.html` (8051 B). The row describes the sources tree; **weak**.
- 1350 canonical-crawler: `.ufo/waves/round-51/` → `.ufo/waves/round-51/sources/receipts.json` (909 B), with the prose "under `.ufo/waves/round-51/`" removed. **needs check** against the row's entry.

Pattern: the repair names one member of a described population and, in two rows, edits the sentence's scope ("over" one file). That satisfies E5 (and therefore the counter's zero-mismatch predicate once all 15 are changed the same way) without naming "the blob the row's entry actually describes", which the freeze requires. The counter cannot distinguish this from a correct repair (section 3.2, X4/X5 show the same). The L1 must judge each row against its entry text; I have not completed that for the rows still unchanged.

## 4. Axis and trend claims (claim 4)

- C1 at HEAD: `met=false`. No calibration move can be reported. Calibration stays at 2 (freeze; SCORECARD row calibration `2`). "Improved" is not allowed unless a repair commit reaches `met=true` **and** the repair passes the row-by-row review in 3.1.
- C2 is an instrument-capability claim. It does not measure the freshness candidate, so no freshness move can be reported from it. Freshness 10 in SCORECARD is a legacy rating "re-anchored on receipts" from round 16, not re-measured (SCORECARD line 18). "Held at 10" is the legacy rating, not a measurement.
- The instrument move 31 → 39 (v1 → v2) is real on the pos-good population but is an instrument-only move; it must be labelled "instrument sensitivity" and not "freshness improved".
- Where a score stays at HOLD without a measured move (calibration 2, freshness 10), the report must say HOLD, not improved.

## 5. Numbers the report will cite (claim 5) — one command each

| Number | Command | Receipt |
|---|---|---|
| C1 base 15 (E5) | `c94_selfassess.py --root <lane> --revision 0f7d9bbc --work <s>` | `c1-base-0f7d9bbc.out` |
| C1 HEAD 15 | same with `ba667b24` | `c1-head-ba667b24.out` |
| C1 selftest 9/9 | `c94_selfassess.py --selftest` | `c1-selftest-rerun.out` |
| C2 v1 hand 44/44 at HEAD | `c93_conditional.py --root <lane> --revision ba667b24 --work <s>` | `c2-v1-head-ba667b24.out` |
| C2 v2 hand 53/53 at HEAD | `c94_conditional.py --root <lane> --revision ba667b24 --work <s>` | `c2-v2-head-ba667b24.out` |
| C2 selftest 7/7 | `c94_conditional.py --selftest` | `c2-selftest-rerun.out` |
| C2 v1 31/40, v2 39/40 (pos-good base) | `python3 -B c2-kill-drive.py` | `c2-kill-table-pos-good-base.json`, `c2-kill-run.txt` |
| M11 equivalent (28512 grid) | `python3 -B c2-m11-equivalence.py` | `c2-m11-equivalence.out` |
| E5 routes X0-X5 | `python3 -B e5-routes-driver.py` (SKILL.md variants in a scratch clone) | `e5-routes-X0-X3.json`, `e5-routes-X4-X5.json` |
| `--skip-battery` met=true | `c94_selfassess.py --root <clone> --revision 2b5a49e6 --skip-battery --work <s>` | `c1-skip-battery-on-X4-variant.out` |
| E4 gap probe | inline python over `c94_selfassess.audit()` (code in section 3.5) | `e4-gap-probe.out` |
| Digests | `sha256sum` on the counters, surfaces, population pins | `git-and-digests.out` |
| `191dd0ed` absent | `git cat-file -t 191dd0ed` → rc 128 | `git-and-digests.out` |
| RFC §9.1, §5.6.1.2, §5.6.3 lines | `grep`/`sed` on scout copy, sha `21c1cdce…` | `rfc9110-excerpts.txt` |
| Executor C2 agreement | `w1/ExecC2Mutants.md` (their v1 31/40, v2 39/40, M11 equivalent, D1) | lane file |

## 6. Defects (for the L1)

- **D1 (C2, material).** The 40-mutant population is a patch list for `pos-good.py`, not `scripts/conditional_eval.py`. 0/40 find strings match the candidate at base. "31/40 at base" is measured on the pos-good base at the unreachable revision `191dd0ed`. Freeze wording must change, or the population must be re-derived (not allowed after scoring).
- **D2 (C2, material).** 40/40 is unreachable: M11 is equivalent. Ceiling 39/40; honest unmet 1 under the frozen kill rule.
- **D3 (C1, material).** `mismatches=0 met=true` is reachable by de-backticking all 13 directory paths or by annotating them as fabricated absences (X4, X5). The counter does not enforce the repair rule in the freeze (name a concrete non-empty blob the row describes).
- **D4 (C1).** Identity pins check SKILL row first cells only; row content is unpinned.
- **D5 (C1).** `--skip-battery` reports `met=true` with `battery=0/8 predecessor_admits=0/0`.
- **D6 (C1).** Battery F2 is refused by construction; it never executes the counter. "8/8" is 7 real routes.
- **D7 (C1).** E4 reports only gaps between two table rows; the docstring promises every blank-line gap.
- **D8 (C1 exit contract; also C2 limit).** The C1 battery is non-idempotent under `--work` (FileExistsError, exit 1, no receipt). Exit 1 means unmet, not unevaluable (2). Separately, M33 is a crash-kill in both v1 and v2.
- **D9 (C2 receipts).** The v2 counter prints `C2v93` and no counter digest. `base-c2-v1.txt` and `base-c2-v2.txt` carry the same label and differ only in the hand counts and detail; a reader cannot tell the counter version from the label.
- **D10 (C2 basis).** The freeze's RFC basis for M40 is §5.6.1; OWS/HTAB is defined in §5.6.3. §5.6.1.2 is a MUST-accept rule for empty list elements, which contradicts the frozen `refuse/empty-member` case and makes M20 an RFC-conforming mutant that the instrument kills. Not disclosed.
- **D11 (freeze wording).** "C1 reads committed prose and SKILL bytes only": the counter also reads its predecessor, its frozen surfaces file, and itself from the working tree. The predecessor digest is clean at HEAD (`4e25b72e…` = committed), so no current effect; the freeze should say so.
- **D12 (freeze digest table).** The round-93 counter digests (`c93_conditional.py` `fee28ea0…`, `c93_selfassess.py` `4e25b72e…`) are not pinned in `instrument-sha256.txt`. Both are unchanged since `bb8012fe` (`git log -1 -- …`), so no current effect.
- **D13 (C1, minor).** E3 checks only the first `source:` line of each knowledge entry.
- **D14 (provenance).** The round-93 base commit `191dd0ed` and the executor's clone-only `6d75ee0c` are not in the lane; the mutant measurements are reproducible only from bytes plus the patch list.

## 7. Limits

- I did not evaluate a C1 repair: `w1/ExecC1Repair/skill.diff` was absent at my last check. Section 3.1 is the rule for the L1.
- I did not check S477/S478 (ExecSourceRows in progress). The freeze's RFC row claim for M37/M40 is supported by the scout copy of §9.1, not by a verified registry row.
- The RFC text is the scout's copy (sha256 `21c1cdce…`); I did not re-fetch it. Scout receipts (status, byte count, access date) are the scout's to report.
- My 31/39 numbers are from my own run of the counters against the pos-good base; they agree with the executor's independent run (`ExecC2Mutants.md`, `mutants-v1.json`, `mutants-v2.json`).
- The 28,512-input grid is not exhaustive; the executor's 115,200-case product is. The analytic argument (section 2.1) is the actual proof; both agree.
- "Battery 8/8" and the predecessor-admit count were taken from the counter's own output; I did not re-derive the predecessor's per-route verdicts beyond the counter's line 1.

## 8. Commands and exit codes (summary)

- `python3 -B .ufo/waves/round-94/c94_selfassess.py --root <lane> --revision 0f7d9bbc --work <s>` → rc 1 (`mismatches=15`).
- `python3 -B .ufo/waves/round-94/c94_selfassess.py --root <lane> --revision ba667b24 --work <s>` → rc 1.
- `python3 -B .ufo/waves/round-94/c94_selfassess.py --selftest` → rc 0 (9/9).
- `python3 -B .ufo/waves/round-94/c94_conditional.py --root <lane> --revision ba667b24 --work <s>` → rc 0 (53/53, 120/120, met=true).
- `python3 -B .ufo/waves/round-93/c93_conditional.py --root <lane> --revision ba667b24 --work <s>` → rc 0 (44/44, 120/120, met=true).
- `python3 -B .ufo/waves/round-94/c94_conditional.py --selftest` → rc 0 (7/7).
- `python3 -B c2-kill-drive.py` (scratch) → v1 31/40, v2 39/40.
- `python3 -B c2-m11-equivalence.py` (scratch) → rc 0, differing 0 over 28,512 inputs.
- `git cat-file -t 191dd0ed` → rc 128.
- `git show 0f7d9bbc:scripts/conditional_eval.py | sha256sum` → `d3bac7de…`.
- Scratch-clone SKILL variants X1-X5 (commits `376967c6`, `284f2003`, `bb83c67c`, `2b5a49e6`, `5ed35f62` in the clone only) → rc 1, 1, 1, 0, 0 (section 3.2).
- `--skip-battery` on `2b5a49e6` → rc 0, met=true with battery 0/8.

Receipts are under `.ufo/waves/round-94/w1/CriticClaims/`. Scratch root `/fast/scratch/hyaku/kake-r94/CriticClaims/` is deleted before yield.
