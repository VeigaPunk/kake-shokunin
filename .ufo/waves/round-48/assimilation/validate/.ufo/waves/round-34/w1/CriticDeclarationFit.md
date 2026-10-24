# KakeR34.CriticDeclarationFit — round-34 declaration fit (wave 1)

Scope: SCORECARD.md "Round 34 — declared claims" at d08d8de26c9a4290c44282b0eee2b860e8ea4ecc (SCORECARD lines 1192-1238), counters and matrix at that commit, receipts at a2fe31b2. Advisory only; no verdict.
Sandbox: /fast/scratch/hyaku/kake-r34/w1/CriticDeclarationFit/ (clone at a2fe31b2; branches hollow-c2, lookup-c1). No tools installed. No network except `git ls-remote` of the public ds4cc-marketplace repo.

## Commands (all exit codes observed)
- `git log -1 --format='%H %cI %aI' d08d8de…` → exit 0: committer 2026-10-22T18:00:16-03:00 (21:00:16Z), author 17:52:08-03:00 (20:52:08Z).
- `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD refs/heads/main` → exit 0: both 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884.
- `python3 -B <lane>/.ufo/waves/round-34/c2_source_census.py --root clone --revision hollow-c2` (0cce15f0) → exit 0, `met 5/5`, controlBroken false. Output: sandbox `c2-hollow.json` sha256 a473147f…0c72.
- `python3 -B <lane>/.ufo/waves/round-34/c1_matrix_count.py --root clone --revision lookup-c1` (dcef39b5) → exit 0, `28/28`, constantGatesAllRejected true (6/28, 0/28, 6/28, 1/28). Output: `c1-lookup.json` sha256 98ca70f6…db73; tool sha256 a2e274c0…30ec.
- The same lookup tool on a fresh page with no Open Graph tags → stdout `{"verdict": "clean", …}`, exit 0.
- Builder: sandbox `make_hollow.py` (modes c2, c1). The first lookup build scored 0/28 because of a bug of mine (JSON `null` embedded in Python source). I fixed it and rebuilt; only the rebuilt commit's run is cited.

## Findings
1. **HIGH — C2 after-value is reachable with no study (trivial baseline).** Hollow commit 0cce15f0 scores `met 5/5`. It adds four junk registry rows (`| S067 | junk <receipt url> | x | … | mined | 2026-10-22 | x | x |`), an entry made of 8 filler lines, one line of four ids, and a census line copied from the committed before-receipt `verification/c2-at-d08d8de.json` (`census.derived`: pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87). Its Gate quotes are the first six words of each retained text, e.g. S067 “The Open Graph protocol The Open”, S069 “Slack Robots | Slack Go to”.
   - The census clause is defined as "equals the counter's recount", and the counter prints that recount even when the clause fails (c2_source_census.py:243). Once a2fe31b landed the receipt, the answer was in committed bytes.
   - "Junk row with copied metrics" is round-33 routed defect 1 (round-33-verifier-spotcheck.md:186-191). It is still accepted, and the declaration does not name it as carried open.
   - Impacted axes: freshness, calibration.
   - Smallest correction: the closure re-measures C2 by reading the entry's prose against S067-S070, as round 33 did ("necessary but not sufficient", spotcheck:109-110), and the round report states that 5/5 is a floor, not proof.
2. **HIGH — C1 after-value is reachable without the capability.** The tool at dcef39b5 hashes the case directory plus argv, then replays the matrix's frozen expected answer. It never parses HTML (the only "og:" text in the file is inside the replayed answer table). It scores 28/28 with all four constant gates rejected, yet calls a tag-less page clean.
   - The matrix publishes every input and expected output, and the declaration has no held-out or real-input case. So "28/28" plus "constants rejected" cannot tell a tool from a memorized table.
   - The declared after-value also adds "a capability row enters" (SCORECARD:1211), and AXES §Capabilities lets a row in only when the capability is shown running. The round-29 row cites a real-input run (SCORECARD:194); round 34 commits to none.
   - Impacted axes: operability (capability entry), calibration.
   - Smallest correction: before the row enters, require one real-input run over the retained ds4cc bytes (102 pages, URLs `https://ds4cc.com/<path>`). Its per-property `og_required_missing` counts must equal 102 minus the C2 recount (og:image 101; og:title, og:type and og:url 15 each). The C2 recount is an independent committed oracle, and the lookup tool fails it.
3. **MEDIUM — Sources cited for the canonical-equality rule do not state it.** The claim cites (S067, S068) for "og:url differs from the page's canonical link".
   - S067 says "og:url - The canonical URL of your object that will be used as its permanent ID in the graph". S068 says "og:url The canonical URL for your page. This should be the undecorated URL…".
   - Neither retained text mentions a `<link rel=canonical>` element (grep `rel="?canonical` over S067.txt and S068.txt finds nothing). Equality with the link element is the lane's inference.
   - S068 also says "If you don't specify a type,the default is website", which weakens treating a missing og:type as a defect for Facebook. The declaration does not disclose this.
   - The `og_url_not_absolute` rule cites no source, and none of S067/S068 contains "absolute".
   - Impacted axes: freshness (provenance), calibration.
   - Correction: mark canonical equality and absoluteness as lane policy, not sourced; disclose the S068 og:type default in the C2 entry.
4. **MEDIUM — Universal clause "network-free" is not measured.** c1_matrix_count.py:115-119 runs the tool with a minimal environment but no network isolation, so a fetching tool passes. Impacted axis: operability. Correction: state it as unmeasured, or have the closure run the tool under `unshare -rn` (an unprivileged network namespace) once.
5. **LOW/MEDIUM — C2's freshness label has no drift component.**
   - AXES freshness means re-verifying skill claims against live surfaces and flagging stale ones. C2 adds first-opened sources plus a census of the pin round 33 already set; that pin is still upstream HEAD (ls-remote above). Nothing stale is re-verified.
   - It fits depth or coverage better. Precedent exists: rounds 29-31 labelled frontier learning claims as freshness (SCORECARD:626, 690, 834).
   - This is a tradeoff for the judge, not a fixable counter defect. Impacted axes: freshness, calibration.
6. **LOW — C1 after-value is not a single value from one command.** The second clause ("a capability row enters `## Capabilities`") is not read by the named counter (it reads only `passed` and `constantGatesAllRejected`). C2's after-value (met 5/5, controlBroken false) is single and re-derivable by its command over committed bytes. Correction: count the row with a separate grep, or drop it from the after cell.
7. **LOW — Screening and timing.**
   - Source receipts were accessed 20:57:39Z-20:57:42Z, after the commit's author time (20:52:08Z) and before its committer time (21:00:16Z). The commit was rewritten after the sources were fetched; the declaration's own text ("opened at 20:57Z") shows this.
   - The declaration takes committer time as its time, and that is set by the author with no outside anchor.
   - The disclosed screening (87 openings per og property, 1 og:image) did give the L1 the census before declaring. Because C2's target is "equals recount", that knowledge does not make C2 easier than finding 1 already makes it. For C1, reading the source phrases before freezing the matrix is inherent to frozen-matrix design and is disclosed.
   - fetcherSha256 eaf37076… equals the committed fetch_sources.py; matrix sha 246a6a3b… equals the pin.
   - No defect beyond disclosure. Impacted axis: calibration.
8. **LOW — Round-33 routed defect 3 (log Gate rejects) is not bound by any count.** S071 and S072 are screened rejection candidates, but C2 counts only the S067-S070 admits. Correction: carry it explicitly in the round-34 lesson.
9. **PASS — structure.** Two claims on distinct axes (operability, freshness). The stagnation nudge applies (saturation 10/10, window N=1, SCORECARD:216-221; round 33 entered no capability, SCORECARD:1129). Capability is claimable in form, but see finding 2. Separability holds: the C2 recount uses its own parser, never the C1 tool.

## Not verified
- I did not run the C1 real-input check from finding 2 against an honest tool (none exists yet).
- I did not run the tool under network isolation.
- I did not read S069 or S070 beyond confirming that they mention Open Graph (S069 "Twitter Card / Open Graph tags"; S070 "generated using OpenGraph tags").
- I did not check any landed tool or entry (none is at a2fe31b2).
