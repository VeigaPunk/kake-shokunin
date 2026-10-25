# ResidualCensus — round-51 residual, round-end census

**Severity:** Informational — validate exits 0 with warnings only; census row count 145.

**Axes named:** operability (does the round-end instrument run clean on the landed registry), freshness (does the landed row count match what the round claims it landed).

**Exploit path:** None. No finding, no boundary touched: the registry is byte-identical to its committed blob at the lane HEAD, and nothing outside this one report file was written.

**Result:** `validate` exit **0** (12 × W04 duplicate-URL warnings, one `ok` line, no E-code); `census` exit **0**; **kake `rows` = 145**. Independently re-derived from the registry bytes as 145 rows, and the round's own append arithmetic (143 → 145) checks out against both base `007d66e` and the committed pre-append receipt.

## Invocation record

Run 2026-10-25 (system date `2026-10-25`, UTC clock `2026-10-25T06:50:10Z`, TZ `-03`). Both commands were invoked from the fleet root; neither was given `--today`, so date-relative checks used the system UTC date.

### 1. validate

argv, exactly as executed:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
```

exit code: **0**. stdout (1010 bytes, 13 lines), verbatim:

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

stderr: **empty** (0 bytes).

Per the script's own contract (header lines 17–18), exit 0 covers "clean or warnings", and W-codes never change status. No E01–E12 finding was emitted, so this is a clean-with-warnings pass — in particular no E11 (dangling `used-by` path), no E03/E04 (duplicate id / duplicate URL+scope), and no E12 (row-shaped source outside `## Registry`).

### 2. census

argv, exactly as executed:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake
```

exit code: **0**. stdout (319 bytes, 17 lines), verbatim:

```
kake	rows	145
kake	tier.A	122
kake	tier.B	6
kake	tier.C	17
kake	status.mined	115
kake	status.queued	8
kake	status.rejected	22
FLEET	rows	145
FLEET	tier.A	122
FLEET	tier.B	6
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	8
FLEET	status.mined	115
FLEET	status.rejected	22
FLEET	status.invalid	0
FLEET	missing	0
```

stderr: **empty** (0 bytes).

**kake row count: 145.** The FLEET block is numerically identical because `kake` was the only lane targeted (`FLEET rows 145` = `kake rows 145`), and `FLEET missing 0` means the lane's registry was found.

## Method

1. `shokunin.conf:48` carries `kake|kake-shokunin|operability + freshness (web properties and publishing)`; the validate run's own `ok` line confirms the resolved registry is `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.
2. Ran both assigned commands, capturing stdout, stderr and exit status separately under `/tmp/r51census/`.
3. Ran `census` twice: the two stdout files are byte-identical (determinism check).
4. Independent parse of the registry bytes (no script): `## Registry` at line 5, `## Paths` at 155; rows matching `^\| *S[0-9]` in lines 6–154 = **145**; `NF` histogram = `145 × 13` (the 11-cell + two-edge-pipe shape the contract requires); duplicate-id list empty; tier column = 122 A / 6 B / 17 C; status column = 115 mined / 8 queued / 22 rejected.
5. Cross-checked the `--root` lane resolution against a direct `--file` run on the same registry: identical metrics after dropping the lane-label column, and the FLEET block byte-identical.
6. Cross-checked the round's append arithmetic against two committed artifacts (base registry, pre-append receipt) and against `LOG.md`.
7. Checked the registry was not modified and that the census script itself did not drift under a concurrently-moving fleet HEAD.

## Evidence

- **Registry unmodified.** `sha256sum corpus/SOURCES.md` = `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`, equal to `git show HEAD:corpus/SOURCES.md | sha256sum` at lane HEAD `907790c78008819fc95c988431188f90b81f0d5f` (2026-10-25 03:48:10 -0300, "round-51: land the wave evidence, the ledger verdict and the mirror repair"). `git status --porcelain -- corpus/SOURCES.md` printed nothing. No registry write occurred.
- **Census is deterministic.** Two consecutive `census` runs produced byte-identical stdout; both exit 0.
- **Row count agrees with three independent sources.**
  - Direct parse of the live registry: 145 rows, all `NF=13`, no duplicate ids.
  - Base `007d66e4e8360a5f88d29a93eeedd8066dad4434:corpus/SOURCES.md`, censused via `--file` from a `/tmp` copy: sha256 `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117`, `rows 143`, `tier.A 120`, `tier.B 6`, `tier.C 17`, `status.mined 113`, `status.queued 8`, `status.rejected 22`, exit 0. Delta to the measured 145: **+2 rows, +2 tier A, +2 mined**, with B/C/queued/rejected unchanged — exactly the two rows `S262`/`S263` this round appended.
  - The committed pre-append receipt `.ufo/waves/round-51/assimilation/pre-append/census-count-stdout.txt` records the same `rows 143` block, and `census-correction.txt` names the pre-append mirror sha256 `cd9ee4cf…` — the same digest my base copy produced, so the mirror really is the base registry.
- **`LOG.md` claim matches the measurement.** `LOG.md:2069` states "Rows S262 and S263 are appended to `corpus/SOURCES.md` (143 rows to 145 rows; no existing row's cell changed)"; measured 145. `LOG.md:2060`/`:2093` state the pre-append registry "143 rows, sha256 `cd9ee4cf…`"; the base blob sha256 I computed is `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117`.
- **The append added no new duplicate-URL warning.** The 12 W04 ids in this run (S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127) are exactly the 12 W04 ids in the committed pre-append `census-stdout.txt`; neither S262 nor S263 appears. The warning set is inherited, not introduced by this round.
- **Script did not drift under the concurrent fleet HEAD.** The fleet checkout's HEAD moved during the session from `907d26386ad7f8997efa80ad0455b9e47ac03d19` to `10f629fac9306f1fa24e900597b36dbb58c13671`; `git rev-parse <rev>:scripts/sources-census.sh` returns blob `3f314620b2395eeb70d8405410132027dfe608e4` at **both** revisions, and `git diff -- scripts/sources-census.sh` is empty with worktree `git hash-object` = the same blob (file sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`). Both runs therefore used the committed script, not a modified worktree copy.
- **Working tree state is not mine.** Before writing this report, `kake-shokunin` already carried 15 `git status --porcelain` entries (5 modified `w1/*.md` seat reports and 10 untracked paths under `round-46/residual/` and `round-48/assimilation/validate/`). During the session two further entries appeared from concurrent seats, not from this one: `M corpus/lessons/round-51.md` and the untracked `?? .ufo/waves/round-51/residual/` directory (which holds this report plus a sibling's `ResidualLogFigure.md`). Neither is read by the census, and `corpus/SOURCES.md` remained unmodified while both runs executed. Nothing was staged, committed, checked out or reset; no mutating `jj` command was run.

## Limits and remaining unknowns

- **Date-relative result.** Without `--today`, E08 ("opened not a past/present ISO date") is judged against the system UTC date 2026-10-25. The clean result is therefore relative to that date; no E08 was emitted, so no row was future-dated as of it. Re-running under a different date could legitimately change only that code.
- **Counts are parser-level, not a source audit.** `rows 145` counts table rows the census parser accepts (0–3 leading ASCII spaces, `NF=13`); it says nothing about whether each row's `teaches`/`anchor` claim is true — that is the lane's own verifier's job, not this census.
- **`FLEET` block is degenerate here.** Because the invocation names exactly one lane, the fleet aggregate equals the kake row and cannot be used as evidence about any other lane's registry.
- **Tooling:** no install or update was made; no `pacman`, `uv`, `npm` or binary download was run. All commands were read-only (`git show`, `rev-parse`, `hash-object`, `status`, `log`, `diff`, `sha256sum`, `awk`, `diff`, `cmp`, plus the two assigned census invocations). Scratch files live under `/tmp/r51census/`.

**Smallest remediation:** none required. The round-end census passes: `validate` exit 0 with the inherited 12-W04 warning set and no E-code; `census` reports kake `rows 145`, consistent with base 143 + the two rows this round appended and with `LOG.md`'s own 143 → 145 statement.
