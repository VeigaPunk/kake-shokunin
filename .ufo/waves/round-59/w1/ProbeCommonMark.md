# ProbeCommonMark

Round-59 w1 probe: do the K8 and K9 fixture shapes of `.ufo/waves/round-59/c59_resolver_cases.py`
render as the counter assumes? Answered by rendering the counter's *exact* fixture bytes with four
independent CommonMark/GFM renderers, plus running the base tool on the same bytes.

## TOOL

| tool | version | channel | reason |
| --- | --- | --- | --- |
| markdown-it-py | 4.2.0 | `uv tool install markdown-it-py` (PyPI, official) | CommonMark+GFM renderer; preset `gfm-like`, table rule on, linkify off (no `linkify-it-py`) |
| cmarkgfm | 2025.10.22 | `uv run --with cmarkgfm` (PyPI, official; wraps cmark-gfm) | the GFM reference implementation — GitHub's own renderer |
| commonmark.js | 0.31.2 | `npx -y commonmark` (npm, official) | CommonMark reference impl; **no GFM table extension in this CLI**, so its table output is a paragraph — used only for the setext/`<h2>` and HTML-block questions, which are core CommonMark |
| marked | 18.1.2 | `npx -y marked` (npm, official) | third independent GFM renderer (cross-check) |

Install record: `uv tool install markdown-it-py` ran with `UV_TOOL_BIN_DIR` pointed at this seat's
scratch, so the executable landed in scratch and **no PATH directory was created or modified** —
`~/.local/bin/markdown-it` is a pre-existing symlink (mtime 2026-10-23 22:58) left untouched. `npx`
packages live in `~/.npm/_npx`; `uv run --with` uses an ephemeral env. **No pacman was run** (host-wide
pacman pause); no host service was restarted.

Fixture bytes were materialized by importing the counter itself and calling its own `registry()` /
`row()` / `HDR()` / `lane()` helpers, so the inputs are byte-identical to what K8/K9 write to
`corpus/SOURCES.md` (saved to `ProbeCommonMark.files/fixture-*.md`; rendered outputs in
`ProbeCommonMark.files/renders.txt`).

## RENDERS

### (a) K8 — GFM table, then a `<!--` / row / `-->` block

Input (`fixture-k8.md`, exact counter bytes; `S200` is the counter's `d8`): a `## Registry` table with
header/delimiter/`S100` row, then `<!--`, a `| S200 | … |` row, then `-->`.

| renderer | `<td>S200</td>`? | what the comment becomes |
| --- | --- | --- |
| markdown-it-py (gfm-like) | **no** | raw HTML block, emitted verbatim |
| cmark-gfm (default) | **no** | `<!-- raw HTML omitted -->` |
| cmark-gfm (`CMARK_OPT_UNSAFE`) | **no** | raw HTML block, emitted verbatim |
| marked | **no** | raw HTML block, emitted verbatim |
| commonmark.js | n/a (no table ext.) | raw HTML block, emitted verbatim |

The commented row is **invisible as content in every renderer**: no renderer puts `S200` in a table
cell; the table closes at `S100` and the comment body becomes inert raw HTML. cmark-gfm's default
(GitHub-like) mode drops it entirely; the other three keep the bytes only as an HTML comment, which
a browser never renders. A blank line before `<!--` (shape `a2`) changes nothing.

### (b) K9 — table, blank line, `Subsection` + `---`, blank line, a pipe row

Input (`fixture-k9.md`, exact counter bytes; `S300` is the counter's `d9`): the same table, then a
blank line, `Subsection`, `---`, a blank line, then a `| S300 | … |` row.

| renderer | `Subsection` + `---` becomes | `S300` in a `<td>`? |
| --- | --- | --- |
| markdown-it-py (gfm-like) | **`<h2>Subsection</h2>`** | no — `<p>| S300 | … |</p>` (paragraph, not table) |
| cmark-gfm | **`<h2>Subsection</h2>`** | no — `<p>| S300 | … |</p>` |
| marked | **`<h2>Subsection</h2>`** | no — `<p>| S300 | … |</p>` |
| commonmark.js | **`<h2>Subsection</h2>`** | no — `<p>| S300 | … |</p>` |

**(b) does yield an `<h2>`** in all four renderers, and it is a *level-2* heading (same level as
`## Registry`). Two consequences the counter relies on: (1) the `## Registry` section ends at
`<h2>Subsection</h2>`, so the `S300` row is no longer inside the Registry section; (2)
independently, a lone pipe row with no header/delimiter row is **not a table row at all** — it is a
paragraph, rendered `<p>| S300 | … |</p>`, never a `<td>`. Both point the same way: `S300` must not
register.

### (c) — the same with `---` after a blank line (thematic break)

Input (`fixture-c.md`): table, blank, `Subsection`, blank, `---`, blank, pipe row.

| renderer | result |
| --- | --- |
| markdown-it-py | `<p>Subsection</p>` then `<hr />` — **no heading at all** |
| cmark-gfm | `<p>Subsection</p>` then `<hr />` — **no heading** |
| marked | `<p>Subsection</p>` then `<hr />` — **no heading** |
| commonmark.js | `<p>Subsection</p>` then `<hr />` — **no heading** |

`---` preceded by a blank line is a thematic break, not a setext underline. A setext heading requires
the `---` to directly follow a **non-blank paragraph line**. So the K9-vs-(c) discriminator is the
blank line *before* `---`, not the one after it.

### (d) — a pipe row immediately after the table, no blank line

Input (`fixture-d.md`): header/delimiter/`S100` row, then the `S400` row immediately.

| renderer | result |
| --- | --- |
| markdown-it-py (gfm-like) | **the `S400` row is absorbed into the same table** — second `<tr>` in the same `<tbody>` |
| cmark-gfm | **same** — `S400` is a second `<tr>` of the same `<table>` |
| marked | **same** — `S400` is a second `<tr>` of the same `<table>` |
| commonmark.js | n/a (no table extension) — one paragraph |

**(d) extends the table.** A GFM table is not terminated by the absence of a blank line; rows keep
being absorbed until a blank line or a line that cannot be a row. This is the sharpest edge in the
K8 fixture: there the `<!--` follows the `S100` row with **no** blank line, so the comment
*interrupts* the table rather than continuing it — all four renderers close the table at `S100`.

## READING

The counter's K8 and K9 shapes render **as the counter assumes**, in all four renderers:

- **K8 (commented row).** The row inside `<!-- … -->` is invisible as content — no renderer emits it
  as a table cell; cmark-gfm (GitHub's own renderer) omits it completely. So "a registry row inside a
  multi-line HTML comment resolves an id markdown does not show" is literally true: the id is in the
  markdown source but not in what markdown shows. The K8 expectation (exit 1, `DANGLING <d8>`, good
  id `R` still resolving) is render-grounded.
- **K9 (setext H2).** `Subsection` + `---` is a genuine level-2 heading in every renderer, so it
  closes the `## Registry` section exactly as the tool's own section rule requires ("the section ends
  at the next `# ` or `## ` heading"). Independently the `S300` row renders as a paragraph, never as a
  table row. Both readings agree `S300` must not register. The K9 expectation (exit 1,
  `DANGLING <d9>`, `R` still resolving) is render-grounded.

Two implementation cautions the renders establish, for whoever writes the fix:

1. **Do not fix K8 by stripping `<!--` / `-->` markers.** A marker-strip makes `S200` a real table
   row (verified: `<td>S200</td>` appears in markdown-it-py *and* cmark-gfm once the markers are
   removed) — the opposite of the required outcome. The comment must be treated as an *opaque HTML
   block* whose body is skipped.
2. **The K9 discriminator is the blank line before `---`, not after it.** A `---` after a blank line is
   a thematic break (no heading, section does not end); a `---` directly after a non-blank paragraph
   line is a setext H2 (section ends). A fix keyed on "any `---` line ends the section" would break
   shape (c) and would also mis-handle `---` as a table delimiter row. Note `===` likewise yields a
   level-1 `<h1>` (verified), and `---`/`===` **immediately after a table row** (no blank line) is a
   thematic break, not a setext heading — a table row is not a paragraph.

Behavioral confirmation against the **base** tool (`fd6303ce…:scripts/id_resolver.py`; identical to
HEAD's `scripts/id_resolver.py` — `git diff` against base is empty), run on these exact fixture bytes:

| fixture | base tool output | matches base control receipt? |
| --- | --- | --- |
| k8 | `exit=0  ids_cited=2 ids_resolved=2 dangling=0` | yes — `K8_html_comment_row_is_not_registered FAIL  exit=0 ids_cited=2 ids_resolved=2 dangling=0` |
| k9 | `exit=0  ids_cited=2 ids_resolved=2 dangling=0` | yes — `K9_setext_heading_ends_registry FAIL  exit=0 ids_cited=2 ids_resolved=2 dangling=0` |
| c | `exit=0  ids_cited=2 ids_resolved=2 dangling=0` | (control shape) |
| d | correct citation `S100,S400`: `exit=0 ids_cited=2 ids_resolved=2 dangling=0` | base tool resolves `S400` |

So the base tool registers `S200` (commented row) and `S300` (post-setext row) — the two false greens
K8/K9 target — and the render evidence says neither *should* be registered. The counter's
expectations are correct; the tool is what is wrong.

Additional render facts beyond the assigned four shapes:

- **Inline `<!--` inside a table cell** (`| S900 | cell <!-- inline | comment --> tail |`) is
  *inline* HTML, not an HTML block: the row stays a table row in markdown-it-py, cmark-gfm and
  marked. A fix treating any `<!--` on a line as opening an HTML block would wrongly drop that row.
- **A row after a closed comment block** (`<!-- … -->` then a pipe row, no blank line) is *not* a
  table row in any GFM renderer (the comment interrupts the table; the following row becomes a
  paragraph) — verified in markdown-it-py and cmark-gfm.
- **The real lane registry is unaffected by either shape.** `corpus/SOURCES.md` (277 lines) contains
  **zero** `---` lines, **zero** `===` lines and **zero** `<!--`/`-->` occurrences; its headings are
  `# SOURCES…` (l.1), `## Registry` (l.5), `## Paths` (l.172), `## Search log` (l.187),
  `## Leads (unopened)` (l.226). A K8/K9 fix that changes parsing cannot regress P7
  (`ids_cited=108 ids_resolved=108 dangling=0` on the real lane) through these shapes.

## VERDICT

CONFIRMED — the counter's K8/K9 expectations are render-grounded, with two fix caveats: skip the
comment body as an opaque HTML block (never strip its markers), and key the setext rule on the blank
line *before* the `---`.

Files: `.ufo/waves/round-59/w1/ProbeCommonMark.md` (this file) and
`.ufo/waves/round-59/w1/ProbeCommonMark.files/` (`renders.txt`, `fixture-{k8,k9,c,d}.md`).

VERDICT: CONFIRMED — the K8 and K9 fixture shapes render exactly as the counter assumes in four independent CommonMark/GFM renderers (the commented row is invisible as content; `Subsection`+`---` is a real `<h2>` that ends the Registry section), with the caveats that a fix must skip the comment body rather than strip its markers and must key the setext rule on the blank line *before* the `---`.