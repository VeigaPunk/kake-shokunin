# Pair01A — reviewer seat, axis freshness

Pair: **(S001, corpus/knowledge/static-canonical-preflight.md)** — Kake r27 w1, C1 ledger row.
Lane: read-only findings. No ledger/source/Git edits made. Milestone: r27-full-citing-set.

## 1. Verdict

**HOLD** (source-kind row; cited bytes unchanged, anchor exact, claim supported at its stated scope).
No STALE correction is required for this pair. No new citing pair discovered (§7).

## 2. Axes named

- **freshness** (seat axis): are the cited bytes still the bytes the row was mined from, and does the citing line still hold against them?
- secondary **operability** note only: does the evidence actually flow through the frozen counter (`count_c1.py`) at the measured revision? (§8.4)

## 3. Exact citation location (range expanded)

`corpus/knowledge/static-canonical-preflight.md`, blob sha256 `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc`
(identical at frozen base `83528f7c` and declarations `be375d9`; 203 lines).

- **Only citation of S001 in this file: line 54**, reached by expanding the literal range `S001–S006` (en dash) at line 54.
  No other S001/S001-containing range exists in the file (full scan of all 203 lines: ranges present are `S020-S027` and `S028-S029` at line 2, `S001–S006` at line 54; all other S-ids are bare literals at lines 184/186-203).
- Surrounding claim, lines 50-56 (verbatim):

```
50 | location: it is opened once, as given, and every page is resolved from that
51 | same opened directory, so a symlink earlier in your own path is followed
52 | while a symlink inside the manifest-relative page path is not. Prepare the
53 | manifest over actual built/deployable HTML when that artifact exists, not over
54 | an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
55 | artifact was available or claimed as tested in round22; its fixtures are local,
56 | authorized publisher examples.
```

- The claim is a **standing local publishing recommendation**, not a dated observation, and its parenthetical points at the *other* entry (`corpus/knowledge/ghp-served-set.md`) and that entry's rows S001-S006.

## 4. Source reopen / retained-byte evidence

Named S001 URLs (`corpus/SOURCES.md` row S001), re-opened once each by this seat, no retention (streamed to sha256):

| fetchIndex | URL | HTTP | live sha256 | r27 retained sha256 | r26 pinned sha256 |
|---|---|---|---|---|---|
| 1 | `https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml` (v4.0.0) | 200 | `4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046` | identical (`.ufo/waves/round-27/fetched/S001-1.raw.gz`, decompressed) | identical |
| 2 | `https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml` (main commit) | 200 | `e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741` | identical | identical |

- Live probe at **2026-10-21T20:02:46Z**. r27 retained fetch time **2026-10-21T19:59:53Z** (`.ufo/waves/round-27/fetched/manifest.json`).
- Extra non-named freshness probe (same document, moving ref, not retained): `.../actions/upload-pages-artifact/main/action.yml` → sha256 `e8ce828a…` ⇒ **`main` still resolves to commit `5f327015`'s content**; the row's "main commit" label is current, not a stale pointer.
- Anchor fidelity against r27 retained bytes (fetchIndex 2, main commit), row anchor "inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39" verified exactly:
  - line 17 `include-hidden-files:` / line 18 description / line 19 `required: false` / line 20 `default: "false"`;
  - line 37 `--exclude=.git \` / line 38 `--exclude=.github \` / line 39 `${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }} \`.
- v4.0.0 copy (fetchIndex 1) has no `include-hidden-files` input and hard-codes `--exclude=".[^/]*"` at lines 35, 53, 71 (Linux/macOS/Windows), with `--exclude=.git`/`--exclude=.github` at 33-34, 51-52, 69-70.
- r26 predecessor evidence: `.ufo/waves/round-26/rechecks/S001.json` = HOLD, fetchIndex 2, same anchor and same quote; r26 retained manifest shas equal r27's. **No byte drift between r26 and r27.**

## 5. Specific contribution of S001 (not "row HOLD")

S001's own scope (`corpus/SOURCES.md`): "Hidden-file inclusion and invariant exclusions in this action";
teaches: "The action exposes hidden-file inclusion while excluding .git and .github regardless".

What S001 contributes to line 54 — and only this:

1. **The published page set is a filtered subset of a build directory, not a checkout listing.** The action archives `--directory "$INPUT_PATH"` (input `path`, default `_site/`), i.e. a build output directory; it then excludes `.git` and `.github` unconditionally in all three OS steps, and (v4.0.0) every dot path unconditionally, or (main) every dot path unless `include-hidden-files: true`.
2. **Therefore the filter is version- and input-dependent**: an "assumed checkout served set" over-approximates the deployed set (dot paths, `.github/…` pages) and the approximation changes with action version/workflow input. This is the factual premise of line 54's negative half ("not over an assumed checkout served set").
3. **What S001 does *not* contribute**: it says nothing about a live site's membership (the sibling entry says so in its own words: "it does not alone establish a live site's membership", `corpus/knowledge/ghp-served-set.md` lines 7-12), and nothing about canonical/HTML policy, which is what the rest of this entry's own rows S020-S034 cover.

Labeled inferential step (local synthesis, **not** entailed by S001 alone): line 54 converts "the deployed set is a filtered build output" into the operating rule "build the manifest over actual built/deployable HTML". S001 supports the premise; the recommendation is this entry's own policy, and the six-row parenthesis is a pointer to `ghp-served-set.md`, not a claim that six sources each entail the rule. The other rows carry the rest: S002 (release-note change of the dotfile default), S003 (publishing source = branch or Actions workflow), S004 (artifact shape and deploy requirements; source folder = repo root or `/docs`), S006 (Jekyll default excludes for the legacy path). **No row individually entails the recommendation; each evidences one mechanism of "published set ≠ checkout set".**

**S005 carries no load for line 54 (range over-cites it).** S005's own scope/teaches (`corpus/SOURCES.md`, population row S005) are custom-domain configuration — "An Actions-published site ignores a repository CNAME file; the domain is configured through Pages settings or the API". Its retained r27 text (`fetched/text/S005-1.txt`, sha256 `6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4`) contains **0** occurrences of "deploy", "artifact", "_site", "dotfile" or "hidden" (23 of "CNAME"), i.e. it speaks to neither build/deploy membership nor artifact contents. So within the `S001–S006` parenthetical, S005 is **over-cited**: it evidences no mechanism of "published set ≠ checkout set". This is flagged for the S005-owning seats (their pair for *this* file comes from the same line 54); S001's own verdict is unaffected — S001 is genuinely load-bearing here.

**Do not edit the citation range to fix the over-citation.** `count_c1.py` enumerates pairs by expanding the literal ranges it finds; rewriting line 54's `S001–S006` (e.g. to `S001–S004, S006`) would remove `(S005, corpus/knowledge/static-canonical-preflight.md)` from the enumerated citing set and silently shrink the C1 denominator (57 → 56), violating the contract's monotone-denominator rule ("denominator grows monotonically, never quietly shrinks"). The monotone-safe remedy is an **append-only** precision note that names each row's contribution (§10), leaving the original citation text and the denominator untouched.

## 6. Stale premise vs source-date vs irrelevant retry boilerplate

- **Stale premise?** No. The line's premise (checkout membership ≠ deployed membership) is exactly what the r27 bytes still show; no clause of line 54 is contradicted by the retained bytes. Nothing at line 54 asserts a version-specific fact that moved.
- **Source-date staleness?** Not applicable to this line: line 54 carries no date and is not a historical observation. The entry's `verified-at:` header (line 2) covers only its own rows S020-S027/S028-S029, not the cross-entry parenthetical; the cited entry's own header (`ghp-served-set.md` line 2) and its round-26 recheck paragraph (line 83) record that S001 was re-fetched 2026-10-21 and judged HOLD at its anchor — freshness is traceable through the named entry, so the missing local date on line 54 is a traceability nit, not a stale claim.
- **Irrelevant retry boilerplate?** Line 54 contains none. (The boilerplate in this file is elsewhere: line 184's "S008 via `manifest-retry.json`" is a round-26 retry note pasted into a sentence that lists only S020-S034 rows; that is the *S008* pair for this file, out of my scope — flagged below for the owning seat, no denominator change.)
- **Inherited STALE check**: the r26 STALE on S001 (`[r26-recheck S001 STALE]`, `ghp-served-set.md` line 93) concerns a *v3.0.1* attribution in that file's lines 21-22. Line 54 of the preflight entry makes no v3.0.1 claim, so nothing is inherited. No stale-prefix contagion.

## 7. Denominator / discovered pairs

- S001 is cited in exactly one form in the counted scope: `S001–S006` at `static-canonical-preflight.md` line 54. No additional citing form (e.g. `S-001`, `S 001`, bare `001`) exists in `corpus/knowledge/**` (scanned). **No new citing pair discovered; the C1 denominator is unchanged at 57 pairs / 32 rows.**
- (For completeness only: `corpus/lessons/*.md`, `corpus/README.md`, `corpus/SOURCES.md` also cite S001 but lie outside the counted `corpus/knowledge` scope of the frozen counter — not a discovered pair under this contract.)

## 8. Verification gaps / uncertainties

1. **The cited text rendition, not the raw bytes, is what the counter checks.** `fetched/text/S001-2.txt` is a compacted single-line rendition that drops the space after a sentence period: it reads `Excludes.git and.github regardless.` where the raw bytes read `Excludes .git and .github regardless.`. A ledger quote must therefore use the rendition form to pass `count_c1.py`'s substring test; raw-accurate spacing would fail the counter. Both forms are quoted below so the L1 copies the machine-checkable one.
2. **`fetched/` is currently untracked in Git** (`git status` shows `?? .ufo/waves/round-27/fetched/`; `git ls-tree be375d9 -- .ufo/waves/round-27/` contains no `fetched/` entries). `count_c1.py` reads the manifest and the raw/text blobs **from the measured revision's blobs** (`git show <rev>:...`), so every `kind:"source"` row will be flagged `source_missing` until `fetched/manifest.json`, `fetched/*.raw.gz` and `fetched/text/*.txt` are committed with the candidate revision. Integration-ordering note for L1, not a defect of this pair.
3. The row's second URL is a **commit-pinned** raw URL, so its bytes are immutable by construction; "live sha == retained sha" for it is confirmatory, not a strong freshness test. The stronger test was the `main`-tip probe (§4), which showed `main` still at `5f327015`'s content on 2026-10-21.
4. I did not re-open S002-S006 individually (other seats' rows); §5's per-row allocation of the synthesis rests on `corpus/SOURCES.md` row scopes and the sibling entry's source-check block, and on S001's own bytes. Treat the "S002-S006 carry the rest" allocation as **[INFERENCE]** pending those seats' independent judgments.

## 9. Suggested C1 ledger record (contract `C1.ledger`, `count_c1.py` schema)

```json
{
  "row": "S001",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "reason": "Only citation is the range S001-S006 at line 54: 'Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set'. S001 contributes the artifact-membership mechanism only: upload-pages-artifact archives --directory \"$INPUT_PATH\" (input path, default _site/), excludes .git and .github unconditionally in all three OS steps, and excludes dot paths unconditionally at v4.0.0 or unless include-hidden-files: true at main 5f327015, so the deployed set is a filtered build output rather than the checkout. The recommendation itself is this entry's local publishing synthesis (inferential step labeled, not entailed by S001 alone); S001 does not establish live-site membership. 2026-10-21T20:02Z live sha256 equals r27 retained and r26 pinned shas; row anchor lines 17-20 and 37-39 verified exactly against the retained main-commit bytes; main tip still resolves to 5f327015 content. No stale premise, no source-date claim, no correction required.",
  "fetchIndex": 2,
  "quote": "--exclude=.git \\ --exclude=.github \\ ${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }}",
  "anchor": "Main commit 5f327015 (fetchIndex 2): Archive artifact step, lines 37-39 (Linux); same pair repeats at 55-56 macOS and 73-74 Windows. input include-hidden-files at lines 17-20. Raw bytes (sha256 e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741) show the same three lines with newlines; fetched/text/S001-2.txt is a compacted rendition (quote as given). v4.0.0 copy (fetchIndex 1, sha256 4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046) hard-codes --exclude=\".[^/]*\" at lines 35, 53, 71."
}
```

- Quote word count: **13** (≤25). Verified present in `fetched/text/S001-2.txt` after the counter's whitespace normalization; verified sha matches `fetched/manifest.json` S001/index 2.
- **One record per pair.** `count_c1.py` flags a repeated `(row,file)` key in `pairs.json` as `duplicate` (a finding → exit 1), so this pair gets exactly one ledger row. A peer seat (Pair01B) reached the same verdict HOLD at **fetchIndex 1** with a 16-word v4.0.0 tar-block quote (unconditional `--exclude=".[^/]*"` plus `--directory "$INPUT_PATH"`); both quotes are counter-valid, but they are alternative records for the same key, not two records. My index-2 choice is the one consistent with the r26 receipt (`.ufo/waves/round-26/rechecks/S001.json`, fetchIndex 2, same anchor); the integrator may substitute the index-1 quote in the same single row (fetchIndex 1 → sha `4524ed61…`) without changing the verdict.
- Raw-byte-accurate alternative quote for humans (NOT counter-usable, space after period): `Include hidden files and directories (those starting with a dot) in the artifact. Excludes .git and .github regardless.` (r26 receipt form, 11 words, also present in the rendition with periods tightened).

## 10. Correction wording

- **None required.** A STALE verdict would demand `[r27-recheck S001 STALE]` in the citing file; this pair is HOLD, so no append.
- *Optional, not contract-required* — if L1 wants the inferential step of the grouped recommendation labelled in the entry (per `C1.sourceVerdict`: "label the inferential step and each source's contribution"), append-only, e.g.:

```
- [r27-precision S001] Line 54's parenthetical is a local synthesis, not a per-row entailment:
  S001 evidences only that upload-pages-artifact archives a build directory (--directory
  "$INPUT_PATH", default _site/) with .git/.github always excluded and dot paths excluded
  by default at v4.0.0 or unless include-hidden-files: true at main 5f327015. Live-site
  membership is not established by S001; the recommendation to build the manifest over
  actual built/deployable HTML is this entry's local publishing policy. Within the same
  parenthetical S001-S004 and S006 each evidence one mechanism of "published set != checkout
  set"; S005 (custom-domain configuration) evidences none of them. The range text is left
  unchanged so the counted citing set does not shrink. Evidence: w1/Pair01A.md.
```

Offered for L1's decision only; the L1 integration seat owns any append to the corpus entry.

## 11. Cross-seat observations (no denominator change)

- `static-canonical-preflight.md` line 184 contains "S008 via `manifest-retry.json`" inside a sentence enumerating only rows S020-S034 — the same paste-artifact the r26 falsify wave flagged in the sibling entry (`ghp-served-set.md` line 95). This is the *S008* pair for this file (already counted, missing, owned elsewhere); it is boilerplate, not a substantive S008 claim, and should not make the S008 pair look STALE. Flagging for the S008 owner; no new pair.
- Line 2's ranges `S020-S027` / `S028-S029` are the only source of the S022/S023 pairs in this file — they are genuine range expansions of the entry's own header, distinct from the S001-S006 grouped parenthetical.

Report: .ufo/waves/round-27/w1/Pair01A.md
