# ScoutSources — round 75, wave w1 (kake lane)

Report path: `.ufo/waves/round-75/w1/ScoutSources.md`
Artifacts: `.ufo/waves/round-75/w1/ScoutSources/`
Measured revision: `c9c5e484c533aa65f4374b841a3edcf572ed19a9` (base; lane master at round open)
Read-only seat: no production file in the lane was created, edited or deleted; no git/jj mutation was
run in the lane. Only this report and its artifact directory were written. The scratch tree
`/fast/scratch/hyaku/kake-r75/ScoutSources-6` was removed before yield (nothing above 50 MB was staged
there; no tool was installed).

## 0. Verdicts

1. **in-toto statement (S443 grounding).** `GET` returned `HTTP 200`, final URL identical to the
   requested URL, 0 redirects, 2,492 bytes, sha256
   `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`; the sentence carrying
   "MUST have `digest` set" is **line 37 (37–37), 6 whitespace words, raw substring**:
   "Each element MUST have `digest` set."
2. **R4 re-derivation.** The permission false-negative quote is at tag-stripped **lines 327–329**
   (21 words, whitespace-collapsed); the Return-True quote is at **lines 325–326** (20 words,
   whitespace-collapsed). The lesson's `326-329` is one line early — **corrected range 327–329**.
3. **SOURCES anchors.** S441's cell (`entry 324-329, quote 325-326`) and S442's cell
   (`entry 3519-3524, quote 3520-3521; Note 236-239, quote 237-238`) are **exact against the retained
   tag-stripped text**; no row mismatch. Adjacent (not R4): `corpus/lessons/round-74.md:49` records
   the module-note quote as `237-239`, one line long for a quote that ends on line 238.

## 1. Item 1 — in-toto statement (`spec/v1/statement.md`)

### 1.1 Fetch record

Command: `curl -sSL -o intoto-statement.md -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\nsize_download=%{size_download}\nnum_redirects=%{num_redirects}\n' https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md`

| field | first GET (2026-11-03 21:01 local) | second GET (2026-11-04T00:02:50Z) |
|---|---|---|
| `http_code` | 200 | 200 |
| `url_effective` | `https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md` | same |
| `num_redirects` | 0 | 0 |
| `size_download` | 2492 | 2492 |
| curl exit | 0 | 0 |
| sha256 of saved bytes | `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` | same (`cmp`: identical) |

- Raw bytes retained at `ScoutSources/intoto-statement.md` (2,492 B, 73 newline characters, ends with
  a newline). Hash and size **match the contract's §Frontier declaration** and the L1's 2026-11-03
  copy.
- L1 copy `/fast/scratch/hyaku/kake-r75/l1/intoto-statement.md` **still exists** at measurement
  (2,492 B, mtime 2026-11-03 20:50): `cmp` → `IDENTICAL`, sha256 equal to the re-fetch. The fetch was
  nevertheless redone from the network, not read from that copy.

### 1.2 Located quote for the `subject` field

Raw source lines (blockquote markers included):

```
36: > Set of software artifacts that the attestation applies to. Each element
37: > represents a single software artifact. Each element MUST have `digest` set.
```

| item | value |
|---|---|
| quote (exact) | ``Each element MUST have `digest` set.`` |
| line range | **37–37** (starts after the blockquote marker on line 37) |
| word count | **6** (whitespace split: Each/element/MUST/have/`digest`/set.) |
| quote class | **raw substring** — byte-exact occurrence in the file; no newline or spacing normalization needed |
| requirement carried | the `subject` field's per-element digest requirement ("Each element MUST have `digest` set.") |

Context-only alternative (not recommended as the quote): with the two preceding sentences it is
22 words, spans **lines 36–37**, and is **not** a raw substring and not a naive whitespace-collapse:
the collapse leaves the blockquote marker mid-sentence
(`…Each element > represents a single software artifact…`). It matches only after
**line-leading blockquote-marker removal followed by whitespace collapse** (verified in
`ScoutSources/verify_sources.py`). A checker that searches raw or naively collapsed bytes will not
find it; the 6-word sentence above is the safe form.

## 2. Item 2 — round-74 R4 re-derivation from retained bodies

Bodies re-opened at `.ufo/waves/round-74/sources/python-os-path.html` and `.txt` (both committed at
base: blobs `9421fc6f…` / `a18809af…`; worktree sha256 equal to `git cat-file` blob sha256). The
tag-stripped `.txt` was reproduced byte-for-byte from the `.html` by the recorded pipeline
(script/style blocks dropped, remaining `<…>` runs dropped, `html.unescape`), so the `.txt` line
numbers are mechanically anchored.

Exact tag-stripped text, lines 324–329:

```
324: os.path.exists(path)¶
325: Return True if path refers to an existing path or an open
326: file descriptor.  Returns False for broken symbolic links.  On
327: some platforms, this function may return False if permission is
328: not granted to execute os.stat() on the requested file, even
329: if the path physically exists.
```

| quote | text | tag-stripped lines | words | class |
|---|---|---|---|---|
| Return-True sentence | "Return True if path refers to an existing path or an open file descriptor. Returns False for broken symbolic links." | **325–326** | **20** | whitespace-collapsed (line break at 325/326; line 326 has a double space after `descriptor.` which the quote normalizes to one) |
| permission false-negative sentence | "may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists" | **327–329** | **21** | whitespace-collapsed (line breaks at 327/328 and 328/329) |

- Neither quote is a raw substring of the `.txt`; both are exact after collapsing each whitespace run
  to one space (`ScoutSources/verify-output.txt`).
- **Corrected permission range: 327–329** (the closure's R4 correction is confirmed). The lesson's
  `326-329` begins one line early: line 326 belongs to the Return-True sentence and its trailing
  `On`, which starts the permission sentence ("**On** some platforms, …").
- Why the off-by-one is easy to make and must not be "fixed" by widening: the full sentence with
  its `On` lead-in is **26 words** (lines 326–329), over the 25-word cap; the recorded 21-word quote
  deliberately starts at `may` on line 327, so its exact range is 327–329.

## 3. Item 3 — SOURCES.md row anchors vs derived line numbers

Rows read at base (`git show c9c5e48…:corpus/SOURCES.md`, lines 187–188) and in the worktree; the two
row byte strings are identical (797 B and 1,019 B).

| row | anchor cell text (exact) | derived from retained text | verdict |
|---|---|---|---|
| S441 | `os.path.exists(path) entry, tag-stripped text lines 324-329, quote at lines 325-326; fetched 2026-11-03, HTTP 200, 90,223 bytes, sha256 aa392ce9…e479a8, retained at .ufo/waves/round-74/sources/python-os-path.html (tag-stripped text alongside)` | heading `os.path.exists(path)¶` at 324; entry body ends at 329; Return-True quote is 325–326 | **no mismatch**; the 324–329 entry range already contains the corrected 327–329 permission sentence. HTML sha256 `aa392ce9…e479a8` and 90,223 B confirmed for both worktree and committed blob |
| S442 | `os.stat(path, *, dir_fd=None, follow_symlinks=True) entry, tag-stripped text lines 3519-3524, quote at lines 3520-3521; module Note at lines 236-239, quote at lines 237-238; fetched 2026-11-03, HTTP 200, 791,358 bytes, sha256 4a8bb54c…3d287a, retained at .ufo/waves/round-74/sources/python-os-stat.html (tag-stripped text alongside)` | heading at 3519; entry body through `object.` at 3524; stat quote (22 words) 3520–3521; `Note` at 236; note block 236–239; 21-word note quote ends at `paths` on 238 | **no mismatch**; all four recorded line numbers exact. HTML sha256 `4a8bb54c…3d287a` and 791,358 B confirmed |

Adjacent observations (reported, not part of R4's S441 range):

- `corpus/lessons/round-74.md:49` records the module-note quote as "21 words, tag-stripped text lines
  237-239". The 21-word quote ends on **line 238** (`…file names and paths`, with line 238 continuing
  `, or other arguments`); the row's `237-238` is the exact anchor. `237-239` is one line long for the
  quote as truncated, though the full sentence does run to 239.
- The round-74 spotcheck calls the row's `teaches` quote "21-word … ('Return True … broken symbolic
  links')". The `teaches` cell is a 21-word paraphrase ("os.path.exists returns True …"); the source
  sentence at 325–326 is **20** words. The line range (325–326) is right either way; only the
  word-count label conflates the paraphrase with the source sentence.
- S443 is **absent** at base and in the worktree (0 rows in both), so the scribe's "`source: S443
  (pending)`" branch applies until the L1 lands the row.

## 4. Method, commands, exit codes

Tag-strip pipeline (retained in `ScoutSources/verify_sources.py`, exit 0):
drop `<script …>…</script>` and `<style …>…</style>` (case-insensitive, dotall), drop every remaining
`<…>` tag run, `html.unescape`. Applied to the retained HTML it reproduces each retained `.txt`
**byte-for-byte**:

| file | bytes | sha256 |
|---|---|---|
| `python-os-path.html` | 90,223 | `aa392ce964293f0919e77c51a35e3007bec1c2a1c81504cde98b308e31e479a8` |
| `python-os-path.txt` | 23,886 | `f7e7bd912a7cc2fdfa3c502d5864623cf541d2ea411f77d64165a93d3985a784` |
| `python-os-stat.html` | 791,358 | `4a8bb54c83fab12232926148f2a8cc72868ce62dffb401c547174c70273d287a` |
| `python-os-stat.txt` | 190,195 | `8d1cbad5cf62b0eb101f17903c23727a6c106f120b680bf1f0204c13b574cc5f` |

Checks run (all exit 0 unless stated):

1. `curl -sSL … statement.md` → HTTP 200, 0 redirects, 2,492 B; saved sha256 `cbe684a1…55ebea`.
2. Second `curl -sSL` → same status/size/hash; `cmp` against retained artifact → identical.
3. `sha256sum` + `cmp` against `/fast/scratch/hyaku/kake-r75/l1/intoto-statement.md` → identical
   (2,492 B, mtime 2026-11-03 20:50).
4. `python3 -B ScoutSources/verify_sources.py <lane> ScoutSources/intoto-statement.md` → exit 0;
   full output at `ScoutSources/verify-output.txt`.
5. `git -C <lane> cat-file -p <blob> | sha256sum` for the four round-74 blobs vs worktree sha256 →
   all equal (`ScoutSources/integrity.txt`).
6. `git show c9c5e48…:corpus/SOURCES.md` row comparison → S441/S442 rows byte-identical to worktree;
   S443 count 0.

## 5. Limits and unknowns

- Line numbers are for the retained **per-line tag-stripped derivative**. They are reproducible from
  the retained HTML by the recorded pipeline, but a different stripper (e.g. one that reflows text or
  drops blank lines) would produce different line numbers. The hash-pinned `.txt` is the anchor.
- `raw.githubusercontent.com/.../main/...` is a mutable ref; the sha256 pins the measurement, and two
  GETs ~3 hours apart were byte-identical. A later drift is detectable only by re-hashing.
- No LSP applies to this ticket: the inputs are a web-spec markdown blob and retained HTML/plain-text
  bodies, not a codebase with a language server; string location on the committed bytes is the
  literal, appropriate method here, and no semantic claim rests on it.
- The only unresolved item is the adjacent round-74.md:49 `237-239` label (documentation defect,
  scribe territory), not a source-line uncertainty.
