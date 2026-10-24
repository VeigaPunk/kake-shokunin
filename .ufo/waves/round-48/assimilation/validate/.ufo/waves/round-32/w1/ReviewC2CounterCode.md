# ReviewC2CounterCode — attack on .ufo/waves/round-32/c2_retained_count.py

Sandbox: /fast/scratch/hyaku/kake-r32/w1/ReviewC2CounterCode/ (clone at HEAD=4d13e68f82e96ea8025e3abb8d22e4f8f2adb016, lane tip; counter unchanged since 5b32cc7). Baseline: `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev HEAD --repo .` → met=3, exit 0.

## Findings (severity high → low)

### F1 — c2 counts any matching row; a fabricated row can produce met=3 with S062 itself absent (HIGH)
`c2` never pins the row id to `S062` (claim: "registered as SOURCES row S062"). Any 11-cell row whose source cell contains both substrings and whose opened cell is 2026-10-22 satisfies it. Combined with F2, the real S062 row can sit outside the scanned window while a planted row wins:
- Mutant B2 (rev 5d2d785107f7790e64db8659f9831f1e75881b4c in sandbox): preamble prose "see ## Registry" + fake row `S900 | ds4cc-marketplace ... 1fbdb8ed | ... | 2026-10-22` placed BEFORE the real `## Registry` heading; entry given one bare "S900" mention. Output: `c2RowIds ["S900"], c3Cites {"S900":1}, met=3` — identical to the declared good result, with the genuine S062 row unexamined.

### F2 — "## Registry" window starts at the first substring occurrence, not the heading line (HIGH)
`c2_retained_count.py:51` `sources.split("## Registry", 1)[-1]` matches the literal string anywhere — prose ("see ## Registry"), a `### Registry` subheading, or a code fence. Anything before the real heading then lands inside the window.
- Mutant B1 (fb5d2116a1624794011be7478eae6f1267cec896): fake S900 row before the real heading → `c2RowIds ["S900"], met=2`; the real registry was cut off by the `\n## ` terminator.
- Mirror case: if `## Registry` is renamed, a later mention (prose or `### Registry`) makes the window run to EOF, counting rows in `## Search log`/`## Leads`.

### F3 — 11-cell `split("|")` breaks on a pipe inside a cell (MEDIUM)
`line 55` `len(cells) == 11` counts a row only if naive `|` splitting yields exactly 11 cells. A literal `|` or GFM-legal escaped `\|` inside any cell splits it into 12 → the row is skipped silently.
- Mutant A1 (bc82c3bfc6ada86dc6c5b3dd34e81518e34169a3): `x|y` appended inside S062's source cell → `met=1` (c2 and c3 lost).
- Mutant A2 (2ba157202786c8b203df1967b5e17ca37e5304b8): `x\|y` (renders as one GFM cell, table still valid) → `met=1`.
This is a false-negative direction: a genuinely compliant registry can report met=1.

### F4 — a `## ` line inside a fenced block inside Registry truncates the window (MEDIUM)
`line 51` end split `.split("\n## ", 1)[0]` is not fence-aware.
- Mutant F (15f069a4ce4b77ab3a1bba38588608d8910c7c0a): ```` ```text / ## fake-heading-inside-fence / ``` ```` inserted right before the S062 row → `met=1`, S062 invisible.

### F5 — c1 ignores path: "retained at .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/" is not verified (MEDIUM)
`lines 41-49` collect blob OIDs from `git ls-tree -r` for the whole repo; any path holding the OID passes.
- Mutant C (84843194bc0606dc9f0cdcd8898e72ac288477ac): `git mv .ufo/waves/round-32/sources/ds4cc-1fbdb8ed attic/` → `met=3`, `c1BlobPaths` points at `attic/…` — a rev with nothing retained at the claimed location scores full marks.

### F6 — c1 ignores mode: a symlink or executable counts as a byte-identical retained file (MEDIUM)
`line 46` checks `parts[1] == "blob"` but not the mode. Git stores symlinks (120000) and executables (100755) as blobs.
- Mutant D (3aff98856e04a1e9323df8610e8b23ca567d802f): `render.yaml` replaced by a symlink whose target string is the blob's bytes (same OID d17ab7e5…) → `met=3`. `ls-tree`: `120000 blob d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`. Checked out, that path is a dangling symlink, not a readable retained copy — the "read offline" claim is not honored.

### F7 — c3 counts any `\bS<rid>\b` occurrence, not a citation of the row/retention (LOW)
`line 60` `re.findall(r"\b%s\b" % rid, entry)` scans the whole file.
- Mutant E (9daf740391addbdc661a8325f8c7e5999a976ab2): the appended "Retained copies" section deleted; a bare "Tracked under registry row S062." in the intro → `met=3`. A passing c3 does not show the entry cites retained copies; a negating or unrelated mention suffices.

## Prompt items checked with no defect
- `\b` regex vs `S0620`: safe — `\bS062\b` does not match S0620/XS062; ids come from `re.fullmatch(r"S\d{3}")` so no injection. (Real defect is scope, F7.)
- Submodule gitlink: `ls-tree` type is `commit`, fails the `blob` check — correctly excluded.
- Header/separator rows: `S\d{3}` fullmatch skips them.
- Short rows: `cells[8]` is under `len==11` guard — no IndexError.

## Commands run (all exit 0)
Per mutant: `git worktree add` + file edit + `git -c user.email=p@t -c user.name=p commit` + `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev HEAD --repo .` inside each sandbox worktree. Mutant revs: A1 bc82c3b, A2 2ba1572, B1 fb5d211, B2 5d2d785, C 8484319, D 3aff988, E 9daf740, F 15f069a (all under /fast/scratch/hyaku/kake-r32/w1/ReviewC2CounterCode/).

## Not verified
Fix proposals are implicit only; did not test `--rev` resolution edge cases, quoted-path parsing in `ls-tree` (tabs in filenames), or non-UTF8 SOURCES.md. No lane files mutated; report file is the only lane write.

Tooling: none installed.
