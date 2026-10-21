# JudgePair10 — (S006, corpus/knowledge/static-canonical-preflight.md), kind=source, proposed HOLD

Axis: **freshness** (semantic judgment at the pair's own scope; byte bindings are other seats' scope).
Milestone: r27-fresh-falsification. Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (= HEAD, verified).
Read-only: no source/docs/registry/ledger edit, no commit/index/jj/remote change, no install, no pacman
transaction, no subagent, no build/lint/formatter. Scratch only: `/fast/scratch/hyaku/kake-r27/JudgePair10/`
(TMPDIR set there). One public GET of the named official source (no credentials/cookies/form/header state kept).
Target-file blob at candidate `7bcf31ddab3689e269ca5d085d5543dad6a2daac` == working-tree `git hash-object`
⇒ every read below is the candidate blob. `pairs.json` row read from the candidate blob.

## 0. Attacked item, verbatim

Ledger row: row `S006`, file `corpus/knowledge/static-canonical-preflight.md`, kind `source`, verdict `HOLD`,
fetchIndex `1`,
quote `By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor`,
anchor `Configuring Jekyll in your GitHub Pages site, default exclusions paragraph`,
reason `Jekyll branch builds omit specified paths by default (include/exclude configuration can change that). This supports only the Jekyll leg, not every Actions workflow; manifest advice is local synthesis.`

Citing sentence (only S006 form in this file — en-dash range `S001–S006`, lines 52–54):
`… Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`).`
Citing-file adjudication (appended lines 205–247) row S006: `HOLD, limited premise: Jekyll branch builds have default exclusions, modifiable by include/exclude settings; not every workflow uses Jekyll.` (same 18-word quote).

## 1. Independent expected results, declared BEFORE each probe

- **P1 (source opened)**: HTTP 200; finalUrl unchanged; quoted sentence present verbatim in visible text; anchor id `configuring-jekyll-in-your-github-pages-site` present; no publication date on the page. Falsify if 404/redirect, quote absent, anchor absent, or sentence materially reworded.
- **P2 (quote vs retained bytes)**: landed quote is a whitespace-normalized substring of the **retained** view (sha256 `535e55d0…`, 7676 B); manifest `sha256`/`bytes` = retained representation; `receivedSha256`/`receivedBytes` = observed HTTP body, **not** reconstructable from retained bytes.
- **P3 (counter predicate)**: quote passes count_c1's source rule (≤25 words, ≥6 tokens, row-specific) and the row is counted **decided**; C1 overall stays **unprovable** (3 carried-UNVERIFIABLE pairs ⇒ missing≠0 ⇒ exit 1) — never green.
- **P4 (dissent coherence)**: HOLD(S006) vs STALE(S005) in the same range/sentence is justified iff S005's page is *not* about file membership while S006's is.
- **P5 (freshness)**: today's live visible text == retained visible text byte-identical ⇒ no prose drift; raw HTML digests may churn without prose churn.

## 2. Actual observations

**P1** — `urllib` GET of `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll`: status **200**, finalUrl unchanged, body 138096 B, raw sha256 `d2bb9c77…` (earlier fetch this session: `b842e44c…`). Visible text via the lane's hash-pinned `.ufo/waves/round-26/source_text.py::text_of` → sha256 **`535e55d0fb1154f0fb86de1d070abebc49c75c2e8f7845c547f8d61626806910`**, 7676 chars — **byte-identical to the retained r27 view**. Quote present verbatim; anchor id present; exclusion paragraph sits between the "settings cannot be changed" list and the `Front matter` H2 (H2 order confirmed in raw HTML). No date on the page ⇒ no time-indexed premise can go stale.

**P2** — retained `fetched/S006-1.public.txt.gz` decompresses to sha256 `535e55d0…` / 7676 B == manifest `sha256`/`bytes`; `fetched/text/S006-1.txt` byte-identical to it (`cmp` equal). Manifest `receivedSha256 f0318abe…` / `receivedBytes 138096` with `retainedRepresentation.rawHttpBodyRetained:false`, `replacedFile:"S006-1.raw.gz"`. Scan of every `.gz` in the candidate: **no** file decompresses to `f0318abe…` ⇒ received HTML body genuinely absent, unreconstructable, as the manifest states. r26 retained text (`2d953b39…`, 7677 B) minus trailing newline == `535e55d0…` ⇒ no prose drift r26→r27→today. S006's view contains **none** of checkout/artifact/served/manifest/.nojekyll/canonical/upload-pages-artifact ⇒ "not built ⇒ not served" is [INFERENCE] (as both W1 seats state); the view does contain `Are excluded by the exclude setting in your configuration file` and `you can use the include setting…`.

**P3** — `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a747…` → exit **1**: citingPairs 58, reviewedPairs 58, **decided 55**, newDecided 18, missing = exactly the 3 carried-UNVERIFIABLE pairs (S001 ghp-served-set 3 u, S007 ghp-custom-domain 1 u, S033 static-canonical-preflight 3 u) = 7 u / 3 pairs. My row: `{'row':'S006','file':'corpus/knowledge/static-canonical-preflight.md','verdict':'HOLD','valid':True}` — decided, quote 18 words / 20 tokens, row-specific (no leak into S001–S005/S008 views).

**P4** — S005 retained view contains no `checkout`/`artifact`/`served`/`manifest`/`exclude`; its cited sentence is `If you are publishing from a custom GitHub Actions workflow, no CNAME file is created…` (domain/CNAME guidance) ⇒ STALE for the file-membership sentence is right, HOLD(S006) is right (S006's page is precisely about which paths a build omits). S003/S004 cross-check: S003's retained general-flow list is Trigger / checkout / **build** / **upload-pages-artifact** / **deploy-pages** ⇒ steps 4–5 are S003's, confirming the S004(ghp-served-set) STALE override and S003's anchor "flow steps 3–4".

**P5** — raw churn vs prose: r26 raw → today's raw differ in **7** regions, all Next.js build artifacts (`webpack-091b7f…`→`webpack-1fbdc652…`, three `NNNN-<hash>.js` chunks, `_buildManifest`/`_ssgManifest` build-id path, `"buildId"`). Two consecutive GETs of the same URL in my own session were **byte-identical** (0 differing bytes) while an earlier one differed ⇒ raw sha256 drift is intermittent deployment churn, not per-request noise.

## 3. Findings (severity order)

**M1 — the landed quote is a different, truncated quote than the cited A/B evidence verified.** `w1/Pair10A.md` §5 and `w1/Pair10B.md` both propose *and* verify the **24-word** quote `Jekyll doesn't build files or folders that: … /node_modules or /vendor Start with _,., or # End with ~` (also the quote in `.ufo/waves/round-26/rechecks/S006.json`). The candidate ledger and the appended table row use an **18-word** truncation that adds `By default,` and drops the `_ . #` / `~` classes *and* the exclude/include clauses. Both are truthful substrings (verified in retained and live text) ⇒ HOLD is not falsified — but the ledger's reason asserts `(include/exclude configuration can change that)`, a clause its own quote does not carry (it is at the anchor). No rationale for the substitution appears in the record. Not edited (read-only lane).

**M2 — this pair's freshness evidence base is stale at the candidate: the raw file the W1 reports hash is gone.** `Pair10A` F1 claims `r27 retained fetched/S006-1.raw.gz … sha256 f0318abe… (recomputed, verified True)`; `Pair10B` claims `zcat S006-1.raw.gz | sha256sum = f0318abe…`. At the candidate `fetched/` holds **no** `S006-1.raw.gz` (only `*.public.txt.gz`/`*.source.gz` + `text/`), and the manifest records `replacedFile:"S006-1.raw.gz"`, `rawHttpBodyRetained:false`. Both A/B raw-digest verifications are therefore unreproducible, and unreproducible in principle (body deliberately not retained). The row survives because I re-verified quote+anchor against the **retained** representation and against today's live page (both `535e55d0…`). Any claim that S006's HTTP body was digest-checked at the candidate is unsupported.

**M3 — the W1 drift characterization is wrong in kind.** `Pair10A` F1: "19 differing regions, all short hex-like request tokens" (implying per-request noise). The differing bytes are Next.js build/chunk/buildId identifiers: of the 7 regions I isolated, 4 are hex webpack chunk content-hashes (`091b7f339815a268`, `c44ed77ff5c225d`, `42872f32ebc7ccb0`, `c25e321b45e9a868`) and 3 are the same base64url buildId (`ndrfAHwVnt-w5Yffjl7If`) in the `_buildManifest`/`_ssgManifest` paths and the `__NEXT_DATA__` field — so "hex-like request tokens" is inaccurate for 3 of 7 regions, and none of them is request-scoped. Two of my own consecutive GETs were byte-identical (0 differing bytes) while an earlier one differed ⇒ churn is build-scoped and intermittent. Raw sha256 is an unreliable freshness signal here; the visible-text view is the stable one (`535e55d0…` across r26, r27 and all fetches today). Recorded because `Pair10A` F1 is the stated basis for comparing text views.

**L1 — "Jekyll branch builds" is narrower than the source's own scope.** The exclusion sentence is stated for Jekyll builds generally ("By default, Jekyll doesn't build files or folders that…", under *Configuring Jekyll in your GitHub Pages site*), so it also covers a custom Actions workflow that runs Jekyll. The narrowing is conservative (not an overclaim) and the appended row already adds "not every workflow uses Jekyll" ⇒ no verdict impact, wording only.

**L2 — no counter-level defect.** `group_source_required` satisfied (kind `source`); quote ≤25 words / ≥6 tokens / row-specific; anchor non-empty; HOLD correctly carries **no** `[r27-recheck S006 STALE]` marker (the file carries exactly one marker, `[r27-recheck S005 STALE]`, for the STALE sibling). C1 remains 55/58 decided with 3 unknown pairs ⇒ "58 review records" ≠ 58 strictly decided.

## 4. Verdict on the attacked item

**HOLD at stated scope stands** — independently confirmed, not falsified. The named official source is live (HTTP 200), the quoted sentence and its anchor are present verbatim today, the visible text is byte-identical to the retained r27 view (no premise drift since r26), and S006's page is the one member of the S001–S006 group that speaks about *which files a build omits* — the mechanism the sentence needs. The inferential step ("not built ⇒ not served") is absent from S006's text and is labelled local synthesis in the ledger reason, the appended table row and the file's Round-27 preamble, as the contract requires. **Not STALE** (attribution is not wrong at its own scope; S005's rejection concerns a different source's topic). **Not UNVERIFIABLE** (bytes retained and independently re-derived from a live fetch). Dissent on S005-preflight, S005/S003-sitemap and S004-ghp-steps is addressed in P4 and does not undercut this row.

## 5. Residual risk / verification gaps

- The pair's *raw* HTTP body is not in the tree; `receivedSha256 f0318abe…` is an unverifiable assertion at the candidate (M2) — only the visible-text representation is reproducible.
- The landed 18-word quote drops the classes most directly about manifest/file membership (M1); a ledger-only reader gets a weaker witness than the A/B reports verified.
- I did not re-derive S001–S005/S008 rows (other seats); I verified only the S003 general-flow numbering that the S004 override and S003's anchor depend on.
- Manifest `fetchedAt` values sit only +16.6 s…+19.1 s after the declaration commit instant — mechanically compliant with count_c1's `fetch date >= declaration`, but with no slack.
- No dated premise exists on this page, so freshness here means prose-identity of visible text, confirmed r26→r27→now; a future recheck must compare the text view (not raw sha) or it reports false drift.
- No gate/selftest beyond the read-only C1 count was run (no build/lint/formatter in this lane).

Report: .ufo/waves/round-27/w2/JudgePair10.md
