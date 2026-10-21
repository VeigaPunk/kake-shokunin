# JudgePair17 — r27 fresh falsification of (S013, corpus/knowledge/ghp-served-set.md)

Seat: KakeR27.JudgePair17 (reviewer, leaf, read-only). Axis judged: **freshness**. Milestone: r27-fresh-falsification.
Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (verified `git rev-parse HEAD` = same). Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`. Declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
No source/ledger/docs edits; no commits; no installs. Scratch only under `/fast/scratch/hyaku/kake-r27/JudgePair17/`.

## Attacked item

`.ufo/waves/round-27/pairs.json` row: `{"row":"S013","file":"corpus/knowledge/ghp-served-set.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/w2/Rejection07S013.md","contains":"It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness.",...}`.

## Independent expected results declared before running

- E1: HOLD is right iff (a) ghp-served-set.md makes **no** source-row-S013 attribution (else STALE/UNVERIFIABLE), and (b) the cited artifact exists at candidate and genuinely bears on this file's S013 token.
- E2: the `contains` witness must be a sentence whose **referent is ghp-served-set.md**; a witness scoped to another entry is scope-shifted.
- E3: the pair must be exactly one obligation, and its recorded discovery rationale must be true **at the measured revision**.
- E4 (dissent): S004→S003 locator correction must be true of retained r27 bytes; S003-vs-S005 sitemap split must be evidence-driven.

## Probes, commands and results

**P1 (E1) — is S013 a source attribution in this file?**
`git show ac46a74:corpus/knowledge/ghp-served-set.md | head -1` → `source: S001, S002, S003, S004, S006, S008 (corpus/SOURCES.md) — …upload-pages-artifact…` (no S013). Base blob `95bfdd1d…` at candidate = worktree. S013 occurrences at base: **one**, embedded in the filename `w2/Rejection07S013.md` at base line 95. `grep -c` base = 0 word-boundary hits; wide scan = 1. → E1(a) confirmed: no S013 attribution exists. Also `corpus/SOURCES.md` S013 row `used-by` = `corpus/knowledge/crawl-scope-per-host.md` only. **No S013 claim to be stale → HOLD direction survives.**

**P2 (E1b) — does the artifact exist and bear on this token?**
`git rev-parse ac46a74:.ufo/waves/round-26/w2/Rejection07S013.md` → `59fca3d14294c156e9837e93b138932832f3b689` (= worktree blob); sha256 `c31e10a4a523b4d661f7c26b7634f88429d0677407603bd35db4328f4c446fa1`. Target line: `- Target: .ufo/waves/round-26/statements.json:128-136 (row S013, \`crawl-scope-per-host.md\`)`. The token is a report-name label for **row S013 of a different file**. `contains` substring count in the artifact = **1**. → E1(b) confirmed; the artifact is the right historical artifact for the token's provenance.

**P3 (E2) — scope of the quoted witness.** Artifact line 70 (Low-severity observation #2, "Copied boilerplate provenance") reads in full: the "(S008 via `manifest-retry.json`)" wording "…but **this entry** cites only S011, S012 and S013. The same wording appears in 5 knowledge files (… crawl-scope-per-host, ghp-custom-domain, ghp-etag-anatomy, **ghp-served-set**, static-canonical-preflight). It is true of the round but **irrelevant to this entry**." "this entry" = crawl-scope-per-host.md (the report's Target). ghp-served-set.md is only *enumerated* among copies, never adjudicated. → **E2 falsified: the recorded witness is scope-shifted.** See F1.

**P4 (E1 corroboration — the file's own sentence).** Candidate line 95: 'The words "S008 via `manifest-retry.json`" in the recheck paragraph name the round's retry, not a source of this entry (w2/Rejection01S001.md, w2/Rejection07S013.md).' Candidate line 83 confirms the parenthetical describes S008's own fetch: "Rows S001…S008 were re-fetched by one public GET each (`…/fetched/manifest.json`, S008 via `manifest-retry.json`)". `.ufo/waves/round-26/fetched/manifest-retry.json` contains exactly **one** row: S008, attempt 2, HTTP 200, sha256 `93281a63…`. ghp-served-set.md cites S008 as a subject source (line 1; bullet line 34; erratum lines 73-79). → in **this** file the parenthetical is *not* irrelevant boilerplate; it is true provenance for a subject row. Confirms F1.

**P5 (E3) — obligation identity and discovery rationale at the measured revision.**
`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a747…` → `citingPairs 58, reviewedPairs 58, decided 55, r26CarriedPairs 41, newDecided 18, knownUnverifiableUnits 7, knownUnverifiablePairs 3, unreviewed []`, `missing` = S001×ghp-served-set / S007×ghp-custom-domain / S033×static-canonical-preflight (all `carried_unverifiable`), S013 outcome `{'verdict':'HOLD','valid':True}`. Counter exit 0.
My own independent scan (fresh script, frozen grammar `\bS(\d{3,})\b` + range expansion, blobs via `git show`): base = **57**, candidate = **58**, delta = **exactly** `(S013, corpus/knowledge/ghp-served-set.md)`. Independent base wide-vs-word-boundary scan: word-boundary 47, wide 48, wide-only = exactly that one pair. → obligation identity confirmed, no silent additions, no duplicates.
But at candidate the file's own r27 append adds two standalone word-boundary `S013` tokens (candidate lines 111, 115) — so at the measured revision the pair is a plain literal citation, not embedded-only. → E3 partially falsified; see F2.

**P6 (E3 — gate separation, no false positive).** `python3 -B scripts/citing_set.py --root . --revision <rev> --population .ufo/waves/round-26/population.json --ledger .ufo/waves/round-26/statements.json --json`:
- at base → `citing 57, ledger 41, findings 16` (S013×ghp-served-set **not** among them);
- at candidate → `citing 58, findings 17`, and the 17th **is** `unadjudicated_citing_pair S013 corpus/knowledge/ghp-served-set.md`.
Gate token rule (scripts/citing_set.py:108) is `(?<!\w)S([0-9]{3,})(?!\w)` → cannot see `Rejection07S013.md`. `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a747…` → `expected 16, detected 16, falsePositive 0, passed true, gateExit 1` (gate pinned to `frozenRevision 83528f7c…`, citing 57). → C2 stays exactly 16/16; the base↔candidate citing-set delta is exactly this one pair.

**P7 (E4, dissent — S004 ghp steps).** From retained r27 bytes: `S003-1.public.txt.gz` contains "upload the static files" ×1 and "deploy the artifact" ×1 inside "Creating a custom GitHub Actions workflow to publish your site … The general flow of a workflow is to: …"; `S004-1.public.txt.gz` contains neither, and contains "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." under "Configuring the upload-pages-artifact action". → the S004→S003 locator correction is **true of the retained bytes**; `[r27-recheck S004 STALE]` present at candidate line 99. This is exactly the r26 leder's `S008 × ghp-served-set.md` row being *overridden* (count_c1 `decided.discard(key)` then re-add) — no rewrite of r26 units.

**P8 (E4, dissent — S005 preflight).** S005 quote in pairs.json = "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created" — present in retained S005 text (count 2), row-specific (absent from every other row's view), 15 words / 15 tokens (within ≤25 / ≥6). Marker `[r27-recheck S005 STALE]` present at candidate static-canonical-preflight.md:235; the r27 table (lines 229-241) gives per-row HOLD/STALE with reasons and "no CNAME servedness conclusion follows". STALE is an attribution-overreach finding, not source drift — consistent with the contract definition and with the corpus wording.

**P9 (E4, dissent — S003/S005 sitemap).** S003 × sitemap-orphan-audit HOLD rests on A2 in `corpus/lessons/round-20.md:261`, whose Fix cell contains byte-exactly "C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`; annotate `round-7.md` append-only" (count 1) and whose Evidence cell names `corpus/knowledge/sitemap-orphan-audit.md:20-24`; S005 × sitemap STALE rests on `.ufo/round-20/resume/citation-disposition.json` (`"supersededClaim": "Each deployment snapshots the entire checked-out tree."`, present). The split is evidence-driven: A2's set contains S003 but not S005 (S005 appears only in A3, which targets ghp-custom-domain) — the corpus note at candidate lines 163-168 states this. Pair03B's contrary "never linked" conclusion and Pair03A's contextual reading are both disclosed in the file (lines 158-162) and in the ledger reason ("Ambiguity and dissent retained"). → no undisclosed dissent found.

## Findings by severity

**F1 — MEDIUM — ledger `contains` witness for the S013 row is transplanted out of its referent scope, and reads false in this file's scope.** The witness sentence's "this entry" is crawl-scope-per-host.md (the artifact's Target); it is the artifact's conclusion that the S008 parenthetical is *irrelevant* because that entry cites only S011/S012/S013. In ghp-served-set.md, S008 **is** a subject source row (source: line 1; bullet :34; erratum :73-79) and the parenthetical is true provenance for it (manifest-retry.json's sole row is S008). The r27 S008 rows show the author knew this ("The named subject rows exclude S008" — for the four files where it holds; ghp-served-set.md is deliberately absent). The S013 row nevertheless records the opposite assertion for this file. The on-point witness, also present in the same artifact (count 1) and proposed by w1/CritFailOpen.md, is "row S013, `crawl-scope-per-host.md`" — it names the other entry and so states the true referent. Impact: ledger provenance precision; the HOLD verdict, the artifact identity and the byte-level `contains` check are unaffected (count_c1 outcome valid=True); no corpus byte is wrong. Smallest fix: replace `contains` with the Target-line witness, or reword the ledger reason to say explicitly that the artifact's "irrelevant to this entry" finding is scoped to crawl-scope-per-host.md and is not asserted for ghp-served-set.md.

**F2 — LOW/MEDIUM — the recorded discovery rationale is base-scoped while the measured revision is candidate-scoped.** `discovered-pairs.json` and `pairs.json` both describe the obligation as an *embedded / embedded-only* evidence-report filename token ("Broad S[digits] sweep of all26 baseline knowledge files found this sole embedded-only pair beyond frozen57"; "embedded evidence-report filename at old line95"). That is true of the base tree (base: 0 word-boundary S013 hits; the sole wide-only pair). At the candidate the r27 correction prose itself introduces two standalone word-boundary `S013` tokens (lines 111, 115), so the pair is at candidate an ordinary literal citation created by its own correction. No counter effect (C1 = 58 either way; C2 = 16/16 because c2_count pins the gate to base); disclosure-only, but the "embedded-only" characterization should not be carried into the candidate-scoped ledger as if still current.

**F3 — LOW — self-referential under-description in the r27 corpus note.** Candidate line 111 says "S013 occurs inside the evidence-report filename at line95". True, but at the candidate the token also occurs at lines 111 and 115 (the note's own prose). A reader auditing "where does S013 occur in this file" at the measured revision gets three sites, not one. Not a false statement; no correction required beyond noting it.

**F4 — INFO — no S008×ghp-served-set.md row exists in r27 pairs.json, correctly.** S008 × ghp-served-set.md remains the r26 carried pair (12 statements, HOLD, real GNU-tar quotes at :34 and erratum :73-79). The r27 S008 artifact rows cover only the four files where S008 is not a subject row. Consistent with P4; no missing obligation found.

## Verdict on the attacked item

**HOLD (kind=artifact) is confirmed at its own scope** — E1 and E2(E1b) both pass: ghp-served-set.md makes no S013 source attribution, the cited artifact is the genuine historical artifact naming that token, and the `contains` substring is present and unique. The HOLD is not a quote/marker/pair-count substitute: the semantic reason (a report-name label, not a source claim) is independently reproducible from the file's own source line and body.
Residual: F1 (scope-shifted witness) and F2 (base-scoped rationale) are ledger-precision defects, not verdict defects. No STALE, no UNVERIFIABLE, no missing obligation, no duplicate found; the C1/C2 separation holds (C1 58 reviewed / 55 strictly decided; C2 exactly 16/16, 0 false positives).

## Verification gaps

- I did not execute any network fetch; all source claims rest on bytes already committed at the candidate (r26 retained fetch bytes, r27 retained fetch bytes, committed reports).
- I did not run the fixture suite, `count_c1.py --selftest`, `c2_count.py --selftest`, or the mutation probes (other seats' scope); my counter/gate runs were measurement only.
- F1's remedy is a ledger-wording choice, not a factual open question: both candidate witnesses are present in the artifact, so no source byte can settle which the L1 prefers.
- The r26 S008×ghp-served-set.md statement set (12 statements, file was 79 lines at that review) predates candidate lines 83/95; I did not audit whether the r26 statement window should have been extended to them — that is the S008 pair's seat's scope, not this pair's.

## Tooling

No tools installed or upgraded; no pacman/uv/cargo/npm action. Commands used: `git` (rev-parse, show, ls-tree, log, cat-file, hash-object), `bash`, `read`, `grep`, `python3` (stdlib only, in-memory) for the pair enumerations, the `contains`-witness byte checks, the retained-bytes quote/anchor checks and the counter/gate invocations. Scratch written only under `/fast/scratch/hyaku/kake-r27/JudgePair17/`. No source, docs, registry, manifest or fleet writes. No /tmp or /dev/shm use.

Report: .ufo/waves/round-27/w2/JudgePair17.md
