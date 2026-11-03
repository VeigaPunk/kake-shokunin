# ExecCensusProbe — validator rejects the two bad row shapes, accepts the normalized row

Base `e5f6fd9e` (kake master), run 2026-11-03 UTC. Validator
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256
`3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` (fleet scripts repo `6e312f2e`).
Lane tracked files unmodified; only this report and `.ufo/waves/round-70/w1/ExecCensusProbe/` written.

**Method.**

```bash
S=/fast/scratch/hyaku/kake-r70/ExecCensusProbe
git -C <lane> archive e5f6fd9e4c243d092160bc74e8bea24256087173 | tar -x -C "$S/tree"
awk 'NR==72' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md > "$S/staged-row.txt"
# sha256 4d0ff087…082c, 845 bytes; NF=14 on -F'|' (escaped pipe in the recheck cell)
# insert one row after line 183 (last "^ {0,3}| S" row; ## Registry line 5, ## Paths line 186) of
# "$S/tree/corpus/SOURCES.md" -> SOURCES.<variant>.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file "$S/tree/corpus/SOURCES.<variant>.md" --today 2026-11-03
```

Variant rows and full stdout retained under `.ufo/waves/round-70/w1/ExecCensusProbe/`
(`row-*.txt`, `validate-out/*.stdout`, `commands.txt`).

**Verdict table** (full-tree mirror = base bytes + one appended row):

| file | exit | E | W | E-codes |
|---|---|---|---|---|
| `corpus/SOURCES.md` baseline | 0 | 0 | 16 | — |
| v1 verbatim staged row | **1** | 2 | 16 | E01, E11 |
| v2 pipe removed, prose recheck | **1** | 1 | 16 | E09 |
| v3 normalized (S438, `180d`, mined, 2026-11-03, used-by entry) | **0** | 0 | 16 | — |
| v4 `ran 2026-10-24, see lesson` (supplementary) | 1 | 1 | 16 | E09 |
| v5 `ran on 2026-10-24` (supplementary) | **0** | 0 | 16 | — |

Exact E lines:

```
file	E01	S352 fields=12
file	E11	S352 missing used-by grep -F -c 'The origin_summary table contains a list of all origins in the CrUX dataset'` -> 1 (ran 2026-10-24)
file	E09	S352 recheck=180d — `curl -fsSL 'https://developer.chrome.com/docs/crux/bigquery' -> grep -F -c 'The origin_summary table contains a list of all origins in the CrUX dataset'` -> 1 (ran 2026-10-24)
```

Reading: the escaped `\|` splits the row into 14 fields → E01 `fields=12` (NF−2) and the row is
skipped; the E11 line is the displaced tail (recheck prose parsed as `used-by`). Prose recheck with
clean pipes → E09. Normalized row: 13 fields, `180d` matches `^[0-9]+d$`, `opened` == today, used-by
resolves in the mirror → exit 0 with only the 16 pre-existing W04 warnings. Baseline W04 ids match the
contract's round-start list exactly: S033,S088,S092,S098,S099,S102,S110,S111,S115,S116,S117,S127,
S416,S417,S427,S433.

**Deliverable verdict: red/green confirmed — no falsification.** Both bad shapes exit nonzero with
shape findings (E01/E11 and E09); the normalized row exits 0. `validate` exits 1 only on `E[0-9]+`.

**E-code meanings observed** (header text, confirmed by trigger):
- E01 malformed row `NF!=13` → prints `fields=NF-2`, then `next`; E02 bad id; E03 duplicate id;
  E04 duplicate URL+scope without `supersedes S###`.
- E05 kind enum; E06 tier enum; E07 status enum; E08 `opened` invalid or future; E10 community at A.
- E09 invalid recheck: not ISO date, not `^[0-9]+d$`, and not `symbolic(cadence)`.
- E11 `used-by` path missing on disk, resolved against `dirname(file)/..`; E12 row-shaped `| S###`
  outside `## Registry`. W01–W04 are warnings and never change the exit status.

**Supplementary boundary** (same gate, beyond the three assigned variants):
- `symbolic(s)` is `^[A-Za-z][A-Za-z0-9 _-]*$`: letter-initial prose made only of letters, digits,
  spaces and hyphens is accepted as a symbolic cadence — `ran on 2026-10-24` → exit 0 (v5), while
  `ran 2026-10-24, see lesson` → E09 (v4, comma). Prose rejection is character-class dependent, not
  generic; the assigned prose shape is rejected.
- C2 mirror caveat: a **corpus-only** archive mirror cannot pass `--file` — 17 base rows citing
  `scripts/…`, `SCORECARD.md`, `.ufo/…` become false E11 (`validate --file mirror/corpus/SOURCES.md`
  → exit 1, 17 E11 + 16 W04). A full-tree mirror at the same revision exits 0 with 16 W04. Any
  exit-0 mirror demonstration must use a full tree (or hold those used-by targets).

**Id derivation** (0–3 leading-space extractor, `## Registry` only): 175 rows, max `S437`, `S438`
absent → next unused id **S438** (used in v3). Contrast with the contract: `S352` occurs **0** times
in the lane's `corpus/SOURCES.md` at base, so the stated registry collision is not reproducible from
these bytes; the staged file itself carries S352. Recorded as measured, not as a ruling.

**Risks / blockers:** none blocking; no tools installed or upgraded (no tool record applies). Scratch
`/fast/scratch/hyaku/kake-r70/ExecCensusProbe` removed (`rm -rf`, verified absent); lane
`git status --porcelain` shows no non-wave changes.
