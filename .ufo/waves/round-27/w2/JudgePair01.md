# JudgePair01 — r27 fresh falsification, pair (S001, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.JudgePair01 (leaf, read-only). Axis: freshness. Milestone: r27-fresh-falsification.
Candidate measured: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Base `83528f7c…`, declarations `be375d9…`.
No source/docs/registry edit made; no install performed (no tool needed).
Scratch (only writes): `/fast/scratch/hyaku/kake-r27/JudgePair01/` (`TMPDIR` set there).

## 1. Attacked item (exact)

`.ufo/waves/round-27/pairs.json` → `pairs[]` entry
`{"row":"S001","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD","fetchIndex":1,
"quote":"tar \\ --dereference --hard-dereference \\ --directory \"$INPUT_PATH\" \\ -cvf \"$RUNNER_TEMP/artifact.tar\" \\ --exclude=.git \\ --exclude=.github \\ --exclude=\".[^\"]*\"",
"anchor":"v4.0.0 action.yml Archive artifact, Linux tar command lines29–36",
"reason":"Configured input path and unconditional .git/.github/default dot-path exclusions can make artifact membership differ from a checkout; the manifest instruction is local synthesis."}`

Citing sentence (candidate blob `corpus/knowledge/static-canonical-preflight.md`, sha256 `40ebd1dabc122e620d09974ac973b3262649be9520fea2fa42ebe4dce1ca8a12`, line 54):
> "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."

A/B evidence: `w1/Pair01A.md` (HOLD, fetchIndex 2), `w1/Pair01B.md` (HOLD, fetchIndex 1) — both present in the candidate tree.
Attack question: does the named official source actually support the attribution at S001's own scope, at the cited anchor, with the cited bytes still current?

## 2. Candidate/tree binding (read-only, full hash only)

- `git show ac46a7472d945a6d7ff135e4d7f07b0b6913d835:corpus/knowledge/static-canonical-preflight.md | sha256sum` → `40ebd1da…ca8a12`; same for `.ufo/waves/round-27/pairs.json` → `f1fa20cab67053fea3945330d14efa59f095ede22b6dacbb058d688d0b376a6a`; working-tree copies hash identically (no drift between measured commit and disk).
- `git ls-tree ac46a7472d945a6d7ff135e4d7f07b0b6913d835 -- .ufo/waves/round-27/fetched/` → 8 blobs + `text/` tree tracked (the w1 seats' "fetched/ untracked → source_missing" hazard is closed at the candidate).

## 3. Probes (expectation declared before each run)

**P1 — reopen the two named S001 sources.**
Expectation: HTTP 200; byte length and sha256 equal to `fetched/manifest.json` `sha256`/`receivedSha256` (4524ed61…, e8ce828a…); any drift ⇒ the HOLD quote/anchor would be stale.
`curl -sS -L` → `s001-1.yml http=200 bytes=2529 sha=4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046`; `s001-2.yml http=200 bytes=2895 sha=e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741`; clock `2026-10-21T21:58:36Z`. **No drift.**

**P2 — retained bytes vs received bytes.**
Expectation: for a `code` row the retained representation is the received bytes verbatim, so decompressed sha == received sha (no HTML-filter reconstruction issue for this row).
`gzip -dc fetched/S001-1.source.gz | sha256sum` → `4524ed61…`; `S001-2.source.gz` → `e8ce828a…`; `fetched/text/S001-1.txt` sha → `4524ed61…` (verbatim, not filtered). Manifest `retainedRepresentation.kind=received_code_bytes`, `rawHttpBodyRetained=true`. **Consistent.**

**P3 — anchor fidelity in the cited bytes.**
Expectation: `lines29–36` must contain the quoted tar block; `inputs.path` at lines 9–12 with default `_site/`; exclusions repeated in all three OS steps.
`cat -n s001-1.yml` (live == retained): 9–12 `path:`/"Path of the directory containing the static assets."/`required: true`/`default: "_site/"`; **29–36** = `tar \` / `--dereference --hard-dereference \` / `--directory "$INPUT_PATH" \` / `-cvf "$RUNNER_TEMP/artifact.tar" \` / `--exclude=.git \` / `--exclude=.github \` / `--exclude=".[^/]*" \` / `.`; macOS 47–54, Windows 65–73. Main pin: `include-hidden-files` 17–20 (`default: "false"`), exclusion block 37–39. **Anchor accurate** (the quote is a whitespace-normalized prefix of lines 29–35).

**P4 — re-derive the counter's quote rules myself (hash-pinned `.ufo/waves/round-26/source_text.py`).**
Expectation: ≥6 tokens, ≤25 words, normalized substring of the row's own text view, and absent from every other row's view (row-specific).
Tokens 17, words 16; own-view normalized substring **True**; present in another row's view: **none**; present in S001's other index (5f327015): **False**. **Passes.**

**P5 — run the frozen counter at the candidate (consumer command, read-only).**
Expectation: my pair appears as `valid: true` with verdict HOLD; C1 exit non-zero because carried UNVERIFIABLE pairs stay undecided (55/58, never green).
`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a7472d945a6d7ff135e4d7f07b0b6913d835` → **exit 1**; `population=32 citingPairs=58 reviewedPairs=58 decided=55 newDecided=18 r26CarriedPairs=41 knownUnverifiableUnits=7 knownUnverifiablePairs=3`; findings = `S001/ghp-served-set.md (3 units)`, `S007/ghp-custom-domain.md (1)`, `S033/static-canonical-preflight.md (3)`; `missing` = those same three; `unreviewed=[]`; outcome row `{row:S001, file:corpus/knowledge/static-canonical-preflight.md, verdict:HOLD, valid:true}`. **My pair decided; C1 stays non-green (55/58).** The still-UNVERIFIABLE `S001` is a different `(row,file)` key (`ghp-served-set.md`) and outside this seat's scope.

**P6 — freshness probe on the moving ref (unpinned `main`, public GET).**
Expectation: either upstream drift (→ the "main commit" label and the invariant-exclusion premise would need re-opening) or byte-identical.
`curl …/upload-pages-artifact/main/action.yml` → http 200, 2895 bytes, sha `e8ce828a…`; `diff main-action.yml s001-2.yml` → identical; tip still excludes `.git`/`.github` unconditionally (lines 37–38). **No drift; the pinned "main commit" label is currently true.**

## 4. Semantic judgment (independent, at S001's own scope)

- **Supported premise.** The cited bytes show the Pages artifact is a tar of a *configured* directory (`--directory "$INPUT_PATH"`, `INPUT_PATH = inputs.path`, default `_site/`), with `.git`/`.github` excluded unconditionally in every OS step and dot paths excluded unconditionally at v4.0.0 (conditionally at the main pin, default `false`). Therefore the archived membership is a filtered build directory, never a checkout listing. This supports the negative half of line 54 ("not over an assumed checkout served set") and nothing about live-site membership.
- **Inferential step.** "Prepare the manifest over actual built/deployable HTML" is local publisher policy; S001 does not entail it. `pairs.json` labels this ("the manifest instruction is local synthesis") and the candidate's appended "Round-27 grouped-citation adjudication" section labels it as well ⇒ contract `C1.sourceVerdict` requirement met.
- **Verdict.** HOLD stands at S001's own scope. Not STALE: no clause of line 54 is contradicted by the current bytes, and the line states no version-specific or dated fact. Not UNVERIFIABLE: both named URLs were re-opened with HTTP 200, byte-identical digests, and the quote is a verbatim substring of the retained bytes.

## 5. Findings (author-side)

1. **[PRECISION — non-blocking] S001 ledger reason reaches one clause beyond the row's registry scope.** `corpus/SOURCES.md` S001 declares scope "Hidden-file inclusion and invariant exclusions in this action"; the record's anchor is lines 29–36. The reason's first clause, "Configured input path", is evidenced by `inputs.path`/default `_site/` at lines **9–12** — same cited document, but outside both the declared scope and the record's anchor range. Not a STALE trigger (the attribution is not wrong at the sentence's scope, and `--directory "$INPUT_PATH"` inside the quote already shows a configured archive root). Suggested remedy for L1, no ledger rewrite needed: state the default as "lines 9–12 of the same v4.0.0 file", or drop the default-`_site/` clause from the reason (the "build output vs checkout root" leg belongs nearer S004).
2. **[PRECISION — non-blocking] "default dot-path exclusions" understates the cited bytes.** At fetchIndex 1 (v4.0.0) the dot-path exclusion is **unconditional** (lines 35/53/71); "default" is accurate only for the main pin (`include-hidden-files` default `false`, lines 17–20). The wording is looser than the bytes but does not overstate support (unconditional ⊇ default), so HOLD is unaffected.
3. **[CONFIRMED] Both w1 seats' pre-integration hazard is resolved at the candidate.** `fetched/` is tracked in the candidate tree and the counter reports no `source_missing` for any source-kind row; the pre-candidate blocker described in `w1/Pair01A.md §8.2` / `w1/Pair01B.md` no longer applies.
4. **[CONFIRMED] Quote-fidelity note for other seats.** For this row the rendition pitfall both seats warned about (whitespace collapsing) does not bite: `kind=code` retention is verbatim, so `text/S001-1.txt` and the decompressed `.raw.gz` have the same sha256 and the raw-accurate quote passes unchanged.

## 6. Reasonable dissent addressed

- **S005 / preflight (`S001–S006` over-inclusion).** Confirmed and already adjudicated: S005's own statement is CNAME/domain configuration, with no bearing on which built HTML populates a manifest. `pairs.json` records `S005 × static-canonical-preflight.md` as source-STALE with quote "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created" (anchor: Configuring an apex domain, step 4); the candidate file carries `[r27-recheck S005 STALE]` (counter `valid: true`). The appended paragraph keeps the sentence's substance as synthesis over S001/S002/S003/S004/S006 and invents no extra host-component leg ⇒ the correction is honest, not a silent rescope.
- **S005 / sitemap.** Artifact-grounded and correct in kind: the evidence artifact `.ufo/round-20/resume/citation-disposition.json` contains `"supersededClaim": "Each deployment snapshots the entire checked-out tree."`, i.e. the checkout-membership claim that S001/S004/S006 superseded; S005 (custom domain) is absent from all eight r20 correction records, so its inclusion in the S001–S006 band is the stale attribution. `STALE` here is partial (date/base stay HOLD) and matches contract STALE semantics (wrong attribution at its own scope), with no r26 record rewritten.
- **S003 / sitemap.** Holds on external historical artifact evidence (`corpus/lessons/round-20.md` contains the named C3 string); it is not self-support and does not claim S003 appears in every inline correction. Consistent with my own reading of S001's mechanism-only contribution.
- **S004 / ghp steps.** The `S004 × ghp-served-set.md` STALE override checks out against retained bytes: S003's retained visible text carries the general flow ("Use the actions/upload-pages-artifact action to upload the static files as an artifact"; "use the actions/deploy-pages action to deploy the artifact"), whereas S004's retained text contains **neither** that upload sentence **nor** the string "general flow"; S004 instead carries the unnumbered "Configuring the upload-pages-artifact action" section ("The GitHub Pages artifact should be a compressed gzip archive containing a single tar file"). The numbered flow therefore belongs to S003. Residual: the retained visible text is not itself numbered (HTML list numbers are not part of the visible-text rendition), so "items 4–5" is an inference from the ordered list, not a byte-read; S004-1 does contain "deploy-pages action" in the unrelated "Deploying GitHub Pages artifacts" requirements context, so that string must not be read as the numbered flow. None of this touches my S001 premise.

## 7. Residual risk / verification gaps

- My seat did not open S002/S003/S004/S005/S006's own named documents beyond the retained r27 renditions needed for the dissent above; my HOLD for S001 does not depend on them.
- "Current upstream `main`" was verified by one public GET at 2026-10-21T21:58Z; a later upstream change would not falsify this HOLD (the cited pins are immutable and line 54 states no version fact), but it would invalidate the registry label "main commit" for S001.
- HTTP authenticity of the retained body is established for a code resource (verbatim bytes, digest match, live 200 re-fetch). No live-site membership, deployment artifact, or canonical-HTML behaviour was tested — none is claimed by this pair.
- C1 as a whole remains UNPROVABLE at 55/58 decided with 7 known unknown units across 3 pairs; the review population of 58 must not be reported as 58 strictly decided.

## 8. Tools / installs

None installed or updated in this seat (no tooling gap; `curl`, `git`, `python3` from base system). pacman transactions PAUSED — none performed.

Report: .ufo/waves/round-27/w2/JudgePair01.md
