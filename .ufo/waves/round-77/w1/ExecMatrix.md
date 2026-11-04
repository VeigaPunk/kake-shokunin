# ExecMatrix — C2 measurement instrument (round 77, w1)

Seat: executor, leaf. Owned paths only; no production file touched, no commit, no after-state run
(`scripts/sitemap_audit.py` is being written concurrently by `ExecSitemapFormats`).

## 1. Files written

| path | role | sha256 |
|---|---|---|
| `.ufo/waves/round-77/c77_sitemap_matrix.py` | the C2 instrument | `5c6eacba266068845144ba59c8e7099cc22fee10ca95c0ab78019ba33d21afce` |
| `.ufo/waves/round-77/cases/build_cases.py` | deterministic case generator | `d4a67274b39fe56affa2dbf57a7623c164b2fa5523f1eeb7138483eb0d12c599` |
| `.ufo/waves/round-77/cases/{g01..g04,t01..t07,r01..r04,a01..a03,s01,d01}/` | 20 case dirs (`manifest.json`, sitemap file, `expect.json`) | per-case hashes in `controls/case-inventory.txt` |
| `.ufo/waves/round-77/cases/README.md` | shape, inventory, g02/t05 regeneration, freeze note | — |
| `.ufo/waves/round-77/consts/always_clean.py` | constant 1 | `ad4f2123504b2b7d7876a8e94012bec00b54ffc0bbf6d55033cc793bee380d1a` |
| `.ufo/waves/round-77/consts/report_every_id.py` | constant 2 | `bdb248fb201f72b97481d547c191dc5aef2c50125bb79cd57dad460d20dc6be9` |
| `.ufo/waves/round-77/consts/empty_findings_real_exits.py` | constant 3 | `3a1cad8e2a2721427326fabe34878c6cc6b3f25cd4b5e05524d155151aa4f15e` |
| `.ufo/waves/round-77/consts/round39_xml_only.py` | constant 4 (extracted blob) | `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` |
| `.ufo/waves/round-77/consts/README.md` | constant roles and the `C2_REAL_TOOL` contract | — |
| `.ufo/waves/round-77/controls/base-c2-matrix.txt` | base receipt | — |
| `.ufo/waves/round-77/controls/base-c2-matrix.json` | base per-case JSON receipt | — |
| `.ufo/waves/round-77/controls/selftest.txt` | selftest output | — |
| `.ufo/waves/round-77/controls/case-inventory.txt` | per-case byte/hash/expectation table | — |

`controls/` also holds another seat's `r77-hreflang-*.txt` (seen by directory listing only); I did
not modify them.

## 2. Instrument behaviour

```
python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . \
  --tool scripts/sitemap_audit.py --revision <full-hash> \
  --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts --work <scratch>
```

Prints exactly one line and nothing else on stdout:

```
C2 revision=<rev> cases=<n> decided=<n> correct=<n> wrong=<n> constants_failed=<k>/4 met=<true|false>
```

`met <=> cases == decided and wrong == 0 and constants_failed == 4`; exit 0 met, 1 not met,
64 usage, 2 cannot-evaluate (case population not the frozen 20 ids, constants dir not exactly
4 tools, git extraction failure). Per-case detail goes to stderr under `--verbose` and a JSON
receipt to `--json-out`; neither changes stdout.

- `decided` — the tool exited and printed one JSON document with a readable `checks` list.
  `correct` — exit code matches `expect.json`, and for exit 0/1 the `findings[].code` set
  matches with no error check; for exit 2 an error check is present, no finding id is
  reported, and the `error` code set equals the expectation (pinned: `gzip_invalid`,
  `format_unsupported`). `wrong` — decided but not correct. Undecided cases are neither, so
  they break `cases == decided`.
- A constant fails a case when the case is not correct for it or is undecided; it is counted
  when it fails at least one case. Constant 3 runs the measured tool through `C2_REAL_TOOL`,
  so its exits are the measured tool's and only the findings comparison can reject it.
- `--tool-revision <hash>` extracts `scripts/sitemap_audit.py` from the committed revision
  into `--work` with `git show` and measures those bytes.
- `--selftest` builds fixtures under `--work` and prints `selftest <passed>/<total> passed`.

## 3. Case inventory (post-amendment expectations)

| id | file | exit | expected finding ids |
|---|---|---|---|
| g01 | `sitemap.xml.bin` | 0 | — |
| g02 | `sitemap.xml.gz` | 1 | `too_large` |
| g03 | `sitemap.xml.gz` | 2 | `gzip_invalid` (input-fault error) |
| g04 | `sitemap.xml.gz` | 0 | — |
| t01 | `sitemap.txt` | 0 | — |
| t02 | `sitemap.txt` | 1 | `text_line_not_url` |
| t03 | `sitemap.txt` | 1 | `text_url_not_absolute` |
| t04 | `sitemap.txt` | 1 | `text_empty` |
| t05 | `sitemap.txt` | 1 | `text_too_many_entries` |
| t06 | `sitemap.txt.gz` | 0 | — |
| t07 | `sitemap.txt` | 0 | — |
| r01 | `feed.xml` | 0 | — |
| r02 | `feed.xml` | 1 | `feed_item_missing_link` |
| r03 | `feed.xml` | 1 | `lastmod_invalid` |
| r04 | `feed.xml` | 1 | `loc_not_absolute` |
| a01 | `atom.xml` | 0 | — |
| a02 | `atom.xml` | 1 | `feed_item_missing_link` |
| a03 | `atom.xml` | 1 | `lastmod_invalid` |
| s01 | `sitemap-index.xml` | 0 | — |
| d01 | `page.xml` | 2 | `format_unsupported` (input-fault error) |

Two expectations are the contract table **as amended by `amendment-1.md`**, recorded before
any after-state: A5 sets `g02` to `too_large` (`sitemap_too_large` is dropped); A6 pins `g03`
to the input-fault error `gzip_invalid`. A9 requires `d01` without a doctype (it has none).
A7's namespace rule holds: `r01` uses unqualified `<rss>`, `a01` uses
`{http://www.w3.org/2005/Atom}feed`.

## 4. Fixture facts and the g02 recipe

- g01 carries gzip bytes under the non-`.gz` name `sitemap.xml.bin` (152 bytes, sha256
  `5c89ffb4e235988bef3dae6aac09e079c0291a22852d1beb7d2d78de35fc78be`); g04 carries plain XML
  under the `.gz` name `sitemap.xml.gz`. Together they decide G2's magic-not-name rule in both
  directions.
- g02: stored `sitemap.xml.gz` is **51,139 bytes**, sha256
  `2c03fc167426b362a4c817aa84fe21451ea311e3848795ec0a14c099d21bb20e`; decompressed body is
  exactly **52,428,801 bytes** (limit + 1) and is a valid 2-entry urlset padded with spaces
  inside the root, decompressed sha256
  `ae48a82fc06a368f2de4e1ca9aa75f6b304cfedd89ccf0c9181ee228a015325d`.
- Deterministic regeneration (same bytes; `mtime=0`, no embedded name):

```python
import gzip, io
prefix = (b'<?xml version="1.0" encoding="UTF-8"?>\n'
          b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          b'<url><loc>https://example.com/alpha</loc></url>\n'
          b'<url><loc>https://example.com/beta</loc></url>\n')
suffix = b'</urlset>\n'
body = prefix + b' ' * (52428801 - len(prefix) - len(suffix)) + suffix
buffer = io.BytesIO()
with gzip.GzipFile(fileobj=buffer, mode='wb', compresslevel=9, mtime=0) as handle:
    handle.write(body)
open('sitemap.xml.gz', 'wb').write(buffer.getvalue())
```

- t05: 50,001 lines, 1,450,029 bytes, sha256
  `bbb27be0abae92c0462049a4107396ad86f7fee2ecd1bee0334794df12969ecd`.
- All 20 dirs are regenerated by `python3 -B .ufo/waves/round-77/cases/build_cases.py`, which
  prints one `case <id> file=<name> bytes=<n> sha256=<hash> exit=<n> findings=<ids>` line each.
  The captured output is `controls/case-inventory.txt`.

## 5. Base receipt (verbatim)

Command (from the lane root):

```
TMPDIR=/fast/scratch/hyaku/kake-r77/ExecMatrix/tmp python3 -B \
  .ufo/waves/round-77/c77_sitemap_matrix.py --root . \
  --tool-revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 \
  --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts \
  --work /fast/scratch/hyaku/kake-r77/ExecMatrix/base-work \
  --verbose --json-out /fast/scratch/hyaku/kake-r77/ExecMatrix/base-c2-matrix.json
```

stdout, verbatim, exit 1:

```
C2 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 cases=20 decided=20 correct=2 wrong=18 constants_failed=4/4 met=false
```

The gzip, text and feed cases are decided **wrong**; only g04 and s01 are correct. Raw base
outputs: g01/g02 `encoding_invalid` (gzip bytes fail the UTF-8 decode), t01-t05/t07
`xml_malformed`, r01-r04/a01-a03/d01 `root_invalid` (d01 exits 1, not the expected input fault
2). Full per-case detail and the raw outputs are in `controls/base-c2-matrix.txt`; the JSON
receipt is `controls/base-c2-matrix.json`. The receipt was re-emitted after g01's payload was
renamed (section 7); the line and every per-case observation are identical.

Constants, each run over the same 20 cases with `C2_REAL_TOOL` set to the measured tool:

| constant | failed | cases |
|---|---|---|
| `always_clean.py` | 12 | a02 a03 d01 g02 g03 r02 r03 r04 t02 t03 t04 t05 |
| `empty_findings_real_exits.py` | 18 | every case except g04, s01 |
| `report_every_id.py` | 20 | all |
| `round39_xml_only.py` | 18 | every case except g04, s01 |

The XML-only constant matches the base tool exactly: same sha256
(`914ebdee…`, git blob `21553d19…`), identical stdout line, and 0 per-case differences
(observed exit, finding ids, error ids, verdict) over the 20 ids.

## 6. Selftest tally

```
$ TMPDIR=<scratch>/tmp python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py \
    --work <scratch>/selftest-work --selftest
selftest 14/14 passed
```

Checks: line shape; 8 fixture cases decided and correct; four fixture constants counted
failed; `met=true`; a surviving constant not counted (`constants_failed=3`, met false); an
exits-right/findings-empty constant killed on exactly the three finding cases; a deliberately
wrong expectation reported wrong; a crashing tool undecided; exit 2 with a clean status
reported wrong; a code-less exit-2 expectation refused; a wrong input-fault code rejected; the
pinned code accepted; a mixed error+finding exit-2 verdict rejected. Output:
`controls/selftest.txt`.

## 7. Defect found during the wave, and its fix

`ExecSitemapFormats` reported that g03 was unsatisfiable: the first `judge()` folded per-check
`error` codes into the compared finding-id set, so any conforming input-fault code made the
observed set non-empty while `expect.json` said `[]`. The instrument was fixed (finding ids
and error codes compared separately; exit 2 requires an error check, no finding id, and the
pinned code) and the selftest gained the three exit-2 checks above. No case byte changed; the
base line is identical before and after the fix (the base tool is wrong on g03 by exit 1
either way).

`ReviewC2` F1 then found a coverage hole: every gzip payload was named `*.gz`, so a
name-dispatching tool could pass. `g01`'s payload is now `sitemap.xml.bin` (gzip bytes under a
non-`.gz` name; id, bytes and expectation unchanged — the rename landed in
`cases/build_cases.py` during the wave and I adopted it) while `g04` keeps the converse
(plain XML under `.gz`). A name dispatcher now goes red on one of the two. The base receipt is
from the current case set; its line and per-case observations are unchanged.

## 8. Risks and open items

1. **`r01`/`a01` dates.** They carry ISO-8601 (`2026-11-02T10:00:00Z`) because amendment A4
   says a malformed feed date reuses the existing `lastmod` validation; a strict RFC-822
   `<pubDate>` parser would make `r01` dirty. The tool author was told the fixture dates and
   reported all 19 other cases correct against their worktree tool (their local driver, not a
   receipt). If the after-state tool parses RFC 822 only, `r01` goes red — that is a real
   disagreement to settle, not an instrument bug.
2. **`--tool` measures worktree bytes.** The `--revision` label is a receipt label; the frozen
   counting command measures `scripts/sitemap_audit.py` as landed. Only `--tool-revision`
   measures committed bytes.
3. **Population guard.** The instrument refuses (exit 2, no line) a case population that is
   not the frozen 20 ids, so deleting a case cannot green the claim; the same holds for a
   constants dir that does not hold exactly 4 tools.
4. **Constant 3 coupling.** It runs the measured tool via `C2_REAL_TOOL`; standalone it falls
   back to `<lane>/scripts/sitemap_audit.py`. It is a control, not a production tool.
5. **Environment.** Contract says python 3.13; observed `Python 3.14.8`. The instrument and all
   tools are stdlib-only.
6. **No after-state.** Per the assignment, the after-state over the landed tool is the L1's
   run with the frozen counting command. `ExecSitemapFormats` reports final tool bytes sha256
   `f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176` (selftest
   `f22e0a67d777ce80ce2d1099520f50f98016c28901e77b7cb5e4b73c386b9c89`) and a worktree
   preview of this counter at
   `C2 revision=worktree-preview cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true`.
   That is their report, not my evidence: I did not re-run the after-state, and the frozen
   receipt must come from the L1's committed-hash run.

## 9. Tooling

No tool installed or upgraded; pacman not used; no network call. Scratch
`/fast/scratch/hyaku/kake-r77/ExecMatrix` removed after the receipts were copied.
