VERDICT: C1 is falsified by construction — three fixture revisions that do none of the work the
claim names read `met=true`, exit 0 (different-gate execution, registry row pointing at a
refusing counter, constant-label harness). C2 is separable from C1 in both directions but is a
case-agreement test, not a conformance test: a lookup table over the counter's own population and
a subject whose refusals carry the wrong message both read `met=true`, and the counter's
reference contradicts contract clause 4. The do-nothing control is clean: neither counter reads
`met=true` at the freeze revision.

# CriticClaims — round 92: the two claim predicates, falsified before the L1 measures them

Freeze `a5640ca02c20f94a0fa03af41b977b46ae99808e`; base
`e143faff1b86aad172dd87696da900c70347b8b2`. Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Per-test detail:
`.ufo/waves/round-92/w1/CriticClaims/{C1.md,C2.md,Controls.md}`.

## Readings (all on committed bytes; all receipts under `w1/CriticClaims/receipts/`)

| Fixture | Contents | C1 line (exit) | C2 line (exit) |
|---|---|---|---|
| freeze `a5640ca0` | nothing | `open=3 closed=0 battery=hit differential=fail self=ok met=false` (1) | `candidate=absent … met=false` (1) |
| base `e143faff` | round-91 tip | `open=3 closed=0 … self=hit met=false` (1) | `candidate=absent … met=false` (1) |
| **F1** `333230ce` | C1 artifacts only; runner+log execute a **decoy gate**, receipt digest names the real gate | `open=0 closed=3 battery=exact differential=ok self=ok met=true` (**0**) | `candidate=absent … met=false` (1) |
| **F2** `605a0026` | F1 with the registry row naming `c92_refuse_all.py` (refuses every revision) | `… met=true` (**0**) | — |
| **F3** `3ae41588` | F1 with `run_controls.sh` printing the nine labels from constants | `… met=true` (**0**) | — |
| **F4** `d8affc1b` | `scripts/heuristic_freshness.py` only, no C1 artifact | `open=2 closed=1 battery=hit … met=false` (1) — item C closed anyway | `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` (**0**) |
| **F5** `1e819995` | F4 with refusal text `boom:` instead of `invalid_input:` | — | `… met=true` (**0**) |
| **F6** `b0e04ed1` | verbatim lookup table over the counter's 28+120 inputs, no clause implemented | — | `… met=true` (**0**) |

## Findings

| id | Claim | Finding | Evidence |
|---|---|---|---|
| C1-D1 | C1/A ← K91-1 | Item A binds the receipt digest to `scripts/cache_key_conformance.py` but never binds the **execution** to it: the runner is invoked with no gate argument and only one mutant is sampled (`sorted(verdicts)[0]`, `c92_defects.py:155,159`). A real execution log over a decoy gate reads `met=true`. K91-1 closes only in its "no execution at all" form (FB), not in its "execution of something else" form. | F1 `met=true`; `A_observed` has exactly `base` and `M01` |
| C1-D2 | C1/B ← K91-2 | Item B is a substring test on one `SKILL.md` line (`:185–189`): a row that names `c92_defects.py` only as superseded, and points at a counter that exits 1 for every revision, reads `met=true`. | F2 `met=true` |
| C1-D3 | C1/C ← K91-5 | Item C asserts the label **set** (`:214`) and cannot tell computed labels from constants; the battery's FD only tests *wrong* labels. | F3 `met=true` |
| C1-D4 | C1/C | Item C is not revision-bound: `run_controls.sh:15` resolves `CARRIER` from `git rev-parse master`, and `clone_at` (`:112–115`) pins the scratch clone's `master` to the root's, not to `--revision`. At F4 (no C1 artifact) item C still closed. The harness comment "nine revision-bound label lines" (line 4) is false. | F4 `open=2 closed=1` |
| C1-D5 | C1/self | `self_ok` compares the pin **at rev** to the counter **at rev** (`:399–402`); both live in the same tree, so a coordinated edit reads `self=ok`. No external digest record exists in the freeze file or controls. | code reading |
| C1-D6 | C1/self | `self=ok` already at the freeze, before any wave work. | `receipts/dn-c1.out` |
| C1-D7 | C1/differential | The differential's `met=true` from `c91_defects.py` comes from round-91 bytes; c91's constants (`:51–58`) name no round-92 path. It proves c91 ignores round-92, not that c91 admits a canned round-92 runner. | `f1-c1.out` `differential.c91_on_FB` |
| C2-D1 | C2/contract | The counter's reference accepts a quoted delta-seconds argument (`max-age="120"` → `explicit`, 120) while contract clause 4 requires a refusal; no hand or generated case covers it, so the pre-score reference self-check cannot catch it. | reference run, quoted in C2.md §3 |
| C2-D2 | C2/refusal | Refusal cases are exit-code-only: `score_subject:407` counts any `got is None`, and `run_subject` returns `None` for any non-zero exit. Stderr text and empty stdout are unchecked. | F5 `met=true` |
| C2-D3 | C2/anti-table | The anti-table scans hand-case input **digests** (`:507`) and forgery stems (`:511`) only; the 120 generated inputs (public default seed 92, `:436`) are not scanned, and a verbatim table of inputs is not a digest hit. | F6 `met=true` |
| C2-D4 | C2/population | The generated population is a fixed function of a public default seed — a population, not a hold-out. | `generate()` + `--seed` default |

## What the claims may honestly say

- **C1** (if it passes): "at `<REV>` the artifacts exist, one sampled mutant's real execution
  differs from base, a `SKILL.md` line mentions the counter with `--revision`/`met`, the harness
  prints the nine labels, five fixture classes are discriminated, and the counter equals the pin
  committed beside it." It **cannot** say the shipped gate's mutation score is real, that the
  registry points at a working counter, that the nine labels were computed from runs, or that
  the counter equals the frozen instrument. Wording that says "K91-1 closes" (or K91-5) fails the
  freeze's own kill rule as written: the admitted class is still admitted, one level up.
- **C2** (if it passes): "a subject agrees with this counter's reference on 28 hand cases and
  120 seeded generated cases, carries no hand-case digest and no forgery stem, and the five
  frozen forgeries are refused under the sandbox." It **cannot** say the contract is
  implemented (F6), that refusals carry the contract's message (F5), that the reference is
  contract-faithful (C2-D1), or that the subject generalises past seed 92.

Smallest safe correction (wording, not an edit to any frozen file): re-word both claim sentences
to the honest forms above, and route C1-D1…C1-D7, C2-D1…C2-D4 to the round's routed list. The
frozen counters stay unedited and are not repaired after scoring.

## Exact commands

```
# do-nothing at the freeze
python3 -B "$S/clone/.ufo/waves/round-92/c92_defects.py"  --root "$S/clone" --revision a5640ca02c20f94a0fa03af41b977b46ae99808e --work "$S/work-dn/c1"
python3 -B "$S/clone/.ufo/waves/round-92/c92_heuristic.py" --root "$S/clone" --revision a5640ca02c20f94a0fa03af41b977b46ae99808e --work "$S/work-dn/c2"
# fixtures (same shape, --revision = the fixture commit)
python3 -B "$S/clone/.ufo/waves/round-92/c92_defects.py"  --root "$S/clone" --revision <F1|F2|F3|F4> --work "$S/work-<tag>"
python3 -B "$S/clone/.ufo/waves/round-92/c92_heuristic.py" --root "$S/clone" --revision <F1|F4|F5|F6> --work "$S/work-<tag>"
```

Exit codes: freeze/base 1 and 1; F1 0; F2 0; F3 0; F4 C1 1 / C2 0; F5 0; F6 0.

## Rebuild recipe (fixture commits lived in the deleted scratch clone)

```
S=$(mktemp -d /fast/scratch/hyaku/kake-r92/rebuild.XXXX)
git clone -q --shared LANE "$S/clone"
git -C "$S/clone" checkout -q --detach a5640ca02c20f94a0fa03af41b977b46ae99808e
git -C "$S/clone" checkout -q -B f1
mkdir -p "$S/clone/.ufo/waves/round-92/integration"
cp W1/receipts/fixture-sources/{gate-copy.py,mutate-tip.py,mutation-tip.log,mutation-tip.txt} \
   "$S/clone/.ufo/waves/round-92/integration/"
cat W1/receipts/fixture-sources/f1-skill-row.txt >> "$S/clone/SKILL.md"
git -C "$S/clone" -c user.name=fixture -c user.email=fixture@scratch.invalid add -A
git -C "$S/clone" -c user.name=fixture -c user.email=fixture@scratch.invalid commit -qm "fixture F1"
git -C "$S/clone" update-ref refs/heads/master "$(git -C "$S/clone" rev-parse HEAD)"
# F2: replace the row with f2-skill-row.txt, add f2-c92_refuse_all.py
# F3: replace controls/run_controls.sh with f3-run_controls.sh
# F4: from a5640ca, add scripts/heuristic_freshness.py = f4-heuristic_freshness.py
# F5/F6: same, with f5-/f6-heuristic_freshness.py
```

Rebuilt commit ids will differ (timestamps); the counter reading is what the receipts record.
`W1` = `.ufo/waves/round-92/w1/CriticClaims`.

## Lane state and bounds

- No commit, push, stage or mutating git/jj in LANE. Fixture commits were made only in the
  scratch `--shared` clone, with `-c user.name=fixture -c user.email=fixture@scratch.invalid`,
  after asserting `git -C "$S/clone" rev-parse --show-toplevel` equalled the clone.
- No frozen file edited: `c92_defects.py`, `c92_heuristic.py`, `c2-contract.md`, `frozen/` and
  `controls/run_controls.sh` were read and executed only.
- Writes: only `.ufo/waves/round-92/w1/CriticClaims/` (this report, the three seat files, and
  `receipts/`). No fleet-root, `MANIFEST.json`, `.ufo/state`, `.scratch`, template, sibling-lane
  or shokuknow write.
- Scratch root `/fast/scratch/hyaku/kake-r92/CriticClaims/` was deleted after the receipts were
  copied; nothing under `/tmp` was used as a tree.
- Tooling: nothing installed or upgraded (pacman paused; no uv/npx/binary install was needed).
- No subagents dispatched (leaf seat).

## Honest limits

- The live wave was writing the LANE working tree during this seat (an uncommitted
  `c92_defects.py` row appeared in `SKILL.md`). Every reading here comes from git objects at a
  revision, never the working tree; a run with `--root LANE` would still read git objects, but
  the L1 should keep using `--revision`.
- C1-D5 (coordinated counter+pin edit) is a code reading, not a fixture: a forged counter that
  still discriminates the battery is outside this seat.
- F6 imports the counter's reference at fixture-build time; it demonstrates the predicate's
  reach, not that any wave seat did this.
- I did not attempt to make C1 read `met=true` at the freeze by manipulating `master` to a
  revision that already satisfies A and B; C1-D4 already shows item C would close, and A/B
  cannot close without the artifacts.
