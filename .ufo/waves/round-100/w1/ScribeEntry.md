# ScribeEntry — round-100 C2 knowledge entry (contract v2)

Scope: draft the full replacement of `corpus/knowledge/freshening-304.md` for
the round-100 C2 capability, with the `## Contract v2 (round 100)` section the
assignment names. Read-only with respect to the lane's tracked files: the
draft, three checkers and five receipts live under
`.ufo/waves/round-100/w1/ScribeEntry/`, and this report is at
`.ufo/waves/round-100/w1/ScribeEntry.md`. No product code, contract, counter,
registry or instrument was edited, and no git or jj command was run against
the lane or the fleet repo other than read-only ones.

## Behavior delivered

**The entry**, drafted at `.ufo/waves/round-100/w1/ScribeEntry/freshening-304.md`
(35 845 bytes, 610 lines), the full replacement of the round-99 entry.

The round-99 entry was read first (committed at
`corpus/knowledge/freshening-304.md`, sha256
`a03f5867992aa82eeb62cbd069f9eb6b4a640f1dc3d713f7358d929a841e8f6f`) and every
still-true v1 statement and its citation was carried over:

- the four front-matter lines, with the trio changed as the assignment
  specifies: `source:` now names `S484, S485, S486, S487`; `verified-at:` is
  `2026-11-06`; `recheck:` is `180d (due 2027-05-05), or sooner after a change
  to the retained RFC bodies or to contract v2 of this lane`. `ground:` and
  `scope:` are kept, with `scope:` extended by the §3.4 and §4.1 items
  contract v2 added to its not-covered list.
- the whole of "What RFC 9111 §4.3.4 says about the initial set", "The three
  first-match rules", "What RFC 9111 §3.2 says about updating stored header
  fields" and "The §3.1 exceptions §3.2 points at", quote for quote and line
  for line (Q1-Q26 unchanged).
- the lane conventions LC1-LC6, each still marked a lane convention and not an
  RFC requirement. LC6 is kept as the convention contract v2 replaces, and the
  v1 reading difference about case-sensitive matching is preserved inside the
  LC6 bullet, with the note that contract v2 closes it by stating the
  comparison explicitly.
- the decision table, the quote table (Q1-Q26 verbatim, now with a `Row`
  column), "What this entry cites", the EID 9185 erratum section with its four
  erratum quotations, and "What this entry does not decide".
- the v1 statements that contract v2 supersedes are kept as history and
  marked: the byte-for-byte value copy is named as what the v2 trimming
  clause replaces; the v1 counter is named as the counter that scores the
  earlier contract and is expected to disagree with a v2 candidate on the
  qualified-form and trimming clauses.

**The new section**, `## Contract v2 (round 100)` (201 lines), with five
subsections:

1. *The Cache-Control of the 304 (the replacement for LC6)* — the
   case-insensitive field-name comparison, the RFC 9111 §5.2 list parse with
   the grammar and the two argument forms, the RFC 9110 §5.6.1.2 list syntax
   with empty elements, the token and quoted-string argument forms, the two
   qualified forms, and the §5.2.3 rule for unrecognised directives. It ends
   in a five-row decision table: qualified `no-cache`/`private` with an
   argument in either form and any case → refused `invalid_input: qualified
   cache-control outside contract`; unqualified → ignored; an unrecognised
   extension whose name merely contains or ends in `no-cache`/`private`
   (`x-no-cache="a"`, `no-cachex=1`) → ignored; an unparseable list → refused
   `invalid_input: malformed cache-control`; the stored response's own
   Cache-Control → copied as data. The refusal of an unparseable list is named
   **LC8** and marked a lane convention: the lane refuses because a list it
   cannot parse cannot be checked for the qualified forms, and RFC 9111 does
   not require the refusal.
2. *Output values are field values without surrounding whitespace* — RFC 9110
   §5.5, the trimming of every output value, inner whitespace kept byte for
   byte, and the unchanged ETag/Last-Modified comparison.
3. *No proxy-specific field in an updated response* — the three names, the
   stored-side drop that v2 adds, and the §3.1 exception 4 rule they rest on.
4. *The seven escape classes* — a decision table with one row per class e1
   to e7, each a decision rather than a description of a tool.
5. *What contract v2 closes, and what stays open* — F1, F2, F3 and F10 as
   closed, each with the clause that closes it; F4, F5, F6, F7, F8, F9 and F11
   as still open, each with its substance.

## Quotes

44 quotes, each at most 25 words, each located by plain-text line number in a
retained body:

| Body | Quotes | Row | Lines |
|---|---|---|---|
| `rfc9111.txt` (`.ufo/waves/round-99/sources/rfc9111.txt`, sha256 `aeb52adb…`) | Q1-Q26 | S484 | 340, 345, 350, 354, 358, 361, 375, 377, 379, 381, 384, 387, 393, 412, 935, 953, 957, 962, 965, 967, 970, 974, 976, 979, 982, 986 |
| `rfc9111.txt` | Q27-Q35 | S486 | 1098, 1099, 1101, 1106, 1273, 1286, 1334, 1344, 1411 |
| `rfc9111.txt` | Q23 (shared with S484) | S484, S486 | 358 |
| `rfc9110.txt` (`.ufo/waves/round-100/sources/rfc9110.txt`, sha256 `21c1cdce…`) | Q36-Q44 | S487 | 1591, 1593, 1695, 1702, 1730, 1733, 1783, 1786, 1794 |

The citation counts in the verdict line are the number of quote rows each row
carries: S486 carries nine of its own (Q27-Q35) plus Q23, which it shares with
S484, for ten; S487 carries nine (Q36-Q44); S484 carries 26 (Q1-Q26, one of
which is the shared Q23).

Six of the quoted strings occur on more than one line of their body, because
the RFCs print the same production twice — the `cache-directive` production at
RFC 9111 lines 1106 and 1783, the quoted-string-form sentence at RFC 9111 lines
1286 and 1344, and the `token`, `quoted-string` and `quoted-pair` productions at
RFC 9110 lines 1733, 1786 and 1794 and again in the ABNF appendix at lines
9963, 9940 and 9939. The quote checker records every occurrence and accepts the
declared line when it is one of them, so each row's line stays checkable.

The four erratum quotations are checked against
`.ufo/waves/round-99/sources/eid9185.html` (sha256 `83c3b795…`) and recorded
in `erratum-wording-check.txt`.

## Gates run

| Command | rc | Observed |
|---|---|---|
| `python3 -B .ufo/waves/round-100/w1/ScribeEntry/quotecheck.py` | 0 | `table_rows=44 blockquotes=48 notfound=0 linemismatch=0 over25=0 blockquote_notfound=0` |
| `python3 -B .ufo/waves/round-100/w1/ScribeEntry/erratumcheck.py` | 0 | `erratum_quotes=4 notfound=0 over25=0`, `erratum_blockquotes_present=5` |
| `python3 -B scripts/knowledge_metatext_lint.py --dir .ufo/waves/round-100/w1/ScribeEntry` | 0 | `files=1 gate_findings=0 review_hits=0` |
| `python3 -B .ufo/waves/round-100/w1/ScribeEntry/entry_selfcheck.py` | 0 | `quote_rows=44`, `citations S484=26 S486=10 S487=9`, `failures=0` |

`knowledge_metatext_lint.py` accepts a path: it takes `--dir <directory>` and
scans the `*.md` files in it, or `--root`/`--revision` for a committed
revision. The `--dir` form was used on the seat directory, so the gate saw the
draft itself. It reported zero gate findings and zero review hits, so no
seat-tree path, seat name or drafting phrase survives in the draft. The lint
was also run over the committed corpus at the lane tip
(`--root . --revision HEAD`, rc 0) to see the baseline; that run prints
review hits from other entries, not from this draft.

The quote check reads the draft's own quote table and its own body block
quotations, so it is bound to the artifact rather than to a hand-kept list:
every table row is searched for in the collapsed body, its observed start
line is compared with the declared line, its word count is recomputed, and
every `> ` line in the body is required to be a substring of one of the three
retained bodies.

## Digests verified before and after

All 21 frozen digests in
`.ufo/waves/round-100/controls/instrument-sha256.txt` were re-derived with
`sha256sum` over the working tree and matched (0 mismatches, 0 missing). The
three bodies this entry quotes from were re-derived independently:

| File | sha256 | bytes | lines |
|---|---|---|---|
| `.ufo/waves/round-99/sources/rfc9111.txt` | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 84 477 | 1 956 |
| `.ufo/waves/round-100/sources/rfc9110.txt` | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 502 941 | 10 785 |
| `.ufo/waves/round-99/sources/eid9185.html` | `83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3` | 10 655 | — |

The two digests the entry names for the contract and the counter were also
re-derived: contract v2 `343b3a558c5d2fb3059f9f9e1de2d26d0c9d7ff9fb977035f905b0729d09a092`,
counter `e7dff63b93d33254ea278bf34d18ae98fc1462616aedad46e6ff416c6d3f3fed`,
contract v1 `2be46b4d8dcc57539b0a45e2e3b7b57e76cb1c4e570891e8cdea88c5ebbba2a6`,
counter v1 `d13bba5d6b663b171ab57d42b5ec054b5f73d8deb8f9fd64f14adad455b6bc4b`.
The lane tip was `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` at the start of this
seat's work and moved to
`06c81f08f48ef32dada6625ddbfb31301491b8f7` (the C2 content commit) while it
ran. The 21 frozen digests were re-verified at both tips with 0 mismatches, and
the draft's references were re-checked against the moved tip (below).

## Touched surfaces

- `.ufo/waves/round-100/w1/ScribeEntry/freshening-304.md` — the draft entry
- `.ufo/waves/round-100/w1/ScribeEntry/quotecheck.py` — the quote checker
- `.ufo/waves/round-100/w1/ScribeEntry/erratumcheck.py` — the erratum checker
- `.ufo/waves/round-100/w1/ScribeEntry/entry_selfcheck.py` — the entry checker
- `.ufo/waves/round-100/w1/ScribeEntry/quotes-check.txt` and
  `quotes-summary.txt` — the quote receipts
- `.ufo/waves/round-100/w1/ScribeEntry/erratum-wording-check.txt` and
  `erratum-summary.txt` — the erratum receipts
- `.ufo/waves/round-100/w1/ScribeEntry/metatext-lint.txt` — the gate receipt
- `.ufo/waves/round-100/w1/ScribeEntry/entry-selfcheck.txt` — the self-check
  receipt
- `.ufo/waves/round-100/w1/ScribeEntry.md` — this report

Scratch root `/fast/scratch/hyaku/kake-r100/ScribeEntry/` was used for the
check runs and removed afterwards. Nothing outside the seat directory and the
scratch root was written.

## Out of scope, not done

- The entry was **not** integrated into `corpus/knowledge/`. That is the L1's
  write; this seat delivers a draft.
- The SOURCES.md rows S486 and S487 were **not** written by this seat. They
  landed in the C2 content commit `06c81f08` while this seat ran, drafted
  elsewhere (`.ufo/waves/round-100/w1/ScoutSources/rows.md`). The entry cites
  both ids, and each of the ten quotes attributed to S486 and the nine
  attributed to S487 falls inside the anchor cell of the landed row: S486's
  §5.2 grammar lines 1098-1102, its `cache-directive` production line 1106,
  its §5.2.2.4 qualified-field-name sentence lines 1273-1279, its §5.2.2.7
  qualified-field-name sentence lines 1334-1339, its §5.2.3 MUST-ignore
  sentence lines 1411-1412 and its §3.1 proxy-fields sentence lines 358-360;
  S487's §5.5 whitespace sentence line 1591, its §5.6.1.2 accept-syntax
  sentence lines 1695-1700 and production line 1702, its §5.6.2 heading line
  1728, and its §5.6.4 productions lines 1786-1787 and quoted-pair production
  line 1794. Two quotes sit inside the anchored row's section scope but below
  its anchor cell's enumerated lines — Q32 at RFC 9111 line 1286 and Q34 at
  line 1344, both the §5.2.2.4 and §5.2.2.7 quoted-string-form sentence — so
  they are attributed to S486 on scope rather than on anchor.
  `scripts/id_resolver.py --root . --revision master` (rc 0) reports six ids
  dangling across the corpus, none of them S486 or S487.
- The C2 candidate was **not** built, scored or measured by this seat. The
  entry states no measurement and claims no conformance. The candidate landed
  in the same C2 content commit; its committed bytes were read once, only to
  confirm that the contract the entry states is the one the candidate
  implements, and nothing in the entry rests on that.
- No claim was made about any live cache, CDN, proxy or browser.
- The seven still-open findings are described, not repaired. They are routed
  by contract v2's own not-covered list and are the L1's to route.

## Limits of this seat's evidence

- The quote check establishes that each quoted string is a whitespace-collapsed
  substring of the retained body at the stated line, and that every body block
  quotation is a substring of one of the three bodies. It does not establish
  that a quoted passage is the whole of a section, nor that the section is the
  RFC's current text. Both bodies were read as retained and were not
  re-fetched; the entry's `verified-at:` reflects that.
- The F-numbers, their severities and their routing are taken from the
  round-99 contract review and the round-100 contract v2's own not-covered
  list. The entry restates their substance; it does not re-adjudicate them.
- Whether the seven escape classes are the only classes the counter can miss
  is the counter owner's question. The entry states what contract v2 binds for
  each class and nothing beyond that.
- The lane's working tree already carried unrelated modifications and
  untracked files when this seat started (`scripts/freshen_304.py` modified,
  `.ufo/waves/round-100/w1/` untracked). Those are other seats' work; this
  seat did not touch them, and the C2 content commit that landed during the
  seat's run has since committed some of them.

## Tools

No tool was installed or upgraded in this seat; no tooling change was needed,
and pacman was not invoked. Python was the stock interpreter.

## Artifacts

- `.ufo/waves/round-100/w1/ScribeEntry/freshening-304.md` — the drafted entry
- `.ufo/waves/round-100/w1/ScribeEntry/quotes-check.txt` — 44-row quote check
- `.ufo/waves/round-100/w1/ScribeEntry/quotes-summary.txt` — its summary
- `.ufo/waves/round-100/w1/ScribeEntry/erratum-wording-check.txt` — 4-row
  erratum wording check
- `.ufo/waves/round-100/w1/ScribeEntry/erratum-summary.txt` — its summary
- `.ufo/waves/round-100/w1/ScribeEntry/metatext-lint.txt` — the gate receipt
- `.ufo/waves/round-100/w1/ScribeEntry/entry-selfcheck.txt` — the self-check
  receipt
- `.ufo/waves/round-100/w1/ScribeEntry/quotecheck.py`,
  `erratumcheck.py`, `entry_selfcheck.py` — the three checkers
- `.ufo/waves/round-100/w1/ScribeEntry.md` — this report

SCRIBE entry=freshening-304.md quotes=44 citations=S486:10,S487:9 lint=0
