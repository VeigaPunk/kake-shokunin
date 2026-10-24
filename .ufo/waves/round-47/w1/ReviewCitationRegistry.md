# ReviewCitationRegistry — `commit-citation-lint` row vs `scripts/citation_lint.py`

Seat: reviewer (operability). Round 47 v1 wave 1. Read-only lane evidence; no production
file, index, ref, `.jj`, or `.ufo/state` touched. Scratch used only under
`/fast/scratch/hyaku/kake-r47/ReviewCitationRegistry/`.

Method: direct reads of `SKILL.md:1198`, `scripts/citation_lint.py` (all 343 lines),
`corpus/knowledge/commit-citation-hygiene.md`, `corpus/QUALITY.md:1071`, the r46 receipts,
plus runtime probes at `HEAD` (766f461), frozen base `cd42e3c`, `7cdbaefd…`, `ee43e66…`.
**No LSP device is mounted** (`xd://lsp` → `No such tool … Mounted devices: ast_edit, debug`),
so caller/definition checks are source-and-runtime, not index-semantic; this is recorded as a
verification gap, not a semantic pass.

## Verdict on C1 for this row

The row exists (`SKILL.md:1198`), is committed at `HEAD` with all eight Gate-standard columns,
and its selftest receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` is
committed at `HEAD` (`git ls-tree -r HEAD --name-only .ufo/waves/round-47/verification/`) with
`tool_sha256: 3c78a0a8…987f` equal to `sha256sum scripts/citation_lint.py` and to
`git show {HEAD,cd42e3c,714e707}:scripts/citation_lint.py | sha256sum`, tally `selftest: 8/8
passed`, `exit=0`. The frozen base has no row and no receipt (`git show cd42e3c:SKILL.md |
grep -c commit-citation-lint` → `0`; `git ls-tree -r cd42e3c --name-only | grep -c round-47`
→ `0`). Counter: `python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision HEAD`
→ `registry_rows=2/2 receipts=2/2 C1_MET`, exit 0; at `cd42e3c` → `0/2 0/2 C1_NOT_MET`, exit 1.
**C1 holds for this row.** No row-vs-shape contradiction was found on frozen population, `--root`,
the 0/1/64 map, selftest spelling, ledger path, write scope, or owner. The findings below are
exit-map and semantics defects, not a falsification of the C1 claim.

## Findings by severity

### M1 (Medium) — A missed ledger is reported as `1=violations found`, not `could-not-evaluate`

The row's map has exactly one non-usage could-not-evaluate class: `2=could-not-evaluate
(population unreadable)` (`SKILL.md:1198`). The write-scope cell says the tool "reads population
+ ledger". `load_adjudications` swallows both the working-tree `OSError` and a failed
`git show <rev>:<ledger>` and returns `{}` (`scripts/citation_lint.py:110-131`); `main` never
distinguishes that from a real clean/red scan (`:314-316`).

Repro (read-only, lane root):

```
python3 -B scripts/citation_lint.py --root . --adjudications nope-missing.md
→ exit=1, stderr empty, JSON {"adjudications":"nope-missing.md","violations":30,"adjudicated":0}
```

A typo'd `--adjudications` therefore presents as 30 dead citations with `1=violations found`,
the same observable shape as a genuine policy failure. The silent empty return is load-bearing
for the pinned before-value (the ledger does not exist at `7cdbaefd`: `git cat-file -e
7cdbaefd:corpus/quality/citation-adjudications.md` → fatal), so the fix is a distinguishable
input diagnostic, not "always exit 2". Either way the row does not tell an operator what a
missing named ledger does; today the answer is "violations, exit 1".

### M2 (Medium) — Previous-line context carry is material, undocumented, untested, and overreaches

`scan` sets `context_line = line if CONTEXT_RE.search(line) else prev_line`
(`scripts/citation_lint.py:148`) and accepts the token when `CONTEXT_RE` matches that
carry (`:163`). Both the tool docstring ("Citation context: the token's line names a
commit-bearing relation", `:15-16`) and `corpus/knowledge/commit-citation-hygiene.md:17-20`
("A commit citation is a hex token in a commit-bearing context") describe same-line context
only; the previous line is never named.

Materiality is not theoretical: **13 of the 28 pinned base violations are adjacency-derived**
(no commit word on their own line). Reconstructed from
`.ufo/waves/round-46/verification/c2-before-7cdbaefd.json` and the `7cdbaefd` blobs:
`SCORECARD.md` lines 907/1416/1418/1453/1458/1552 and `LOG.md` lines 49 (×3)/166/249 (×2)/630.
Example: `SCORECARD.md:906` ends with "hollow commit (sandbox"; line 907 is a wrapped
continuation `  \`b6580c79\`) that the declared C2 counter scores 4/4…` — its own line has no
context word, yet it is filed as a violation at line 907. So the pinned "28 violations" is
count-accurate but is not "28 lines naming a commit relation" as the documentation implies.

Overreach demo (scratch fixture, resolving token on line 1):

```
files = {"SCORECARD.md": ["measured at commit 228451bf…c5af resolves",
                          "plain token cafe012 sits in prose"]}
scan(...) → [{'file':'SCORECARD.md','line':2,'token':'cafe012','reason':'dead_citation'}]
```

A self-contained sentence is judged by its predecessor; on a population that happens to place a
plain hex token after a citation line, a clean tree exits 1.

The 8/8 selftest does not cover this branch: a scratch mutant replacing line 148 with
`context_line = line` still prints `selftest: 8/8 passed`, exit 0. The eight checks
(`scripts/citation_lint.py:237-286`) and the selftest population never place a non-context
line directly after a context line. Current population is unaffected: gate at `HEAD`,
`cd42e3c`, `766f461` → exit 0, 0 violations, 30 adjudicated.

### L1 (Low) — Exit 2 has a second, undeclared path

`--json` write failure returns `EXIT_INPUT` (`scripts/citation_lint.py:330-336`):

```
python3 -B scripts/citation_lint.py --root . --json /nonexistent-dir/x.json
→ citation_lint.py: cannot write JSON output: [Errno 2] …
→ exit=2
```

The row's 2 is "population unreadable" only. Under the row's entry command (no `--json`) the
map is exact; against the optional flag named in the same row's write scope it is not, and a
caller mapping 2→"population unreadable" misdiagnoses a permissions/full-disk failure.

### L2 (Low) — `--selftest` is dispatched before validation; the tool's own guard is dead

`main` returns `selftest()` whenever `--selftest` appears (`scripts/citation_lint.py:300`),
before `parse_cli`, making the `--selftest takes no --root` guard at `:77-78` unreachable.
Observed: `--selftest --root .` → exit 0 and runs the selftest (not the documented usage
error); `--selftest --json /tmp/x.json` → exit 0, no file written; `--help --selftest` →
selftest output. The row's spelling `python3 -B scripts/citation_lint.py --selftest` is correct
and works; this is a misuse-path defect, not a row contradiction.

### L3 (Low) — Pinned receipt citations carry no sha256, and the "after" glob is not receipt-unique

The row files counts (`28 violations (17 unique tokens)`, `30 adjudicated occurrences`,
`8/8`) against receipts cited only as `.ufo/waves/round-46/verification/c2-{before,after}-*.json`
and by receipt path for the selftest. `corpus/QUALITY.md:1071` ("Receipt identity for filed
counts") requires "that receipt's path + sha256" and re-derivation from the named committed
bytes, "rather than another same-named receipt's values". Two receipts match the after-glob:
`c2-after-ee43e66.json` (revision `ee43e66…`, sha256 `1d9a5a23…c085f9`, clean/0/30) and
`c2-after-working.json` (revision `null`, sha256 `2a333f07…acef3e`, clean/0/30). The row's
`ee43e66…` wording disambiguates, and every filed number re-derived exactly (below), but the
citation itself cannot bind a reader to one byte sequence. The selftest receipt's own sha256
(`b3902de6…b735`, verified) is likewise absent from the row.

## Checks that match (verified, not inferred)

| Axis | Row (`SKILL.md:1198`) | Script / evidence |
|---|---|---|
| Frozen population | `{SCORECARD.md, LOG.md}` | `POPULATION` tuple `:37`; no CLI/env override in `parse_cli :66-79` |
| `--root` required | `--root .` in entry command | `required=True` `:70`; no root → exit 64 `the following arguments are required: --root`; duplicate `--root` → 64 `--root given more than once` |
| Exit 0 / 1 | `0=clean`; `1=violations found (file, line, token)` | `7cdbaefd…` → exit 1, 28 violations, 17 unique tokens (matches receipt and row); `ee43e66…` → exit 0, 30 adjudicated (matches); `HEAD`/`cd42e3c`/`766f461` → 0/30 |
| Exit 2 | `could-not-evaluate (population unreadable)` | `--root /tmp` → exit 2 `cannot read SCORECARD.md` (extra path: L1) |
| Exit 64 | `usage` | `--bogus` → exit 64; missing/duplicate `--root` → 64 |
| Selftest spelling/tally | `python3 -B scripts/citation_lint.py --selftest` (8/8) | live run → `selftest: 8/8 passed`, exit 0; receipt names tool path + `tool_sha256` + tally + `exit=0` |
| Ledger reference | `corpus/quality/citation-adjudications.md` | `DEFAULT_ADJUDICATIONS` `:38`; present at `HEAD` and `ee43e66`, absent at `7cdbaefd` (consistent with the before/after pins); 20 ledger rows → 30 occurrences, 20 unique `(token,file)` pairs |
| Write scope | "reads population + ledger; writes only an optional `--json` report path" | only `open(args.json,"w")` `:330-336`; otherwise prints stdout; selftest writes a temp git repo only (row omits that selftest temp write; other rows state it) |
| Owner | `kake` | same as every other registry row (e.g. `:1045`, `:1066`, `:1067`, `:1092`, `:1127`, `:1197`) |
| Kind offline/no network | `gate (offline; no network)` | imports `argparse,json,os,re,subprocess,sys,tempfile` `:24-30`; subprocess is `git show/rev-parse` only |

## Residual risk

- The 8/8 selftest never calls `main`, `parse_cli`, `read_population`, or `load_adjudications`.
  Exit 2, exit 64, the `--root` requirement, and the `--revision` reader are evidenced only by
  the r46 receipts and my manual probes; mutants of `EXIT_INPUT` or `--root required=True`
  would keep 8/8.
- `c47_registry_count.py` credits a receipt on `needle in text` + `selftest: 8/8 passed` +
  `exit=0` + any 64-hex (`.ufo/waves/round-47/c47_registry_count.py:116-131`); it does not bind
  `tool_sha256` to the tool bytes. C1 holds here only because the hashes were compared
  directly; the counter alone would not catch a stale receipt hash.
- Ledger key is `(token,file)`, so every occurrence of an adjudicated token is suppressed —
  already declared as inherited residual scope (`commit-citation-hygiene.md:65-72`); not
  re-adjudicated here.
- M2 means a "dead" verdict can attach to a line that names no commit; the ledger classes
  record why an adjacency hit is not a violation, but a new wrapped plain token after a
  citation line will add a false violation until adjudicated.

## Verification gaps

- LSP unavailable (`xd://lsp` → no such tool; mounted devices `ast_edit`, `debug`), so no
  semantic references/definition pass; findings are source-line and runtime evidence.
- No `--adjudications` absolute-path probe under `--revision` (it would form
  `git show REV:/abs/path` and fail closed to `{}`); not tested, not claimed.
- Mutation controls were limited to the scratch selftest mutant (line-148 carry removal);
  the scratch clone was local only and nothing was pushed.
