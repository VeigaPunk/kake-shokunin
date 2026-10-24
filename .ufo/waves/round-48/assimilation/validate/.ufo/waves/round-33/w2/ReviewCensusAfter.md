# ReviewCensusAfter — round 33 wave 2 (falsify)

Scope: source census at tip 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0 vs base
5777d5af79cac1ebf9144b348a9d274099e77338. Attacked: whether the registry delta
is honest (row counts, tier/status split, validate cleanliness, upstream pin).
Sandbox clone: /fast/scratch/hyaku/kake-r33/w2/ReviewCensusAfter/clone @ 0a0acfb1;
receipts under /fast/scratch/hyaku/kake-r33/w2/ReviewCensusAfter/out/.

## Assigned commands

1. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, stderr empty.
   stdout (out/validate-root.out):
   `kake\tW04\tS033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`
   `kake\tok\t/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`
   Same W04 fires identically on the base tree (below) — pre-existing, not introduced this round.

2. `bash .../sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → exit 0, stderr empty.
   (out/census-root.out, sha256 eddfcc840b75e9ef91b38a65e0678e43d0c7093f9731d6c80658a647dc81727b):
   kake rows 66 · tier.A 55 tier.B 1 tier.C 10 tier.invalid 0 ·
   status.mined 51 queued 6 rejected 9 invalid 0 · FLEET identical, missing 0.
   w1/ExecCensusModeReceipt.md recorded rows 65 / tier.A 54 / mined 50 mid-wave —
   consistent with S065 landing at b1752a2 and S066 at e490381 (see below).

## Row counts (git show <rev>:corpus/SOURCES.md | grep -c '^| S0')

- 5777d5af (base): 64 (exit 0)
- bc6c4a8d (declaration): 64 — claim declared before the rows landed; consistent.
- 0a0acfb1 (tip): 66 (exit 0)

`git diff --stat base..tip corpus/SOURCES.md`: 1 file, +2 lines, the two new
registry rows. `git log` base..tip on that file: b1752a2 (+S065), e490381 (+S066).

## Before→after tier/status split (census on git-archived trees, fake roots)

Fake roots at out/{before,after}-root/ (conf `kake|kake-shokunin`), trees from
`git archive`; census `--root <root> kake` — both exit 0:

- before (5777d5af): rows 64 · A53 B1 C10 · mined 49 queued 6 rejected 9
- after (0a0acfb1): rows 66 · A55 B1 C10 · mined 51 queued 6 rejected 9
- delta: +2 rows, both tier A / status mined (S065 kind=code, S066 kind=dataset;
  neither community — contract holds). grep counts equal census rows at both
  revs: no row-shaped lines outside ## Registry.

`validate --today 2026-10-22` on both extracted trees → exit 0 each, identical
pre-existing W04(S033), no E-codes, no new W-codes (W01/W02/W03 absent).

## Freshness spot-check (outside counter scope)

Upstream clone /fast/scratch/hyaku/kake-r33/ds4cc-upstream: `cat-file -t
7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` → commit; committer/author date
2026-10-21T17:32:55Z (matches declared); subject "magga: Frostbite — Classic &
Remastered at /magga/frostbite/"; `show --stat`: 3 index.html under
magga/frostbite/ (root, classic/, remastered/) and sitemap.xml +3 lines —
consistent with the declared "+3 locs" and S065's scope wording.

Working-tree corpus/SOURCES.md sha256 (836166c3…dca) equals the git-archived tip
copy — the live validate/census readings reflect the tip blob exactly.

## Findings

None. Census behavior and registry delta are honest: 64→66 rows, clean cutover
(S065, S066 both mined/A), no new validate findings, FLEET metrics coherent,
upstream pin exists with the declared timestamp and footprint.

## Not verified

- c2_pin_count counter conditions (blob-identity of retained bytes, audit
  section numbers) — other seat/counter scope.
- `overdue`/`shared` modes — not requested.
- Local ~/Projects/ds4cc-marketplace checkout pinned behind at 1fbdb8ed (S065
  asserts this) — read-path check not performed; row's own scope disclaims it.

No tools installed or updated (bash/git/coreutils/gawk sufficed). No lane file
changed except this report.
