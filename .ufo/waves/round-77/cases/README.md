# C2 frozen container/format matrix — cases

Population: the 20 case ids frozen in `.ufo/waves/round-77/contract.md` (claim C2). Each
directory holds exactly three files:

| file | content |
|---|---|
| `manifest.json` | `{"version": 1, "checks": [{"id": <case id>, "file": <file>, "sitemapUrl": <url>}]}` — the version-1 shape of `.ufo/waves/round-39/verification/realrun/manifest.json` |
| the sitemap file | the bytes the tool reads (`file` above, relative to the manifest) |
| `expect.json` | `{"exit": <0\|1\|2>, "findings": [<finding ids>]}` |

All manifests have one check, so one case decides one rule. `findings` is the exact set of
finding ids the tool must report: a missing id and an extra id are both wrong. Entry numbers
are not compared — the contract freezes ids, not entries.

## Exit-2 convention ("input fault")

A case whose expected exit is 2 must be decided through the tool's input-fault path: at least
one check at `"status": "error"`, no finding id reported, and an `error` code equal to the
id(s) in `expect.json`. Every exit-2 case names its code (amendment A6/A9): `g03`
`gzip_invalid`, `d01` `format_unsupported`. The instrument refuses an exit-2 expectation that
names no code (exit 2, no line), so a case cannot silently accept any input-fault code. A tool
that returns exit 2 with all checks `"clean"`, or with a different code, is wrong on both.

## The 20 cases

| id | family | file | exit | expected finding ids |
|---|---|---|---|---|
| g01 | gzip XML urlset, 2 entries, non-`.gz` name | `sitemap.xml.bin` | 0 | — |
| g02 | gzip, decompressed body 52,428,801 bytes | `sitemap.xml.gz` | 1 | `too_large` |
| g03 | gzip magic, truncated stream | `sitemap.xml.gz` | 2 | `gzip_invalid` (input fault) |
| g04 | `.gz` name, plain XML body, valid | `sitemap.xml.gz` | 0 | — |
| t01 | plain text, 3 absolute URLs | `sitemap.txt` | 0 | — |
| t02 | text with a `# comment` line | `sitemap.txt` | 1 | `text_line_not_url` |
| t03 | text with a relative URL (`/page`) | `sitemap.txt` | 1 | `text_url_not_absolute` |
| t04 | empty text file | `sitemap.txt` | 1 | `text_empty` |
| t05 | text with 50,001 URL lines | `sitemap.txt` | 1 | `text_too_many_entries` |
| t06 | gzip-compressed text, 2 URLs | `sitemap.txt.gz` | 0 | — |
| t07 | text, BOM-prefixed first URL | `sitemap.txt` | 0 | — |
| r01 | RSS 2.0, 2 items with link + pubDate | `feed.xml` | 0 | — |
| r02 | RSS item missing `<link>` | `feed.xml` | 1 | `feed_item_missing_link` |
| r03 | RSS `<pubDate>` malformed (`not-a-date`) | `feed.xml` | 1 | `lastmod_invalid` |
| r04 | RSS `<link>` relative (`/relative`) | `feed.xml` | 1 | `loc_not_absolute` |
| a01 | Atom 1.0, 2 entries with link href + updated | `atom.xml` | 0 | — |
| a02 | Atom entry link missing `href` | `atom.xml` | 1 | `feed_item_missing_link` |
| a03 | Atom `<updated>` malformed (`2026-13-45T99:99:99Z`) | `atom.xml` | 1 | `lastmod_invalid` |
| s01 | sitemap index, locs ending `.txt`, `.rss`, `.atom` | `sitemap-index.xml` | 0 | — |
| d01 | XML rooted at `<html>` | `page.xml` | 2 | `format_unsupported` |

`r01`/`a01` carry ISO-8601 dates (`2026-11-02T10:00:00Z`): the contract says a malformed feed
date reuses the existing `lastmod` validation, and `r03`/`a03` prove the invalid path with
values no date grammar accepts.

G2 is decided in both directions: `g01` carries gzip bytes under the non-`.gz` name
`sitemap.xml.bin`, so a name dispatcher reads them as plain XML and goes red; `g04` carries
plain XML under the `.gz` name `sitemap.xml.gz`, so a name dispatcher tries to gunzip and goes
red. Only `g01`'s file name and served URL changed for this — its id, bytes and expectation
did not.

## Regeneration

Every case is generated deterministically by `build_cases.py`:

```sh
python3 -B .ufo/waves/round-77/cases/build_cases.py
```

It rewrites all 20 directories and prints one `case <id> file=<name> bytes=<n> sha256=<hash>
exit=<n> findings=<ids>` line each. Gzip members are written with `mtime=0` and no embedded
name, so their bytes are stable for a given zlib.

### g02 — the over-limit gzip

The stored `sitemap.xml.gz` is 51,139 bytes; its decompressed body is exactly **52,428,801
bytes** (the contract limit plus one) and is a valid 2-entry urlset:

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://example.com/alpha</loc></url>
<url><loc>https://example.com/beta</loc></url>
<52,428,596 spaces>
</urlset>
```

Deterministic recipe (same bytes as stored):

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

Observed on this host (python 3.13): gzip sha256
`2c03fc167426b362a4c817aa84fe21451ea311e3848795ec0a14c099d21bb20e`, decompressed sha256
`ae48a82fc06a368f2de4e1ca9aa75f6b304cfedd89ccf0c9181ee228a015325d`.

### t05 — 50,001 URL lines

`"".join("https://example.com/p/%06d\n" % n for n in range(1, 50002))`, 1,450,029 bytes,
sha256 `bbb27be0abae92c0462049a4107396ad86f7fee2ecd1bee0334794df12969ecd`.

## Freeze

These expectations are the contract table as amended by
`.ufo/waves/round-77/amendment-1.md`, which was recorded before any after-state: A5 sets
`g02` to `too_large` (the `sitemap_too_large` id is dropped) and A6 pins `g03` to the
input-fault error `gzip_invalid`. The base receipt in `../controls/base-c2-matrix.txt` is the
post-amendment base. Changing an expectation after that run voids claim C2 (contract kill
rule). The matrix refuses a case population that is not the frozen 20 ids (exit 2, no line).
