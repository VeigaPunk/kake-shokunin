# Round 29 wave 1 — CriticMatrixOracle: attack on the C2 frozen matrix expectations

Seat: critic, leaf, advisory only. Target: `.ufo/waves/round-29/c2-matrix.json` (sha256 `75c08f641a31356d0f3446d9e6e435c44ee02bc4cf49102904e2466dbac2e84a`, lane head `e58b66c`). Axis judged: operability.

## Bottom line
- Matrix errors: none. All 30 expected outcomes are correct for a GitHub Pages project site under the contract as written. An independent oracle (Python `html.parser` for extraction, Node 24.21.0 `new URL()` for resolution, the contract's inside rule) agrees on 21 of 21 control and defect cases. The 9 input and usage cases agree with the interface text by reading.
- One contract defect: the "ignored: other origins (scheme, host, port)" rule (matrix line 11) silently passes `http://o.github.io/other/` on an https page. S040 documents the project site as reachable over both schemes, so this is a false negative. It is a gap, not a wrong expectation, because no case pins it.
- Main operability risk: the matrix cannot tell a WHATWG-correct implementation from a Python `urljoin` one. I found six divergence classes, all invisible to the 30 cases. The counter can reach 30/30 with a tool that misses real escapes.

## Evidence commands (sandbox `/fast/scratch/hyaku/kake-r29/w1/CriticMatrixOracle/`, TMPDIR inside it)
- `python3 -B extract.py <matrix> > extracted.json` exited 0. `node resolve.mjs < extracted.json` exited 0 and printed "oracle agrees on 21/21 control+defect cases" (`oracle.out`).
- `node probe_node.mjs probes.json` exited 0 (`probe_node.out`). `python3 -B probe_py.py probes.json` exited 0 (`probe_py.out`, Python 3.14.8). The probes are 36 adversarial values against page `https://o.github.io/repo/` with base path `/repo/`.
- `python3 -B html_probe.py` exited 0 (HTML parser edge cases).
- Quote check: each quote below is an exact substring of the retained text at the shown offset. Text sha256: S040 `625f2b07…`, S041 `86a77ee2…`, S042 `b66fefc1…`, S043 `d665dd23…`.

## The six attacked expectations
- **K4, base path minus its final slash is inside** (lines 59–71). Fine. S040@2215 "Default site location http(s):/ / <owner>.github.io http(s):/ / <owner>.github.io/ <repositoryname>" and S041@3569 "…such as username.github.io/project" give the site location without a final slash. Probes: `/repo`, `/repo?x=1` and `/repo#top` give pathname `/repo` and are inside; `/repo.css`, `/repo;x` and `/repo%2F` are outside under both Node and Python. That the server redirects `/repo` to `/repo/` is [INFERENCE] and not in the retained sources. The page-URL rule is still open: "page URL whose path is under basePath" (line 9) does not say whether page `https://o.github.io/repo` is accepted. If it were, relative references would resolve against `/`.
- **D9, case-sensitive path** (lines 283–300). Fine as policy, but it must be stated as a documented limit. WHATWG keeps path case, so `/Repo/x` resolves to `/Repo/x`. Whether GitHub Pages folds case in the repository segment is not in S040–S043 [unverified; no live probe allowed]. If it does, D9 is a conservative false positive, not a wrong expectation. The host is the reverse case: `https://O.GITHUB.IO/repo/x` must be inside. Node lowercases the host, but Python `urlsplit().netloc` keeps `O.GITHUB.IO`, so a netloc-comparing tool would wrongly ignore it. No case pins this.
- **Cross-scheme, same host, ignored** (interface line 11; no case). Contract defect, documented limit for this round. S040@2215 "http(s)" shows both schemes serve the site. `http://o.github.io/other/` leaves the project site but is ignored by both oracles ("ignored-other-origin-SAME-HOST"). Related: `https://o.github.io:443/other/` is outside under Node (default port dropped) but ignored under Python, which compares port 443 with None, so it is a false negative. Custom domains (S040@2349 "You can host your site on GitHub's github.io domain or your own custom domain.") create an alias host that the tool also treats as foreign.
- **K3, non-http references ignored** (lines 44–57). Fine. `mailto:`, `tel:`, `javascript:` and `data:` fetch nothing on the site, and `ftp://o.github.io/x` is ignored under both. The scheme must be read after parsing: `HTTPS://o.github.io/other/` is outside under both. A raw `startswith("http")` check would ignore it, and no case pins that.
- **D13, raw value with spaces** (lines 374–393). Fine. The URL parser strips leading and trailing C0 control and space, so `" /x.css "` resolves to `/x.css`, outside, and the raw value `" /x.css "` matches the interface's finding value rule. Two caveats. First, Python `urljoin` gives resolved `https://o.github.io/x.css ` with a trailing space (Node gives none); the `resolved` field is not compared, so the tool documentation must say which resolver it uses. Second, the ignore rule strips ASCII whitespace while the URL parser strips C0 controls (`\u000b/x.css` resolves to `/x.css` in both). A value of only `\u000b` resolves to the page URL, which is inside, so the verdict is the same.
- **D8, segment prefix** (lines 262–281). Fine. `/repository/x` is outside under both, as are `/repo.css` and `/repo;x`. Strongest neighbour: `//repo/x` (a typo for `/repo/x`) resolves to host `repo` and is ignored as another origin. That is a real broken link the tool cannot report: documented limit.

## Remaining 24 cases (fine unless noted)
- K1 (`#top`, `?q=1`, `./x/` and `img/a.png` resolve under `/repo/`), K2, K5 (with base `/`, base minus slash is empty and never equals a pathname), K6 (first base with href wins; S024), K7 (empty href resolves to the page URL, inside, same verdict): fine.
- D1, D2 and D6 match the grounding: S041@1765 "The subdirectory-like URL structure GitHub uses for Project Pages complicates the proper resolution of URLs."; S042@786 "Prepend baseurl config value to the input to convert a URL path into a relative URL."; S043@3331 "set base to '/<REPO>/'".
- D3, D4, D5, D10, D11, D12 and D14: fine. The oracle reproduces each exact tuple multiset.
- D7: fine. Because the counter compares whole multisets (`c2_matrix_count.py:62-72`), a tool that also reported `<base href="/">` itself would fail. The contract therefore implies the base element is not a reference; the documentation should say so.
- I1–I8 and U1: fine by reading against interface lines 7–9. Not executed, because no tool exists yet.

## WHATWG versus Python `urljoin` divergences the matrix does not pin (gaps, not errors)
Each pair below is Node verdict, then Python verdict.
1. `\style.css`: Node outside, Python inside (a false negative). `\\o.github.io\x`: Node outside, Python inside.
2. `/repo/%2e%2e/x` and `/repo/.%2E/x`: Node outside (resolves to `/x`), Python inside (a false negative).
3. `https://o.github.io/repo/../other/` and `//o.github.io/repo/../other/`: Node outside, Python inside, because `urljoin` skips dot-segment removal when a host is present (a false negative).
4. `/\cdn.example.net/x`: Node treats it as another origin; Python reports it outside (a false positive).
5. `:443` default port: Node outside; Python ignores it (a false negative).
6. Uppercase host compared through netloc: Node inside; Python ignores it as another origin.

HTML side (Python 3.14 `html.parser`): `<title>` and `<textarea>` contents are not parsed, which is correct. Comments are skipped. Duplicate attributes come through in order, so the tool must keep the first, as the HTML spec does. `<template>` content is exposed even though browsers never fetch it: a false-positive risk.

## Limits the tool documentation must state
1. Only the page's own origin is audited. Same host over the other scheme, default-port spellings (unless normalized), and custom-domain or `github.io` aliases are treated as foreign and ignored.
2. Path comparison is case-sensitive, and percent-encoding is not decoded: `/re%70o/x` is outside under both, though a server may serve it as `/repo/x` [INFERENCE].
3. Paths that look like host typos (`//repo/x`) and any other-origin breakage are out of scope.
4. Only the listed element and attribute pairs are references. Not covered: `formaction`, `object[data]`, `input[type=image][src]`, `link[imagesrcset]`, SVG `href`, `meta http-equiv=refresh`, CSS `url()`, `@import`, JavaScript-built URLs, and `<base>` itself.
5. The resolver must be named. If it is not WHATWG-equivalent, state divergences 1–6 above. `<template>` content and duplicate-attribute handling must also be stated.
6. Whether a page URL equal to the base path minus its final slash is accepted.
7. Whether GitHub Pages redirects `/repo` to `/repo/`, and whether it folds case, is unverified by the retained sources.

## Smallest safe corrections (the matrix is frozen, so these are for the L1 or next round, not edits now)
- This round: put limits 1–7 in the tool's documentation, and do not claim scheme, port or encoding coverage.
- Next round: change the ignore rule to "other hosts, or non-default ports". Add cases for `http://o.github.io/other/` (expect a finding), `/repo/%2e%2e/x`, `https://o.github.io/repo/../other/`, `\style.css`, `https://O.GITHUB.IO/repo/x` (expect clean), `https://o.github.io:443/other/`, and a page URL of `https://o.github.io/repo`.

Side note for the C1 seat: the S040 receipt shows the requested `…/about-github-pages` URL redirected to final URL `…/what-is-github-pages` (`sources/receipts.json`).

## Not verified
No `base_path_audit.py` exists at `e58b66c`, so the counter was not run. GitHub Pages server behaviour (redirects, case, percent-decoding) was not probed; no network was used. Installs: none.
