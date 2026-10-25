# CriticQuarantine — round 51, wave 1 (kake)

Seat: `L1Kake51.CriticQuarantine-2`. Read-only review; nothing fetched, nothing edited outside this file.
Lane revision read: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (base `007d66e4e8360a5f88d29a93eeedd8066dad4434`).
No tool installed or upgraded; no install record owed.

## The clause, quoted

Round prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-51.md`, lines 450-464;
byte-identical clause in `scripts/hyaku/lane-addendum.md` lines 310-324):

> **Quarantine — payload-absent rows.** Register (read-only; its header AND `## By lane` summary
> totals are stale — derive your slice yourself), data rows only — the lane cell, a round cell
> and an id cell (summary rows match a bare lane name and print blanks):
>
> ```
> A=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/assimilation; mkdir -p "$A"
> R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
> awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
>   {print $4, $5}' "$R" > "$A/quarantine-slice"    # every line must carry an S-id
> ```
>
> Every slice row is quarantined: not appendable until hand-checked this round — fetch the cited
> source and locate the quote; absent → refuse the row (fabrication class, reason in the Gate
> block); present → adopt with the anchor you located. A prose class cell ("could not be
> fetched", "named no locator") is the register's unchecked family: mark the row unverifiable —
> `unreachable` is not fabrication. Never edit the register or any campaign file; verdicts land
> in the lane's lesson and report.

The only per-row verdict duty in the same prompt is the next bullet (lines 465-469):

> **Wave-4 quarantine-first (tabi, revenger, chousa, kotodama).** This lane's first round under
> this item adopts nothing from its package: it hand-checks the lane's full register slice and
> lands a verdict per row …

## Ruling

**Unadopted is acceptable for kake in round 51. The quarantine clause does not require a verdict
per row this round.**

Textual basis, tested against the strongest counterexample:

1. The clause's only obligation grammar is conditional: *"not appendable until hand-checked this
   round"* gates appending on a same-round hand-check; *"absent → refuse … present → adopt"* states
   what a hand-check yields. It never says "hand-check every slice row this round". Read as a
   drain duty it would need a sentence like the wave-4 bullet's "*lands a verdict per row*" — and
   that sentence exists only in the wave-4 clause, which enumerates tabi, revenger, chousa and
   kotodama and speaks of "*this lane's first round under this item*".
2. Kake is not a wave-4 lane and is not in its first round under the item: `grep -c 'Quarantine — payload-absent'` on the lane's prompts returns 0 for rounds 46-47 and 1 for rounds 48, 49, 50, 51. Round 51 is the fourth round under the item; the wave-4 clause's trigger does not fire.
3. Counterexample tested and rejected: if "verdicts land in the lane's lesson and report" were a
   round-scoped duty to land *some* verdict, the round would be non-compliant because the lesson's
   `## Quarantine` block (corpus/lessons/round-51.md:69-74) lands no per-row verdict. The reading
   fails because the clause's disposition is triggered by a hand-check ("fetch the cited source and
   locate the quote; absent → refuse"); no hand-check, no verdict owed. The register's own header
   agrees the class cell is not a verdict: "A quote the checker could not match is a CANDIDATE, not
   a verdict."

**The exemption is conditional on four things the clause *does* require.** Three pass; one fails.

| Requirement | Verdict | Evidence |
|---|---|---|
| Slice re-derived with the stated filter, every line carrying an S-id | **FAIL (byte fidelity)** | see E2 below |
| Nothing quarantined appended or cited | PASS | E3 |
| Register and campaign files never edited | PASS | E4 |
| Verdicts land in the lane's lesson and report | **PARTIAL** — lesson yes, report not yet written | E5 |

## Evidence (commands actually run, output as printed)

**E1 — slice is complete.** Register holds 13 `^| \`kake\` |` rows: 12 data rows plus the stale
summary line `| \`kake\` | 9 |`. The filter excludes only the summary line. Filter output and
committed file carry the same 12 ids in the same order: S142 S143 S148 S156 S161 S193 S194 S195
S206 S154 S178 S184 (9 `payload-absent`, 3 "the cited source could not be fetched"). No kake data
row is missed; the 12-vs-9 gap is explained (the summary counts payload-absent only).

**E2 — the committed artifact is not the command's output.** Re-running the prompt's verbatim
filter (lines 456-457 above) into a `/tmp` scratch file (transient; the reproducible input is the
quoted command) and diffing against
`.ufo/waves/round-51/assimilation/quarantine-slice` (committed at `19a99bd`) yields 12/12 changed
lines; the essential lines are inlined here, so nothing rests on the scratch file:

```
<  S142   `payload-absent`            >  S142   payload-absent
...
<  S154`   the cited source could ... >  S154   the cited source could ...
<  S178`   the cited source could ... >  S178   the cited source could ...
<  S184`   the cited source could ... >  S184   the cited source could ...
```

The committed file strips the register's code-span backticks from the class cell and the trailing
backtick that the register's id cell carries for S154/S178/S184 (register lines 319-321 read
`| S154` |`, an unopened code span). Neither the lesson nor any receipt records that
normalization. Consequence: a reader re-running the prompt's command does not reproduce the
committed evidence, and the register's three malformed id cells — exactly the kind of structural
defect the derivation exists to surface — are silently repaired out of the artifact. The S-id set
and the class text are semantically unchanged, so this is a provenance defect, not a content one.

**E3 — nothing quarantined was appended or cited.** `git diff --numstat 007d66e..9d13768 --
corpus/SOURCES.md` is `2 0` (two added lines, S262 and S263; no removal, no edit). The two admitted
entries cite `S021 S022 S262` and `S011 S095 S096 S263` only. `grep -nE` for the 12 slice ids
across `corpus/knowledge`, `corpus/handoffs` returns nothing. None of the 12 ids appears in
`corpus/SOURCES.md` at base or at tip (`git show 007d66e:corpus/SOURCES.md | grep -c "| S142 |"` →
0, same for all 12), and `git log -S"S142" -- corpus/SOURCES.md` is empty — the ids were never
committed to this lane's registry. "Adopted nothing" is therefore the standing state, not a new
suppression: appending any of them this round would have re-introduced the very rows the register
classes as suspect.

**E4 — campaign files untouched.** In `/home/vgpnk/Projects/shokuknow`,
`git status --porcelain -- .ufo/waves/corpus-expansion-1/absent-defect-register.md` prints nothing;
the file's mtime is `2026-10-24 08:37:00.746072780 -0300`, before the round's single fetch pass
(`2026-10-24T23:16:49-03:00`, `sources/receipts.json`). Only S262 and S263 were fetched this round,
neither in the slice — consistent with the lesson's "no quarantined id was hand-checked this
round".

**E5 — the record leg.** The lesson's `## Quarantine` block states the deferral and the artifact.
`.ufo/reports/round-51/` currently holds only `kotoba.md`, `kotodama.md` and `kumitate.md` — there is
no `kake.md`, so the clause's "*lesson and report*" is half-discharged at wave 1. The report is owed
at round end; if it omits the line, the deferral becomes an unstated omission and this leg fails.

## Counterexample and residual risk (not a violation)

The honest attack on the lane's handling is not the clause, it is liveness. Four rounds under the
item (48-51), one hand-check total (round 48, 9 absent / 3 unreachable). Because "not appendable
until hand-checked this round" only ever gates an append, a round that re-derives and appends
nothing changes no state: the 12 lines are byte-for-byte the same next round, and the round prompt's
own wave-4 clause exists because that is the failure mode it wanted to pre-empt. Kake's handling is
compliant, and the deferral is honest rather than a dodge — 9 of the 12 are the register's
fabrication class, so adopting any would break the corpus's quote bar, and the 3 prose rows are
credentialed API endpoints (S154/S184 `chromeuxreport.googleapis.com/v1/records:queryRecord`, S178
`googleapis.com/pagespeedonline/v5/runPagespeed`) that a re-fetch cannot settle without a key —
but the round produces an artifact with no consumer.

One adjacent fact worth recording for a future hand-check round: S161's cited URL
`https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` is held ground
today under S274 (corpus/SOURCES.md:150) with a different, present quote. That is not a duplicate
(the quarantined row is not in the registry) and it is not an adoption basis — the S274 body was
not retained this round — but it makes S161 the one slice row whose source is already in hand.

## Impacted axes

- **freshness** — the slice's provenance is not reproducible from the prompt's command; the
  round-51 lesson cites the artifact as evidence without the derivation step. Defect, small.
- **operability** — a re-derivation is a reader operation; today it yields a different file than
  the committed one, so the ledger-style "re-derive from committed bytes" property the round is
  building does not extend to `assimilation/quarantine-slice`.
- Not impacted: C1 (reads settlement/payload/route receipts/timing/LOG only), C2 (reads registry,
  the two entries, the lesson Gate block, retained bodies, pre-append mirror). Neither counter
  reads the slice, so the correction below cannot move either predicate.

## Smallest safe correction

Two additive lines, no change to any frozen claim, predicate, counter or the committed slice:

1. Commit the verbatim filter output beside the normalized file as
   `.ufo/waves/round-51/assimilation/quarantine-slice.raw` (12 lines, backticks intact), so a
   reader can reproduce the prompt's command byte-for-byte.
2. Add one line to the lesson's `## Quarantine` block: the committed slice is the filter output
   with backticks stripped (class cell code spans; the unopened code span in the register's id
   cells for S154, S178, S184), and name those three malformed id cells.

Both land in the commit the L1 must make anyway for C1's wave evidence, so there is no extra
revision. After that commit, re-run both counters at the new revision (`c51_wave_ledger.py`,
`c51_quote_truth.py`) before scoring — C2's C8 ancestry still holds, but the measured revision
moves and the lane should not quote figures from a superseded commit.

## Adjacent observation — outside my ruling (route to ReviewC2Conditions-2 / ExecCensusMirrorValidate-2)

Not a quarantine finding; recorded because it is a false-provenance risk I hit while reading the
same tree, and it must not be mistaken for part of the quarantine verdict. I do not rule on C2.

- The committed "pre-append mirror" blob is contaminated. `git show
  19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -c "^| S262 |"`
  prints `1`; `git show 19a99bd:corpus/SOURCES.md | grep -c "^| S262 |"` prints `0`. The mirror copy
  at the mirror commit already carries the post-append row. This was found by the wave-1 seat
  ExecRegistryDiff (`assimilation/pre-append/census-correction.txt` names it); I re-ran only the two
  counts above.
- C8 as implemented cannot see that. `REGISTRY = "corpus/SOURCES.md"` (line 47),
  `MIRROR = ".ufo/.../pre-append/corpus/SOURCES.md"` (line 51), and line 277 reads
  `show(root, mirror_commit, REGISTRY)` — the *lane's* registry at the mirror commit, never the
  mirror copy. That is why `c51_quote_truth.py --revision 9d13768…` prints `C2 quote-truth 8/8
  met=True`: the ordering is proven, the snapshot's content is not. The frozen contract's C8 wording
  ("the mirror's registry carries none of the adopted ids") is the stricter statement; the counter is
  weaker than the condition it certifies.
- Working-tree hazard in the in-flight correction: `pre-append/census-exit.txt` currently reads
  `exit=0` (`git diff` shows `-0` → `+exit=0`), and C7 line 260 requires `exit_text.strip() == "0"`.
  Committed as-is, that turns C7 to fail. The corrected mirror itself now holds 143 data rows and
  0 `S262` rows in the working tree, and the re-run stdout carries no E03/E04 (`grep -c` → 0, tail
  `file ok …/pre-append/corpus/SOURCES.md`).

This in no way touches my ruling: C2's counter reads neither the slice nor any file this report
covers.

## What this report does not claim

- I did not fetch any of the 12 cited sources; my ruling is on the clause, not on whether any row
  is present or absent. The register's classes are the campaign's findings, quoted as such.
- I did not read `ScoutQuarantineSlice.md` (not yet present in `w1/`), so the byte-level slice
  comparison above is my own run of the prompt's filter, not the scout's conclusion.
