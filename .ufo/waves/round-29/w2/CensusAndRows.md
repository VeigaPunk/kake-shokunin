# KakeR29 wave 2 — CensusAndRows: registry conformance of round-29 rows

Attacked: kake `corpus/SOURCES.md` rows S040–S048 against CORPUS.md
"SOURCES.md — where a shokunin learns" (contract v1, frozen), plus the
append-only property vs base fe1805cf, using `scripts/sources-census.sh
validate`. Judged bytes: lane commit 7697990 (sandbox clone); the assigned
fleet-root run was also executed. Sandbox:
`/fast/scratch/hyaku/kake-r29/w2/CensusAndRows/` (clone + TMPDIR live there).
Script read-only claim verified by reading it: `validate` writes only stdout
unless `--out` is given (never given); only `selftest` touches temp files.

## Commands and exits (all read-only)

1. Assigned run, fleet root — exit 0:
   `TMPDIR=$S/tmp bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
   ```
   kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
   kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
   ```
2. Same tool on committed bytes — exit 0:
   `git clone -q <lane> $S/clone && git -C $S/clone checkout -q 7697990cbca20291f3b0367b8ff4220e93b38b03`
   then `sources-census.sh validate $S/clone` → same two lines, lane `ok`, only W04.
3. Base comparison — `git show fe1805cf…:corpus/SOURCES.md` vs
   `git show 7697990…:corpus/SOURCES.md`, S001–S039 extracted with the
   contract's own row regex, `cmp` → byte-identical, 39 rows each side.
4. Full-file diff base→7697990: 0 deletions, 12 insertions = rows S040–S048 (9),
   one `## Paths` bullet, one `## Search log` entry, one blank line.
   Append-only held; no pre-existing row edited in place.
5. Contract one-liners (CORPUS.md census block) on the registry: malformed
   (NF!=13) = 0; duplicate ids: none; kind/tier/status enum violations: none;
   community-at-A: none; extra check `status=rejected ⇒ teaches ~ /REJECTED: .*; flip: /`:
   no output.
6. Used-by existence at 7697990: `git cat-file -e 7697990…:corpus/knowledge/pages-base-path.md`
   and `…:corpus/lessons/round-29.md` → both exist; census E11: none.

## Per-clause results for S040–S048 (committed bytes, SOURCES.md:48-56)

- 11 cells in all 9 rows (E01 none, malformed=0); table header and separator
  match the contract's 11-column lines (SOURCES.md:7-8).
- ids S040–S048: next-unused, sequential, no duplicates (E02/E03 none).
- kind: docs×5 (S040–S043, S048), community×4 (S044–S047); all in enum.
- tier: A for official vendor docs (GitHub, Jekyll×2, Vite, Hugo), each scoped
  to that vendor's own documentation; C for all four community rows — community
  never A (E10 none). Registry-wide histogram: tier A=42, C=6.
- status: mined×4 (S040–S043), rejected×3 (S044–S046), queued×2 (S047–S048).
- opened 2026-10-22 (present date; E08 none); recheck 90d cadence (E09 none).
- used-by: mined rows cite corpus/knowledge/pages-base-path.md +
  corpus/lessons/round-29.md, both present in the commit; queued/rejected rows
  use `—`.
- rejects: S044–S046 all read `REJECTED: <reason>; flip: <what would change the
  verdict>` in the committed bytes (SOURCES.md:52-54). Anchors cite exact
  sections plus doc version/date; none is a bare homepage; S040 records its own
  redirect target honestly.
- Rule-1 gate: round-29 lesson `## Gate` has Source-openings entries for
  S040–S043 (URL, access date, ≤25-word quote, location;
  corpus/lessons/round-29.md:36-39) and Screened-candidates entries for
  S044–S048 (:51-55), plus a "Registry changes (old → new)" block logging all
  nine rows (:60-67). Rule-5 search log: round-29 bounded-question entry present
  (SOURCES.md:102).

## Findings

- None blocking. Verdict for this item: **holds** at 7697990.
- Observation, not a round-29 defect: the only census finding is W04 — S033 and
  S028 share www.rfc-editor.org/rfc/rfc9110.txt across two deliberately
  different scopes (media types vs URI schemes). Both rows sit inside the
  byte-identical S001–S039 set, so the warning predates round 29; wave-1's own
  `.ufo/waves/round-29/verification/census-before.txt` shows the identical
  output at base fe1805cf (exit 0). W04 is warning-class; the lane still
  validates `ok`, matching "warnings do not affect clean lanes".
- Working-tree drift noted, not judged: while I worked, the lane tree's
  S044–S046 teaches/anchor cells were revised in place relative to 7697990
  (in-flight wave-2 integration; `git diff --stat 7697990 -- corpus` showed
  SOURCES.md 3+/3−, pages-base-path.md 28±, QUALITY.md 21±, README.md 2±,
  12 dirty entries). I checked both revisions: the revised cells keep
  `REJECTED: …; flip: …` and pass the same one-liners, and the revised S044
  citation "S016 lists Jekyll 3.10.0" is accurate to the existing S016 row
  (SOURCES.md:24). The committed-bytes verdict does not depend on the moving
  tree.

## Not verified

- Live URLs were not fetched (bounds: no live probes of owned properties;
  pages here are third-party public docs). Freshness of the cited pages rests
  on the round-29 receipts referenced by the Gate — other seats' scope.
- Quote truth against retained source text (C1 counter) and the C2 matrix are
  out of my scope; I verified registry shape and citations, not quote
  provenance.
- Census modes other than `validate` were not exercised against the lane.
- The working tree is shared live state; WT observations are timestamped to
  this run and may be stale when read.

Tooling: no installs or upgrades needed (bash, git, gawk, coreutils only);
nothing installed, no pacman transactions run.
