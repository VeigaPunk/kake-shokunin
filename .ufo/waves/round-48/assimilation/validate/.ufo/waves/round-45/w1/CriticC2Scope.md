# CriticC2Scope — C2 composition and receipt-identity attack

## Axes and result

- **Judged axis: freshness.** Operability is the lane's other axis, not independently scored by this review.
- **Named attack: PASS — counterexample found. Composition: UNSOUND as frozen.** The defect is false receipt provenance, not merely having three measurements in one conjunction.
- The declaration specifies one command and explicitly requires all three after-values simultaneously: `after=(4/4, false, 22/1/4)` (`SCORECARD.md:3697-3701`, checked at frozen revision `3b4c430a`). There is no averaging or optional leg in that sentence. A three-component freshness repair can be presented as one compound target; this review establishes no separate rule that the component count alone makes three smuggled claims. One wrapper command also would not prove common causality or confer three credits. Claim sizing/admission belongs to the canonical judge.
- **Actual one-command coverage is unproved:** the frozen counting command exits 2 because `c45_freshness.py` is absent. No implementation-level false-green was observed, and no actual MET was produced.
- **The strongest local counterexample is already committed:** the final, 27-witness claim receipt partitions as **26 class-only + 1 mixed + 0 met**. The required **22 + 1 + 4** belongs to the earlier, 23-witness/pre-G6 receipt. Substituting that earlier receipt satisfies the numeric split component while making the stated final-receipt leg false.

## Evidence and interpretation

The frozen declaration is the authority, not the wave proposal. `git show 3b4c430a:SCORECARD.md` and the current ranged read agree on the relevant text:

- `SCORECARD.md:3681-3689`: the sentence begins with two standing self-claims, joins repairs (a)/(b), then adds `; and (c) the round-44 claim receipt's 27 witnessed controls re-derive as 22 class-only + 1 mixed + 4 met`.
- `SCORECARD.md:3697-3701`: one frozen command prints all three metrics; `Claim MET iff after=(4/4, false, 22/1/4)` is conjunctive.
- `SCORECARD.md:3602-3611`: the final round-44 claim receipt is explicitly `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`, with witnessed 27/27.
- `c44_audit.py:63-66,167-168,199-200`: a semantic witness requires `met is False` and a class key. Therefore class-only + mixed = witnessed; four met controls cannot also be four of the 27 witnessed controls in a coherent 27-control receipt.
- The original `round-44/w2/CriticC1Predicate.md:8,41,101-126` identifies the earlier `verification/claim/after-v5.json`, explicitly reports **23/27**, and qualifies its 22-class-only/one-mixed result. Importing its numbers into the final cohort changes identity.
- Proposal data `round-45/make_w1_spec.py:256-268` independently exposes the mismatch: it points its jq command at `after-final/after-v5.json` but expects 22/1/4. This proposal does not supersede the frozen contract.

### Decisive command: final committed claim receipt

Working directory for every command below: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json | jq -c '{receipt:"3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json",witnessed:.witnessed,split:(.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length,mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length,met:map(select(.met==true))|length,other:map(select(.met==false and (.classCaught|length)==0))|length})}'
```

Verbatim stdout (exit 0):

```text
{"receipt":"3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json","witnessed":27,"split":{"class_only":26,"mixed":1,"met":0,"other":0}}
```

### Decisive command: earlier committed receipt

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json | jq -c '{receipt:"3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json",witnessed:.witnessed,split:(.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length,mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length,met:map(select(.met==true))|length,other:map(select(.met==false and (.classCaught|length)==0))|length})}'
```

Verbatim stdout (exit 0):

```text
{"receipt":"3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json","witnessed":23,"split":{"class_only":22,"mixed":1,"met":4,"other":0}}
```

### Receipt fingerprints

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-final/after-v5.json | sha256sum
```

Verbatim stdout (exit 0):

```text
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  -
```

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json | sha256sum
```

Verbatim stdout (exit 0):

```text
2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902  -
```

### Constructed false-green state: numeric predicate only

[INFERENCE] Suppose the real repaired selftest and v4 receipt satisfy (a)/(b). A wrapper that takes (c)'s split from the earlier receipt, without enforcing the final receipt identity, obtains the exact declared after tuple while the final-claim leg is false. This is a counterexample to a value-only interpretation of the written iff, **not** a demonstrated bug in the absent runner. It also need not edit any frozen receipt, so a frozen-byte guard alone does not reject it.

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json | jq -c '(.rows | [(map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length),(map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length),(map(select(.met==true))|length)]) as $split | {kind:"conditional predicate model; not c45_freshness execution",source:"3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json",source_witnessed:.witnessed,split:$split,tuple_MET_if_a_and_b_true:($split==[22,1,4]),source_has_27_witnessed_controls:(.witnessed==27)}'
```

Verbatim stdout (exit 0):

```text
{"kind":"conditional predicate model; not c45_freshness execution","source":"3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json","source_witnessed":23,"split":[22,1,4],"tuple_MET_if_a_and_b_true":true,"source_has_27_witnessed_controls":false}
```

### Frozen counting command dependency

```sh
python3 -B .ufo/waves/round-45/c45_freshness.py
```

Verbatim stderr (exit 2):

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_freshness.py': [Errno 2] No such file or directory
```

The declaration promises one command covering all legs; no available command implementation demonstrates that promise, its simultaneous checks, receipt identity binding, or the requirement that the split actually be filed in SCORECARD. I did not wait for another seat or rerun the absent command.

## Smallest safe correction and exact sentence boundary

**Current frozen round:** preserve the declaration and receipt bytes, disclose the mismatch, and do not treat the requested tuple as evidence about the final cohort. This is a fixable provenance/reporting defect, but accepting a wrong receipt or silently changing the frozen expected tuple is not a permissible implementation tradeoff. Any acceptance change requires the canonical owner's explicit handling; this critic makes no admission judgment.

**Exact boundary for a future sound two-repair declaration:** end the claim at `SCORECARD.md:3687`, immediately after **“predicate names only the eleven v4 runs”**. Replace the following **`; and (c)`** with a period, and make the historical clarification its own explicitly non-credit sentence:

> Historical clarification, not an additional claimed repair: the pre-G6 receipt `.ufo/waves/round-44/verification/claim/after-v5.json` at `3b4c430a` contains 27 controls, of which 23 are witnessed (22 class-only + 1 mixed) and 4 are met; the final claim receipt `.ufo/waves/round-44/verification/claim/after-final/after-v5.json` at the same revision contains 27 witnessed controls (26 class-only + 1 mixed) and 0 met.

The corresponding future two-repair MET condition must then cover (a)/(b), rather than quietly retaining the detached 22/1/4 target. This is a proposed new sentence boundary, **not** a post-freeze scope reduction performed by this seat.

If the owner instead retains all three legs in one compound target, the sound future (c) must explicitly name the final receipt/revision/hash and require **26/1/0**, `other=0`, and filing of the matching split and command. A runner must derive those values from that identity, not trust a cached `split.json` or select whichever receipt yields the desired tuple. Merely replacing the counts without provenance leaves the counterexample class open. The common freshness axis does not authorize silent source substitution.

## Work, commands, files, and blockers

- Created the required scratch directory with `mkdir -p /fast/scratch/hyaku/kake-r45/CriticC2Scope` (exit 0, no output); it remains empty.
- Executed `git show 3b4c430a:SCORECARD.md` (exit 0); read its relevant frozen section and the current ranged declaration, the original witness critique, audit witness semantics, and the proposal's split command. Other exact shell commands and decisive output are recorded above.
- One failed scratch-free jq model attempt preceded the successful model. Exact command:

```sh
git show 3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json | jq -c '(.rows | [map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length,map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length,map(select(.met==true))|length]) as $split | {kind:"conditional predicate model; not c45_freshness execution",source:"3b4c430a:.ufo/waves/round-44/verification/claim/after-v5.json",source_witnessed:.witnessed,split:$split,tuple_MET_if_a_and_b_true:($split==[22,1,4]),source_has_27_witnessed_controls:(.witnessed==27)}'
```

Verbatim stderr (exit 5):

```text
Error: cannot use 22 as iterable (array or object)
```

  Parenthesizing each array element corrected jq precedence; this failed attempt is not evidence against the repository.
- Sent short provenance warnings to `kake-r45.ExecWitnessSplit` and `kake-r45.ScribeDeclarations`; no response was required or awaited.
- **Every file written:** `.ufo/waves/round-45/w1/CriticC2Scope.md` only. No code, fixtures, frozen receipts, ledger, corpus, or sibling-owned draft was changed; no git commit/push or other orchestration runtime was invoked.
- **Tools installed/updated:** none. Read the required tool-install rules; no package transaction was needed.
- **Blocker:** missing `c45_freshness.py`. Full three-leg execution, v2 mutant tests, v6 receipt regeneration, and SCORECARD integration checks were not run by this seat. Reachable committed-byte provenance and predicate-model attacks are complete.
