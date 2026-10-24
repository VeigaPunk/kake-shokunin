# SourceOpenS001 — S001 live reopen and the preflight inference

Seat KakeR27.SourceOpenS001 (read-only leaf, no dispatch). Axis: freshness. Milestone:
r27-full-citing-set. Scope: reopen both URLs in `corpus/SOURCES.md` row S001, compare with the
round-27 retained capture, test the grouped inference at `corpus/knowledge/static-canonical-preflight.md:53-54`.
The row lists exactly two public URLs; no third S001 URL exists.

## Row apparatus (SOURCES.md:9)

- URL 1 `https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml` (v4.0.0)
- URL 2 `https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml` (main)
- kind `code`, tier A; scope: hidden-file inclusion and invariant exclusions.
- anchor: "inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39; v4.0.0 tag and main 5f327015…".
- teaches: "The action exposes hidden-file inclusion while excluding .git and .github regardless;
  v4.0.0's default dotfile exclusion is separately evidenced by S002".
- status `mined`, opened `2026-10-19`, recheck `on-release`, used-by `corpus/knowledge/ghp-served-set.md`.

## Live reopen (one public GET per URL, no credentials/cookies)

| idx | HTTP | bytes | sha256 (decoded body) | GET window (UTC) |
|---|---|---|---|---|
| 1 v4.0.0 @7b1f4a7 | 200 | 2529 | `4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046` | 2026-10-21T20:01:41.735Z → .752Z |
| 2 main @5f327015 | 200 | 2895 | `e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741` | 2026-10-21T20:01:41.753Z → .768Z |

finalUrl identical to the row URLs (no redirect). HEAD at response `Date: Wed, 21 Oct 2026
20:03:49 GMT`: `content-length` 2529 / 2895, `cache-control: max-age=300`, `via: 1.1 varnish`,
`x-served-by: cache-gig2250026-GIG` / `cache-gig2250034-GIG`, etags
`2f3888204c39638a08710062d94b8ceb784d4c7f27ea7e2bc0d97e0bb3e695af` / `ee49149e960484950efc5aec4462a29e28ede93b916e18ceb7e7be8607113930`.

## Retained comparison

- r27 `fetched/manifest.json`: idx 1 `fetchedAt 2026-10-21T19:59:53.614354+00:00`, 2529 B,
  sha `4524ed61…cd046`; idx 2 `fetchedAt 2026-10-21T19:59:53.803523+00:00`, 2895 B, sha `e8ce828a…ca6741`.
- Retained `.raw.gz` decompress to exactly those hashes (verified); `cmp` live vs decompressed
  retained is **byte-identical for both indexes**.
- r26 capture (15:09:32Z) carries the same two sha256 values. Three captures today
  (15:09Z, 19:59Z, 20:01Z) agree byte for byte; the URLs are commit-addressed, so this is
  revision identity, not merely cache luck.
- Text views `fetched/text/S001-1.txt` sha `90ef84b80160d4539df2088c570e08d5fef8a531aa0dc4045beb72f3a2312753`,
  `S001-2.txt` sha `ea804af2dcab49e31c931ce6e76b5a911ec3642eaa599d7978e86a80a91f63c5` (same as r26);
  sizes 2000 B / 2350 B vs 2529 B / 2895 B raw.
- Text-view fidelity defect (new): whitespace normalization deletes spaces. Tokens raw→text
  254→246 (S001-1), 302→292 (S001-2); diffs are `echo ::group::Archive`→`echo::group::Archive`
  (3× each), `\`+`.`→`\.` (2× each), and S001-2 `Excludes .git and .github`→`Excludes.git and.github`.
  Because `count_c1.py` requires `quote ⊆ text view`, a raw-verbatim "Excludes .git and .github"
  quote **fails the C1 quote rule**, and the text view prints a spelling the source lacks.
  Quotes below avoid the defect and pass in both views.

## Anchor verification against live raw bytes

| element | v4.0.0 @7b1f4a7 (85 lines) | 5f327015 (89 lines) |
|---|---|---|
| `include-hidden-files` | absent (0) | key 17, description 18, required 19, default `"false"` 20 |
| `path` input, default `"_site/"` | 9-12 (default 12) | 9-12 (default 12) |
| `name: Archive artifact` | 24, 42, 60 | 28, 46, 64 |
| `--directory "$INPUT_PATH"` | 31, 49, 67 | 35, 53, 71 |
| `--exclude=.git` unconditional | 33, 51, 69 | 37, 55, 73 |
| `--exclude=.github` unconditional | 34, 52, 70 | 38, 56, 74 |
| dot-path exclusion | `--exclude=".[^/]*"` unconditional 35, 53, 71 | `${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }}` 39, 57, 75 |

**Teaching verdict: HOLD at row scope.** Both limbs persist on live bytes: main exposes
`include-hidden-files` defaulting to `"false"`; `.git`/`.github` are excluded unconditionally in
all three OS archive blocks at both pins; v4.0.0 hard-codes the dot exclusion three times and has
no inclusion input. No status/recheck/used-by/teaches cell needs change.

Anchor caveat (precision, not STALE): the coordinates 17-20 and 37-39 are exact for the **main**
copy only. At v4.0.0 lines 17-20 are the `outputs:` block and 37-39 are `echo ::endgroup::` /
`env:` / `INPUT_PATH:`; v4's archive block is 24-39 with excludes 33-35. The coordinate-bearing
phrase exists only in main, so the main-scoped reading is the only self-consistent one (r26 read
it so). Optional annotation; no `[r27-recheck S001 STALE]` warranted — the anchored claim is true
at both pins. Minor understatement, not error: S001's own v4 bytes already carry
`--exclude=".[^/]*"`; the retained `fetched/text/S002-1.txt` does read "Potentially breaking
change: hidden files (specifically dotfiles) will not be included in the artifact", but S002 is
another seat's row and was not reopened here.

Freshness identity (GitHub API, public, unauthenticated): tag `v4.0.0`→`7b1f4a7` (2025-08-14T14:24:33Z),
`v4`→same; `v5.0.0`→`fc324d3` (2026-04-08T19:09:19Z), `v5`→same; `refs/heads/main`→`5f327015`
(2026-10-15T14:12:04Z). No tag newer than v5.0.0. Both row URLs are SHA-pinned, so the `on-release`
trigger has not fired and no drift is possible at the pin.

## Inference test — `static-canonical-preflight.md:53-54`

Target (grouped S001–S006 plus `ghp-served-set.md`): "Prepare the manifest over actual
built/deployable HTML when that artifact exists, not over an assumed checkout served set."

Located quote — 13 words, main lines 9-12, identical at v4.0.0 lines 9-12; verified normalized
substring of both raw bodies **and** both retained text views (so `count_c1.py` accepts it):

```
  path:
    description: "Path of the directory containing the static assets."
    required: true
    default: "_site/"
```

Ledger form: `description: "Path of the directory containing the static assets." required: true
default: "_site/"`.

Secondary anchor (not the ledger quote): main 33-40 / v4 29-36 — `tar --dereference
--hard-dereference --directory "$INPUT_PATH" -cvf "$RUNNER_TEMP/artifact.tar" --exclude=.git
--exclude=.github .` (v4 adds `--exclude=".[^/]*"`; main makes it conditional). Archive root is
the caller's `path`, never the repository root.

**Classification: indirect contribution.**

- Direct: the deployable artifact is a tar of a named "static assets" directory whose default
  `_site/` is a site-generator output name, and `.git`/`.github` never ship (dot paths excluded by
  default at main, always at v4). The artifact is therefore neither the repository tree nor all of
  the configured directory, so any equation of checkout and served set lacks support. This is the
  premise half — "the checkout is not the served set".
- Not established: any canonical/manifest instruction; that the directory holds *built* HTML; or
  that uploaded bytes equal served bytes. `path: .` remains legal, so S001 supports "not an
  *assumed* checkout served set", not "never the checkout". S001 never mentions HTML.
- "built" is partly [INFERENCE]: the text says "static assets"; the build-output reading rests on
  `_site/` convention (S006 is the Jekyll source), not on an S001 sentence.
- Dotfile nuance ([INFERENCE], tar matching per S008): a dot-prefixed publish path such as
  `.well-known` is dropped by default at main and always at v4 — "deployable" means "as archived".
- No contradiction; exclusions only sharpen "actual built/deployable" to "as archived".
- Grouped scope (contract `C1.sourceVerdict`): S001 alone does **not** entail the 53-54 sentence.
  S001 gives artifact root plus exclusions; S002 the v4/v5 hidden-input change, S003/S004 artifact
  and build shapes, S006 Jekyll exclusions. "Point the manifest at build output" is local
  operational synthesis; a grouped HOLD is defensible only with that step named per source.

## Citing set and denominator

S001 token occurrences in `corpus/knowledge/`: ghp-served-set.md 7, ghp-subpath-spotcheck.md 4,
publish-channels.md 6 (metadata range `S001-S007` line 2), sitemap-orphan-audit.md 12 (metadata
range `S001-S006` line 2), speedrun-pipeline.md 4, static-canonical-preflight.md 1 (group
`S001–S006` line 54, en dash). `count_c1.py`'s range regex expands all three ranges.

- No new citing pair discovered; the six-file set equals the counter's enumeration.
- r26 `statements.json` carried five S001 pairs (all but static-canonical-preflight). The missing
  sixth is exactly `(S001, corpus/knowledge/static-canonical-preflight.md)` — the frozen r27
  obligation, not a discovery. Denominator unchanged by this report.
- `corpus/lessons/round-20.md:203` and `corpus/lessons/round-7.md:57` also cite S001, but
  `count_c1.py` reads `corpus/knowledge/**` only; named here so they are not mistaken for missed pairs.

## Suggested ledger record (author-side; L1 adjudicates)

```json
{"row":"S001","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD",
 "fetchIndex":1,
 "quote":"description: \"Path of the directory containing the static assets.\" required: true default: \"_site/\"",
 "anchor":"main action.yml lines 9-12 (path input, default _site/); identical at v4.0.0 lines 9-12; archive root main 33-40, v4 29-36",
 "reason":"Both S001 URLs reopened 2026-10-21T20:01Z, HTTP 200, bytes identical to r27 retained (sha256 4524ed61...cd046, e8ce828a...ca6741). The action archives a caller-named static-assets directory (default _site/) with unconditional .git/.github excludes, so the deployed artifact is not the checkout tree. That supports the premise of lines 53-54 only; preparing the manifest over build output is local synthesis and S001 alone does not entail it."}
```

## Uncertainties and gaps

- Anchor coordinates are main-scoped; whether they were meant for both copies is unresolvable
  from the row. Recorded as ambiguity, not correction.
- "built" HTML is not asserted; `_site/` is the sole build-output signal. The action is
  content-agnostic.
- Served copies came via Fastly (`max-age=300`); cached bytes could be ~5 minutes old, but both
  URLs are commit-addressed, so a cached copy cannot be another revision.
- Pages processing between artifact and HTTP response is outside S001 and was not probed.
- No production artifact, public site, browser, account or property operation; no broad download.
- No production-artifact claim is implied: line 55 of the citing file already records that
  round 22 had no production artifact, and this report does not change that.

## Repro (scratch `/fast/scratch/hyaku/kake-r27/SourceOpenS001`)

```sh
curl -sS --max-time 60 -A "kake-source-recheck/1.0" -o live-1.body -w 'http=%{http_code} bytes=%{size_download}\n' \
  https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml
curl -sS --max-time 60 -A "kake-source-recheck/1.0" -o live-2.body -w 'http=%{http_code} bytes=%{size_download}\n' \
  https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml
cmp live-1.body <(gzip -dc ../../../../home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-27/fetched/S001-1.raw.gz)
```

Scratch: `live-1.body`, `live-2.body`, `S001-1.body`, `S001-2.body`, `headers.txt`, `access-time.txt`.
No tool install, no pacman/upgrade/service operation, no corpus/lane/index/jj/Git mutation.
Checks not run (L1 runs integration).

Report: `.ufo/waves/round-27/w1/SourceOpenS001.md`
