# CriticC2Deaths — round-54 w1

Scope: attack `.ufo/waves/round-53/settlement.md`'s "40 spawned / 0 committed
reports" statement against `w53-spec.json` and the non-author closure. Test:
does it honestly leave the individual dead-seat count unverified, and could
the prose overclaim deaths? Reviewed at lane tip `8e408e0` (master; settlement
committed there). Working tree at review time carries two uncommitted edits by
the lane (`MANIFEST_RE` backtick fix in `c54_ops_debt.py`, `read-only` token in
the `SKILL.md` registry row).

## Verdict on the two assigned questions

1. **Honesty on dead-seat count: YES.** The settlement twice declares the
   individual death count unverified ("individual death outcomes are not
   recoverable and are **unverified**, not inferred from absent reports"; "the
   individual dead-seat count remains unverified"), and labels the seven cited
   names "lost pointers, not as recovered agent transcripts". This matches the
   non-author closure's own line: "Dead-seat count remains unverified …
   seat-level settlement was not captured"
   (`corpus/lessons/round-53-verifier-spotcheck.md` §Dead-seat reconciliation).
   `resolved:` rows: none — accurate, since no report was recovered.

2. **Overclaim of deaths: NO for the literal claim, marginal for one phrase.**
   The prose never claims 40 (or any) deaths; it explicitly refuses that
   inference. Numbers verified independently:
   - `w53-spec.json`: `items` length 40, role mix `scout 14, connector 1,
     executor 3, scribe 6, reviewer 8, critic 8` — exactly as the settlement
     states. No duplicate seat names.
   - `git log --all -- '.ufo/waves/round-53/w1'` → 0 commits; tip tree has no
     `round-53/w1/` entry; each of the 7 cited report names has 0 hits across
     all history. "0 committed reports" is fully verified, not merely
     evidence-backed.
   - Marginal: "The 40-seat launch happened" is supported only by the spec
     declaration plus wave products — seats could have died at spawn. The
     evidence establishes a declared 40-seat wave and zero committed reports;
     actual spawn-outcome is unverifiable. Minor; the sentence immediately
     concedes the count is unverified.

## Counterexample (fixable defect, not a prose overclaim)

**The committed settlement fails its own frozen C2 counter at tip `8e408e0`.**
`python3 -B .ufo/waves/round-54/c54_ops_debt.py` would exit 1 on the committed
state for two independent reasons:

- `MANIFEST_RE` (`^\|\s*([A-Za-z0-9_-]+\.md)\s*\|…`) cannot match the
  settlement's backtick-quoted filenames (`` `ReviewerProvenance.md` ``) —
  `settled` parses to `[]`, so `settled_required` fails on all 7
  REQUIRED_SEAT_NAMES. Re-derived: committed regex → `[]`; WT-fixed regex →
  all 7 names.
- The `SKILL.md` registry row at `8e408e0` lacks the `read-only` REQUIRED
  token; WT edit adds it ("Normal path is read-only and reads committed Git
  blobs").

Both fixes exist only as uncommitted working-copy edits — so the committed
state the lane declared frozen-and-settled still fails P2.1 and P2.2/P2.3 as
encoded. Note also the settlement prose was amended between `acae1dc` and
`8e408e0` to carry the literal "0 committed seat reports" the
`has_loss_basis` regex requires; regex-fitted wording is acceptable, but it
means the counter is what the prose must satisfy, and the remaining two
mismatches show it doesn't yet.

Secondary observation: `NAME_RE` misses the bare `ScribeGate.md` citation in
`corpus/lessons/round-53.md` (no `w1/` path prefix), so `cited` = 6 while
`REQUIRED_SEAT_NAMES` = 7 — the explicit required-set is what actually closes
the coverage gap. Consistent, but the regex citation basis is narrower than
the closure's named loss list.

## Evidence

- `.ufo/waves/round-53/settlement.md` @ `8e408e0` — committed; WT identical.
- `.ufo/waves/round-53/w53-spec.json` — items 40; role mix matches exactly.
- `corpus/lessons/round-53-verifier-spotcheck.md` §§Conformance, Dead-seat
  reconciliation — 0 committed seat reports, no `w1/` dir, count unverified.
- `git log --all -- '.ufo/waves/round-53/w1'` → 0; `git ls-tree -r 8e408e0` →
  no `round-53/w1` paths; 7 cited names → 0 history hits each.
- Committed `MANIFEST_RE` → `settled=[]` on committed settlement bytes;
  patched regex → all 7. Registry row at `8e408e0` missing `read-only` only.
- Base control `controls/base-c2-ops-debt.txt` (`registry=absent
  manifest=absent uncovered=4`) re-derived as correct at `68228b2`.

## Impacted axes

- **operability** (direct): C2 not met on committed bytes; settlement is
  honest but under-pinned — its own gate would reject the committed state.
- **discernment**: prose honesty is clean; the defect is mechanical coverage,
  not overclaim.

## Smallest safe correction

1. Commit the two pending WT edits (`MANIFEST_RE` backtick allowance;
   `read-only` in the registry row). 2. Re-run the frozen counter at tip and
   commit the receipt. No settlement-prose change is needed for the deaths
   question — the unverified-count disclosure is already honest; optionally
   soften "the 40-seat launch happened" to "the 40-seat wave was dispatched
   per the committed spec".

Installs: none. Pacman untouched (paused host-wide). Read-only review — only
this report was written.
