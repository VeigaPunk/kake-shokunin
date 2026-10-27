# ExecValidateAppend

Claim C3 condition C7 tooling: round-60 `validate_append.sh` + mirror-pin JSON generator, dry-run in scratch only. Lane repo untouched (verified: no writes outside `.ufo/waves/round-60/w1/ExecValidateAppend*`).

## SCRIPT:

Two files in `.ufo/waves/round-60/w1/ExecValidateAppend.files/`:

- `validate_append.sh` — adaptation of `.ufo/waves/round-59/validate_append.sh`. Round-60 changes:
  - Mirror is built at the pinned base, never the worktree: `git archive 97cdc122... corpus | tar -x -C <work>` (the lane has no `.gitattributes`, so archive bytes == worktree bytes for `corpus/`; confirmed identical sha256 to the committed pre-append mirror).
  - Non-corpus used-by targets are re-derived from the BASE registry with `gawk`, restricted to `status=mined` rows (the census `usedby_findings` reads only mined rows; base S056 is `queued` with a `-` used-by cell, which is why a naive all-rows extraction pulls a bogus `-` path — first dry run caught this). Base yields exactly the round-59 set: `SCORECARD.md`, `SKILL.md`, `scripts/source_recheck.py`, `.ufo/waves/round-41/c1_count.py`, `.ufo/waves/round-41/oracle_crosscheck.py`, each extracted via `git show BASE:path`.
  - `--rows <file>` (repeatable, concatenated in order) is inserted immediately after the LAST `|`-row of `## Registry` (located as the last table row before the next `## ` heading — `## Paths` at line 174 in the base file), so the 3-row block lands inside the Registry section, not after it.
  - `--file <repo-rel>[=<src>]` overlays admitted files at repo-relative paths (the two new entries + `corpus/lessons/round-60.md` for the C3 run; the `googlebot-verification.md` correction is in-file, so it is already in the base mirror and needs no `--file`). `rel=src` reads `src` instead of the lane worktree — needed for scratch dry runs and for staging uncommitted drafts. Missing src → warn + leave absent so the census reports E11 honestly.
  - Census: `sources-census.sh validate --file <work>/corpus/SOURCES.md`; `--file` makes the census resolve used-by paths under `<work>/`. Script exits with the census exit verbatim (0 clean / 1 findings / 2 usage); 64 on bad args.
  - Receipt: default `$LANE/.ufo/waves/round-60/controls/validate-append.txt` (single self-contained receipt: date, argv, base, rows-appended count, files-admitted, registry row count, exit, full census stdout+stderr); `--receipt`/`--work`/`--today`/`--keep-work` overridable. Census artifacts also kept in `<work>/census-{argv,stdout,stderr,exit}.txt` as in round 59.
- `mirror_pin.sh` — mirror-pin JSON generator (C8): materializes `corpus/SOURCES.md` at `97cdc122379711c2b02a8970752c8782da3ac81d` to `<root>/<path>` (default the committed `assimilation/pre-append/corpus/SOURCES.md`) and writes the pin to `<root>/<pin>` (default `assimilation/mirror-pin.json`); JSON also goes to stdout. `--root` pointing at scratch touches nothing in the lane (dry-run mode); default root is the lane (L1 run).

## DRY RUN:

Executed in `/fast/scratch/hyaku/kake-r60/ExecValidateAppend/` only (dummy inputs preserved in `.files/dry-run/`):

- `mirror_pin.sh --root <scratch>`: emitted pin JSON `cmp`-identical to the committed `.ufo/waves/round-60/assimilation/mirror-pin.json`, and the materialized mirror `cmp`-identical to the committed `pre-append/corpus/SOURCES.md`.
- `validate_append.sh --rows rows.md --file x3 --work <scratch> --receipt <scratch>` with three dummy well-formed rows (S427 `supersedes S425 —`, `common crawlers`/`special-case crawlers` scope; S428 two used-by paths; S429) and three dummy entries (`google-user-triggered-fetchers.md`, `robots-txt-limits.md`, `lessons/round-60.md`):
  - `exit=0`; census stdout `file ok` + W04 warnings only (the 14 base W04s plus `S427 duplicate url .../overview-google-crawlers across scopes` — expected: S427 deliberately re-opens S425's URL; W-codes do not affect exit).
  - Mirror diff vs base registry = exactly the 3 inserted rows at lines 173–175 (registry-rows-after: 167); overlaid files present at repo-relative paths; all 5 non-corpus used-by targets present.
  - Negative path exercised (pre-fix run): missing `--file` sources → census `E11 missing used-by` + script exit 1 — the check fails honestly instead of masking.
  - `validate_append.sh` with no `--rows` → usage + exit 64.
- Full dry-run receipt: `.files/dry-run/receipt-dry-run.txt`; dummy rows: `.files/dry-run/rows-S427-S429-dummy.md`.

## MIRROR PIN:

Base registry `corpus/SOURCES.md` at `97cdc122379711c2b02a8970752c8782da3ac81d` (lane master at round open):

- rows: 164 (registry `| S[0-9]` rows inside `## Registry`; matches `assimilation/reg-ids` line count)
- bytes: 152817
- sha256: `bc054d10868d3dd5e59b60f71134d21ee974bb63a0ff6a462f2d2048f76be119`

All three values match the committed `.ufo/waves/round-60/assimilation/mirror-pin.json` byte-for-byte; regenerated copy and mirror verified `cmp`-equal.

## L1 INVOCATION:

    ROWS=<real S427-S429 rows file>
    validate_append.sh --rows "$ROWS" \
      --file corpus/knowledge/google-user-triggered-fetchers.md \
      --file corpus/knowledge/robots-txt-limits.md \
      --file corpus/lessons/round-60.md
    # exits with the census code; receipt lands at .ufo/waves/round-60/controls/validate-append.txt
    mirror_pin.sh   # defaults regenerate the committed pre-append mirror + pin in the lane

## TOOLING:

No installs; bash + coreutils + gawk + git only (per RULES.md, nothing installed, pacman untouched).

## RISKS / NOTES:

- `--rows` content is not pre-validated for cell count; malformed rows surface as E01/E12 from the census (fail-closed). [INFERENCE: acceptable — census is the gate of record.]
- `git archive` honors `export-ignore` if a `.gitattributes` is ever added under `corpus/`; none exists at base.
- The W04 on S427 is structural (same URL, different scope) and matches the real row's semantics; it stays a warning, exit unaffected.

VERDICT: validate_append.sh + mirror_pin.sh delivered; dry run exits 0 with 3 dummy rows + 3 dummy entries; mirror pin reproduces the committed pin byte-for-byte (164 rows, 152817 bytes, sha256 bc054d10...f76be119).
