# W2 falsify — S040 re-opened by hand (`moved`)

Seat: ReopenFlagS040. Lane head f3a38bf8e68f6cee386125d34b5e95ac9b2df66e, base b720d799.
Sandbox: /fast/scratch/hyaku/kake-r36w2/ReopenFlagS040/ (bodies, manifests, clone). No tools installed.

## What I attacked
The real-input re-check's sole S040 finding: `{"check":"S040","reason":"moved","target":
"https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"}` in
`.ufo/waves/round-36/realrun/audit.json`, an input whose row is `corpus/SOURCES.md:48`.

## Commands (all run in the sandbox, TMPDIR set, each `timeout`-capped)
1. `curl -sS -D nofollow.hdr -o nofollow.body 'https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages'` → exit 0.
2. `curl -sSL -D follow.hdr -o live.html '<same URL>'` → exit 0; sha256 live.html `65f68e3d68a109da1bf7a74ab44ee8d65732e2aad216b12bc4408e585c8f4a6b`.
3. `curl -sS -o /dev/null -w '%{http_code} %{num_redirects}' '<what-is-github-pages>'` → exit 0, `200 0`.
4. Second no-follow `curl -D -` of the S040 URL → exit 0, same `301` + same `location`.
5. `tar -xJf …/realrun/snap-bodies.tar.xz ./S040.body` → exit 0; snapshot sha256 `e3711c09918ba9c7df3cb0610a96c530550d3b4a9d047c6f05c63e981f4575a2`.
6. `python3 -B clone/scripts/source_recheck.py --manifest m1/manifest.json` (my live body, real hops) → exit 1,
   `{"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S040","reason":"moved","target":"https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"}]}`.
7. Same tool on `m2/manifest.json` (same quote/body, `url` = the canonical `what-is-github-pages`, one 200 hop) → exit 0, `"verdict":"clean","findings":[]`.
8. `python3 -B` importing `clone/scripts/source_recheck.py:html_text` on live.html → `quote_norm_in_text: True`.

## Observed facts
- Hop chain, verbatim: `HTTP/2 301` / `location: /en/pages/getting-started-with-github-pages/what-is-github-pages` / `content-type: text/plain; charset=utf-8`, 98-byte body `Moved Permanently. Redirecting to /en/pages/getting-started-with-github-pages/what-is-github-pages`; then `HTTP/2 200` `text/html; charset=utf-8`. One hop, permanent, reproduced on a second uncached request. 301 is permanent under S088/contract (b), so `moved` is exactly what the frozen contract prescribes.
- The redirect target in audit.json matches the RFC 3986 resolution of that relative `location` byte for byte, so no resolution or hop-count error.
- Live table text (tags flattened to spaces, whitespace collapsed), read from `live.html` at byte 52177 under `<h2>Types of GitHub Pages sites`: `… Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>`. Raw cells: `<code>http(s):/<wbr/>/<wbr/>&lt;owner&gt;.github.io</code>` and `<code>http(s):/<wbr/>/<wbr/>&lt;owner&gt;.github.io/<wbr/>&lt;repositoryname&gt;</code>`; with the tags stripped the code text is `http(s)://<owner>.github.io` and `http(s)://<owner>.github.io/<repositoryname>`. The odd `http(s):/ /` in the Gate quote is therefore `<wbr/>` removal, not a paraphrase: rule (c) drops the tag and rule (d) deletes whitespace from both sides, which is why the tool finds the quote and reports no `quote_missing`.
- Snapshot vs my live GET: same length (94 214 B), 63 differing bytes spanning 8037–94003, all Next.js build ids (`/_next/static/w28cKZSntYh6_95anoP2E/` vs `/_next/static/MJcDVbR69bF2a-P6om5l5/`); the table region 52100–53900 is byte-identical. The quoted content did not change between the recorded fetch and now.
- The row already says the redirect exists: `corpus/SOURCES.md:48` anchor ends "fetched 2026-10-22, the requested URL redirects to https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"; `corpus/SOURCES.md:148` (round-29 note) repeats "GitHub Docs about-github-pages, which redirects to what-is-github-pages". The URL column still holds the 301 alias, and title/teaches/quote (page title `What is GitHub Pages? - GitHub Docs`) all describe the target page.

## Verdict
**Real, not a tool miss, not an extraction miss, not a paraphrase.** The page permanently (301, one hop) redirects to `what-is-github-pages`, my own fetch reproduces the exact finding and exit 1, and the quote is a verbatim flattened transcription of the target page's table, not a paraphrase.

Two qualifications the audit summary should not lose:
1. **Documented alias, not drift.** S040's finding is a re-flag of a redirect the row and the round-29 provenance note both record, and the page body is unchanged. Counted inside "14 findings on 13 rows", it reads as a stale row when the only stale part is the URL field.
2. **The row URL should change** on hygiene grounds, and the fix is proven safe: `what-is-github-pages` answers `200` with no redirect directly, and the same quote/body under that URL scores `clean` (command 7). Keeping the 301 alias guarantees every future audit re-flags S040; the redirect note can stay as history. This is a URL-field edit only — teaches, scope and quote are already correct.

## Not verified
- Whether GitHub intends `about-github-pages` as a permanent public alias (only two same-day observations of the 301).
- No other row was re-opened; I only counted that 9 registry rows mention redirects, while the audit flags `moved` on 2 of them (S040, S068), so the documented-redirect pattern may also apply to S068.
- The `og:url` on the target page is `https://docs-internal.github.com/...`; not investigated, since no S040 claim rests on it.

## Evidence
- `live.html` (200 body, sha256 `65f68e3d…8f4a6b`), `nofollow.hdr` (301 + location), `nofollow.body`, `follow.hdr`, `./S040.body` (recorded snapshot), `m1/manifest.json`, `m2/manifest.json` — all under `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS040/`.
