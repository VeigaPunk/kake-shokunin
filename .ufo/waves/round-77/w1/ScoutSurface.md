# ScoutSurface — kake round 77, wave w1: read-only data walk for C1 and C2

**Seat.** ScoutSurface (leaf; no subagent dispatch, no network, no production edits).
**Lane.** `/home/vgpnk/Projects/shokunin/kake-shokunin`.
**Revisions.** Base of record `a2cc5f51` (`a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`). Lane HEAD at the time
of this walk is `bc2e5fb9`, whose only change against base is the added
`.ufo/waves/round-77/contract.md` (`git diff --stat a2cc5f51..bc2e5fb9` → 1 file, +169). Every file this
report measures is blob-identical at `bc2e5fb9` and `a2cc5f51`:

```
$ for f in scripts/sitemap_audit.py scripts/sitemap_audit_selftest.py SHONEN.md LOG.md SKILL.md PROVINCE.md SCORECARD.md; do
    a=$(git rev-parse a2cc5f51:$f); b=$(git rev-parse bc2e5fb9:$f); [ "$a" = "$b" ] && echo "same $f" || echo "DIFF $f"; done
same scripts/sitemap_audit.py
same scripts/sitemap_audit_selftest.py
same SHONEN.md
same LOG.md
same SKILL.md
same PROVINCE.md
same SCORECARD.md
```

**Line numbers.** All `scripts/sitemap_audit.py` line numbers below are **base-blob numbers**
(`git show a2cc5f51:scripts/sitemap_audit.py`, 657 lines). The worktree file is being edited by an executor
while this walk ran: the worktree held 665 lines (`git status --porcelain scripts/` → ` M
scripts/sitemap_audit.py`, `git diff --stat` → 8 insertions; `git diff` shows two hunks — the module
docstring/imports/constants block, and a new `_valid_feed_date` after `_valid_priority` — with further work in
flight). Do not read worktree line numbers as base numbers; a +8 shift already applies below the module
docstring.

**Method.** Structural read of the two scripts; retained-spec read of S012 from the committed round-39 copies;
and an empirical base run of the 20 frozen C2 cases. The base-run harness is reproduced in §B.0 so any seat
can re-derive the `base observed` column.

---

## A. `scripts/sitemap_audit.py` — the surface a format extension must respect

### A.1 Module constants and the exit alphabet (lines 25–60)

| line | symbol | value |
|---|---|---|
| 25–26 | `SM_NS`, `SM_PREFIX` | `http://www.sitemaps.org/schemas/sitemap/0.9`; `{…}` Clark form |
| 28 | `MAX_BYTES` | `52428800` (comment: "sentence 19") |
| 29 | `MAX_ENTRIES` | `50000` ("sentence 20") |
| 30 | `MAX_LOC_CODEPOINTS` | `2048` ("sentence 23") |
| 32 | `XML_WS` | `" \t\r\n"` ("sentence 21") |
| 34–37 | `EXIT_CLEAN` / `EXIT_FINDINGS` / `EXIT_CANNOT` / `EXIT_USAGE` | `0` / `1` / `2` / `64` |
| 39–41 | `CHANGEFREQ_VALUES` | the seven sitemap values |
| 46–51 | `_LASTMOD_RE` | `YYYY-MM-DD[Thh:mm[:ss[.f]][Z\|±hh:mm]]` |
| 53 | `_DECIMAL_RE` | signed decimal |
| 55, 57–60 | `_XML_DECL_RE`, `_ENC_ATTR_RE` | declaration and `encoding=` extraction |

The tool is a single-purpose CLI: `main` (615) accepts exactly `["--manifest", path]` (616–617; anything else
returns 64).

### A.2 The manifest loader — `_load_manifest`, lines 523–552

1. Read whole file as bytes (525–527); an `OSError` returns `None` → `input_invalid` (623–626).
2. Decode UTF-8; a `UnicodeDecodeError` returns `None` (530–533).
3. **Strip a leading U+FEFF** (534–535) — the one place a BOM is already tolerated.
4. `json.loads` with `parse_constant` that raises, so `NaN`/`Infinity` are rejected (537–543).
5. Require a `dict` (544–545), `version` exactly `int` 1 — `type(version) is not int` rejects `True` and
   `1.0` (546–548), and a non-empty list `checks` (549–551).
6. Return the raw check list; per-check validation happens in `_evaluate_check` (561–602).

`_file_value_invalid` (555–558) rejects absolute paths and any `..` segment. `base_dir` is the manifest's own
directory (`os.path.dirname(os.path.abspath(manifest_path))`, 628), so every `file` value is resolved relative
to the manifest.

`_evaluate_check` (561–602): non-dict → `check_invalid` (563–564); duplicate or non-string `id`/`file`/
`sitemapUrl` → `check_invalid` (574–583); bad file value → `check_invalid` (585–586); an unparseable
`sitemapUrl` → `check_invalid` (588–590). Only then `_audit_file` (592).

### A.3 The read / container / parse path — `_audit_file`, lines 405–431

This is the whole format front-end, and the order matters:

| step | lines | behaviour |
|---|---|---|
| read | 407–409 | `handle.read(MAX_BYTES + 1)` — reads at most one byte past the limit |
| size gate | 412–413 | `len(data) > MAX_BYTES` → **finding** `too_large`, entry `None` |
| unreadable | 410–411 | `OSError` → **error** `file_unreadable` (exit 2, not a finding) |
| decode | 414–417 | strict UTF-8; `UnicodeDecodeError` → finding `encoding_invalid` |
| BOM | 418–419 | leading `\ufeff` stripped |
| declared encoding | 420–422 | a declaration naming anything but UTF-8 → `encoding_invalid` |
| doctype | 423–424 | `_has_doctype` → finding `doctype_present`, **before** any root decision |
| NUL | 425–426 | `"\x00"` → `xml_malformed` |
| parse | 427–430 | `ElementTree.fromstring`; any exception → `xml_malformed` |
| tree | 431 | `_audit_tree(root, sitemap_url)` |

Two parse paths, not one:

- **expat** is used only for doctype detection — `_has_doctype` (388–402) builds
  `xml.parsers.expat.ParserCreate()`, installs `StartDoctypeDeclHandler`, sets
  `SetParamEntityParsing(…NEVER)`, and runs a full `Parse(text, True)` whose `ExpatError` is swallowed.
- **ElementTree** (`fromstring`, 428) builds the actual tree. `_audit_tree` then walks `root` in Clark
  notation.

**Consequence for the extension.** A container layer (gzip) must be inserted **between 409 and 412**: the byte
limit is currently a `stat`-like check on the *file*, so a gzip stream must be decompressed first and the limit
applied to the decompressed length, otherwise `g02` cannot be decided (measured: the base reads 51,124
compressed bytes and dies at 417 with `encoding_invalid`). The decode at 415 must then run on the decompressed
bytes, and the BOM strip at 418 applies to them.

### A.4 Where the document root is decided — `_audit_tree`, lines 434–459

```
436–437   root.tag == SM_PREFIX + "urlset"     -> kind="urlset",      entry_name="url"
438–439   root.tag == SM_PREFIX + "sitemapindex" -> kind="sitemapindex", entry_name="sitemap"
440–441   otherwise                              -> return {("root_invalid", None)}
```

The comparison is **namespace-qualified**: `<urlset>` without the sitemaps namespace is already
`root_invalid` (selftest `root_no_namespace`, 332–334), as is `<feed>` in the sitemaps namespace (selftest
`root_wrong_local`, 335–339). After the root gate: children not in `SM_PREFIX` are skipped silently (445–446);
in-prefix children other than the entry element raise `element_unexpected` at entry `None` (449–450); zero
entries → `no_entries` (452–453); `> MAX_ENTRIES` → `too_many_entries` (454–455); then per-entry
`_audit_entry` (462–501) and per-`loc` `_audit_loc` (502–524).

`_audit_loc` (502–524) is the entry-level URL rule set: `len(value) >= MAX_LOC_CODEPOINTS` → `loc_too_long`
(504–505); `_parse_url` `None` → `loc_not_absolute` and **return** (506–509);
`parsed[:3] != sitemap_url[:3]` → `loc_out_of_scope` and return (510–512); for `urlset` only, the directory
prefix check (513–516). `_parse_url` (287–306) normalises to `(scheme, host.lower(), port, path-or-"/")` and
already defaults ports 80/443.

### A.5 The three limits and where each is enforced

| limit | constant | enforced at | emitted id | entry |
|---|---|---|---|---|
| 52,428,800 bytes | 28 | `_audit_file` 412–413 (on the bytes actually read, `MAX_BYTES + 1`) | `too_large` | `None` |
| 50,000 entries | 29 | `_audit_tree` 454–455 (`len(entries) > MAX_ENTRIES`) | `too_many_entries` | `None` |
| 2,048 codepoints per `loc` | 30 | `_audit_loc` 504–505 (`len(value) >= MAX_LOC_CODEPOINTS`) | `loc_too_long` | `entry` |

Measured boundary (base, plain XML urlset, same fixture padded with spaces after `</urlset>`'s opening):

```
plain-exact    bytes=52428800 exit=0 status=clean
plain-over-1   bytes=52428801 exit=1 status=findings findings=[('too_large', None)]
```

So the limit is **inclusive** at exactly 52,428,800 bytes; the extension must preserve that off-by-one on the
decompressed length. The `loc` limit is the opposite polarity (`>=`, so 2,048 codepoints is already too long) —
a trap if the text/feed layer reuses `_audit_loc` for a line or an `href`.

### A.6 Finding vocabulary and emitters (base, 17 codes)

| id | emitted at | entry |
|---|---|---|
| `too_large` | `_audit_file` 413 | `None` |
| `encoding_invalid` | `_audit_file` 417, 422 | `None` |
| `doctype_present` | `_audit_file` 424 | `None` |
| `xml_malformed` | `_audit_file` 426, 430 | `None` |
| `root_invalid` | `_audit_tree` 441 | `None` |
| `element_unexpected` | `_audit_tree` 450; `_audit_entry` 476 | `None` / index |
| `no_entries` | `_audit_tree` 453 | `None` |
| `too_many_entries` | `_audit_tree` 455 | `None` |
| `loc_missing` | `_audit_entry` 479 | index |
| `loc_repeated` | `_audit_entry` 481 | index |
| `field_repeated` | `_audit_entry` 488 | index |
| `lastmod_invalid` | `_audit_entry` 493 | index |
| `changefreq_invalid` | `_audit_entry` 496 | index |
| `priority_invalid` | `_audit_entry` 499 | index |
| `loc_too_long` | `_audit_loc` 505 | index |
| `loc_not_absolute` | `_audit_loc` 508 | index |
| `loc_out_of_scope` | `_audit_loc` 511, 516 | index |

Ordering and shape of the emitted list are frozen by `_evaluate_check` 590–596: findings are sorted by
`(-1 if entry is None else entry, code)` and rendered as `{"code": …, "entry": …}` objects. A new family's
findings must go through the same set, so the entry key is `None` for document-level ids and an integer for
entry-level ids — a text line number and a feed item index both fit, but they will interleave in one sort key,
so a text file and an XML file cannot share a check id in one manifest entry (each check audits one file, so
this is safe as written).

Four of the contract's new ids are *parallel names* for conditions the base already names differently:
`too_large`/`sitemap_too_large`, `too_many_entries`/`text_too_many_entries`,
`loc_not_absolute`/`text_url_not_absolute`. None of the seven new ids exists anywhere at base — verified:

```
$ for id in sitemap_too_large text_line_not_url text_url_not_absolute text_empty \
           text_too_many_entries feed_item_missing_link format_unsupported gzip_invalid; do
    printf "%-26s " "$id"; git grep -l -- "$id" a2cc5f51 -- . ':(exclude).ufo/waves/round-77/*'; echo; done
sitemap_too_large          (no output)
… all eight: no output
```

### A.7 Per-check errors and the top-level error

- Per-check `error` values: `check_invalid` (563–564, 583, 586, 590) and `file_unreadable` (411).
- Top-level `error`: `input_invalid` only (624–626 and 642–644), emitted with `checks: []`.
- A check with `status: "error"` forces `any_error` and therefore exit 2 for the whole document, even if
  another check produced findings (636–637, 646–647). This is how `g03` and `d01` must surface: exit 2 is a
  *check error*, and the document verdict becomes `could-not-evaluate`, not `failed-policy`.

### A.8 Determinism

`_emit` (605–607) writes `json.dumps(..., ensure_ascii=True)` plus one `"\n"` and flushes. Nothing else may
reach stdout; the selftest fails a case on any stderr byte (`sitemap_audit_selftest.py:1131-1132`).

### A.9 Exit-code mapping — `main`, 646–653

```
646–647   any check status == "error"        -> verdict "could-not-evaluate", EXIT_CANNOT (2)
648–649   any check status == "findings"     -> verdict "failed-policy",      EXIT_FINDINGS (1)
650–651   otherwise                           -> verdict "clean",              EXIT_CLEAN (0)
652       _emit({"version": 1, "verdict": …, "checks": items})
653       return exit_code
```

`EXIT_USAGE` 64 is returned only for a bad argv (616–617). So `format_unsupported` **must** be a check
*error*, not a finding: a finding would give exit 1 and verdict `failed-policy`, and `d01` would be wrong.

### A.10 `--selftest` — the ticket's premise does not hold

`scripts/sitemap_audit.py` has **no `--selftest` entry point**. `main` (615–617) accepts only
`["--manifest", path]`; the string "selftest" occurs exactly once in the file, in a comment
(`81: # used; the selftest passes under Python 3.10 as it did for the round-41 tool.`). Every other counter in
this lane of that shape (`receipt_lineage.py`, `quote_class.py`, `canonical_audit.py`) does carry `--selftest`;
this one does not. What exists is a **separate delivered runner**, `scripts/sitemap_audit_selftest.py`
(1,323 lines), invoked as `--tool <path>`:

```
usage: sitemap_audit_selftest.py --tool <path> [--fault-injection] | --map     (main, 1253–1268)
```

Consequence for C2: "its delivered selftest still passes" means `python3 -B scripts/sitemap_audit_selftest.py
--tool scripts/sitemap_audit.py` exits 0 and prints `PASS <n>/<n>` — it is a second program, so the extension
must keep that program's *expectations* green, not just the tool's behaviour.

### A.11 The delivered selftest: declaration, tally line, writes

- **Case declaration.** One flat list built by `build_cases()` (114) via a local `add(...)` (117–135) with the
  keyword shape `name, files, sentences, rules=(), manifest=None, argv=None, expect_exit=0, verdict=None,
  error=None, checks=None, manifest_path="manifest.json", usage=False`. `files` maps a relative path to bytes
  **or a callable** (used for the 52 MB fixture: `_oversized`, 102–108, seeks to offset 52,428,800 and writes
  one byte). Expectations are tuples `E(cid, status, error, findings)` (73) holding a **set** of
  `(code, entry)` pairs (77). `sentences` is a list of ints; `rules` a list of `(letter, "pos"|"neg")` pairs.
- **Coverage gate.** `SENTENCES = tuple(range(1, 35))` (32) and `RULES = "abcdefghijk"` (33); `coverage()`
  (1222–1236) fails if any sentence number has no fixture or any rule letter lacks a positive or a negative
  fixture; `main` prints `COVERAGE FAIL: …` (1284–1292). The sentence numbers are the **round-39 contract's**
  34 sentences — they are not extendable by adding a format family, so new gzip/text/feed behaviour can only
  be covered by *cases*, not by new sentence numbers, unless the sentence map itself is re-frozen.
- **Comparison.** `check_case` (1129–1199) compares exit code, empty stderr, the exact top-level key set
  (`{version, verdict, checks}`, plus `error` when the case expects a top-level error), `version`, `verdict`,
  the check count, each check's key set `{id, status, error, findings}` and the findings **as a set** against
  `E(...)`. `usage=True` cases return after the exit/stderr check (1133–1134).
- **Tally line (exact).** `print("PASS %d/%d" % (passed, total))` at **1300**, one line, after a `FAIL <name>`
  block per failing case (1296–1299). Exit status: 1 on any failure, coverage gap, or unrejected fault
  (1301–1321).
- **Writes.** Inside the repo: **none**. Each case gets its own `tempfile.mkdtemp(prefix="sitemap-audit-case-")`
  (1201) and is removed in a `finally` via `shutil.rmtree(..., ignore_errors=True)` (1213–1214); `keep_root` is
  never passed from `main`, so it is always `None`. Fault injection writes into a
  `tempfile.TemporaryDirectory(prefix="sitemap-audit-faults-")` (1304). The tool is executed as
  `[sys.executable, "-B", tool] + argv` with `cwd=<case dir>` (`run_tool`, 1119–1123, 300 s timeout).
- **Fault tools.** `SILENT_TOOL` (1045–1048) is `sys.exit(0)` with no output; `CONSTANT_CLEAN_TOOL`
  (1050–1079) echoes a well-formed `clean` document for any valid manifest. Both must keep being rejected
  (`FAULT <label>: rejected as expected (…<total> cases accepted)`, 1307–1316) after the extension: the
  three-family claims add cases that a clean-printer cannot satisfy.

---

## B. The C2 matrix: 20 cases, minimal bytes, expected values, base behaviour

### B.0 The base run (reproducible)

Run at `a2cc5f51` (tool blob `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`, identical to the
worktree before the executor's edit). One manifest per case, `{"version":1,"checks":[{"id":<cid>,
"file":<name>,"sitemapUrl":"http://example.com/"}]}`, tool invoked as `python3 -B scripts/sitemap_audit.py
--manifest manifest.json` with `cwd` = the case dir:

```python
# fixtures (NS = "http://www.sitemaps.org/schemas/sitemap/0.9")
gz  = lambda b: gzip.compress(b, 9)
# g01 gz(urlset(url(a)+url(b))) · g02 gz(urlset(url(a)) padded to 52_428_801 B)
# g03 b"\x1f\x8b\x08\x00" + b"\x00"*20 · g04 plain urlset named "a.xml.gz"
# t01 "http://example.com/a\n…/b\n…/c\n" · t02 same + "# comment" line
# t03 "http://example.com/a\n/page\n" · t04 b"" · t05 50_001 "http://example.com/p<N>" lines
# t06 gz(2 text URLs) · t07 b"\xef\xbb\xbfhttp://example.com/a\n"
# r01-r04 RSS 2.0 <channel> with <item><link>[<pubDate>] · a01-a03 Atom <feed> with <entry><link href>[<updated>]
# s01 sitemapindex with <loc>…/sitemap.txt, …/feed.rss, …/feed.atom · d01 <html><body><p>x</p></body></html>
```

| id | smallest deciding file (bytes measured) | expected (contract) | base observed at `a2cc5f51` |
|---|---|---|---|
| g01 | gzip(urlset, 2 `<url>`) — **147 B** | 0, clean | exit 1, `encoding_invalid` |
| g02 | gzip; decompressed **52,428,801 B** → **51,124 B** on disk | 1, `sitemap_too_large` | exit 1, `encoding_invalid` |
| g03 | `1f 8b 08 00` + 20 NULs — **30 B** | 2, input fault | exit 1, `encoding_invalid` |
| g04 | plain urlset, 1 `<url>`, named `a.xml.gz` — **150 B** | 0, clean | **exit 0, clean** ✔ |
| t01 | 3 absolute URLs, one per line — **63 B** | 0, clean | exit 1, `xml_malformed` |
| t02 | 2 URLs + `# comment` line — **52 B** | 1, `text_line_not_url` | exit 1, `xml_malformed` |
| t03 | 1 URL + `/page` — **27 B** | 1, `text_url_not_absolute` | exit 1, `xml_malformed` |
| t04 | **0 B** | 1, `text_empty` | exit 1, `xml_malformed` |
| t05 | 50,001 URL lines — **1,288,916 B** | 1, `text_too_many_entries` | exit 1, `xml_malformed` |
| t06 | gzip(2 text URLs) — **46 B** | 0, clean | exit 1, `encoding_invalid` |
| t07 | BOM + 1 URL — **24 B** | 0, clean | exit 1, `xml_malformed` |
| r01 | RSS 2.0, 2 items, `link`+`pubDate` — **379 B** | 0, clean | exit 1, `root_invalid` |
| r02 | RSS, second item without `link` — **298 B** | 1, `feed_item_missing_link` | exit 1, `root_invalid` |
| r03 | RSS, `pubDate` = `not-a-date` — **250 B** | 1, `lastmod_invalid` | exit 1, `root_invalid` |
| r04 | RSS, `link` = `/a` — **203 B** | 1, `loc_not_absolute` | exit 1, `root_invalid` |
| a01 | Atom 1.0, 2 entries, `link href`+`updated` — **395 B** | 0, clean | exit 1, `root_invalid` |
| a02 | Atom entry `<link/>` with no `href` — **209 B** | 1, `feed_item_missing_link` | exit 1, `root_invalid` |
| a03 | Atom `<updated>nope</updated>` — **260 B** | 1, `lastmod_invalid` | exit 1, `root_invalid` |
| s01 | sitemapindex, 3 `<loc>`: `.txt`, `.rss`, `.atom` — **295 B** | 0, clean | **exit 0, clean** ✔ |
| d01 | `<html><body><p>x</p></body></html>`, **no doctype** — **34 B** | 2, `format_unsupported` | exit 1, `root_invalid` |

Base score against the frozen expectation: **2 of 20 correct** (`g04`, `s01`). Note that `g01` and `g02` are
*indistinguishable at base* — both exit 1 with `encoding_invalid` — which is the concrete reason the matrix
must compare finding ids and not only exit codes (the contract's kill rule already says so; this is the byte
that shows it mattering).

Also measured, for the extension's off-by-one: `d01` **with** `<!DOCTYPE html>` (50 B) returns
`doctype_present` at exit 1, because the doctype gate (423–424) runs before the root gate (434–441). A
realistic HTML document therefore cannot decide `d01`; the case must be built without a doctype, or the
implementation must resolve the root name from the doctype (XML 1.0 ties the doctype name to the root name)
before firing `doctype_present`.

### B.1 Ambiguities against S012, with the sentence that makes them ambiguous

S012 identity: the contract names "S012 (`sitemaps.org/protocol.html`) … 45,292 B, sha256 `5e757059…`". The
committed round-39 artifacts match exactly — `.ufo/waves/round-39/sources/sitemaps-protocol.html` is
**45,292 bytes**, sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`; the tag-stripped
text `.ufo/waves/round-39/sources/sitemaps-protocol.txt` (22,366 B) is line-citable evidence at base. All line
numbers below are that file.

1. **G1's quote is a splice, not a contiguous S012 sentence.**
   S012:177–180 reads "have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes). If
   you would like, you may compress your Sitemap files using gzip to reduce your bandwidth requirement;
   however the sitemap file once uncompressed must be no larger than 50MB."
   The contract renders "**the file once uncompressed must be no larger than 52,428,800 bytes**". The meaning
   is right (50MB is defined as 52,428,800 at 177) but the rendered string is not contiguous in S012, and it is
   not contiguity-preserving under elision either (the number is imported from the previous sentence). The
   lane's own C1 counter (`scripts/doc_quote_truth.py`) red-flags exactly this class, so a C2 report quoting G1
   as a whole S012 sentence will not survive the round's own calibration gate. Quote 177 and 179–180 separately,
   or quote the 177 sentence alone.
2. **"no comment line" is not in S012.** T1's rendering ends "…and no other information (no header, footer or
   comment line)". S012:271–272 says "The text file **should** contain no information other than the list of
   URLs. The text file **should** contain no header or footer information." The word "comment" occurs **zero**
   times in the file (`grep -c -i comment` → 0), and both sentences are SHOULD, not MUST. `t02`'s expectation is
   still derivable — from S012:263 "The text file **must** have one URL per line", which a `# comment` line
   violates — but the contract's sentence overstates the source. Cite 263 for the finding; cite 271–272 only as
   the SHOULD that motivates it.
3. **The decompressed-size rule is stated for XML, not for text.** S012:179–180 attaches "once uncompressed" to
   the XML sitemap; the text-file limit at S012:265–266 has no such clause, and S012:273–274 ("you may compress
   your Sitemap text file using gzip") appears after it. So `t06` plus `g02`'s rule being applied to text is an
   *inference* from G1's generalisation, not a quote. It is the sane reading (otherwise a 40 KB gzip could
   expand unboundedly) but the contract should say "applied to all containers by this lane's reading", not
   attribute it to S012.
4. **BOM tolerance is not in S012.** `t07` expects a BOM-prefixed first URL to be clean. S012:268 says only
   "The text file must use UTF-8 encoding"; U+FEFF is legal UTF-8 but is not part of a URL, and S012:263–264
   require one fully specified URL per line. The base tool's XML path already strips a BOM
   (`_audit_file:418–419`, blessed by selftest `enc_utf8_bom_allowed`, 245–247), so stripping in the text path
   is the consistent choice — but it is a lane convention, and `t07` would be `text_url_not_absolute` under a
   strict reading. State it as a lane convention in the tool's docstring and the report.
5. **`r03`/`a03` (`lastmod_invalid` for a malformed pubDate/updated) rest on no S012 sentence.** S012:256–259
   says only "modified date field (the `<pubDate>` field for RSS feeds and the `<updated>` date for Atom feeds)
   - indicates when each URL was last modified. Use of the modified date field is optional." No format, no
   validity rule, and optionality cuts the other way. The XML analogue (S012:64–65 "This date should be in W3C
   Datetime format") is a SHOULD for `<lastmod>` only. The ids are defensible lane policy; the report must not
   claim S012 requires them.
6. **`g02`'s id, `sitemap_too_large`, does not match the tool's existing id for the same condition.** The base
   emits `too_large` (413) for a plain oversized file and the delivered selftest pins that (`lim_too_large`,
   489–491). Two ids for one condition means the C2 matrix must decide which id a plain oversized file emits
   going forward — the contract's own "existing round-39 behaviour is unchanged" sentence freezes `too_large`
   for the plain path. Either keep both names (family-prefixed, like `text_*`) or rename the contract's case.
7. **`g03` names no error string.** The contract says "input fault (2)" but the tool's vocabulary requires a
   concrete `error` value in the check object. The matrix must freeze one (e.g. `gzip_invalid`) or
   `cases == decided` will be satisfied by a case that cannot be compared. Same gap applies to nothing else:
   `d01` does name `format_unsupported`.
8. **X1's root set has no namespace rule, and `rss`/`feed` differ.** RSS 2.0's root is an unqualified `rss`;
   Atom 1.0's is `{http://www.w3.org/2005/Atom}feed`. X1 says "root is none of `urlset`, `sitemapindex`, `rss`,
   `feed`", which reads as local names. This collides with the delivered selftest: `root_wrong_local`
   (`sitemap_audit_selftest.py:335–339`) and `root_invalid_suppresses_entries` (350–354) both use
   `doc("feed", …)`, i.e. a **sitemaps-namespaced** `<feed>`, as their negative fixture. Under a local-name
   rule those two cases flip to feed handling and their `root_invalid` expectation becomes wrong; under a
   namespace-qualified rule (Atom namespace for `feed`) both stay green. S012:248 ("RSS … 2.0 or Atom 0.3 or 1.0
   feed") supports the qualified rule. The contract should say which, and the executor should not discover it
   from a red selftest.
9. **Entry-count limits for feeds are undecided.** S012:177 states 50,000 URLs for an XML sitemap and
   S012:265 for a text file; for syndication feeds S012:250–253 only warns that a feed "may not let search
   engines know about all the URLs in your site". No matrix case covers a >50,000-item feed, so this is a
   silent gap rather than a wrong expectation — record it as such rather than letting a future reader infer a
   rule.
10. **`d01`'s exit code has no S012 support at all.** No S012 line mentions an unsupported format, a rejection
    code, or an exit alphabet (`grep -c -i 'unsupported\|not supported'` → 0). X1 is a lane rule, correctly
    frozen in the contract, but it must be presented as a lane convention; and it is an exit-2 *error*, which
    the tool's own alphabet supports only through `status: "error"` (see A.7/A.9).

### B.2 Implementation anchors the executor will need (derived from A)

| family | anchor that must change | reason |
|---|---|---|
| container | insert decompression between `_audit_file:409` and `:412`; keep the `> MAX_BYTES` inclusive boundary | the limit must see decompressed length; measured boundary at §A.5 |
| container | surface a truncated/invalid gzip as a check **error** (exit 2), not a finding | A.7/A.9 |
| text | a dispatcher before `ElementTree.fromstring` (428) that decides "not markup, not a feed" | text bodies currently die at 430 as `xml_malformed` (t01–t05, t07) |
| text | new ids, not `loc_*`/`too_*` | contract freezes `text_*`; ids are family-parallel (§A.6) |
| feed | root gate at 436–441 extended for `rss`/`feed` **with** a namespace decision | §B.1 item 8 |
| feed | a date rule that accepts RFC 822 (RSS `pubDate`) and RFC 3339 (Atom `updated`) | `_valid_lastmod` (336–354) rejects RFC 822 (`Mon, 02 Nov 2026 00:00:00 GMT`) outright: `_LASTMOD_RE` is anchored on `YYYY-MM-DD` |
| index | none: `_audit_loc` already accepts any absolute in-scope path for `kind="sitemapindex"` (510–516) | s01 already passes at base |
| unsupported | 441 must return a check error, not `root_invalid` | §A.9; and the doctype gate 423–424 runs first | 

---

## C. The C1 surface: four boxes, checks, and what the tree passes today

### C.1 The four boxes, verbatim (`SHONEN.md:5-8`)

```
- [ ] SKILL.md contains real decision tables, error patterns, checklists, cited sources
- [ ] At least one end-to-end domain task executed and logged in LOG.md
- [ ] Instructions executable by an agent without oral context
- [ ] No cross-domain bleed (PROVINCE.md still accurate)
```

`SHONEN.md` is 8 lines total; the four item lines are 5–8, no other `^- \[([ x~])\] ` line exists.

### C.2 Proposed checks (all derivable from committed bytes at one revision)

Each check names the revision it is measured at. Counts below are at `a2cc5f51`, reproduced by the command
shown.

**Box 1 — "real decision tables, error patterns, checklists, cited sources"**

| check | command | measured at `a2cc5f51` | holds |
|---|---|---|---|
| 1.1 every `S###` cited in SKILL.md is a row in SOURCES.md | `comm -23 <(git show $R:SKILL.md \| grep -oE '\bS[0-9]{3}\b' \| sort -u) <(git show $R:corpus/SOURCES.md \| grep -oE '^\| S[0-9]{3}' \| grep -oE 'S[0-9]{3}' \| sort -u)` | empty output; **77** distinct ids, all resolve | ✅ |
| 1.2 decision tables exist | `git show $R:SKILL.md \| grep -cE '^\|[- :|]+\|$'` | **38** table blocks (**245** `^\|` lines) | ✅ |
| 1.3 error patterns exist | `git show $R:SKILL.md \| grep -cE '^#{2,3} .*[Ee]rror'` | **0** headings; `grep -ci error` → **29 lines** carry the word in prose or in table cells (e.g. 104, 221, 388) | ❌ as written |
| 1.4 checklists exist | `git show $R:SKILL.md \| grep -cE '^#{2,3} .*[Cc]hecklist'` + gate registry headings | **1** heading (`## Audit → source-fix → publish checklist`, 57) + **19** `… gate registry` headings; **0** `- [ ]` items | ✅ (heading form) |

Box 1's "error patterns" clause is the weak one: SKILL.md carries error *ids* inside table cells (e.g.
`error.code`, `2=could-not-evaluate` at 388) but no section that states patterns. A check written as
"a heading names error patterns" fails today; a check written as "≥N rows carry an exit-code or error-id
cell" would pass. The ledger must freeze one form, and the honest choice is the row-form with a count.

**Box 2 — "at least one end-to-end domain task executed and logged in LOG.md"**

| check | command | measured | holds |
|---|---|---|---|
| 2.1 LOG.md has round headings | `git show $R:LOG.md \| grep -cE '^## .*[Rr]ound'` | **57** | ✅ |
| 2.2 LOG.md names committed receipt paths | count distinct `.ufo/waves/round-N/…\.(txt\|json\|md\|py)` in LOG.md | **96** distinct | ✅ |
| 2.3 every named receipt path exists at `$R` | per-path `git cat-file -e $R:<path>` | **93/96 exist**; 1 missing: `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt` (cited `LOG.md:1810-1812`); 2 are glob patterns | ❌ by one |
| 2.4 the newest round names a real-input run | `git show $R:LOG.md \| grep -c 'round-76\|Round 76\|Round-76'` | **3** lines | ✅ |

**Box 3 — "instructions executable by an agent without oral context"**

| check | command | measured | holds |
|---|---|---|---|
| 3.1 every `scripts/*.py|sh` named in SKILL.md exists | `for p in $(git show $R:SKILL.md \| grep -oE 'scripts/[a-z0-9_]+\.(py\|sh)' \| sort -u); do git cat-file -e $R:$p \|\| echo MISS $p; done` | **29/29**, no MISS | ✅ |
| 3.2 every `.ufo/waves/round-N/*.py` counter named in SKILL.md exists | same loop over `\.ufo/waves/[a-z0-9-]+/[A-Za-z0-9_./-]+\.py` | **83/83**, no MISS | ✅ |
| 3.3 every `python3 -B <path>` invocation names an existing repo-relative path | extract `python3 -B\s+([A-Za-z0-9_./-]+\.(py\|mjs))` from SKILL.md, `git cat-file -e` each | **89** distinct paths, **0** missing, **0** non-repo-relative | ✅ |

**Box 4 — "no cross-domain bleed (PROVINCE.md still accurate)"**

| check | command | measured | holds |
|---|---|---|---|
| 4.1 no sibling-lane path in `corpus/knowledge/*.md` | `git grep -l -- 'kama-shokunin' $R -- 'corpus/knowledge/*.md'` | **0** files | ✅ |
| 4.2 blanket: none anywhere under `corpus/knowledge` | `git grep -l -- 'kama-shokunin' $R -- corpus/knowledge` | **2** files: `freshness-pins.json:106,410`, `freshness-sidecar.json:2053–2094` (a probe token `~/Projects/shokunin/kama-shokunin/…`, recorded as absent on this host) | ❌ as written |
| 4.3 PROVINCE's declared Present surfaces exist | read `PROVINCE.md:49-60`, `git cat-file -e` each | **2/2** (`scripts/freshness-sweep.mjs`, `scripts/probe-delta.mjs`) | ✅ |
| 4.4 every `## Round-NN` frontier section in PROVINCE.md has a SCORECARD round section | compare heading numbers | PROVINCE **23** distinct rounds ⊂ SCORECARD **57** distinct rounds (20–76) | ✅ |

Note for 4.2: the two JSON files are *probe registries*, not domain absorption — the path is the thing being
probed and is recorded absent. A blanket "no sibling path" check therefore fails on evidence rather than on
bleed; the check must be scoped to entry prose (`*.md`), or must exclude `freshness-*.json`, and say so. The
same holds for the 3 `corpus/knowledge/*.md` files holding `/home/vgpnk/Projects/shokunin/kake-sh…` absolute
paths (`keeper-timer-inert.md:185`, `probe-delta-alerting.md:119,123`, `vault-properties.md:100`) — those are
*this* lane's own paths, not a sibling's.

### C.3 Which boxes the current tree passes

| box | verdict today | the count that decides it |
|---|---|---|
| 1 | **passes** on three of four clauses | 77/77 cited sources resolve, 38 tables, 1 checklist heading; the "error patterns" clause is 0 headings unless restated as row-form |
| 2 | **fails** | 93/96 receipt paths named in LOG.md exist; `round-47/.../offline-sweep-r46-verdict-time.txt` is absent at base, cited at `LOG.md:1810-1812` |
| 3 | **passes** | 29/29 script paths and 89/89 command paths resolve at the revision |
| 4 | **passes** on the scoped check, **fails** on the blanket one | 0 `*.md` files with a sibling path; 2 `freshness-*.json` probe tokens |

This is the calibration finding the C1 seat needs: the lane cannot honestly tick all four. Box 2 is a real
gap (a logged task whose cited receipt does not exist at the revision), and box 4's verdict depends on whether
the check is scoped — which must be written down, not chosen after seeing the result.

### C.4 Consequence for the frozen predicate and the ledger

The frozen predicate is `met <=> boxes == 4 and unexamined == 0 and mismatches == 0`; gaps are *examined*, so
a `status="gap"` row with `reason` + `flip` can still reach `met=true` while the box stays unticked. That is
the honest path here:

- box 1 → `status="evidenced"`, checks 1.1/1.2 plus the row-form of 1.3 with its count.
- box 2 → `status="gap"`; `reason`: the LOG names `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`
  at `LOG.md:1810-1812` and no such blob exists at `a2cc5f51` (`git cat-file -e` → 128); `flip`: that receipt
  is committed (or the LOG line is corrected to a path that exists), after which check 2.3 is 96/96.
- box 3 → `status="evidenced"`, checks 3.1/3.3.
- box 4 → `status="evidenced"` **only** with checks 4.1/4.3/4.4 and the scope sentence written into the check;
  with the blanket 4.2 it is a `gap` whose `flip` is "the two probe registries are excluded by name".
- Markers: all four are `[ ]` at base, so an `evidenced` row against a `" "` marker is a **mismatch** under the
  contract's definition (a) — the markers and the rows must move together, and `"x"` additionally requires a
  named non-author `verifier` in the row.

---

## D. The six routed defects (`corpus/lessons/round-76-verifier-spotcheck.md:147-173`)

First a scope fact: four of the six point at the **fleet** report `.ufo/reports/round-76/kake.md`
(outside the lane, operator/L1-owned), and the other two point at lane files. Lane-side repairs are
append-only by the lane's own rule (a correction line quoting the defective span verbatim plus the re-derived
value), not in-place rewrites of a prior round's row.

| # | pointer(s) | observed bytes | cheapest repair inside this round's write scope | owner |
|---|---|---|---|---|
| 1 | `.ufo/reports/round-76/kake.md:30-35`; lane `.ufo/waves/round-76/w1/ScribeRegistry.md:91,111`; receipt `.ufo/waves/round-76/controls/after-c2-matrix.txt:1` (`tool_sha256=0762452f…`) | receipt head names `revision=master … head=d00ea7fb`; `git cat-file -e d00ea7fb:scripts/hreflang_audit.py` → **absent**; `2cccd59a:…` → present. The matrix's tool digest *is* the landed `0762452f`. | None in the lane: the historical receipt cannot be rewritten, and re-running it is this round's `ExecRevisionReceipts` (contract frontier: "D1 is repaired by the C2 re-run at a full-hash committed revision"). This round's report must name one revision per artifact and state that the r76 matrix lane came from the pinned predecessor. | **executor (D1)**, report wording in lane |
| 2 | `.ufo/reports/round-76/kake.md:130` | "same 16 pre-existing `W04` duplicate-URL warnings, unchanged" | Fleet report line: operator-owned. Lane-side: an append-only correction line in `corpus/lessons/round-77.md` §Corrections quoting the span and giving "17 = 16 inherited + the new S445 duplicate-URL warning". Re-derive the count with the census command before quoting it. | **operator** (fleet text) / lane correction line |
| 3 | `.ufo/reports/round-76/kake.md:34`; receipt `.ufo/waves/round-76/controls/after-c2-realrun.txt:1-2` | report renders `pages=8 findings=[] exit=0`; the receipt is one JSON line (`{"version": 1, "pages": 8, "findings": [], …}`) plus `rc=0` — the rendered string is not a contiguous substring of either line | Fleet line: operator-owned. Lane-side: the correction line must quote the JSON or mark the rendering as a composite (`pages=8` and `findings=[]` are fields of one line; `exit=0` is `rc=0` on the next). | **operator** / lane correction line |
| 4 | `SCORECARD.md:4942` (claim row) and `SCORECARD.md:4913-4929` (section); fleet `.ufo/reports/round-76/kake.md:26-28` | the section holds **five** numbered rows (`SCORECARD.md:4925-4929`) and its own prose says the other two spans live in `corpus/QUALITY.md` and `corpus/lessons/round-75.md`; the claim row says "closed by seven whole-line correction rows in the section above, one QUALITY criterion and one lesson correction" → reads 7+1+1=9 | Lane repair is in scope: append the correction line to `corpus/lessons/round-77.md` §Corrections quoting `seven whole-line correction rows in the section above` and stating **5 + 1 + 1 = 7** with the section's row numbers 4925–4929. Do **not** edit 4942 in place (append-only rule). | **lane** |
| 5 | `.ufo/reports/round-76/kake.md:135` | "hreflang declarations entered from frontier to core" | Evidence: `git grep -in hreflang a0491fcd -- PROVINCE.md corpus/README.md \| wc -l` → **0**; at `a2cc5f51` → **11**. So the area entered from unlisted ground. Fleet line: operator-owned. Lane-side: the correction line states "entered from unlisted ground; the PROVINCE text 'are now core' is accurate, 'frontier to core' is not", with both counts and the two revisions. | **operator** / lane correction line |
| 6 | `.ufo/reports/round-76/kake.md:38`; receipt `.ufo/waves/round-76/controls/ctl-deletion.txt:8` | report writes "deletion (`A1`, `append_only=false`)"; the control's line 8 is `  A1 SCORECARD.md:0 claim row present at --base is gone at the measured revision` — `A1` only, no `append_only=` field (`append_only=` appears only on the `T1` lines, 2–7) | Fleet line: operator-owned. Lane-side correction line: quote the A1 line and drop the parenthetical. | **operator** / lane correction line |

Net: **defect 4 is fully repairable in-lane**; 2, 3, 5, 6 are repairable only as lane-side correction lines
(the defective text itself lives in the fleet report); 1 is repaired by evidence, not by editing — the
revision-pinned re-run the contract already assigns to `ExecRevisionReceipts`.

---

## E. Residual unknowns

1. Whether `scripts/sitemap_audit.py` had a `--selftest` mode in a round-39 draft: not checkable from the
   committed tree (the delivered file has none, and `.ufo/waves/round-39/` would need a per-file read I did
   not do). The ticket's wording is the only place the mode is named.
2. The exact intended semantics of the two SM-namespaced `<feed>` selftest fixtures after feed support (§B.1
   item 8) — the contract does not say, and the executor's in-flight work may already have chosen; the
   delivered selftest is the authority that must stay green or be explicitly amended.
3. Whether `g02`'s `sitemap_too_large` is meant to replace or to coexist with `too_large` for plain files
   (§B.1 item 6); the contract freezes both behaviours in different sentences.
4. The `W04` census count (16 vs 17) is a routed-defect item; I did not re-run the census (it is defect 2's
   repair, owned by the connector/sources seat), so my report carries the pair of numbers only as the defect
   states them.

---

**Scratch.** `/fast/scratch/hyaku/kake-r77/ScoutSurface` (fixtures under `…/tmp`, per-case `mkdtemp`), every
fixture built with an explicit `--work`-style scratch prefix and removed before finishing; no file was written
outside it and `.ufo/waves/round-77/w1/ScoutSurface.md`. **No tool installs or upgrades were made.**
**No network calls.**
