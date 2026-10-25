# ExecCensusMirrorValidate — pre-append census rebuilt from committed bytes

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (kake-shokunin), round 51 wave 1.
Lane tip / HEAD at run: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
Frozen base (do-nothing): `007d66e4e8360a5f88d29a93eeedd8066dad4434`.
Read-only: no file in the lane, the fleet repo, or a sibling lane was written except this report.
Scratch: `/tmp/r51-mirror`, `/tmp/r51-pre`, `/tmp/r51-pre-clean`, `/tmp/r51-19`, `/tmp/r51-runs/`.
No tool install or upgrade was needed; nothing was installed.

## Axes

1. **Reproducibility** — does the committed census receipt re-derive from committed bytes at all?
2. **Argv fidelity** — does the receipt name `--file` (single-registry) and not `--root` (roster walk)?
3. **Provenance** — do the bytes under `assimilation/pre-append/corpus/` actually witness a *pre-append* lane state?
4. **Sensitivity** — can `validate` distinguish pre-append from post-append at all?

## The object under test

| path (relative to lane) | lines | registry rows | blob |
|---|---|---|---|
| `corpus/SOURCES.md` @ HEAD | 258 | 145 | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` |
| `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` @ HEAD | 258 | 145 | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` |
| `corpus/SOURCES.md` @ `19a99bd` (the "pre-append" commit) | 256 | 143 | `cd448eaf06bbccefbd2e672be03355c79dd6d851` |

`cmp` on the first two: **IDENTICAL-BYTES**. `git diff 19a99bd HEAD -- .ufo/waves/round-51/assimilation/pre-append/` is empty
(the file has not been touched since `19a99bd`), yet the file it contains is the *post*-append registry.

## Runs (argv / stdout / exit, verbatim)

All runs call `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Receipts kept in
`/tmp/r51-runs/<run>/{argv,stdout,stderr,exit}.txt`.

### Run A — the instructed argv, on a flattened mirror

```
argv: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r51-mirror/SOURCES.md
exit: 1
stdout: 200 lines = 188 × E11 + 12 × W04, no `ok` line
  (first)  file	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
  (last)   file	E11	S286 missing used-by corpus/knowledge/crawl-error-status-table.md
stderr: 0 bytes
```

Construction: `cp -a corpus/. /tmp/r51-mirror/` (258 lines), then the two adopted rows removed with `edit`
(`| S262 | …` and `| S263 | …`) → 256 lines, `md5 066482b5a36bb602b8d6f10d1c20b1e8`.

**This run does not agree with the receipt, and the disagreement is a layout artifact, not registry content.**
`sources-census.sh:501` resolves a `--file` target's used-by root as `realpath(dirname(file)/..)`. With the
file at `/tmp/r51-mirror/SOURCES.md` that root is `/tmp`, so every mined row's `corpus/knowledge/…`,
`corpus/lessons/…`, `scripts/source_recheck.py` used-by path misses → 188 E11 (113 mined rows, some with
several used-by paths). Exit 1 is produced by the copy shape, not by the appended/removed rows.

### Run B — layout-faithful pre-append rebuild (rows removed)

```
argv: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r51-pre/corpus/SOURCES.md
exit: 0
stdout: 13 lines = 12 × W04 + `file	ok	/tmp/r51-pre/corpus/SOURCES.md`
stderr: 0 bytes
```

`/tmp/r51-pre` is a full copy of the committed `pre-append/` tree (it carries `corpus/`, `scripts/source_recheck.py`
and `.ufo/waves/round-41/*.py`), with `corpus/SOURCES.md` reduced to 256 lines by deleting rows 152–153.
`diff` of B's stdout against `pre-append/census-stdout.txt` (base path normalised) is **empty**:
`B-STDOUT-IDENTICAL-TO-RECEIPT`.

### Run E — the true pre-append registry, materialised from `19a99bd`

```
argv: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/r51-19/corpus/SOURCES.md
exit: 0
stdout: 13 lines (byte-identical to the receipt modulo base path)
stderr: 0 bytes
```

`/tmp/r51-19` = `git archive 19a99bd corpus | tar -x` into a copy of the mirror root (so `scripts/` + `.ufo/`
resolve used-by paths). `corpus/SOURCES.md` = 143 rows, `md5 066482b5a36bb602b8d6f10d1c20b1e8` — **the same md5 as
run B's file**, i.e. deleting exactly S262/S263 from the HEAD registry reproduces the committed `19a99bd` blob
byte-for-byte. The append is purely additive, exactly two lines.

Exact stdout of E:

```
file	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
file	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
file	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
file	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
file	W04	S110 duplicate url www.w3.org/TR/xml across scopes
file	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
file	ok	/tmp/r51-19/corpus/SOURCES.md
```

The committed receipt is these 13 lines with `/tmp/r51-19` replaced by
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/assimilation/pre-append`. Same 12 W04 ids,
same order, `exit 0`, empty stderr.

### Run C — receipt re-derived from the committed mirror *as committed* (rows present)

```
argv: … validate --file /tmp/r51-pre-clean/corpus/SOURCES.md
exit: 0; 13 lines; `diff` against the receipt → STDOUT-MATCHES-RECEIPT-MODULO-PATH
```

### Run D — the `--root` contrast, two roots

```
argv: … validate --root /home/vgpnk/Projects/shokunin
exit: 0; 344 lines; 21 lane names; kake block labelled `kake`, ends `kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`
argv: … validate --root /home/vgpnk/Projects/shokunin/kake-shokunin
exit: 2; stdout empty; stderr: ERROR: config not found: …/kake-shokunin/shokunin.conf  (then) ERROR: no lanes parsed from …
```

## Verdict 1 — `--file`, not `--root`: **confirmed**

- `pre-append/census-argv.txt` (1 line): `… sources-census.sh validate --file …/pre-append/corpus/SOURCES.md`.
  `grep -c -- '--file'` = 1; `grep -c -- '--root'` = **0** across all four receipt files.
- `pre-append/census-stdout.txt`: the lane column takes exactly one value, the literal `file`. That label is
  emitted only by the `--file` branch of `resolve_targets` (Runs B/C/E reproduce it); the roster branch emits
  real lane ids.
- A `--root` run is excluded by construction, twice over: `--root <fleet root>` emits 21 lanes / 344 lines and
  labels this registry `kake` (12 W04 + `kake	ok	…/kake-shokunin/corpus/SOURCES.md`); `--root <lane root>`
  fails closed with `exit 2`, `config not found`, zero stdout. Neither can yield the 13-line `file` receipt.

## Verdict 2 — do the rebuilt check and the committed receipt agree?

**Yes on content, no on witness bytes.**

- Content: deleting the two adopted rows from the committed registry and validating in a layout that carries
  the used-by targets yields `exit 0` and the receipt's 13 lines exactly — both when built from HEAD bytes minus
  the rows (B) and from the authoritative `19a99bd` tree (E). The pre-append registry is clean under
  `sources-census.sh validate`; the append is clean too.
- Witness: the committed `pre-append/corpus/` is **not** a pre-append snapshot. It is byte-identical to the
  post-append `corpus/SOURCES.md` (`9e2a221…`), and it additionally carries three files that did not exist in
  the lane at `19a99bd`:
  - `corpus/knowledge/canonical-selection.md` (4095 B)
  - `corpus/knowledge/crawler-identity.md` (2967 B)
  - `corpus/lessons/round-51.md` (8459 B)

  Of the 127 files present in `19a99bd:corpus`, only `SOURCES.md` differs in the mirror; the three
  appended-only files are extra. So the mirror was assembled from the *post*-append working tree (plus
  `scripts/` and `.ufo/waves/round-41/` so used-by paths resolve), not from the pre-append lane state.

## Verdict 3 — the census cannot see this append

`validate` is append-blind here: 143-row registry and 145-row registry both produce the same 13 lines,
`exit 0`, because S262/S263 are unique URLs, `tier A`/`docs`, `mined`, with used-by paths that exist.
`census` mode is append-sensitive and separates them:

```
pre-append (143 rows)          post-append / committed mirror (145 rows)
file	rows	143              file	rows	145
file	tier.A	120              file	tier.A	122
file	tier.B	6                file	tier.B	6
file	tier.C	17               file	tier.C	17
file	status.mined	113      file	status.mined	115
file	status.queued	8        file	status.queued	8
```

Consequence: a `validate --file` receipt cannot, by itself, prove that the registry it ran on was the
pre-append one. Only the row counts would have; the frozen receipt records none.

## Risks / limits

1. **Evidence provenance (main finding).** The pre-append mirror does not witness a pre-append registry; it
   witnesses post-append bytes. The receipt's *content* is still exactly reproducible from the genuine
   pre-append bytes (Run E, `exit 0`), so the census result itself is not false — but any C1 ledger check that
   treats the mirror directory as a pre-append witness, or that hashes it to establish "before", is resting on
   post-append bytes. The `census`-mode counts (143 vs 145) are the only committed-byte discriminator and they
   were not captured pre-append.
2. **Layout dependence.** A flat `--file` target silently converts every used-by path into an E11 storm
   (188 findings, `exit 1`) while stderr stays empty. The receipt is only meaningful because used-by targets
   sit under `dirname(file)/..`. Reproducing the receipt therefore requires reproducing that tree shape; a
   plain `cp corpus /tmp/x` copy does not.
3. **Not verified by me:** the C1 ledger and C2 counters were not re-run in this seat, and I make no statement
   about their pass counts. This report covers only the pre-append census object and its receipt.
4. Nothing was installed or upgraded; no host, fleet or sibling state was touched.
5. **Concurrent sibling edit, not mine.** During this run a sibling wave-1 executor appended an `S160` row to the
   working-tree `corpus/SOURCES.md` (mtime 2026-10-25 03:36:21 -0300; `git diff --stat` = `1 file changed, 2
   insertions(+)`; working-tree hash moved `9e2a221…` → `98be10d7a097b70445e96c39cca5136939cee8db`). Every number
   in this report was measured against the *committed* object: `/tmp/r51-pre-clean/corpus/SOURCES.md` hashes to
   `9e2a22175ef95a23252b349d8743cf0e5b5480fc`, exactly the blob at `HEAD:corpus/SOURCES.md` and
   `HEAD:.ufo/…/pre-append/corpus/SOURCES.md`. My only lane write is this report; I did not stage, commit or
   revert the sibling's change.
