# UncoveredLessonCites — S022–S025 lesson cites vs. the round-26 retained bytes

- Seat: `KakeR26-2.UncoveredLessonCites` (reviewer, leaf — no dispatch, no subagents). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Checked 2026-10-21.
- Target (lane scope): the `corpus/lessons/` statements that cite rows **S022–S025** — `corpus/lessons/round-22.md:45-48` (the four Gate quotes) and `corpus/lessons/round-23.md:37` (the re-open line) — plus the registry cell each row's lesson cite rests on (`corpus/SOURCES.md:30-33`, `used-by`).
- Lane premise as dispatched: *"Rows S022–S025 are used only by lessons (round-22.md, round-23.md)."* — **partly false, and the falsification is the finding** (§2).
- Retained bytes used: `.ufo/waves/round-26/fetched/text/S02{2,3,4,5}-1.txt` and the matching `fetched/S02{2,3,4,5}-1.raw.gz` (sha256 `4d42dd82…b173e47`, `82a81f23…f6b7`, `fd9ae4b6…2db959`, `5854951b…9abe43`; manifest `fetched/manifest.json`, all four status 200, Last-Modified `Fri, 21 Aug 2026 11:28:27 GMT` / `Tue, 20 Oct 2026 12:58:32 GMT` ×3). Provenance: `.ufo/waves/round-26/rechecks/S02{2,3,4,5}.json` (all HOLD).
- Tooling: **no tool installed or upgraded this run** (no `pacman`, no `uv`, no `cargo`/`npm`; `python3` 3.14.8, `git`, `grep`, `sed` already present). All checks read-only; **no corpus, script, lesson, SOURCES cell, fleet file or Git index/jj was mutated by this seat**. All pacman transactions remain paused.

## Verdict: DISAGREE (low) — no lesson *quote* is false; one registry cell and one routing premise are

The four lesson quotes are all still verbatim-true against the round-26 bytes, so no lesson correction is owed and no lesson may be edited. What is false is the **registry cell** that says the lesson is those rows' only citing file (S024, S025) and the **round-26 routing rule** built on that cell. Both are mutable/append-only-fixable and neither is remediated in the current worktree.

---

## 1. The four lesson quotes — HOLD, all four verified verbatim in the committed views

Command (read-only, in the lane):

```
$ python3 - <<'PY'
s=open('fetched/text/S022-1.txt',encoding='utf-8').read(); print(s.find('Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons'), s.count(...))
PY
```

| Row | Lesson cite | Committed-view location | Words | Occurrences in own view | Anchor re-check |
|---|---|---|---|---|---|
| S022 | `round-22.md:45` "Opening paragraph: “Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons”" | `S022-1.txt` char **6540** | 17 | **1** | raw: first `<p>` after `<h1 class="page-title" id="fix-canonicalization-issues">Fix canonicalization issues</h1>`; footer `Last updated 2026-08-21 UTC` |
| S023 | `round-22.md:46` "Section 4.6.8.4: “The canonical keyword indicates that URL given the href attribute is the preferred URL for the current document.”" | `S023-1.txt` char **53082** | 19 | **1** | §4.6.8.4 body heading at 52963; nearest preceding raw `secno` spans 4.6.8.4 |
| S024 | `round-22.md:47` "Section 4.2.3: “If there are multiple base elements with href attributes, all but the first are ignored.”" | `S024-1.txt` char **10172** | 15 | **1** | §4.2.3 body heading at 8398; normative restatement also at 9795 ("There must be no more than one base element per document.") and 11210 ("A base element that is the first base element with an href content attribute in a document tree has a frozen base URL.") |
| S025 | `round-22.md:48` "Section 4.12.3: “The template contents of a template element are not children of the element itself.”" | `S025-1.txt` char **62638** | 14 | **1** | raw `secno` 4.12.3 precedes the phrase (raw byte 211622) |

- `round-22.md:39` ("Located quotes below are each at most 25 words") still holds: 17/19/15/14 words.
- `round-22-verifier-spotcheck.md:126` (S022, "last updated 2026-08-21") still holds: the retained view's footer is `Last updated 2026-08-21 UTC` and `manifest.json` gives `Last-Modified: Fri, 21 Aug 2026 11:28:27 GMT`.
- `round-23.md:37` ("Re-opened without change: S021, S023, S024, S025, S026") is a round-23 historical record scoped to that round's Gate; it is not falsifiable by the round-26 bytes and is **not** edited.

**So: zero lesson statements are now false.** Every quote, location and word count above was re-derived from the committed round-26 views, not from the receipts.

## 2. FALSIFICATION — the lane premise fails for S024 and S025, and the registry cell + routing rule are wrong

The dispatched premise "used only by lessons" is true for **S022 and S023** and **false for S024 and S025**.

**Evidence A — the knowledge entry cites S024 and S025.** `corpus/knowledge/static-canonical-preflight.md` (candidate `e28312b1`) cites:

- `:101` — "S030 (…), S031 (…), **S024** (the first base in tree order wins), S026."
- `:117` — "a body base is still the document's first base in tree order (**S024**) and would change a relative canonical."
- `:144` — "[r23-correction] 'template descendants cannot supply a document-head canonical' rests on **S025** (template contents are not children of the template)".

**Evidence B — the registry cell does not say so.** `corpus/SOURCES.md:30-33` at the candidate:

```
$ git show e28312b1:corpus/SOURCES.md | awk -F'|' '/^\| S02[2-5] /{...print $2" -> "$12}'
 S022  -> corpus/lessons/round-22.md
 S023  -> corpus/lessons/round-22.md
 S024  -> corpus/lessons/round-22.md      <-- omits corpus/knowledge/static-canonical-preflight.md
 S025  -> corpus/lessons/round-22.md      <-- omits corpus/knowledge/static-canonical-preflight.md
```

Every sibling row cited by the same file lists both paths — S020, S021, S026–S034 all carry `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-2{2,3,4}.md`. S024 and S025 are the only two exceptions, and they are the only two of that set whose knowledge-entry claim is a real attribution. `CORPUS.md:107` defines `used-by` as "repo-relative paths of the knowledge entries or lessons citing the row"; the cell is therefore incomplete as written.

**Evidence C — the drift's origin is round 23, not round 26.** `83098b5` ("round-23: integrate wave 1") added the S024/S025 knowledge citations (`+52` lines in the knowledge entry, incl. the three lines above) while touching `corpus/SOURCES.md` only to add the **new** S030/S031 rows and a note — it did not touch the S024/S025 `used-by` cells. `round-23.md:65` ("No old row's status/recheck/used-by changed") is literally true and yet leaves the registry inconsistent with the corpus.

**Evidence D — the round-26 rules turned that cell into a live routing rule.** `.ufo/waves/round-26/w1/SourceRulesConnect.md:336-341`:

> 2. **Only historical lessons cite the row** (e.g., S022-S025's `used-by` is `corpus/lessons/round-22.md`) → do **not** edit the historical lesson. Append the block to `corpus/lessons/round-26.md`, citing `round-22.md:LL`.

Applied to S024/S025 that rule sends a STALE correction to a **lesson** instead of to the knowledge entry that actually states the claim — the wrong citing file, and one that would leave the live claim uncorrected. (The L1's in-flight adjudication did the right thing and put the S024 STALE blocks in `corpus/knowledge/static-canonical-preflight.md`; the false premise and the wrong rule remain standing in the rules document.)

**Evidence E — no automated gate catches it.** `scripts/sources-census.sh:567` implements E11 as a *path-existence* test only (`[ ! -e "$dir/$path" ]`); there is no completeness check, so the incomplete cells pass silently:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04:S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
EXIT=0
```

`node scripts/corpus-contract.mjs` also exits 0 (0 findings, 23 knowledge entries, 21 lane lessons).

**Remediation state.** `git diff e28312b1 -- corpus/SOURCES.md` is **empty** in the current worktree: the in-flight L1 added the S024/S025 statement units (3 units) and the `[r26-recheck S024 STALE]` blocks to the knowledge entry, but the `used-by` cells at `corpus/SOURCES.md:32-33` are still uncorrected, and the round-26 lesson's coverage row (`corpus/lessons/round-26.md:118`) records only that "ledger followed `usedBy` cells only" — it does not record the registry-cell defect or the routing-premise correction. **This is the distinct remaining gap.** (The locator drift in the S024/S025 receipts is *not* a gap: it is already recorded in `.ufo/waves/round-26/receipt-locator-errata.json` — S024 "quote 10172-10260; heading 8398", S025 "quote at char 62638" — with `w1/RowS023.md`/`RowS024.md` seat-report sizes in `alsoStale`. My independent recomputation reproduces those values exactly, so I confirm rather than duplicate them.)

## 3. Minimal correction (no lesson edit; two mutable cells + one note)

1. `corpus/SOURCES.md:32` (S024) `used-by`: `corpus/lessons/round-22.md` → `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md`.
2. `corpus/SOURCES.md:33` (S025) `used-by`: `corpus/lessons/round-22.md` → `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md`.
   Both paths exist at the measured revision, so E11 stays clean (`scripts/sources-census.sh validate` → `ok`, exit 0), the cell order matches S020/S021/S026–S034, and `CORPUS.md:116` (append-only; `used-by` mutable with a logged old→new) plus `.ufo/waves/round-26/w1/SourceRulesConnect.md:65` ("a knowledge entry or lesson substantively cites the row and the path is missing from the cell") authorise exactly this edit. Log old→new in the round-26 lesson.
3. Append to `corpus/lessons/round-26.md` (append-only; **do not** edit `round-22.md` / `round-23.md`): that S024's and S025's `used-by` omitted `corpus/knowledge/static-canonical-preflight.md` from round-23 (`83098b5`) onward, that the row therefore looked lesson-only, that the round-26 routing rule at `w1/SourceRulesConnect.md:338` inherited that premise, and that the S024/S025 STALE/HOLD blocks were consequently placed in the knowledge entry (the citing file) rather than in a lesson. Do **not** touch `round-22.md:55` — it is a round-22-scoped Gate record, correct at its base revision, and the round-26 rule (historical and base-scoped pointers are not stale) forbids rewriting it.
4. No counter, receipt, verdict or count changes: `measure.py` never parses `anchorObserved` offsets and the S024/S025 verdicts are HOLD and independently re-verified above.

## 4. Residual risk and verification gaps

- **Residual risk (low, documentary).** With the cells still lesson-only, any later round that scopes its statement review by `used-by` will again skip S024/S025 knowledge claims — the exact failure the in-flight L1 had to repair by hand. A reader of `corpus/SOURCES.md:32-33` alone is told those rows are cited by a lesson only, which is false.
- **Residual risk (low, no behaviour).** No published artefact, tool behaviour, receipt verdict, counter exit code or knowledge-entry claim is wrong because of this; the S024/S025 statements that the L1 reclassified/appended are adjudicated in the in-flight corpus block, and the round-22/round-23 lesson text remains literally true at its own round.
- **Verification gaps.** (i) I did not GET any URL; every quote, offset, section number and footer date above is read from the committed round-26 retained bytes, whose `manifest.json` digests match the pinned population digests. (ii) The S024 quote sits in the section's note paragraph (per `rechecks/S024.json`'s own reason text) rather than in normative prose; the lesson's location claim "Section 4.2.3" and the row's `teaches` are nonetheless supported normatively by the same section's frozen-base-URL prose at text offsets 9795 and 11210, which I read directly. (iii) Whether the S024/S025 STALE classification is right is the L1's adjudication (accepted in the worktree); I do not contest it and my finding is the registry cell plus the routing premise, independent of that verdict. (iv) I did not re-open the round-22/23 verifier files' own quotes beyond the S022 line; every other row in this wave is out of this seat's scope.

## 5. Bottom line

The four S022–S025 lesson quotes are **all still verbatim-true** against the round-26 retained bytes (offsets 6540 / 53082 / 10172 / 62638; 17/19/15/14 words; one occurrence each; section numbers and the S022 footer date unchanged), so **no lesson statement is false and no lesson may be edited**. The falsification is one level up: the dispatched premise that these rows are used only by lessons is **false for S024 and S025**, whose `used-by` cells at `corpus/SOURCES.md:32-33` omit the knowledge entry that cites them at `static-canonical-preflight.md:101,117,144` — a drift that `83098b5` created and that round 26's own routing rule (`w1/SourceRulesConnect.md:338`) turned into a live misroute (a STALE correction would have gone to a lesson instead of the file stating the claim). Two `used-by` cells plus one append-only note in `corpus/lessons/round-26.md` close it; no counter, receipt or verdict moves.

```json
{"target":"corpus/SOURCES.md:32-33 (S024/S025 used-by) + .ufo/waves/round-26/w1/SourceRulesConnect.md:338 (lessons-only routing premise); lesson cites corpus/lessons/round-22.md:45-48 and corpus/lessons/round-23.md:37 re-verified HOLD against the round-26 bytes","verdict":"DISAGREE","severity":"low"}
```
