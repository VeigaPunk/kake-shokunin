# Pair03A — (S003, corpus/knowledge/sitemap-orphan-audit.md) — r27 C1 adjudication

Seat: reviewer (read-only findings; no ledger/source edits). Axis judged: **freshness**.
Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
No r24 work read, retried, rephrased or rerouted. No fetches performed by this seat; only bytes already in the repo plus the r27 fetch manifest already on disk.

## 1. The pair and where it is cited

Pair: row `S003` × file `corpus/knowledge/sitemap-orphan-audit.md`.

The pair is **not** a literal `S003` token. It is produced by expanding the range on the entry's `verified-at:` metadata line.

`corpus/knowledge/sitemap-orphan-audit.md:2` (verbatim, complete line):

```
verified-at: 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2xZ as recorded; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; no live sitemap or domain fetch this round
```

`S001-S006` expands (count_c1 `RANGE`) to S001, S002, **S003**, S004, S005, S006 — six pairs, of which the two not already decided are this pair and `(S005, corpus/knowledge/sitemap-orphan-audit.md)`.

**This is the only S003-bearing token in the file.** Enumeration of the frozen blob (`git show 83528f7:corpus/knowledge/sitemap-orphan-audit.md`) yields exactly one range (`S001-S006`, line 2) and literals S001/S002/S004/S006 only; no other line contains `S003`. Confirmed by the frozen counter: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7…` → `population 32, citingPairs 57, decided 41, r26CarriedPairs 41, newDecided 0, findings []`, with `missing` containing `{row: S003, file: corpus/knowledge/sitemap-orphan-audit.md}`. The r26 ledger `.ufo/waves/round-26/statements.json` carries S003 only for `ghp-custom-domain.md`, `ghp-served-set.md`, `publish-channels.md` — not this file.

## 2. Surrounding claim in the same entry (all committed)

- `corpus/knowledge/sitemap-orphan-audit.md:1` — `source:` line names the entry's own r20-correction sources: `S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections`.
- `:120-127` — the eight `## Round-20 corrections (append-only; base cb807bc)` lines. Their inline citations are S001/S002/S004/S006 only; **S003 is not cited inline anywhere in this entry**.
- `:149` — r26 EOF provenance block: “The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127).”

So the entry itself distinguishes (i) the rows that support its r20 correction lines (line 1, line 149) from (ii) the coarser `S001-S006` block on line 2.

## 3. Testing the citing line at its own stated scope

Stated scope of the line-2 range: *round-20 quote corrections, dated 2026-10-19, against base `cb807bc`*.

**(a) Date and base — accurate, preserved history.**
`cb807bc8d8bc94be1268e4741191bb3d5e518565` is the **direct parent** of the round-20 commit `02b6dd0` (“round-20: resume — citation-local debt cleared…”, 2026-10-19 19:38 -0300) (`git rev-parse 02b6dd0^` → cb807bc8d8bc94be1268e4741191bb3d5e518565; `git merge-base --is-ancestor cb807bc 02b6dd0` → true). The base line coordinates cited in `:120-127` check out against `git show cb807bc:corpus/knowledge/sitemap-orphan-audit.md`: base :14 = the coverage-matrix orphan row; :18 = “## GHP live-only orphans are impossible by construction”; :21 = “**fresh snapshot of the entire checked-out tree** every push — both”; :25 = “deploy never retains files from the previous artifact…”; :28 = “the live tree IS the last-pushed `origin/main`”; :32 = “Residual live-only exposure on GHP is therefore **listing coverage**”; :38 = “list names,” …; :112 = “deploy graph; if a row ever switches deploy modes, re-derive this.” The 2026-10-19 date and the `cb807bc` base are not stale; they are the historical coordinates of the r20 pass.

**(b) S003's part of the range — supported by r20 tails, not by an inline quote.**
`corpus/lessons/round-20.md:261` (r20 mistake tail **A2**, class “Platform mechanism inferred from workflow shape: the served set equated with the `origin/main` tree (deploy taken as the whole tree)”) lists, in its evidence-pointer cell, this very entry's base lines and, in its Fix cell, the C3 row set that includes S003:

```
`corpus/knowledge/sitemap-orphan-audit.md:20-24` | `none` | C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`; annotate `round-7.md` append-only
```

Base lines 20-24 sit inside the corrected span (18/21/25) — i.e. the “impossible by construction” passage that A2 names. `corpus/lessons/round-20.md:205` records S003's r20 quote with its opening date:

```
| S003 | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.” | “About publishing sources”; fetched 2026-10-19. |
```

`corpus/SOURCES.md` row S003: status `mined`, opened `2026-10-19`, scope “GitHub Pages publishing modes and repository source selection”, anchor “About publishing sources and note under Creating a custom GitHub Actions workflow; fetched 2026-10-19”.

**Each source's contribution (labelled, per contract):** S003 grounds the *deploy-mode scope* of the r20 correction of this entry — that Pages publishes either from a branch or from an Actions workflow — which is what conditions this entry's conclusion (“A live orphan could exist only via a non-workflow Pages deploy (branch deploy) … if a row ever switches deploy modes, re-derive this”, base :112). It does **not** ground the artifact-membership content (`.git/.github` exclusion, v4 dotfile default, gzip-tar shape) — that is S001/S002/S004/S006, cited inline at `:122`, `:124`, `:126`.

**Inferential step (explicit):** the judgment treats line 2's `S001-S006` as the round-20 *source-block* descriptor of the correction pass (its sibling entry `corpus/knowledge/publish-channels.md:2` uses the identical block with the gloss “(S001-S006 opened that day)”), reconciled with line 1 and line 149 by the A2 tail. Under that reading S003's inclusion is backed by committed r20 bytes (A2 fix set + S003's retained r20 quote and 2026-10-19 opening date). The range is **coarse, not exhaustive** (A2's set also contains S008, which the range omits) — imprecision, not falsity.

## 4. Freshness: is the premise stale?

- S003 was re-fetched in r26 (`.ufo/waves/round-26/fetched/manifest.json`, row S003 index 1, 2026-10-21T15:09:34Z, sha256 `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`) and re-judged HOLD at its anchor (`.ufo/waves/round-26/rechecks/S003.json`: `"verdict": "HOLD"`, quote “You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.”). The source still supports its teaches; the historical `2026-10-19` in the citing line is a preserved reading date, and the line itself declares `historical-not-live-reverified`.
- r27 fetch already on disk (`.ufo/waves/round-27/fetched/manifest.json`, row S003 index 1, 2026-10-21T19:59:55Z): decompressed sha256 `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5` — matches the manifest entry; the 25-word quote is present in `.ufo/waves/round-27/fetched/text/S003-1.txt` and “About publishing sources” is present at the anchor.
- **Retry boilerplate is irrelevant here:** `.ufo/waves/round-26/fetched/manifest-retry.json` contains **only S008** (attempt 2 after a timeout). S003 needed no retry in r26 or r27; no retry text touches this pair.
- House precedent against a stale verdict on dated/base-scoped pointers: `corpus/lessons/round-26-verifier-spotcheck.md:92` — “The pointers explicitly say ‘at base cb807bc’; later coordinates do not make a dated statement false.” And `:89` records S003's r20 correction attribution as **admit**/source-supported.

## 5. Verdict

**HOLD** — the S003 attribution carried by the `S001-S006` range on `corpus/knowledge/sitemap-orphan-audit.md:2` is supported at its stated scope (round-20 quote corrections, 2026-10-19, base cb807bc) by committed r20 bytes: `corpus/lessons/round-20.md:261` places S003 in the C3 remediation set for this entry's base lines 20-24, and `corpus/lessons/round-20.md:205` retains S003's quote and its 2026-10-19 opening date; `corpus/SOURCES.md` row S003 agrees. Nothing in the citing line is wrong; the source date is historical and correct; S003's contribution is scope-level (branch-vs-Actions deploy mode), not an inline claim quote.

**Competing reading that would flip this to STALE** (stated for the parent): if `S001-S006` is read as the entry's *inline* citation set for its r20 correction lines, then S003 (and S005) are over-attributed, because `:120-127` and `:149` enumerate only S001/S002/S004/S006. I did not adopt that reading because (i) line 1 already enumerates the entry's inline r20 sources separately, (ii) the sibling entry uses the same block with a corpus-level gloss, (iii) A2 ties S003 to this entry's base lines, and (iv) the r26 spot-check rejects STALE for dated/base-scoped pointers. A reviewer who prefers the entry-level reading must append a `[r27-recheck S003 STALE]` correction and say which of the two readings is being enforced.

## 6. Suggested C1 ledger record (contract `pairs.json` row)

```json
{
  "row": "S003",
  "file": "corpus/knowledge/sitemap-orphan-audit.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "evidence": "corpus/lessons/round-20.md",
  "contains": "corpus/knowledge/sitemap-orphan-audit.md:20-24` | `none` | C3: S001/S002/S003/S004/S006/S008 rows plus `ghp-served-set`",
  "reason": "Historical-metadata citation: the only S003-bearing token in this entry is the range 'S001-S006' on the verified-at line 2 ('r20 S001-S006 quote corrections 2026-10-19, base cb807bc'). Base cb807bc8d8bc94be1268e4741191bb3d5e518565 is the parent of the r20 commit 02b6dd0 and the base line numbers cited at lines 120-127 match it. The r20 tail A2 (corpus/lessons/round-20.md:261) places S003 in the C3 remediation set for this entry's base lines 20-24, and round-20.md:205 retains S003's quote with 'fetched 2026-10-19'; corpus/SOURCES.md row S003 is opened 2026-10-19. The date and base are preserved history, not stale coordinates. S003 contributes scope only: it grounds the branch-versus-Actions publishing-mode condition of the entry's corrected conclusion (base :112), not the artifact-membership content that S001/S002/S004/S006 carry inline at lines 120-127. Secondary evidence: .ufo/waves/round-26/rechecks/S003.json (HOLD), .ufo/waves/round-26/fetched/manifest.json (S003 index 1, sha256 aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac); the r26 retry file manifest-retry.json covers S008 only and is irrelevant to S003."
}
```

`contains` is a verbatim, contiguous substring of `corpus/lessons/round-20.md` (verified byte-wise; the A2 row is a single table line carrying both the pointer and the fix set). `kind: artifact` is the honest classification — the support for a historical-metadata citation is a committed repo artifact, not S003's own bytes.

Alternative if the executor prefers a source-anchored row (also verifiable): `kind: source`, `fetchIndex: 1`, `quote: "You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site."` (25 words; present in `.ufo/waves/round-27/fetched/text/S003-1.txt`), `anchor: "About publishing sources — 'About publishing sources' section, first paragraph"`, with the same reason plus the manifest sha256 `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5`. This variant supports the *source's* continued currency, not the metadata claim itself; I recommend the artifact form.

## 7. Appended wording (optional precision note — HOLD needs no STALE marker)

Not required by the contract for a HOLD. If the executor wants the range's granularity made unambiguous for later rounds, append inside the file's tail (after the Round-26 block), unchanged historical dates preserved:

```
- [r27-recheck S003 HOLD] The `S001-S006` range on the verified-at line (line 2) is a round-20 source-block descriptor — "r20 S001-S006 quote corrections 2026-10-19, base cb807bc" — not the list of rows cited by this entry's round-20 correction lines, which are S001, S002, S004 and S006 (lines 120-127). S003 belongs to that correction through the A2 remediation set recorded at corpus/lessons/round-20.md:261 (this entry's base lines 20-24); its retained round-20 quote and 2026-10-19 opening date are at corpus/lessons/round-20.md:205. The 2026-10-19 date and the cb807bc base are historical coordinates and are not restated as current.
```

**Denominator consequence to declare:** that wording names only S003 and the existing `S001-S006` block, so it adds no new citing pair. If the executor instead names **S008** (which is also in A2's C3 set), it **adds a new obligation** — pair `(S008, corpus/knowledge/sitemap-orphan-audit.md)` — growing the C1 denominator from 57 to 58 and requiring its own HOLD/STALE/UNVERIFIABLE adjudication. I flag it here rather than letting the denominator change silently.

## 8. Uncertainties, residual risk, verification gaps

1. **Granularity of the range is not defined in the corpus.** Two committed statements coexist (line 2's `S001-S006`; line 149's enumeration of S001/S002/S004/S006). My HOLD resolves them via the A2 tail; a parent that reads line 2 entry-level will land on STALE. The adjudication should record which reading is being enforced so the sibling `(S005, sitemap-orphan-audit.md)` pair is judged consistently.
2. **The range is coarse, not exhaustive** (S008 in A2's set, outside `S001-S006`). No action unless the executor's appended wording names it (§7).
3. **A2's fix cell is a class-level remediation** for a defect spanning four evidence pointers, so S003's link to *this* entry is one hop (A2 → this entry's base lines 20-24). I consider that hop supported but it is the weakest step in the chain; it is labelled in §3.
4. **Not verified by this seat:** no live fetch of S003 was made (out of seat scope); freshness rests on the r26 receipt (HOLD) and the r27 fetch already on disk (sha256 verified locally, decompressed bytes match the manifest). The r26 receipt's reason names only `ghp-custom-domain.md:22` and `ghp-served-set.md:28` — it does not cover this entry; that gap is what this row closes.
5. **Vanished local inputs** (`/tmp/orphan-check.mjs`, the two `pages.yml` files, `fleet.config.json`; see the `recheck:` line) remain unrestorable; nothing in this judgment depends on them, and no restoration attempt was made.
6. **Sibling pair not adjudicated here:** `(S005, corpus/knowledge/sitemap-orphan-audit.md)` arises from the same range and shares the §3 evidence; its own row and reason still need to be recorded by its seat.

## 9. Hygiene

No tool installs were required or performed (no pacman/uv/cargo/npm action; pacman transactions remain paused host-wide). No scratch files were written; the two `python3`/`git` commands above read repo bytes only, under the repo root, and wrote nothing. No source, ledger, index, fleet or Git state was mutated by this seat — only this report file was written.
