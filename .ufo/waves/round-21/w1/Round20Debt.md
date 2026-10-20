# Round20Debt — independent round-20 spot-check vs QUALITY

Scope: read-only reconciliation. Report-only seat; no target edited, no commit.
Base `5009ecaa1cce10b895617a585ddd3f7c7c923a84` (HEAD). Worktree observed
2026-10-20 while sibling seats were mid-flight, so line numbers in
`corpus/knowledge/*` are the current prefixed positions, not base positions.

Axes named: **freshness** (C1 citation/annotation debt) and **operability**
(C2 confinement checker). **Evidence integrity** (quality/discernment claims)
is the reporting axis; no new domain read, no live probe.

Sources read completely:
- `corpus/lessons/round-20-verifier-spotcheck.md` (17 lines, commit `7e17c66`,
  integrator-written; the "independent spotcheck").
- `corpus/QUALITY.md` rows 9–20 and §Post-review append-only ruling; L1's
  uncommitted round-21 section was observed but is not my artifact.
- Backing evidence cited by the spotcheck: `.ufo/round-20/resume/{post-review-restoration.txt,
  citation-disposition.json, confinement-mutation-probe.txt,
  confinement-reviewer-recipe.txt}`, `.ufo/round-20/resume/paths-after.txt`,
  `corpus/lessons/round-20.md` §Round-20 resume/§Post-review fixes,
  `SCORECARD.md` §Post-review ruling, `LOG.md` post-review entry.
- The full non-author reports the spotcheck summarizes:
  `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kake-review.md` and
  `kake-critic.md` (outside this repo; read-only, data only).

## What the spot-check actually decides

Observed (high confidence): `7e17c66` is later than the post-review commit
`9639ec7`; the spotcheck records **ADMITTED**, 3/3 sampled gate decisions
agree (1 admit, 2 rejects), C1 "improved-bounded (unannotated 26→4, drift
targets 7→3, `--section=paths` still exit 1)", C2 "improved (selftest 14→15;
planted writes 25 functions 0/25→25/25)", capability `sources-registry`
(18 rows, census ok), expansion narrow (capability + one new-ground entry),
quality and discernment improved.

The verifier file is itself a lesson file but is **not lane-authored**; it must
never receive a Gate or be edited (`corpus/lessons/round-20-verifier-spotcheck.md`
has no `## Gate` heading, correctly).

## Disagreement / routed-defect register

`Reflected?` means the authoritative fix exists in QUALITY or in an append-only
lane artifact. "Not reflected" means no current criterion/artifact states the
narrower truth, so a later claim could overreach.

| # | Disagreement or defect | Sources in conflict | Lesson-backed handling | Reflected? |
|---|---|---|---|---|
| D1 | Admission status: spotcheck says ADMITTED/discernment improved; lane report `.ufo/reports/round-20/kake.md` says blocked/unadmitted; `SCORECARD.md` intro says "Round 20 is a blocked attempt" (`SCORECARD.md:7`) and its resume table says "outside spot-check still owed" (`:185`); `round-20.md` §Gate — round-20 resume (`:182-240`, owed at `:194`) says "Outside spot-check: still owed". All lane statements predate `7e17c66`. | spotcheck lines 5–17 vs `round-20.md:182-240`, `SCORECARD.md:7,166-185`, lane report §Per-axis | Append-only adjudication note in LOG/SCORECARD (L1 owns both); r21 Gate cites the verifier lesson as the closure record. QUALITY row 12 already requires non-author review be evidenced separately; it is, at `7e17c66` + the two external reports. Do not rewrite the blocked report. | Partially — only the verifier lesson states it; no lane-owned file does. |
| D2 | C1 final numbers: spotcheck says 22/26 cleared, 4 unannotated locations / 3 drift targets remain, exit 1; `round-20.md` §Round-20 resume C1 bullet, `LOG.md` 2026-10-19 entry and `SCORECARD.md` resume table still say exit 1→0, drift 7→0, unannotated 26→0. | spotcheck line 17; `round-20.md:156-166` (exit 1→0 at `:162`); `LOG.md:600-616` (C1 at `:614`); `SCORECARD.md:166-185` | The later §Post-review fixes (`round-20.md:284+`), SCORECARD §Post-review ruling (`:214+`) and LOG post-review entry (`:641+`) supersede; history stays byte-identical. Any r21 Gate must use 22/4/3/exit 1, never the earlier green line. | Yes, later sections; earlier lines remain unqualified (append-only history). |
| D3 | Residual 4 are **gate-window** debt, not unmarked live instructions. `citation-disposition.json` sets `disposition:"uncleared"` because the note is outside ±2, while each `annotationLine` points to an EOF block that names target + dated event + "historical record, not executable". QUALITY row 14's content bar is met; the scanner's ±2 rule is not. | `citation-disposition.json` note + 4 uncleared rows; `post-review-restoration.txt:33`; QUALITY row 14 | Describe as "4 out-of-window (table-distance) locations / 3 targets", never "4 unannotated citations" flatly. QUALITY §Post-review ruling already authorizes leaving them uncleared. | Yes in ledger + restoration evidence; the spotcheck says "unannotated" without the window nuance. |
| D4 | C2 population wording: QUALITY row 17 says "a mutation case plants a write at every out-of-region function"; both enumerators match only `^(?:async\s+)?function\s+name(` — named function declarations. Arrows, function expressions and object/class methods are outside the demonstrated population (critic independently falsified the broader reading). | QUALITY:17; `scripts/freshness-sweep.mjs:1421-1445`; `.ufo/round-20/resume/confinement-mutants.mjs:32-60`; `kake-critic.md` §C2 | Append a superseding QUALITY row (L1) or require the Gate/report to say "every out-of-region named function declaration"; do not claim "every function". | No. Post-review only bounded bypasses; the criterion text still overstates the population. |
| D5 | API-list requirement: QUALITY row 17 says "the report names the API list it covers"; the script comment names all 31 (`scripts/freshness-sweep.mjs:1126-1136`, pin `31:cf1b238d8d9f2486`), but `round-20.md`/the lane report only say "15 more APIs" / "31/31 pinned". | QUALITY:17; script comment; `round-20.md` §Round-20 resume C2 | Cite `scripts/freshness-sweep.mjs:1126-1136` as the named list, or enumerate the 31 in the Gate. Strictly, the report does not satisfy the word "report". | Partially (source names it; lane report does not). |
| D6 | Spotcheck's confinement bound is lossy: it lists "aliased calls, split lines and child processes" and omits **bracket access** and **metadata/fd writes**. Authoritative list is broader. | spotcheck line 17 vs `scripts/freshness-sweep.mjs:1131-1135`; `round-20.md` §Post-review fixes; `SCORECARD.md` §Post-review ruling | Never quote the spotcheck sentence as the bound; use the source-comment list retained below. | Authoritative list reflected in source + SCORECARD; spotcheck omission is permanent in a protected file. |
| D7 | Mutation counts use two units: 26/26 in-memory named-function body sites (`e2`) vs 25/25 process-level site placements (`confinement-mutants.mjs`). Spotcheck reports only 25. | `confinement-after.txt`; `SCORECARD.md` operability resume row; QUALITY row 18 | Always name the unit with the number; do not merge 25/26/31 into one tally. | Yes in SCORECARD post-review row; spotcheck partial. |
| D8 | Append-only: reviewer found a literal breach at `02b6dd0` (17 prior lesson lines rewritten, 27 knowledge tails, 5 SCORECARD lines replaced) that the old "Append-only tails" criterion passed. | `kake-review.md` §2/M1; QUALITY row 20 + §Post-review ruling | Criterion is rejected history; superseding rule = pure new lines/EOF blocks, byte-identical prior lines. r21 Gate additions are pure EOF by contract. | Yes (QUALITY ruling + `post-review-restoration.txt` subsequence proof 17/17 files). |
| D9 | Expansion basis: reviewer found 3 of 4 new entries supersede covered ground. | `kake-review.md` M2; `round-20.md` §Post-review fixes | Basis is capability row + `crawl-scope-per-host` only. Spotcheck repeats the corrected basis. | Yes. |
| D10 | S007 quote is a schema transcription, not verbatim; S008 "GNU tar 1.35" label unsourced. | `kake-review.md` L3/L4; spotcheck line 12; `sources-gate.md:135-143`; `ghp-custom-domain.md:52-58`; `ghp-served-set.md:73-78`; `round-20.md:309-312` | Cite the errata; SOURCES cells intentionally unchanged. Do not present either as a verbatim quote or a version fact. | Yes (two entries + gate + lesson paragraph). |
| D11 | C1's wider population is omitted by the spotcheck: 55 declared-absent missSet (unchanged), 8 unresolved placeholder/glob targets, 493 relative-form cites outside `PATH_RE`; critic adds `SKILL.md:59-65` still refers to `webzites status`. | `kake-critic.md` §C1; `.ufo/round-20/resume/paths-after.txt:62-64`; QUALITY rows 11,18 | Keep the populations separate; no whole-runbook freshness or source-restoration claim from the annotation move. | Partially (evidence file + missSet in SCORECARD; spotcheck silent). |
| D12 | r21 C2 counting command denominator is wrong: `ls corpus/lessons/round-*.md \| grep -v aggregator` now yields **17** files, **16** with `^## Gate`; the only ungated file is the protected `round-20-verifier-spotcheck.md`, and `round-21.md` is a new 16th lane lesson not in the declared 15-file list. | `SCORECARD.md` §Planned item 2 vs live `corpus/lessons/` | Define the population explicitly (the 15 files in `.ufo/waves/round-21/initial.json`), exclude the verifier lesson and decide whether `round-21.md` counts; a bare heading count cannot prove gate content (L1's new QUALITY §r21 already says this). | No in the command; the principle is now stated in L1's uncommitted QUALITY section. |
| D13 | r21 metadata prefixes shift inbound line pointers: adding 4 lines (3 fields + blank) to knowledge entries moves every literal `corpus/knowledge/<f>:NN`. The four residual cites shift: drift-detection 73→77, fleet-registry 53→57, free-read-verbs 317→321; round-6 lesson cite stays 48. | live reads 2026-10-20; QUALITY §Post-review ruling (anchor census) + L1 §r21 (same-byte mapping) | Round must ship the same-byte line mapping; frozen r20 evidence is not rewritten. Residual line numbers below are given in both frames. | Rule reflected (L1 §r21); the concrete shift list is here. |

No other disagreement found. The spotcheck's 3/3 sample, 18/18 row re-open,
capability census and credential sweep agree with the reviewer/critic and with
the lane's later artifacts. Spotcheck's "S007/S008 corrected by appended
errata" matches D10. QUALITY row 9 (citation-local absence) and row 14
(annotation content) do not conflict once D3's window/content distinction is
kept.

## Residual debt retained (C1)

Measurement frame: post-review commit `9639ec7`, command
`TZ=UTC node scripts/freshness-sweep.mjs --section=paths`, observed
2026-10-19T23:04:22Z, Node v24.21.0, exit **1**
(`.ufo/round-20/resume/post-review-restoration.txt:33`). I did **not** re-run
the sweep.

Counters: 48 files · 353 occurrences · 68 unique tokens · resolve 5 ·
declaredAbsent **52** · drift **3** · unresolved **8** · missSet **55** ·
newMissing **0** · no miss outside `pins.pathsMissSet`.

Four uncleared locations across three targets (`citation-disposition.json`,
`disposition:"uncleared"`; lines below are `9639ec7` then current prefixed):

| Target (missing) | Citing location at 9639ec7 | Current location (2026-10-20) | Cell/context | EOF note at 9639ec7 / current |
|---|---|---|---|---|
| `~/Projects/plazir-15-site` | `corpus/knowledge/drift-detection.md:73` | `:77` | table header cell `source (~/Projects/plazir-15-site)` | `:91` / `:95` |
| `~/Projects/plazir-15-site` | `corpus/knowledge/fleet-registry.md:53` | `:57` | last cell of a table row (`plazir15`, live broken 404) | `:81` / `:85` |
| `~/Projects/webzites/bin/webzites.mjs` | `corpus/knowledge/free-read-verbs.md:317` | `:321` | table-row command cell (`probe ds4cc-com --json`) | `:479` / `:483` |
| `~/Projects/webzites/scripts/kimi-surface.mjs` | `corpus/lessons/round-6-aggregator-audit.md:48` | `:48` (lesson Gate is EOF; no prefix shift) | table-row `zip-exclude` command cell | `:145` / `:145` |

Per-target cite populations (from the same ledger): `plazir-15-site` 14 cites
(2 uncleared), `webzites/bin/webzites.mjs` 11 (1), `webzites/scripts/kimi-surface.mjs`
18 (1). Every one of the four has an EOF/correction-block note naming the
target, the W7 2026-10-12 `~/Projects` prune/migration event, and
"historical record, not an executable instruction". The scanner cannot see
those notes because it only looks at citing line ±2; the QUALITY content bar
(row 14) is satisfied. Do not "fix" these by splitting or editing table rows
(QUALITY §Post-review ruling) and do not re-pin `pathsMissSet`.

Named debt ownership for the three targets: operator restore-or-retire
(`~/Projects/plazir-15-site`, `~/Projects/webzites/{bin,scripts}` subtrees);
until then the annotation, not the recipe, is the artifact.

## Confinement bounds retained (C2)

Mechanism (`scripts/freshness-sweep.mjs`, `writeConfinement()` /
`selftest()`):
- Region markers must be exact standalone comment lines:
  `// SELFTEST-WRITES-BEGIN` (optional ` (…)` suffix) and
  `// SELFTEST-WRITES-END`; nested, unbalanced, unterminated and trailing-junk
  markers error; a suffix-named call decoy must not open a region; region
  opens must be inside `async function selftest()` (`e2`).
- Covered API names: **31**, pinned as `31:cf1b238d8d9f2486`
  (`scripts/freshness-sweep.mjs:1126-1136,1497-1500`):
  direct `writeFileSync, mkdirSync, appendFileSync, rmSync, unlinkSync,
  rmdirSync, copyFileSync, renameSync, cpSync, truncateSync, symlinkSync,
  linkSync, writeSync, openSync, mkdtempSync, createWriteStream`;
  callback/promise `writeFile, mkdir, appendFile, copyFile, rename, cp,
  truncate, symlink, link, write, open, rm, unlink, rmdir, mkdtemp`.
- Demonstrated populations, two different units:
  - `e2` in-memory: plants one `fs.writeFileSync('/dev/null','')` at the first
    body line of every out-of-region **named function declaration**;
    `caught 26/26`, positive and decoy controls PASS (`confinement-after.txt`).
  - Process replay `node .ufo/round-20/resume/confinement-mutants.mjs`:
    `cb807bc` killed 0/25, working tree killed 25/25 — site placements of the
    same single mutation, not 25 independent mutation classes.
- Residual bypasses, explicitly **not covered**: destructuring aliases
  (`const { writeFileSync: w } = fs`), bracket access
  (`fs['writeFileSync']`), a call split across lines, metadata/fd writes
  (`chmod, chown, utimes, ftruncate, writev, fsync`), and child-process side
  effects (`execFileSync`/`spawn`; `execFileSync` is legitimate inside the
  selftest runner). Static self-source scan only; the normal path is not
  runtime-traced. A green selftest is not a complete write-free proof.
- Criterion gap D4 above: QUALITY row 17's "every out-of-region function" is
  broader than the named-function-declaration population. Arrow/function
  expressions and methods would need new cases to support that wording.

## Handoff actions

- **L1 (owns SCORECARD/LOG/QUALITY):** append an adjudication note recording
  `7e17c66` ADMITTED and its sample (never rewrite the blocked report); fix
  the C2 counting population (D12); decide whether to append a superseding
  QUALITY row narrowing "every function" (D4) or accept the Gate-level
  wording; the new §r21 pointer-mapping rule already covers D13.
- **Lesson08 (round-20 target):** the appended Gate must use post-review C1
  (22 cleared / 4 out-of-window / 3 targets / exit 1 / missSet 55, annotation
  only), the full C2 bound list above, and the retrospective-adjudication
  sentence from D1. It must not repeat "26→0 / exit 0" or "discernment
  unchanged" as current.
- **GateContract / SourceScope:** treat the spotcheck summary as a pointer to
  the evidence, not the evidence. Quote bounds from the script comment and
  §Post-review fixes; keep `26/26` (in-memory body sites), `25/25` (process
  mutant placements), `31` (pinned API names), `declaredAbsent 52`,
  `unannotated locations 4`, `drift targets 3`, `missSet 55` and
  `unresolved 8` as separately named populations.
- **Main (one verification):** after integration run
  `node scripts/freshness-sweep.mjs --section=paths` once to confirm the
  residual state is unchanged (I did not run it), and once run the r21
  metadata/gate counts against the explicit 15-file population.

## Limitations

- I re-measured nothing: no sweep, selftest, mutation replay, census, or
  network read. All figures are quoted from the cited evidence at its stated
  commit; only file content and line positions were read directly.
- The spotcheck is an integrator-written summary; its independence rests on
  orchestrator dispatch of fresh W3ReviewKake/W3CriticKake agents, whose full
  reports live outside this repo (read, not re-executed). The lane's own
  report correctly declines to treat a self-dispatched reviewer as closure.
- The worktree is dirty from concurrent r21 seats (21 knowledge prefixes
  applied, 16/17 round lessons gated, `round-21.md` untracked, L1's QUALITY
  §r21 uncommitted). Counts and line numbers here are a snapshot, not the
  integrated state.
- No credential/auth files, agent DBs or omp CLI were touched. No tool was
  installed or upgraded for this report.
