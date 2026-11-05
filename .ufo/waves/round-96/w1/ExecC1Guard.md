# ExecC1Guard report — round 96 (hyaku run 15, attempt 1), w1

Seat: ExecC1Guard. Task: verify the C1 successor's committed verdict survives the wave's
concurrent state and probe the new E1 rule against the real round-95/96 lesson gates.

## Instrument digests (verified before attacking; match `controls/instrument-sha256.txt`)

```
a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134  c96_selfassess.py   (expected a282da65… ✓)
ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9  c96_reval.py        (expected ec40aec19… ✓)
8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193  c95_selfassess.py   (frozen round-95 ✓)
```

No mismatch: no instrument defect, no repair license taken. Receipts in
`.ufo/waves/round-96/w1/ExecC1Guard/receipts.txt`.

## (1) Successor run at HEAD `049e8eca` (freeze commit)

Counting command:
`TMPDIR=/fast/scratch/hyaku/kake-r96/ExecC1Guard python3 -B .ufo/waves/round-96/c96_selfassess.py --root . --revision $(git rev-parse HEAD) --work /fast/scratch/hyaku/kake-r96/ExecC1Guard/work-succ`

Line 1 (rc = 0):
`C1v96 revision=049e8eca… counter=a282da65… lessons=90 entries=83 rows=260 criteria=40 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=ok battery=23/23 admit=5/5 shadow=absent predecessor_admits=6/22 floor=4 ng_pred_admits=3/3 self_pin=ok met=true`

Expected per seat spec: `met=true pins=ok battery=23/23 admit=5/5 ng_pred_admits=3/3` — **all match**,
and line 1 is identical modulo the revision stamp to the committed
`controls/c1-successor-at-base.txt` at `bde98691…` (diff in `control-diff.txt`, diff rc = 0).
The successor's committed verdict survives the wave's concurrent state end-to-end:
HEAD is still the freeze commit, worktree clean apart from my own w1 directory.

## (2) Predecessor (do-nothing control) at HEAD — must stay red

Counting command: same convention with `.ufo/waves/round-95/c95_selfassess.py`.

Line 1 (rc = 1):
`C1v95 revision=049e8eca… counter=8fd27d62… lessons=90 entries=83 rows=260 criteria=40 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=identity battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 self_pin=ok met=false`

`met=false pins=identity` as required; identical modulo revision stamp to
`controls/base-c1-predecessor.txt`. The do-nothing control stays red — the C1
predecessor/successor pair is differentially green/red at the current tip.

## (3) E1 body-word rule vs the real lessons

Rule (R95-5 NG01/NG08/NG11, from `c96_selfassess.py:277-295`): for lessons of rounds
`>= 96`, decision vocabulary must appear as **whole words** in the Gate body
(`DECISION_RE = \b(?:admits?|admitted|rejects?|rejected)\b`, case-insensitive,
line 146); heading tokens never count; substring hits (`rejection`,
`admiralty`) do not match. Decision tokens are required from both admit and reject
classes. Spot-check files are excluded via `LESSON_SKIP = ("-verifier-spotcheck.md",)`.

Extraction over the real corpus at HEAD (`git ls-tree -r HEAD -- corpus/lessons`):
- 90 lane-authored lessons in scope (aggregators and all 73 verifier spot-checks
  excluded). **Round ≥ 96 lessons present: 0** — `corpus/lessons/round-96.md` does
  not exist yet and no peer has created one in the tree (concurrent wave state,
  observed). Hence the new rule has no real round-96 Gate body to name yet:
  **no E1 finding names any real lesson** (successor mismatches total = 0, E1
  entries = 0). The rule is vacuously green on the real corpus this wave; it will
  bind the round-96 lesson when a seat writes it.
- Hypothetical probe — real `corpus/lessons/round-95.md` Gate body under the new rule:
  1 Gate section, body 66 lines, **8 whole-word decision tokens** carrying both
  classes: admit forms `admit`(×1, line 58 `admit 5/5`), `admitted`(×4, lines
  16/29/33/62); reject forms `rejected`(×3, lines 25/42/50). **PASS** — the real
  round-95 Gate body satisfies the new body-word rule. Heading is the bare
  `## Gate` (zero heading tokens), so heading-vs-body is not exercised by this file;
  code inspection (`audit`, lines 283-295) confirms only `body` is searched.
- Word-boundary sanity: `rejection` does NOT match `DECISION_RE`; NG11 substring
  trap absent from the real Gate (`rejection`/`admiralty` both absent), which is
  exactly why the strict rule can be green here — the corpus never relied on
  substring hits for its decisions.
- Full probe output in `real-e1-probe.txt` (rc = 0).

## (4) Mismatch diagnosis

**No real mismatch appeared.** Successor reproduces its control line-1 exactly;
predecessor stays red; the real round-95 Gate passes the new whole-word rule on
its own; zero round-≥96 Gate bodies exist yet to trip it. Consequently: no lane
defect and no instrument defect to diagnose; no repair proposal is owed, and no
finding is routed. (If a round-96 lesson lands later this wave, the rule binds it;
a vacuous/junk-body Gate would then be a real E1 finding by design.)

## Deliverables (all under `LANE/.ufo/waves/round-96/w1/ExecC1Guard/`)

- `successor-run.txt` — line 1 + full JSON + `rc=0`
- `predecessor-run.txt` — line 1 + full JSON + `rc=1`
- `receipts.txt` — condensed receipts (command, line 1, rc, digests)
- `control-diff.txt` — both line-1 diffs vs committed controls (IDENTICAL, diff rc=0)
- `real-e1-probe.txt` — one-line extraction + body-word probe (rc=0)
- This report at `.ufo/waves/round-96/w1/ExecC1Guard.md`

Scratch tree `/fast/scratch/hyaku/kake-r96/ExecC1Guard/` deleted before yielding;
no unread check, no fabricated output.

Verdict line:

```
EXEC-C1GUARD successor=0 predecessor=1 realE1=0
```
