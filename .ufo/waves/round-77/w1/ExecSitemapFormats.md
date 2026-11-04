# ExecSitemapFormats — round 77, wave w1 (claim C2)

Seat: executor (leaf). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base revision (contract): `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`.
Lane HEAD while the wave ran: `bc2e5fb91e23c8acdac2470ac0f042c76f75417e` (contract commit).
My two files are modified but **uncommitted**; only the L1 writes lane history.
Contract, amendment 1 A1–A10 (amendment 2 is C1-only) and the review findings were read before the final
pass; every receipt below measures the final bytes in §1.

## 1. Files changed and their hashes

| file | lines | sha256 |
|---|---|---|
| `scripts/sitemap_audit.py` | 901 | `f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176` |
| `scripts/sitemap_audit_selftest.py` | 1589 | `f22e0a67d777ce80ce2d1099520f50f98016c28901e77b7cb5e4b73c386b9c89` |

`git status --porcelain -- scripts/` (read-only):

```
 M scripts/sitemap_audit.py
 M scripts/sitemap_audit_selftest.py
```

No other file in the checkout was written by this seat.

## 2. Behaviour landed

- **G2 container.** `_load_payload` (`scripts/sitemap_audit.py:461-487`) reads the first two bytes; `1f 8b`
  means gzip and nothing else (`:476`). The file name is never consulted
  (`r77_gzip_magic_reads_body` = gzip body named `.txt`; `r77_gzip_name_plain_body` = XML body named
  `.xml.gz`; `r77_text_suffix_no_inference` = text body named `.xml`).
- **G1 / A1 / A5 size limit.** A gzip member is streamed through `gzip.GzipFile` keeping only
  `stream.read(MAX_BYTES + 1)` (`:479`); when under the cap one more byte is read to force EOF/CRC/ISIZE
  verification. `len(data) > MAX_BYTES` emits the round-39 `too_large` (`:503-506`) for **every** family —
  gzip body, plain text and feed body (A1's lane reading; the module docstring says so). One byte over the
  limit is `too_large` (`r77_gzip_decompressed_too_large`, `r77_text_too_large`); exactly 52,428,800
  decompressed bytes is clean (`r77_gzip_exact_limit_clean`).
- **G2 / A6 corrupt container.** Truncated members, bad magic bodies, CRC/length failures and trailing
  garbage map to the check error `gzip_invalid`, hence exit 2 (`:482-483`), never to a finding.
- **T1 plain text.** `_audit_text` (`:652-670`) splits on `\n`, strips `XML_WS` per line, ignores blank
  lines, strips one leading BOM (`:511-512`), and limits to 50,000 non-blank lines. Findings:
  `text_empty` (`:666-667`), `text_too_many_entries` (`:668-669`), `text_line_not_url` (comment/prose),
  `text_url_not_absolute` (path-, network-path- or scheme-prefixed reference, `:661-665`); text entries
  carry the 1-based line number as `entry` (A10). A document is XML only when, after a leading BOM and
  XML whitespace, its first byte is `<` — except that a NUL in the opening bytes routes to the XML path so
  round-39's UTF-16-without-BOM `xml_malformed` stays unchanged (`:490-495`).
- **F1 RSS 2.0.** `_audit_rss` (`:673-708`): root `rss`, unqualified (A7); items under `channel`; URL is the
  first non-empty `<item><link>` text; absent/empty → `feed_item_missing_link` (`:702-703`); non-absolute →
  `loc_not_absolute` (`:704-705`); optional `<pubDate>` via `_valid_feed_date` (`:388-403`, ISO-8601 or
  RFC 822) → `lastmod_invalid` (`:706-707`). S012 states no feed-date validity rule, so the dual grammar is
  lane policy (A4) and the docstring says so.
- **F2 Atom 1.0.** `_audit_atom` (`:711-739`): root `{http://www.w3.org/2005/Atom}feed`; URL is the first
  `<entry><link href>` with a non-blank href; absent → `feed_item_missing_link` (`:733-734`); non-absolute →
  `loc_not_absolute` (`:735-736`); optional `<updated>` reuses `_valid_lastmod` → `lastmod_invalid`
  (`:737-738`).
- **F3 container-agnostic index.** No suffix test exists on `<loc>` (`_audit_loc`, `:620`);
  `r77_index_container_agnostic` pins `.txt`, `.rss`, `.atom` locators as clean, and a mutant that rejects
  non-`.xml` locators fails it.
- **X1 unsupported root.** `_audit_tree` (`:541-557`): a root whose expanded name is not `{SM}urlset`,
  `{SM}sitemapindex`, `{Atom}feed` or unqualified `rss` returns the check error `format_unsupported`
  (exit 2, `:556`). A known local name in the wrong namespace keeps round-39's `root_invalid` (A7 / four
  frozen cases). The doctype gate runs **before** the root gate (A9, `:523-525`): any doctype is
  `doctype_present`, so a doctype-bearing `<html>` is not `format_unsupported`; d01 is doctype-free.
- **Round-77 file-plumbing guards** (security review, round-39 code):
  - `_open_regular` (`:441-458`): `os.open(O_RDONLY|O_NONBLOCK)` then `S_ISREG` (`:452`); a manifest-named
    FIFO/device is `file_unreadable` at once instead of blocking `open()` forever. Real tool on the FIFO
    case: 0.021 s; a blocking-open mutant was still running after a 60 s external cap.
  - `_resolves_inside` (`:789-798`) used by `_evaluate_check` (`:825`): a manifest-named path must resolve
    inside the manifest directory; a symlink escaping it is `check_invalid`, a symlink to a file inside it
    stays clean. This closes the read-any-file and text line-structure oracle.
  - `_load_manifest` (`:746-757`): the manifest is read bounded to `MAX_MANIFEST_BYTES + 1` (`:47`, 4 MiB);
    a larger manifest is `input_invalid` (exit 2) instead of an unbounded `read()`.
- **Round-39 surface.** Manifest shape, `check_invalid`/`file_unreadable`, encoding/doctype/malformed
  ordering, entry rules, `lastmod`/`changefreq`/`priority`, loc scope, exit alphabet 0/1/2/64 and every
  existing finding id are unchanged; there is now one over-size id, `too_large` (A5). The three guards only
  change inputs outside the frozen cases (symlink escape, FIFO, >4 MiB manifest).
- **A8.** No entry-count rule is applied to feeds (50,000 remains an XML/text rule).

## 3. Selftest receipt (exact command and observed line)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ TMPDIR=/fast/scratch/hyaku/kake-r77/ExecSitemapFormats/tmp \
    python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py
PASS 271/271
```

Exit status 0, no `FAIL` line, stderr empty. The suite's tally line is `PASS <passed>/<total>`
(271/271 = 235 round-39 cases + 36 round-77 cases; `grep -c 'add("r77_'` = 36).

Fault-injection mode on the same bytes:

```
$ TMPDIR=/fast/scratch/hyaku/kake-r77/ExecSitemapFormats/tmp \
    python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py --fault-injection
PASS 271/271
FAULT silent: rejected as expected (0/271 cases accepted)
FAULT constant-clean: rejected as expected (86/271 cases accepted)
```

Coverage gate (runs before PASS):

```
$ python3 -B scripts/sitemap_audit_selftest.py --map > map.out
case count: 271
sentence coverage: 34/34
```

11 rule-polarity lines (a–k) are printed and all have both signs. (Piping `--map` directly into `head`
raises a `BrokenPipeError` inside `print_map` — a pre-existing suite cosmetic, not a coverage failure;
the receipt above used a file.)

## 4. Rule → failing case if the rule is removed

Each row was produced by copying the final tool to scratch, replacing exactly the named construct, and
running the named selftest case through the suite's own `materialize`/`run_tool`/`check_case` machinery.
"Observed" is the first problem the mutant produced. All mutation rows printed `FAILS AS EXPECTED`.

| contract rule | code (final tool) | case that fails | observed for the mutant |
|---|---|---|---|
| G2 magic, never the name | `_load_payload` `:476` | `r77_gzip_magic_reads_body` | `exit 1 != 0` |
| G1/A1 expanded size limit (gzip) | `:479-480, :503-506` | `r77_gzip_decompressed_too_large` | `findings [('text_empty', None)] != [('too_large', None)]` |
| G1/A1 expanded size limit (text) | `:503-506` | `r77_text_too_large` | `findings [('text_too_many_entries', None)] != [('too_large', None)]` |
| G1 exact boundary `<=` | `:479, :503` | `r77_gzip_exact_limit_clean` | boundary pin (no separate mutant) |
| G2/A6 corrupt/truncated is exit 2 | `:482-483` | `r77_gzip_truncated_stream` | `exit 1 != 2` |
| T1 `text_line_not_url` | `_audit_text` `:661-665` | `r77_text_comment_line` | `exit 0 != 1` |
| T1 `text_url_not_absolute` (path) | `:661-665` | `r77_text_relative_url` | `exit 0 != 1` |
| T1 `text_url_not_absolute` (scheme) | `:661-665` | `r77_text_scheme_url` | `exit 0 != 1` |
| T1 `text_empty` | `:666-667` | `r77_text_empty`, `r77_text_blank_only` | `exit 0 != 1` |
| T1 `text_too_many_entries` | `:668-669` | `r77_text_too_many_entries` | `exit 0 != 1` |
| T1/A3 BOM stripped from first URL | `:511-512` | `r77_text_bom_first_url` | `exit 1 != 0` |
| F1 RSS `feed_item_missing_link` | `_audit_rss` `:702-703` | `r77_rss_missing_link` | `findings [('loc_not_absolute', 1)] != [('feed_item_missing_link', 1)]` |
| F1 RSS `lastmod_invalid` (`<pubDate>`) | `:706-707` | `r77_rss_bad_pubdate` | `exit 0 != 1` |
| F1 RSS `loc_not_absolute` | `:704-705` | `r77_rss_relative_link` | `exit 0 != 1` |
| F2 Atom `feed_item_missing_link` | `_audit_atom` `:733-734` | `r77_atom_link_without_href` | `findings [('loc_not_absolute', 1)] != [('feed_item_missing_link', 1)]` |
| F2 Atom `lastmod_invalid` (`<updated>`) | `:737-738` | `r77_atom_bad_updated` | `exit 0 != 1` |
| F2 Atom `loc_not_absolute` | `:735-736` | `r77_atom_relative_href` | `exit 0 != 1` |
| X1 unknown root is exit 2 | `_audit_tree` `:541-557` | `r77_root_html_unsupported` | `exit 0 != 2` |
| A9 doctype gate precedes root gate | `_audit_xml` `:523-525` | `r77_root_html_doctype_first` | `exit 2 != 1` |
| F3 index locs container-agnostic | `_audit_loc` `:620` (no suffix test) | `r77_index_container_agnostic` | suffix-inference mutant added to `_audit_loc`: `exit 1 != 0` |
| Manifest containment (realpath) | `_resolves_inside` `:789-798`, `:825` | `r77_symlink_escape_rejected` | `exit 0 != 2` |
| Bounded manifest read | `_load_manifest` `:753, :756` | `r77_manifest_too_large` | `exit 0 != 2` |
| Non-regular file never blocks | `_open_regular` `:441-458` | `r77_fifo_named_file_unreadable` | timing: real tool 0.021 s; blocking-open mutant still running after the 60 s external cap |

The FIFO row is timing-verified rather than mutation-verified: removing `S_ISREG` alone still returns
`file_unreadable` because the subsequent `seek` on the non-seekable descriptor fails, so the file-level
case does not discriminate that line; `O_NONBLOCK` is what removes the hang, and a mutant without it
cannot be run to completion.

Additional pins that are not mutation rows: `r77_text_gzip` (gzip + text dispatch),
`r77_gzip_name_plain_body` (`.gz` name, plain XML), `r77_text_suffix_no_inference` (text named `.xml`),
`r77_gzip_exact_limit_clean`, `r77_text_exactly_50000_entries`, `r77_text_invalid_utf8` (round-39
`encoding_invalid`), `r77_rss_rfc822_pubdate` (real RSS 2.0 date, clean), `r77_doctype_prefixed_name`,
`r77_text_blank_only`, `r77_symlink_inside_allowed` (a symlink inside the manifest directory stays clean).

Exact harness commands (from the lane root):

```
$ TMPDIR=/fast/scratch/hyaku/kake-r77/ExecSitemapFormats/tmp \
    python3 -B /fast/scratch/hyaku/kake-r77/ExecSitemapFormats/mut/run_all.py
$ TMPDIR=... python3 -B .../mut/guards.py     # the two guards above, before run_all absorbed them
$ TMPDIR=... python3 -B .../mut/guards2.py    # manifest-unbounded + FIFO timing probes
```

The harnesses imported `scripts/sitemap_audit_selftest.py` read-only and wrote mutants only under scratch.

## 5. Matrix preview (not the frozen receipt)

The frozen counting command must be run by the L1 against a **committed full hash**. My bytes are
uncommitted, so I ran the instrument with `--tool` on the worktree and a placeholder revision label:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ TMPDIR=/fast/scratch/hyaku/kake-r77/ExecSitemapFormats/tmp \
    python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool scripts/sitemap_audit.py \
      --revision worktree-preview --cases .ufo/waves/round-77/cases \
      --consts .ufo/waves/round-77/consts --work /fast/scratch/hyaku/kake-r77/ExecSitemapFormats/matrix4
C2 revision=worktree-preview cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true
```

Constants from the last verbose run: `always_clean` fails 12 cases, `empty_findings_real_exits` 10,
`report_every_id` 20, `round39_xml_only` 18 — each fails at least one, as the instrument requires.

Case expectations were aligned by the instrument owner while this seat edited: `cases/g02/expect.json`
names `too_large`, `cases/g03/expect.json` names `gzip_invalid`, and `cases/g01` now carries a gzip body
named `sitemap.xml.bin` so the population decides G2 (the instrument owner's F1 closure). This preview is
preview evidence only: the printed revision is a label I supplied, not a committed measurement.

## 6. Review responses and residual risks

- **SentinelC criteria 1, 2, 5** held on the superseded `742c2ab1` bytes (bounded gzip read with flat
  memory, doctype rejected before any parser, exit alphabet 0/1/2/64, MemoryError/RecursionError → exit 2).
- **SentinelC F2 (symlink escape / line oracle)** fixed: `_resolves_inside` + `_evaluate_check`; the
  escape is `check_invalid`, an inside symlink stays clean (`r77_symlink_escape_rejected`,
  `r77_symlink_inside_allowed`).
- **SentinelC F3 (FIFO blocks `open`)** fixed: `_open_regular` uses `O_NONBLOCK` + `S_ISREG`; the FIFO
  case returns `file_unreadable` in 0.021 s, while the blocking-open mutant exceeded a 60 s external cap.
- **SentinelC F4 (unbounded manifest read)** fixed: `_load_manifest` caps at 4 MiB + 1; a 4 MiB+ manifest
  is `input_invalid` exit 2 (`r77_manifest_too_large`).
- **SentinelC criterion 4**: invalid UTF-8 in a sitemap body keeps the frozen round-39 `encoding_invalid`
  finding at exit 1 (selftest `enc_invalid_bytes`, `scripts/sitemap_audit_selftest.py:358-362`); container
  corruption stays exit 2.
- **ReviewC2 F1** is closed by the instrument owner (g01 renamed to `sitemap.xml.bin`); the tool was
  already magic-dispatched and its selftest rejected a name-gated wrapper.
- **ReviewC2 F3/F4/F6** as before: RFC 822 branch pinned in the selftest; date-only Atom `<updated>` is
  accepted because F2 says "reuse the existing date validation" (A4 lane policy; knowledge entry owed by
  `ScribeSources`); A5/A6 reflected in tool, selftest and cases.
- **Hash process note.** Three hashes were emitted while bytes legitimately changed: `16ea784f…`
  (pre-amendment), `742c2ab1…` (amendment-aligned), and the final `f767af77…` (after the security guards).
  This report measures only `f767af77…` / `f22e0a67…`; no further edits were made after these receipts.
- **Frozen receipt pending.** The committed-hash run of `.ufo/waves/round-77/c77_sitemap_matrix.py` is the
  claim's receipt; this seat must not commit. The worktree preview is 20/20, 4/4 with `met=true`.
- **Format decision is content-based.** XML iff the first non-BOM, non-whitespace byte is `<` (or a NUL
  appears in the opening bytes, preserving round-39 UTF-16-without-BOM). A suffix never decides anything.
- **Text lines.** Leading/trailing XML whitespace is stripped before judging and blank lines are ignored;
  a whitespace-only line is blank (A3's BOM convention is documented in the code).
- **Empty feeds.** An RSS/Atom document with no items/entries yields `no_entries`, consistent with an empty
  `urlset`; outside the frozen matrix and outside A8's entry-count gap.
- **No network, no installs.** The tool remains Python standard library only, offline. Nothing was
  installed or upgraded for this seat.
- Scratch `S=/fast/scratch/hyaku/kake-r77/ExecSitemapFormats` held all temporary fixtures, mutants and
  preview receipts and is removed after this report; `/tmp` was not used for fixtures.
