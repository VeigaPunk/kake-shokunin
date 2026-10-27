# ProbeBodyStability

Seat: `ProbeBodyStability` (leaf, wave 1 of round-59, lane `kake-shokunin`).
Scope: stability of the two retained C3 source bodies (S425, S426) under repeated fetches, and a
recheck grep span per page that does not cross a source line break.
Scratch (deleted at end): `/fast/scratch/hyaku/kake-r59/ProbeBodyStability/`; receipts copied to
`.ufo/waves/round-59/w1/ProbeBodyStability.files/`.
No lane file was read for writing; no git/jj mutation was performed in the lane, in the fleet repo or
in any fixture (no fixture repo was needed: this seat only fetches and compares).

## FETCHES:

Tool: `curl` (system `/usr/bin/curl`), UA `kake-shokunin-round59-probe`, `Accept-Language: en-US,en;q=0.9`,
`--compressed`, `--max-time 60`, 3 fetches per URL, the two URLs fetched concurrently, 35 s sleep between
rounds (round start times 01:46:26Z, 01:47:01Z, 01:47:37Z → inter-fetch spacing 35 s / 36 s, both >= 30 s).
All six responses were HTTP 200. Command: `ProbeBodyStability.files/fetch.sh`.

S425 `https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers`

| fetch | UTC | bytes | sha256 |
|---|---|---|---|
| retained (2026-10-27T01:21:22Z, UA `kake-shokunin-round59`) | — | 74477 | `ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa` |
| f1 | 2026-10-27T01:46:26Z | 74481 | `f530c83298ebae178a558f8601dcbeb41c4ede4af382438a144a30c2aaed7855` |
| f2 | 2026-10-27T01:47:01Z | 74481 | `72f57c6ca637e1e40deb38ee829ba2028f2880d8f5e4d6b6dcb7be4e3d6614c0` |
| f3 | 2026-10-27T01:47:37Z | 74477 | `5615df49b5a20c2854d05c668ec0e08e6a84651417023b61143c13563b0212bc` |

S426 `https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests`

| fetch | UTC | bytes | sha256 |
|---|---|---|---|
| retained (2026-10-27T01:21:22Z, UA `kake-shokunin-round59`) | — | 69789 | `8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879` |
| f1 | 2026-10-27T01:46:26Z | 69793 | `47433651fd7322e1f84d9bb01c42ddc23386884adf7ce832ad5a9c2a50ef8943` |
| f2 | 2026-10-27T01:47:01Z | 69789 | `097119218ffb4cd37dc2daff3974b32b38274ce69afbe221b1f370009e2c3665` |
| f3 | 2026-10-27T01:47:37Z | 69793 | `04bbc7b74cdccc29a9439eb602e36bbbfccc1fd4ed685428ce57260b7728bfcd` |

Facts established: the retained bodies' digests equal the frozen `BODY_SHA256` in
`.ufo/waves/round-59/c59_quote_truth.py` and the `sha256`/`bytes` in `sources/receipts.json`
(both `match=True`, recomputed from the on-disk bytes). No fresh fetch reproduces the retained
sha256 for either page: **full-body sha256 is not stable** on either URL.

## VARIATION:

Variation was computed two ways: (a) with the counter's own extractor
(`c59_quote_truth.py` `content_window()` + `text_segments()`, i.e. exactly the article-block text
nodes the C5 test sees) and (b) byte/line level on the raw files.

Article text (counter-visible):
- S425: 217 text nodes / 6424 node chars in the retained body and in f1, f2, f3. The node lists are
  identical **in order and content** (`identical_order=True`) for retained-vs-f1, retained-vs-f2,
  retained-vs-f3, f1-vs-f2, f1-vs-f3.
- S426: 165 text nodes / 3775 node chars in all four bodies; identical in order and content, same
  comparisons.
- Raw article-block bytes are also identical: sha256 over raw lines 1073..1343 (S425)
  = `5a1ddff09a7239e312433449175f7ed8b30a16b002873a712289292011398f06` and over raw lines 1073..1272
  (S426) = `d45be935f445b4e46564b648133bd61ed3255eb3f157919a5d02df6135253085` for the retained body
  **and** for f1, f2, f3 (one digest each, four bodies). Article-block raw line ranges are
  `1073..1343` (S425) and `1073..1272` (S426) in every body; whole-file line counts are identical
  across the four bodies (2084 for S425, 2013 for S426).

Varying regions (the only differences; all outside the article block — `varying_inside_article=[]`):
- S425: raw lines **2062, 2073, 2078**. S426: raw lines **1991, 2002, 2007**.
  - one line with `<script type="application/json" analytics>`: the Google-Analytics dimension JSON —
    key order and the presence of individual `dimensionN` keys vary per response
    (e.g. S425 retained starts `dimension6, dimension5, …`, f1 starts `dimension11: false, dimension6, …`).
  - one `<script nonce="…">` line: a fresh CSP nonce per response
    (S425 retained `2/XydDFrTB3/evDyPSvKFFm+miv1WK` vs f1 `TZfU55c90hvNAqYMtXZn7VFXD/dU1v`, etc.).
  - one devsite boot-payload line (~8.5 kB): the `MiscFeatureFlags__*` / `Profiles__*` /
    `Search__*` feature-flag list and the experiment-id map — both membership and ordering vary per
    response; this line alone accounts for the ±4-byte body-length difference.
- Characterisation: **page chrome varies, article text does not.** The counter's `BODY_SHA256`
  freeze is therefore only satisfied by the retained blob as committed (it is: verified above); a
  re-fetch cannot be expected to reproduce the frozen digest. [INFERENCE] The C5/C6 checks compare the
  digest of the *committed* body (`show_bytes(root, rev, path)`), not of a fresh fetch, so this
  instability does not by itself falsify C5 or C6 — but any recheck that re-fetches and compares
  digests would report a false difference.
- The printed revision anchors are stable across all four bodies and are **outside** the article
  block window: S425 prints `Last updated 2026-06-12 UTC.`, S426 prints `Last updated 2026-03-20 UTC.`
  (each twice: once in a `<p>` after the article end marker, once inside the boot payload). The
  counter's C5 revision check scans text nodes of the whole body (`re.findall(r">([^<>]+)(?=<)", …)`),
  not only the article block, so the anchor is found there; note the in-article-block node scan
  (`text_segments`) finds no `Last updated` node in either page, in any of the four bodies — i.e. that
  anchor text is not inside the article block for either row.
- `article_headings()` is stable: S425 has 7 h2/h3 headings in the article block, S426 has 2, in all
  four bodies.

## RECHECK SPANS:

One span per page, each satisfying: (a) a substring of exactly ONE whitespace-collapsed text node of
the article block (counter `in_content`), (b) 6..25 units and <= 160 characters, (c) page-unique
(`count_in_body == 1` and 0 occurrences in the other page's body), (d) carries the row's page-named
subject (`TOPIC["S425"] = "IP address"`, `TOPIC["S426"] = "reverse DNS"`), and (e) does **not** cross a
source line break: a plain `grep -F` finds it on exactly ONE raw line of every body, and that line
number is the same in the retained body and in all three fresh fetches.

S425 — raw line 1128 (identical line number in retained, f1, f2, f3; inside article block 1073..1343):

    Therefore, your logs may show visits from several IP addresses.

`span_tools.py check S425` (counter's own test, on the retained body):
`{'units': 10, 'chars': 63, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}`
— 10 units, 63 chars, inside one text node, page-unique, carries `IP address`.
Re-verified against all three fresh fetches: `in_one_text_node=True`, `count_in_body=1`,
`raw_line_hits=[1128]`. Raw line 1128 is `  might access. Therefore, your logs may show visits from
several IP addresses.` — the span begins mid-line, so it does not cross a line break.

S426 — raw line 1160 (identical line number in retained, f1, f2, f3; inside article block 1073..1272):

    Run a reverse DNS lookup on the accessing IP address from your logs, using the

`span_tools.py check S426` (counter's own test, on the retained body):
`{'units': 15, 'chars': 78, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}`
— 15 units, 78 chars, inside one text node, page-unique, carries `reverse DNS`.
Re-verified against all three fresh fetches: `in_one_text_node=True`, `count_in_body=1`,
`raw_line_hits=[1160]`. Raw line 1160 is `    Run a reverse DNS lookup on the accessing IP address
from your logs, using the` — the span ends before the following `<code translate="no" …>host</code>`
line, so it does not cross a line break.

Both spans are stable across the three spaced fetches and identical between the retained bodies and
the fresh bodies; both were stable under a different UA than the retained fetch
(`kake-shokunin-round59-probe` here vs `kake-shokunin-round59` in `receipts.json`), which is the
strongest evidence that the article text is UA-independent and the chrome is per-response noise.

Recheck command (fetches into scratch; no lane writes):

    curl -sS -A 'kake-shokunin-round59-probe' -o body.html "$URL" && grep -nF 'Therefore, your logs may show visits from several IP addresses.' body.html

Secondary, equally stable spans observed (same line-number stability, useful as backups):
S425 line 1129 `Google egresses primarily from IP addresses in the United States.`; S425 line 1276
`The source IP address of the request.`; S426 line 1160 alternative
`reverse DNS lookup on the accessing IP address from your logs` (11 units, 61 chars).

Receipts: `.ufo/waves/round-59/w1/ProbeBodyStability.files/` — `fetch-timeline.txt` (fetch times,
bytes, digests), `fetch.sh` (exact fetch command), `analyze.py`/`analyze.out` (article-node
equality, line-level diffs), `summary.py`/`summary.out` (varying-region classification, span table),
`spans.py`/`spans.out` (span candidates), `spans2.py` (boot-line opcode detail), `final.py`/`final.out`
(counter-verdict re-check per span).

No tool was installed or upgraded for this seat (system `curl` and `python3` 3.14.8 sufficed), so
no tool/version/channel/reason record is owed under the operator tooling directive.

## VERDICT:
Hypothesis confirmed: the S425/S426 article text is byte-stable across three >= 30 s-spaced fetches
(and across two user agents), while only three chrome lines per page vary (analytics dimension JSON
key order, CSP nonce, devsite boot payload) — so the retained bodies' frozen sha256 is not
reproducible by re-fetching, but every C3 quote span tested is; recommended recheck spans
`Therefore, your logs may show visits from several IP addresses.` (S425, raw line 1128) and
`Run a reverse DNS lookup on the accessing IP address from your logs, using the` (S426, raw line 1160)
each sit on a single source line and pass the counter's own span check.
