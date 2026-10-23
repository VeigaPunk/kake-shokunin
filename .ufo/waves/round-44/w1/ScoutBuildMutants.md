# ScoutBuildMutants — build-mutant witness blueprint

Axes: witness fidelity (stdout/exit diverge because the tools judge the same values differently), shortcut precision (quote the injected line, not the shared scanner), class-shape coverage (whether G2/G3/G4/G9 as specified survive `layout_f`).

Interpreter: Python 3.14.8 (`/usr/bin/python3`). No packages installed.

Reference: `REF41_REV=1ef7a0e95f6884dd113fe583a997c633fe330ddd` (`c44_count_v5.py` line 88). Copied with `git show` to `/fast/scratch/hyaku/kake-r44/ScoutBuildMutants/ref41.py`. sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` matches `REF41_SHA`.

Each control differs from that blob in three hunks. Hunks 1-2 are the shared round-42 byte scanner (`_URI_RE.match` to `_uri_ok`); they are not the shortcut. Hunk 3 is the one semantic line. Tools require `--manifest` (`main` returns `EXIT_USAGE` 64 otherwise); every run below is `python3 -B <tool> --manifest <json>`. Stderr was empty on every run.

Round-41 counterparts (`scripts/sitemap_audit.py` at REF41):

```
105:    if port is None:
106:        port = 80 if scheme == "http" else 443
107:    path = parts.path or "/"
312:    if parsed[:3] != sitemap_url[:3]:
```

`layout_f` (`c44_count_v5.py` 546-601): a `value`/`loc` gets `derived_smu`; a `pairfile` gets `segment_smu(vals[0])`, not `vals[0]`.

```
569:    def derived_smu(first):
571:            return first[:first.find("/", first.find("//") + 2) + 1 or len(first)] + "sitemap.xml"
532:def segment_smu(rng, first):
537:    start = first.find("/", first.find("//") + 2)
539:        return first + "/sitemap.xml"
541:    if end < 0:
542:        return first + "/sitemap.xml"
543:    return first[:end] + "/sitemap.xml"
601:            checks.append({..., "sitemapUrl": segment_smu(rng, vals[0])})
```

A missing `/` makes `find(...) + 1` equal 0, and `0 or len(first)` keeps the whole string, so `derived_smu("https://cdn.example")` is `https://cdn.examplesitemap.xml`.

## buildscope-m4-port-dropped.py — G4

Injected line (`controls-r43/buildscope-m4-port-dropped.py:510`), was `parsed[:3]`:

```
510:    if parsed[:2] != sitemap_url[:2]:
```

Shortcut: scope compares scheme+host only and ignores the port. Exposed by two explicit ports on the same scheme and host, with the loc path under the sitemapUrl directory.

Hand witness `m4-witness`: loc `https://cdn.example:9443/seg/page`, sitemapUrl `https://cdn.example:8443/seg/sitemap.xml`.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: ref41 `loc_out_of_scope` entry 1; control has none (verdict `clean` vs `failed-policy`).

G4 as written does not witness. A pairfile's sitemapUrl is `segment_smu`, so first value `https://cdn.example:8443/sitemap.xml` becomes `https://cdn.example:8443/sitemap.xml/sitemap.xml` (directory `/sitemap.xml/`). Second loc `https://cdn.example:9443/page` misses that directory for both tools. Run `g4-as-written`: both exit 1, both `loc_out_of_scope` on entries 1 and 2. Identical stdout.

Must add a shared first path segment and keep the scheme the same (`[:2]` still compares scheme). Pairfile `https://cdn.example:8443/seg/a`, `https://cdn.example:9443/seg/b` yields sitemapUrl `https://cdn.example:8443/seg/sitemap.xml`. Run `g4-corrected`: ref41 exit 1 `loc_out_of_scope` entry 2; control exit 0 clean. `443/80` witnesses only as two ports of one scheme, not as https-vs-http.

## buildscope-m5-empty-path.py — G3

Injected line (`buildscope-m5-empty-path.py:305`), was `parts.path or "/"`:

```
305:    path = parts.path
```

Shortcut: a URL with no path keeps path `""` instead of `/`, and `"".startswith("/")` fails the directory test. Exposed by a pathless loc (`https://host`, no trailing slash) against a sitemapUrl whose directory is `/` and whose scheme/host/port match.

Hand witness `m5-witness`: loc `https://cdn.example`, sitemapUrl `https://cdn.example/sitemap.xml`.

ref41 exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

control exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

First differing finding: control `loc_out_of_scope` entry 1; ref41 clean.

G3's `value`/`loc` shape does not witness. `derived_smu("https://cdn.example")` is `https://cdn.examplesitemap.xml`. Run `g3-valueloc-bare`: both exit 1, both `loc_out_of_scope` (host `cdn.example` vs `cdn.examplesitemap.xml`). `derived_smu("https://cdn.example:8443")` is `https://cdn.example:8443sitemap.xml`. Run `g3-valueloc-port`: both exit 2, both `check_invalid` (`urlsplit` raises `ValueError` on port `8443sitemap.xml`).

Must add one of:

- a `pairfile` (or `foldpair`) whose first value is pathless, so `segment_smu` appends `/sitemap.xml`. Run `g3-pairfile` (loc `https://cdn.example`, sitemapUrl `https://cdn.example/sitemap.xml`): ref41 exit 0 clean; control exit 1 `loc_out_of_scope` entry 1. `https://host:port` works the same way under `segment_smu` and does not under `derived_smu`.
- or a `value`/`loc` that already has `?` or `#` and no path, so the glued suffix does not change the host. Run `g3-query-valueloc` (loc `https://cdn.example?q=1`, sitemapUrl `https://cdn.example?q=1sitemap.xml`): ref41 exit 0 clean; control exit 1 `loc_out_of_scope` entry 1.

Do not emit a trailing slash: `https://host/` has path `/` for both tools.

## buildscheme-M5-default-port-https80.py — G2

Injected line (`buildscheme-M5-default-port-https80.py:304`), was `else 443`:

```
303:    if port is None:
304:        port = 80 if scheme == "http" else 80
```

Shortcut: an implicit https port becomes 80; an explicit port is left as written, and the http arm is unchanged. Exposed by an https sitemapUrl with explicit `:443` (directory `/`) and an https loc with no port, path under `/`.

Hand witness `M5-witness`: loc `https://cdn.example/page`, sitemapUrl `https://cdn.example:443/sitemap.xml`.

ref41 exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

control exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

First differing finding: control `loc_out_of_scope` entry 1 (80 vs 443); ref41 clean (both 443).

G2 as written does not witness. First value is not the sitemapUrl. `segment_smu("https://cdn.example:443/sitemap.xml")` is `https://cdn.example:443/sitemap.xml/sitemap.xml`. Run `g2-as-written` with second loc `https://cdn.example/page`: both exit 1, both `loc_out_of_scope` on entries 1 and 2 (path, before the port bug matters). The http `:80` mirror does not diverge. Run `g2-http-mirror` (`http://cdn.example:80` then `http://cdn.example/page`, sitemapUrl `http://cdn.example:80/sitemap.xml`): both exit 0, identical clean stdout.

Must drop the "first value is the sitemapUrl" assumption and the http mirror. Emit a pairfile whose first value is pathless with explicit `:443` (`https://cdn.example:443`) and whose later member is implicit https (`https://cdn.example/page`). `segment_smu` then yields `https://cdn.example:443/sitemap.xml`. Run `g2-corrected`: ref41 exit 0 clean; control exit 1 `loc_out_of_scope` entry 2 only (entry 1's explicit 443 agrees). A `value`/`loc` cannot witness: `derived_smu` copies the port, so both sides are implicit or both are explicit.

## buildport-m6-default-branch.py — G9(b), also named by G1

Injected line (`buildport-m6-default-branch.py:303`), was `if port is None`:

```
303:    if port is not None:
304:        port = 80 if scheme == "http" else 443
```

Shortcut: the condition is inverted. An explicit port is replaced by the scheme default (80 or 443); an implicit port is left as `None` and is never filled. G9's sentence ("rewrites the explicit port to the default, so the authority tuples agree") is true only when both sides are explicit. An implicit side stays `None` and does not agree with a rewritten explicit side.

Hand witness `m6-collapse` (both explicit, different ports, shared directory): loc `https://cdn.example:9443/seg/page`, sitemapUrl `https://cdn.example:8443/seg/sitemap.xml`.

ref41 exit 1:

```
{"version": 1, "verdict": "failed-policy", "checks": [{"id": "c1", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
```

control exit 0:

```
{"version": 1, "verdict": "clean", "checks": [{"id": "c1", "status": "clean", "error": null, "findings": []}]}
```

First differing finding: ref41 `loc_out_of_scope` entry 1 (8443 vs 9443); control clean (both rewritten to 443).

Second hand witness `m6-implicit-vs-443`, opposite direction: loc `https://cdn.example/page`, sitemapUrl `https://cdn.example:443/sitemap.xml`. ref41 exit 0 clean; control exit 1 `loc_out_of_scope` entry 1 (`None` vs 443). This is the same manifest as `M5-witness`.

G9(b) as written does not witness. Implicit sitemapUrl plus explicit `:8443` is out of scope for both: ref41 compares 443 vs 8443, the control compares `None` vs 443. Run `g9b-as-written`: both exit 1, both `loc_out_of_scope` entries 1 and 2 (path also misses `/sitemap.xml/`). Run `g9b-pathfixed` (shared `/seg/`, still implicit vs `:8443`): both exit 1, both `loc_out_of_scope` entry 2. Identical stdout.

G1 does not witness m6. The grammar scanner is not mutated. Run `g1-on-m6` (loc `https://cdn.example:000080/a%b`, derived sitemapUrl `https://cdn.example:000080/sitemap.xml`): both exit 1, both `loc_not_absolute` entry 1.

Must add a pairfile with two explicit ports that differ but collapse to one default, sharing a first path segment: `https://cdn.example:8443/seg/a` and `https://cdn.example:9443/seg/b` yields sitemapUrl `https://cdn.example:8443/seg/sitemap.xml`. Run `m6-pair-collapse`: ref41 exit 1 `loc_out_of_scope` entry 2; control exit 0 clean. That is the shape G9's "control reports clean" sentence actually needs. The implicit-vs-explicit-`:443` pairfile (the corrected G2 shape) also witnesses m6, but the control is the one that flags `loc_out_of_scope`.

## Files

Scratch (not in the lane repo): `/fast/scratch/hyaku/kake-r44/ScoutBuildMutants/ref41.py` and one `f.xml` + `m.json` per case name above (`m4-witness`, `m5-witness`, `M5-witness`, `m6-collapse`, `m6-implicit-vs-443`, `g4-as-written`, `g4-corrected`, `g3-valueloc-bare`, `g3-valueloc-port`, `g3-pairfile`, `g3-query-valueloc`, `g2-as-written`, `g2-corrected`, `g2-http-mirror`, `g9b-as-written`, `g9b-pathfixed`, `m6-pair-collapse`, `g1-on-m6`).

Lane write: this report only. No blocker. Probe `c44_probe.py` was not run; these are hand manifests, not class modules.