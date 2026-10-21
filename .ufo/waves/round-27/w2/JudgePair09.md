# JudgePair09 — falsification of (S006, corpus/knowledge/publish-channels.md), proposed HOLD kind=artifact

Seat: KakeR27.JudgePair09 (reviewer, read-only, leaf; no subagent dispatch). Axis: freshness. Milestone: r27-fresh-falsification.
Authority: frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate; `git diff --name-only ac46a747…` empty → working tree == candidate for tracked files; only untracked `.ufo/waves/round-27/w2*` + `__pycache__` present). Repo `/home/vgpnk/Projects/shokunin/kake-shokunin`. No source/ledger/Git/manifest write; only this report + scratch under `/fast/scratch/hyaku/kake-r27/JudgePair09/`.

## 1. Exact attacked item

`.ufo/waves/round-27/pairs.json` pair: `row=S006`, `file=corpus/knowledge/publish-channels.md`, `kind=artifact`, `verdict=HOLD`, `evidence=corpus/SOURCES.md`, `contains="| S006 | GitHub Docs: About GitHub Pages and Jekyll — https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll | docs | A | Default file exclusions in GitHub Pages Jekyll branch builds | Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19 | By default Jekyll skips paths starting with underscore, dot, or hash, paths ending in tilde, node_modules, and vendor | mined | 2026-10-19 | 90d |"`, `reason="Historical opened-date metadata only: 2026-10-19 for the r20 opened batch. The registry and historical lesson records agree. The date/range is not a claim that this row supports every body correction and is not relabelled a fresh r27 source observation."`, reviews `w1/Pair09A.md`, `w1/Pair09B.md`.

## 2. Independent expected results declared before each probe

- **E1** the pair is a real r27 obligation: `count_c1.py` at base `83528f7` lists it missing; at candidate it is decided.
- **E2** the citing site is a *date* band, not a support attribution: literal `S006` absent from the file; only the range `S001-S007` (line 2) covers S006.
- **E3** the band predicate ("opened that day" = 2026-10-19) is literally true for every row the range spans, at the candidate revision.
- **E4** the entry asserts no substantive S006 support (its support set is enumerated at line 1 and line 84 and excludes S006; r26 ledger has five publish-channels rows S001/S002/S003/S005/S007 and no S006) ⇒ HOLD at date scope; STALE would require a wrong/unsupported attribution.
- **E5** the artifact binding must be an exact substring of the candidate `corpus/SOURCES.md` blob, and must not silently bind more than the row prefix.
- **E6** the underlying source is live and scope-stable (200 on 2026-10-21; exclusion text unchanged vs the r26 text view).
- **E7** every digest/cell asserted in `w1/Pair09A.md` / `w1/Pair09B.md` must be independently recomputable; unverified assertions are findings, not evidence.

## 3. Probes run (command → exit → key output)

**P1 (E1)** `TMPDIR=/fast/scratch/hyaku/kake-r27/JudgePair09 python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` → exit 0; `citingPairs=57, reviewedPairs=41, decided=38`; missing list contains `{'row':'S006','file':'corpus/knowledge/publish-channels.md'}` (and S004 same file). Same command at `--revision ac46a747…` → exit 0; `citingPairs=58, reviewedPairs=58, decided=55, newDecided=18`, missing = 3 carried-UNVERIFIABLE pairs (S033/preflight, S007/ghp-custom-domain, +1). ⇒ pair is genuine, obligation discharged by this ledger row, not self-declared.

**P2 (E2)** `git show ac46a747…:corpus/knowledge/publish-channels.md | grep -oE 'S[0-9]{3}' | sort | uniq -c` → `6 S001, 5 S002, 5 S003, 5 S005, 5 S007, 1 S019` — **no S006 token**. `grep -nE 'S[0-9]{3}'` → sites only lines 1, 2, 58, 59, 60, 61, 84; line 2 = `verified-at: … round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed`. `grep -n '006|S6|[Jj]ekyll'` → none. ⇒ only occurrence = range expansion at line 2.

**P3 (E3)** `git show ac46a747…:corpus/SOURCES.md | sed -n '9,15p'` → rows S001–S007 all carry `| mined | 2026-10-19 |` in the `opened` column (S001 `on-release`, S002–S007 `90d`). Row S006 (line 14) `opened` = `2026-10-19`, identical at base `83528f7`; row created by `02b6dd0 2026-10-19 19:38:03 -0300`. `.ufo/round-20/resume/sources-gate.md` → `## S006 — About GitHub Pages and Jekyll … - Accessed: 2026-10-19`. `corpus/lessons/round-20.md:208` → S006 row `fetched 2026-10-19`. ⇒ the premise is literally true; no stale date.

**P4 (E4)** Candidate file line 1 = `source: S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections …`; line 84 = `The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61)`. `.ufo/waves/round-26/statements.json` (41 pairs) → publish-channels rows S001,S002,S003,S005,S007 only; its S006 pairs are `ghp-served-set.md`, `sitemap-orphan-audit.md`. ⇒ no substantive S006 attribution at this site ⇒ HOLD at the site’s own stated (date) scope is correct; a STALE verdict would need a wrong attribution, and none exists at that scope.

**P5 (E5)** Python check against `git show ac46a747…:corpus/SOURCES.md`: ledger `contains` occurs **exactly 1×** and is a literal prefix of row 14; the binding stops before the `used-by` cell (row 14 tail = `corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md |`). ⇒ binding is exact and does not over-bind; the used-by cell is deliberately unbound.

**P6 (E6)** `.ufo/waves/round-27/fetched/manifest.json` row S006: `status 200`, `fetchedAt 2026-10-21T19:59:56Z`, `file S006-1.public.txt.gz`, `bytes 7676`, `sha256 535e55d0fb1154f0fb86de1d070abebc49c75c2e8f7845c547f8d61626806910`, `receivedSha256 f0318abe…742b6`, `receivedBytes 138096`, `retainedRepresentation.kind=public_visible_text`, `rawHttpBodyRetained=false`. Recomputed: `sha256(.ufo/waves/round-27/fetched/text/S006-1.txt)=535e55d0…`, decompressed-gz same. `difflib` r26 text (`2d953b39…`, 7676) vs r27 text (7675) ⇒ single trailing-newline deletion, no substantive change. Exclusion text present verbatim: `By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~`. `.ufo/waves/round-26/rechecks/S006.json` = HOLD on the same quote. ⇒ source live and scope-stable; recheck cadence 90d from 2026-10-19 ⇒ not overdue.

**P7 (E7)** recomputed every digest/cell asserted by the two w1 reviews (see findings F1/F2 below).

## 4. Verdict

**HOLD (artifact) confirmed at the pair’s own scope.** The citing site claims only that S001–S007 were *opened* on 2026-10-19; the registry, the r20 sources-gate and the r20 lesson all record that date, so the premise is true and no attribution is made that S006 supports this entry. This is not a quote/marker/pair-count substitute: the bound artifact text is the registry row carrying the date the sentence asserts, and the entry’s two independent support-set enumerations exclude S006.

## 5. Findings by severity

**F1 — Medium (evidence defect in the w1 record, ledger-uncontaminated):** `w1/Pair09A.md` §3 asserts “`corpus/SOURCES.md:14` `used-by` for S006 = `corpus/knowledge/ghp-served-set.md` only”. The candidate blob’s row 14 `used-by` cell lists **five** paths, including `corpus/knowledge/publish-channels.md`. A’s supporting argument (“the registry does not record publish-channels.md as a user of S006”) is therefore false. §4 of A is also wrong on the r27 fetch facts: A cites `file S006-1.raw.gz`, `bytes 138096`, `sha256 f0318abe…`, “recomputed sha256 of the decompressed blob = identical (re-verified)”, and “text view sha256 `2d953b39…` … byte-identical to the r26 text view”. Actual r27 state: `S006-1.public.txt.gz`, `bytes 7676`, retained `sha256 535e55d0…`, `receivedSha256 f0318abe…`/`receivedBytes 138096` (received body ≠ retained public text, per the round-27 retention rule), and the r27 text view is **not** byte-identical to r26’s (7675 vs 7676 chars; one trailing newline). A’s *conclusion* (page substance unchanged) survives my own recomputation (P6), but its recorded digests must not be carried into any ledger `reason`/`quote`. The shipped ledger row is artifact-kind and binds only `corpus/SOURCES.md`, so no contaminated value entered `pairs.json`.

**F2 — Low (registry over-attribution, adjacent file, not this pair):** `corpus/SOURCES.md` S006 `used-by` names `corpus/knowledge/publish-channels.md`, yet that entry never uses S006’s teaching (Jekyll branch-build default exclusions) — the only link is the incidental line-2 range. The same row’s `used-by` claim is accurate for `ghp-served-set.md` (line 30), `sitemap-orphan-audit.md` (lines 122/124) and `static-canonical-preflight.md` (line 233). The registry cell — not this pair’s citing file — is the place where an over-attribution lives; this pair’s binding stops before that cell. Observation for L1; no verdict change, no ledger rewrite.

**F3 — Low (precision, no action required):** the ledger `reason` says “The registry and historical lesson records agree”, true for the opened date (P3) but silent on the registry’s `used-by` cell naming this file; a reader could over-read the agreement as substantive support. Non-binding clarification available for L1 (append-only, in the citing file) — not required by the contract (HOLD needs no `[r27-recheck S0NN STALE]`).

## 6. Dissent addressed (with citations, not restatement)

- **S005 preflight (STALE, `w1/Pair08*`)** — consistent, no contradiction: preflight’s line 54 band is a *content* band (“an assumed checkout served set (S001–S006, `ghp-served-set.md`)”), so over-inclusion of S005 is a misattribution → STALE (candidate file line 235: “The source range at line54 over-includes S005.”). My site’s band predicate is explicitly temporal (“opened that day”), and the entry names its support set twice (lines 1, 84) → different scope class.
- **S005/S003 sitemap (STALE/HOLD)** — consistent: sitemap’s line-2 band reads “r20 S001-S006 **quote corrections** 2026-10-19” (attribution-flavoured) and that file’s line 1 support set omits S005 → S005 STALE there (candidate lines 163-167). My band reads “(**S001-S007 opened that day**)” and the file’s own enumerations exclude S004/S006 → date band, HOLD.
- **S004 ghp steps (STALE override)** — consistent: that is a locator misattribution (candidate `ghp-served-set.md` lines 99-103: “Lines29–30 attribute ‘steps 4-5 upload static files and deploy the artifact’ to S004” → those numbered items are S003’s). My site contains no step reference and no source quotation at all; the ledger binds an opened-date row, so no locator can be mis-attributed here.
- **Same-wave convention check (not a dissent, a consistency test):** the r27 wave itself classifies the *other* date band in the sibling file as date-only (candidate `static-canonical-preflight.md` lines 241-243: “The line2 S020–S027 metadata band records historical opening dates, including S022 and S023, not fresh round27 observations or individual support for …”), and HOLDs S022/S023 as artifact rows with the same reason template. My HOLD is that same treatment, not an isolated leniency.
- **Counterexample “registry `used-by` proves substantive use”** (implied by F2): rejected for this pair — `used-by` is a registry-side usage list, the cited sentence’s own scope is a date, and the entry’s support enumerations contradict substantive use.

## 7. Residual risk / verification gaps

- The 2026-10-19 “opened” date is round-20 self-attestation (registry + sources-gate + lesson + commit timestamp 02b6dd0 2026-10-19 22:38Z); no raw 2026-10-19 fetch bytes are retained for S006. Three independent records agree and none conflicts — adequate for a date-scope HOLD, and disclosed.
- No live re-fetch by this seat (retained r27 bytes only); “live at 2026-10-21T19:59:56Z” rests on the round-27 manifest + recomputed retained digest.
- Review A’s byte-level claims (F1) could not be reproduced as written; I could not determine whether they were computed against the r26 raw artifact and mislabelled — no bearing on the verdict, since the shipped ledger row is artifact-bound to `corpus/SOURCES.md` only.
- Pair-count agreement is not support: E1 was used only to prove the obligation is real, not to justify HOLD.

## 8. Tooling

No install, upgrade, downgrade or service mutation; no pacman transaction (host-wide PAUSED untouched). Tools used: `read`, `bash` (git show, grep, python3 stdlib for digests/difflib), `write` (this report only). Scratch: `/fast/scratch/hyaku/kake-r27/JudgePair09/{c1-base.json,c1-cand.json}`. No network, no account/credential/publication operation; no r24 work read/retried.

Report: .ufo/waves/round-27/w2/JudgePair09.md
