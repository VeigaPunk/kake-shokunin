# Pair08A — (S005, corpus/knowledge/static-canonical-preflight.md) — r27 C1 source adjudication

Seat: KakeR27.Pair08A (reviewer, read-only). Axis judged: **freshness**. Lane: kake-shokunin. Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`. No production/source/ledger/state edit, no subagent dispatch, no builds/lint/tests, no tool installed or updated; scratch: none outside this report. r24 policy-stop / L0 stopped work was not read, retried, rephrased or rerouted.

## 1. Verdict

**HOLD** (source row S005), scoped to S005's own stated scope, with the inferential step of the grouped recommendation labelled explicitly. Not STALE; not UNVERIFIABLE; not a stale premise; not source-date drift; not retry boilerplate. The grouped recommendation at `corpus/knowledge/static-canonical-preflight.md:53–54` is **local synthesis**, not a claim that S005 alone entails it; S005's contribution is real but bounded to the **domain-configuration leg** (§3). All evidence paths are cited inline; this seat made no source, ledger or state edit.

## 2. Citing location (exact)

`corpus/knowledge/static-canonical-preflight.md` (203 lines) contains **exactly one** S005-citing line — exhaustive literal scan of `corpus/knowledge/` for `S-?005\b`: the 13 other hits are in `ghp-custom-domain.md`, `ghp-subpath-spotcheck.md`, `publish-channels.md` (adjudicated in r26) and `sitemap-orphan-audit.md` (a different missing pair, not this seat's); no `S5`/`S-005` variant forms exist, so no undiscovered citing form is omitted.

Citing lines (sentence spans 53–54; the citation token is on **line 54**): L53 `manifest over actual built/deployable HTML when that artifact exists, not over` / L54 `an assumed checkout served set (S001–S006, \`ghp-served-set.md\`). No production`.

`(S001–S006, ...)` is a **range** (en-dash); expanded per `count_c1.py`'s RANGE regex it yields S001…S006 → six pairs `(S001…S006, corpus/knowledge/static-canonical-preflight.md)`; S005 is one. This is the known r26 gap named at `corpus/lessons/round-26-verifier-spotcheck.md:11` and `:119`. Denominator, recomputed not restated: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` → `citingPairs 57, decided 41, r26CarriedPairs 41, missing 16`; the missing list contains `S005 corpus/knowledge/static-canonical-preflight.md`. **This seat discovers no new citing pair** — the denominator stays 57, the missing set stays 16 until L1 lands the six grouped adjudications.

## 3. What the row claims, and S005's specific contribution

Claim at L53–54 (local publishing policy for the canonical preflight): *"Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`)."* Three separable legs:

- **(a)+(b) positive and content dimension** — build the manifest over the **actual built/deployable HTML artifact**, and do not treat the checkout as the served set (artifact excludes `.git`/`.github`/dotfiles). Carried by S001/S002 (`upload-pages-artifact` uploads a declared `path`), S004 (custom workflow uploads build output), S003/S006 (publishing source; Jekyll build output), S008 (+ `ghp-served-set.md`). **S005's share: none** — S005 never states which HTML is served, nor artifact membership.
- **(c) configuration dimension** — under Actions publishing the checkout does not determine the live site's configuration: no `CNAME` is created, any existing one is ignored. **S005's share: all of it** — S005 is the sole carrier.

**S005's specific contribution is leg (c) only.** For a site published by a custom GitHub Actions workflow the domain (hence the host component of every served URL) comes from **Pages settings**, not the checkout; so a manifest prepared over "an assumed checkout served set" can be wrong in its **host/URL-set** component, not only its path component. Real, non-redundant, and the only one S005 makes. Inferential step, labelled as the contract requires: the row cites a group and a companion entry, not "S005 states X". S005's leg-(c) fact entails that checkout-derived URL assumptions are unsafe in the configuration dimension; it does **not** entail legs (a)/(b), which rest on S001/S002/S004/S006/S008 and `corpus/knowledge/ghp-served-set.md`.

Precision observations (verdict unchanged): the file's `source:` header (L1) declares only S020, S021, S026, S027, S028, S029 and `verified-at:` (L2) covers "S020-S027"/"S028-S029" only, so **S001–S006 are never declared in this file's header** — the line-54 group citation is body-level and outside the file's declared verification coverage; this r27 fetch is the first grounding of these six rows *for this file*. The companion entry named at L54, `corpus/knowledge/ghp-served-set.md`, has `source: S001, S002, S003, S004, S006, S008` — it does **not** cite S005, so S005 reaches this row through the row's own range citation only; S005's registry scope (`corpus/SOURCES.md:13`) does cover the L54 use, so this is not an out-of-scope attribution.

## 4. Source evidence (retained bytes, re-read this round)

- Row `S005` — GitHub Docs: *Managing a custom domain for your GitHub Pages site*; URL `https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site`
- `fetchIndex` **1** (single public GET, HTTP 200, `fetchedAt 2026-10-21T19:59:56.085676+00:00`).
- Retained raw `.ufo/waves/round-27/fetched/S005-1.raw.gz` → 240 439 bytes decompressed, `sha256 6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4` — recomputed from the gzip, **matches** the manifest `sha256` exactly; retained text `.ufo/waves/round-27/fetched/text/S005-1.txt` (14 701 bytes).
- **Exact quote (22 words, ≤25):** *"If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored"*.
- **Anchor:** S005 §"Configuring an apex domain", step 4 (Settings → Pages → Custom domain → Save), first of two occurrences; the identical sentence recurs verbatim at §"Configuring a subdomain", step 4 (both verified present in the retained text). Full sentence for context (26 words, **not** the ledger `quote` field): "…no CNAME file is created, and any existing CNAME file is ignored and is not required."

Freshness / no-drift evidence (this axis): the r26 re-fetch (`.ufo/waves/round-26/fetched/`, sha256 `dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9`) and the r27 re-fetch (`6f3d1ad2…`) have **different raw HTML** (docs boilerplate/CSRF churn) but **character-identical extracted text** — both extractions 14 698 characters, SequenceMatcher ratio **1.0**, zero differing opcodes; the relied-on sentence and its anchor context are unchanged as of 2026-10-21T19:59:56Z, so **no source-date drift, no stale premise**. Required distinctions: **stale premise** → NO (nothing in S005 contradicts the row; its premise is local policy S005 does not falsify); **source-date staleness** → NO (anchor text byte-identical across the r26 and r27 fetches; the registry row's `fetched 2026-10-19` stamp is a historical record, not rewritten — same rule as the r26 EOF prose at `ghp-custom-domain.md:62` / `publish-channels.md:84`); **irrelevant retry boilerplate** → NO (L53–54 is a substantive operational instruction in the "Input and handoff" section — not a `recheck:` line, not a version/date stamp, not the exit-code legend at L58–L63, not an EOF historical note; it carries real freshness load).

## 5. Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json`, `pairs[]`)

```json
{
  "row": "S005",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "source",
  "verdict": "HOLD",
  "fetchIndex": 1,
  "quote": "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored",
  "anchor": "S005 (corpus/SOURCES.md:13) §\"Configuring an apex domain\", step 4 (Settings → Pages → Custom domain → Save); identical sentence repeats at §\"Configuring a subdomain\", step 4; retained bytes .ufo/waves/round-27/fetched/text/S005-1.txt, sha256 6f3d1ad215c9ad1917638c69d60732861dbc1ee758642976c8b1ce08c79e6be4, fetched 2026-10-21T19:59:56.085676+00:00",
  "reason": "Grouped recommendation at lines 53-54 is local synthesis; S005 carries only the configuration leg: under a custom Actions workflow no CNAME file is created and any existing one is ignored, so the served URL set's host component comes from Pages settings, not the checkout. Anchor sentence present verbatim in the r27 retained bytes (sha256 6f3d1ad2..., 240439 bytes) and character-identical to the r26 re-fetch extraction, so no source-date drift. S005 states nothing about which HTML is served; that leg rests on S001/S002/S004/S006/S008 and ghp-served-set.md. HOLD at S005's stated scope with the inferential step labelled."
}
```

Acceptance re-checked by hand against the counter's own logic (both the frozen `be375d9` version and the current working-tree version, §7b): manifest lookup by `(row, fetchIndex)` resolves; gzip `sha256` recomputed equals the manifest value; `quote` = 22 words ≤ 25 and a whitespace-normalized substring of the extracted S005 text; `anchor` non-empty; the pair is inside the enumerated citing set; `kind=source` satisfies the grouped-row rule for S001–S006 in this file; the quote is row-specific (absent from every other fetched row's text). **No `[r27-recheck S005 STALE]` marker is required.**

## 6. Suggested appended wording (optional precision append — not required for HOLD)

HOLD needs no correction. If L1 wants the group citation to stop reading as "six sources jointly entail this sentence", the minimal append-only wording (original lines untouched) is:

> `[r27-recheck S005 HOLD]` Line 54's grouped citation (S001–S006) is local synthesis: S005 supports only the configuration leg (under a custom Actions workflow no `CNAME` file is created and any existing one is ignored, so the served URL set's host component comes from Pages settings, not the checkout). Which HTML is served rests on S001/S002/S004/S006/S008 and `ghp-served-set.md`. Anchor text re-read 2026-10-21 unchanged (`.ufo/waves/round-27/fetched/`, sha256 `6f3d1ad2…`).

Exact wording is L1's call; this seat is findings-only and made no append.

## 7. Actionable findings for the L1 integrator (KakeR27)

**7a — retained bytes are untracked (hard blocker).** `.ufo/waves/round-27/fetched/` is **untracked in git** at `be375d9` (`git status --porcelain` → `?? .ufo/waves/round-27/fetched/`; `git ls-tree -r be375d9 -- .ufo/waves/round-27/fetched/` → **0 paths**). The counter reads blobs via `git show <revision>:<path>`, so the manifest, the `.raw.gz` files and the text views must be committed for any `kind=source` row to validate; otherwise every source row fails `source_missing` at the measured revision. r26 precedent commits them: `git ls-files .ufo/waves/round-26/fetched/` lists the `.raw.gz` files **and** 34 `text/*.txt` paths.

**7b — the declared frozen counting command was edited in the working tree (uncommitted).** `git status` shows `.ufo/waves/round-27/count_c1.py` and `c2_count.py` **modified** relative to the frozen declaration `be375d9` (30 insertions / 5 deletions in `count_c1.py`), with `.ufo/waves/round-27/oracle_selftest.py` newly added. The `count_c1.py` diff (a) forces the monotone denominator via `c1-before.json` + r26 decided pairs, (b) re-derives quote text from the **raw bytes** through the pinned round-26 helper `.ufo/waves/round-26/source_text.py` (sha256 `55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6`, verified matching on disk) instead of the r27 `text/*.txt` files, (c) adds `quote_not_row_specific`, `group_source_required` and `artifact_self_support` failure modes, (d) discards inherited r26 credit for re-adjudicated pairs, and (e) adds a `--selftest` hook. These changes **strengthen** the checks and fit the contract's monotone-denominator rule, but the contract names `count_c1.py` as the *frozen* command; an unfrozen edit to the measurement instrument must be adjudicated and disclosed by the parent, and the round record must state which version was used. This seat did not make that edit; its §5 record was re-validated against both counter versions and satisfies each.

## 8. Residual risk, uncertainties, verification gaps

- **One-source-deep inference.** S005 supports leg (c) only; legs (a)/(b) are carried by S001/S002/S004/S006/S008. If L1 records the six grouped pairs as jointly entailed by the group, the record overstates S005; the `reason` field above states the split explicitly, per contract "label the inferential step and each source's contribution".
- **Not independently re-fetched over the network.** The seat used the r27 retained bytes (fetched 2026-10-21T19:59:56Z, HTTP 200) rather than a second GET, per the retained-bytes allowance; the r26-vs-r27 extraction identity is a strong no-drift proxy but not a third independent observation.
- **Registry `used-by` gap.** `corpus/SOURCES.md:13` lists `corpus/knowledge/ghp-custom-domain.md` as S005's only using entry; this row and `sitemap-orphan-audit.md` are not listed — flagged, not corrected (registry bookkeeping, outside this read-only seat's scope).
- **Ledger mechanics not exercised end-to-end.** `pairs.json` did not exist at inspection time (`discovered-pairs.json` appeared during this seat's run with one discovered pair, S013 in `ghp-served-set.md`, raising the denominator to 58 by the predeclared monotone rule), so the counter could only run in its base configuration; the record above was validated by replicating the acceptance logic by hand against the retained bytes, not by running a finished ledger. The `quote` must appear in the *extracted text*, not the raw HTML — it does (normalized substring, 2 occurrences); a regenerated extraction needs the quote re-checked.
- Adjacent unadjudicated pairs (S022/S023 in this file via the `verified-at` range "S020-S027"; S003/S005/S006 in `sitemap-orphan-audit.md`; S008 in four files) are **not** this seat's; no judgment is offered on them and the denominator is not adjusted here.

**Reported verdict: HOLD** for `(S005, corpus/knowledge/static-canonical-preflight.md)`, scoped to S005's configuration leg, inference labelled, no STALE correction required. Recommendation only — the parent judges independently.
