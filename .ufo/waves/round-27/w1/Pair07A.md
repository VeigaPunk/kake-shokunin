# Pair07A — (S005, corpus/knowledge/sitemap-orphan-audit.md), Kake r27 w1 C1 ledger row

Seat: KakeR27.Pair07A (author-side, read-only findings). Axis: **freshness**. Milestone: r27-full-citing-set.
Leaf member, no dispatch. No ledger/source/Git/fleet edits; no builds/lint/tests; no tool installs.
Measured revision `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (worktree HEAD); frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`.
Citing file sha256 `553ad1006e9e5800668afb033cd655b5d938fe1736b769dd9d82a3019268a0ec` (149 lines) — byte-identical at base
`83528f7c`, at `be375d90` and in the worktree (`git show … | sha256sum`).

## 1. Verdict

**STALE (partial — the source-id attribution only).** The date `2026-10-19`, the base `cb807bc` and the
`historical-not-live-reverified` marker on line 2 **hold**. The id band `S001-S006` **over-attributes S005**: at its own
stated scope (the sources of *this entry's* r20 quote corrections) S005 grounds none of them, and that attribution was
already false at the base revision. `corpus/QUALITY.md` §Recheck adjudication — round 26: *"A statement whose attribution
was false even at its base revision is STALE"*; the date/base pointer parts of the same line are expressly **not** stale
("record it as a note"). Axes: **freshness** (seat axis — are the cited bytes still the bytes the row was mined from, and
does the citing line hold against them at its own stated scope?); secondary **operability** note only (§8, §11).

## 2. Exact citation location (range expanded)

- The **only** S005 citation in this file is reached by expanding the ASCII-hyphen range on **line 2**; there is **no
  literal `S005`** on any of the 149 lines (sweep with the `count_c1.py` patterns: 1 range, 0 literals; the file's other
  S-tokens are the literals S001/S002/S004/S006 on lines 1, 120–127, 149). Kind: **historical metadata** (front-matter
  `verified-at:`), *not* r26 EOF prose; not a source-date stamp defect.
- `corpus/knowledge/sitemap-orphan-audit.md:2` (verbatim):

```
verified-at: 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2xZ as recorded; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; no live sitemap or domain fetch this round
```

- Provenance: introduced by the r21 commit `df6196b` ("round-21: make publishing corpus provenance and gates
  inspectable", 2026-10-20 06:08:53 -0300) together with line 1 (`git log -S 'r20 S001-S006 quote corrections'`); the
  r20 commits did not write it.
- Frozen denominator: this pair is **already** item 7 of the 16 missing pairs in `.ufo/waves/round-27/c1-before.json` and
  in `.ufo/waves/round-27/c2-oracle.json` `expectedPairs`. **No new pair is discovered here** (§10).

## 3. The claim at that location, and its scope

Line 2 makes three separable assertions about *this entry*: (a) evidence dates 2026-09-28 / r16 re-read 2026-09-29T02:2xZ
— **hold** (file body §"Baseline 2026-09-28", §r16); (b) the r20 quote corrections are dated **2026-10-19** at base
**cb807bc** — **holds** (correction block header `## Round-20 corrections (append-only; base cb807bc)`, lines 118–127);
(c) the sources of those corrections include **S001–S006** — **fails for S003 and S005**. The r20 tails (lines 120–127)
cite only `S001, S004`, `S001, S002, S004, S006` and `ghp-served-set.md (S001, S004)`; line 1 narrows the same set
(`S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`); the r26 EOF line 149 repeats it
(`The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127).`).

## 4. Evidence — artifact side (attribution)

1. **r20 authoritative disposition ledger** `.ufo/round-20/resume/citation-disposition.json` (tracked; sha256 at
   `be375d90` `d3f33e0b75ba63dde82b0d685bb2b97e5d7f07c14a7bf89ad998dd487c8c56b6`; `base: "cb807bc"`; note: *"`platformCorrections`
   preserves the original 02b6dd0 locations"*). `platformCorrections` records **all 8 locations of this file** (indices
   8–15), every source list `["S001","S004"]` or `["S001","S002","S004","S006"]` (index 8 verbatim in §8's artifact
   record). The ledger's only four S005 records are index 0 (`SKILL.md:16`), 5 and 7 (`publish-channels.md:9` and `:12`),
   26 (`ghp-subpath-spotcheck.md:83`) — **none is this file**.
2. **r20 lesson row** `corpus/lessons/round-20.md:261` (mistake A2) lists this file
   (`corpus/knowledge/sitemap-orphan-audit.md:20-24`) with C3 rows `S001/S002/S003/S004/S006/S008` — **S005 absent**;
   S005 sits in the *other* misconception's C3 list at `corpus/lessons/round-20.md:262` (A3 → publish-channels.md /
   `ghp-custom-domain`).
3. **Registry** `corpus/SOURCES.md:13` — S005 scope "Custom-domain configuration for Actions-published Pages sites",
   opened `2026-10-19`, used-by `corpus/knowledge/ghp-custom-domain.md` only; the file contains no `CNAME` and no
   `custom domain` text (`grep -ci` → 0 and 0). **r26 ledger** `.ufo/waves/round-26/statements.json` carries exactly four
   pairs for this file (S001, S002, S004, S006) — r26 never expanded the line-2 range, which is why this pair sat in the
   frozen 16.

## 5. Evidence — source side (freshness of S005 itself)

- r27 retained fetch: `.ufo/waves/round-27/fetched/manifest.json`, row S005, **fetchIndex 1**, HTTP 200, 240439 bytes,
  sha256 `6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4`, fetchedAt `2026-10-21T19:59:56.085676+00:00`;
  text `.ufo/waves/round-27/fetched/text/S005-1.txt` sha256 `b2a7d47d7193dd2f3d8303d32e7d2379b14e7908f26208115516237f6fd8d2ba`.
- Located quote (9 words, present in that text, **unique** — absent from S001-1/2, S002-1/2, S003-1, S004-1, S006-1, so
  it satisfies `corpus/QUALITY.md` §r26 "a recheck HOLD needs a row-specific located quote"):
  `any existing CNAME file is ignored and is not required`
  Anchor: *Managing a custom domain for your GitHub Pages site* — **Configuring an apex domain**, step 4 ("Under \"Custom
  domain\", type your custom domain, then click Save."); the same sentence appears in **Configuring a subdomain**, step 4.
- Historical note preserved: r26's fetch of the same URL has sha256
  `dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9` (2026-10-21T15:09:34Z) — different bytes, same text
  at the anchor; per `corpus/lessons/round-26.md` a living document is judged by quote at anchor, never by sha equality;
  r26 receipt `.ufo/waves/round-26/rechecks/S005.json` = HOLD. **S005's content is fresh and intact; content freshness is
  irrelevant to this pair** — the defect is the attribution.

## 6. Stale premise vs source-date vs retry boilerplate (three-way distinction)

- **Source-date: holds, preserved.** S005 opened `2026-10-19` (`corpus/SOURCES.md:13`); r20 resume dated 2026-10-19 at
  base `cb807bc`; r20 source table row S005 reads "fetched 2026-10-19" (`corpus/lessons/round-20.md:207`).
- **Stale premise: not the defect.** S005's bytes, anchor and scope are intact (§5); no time-decay is involved.
- **Retry boilerplate: irrelevant.** "no live sitemap or domain fetch this round" describes r21's own fetch activity, not
  an S005 claim; the r26 `S008 via manifest-retry.json` paste-artifact belongs to *other* entries' EOF prose.
- **The actual defect: an authoring-time over-broad range.** The r21 header writer collapsed the four grounding rows
  {S001, S002, S004, S006} into `S001-S006`, sweeping in S003 and S005. S005 is the element judged in this seat.

## 7. Alternative reading considered (uncertainty, disclosed)

The strongest objection to STALE is a **min–max interval reading** of provenance bands: in all five band occurrences in
`corpus/knowledge/` the endpoints are exactly the min and max of the rows actually cited (`sitemap-orphan-audit.md:2`
`S001-S006` = {S001,S002,S004,S006}; `publish-channels.md:2` `S001-S007` = {S001,S002,S003,S005,S007};
`static-canonical-preflight.md:2` `S020-S027` / `S028-S029`; `static-canonical-preflight.md:54` `S001–S006` =
ghp-served-set.md's {S001,S002,S003,S004,S006}). Under that convention `S001-S006` asserts no S005 attribution, the pair
exists only because `count_c1.py` conservatively expands intervals, and the honest verdict would be HOLD scoped to band
membership (never to the zero-orphan claim) with no append. [INFERENCE] — inferred from five instances; **no corpus rule
defines band notation** (`corpus/QUALITY.md`, `corpus/SOURCES.md` §SOURCES contract v1 and the canonical `CORPUS.md`
provenance rules put the `S###` citation of an external source in `source:` and say nothing about ranges in
`verified-at:`). I weigh the enumeration reading higher and judge STALE, because: (i) the same header's **line 1**
enumerates (`S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`) — same author, same
commit, writes a list when it means specific rows; (ii) the two sibling headers qualify their bands explicitly
(`S001-S007 opened that day`; `documentation opened this round`) — a band-as-opened-rows reading — whereas **this** line
qualifies its band with `quote corrections`, i.e. the rows behind this entry's corrections; (iii) the r20 disposition
ledger (§4.1) grounds this file's corrections on S001/S002/S004/S006 only; (iv) the corpus binds the consequence:
attribution false at base ⇒ STALE, date/base ⇒ note. **If the L1 instead adopts the interval reading for provenance bands,
the verdict for this pair is HOLD and no append is required** — that branch's record and reason text are in §8a so
integration is not blocked by this ambiguity.

## 8. Suggested C1 ledger records (`.ufo/waves/round-27/pairs.json` → `pairs[]`)

Kind **source** is primary: the contract requires the grouped pairs to be "grounded against sources opened this round",
and S005's bytes are what show its scope (custom domains) is disjoint from this entry's claims.

```json
{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"source","verdict":"STALE","fetchIndex":1,"quote":"any existing CNAME file is ignored and is not required","anchor":"Managing a custom domain for your GitHub Pages site — Configuring an apex domain, step 4 (same sentence in Configuring a subdomain, step 4)","reason":"Only S005 occurrence is the line-2 range 'r20 S001-S006 quote corrections 2026-10-19, base cb807bc' (r21 df6196b historical metadata). Date, base cb807bc and the historical-not-live-reverified marker hold; the S005 attribution does not: .ufo/round-20/resume/citation-disposition.json platformCorrections[8..15] list only S001/S002/S004/S006 for all 8 locations of this file; line 1 and line 149 enumerate the same four; S005 (custom-domain/CNAME scope, used-by corpus/knowledge/ghp-custom-domain.md) grounds none of them. Attribution false at base => STALE per QUALITY round-26; the source bytes are themselves fresh (r27 fetch index 1, HTTP 200, sha256 6f3d1ad2..., quote present at the apex-domain step-4 anchor)."}
```

Self-check against the frozen `count_c1.py`: `fetchIndex 1` resolves in `.ufo/waves/round-27/fetched/manifest.json`; the
manifest sha256 equals the decompressed raw bytes; the 9-word quote is a whitespace-normalised substring of
`fetched/text/S005-1.txt` and unique across all eight fetched texts; `anchor` non-empty; the key
`(S005, corpus/knowledge/sitemap-orphan-audit.md)` is in the enumerated citing set; **a STALE verdict additionally
requires the literal marker `[r27-recheck S005 STALE]` inside the citing file at the measured revision** — not present
yet, so the L1 must append §9 (or record the HOLD of §8a) before this row validates. Precondition: the r27 fetched
artifacts must be committed at the measured revision.

### 8a. HOLD-branch record (use only if L1 rules bands = min–max intervals)

```json
{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"source","verdict":"HOLD","fetchIndex":1,"quote":"any existing CNAME file is ignored and is not required","anchor":"Managing a custom domain for your GitHub Pages site — Configuring an apex domain, step 4; Configuring a subdomain, step 4","reason":"Only occurrence is the line-2 band 'r20 S001-S006 quote corrections 2026-10-19, base cb807bc'. Under the corpus's min-max band convention (5/5 instances) the band bounds {S001,S002,S004,S006}; S005 is an interior element, contributes no claim here, and the line's date/base/marker assertions all hold. HOLD is scoped to band membership and to the truth of the line's assertions, never to the zero-orphan claim."}
```

Artifact-kind alternative (evidence must **not** be the citing file — peer `CritClaimFit.md` F1); its `contains` string is
byte-exact against the tracked ledger bytes and is the r20 grounding record itself, not the citing file and not a
`corpus/knowledge/` file — the source-kind primary in §8 avoids peer F1's self-citation concern altogether:

```json
{"row":"S005","file":"corpus/knowledge/sitemap-orphan-audit.md","kind":"artifact","verdict":"STALE","evidence":".ufo/round-20/resume/citation-disposition.json","contains":"\"location\": \"corpus/knowledge/sitemap-orphan-audit.md:14\",\n   \"currentLine\": 14,\n   \"supersededClaim\": \"A zero orphan count and GHP orphan impossibility are established by checkout membership.\",\n   \"sources\": [\n    \"S001\",\n    \"S004\"\n   ]","reason":"r20 authoritative disposition: this file's eight corrections are grounded on S001/S002/S004/S006 only; S005 grounds none of them, so the line-2 band over-attributes S005 (date/base hold)."}
```

## 9. Append-only correction wording (L1 applies; nothing appended by this seat)

New EOF section in `corpus/knowledge/sitemap-orphan-audit.md`; lines 1–149 stay byte-identical (round-20 append-only
ruling; `corpus/QUALITY.md` §Post-review append-only ruling):

```markdown
## Round-27 citing-set recheck

- [r27-recheck S005 STALE] Line 2's `r20 S001-S006 quote corrections` over-attributes S005. The round-20 corrections in this entry (lines 120-127) cite only S001, S002, S004 and S006 (`.ufo/round-20/resume/citation-disposition.json`, platformCorrections for this file); S005 (custom-domain configuration) grounds none of them. The 2026-10-19 date and base `cb807bc` stand. Line 2 is historical r21 metadata and stays unchanged.
```

## 10. Sibling pairs, denominator, peer notes (no denominator change)

- **No new citing pair.** A literal+range scan of this file at `be375d90` yields S001, S002, S003, S004, S005, S006 —
  4 decided in r26 + the 2 header-range-only pairs, both already inside the frozen 57/16; nothing to add to
  `.ufo/waves/round-27/discovered-pairs.json`.
- **Sibling `{S003, corpus/knowledge/sitemap-orphan-audit.md}`** (same band) — *not mine*; evidence differs: S003 is absent
  from `platformCorrections[8..15]` too, but `corpus/lessons/round-20.md:261` (A2) names S003 among the C3 rows for **this
  file's** misconception, and S003's scope (branch vs Actions publishing) bears on the superseded claims "The live served
  tree equals the last-pushed origin/main tree" and "Live-only paths could only come from branch publishing"; the owning
  seat should weigh that, and if both land STALE one EOF section may carry both markers (`count_c1.py` checks each
  `[r27-recheck S0NN STALE]` independently).
- **Same band shape elsewhere (owner seats, not mine):** `publish-channels.md:2` `S001-S007` (S004, S006);
  `static-canonical-preflight.md:54` `S001–S006` (S005 contributes none there either); `static-canonical-preflight.md:2`
  `S020-S027` (S022, S023).
- **Naming note for the L1:** the r26 non-author closure (`corpus/lessons/round-26-verifier-spotcheck.md:11`) named only
  the grouped `S001–S006` claim at `static-canonical-preflight.md:53–54`; the **second** grouped citation at
  `sitemap-orphan-audit.md:2` was not named there, although the frozen r27 counter does expand it (missing item 7). Both
  bands should be judged under one convention.
- **Peer convergence (disclosed):** critic seat `w1/Pair07B.md` independently reached **STALE** for this same pair (my
  route differed — the r20 disposition ledger plus `corpus/QUALITY.md` §r26 and the interval counter-reading of §7; I did
  not read Pair07B before forming this judgment). Peer `w1/CitingSweep12.md` states the scope caveat this seat follows:
  any HOLD/STALE here must be scoped to the id attribution, never to the zero-orphan claim.

## 11. Checks for the L1 after integration

- `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>` → the S005/sitemap outcome must be
  `valid:true`; the missing list must lose exactly this pair (16 → 15 unless other seats land).
- `grep -F '[r27-recheck S005 STALE]' corpus/knowledge/sitemap-orphan-audit.md` → must hit (STALE branch).
- `git show <base>:corpus/knowledge/sitemap-orphan-audit.md | sha256sum` vs candidate: lines 1–149 unchanged (append-only).
- `git diff be375d90 <candidate> -- .ufo/waves/round-26/ .ufo/waves/round-27/{count_c1.py,c2_count.py,c2-oracle.json,frozen/,contract.json}` → empty (peer `CritClaimFit.md` F2).

## 12. Boundaries, tools, evidence index

- Read-only: this report is the only write
  (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-27/w1/Pair07A.md`). No corpus/ledger/source/Git/fleet/jj/
  index mutation; no commits; no dispatch; no state/grade operation. No r24 stopped work read, retried, rephrased or
  rerouted; no publication/property/browser/account/credential operation; no URL fetched by this seat (the r27 fetch bytes
  are the frozen shared artifacts).
- No tool installed or updated; no pacman transaction (pacman paused host-wide); no builds, lint, tests or formatters.
- Evidence read: `corpus/knowledge/sitemap-orphan-audit.md` (1, 2, 118–127, 149); `corpus/knowledge/{publish-channels.md:2,
  static-canonical-preflight.md:2,54, ghp-served-set.md:12–30}`; `corpus/SOURCES.md:13`; `corpus/QUALITY.md` (43–51, 178–233);
  `corpus/lessons/round-20.md` (207, 261–262); `corpus/lessons/round-21.md` (49–54); `corpus/lessons/round-26.md` (25–60);
  `corpus/lessons/round-26-verifier-spotcheck.md` (11, 119); `.ufo/round-20/resume/citation-disposition.json`;
  `.ufo/waves/round-26/{statements.json,rechecks/S005.json,fetched/manifest.json}`;
  `.ufo/waves/round-27/{contract.json,count_c1.py,c1-before.json,c2-oracle.json,fetched/manifest.json,fetched/text/S005-1.txt}`.

Report: .ufo/waves/round-27/w1/Pair07A.md
