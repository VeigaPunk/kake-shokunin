# PairS005GhpCustomDomain: round-26 freshness recheck

- Pair: S005 × `corpus/knowledge/ghp-custom-domain.md` (entry tag #109A, 58 lines)
- Judged on: freshness. Milestone: r26-recheck-build. Seat: knowledge pair, leaf (no dispatch).
- Source bytes: S005-1 (manifest index 1). `fetchedAt` 2026-10-21T15:09:34.843922Z; `text/html`; 240439 bytes; sha256 `dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9`; raw `fetched/S005-1.raw.gz`; text view `fetched/text/S005-1.txt` (14698 chars, one line).
- Verdicts: **HOLD** = the S005-attributed statement stands at its anchor, quote verbatim. **STALE** = a cited version, date or line anchor is superseded; append-only correction below. Quotes are verbatim from `S005-1.txt`. Markdown backticks in the entry are absent from the text view and were removed only for comparison.

## Result

- 17 statements in the entry cite or rely on S005: body lines 1–46, including the r20 tail (lines 13–15). Lines 50–58 (S007 erratum) do not cite S005.
- **HOLD 14 · STALE 3.**
- Every S005 mechanism claim still holds verbatim: apex step 4, branch-versus-Actions publishing, domain verification, wildcard warning. The STALE items are verification stamps and one moved line anchor: P02 and P09 (2026-10-19 verification dates) and P06 (`publish-channels.md:9`, now `:13`).

## Statement table

| ID | Line | Statement (abridged) | S005 verbatim quote (count, words) | Anchor observed in round-26 bytes | Verdict | Note |
|---|---|---|---|---|---|---|
| P01 | 1 | Header: S005 URL and anchor §Configuring an apex domain | "Configuring an apex domain To set up an apex domain, such as example.com, you must configure a custom domain" (n=1, 19w) | h2 "Configuring an apex domain" (raw offset 57237); URL identical to manifest S005-1 URL | HOLD | Same line lists S003 and S007, which have no URLs of their own here |
| P02 | 2 | `verified-at: 2026-10-19` for GitHub Docs | same witness as P01 (n=1, 19w) | manifest S005-1 `fetchedAt` 2026-10-21T15:09:34Z | **STALE** (C1) | Stamp superseded as latest S005 verification; the REST API clause is S007's |
| P03 | 3 | Recheck argv: `.md` URL piped to `grep -cF` of the phrase with backticked CNAME | "any existing CNAME file is ignored and is not required" (n=2, 10w) | phrase sits in the article body twice, `<code>`-wrapped: raw offsets 62011 (apex step 4) and 75666 (subdomain step 4) | HOLD | `.md` form not retained; argv not replayed (F1) |
| P04 | 7–8 | Workflow publishing: GitHub documents the custom domain as Pages configuration | 'Under "Custom domain", type your custom domain, then click Save.' (n=2, 10w) | apex ordered list item 4 of 7 (raw offset 57678); item 3 is "click Pages" | HOLD | — |
| P05 | 8–9 | Under workflow publishing an existing repository CNAME file is ignored | "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored" (n=2, 22w) | apex list item 4; subdomain list item 4 (raw offset 71333 list) | HOLD | — |
| P06 | 13 | r20 tail: "Refines corpus/knowledge/publish-channels.md:9" | "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created" (n=2, 15w), mechanism witness | Repo anchor: at base cb807bc, `publish-channels.md:9` is "`CNAME` file pins `ds4cc.com`."; that line is now :13 (+4 after front matter was added); :9 is now the bullet head | **STALE** (C2) | Cited line superseded; the attribution claim itself holds |
| P07 | 14 | r20 tail: "and `SKILL.md:16`: those lines attribute the domain to a repository file" | "no CNAME file is created, and any existing CNAME file is ignored" (n=2, 12w) | Repo anchor: SKILL.md:16 ds4cc row "GH Actions on push to `main` (`CNAME` = ds4cc.com)"; identical line at base cb807bc and now, with r20 bracket appended | HOLD | — |
| P08 | 15 | "the documented mechanism depends on Pages publishing mode" | "If you are publishing your site from a branch, this will create a commit" (n=2, 14w) | apex list item 4 (both publishing-mode sentences) | HOLD | — |
| P09 | 17 | "Source checks (quotes reopened 2026-10-19)." | "no CNAME file is created, and any existing CNAME file is ignored" (n=2, 12w) | manifest `fetchedAt` 2026-10-21T15:09:34Z | **STALE** (C3) | Reopen date superseded; the quote is still verbatim |
| P10 | 18–19 | S005 apex step 4: "no CNAME file is created, and any existing CNAME file is ignored" | same quote (n=2, 12w) | apex ordered list item 4 of 7 (raw 57678); "step 4" confirmed in markup | HOLD | Backticks removed for comparison |
| P11 | 19–20 | "branch publishing instead creates a root file when the domain is saved" | "this will create a commit that adds a CNAME file directly to the root of your source branch" (n=2, 18w) | apex list item 4, after "then click Save." | HOLD | — |
| P12 | 20 | "S005 recommends domain verification" | "We recommend verifying your custom domain prior to adding it to your repository" (n=1, 13w) | tip under h2 "About custom domain configuration" (raw offset 54545) | HOLD | — |
| P13 | 21 | "and warns against wildcard DNS records" | "We strongly recommend that you do not use wildcard DNS records, such as *.example.com" (n=3, 14w) | warning blocks in apex, subdomain and DNS-records sections | HOLD | — |
| P14 | 32 | Falsifier: "In that branch mode, S005 says saving the custom domain writes a root CNAME file." | "this will create a commit that adds a CNAME file directly to the root of your source branch" (n=2, 18w) | apex list item 4 | HOLD | The `build_type: legacy` = branch mapping (lines 30–31) is S007's and is not judged here |
| P15 | 41 | "Recheck (2026-10-19). The header argv returned `2` matches." | "any existing CNAME file is ignored and is not required" (n=2, 10w) | article-body count 2 (raw offsets 62011, 75666) | HOLD | The 2026-10-19 `.md` result was not re-run (F1) |
| P16 | 44 | "Replayable claim: gives the authoritative docs, exact recheck argv, and count." | same quote as count witness (n=2, 10w) | S005 URL as manifest; argv and count as P03 and P15 | HOLD | Replayability against `.md` is unverified with retained bytes (F1) |
| P17 | 46 | "Admission authority: official Pages docs and API schema support the distinction." | "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created" (n=2, 15w) | apex and subdomain list item 4 | HOLD | S005-1 has zero "API" tokens; the "API schema" clause is S007's |

## Corrections (append-only; no original line is rewritten)

Suggested placement: one appended section after line 58, headed `## Round-26 freshness corrections (2026-10-21)`, containing C1 to C3.

C1 (P02, line 2):

```text
Round-26 re-verification (2026-10-21), S005 only: the GitHub Docs page Managing a custom domain for your GitHub Pages site was re-fetched 2026-10-21T15:09:34Z (manifest S005-1; sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9; 240439 bytes). The apex step-4, branch-publishing, domain-verification and wildcard-DNS sentences cited in this entry are present in those retained bytes. The 2026-10-19 date on line 2 is the earlier verification; the 2026-10-21 fetch is the latest S005 verification. The REST API clause on line 2 is S007's and is not re-verified here.
```

C2 (P06, line 13):

```text
Anchor update (round 26, 2026-10-21): the CNAME-file attribution cited on line 13 as corpus/knowledge/publish-channels.md:9 was at line 9 at base cb807bc. After four lines (three front-matter lines and a blank line) were added above it, the attribution is at corpus/knowledge/publish-channels.md:13 (`CNAME` file pins `ds4cc.com`); line 9 is now the head of the same pages.yml bullet (lines 9-13). The attribution claim itself still holds.
```

C3 (P09, line 17):

```text
Round-26 re-check (2026-10-21): the apex step-4 quotation in this list (Markdown backticks removed) and the paraphrased branch-root, domain-verification and wildcard-DNS points were found in the round-26 retained S005-1 text (sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9). The 2026-10-19 reopen date on line 17 is historical; the 2026-10-21 check is the latest.
```

## Flags (HOLD; not counted as STALE)

- **F1 (P03, P15, P16):** The recheck argv targets the `.md` form, which is not among the retained round-26 bytes. Retained S005-1 is the HTML page and contains the phrase twice in article body, `<code>`-wrapped, which matches the backticked pattern and the recorded count of 2. The argv was not replayed in round 26 (no extra fetch). Optional addendum:

```text
Round-26 note: the recheck argv targets the .md form, which was not retained in round 26. The retained HTML bytes (sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9) contain the phrase twice in the article body, consistent with the 2026-10-19 count. The .md argv has not been replayed since 2026-10-19.
```

- **F2 (P01):** The header gives one URL and one anchor for three sources (S003, S005, S007). The URL and anchor belong to S005 only.
- **F3 (row seat, RowS005):** `corpus/SOURCES.md` S005 row reads "fetched 2026-10-19", now superseded by the 2026-10-21 fetch. Its teaches includes "or the API", which S005-1 does not state (zero "API" tokens); the API half rests on S003/S007.

## Out of pair (routed, not judged)

- Lines 2 (REST API clause), 9–10 (`cname`/`build_type`), 22–27 (S003 and S007 bullets), 29–31 (`build_type: legacy` mapping), 50–58 (S007 erratum): route to the S007 and S003 pairs.
- Line 35 cites `corpus/knowledge/publish-channels.md:5-9`. That range also drifted +4, as P06 did; the Actions label is still present at :9. Route to the publish-channels owner.

## Verification performed

1. Read `manifest.json` S005 record (index 1, URL, `fetchedAt`, bytes, sha256) and `manifest-retry.json` (S008 only; no S005 retry).
2. In-memory python3 (stdlib, nothing written): gunzipped `S005-1.raw.gz` is 240439 bytes with sha256 equal to the manifest. Text view is 14698 chars. Counted every quotation (counts and word counts in the table). Located raw offsets of h2 headings, apex and subdomain ordered lists, and phrase occurrences. Token count of `API` in text view: 0. Embedded JSON duplicates of the phrase (raw offsets 123790, 140920, 173454, 203126) were excluded from counts.
3. `_grep` on the entry for exact line numbers 1–58.
4. Read-only git: `cat-file -t cb807bc` (commit); `show cb807bc:corpus/knowledge/publish-channels.md` (49 lines) and `show cb807bc:SKILL.md` compared with current lines; `log -- corpus/knowledge/ghp-custom-domain.md` (latest 9639ec7); `status --short` empty for the four corpus files.

Not performed: no network or `.md` fetch, no builds, tests or linters, no edits outside this report.

## Tooling

- Installs or upgrades: none. Tools used: existing python3 (in-memory), gunzip, git (read-only). pacman not used (host-wide pause).

```json
{"pair":"S005xghp-custom-domain","statements":17,"hold":14,"stale":3,"corrections":[{"id":"P02","at":"corpus/knowledge/ghp-custom-domain.md:2","append":"Round-26 re-verification (2026-10-21), S005 only: the GitHub Docs page Managing a custom domain for your GitHub Pages site was re-fetched 2026-10-21T15:09:34Z (manifest S005-1; sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9; 240439 bytes). The apex step-4, branch-publishing, domain-verification and wildcard-DNS sentences cited in this entry are present in those retained bytes. The 2026-10-19 date on line 2 is the earlier verification; the 2026-10-21 fetch is the latest S005 verification. The REST API clause on line 2 is S007's and is not re-verified here."},{"id":"P06","at":"corpus/knowledge/ghp-custom-domain.md:13 (publish-channels.md:9 pointer)","append":"Anchor update (round 26, 2026-10-21): the CNAME-file attribution cited on line 13 as corpus/knowledge/publish-channels.md:9 was at line 9 at base cb807bc. After four lines (three front-matter lines and a blank line) were added above it, the attribution is at corpus/knowledge/publish-channels.md:13 (`CNAME` file pins `ds4cc.com`); line 9 is now the head of the same pages.yml bullet (lines 9-13). The attribution claim itself still holds."},{"id":"P09","at":"corpus/knowledge/ghp-custom-domain.md:17","append":"Round-26 re-check (2026-10-21): the apex step-4 quotation in this list (Markdown backticks removed) and the paraphrased branch-root, domain-verification and wildcard-DNS points were found in the round-26 retained S005-1 text (sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9). The 2026-10-19 reopen date on line 17 is historical; the 2026-10-21 check is the latest."}]}
```
