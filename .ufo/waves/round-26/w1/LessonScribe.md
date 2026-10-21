# Round-26 lesson skeleton (draft, report only) — LessonScribe

Scope: draft of the round-26 lesson body for `corpus/lessons/round-26.md`, grounded in `.ufo/waves/round-26/contract.json`, `corpus/lessons/round-25.md`, `population.json`, `fetched/manifest.json`, `fetched/manifest-retry.json`, and MANIFEST `rounds[420]` (round 25 closure notes). Nothing in this file is an execution result. No production file, SOURCES row, knowledge entry, measurement script, or lesson file was edited. Tooling: no tool was installed or updated by this seat; no network access was made by this seat.

Status of every outcome below: **PENDING until execution**. Results are appended only after the named command runs at a recorded revision.

## Claims

C1 freshness (selected; operability tied at legacy 10 and not worked this round): re-verify the 32 previously opened external SOURCES rows against bytes re-fetched on 2026-10-21 and decide each row HOLD or STALE; report UNVERIFIABLE separately and never count it as decided. Every STALE row gets an append-only correction block tagged `[r26-recheck S0NN STALE]` in the citing corpus file. Knowledge-entry claims that cite the rows are rechecked in pairs.

- Before: 0/32 prior external SOURCES rows carry a round-26 dated live-source recheck receipt (contract `claim.before`).
- After: PENDING. Written only from the measured command output below.
- Population: S001–S034 minus own-work S014 and S019 (32 rows). S035 (opened round 25) is excluded. Rejected rows S017 and S018 are included; HOLD on a rejected row means the rejection still holds because its flip condition is not met.
- Fetch: one public GET per recorded URL (34 recorded fetch entries: 32 rows, plus a second URL for S001 and S002). S008 has one documented retry after a 60 s TimeoutError, with a 240 s timeout (`fetched/manifest-retry.json`).
- Boundaries: documentation and specification GET reads only. No property probing, browser, account, publication, credential, or security testing. Round-24 C1/C2 debt remains held; no round-24 assignment, probe, or counter is retried, rephrased, or rerouted.
- appendOnly: SOURCES row cells stay unchanged except the allowed status, recheck, and used-by cells, and those changes are logged. Prior corpus bytes are preserved.

Why this claim: MANIFEST `rounds[420]` (round 25, admitted, verdict `freshness: unchanged`) states that no prior entry was re-verified or superseded, so the quality trend stayed unchanged. Round 26 targets exactly that.

## Gate

### Sources re-opened (32 rows)

Access date is the UTC date of the recorded fetch (`fetchedAt`, 2026-10-21 for every row, between 15:09 and 15:11 UTC). Quote and verdict columns are placeholders. Each row's quote must be copied verbatim from `fetched/text/S0NN-N.txt`, must be 6–25 whitespace-delimited words, and must be located at the row's anchor. The verdict is written by the row seat's receipt, not by this skeleton.

| id | URL (first recorded fetch) | access date (UTC) | ≤25-word quote (6–25 words) | verdict |
|---|---|---|---|---|
| S001 | https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml | 2026-10-21 | PENDING row receipt | PENDING |
| S002 | https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0 | 2026-10-21 | PENDING row receipt | PENDING |
| S003 | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | 2026-10-21 | PENDING row receipt | PENDING |
| S004 | https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | 2026-10-21 | PENDING row receipt | PENDING |
| S005 | https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site | 2026-10-21 | PENDING row receipt | PENDING |
| S006 | https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll | 2026-10-21 | PENDING row receipt | PENDING |
| S007 | https://docs.github.com/en/rest/pages/pages | 2026-10-21 | PENDING row receipt | PENDING |
| S008 | https://cgit.git.savannah.gnu.org/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418 (retry) | 2026-10-21 | PENDING row receipt | PENDING |
| S009 | https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c | 2026-10-21 | PENDING row receipt | PENDING |
| S010 | https://www.rfc-editor.org/rfc/rfc9110.html#section-8.8 | 2026-10-21 | PENDING row receipt | PENDING |
| S011 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-10-21 | PENDING row receipt | PENDING |
| S012 | https://www.sitemaps.org/protocol.html | 2026-10-21 | PENDING row receipt | PENDING |
| S013 | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | 2026-10-21 | PENDING row receipt | PENDING |
| S015 (queued) | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | 2026-10-21 | PENDING row receipt | PENDING |
| S016 (queued) | https://pages.github.com/versions.json | 2026-10-21 | PENDING row receipt | PENDING |
| S017 (rejected) | https://docs.astro.build/en/guides/deploy/github/ | 2026-10-21 | PENDING row receipt | PENDING (rejection HOLD only if flip condition still unmet) |
| S018 (rejected) | https://www.debugbear.com/blog/firefox-safari-web-vitals | 2026-10-21 | PENDING row receipt | PENDING (rejection HOLD only if flip condition still unmet) |
| S020 | https://www.rfc-editor.org/rfc/rfc6596.html | 2026-10-21 | PENDING row receipt | PENDING |
| S021 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | 2026-10-21 | PENDING row receipt | PENDING |
| S022 | https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting | 2026-10-21 | PENDING row receipt | PENDING |
| S023 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | 2026-10-21 | PENDING row receipt | PENDING |
| S024 | https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | 2026-10-21 | PENDING row receipt | PENDING |
| S025 | https://html.spec.whatwg.org/multipage/scripting.html#the-template-element | 2026-10-21 | PENDING row receipt | PENDING |
| S026 | https://docs.python.org/3/library/html.parser.html | 2026-10-21 | PENDING row receipt | PENDING |
| S027 | https://docs.python.org/3/library/urllib.parse.html | 2026-10-21 | PENDING row receipt | PENDING |
| S028 | https://www.rfc-editor.org/rfc/rfc9110.txt | 2026-10-21 | PENDING row receipt | PENDING |
| S029 | https://www.rfc-editor.org/rfc/rfc3986.txt | 2026-10-21 | PENDING row receipt | PENDING |
| S030 | https://html.spec.whatwg.org/multipage/syntax.html#start-tags | 2026-10-21 | PENDING row receipt | PENDING |
| S031 | https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign | 2026-10-21 | PENDING row receipt | PENDING |
| S032 | https://www.rfc-editor.org/rfc/rfc3339.txt | 2026-10-21 | PENDING row receipt | PENDING |
| S033 | https://www.rfc-editor.org/rfc/rfc9110.txt | 2026-10-21 | PENDING row receipt | PENDING |
| S034 | https://www.rfc-editor.org/rfc/rfc8259.txt | 2026-10-21 | PENDING row receipt | PENDING |

Additional recorded URLs (same rows, same access date): S001 `https://raw.githubusercontent.com/actions/upload-pages-artifact/5f327015a708106f6f1b7c9a633901af30fe80cb/action.yml`; S002 `https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0`.

Excluded from this gate: S014 and S019 (own-work), S035 (opened round 25; its round-25 Gate stands unchanged unless a later round rechecks it).

### Gate rules for this round

- Quote window: 6–25 whitespace-delimited words, verbatim from the retained text view. Word count is computed mechanically by whitespace split, not estimated. (Round-25 erratum: a quote was labelled "12 whitespace-delimited words" and contained 10; see Mistakes.)
- Quote binding: quote must occur in the cited `fetched/text/S0NN-N.txt` at the anchor. Heading, navigation, and doclink text do not ground a quote.
- Verdict: HOLD (teaches and scope still supported at the anchor; a moved anchor with the same content is HOLD with `anchorObserved` noting the move), STALE (content changed so teaches, anchor, or version is now wrong or incomplete; correction text required), or UNVERIFIABLE (retained bytes cannot decide; reason required; never counted as decided).
- The mechanical gate checks structure, word count, and quote presence only. Whether a HOLD or STALE judgment is semantically right is a manual review duty (see Mistakes).

## Mistakes

Routed defects carried from MANIFEST `rounds[420]` (round 25) and from the round-25 lesson, with the round-26 disposition.

| Class | Evidence pointer | Captured-by | Fix / fail-capable witness |
|---|---|---|---|
| seat-scratch | MANIFEST `rounds[420]` notes: seat `/tmp` scratch writes (SC333 and ReviewPopulation); round-25 lesson lines 176–182 | Explicit lane-only seat-write instruction | Round 26: seats write only their named sandbox or report file; nothing under `/tmp`. Disclosed, not repaired in round 25. Witness PENDING: a bounded path check of seat receipts for `/tmp` references, to be run after the wave concludes and recorded only then. |
| number-drift (Gate word-count) | round-25 lesson line 23 says "12 whitespace-delimited words" for the §5.2.2 quote; line 24 quote has 10 words; erratum at lines 107–110; execution at lines 230–232 (cc1=22, cc2=10, cc3=13, cc4=14, cc5=16) | Mechanical whitespace-split count against retained source | Round 26: word counts are generated by command, not typed. Append-only correction carried; original line 23 is not rewritten. Witness PENDING: the round-26 quote-count check must reject a deliberately wrong count. |
| prose-semantics (manual) | MANIFEST `rounds[420]` notes: "gate checks structure/quote binding, card prose semantics remain manual" | Gate design limit (round 25) | Round 26: the Gate verifies quote presence and word window only. HOLD/STALE semantics are a named manual duty of the pair reviewer and are recorded in the receipt. Witness PENDING: a pair reviewer must cite a file:line and a verbatim quote for every STALE. |
| reference-drift (candidate, for L1) | `.ufo/waves/round-26/` contains no `measure.py`, while `contract.json` `claim.count` names `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`. Round 25 had `.ufo/waves/round-25/measure.py`. | Direct directory listing at drafting time | Not a result. The count cannot run until L1 provides the script. Do not report C1 as measured until it exists and runs. |
| scope (carried, not repaired) | Round-24 C1/C2 debt and the open L0 policy-stop disposition (round-25 lesson lines 12–16, 261–274) | Existing no-reroute instruction | Round 26 does not touch them. Disposition remains open. |

Seat-scratch note: the round-26 seats were dispatched after round 25's `/tmp` problem was disclosed, so their receipts must state where their scratch lived. A receipt that does not state this is not counted as clean.

## Measurement

All entries below are placeholders. They are appended only after execution, at a recorded revision, with the exact command, exit code, and stdout retained.

- M1 freshness count: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`. Status: PENDING (script not present at drafting; see Mistakes). Result: PENDING. Expected shape: decided = HOLD + STALE count over 32 rows; UNVERIFIABLE listed separately, not in decided.
- M2 receipt coverage: number of rows with a round-26 receipt that has a verbatim quote of 6–25 words found in the retained text. Result: PENDING.
- M3 STALE corrections: each STALE row has one `[r26-recheck S0NN STALE]` EOF block in the citing corpus file, with prior bytes preserved. Result: PENDING.
- M4 SOURCES append-only check: only status, recheck, and used-by cells changed; all prior row bytes present. Result: PENDING.
- M5 census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`. Baseline from `census-before.txt`: `kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` (inherited, nonfatal) and `kake ok`, exit 0. Result after execution: PENDING.
- M6 fetch integrity: per-file SHA-256 against `fetched/manifest.json` and `fetched/manifest-retry.json`. Result: PENDING.
- M7 knowledge pairs: knowledge entries citing the rows, rechecked as pairs (see list below). Result: PENDING.
- M8 self-verdict axes (freshness, operability): PENDING until M1 to M7 are observed. No score is claimed here.

Knowledge entries that cite population rows (from SOURCES `used-by`, rows in scope), for M7: `corpus/knowledge/ghp-served-set.md` (S001, S002, S003, S004, S006, S008), `corpus/knowledge/ghp-custom-domain.md` (S003, S005, S007), `corpus/knowledge/ghp-etag-anatomy.md` (S009, S010), `corpus/knowledge/crawl-scope-per-host.md` (S011, S012, S013), `corpus/knowledge/static-canonical-preflight.md` (S020–S034 where listed). Each statement is listed with file:line by the pair seat; original lines are never rewritten, and corrections are appended only.

## Hand-off

- For L1: the round-26 lesson should be written only after M1 to M7 are observed. The contract's `measure.py` is absent at drafting; that is the first blocker to route.
- Do not treat PENDING cells as passed. Do not promote any row from its receipt alone.
- Freshness result, if any, is the decided count from M1 at the measured revision. Anything else is `[INFERENCE]`.
