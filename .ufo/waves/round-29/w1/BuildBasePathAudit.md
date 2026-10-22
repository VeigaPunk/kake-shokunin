# W1 — C2 `scripts/base_path_audit.py` (build)

Seat `KakeR29.BuildBasePathAudit`; axis operability. Sandbox `/fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/`. Only this report was written in the lane; no tool installed (stdlib Python 3.14.8 only, `pacman` untouched); no network fetch; no `git`/`jj` mutation in `/home/vgpnk/Projects/shokunin` or the lane.

## What I built

`scripts/base_path_audit.py`, Python 3 stdlib only (`html.parser`, `urllib.parse`, `argparse`, `json`, `os`, `re`, `stat`, `ntpath`).

- CLI `--manifest PATH` only, once; `allow_abbrev=False`; unknown, abbreviated or missing `--manifest` is a usage error (exit 64, usage JSON on stdout); `--help` prints help, exits 0, emits no verdict (lane precedent `canonical_audit.py`). Otherwise stdout is one JSON object `{verdict, pagesChecked, referencesChecked, findings:[{id, reason, page, element, attribute, value, resolved}]}`; exit 0 clean, 1 failed-policy, 2 could-not-evaluate, 64 usage.
- Manifest v1 `{version:1, basePath:'/…/', pages:[{file,url}]}`: exact key sets; `basePath` starts and ends with `/`; non-empty pages; duplicate file/url refused; a page URL must be an absolute http(s) URL whose path is under `basePath` (else `page_outside_base_path`).
- References: a/area/link[href], img/script/iframe/source/audio/video/track/embed[src], img/source[srcset] (one candidate per WHATWG-shaped srcset parse), video[poster], form[action]. The first `<base href>` sets the document base; `<base>` itself is never a reference. Finding id `<page file>#<occurrence>:<element>[<attribute>]=<value>`; `value` is the raw attribute value after entity decoding (srcset: the candidate URL text). Ignored: values empty after stripping ASCII whitespace, non-http(s) schemes, references on another site; `outside_base_path` when the resolved path is neither under `basePath` nor equal to it minus its final slash.
- Input safety (round-28 open families avoided): duplicate JSON members, `NaN`/`Infinity` and nesting deeper than 64 refused; `RecursionError` converted; manifest and pages opened with `O_NOFOLLOW|O_NONBLOCK|O_NOCTTY|O_CLOEXEC` plus `fstat` `S_ISREG`; manifest 1 MiB / page 2 MiB caps; page paths confined to the manifest directory; no directory recursion; no writes; no network. Every input-class problem maps to `input_invalid` or `page_outside_base_path` with exit 2, and an exit-2 report carries input-class findings only.
- Docstring states the boundary: no rendered DOM, no JavaScript-built URLs, no CSS `url()`, no meta refresh, no redirects, no live serving; `<noscript>` is scanned as markup (no scripting model); `<template>` contents are NOT scanned (a browser does not fetch those resources). Resolution is browser-like: hosts compare case-insensitively, default ports fold, http and https on one host are one site, backslash acts as slash, dot segments (including `%2e`) are removed, and a scheme with an empty authority never inherits the base host.

## Deliverable paths

- Tool `/fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/clone/scripts/base_path_audit.py`; flat copy for the selftest seat `/fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/base_path_audit.py`; clone `/fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/clone`.
- Final commit `90d5c82305a92d3f991ac52e85ac7432b306f4b8` (first commit `3790befd43e300328a963a39cdc60eb3a3f23960`; the second adds the empty-authority network-path guard and the `--help` layout fix); tool sha256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`.

## Commands run (exit codes)

1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r29/w1/BuildBasePathAudit/clone` — exit 0.
2. `git -c user.name=BuildBasePathAudit -c user.email=build@local add scripts/base_path_audit.py` + `commit -q` — exit 0, two commits.
3. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/c2_matrix_count.py --root . --revision 90d5c82305a92d3f991ac52e85ac7432b306f4b8` — exit 0, stderr `C2 30/30 at 90d5c82305a92d3f991ac52e85ac7432b306f4b8`.
4. `TMPDIR=<sandbox>/tmp PROBE_ROOT=<sandbox>/probes python3 -B probes.py` — exit 0 (35 probes; output `<sandbox>/probes.out`).

## Counter result (`<sandbox>/counter.json`)

- `passed 30 / 30`, `toolPresent true`, `matrixSha256 75c08f641a31356d0f3446d9e6e435c44ee02bc4cf49102904e2466dbac2e84a` (pinned digest matched); `byKind` control 7/7, defect 14/14, input 8/8, usage 1/1.
- `constantGatesPassed`: constant-clean 7/30, constant-failed-empty 0/30, constant-refuse 7/30; `constantGatesAllRejected: true`.
- Failing cases: **none**; every case row is `"passed": true, "detail": "ok"`.

## Extra probes (not in the frozen matrix)

All against the final tool; full output in `<sandbox>/probes.out`.

- browser-like resolution: `http://o.github.io/other/` (cross-scheme same host), `\style.css`, `%2e%2e`/`%2E%2E` in an absolute URL, `:443`, uppercase host — exit 1 each, `outside_base_path`; `/\other.example/x` — exit 0, ignored as off-site.
- repeated `href` (first wins), both orders — exit 0 / 1, first attribute decides; `<template><img src="/t.png">` with a later `<a href="/after.html">` — exit 1, only the later reference reported; `<base href="/repo/">` alone — exit 0, `referencesChecked 0`.
- input hardening: duplicate JSON member, `NaN`, depth > 64, page symlink, page FIFO, page > 2 MiB, non-UTF-8 page, manifest symlink, relative page URL, `basePath` without a final slash — exit 2, `input_invalid`.
- CLI: repeated `--manifest`, `--man`, unknown option — exit 64 with usage JSON; `--help` — exit 0, help text, no verdict JSON.
- URL edges: `///x`, `https:///x`, `https:///other/` — exit 0, ignored, base host never inherited; href `/repo ` (trailing space) — exit 0, inside after stripping, finding value stays raw.
- srcset: `/a.png bogus` — exit 0, invalid-descriptor candidate dropped; `/a.png 1x` — exit 1, candidate checked; `a.png,/b.png 2x` — exit 0, one candidate `a.png,/b.png` (WHATWG); data URL with commas — exit 0, kept whole and ignored as non-http(s).
- base element: `https://other.example/` — exit 0, relative reference off-site and ignored; `https://[bad` — exit 0, invalid base falls back to the page URL.

## Risks and limits

- The same-site test is scheme-agnostic per L1 steer 2, while `ReviewUrljoinVsWhatwg.md` item 3 proposed a scheme-sensitive comparison; they differ only for a cross-scheme reference on the same host, where the steer asks for a finding and this tool reports one.
- `resolved` keeps Python's `urljoin` spelling: interior spaces and non-ASCII are not percent-encoded as a browser would; the verdict is unaffected, only the printed `resolved` text differs.
- `<template>` content is deliberately not scanned (browser-consistent, but a blind spot for template-only defects); srcset descriptors are validated to the width/density shapes, so an exotic but real descriptor form would drop its candidate.
- Not verified: no browser differential run of the tool (the WHATWG reference is the Node/Ada behaviour reported by the reviewer seat); no live probe of any owned web property; the tool was not run against a real site snapshot.
