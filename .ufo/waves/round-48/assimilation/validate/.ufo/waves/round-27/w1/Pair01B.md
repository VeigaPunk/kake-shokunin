# Pair01B — critic: (S001, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair01B (critic, read-only leaf). Axis: freshness. Milestone: r27-full-citing-set.
Measured revision: be375d90afc6fc7aca369ab3cf5247bf460aeed2 (`git diff 83528f7 be375d9 -- corpus/knowledge` empty, so the file is the same at the frozen base; frozen snapshot line 54 is identical).
Did not read Pair01A. No tool installs. Scratch: /fast/scratch/hyaku/kake-r27/Pair01B/ (two re-fetched yml files only).

## Verdict

**HOLD at narrow scope**, for S001's specific contribution only: the archived artifact is not the checkout. The grouped recommendation itself ("Prepare the manifest over actual built/deployable HTML…") is a **local synthesis/policy step that S001 does not entail**. The current text does not label that step. Recommend an append-only precision note (wording below). It is not STALE. No discovered pair added for S001.

## Citing set for this pair (expanded)

- `count_c1.py` LITERAL/RANGE regexes over the whole file find ranges `S020-S027` (line 2), `S028-S029` (line 2) and `S001–S006` (line 54, en dash). S001 appears **only** through the line-54 range. No bare `S001` literal, no S001 in the `source:`/`verified-at:` header, no S001 in r23/r24/r26 EOF blocks.
- Line 54 (with 52–56 context), blame `c0fd6d5` round-22, 2026-10-20:
  > Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`).
- The pair is absent from `.ufo/waves/round-26/statements.json` (the r26 S001 pairs cover only ghp-served-set, publish-channels, sitemap-orphan-audit, ghp-subpath-spotcheck and speedrun-pipeline). It is one of the 16 pairs in `c2-oracle.json`. This would be a fresh r27 adjudication, not a carried r26 one.

## Source evidence (r27 retained and independently re-fetched)

| fetchIndex | URL (pinned) | status | bytes | sha256 (raw) | r27 fetchedAt |
|---|---|---|---|---|---|
| 1 | …/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml (v4.0.0) | 200 | 2529 | 4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046 | 2026-10-21T19:59:53Z |
| 2 | …/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml (main pin) | 200 | 2895 | e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741 | 2026-10-21T19:59:53Z |

- `zcat fetched/S001-N.raw.gz | sha256sum` matches the manifest for both fetches.
- Text sha256: S001-1.txt `90ef84b8…2753`, S001-2.txt `ea804af2…63c5`.
- My own independent curl at 2026-10-21T20:02:02Z (HTTP 200, same byte counts) gave the **identical sha256** for both URLs. The r26 retained hashes (15:09Z) are also identical. The URLs are commit-pinned, so the bytes are immutable.

Raw anchors:
- idx1 lines 9–12: `path:` "Path of the directory containing the static assets." default `"_site/"`.
- idx1 lines 29–36 (Linux; repeated for macOS and Windows): `tar … --directory "$INPUT_PATH" … --exclude=.git --exclude=.github --exclude=".[^/]*" .`, which is unconditional at v4.0.0.
- idx2 lines 17–20: the `include-hidden-files` input, default `"false"`. Line 18: "…Excludes .git and .github regardless."
- idx2 lines 37–39: `.git` and `.github` are always excluded. The dot-path exclusion applies unless `include-hidden-files == 'true'`.

## What S001 contributes, and what it does not

1. **Supported (S001's own contribution).** The Pages artifact is a tar of the configured `path`, not the repository checkout. Both pins always drop `.git` and `.github`. v4.0.0 always drops dot paths, and the main pin drops them by default. So a checkout-derived page list can contain paths that the uploaded artifact omits. That supports the negative half, "not over an assumed checkout served set".
2. **Inferential step not in S001.** "Served set = deployed artifact" needs S004 (artifact upload and deploy contract) and GitHub's serving behaviour. S001 never says "served", "deploy target membership" or anything about HTML or canonical tags. The positive policy, "prepare the manifest over actual built/deployable HTML when that artifact exists", is local runbook policy. `ghp-served-set.md:11-12` itself warns that the archive "does not alone establish a live site's membership".
3. **Scope edge.** The strongest supporting bytes, the `path` input with default `_site/`, lie outside the row's declared scope ("Hidden-file inclusion and invariant exclusions") and anchor (lines 17-20, 37-39). In-scope support is the exclusions only. For HTML audits that is a real but narrow effect: HTML under dot directories (e.g. `.well-known/*.html`) or under `.github/` would sit in a checkout list but not in the artifact. Recommend citing the in-scope exclusions and treating the `path` contrast as S004's.
4. **No overreach found on S001.** The sentence does not claim S001 shows build output differs from source (that would be S006/Jekyll or workflow-specific). It also makes no claim about the CNAME/custom domain (S005) and no version claim.

## Freshness analysis (stale premise vs source-date vs boilerplate)

- **Premise freshness: not stale.** Both pins re-fetch identically and both support "artifact ≠ checkout". Even a newer action run with `include-hidden-files: true` still excludes `.git` and `.github` (idx2 line 18). The line-54 claim does not depend on any pin being the current release.
- **Unverified and not needed:** whether upstream `main` has moved past `5f327015`. The row labels it "main commit" and `ghp-served-set.md:9` says "pinned current action". That freshness claim lives in ghp-served-set and the row, not in line 54. Opening unpinned `main` is not a named S001 URL, so I did not open it. Mark it UNVERIFIABLE if any ledger needs it. It does not affect this verdict.
- **Source-date:** this file attaches no date to S001. The header `verified-at` covers S020–S029 only. The S001 row reads `opened 2026-10-19`, before the round-22 citing commit `c0fd6d5` (2026-10-20). The `SOURCES.md` S001 row is byte-identical at `c0fd6d5` and at HEAD (introduced in `02b6dd0`, round 20). The citation did not predate or outlive a row change.
- **Retry boilerplate:** "S008 via `manifest-retry.json`" at line 184 refers to round 26's S020–S034 recheck of this file. It is irrelevant to S001 and is neither a citation nor stale wording for this pair.

## Counterexamples tried (all failed to falsify the narrow claim)

- *"S001 is only about hidden files, so it is irrelevant to HTML pages."* Partly true: relevance is narrow. But dot-directory and `.github` HTML are concrete checkout-versus-artifact divergences, so the attribution is weak but not wrong.
- *"Main pin makes dot exclusion optional, so checkout = artifact is possible."* No: `.git`/`.github` are excluded "regardless", and `--directory "$INPUT_PATH"` limits the tar to the configured path.
- *"Bytes drifted since r20/r26."* No: three observations (r26, r27 seat fetch, this seat) share the same sha256.

## Cross-row observations (not this pair's verdict, for the parent)

- The range `S001–S006` carries the pointer `ghp-served-set.md`, but that entry's sources are S001, S002, S003, S004, S006 and S008. **S005 is not a ghp-served-set source** (S005 is custom-domain/CNAME), and S008 (tar matching) is used there but sits outside the range. This is relevant to the S005 pair's reviewers.
- The `SOURCES.md` S001 `usedBy` cell lists only `ghp-served-set.md`, although at least six knowledge files cite S001 (including this one). This is registry incompleteness, not a STALE knowledge attribution.
- The S001 row's `teaches` says v4.0.0's dotfile exclusion is "separately evidenced by S002". idx1 lines 35/53/71 show it directly as well. This is a conservative understatement, not a defect.
- **Ledger quote pitfall:** the retained text normalizes idx2 line 18 to `Excludes.git and.github regardless.` (spaces lost before the dots). A quote of the raw wording "Excludes .git and .github regardless" therefore **fails** `count_c1.py`'s quote check (verified: substring False). Use quotes that do not cross that boundary.

## Suggested C1 ledger record (pairs.json)

Checked against `count_c1.py` logic: 16 words, whitespace-normalized substring of `text/S001-1.txt` = True (it occurs twice, Linux and macOS steps); manifest row S001 index 1 exists; raw hash verified.

```json
{"row":"S001","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD","fetchIndex":1,"quote":"tar \\ --dereference --hard-dereference \\ --directory \"$INPUT_PATH\" \\ -cvf \"$RUNNER_TEMP/artifact.tar\" \\ --exclude=.git \\ --exclude=.github \\ --exclude=\".[^/]*\"","anchor":"v4.0.0 action.yml (7b1f4a7) Archive artifact step lines 29-36 (Linux; same in macOS/Windows steps); main pin 5f327015 lines 17-20, 37-39 keep .git/.github exclusion regardless","reason":"Line 54 cites S001–S006 for 'not over an assumed checkout served set'. S001 supports only that the Pages artifact is a tar of the configured path excluding .git/.github (and dot paths by default), so a checkout list can contain unarchived paths. It does not establish served membership or the built-HTML manifest policy, which is local synthesis with S004. r27 bytes sha256 4524ed61… identical to r26 and an independent re-fetch at 2026-10-21T20:02Z."}
```

Alternative idx2 quote (13 words, passes): `Include hidden files and directories (those starting with a dot) in the artifact.` (anchor lines 17-18). Weaker for this sentence.

Cross-check with Pair01A, from its IRC message after this report was written (its report not read): it also reached HOLD, using fetchIndex 2 with the 13-word exclusion-block quote (`--exclude=.git \ --exclude=.github \ ${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }}`). This seat had independently confirmed that quote passes `count_c1.py`. Either record is counter-valid. Index 1 is the more direct support for "not the checkout": the dot-path exclusion is unconditional and `--directory "$INPUT_PATH"` sits inside the quote. Index 2 shows that `.git`/`.github` stay excluded even when hidden files are opted in. The integrator may pick either. One record per pair: `count_c1.py` flags a repeated (row,file) key as `duplicate`, so landing both records exits 1. **Revised recommendation: land fetchIndex 2.** It matches `.ufo/waves/round-26/rechecks/S001.json` (fetchIndex 2, HOLD, same lines 17-20/37-39 anchor). Treat the index-1 record above as a counter-valid alternative for the same row, not a second row. Remaining load: S004 carries "the deployed artifact is what gets served", S002/S006 carry the further ways the served set differs from the checkout, and S003 carries "Actions vs branch publishing". S005 (custom domain/CNAME) is not a `ghp-served-set.md` source and adds nothing to a built-HTML manifest policy. Its pair's seat should judge whether the range over-cites it.

Denominator hazard (raised by Pair01A, confirmed here): a search for S001–S006 IDs in this file matches only line 54, so the `S001–S006` range is S005's sole citation. Rewriting the range would drop (S005, static-canonical-preflight.md) from `count_c1.py`'s enumerated set and shrink the counted citing set, against the contract's rule that the denominator never shrinks. Leave line 54 unchanged and handle over-citation only through append-only notes.

Integration gap (raised by Pair01A, confirmed here): `git ls-files .ufo/waves/round-27/fetched` returns 0 files and `git status` shows `fetched/` as untracked. `count_c1.py` reads the manifest, raw gz and text from the measured revision's blobs, so any `kind:"source"` record fails `source_missing` until `fetched/` is committed in the candidate revision. Counter run here at `be375d9`: population 32, citingPairs 57, decided 41, missing 16 (this pair included). Upstream `main`: Pair01A made its own single GET of `…/upload-pages-artifact/main/action.yml` at 2026-10-21T20:02:46Z (streamed to sha256, bytes not retained) and got `e8ce828a…`, the same as the pinned main commit. That was Pair01A's own observation, recorded in its report §4. This seat did not repeat it, because that URL is not a named S001 URL. No bytes are retained, so the observation is not counter-checkable. Line 54 does not depend on it.

## Suggested append-only wording (precision note, not STALE; no `[r27-recheck S001 STALE]` tag needed)

> - Round-27 recheck, S001 (2026-10-21, append-only): line 54's "(S001–S006, `ghp-served-set.md`)" is grouped support for a local runbook policy. S001 (pinned action.yml, re-fetched 2026-10-21, sha256 unchanged) contributes only that the artifact is a tar of the configured path excluding `.git`, `.github` and, by default, dot paths, so it is not the checkout. That served membership follows the deployed artifact is S004's contract, and preferring built HTML is this entry's policy, not a statement of any one source. Evidence: w1/Pair01B.md.

## Uncertainties

- Whether `5f327015` is still upstream `main` is UNVERIFIABLE in this round's bounds and not relied on.
- Whether a real workflow uses `upload-pages-artifact` at all (vs branch publishing) is outside S001 (S003's ground). Line 54's "when that artifact exists" conditional covers that case.

Report: .ufo/waves/round-27/w1/Pair01B.md
