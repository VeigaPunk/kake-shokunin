# ScoutSources — round 74, wave w1 (kake lane)

Report path: `.ufo/waves/round-74/w1/ScoutSources.md` (lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`)
Artifacts: `.ufo/waves/round-74/w1/ScoutSources/`
Measured revision: `ced2878a1e77f57afb4ee3baebf1021e5130399b` (base; lane master at round open)
Read-only seat: no production file in the lane was created, edited or deleted; no git/jj mutation in the lane.

## 0. Answer in one block

Both sources fetched (`HTTP 200`, no redirect) and **byte-identical** to the copies the L1 retained at
`.ufo/waves/round-74/sources/` — all four files, HTML and tag-stripped text, zero delta. All three quotes
are located in the tag-stripped text with exact line numbers, joins and word counts (20 / 22 / 21 words,
all ≤ 25). At base neither URL appears in `corpus/SOURCES.md`, the highest id is `S440`, so **S441/S442 are
free**; census validate exits 0 with 178 rows. Two landmine constraints found for the L1's landing (both
measured, §3.3): the new `used-by` file `corpus/knowledge/sidecar-reobservation.md` **must land in the same
commit** as the rows (else `E11` ×2, exit 1), and the rows **must be inserted inside `## Registry`** (last
rows after `S440` at line 186), not appended at EOF (else `E12` ×2, exit 1).

## 1. Fetch and retention

Commands run in scratch; exit 0 for both GETs.

| source | requested URL | final URL (`url_effective`) | HTTP | redirects | bytes | content-type |
|---|---|---|---|---|---|---|
| os.path | `https://docs.python.org/3/library/os.path.html` | same (identical) | 200 | 0 | 90,223 | `text/html` |
| os | `https://docs.python.org/3/library/os.html` | same (identical) | 200 | 0 | 791,358 | `text/html` |

`curl -sSL` with `-w 'url_effective=%{url_effective}\nhttp_code=%{http_code}\nsize_download=%{size_download}\ncontent_type=%{content_type}\n'`;
redirect count separately confirmed with `curl -sSIL -o /dev/null -w '%{num_redirects}'` → `0` for both.

Tag-stripped derivative pipeline (`ScoutSources/strip-tags.py`, exit 0 on both files): drop `<script …>…</script>`
(case-insensitive, dotall), drop `<style …>…</style>`, drop every remaining `<…>` tag run, then
`html.unescape`. Saved as `python-os-path.txt` / `python-os-stat.txt`.

### 1.1 sha256 and byte-identity against the L1 retention

| file | bytes | sha256 | L1 copy sha256 | verdict |
|---|---|---|---|---|
| `python-os-path.html` | 90,223 | `aa392ce964293f0919e77c51a35e3007bec1c2a1c81504cde98b308e31e479a8` | identical | byte-identical |
| `python-os-path.txt` | 23,886 | `f7e7bd912a7cc2fdfa3c502d5864623cf541d2ea411f77d64165a93d3985a784` | identical | byte-identical |
| `python-os-stat.html` | 791,358 | `4a8bb54c83fab12232926148f2a8cc72868ce62dffb401c547174c70273d287a` | identical | byte-identical |
| `python-os-stat.txt` | 190,195 | `8d1cbad5cf62b0eb101f17903c23727a6c106f120b680bf1f0204c13b574cc5f` | identical | byte-identical |

Delta: **none**. Because the derivative reproduces the retained `.txt` byte-for-byte, my strip pipeline and
the L1's are the same pipeline on these inputs; the retained text is the valid quote anchor and no
script/analytics drift was observed between the two fetches.

Retained copies also carry the page title `Python 3.15.2 documentation` in both files (line 20 of each
`.txt`: `os.path — Common pathname manipulations — Python 3.15.2 documentation` /
`os — Miscellaneous operating system interfaces — Python 3.15.2 documentation`), so the version stamp to cite
in the registry rows is **3.15.2**, not `3.15` / `3.15.1`.

## 2. Located quotes (anchors are line numbers in the tag-stripped text)

| # | claim | file | line range | heading line | quote | words | join at each break |
|---|---|---|---|---|---|---|---|
| (a) | `os.path.exists` return contract | `python-os-path.txt` | **325–326** | 324 (`os.path.exists(path)¶`) | Return True if path refers to an existing path or an open file descriptor. Returns False for broken symbolic links. | **20** | `…or an open` + 1 space + `file descriptor.` |
| (b) | `os.stat` call contract | `python-os-stat.txt` | **3520–3521** | 3519 (`os.stat(path, *, dir_fd=None, follow_symlinks=True)¶`) | Get the status of a file or a file descriptor. Perform the equivalent of a stat() system call on the given path. | **22** | `…equivalent of a` + 1 space + `stat() system call…` |
| (c) | module-wide `OSError` note | `python-os-stat.txt` | **237–238** | 236 (`Note`) | All functions in this module raise OSError (or subclasses thereof) in the case of invalid or inaccessible file names and paths | **21** | `…(or subclasses thereof) in` + 1 space + `the case of…` |

Notes that matter when the rows are written:

- (a) source line 326 has a **double space** after `descriptor.` (`descriptor.  Returns`); the rendered quote
  above and in the draft row normalizes it to one space. Every other break is a plain space join; there is no
  hyphenation at any of the three breaks (verified: reconstructed text `startswith` the quoted string after
  whitespace normalization, `join-ok=True` for all three).
- (b) the entry continues to line 3524 (`…Return a stat_result / object.`); the quote stops at `path.` on 3521.
- (c) the Note sits in the module introduction, under the block opened by `Notes on the availability of these
  functions:` (line 214), after the VxWorks / WebAssembly paragraphs, and is a standalone `Note` block. The
  quoted sentence **does not end at `paths`**: line 238 continues `, or other arguments` and the sentence ends
  on line 239 (`that have the correct type, but are not accepted by the operating system.`). The quote is a
  truncation at a clause boundary, not a complete sentence — worth keeping in the `anchor` cell so a reader can
  see the tail.
- No quote contains a literal `|` or an escaped `\|` (checked programmatically for all three).

## 3. Corpus state at base (`ced2878a`)

### 3.1 URL presence

| probe | command | result |
|---|---|---|
| exact `…/os.path.html` | `grep -c 'library/os.path.html' SOURCES.md` | **0** |
| exact `…/os.html` | `grep -n 'library/os\.html' SOURCES.md` | no match, exit 1 |
| normalized (`docs.python.org/3/library/os[.path].html`, anchor/scheme/trailing-slash stripped as `url_of()` does) | `grep -cE 'os\.path\.html\|library/os\.html\|os\.html#'` | **0** |
| any `docs.python.org/3/library/os…` row | `grep -nE 'docs\.python\.org/3/library/os' \| wc -l` | **0** |

Neither URL is present, exact or normalized. No `E04`/`W04` risk from these two rows: the census normalizes
to `docs.python.org/3/library/os.path.html` and `docs.python.org/3/library/os.html`, both new.

### 3.2 Ids and row count

- Highest id at base: **S440** (`Shell Parameter Expansion (Bash Reference Manual)`), last row of `## Registry`.
- `grep -cE '^\| S44[12] '` = **0** → **S441 and S442 are free**.
- Registry table rows at base: **178** (matches the contract's "census before … 178 rows").

### 3.3 Census validator (required run)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
… 16 × W04 duplicate-url-across-scopes (S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117 S127 S416 S417 S427 S433)
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit 0 · rows 178 · E codes 0
```

Two constraints for the landing, measured in a scratch `git clone --shared` of the lane checked out at
`ced2878a` (never in the lane itself):

| variant | command | exit | finding |
|---|---|---|---|
| base clone, no new rows | `validate --today 2026-11-03 <clone>` | 0 | control |
| S441+S442 inserted as last `## Registry` rows after line 186, `corpus/knowledge/sidecar-reobservation.md` present | `validate --today 2026-11-03 <clone>` | **0** | E codes 0; `census` → rows **180**, tier.A **157**, tier.B 6, tier.C 17, status.mined **150**, queued 8, rejected 22, missing 0 |
| same rows, knowledge file absent | `validate …` | **1** | `E11 S441 missing used-by corpus/knowledge/sidecar-reobservation.md`, `E11 S442 …` |
| same rows appended at EOF (after `## Paths` / `## Search log` / `## Leads`) | `validate …` | **1** | `E12 S441 row outside Registry section`, `E12 S442 …` |

Consequence for the L1: `corpus/knowledge/sidecar-reobservation.md` **does not exist at base**
(`git cat-file -e ced2878a:corpus/knowledge/sidecar-reobservation.md` → exit **128**; `corpus/knowledge/`
holds `freshness-sidecar.json` only). The two rows and that knowledge file must land in the **same** commit,
and the rows must go **inside `## Registry`** (it spans lines 5–188; `## Paths` starts at 189). Landing the
rows alone fails the harm battery's `census validate exit 0` line.

## 4. Draft registry rows (11 columns, `CORPUS.md` schema)

Verified: each row splits to **13** fields (11 cells + the two empty edge fields) and carries exactly **12**
`|` delimiters; no cell contains a literal or escaped `|`. `kind=docs`, `tier=A`, `status=mined`,
`opened=2026-11-03`, `recheck=90d`, `used-by=corpus/knowledge/sidecar-reobservation.md` (single path; add more
only if the knowledge entry genuinely cites both).

```
| S441 | Python 3.15.2 documentation: os.path — Common pathname manipulations — https://docs.python.org/3/library/os.path.html#os.path.exists | docs | A | os.path.exists's return contract only — not readability, not permissions, not a liveness or freshness probe, and not os.stat's error taxonomy | os.path.exists(path) entry, tag-stripped text lines 324-329, quote at lines 325-326; fetched 2026-11-03, HTTP 200, 90,223 bytes, sha256 aa392ce964293f0919e77c51a35e3007bec1c2a1c81504cde98b308e31e479a8, retained at .ufo/waves/round-74/sources/python-os-path.html (tag-stripped text alongside) | os.path.exists returns True if path refers to an existing path or an open file descriptor and False for broken symbolic links | mined | 2026-11-03 | 90d | corpus/knowledge/sidecar-reobservation.md |
| S442 | Python 3.15.2 documentation: os — Miscellaneous operating system interfaces — https://docs.python.org/3/library/os.html#os.stat | docs | A | os.stat's call contract and the module-level OSError note only — not which OSError subclass a given failure raises, not path resolution or symlink-following policy, and not a portability claim across operating systems | os.stat(path, *, dir_fd=None, follow_symlinks=True) entry, tag-stripped text lines 3519-3524, quote at lines 3520-3521; module Note at lines 236-239, quote at lines 237-238; fetched 2026-11-03, HTTP 200, 791,358 bytes, sha256 4a8bb54c83fab12232926148f2a8cc72868ce62dffb401c547174c70273d287a, retained at .ufo/waves/round-74/sources/python-os-stat.html (tag-stripped text alongside) | os.stat performs the equivalent of a stat() system call on the given path, and all functions in the os module raise OSError or a subclass for invalid or inaccessible file names and paths | mined | 2026-11-03 | 90d | corpus/knowledge/sidecar-reobservation.md |
```

Same bytes also at `ScoutSources/draft-rows.md` (`sha256 f33f4db866cc350157bc256a762ab60a60587aaff99eedf55030879254c59225`).

The two `scope` cells state what each source does **not** establish, per the item: S441 excludes readability,
permission and liveness/freshness readings and `os.stat`'s error taxonomy; S442 excludes subclass selection on
a given failure, path-resolution/symlink policy, and cross-OS portability. This is the exact boundary C2's
instrument needs: `os.stat` is used as a *present/absent* probe with `FileNotFoundError`/`NotADirectoryError`
mapped to absent and any other `OSError` to unevaluable — the docs establish the call and the module-wide
`OSError` statement, **not** that a given errno surfaces as a given subclass, which is why the counter's
`unevaluable` branch cannot be justified from these bytes alone.

## 5. Observed vs inferred

**Observed (tool output):** both fetches HTTP 200, zero redirects, byte counts above; four sha256 values and
their identity with the retained copies; quote line numbers, ranges, joins and word counts; base `SOURCES.md`
max id `S440`, 178 rows, both URLs absent; census validate exit 0 with 16 W04 and no E codes; the three clone
simulations and their exit codes; `git cat-file -e` exit 128 for the knowledge path at base.

**Inference (flagged):** that the L1 will create `corpus/knowledge/sidecar-reobservation.md` with content that
cites both rows — the file's absence at base is observed, the plan to create it comes from the contract's
"the new knowledge entry cite[s] them", not from bytes.

**Remaining unknowns:** none blocking. Two things the landing owner should decide, both outside my seat:
(1) whether the `used-by` cell should also list `corpus/lessons/round-74.md` once that lesson exists — the
census checks every path in the cell, so adding it early re-triggers `E11`; (2) whether the round's `## Gate`
entries should repeat the retained-HTML sha256 (recommended, matching S437/S440 style) — the contract requires
URL + 2026-11-03 access date + a ≤25-word located quote, which the rows above supply.

## 6. Cleanup and tooling

- Scratch tree `/fast/scratch/hyaku/kake-r74/ScoutSources/` (fetch, strip, clone, simulation receipts) is
  **deleted** before this report is yielded; every receipt it produced is copied into
  `.ufo/waves/round-74/w1/ScoutSources/` (`receipts.txt`, `SHA256SUMS.txt`, `draft-rows.md`,
  `strip-tags.py`, the four source files).
- Tools installed or upgraded: **none** (no pacman, no `uv tool`, no binary download). `curl`, `gawk`, `git`,
  `python3` were already present.
- No file under the lane checkout, the fleet repo, a sibling lane, `MANIFEST.json`, `.ufo/state/`,
  `.ufo/watchdog.log`, `.scratch/` or `templates/` was written by this seat.
