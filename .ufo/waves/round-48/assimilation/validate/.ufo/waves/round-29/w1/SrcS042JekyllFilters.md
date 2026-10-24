# SrcS042JekyllFilters — S042 (Jekyll Liquid filters) base-path extraction

Seat: `KakeR29.SrcS042JekyllFilters` (leaf scribe, read-only). Axis named: **freshness**.
Scope: only what the S042 page says about `relative_url` and `absolute_url`.

No product-code edit, no registry edit, no commit, no install, no build/test.

## Target and retained bytes

| field | value |
|---|---|
| source id | S042 |
| URL / final URL | `https://jekyllrb.com/docs/liquid/filters/` (no redirect) |
| retained text | `.ufo/waves/round-29/sources/S042.txt`, 9266 bytes, 1 line, 1432 words |
| retained text sha256 | `b66fefc15f2b1ba5d83f1c15db7b6dff52b19af442fc9e2faeb4b349321fec31` |
| receipt (sources/receipts.json) | status 200, accessed 2026-10-22T10:29:37Z, bodyBytes 40985, bodySha256 `610d127b38f9c9766c71753903666334ae3feb09d9793c00789885d4ff79e91a`, textSha256 `b66fefc1…` |

The retained text sha256 equals the receipt `textSha256` — the retained file is the file the counter will read.

## Freshness re-open (one public GET, no browser)

I re-opened the same URL once with the same ordinary GET the round's fetch script uses.

```
python3 -B (inline) — urllib GET https://jekyllrb.com/docs/liquid/filters/
at 2026-10-22T10:33:25Z status 200 final https://jekyllrb.com/docs/liquid/filters/
bodyBytes 40985 bodySha 610d127b38f9c9766c71753903666334ae3feb09d9793c00789885d4ff79e91a
textSha b66fefc15f2b1ba5d83f1c15db7b6dff52b19af442fc9e2faeb4b349321fec31 words 1432
```

**Live bytes are byte-identical to the retained body** (same 40985 bytes, same body sha256) and the live derived visible text is byte-identical to the retained text (same text sha256, same 1432 words). No drift. The page carries no visible "last updated" stamp; freshness rests on this identical-byte re-open.

Sandbox copies: `/fast/scratch/hyaku/kake-r29/w1/SrcS042JekyllFilters/S042.live.html.gz`, `S042.live.txt`.

### Version marker observed

The page's site meta links to the Jekyll release `v4.4.1` (nav `<a href="https://github.com/jekyll/jekyll/releases/tag/v4.4.1">v4.4.1</a>`), and `<meta name="generator" content="Jekyll v4.4.1" />`. The retained visible text contains the token `v4.4.1` once, in the nav. The page states no per-page revision date, so `v4.4.1` is the only revision marker available; the anchor cell names it.

### HTML anchor structure (from the live body, for the anchor cell)

- Page heading `<h1>Liquid Filters</h1>`.
- One table, header row `Description | Filter and Output`.
- Row anchors: `<p id="relative-url" class="name"><strong>Relative URL</strong></p>` and `<p id="absolute-url" class="name"><strong>Absolute URL</strong></p>`.
- Each row has a `<p class="filter">` code line and a `<p class="output">` result line, which is why the retained text shows filter and output adjacent.

## Statements and verified quotes

Every quote below was re-checked by me, three ways: (a) substring test against the whitespace-collapsed retained text, (b) substring test against the raw retained bytes, (c) an independent `grep` of the retained file. All five are ≤25 words and all five pass the counter's flip-letter control (the first letter flipped to `q`/`z` does **not** occur in the retained text).

**S1 — `relative_url` prepends the `baseurl` config value.**
Quote (16 words): `Prepend baseurl config value to the input to convert a URL path into a relative URL.`

**S2 — The page recommends `relative_url` for a site hosted on a subpath of a domain.**
Quote (15 words): `This is recommended for a site that is hosted on a subpath of a domain.`
This is the subpath recommendation; it is the sentence that connects the filter to the round's frontier (a GitHub Pages project site is served under `/<repo>/`).

**S3 — The `relative_url` worked example prepends `/my-baseurl` to the input path.**
Quote (6 words): `{{ "/assets/style.css" | relative_url }} /my-baseurl/assets/style.css`
In the live HTML this is the `<p class="filter">` line followed by the `<p class="output">` line ` /my-baseurl/assets/style.css`; the retained text keeps them adjacent.

**S4 — `absolute_url` prepends the `url` and `baseurl` values.**
Quote (17 words): `Prepend url and baseurl values to the input to convert a URL path to an absolute URL.`

**S5 — The `absolute_url` worked example produces a scheme-qualified URL.**
Quote (6 words): `{{ "/assets/style.css" | absolute_url }} http://example.com/my-baseurl/assets/style.css`

### What the page does not say (scope limits for the L1)

- It does not mention GitHub Pages, `username.github.io`, project sites, or any repository name.
- It does not define `baseurl` or `url` values; it only says which values the filters prepend. The definition of `baseurl` belongs to S041, not S042.
- It does not say a root-relative path is wrong, only that `relative_url` is "recommended" for a subpath-hosted site. Do not upgrade "recommended" into "required".
- The page contains `relative_url` and `absolute_url` exactly once each; there is no second mention elsewhere on the page to cross-check.

## Proposed S042 registry row (11 cells)

```markdown
| S042 | Jekyll Docs: Liquid Filters — https://jekyllrb.com/docs/liquid/filters/ | docs | A | Jekyll relative_url and absolute_url filter semantics for base-path-prefixed links | Liquid Filters page, table rows "Relative URL" and "Absolute URL"; Jekyll docs v4.4.1, accessed 2026-10-22 | relative_url prepends the baseurl config value and is recommended for a site hosted on a subpath of a domain | mined | 2026-10-22 | on-release | corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md |
```

Cell-by-cell: `id` S042 · `source` Jekyll Docs: Liquid Filters — canonical URL · `kind` docs · `tier` A (primary docs for its scoped topic, per CORPUS.md tier rule; `docs` is not excluded from A) · `scope` the filter semantics only · `anchor` heading plus the two named table rows plus the `v4.4.1` marker and access date (CORPUS.md requires a revision marker, never a bare homepage) · `teaches` one grounded benefit (S1 + S2) · `status` mined · `opened` 2026-10-22 · `recheck` on-release (the page has no per-page date; the Jekyll release tag is the only version handle) · `used-by` the entry and the round lesson.

## Proposed lesson Gate line for S042

```markdown
- S042 — https://jekyllrb.com/docs/liquid/filters/ — accessed 2026-10-22, Liquid Filters page, table rows "Relative URL" and "Absolute URL": “Prepend baseurl config value to the input to convert a URL path into a relative URL.”
```

**L1 caution:** the counter extracts quotes with a curly-quote regex and requires **exactly one** quoted span on the `- S042 — ` line, so this line must carry a single quoted sentence. S2–S5 belong in a separate "further located support" table (round-28 used that shape), not in additional curly quotes on the same line.

## Verification performed

Harness: `/fast/scratch/hyaku/kake-r29/w1/SrcS042JekyllFilters/s042_sim.py` (reads the lane read-only; re-implements the counter's own rules for S042).

```
$ python3 -B s042_sim.py ; echo "exit=$?"
retained text sha256 matches receipt: True
relative_url prepends baseurl words=16  in_text=True flip_ok=True -> PASS
subpath recommendation       words=15  in_text=True flip_ok=True -> PASS
relative_url worked example  words=6   in_text=True flip_ok=True -> PASS
absolute_url prepends url+baseurl words=17  in_text=True flip_ok=True -> PASS
absolute_url worked example  words=6   in_text=True flip_ok=True -> PASS
row cells: 11
  row.cell_count_ge_11: True   row.status_mined: True   row.opened_2026_10_22: True
  row.url_in_source_cell: True  row.id_cell: True
gate line quote count: 1 words: 16 in_text: True ->  PASS
OVERALL: PASS
exit=0
```

The simulated checks mirror `.ufo/waves/round-29/c1_quote_truth.py`: row cell count ≥11, `status` == `mined`, `opened` == `2026-10-22`, the receipt URL present in the source cell, quote length 1..25 words, quote present in the collapsed retained text, and the flip-letter control not broken.

**Not verified:** the real counter was not run, because it needs a commit that contains the S042 row, the `corpus/knowledge/pages-base-path.md` entry, `corpus/lessons/round-29.md`, and the retained sources — none of which exist yet (`pages-base-path.md` and `lessons/round-29.md` are both absent in the lane today). The L1 must run
`python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision <commit>` after integration.

## Overlap note for the L1

S041 (`https://jekyllrb.com/docs/github-pages/`) also mentions `relative_url` and states that project output is served "under a subpath of your user pages subdomain, such as username.github.io/project". That is S041's ground, not S042's. S042's contribution is the filter semantics and the subpath recommendation; do not merge the two rows' teaching.

## Actions and bounds

Read the lane's retained S042 text, receipts, SOURCES contract, and the C1 counter. Performed one public GET of the one named URL (same site, no other page). Wrote only this report inside the lane; all other artifacts are in the sandbox. No install, no pacman, no git/jj write, no registry or corpus edit, no second judge, no subagent.

Artifacts (sandbox): `/fast/scratch/hyaku/kake-r29/w1/SrcS042JekyllFilters/{s042_sim.py,quotes.json,row.md,gate.md,S042.live.html.gz,S042.live.txt}`.

Report: .ufo/waves/round-29/w1/SrcS042JekyllFilters.md
