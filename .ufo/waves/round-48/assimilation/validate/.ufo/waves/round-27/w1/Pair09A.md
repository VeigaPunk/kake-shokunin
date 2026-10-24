# Pair09A — r27 C1 adjudication, row S006

Seat: KakeR27.Pair09A (reviewer, read-only findings). Axis: freshness. Scope: **(S006, corpus/knowledge/publish-channels.md)**.
Repo: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations landed `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
No ledger/source/manifest/Git mutation; no subagent dispatched; no network fetch (retained r26/r27 bytes only).

## 1. Verdict

**HOLD**. The pair exists only through one expanded range in the entry's `verified-at:` header. At that site's own stated scope — an *opened-date* provenance statement, not a substantive attribution — the premise is verified true: no stale premise, no `[r27-recheck S006 STALE]` marker required.

## 2. Exact citing site (ranges expanded)

One citing site only, `corpus/knowledge/publish-channels.md:2` (identical in the blob at `be375d9:corpus/knowledge/publish-channels.md`):

```
2:verified-at: 2026-09-26 (kimi-webbridge "not supported on Linux" check) and 2026-09-28 (round-1 commit cd5b381 that introduced this entry; wz1-ds4cc emptied 2026-09-28T21:42-03:00); round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed
```

The hyphen range `S001-S007` expands to S001…S007 and is the **only** source of the S006 occurrence: the literal token `S006` never occurs in the file. S-id tokens occur on lines 1, 2, 58, 59, 60, 61, 84 only; line 2 is the sole range (`grep -nE "S[0-9]{3}[-–—.]"` → line 2 only). Located support from line 2 (7 words): "round-20 corrections 2026-10-19 (S001-S007 opened that day)".

## 3. Scope test of the citing line

The parenthetical's predicate is *"opened that day"* (2026-10-19) — a date, not a support set.

- `corpus/SOURCES.md:14` row S006 `opened` = `2026-10-19`; rows S001–S007 (`:9`–`:15`) all carry `opened = 2026-10-19` → **the range's premise is literally true for S006 and every row it spans.**
- The entry never claims substantive support from S006; the supporting set is enumerated twice, both times *without* S006 — `:1` "S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections"; `:84` (r26 EOF provenance) "The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61)".
- `.ufo/waves/round-26/statements.json` carries exactly five `publish-channels.md` rows (S001, S002, S003, S005, S007) and **no S006 row** → this pair is a new r27 obligation, present in the base missing list.
- `corpus/SOURCES.md:14` `used-by` for S006 = `corpus/knowledge/ghp-served-set.md` only → the registry does not record publish-channels.md as a user of S006, consistent with a metadata-only occurrence.
- S006's scope (`Default file exclusions in GitHub Pages Jekyll branch builds`) is orthogonal to this entry's four r20 correction claims (upload-pages-artifact hidden-file exclusions; repo `CNAME` vs the Pages `cname` setting): no supporting contribution is asserted here, so none is needed.

Inferential step labelled: the HOLD rests on the **SOURCES.md opened-date column plus the entry's own two enumerations**, not on S006's page content. The fetched-page grounding below satisfies the contract's source-kind record fields and independently shows the source live and scope-stable.

## 4. Source evidence (round-27 retained bytes; no re-fetch)

`.ufo/waves/round-27/fetched/manifest.json`, row S006 index 1: status 200, error null, `url` = `finalUrl` = `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll`, `fetchedAt` `2026-10-21T19:59:56.112484+00:00`, bytes 138096, sha256 `f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6`, file `S006-1.raw.gz`, text `text/S006-1.txt`; recomputed sha256 of the decompressed blob = identical (re-verified).

- Primary support quote (24 words, whitespace-normalised substring of `fetched/text/S006-1.txt`): "Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~"
- Anchor: H2 "Configuring Jekyll in your GitHub Pages site" (raw HTML carries `id="configuring-jekyll-in-your-github-pages-site"`); exclusion list between the locked-settings paragraph and the "Front matter" H2; the scope sentence "If you are publishing from a branch" is still present, so S006's recorded scope ("branch builds") is unchanged.
- Cross-round stability: `fetched/text/S006-1.txt` sha256 `2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8` (7677 bytes) is **byte-identical** to the r26 text view; only the raw HTML digest differs (r26 `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd` vs r27 `f0318abe…`, identical content-length 138096) → page-furniture drift, no substantive change.
- r26 corroboration: `.ufo/waves/round-26/rechecks/S006.json` (verdict HOLD, fetchIndex 1, same quote, anchorObserved H2 "Configuring Jekyll in your GitHub Pages site"); r26 manifest row S006 fetchedAt `2026-10-21T15:09:35.317006+00:00`, sha256 `71a698604486380c05ca092adbc863dc653fc175eecea5a675891651cd3bdfbd`.

Artifact evidence (the file carrying the opened-date premise), `corpus/SOURCES.md:14` — exact contains substrings, both verified present: `Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19` and `paths ending in tilde, node_modules, and vendor | mined | 2026-10-19 | 90d | corpus/knowledge/ghp-served-set.md |`

Historical dates preserved as written (2026-09-26 / 2026-09-28 local checks, 2026-10-19 opening and r20 corrections, 2026-10-21 re-fetches). The header's `historical-not-live-reverified` and "no live domain recheck performed" are untouched and not contradicted: no live platform verification is claimed for S006 here.

## 5. Required distinctions (stale premise vs source-date vs retry boilerplate)

- **Stale premise? No.** The premise at line 2 is "S001-S007 opened that day"; `corpus/SOURCES.md:9-15` shows `opened = 2026-10-19` for every row the range spans, S006 included — a historical date fact that remains true, not an attribution that went wrong.
- **Source-date boilerplate?** Exactly the case the contract admits ("INCLUDE historical metadata/r26 EOF prose"). Line 84 (r26 EOF block) and the `verified-at:` header are the metadata layer; neither asserts a live platform state, so no live-recheck obligation attaches.
- **Irrelevant retry boilerplate?** `.ufo/waves/round-26/fetched/manifest-retry.json` contains **only S008** (first attempt `TimeoutError at 60s; single retry with 240s timeout`). S006 has no retry row in r26 and was fetched first-try in both r26 and r27 — the retry artifact is not provenance for this pair.
- **Over-inclusive range (precision, not staleness).** `S001-S007` spans S004 as well as S006, and neither is in this entry's supporting set; the range is over-inclusive *as an enumeration of supporting sources* but not *as a date statement*. Because `:1` and `:84` state the supporting set explicitly and `SOURCES.md` `used-by` omits publish-channels.md, no reader-facing misattribution is created. Observation for L1, not a STALE finding, not a source-date error.

## 6. Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json`)

```json
{
  "row": "S006",
  "file": "corpus/knowledge/publish-channels.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor Start with _,., or # End with ~",
  "anchor": "About GitHub Pages and Jekyll page, H2 \"Configuring Jekyll in your GitHub Pages site\" (raw id configuring-jekyll-in-your-github-pages-site); default-exclusion list between the locked-settings paragraph and the \"Front matter\" H2; scope sentence \"If you are publishing from a branch\" still present",
  "reason": "Sole citing site is the expanded range at corpus/knowledge/publish-channels.md:2, \"round-20 corrections 2026-10-19 (S001-S007 opened that day)\"; the literal token S006 does not occur in the file. The range's predicate is an opened-date, not a support set, and corpus/SOURCES.md:14 records S006 opened=2026-10-19 (as do S001-S007 at :9-:15), so the premise holds; the entry's supporting set is enumerated without S006 at :1 (\"S001, S002, S003, S005 and S007 ... support the EOF round-20 corrections\") and at :84 (r26 EOF provenance), and .ufo/waves/round-26/statements.json has five publish-channels rows (S001,S002,S003,S005,S007) and no S006 row, so this is a metadata-only occurrence. Round-27 retained bytes re-ground the source: fetched/manifest.json S006 index 1 status 200 fetchedAt 2026-10-21T19:59:56Z bytes 138096 sha256 f0318abe7e63ecded4e7294484bd8cb68721e920b46d0b85399acb2a187742b6 (recomputed from the decompressed blob, matches); fetched/text/S006-1.txt sha256 2d953b39b80cab8f7a51496dbbc627882d5b2451faa0567e0a1008e1bb5aa1f8 is byte-identical to the r26 text view, and the exclusion passage and the branch-publishing scope sentence are unchanged, so S006's recorded scope is stable. Artifact corroboration: corpus/SOURCES.md:14 contains \"Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19\" and \"paths ending in tilde, node_modules, and vendor | mined | 2026-10-19 | 90d | corpus/knowledge/ghp-served-set.md |\". No stale premise, no correction required; historical dates preserved."
}
```

Alternative equivalent form if L1 prefers artifact grounding for this metadata-scope pair (`contains` must be a substring of the evidence blob):

```json
{
  "row": "S006",
  "file": "corpus/knowledge/publish-channels.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "evidence": "corpus/SOURCES.md",
  "contains": "Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19",
  "reason": "The only S006 occurrence in this file is the range \"S001-S007 opened that day\" at corpus/knowledge/publish-channels.md:2; corpus/SOURCES.md:14 records S006 as fetched/opened 2026-10-19, and the entry enumerates its supporting rows without S006 at :1 and :84, so the row is a historical date provenance, not a substantive attribution."
}
```

Field check against the frozen counter: `verdict` ∈ {HOLD,STALE,UNVERIFIABLE} ✓ · `reason` non-empty ✓ · kind=source → manifest row S006 / index 1 exists, raw sha256 recomputes ✓ · `quote` = 24 words (≤25), a whitespace-normalised substring of `fetched/text/S006-1.txt` ✓ · `anchor` non-empty ✓ · no STALE marker needed for a HOLD ✓.

## 7. Appended-correction wording

**None required.** A HOLD needs no appended tag; the counter requires `[r27-recheck S0NN STALE]` inside the citing file only for STALE verdicts. Nothing in the citing file is wrong.

Optional provenance append (L1's call; asserts no staleness, rewrites no original line, omittable without affecting the C1 count). One block can cover the sibling range pair (S004, same line):

```
### Round-27 range-pair provenance — S004, S006 (2026-10-21, append-only; original lines unchanged)

- The `verified-at:` header's range "(S001-S007 opened that day)" is an opened-date enumeration, not a support set: S004 and S006 fall inside it but are not among this entry's supporting rows, which are S001, S002, S003, S005 and S007 (see :1 and the round-26 recheck note at :84). Both rows were opened 2026-10-19 (corpus/SOURCES.md:9-15), so the range's premise is accurate and no original line is stale. Re-grounded this round against bytes opened 2026-10-21 (`.ufo/waves/round-27/fetched/manifest.json`, retained text under `fetched/text/`); S006's page still documents Jekyll's default exclusions under "Configuring Jekyll in your GitHub Pages site" and still scopes them to branch publishing. No live domain recheck was performed and none is claimed.
```

## 8. Denominator / discovery note

- The pair is in the frozen base missing list (r27 `count_c1.py` at base `83528f7` → missing includes `{"row":"S006","file":"corpus/knowledge/publish-channels.md"}`) → a required r27 obligation.
- **No new citing pair is added by this seat.** The file's enumerated ids are S001–S007 (literals plus the line-2 range) plus S019; S019 is outside the frozen 32-row population (`.ufo/waves/round-26/population.json`), so under the frozen denominator it adds no pair — no `discovered-pairs.json` addition is proposed.
- Sibling pair on the same line, named so no obligation is dropped: **(S004, corpus/knowledge/publish-channels.md)** arises from the same `S001-S007` expansion and is likewise a metadata date-provenance occurrence (S004 opened 2026-10-19). No verdict is claimed for it here.

## 9. Cross-seat observations (L1 integration only; no action taken)

- Working-tree drift vs the frozen declaration commit: `.ufo/waves/round-27/count_c1.py` and `c2_count.py` are modified relative to `be375d9` (count_c1 gains a baseline/`decided` union, a population guard, a `--selftest` branch). The drift is monotone (enlarges the denominator, removes no expectation) and does not affect this pair, missing under both the committed and the modified counter.
- `.ufo/waves/round-26/receipt-locator-errata.json` lists S006 among rows whose w1/w2 seat reports published pre-amendment text-view digests; committed views and `fetched/manifest.json` are authoritative. The r27 text view used here is authoritative and its sha256 equals r26's.

## 10. Verification commands (read-only, re-runnable)

```
git show be375d9:corpus/knowledge/publish-channels.md | grep -nE 'S[0-9]{3}'
grep -nE "S[0-9]{3}[-–—.]" corpus/knowledge/publish-channels.md
python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba
zcat .ufo/waves/round-27/fetched/S006-1.raw.gz | sha256sum
sha256sum .ufo/waves/round-27/fetched/text/S006-1.txt .ufo/waves/round-26/fetched/text/S006-1.txt
grep -cF "Jekyll doesn't build files or folders that" .ufo/waves/round-27/fetched/text/S006-1.txt
```

## 11. Gaps / uncertainties

- No live re-fetch by this seat (retained bytes only); "still live at 2026-10-21T19:59:56Z" rests on the round-27 manifest + hash-verified retained blob.
- r26 vs r27 raw HTML digests differ at identical content-length; extracted text views are byte-identical, so this is judged page-furniture drift. I did not diff the raw HTML; the identical text view is the evidence offered.
- Whether L1 wants a HOLD-append (or a SOURCES `used-by` mention) for a metadata-only range member is a policy choice; this seat records the option and takes no source action.

## 12. Tooling / transaction record

No tool install, upgrade, downgrade or service mutation was needed or performed; no pacman transaction (all pacman transactions are PAUSED host-wide and untouched). Reads used `read`, `grep`, `bash` (git / python3 stdlib for hashing and range arithmetic) and `write` for this report only. Scratch reserved at `/fast/scratch/hyaku/kake-r27/Pair09A/` (empty). No network access; no account/credential/cookie/property/publication operation. No r24 stopped work was read, retried, rephrased or rerouted.

Report: .ufo/waves/round-27/w1/Pair09A.md
