# W1 review — urljoin versus WHATWG (C2 resolution semantics)

Seat KakeR29.ReviewUrljoinVsWhatwg; godspeed run. Axes: operability (must the
C2 tool classify like a browser?) and freshness (project-site base-path frontier).

## What I attacked

The C2 contract resolves every reference against the page URL (first `base href`
wins) and tests the resolved path against the base path. Python's
`urllib.parse.urljoin` implements RFC 3986-style merging, browsers implement the
WHATWG URL parser. I resolved every reference value in the frozen matrix plus 22
tricky extras with both engines and classified each result with the matrix's own
contract rules (non-http(s) ignored; other origin ignored; path equal to
basePath minus its final slash or starting with basePath = inside; else
outside_base_path). The Python side models a naive tool: raw `urlsplit` netloc
string compare, no host lowercasing, no default-port folding. Tool state note:
`scripts/base_path_audit.py` is absent at lane HEAD e58b66c (lane and my clone
list no such file), matching the declared "before 0/30 (tool absent)"; I modeled
the contract from the `interface` field of `.ufo/waves/round-29/c2-matrix.json`,
and the must-handle list below applies to the built tool either way.

## Commands run (all exit 0)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r29/w1/ReviewUrljoinVsWhatwg/clone`
- `python3 --version` → Python 3.14.8; `node --version` → v24.21.0 (no installs; pacman untouched)
- `TMPDIR=<sandbox>/tmp python3 -B compare.py` → pairs.json, results.json, full_run.txt

Harness: extract.py parses each case's HTML (html.parser) collecting every
contract attribute value incl. srcset candidates and the first `base href`
resolved against the page URL; whatwg.js resolves with Node `new URL(ref, base)`;
compare.py resolves with urljoin, classifies, diffs.

## Result: 67 pairs (45 matrix + 22 extras), 57 same, 10 disagree

All 45 matrix pairs agree. Every disagreement comes from the extras.

| # | ref (base `https://o.github.io/repo/`) | urljoin 3.14.8 | Node WHATWG | effect for a naive Python tool |
|---|---|---|---|---|
| 1 | `\..\..\x` | inside → `…/repo/\..\..\x` | outside → `…/x` | missed finding |
| 2 | `\\o.github.io\other\` | inside → `…/repo/\\o…` | outside → `…/other/` | missed finding |
| 3 | `\\evil.com\x` | inside | ignored (origin `evil.com`) | both no-finding; browser leaves site silently |
| 4 | `/repo/%2e%2e/other/` | inside | outside → `…/other/` | missed finding |
| 5 | `/repo/%2E%2E/x` | inside | outside → `…/x` | missed finding |
| 6 | `HTTPS://O.GITHUB.IO/other/` | ignored (origin `O.GITHUB.IO` ≠ `o.github.io`) | outside → `…/other/` | missed finding |
| 7 | `https://o.github.io:443/other/` | ignored (netloc `…:443` ≠ `o.github.io`) | outside → `…/other/` | missed finding |
| 8 | `https:///repo/x` | inside (urljoin folds base netloc onto empty authority) | ignored (host `repo`) | same no-finding, wrong reason |
| 9 | `https:///other/` | outside → **false finding** | ignored (host `other`) | false finding |
| 10 | `/repo ` (trailing space on base-minus-slash) | outside → **false finding** (`…/repo ` ≠ `/repo`) | inside (`/repo`) | false finding |

Class-same but resolved text differs (verdict never flipped): D13 ` /x.css `
(urljoin drops the leading space, keeps the trailing one; WHATWG strips both),
`/x\y` (`/x\y` vs `/x/y`), `https:/../x` (both outside — WHATWG keeps the base
authority after a single slash, three slashes promote the first path segment to
host), `/re\tpo/x`, `/style.css\n`, `/st\rstyle.css` (urljoin already removes
ASCII tab/LF/CR anywhere, matching WHATWG), `/./repo/x`, `/repo/./../repo/x`,
`?`, `#`, `/repo/x `.

## What the tool must handle (behavioral, browser-faithful)

1. Backslashes: for http(s) refs, replace `\` with `/` before resolving (WHATWG
   special-scheme rule). Covers rows 1–3; without it `..\`-style references pass
   silently while a browser navigates outside the base path.
2. Percent-encoded dot segments: a segment whose percent-decoded form is `..`
   (WHATWG "double-dot path segment": `..`, `.%2e`, `%2e.`, `%2e%2e`,
   case-insensitive) must resolve as dot-dot. Covers rows 4–5.
3. Origin comparison: compare scheme plus `urlsplit().hostname` (lowercased)
   plus effective port (`port` else 80/443 default). Covers rows 6–7; plain
   netloc string equality silently drops real findings on uppercase hosts or
   explicit `:443`.
4. Empty authority with a scheme: if the ref carries a scheme and an empty
   netloc, never inherit the base netloc (urljoin does); treat as origin
   mismatch or input-invalid. Covers rows 8–9; row 9 is a false finding today.
5. Whitespace: strip leading and trailing C0-control-and-space before resolving
   (urljoin strips only the leading end); keep reporting the raw value in the
   finding, as the contract already says. Covers row 10, the K4 boundary.

Also document (no observed verdict flip): interior-backslash resolved text, single-slash
`https:/…` authority behavior, `%2f` left raw by both engines, `resolved`-field percent-encoding.

## Residual risk and what I did not verify

- WHATWG reference is Node v24.21.0 (Ada URL), spec-aligned but not a direct
  Chrome/Firefox probe; no live probes of any web property (bounds).
- I reviewed the contract, not the tool: `base_path_audit.py` did not exist at
  HEAD when I ran; re-check these rows against the built implementation.
- Untested for verdict impact: srcset URLs containing commas (harness splits on
  commas; no matrix case needs more), non-ASCII/IRI references (observed only as
  resolved-text differences).

## Evidence

- Sandbox `/fast/scratch/hyaku/kake-r29/w1/ReviewUrljoinVsWhatwg/`: extract.py,
  whatwg.js, compare.py, pairs.json, results.json, full_run.txt; TMPDIR inside
  the sandbox; nothing written to /tmp.
- sha256 — full_run.txt 637e9762fe4cd7aae550224c7ad5bd9a54582f20341d17e81022ec92e45cd238;
  results.json 696dd17dc68a8275cb6bad73bc6860af7a3bc08e1e1e0f2c65ed55256d1410fb; pairs.json e4e1df1bd4a7874d4f74019d9dfe0b18a40f2b2b7f7684c819f65b4c16d2bb6a.
- Matrix `.ufo/waves/round-29/c2-matrix.json` (588 lines, 30 cases, `interface` field = contract);
  lane HEAD at clone time: e58b66c. No lane files other than this report were touched; no git/jj state changed.
