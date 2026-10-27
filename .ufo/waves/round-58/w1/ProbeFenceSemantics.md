# ProbeFenceSemantics

Round-58 kake wave w1. Lane files touched: none (report only). Fixtures, scripts and parser runs
lived under `/fast/scratch/hyaku/kake-r58/ProbeFenceSemantics/` (deleted at end; every retained
line of evidence is in this report). No lane jj/git mutation, no pacman, no host service.

## INPUTS:

Eight registry-shaped inputs `inputs/inNN_*.md`. Each carries at least one real GFM table (header
+ delimiter row) so an "outside the fence" row can be identified as a table row, not merely as a
non-code paragraph. Markers S401..S473 are unique; every registry row is `| S### | word | word |`.

- in01_plain_backtick.md (9 L): table row S402; blank; 3-backtick fence + info "text"; S401;
  3-backtick close; blank; "Outro paragraph."
- in02_tilde.md (7 L): 3-tilde fence; S411; 3-tilde close; blank; table row S412.
- in03_indent3.md (7 L): fence opened with **3 leading spaces**; S421; 3-space closer; blank; table
  row S422.
- in04_indent4.md (9 L): table row S430; blank; **4-space-indented** "```text"; S431; bare
  3-backtick line at column 0; blank; S432.
- in05_mismatch.md (8 L): table row S440; blank; 3-backtick fence + "text"; S441; a 3-tilde line
  (wrong char); S442; EOF.
- in06_close_length.md (19 L): S450 row; blank; 4-backtick opener, 3-backtick line inside, S451,
  S452, 4-backtick closer; blank; 3-backtick opener, S453, **5-backtick** closer, S454; blank;
  3-backtick opener, S455, closer = 3 backticks + **3 trailing spaces**, S456.
- in07_infobt.md (15 L): S460 row; blank; opener candidate "```js`x" (**backtick in info string**),
  S461, 3 backticks, S462, 3 backticks; blank; fence + "text", S463, closer candidate
  "``` trailing words", S464, 3 backticks.
- in08_containers.md (15 L): S470 row; blank; fence in blockquote (`> ``` + 3 backticks), S471,
  `> ``` ` ; blank; list item "- item", blank, fence at the item's **content column (2 raw
  spaces)** + info, S472; blank; S473 at column 0.

## PARSER OUTPUT:

Two independent implementations over the raw files: `cmark 0.31.2` (reference C parser,
CommonMark spec 0.31.2; per-marker element ancestry read from emitted HTML) and
`markdown-it-py 4.2.0` token stream, presets `commonmark` and `gfm-like` (linkify disabled —
linkify-it-py absent; table rule active, proven by `table_open > tbody_open > tr_open` chains).
They agree on **28/28** markers across all three configurations.

Fence extents from token maps (1-based source lines; identical in all three):
in01 5-7 · in02 1-3 · in03 1-3 · in04 **only 7-9** · in05 5-8 (EOF, unclosed) ·
in06 5-9, 11-13, 16-18 · in07 7-9, 11-15 · in08 5-7 (blockquote), 11-13 (list item).

Per marker — "inside" = cmark `pre > code` + markdown-it `fence`; outside rows show the
markdown-it gfm chain:

- in01: S401 inside (L6) · S402 `table_open > tbody_open > tr_open` (L3)
- in02: S411 inside (L2) · S412 table row (L7)
- in03: S421 inside (L2) · S422 table row (L7)
- in04: S430 table row (L3) · S431 **paragraph, outside code** (L6) · S432 **inside** (L9)
- in05: S440 table row (L3) · S441 inside (L6) · S442 inside (L8; tilde line did not close)
- in06: S450 table row (L3) · S451 inside (L6) · S452 inside (L8; 3 backticks did not close a
  4-backtick opener) · S453 inside (L12) · S454 paragraph, outside (L14; 5-backtick closer did
  close) · S455 inside (L17) · S456 paragraph, outside (L19; closer + trailing spaces did close)
- in07: S460 table row (L3) · S461 **paragraph, outside** (L6; backtick info → no fence) ·
  S462 inside (L8) · S463 inside (L12) · S464 **inside** (L14; closer + trailing text did not close)
- in08: S470 table row (L3) · S471 inside `blockquote > pre > code` (L6) · S472 inside
  `ul > li > pre > code` (L12) · S473 paragraph, outside (L15)

Totals: 15 markers inside code; 13 outside — 8 of those are true GFM table rows, 5 are
paragraphs (a lone `| S### |` line with no header+delimiter above is not a table row).

Raw cmark HTML for the two decisive inputs (verbatim; the wrap is presentational):

    in04: <p>| id | state | src |
          | -- | ----- | --- |
          | S430 | alpha | live |</p>
          <pre><code>```text
          </code></pre>
          <p>| S431 | beta | staged |</p>
          <pre><code>
          | S432 | alpha | live |
          </code></pre>

    in07: <p>```js`x
          | S461 | beta | staged |</p>
          <pre><code>| S462 | alpha | live |
          </code></pre>
          <pre><code class="language-text">| S463 | beta | staged |
          ``` trailing words
          | S464 | alpha | live |
          </code></pre>

Spec text consulted (spec.commonmark.org/0.31.2, fetched this run, §4.5): opening fence
"preceded by up to three spaces of indentation" (line 2262); "If the info string comes after a
backtick fence, it may not contain any backtick characters" (2266-2268); "The closing code fence
… may be followed only by spaces or tabs" (2281-2282); "must use the same character as the
opening fence" (2347); "must be at least as long as the opening fence" (2380).

## HYPOTHESIS:

**Falsified** as an exact characterization: two clauses are necessary-condition only and one
phrase is container-relative. What survives is that for the fenced regions probed, the account
predicts all 15 inside-code markers correctly, and each structural claim below reproduced
identically in both parsers.

1. **Opening clause insufficient (in07 L5-6).** "```js`x" is at column 0 with three backticks —
   it satisfies "0-3 spaces, >= 3 backticks" — yet it does not open a fence: a backtick fence's
   info string may not contain backticks. S461 is parsed as a paragraph, outside code. A second
   necessary condition (info-string restriction) is missing from the hypothesis.
2. **Closing clause insufficient (in07 L13-14).** "``` trailing words" uses the same character
   and the same length as the opening fence, yet does not close: S464 stays inside code. Closing
   requires nothing but spaces/tabs after the marker. Control (in06 L18: closer + 3 trailing
   spaces) does close (S456 outside), isolating "only spaces/tabs" as the discriminator, not
   trailing whitespace in general. So "same char + >= opening length" is necessary, not
   sufficient.
3. **Indent is container-relative, not raw columns.** in08 L11 is indented two raw columns and is
   still a fence (extent 11-13, S472 inside `ul > li > pre > code`) because indentation is
   measured after container prefixes are stripped; the blockquote fence at L5 fences S471. A
   literal reading of "0-3 spaces" against the physical line misclassifies both.

Confirmed sub-claims (identical in cmark and both markdown-it presets):

- **4 spaces is not a fence** (in04): the "    ```text" line becomes an indented code block
  holding only itself (extents 7-9, not 5-9), so S431 escapes into a paragraph; the bare
  3-backtick line at column 0 then opens a fence that swallows S432 to EOF. Operational hazard:
  a mis-indented marker does not merely fail to open — it releases its row as a non-table
  paragraph, and the next column-0 marker can silently silence every later row to end of file.
- 3-space-indented opening fence works (in03: 1-3, S421 inside).
- Tilde fences work and cannot be closed by backticks nor vice versa (in02; in05: the tilde line
  neither closes nor opens inside the open backtick fence, so S441 and S442 are both code and the
  fence runs to EOF).
- Closer shorter than opener does not close (in06 L7: S452 inside); closer longer than opener
  does close (in06 L13, five backticks: S454 outside).
- "Outside code" ≠ "table row": 5 of 13 outside markers render as paragraphs (S431, S454, S456,
  S461, S473), so a registry checker keyed on GFM row tokens must not equate the two.

Residual limit: 8 inputs / 28 markers / two implementations (one the reference C parser), all
CommonMark + GFM tables. GitHub's own renderer was not exercised; only what GFM table tokens
imply [INFERENCE].

## INSTALLS:

- `markdown-it-py 4.2.0` (+ `mdurl 0.1.2`) via uv: `uv tool install markdown-it-py` — reason: an
  independent second parser whose tokens expose fence `map`/`markup`/`info`. The console-script
  link was refused ("Executable already exists: markdown-it": a dangling symlink
  `~/.local/bin/markdown-it -> ~/.local/share/uv/tools/markdown-it-py/bin/markdown-it` dated
  Oct 23, stale residue with no backing tool dir), so runs used
  `uv run --with markdown-it-py python fence_probe.py`; `import markdown_it` reports 4.2.0. No
  `--force`, no PATH directory written.
- `cmark 0.31.2` already at `/usr/bin/cmark` — nothing installed (pacman paused host-wide).
  `linkify-it-py` absent, not installed; gfm-like preset created with `.disable("linkify")`, which
  leaves table and fence rules intact (verified by the table token chains).
- Nothing else installed; no host service started or restarted.

VERDICT: Falsified as stated — the parser account needs two extra necessary conditions (no backtick in a backtick-fence info string; closer followed only by spaces/tabs) plus container-relative indentation; the 4-space, length and character cases behave exactly as the hypothesis predicts, in cmark 0.31.2 and markdown-it-py 4.2.0 alike.
