# CriticC1Parse

CASES:
- Method: shared scratch clone of the lane, isolated worktrees committed with `selftest` identity; counter run as `python3 -B .../c59_axis_evidence.py --root <worktree> --revision HEAD` against frozen base `fd6303ce5c14b3f892dec586297a942ab6e4193b`. A constructed compliant control returned `mismatches=0`, `rows=3`, `scores_held=2`, `superseded_kept=3`, `met=True`.
- Escaped `\|` late in the evidence cell: `met=True`; the parser nevertheless splits at the escaped pipe, but the receipt/tally remain in its chosen third cell. Verdict is correct for this placement. Escaped `\|` before the receipt: `rows_no_receipt=1`, `rows_no_tally=1`, `met=False`. In GFM the escaped pipe is cell content, so this is a **false red** for a valid equivalent table.
- Code span containing raw `|`: `met=False`; the pipe splits the row, and the resulting backticked `21/21` is misread as a path (`unresolved=1`) while the tally is omitted. Under GFM a pipe in a table cell must be escaped, including when in code; this fixture is malformed, so rejection is **correct**, though the parser diagnostics expose the split/path confusion.
- Header `| Axis | Score | Evidence | Last change |`: no exact header recognized (`rows=0`), `met=False`. This fails the literal frozen header contract; a semantically equivalent header variant would be a **false red** if header wording is intended to be flexible.
- Two exact-header tables, broken/base first and compliant second: parser measures only the first, reports the base's 16 mismatches and `met=False`. Inverse fixture (compliant first, stale/base duplicate second) reports `met=True`, including `superseded_kept=3`: **false-green risk** when the later table is the intended authority; the counter neither rejects duplicates nor establishes which table is authoritative.
- Three leading spaces: `met=True` (valid Markdown table; **correct**). Four leading spaces on header, separator, and rows: `met=True`, all predicate counts satisfied. Four-space-indented Markdown is a code block, not a table: **false green**.
- Trailing spaces after row pipes: `met=True` (**correct**; whitespace is trimmed).
- HTML comment wrapping the middle row: parser stops at the comment, `rows=1`, `met=False` (**correct**; the comment interrupts the Markdown table).
- Row split across physical lines: parser sees only two rows, `met=False` (**correct**; Markdown table rows do not continue across lines).
- Compliant table moved below the round sections, with base cells retained outside its span: `met=True` (**correct**). Table position alone does not defeat parsing or receipt attribution.
- A fenced-code fixture was attempted but constructed with the closing fence inserted before the third row; it returned `rows=2`/`met=False` and is not evidence about a correctly fenced table.

FALSE GREENS:
- Reproducible four-space-indented code-block fixture: `axis_table()` uses `.strip()` for the header and rows, erasing indentation before recognition. A document with no rendered axis table can satisfy the whole predicate. Reject headers/rows in fenced or indented code, preferably by parsing Markdown tables rather than line-prefix heuristics.
- Duplicate-table authority: first-match parsing can report green while a later duplicate retains the stale table. At minimum, require exactly one eligible axis table; a reviewer must still define whether archived copies are permissible and how they are marked.

FIXES:
- Use a small Markdown-aware table parser or implement its relevant rules: ignore fenced/indented code, split only unescaped pipes, and recognize cell-equivalent header spacing. Require exactly one eligible axis table rather than silently selecting the first. Keep the frozen required column semantics and the three ordered axis rows.
- Escaped-pipe-before-pointer fixture is false red: the current raw `.split("|")` shifts the evidence column and loses its receipt/tally. The code-span fixture is malformed but shows that splitting before inline-token extraction can also reinterpret a tally as a path.
- No change is needed for ordinary leading/trailing whitespace, an HTML comment that actually interrupts a table, physical-line row breaks, or moving the table below round sections; observed results align with the corresponding Markdown structure/contract.

VERDICT: Parsing has a confirmed false-green for four-space-indented code and a first-match duplicate-table authority hole, plus a confirmed false-red for valid escaped-pipe evidence. Make parsing Markdown-aware and reject ambiguous duplicate tables before relying on C1's green result.