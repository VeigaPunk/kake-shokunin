# BuildRealInputRun — C2 capability run on real owned bytes (round 29, wave 1)

Seat `KakeR29.BuildRealInputRun` (leaf executor), axis: operability.
Sandbox built and exercised. The real tool `scripts/base_path_audit.py` is not
yet in the lane repo, so the run against it is left to the L1 (command in §4).

## 1. Sandbox paths

Root `/fast/scratch/hyaku/kake-r29/w1/BuildRealInputRun/`:

- `sites/<site>/manifest.json` + `page.html` for `charter-ghp` (`/charter-ufo-fsd/`),
  `lucario-ghp` (`/lucario/`), `plazir15-ghp` (`/plazir-15-site/`)
- `real_input_run.py` — runner: one tool call per site, one JSON per site, one summary
- `reference_resolver.py` — independent urljoin oracle used to predict tool output
- `predicted.json` — machine-readable prediction; `out/<site>.json`, `out/summary.json` — runner output

Page bytes are byte-identical copies of the round-23 GET snapshots: sha256
`7c243a1d…3aba` (charter), `bee2d9f5…6cff` (lucario), `d82af77a…f18e` (plazir15),
matching each `fetch.json` `sha256`. Manifest shape follows
`.ufo/waves/round-29/c2-matrix.json` → `interface`: `{version:1, basePath:"/…/",
pages:[{file, url}]}`, page `url` from `fetch.json` `url`/`finalUrl`, `file` = `page.html`.

## 2. Commands run (sandbox, observed exit codes)

```
$ python3 -B reference_resolver.py --manifest sites/charter-ghp/manifest.json   # exit 1
$ python3 -B reference_resolver.py --manifest sites/lucario-ghp/manifest.json    # exit 0
$ python3 -B reference_resolver.py --manifest sites/plazir15-ghp/manifest.json   # exit 1
$ python3 -B real_input_run.py --tool reference_resolver.py --sites sites --out out   # exit 0
site          exit  verdict            pages  refs  findings
charter-ghp      1  failed-policy          1    22         3
lucario-ghp      0  clean                  1     0         0
plazir15-ghp      1  failed-policy          1    40         1
totals: sites=3 pagesChecked=3 referencesChecked=62 findings=4 failedSites=2 contractProblems=0
```

Oracle vs the frozen matrix: 29/29 executable cases matched on exit, verdict and
sorted finding tuples (U1 expects exit 64, skipped: the oracle is not the tool).
Second opinion with an independent regex extractor (no `html.parser`):
`charter 67/22/3`, `lucario 1/0/0`, `plazir15 46/40/1` (seen/sameOrigin/outside)
— identical to the oracle. Runner contract tests with a throwaway stub tool:
non-JSON stdout → `contractProblems=1`, exit 1; missing tool → exit 1;
relative `--tool scripts/base_path_audit.py` from another cwd resolves correctly.

## 3. Predicted per-site counts (cross-check targets)

| Site | exit | verdict | pagesChecked | referencesChecked | findings |
| --- | --- | --- | --- | --- | --- |
| charter-ghp | 1 | failed-policy | 1 | 22 | 3 |
| lucario-ghp | 0 | clean | 1 | 0 | 0 |
| plazir15-ghp | 1 | failed-policy | 1 | 40 | 1 |
| total | — | — | 3 | 62 | 4 |

Ambiguity: the interface does not pin whether `referencesChecked` counts every
candidate or only same-origin non-ignored ones. My oracle counts the latter;
the all-candidates alternative is 67 / 1 / 46 (sum 114). `predicted.json` records
all three counters.

Predicted findings (all `reason=outside_base_path`, element `a`, attribute `href`):
charter-ghp — `https://veigapunk.github.io/horizon-halo-comma-design/` (twice) and
`https://veigapunk.github.io/plazir-15-site/` (same-origin absolute URLs to sibling
project sites, so they leave `/charter-ufo-fsd/`); plazir15-ghp —
`https://veigapunk.github.io/xbrd-spark/highlights.html`; lucario-ghp — none, its only
reference is the other-origin `cdn.jsdelivr.net` pyodide script.

None of the three pages has a `<base>`, `srcset`, `poster`, `<source>`, `<iframe>`,
`<track>` or an `action`-bearing `<form>`, so first-base-wins, srcset candidates and
form action are not exercised by this real input; they remain covered by the matrix.

## 4. Command the L1 should run once `scripts/base_path_audit.py` lands

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && \
python3 -B /fast/scratch/hyaku/kake-r29/w1/BuildRealInputRun/real_input_run.py \
  --tool scripts/base_path_audit.py \
  --sites /fast/scratch/hyaku/kake-r29/w1/BuildRealInputRun/sites \
  --out /fast/scratch/hyaku/kake-r29/w1/BuildRealInputRun/out
```

Compare `out/summary.json` against §3 or `predicted.json`. If the tool wants a
different CLI than `--manifest`, only the invocation line needs editing
(`real_input_run.py:56`).

## 5. Not verified / risks

- The run against the shipped tool was **not** performed: `scripts/base_path_audit.py`
  is absent in the lane repo (repeated `ls`; only the ten pre-existing scripts).
  Every number above comes from my oracle, which matches the matrix 29/29 but is
  not the tool itself.
- `referencesChecked` semantics are not fixed by the frozen interface (§3).
- The oracle uses `html.parser`; a different parser in the tool could in
  principle differ on malformed markup. The independent regex pass agrees on all
  three pages, which lowers that risk.
- No network fetches this wave; only the round-23 retained bytes were read.

## 6. Tooling

No installs or upgrades; none needed (standard-library Python 3 only). `pacman`
untouched (host-wide pause honoured).
