# Reopen of S051 and S052 (round 30, wave 2)

- Seat: KakeR30.ReopenS051S052. Milestone r30-falsify. Axis: freshness. Checked 2026-10-22.
- Evidence commit: 451e98fc8415edf10f41b2aad656318e7edc84ca (lane HEAD; the C2 commit).

## Verdict

The rows for S051 and S052 and both Gate quotes hold against the pages fetched at 13:22Z.
Nothing in the item is falsified. Three low-severity findings and one unopened lead follow.

## 1. Method

- One GET per named URL, through a byte-identical copy of `.ufo/waves/round-30/fetch_sources.py`
  (sha256 b9431a5f349c7b857e2139fd148b8f75a2ddb8a4d94a3ea7013709a28a9190b4, equal to the
  receipts' `fetcherSha256`), run in the sandbox as `python3 -B fetch_sources.py --only S051,S052`.
- Output goes only to `/fast/scratch/hyaku/kake-r30/w2/ReopenS051S052/fetch/sources/`.
  The lane `sources/` directory was not written and still holds its 10 entries.
- The fetcher makes one `urlopen` per id. `finalUrl` equals `url` for both, so no redirect was followed.
- User-Agent: `kake-shokunin-round-30-source-opening (one GET per page)`, the original string.
- No other URL. No owned-property request. Not run: freshness-sweep.mjs, probe-delta.mjs, live_snapshot.py.

## 2. Status

| id | GET | HTTP | accessedUtc | finalUrl equals url |
|---|---|---|---|---|
| S051 | https://render.com/docs/static-site-headers | 200 | 2026-10-22T13:22:17Z | yes |
| S052 | https://render.com/docs/custom-domains | 200 | 2026-10-22T13:22:18Z | yes |

## 3. sha256 comparison (retained at 451e98f against this GET)

| id | retained body bytes | new body bytes | body sha256 equal | visible text sha256 equal |
|---|---|---|---|---|
| S051 | 280291 | 280374 (+83) | no | yes |
| S052 | 371923 | 372006 (+83) | no | yes |

- S051 body: retained `7ba689dc5b68d177bba05484ccb170a8765084347f154e6fdd29192f34d03aac`;
  new `8e03470e61e98b798f70b317044c4880b13874549c61ccd02c3eaefec50cffe3`.
- S052 body: retained `59469467e22fec821d9971756b5b0c83de002f7f89578df8913b1d2d5094e543`;
  new `04cc60e9e97a7915c362eb8fca31c4d589c9dec7c5c2ab01e6956ba6c9167807`.
- S051 visible text, retained and new: `e98982cef9434d9521063602ea05bfa16af4dc756e1068cdf3a60d058332a27d` (539 words).
- S052 visible text, retained and new: `6c1616f8214a4f5987681ea9b38db60a6b7d0b54d89cdd23687452566858f769` (1488 words).
- Retained integrity holds for both: the committed `.html.gz` decompresses to the receipt
  `bodySha256`, and the committed `.txt` matches `textSha256`. Lane working-tree `.txt` equals committed.
- Body difference, classified. The 83-byte change equals the length change of the deploy
  identifier alone: `data-dpl-id` changed once and `dpl=8b4d78f7c` changed 82 times, each value
  growing from 9 to 10 characters. Other changes: `dpl=zcqt4` became `dpl=lnrn8` (50 places),
  21 build chunk paths were renamed, an Open Graph image cache token changed, and per-render
  trace metadata changed. None of these touches visible text. After normalizing them, the residual
  is one moved navigation entry (S051: 2 blocks; S052: 7 blocks, which also move one identical
  image row and renumber internal references). [INFERENCE] The site was redeployed between
  11:49Z and 13:22Z. The cited text did not change.

## 4. Quote checks

| quote | words | found in new text | found in retained text | one-letter control found in new text |
|---|---|---|---|---|
| S051 Gate, lesson line 45 | 23 | yes | yes | no |
| S052 Gate, lesson line 46 | 25 | yes | yes | no |
| 25 knowledge quotes cited to S051 or S052 | - | 25 of 25 | 25 of 25 | - |

## 5. Row cell verdicts (corpus/SOURCES.md rows 59 and 60 at 451e98f; 11 cells each)

| cell | S051 | S052 |
|---|---|---|
| 0 id | ok | ok |
| 1 name and URL | confirmed: 200, same final URL | confirmed |
| 2 kind | docs; consistent | docs; consistent |
| 3 tier | A; consistent (vendor's own docs) | A; consistent |
| 4 scope | confirmed: dashboard headers, path matching, key and value rules | confirmed: custom domains on web services and static sites |
| 5 source location | confirmed: title, "Header syntax", "Path Effect" table, name and value rules | confirmed: opening paragraph, and "1. Add your domain in the Render Dashboard" |
| 6 claim | confirmed clause by clause (6 clauses) | confirmed clause by clause (4 clauses) |
| 7 status | mined; registry field | mined; registry field |
| 8 date | 2026-10-22; matches both fetches | same |
| 9 recheck | 90d, due 2027-01-20; see F2 | same |
| 10 used-by | render-static-sites.md; confirmed (25 quotes) | confirmed |

Claim clauses. S051: no server-side header injection; set in the dashboard; relative path without
the domain; matched against every custom domain; key normalized; value sent as-is. S052: attached
to web services and static sites; TLS issued and renewed automatically; HTTP redirected to HTTPS;
onrender.com kept unless disabled.

## 6. Findings, by severity

- F1 (low, quote fidelity). 8 of 27 quotes carry a space before punctuation that the page does not
  have. The raw markup is `Dashboard</a>.` and `static sites</span>.`; the text rule turns the tag
  into a space. Affected: S052 Gate line 46 ("static sites ."); knowledge lines 49, 58, 60, 63,
  66, 86 and 91. They pass the counter because it compares against the same extracted text, so
  they are exact to the extraction but not to the rendered page. No change of meaning. Fix options:
  collapse space-before-punctuation on both sides inside the counter, or re-cut the quotes.
- F2 (low, freshness mechanism). The body hash changes on every deploy with no content change, so
  the receipts' `bodySha256` cannot detect change. The entry's recheck trigger, "on a Render Docs
  change", is undefined. Define it as a change in `textSha256`, which the counter already uses.
- F3 (low, wording). Knowledge line 52 says "The header name is matched case-insensitively". The
  quote it cites says "The name is the case-insensitive name for the header." The word "matched"
  goes one step beyond the quote. Mark it as inference or reword.
- Lead, not opened: https://render.com/docs/configure-other-dns. The S052 body fetched in this
  session links it as `<a href="/docs/configure-other-dns">All other providers` (five occurrences).
  It is outside the two named URLs, so I did not open it, as the L1 instructed. The S052 text
  contains no "ALIAS", "ANAME" or "216.24.57.1", so S052 alone does not settle the S053 or S054 flips.

## 7. Residual risk and gaps

- Substring checks do not prove that each sentence follows from its quote; that reading is the closure's.
- Freshness is as of 13:22Z. The row's 90-day recheck is due 2027-01-20.
- Not checked: S049 and S050 (outside the item); the Blueprint `domains` field that the entry records as open.
- The lane counter ran on committed bytes (4/4), as designed; it does not read the new fetch.
  The new-fetch comparison is `reopen_check.py` in the sandbox.

## 8. Commands run (exit codes)

1. `cp -p` of the fetcher into the sandbox, then `sha256sum` of both copies: exit 0; both b9431a5f.
2. `python3 -B fetch_sources.py --only S051,S052` in sandbox `fetch/`: exit 0. Output: "S051 200 280374 2026-10-22T13:22:17Z ..." and "S052 200 372006 2026-10-22T13:22:18Z ...".
3. `git rev-parse --verify` for HEAD and five commits; `git show 451e98f:<path> | sha256sum` for the three corpus files and the receipts; `gzip -dc` on the retained bodies: exit 0. Results as in section 3.
4. `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision 451e98fc...` in the lane, read-only: exit 0. Result: 4/4, controlBroken false, counter sha a2cd3164.
5. `python3 -B reopen_check.py` in sandbox: exit 0. Wrote `reopen_check.json`.
6. `python3 -B body_delta.py`: exit 0.
7. `python3 -B token_delta.py`: exit 0. Byte delta 83 on each page; token-length contribution 83.
8. `python3 -B token_delta_v2.py`, `token_delta_v3.py`, `token_delta_v4.py`: each exit 0. Normalized equality stayed false; each pass narrowed the residual (Open Graph token, trace metadata, widened chunk paths).
9. `python3 -B residual_diff.py`: exit 0. S051 2 residual blocks; S052 7.
10. Read-only Python in the sandbox: raw markup around quotes, the artifact list, and the DNS lead occurrences.
11. `sha256sum` and `ls` of the lane `sources/` directory after the run: 10 entries, no new files.

## 9. Evidence pointers

- Sandbox `/fast/scratch/hyaku/kake-r30/w2/ReopenS051S052/`: `fetch/sources/{S051,S052}.html.gz` and `.txt`;
  `fetch/sources/receipts.json` (sha256 a3d48b55407780520a23136acf8fa27825f4762febbcfa650357a2588b15aadc);
  `reopen_check.py` (0e17c235...), `reopen_check.json` (f412d6ed...); `body_delta.py`;
  `token_delta.py`, `token_delta_v2.py`, `token_delta_v3.py`, `token_delta_v4.py`; `residual_diff.py`.
- Lane, read-only: `corpus/SOURCES.md:59-60` (commit 451e98f; working-tree sha 578da75b...);
  `corpus/lessons/round-30.md:45-46` (sha a150e0ca...);
  `corpus/knowledge/render-static-sites.md:49-53, 57-66, 85-86, 91` (sha 53711959...);
  `.ufo/waves/round-30/c2_quote_truth.py` (sha a2cd3164...).

## 10. Tooling

No tool was installed or updated. Used the system `python3`, `sha256sum`, `gzip`, and read-only
`git` (`show`, `rev-parse`). No pacman, package manager, or service call.
I sent one message to KakeR30.CriticRejects declining the extra page. The L1 instructed that
configure-other-dns must not be opened, and I complied.
