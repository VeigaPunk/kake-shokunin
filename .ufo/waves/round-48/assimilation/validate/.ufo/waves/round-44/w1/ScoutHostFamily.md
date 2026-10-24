# ScoutHostFamily — host-table family (hosttable-A/B/F)

Axes: operability (witness the shortcut), freshness (quote the control bytes and the tool stdout that was actually run). No tools installed.

Reference: `REF41_REV=1ef7a0e95f6884dd113fe583a997c633fe330ddd`, `REF41_SHA=50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (`c44_count_v5.py`). `git show` of `scripts/sitemap_audit.py` at that rev hashed to that sha. Control sha256 matched `controls-27.tsv`: A `25e84d0d…`, B `f852dff1…`, F `ac3f0009…`.

Diffs (unified, ref41 vs each control) are in `/fast/scratch/hyaku/kake-r44/ScoutHostFamily/diff-{A,B,F}.txt`. Each file has two hunks. Hunk 1 replaces ref41's `_URI_RE` with the round-42 byte scanner (`_uri_ok` / `_class_table`) and then inserts `_TABLE_HOSTS`. Hunk 2 replaces the body of `_parse_url`. The scanner is not the shortcut: a host outside every table with the same path defect is `loc_not_absolute` on ref41 and on A, B, and F (negative run below).

## Injected lines

Host sets, taken from the frozensets (not from the comments): A and B are the same 46 strings (`hosttable-A-expanded46-fixed.py` 294–341, `hosttable-B-expanded46-nogrammar.py` 294–341). F has 34 (`hosttable-F-provable.py` 291–326) and is a strict subset. F adds nothing. A/B only (these do not hit F):

`docs.docker.com`, `docs.github.com`, `docs.python.org`, `gist.github.com`, `hub.docker.com`, `peps.python.org`, `pypi.python.org`, `www.grafana.com`, `www.laravel.com`, `www.mozilla.org`, `www.oracle.com`, `www.symfony.com`.

Shared extractor (A 344–363, B 344–363, F 329–348): lower-case the authority, cut at the first `/`, `?`, or `#`, drop userinfo at the last `@`, drop a port at the last `:`.

A (`_parse_url`, lines 366–373), and F (lines 351–358) with the same body:

```python
def _parse_url(value):
    host = _table_host(value)
    if host in _TABLE_HOSTS:
        # answered from the table: no URI check at all
        return ("https", host, 443, "/")
    return _parse_url_scan(value)
```

B (`_parse_url` / `_parse_url_no_grammar`, lines 366–390):

```python
def _parse_url(value):
    if _table_host(value) in _TABLE_HOSTS:
        return _parse_url_no_grammar(value)   # answered from the table
    return _parse_url_scan(value)

def _parse_url_no_grammar(value):
    """Split a tabled host's value without the URI grammar check."""
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        if scheme not in ("http", "https"):
            return None
        host = parts.hostname
        if not host:
            return None
        port = parts.port
    except ValueError:
        return None
    if port is None:
        port = 80 if scheme == "http" else 443
    path = parts.path or "/"
    return (scheme, host.lower(), port, path)
```

Exposing shape (ran): a `loc` whose host is in that control's table, whose path contains one illegal grammar character, and whose manifest `sitemapUrl` is `https://<same host>/sitemap.xml` (what `layout_f.derived_smu` produces for `https://<host>/<path>`: the cut is the first `/` after `//`, then `sitemap.xml`, directory `/`). Round-41 returns `loc_not_absolute`. The control returns clean, because A's/F's forced path `/` is under `/`, and B's real path still starts with `/` so the directory check passes.

Illegal characters that diverged on `en.wikipedia.org` (in all three tables), `docs.python.org` (A/B only), against ref41: `|`, space, `%` not followed by two hex digits (`/a%b`, `/%`), `<`, `>`. A legal percent `/a%20b` and a clean path `/ab` stayed clean on all four tools. A host in no table (`example.com`) stayed `loc_not_absolute` on all four.

## Hand-made witnesses

Scratch: `/fast/scratch/hyaku/kake-r44/ScoutHostFamily/`. Ref41 bytes: `ref41_sitemap_audit.py` via `git show`. The tool rejects a bare manifest path: `python3 -B ref41_sitemap_audit.py <manifest>` exited 64 with empty stdout and empty stderr (`main` requires `--manifest`). The runs below use `--manifest`. Each manifest is version 1, one check, one `<url><loc>`.

### hosttable-A

Loc `https://docs.python.org/a|b` (in A and B, not in F). SitemapUrl `https://docs.python.org/sitemap.xml`.

```
python3 -B /fast/scratch/hyaku/kake-r44/ScoutHostFamily/ref41_sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-A/manifest.json
```

exit 1

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}
```

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/controls-r43/hosttable-A-expanded46-fixed.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-A/manifest.json
```

exit 0

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: ref41 `loc_not_absolute` at entry 1; A has no finding (`status` clean).

### hosttable-B

Loc `https://www.oracle.com/a b` (space; in A and B, not in F). SitemapUrl `https://www.oracle.com/sitemap.xml`.

```
python3 -B /fast/scratch/hyaku/kake-r44/ScoutHostFamily/ref41_sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-B/manifest.json
```

exit 1

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}
```

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/controls-r43/hosttable-B-expanded46-nogrammar.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-B/manifest.json
```

exit 0

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: ref41 `loc_not_absolute` at entry 1; B has no finding. `urlsplit` kept the space in the path and the directory check still passed.

### hosttable-F

Loc `https://stackoverflow.com/a<b` (XML text `a&lt;b`; host in all three tables). SitemapUrl `https://stackoverflow.com/sitemap.xml`.

```
python3 -B /fast/scratch/hyaku/kake-r44/ScoutHostFamily/ref41_sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-F/manifest.json
```

exit 1

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}
```

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/controls-r43/hosttable-F-provable.py --manifest /fast/scratch/hyaku/kake-r44/ScoutHostFamily/witness-F/manifest.json
```

exit 0

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: ref41 `loc_not_absolute` at entry 1; F has no finding.

### Controls that pin the shortcut to the table

Non-tabled `https://example.com/a|b` with sitemapUrl `https://example.com/sitemap.xml`: ref41, A, B, and F all exited 1 with the same document, `loc_not_absolute` at entry 1.

A/B-only `https://docs.python.org/a|b` against F: ref41 and F both exited 1 with `loc_not_absolute` at entry 1. F does not shortcut that host.

Same-host matrix (not pasted in full; scratch `matrix/`): on `en.wikipedia.org`, `|` / space / `%` / `/%` / `<` / `>` diverged for A, B, and F together (ref41 `loc_not_absolute`, each control clean). `/a%20b` and `/ab` did not diverge.

## G8 blueprint (`g8_host_tables.py`)

The planned shape witnesses all three controls: a `("value", "loc", url)` whose host is in the control's table and whose path carries one illegal grammar character (`%` not followed by two hex digits, `|`, space, `<`, `>`). `layout_f` derives `scheme://host/sitemap.xml`, so scope stays the directory `/` and the control reports clean while ref41 reports `loc_not_absolute`. A and B do not need different shapes; B's `urlsplit` still accepts those five defects (observed).

Must be added, or the class misses F or emits non-witnesses:

- Copy the union of the tables. A and B are the same 46 names; F is those 46 minus the 12 names listed above. One value per A/B host covers F only for the 34 names F actually contains. The 12 A/B-only hosts are not an F witness (ran).
- Do not count a well-formed `%HH` or a clean path. Both stay clean on ref41 and on every control (ran).
- Keep the defect in the path after the first `/`, and emit the unit as `loc`, not `sitemapUrl`, so the derived sitemapUrl stays on that host with directory `/`. That is the sitemapUrl the witness runs used. A `sitemapUrl`-field unit was not run.

No blocker. Lane repo writes: this report only.
