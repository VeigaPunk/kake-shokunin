# ScribeReportSources — round 51 wave 1 leaf report

Seat: `L1Kake51.ScribeReportSources-2` (scribe, freshness). Date: 2026-10-25.
Scope: draft the `Sources & frontier` paragraph for the round report from committed bytes only, and
record what the committed bytes prove or fail to prove. The L1 owns the real report; this file is a
seat report plus a draft.

Measured revision for every reading below: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
Base (do-nothing) revision: `007d66e4e8360a5f88d29a93eeedd8066dad4434`.

## Draft (written to `/tmp/c51-scribe-sources.md`, sha256 `f3e49bc452e8d82aba914c788a86daf18cc635a33b54f07703b48070e3b6af50`)

<!-- DRAFT-BEGIN -->
### Sources & frontier

Census before the append ran on the pre-append mirror, not on the lane registry:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`,
exit `0`, stdout twelve `file W04 … duplicate url … across scopes` warnings (S033, S088, S092, S098,
S099, S102, S110, S111, S115, S116, S117, S127) then `file ok …/pre-append/corpus/SOURCES.md`
(`.ufo/waves/round-51/assimilation/pre-append/census-argv.txt`, `census-exit.txt`, `census-stdout.txt`;
empty stderr). The after census ran the same shape with `--file` on the live registry
`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`: exit `0`, the same twelve `W04` lines and
the same `ok` line apart from its path — the two stdout files are identical after normalising the final
path (normalised sha256 `25adb12a1605a546589b7796f99ba98054d01f4178ac67baba440c1afe82bcd8`). That pair
does not by itself witness the append: both inputs are 145-row documents (census mode prints `rows 145`
for the mirror and for the live registry), because the mirror already carries the two staged rows. The
row arithmetic therefore comes from git plus the census `census` mode: 143 rows at the base
`007d66e4e8360a5f88d29a93eeedd8066dad4434` (tier A 120 / B 6 / C 17; mined 113, queued 8, rejected 22)
→ 145 rows at the measured revision `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (tier A 122 / B 6 / C 17;
mined 115, queued 8, rejected 22). Rows added by tier: two, both tier A, both kind `docs` — S262 (Google
Search Central, URL canonicalization) and S263 (Google Search Central, Googlebot); tier B and tier C are
unchanged. Rows touched old-to-new: none — `git diff --numstat 007d66e4 9d13768c -- corpus/SOURCES.md` is
`2 0`, and an eleven-cell comparison of all 143 pre-existing ids between the two revisions finds no
changed row, so no status, recheck or used-by cell of an existing row moved. Frontier rows advanced: no
pre-existing frontier row advanced status (no queued→mined, no rejected→mined); the frontier moved by the
two new rows, each tier A, `mined`, `opened 2026-10-24`, `recheck 180d`, and each `used-by` exactly the one
admitted entry that cites it (`corpus/knowledge/canonical-selection.md` for S262,
`corpus/knowledge/crawler-identity.md` for S263). At least one sourced claim landed this round: S262 and
S263 are backed by retained bodies whose sha256 match their receipts
(`.ufo/waves/round-51/sources/S262.html` `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`,
`S263.html` `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de`), and the round's
sourced claim C2 counts `8 of 8` at the measured revision (exit `0`) against `0 of 8` at the base control
(`.ufo/waves/round-51/controls/c2-before-base.txt`) and `5 of 8` for the junk control.
<!-- DRAFT-END -->

## Behavior verified

Each line states what was run and what it printed. Nothing below is inferred from another seat's report.

| Reading | Command | Result |
|---|---|---|
| C2 at the measured revision | `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c…` | `C2 quote-truth 8/8 met=True`, all eight conditions `pass`, exit `0` |
| Census, pre-append mirror (committed receipt) | `sources-census.sh validate --file …/assimilation/pre-append/corpus/SOURCES.md` | exit `0`; twelve `file W04` duplicate-URL warnings (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127); `file ok …/pre-append/corpus/SOURCES.md`; stderr empty; no `E03`/`E04` |
| Census, live registry (my run, not committed) | `sources-census.sh validate --file …/kake-shokunin/corpus/SOURCES.md` | exit `0`; identical stdout after normalising the `ok` path (normalised sha256 `25adb12a…`) |
| Census row histogram, mirror (my run) | `sources-census.sh census --file …/pre-append/corpus/SOURCES.md` | `rows 145`, `tier.A 122`, `tier.B 6`, `tier.C 17`, `status.mined 115`, `status.queued 8`, `status.rejected 22`, `invalid 0`, `missing 0`, exit `0` |
| Census row histogram, live (my run) | `sources-census.sh census --file …/kake-shokunin/corpus/SOURCES.md` | identical figures, exit `0` |
| Census row histogram, base bytes (my run) | `git show 007d66e:corpus/SOURCES.md > /tmp/c51-base-SOURCES.md` then `census --file /tmp/c51-base-SOURCES.md` | `rows 143`, `tier.A 120`, `tier.B 6`, `tier.C 17`, `status.mined 113`, `status.queued 8`, `status.rejected 22`, exit `0` |
| Registry delta | `git diff --numstat 007d66e 9d13768c -- corpus/SOURCES.md` | `2  0  corpus/SOURCES.md` (two insertions, zero deletions) |
| Rows added | eleven-cell parse of both revisions | added `S262`, `S263`; removed none; changed pre-existing rows: none |
| Row S262 | `grep` of the live registry | tier `A`, kind `docs`, status `mined`, opened `2026-10-24`, recheck `180d`, used-by `corpus/knowledge/canonical-selection.md` |
| Row S263 | `grep` of the live registry | tier `A`, kind `docs`, status `mined`, opened `2026-10-24`, recheck `180d`, used-by `corpus/knowledge/crawler-identity.md` |
| Retained bodies vs receipts | `sha256sum .ufo/waves/round-51/sources/S262.html S263.html` | `79222433…` and `6afbdc82…`, equal to `receipts.json` (`httpStatus` 200, 174 926 and 175 561 bytes) |
| Gate quotes are raw substrings | `grep -c` in each retained body | `1` and `1`; word counts 10 and 9 (inside the 6–25 bound) |
| Blindness to the working tree | `git hash-object corpus/SOURCES.md` vs `git rev-parse 9d13768:corpus/SOURCES.md` | both `9e2a22175ef95a23252b349d8743cf0e5b5480fc` — the live registry is the committed tip byte-for-byte |
| C1 at the measured revision (recorded, not mine to advance) | `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c…` | `C1 ledger 0/3 met=False`, L1/L2/L3 all fail on absent settlement and route map, exit `1` |

Base census caveat: `validate --file` on a `/tmp` copy of the base registry exits `1` with `E11 missing
used-by …` lines, because `E11` resolves `used-by` relative to the registry's own directory. That run is a
path artefact, not a base-revision finding; only the `census`-mode histogram above is used.

## Gates

- Committed bytes only: every row, tier, status and quote reading above comes from `git show`/`git show
  <rev>:path`, `git diff`, `git merge-base`, or from files already in the tree whose blob equals the
  committed tip blob.
- Word-bound for the draft: the paragraph is 100 % re-derivable from the five artifacts it names
  (`census-argv/exit/stdout.txt`, `receipts.json`, `corpus/SOURCES.md` at two revisions) plus
  `controls/c2-before-base.txt` and `controls/c2-junk-entries.txt`.
- Pre-append census shape: argv uses `--file` on the mirror path and no `--root`; exit `0`; stdout carries
  no `E03` and no `E04` (C7's sentence), confirmed by reading the three receipt files.
- Both committed C2 controls re-read: base revision `007d66e` → `0/8`, all eight conditions `FAIL`; junk
  control revision `cc57cb80` → `5/8` with `C2`, `C5`, `C8` failing. The counter can fail, and it fails
  on the controls.

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/w1/ScribeReportSources.md`
  (this file, untracked — the `w1/` directory is untracked at the measured revision).
- Written outside the lane: `/tmp/c51-scribe-sources.md` (the draft),
  `/tmp/c51-after-validate.out`, `/tmp/c51-after-validate.err`, `/tmp/c51-base-SOURCES.md`.
- Not touched: fleet repo, sibling lanes, sibling round-51 seat reports, the lane Git index, jj state,
  `considerthese/`, `.ufo/waves/round-46/residual/`, `.ufo/waves/round-48/assimilation/validate/`,
  `/home/vgpnk/Projects/shokunin/../shokuknow/`. No `git add`/`commit`/`stash`/`checkout`/`switch`/
  `reset`/`pull`/`push` and no mutating `jj` command was run.
- Pre-existing or sibling dirt observed and left alone: ` M SCORECARD.md`, ` M PROVINCE.md`; ` M
  .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` and ` M
  .ufo/waves/round-51/assimilation/pre-append/census-exit.txt` (another seat's live mutation, see F5);
  untracked `build_wave_evidence.py`,
  `make_spec_w1.py`, `route-map.json`, `route-probes/`, `w1/`, `w51-spec.json`, `w51-taskcall.json`,
  `w51-validator.err`, `wave-grant.txt`, `wave-start-utc.txt`, and the inherited round-46/48 untracked
  copies.

## Findings

**F1 — C8's sentence and C8's implementation name different objects (freshness; medium).**
Contract C8 reads: "the pre-append mirror commit is a strict ancestor of the measured revision, the
mirror's registry carries none of the adopted ids and the measured revision's registry carries all of
them" (`.ufo/waves/round-51/contract.json:47`). The committed mirror artifact at
`.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` **does** carry both ids — 145 rows, with
`S262` at line 152 and `S263` at line 153 at the mirror commit `19a99bd8c30d36a4d664871236ba2015d893b5b9`
(read with `git show`; the working-tree copy has since been changed by another seat, see F5). The counter
(`c51_quote_truth.py:277`) instead reads
`show(root, mirror_commit, REGISTRY)` — the lane's `corpus/SOURCES.md` *at* that commit, which holds 143
rows and neither id — so the check passes. LOG.md's own description of the mirror ("the lane's `corpus/`
plus the two new rows", `LOG.md:2058`) agrees with the artifact, not with the sentence. Reported
verbatim for the canonical judge: as written, C8 is false of the mirror file and true only under the
reading "the lane registry at the mirror commit". C2's `8/8` therefore depends on which object "the
mirror's registry" denotes.

**F2 — the round's census pair cannot witness the append (freshness; low, structural).**
The only committed census receipt for round 51 validates the mirror, which already holds the two appended
rows (145). An after-census on the live registry is byte-identical apart from the `ok` path, and also 145.
Both exit `0`, so the pair is sound as a *validity* witness; it is not a delta witness. The 143 → 145
movement is attested only by git (`git diff --numstat` = `2 0`) and by the census `census`-mode histogram
over `git show 007d66e:corpus/SOURCES.md` (my run, not committed). The draft says so rather than implying
the census pair shows the append.

**F3 — the wave evidence C1 counts is untracked (operability; state, not defect).**
`build_wave_evidence.py`, `route-map.json`, `route-probes/`, `wave-grant.txt`, `wave-start-utc.txt`,
`w51-spec.json` and `w51-taskcall.json` are untracked in the lane at the measured revision, and
`c51_wave_ledger.py --revision 9d13768c…` prints `0/3` because settlement and route map are absent *from
committed bytes*. That matches the dispatch's measured state and the contract's `before` sentence; the L1
writes and commits the evidence after this wave settles. Recorded, not treated as a C1 failure of the
round.

**F4 — the C2 counter was edited after the append commit (freshness; disclosed, no predicate change).**
`9d13768` modifies `c51_quote_truth.py` (the C6 receipt lookup: `receipts["sources"]`) after the append at
`5591557`. The predicate string, the eight condition sentences and the counted artifacts are unchanged, and
the corrected counter reads `8/8` at `9d13768`; LOG.md records the fix and the pre-fix state. No condition
was weakened on inspection: each check still reads the same paths and thresholds.

**F5 — the working-tree mirror and census receipt now disagree with their committed blobs (observation,
not a defect of the committed claim).**
Between 03:33 and 03:36 local the working tree changed under this seat: 
`.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` went from 145 rows (committed blob
`9e2a22175ef95a23252b349d8743cf0e5b5480fc`) to 143 rows with neither S262 nor S263 (blob
`cd448eaf06bbccefbd2e672be03355c79dd6d851`), and
`.ufo/waves/round-51/assimilation/pre-append/census-exit.txt` went from `0\n` to `exit=0\n`
(`git status --porcelain` shows ` M` on both). Another round-51 seat is evidently running a mutation on
these paths. Every figure in this report and in the draft comes from the committed objects
(`git show <rev>:<path>`), not from the working-tree copies, and the live registry is still tip-identical
(`git hash-object corpus/SOURCES.md` = `9e2a2217…`). Recorded so a verifier who greps the working tree is
not misled; this seat did not restore or edit either file (bounds: read-only outside its own report).

## Out of scope

- Authoring the wave evidence, the settlement, the route receipts or the time accounting (L1).
- Editing `corpus/SOURCES.md`, the two knowledge entries, the lesson, the counters or the controls.
- Scoring either axis, admitting or rejecting the two entries, or ruling on F1 — the canonical judge and
  the L1 own that.
- Verifying the 48 seats' own reports.

## Artifact paths

- Draft: `/tmp/c51-scribe-sources.md` (sha256 `f3e49bc452e8d82aba914c788a86daf18cc635a33b54f07703b48070e3b6af50`)
- After-census stdout: `/tmp/c51-after-validate.out` (sha256 `3ff7329c1005e3a250521a27598b496b23f4472d7c52d22d081504b921c142e6`; stderr empty)
- Base registry copy: `/tmp/c51-base-SOURCES.md` (sha256 `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117`)
- Committed census receipt: `.ufo/waves/round-51/assimilation/pre-append/census-stdout.txt` (sha256 `6dbb5497639eaf00bf8dd56a84d62a780fc2e5e3985e7042c8818f2aaf0f7141`)
- Retained bodies: `.ufo/waves/round-51/sources/S262.html`, `S263.html`; receipts `.ufo/waves/round-51/sources/receipts.json`
- Controls: `.ufo/waves/round-51/controls/c2-before-base.txt`, `c2-junk-entries.txt`, `c1-before-base.txt`

Durability note: no `/tmp` file is load-bearing. The draft is inlined verbatim in this report above
(`DRAFT-BEGIN`/`DRAFT-END`, byte-identical to the `/tmp` copy by `diff`), the twelve `W04` ids and the
normalised stdout sha256 are printed in the draft, the 143/145 histograms are in the table above, and every
`/tmp` reading is re-derivable by rerunning the command printed beside it. This report cites no
`.ufo/waves/round-35/scratch/` or `scratch-evidence/` path (that tree belongs to `mado-shokunin`, not to
this lane), so the 03:43–03:46 relocation and re-sweep reported by that round's seats do not touch it.

Tool installs/updates: none. Lane bound honoured: leaf member, no subagent dispatch.
