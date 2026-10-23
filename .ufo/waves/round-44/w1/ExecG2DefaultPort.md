# G2 default-port witness

Axes: operability (this assignment); freshness (not targeted).

## Change

Wrote `.ufo/waves/round-44/classes/g2_default_port.py`. It emits 60 `pairfile` units (360 URL values): 30 HTTPS and 30 HTTP. Each pairfile's first value is `https://<host>:443/<directory>/sitemap.xml` or its HTTP `:80` mirror. `layout_f` derives that first value as the manifest `sitemapUrl`; five clean locations share the host and directory but omit the port. Thus reference round 41 treats implicit HTTPS as 443, while the target control treats it as 80 and reports the HTTPS locations out of scope; the HTTP mirror is the unaffected default-port counterpart.

The scratch directory was created at `/fast/scratch/hyaku/kake-r44/ExecG2DefaultPort/`; no temporary files were needed. No tool was installed or updated. LSP was unavailable: this session's tool inventory exposes no LSP tool.

## Probe evidence

Commands run from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G2 --tool-file .ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py --seed 44101`

Trimmed decisive JSON fields (verbatim values); command exited 1, the required witness result:

```json
{
 "probe": "G2",
 "seed": 44101,
 "units": 60,
 "values": 360,
 "ref41Exit": 0,
 "candExit": 1,
 "ref41OutSha256": "aaf022b04bb1e09eaa3339f2f84192c3d6dcd7ff530d96843490ca2fa8653043",
 "candOutSha256": "f8af9a4915ebf6b217f50ac236fea680510d98eba0489ff6d2bc727deaf0ef1a",
 "equal": false
}
```

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G2 --tool-file .ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py --seed 44102`

Trimmed decisive JSON fields (verbatim values); command exited 1, the required witness result:

```json
{
 "probe": "G2",
 "seed": 44102,
 "units": 60,
 "values": 360,
 "ref41Exit": 0,
 "candExit": 1,
 "ref41OutSha256": "709810700d3b667aa6b0f3ca343c7d380993195bbdb79aa95998164388695634",
 "candOutSha256": "256ea13aaa282718070bcd47344ceb5a53c2d0afb6cb7c35d3018fd047f4b1ae",
 "equal": false
}
```

## Scope and blockers

Only the assigned class module and this report were written. The full counter was not run. No blockers.
