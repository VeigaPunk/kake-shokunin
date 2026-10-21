# Pair S008 × ghp-served-set — round-26 freshness re-check

- Seat: KakeR25.PairS008GhpServedSet-6 (knowledge pair, leaf). Axis: freshness (operability note below).
- Knowledge entry: `corpus/knowledge/ghp-served-set.md` (79 lines; last line 79).
- Source: S008 = GNU tar manual, "Controlling Pattern-Matching", `doc/tar.texi` at commit `cfdb891bbd68c920ea75210977593f3cd08f0418`.
- Fetch used: index 1, attempt 2 (retry). Attempt 1 is `TimeoutError` with 0 body bytes (`fetched/manifest.json`; its `S008-1.raw.gz` is a 20-byte file). Attempt 2: HTTP 200, `fetchedAt` 2026-10-21T15:11:01Z, 512,359 bytes, sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` (`fetched/S008-1-retry.raw.gz`). I decompressed and hashed it in memory; it matches `manifest-retry.json`.
- Text view: `fetched/text/S008-1.txt` (503,332 bytes; one LF). Exact derivation confirmed: `re.sub(r'\s+([,.;:)\]])', r'\1', ' '.join(raw.split())) + '\n'`. The raw has 13,681 lines.
- Operability: the text view is a single line, so line anchors can only be checked on raw bytes. Quotes are checked against the text view.

## Result

Statements: 12 · HOLD: 12 · STALE: 0 · Flags: 4 (DATE ×2, VERSION ×1, ANCHOR note ×1).

Row-level `teaches` (`population.json:198`, S008 row): HOLD on the same evidence (rows 4, 5, 11).

## Statements

| # | Entry:line | Statement (short) | Verdict | Flag | Quote (verbatim, `fetched/text/S008-1.txt`) | Anchor (raw line / text offset) | Reason |
|---|---|---|---|---|---|---|---|
| 1 | :1 | Source list cites S008 | HOLD | — | `@unnumberedsubsec Controlling Pattern-Matching` (3 w) | raw 8481 / text 303800 | S008 is the commit-pinned `tar.texi` and the cited section exists. The pinned URL on :1 is S001's `action.yml`, which is outside this pair. |
| 2 | :2 | "verified-at: 2026-10-19" covers S008 | HOLD | DATE superseded | `Default is @option{--no-anchored} for exclusion members and @option{--anchored} inclusion members.` (10 w) | raw 8587–8588 / text 307131 | The date is accurate as history. S008 was re-fetched 2026-10-21T15:11:01Z with the same quoted content. The entry-level date also covers S001 (out of pair). |
| 3 | :20 | "Source checks (quotes reopened 2026-10-19)." | HOLD | DATE superseded | same as #2 (10 w) | raw 8587–8588 / text 307131 | The 2026-10-19 reopen is historical. The quotes are still present verbatim on 2026-10-21. |
| 4 | :34–35 | "S008, GNU tar 1.35, Controlling Pattern-Matching: ‘Default is … inclusion members.’" | HOLD | VERSION superseded: "1.35" withdrawn at :73–74 | same as #2 (10 w) | raw 8481, 8587–8588 / text 303800, 307131 | Quote substance is verbatim. The entry shows Texinfo-rendered backticks where the source has `@option{}`. The body contains 0 occurrences of "1.35" and takes its version from `@include version.texi` (raw 4). The label stays withdrawn, and the existing erratum already corrects it. |
| 5 | :36 | Exclusion defaults let wildcard `*` match `/` in a member name | HOLD | — | `When wildcards match slash (the default for exclusion members), a wildcard like @samp{*} in the pattern can match a @samp{/} in the name.` (23 w) | raw 8602–8604 / text 307627 | The exclusion default is wildcards-match-slash; the summary row is raw 8618. "member name" glosses "the name". |
| 6 | :43–51 | Local depth repro output, presented as S008-dependent (`./`, `./a/`, `./a/b`, `./CNAME`; `.nojekyll`, `.well-known/x`, `a/.keep` absent) | HOLD (S008 reliance) | — | `@item Exclusion @tab @option{--wildcards --no-anchored --wildcards-match-slash}` (6 w) | raw 8618 / text 308277 | The repro's exclusion set depends on the unanchored and wildcards-match-slash defaults that this row states. The repro was NOT re-executed, because its `mktemp` scratch lands under /tmp, which lane bounds bar. Its 2026-10-19 output is therefore unverified today. |
| 7 | :52–54 | [INFERENCE] depth result follows from GNU tar's unanchored and slash-matching defaults | HOLD | — | `Otherwise, the pattern can match any subsequence.` (7 w) | raw 8586 / text 307081 | The unanchored default (raw 8587) and the slash default (raw 8602) are both present, and the inference label is kept. The clause "GitHub's action source alone …" is S001 scope and is not judged here. |
| 8 | :67 | GNU tar manual cited "at [its] scoped source" | HOLD | — | `@end menu @node controlling pattern-matching @unnumberedsubsec Controlling Pattern-Matching` (8 w) | raw 8478–8481 / text 303755 | The scoped source is the commit URL (`SOURCES.md:16`). This holds only together with erratum :73–74, because the :34 label is otherwise an unscoped citation. |
| 9 | :73–74 (erratum) | "GNU tar 1.35" label withdrawn; cited source is manual text at commit `cfdb891…` | HOLD | — | `@setfilename tar.info @include version.texi @settitle GNU tar @value{VERSION}` (8 w) | raw 4–5 / text 60 | The commit identity comes from the fetch URL `id=cfdb891…` (`manifest-retry.json`). The body does not carry it. The withdrawal is correct. |
| 10 | :75–76 (erratum) | "not evidence of release 1.35; it uses `@value{VERSION}`" | HOLD | — | same as #9 (8 w) | `@value{VERSION}` at raw 5, 46, 80, 672, 3011, 4041, 8146, 8194, 9734, 9912 | Confirmed: `@value{VERSION}` occurs 10 times and "1.35" is absent from both the raw and the text view. |
| 11 | :76–77 (erratum) | Exclusion-default quotes at lines 8587–8588 and 8602 "remain supported" | HOLD | — | `Default is @option{--no-anchored} for exclusion members and @option{--anchored} inclusion members.` (10 w); 8602 quote as #5 | raw 8587–8588, 8602 | Verified on raw. Lines 8587–8588 hold the `--no-anchored` default. Line 8602 holds "When wildcards match slash (the default for exclusion members)". |
| 12 | :77–79 (erratum) | SOURCES range 8478–8617 and "gate range" 8478–8603 both contain those lines | HOLD | ANCHOR note (not superseded) | `@end menu @node controlling pattern-matching @unnumberedsubsec Controlling Pattern-Matching` (8 w) | raw 8478–8481; 8587–8588 and 8602 inside both ranges | Containment is true. The "gate range" 8478–8603 occurs only at `corpus/lessons/round-20.md:210`. A grep of `corpus/`, `w1/`, `contract.json`, and `population.json` found no other occurrence. 8478–8617 omits raw 8618 (the Exclusion default row). 8478–8603 cuts mid-sentence at raw 8603–8604. |

Verdict legend: HOLD = teaches and scope still supported at the anchor. STALE = none.

## Flags (superseded version, date, or anchor)

- **DATE (#2, #3).** The 2026-10-19 verification date is superseded for S008 by the 2026-10-21 re-fetch. The quoted content is unchanged. This is not STALE. An optional append-only note is given below.
- **VERSION (#4).** "GNU tar 1.35" is superseded. The round-20 erratum at :73–74 withdraws it in place, and this re-check confirms the withdrawal is correct. No new correction is required.
- **ANCHOR (#12).** Not superseded, but narrower than the defining table. `SOURCES.md:16` and `population.json:197` use 8478–8617, which ends at the Inclusion row (raw 8617) and omits the Exclusion default row (raw 8618). The knowledge entry does not cite 8618 and does not depend on it, so no verdict changes.

Optional append-only note (not STALE, not counted in `corrections`, for L1's discretion):
> Re-verified 2026-10-21 (S008 attempt 2, HTTP 200, 512,359 bytes, sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084). The Controlling Pattern-Matching heading (raw line 8481), the `--no-anchored` default (raw 8587–8588), and the wildcards-match-slash default (raw 8602) are present at those raw lines. The body contains no "1.35" string and takes its version from `@include version.texi`.

## Method

1. Located S008 citations with grep (:1, :34, :73) and mapped reliance by reading the full entry (:2, :20, :36, :43–54, :67, :74–79). Other lines were checked and are not S008-dependent. Examples: :7–12 (S001 action behavior); :14–18 (r20 base correction); :21–33 (S001–S006 bullets); :38–41 (dotfile rechecks); :56–62 (named debt and CNAME prediction; `CNAME` matches no pattern, since every pattern starts with `.`); :64–69 (QUALITY mapping, apart from :67).
2. Quote check, in code: all 7 distinct quotes used above are present exactly once in the text view, with 3–23 words each.
3. Anchor check, on raw bytes: 8478 `@end menu`; 8480 `@node`; 8481 heading; 8586–8588 default; 8602–8604 wildcard sentence; 8617 Inclusion row; 8618 Exclusion row. Raw sha256 matches the manifest.
4. Sibling notes in `w1/` (`FetchCritic.md` §9; `ClaimCritic.md` lines 33–37) describe the same single-line normalization. My exact rule check confirms it. I did not rely on them for any verdict.

## Verification gaps

- The repro (:43–51) was not re-executed. Its scratch directory uses `mktemp`, which writes under /tmp, and lane bounds bar that. Only its S008 reliance was judged.
- No earlier S008 bytes are retained, so there is no pre-2026-10-21 sha256 to diff. Freshness rests on quote presence and raw line anchors, not on byte identity with the original fetch. Because the URL is commit-pinned, content should be stable. [INFERENCE]
- The body does not carry its commit id (`cfdb891` is absent from the text view). Commit identity rests on the fetch URL.
- The manual's release identity cannot be read from this body, because `version.texi` is not retained. "Not release 1.35" is shown only by the absence of "1.35".
- Rendering: :34–35 shows Texinfo-rendered backticks where the source has `@option{}`. The verbatim check uses the source form.

## Tooling

No tools installed or upgraded. Python standard library only, in the eval kernel, held in memory. No writes outside this report, no /tmp use, no network calls, and no builds, tests, or linters. `RULES.md` was not needed, since nothing was installed.

## Observations outside this pair (for L1; not verdicts)

- `SOURCES.md:16` and `population.json:197` anchor 8478–8617 omits raw 8618 (Exclusion default row). Consider widening to 8478–8618.
- `corpus/lessons/round-20.md:210` anchor 8478–8603 ends mid-sentence (raw 8603–8604). It is the sole origin of the "gate range" that the erratum cites.
- The pinned URL at :1 and the commit pins at :2 belong to S001 and belong to the S001 × ghp-served-set pair.

```json
{"pair":"S008xghp-served-set","statements":12,"hold":12,"stale":0,"corrections":[]}
```
