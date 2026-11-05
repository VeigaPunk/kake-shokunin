# QUALITY.md criteria — round 95 (draft for the L1)

Seat: ScribeEntry (kake round 95, wave `w1`, 2026-11-05). Draft only; the L1
integrates. These are three new `## Round 95 — ...` sections for
`corpus/QUALITY.md`, in the file's established style (a `Grounding:` line that
names the lesson file and its routed item, then the rule, then the falsifier).

**Integration note (ordering constraint the L1 must honour).** The frozen C1
counter audits every `## ` section of `corpus/QUALITY.md` whose heading
matches `Round[- ]\d+` and whose body contains the string `criteri`: it
requires each such section to cite a `corpus/lessons/...` path that exists as a
**non-empty blob at the measured revision**
(`c95_selfassess.py`, E2 check; the base control reports
`controls/base-c1.txt` `criteria=39`, `E2=0`). The three sections below each
name `corpus/lessons/round-95.md`, so that lesson file must land **in the same
commit or earlier** as these sections. If `corpus/lessons/round-95.md` is not
present when the QUALITY sections are added, the C1 counter raises an E2
finding (`section 'Round 95 — ...' cites missing corpus/lessons/round-95.md`)
and the C1 claim's target (`mismatches=18 → 0`) becomes unreachable through
the declared repair route. The lesson skeleton drafted by this seat is
`corpus/lessons/round-95.md` in the same wave directory, so both can land in
one integration commit.

A second ordering constraint: the C1 counter's identity surface pins the
**head-8-line digest** of every base knowledge entry and the **full content
digest** of every base lesson. A new lesson file (`corpus/lessons/round-95.md`)
is not a base lesson, so it is not pinned — but the QUALITY sections that cite
it are read at the measured revision, so the file must be a non-empty blob
there.

---

## Round 95 — a counter's `met` conjunct battery covers every rule class the counter enforces

Grounding: `corpus/lessons/round-95.md` Mistakes row 1; round-94 lesson
mistake 10 (the strict counter accepted routes the battery did not cover) and
round-94 routed item R94-7 (the counter's own battery killed only 4 of 12 of
its mutants). This criterion admits a counter's `met` verdict only when the
counter's own battery exercises **every rule class the counter enforces**: for
each finding shape the audit can emit, there must be at least one battery
route that plants that shape and observes the counter refuse it. A battery that
covers the classes it names while leaving a sibling branch of the same class
unexercised does not license `met`; the uncovered branch is a route the counter
can take without the battery noticing. Reject a `met` whose battery count is a
route count rather than a rule-class count — a battery that grows by adding
routes inside the classes it already covers, while a class's other branches
stay unplanted, leaves the same false-green open.

Able-to-fail witness for this round: the frozen C1 counter
`.ufo/waves/round-95/c95_selfassess.py` emits **23 distinct finding shapes**
across E1–E5, and its battery plants **19 defect routes**; 7 of the 23 shapes
have no route that expects them, and all 7 are reachable by the frozen
`audit()` — the uncovered branches are E1 `vacuous Gate: no reject decision
line (route R01)`, E2 `section ... names no corpus/lessons/ file`, E2
`section ... cites missing <lesson>`, E3 `missing source:`, E3
`missing verified-at:`, E3 `missing recheck:`, and E3 `vacuous source: no row
id, URL or path locator`. Receipt: `w1/ScribeEntry/battery_coverage.py`
(run `python3 -B battery_coverage.py`, exit 0), which enumerates the emitted
shapes from the frozen bytes, maps the routes with the counter's own
`fragment in detail` rule, and then builds a scratch fixture for each
uncovered branch and shows the frozen `audit()` really emits it.

The gap is **proved**, not merely enumerated: `w1/ScribeEntry/branch_mutation.py`
(run `python3 -B branch_mutation.py`, exit 0) applies one surgical mutation per
uncovered branch to a scratch copy of the frozen counter, in a lane-shaped side
tree so every battery field stays comparable, and then runs the mutated
counter's own `battery()`. For all seven mutations the battery reads
`battery=20/20 admit=5/5 shadow_absent=1 predecessor_admits=10/19` — byte-for-byte
the pristine verdict — while the mutated branch stops firing. A regression in
any of those seven branches is therefore invisible to the battery that the
`met` conjunct counts.

The class-level reading of this criterion is **satisfied** by the round-95
counter (E1, E2, E3, E4 and E5 each have at least one route), so the finding
refines the criterion to shape level rather than contradicting it: the landed
R95-A wording ("cover every rule class the counter enforces") is true as
written, and the seven uncovered shapes are the same defect one granularity
down. MutC1's survivor M03/M03b (E1-vocabulary) is a **separate** mechanism in
the same family: it mutates the `admit` half of the disjunction and is invisible
to both the battery and the base run, because every fixture satisfies both
alternatives at once.

## Round 95 — a mutant population names its measured base, and the base resolves at measurement time

Grounding: `corpus/lessons/round-95.md` Mistakes row 2; round-94 routed item
R94-8 and round-94 closure item 5 (the population's `base_rev` pointer names
an absent commit). This criterion admits a mutant-population kill count only
when the population **names the base it was measured against** and that base
**resolves at the time the count is read** — either a revision that
`git cat-file -t` resolves in the lane, or bytes pinned by content digest that
are present in the lane. A `base_rev` pointer that names a commit no lane ref
carries is not a base: it makes the kill count unreproducible from the lane,
because the measurement's own starting point cannot be reconstructed. Reject a
kill count whose population pins its base by revision only, and reject a base
that is pinned by digest but whose digest is not re-checkable at the revision
where the count is quoted. The pointer and the bytes are both recorded: naming
the absent revision as unrecoverable is correct and required, and it does not
substitute for naming the bytes the measurement actually ran on.

Able-to-fail witness for this round: the round-93 mutant-scoring receipt
`.ufo/waves/round-93/w1/recovered-partial/MutConditional/posgood-out/mutants.json`
line 7 declares `"base_rev": "191dd0ed0cf594a29668f5862f536a925998cadd"`, and
`git cat-file -t 191dd0ed0cf594a29668f5862f536a925998cadd` → `fatal: git
cat-file: could not get object info`, rc 128 (the round-94 critic recorded
the same rc at `.ufo/waves/round-94/w1/CriticClaims/git-and-digests.out`
lines 3–4). The patch population
`.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json`
carries no `base_rev` at all; it pins its base **by content** —
`base.source = .ufo/waves/round-93/frozen/pos-good.py`, `base.sha256 =
0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4` — and
`git show fdd5fdbe:.ufo/waves/round-93/frozen/pos-good.py | sha256sum` returns
that same digest, so the bytes resolve even though the revision does not.
Receipt: `.ufo/waves/round-95/w1/ExecReceipts/erratum-r94-8.md`.

## Round 95 — a repair that removes a path token names its replacement

Grounding: `corpus/lessons/round-95.md` Mistakes row 3; round-94 routed item
R94-3 (the identity pin covered the row's first cell only, so a repair could
drop a path token) and round-94 lesson mistake 8 (an executor removed the
backticks from directory paths, passing the counter without naming a file).
This criterion admits a repair that removes a path token from a cited row only
when the same repair **names the replacement path**, and the replacement is a
path that resolves to a non-empty regular blob at the revision where the repair
is audited. Removing a token without naming a replacement is not a repair: it
removes the citation without moving the claim onto a checkable target, and it
leaves the row's content weaker than the counter's own finding required it to
be. Reject a repair whose diff shows a path token deleted and no replacement
path added, and reject a replacement that names a tree, an empty blob or a
symlink — the same three shapes the counter's E5 rule already refuses. The
repair is read as a diff, not as a green: a green that follows from the token's
removal is the counter-gaming shape, not calibration.

Able-to-fail witness for this round: the round-94 counter's own identity
surface pinned only the SKILL row's **first cell**, so
`.ufo/waves/round-94/w1/ExecC1Repair/skill.diff` (13 directory rows losing
their backticks) read `mismatches=0 … met=true` while naming no blob at all —
the counter could not distinguish the gaming route from a repair
(`.ufo/waves/round-94/w1/CriticClaims.md` X4/X5; the diff is kept as evidence
and SKILL.md was reverted to the freeze bytes). The frozen round-95 counter
closes the hole by pinning the **path-token count** per SKILL row
(`.ufo/waves/round-95/c95_selfassess.py`, `skill_row_tokens:` identity
finding, route `B15-row-token-stripped`) and by refusing a named path that is
a tree, an empty blob or a symlink (E5). The C1 base control still reports
`E5=15` at the round base, so the replacement-path rule is live, not
hypothetical: every one of the 15 findings is a row that names a tree and
still needs a concrete non-empty blob named in its place.
