# Pair04B — critic: (S003, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair04B (critic, read-only leaf). Axis: freshness. Milestone: r27-full-citing-set.
Independent judgment; the A report was not read. No ledger, source, or SOURCES edits. No tool installs.

## Verdict

**HOLD (kind: source), scoped to S003's specific contribution.** Line 54's grouped recommendation is a
local synthesis. S003 supports only the premise that GitHub Pages serves a chosen branch's source folder,
or a workflow-uploaded artifact of possibly built static files, so the served set is not "the checkout".
S003 does not entail the recommendation itself (build the canonical-audit manifest over built HTML), and
it does not entail any file-level membership difference. No STALE marker is required.

## Citing line (range expanded)

- Line 54 is the only citing line: `an assumed checkout served set (S001–S006, \`ghp-served-set.md\`).`
  The en-dash range expands to S001, S002, S003, S004, S005, S006 under the `count_c1.py` RANGE regex.
  There is no other S003 literal or range in the file (`grep -n "S00[0-9]"` returns only line 54).
- Surrounding claim (lines 52-56): "Prepare the manifest over actual built/deployable HTML when that
  artifact exists, not over an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
  artifact was available or claimed as tested in round22".
- Origin: commit `c0fd6d5` (round-22, 2026-10-20). That commit's `source:` and `verified-at:` header lists
  only S020, S021, S026 and S027; the current header adds S028 and S029. S001–S006 were never declared in
  this entry's header.
- In `c1-before.json`, the pair is in `missing`. It is absent from `.ufo/waves/round-26/statements.json`.
  The only other S003 pair still missing is `sitemap-orphan-audit.md`, which is not in this seat's scope.

## Source bytes (r27 retained)

| Field | Value |
|---|---|
| manifest row/index | S003 / fetchIndex 1 |
| url = finalUrl | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site |
| status, fetchedAt | 200, 2026-10-21T19:59:55.678521+00:00 |
| raw sha256 (recomputed from gunzip) | `f42d48b59277843e489896f52f97bb9c62e68970f0c3bebb3021b586ba62a3f5` (154136 B), matches manifest |
| text file sha256 | `0a510dac7bbc93f1ea27185425cb8b53a60eec665242aebf3ab7681eb634a643` (`fetched/text/S003-1.txt`) |

Freshness against r26: the r26 raw hash is `aa758b4a…f1ac` and the r27 raw hash is `f42d48b5…62a3f5`. They
differ only in Next.js page chrome: the stylesheet and script `<link>` line, and the trailing footer
newline. The extracted text files are byte-identical (`cmp` exit 0). The relied-on prose is therefore
unchanged across the r26 and r27 fetches. The hash change is page-chrome churn, not a content change.

## Quotes (each ≤25 words; each passes count_c1's whitespace-normalized substring check)

1. **Primary.** Anchor: "Creating a custom GitHub Actions workflow to publish your site", general-flow steps 3-4.
   "If required by your site, build any static site files. Use the actions/upload-pages-artifact action to upload the static files as an artifact." (22 words)
2. Anchor: "About publishing sources".
   "the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch." (24 words)
3. Anchor: "About publishing sources".
   "Whenever changes are pushed to the source branch, the changes in the source folder will be published to your GitHub Pages site." (22 words)
4. Anchor: "Troubleshooting publishing from a branch", note.
   "Most external CI workflows \"deploy\" to GitHub Pages by committing the build output to the gh-pages branch of the repository" (20 words)

## S003's specific contribution, and the inferential step

- **S003 supplies:** two publishing modes. In branch mode, only the source folder (`/` or `/docs`) of the
  selected branch is published (quotes 2 and 3). In Actions mode, the site is built if required and
  uploaded as an artifact (quote 1). External CI commits "the build output" (quote 4). Together these
  show that what GitHub Pages serves is defined by the publishing source, the folder, and the build. It
  is not defined by the repository checkout.
- **Local synthesis, not S003:** "therefore build the canonical-audit manifest over the built/deployable
  HTML when it exists". The retained text contains no "manifest", "canonical", "audit", or "served set".
  The recommendation is the lane's inference.
- **Other rows' contributions (not S003's):** file-level omission from the uploaded archive comes from
  S001 and S002 (dotfile and `.git` exclusions). Upload and deploy steps come from S004. Jekyll skip rules
  come from S006. This seat does not attribute those to S003. S005 (custom domain) has no visible role in
  line 54. That is for the S005 seat to judge; it is flagged here only as a grouped-citation risk.

## Adversarial probes

- **Strongest counterexample.** Under branch publishing with `.nojekyll` and source `/`, the served set
  is approximately that branch's checkout. S003 therefore does not say a checkout is always wrong. Line 54
  attacks an *assumed* checkout served set and is hedged with "when that artifact exists". At that scope
  it holds. With Jekyll in branch mode, GitHub builds the site, so no local deployable artifact may exist.
  Line 54's hedge, and its admission that no production artifact was tested, cover that case.
- **Scope creep.** Line 54 is phrased as generic publisher advice, while S003 is specific to GitHub Pages.
  The parenthetical binds the citation to the GitHub Pages "checkout served set" concept from
  `ghp-served-set.md`, so the citation is not over-claimed. The general advice rests on local policy.
- **Inherited staleness through `ghp-served-set.md`.** That file's r26 S003 STALE items fix a non-verbatim
  quote (it dropped "on the source branch") and a misattributed Actions-versus-branch pointer. Line 54
  neither quotes S003 nor relies on either sentence. The root-or-`/docs` substance is unchanged, so
  nothing stale is inherited.
- **Stale premise versus date and boilerplate.**
  - The SOURCES anchor's "fetched 2026-10-19" is a source date, not a stale premise.
  - Line 184's "S008 via `manifest-retry.json`" is round-26 retry boilerplate. It does not concern S003
    or line 54.
  - The header `verified-at: 2026-10-20 (S020-S027)` makes no claim about S003, so there is no false
    freshness claim.
- **Provenance gaps (registry or metadata, not STALE at line 54's scope):**
  - (a) In `corpus/SOURCES.md:11`, the S003 `usedBy` cell lists only `ghp-custom-domain.md` and
    `ghp-served-set.md`. It omits this file and `publish-channels.md`, which r26 ledgered.
  - (b) This entry's `source:` header never declares S001–S006. The citation is transitive through
    `ghp-served-set.md`. [INFERENCE] The round-22 author did not reopen S003 for this entry, since its
    header lists only S020–S027.

## Suggested C1 ledger record (`pairs.json` → `pairs[]`)

```json
{"row":"S003","file":"corpus/knowledge/static-canonical-preflight.md","kind":"source","verdict":"HOLD","fetchIndex":1,"quote":"If required by your site, build any static site files. Use the actions/upload-pages-artifact action to upload the static files as an artifact.","anchor":"Creating a custom GitHub Actions workflow to publish your site — general workflow flow, steps 3-4 (also About publishing sources: source folder / or /docs on the source branch)","reason":"Line 54 grouped S001–S006 range; S003 contributes only that Pages serves a branch source folder or a workflow-uploaded (optionally built) artifact, not the checkout. Recommending a manifest over built HTML is local synthesis. Text byte-identical to r26 fetch; raw differs only in page chrome."}
```

## Appended wording (optional precision note, not STALE; no `[r27-recheck S003 STALE]` needed)

> - [r27-recheck S003 HOLD] Precision note (not STALE): line 54's grouped (S001–S006) citation is local
>   synthesis. S003 (re-fetched 2026-10-21, fetchIndex 1) contributes only that GitHub Pages publishes a
>   chosen branch's source folder (`/` or `/docs`) or a workflow-uploaded artifact of built static files,
>   so the served set is not the checkout. Auditing built HTML is this lane's recommendation, not S003's.
>   Evidence: w1/Pair04B.md.

Registry follow-up for L1 (not this seat's edit): add `corpus/knowledge/static-canonical-preflight.md`
to the S003 `usedBy` cell, along with the other uncovered citing files.

## Uncertainties

- [INFERENCE] Whether S003 was reopened during round 22 for line 54. Round-22 receipts were not opened.
  This affects provenance only, not the HOLD verdict, which rests on the r27 bytes.
- The verdict applies to this pair's attribution scope only. It is not proof that every
  file-membership claim in `ghp-served-set.md` is true.
- Discovered pairs: none added from this file. Line 54 is the sole S003 citing form.
