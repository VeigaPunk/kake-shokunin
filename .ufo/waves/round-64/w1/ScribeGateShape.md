# ScribeGateShape — round-64 lesson Gate shape audit (seat report)

Seat: w1/ScribeGateShape · date 2026-10-30 · read-only audit, no lane tree
edits. Every command below was run verbatim; scratch tree
`/fast/scratch/hyaku/kake-r64/ScribeGateShape/` was deleted after the report
was written (nothing needed keeping).

## Scope

Audit the `## Gate` section of `corpus/lessons/round-64.md` (at measured
revision `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, identical bytes at
green-after `cc8add1fa740b920ea5179a71152680ab220c70c`) against
`/home/vgpnk/Projects/shokunin/LEARNING.md` clause by clause, and confirm the
Gate carries everything `.ufo/waves/round-64/c64_calibration.py`'s
`lesson_gate` binds — the binding's ground truth.

Ground truth files (committed, frozen):

- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md`
  (at `4c8295fa`; working-tree copy byte-identical: `git show
  4c8295fa:corpus/lessons/round-64.md` sha256
  `b4ac2fbd4ca77fdb66c54ce514719d743127b1c895b2d044e564609a796b1271`,
  identical at `cc8add1f`).
- `/home/vgpnk/Projects/shokunin/LEARNING.md` (fleet root).
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py`
  (sha256 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`,
  verified against the contract freeze — `sha256sum` matches).

Gate section extent: lesson lines **46–101** (from `## Gate` at line 46 to
the `## Sources census` heading at 102, extracted with the counter's own
`section()` regex, `c64_calibration.py:165-168`).

## Binding ground truth — what `lesson_gate` requires

`c64_calibration.py:252-259` — the Gate section must contain, as substring
tests over the revision blob:

| # | token | defined at | in lesson at |
|---|---|---|---|
| 1 | `"S432 / Fetch"` | `c64_calibration.py:255` | round-64.md:95 |
| 2 | `SPOT_VERDICT_SPAN` = "is only a generic lead-in, not substantive evidence for a response-header expectation" | `c64_calibration.py:78-81` | round-64.md:95 |
| 3 | `"collapsed-only"` | `:257` | round-64.md:58, 99 |
| 4 | `"c64_calibration.py"` | `:258` | round-64.md:54 (line 8 is outside the Gate) |
| 5 | `"author-side"` **or** `"self-assessment"` | `:259` | round-64.md:100–101 (both present) |

Empirical confirmation (commands run from the lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
revision=4c8295fa... disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok
derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1
lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 1a48131577ba82c967650561be34e8dba909432a
... lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision cc8add1fa740b920ea5179a71152680ab220c70c
... lesson_gate=1 ... met=true
exit=0

$ python3 -B .ufo/waves/round-64/c64_calibration.py --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ScribeGateShape/selftest
selftest 26/26   (exit=0)
```

So the binding's ground truth holds: every token the counter requires is in
the committed Gate, and the machine binding discriminates base (lesson_gate=0)
from measured (lesson_gate=1).

## Clause-by-clause verdict

### 1. ≥1 admit and ≥1 reject, each with reasons — PASS

- LEARNING.md:14–15: "Every rejection is logged with its reason"; LEARNING.md:69–70:
  the lesson "carries a `## Gate` section: candidates considered, admitted,
  rejected (with reasons)".
- Admit: round-64.md:53–70, `- **Admit (a):** …` — gives component-by-component
  reasons (pins, recipe re-execution, `collapsed-only` re-derivation, located
  range `6150-6154`, unmasked `unresolved`, block-level prose gates) and lists
  the five control fixtures with their expected failures (lesson lines 66–70).
- Reject: round-64.md:71–79, `- **Reject (b), kept rejected:** …` — reason:
  the standing historical-gate list already exists as the SKILL.md gate-registry
  `Kind` labels plus `c60_gate_status.py` (28 members, 76-check selftest); a
  second list "would duplicate the registry without adjudicating anything new".
- One reject is the minimum; the (c) candidate is rejected inside
  "Assimilation: none." (round-64.md:80–82) with reasons but without a reject
  heading or a flip — see clause 2.

### 2. A flip condition on the reject — PASS

- round-64.md:76–79: "Flip: a gate found red on a later tree whose registry
  row carries no `historical`/`never met` label — the exact failure the
  round-60 relabel pass closed for the 28 known members." Concrete,
  falsifiable, and it names the precedent failure class.
- Ground-truth note: LEARNING.md itself demands only a reason per rejection
  (LEARNING.md:14–15); the flip requirement is lane convention
  (`CORPUS.md:101–102` — rejected rows read `REJECTED: <reason>; flip:
  <what would change the verdict>`; fleet prompt template "Rejections stay as
  rows with reason and flip", e.g.
  `/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-39.md:51-52`). The
  reject (b) satisfies both readings. The assimilation entry (candidate (c),
  round-64.md:80–82) carries reasons but no flip; precedent round-63.md
  (at `1a481315`) likewise gave (c) no flip while (b)/(c) rejects did. Minimum
  met; no defect.

### 3. The outside verdict recorded — PASS (with a scoping observation)

- round-64.md:93–101, `**Outside verdict:**` paragraph: records the round-61
  non-author spot-check `Disagree` on the S432 admission, names its file
  `corpus/lessons/round-61-verifier-spotcheck.md`, and quotes its reason. The
  quoted span is a verbatim substring of the actual round-61 verdict cell:
  `corpus/lessons/round-61-verifier-spotcheck.md:33` (at `4c8295fa`) reads
  `| S432 / Fetch | Admit | … | Disagree | “Web developers and conformance
  checkers must use the following” is only a generic lead-in, not substantive
  evidence for a response-header expectation. …` — the lesson quotes the tail
  of that reason exactly (token 2 above), so the recorded outside verdict is
  the actual recorded verdict, not a paraphrase.
- Observation (for the judge, not a defect I can rule on): the recorded
  outside verdict is the **round-61** spot-check — the routed disagreement
  this round resolves — not a round-64 spot-check verdict. LEARNING.md:42–45
  has each round's non-author spot-check "record agree/disagree with a reason
  in the round's lesson"; LEARNING.md:69–70 lists "the spot-check result" as
  Gate content. The lesson handles this explicitly: round-64.md:100–101
  "This round's own gate decisions (admits/rejects above) are author-side
  self-assessment; the round-64 non-author closure decides agreement." This
  matches the lane's established sequencing — round-63.md §Gate made the same
  deferral and the verdict then landed as
  `corpus/lessons/round-63-verifier-spotcheck.md` (commit `1a481315`);
  `corpus/lessons/round-64-verifier-spotcheck.md` does not exist yet (only
  `round-64.md` matches `round-64*` in `corpus/lessons/`, verified by ls).
  Strictly, clause 3 of LEARNING.md:69–70 is carried by the round-61 verdict
  reference alone until closure lands; the lane pattern treats closure as the
  recording point. Flagged so the closure wave is not skipped.

### 4. The author-side label present — PASS

- round-64.md:100–101: "This round's own gate decisions (admits/rejects
  above) are author-side self-assessment; the round-64 non-author closure
  decides agreement." Both alternatives the counter accepts (`author-side`
  and `self-assessment`) are present. Matches LEARNING.md:42 "Self-assessed
  taste is not discernment" — the lane labels its own assessment instead of
  claiming outside validation it does not have. Machine-bound at
  `c64_calibration.py:259`.

### 5. Candidates enumerated (a)/(b)/(c) — PASS

- round-64.md:48–51: "Candidates considered this round: (a) re-entry of the
  round-63 S432 resolution as calibration evidence under the repaired
  counter; (b) `considerthese/2026-10-26.md` proposal 5 (a standing
  historical-gate list); (c) the `merge/kake/` assimilation package." Each
  enumerated candidate is then dispositioned: (a) admitted (53–70), (b)
  rejected with flip (71–79), (c) assimilation none (80–82).

## What the machine binding does NOT carry (limits, for the judge)

The counter binds exactly the five tokens above. It does **not** bind: the
presence of `Admit`/`Reject` labels, the reasons, the `Flip:` line, the
`**Outside verdict:**` heading, the candidates enumeration, or that the
tokens appear in the same sentence/bullet. Consequences, both exercised by
the committed instruments:

- Marker prose satisfying 4/5 tokens fails only on the verdict span:
  `MARKER_LESSON` (`c64_calibration.py:323`) is
  `"## Gate\n\nplanted gate marker: S432 / Fetch resolved collapsed-only by c64_calibration.py author-side"` →
  `control-marker.txt` shows `lesson_gate=0 unresolved=1 met=false` (exit 1).
  The verdict span is the load-bearing anti-marker token.
- A fabrication that does contain the exact span flips `lesson_gate` to 1:
  selftest case t5 (`c64_calibration.py:392-402`) builds a lesson with
  `"outside verdict: S432 / Fetch " + SPOT_VERDICT_SPAN + " — "` →
  `t5 gate1 … unresolved0 … metfalse` (exit 1 overall). So the Gate-shape
  binding is necessary but not sufficient; C1's falsifiability rests on the
  byte pins + recipe re-execution + located re-derivation, not on Gate prose.
  This is exactly the division of labor the contract's separability section
  describes, and it is why this seat audits the remaining shape clauses in
  prose (this report).

Structural gate cross-check (lane's own shape instrument, read-only by
construction): `node scripts/corpus-contract.mjs --json --root .` →
`ok=true code=0 counts={knowledgeChecked:58, lessonsChecked:59} findings=[]`
— `corpus/lessons/round-64.md` carries a non-empty level-2 `## Gate` section.

## Verdict

Gate shape: **PASSES** all five audited clauses (admit+reject with reasons;
flip on the reject; outside verdict recorded; author-side label; candidates
(a)/(b)/(c) enumerated), and the Gate carries all five tokens
`c64_calibration.py`'s `lesson_gate` binds, verified in-counter
(`lesson_gate=1` at `4c8295fa` and `cc8add1f`, `lesson_gate=0` at base
`1a481315`, selftest 26/26). One observation for closure: the Gate's outside
verdict is the round-61 spot-check; the round-64 non-author spot-check result
is deferred to closure per lane pattern and must land as
`corpus/lessons/round-64-verifier-spotcheck.md` for LEARNING.md:42–45 to be
fully carried by round 64. Nothing in this audit warrants `unprovable` on C1.

## Touched surfaces

- Wrote only this report:
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/w1/ScribeGateShape.md`.
- Scratch `/fast/scratch/hyaku/kake-r64/ScribeGateShape/` (lesson blob
  extracts, selftest fixtures) — deleted before yielding.
- No git/jj mutations anywhere; lane working tree untouched (only reads via
  `git -C … show` and file reads; the counter runs used `git show` internally
  and temp dirs under /tmp).
- No tools installed (none needed).
