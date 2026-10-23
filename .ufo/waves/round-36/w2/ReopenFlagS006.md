# ReopenFlagS006 — S006 `quote_missing` re-opened by hand

**Verdict: not real as drift — extraction-rule miss on the Gate quote.** The live page is byte-identical
to the recorded snapshot and states the quoted sentence; the quote fails only because it carries two
markdown code-span backticks copied from `corpus/lessons/round-20.md:208`. The tool conforms to frozen
contract (d): the backticked string never exists in the page text or the raw HTML. No row change needed.

## 1. Input and row
- `realrun/input.json`: `{"id":"S006", "url":"https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll", "quote":"Are located in a folder called `/node_modules` or `/vendor`", "from":"round-20.md"}`
- `corpus/SOURCES.md` S006 row: docs, tier A, anchor "Configuring Jekyll in your GitHub Pages site; fetched 2026-10-19", recheck 90d, teaches the default Jekyll exclusions.
- Audit entry: `.ufo/waves/round-36/realrun/audit.json` finding `{"check":"S006","reason":"quote_missing","target":null}`.

## 2. Live open (GET only)
- No-redirect pass: `timeout 120 curl -sS -o live-noredir.body -D live-noredir.headers -w '...' <url>` → exit **0**,
  `HTTP 200 final=<same url> type=text/html; charset=utf-8 size=138096`; headers show **no `location:`** and no
  `etag`/`last-modified` (Varnish HIT, `age: 489`, `date: Fri, 23 Oct 2026 02:04:01 GMT`).
- Follow pass: `curl -sSL ... -w '%{num_redirects}'` → exit **0**, `HTTP 200 final=<same url> redirects=0 size=138096`.
- Hashes: `sha256sum live-noredir.body live-follow.body S006.body` →
  `45f1734141d1d8a10148e7799854cc50308717f54d57ffb70c95608b2c5a34fb` for **all three**. The live page equals the
  recorded `realrun` body (`snap-bodies.tar.xz:./S006.body`, 138096 bytes) byte for byte, so the finding cannot be
  page drift after the snapshot.

## 3. Live text around the quote (tool's own `html_text` applied to the live body)
```
By default, Jekyll doesn't build files or folders that:\n\nAre located in a folder called /node_modules or /vendor\nStart with _, ., or #\nEnd with ~\nAre excluded by the exclude setting in your configuration file
```
Raw HTML at the same place (one `<li>`, deterministic HTML, **not** JS-rendered):
`<li>Are located in a folder called <code>/node_modules</code> or <code>/vendor</code></li>`
Section anchor present live: "Configuring Jekyll in your GitHub Pages site" occurs 5 times in the body; the row's
teaching (underscore/dot/hash prefix, trailing tilde, node_modules, vendor) is stated in that same list.

## 4. Direct reproduction of the finding (recorded body, sandbox manifests)
`python3 -B <lane>/scripts/source_recheck.py --manifest m1/manifest.json` (quote with backticks) →
`{"version":1,"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S006","reason":"quote_missing","target":null}]}` exit **1**.
Same manifest, quote with the two backticks stripped → `{"version":1,"verdict":"clean","checksEvaluated":1,"findings":[]}` exit **0**.
So the sole cause is the two U+0060 characters; wording, case and whitespace match after contract (d) normalization.

## 5. Where the backticks came from
`corpus/lessons/round-20.md:208` writes the quote as markdown: “Are located in a folder called `/node_modules` or `/vendor`”.
The wave-1 gate-quote extractor copied the markdown source verbatim into `input.json`, including the code-span
delimiters, which the rendered page (inline `<code>`) does not contain. Contract (d) (SCORECARD.md:1633) is
case-sensitive substring matching after NFKC + whitespace deletion with **no markdown handling**, so the tool is right
and the input string is wrong. Not a page change, not JS-rendered content (the `<li>` is in the static HTML),
not a paraphrase (the words are verbatim).

## 6. Same-class note (offline, on the recorded snapshots only)
Of the 9 `quote_missing` rows in `audit.json`, 7 quotes carry backticks. Evaluating each recorded body with the same
normalization (one command, `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/source_recheck.py` imported, bodies
from `snap-bodies.tar.xz`): as-is False / with backticks removed True for **S004, S005, S006, S008, S017**; still False
for S007 and S065 (their own seats own those). So at least **5 of the headline 14 findings are pure markdown artifacts**
on the snapshots as recorded, i.e. the real-input headline overstates drift by ≥5 rows. The capability row
(SCORECARD.md:197) says the tool reports "whether each row's quote still occurs in its source" — for markdown-sourced
quotes it conflates formatting with absence; that wording is the overstated part, not the sealed predicate (28/28).

## 7. Row disposition and limits
- S006 stays as is: page fresh, anchor and teaching hold, opened 2026-10-19 within 90d. The only fix is upstream:
  de-render markdown code spans when building `input.json` (or record the rendered quote), not a tool change.
- Not verified: live re-open of S004/S005/S008/S017 (offline class check only, one snapshot each); S007/S065 remain
  unexplained by backticks; the other 6 findings untouched.
- Sandbox deliverables: `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS006/{live-noredir.body,live-noredir.headers,live-follow.body,S006.body,m1/,m2/}`.
- No tool installs or updates. No lane file written except this report.
