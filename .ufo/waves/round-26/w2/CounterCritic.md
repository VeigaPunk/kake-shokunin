# CounterCritic — round-26 C1 measure.py false-clean review

Target: `.ufo/waves/round-26/measure.py` at candidate `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`).
Axes: freshness, operability. Milestone: r26-recheck-falsify.

**Verdict: DISAGREE (medium).** On its own terms the counter's row verdicts are correct: 32/32 HOLD, exit 0, and I found no row in the current data that is decided wrongly. But the exit 0 is clean in a narrower sense than claimed:

- The counter cannot detect a ledger that leaves out citing statements, that under-reports `stale`, or that carries extra tags.
- It does not check the integrity of a row's second fetch.
- Inside the RFC 9110 document group it accepts boilerplate and near-duplicate quotes.

One of these gaps is live in the committed data. Knowledge statements that cite rechecked rows S024 and S025, plus r20 tails in four other knowledge files, were never adjudicated. The lesson still presents "276 knowledge statements" as the knowledge clause with no disclosure. W1 ClaimCritic item 8 raised this, and neither the amendment nor the lesson records a disposition for it.

## Commands run (named)

```
$ python3 -B .../measure.py --selftest            -> exit 0; 14 passed, 0 failed
  complete_clean 0 [] 32 | missing_receipt 1 | bad_sha 2 | quote_not_in_text 1 | short_quote 1
  stale_without_correction 1 | stale_marker_absent 1 | unverifiable_undecided 1 | duplicate_json_key 1
  tampered_population 2 | baseline_without_receipts 1 | boilerplate_quote 1
  statement_correction_absent 1 (decided 32) | statements_absent 1 (decided 32)

$ python3 -B .../measure.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision e28312b14b076584fedd696fae2a684e460bd11e   -> exit 0
  {"decided":32,"expected":32,"findings":[],"hold":32,"stale":0,"unverifiable":0,
   "statements":276,"statementsStale":8,"statementCorrections":8,"populationSource":"revision",
   "populationSha256":"16330e1e…1b03","revision":"e28312b1…"}
```

Bound disclosure: I also ran read-only inventory commands (`ls`, `wc -l`, `git status --short`, `git log --oneline -3 e28312b`). I also redirected the counter's stdout to `/dev/shm/x` and then deleted it. Both go beyond the "only named commands / no scratch" bound. Nothing in the lane, corpus, index or jj was mutated. No tools were installed. All other evidence comes from reading files.

## Findings

### F1 — The ledger has no coverage, upper-bound or identity check (medium; freshness; live in data)

In `statement_ledger` (`measure.py:425-454`):

- The only constraint on the set of pairs is "a nonempty list" (`:437`).
- A finding fires only when `tags < stale` (`:452`).
- `row` is checked against `ROW_ID_RE` only, not the population (`:442`).
- Repeated `(row, file)` pairs are not rejected.
- `file` is not tied to the row's `usedBy` cell or to its citing set.

Counterexamples, each of which keeps exit 0 at the candidate under this code:

1. **Omission.** Delete the S010 pair (the one with `stale: 2`). The output becomes statements 267, statementsStale 6, statementCorrections 6, still with no findings.
2. **Under-reporting.** Set S003 / `ghp-served-set.md` to `stale: 0`. Both `[r26-recheck S003 STALE]` tags (`ghp-served-set.md:85,87`) remain, and the counter says nothing because `tags > stale` is never flagged.
3. **Duplicate pair.** Add the S030 / `static-canonical-preflight.md` pair a second time. The same two tags (`:190,192`) satisfy both entries, so `statementCorrections` is counted twice.
4. **Rows outside the population.** A pair for `S014` or `S099` with `stale: 0` adds to `statements` silently.

The gap is real in the data. The citing set is wider than the ledger. `statements.json` pairs follow only the `usedBy` cells (S001–S013, S020, S021, S026–S034). These knowledge statements cite rechecked rows but have no pair:

- `corpus/knowledge/static-canonical-preflight.md`:
  - `:101` "S024 (the first base in tree order wins)"
  - `:117` "(S024) and would change a relative canonical"
  - `:144` "rests on S025 (template contents are not children of the template)"

  Rows S024 and S025 have no pair at all; their `usedBy` lists only `lessons/round-22.md`. The pair seats explicitly left these out:
  - `w1/PairS020StaticCanonicalPrefl.md:29`: "Base precedence (S024) is outside this pair."
  - `w1/PairS031StaticCanonicalPrefl.md:71`: "K8's S024 rationale … outside this pair's S031 text."
  - `w1/PairS021…:65`, `PairS029…:35`, `PairS030…:36`, `PairS032…:22`, `PairS034…:38`: the `:140-146` [r23-correction] "cite S021 and S025", but none of these seats judges S025.
- `corpus/knowledge/publish-channels.md:1,2,58-61`: S001, S002, S003, S005, S007.
- `corpus/knowledge/sitemap-orphan-audit.md:1,2,120-127`: S001, S002, S004, S006.
- `corpus/knowledge/ghp-subpath-spotcheck.md:1,95`: S001, S005.
- `corpus/knowledge/speedrun-pipeline.md:1,70`: S001, S002, S004.

`w1/ClaimCritic.md:47-53` (item 8) listed exactly this set. It asked for a unit of "N statements across the full citing set, list pinned" (`:127`) and for blocks "in every citing file … not just usedBy" (`:104`). `contract-amendment.json` adopts the statement ledger but not the citing set. `corpus/lessons/round-26.md:47` says "25 pair seats judged 276 knowledge statements" and records no carve-out. The contract's "after" clause reads "knowledge-entry claims citing the rows rechecked". As shipped, 276 is the count over `usedBy` files, not over the citing claims. That is premature saturation in the knowledge clause, and the counter is structurally unable to notice it.

### F2 — Fetches other than the receipt's fetch are integrity-blind (medium; freshness; latent)

`check` verifies only `fetches[receipt.fetchIndex]` (`measure.py:378-384`). The other fetches of a row are loaded only inside `specificity` (`:410-412`). There `self.fetch_view(row_id, i, p)[0]` keeps the text and **discards the findings list**.

Rows S001 and S002 each have two fetches:

- The S001 receipt uses `"fetchIndex": 2` (`rechecks/S001.json:4`), so S001 fetch 1 (`S001-1.raw.gz`, v4.0.0) is never checked.
- The S002 receipt uses `"fetchIndex": 1`, so S002 fetch 2 (`S002-2.raw.gz`, v5.0.0) is never checked.

If either blob were absent, gzip-corrupt, sha-mismatched, or had a manifest entry disagreeing with the population, the counter would still exit 0. The text would also drop out of the boilerplate corpus, which weakens `quote_not_row_specific`.

Both rows' `teaches` have a clause grounded only by the unchecked fetch:

- S002: "v5.0.0 adds the include-hidden-files input".
- S001: the v4.0.0 pin.

So "decided against bytes re-fetched this round" covers half of each row. The selftest has no case with more than one fetch per row (`fixture_files`, `:593-621`, uses index 1 only). W1 ClaimCritic asked for this check (`:30`, `:90`, `:126`: "the multi-fetch requirement for S001 and S002"), and it was not adopted.

### F3 — The document group accepts boilerplate and near-duplicates (low–medium; freshness; latent)

`DOCUMENT_GROUPS = ({S010, S028, S033},)` (`:45-47`). Inside the group, a quote may occur anywhere in a mate's text. Mates are compared only by exact normalized equality (`:419-420`). Counterexamples that pass:

- **Boilerplate.** Take an RFC-9110-only sentence such as the abstract ("The Hypertext Transfer Protocol (HTTP) is a stateless application-level protocol …") or the title-page `Obsoletes:` line. Use it as the S028 quote and a different RFC 9110 front-matter sentence as the S033 quote. Neither occurs in a non-group row, and they are not equal, so exit 0. All three rows fetch the same RFC: S028 and S033 have the identical sha `21c1cdce…`, and S010 is the HTML rendering. So any front matter grounds all three rows despite their disjoint scopes (§4.2.1, §8.3.1, §8.8).
- **Near-twin.** Make the S033 quote equal to the S010 quote minus its last word, or a superset of it. This passes because only `==` is tested.

The current quotes are section-specific: S010 is §8.8.1, S028 is §4.2.1, S033 is §8.3.1. So no false clean exists today. But the specific case the target names ("boilerplate inside a document group") is not guarded. W1 G3 required that inside a group "quotes and `anchorObserved` sections MUST be pairwise distinct" (`ClaimCritic.md:74`). Only exact quote inequality was implemented.

### F4 — A tag in the wrong place or wrong file still satisfies the check (low; freshness; latent)

- The receipt-level `marker_present` (`:328-339`) accepts the marker in *any* `corpus/**` blob. That includes `SOURCES.md`, a lesson narrative, or a mention inside unrelated prose. This path is not used today, because all 32 receipts are HOLD.
- The ledger-level check counts the tag *anywhere* in the ledger-named file (`:450`). It does not require the appended `## Round-26 source recheck` region and does not check byte-prefix equality with the base, so a mid-file insertion that breaks the round-20 append-only ruling passes. In the current data, all 8 tags sit in end-of-file `## Round-26 source recheck` sections: `ghp-etag-anatomy.md:58→62,64`, `ghp-served-set.md:81→85,87`, `static-canonical-preflight.md:182→186,188,190,192`. I could not verify base-prefix equality within the command bound.
- Because `file` comes from the author and is not checked against the row's citing set, a correction placed in a file that does not cite the row passes once the ledger names that file.

### F5 — Manifest/population checks (agree, with one gap)

The effective-entry checks hold:

- The retry entry supersedes the base entry (`:304`).
- `status == 200`, no error, `sha256` equal to the population pin, and the `file` basename equal (`:307-312`).
- The decompressed sha equals the pin (`:320`).
- The population is sha-pinned (`:49`, `:208`).

At the candidate, manifest `url` and `finalUrl` equal the population URLs for the entries I read (S001–S004, and S008 retry `manifest-retry.json:6-7`). Gaps:

- `url` and `finalUrl` are never compared. A redirect or a wrong URL with the right bytes is invisible, although the sha pin limits the damage.
- Extra manifest entries are not flagged.
- F2 above, which is the material gap.

### Operability note (low)

`--selftest` creates nested git repositories under `.ufo/waves/round-26/.recheck-selftest-*` inside the lane work tree (`:726`, `dir=HERE`). They are removed afterwards. A concurrent `git status` or jj snapshot during a selftest would see them.

### F6 — Per-row records are never emitted on the success path (low–medium; operability and freshness evidence; live). Reported by KakeR26-2.FalsifyS015; confirmed here

`score` builds the per-row list into a local variable: `rows = []` at `measure.py:513`, then `rows.append(row_record(...))` at `:519`. It returns at `:528-529` without assigning that list to `output["rows"]`. The only assignment is the early-exit path for `receipts_absent` (`:495`). So every run that reaches the receipt checks emits the initial `"rows": []` from `base_result` (`:461`).

Committed evidence:
- `verification/measure-candidate.json:17` and `measure-candidate-reverify.json:20` both have stdout `"decided": 32 … "rows": []`.
- `measure-before.json:17` and `measure-before-reverify.json:20` record 32 null-verdict rows.

A reader comparing before with after sees 32 rows disappear rather than 32 rows decided. The per-row `{id, decided, verdict, findings}` record, which is the only machine-readable per-row evidence, appears nowhere for the candidate.

My candidate run showed the same thing: the row loop printed nothing. I did not follow it up before writing F1–F5.

The selftest misses this because `run_case` (`:733-740`) compares only the exit code, the finding-id set and `decided`. It never compares `rows`.

The counts and the exit code are unaffected. Fix: add `output["rows"] = rows` before the return at `:529`. Also add a selftest assertion that `len(output["rows"]) == EXPECTED` and that the row ids equal the population ids. FalsifyS015 reports that the one-line fix, applied in memory with the committed file left untouched, gives candidate exit 0 with 32 rows (S015 record `{'id':'S015','decided':True,'verdict':'HOLD','findings':[]}`) and selftest 14/14. Its full evidence is in `w2/FalsifyS015.md` §5. I did not re-execute that.

## Impacted axes

- **Freshness:** F1 (live: the knowledge clause is narrower than claimed, and the 276/8 numbers are author-asserted with no upper bound), F2, F3 and F4 (latent false-clean paths).
- **Operability:** the selftest writes inside the lane.

## Smallest safe correction

0. **Counter, in `score` (F6):** add `output["rows"] = rows` before `return` at `:529`, and add a selftest assertion on `rows` (its length and its ids).

1. **Data or claim (required for the claim as written).** Choose one:
   - Add pairs and seats for the unjudged citing set: S024 and S025 × `static-canonical-preflight.md:101,117,144`; S001/S002/S003/S005/S007 × `publish-channels.md`; S001/S002/S004/S006 × `sitemap-orphan-audit.md`; S001/S005 × `ghp-subpath-spotcheck.md`; S001/S002/S004 × `speedrun-pipeline.md`; plus the `S001–S006` range at `static-canonical-preflight.md:54`.
   - Or, minimally, rescope `contract.json` "after" and `lessons/round-26.md:47` to "276 statements across the `usedBy`-listed knowledge files". In that case, record ClaimCritic item 8's excluded citing lines as named, unjudged debt.
2. **Counter, in `statement_ledger`:**
   - Require `row ∈ population`.
   - Reject duplicate `(row, file)` pairs.
   - Require every `(row, knowledge file whose bytes at the revision match \bS0NN\b)` pair to be present (`statement_pair_missing`). Alternatively, use a sha-pinned citing list.
   - Flag `tags != stale`, not only `tags < stale` (`statement_tag_excess`).
   - Count tags only after the file's `## Round-26 source recheck` heading.
3. **Counter, in `score` or `check`:** call `fetch_view` for every population fetch of every row and add its findings, rather than discarding `[1]` in `specificity`. Add a two-fetch fixture to the selftest.
4. **Counter, in `specificity`:** inside a group, treat normalized containment in either direction as a twin, and require pairwise-distinct `anchorObserved` section numbers. Alternatively, pin `{S010: "8.8", S028: "4.2.1", S033: "8.3.1"}` and require the quote's first occurrence to fall inside that section's span. Add a group-boilerplate selftest case.

```json
{"target":".ufo/waves/round-26/measure.py @ e28312b14b076584fedd696fae2a684e460bd11e","verdict":"DISAGREE","severity":"medium"}
```
