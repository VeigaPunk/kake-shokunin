ExecC1Population — C1 receipt construction (round 78, w1)
=========================================================

All receipts were produced in scratch under $HYAKU_SCRATCH/kake-r78/ExecC1Population
(deleted before yield; these copies are the retained bytes). Ledger sha256 as delivered:
828ab893e9e69693844bd8bd975cede3874473b42670af8010faf30a36f51adf

base-c1-population.rerun.txt
  command: python3 -B .ufo/waves/round-78/c78_shonen_population.py --root \
           /home/vgpnk/Projects/shokunin/kake-shokunin --revision fe50945399a386b48678b1f2051fdbe8a77b10bd
  exit: 1
  byte-identical to .ufo/waves/round-78/controls/base-c1-population.txt
  sha256 both: bb3ddcda58e3b317788f0102ab038b52ad84d1df64475e6972a66ef6e0d66c09
  (see base-rerun-identity.txt)

selftest.txt
  command: python3 -B .ufo/waves/round-78/c78_shonen_population.py --selftest --work <scratch>
  exit: 0 · tally 9/9

after-c1-population.txt (in controls/)
  PRE-INTEGRATION projected carrier, cut before the L1 commits (the seat spec sanctions
  a scratch carrier; KakeR78 confirmed it will re-cut at the integration commit).
  Construction:
    git -C <lane> archive HEAD | tar -x -C <scratch>/carrier      # HEAD = 78711a6 (round-78 contract commit)
    cp <lane>/corpus/knowledge/shonen-ledger.json <scratch>/carrier/corpus/knowledge/shonen-ledger.json
    # ScribeMetaRobots' corpus/knowledge/meta-robots-directives.md was NOT on disk at cut time;
    # a one-line placeholder was created at that contract-fixed path so the population count (65)
    # matches the integrated carrier (KakeR78 confirmed the real doc is a §C3 deliverable and that
    # 65 is the correct count).
    git init + commit under the fixture only; fixture commit 1729712e4ee5c2960bcad1c3d55fe8babbf9f1b7;
    `git ls-tree -r <rev> corpus/knowledge | grep -c '\.md$'` = 65.
  command: python3 -B .ufo/waves/round-78/c78_shonen_population.py --root <scratch>/carrier --revision 1729712e4ee5c2960bcad1c3d55fe8babbf9f1b7
  exit: 0 · met=true
  sha256 of this receipt file: 5d1cddb807884bf422b37047fdd33641339a40832e73f453d9dfb5e27047d4a1
  RE-CUT AT THE REAL INTEGRATION COMMIT (real ScribeMetaRobots doc in place):
    python3 -B .ufo/waves/round-78/c78_shonen_population.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision <integration-rev>
  If meta-robots-directives.md is not part of the carrier, change box 4's declared count
  65 -> 64 in corpus/knowledge/shonen-ledger.json (one integer; see carrier-before-c3.txt
  for that state: stale_populations=1, declared=65 derived=64).

carrier-before-c3.txt
  Same fixture without the C3 doc: 64 knowledge .md; declared 65; exit 1;
  `S1 box 4: declared=65 derived=64` · stale_populations=1. Fixture rev 86f424e3d5e14960394c1778e391be35706da8b6.
  Proves the population layer reacts to a corpus/knowledge .md landing without the ledger moving.
  sha256: 505f3b2e7f5f4313b3c4a0669ec1747445f17b59de97b797e9debd5f0b067878

fake-population.txt
  Same carrier fixture with box 4's count mutated to 999: exit 1;
  `S1 box 4: declared=999 derived=65` · rows_with_population=4 · stale_populations=1.
  Fixture rev 731c17d8e3f6e84577263c9370b59da2bbfd1717.
  Proves the counter fails on a fabricated population.
  sha256: 037ed0fafe971e5c098615fbbd7c782a1266b6aaaa8e16403c924fa834a346ba

Note on the projected carrier: b4-lanes' observed=0 is measured over the placeholder; with the
real C3 entry the same check must still re-derive 0 (no sibling-lane path in that entry). C1's
gate at the real carrier will catch it if not, as an exact mismatch owned by the C3 entry.
