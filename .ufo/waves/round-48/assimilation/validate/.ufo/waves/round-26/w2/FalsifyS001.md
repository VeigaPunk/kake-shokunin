# Falsify S001 — round-26 C1 freshness recheck (receipt HOLD)

Seat: KakeR26-2.FalsifyS001 (leaf member, no subagent dispatch). Milestone: r26-recheck-falsify. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S001.json` (verdict **HOLD**) + the S001 row line in `corpus/SOURCES.md:9`.
Goal: try to show the receipt is WRONG — quote does not ground the row's teaches (page chrome / neighbouring clause instead), anchor mislocated in raw bytes, or a content/version change missed.

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity: **low** (four documentary observations, none of which change the verdict or require a correction; see "Non-blocking observations").

## The row under attack (ground truth)

`corpus/SOURCES.md:9` (byte-identical at base `97404de4` and candidate `e28312b1` — verified by `diff <(git show 97404de4:corpus/SOURCES.md | sed -n '9p') <(git show e28312b1:corpus/SOURCES.md | sed -n '9p')` → identical; the only SOURCES.md change in the candidate is the appended round-26 narrative paragraph at line 79):

```
| S001 | actions/upload-pages-artifact action.yml at v4.0.0 and main commit — https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml; https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml | code | A | Hidden-file inclusion and invariant exclusions in this action | inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39; v4.0.0 tag and main 5f327015a708106f6f1b7c9a633901af30fe80cb | The action exposes hidden-file inclusion while excluding .git and .github regardless; v4.0.0's default dotfile exclusion is separately evidenced by S002 | mined | 2026-10-19 | on-release | corpus/knowledge/ghp-served-set.md |
```

- teaches: *“The action exposes hidden-file inclusion while excluding .git and .github regardless; v4.0.0's default dotfile exclusion is separately evidenced by S002”*
- anchor: *“inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39; v4.0.0 tag and main 5f327015a708106f6f1b7c9a633901af30fe80cb”*

Receipt under attack (`.ufo/waves/round-26/rechecks/S001.json:1-9`; identical to the committed blob at `e28312b1` — `git show e28312b1:.ufo/waves/round-26/rechecks/S001.json | sha256sum` == `sha256sum` of the worktree file == `75a7ad99c367834727238eb8fc25eeb4b18fc2a40a846a572aba2c961db7b862`):

```json
{"id":"S001","verdict":"HOLD","fetchIndex":2,
 "quote":"(those starting with a dot) in the artifact. Excludes.git and.github regardless.",
 "anchorObserved":"Main-commit copy (S001-2): inputs.include-hidden-files lines 17-20; Linux Archive artifact exclusion block lines 37-39 (same unconditional .git/.github pair repeats at 55-56 macOS and 73-74 Windows)",
 "reason":"Main-commit copy exposes include-hidden-files (default \"false\") that gates only the dotfile exclude, while --exclude=.git and --exclude=.github remain unconditional in all three OS archive steps; the v4.0.0 copy (S001-1) has no such input and hard-codes --exclude=\".[^\/]*\" three times, exactly the split the row attributes to S002. Scope and teaches still hold.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)?  → NO DEFECT

The quote is taken from the `include-hidden-files` input **description string** — the very clause the row is about — not from nav chrome, a sidebar, a neighbouring section, or a different row’s document.

Retained raw bytes `fetched/S001-2.raw.gz` (gzip container 895 B; decompressed 2 895 B; sha256 of the decompressed bytes `e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741`, equal to `fetched/manifest.json:22-38` and to `population.json`’s pinned sha for S001 index 2). Raw line 18:

```
    description: "Include hidden files and directories (those starting with a dot) in the artifact. Excludes .git and .github regardless."
```

- The quoted fragment is the tail of that description — the clause that states the invariant exclusions the row teaches. It is the *only* occurrence of “starting with a dot” in any retained text view (grep over all 32 `fetched/text/*.txt`: `S001-2.txt` only), so it is row-specific, not boilerplate.
- Clause-by-clause grounding of the teaches:
  - “exposes hidden-file inclusion” ← the input key `include-hidden-files:` at raw line 17, `required: false`, `default: "false"` at line 20, plus the quoted description. The receipt’s `anchorObserved` names exactly lines 17-20.
  - “while excluding .git and .github regardless” ← raw lines 37-38 (Linux), 55-56 (macOS), 73-74 (Windows): `--exclude=.git \` and `--exclude=.github \` sit **outside** the conditional; the only conditional exclusion is line 39/57/75 `${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }}`. So the input gates **only** the dotfile exclude — precisely the receipt’s reason (“gates only the dotfile exclude”). The word “regardless” in the row’s teach is the source’s own word, in the same sentence as the quote.
  - “v4.0.0’s default dotfile exclusion is separately evidenced by S002” ← retained `fetched/S002-1.raw.gz` (v4.0.0 release page) contains “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact”; `S002-2` (v5.0.0) contains “feat: add include-hidden-files input”. The receipt’s reason states the same split from the S001 side (v4.0.0 copy has **no** such input — `gzip -dc S001-1.raw.gz | grep -c include-hidden-files` → `0` — and hard-codes the dot pattern 3×).
- Counter-rule replication (I re-implemented `measure.py`’s own `quote_in_text` against the committed `source_text.py` at `e28312b1`, which is byte-identical to the worktree copy): normalized quote is a word-bounded substring of S001-2’s effective text → **True**; and it occurs in **no other** population row’s fetch text (loop over all `population.json` rows × fetches → hits only `('S001', 2)`), so the specificity rule holds. Token/word budget: 13 alphanumeric tokens / 11 whitespace words (≥6 / ≤25 required).

## Attack 2 — Is the anchor observed correct in the raw bytes?  → NO DEFECT

`gzip -dc fetched/S001-2.raw.gz | cat -n` (line numbers are raw-file line numbers, since the file is plain YAML with no HTML view):

| receipt claim | raw lines | raw content |
|---|---|---|
| `inputs.include-hidden-files lines 17-20` | 17-20 | `include-hidden-files:` / description / `required: false` / `default: "false"` ✓ |
| `Linux Archive artifact exclusion block lines 37-39` | 37-39 | `--exclude=.git \` / `--exclude=.github \` / `${{ inputs.include-hidden-files != 'true' && '--exclude=.[^/]*' || '' }} \` ✓ (Linux step header `- name: Archive artifact` at line 28) |
| “same unconditional .git/.github pair repeats at 55-56 macOS and 73-74 Windows” | 55-56, 73-74 | `--exclude=.git \` / `--exclude=.github \` at both ✓ (macOS step header line 46, Windows step header line 64) |

Text-view fidelity (the text views are the comparison surface the counter itself uses): `normalize(text_of(raw,'text/plain; charset=utf-8'))` reproduces `fetched/text/S001-2.txt` exactly (modulo one trailing newline) → **True**; same check for S001-1 → **True**. The views are 2 lines each (one long line + newline), so the receipt's line references are unambiguously raw-file references.

Manifest/population consistency: `population.json` S001 index 1 → `sha256 4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046`, `file fetched/S001-1.raw.gz`, `status 200`; index 2 → `sha256 e8ce828a…`, `file fetched/S001-2.raw.gz`, `status 200`. `fetched/manifest.json:3-19` and `:22-38` carry the identical shas and `content-length` 2 529 / 2 895; recomputing sha256 over the decompressed retained bytes reproduces both values (`4524ed61…`, `e8ce828a…`). The manifest pins the **decompressed** bytes (the .gz containers hash to `37099a34…` / `198748c5…`), which is what `measure.py`’s `fetch_sha_mismatch` check expects.

## Attack 3 — Did content/version change in a way the receipt missed?  → NO DEFECT

Plain public GETs of the same upstream document (read-only, piped straight to `sha256sum`/`diff`; nothing written to disk, no accounts, no credentials, no property probing):

| fetch | live sha256 | retained sha256 | verdict |
|---|---|---|---|
| pinned `7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml` (row URL 1) | `4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046` | `4524ed61…` (S001-1) | identical |
| pinned `5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml` (row URL 2) | `e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741` | `e8ce828a…` (S001-2) | identical |
| tag `v4.0.0/action.yml` | `4524ed61…` | `4524ed61…` | identical (tag still points at the pinned content) |
| branch `main/action.yml` (today) | `e8ce828a…` | `e8ce828a…` | identical — **upstream main’s action.yml has not changed at all** |
| tag `v5.0.0/action.yml` | `f84e759011e0c497e696f5bce4ebb5fbe9bbdc5aea309b73795283fa139c1558` | — | differs from pinned main in **one line only** |

The `v5.0.0` vs pinned-main diff is exactly one line and it is **outside S001’s scope**:

```
84c84
<       uses: actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f # v7.0.0
---
>       uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1
```

The hidden-file semantics (`include-hidden-files` input, unconditional `.git`/`.github` excludes) are identical in v4.0.0, v5.0.0 and current main. No newer upstream release exists to invalidate the row: the public release feed lists **v5.0.0 as the newest** release, the tag list stops at `v5.0.0`/`v5`, and the retained `S002-2` page (fetched 2026-10-21) independently shows `v5.0.0 / Latest`. The row’s own anchor names a pinned commit SHA, so its content is immutable by construction — and the live fetch confirms the pins still resolve to the retained bytes.

Downstream consistency of the HOLD (the receipt’s decision must be coherent with the row-level and statement-level ledgers):

- `statements.json:7-13` (S001 pair): `statements 28, seatStale 3, stale 0, seatUnverifiable 4`, with an explicit `l1Disposition` recording why the three seat-STALE anchor-drift findings were rejected (base-scoped pointers, QUALITY round-21 coordinate rule) and that the four v3.0.1 statements are UNVERIFIABLE. Row-level HOLD is therefore consistent with statement-level adjudication.
- The corpus carries **no** `[r26-recheck S001 STALE]` tag (`grep -c` over `corpus/**` at `e28312b1` → 0 for S001), and the 8 tags that do exist (S003×2, S010×2, S021×1, S026×1, S030×2) exactly match `statements.json`’s `stale` total of 8 — so the counter’s `statement_correction_absent` rule is satisfied and no S001 correction was silently dropped.
- The four UNVERIFIABLE v3.0.1 statements are disclosed in the corpus itself at `corpus/knowledge/ghp-served-set.md:89` (“UNVERIFIABLE this round (not STALE): the four upload-pages-artifact v3.0.1 statements. S001 pins only v4.0.0 and main, and no v3.0.1 bytes are retained under round 26…”).

## Attack 4 — Receipt schema / counter-rule conformance (replicated locally)  → NO DEFECT

Re-implementing `measure.py`’s `Checker.check` rules for this receipt, against the committed `source_text.py` (identical to worktree) and the committed manifest/population:

- key set == `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}` → **True** (no missing/extra keys).
- `id == "S001"` ✓; `verdict == "HOLD"` ∈ {HOLD, STALE, UNVERIFIABLE} ✓; `reason` non-empty ✓; `anchorObserved` non-empty ✓; `correction == null` (required for HOLD) ✓.
- `fetchIndex 2` is a population fetch of S001 ✓; manifest entry status 200, sha matches the population pin, file name matches ✓.
- quote: 13 tokens / 11 words ✓; word-bounded normalized substring of the effective fetch text ✓; unique across rows ✓.

## Non-blocking observations (documentation only — no correction to the receipt, none to the row cells)

1. **The receipt’s `quote` is a normalized text-view rendering, not byte-verbatim raw text.** Raw line 18 reads `Excludes .git and .github regardless.`; the recorded quote reads `Excludes.git and.github regardless.` The difference comes from the wave’s own `source_text.normalize()` rule (`re.sub(r'\s+([,.;:)])', r'\1', text)` drops a space before `.`), which the counter applies to both sides of `quote_in_text`, so the receipt passes the defined rule; `w1/PairS001GhpServedSet.md` §“Checks and boundaries” documents this lossy render explicitly. A reader who checks the quote against the raw source will see the space collapse — expected, but worth stating.
2. **The receipt’s `reason` renders the v4.0.0 flag with single quotes** (`--exclude='.[^/]*'`), while the raw bytes use double quotes (`--exclude=".[^/]*"`, S001-1 lines 35/53/71). Cosmetic rendering difference in prose only; the semantic content quoted is identical, and the same pair report quotes the raw double-quoted form correctly.
3. **The row cell’s line numbers resolve only in the main copy.** At v4.0.0 (S001-1) lines 17-20 are `outputs:` / `artifact_id:` / its description / its value, and lines 33-35 / 51-53 / 69-71 are the three exclusion blocks — so “inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39” is a main-commit anchor only. The receipt handles this honestly (`anchorObserved` says “Main-commit copy (S001-2)”), and `w1/RowS001.md` caveat 1 records it. Since row cells are append-only this round, the anchor cell stays as it is; the receipt’s qualification is the mitigation.
4. **Traceability nit (wave-wide, not S001-specific):** `w1/PairS001GhpServedSet.md:51,56,61` and its trailer (line 97) still carry three `[r26-recheck S001 STALE]` correction blocks and `"stale":3`, while L1 later adjudicated `stale: 0` (`statements.json`) and the corpus correctly contains zero S001 STALE tags. The corpus and the ledger agree, so the counter’s rule is satisfied and the row’s HOLD is unaffected; but the pair report read in isolation would suggest three S001 corrections that do not exist. The same seat-vs-ledger pattern appears for S005, S011, S012, S013, S020, S027, so it is a wave reporting convention, not an S001 defect.

## Checks that could NOT be closed (residual risk)

- **“Current action commit 5f327015”** (`corpus/knowledge/ghp-served-set.md:2`) was not verified as *commit-HEAD* identity: I confirmed the **content** of upstream `main/action.yml` today is byte-identical (`e8ce828a…`) to the pinned commit’s file, but I did not fetch the branch-head commit metadata (that endpoint is outside the row’s URL set and the lane’s GET budget). The pair report already records this as a FLAG (“‘current’ is a moving label”, judged HOLD on content identity). Same for the row anchor’s phrase “main 5f327015…” — that anchor names the SHA, so it is immutable regardless.
- **v3.0.1 claims** (four statements in `ghp-served-set.md`) remain UNVERIFIABLE for this round: no v3.0.1 bytes are retained under round 26. They stay historical claims, disclosed in the corpus EOF block at `corpus/knowledge/ghp-served-set.md:89`.
- **GNU tar pattern semantics** of `--exclude=.[^/]*` (anchoring, depth) are S008’s surface, not S001’s; the receipt makes no matching-detail claim and I made none. (Checked and dismissed as a non-issue: the unquoted main-branch form `--exclude=.[^/]*` is a single shell word whose pattern would have to match a filename literally starting with `--exclude=.`, which no file does — bash leaves it unchanged.)

## Verification gaps / boundaries

- Network use: only read-only public GETs of `raw.githubusercontent.com` action.yml at the row’s own pinned SHAs, at tags `v4.0.0` / `v5.0.0`, at branch `main`, plus the repository’s public release-feed and tag-list pages, to test for a content/version change. Nothing was saved to disk (all output piped to `sha256sum`/`diff`/stdout), no accounts or credentials, no property probing, no publication, no round-24 material read or run, no delegation. No file outside this report was written; no scratch files in `/tmp`.
- No build, test, linter or counter run was performed: this item does not name `measure.py`, and the round's counter result (candidate 32/32, exit 0) was supplied with the assignment. The S001-specific counter rules were instead replicated directly from the committed `measure.py` / `source_text.py` in-process.
- Tooling: nothing installed or upgraded (python3, gzip, sha256sum, curl, git plumbing all pre-existing). Git access was read-only (`git show` / `git rev-parse` / `git grep` on committed objects); the lane Git index and jj state were not touched. The working tree already carried unrelated untracked round-26 artifacts (`.ufo/waves/round-26/w2/`, `verification/`, `w2-*.json`, `__pycache__/`) that I did not create or modify.

```json
{"target":".ufo/waves/round-26/rechecks/S001.json (SOURCES.md:9 row S001, verdict HOLD)","verdict":"AGREE","severity":"low"}
```
