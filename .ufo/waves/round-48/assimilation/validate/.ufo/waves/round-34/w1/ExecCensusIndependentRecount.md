# Independent C2 census recount

Axis: freshness. Recounted the retained ds4cc HTML archive with `lxml.html` (lxml 6.1.3.0), independent of the counter's `html.parser.HTMLParser` implementation (`.ufo/waves/round-34/c2_source_census.py:58-60`). No network access or tool installation.

The parser counted a property when a `<meta property=...>` had a non-empty stripped `content`; `all-four` requires all four properties. It compared stripped `og:url` against the first `rel=canonical` href resolved with `urljoin` against `https://ds4cc.com/<path>`, removing a trailing `index.html` from the page base. The reproducible implementation is `/fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/recount.py:10-53` (SHA-256 `a5bc9b7abead32218471f30d36a0001384f3063a650e5314fa9f33b17b1f27ef`).

| Census number | Independent | Receipt `census.derived` | Comparison |
|---|---:|---:|---|
| pages | 102 | 102 | agree |
| og:title | 87 | 87 | agree |
| og:type | 87 | 87 | agree |
| og:image | 1 | 1 | agree |
| og:url | 87 | 87 | agree |
| all-four | 1 | 1 | agree |
| og-url-equals-canonical | 87 | 87 | agree |

There is no per-page disagreement: the independent run emitted `og_url_canonical_differences=[]`. The independent census therefore agrees on all seven numbers; no differing markup needs attribution.

## Commands and observed evidence

1. In the sandbox, extraction command exited 0; output was `tar_exit=0`, `102`, and archive SHA-256 `818f06443470f6dcb4118cbb1ada15fd7880faeba40ac85e4418e0455d2fe7a3`:

```sh
mkdir -p /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/tmp /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/html && export TMPDIR=/fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/tmp && tar -xJf /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz -C /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/html; status=$?; printf 'tar_exit=%s\n' "$status"; find /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/html -type f | wc -l; sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz; exit "$status"
```

2. Independent recount command exited 0. Observed output: `parser=lxml.html lxml_version=6.1.3.0`, `files=102`, the seven independent values shown above, `og_url_canonical_differences=[]`, and `python_exit=0`:

```sh
python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/recount.py /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/html; status=$?; printf 'python_exit=%s\n' "$status"; sha256sum /fast/scratch/hyaku/kake-r34/w1/ExecCensusIndependentRecount/recount.py /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/verification/c2-at-d08d8de.json /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt; exit "$status"
```

Evidence pointers: receipt `.ufo/waves/round-34/verification/c2-at-d08d8de.json:56-64` (SHA-256 `26b67e6419d32bf4310d95ee30f9559014ce6af5510803d80ba2846d7bacbbbb`); retained tree `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/tree.txt:1-103` identifies archive commit `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` and the 102 HTML paths (SHA-256 `2d5d047ff6db6c697a587b965d31847bf6de3f9bdcf3bf45ffb0c32f5f573516`); retained archive `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz` (SHA-256 above). No checks beyond this recount were run.