# ExecValidateAppend

Claim C3, C7 tooling: round-59 append-block validation script, written from
`.ufo/waves/round-58/validate_append.sh` with round-59 paths, the whole working-tree corpus mirrored,
and the **non-corpus used-by target list derived at run time from the registry's own used-by cells**
(not copied from round 58's hard-coded list).

Delivered file (only path this seat wrote in the lane, besides this report):

- `.ufo/waves/round-59/w1/ExecValidateAppend.files/validate_append.sh` (mode 755, `bash -n` clean)
- `.ufo/waves/round-59/w1/ExecValidateAppend.files/validate_append.dryrun.txt` (dry-run receipt)

The lane-level `.ufo/waves/round-59/validate_append.sh` (untracked in the lane working tree when this
seat started) was **not** modified — it is a separate file; this seat's deliverable is the copy under
`w1/ExecValidateAppend.files/`.

## SCRIPT:

```bash
#!/usr/bin/env bash
# Round-59 append-block validation (C7 receipts). Re-run after ANY edit to corpus/SOURCES.md or the two
# adopted entries (crawler-identity-signals.md, googlebot-verification.md): mirrors the working-tree
# corpus/ (registry + entries included) into .ufo/waves/round-59/assimilation/validate/ and gates the
# append on `sources-census.sh validate --file <mirror registry>` (exit 0 required).
#
# The non-corpus used-by targets are DERIVED at run time from the registry's own used-by cells (the
# mined rows of the `## Registry` section) — not copied from round 58's list. The census resolves every
# used-by path relative to the mirror root, so a mined row that names a target outside corpus/ makes
# that target a mirror member; a mined row naming a target that is absent from the lane leaves it
# absent from the mirror and the census reports E11 (exit 1) on its own.
#
# LANE may be overridden (env) to validate a scratch copy of the lane; it defaults to the lane.
set -u
LANE="${LANE:-/home/vgpnk/Projects/shokunin/kake-shokunin}"
CENSUS="${CENSUS:-/home/vgpnk/Projects/shokunin/scripts/sources-census.sh}"
V=".ufo/waves/round-59/assimilation/validate"
cd "$LANE" || exit 64
rm -rf "$V"; mkdir -p "$V"
cp -r corpus "$V/corpus"   # whole-corpus mirror: the census checks that every used-by path exists

# --- derive the non-corpus used-by targets from the registry's used-by cells (mined rows) ---
# Row parsing mirrors the census parser: `## Registry` section only, 0-3 leading spaces, 11 cells
# (NF==13 with the leading/trailing empty fields), status in column 9, used-by in column 12.
# A cell is a path only when it is ASCII and looks like a relative path; "—" and "-" are skipped.
# Only `mined` rows are considered: the census existence check (E11) covers mined rows only, so
# those are exactly the used-by targets the mirror has to carry outside corpus/.
gawk -F'|' '
function trim(s) { gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
function pathlike(s) { return (s ~ /^[A-Za-z0-9._][A-Za-z0-9._\/-]*$/) }
{
  line=$0
  if (line ~ /^ {0,3}##[ \t]/) { sub(/^ {0,3}/,"",line); in_registry=(trim(substr(line,3))=="Registry"); next }
  if (line ~ /^ {0,3}#[ \t]/) { in_registry=0; next }
  if (!in_registry) next
  if (line !~ /^ {0,3}\|/) next
  sub(/^ {0,3}/,"",line); $0=line
  if (NF!=13) next
  if (trim($9)!="mined") next
  ub=trim($12)
  n=split(ub, cells, ",")
  for (i=1;i<=n;i++) {
    p=trim(cells[i])
    if (!pathlike(p)) continue          # "—", "-", empty and any non-path cell
    if (p ~ /^corpus\//) next           # already in the whole-corpus mirror
    print p
  }
}' corpus/SOURCES.md | sort -u > "$V/used-by-targets.txt"

missing=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in
    /*|../*|*/../*|*/..) missing="$missing $f"; continue ;;   # never leave the lane root
  esac
  if [ -e "$LANE/$f" ]; then
    mkdir -p "$V/$(dirname "$f")"
    cp -p "$LANE/$f" "$V/$f"
  else
    missing="$missing $f"
  fi
done < "$V/used-by-targets.txt"

ARGV="$CENSUS validate --file $V/corpus/SOURCES.md"
printf '%s\n' "$ARGV" > "$V/census-argv.txt"
$ARGV > "$V/census-stdout.txt" 2> "$V/census-stderr.txt"
rc=$?
echo "exit=$rc" > "$V/census-exit.txt"
cat "$V/census-exit.txt"; tail -1 "$V/census-stdout.txt"
[ -n "$missing" ] && echo "MISSING_USED_BY_TARGETS:$missing" >&2
exit "$rc"
```

Delta vs round 58 (`git show 45a92b64:.ufo/waves/round-58/validate_append.sh`): round-59 mirror path
`.ufo/waves/round-59/assimilation/validate`; `LANE`/`CENSUS` are env-overridable (LANE defaults to the
lane) instead of hard-coded; the five non-corpus used-by targets are **computed** from the registry
instead of hard-coded; `cp -p`; the script's own exit status now mirrors the census exit status
(round 58 always exited 0); `tail -1` (the `file<TAB>ok<TAB>…` line) instead of `tail -2`; the census
stderr is captured but the exit line is still written to `census-exit.txt` in the counter's expected
`exit=N` form. The counter's C7 requirements are met: `census-argv.txt` holds a single `--file
.ufo/waves/round-59/assimilation/validate/corpus/SOURCES.md` (no `--root`), `census-exit.txt` holds
`exit=0`, and the last stdout line is `file<TAB>ok<TAB><mirror registry>`.

## USED-BY TARGETS:

Derivation (run-time, over the lane's live `corpus/SOURCES.md`, `## Registry` section only, `mined`
rows only, `used-by` cell split on commas, ASCII path-like cells, `corpus/`-prefixed cells dropped
because the whole-corpus mirror already carries them):

| used-by target (non-corpus) | named by (mined rows) |
|---|---|
| `SCORECARD.md` | 9 rows |
| `scripts/source_recheck.py` | 5 rows (S088–S092) |
| `SKILL.md` | 1 row (S124) |
| `.ufo/waves/round-41/c1_count.py` | 1 row |
| `.ufo/waves/round-41/oracle_crosscheck.py` | 1 row |

Counts are from the base registry at `fd6303ce5c14b3f892dec586297a942ab6e4193b` (162 rows: 132
`mined`, 22 `rejected`, 8 `queued`); 65 distinct used-by paths, 60 under `corpus/`, 5 outside it. The
derived set happens to equal round 58's hard-coded list — but it was re-derived from the registry
cells, not copied: the derivation is what makes the script correct for the two new rows, whose
used-by cells (`corpus/knowledge/crawler-identity-signals.md`, `corpus/knowledge/crawler-identity.md`,
`corpus/knowledge/googlebot-verification.md`) are corpus paths covered by the corpus mirror, and it
keeps the script correct if a future mined row names a new non-corpus target.

Non-mined rows were checked and need no mirror member: the four `rejected` rows with a used-by cell
(S101, S125, S128, S134) all name `corpus/` paths, and the one `queued` row (S056) carries the literal
`-`, which is not a path and is skipped by the path-like filter (the census's own existence check,
E11, also only applies to `mined` rows).

The mirror therefore contains, under `.ufo/waves/round-59/assimilation/validate/`:
`corpus/` (whole tree: registry + every entry + lessons), plus the five non-corpus targets at their
repo-relative paths (`SCORECARD.md`, `SKILL.md`, `scripts/source_recheck.py`,
`.ufo/waves/round-41/c1_count.py`, `.ufo/waves/round-41/oracle_crosscheck.py`) — exactly the layout
round 58 committed, so the counter's C7 lookup of `VALIDATE/<entry path>` resolves for both new
entries (`corpus/knowledge/crawler-identity-signals.md`, `corpus/knowledge/googlebot-verification.md`).

## DRY RUN:

Scratch copy of the lane (never the lane itself): `git clone -q --shared` of the lane into
`/fast/scratch/hyaku/kake-r59/ExecValidateAppend/lane-copy`, `git rev-parse --show-toplevel` ==
that path (verified), at lane HEAD `cb68527`. Into the scratch copy only: two draft registry rows
`S425` / `S426` appended to the `## Registry` section (11 cells, `docs`/A/`mined`/`2026-10-27`/`90d`,
used-by = the three corpus paths above) and stub entry files
`corpus/knowledge/crawler-identity-signals.md`, `corpus/knowledge/googlebot-verification.md`.

Command (LANE override; the script's default LANE is the lane, and the lane was never used as the
target of a run):

```
LANE=/fast/scratch/hyaku/kake-r59/ExecValidateAppend/lane-copy \
  bash /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/w1/ExecValidateAppend.files/validate_append.sh
```

Result — **exit 0**; stdout (2 lines), stderr empty (0 bytes):

```
exit=0
file	ok	/fast/scratch/hyaku/kake-r59/ExecValidateAppend/lane-copy/.ufo/waves/round-59/assimilation/validate/corpus/SOURCES.md
```

**Last stdout line:**

```
file	ok	/fast/scratch/hyaku/kake-r59/ExecValidateAppend/lane-copy/.ufo/waves/round-59/assimilation/validate/corpus/SOURCES.md
```

`census-argv.txt` (as written): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--file .ufo/waves/round-59/assimilation/validate/corpus/SOURCES.md` — one `--file`, no `--root`.
`census-exit.txt`: `exit=0`. The 14 `W04` same-URL-across-scopes warnings of the base registry are
carried through unchanged (warnings do not change the exit status); no `E0x` finding.

Negative controls (each run against the same scratch copy, restored afterwards):

| control | mutation | result |
|---|---|---|
| A | `SKILL.md` hidden in the scratch lane | script exit **1**; census `file E11 S124 missing used-by SKILL.md`; script also prints `MISSING_USED_BY_TARGETS: SKILL.md` — a mined row's non-corpus target is genuinely required in the mirror |
| B | target present in the lane but deleted from the mirror by hand, census re-run | census exit **1**, `file E11 S124 missing used-by SKILL.md` — the mirror member is what satisfies E11, not the lane |
| C | draft entry `corpus/knowledge/crawler-identity-signals.md` removed from the scratch corpus | script exit **1**; `file E11 S425 missing used-by corpus/knowledge/crawler-identity-signals.md` — the whole-corpus mirror carries the new rows' used-by entries |

All three controls were reverted and the clean run re-confirmed at exit 0. The lane working tree was
not touched by this seat beyond the two files under `w1/ExecValidateAppend.files/` (the `M` entries on
`.ufo/waves/round-59/c59_axis_evidence.py` / `c59_quote_truth.py` in `git status` are other seats'
in-flight edits, present before this seat ran anything).

Tooling: none installed, none needed (`bash`, `gawk`, `cp`, `git` are pre-existing system binaries;
the operator's pacman pause was not exercised). Scratch dir
`/fast/scratch/hyaku/kake-r59/ExecValidateAppend/` removed after the receipt
(`.ufo/waves/round-59/w1/ExecValidateAppend.files/validate_append.dryrun.txt`) was copied out.

## RISKS / NOTES:

- The script writes its receipt into the lane at `.ufo/waves/round-59/assimilation/validate/`
  (`rm -rf` then rebuild) — the round-58 pattern; the L1 must run it against the lane after the
  append lands so the mirror registry is byte-equal to the landed registry (counter C7 requires
  byte-equality of `VALIDATE/corpus/SOURCES.md` with the landed `corpus/SOURCES.md`).
- The mirror's `used-by-targets.txt` is an extra file inside `VALIDATE/`; the counter's C7 check
  does not read it (it only reads `census-argv.txt`, `census-stdout.txt`, `census-exit.txt`,
  `VALIDATE/corpus/SOURCES.md` and `VALIDATE/<entry>`), so it is inert evidence. If the L1 prefers
  the round-58 file set exactly, deleting that one line from the script is safe.
- The census resolves `--file` relative to the current directory; the script `cd "$LANE"` first, so
  the argv line and the mirror path stay lane-relative exactly as in the round-58 receipt.

VERDICT: Round-59 `validate_append.sh` written (lane-relative paths, env-overridable LANE, run-time derivation of the non-corpus used-by targets from the registry cells), dry-run green at exit 0 with the last stdout line `file<TAB>ok<TAB><mirror registry>`, and three negative controls confirm the derived targets and the corpus mirror are load-bearing.
