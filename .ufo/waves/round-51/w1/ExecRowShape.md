# ExecRowShape — S262/S263 registry row shape under the census parser

Seat: `L1Kake51.ExecRowShape-2` (leaf executor). Scope: parse `corpus/SOURCES.md` with the
census parser's own 0-to-3-leading-space row pattern and report, for S262 and S263, cell count,
literal/escaped pipe presence, `status`, `opened`, `recheck` and `used-by`; then say whether the
two rows parse as eleven cells.

Axes held while working: **A1 parser fidelity** (use the parser's actual regex and cell split, not
a lookalike), **A2 row-cell integrity** (count and pipe audit), **A3 evidence anchoring**
(every claim re-derived from committed bytes at the measured revision). No move was made that
improved one axis by harming another; nothing outside this report was written.

## 1. The census parser pattern (as implemented, not paraphrased)

Two independent implementations agree on the pattern:

- Census grep form, used in round-50 and quoted in the round-51 contract family:
  `^ {0,3}\|[[:space:]]*S[0-9]{3,}`
  (`.ufo/waves/round-50/make_spec_w1.py:108`, `.ufo/waves/round-36/w1/ScoutRecheckDue.md:45`)
- The round-51 C2 counter's own `parse_registry()`, which is the authoritative consumer of these
  two rows (`.ufo/waves/round-51/c51_quote_truth.py:86-103`):

  ```python
  if not re.match(r"^ {0,3}\|", line):
      continue
  cells = [c.strip() for c in line.strip().strip("|").split("|")]
  ```

  It additionally requires the line to sit inside the `## Registry` section (opened at
  `corpus/SOURCES.md:5`, closed at `:155`), at least 2 cells, and `cells[0]` a full match of
  `S[0-9]{3,}`. Last row for a repeated id wins (`rows[cells[0]] = cells`).

Consequence of the split rule that matters here: the parser splits on **every** ASCII `|`; an
escaped `\|` is *not* treated as literal — it would split and produce an extra cell, which is why
the counter's C3 separately flags `"\\|" in cell` and `len(row) != 11`.

## 2. Cell-level findings

Measured at lane tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (`git show <rev>:corpus/SOURCES.md`;
`git status --porcelain corpus/SOURCES.md` is empty, so the worktree row bytes are the tip bytes).
Both rows sit at **0 leading spaces**, so they match under both `^ {0,3}\|` and the stricter `^\|`.

| Row | Line | Cells | Literal `\|` in a cell | Escaped `\\|` in a cell | `status` | `opened` | `recheck` | `used-by` |
|---|---|---|---|---|---|---|---|---|
| S262 | 152 | **11** | no | no | `mined` | `2026-10-24` | `180d` | `corpus/knowledge/canonical-selection.md` |
| S263 | 153 | **11** | no | no | `mined` | `2026-10-24` | `180d` | `corpus/knowledge/crawler-identity.md` |

Cell-by-cell for S262 (indices are the parser's, mapped to header `:7`):

```
[0] S262
[1] Google Search Central — What is URL canonicalization — https://developers.google.com/search/docs/crawling-indexing/canonicalization
[2] docs
[3] A
[4] Google's canonical selection mechanism — the ground the lane's held static preflight explicitly disclaims
[5] § "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC)
[6] a declared canonical is a hint, not a rule; Google chooses the page that is objectively the most
    complete and useful for search users, weighing HTTP/HTTPS, redirects, sitemap presence and
    rel=canonical annotations
[7] mined
[8] 2026-10-24
[9] 180d
[10] corpus/knowledge/canonical-selection.md
```

Cell-by-cell for S263:

```
[0] S263
[1] Google Search Central — Googlebot — https://developers.google.com/search/docs/crawling-indexing/googlebot
[2] docs
[3] A
[4] The identity of Google's crawler on the wire — which user-agent a publisher meets per device class
    and how to tell the subtypes apart
[5] § "Googlebot is the generic name for two types of web crawlers used by Google Search"
    (doc rev. Last updated 2026-02-03 UTC)
[6] Googlebot is a generic name covering Googlebot Smartphone and Googlebot Desktop; the subtype is
    identified from the HTTP user-agent request header, and both obey the same robots product token
[7] mined
[8] 2026-10-24
[9] 180d
[10] corpus/knowledge/crawler-identity.md
```

Header-to-index map used above (`corpus/SOURCES.md:7`):
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`
— 11 columns, matching the 11-cell separator row at `:8`.

`used-by` is a single path in both rows, and the counter's C4 splits on `,` and compares the
resulting list to exactly one entry, so a single path is the only accepted shape:
`['corpus/knowledge/canonical-selection.md']` and `['corpus/knowledge/crawler-identity.md']`.

## 3. Do the two rows parse as eleven cells?

**Yes — both rows parse as exactly eleven cells**, and neither contains a literal or escaped pipe
in any cell. Two independent confirmations:

- Parser re-implementation of `parse_registry` over `git show <tip>:corpus/SOURCES.md`:
  `S262: cells: 11`, `S263: cells: 11`; `pipes|escaped: False False`; fullwidth `｜` / `&#124;` /
  `&vert;` pipe stand-ins: `[]`.
- Character audit: each raw line holds **12** ASCII `|` characters (`sed -n '152,153p' | tr -cd '|' | wc -c` → `24` for the pair), i.e. *n+1* boundary pipes for *n=11* cells, leaving zero
  interior pipes.

Round-trip through the real counter (`python3 -B .ufo/waves/round-51/c51_quote_truth.py --root .
--revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658`):

```
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth pass
  C6_receipt_pins pass
  C7_validate_before_append pass
  C8_append_after_mirror pass
  revision: 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
exit=0
```

`C3_row_shape pass` with an empty notes list is the parser's own attestation of exactly the four
facts asked for: 11 cells, no literal/escaped pipe, `status == 'mined'`, `opened == '2026-10-24'`,
and `recheck` matching `(\d{4}-\d{2}-\d{2}|\d+d|on-release)` (`180d` matches). `C4_used_by pass`
attests the single-entry `used-by`.

## 4. Attacks tried (all negative — the shape holds)

1. **Duplicates / id shadowing.** `rows[cells[0]] = cells` silently overwrites, so a second S262 or
   S263 row elsewhere in the Registry section would let a malformed row be replaced by a well-formed
   one (or vice versa). Counted occurrences at tip: `S262: occurrences=1`, `S263: occurrences=1`.
   No shadowing.
2. **Fenced table copy.** The parser does not fence-skip (unlike `corpus-contract.mjs`'s
   `FENCE_RE`), so a ```` ``` ````-wrapped duplicate row would be counted. Fences inside the
   Registry section (lines 5-154): `0`.
3. **Leading-space headroom.** The ` {0,3}` allowance is dead on this file today: rows matching
   `^ {1,3}\|[[:space:]]*S[0-9]{3,}` → `0`; `^ {0,3}\|...` → `145`; `^\|...` → `145`. The looser
   and stricter patterns select the identical row set, so the allowance neither hides nor admits
   these two rows.
4. **Section containment.** Both rows lie between `## Registry` (`:5`) and `## Paths` (`:155`), so
   they are inside the section the parser scans; a row below `:155` would be invisible.
5. **Freshness of the rows themselves.** At the do-nothing base `007d66e4e8360a5f88d29a93eeedd8066dad4434`
   neither id is present (`git show 007d66e...:corpus/SOURCES.md | grep -nE '^ {0,3}\|[[:space:]]*S26[23][[:space:]]*\|'`
   → no output). At tip both are present, unique, at lines 152/153. The rows are new this round,
   not inherited.
6. **Registry totals as a sanity bound.** Parser-reconstructed `registry rows total: 145`, equal to
   the census grep count `145` — the two implementations agree on the population, so the two rows
   are counted exactly once in the round's accounting.

## 5. What this does not establish

- It does **not** verify the retained bodies, receipts, `sha256` pins, receipt-URL equality, the
  pre-append mirror lineage, or that the Gate quotes are raw substrings of what Google actually
  served (C5-C8). Those are other seats' surfaces; C3 is a row-shape claim only.
- I did not fetch `developers.google.com` for either URL — the `opened 2026-10-24` and the doc-rev
  strings are read as written in the row, not re-grounded by me.
- `c51_wave_ledger.py` (C1) was not run by me: the wave evidence it derives does not exist until
  the wave settles, and authoring it is L1's step, not this seat's.

## 6. Files written

- `.ufo/waves/round-51/w1/ExecRowShape.md` (this file) — the only write.

No commits, no staging, no `jj`/`git` mutation. Scratch under `/tmp` only (`/tmp/rows.txt`).
No tools installed or upgraded (nothing was needed), so there is no install record to make.
