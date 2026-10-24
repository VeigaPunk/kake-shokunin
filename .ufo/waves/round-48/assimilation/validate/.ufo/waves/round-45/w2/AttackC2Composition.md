# AttackC2Composition — round 45, wave 2

## Scope and result

Axes: **freshness** (assigned); **operability** is a boundary, not independently rescored.

Named attack: does the C2 **NOT MET as declared** disposition erase verified legs (a)/(b), or inflate those legs into more than their evidence supports?

**Attack FAIL — the composition disposition withstands this attack.** The frozen declaration explicitly requires the conjunction `(4/4, false, 22/1/4)` (`SCORECARD.md:3681–3701`). The measured append explicitly preserves both successful sub-moves: `SCORECARD.md:3767` says, verbatim:

> **Verdict: NOT MET as declared** (conjunctive MET fails on leg (c)); legs (a) and (b) verify.

The append bounds (a) to the same four named mutations (`3747–3752`) and (b) to v4 predicate wording (`3753–3758`); it does not turn them into universal selftest completeness, receipt authenticity, two additional claims, or a numeric score rise. The final summary also preserves the bounded repairs (`3771–3772`). A failed conjunction is not a finding that every constituent failed or that freshness was harmed.

**Separate, fixable freshness defect:** the append cites `verification/selftest-coverage/after/` as evidence for (a), but that directory is empty. The aggregate result exists, so this does not falsify the stated composition or the supplied measured round state; it does overstate what the cited per-mutant after directory retains. See the exact read result below.

## Strongest counterexample tested

Both historical receipts contain 27 control rows. Nevertheless, the final named receipt yields **26/1/0**, while the earlier receipt yields exactly the frozen **22/1/4**. Equal denominator is therefore insufficient to preserve receipt identity. Replacing the final receipt with the earlier one would make leg (c) look true only by changing the named evidence, not by repairing arithmetic. The append identifies both receipts and reports the mismatch rather than using the earlier receipt to green the conjunction.

This is a false frozen receipt attribution, not an observed regression in (a) or (b). Keeping the repaired sub-moves and refusing the full frozen conjunction are compatible. Changing C2 to MET on the strength of (a)/(b) alone would change the claim, not correct a reporting defect. Canonical judgment/admission remains outside this critic's authority.

## Commands and decisive output

All shell commands below ran from `/home/vgpnk/Projects/shokunin/kake-shokunin`; all completed with exit 0. The `jq` commands read existing evidence; none executes the freshness runner or selftests.

### Recorded sub-moves, without hiding the failed leg

```sh
jq -r '"selftest_kills before=\(.selftest_kills.before)/\(.selftest_kills.of) after=\(.selftest_kills.after)/\(.selftest_kills.of)", "v4_predicate_names_class_runs before=\(.v4_predicate_names_class_runs.before) after=\(.v4_predicate_names_class_runs.after)", "witness_split class_only=\(.witness_split.class_only) mixed=\(.witness_split.mixed) met=\(.witness_split.met)"' .ufo/waves/round-45/verification/freshness/freshness.json
```

Verbatim stdout:

```text
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
```

### Conjunction arithmetic against the frozen target

```sh
jq -r '["leg_a_after_matches_frozen=" + ((.selftest_kills.after == 4 and .selftest_kills.of == 4)|tostring), "leg_b_after_matches_frozen=" + ((.v4_predicate_names_class_runs.after == false)|tostring), "leg_c_matches_frozen=" + ((.witness_split == {class_only:22,mixed:1,met:4})|tostring), "conjunctive_frozen_after=" + ((.selftest_kills.after == 4 and .selftest_kills.of == 4 and .v4_predicate_names_class_runs.after == false and .witness_split == {class_only:22,mixed:1,met:4})|tostring)] | .[]' .ufo/waves/round-45/verification/freshness/freshness.json
```

Verbatim stdout:

```text
leg_a_after_matches_frozen=true
leg_b_after_matches_frozen=true
leg_c_matches_frozen=false
conjunctive_frozen_after=false
```

### Direct re-derivation from both historical receipts

```sh
jq -r '[input_filename, "rows=" + (.rows|length|tostring), "class_only=" + ([.rows[]|select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0)]|length|tostring), "mixed=" + ([.rows[]|select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0)]|length|tostring), "met=" + ([.rows[]|select(.met==true)]|length|tostring)]|join(" ")' .ufo/waves/round-44/verification/claim/after-final/after-v5.json .ufo/waves/round-44/verification/claim/after-v5.json
```

Verbatim stdout:

```text
.ufo/waves/round-44/verification/claim/after-final/after-v5.json rows=27 class_only=26 mixed=1 met=0
.ufo/waves/round-44/verification/claim/after-v5.json rows=27 class_only=22 mixed=1 met=4
```

```sh
sha256sum .ufo/waves/round-44/verification/claim/after-final/after-v5.json .ufo/waves/round-44/verification/claim/after-v5.json
```

Verbatim stdout:

```text
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  .ufo/waves/round-44/verification/claim/after-final/after-v5.json
2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902  .ufo/waves/round-44/verification/claim/after-v5.json
```

### Predicate repair is specifically a text correction

```sh
jq -r '[input_filename, "classesMode=" + .classesMode, "classRuns=" + (.classRuns|length|tostring), "has_class_runs_phrase=" + (.predicate|contains("class runs")|tostring), "predicate=" + .predicate]|.[]' .ufo/waves/round-44/verification/claim/v4-final/v4.json .ufo/waves/round-45/verification/v6v4/counter-v4.json
```

Verbatim stdout:

```text
.ufo/waves/round-44/verification/claim/v4-final/v4.json
classesMode=v4
classRuns=0
has_class_runs_phrase=true
predicate=met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
.ufo/waves/round-45/verification/v6v4/counter-v4.json
classesMode=v4
classRuns=0
has_class_runs_phrase=false
predicate=met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
```

### Referenced individual after evidence is absent

Exact tool invocation:

```text
functions.read({"i":"Inspecting referenced after evidence directory","path":"/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/verification/selftest-coverage/after"})
```

Verbatim output:

```text
(empty directory)
```

The aggregate `verification/freshness/freshness.json` remains available and records after=4/4. This seat did not freshly execute the four mutant selftests, so the absent individual transcripts are reported as an archival dependency, not invented or treated as behavioral failure.

## Smallest safe correction

- **Composition:** none. Retain the full-claim NOT-MET-as-declared disposition and the explicit verified-(a)/(b) sentence. Do not substitute the earlier receipt or promote two successful conjuncts into full MET.
- **Evidence pointer:** append a correction naming the existing aggregate receipt as the retained evidence for 4/4 and explicitly noting that individual after transcripts are not retained in the cited directory. Alternatively, the owner can retain real per-mutant outputs from an authorized replay and cite those; this critic produced no replacement outputs.

## Limits and writes

Unrun by this seat: shipped selftests, mutant executions, full `c45_freshness.py`, matrix runner, build, ledger gate, frozen-byte guard, and canonical judge. The full freshness runner writes into the lane, so it was not invoked under this seat's read-only bounds. No broad no-harm or admission verdict is issued here.

Scratch creation command (exit 0, no stdout):

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/AttackC2Composition
```

Every file written by this seat:

- `.ufo/waves/round-45/w2/AttackC2Composition.md` — this report only.

The scratch directory contains no files created by this seat. No committed file, frozen artifact, routing/state file, or history was edited; no git/jj command, install, or runtime dispatch was performed. Tool installs/updates: none.
