# census.md — ExecCensus seat receipts (kake round 97, wave 1)

Seat: ExecCensus (executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin at tip
`9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (= the round's C1 repair commit; verified with
`git -C LANE rev-parse master`). Frozen instrument digests verified before any work:
`c97_index.py` `8535150e…aa008` ✓, `c97_reval.py` `f3895a32…39266` ✓,
`frozen/neg-lookup-table.py` `898df9a2…460cc` ✓ (sha256sum, each rc=0; all three equal
`controls/instrument-sha256.txt`). No tool installs were needed (bash+coreutils+gawk only).
Reads of `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` were read-only
(absolute paths, cwd never inside shokuknow); nothing anywhere outside this seat's w1 dir
and scratch was written.

## 1. Census now (seat item 1)

Command (TMPDIR pointed at the seat scratch; cwd = scratch):

    /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake

Full output + rc: `census-now.txt` (this dir). Observed: **exit 0**, 40 × `W04`
duplicate-URL warnings, `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`,
zero E-class findings. The 40 W04 lines are byte-identical to the pre-freeze receipt
`controls/census-before.txt` (diff of the W04 line sets: empty, "W04-SETS-IDENTICAL") —
consistent with `corpus/SOURCES.md` being unchanged since round start.

## 2. Assimilation id-collision guard (seat item 2)

Dir: `assimilation/`. Pipeline = prompt §10 verbatim (`.ufo/prompts/kake-round-97.md`
lines 609–613), paths adjusted to this seat's bound w1 dir:

    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids        # rc=0
    grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids        # rc=0
    comm -12 reg-ids staged-ids > collisions                                                                                                                # rc=0

Counts: **reg-ids=217** (S001…S480), **staged-ids=129** (S287…S415), **collisions=8**
(S312 S329 S367 S372 S373 S374 S390 S409). The collision set is identical to the committed
round-96 receipt `.ufo/waves/round-96/w1/ExecReceipts/assimilation/collisions` (byte
comparison of content; the reg delta 216→217 is exactly S480, which is not staged, so the
collision set is unaffected — the R96 spot-check count-accuracy note stays satisfied at the
current tip).

Guard proof (`assimilation/guard-proof.txt`): a scratch registry holding the row
`  | S002 | Guard proof — https://guard.example/s002 | …` (two leading spaces) run through
the same extractor yields guard-ids=[S002]; `comm -12 reg-ids guard-ids` yields a NONEMPTY
collisions file [S002]. The 0–3-space window means an indented row cannot smuggle an id
past the guard. **guard=ok.**

## 3. Scratch validation of the planned S481 append (seat item 3)

Mirror: `cp -r LANE/corpus → $SCRATCH/mirror` (rc=0). Appended row S481 at line 227,
directly after S480: verbatim copy of the S479 row shape with id `S479→S481` and source URL
`https://www.rfc-editor.org/errata_search.php?rfc=9111`; no other byte changed;
placeholder-free. The S481 id/URL are unique in the mirror; extractor sees 217→218 rows
(last ids S480, S481).

Command and observed rc:

    /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $SCRATCH/mirror/corpus/SOURCES.md   # exit 1

Full output + attribution: `mirror-validate.txt` (this dir). Delta isolation (baseline run
on the same mirror WITHOUT S481, also exit 1):

- Baseline already carries **19 E11** findings: mined rows whose used-by names
  lane-root-relative paths (`scripts/source_recheck.py`, `SCORECARD.md`, `SKILL.md`,
  `.ufo/waves/round-41/…`, `.ufo/waves/round-73/contract.md`, `.ufo/waves/round-95/freeze.md`)
  that do not exist under a corpus-only mirror (S088–S092, S117–S122, S124, S129, S131–S132,
  S440, S479). Plus the same 40 W04.
- S481 adds exactly **one** line of that same pre-existing class:
  `file E11 S481 missing used-by .ufo/waves/round-95/freeze.md` (copied verbatim from S479's
  used-by cell). E11 removed: none; W04 line set: identical.
- No E01/E02/E03/E04/E05–E10/E12 for S481: 13 fields, unique id, new URL, enums valid,
  opened past, recheck well-formed, mined with non-empty used-by.

Interpretation (reporter note, nothing repaired): the spec's "expected exit 0, W04 class
allowed" holds **at the real lane root**, where every used-by path exists (§1 is that run:
exit 0). The mirror's exit 1 is a corpus-only-mirror context artifact, fully attributed by
the baseline delta; if the L1 appends this row shape to the real registry, the expected
census stays exit 0 with only the pre-existing W04 class — provided the appended row's
used-by keeps pointing at paths that exist at the lane root (S479's `.ufo/waves/round-95/freeze.md`
does).

## 4. Verdict lines

- Census: `EXEC-CENSUS-SUB census_rc=0 w04=40 e=0` (command in §1; exit 0 observed).
- Assimilation: `EXEC-CENSUS-SUB reg=217 staged=129 collisions=8 guard=ok` (§2; all rc=0).
- Mirror S481: `EXEC-CENSUS-SUB mirror_rc=1 s481_new_E11=1 s481_new_W04=0` (§3; observed).

## 5. Environment incident (disclosed, not mine)

ConnectorScope-23 deleted the round scratch parent `/fast/scratch/hyaku/kake-r97` (~18:14Z),
removing this seat's then-empty scratch tree; it was recreated before the next scratch write
(`tmp/`, `guard/`, `mirror/` all recreated fresh). No receipt was lost: every deliverable was
written directly into this w1 dir.

## 6. Cleanup declaration

Scratch root `/fast/scratch/hyaku/kake-r97/ExecCensus/` (tmp/, guard/, mirror/, baseline
capture) is deleted before yielding; all receipts above live in this w1 dir. No mutating
git/jj command was run anywhere; no fixture repo was needed (no commit was made in this seat).
