# Round 21 · w1 · SourceScope — S014 review, S019 scope decision

Seat: KakeR21.SourceScope (reviewer, leaf). Read-only apart from this file. No commits, no installs, no network reads, no publishing. Tool installs or updates made: none.

## Verdict

- **S014 is sound as an own-work row.** Its label, tier scope, status and both `used-by` paths check out. One anchor is loose: the `1021-1044` pin covers `main()` (flag selection and verdict), not the §paths execution. Add the real execution pins and a revision (see F5).
- **S019 can honestly support C1, but only at the format level.** The canonical contract requires that knowledge entries open with `source:`, `verified-at:` and `recheck:`, and that lesson Gate sections exist. It says nothing about the 8-line window, the 21/21 population count, whether any `verified-at` is historical, or any platform fact. Those must rest on the lane's own gate output and on each entry's own evidence. S019 must never appear as a domain source.
- **The S019 row as it sits in the working tree needs four corrections before it is treated as canonical**: kind and tier wording, a missing revision, a `used-by` list that omits the files that already cite it, and an anchor to a script that does not exist yet (which will trip §paths).
- **Two C1-adjacent defects in existing entries** (not S014 or S019 themselves): several entries cite `corpus/CORPUS.md`, which does not exist in this lane, and several say S019 registration is "pending" although the row is now in the working tree (F6, F7).

## Scope and method

Read: `corpus/SOURCES.md` (registry, paths, search log), `corpus/knowledge/freshness-sweep.md`, `corpus/lessons/round-20.md` (S014 cites), `corpus/lessons/round-21.md`, `scripts/freshness-sweep.mjs` (lines 340–430, 890–1080, §SECTIONS and `ABSENT_RE`), the canonical `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` and `LEARNING.md`, and `.ufo/waves/round-21/wave1-spec.json` (SourceScope item). Read-only git checks: kake `HEAD` `5009eca`; kimi-shokunin `HEAD` `e737d2e`. The working tree showed `corpus/SOURCES.md` as modified (one added line, S019), and no other tracked file in the S014 set as modified. Did not run `freshness-sweep` or any gate. Did not read credential or auth files or `agent.db`.

## S014 — own-work freshness-sweep §paths

Current row (SOURCES.md:22): `own-work` · tier A · scope "Lane citation-local filesystem-path freshness gate" · status `mined` · opened 2026-10-19 · recheck 90d · used-by `corpus/lessons/round-20.md, corpus/knowledge/freshness-sweep.md`.

| Check | Result | Evidence |
|---|---|---|
| Kind `own-work` correct | Yes: the authority is a repo script in this lane | `scripts/freshness-sweep.mjs` exists, tracked |
| Tier A scoped | Yes: scope is lane citation resolution only, and the knowledge entry says so | `knowledge/freshness-sweep.md:178-179` |
| Teaches claim (±2 window, citation text blanked) | Accurate | Comment `freshness-sweep.mjs:405-412`; `annotate(...)` call at `:413`; `ABSENT_RE` at `:122` |
| Lines `404-411` | Accurate: the window comment and the annotate call | `:404-413` |
| Lines `1021-1044` as "§paths execution" | **Loose.** 1021-1044 is `main()`: `--section` selection at `:1040` and verdict at `:1043-1044`. The §paths dispatch is `runSections` at `:975-978`; the scan is `scanCitations` at `:346`; printing is `printPaths` at `:893` | `:975-978`, `:1040-1044` |
| `used-by` paths exist and cite S014 | Yes: `corpus/lessons/round-20.md:162-163, 216`; `corpus/knowledge/freshness-sweep.md:1, 178, 182` | both files present |
| Revision in anchor | Only a date ("run 2026-10-19"). The contract asks for section plus version, commit or date; a date is acceptable. Adding a commit is better: `scripts/freshness-sweep.mjs` was unmodified against kake `HEAD` `5009eca` in my check | `git status` on the S014 files |
| Status `mined` | Correct: `used-by` paths exist and cite it | — |

**S014 decision: keep the row, status `mined`.** Recommended anchor edit (SOURCES.md:22, owned by L1, not this seat): `scripts/freshness-sweep.mjs` at `5009eca`; `scanCitations` `:346-424` (window comment `:404-411`); `runSections` §paths dispatch `:975-978`; `main` section selection `:1022-1044`. Keep "run 2026-10-19" as the run date.

**S014 should not become a C1 citation.** It governs citation-path absence, not provenance trio presence or `verified-at` honesty. Do not add C1 knowledge files to its `used-by`.

## Own-work labels in use

| Where | Label | Status |
|---|---|---|
| `SOURCES.md:22` S014 | `own-work` registry row | correct |
| `SOURCES.md:27` S019 | `own-work` registry row | label mismatch, see F2 |
| `knowledge/freshness-sweep.md:1` | `source: S014 (corpus/SOURCES.md, own-work)` | correct |
| `knowledge/probe-delta-alerting.md:1` | `own-work, no SOURCES.md row` + `scripts/probe-delta.mjs` (present) | honest: says it has no S-id |
| `knowledge/fire-journal-codes.md:1` | `own-work; no SOURCES.md id` | honest |
| `knowledge/keeper-timer-inert.md:1` | `own-work: this host's read-only ...` | entry-local evidence; no S-id claimed, which is fine |
| `knowledge/ops-automation.md:1` | "not registered in corpus/SOURCES.md (no S-id)" | honest, but see F7 (S019 pending wording) |

Only S014 and S019 are own-work registry rows. The other own-work labels are entry-local evidence. They do not count toward expansion (LEARNING.md:33 counts `mined` rows only) and make no false row claim.

## S019 — findings

### F1 (high) Working tree only, revision missing from anchor

- S019 is in the working tree (`corpus/SOURCES.md:27`, one added line), not in `HEAD` `5009eca`, which ends at S018. `status` `mined`, `opened` 2026-10-20, `recheck` `on-release`, `used-by` `corpus/lessons/round-21.md`.
- The anchor reads "Canonical input Layout and Additional corpus rules, opened 2026-10-20". **It has no revision.** CORPUS.md's Census and rules ask for "exact section plus revision". The last commit touching the canonical file is kimi-shokunin `e737d2ea97f6b0198503e077676c3f2ea07974a9` (2026-10-19T21:21:25-03:00). CORPUS.md itself says "Contract v1, ratified 2026-10-19 and integrated from the fleet root revision `dcf3b6484e02452fc7aec55d724744de188779b9`". That fleet root hash is not an object in the kimi-shokunin repo (`git cat-file` failed), so cite it only as the contract's self-declared origin, not as this file's revision.
- **Fix:** add `kimi-shokunin@e737d2e (last commit to CORPUS.md, 2026-10-19)` to the anchor. Keep the self-declared `dcf3b64` as provenance text only.

### F2 (medium) Kind and tier describe the wrong object

- The row says `own-work`, but the authority it names is the fleet's canonical `CORPUS.md`, an external protocol document (kimi-shokunin). CORPUS.md's kind list has `spec`, which fits. The lane's own gate (`scripts/corpus-contract.mjs`, not yet created) would be the own-work part.
- **Fix:** kind `spec`, tier A scoped to "knowledge provenance fields and lesson Gate section shape only; not platform, freshness or domain evidence". Make the own-work gate a separate row only when `scripts/corpus-contract.mjs` exists and is run. Tier A is justified because CORPUS.md is the maintainer's own statement of the format (rule 1 of the SOURCES contract).

### F3 (high) `used-by` omits files that already cite S019

S019 is cited by name in the working tree by these files (snapshot; the set is still changing because scribes are writing):

- Knowledge, 15: `drift-detection`, `fire-journal-codes`, `fleet-registry`, `free-read-verbs`, `freshness-sweep`, `ghp-subpath-spotcheck`, `keeper-timer-inert`, `mirror-pitfalls`, `ops-automation`, `origin-repos`, `probe-delta-alerting`, `publish-channels`, `publish-queue`, `speedrun-pipeline`, `vault-properties` (all under `corpus/knowledge/`).
- Lessons (`corpus/lessons/`): `round-3`, `round-4`, `round-5`, `round-7`, `round-8`, `round-10`, `round-12`, `round-16`, `round-17`, `round-19-recensus`, `round-21`. (`round-6` line 53 matched but output was truncated; re-derive.)

The contract says `used-by` is "repo-relative paths of the knowledge entries or lessons citing the row". The row lists one file. Two choices for L1:

1. **Recommended:** `used-by` = the exact `grep -rl S019 corpus --exclude=SOURCES.md` output at integration. This is honest, and it requires no edits to 15 knowledge entries mid-flight.
2. Alternative: narrow the citations. Remove the S-id from the knowledge `source:` lines (see F4) and set `used-by` to `corpus/lessons/round-21.md` only.

With option 1, `status` `mined` holds once the listed paths exist (they do). Do not hand-trim the list.

### F4 (medium) S019 sits in knowledge `source:` fields

Entries such as `fire-journal-codes.md:1`, `fleet-registry.md:1`, `free-read-verbs.md:1`, `vault-properties.md:1` write "metadata format per S019 (metadata authority only, not a platform source)". Each carries a qualifier, so none falsely sources a domain claim. But the `source:` field is meant to name the evidence, and CORPUS.md asks `source:` to cite URL, path or command. Preferred: keep the S-id out of `source:` and cite it only in `used-by` (option 2 in F3), or keep it with the qualifier and list every such file in `used-by` (option 1). Either is honest. Mixing them is not.

### F5 (medium) §paths will see S019's own cited script

- SOURCES.md is under `corpus/**/*.md`, so the §paths scanner reads it (`freshness-sweep.mjs:5`).
- S019's anchor cites `scripts/corpus-contract.mjs`, which does not exist (`ls` confirmed). The row has no absence vocabulary (`ABSENT_RE` at `:122`: absent, gone, vanished, emptied, no longer, dangling, no such file, never published, missing). So it becomes an unannotated missing path → §paths drift → exit 1.
- **Fix options:** (a) delay S019's anchor to the script until MetadataCheck creates it, and cite only the canonical CORPUS.md now; or (b) annotate honestly on the same line ("scripts/corpus-contract.mjs — absent until MetadataCheck lands"). Option (b) uses the existing vocabulary truthfully. Do not word it to dodge the gate, and do not re-pin the miss set.
- I did not run the gate. The integrator should run `node scripts/freshness-sweep.mjs --section=paths` once after integration, as the one verification pass.

### F6 (high, C1-adjacent) `corpus/CORPUS.md` is cited but does not exist

Glob `corpus/**/CORPUS*` returned nothing. Knowledge entries cite `corpus/CORPUS.md` as the contract location: `ops-automation.md:3` ("corpus/CORPUS.md, pending L1 registration"), `probe-delta-alerting.md:1` ("corpus/CORPUS.md, L1 registration pending"), `ghp-subpath-spotcheck.md:2` ("corpus/CORPUS.md, pending L1 registration"), `fleet-registry.md:1` ("S019 (CORPUS.md)"). Two consequences:

- The citation is a false path. Under §paths it is an unannotated miss on a line without absence vocabulary, so it may drift.
- It conflicts with the registry, which points at the kimi-shokunin canonical file.

**Fix:** replace `corpus/CORPUS.md` with `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (with `S019`), or with `S019 (corpus/SOURCES.md:27)`. Entry-owning scribes make this edit; I did not edit.

### F7 (medium, C1-adjacent) "Registration pending" wording is now stale

Five entries say S019 registration is pending (`keeper-timer-inert.md:1`, `probe-delta-alerting.md:1`, `ops-automation.md:3`, `ghp-subpath-spotcheck.md:2`, `vault-properties.md:1`). The row is now in the working tree. Once L1 integrates, the wording is false. Replace "pending registration" with "S019, corpus/SOURCES.md:27 (working tree, not yet committed)" only if the commit has not landed; otherwise drop "pending". Scribes own these lines.

### F8 (low) Historical Gate sections cite S019 with labels

Checked the ones I could open: `round-10.md:64` and `round-3.md:31-49` are labeled "retrospective round-21 reconstruction, not the original admission". That is honest. The lessons that say S019 was absent at their read time (`round-4.md:50`, `round-5.md:146-148`, `round-8.md:68`, `round-16.md:169-171`, `round-17.md:85`) are also honest time-stamped notes. Contract for L1: every historical Gate that cites S019 must keep the retrospective label, and no historical Gate may say a historical admission was made "under S019". I did not audit every appended block; the C2 seats should check their own.

## What S019 supports for C1 (honest matrix)

| C1 claim | Supported by S019? | Source that does support it |
|---|---|---|
| Knowledge entries open with `source:`, `verified-at:` and `recheck:` | **Yes, format.** CORPUS.md Layout lines 18-19 ("Each `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`"); Additional rules line 162-163 ("opens with its provenance trio ... come first") | — |
| The trio sits "first" in the file | **Yes, order only** ("come first", line 163-164). **No line count.** Grep of CORPUS.md and LEARNING.md for `first 8`, `eight lines`, `8 lines` found nothing | The "first eight lines" window is the lane gate's own policy. It needs own-work evidence (MetadataCheck), not S019 |
| `verified-at` is a commit or a date | **Yes**, LEARNING.md lines 69-70 ("`verified-at:` (commit or date)") | LEARNING.md is not in S019's anchor. Add it to the anchor if this is cited |
| `recheck` is a command or citation | **Yes**, LEARNING.md lines 69-70 ("`recheck:` (the command or citation that re-verifies it)") | same as above |
| A `verified-at` names the original evidence date, marked historical-not-live | **No.** The contract does not say how to label historical state | Each entry's own evidence (r13, r16, r18 re-census lines in those entries) |
| "historical-not-live-reverified" label | **No** | The entry's own evidence and dated re-census notes |
| 21/21 population, 4/21 baseline | **No** | `measure.mjs` / MetadataCheck output |
| Lesson `## Gate` section exists | **Yes**, Layout lines 19-20 and LEARNING.md lines 71-73 | — |
| Gate records candidates, admissions, rejections, spot-check | **Yes**, Layout line 20 | — |
| Gate records URL, access date, ≤25-word quote for each new row | **Yes**, SOURCES rule 1 (CORPUS.md lines 112-115) | round-21.md Gate, lines 37-44 |

Round-21 Gate quotes check out verbatim against CORPUS.md lines 18-19 and 19-20. Both are under 25 words and located in "Layout". The round-21 Gate meets the row-admission requirement, and its line 44 scopes S019 as "own-work evidence ... not a new domain source", which is the right limit.

## Recommended S019 row (for L1 to apply; this seat did not edit SOURCES.md)

`| S019 | Shokunin Corpus Contract v1, CORPUS.md — ~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md (fleet canonical; fleet copies vendored) | spec | A | Format of knowledge provenance fields (source, verified-at, recheck) and lesson ## Gate section shape only; not platform, freshness or domain evidence | kimi-shokunin@e737d2e (last commit to CORPUS.md, 2026-10-19); §Layout lines 9-20; §Additional corpus rules lines 162-165; LEARNING.md lines 69-73 | Knowledge entries open with source, verified-at and recheck; round lessons carry a Gate with candidates, admissions, rejections and spot-check; metadata shape only, not verification of any claim | mined | 2026-10-20 | on-release | <grep-derived list, see F3> |`

Notes on that row:
- `opened` 2026-10-20 is honest only for whoever actually opened CORPUS.md on that date. I read it today; L1 should confirm that this is the opener's date.
- Keep `mined` only if the `used-by` list is complete and existing. If L1 cannot finalize that list before integration, use `queued` and state why.
- Do not put "domain" or "platform" in `teaches`. It is a format row.

## Checks for the integrator (run once after integration; I did not run them)

1. `grep -cE '^\| S0[0-9]{2}' corpus/SOURCES.md` → 19 expected with S019 (18 in HEAD).
2. The CORPUS census malformed-row check (`NF!=13`) must print 0; S019's `teaches` contains no `|`.
3. `mined` rows' `used-by` paths must exist (CORPUS census line 147): confirm `corpus/lessons/round-21.md` and every F3 path exist.
4. `node scripts/freshness-sweep.mjs --section=paths` once. Expect the F5 and F6 items to be the only new misses; if it reports other new misses, stop and route them.
5. `grep -rn 'corpus/CORPUS.md' corpus` must return nothing after F6 fixes.

## Limits

- Historical content of knowledge and lessons is not re-verified here; this report only checks citation and sourcing shape.
- I did not confirm that every S019 citer's appended Gate is correctly labeled (F8 is a sample).
- The fleet-root revision `dcf3b64` could not be resolved in kimi-shokunin; treat it as text, not evidence.
- The `used-by` snapshot changes as scribes write; re-derive it at integration.
- No live domain, platform or network evidence was consulted. No S015–S018 claim was touched.
