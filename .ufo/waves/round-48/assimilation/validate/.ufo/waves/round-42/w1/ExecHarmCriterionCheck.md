# ExecHarmCriterionCheck — a check for the QUALITY criterion "frozen harm rule names each new fixture's class and a numeric cost bound"

Seat: `KakeR42.ExecHarmCriterionCheck` (executor, leaf). Lane `kake-shokunin`, tip `d1c3f37`. Axis: operability.

## What I built

`harm_rule_check.py <scorecard-path|-> <round>` — reads a SCORECARD's bytes, splits them into
`## Round N — …` sections, selects the round's **pre-freeze / declared** section (heading containing
"pre-freeze" or "declared"; a "pre-freeze" heading wins when several match), extracts that section's
**harm-rule bullet** (a `- ` bullet whose text names the harm rule, plus its indented continuation
lines), and passes only when the bullet

* (a) names the fixture classes — a change fixture *and* a guard (`change fixture`/`red on` and
  `guard`/`green on`), **or** the single-class form (`guards only` or `no change fixture`); and
* (b) gives a numeric cost bound — a ratio (`2.0 times`, `2.0x`, `≤ 2.0`, `at most 2.0`) or a time
  (`250 ms`, `5 s`, `2 seconds`).

Exit **0** pass, **1** fail, **2** cannot evaluate (bytes unreadable, no declared/pre-freeze section
for the round, unparsable round argument). Every matched phrase is printed with its 1-based line
number, so a reader can re-check the verdict by hand. "frozen" is reported as an advisory, not a
gate (the criterion's wording is what it is; the section selection already establishes "before data").

## Paths and sha256

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kake-r42w1/ExecHarmCriterionCheck/harm_rule_check.py` (312 lines) | `df32595dcd60558188eb29095d479349c6a62658a10637242054a936ea9422b1` |
| `…/sc_r41_1ef7a0e9.md` (`git show 1ef7a0e9:SCORECARD.md`) | `c0f026a210eb9ffcd4ffe7f3596b27126b1aed0758431545a49c7e6f5e3e2be1` |
| `…/sc_tip_d1c3f37.md` (`git show d1c3f37:SCORECARD.md`, lane tip) | `8cc3171668f37bd00bc4e50da6790b056c811e5150b29bf6369b8a923290dcc8` |
| `…/sc_base_8eb121c8.md` (`git show 8eb121c8:SCORECARD.md`, round-40 base) | `3b3705f9cc7d028c096e2fc6ba27a977d13d9878feb57bed739a17e0b9d5b5cb` |

## The four runs (all via `timeout 60 python3 -B harm_rule_check.py <file> <round>`)

1. **round 41, `sc_r41_1ef7a0e9.md` → exit 1 (FAIL).** Section line 2672 `## Round 41 — C1 counter
   candidate (pre-freeze: …)` (lines 2672-2754); harm-rule bullet lines 2746-2748. Matched lines:
   2747 `red on` (change class only). No guard naming, no `guards only`, no `no change fixture`; no
   ratio and no time bound. Verdict: "names neither fixture classes nor a numeric cost bound".
   The bullet reads: "passes every fixture (183 plus the round's new ones, which must be red on
   `8eb121c8`), and the round-39 real run is byte-equal (`fd985a41…`)" — no cost bound at all.
2. **round 42, `sc_tip_d1c3f37.md` → exit 0 (PASS).** Section line 2907 `## Round 42 — C1 counter
   candidate (pre-freeze: …)` (lines 2907-2992); harm-rule bullet lines 2976-2987. Matched lines:
   2978 `guards only`; 2979 `change fixture`, `red on`, `no change fixture`; 2980 `change fixture`;
   2981 `guards`, `green on`; 2982 `guard`, `guards`; cost bound 2983 `≤ 2.0`. Advisory: `frozen`
   at line 2976.
3. **round 39, `sc_tip_d1c3f37.md` → exit 1 (FAIL).** Section line 2347 `## Round 39 — C1 declared
   (before any seat is dispatched)` (lines 2347-2416). No harm-rule bullet; the section never
   mentions "harm".
4. **round 40, `sc_tip_d1c3f37.md` → exit 1 (FAIL).** Section line 2548 `## Round 40 — C1 declared
   (before any seat is dispatched)` (lines 2548-2628). No harm-rule bullet; the only "harm" token
   is line 2618 `and wave 2 report it as harm.` (inside the kill-rule paragraph, not a harm rule).

Extra, for the "8eb121c8 style bytes" wording: **round 41 in `sc_base_8eb121c8.md` → exit 2**
(cannot evaluate — those bytes predate round 41 and hold no round-41 section). Round 41's own
declared bytes are `1ef7a0e9` (its base), used in run 1.

## Discrimination check (synthetic, `synth/*.md`, round 90)

Proves the exit codes are not keyed on the file: `both` (change fixture + guard + "2.0 times") → 0;
`classes_only` (classes, no bound) → 1 "no numeric cost bound"; `cost_only` ("at most 2.0 times",
no class naming) → 1 "no fixture class"; `neither` → 1; `guards_only` ("guards only" + "250 ms") → 0;
`time_bound` (classes, no bound) → 1. A decoy `## Round 90 — measured results` section carrying a
harm-rule bullet is ignored: the checker stays in the declared section.

Other exits: missing file → 2; unknown round (77) → 2; unparsable round → 2; no args → 2 (usage);
stdin (`-`) → same verdict as the file.

## Findings (path:line)

* `kake-shokunin/SCORECARD.md:2746-2748` — round 41's harm rule names a change fixture only
  ("must be red on `8eb121c8`"), never a guard class, and carries no cost bound: it fails the
  criterion's two halves.
* `kake-shokunin/SCORECARD.md:2976-2987` — round 42's corrected harm rule satisfies both halves:
  fixture classes named (guards only; no change fixture; the 42 `r41_*` fixtures classified 29 change
  / 13 guards) and a numeric cost bound (`≤ 2.0`, H3).
* `kake-shokunin/SCORECARD.md:2347-2416` and `:2548-2628` — rounds 39 and 40 have no harm-rule bullet
  in their declared sections, so neither can satisfy the criterion (measured, not assumed).

## Per checked statement

* "the checker finds the round's pre-freeze / declared section" — **holds** (runs 1-4 name the
  section and its line range; the round-39/40 sections are the `C1 declared` ones).
* "the checker finds that section's harm-rule bullet" — **holds** for rounds 41 and 42; for rounds
  39 and 40 there is none, and the tool says so with the evidence lines rather than guessing.
* "pass only when it names fixture classes and a numeric cost bound" — **holds** (r42 → 0; r41 →
  1; synthetic `classes_only`/`cost_only`/`neither` → 1).
* "round 41 expected FAIL" — **holds** (exit 1).
* "round 42 expected PASS" — **holds** (exit 0).
* "rounds 39 and 40" — **holds as measured** (both exit 1: no harm-rule bullet in the declared
  section). I did not assume an expected code for these two; the assignment named none.
* Cost-bound reading "a ratio such as `2.0 times` / `≤ 2.0` or a time" — **holds** as implemented;
  a bare comparison is counted as a ratio only when the number is not the head of a time
  ("within 250 ms" is a time, not a ratio). I widened the wording slightly to admit a time bound
  with any unit and to treat `guards only` / `no change fixture` as the single-class form, which the
  task text allows.
* Scope statement "the tool's judgments…" — not applicable; this seat builds a QUALITY-criterion
  checker, not a scored tool. The counter `c42_count.py` was **not** run (build seats never run it).

## Risks / blockers

* The class test is lexical. A harm rule that says "guards" in an unrelated sentence would satisfy
  it; a rule that classifies fixtures with other wording ("red/green on the base" without the word
  "guard") would fail it. Round 42's bullet happens to use both the words and the red/green form.
* Section selection is heading-keyed ("pre-freeze" / "declared"); a future round that titles its
  declaration differently would return exit 2 rather than a wrong verdict.
* No tools were installed or upgraded this seat (nothing needed beyond python3 3.14.8, already
  present); no network access was used; no lane file was mutated except this report.

Report: `.ufo/waves/round-42/w1/ExecHarmCriterionCheck.md`
