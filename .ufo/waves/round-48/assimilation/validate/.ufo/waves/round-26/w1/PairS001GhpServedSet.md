# S001 × ghp-served-set — round-26 freshness pair

Axis: freshness. Milestone: r26-recheck-build. Entry: `corpus/knowledge/ghp-served-set.md` (79 content lines; not modified by this pair). Row: `corpus/SOURCES.md:9` (usedBy: `corpus/knowledge/ghp-served-set.md`).

## Basis

- Retained raw bytes (public GET, fetchedAt 2026-10-21T15:09:32Z):
  - `fetched/S001-1.raw.gz` = v4.0.0 @ 7b1f4a7; raw sha256 `4524ed61c2fb61b4d7e88de2d779fe937461b6926aeb716b56f047ae3abcd046`, 2529 B; equals `manifest.json:18`.
  - `fetched/S001-2.raw.gz` = main @ 5f327015; raw sha256 `e8ce828a4f2a0e500dc506bc03c706881dab7dc4b7cd527c7ea175c6c0ca6741`, 2895 B; equals `manifest.json:37`.
- Text views: `fetched/text/S001-1.txt` (sha256 `90ef84b80160d4539df2088c570e08d5fef8a531aa0dc4045beb72f3a2312753`), `fetched/text/S001-2.txt` (sha256 `ea804af2dcab49e31c931ce6e76b5a911ec3642eaa599d7978e86a80a91f63c5`). Every quote below is a verbatim substring of these text views (checked programmatically).
- Row teaches (`population.json` id S001) on retained bytes: HOLD. Main carries the `include-hidden-files` input (raw lines 17-20); `.git`/`.github` excludes are unconditional at both commits; v4.0.0 dot-pattern is unconditional (raw lines 35, 53, 71).
- Result: **28 statements. 21 HOLD. 3 STALE (anchor drift in the r20 tail; no S001 content change). 4 UNVERIFIABLE (v3.0.1, not retained; reported separately, not counted decided).**

## Verdicts

| # | file:line | Statement | Verdict | Verbatim quote (S001 text view) | Basis / anchor observed / flags |
|---|---|---|---|---|---|
| 1 | ghp-served-set.md:1 | Header cites S001 at the v4.0.0 URL and anchor `§Archive artifact` | HOLD | `- name: Archive artifact shell: sh if: runner.os == 'Linux'` (S001-1, S001-2) | Anchor present: three `Archive artifact` steps (S001-1 raw lines 24, 42, 60). |
| 2 | ghp-served-set.md:2 | `verified-at: 2026-10-19 (v4.0.0 commit 7b1f4a7 …)` | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Bytes unchanged: sha256 matches manifest:18; live pinned 7b1f4a7 and tag v4.0.0 identical today. FLAG: date superseded by the 2026-10-21 re-fetch, content identical; no correction required. |
| 3 | ghp-served-set.md:2 | `current action commit 5f327015` | HOLD | `Include hidden files and directories (those starting with a dot) in the artifact.` (S001-2) | Bytes match manifest:37; live branch main identical today (content identity, not commit-HEAD identity). FLAG: "current" is a moving label. |
| 4 | ghp-served-set.md:3 | Recheck command for v4.0.0 and main, `grep -cF -- '.[^/]*'` | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Pattern occurs on S001-1 lines 35, 53, 71 (count 3) and S001-2 lines 39, 57, 75 (count 3). |
| 5 | ghp-served-set.md:3 | Recheck command, v3.0.1 component | UNVERIFIABLE | none (no v3.0.1 text retained) | Not in the fetched set (see Flags). Same-day in-memory GET of tag v3.0.1 reproduces the counts; not retained, so not decided. |
| 6 | ghp-served-set.md:7-8 | `upload-pages-artifact` excludes `.git` and `.github` for `path: .` | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1); `--exclude=.git \ --exclude=.github \ ${{ inputs.include-hidden-files` (S001-2) | Unconditional in all three OS steps at both commits: S001-1 lines 33-34, 51-52, 69-70; S001-2 lines 37-38, 55-56, 73-74. Exclusions do not depend on the `path` input. |
| 7 | ghp-served-set.md:8-9 | v4.0.0 excludes dot paths by default | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | v4.0.0 has no include input (inputs block lines 4-16); pattern unconditional at lines 35, 53, 71. |
| 8 | ghp-served-set.md:9-10 | Pinned current action defaults `include-hidden-files` to `false` | HOLD | `required: false default: "false" outputs: artifact_id: description:` (S001-2) | Input block S001-2 lines 17-20; default `"false"` at line 20. |
| 9 | ghp-served-set.md:10-11 | …while excluding `.git` and `.github` regardless | HOLD | `--exclude=.git \ --exclude=.github \ ${{ inputs.include-hidden-files` (S001-2) | Excludes precede and sit outside the conditional (lines 37-38, 55-56, 73-74). Input description (line 18) reads "Excludes .git and .github regardless." (text view renders it `Excludes.git and.github`; see Checks). |
| 10 | ghp-served-set.md:11-12 | Archive can omit checkout paths; does not alone establish a live site's membership | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Follows from rows 6-7. S001 makes no site-membership claim. |
| 11 | ghp-served-set.md:14-15 | r20 tail: "Refines `corpus/README.md:26,52-55`" | STALE (anchor) | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1, premise) | Base cb807bc: README:26 = Sitemap/orphan audit row; :52-55 = Live-only orphan paths bullet (both correct then). Now: :26 = Speedrun pipeline row; the refinement sits at :28 (Sitemap/orphan row, r20 tag) and :59-62 (Live-only bullet, r20 tag at :60). See C1. |
| 12 | ghp-served-set.md:15 | r20 tail: "`SKILL.md:227`" | STALE (anchor) | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1, premise) | Base cb807bc :227 = URL lists (sitemap) row. Now :227 = Byte-twin copies row; the URL-lists row carrying the r20 tag is :229. See C2. |
| 13 | ghp-served-set.md:15-16 | r20 tail: "`corpus/knowledge/sitemap-orphan-audit.md:20-30`" | STALE (anchor, incomplete) | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1, premise) | Base heading :18, paragraph :20-30. Now heading :22, paragraph :24-34 (+4). Decisive sentence "the live tree IS the last-pushed `origin/main`" is at :32, outside the cited 20-30 range. See C3. |
| 14 | ghp-served-set.md:16 | r20 tail: "`corpus/lessons/round-7.md:20-25`" | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1, premise) | Range unchanged, base and now: round-7.md:22 reads "every deploy ships the entire checked-out tree as a fresh artifact." |
| 15 | ghp-served-set.md:16-17 | "checkout membership alone was used as a proxy for publication" | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1, premise) | Exclusions make archive membership differ from checkout membership. Proxy use stated in past tense; still visible at sitemap-orphan-audit.md:25 and round-7.md:22. |
| 16 | ghp-served-set.md:21 | v4.0.0 excludes `.[^/]*` in all three OS steps | HOLD | `--exclude=".[^/]*" \.` (S001-1; three occurrences in text view) | Raw lines 35 (Linux), 53 (macOS gtar), 71 (Windows). |
| 17 | ghp-served-set.md:21-22 | "v3.0.1 does not" (exclude dot paths) | UNVERIFIABLE | none (no v3.0.1 text retained) | As row 5. Same-day in-memory tag v3.0.1 has 0 dot-pattern lines; not retained. |
| 18 | ghp-served-set.md:22 | Current commit conditionally excludes unless `include-hidden-files: true` | HOLD | `inputs.include-hidden-files != 'true' && '--exclude=.[^/]*'` (S001-2) | Raw lines 39, 57, 75 (three OS steps). |
| 19 | ghp-served-set.md:23-24 | Input quote "Include hidden files and directories (those starting with a dot) in the artifact." | HOLD | `Include hidden files and directories (those starting with a dot) in the artifact.` (S001-2) | Verbatim in text view and in raw line 18. |
| 20 | ghp-served-set.md:38 | Header dotfile loop returned `v4.0.0 3`, `main 3` | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Raw counts: S001-1 lines 35/53/71 = 3; S001-2 lines 39/57/75 = 3. |
| 21 | ghp-served-set.md:38 | Header dotfile loop returned `v3.0.1 0` | UNVERIFIABLE | none (no v3.0.1 text retained) | As row 5. |
| 22 | ghp-served-set.md:39-41 | `.github` loop returned `v4.0.0 3`, `main 3` | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Raw counts: S001-1 lines 34/52/70 = 3; S001-2 lines 38/56/74 = 3. |
| 23 | ghp-served-set.md:39-41 | `.github` loop returned `v3.0.1 3` | UNVERIFIABLE | none (no v3.0.1 text retained) | As row 5. |
| 24 | ghp-served-set.md:43-51 | Local repro flags reproduce the S001 exclusion set | HOLD (flags only) | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | Repro argv `--exclude=.git --exclude=.github '--exclude=.[^/]*'` matches S001 after shell quoting. Outcome lines 46-51 NOT re-run (needs a fixture under /tmp, prohibited); they are GNU tar behaviour, S008 pair. |
| 25 | ghp-served-set.md:52-54 | [INFERENCE] action source alone does not specify matching detail | HOLD | `--exclude=".[^/]*" \.` (S001-1) | Neither S001 text nor raw contains "anchored" or "wildcard"; exclusions are bare patterns. |
| 26 | ghp-served-set.md:60-62 | `CNAME` not excluded, so a root upload may package it; /CNAME unverified | HOLD | `--exclude=.git \ --exclude=.github \ --exclude=".[^/]*" \.` (S001-1) | "CNAME" absent from both raw files and both text views. Public /CNAME service is a status note (not probed). |
| 27 | ghp-served-set.md:65 | Replayable claim: records pinned action revisions, exact argv, outputs | HOLD | none (revisions live in fetch URLs, manifest.json:5 and :24, not the text view) | Pinned sha256 identities re-derived today (rows 2-3). |
| 28 | ghp-served-set.md:67 | Admission authority: action cited at its scoped source | HOLD | `A composite action that prepares your static assets to be deployed to GitHub Pages` (S001-1, S001-2) | Action self-describes as the GitHub Pages artifact composite. |

## Corrections (append at EOF of `corpus/knowledge/ghp-served-set.md`; original lines untouched)

C1 (row 11):
```
[r26-recheck S001 STALE] Anchor refresh for the r20 refinement at lines 14-17 (content unchanged). The cited corpus/README.md lines moved after base cb807bc. At the r26 tree the checkout-membership refinement sits at corpus/README.md:28 (Sitemap/orphan audit row; was :26) and corpus/README.md:59-62 (Live-only orphan paths bullet; was :52-55). The S001 exclusion facts in the Claim and Source checks sections are unchanged.
```

C2 (row 12):
```
[r26-recheck S001 STALE] Anchor refresh for SKILL.md:227 cited at lines 14-17 (content unchanged). At base cb807bc that line was the URL lists (sitemap) row. At the r26 tree that row, carrying the r20 correction, is SKILL.md:229; SKILL.md:227 is now the Byte-twin copies row.
```

C3 (row 13):
```
[r26-recheck S001 STALE] Anchor refresh for corpus/knowledge/sitemap-orphan-audit.md:20-30 cited at lines 14-17 (content unchanged). The GHP live-only orphan section moved by +4 lines: the checkout-as-deployed paragraph now spans corpus/knowledge/sitemap-orphan-audit.md:24-34, and the sentence 'the live tree IS the last-pushed origin/main' is at :32 (was :28), outside the cited 20-30 range as it reads at the r26 tree.
```

## Excluded (not attributed to S001; not counted)

- ghp-served-set.md:17-18 `publish-channels.md:5-14` "distinguishes Actions from branch publishing": S003 claim. Anchor drifted +4 (heading :3 at cb807bc, now :7; bullets :5-14, now :9-18). Route to the S003 pair.
- ghp-served-set.md:25-27 (S002), :28-33 (S003, S004, S006), :34-36 (S008): other row attributions.
- ghp-served-set.md:43-51 repro outcome lines (`.nojekyll`, `.well-known/x`, `a/.keep` absent): local GNU tar result; not re-run; S008 pair.
- ghp-served-set.md:56-58 Named debt (ds4cc/plazir): entry-internal debt; no S001 text reliance.
- ghp-served-set.md:66, :68, :69 QUALITY bullets: entry self-description; no S001 reliance.
- ghp-served-set.md:71-79 round-20 S008 erratum: attributes to S008 only; no S001 reference.

## Flags for L1

- `SOURCES.md:9` usedBy lists only `ghp-served-set.md`. S001 is also cited (plain ID search, not judged) in SKILL.md:229; corpus/README.md:28,60; knowledge/ghp-subpath-spotcheck.md:1,95; knowledge/publish-channels.md:1,2,58,60; knowledge/sitemap-orphan-audit.md:1,2,120-127; knowledge/speedrun-pipeline.md:1,70; knowledge/static-canonical-preflight.md:54; lessons/round-7.md:57-65; lessons/round-20.md:203,261; lessons/round-21.md:45. The used-by cell is an allowed logged edit; not applied here.
- `SOURCES.md:9` anchors hold on main bytes today: include-hidden-files lines 17-20 and Linux exclusion lines 37-39.
- v3.0.1 is outside the row's pinned set (SOURCES.md:9 pins v4.0.0 tag and main 5f327015; population.json S001 has two fetches). Rows 5, 17, 21, 23 need a retained fetch, or the entry must drop the v3.0.1 claims. Not decided here.
- Rows 2 and 3: date and "current" label refreshed by today's bytes; no correction required.

## Checks and boundaries

- Hashes and line numbers re-derived in memory from the `.raw.gz` files; sha256 and sizes equal manifest:18 and :37.
- Text-view fidelity: the text views are a lossy render. Whitespace runs collapse to one space, and a space before `.` or `:` is dropped (raw `Excludes .git and .github regardless.` renders as `Excludes.git and.github regardless.`). Applying that transform to the raw bytes reproduces each text view except the trailing newline (both files checked). Quotes are verbatim in the text views. Quotes on a single raw line: rows 3, 18, 19, 28. Every other quote spans raw line breaks that the view joins with spaces; in the exclusion-block quote the final `\.` is raw `\`, newline, indent, `.`.
- Live same-day GETs, in memory only (not written, not retained): pinned 7b1f4a7 and tag v4.0.0 → sha256 4524ed61… (identical to retained); pinned 5f327015 and branch main → e8ce828a… (identical to retained); tag v3.0.1 → sha256 `7c93bf9e88f1d495ffdbaf860fd9d6a5e75db9550a38ecbd44c6b53dfb2dbf22`, 2389 B, 0 dot-pattern lines, 3 `.github` lines (consistent with the entry's 2026-10-19 numbers; not decided).
- Base anchors: read-only `git show cb807bc:<path>`; commit cb807bc exists. Current anchors read from the working tree (HEAD 97404de).
- Tooling: nothing installed or updated. Used python3 stdlib (gzip, hashlib, urllib, re, subprocess), read-only git plumbing (rev-parse, cat-file, show), and five public GETs of `raw.githubusercontent.com` action.yml (pinned 7b1f4a7, pinned 5f327015, tags v4.0.0 and v3.0.1, branch main). Nothing written except this report; no /tmp; no builds, tests or linters; no delegation; no round-24 material read.

## Verification gaps

- No v3.0.1 bytes retained: four statements UNVERIFIABLE.
- "current" and "main" judged by action.yml content identity, not commit-HEAD identity.
- GNU tar repro outcome not re-run (S008 pair).
- Cross-file anchors checked against the working tree; other lanes' uncommitted edits could shift them again.
- Deployed payload and public /CNAME not probed, per bounds.

```json
{"pair":"S001xghp-served-set","statements":28,"hold":21,"stale":3,"unverifiable":4,"corrections":["[r26-recheck S001 STALE] Anchor refresh for the r20 refinement at lines 14-17 (content unchanged). The cited corpus/README.md lines moved after base cb807bc. At the r26 tree the checkout-membership refinement sits at corpus/README.md:28 (Sitemap/orphan audit row; was :26) and corpus/README.md:59-62 (Live-only orphan paths bullet; was :52-55). The S001 exclusion facts in the Claim and Source checks sections are unchanged.","[r26-recheck S001 STALE] Anchor refresh for SKILL.md:227 cited at lines 14-17 (content unchanged). At base cb807bc that line was the URL lists (sitemap) row. At the r26 tree that row, carrying the r20 correction, is SKILL.md:229; SKILL.md:227 is now the Byte-twin copies row.","[r26-recheck S001 STALE] Anchor refresh for corpus/knowledge/sitemap-orphan-audit.md:20-30 cited at lines 14-17 (content unchanged). The GHP live-only orphan section moved by +4 lines: the checkout-as-deployed paragraph now spans corpus/knowledge/sitemap-orphan-audit.md:24-34, and the sentence 'the live tree IS the last-pushed origin/main' is at :32 (was :28), outside the cited 20-30 range as it reads at the r26 tree."]}
```
