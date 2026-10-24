# ClaimCritic — round 26 C1 (freshness), pre-result attack

Seat: critic, read-only. Inputs read: `contract.json`, `population.json`,
`w1-spec.json` (Row/Pair/RecheckCounter prompts), `fetch_sources.py`,
`source_text.py`, `fetched/manifest*.json`, all 34 `fetched/text/*.txt`,
raw `fetched/*.raw.gz` (gunzip in memory), `corpus/QUALITY.md`,
`corpus/SOURCES.md`, lessons round-20/22/23/24, `scripts/sources-census.sh`
header (fleet repo, read only). No tools installed. No build/test/lint run.
All checks below are in-memory reads of retained bytes.

## Verdict

As written, "32/32 decided" is **falsifiable but nearly vacuous**. It fails
on an honest UNVERIFIABLE (good). But a HOLD only needs *any* 6–25-word
substring of the row's own text view, so it can be satisfied by page chrome.
The "knowledge-entry claims rechecked" clause has no unit or count. The
STALE check (the tag appears "in some corpus/** file") does not prove that
the round-20 append-only rule was followed. Every defect has a small fix,
listed under Smallest safe correction at the end.

## Counterexamples (local evidence)

1. **Boilerplate HOLD passes the counter.** `Back to top Help and support Was this Doc helpful? Yes No` appears in all six docs.github views: S003, S004, S005, S006, S007 and S015. It has 11 words and is word-bounded. Under the RecheckCounter rules it would ground HOLD for all six rows. Other strings do the same for their groups:
   - `HTML Living Standard — Last Updated 20 October 2026` appears in all five WHATWG views: S023, S024, S025, S030 and S031.
   - `| next | previous | Python » 3.15.1` appears in S026 and S027.
   - Google chrome is shared by S013, S021 and S022 (940 common 8-word shingles).
   - The two GitHub release pages (S002 fetches 1 and 2) share 352 shingles, for example `Uh oh! There was an error`.
2. **The single-quote receipt cannot ground multi-clause or multi-URL rows.**
   - S001: the anchor (`inputs.include-hidden-files lines 17-20 … 37-39`) is true only for fetch 2, main `5f32701`. In fetch 1 (v4.0.0, `7b1f4a7`), raw lines 17-20 are `outputs: artifact_id`, and the string `include-hidden-files` is absent. A HOLD with `fetchIndex:1` therefore cannot ground the teaches.
   - S002: the teaches has a v4.0.0 clause, grounded by fetch 1 (`Potentially breaking change: hidden files (specifically dotfiles) will not be included`), and a v5.0.0 clause, grounded by fetch 2 (`feat: add include-hidden-files input`). One quote grounds only half the row.
3. **The same bytes back three rows.** S028 and S033 have the identical effective sha256 `21c1cdce…47232a`, and S010 is the HTML rendering of the same RFC 9110. One quote can satisfy all three receipts. Their scopes are disjoint (§4.2.1–4.2.2, §8.3.1, §8.8), and nothing enforces that.
4. **Line anchors cannot be checked against the text views.**
   - Every `fetched/text/*.txt` is a single line (`wc -l` totals 34 lines across 34 files), because `normalize()` collapses all whitespace.
   - So the line anchors in S001 (17-20, 37-39), S008 (8478-8617) and S009 (1682, 1708-1710) are checkable only on `gunzip(raw).split('\n')`.
   - Observed on raw: S001 fetch 2 lines 17-20 and 37-39 match. S009 line 1682 is `ngx_http_set_etag` and lines 1708-1710 are the `"%xT-%xO"` sprintf. In S008, line 8478 is `@end menu`, the node is at 8480, and lines 8617/8618 are the defaults table — the same content as the anchor, starting 2 lines later.
5. **The text views lose information.** The rule `\s+([,.;:)\]])→\1` rewrites dotfile names:
   - S001-2 reads `Excludes.git and.github regardless`; the raw has `Excludes .git and .github regardless`. A verbatim copy of the raw text is therefore *not* a substring of the text view.
   - S006 reads `Start with _,., or #`.
   - S017 reads `Add a./public/CNAME`.

   The counter normalizes both sides, so binding is consistent. However, the seat instruction ("VERBATIM from fetched/text") and a reviewer reading the raw bytes will disagree, and a semantic judge reading the text view may misread dot-prefixed paths.
6. **The rejected rows' flip conditions cannot be decided from their own bytes.**
   - S017's flip is "GitHub docs say the CNAME file is honored under Actions". That needs S005's bytes, not Astro's. S005-1 still says `any existing CNAME file is ignored and is not required.` (2 hits).
   - S018's flip needs a tier-A Firefox source. The Firefox 144.0 cross-check (round-20.md:220) was **not re-fetched**. S018-1 still says `Mozilla released version 114 of Firefox on the 14th of October 2025.`
   - The receipt schema only allows a fetchIndex within the row's own fetches.
7. **The STALE tag check can be met without a correction.** The counter accepts any `corpus/**` file containing `[r26-recheck S0NN STALE]`. That could be a lesson narrative, QUALITY prose, or a mid-file insertion that breaks the round-20 ruling. Nothing ties the tag to the row's citing file, to an EOF position, or to a STALE receipt (an orphan tag on a HOLD row would be false provenance).
8. **The knowledge clause is unmeasured, and pair coverage is narrower than the citing set.** The 25 Pair seats follow only the `usedBy` cells. Statements that cite rows elsewhere have no seat:
   - `knowledge/publish-channels.md:58-61` (S001, S002, S003, S005, S007)
   - `knowledge/ghp-subpath-spotcheck.md:95` (S001, S005)
   - `knowledge/sitemap-orphan-audit.md:120-127` (S001, S002, S004, S006)
   - `knowledge/speedrun-pipeline.md:70` (S001, S002, S004)
   - `knowledge/static-canonical-preflight.md:101,117,144` (S024, S025 — rows with **no pair seat at all**; their `usedBy` lists only `lessons/round-22.md`)
   - the range citation `S001–S006` at `static-canonical-preflight.md:54`

   QUALITY.md:18 ("Population unit named") requires the unit and the command.
9. **The counter that measures the claim does not exist yet, and its paths disagree.**
   - The contract's `count` is `python3 -B .ufo/waves/round-26/measure.py`, which is absent.
   - RecheckCounter writes `sandbox-counter/measure.py`.
   - The receipt path `rechecks/S0NN.json` appears only in the counter prompt, not in the contract.
   - `.ufo/waves/round-26/` is entirely untracked (`git status`: `??`), so a revision-bound replay currently has nothing to read.
10. **32/32 HOLD is the expected outcome (saturation risk).**
    - Rows were opened 2026-10-19..21 and none is overdue under its own cadence.
    - Seven rows are byte-identical to digests recorded when they were opened: S028 and S033 (round-24.md:32), S032 (round-24.md:31), S034 (round-24.md:33), S030 and S031 (round-23.md:207 and :210), and S029 (`3102dae4…b2d683`, its SOURCES anchor).
    - All 40 opening-quote fragments in lessons round-20:202-220, round-22:43-50 and 183-184, round-23:60-61 and round-24:31-33 survive in today's effective fetch. The only miss is S001 fetch 1, which is expected because v4.0.0 has no such input.
    - The result is a valid dated receipt, but it carries no evidence of improved quality.
11. **The round-23 digest columns are swapped (trap).** round-23.md:60-61 lists S030 → `a11dcf17…` and S031 → `04b65bf0…`. Today S030 is `04b65bf0…` and S031 is `a11dcf17…`, which matches the appended register at round-23.md:206-212. A seat that compares against lines 60-61 would wrongly report drift.

## Per-row HOLD conditions

These rules apply to every row. HOLD MUST satisfy all of them. A failure means STALE if the content changed, or UNVERIFIABLE if the bytes cannot decide.

- **G1 – quote binding.** `normalize(quote)` is a word-bounded substring of `normalize(text_of(gunzip(raw)))` for the *effective* fetch. For S008 the effective fetch is the retry `S008-1-retry.raw.gz` (sha `93281a63…`); the failed attempt has empty-body sha `e3b0c442…` and is never effective. The receipt quote may be copied from the raw bytes; binding is on normalized text.
- **G2 – teaches grounding.** Each `;`-separated teaches clause gets its own quote and fetchIndex. A clause that only points to another row (S001: "separately evidenced by S002") is exempt only if it names that row.
- **G3 – anti-boilerplate.** A HOLD quote MUST NOT occur in the effective text of any other population row, except inside a same-document group, currently {S010, S028, S033}. Within a group, quotes and `anchorObserved` sections MUST be pairwise distinct.
- **G4 – opening-quote survival.** The row's opening quote, as recorded in the lesson path:line cited above, survives under G1. If it does not survive, HOLD requires a replacement quote plus a reason, and is gated by review rather than counted mechanically. Today every row passes this check on its anchor fetch.
- **G5 – anchor.** The rule depends on the anchor type:
  - Section anchors: `anchorObserved` names a heading string that exists in the text view, and the reason says whether the anchor moved.
  - Line anchors (S001 fetch 2, S008, S009): verified on raw lines and reported as `raw:L-L`.
  - A moved anchor with the same content is HOLD with the drift recorded, for example S008 starting at 8480 rather than 8478.
- **G6 – dated or versioned anchors.** A HOLD without a note requires the observed date or version to equal the anchor's. Today's values:
  - S013 `Last updated 2026-07-08 UTC`, S021 `2026-07-10`, S022 `2026-08-21`.
  - WHATWG rows: `Last Updated 20 October 2026`.
  - S018: `Updated on March 19, 2026`.
  - S026/S027 show **`Python 3.15.1`** against the anchor's "Python 3.15". The minor-version pin still holds, so this is HOLD with the patch level in `anchorObserved`, provided the quoted text is unchanged.

Rules that apply only to specific row classes:

| class | rows | extra condition |
|---|---|---|
| Pinned by content (commit/id) | S001, S008 | Both S001 fetches are judged: fetch 1 proves `--exclude=.git`, `--exclude=.github` and `--exclude=".[^/]*"` are unconditional at v4.0.0; fetch 2 proves the input and lines 17-20/37-39. |
| Pinned by mutable ref | S009 (tag `release-1.28.0`) | Bytes are tag-resolved. The receipt states that commit `481d28cb` identity is not proven by this fetch. |
| Release HTML for immutable tags | S002 | Two quotes (fetch 1 → v4 clause, fetch 2 → v5 clause). Body text is present despite dynamic `Uh oh!` fragments. |
| Immutable spec (RFC) | S010, S011, S020, S028, S029, S032, S033, S034 | Where a digest was recorded at opening (S028, S029, S032, S033, S034), digest equality is primary evidence, citing the path:line of that digest. Otherwise G1–G5 apply. |
| Living docs/specs | S003–S007, S012, S013, S015, S021–S027, S030, S031 | G3 is mandatory, because chrome collisions are proven. For S030/S031, digest equality is evidence only against round-23.md:206-212, never :60-61. |
| Dated value pin | S016 | Values must equal today's values (they do: `"jekyll":"3.10.0"`, `"github-pages":"232"`). The "At fetch time" wording never licenses HOLD on changed values; a changed value is STALE. |
| Rejected | S017, S018 | HOLD means the flip condition is not met, and the receipt must say what decided it. S017 cites S005-1 (`any existing CNAME file is ignored and is not required.`). For S018, the rejection stands by default, but the reason MUST state that the tier-A Firefox cross-check was not re-fetched. That is a tradeoff the judge should accept only if disclosed. |
| Queued, no citer | S015, S016 | The only citing file is `lessons/round-20.md:217-218`. |

QUALITY.md:146-147 applies: a gone surface is UNVERIFIABLE and is never relabelled HOLD.

## STALE corrections (round-20 ruling, QUALITY.md:31-41)

- Every base line of `corpus/knowledge/**` and `corpus/lessons/**` stays byte-identical. Corrections are pure end-of-file blocks tagged `[r26-recheck S0NN STALE]`. Each block cites the old `file:line` at **base** coordinates, the effective fetch sha256, and the new quote. Never add a suffix to an old line (that criterion was rejected), never split a table, and never add an adjacent note without an inbound-pointer movement census.
- Place a block in every citing file whose statement depends on the stale clause: the full citing set from counterexample 8, not just `usedBy`. For S015–S018 that file is `lessons/round-20.md`.
- **SOURCES.md:** do not edit the teaches, anchor or scope cells. If status, recheck or used-by cells change:
  - `recheck` must still match `sources-census.sh` E09 (ISO date, `NNd`, or symbolic).
  - Every used-by path must exist (E11).
  - No `|` is allowed in correction text (E01).

  An appended recheck log MUST NOT use `| S0NN |` row-shaped lines outside `## Registry`, because E12 would exit 1. Use bullets, or the `rechecks/` sidecar. Precedent: round-21.md:45 left the S001–S018 cells unchanged.
- Correction blocks carry no absence vocabulary unless they are absence notes, to avoid ±2-line annotation bleed in the freshness sweep (QUALITY.md:162).

## No-harm checks (for L1 to run on the candidate; not run here)

1. **Prefix check.** For each changed `corpus/**` file other than SOURCES.md, `cand.startswith(git show 97404de:file)`. The appended region contains only `[r26-recheck S0NN STALE]` blocks, apart from new files such as `lessons/round-26.md`. This also proves that no inbound line pointer moved.
2. **SOURCES.md.** Header and preamble are byte-equal. Rows S014, S019 and S035 are byte-equal. In the other rows, only status, recheck and used-by cells differ, and each difference is logged. `scripts/sources-census.sh validate --file corpus/SOURCES.md` output equals `census-before.txt` (only `W04 S033 duplicate url`, exit 0).
3. **Tags match receipts.** The set of tagged ids equals the set of STALE receipts. Each tag sits in the appended region of a file in that row's citing set. No tag exists for a HOLD or UNVERIFIABLE row.
4. **Population and bytes.** The pinned population sha matches; the population has 32 ids, equal to the external SOURCES rows at base minus S014/S019/S035. For each fetch, sha(gunzip(raw)) equals the manifest sha and the population sha, and S008 resolves to the retry. Each text view equals `text_of(gunzip(raw))` (RecheckFixtures).
5. **Receipt distinctness.** Apply G3, plus no duplicate quote across receipts.
6. **Earlier gates unchanged against base.** Run `node scripts/freshness-sweep.mjs --selftest` and its path section, and confirm no new unannotated citations from appended blocks. Replay `round-24/measure_c1.py` and `measure_c2.py` at the candidate.
7. **Diff scope.** `git diff --stat 97404de..cand` touches only `.ufo/waves/round-26/**`, appended `corpus/**` tails, allowed SOURCES cells, and the new lesson. No earlier round's evidence is touched.

## Smallest safe correction

- **Receipt schema.** Replace the single quote with `quotes:[{clause,fetchIndex,quote,anchorObserved}]`. Add an optional `crossFetch` field for rejected rows (S017 → S005-1). Add `digestMatch` with the path:line of the opening digest.
- **Counter.** Add G3 (cross-row collision, with the same-document group allowed list), G4 (an opening-quote table pinned with its lesson path:line), the multi-fetch requirement for S001 and S002, line-anchor checks on raw bytes, and stronger tag rules (citing set, appended region, STALE only). Keep the existing rules: exit 1 on UNVERIFIABLE, and no relabelling.
- **Contract.** Fix the count path, or state the move from `sandbox-counter/` to `measure.py`. Name the receipt path. Give the knowledge clause a unit: "N statements across the full citing set, list pinned".
- **Lesson framing.** Report the expected saturation honestly: "dated receipts exist; 7 rows byte-identical to their opening digest; 0 overdue by cadence". Do not present it as a quality-trend gain.

Impacted axes: freshness (vacuous HOLD, the swapped-digest trap, the
unmeasured knowledge clause) and operability (counter path, single-line
text views, the E12/E09/E01 traps in the census).
