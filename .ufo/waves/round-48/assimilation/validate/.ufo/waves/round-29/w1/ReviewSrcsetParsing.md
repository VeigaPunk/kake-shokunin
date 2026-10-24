# Kake R29 wave 1 — ReviewSrcsetParsing (C2 srcset splitting: spec vs naive comma split)

Axes: operability (candidate-URL extraction for the C2 base-path audit contract), freshness (pinned
to the live WHATWG text fetched this round). Leaf reviewer, advisory only. Sandbox:
/fast/scratch/hyaku/kake-r29/w1/ReviewSrcsetParsing/. No tools installed, no pacman use, no
fleet-repo mutation; the only lane file written is this report.

## What was attacked

Question: for the C2 contract line "img/source[srcset] (each candidate URL)" (c2-matrix.json:10-12),
is `value.split(',')` a faithful implementation of "each candidate URL"? Compared against the WHATWG
"parse a srcset attribute" algorithm.
Source opened this round (one GET, 2026-10-22):
https://html.spec.whatwg.org/multipage/images.html#parsing-a-srcset-attribute (§4.8.4.3.10) plus
same-page grammar §4.8.4.2.1 #srcset-attributes. Retained at
/fast/scratch/hyaku/kake-r29/w1/ReviewSrcsetParsing/spec-images.html (262,494 bytes, sha256
3d9f0ba680cda1e97cf0453575279b5ede6609846c9ba0041b947825e23a2279), extracted visible text in
spec-srcset-parsing.txt / spec-srcset-grammar.txt (same directory).

## Located spec quotes (exact visible text, <=25 words each)

Q1 (21 words, URL token is whitespace-delimited, not comma-delimited): "Collect a sequence of code points that are not ASCII whitespace from input given position, and let url be the result."
Q2 (14 words, a comma only terminates a URL when it ends the token): "If url ends with U+002C (,): Remove all trailing U+002C COMMA characters from url."
Q3 (10 words, grammar §4.8.4.2.1 — authoring side): "each separated from the next by a U+002C COMMA character".
Authoring and parsing disagree on glued input; the parsing algorithm is what browsers run, so it is
the right contract for auditing real pages. Each quote verified as an exact substring (count=1) of
the retained text.

## Battery: inputs, expected candidates (spec), naive split

spec = faithful port (splitting loop; URL = non-whitespace run; trailing-comma strip; descriptor
tokenizer with paren state; candidate appended only when descriptor parse error = no); naive =
`split(',')` + strip + first whitespace token. Script battery.py sha256
48358b2cfb48b9dcb60d0271d18a605f38b7f1a50f1fd7b67284455a2b646c9a and output battery.out sha256
d01169092c965122a61ffe0f47cfd89291c6c85698b2335d3896242bbd77057b, both in /fast/scratch/hyaku/kake-r29/w1/ReviewSrcsetParsing/.

| id | srcset value | spec candidates | naive candidates | verdict |
|----|--------------|-----------------|------------------|---------|
| S1 | `a.png 1x, /b.png 2x` | a.png; /b.png | same | agree |
| S2 | `a.png 1x,b.png 2x` | a.png; b.png | same | agree |
| S3 | `a,b.png 1x` | a,b.png | a; b.png | BREAK |
| S4 | `data:image/png;base64,iVBORw0KGgo= 2x` | data:image/png;base64,iVBORw0KGgo= | data:image/png;base64; iVBORw0KGgo= | BREAK |
| S5 | `https://example.com/a,b.png 2x` | https://example.com/a,b.png | https://example.com/a; b.png | BREAK |
| S6 | `a.png 1x,/b.png` | a.png; /b.png | same | agree |
| S7 | `a.png,/b.png 2x` | a.png,/b.png (one URL) | a.png; /b.png | BREAK |
| S8 | `,a.png 2x` | a.png | a.png | agree |
| S9 | `a.png 1x,,b.png` | a.png; b.png | same | agree |
| S10 | `a.png (density 2)` | (none — descriptor parse error) | a.png | BREAK |

## Findings (severity order, advisory)

F1 medium (operability): S7 is the audit-relevant divergence. Naive split emits a root-relative
`/b.png` the spec never produces; per the algorithm the single URL is `a.png,/b.png`, which resolves
under the page directory (e.g. https://o.github.io/repo/a.png,/b.png — inside basePath, no finding),
so a comma-splitting tool reports a false-positive root-relative finding. The differential is
false-positive-dominant; no input found where naive misses a spec candidate yielding a root-relative
finding (absence claim backed by the 10-case battery).

F2 low (operability): S3/S4/S5 — a comma inside a URL stays part of the URL (Q1); naive corrupts the
candidate and invents fragments (`a`, `b.png`, `iVBORw0KGgo=`). The C2 finding value "the candidate
URL text" is then wrong even when the inside/outside verdict is unaffected; data URL fragments are
non-http(s) and ignored per c2-matrix.json:11, so no false finding there today.

F3 low (contract sharpness): S10 — the spec appends an image source only when descriptor parsing
sets error = no; `a.png (density 2)` yields zero candidates, so a matrix row treating every URL token
as a candidate would diverge from browsers. `2x /b.png`-style shapes (URL-first-token bias) drop text
that is not a candidate either way — no divergence found in the battery.

F4 info (freshness frontier): §4.8.4.2.1 authoring rule requires a no-descriptor candidate to be
followed by whitespace before the next (Q3 context); glued inputs like S7 are nonconforming authoring
yet still parse to one URL — auditors must implement the parser, not the authoring grammar. The
frozen 30-case matrix (c2-matrix.json:157-173; D3 uses `"a.png 1x, /b.png 2x"`) has only
space-after-comma srcset shapes, so it does not distinguish the two implementations today; flagged
for the L1 if the matrix is ever revised — not my seat to change it.

## Grounding in the live corpus (negative)

No srcset occurrences in any round-23 snapshot: 0 in all 8 page.html files present (burnerchrome-kimi,
charter-ghp, ds4cc-kimi, ds4cc-primary, lucario-ghp, plazir15-ghp, ufo-fsd-kimi-pro,
vault-index-kimi); charter-kimi, lucario-kimi, plazir15-kimi, plazir27-kimi have no page.html (grep
os error 2). So this is a robustness/frontier item for the C2 contract, not a found live-site bug.

## Commands run (exit codes)

1. `curl -sS -L --max-time 60 'https://html.spec.whatwg.org/multipage/images.html' -o spec-images.html` — exit 0; python section extraction — exit 0.
2. Quote substring verification (python, normalized counts) — all seven quotes count=1.
3. `python3 battery.py > battery.out` — exit 0; output matches the table above; `sha256sum` — hashes above.
4. `grep -c/-o srcset` over round-23 live snapshots — zero occurrences; grep exit 2 = missing page.html in 4 dirs, expected.

An earlier battery run had a port bug (comma jump returned to the tokenizer instead of the
splitting loop; S1/S2/S6/S9 returned []); the corrected run above matches hand traces for all 10 inputs.

## Residual risk and verification gaps

- No browser differential run; "browsers do this" rests on the spec algorithm being the normative
  parsing rule, not an observed browser. [INFERENCE for browser behavior; algorithm text is quoted
  evidence.] Port is mine, not web-platform-tests (WPT not fetched).
- Descriptor port covers w/x/h integer/float shapes; exotic float forms are outside the battery. The
  4 round-23 dirs without page.html were not investigated (another seat's scope).
