# W1 ReopenSources — independent re-open of S057-S061 (Kake r31)

Seat: KakeR31.ReopenSources (leaf, no subagents). 2026-10-22.
Sandbox: /fast/scratch/hyaku/kake-r31/w1/ReopenSources/ (script, bodies, texts, reopen.json).
No installs performed. No owned-property requests; only the five declared render.com URLs, one GET each, no retries, no headless browser.

## Method
- Copied `visible_text` verbatim from .ufo/waves/round-31/fetch_sources.py (HTML minus script/style, comments and tags removed, entities decoded, whitespace collapsed, trailing newline). Same UA string as the lane fetcher, urllib GET, timeout 60.
- Compared fresh body/text sha256 against .ufo/waves/round-31/sources/receipts.json (L1 fetches 2026-10-22T15:41:23Z-15:41:29Z).
- Local-only second pass: gunzipped my bodies and the lane's stored S*.html.gz, located first/last differing bytes, sampled the differing windows; classified them heuristically against script/style/comment spans of the old body.
- No text diff was needed anywhere: no text hash differed.

## Commands and exit codes
1. `TMPDIR=<sandbox>/tmp python3 -B <sandbox>/fetch_reopen.py` → EXIT=0 (the 5 GETs; 15:55:44Z-15:55:47Z).
2. `python3 -B <sandbox>/body_delta.py` → EXIT=0 (local body comparison, no network).
3. `sha256sum sources/S057..S061.txt fetch_sources.py` in .ufo/waves/round-31 → EXIT=0.

## Per-page results (fresh 15:55Z vs receipts 15:41Z)

| ID | URL path | Time (UTC) | Status | Body sha256 (fresh) | Text sha256 (fresh) | Body eq | Text eq | Text diff |
|----|----------|------------|--------|---------------------|---------------------|---------|---------|-----------|
| S057 | /docs/blueprint-spec | 15:55:44Z | 200 | 58a56cec591b29128a8769b6c4776d0a7b0240f76a6691019ca35afc2f6ee7e4 | ca8179f2098b142d5040c17763ecf205f630342d0d01a6a386a1f10e9848e51a | no | YES | none (8223 words both) |
| S058 | /docs/web-services | 15:55:44Z | 200 | c615d00bd5939fac831090ef5709b0ab2c8d0d5646a1a12eb6d3502c3965acb8 | 983a792dc65dbbe95bf3437f1b02bfa88c4a6f009282486480f786b45aee8aee | no | YES | none (1817 words both) |
| S059 | /docs/docker | 15:55:45Z | 200 | c316326253f0e438b60df85efe4d95d5fbc890a10377bcf403e7b9a69ba58b01 | f8e60da01b3087b31fbea6596f796746815c1ee28c735221d3c26f5d96b48618 | no | YES | none (1301 words both) |
| S060 | /docs/health-checks | 15:55:46Z | 200 | eccab9b2af08c649fb323e96234af1007737163fdce062aeb2ccddc3f742271c | 1f934877247b6d636683b124da72385af8afa6ef4644ccb72e15aa2b3e065d7b | no | YES | none (1018 words both) |
| S061 | /docs/configure-other-dns | 15:55:47Z | 200 | 9a4741a1560da26ff52d6e7e61f3d38250a85e2a2c3fbb24556932d00cdb97ea | aa904927cf6cce3782594518c859dda5c88167e1b84ca674874acfe9c47c0c3d | no | YES | none (899 words both) |

Receipt text sha256 values are identical to the fresh column above on all five. finalUrl equals the requested URL on all five (no redirect).

## Why bodies differ while text is identical
- All five bodies contain per-request Sentry instrumentation: `<meta name="sentry-trace" content="<32hex>-<16hex>">` differs every fetch (e.g. S061 old `e4a6ee50a21e4110acefa824c419334e-8d90f29bb0db6bd0` → new `4b60a1f4cb0f4f6fb0d8f4767a48a50f-8903a8d6b3b17668` at offset 16007; S061's entire body delta is that one 267-byte window; `baggage` meta is unchanged).
- S058/S059 additionally reference a different Next.js deploy: chunk URLs moved `?dpl=lnrn8` → `?dpl=6f79ff4995` with renamed chunks (`3b4h2g1drvkb3.js` → `2cjipp2x9lhtd.js` style), first divergence at offsets 4327/5623. S059's fresh body mixes both deploy tags (CDN mix), same size class. S057/S060 byte size moved -43/+73 with divergence starting at 16038/15893 inside the head instrumentation.
- After the first divergence byte alignment cascades, so my span classification of every differing byte is heuristic (e.g. S057: 942987/1416637 mid bytes provably inside script/style spans, remainder includes alignment drift). The decisive, non-heuristic evidence is the text-sha equality under the exact lane rule, plus matching word counts.

## Loop closure on lane artifacts (no GETs)
- sha256 of stored .ufo/waves/round-31/sources/S057..S061.txt each equals its receipts textSha256 (e.g. S057.txt ca8179f2…).
- sha256 of .ufo/waves/round-31/fetch_sources.py = bc66ceb0d136eab0f134dca60c3a614ee4fdb9e4090ab6242605364e079242c9 = receipts fetcherSha256.
- So receipts faithfully describe the stored texts and fetcher; my independent fetch reproduces all five text hashes 14 minutes later.

## Finding
C2's grounding (S057-S061 fetched 2026-10-22T15:41:23Z-15:41:29Z) is fresh as of 2026-10-22T15:55:44Z-15:55:47Z: visible text byte-identical on all five pages; body deltas are request-scoped Sentry nonces and Next.js deploy build IDs, not document content. No drift, no doc change to report. Full machine evidence: <sandbox>/out/reopen.json, per-page <sandbox>/out/S0xx.{html.gz,txt}.

## Not verified
- Anything before 15:41Z or after 15:55Z today; content between the two fetch moments is assumed continuous (bodies show only per-request noise, but a change within those 14 minutes that was itself reverted cannot be excluded).
- Heuristic attribution of every differing body byte (alignment cascades); text-sha equality is the load-bearing check and it is exact.
- No second fetch of any URL: body-level conclusions rest on exactly two samples per page (L1's and mine).
