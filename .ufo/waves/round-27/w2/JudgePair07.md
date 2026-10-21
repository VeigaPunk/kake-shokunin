# JudgePair07 — (S005, corpus/knowledge/sitemap-orphan-audit.md), STALE kind=artifact

Seat: KakeR27.JudgePair07 (author-side reviewer, read-only, leaf, no dispatch). Axis: **freshness**.
Milestone: r27-fresh-falsification. Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (base
`83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`, declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`). Only write: this
report; scratch `/fast/scratch/hyaku/kake-r27/JudgePair07/`. No source/ledger/state/Git edit, no build/lint/test, no tool
installed, no network. Author-side evidence — a verdict here is a recommendation, not an admission.

## 1. Attacked item (exact)
`.ufo/waves/round-27/pairs.json:80-89` (candidate blob sha256 `f1fa20cab67053fea3945330d14efa59f095ede22b6dacbb058d688d0b376a6a`):
`{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"artifact","verdict":"STALE",
"evidence":".ufo/round-20/resume/citation-disposition.json",
"contains":"\"supersededClaim\": \"Each deployment snapshots the entire checked-out tree.\"", ...}`

Citing sentence — `corpus/knowledge/sitemap-orphan-audit.md:2` (front-matter `verified-at:`), unchanged from base:
"verified-at: 2026-09-28 (...; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; no live sitemap or domain fetch this round".
S005 enters only by expanding the `S001-S006` range. Appended correction: candidate lines 150–174 (`[r27-recheck S005 STALE]`), marker count **1**.

## 2. Verdict on the attack
**CONFIRM the STALE at its own scope, as a partial attribution correction only.** Re-derived from committed bytes, not reviewer prose:
- Artifact `.ufo/round-20/resume/citation-disposition.json` (sha256 `d3f33e0b75ba63dde82b0d685bb2b97e5d7f07c14a7bf89ad998dd487c8c56b6`, **byte-identical base→candidate**) holds **all 8** platformCorrections for this file (:14,:18,:21,:25,:28,:32,:38,:112). Parsed sources arrays are exactly `{S001,S004}` ×6 and `{S001,S002,S004,S006}` ×2. **S005 appears in none.**
- `corpus/lessons/round-20.md:261` (A2, the mechanism group naming `sitemap-orphan-audit.md:20-24`) lists C3 = S001/S002/S003/S004/S006/S008 — omits S005. :262 (A3, CNAME mistake) names only publish-channels.md:9 and SKILL.md:16.
- The file contains **0** occurrences of `CNAME`/`custom domain` — S005's scope is topically disjoint from this entry.
- The band's S005 attribution was false **at base** (band authored r21 `df6196b`; base blob sha256 `553ad100…` has 0 literal S005), so base `corpus/QUALITY.md:217-221` ("a statement whose attribution was false even at its base revision is STALE") licenses it independently of any r27-added text.
- Date `2026-10-19`, base `cb807bc` and the historical-not-live-reverified marker are untouched; the appended block says so.
- Prefix preserved: `git diff base..candidate` on this file shows **additions only** at 150–174 (149 base lines intact).
- `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a7472d945a6d7ff135e4d7f07b0b6913d835` → exit **1** (strict, expected: C1 unprovable). stdout: citingPairs 58, reviewedPairs 58, decided 55, missing 3 (S001/ghp-served-set, S007/ghp-custom-domain, S033/static-canonical-preflight — all `carried_unverifiable`), findings = 3 `carried_unverifiable`; my outcome row: `{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","verdict":"STALE","valid":true}`.

**Dissent addressed (min/max-band reading — the strongest attack).** If `S001-S006` were a min–max interval whose endpoints are min/max of the truly-cited rows {S001,S002,S004,S006}, S005 would never be asserted and the row would be HOLD with no append. I judge the enumeration reading better supported — the *same file*, same r21 commit, carries the exact set twice (line 1 "S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections"; r26 line 149 "cite S001, S002, S004 and S006 (lines 120-127)"), and the band's qualifier "quote corrections" attributes grounding rows, unlike `publish-channels.md:2` "S001-S007 opened that day" (a date/open-batch scope). But no corpus rule defines band notation (CORPUS.md: none; base QUALITY.md: none), so the verdict rests on the file's own paired enumerations, not a stated convention — which is why the alternative must stay retained. It is, in both reviews and in the citing file (lines 169-170). Substance unchanged; F2/F4 record what the ledger still omits.

## 3. Findings
**F1 (medium) — the artifact anchor does not bind the premise the verdict rests on.** `contains` = `"supersededClaim": "Each deployment snapshots the entire checked-out tree."` — the *claim text* of the :21 record, also the text of the citing file's own corrected line 21. The premise of the STALE is the **absence of S005 from the `sources` arrays of all 8 records**, and that string is not inside the anchored substring. Probe (expected before running: an anchor binding S005's role must fail once S005 is inserted into that record's sources; actual): mutating the :21 record's sources to add "S005" leaves the anchored substring **present** (True → True), so `count_c1`'s substring test cannot detect it. A stronger, already-authored anchor existed: Pair07A §8a's own artifact alternative included the `sources` array in `contains`; that one **is** discriminating (present in original True, absent after the same mutation False). The ledger dropped it. Effect: a reviewer following only `evidence`+`contains` lands on a superseded-claim quote, not the source-set evidence. The verdict itself is confirmed (the reason text and citing-file correction carry the premise, and I verified the full record set myself). Remedy for L1: strengthen `contains` to include the `sources` array of at least one sitemap record, or cite a substring enumerating the eight records' source sets. Ledger-only edit, no corpus change.

**F2 (low) — the S003-vs-S005 asymmetry inside one band is real but unexplained in this row.** Same band, same line, opposite verdicts (S003/sitemap HOLD, S005/sitemap STALE). Defensible: A2 (r20 lesson :261) names this entry's misconception and includes S003, so S003 has affirmative linkage; S005 has none (A2 omits it, A3 assigns it elsewhere). But the S005 reason does not state the discriminating principle, and the S003/S005 band is where a reader will look; the argument currently lives only in the S003 row's reason. Cross-referencing A2/A3 in the S005 reason (and appended block) removes the "arbitrary split" reading without changing any verdict.

**F3 (low) — registry routing lists a file whose S005 attribution the round judged STALE.** `corpus/SOURCES.md:13` used-by (candidate) includes `corpus/knowledge/sitemap-orphan-audit.md` for S005. Defensible: CORPUS.md defines used-by as "paths … citing the row" (the file does cite S005), and the round-27 lesson says routing includes "rejected-attribution discussions, not an assertion that every use is admitted platform support". But the registry cell alone reads as support; the disclosure lives only in the lesson and pairs.json reasons.

**F4 (informational) — the most on-point rule text was added by this same candidate commit.** `corpus/QUALITY.md` r27 (candidate, +47 lines) supplies "Incorrect source-set attribution in a metadata band is a separate question: name precisely which part is corrected, keep the dated observation, and retain reasonable dissent" — the exact rule this verdict applies. The verdict does **not** depend on it: base QUALITY.md:217-221 already makes a false-at-base attribution STALE, and the appended text complies anyway (names the part, keeps date/base, retains dissent). Stated so the L1 does not treat newly added text as independent authority for a verdict committed in the same commit.

## 4. Sibling rows re-checked because they bear on this pair
- **S005/preflight** (source kind, STALE): quote "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created" — present in retained `fetched/text/S005-1.txt` (2 occurrences: apex + subdomain step 4, matching the anchor), 15 words, **row-specific** (absent from other fetched texts). That band is a *body* recommendation, not metadata, so its STALE is better anchored than the sitemap one — a difference the S005/sitemap reason omits.
- **S004/ghp-served-set** override (source kind, STALE; the one `carriedPairOverrideReviews` entry): the locator correction ("steps 4-5 upload static files and deploy the artifact" belongs to S003, not S004) is **independently confirmed from retained public text** — S003-1.txt contains "The general flow of a workflow is to: … upload the static files as an artifact … deploy the artifact"; S004-1.txt has 0 occurrences of "upload static files"/"deploy the artifact" and no "general flow of a workflow". The override retains the old r26 review/units: `git diff base..candidate -- .ufo/waves/round-26/` is **empty**.
- **S005 source freshness**: manifest row S005/1 = HTTP 200, fetchedAt 2026-10-21T19:59:56Z, receivedSha256 `6f3d1ad2…` (240439 B) vs retained sha256 `854c3466…` (14700 B) — HTML retained as visible text only; the verdict is about attribution, not source drift, so no live re-open was required or claimed.

## 5. Residual risk / verification gaps
- The band convention is unstated corpus-wide, so a future round could reopen the min/max reading and reverse this row. The retained alternative plus the file's own two enumerations are the current defence; a one-line band rule in CORPUS.md would close the ambiguity for all five band occurrences.
- I did not re-open the S005 URL myself (lane discipline: r27 retained bytes + manifest are the evidence; a re-fetch would re-confirm source freshness, not the attribution question). The retained S005-1 text suffices for the sibling checks above.
- No r24 stopped work read, retried, rephrased or rerouted; no policy-stop encounter; no tool install; no pacman transaction (paused host-wide); no network fetch by this seat.

## 6. Recommendation
Admit the `(S005, corpus/knowledge/sitemap-orphan-audit.md)` STALE artifact row **as written in verdict and scope** (partial attribution correction only; date/base preserved; dissent retained). Take **F1** as a ledger-only strengthening of `contains` (or an added artifact anchor carrying the `sources` arrays), **F2** as a reason-text cross-reference to A2/A3, and **F3/F4** as disclosures, not edits. No corpus source edit, no rewrite of the r26 ledger, no change to the 55/58 strict count, no admission claim.

Report: .ufo/waves/round-27/w2/JudgePair07.md
