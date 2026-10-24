# ReopenFlagS017 — S017 `quote_missing` re-opened by hand

**Verdict: not real drift — quote-format artifact (tool/contract normalization miss).** The live
page is byte-identical to the recorded snapshot, the Gate sentence is present verbatim in
server-rendered HTML, and the shipped tool returns `clean` on the same body once the Gate quote's
Markdown code-span backticks are removed. The finding holds only under bullet (d) as written
(NFKC + whitespace deletion, case-sensitive, no code-span rule); it is not staleness evidence.

## Targets
- Gate input `.ufo/waves/round-36/realrun/input.json:93`: `S017`,
  url `https://docs.astro.build/en/guides/deploy/github/`,
  quote ``Add a `./public/CNAME` record to your project.``, `from: round-20.md`
  (lesson string, typographic quotes, `corpus/lessons/round-20.md:219`).
- Row `corpus/SOURCES.md:25`: quote column `Change your GitHub URL to a custom domain, step 2;
  fetched 2026-10-19` — paraphrase + metadata, not the Gate quote.
- Finding `audit.json:1`: `{"check":"S017","reason":"quote_missing","target":null}`, bundle verdict
  `failed-policy`, `checksEvaluated` 90, exit 1 (`realrun/audit.exit`).
## Commands (GET only, browser UA, `timeout 60`; all exit 0)
```
mkdir -p /fast/scratch/hyaku/kake-r36w2/ReopenFlagS017/tmp
tar -xJf .ufo/waves/round-36/realrun/snap-bodies.tar.xz -C /fast/scratch/hyaku/kake-r36w2/ReopenFlagS017
curl -sS -o live-noredir.body -D live-noredir.hdr https://docs.astro.build/en/guides/deploy/github/
curl -sS -L -o live-follow.body -D live-follow.hdr https://docs.astro.build/en/guides/deploy/github/
sha256sum live-follow.body live-noredir.body S017.body
python3 -B scripts/source_recheck.py --manifest <sandbox>/repro/{with-bt,rendered}/manifest.json
```
## Observed
No-redirect response: `HTTP/2 200`, `date: Fri, 23 Oct 2026 02:03:45 GMT`, `content-type: text/html`,
`content-length: 187760`, `etag: "3ad78cca2f1006ae7b5ac1216db54789"`, `cf-cache-status: HIT`, no
`location` — one hop, nothing to follow.

Hash identity (snapshot from tar = no-redirect = `-L` = both repro copies):
`8a11a811b80c2400d808e3f44ae9c92ef385b6d4df2676f4ec5b1a6a7763d402` for
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS017/{S017.body,live-noredir.body,live-follow.body,repro/with-bt/S017.body,repro/rendered/S017.body}`.
**Page unchanged between the 2026-10-22 22:56 snapshot and my 2026-10-23 02:03 GET.**

Live raw HTML at byte 158363, server-rendered (no JS needed):
```
<p>Add a <code dir="auto">./public/CNAME</code> record to your project.</p>
```
Tool-extracted, normalized text:
`...ConfigureDNSforyourdomainprovider.Adda./public/CNAMErecordtoyourproject.Createthefollowingfileinyourpublic/folderwithasingle...`

Step numbering still matches the row: enclosing `sl-steps` list is (1) "Configure DNS for your
domain provider.", (2) "Add a ./public/CNAME record to your project. …", (3) "In your Astro config,
update the value for site …", (4) "If necessary, update all your page internal links …"; heading
`<h2 id="change-your-github-url-to-a-custom-domain">` present.

Reproduced with the shipped tool on the live body:
- Gate quote (backticks): `{"version":1,"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S017","reason":"quote_missing","target":null}]}` **exit 1**
- Rendered text: `{"version":1,"verdict":"clean","checksEvaluated":1,"findings":[]}` **exit 0**

Mechanism: bullet (c) removes `<code>` tags so rendered text has no backticks; bullet (d) compares
NFKC + whitespace-deleted, case-sensitive substrings with no code-span folding. Nothing is lost in
extraction (sentence fully present, not JS-injected), so this is not an extraction or rendering
miss; the tool behaves as its frozen contract says. The page holds 4 other backticks, so the tool
does not strip them generally.
## Breadth (advisory; recorded bodies only)
7 of 90 Gate quotes carry backticks (`S004,S005,S006,S007,S008,S017,S065`). Re-running the tool's
`html_text`+`normalize` over the recorded bodies, deleting only backticks turns `quote_missing`
into a match for **S004, S005, S006, S008, S017** — 5 of the 8 `quote_missing` findings (`S007`,
`S065` still miss; `S025`, `S068` have no backticks). I did not fetch live pages for those, so this
is about the recorded bodies, not freshness. Up to half the run's 14 findings may be formatting.

## Row-level note
Driving the audit from the `SOURCES.md` quote column instead of lesson strings would match no row:
for S017 the full column text is absent from the live text, while `Change your GitHub URL to a
custom domain` alone is present. The 90 `input.json` quotes contain no `fetched` marker and come
from lesson files (`round-20.md` 17, `round-34.md` 11, `round-22.md` 10, …), so the column format is
untested by the run.

## Did not verify
- The 25-of-28 sealed counter and its receipts (not this seat).
- Live status of any row other than S017.
- Whether bullet (d) should fold Markdown code spans (contract change, L1's call).

## Artifacts
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS017/`: `live-noredir.body`, `live-noredir.hdr`,
`live-follow.body`, `live-follow.hdr`, `S017.body`, `repro/with-bt/`, `repro/rendered/`.
No tool installs or upgrades were needed; no stray processes left running.
