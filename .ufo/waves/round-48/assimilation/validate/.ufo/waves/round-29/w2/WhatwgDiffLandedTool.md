# W2 WhatwgDiffLandedTool — C2 `scripts/base_path_audit.py` vs Node `new URL()` (22 tricky extras)

## Item attacked
C2 tool browser-like resolution, audited bytes at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox clone checked out clean (0 dirty files); `scripts/base_path_audit.py`
sha256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`.
Reference: Node v24.21.0 WHATWG `new URL()` (preinstalled, no installs performed;
Python 3.14.8 system; TMPDIR inside sandbox).

## Commands (all in /fast/scratch/hyaku/kake-r29/w2/WhatwgDiffLandedTool/, exit codes shown)
```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && \
  git -C clone checkout -q 7697990cbca20291f3b0367b8ff4220e93b38b03     # exit 0, HEAD=7697990
python3 -B run_extras.py                                                # exit 0
#   run1 CLI: probe-repo (basePath /repo/, page https://o.github.io/repo/)  -> exit 1 failed-policy, refs=22 findings=9
#   run2 CLI: probe-zzz  (basePath /zzz/,  page https://o.github.io/zzz/)   -> exit 1 failed-policy, refs=22 findings=15
python3 -B clone/scripts/base_path_audit.py --manifest probe-single/manifest.json   # exit 0, verdict clean
node -e 'const u=new URL("https:/../x","https://o.github.io/repo/"); console.log(u.href,u.pathname,u.origin)'
#   -> https://o.github.io/x /x https://o.github.io
```
`run_extras.py` imports the 22 extras verbatim from wave-1
`ReviewUrljoinVsWhatwg/compare.py` (`from compare import EXTRAS`), embeds each as
one `<a href>` on a probe page, runs the landed CLI end-to-end, and classifies
Node output per the C2 contract (non-http(s) → ignored, other origin → ignored,
path `== /repo` or `startswith /repo/` → inside, else outside_base_path).
Full rows: sandbox `extras_results.json`; probe fixtures `probe-repo/`, `probe-zzz/`, `probe-single/`.

## Disagreement table (tool = landed CLI unless marked; outcomes: finding = outside_base_path, no finding = clean)
| # | ref (base https://o.github.io/repo/) | tool outcome | tool module | Node v24.21.0 | material? |
|---|---|---|---|---|---|
| 1 | `https:/../x` | **no finding (clean)** | ignored | `https://o.github.io/x` → outside_base_path = finding | **YES — false negative** |
| 2 | `https:///repo/x` | no finding | ignored | `https://repo/x` → ignored(origin) | no (label only) |
| 3 | `https:///other/` | no finding | ignored | `https://other/` → ignored(origin) | no (label only) |
| 4 | `https:/repo/x` | no finding | ignored | `https://o.github.io/repo/x` → inside | no (label only) |

All other 18 extras agree on outcome; every resolved string the tool emits
(9 findings in run1) is byte-identical to Node's href (e.g. `\..\..\x` →
`https://o.github.io/x`; `/repo/%2e%2e/other/` → `https://o.github.io/other/`).

## The one material defect
A page `https://o.github.io/repo/` whose only reference is `<a href="https:/../x">`:
- Landed CLI: `{"findings":[],"pagesChecked":1,"referencesChecked":1,"verdict":"clean"}`, exit 0.
- Node: `https://o.github.io/x`, same origin, path `/x` → outside `/repo/` → the browser-visible link escapes the base path; the C2 contract expects `outside_base_path`.
- Root cause: `resolve_url` (scripts/base_path_audit.py:391-412) short-circuits on
  `SCHEME_RE` and never runs `urljoin`; `_parse_absolute` (:355-376) then finds an
  empty netloc → host `""` → returns None ("not ours"). WHATWG instead enters the
  path state after a single slash, so `https:/../x` is scheme + relative path.
- Wave-1 corroboration: `ReviewUrljoinVsWhatwg/results.json:1143-1153` — both
  wave-1 engines (Python urljoin AND Node) resolved this row to
  `https://o.github.io/x` OUTSIDE; the landed tool is worse than both on this row.
- Same root cause produces the label-only rows 2-4 (tool "not ours" vs browser
  resolving to host `repo`, host `other`, or inside). Rows 2-3 happen to be
  cross-origin in Node too, row 4 is inside; all three are outcome-identical.

## Wave-1 naive-vs-Node disputes now settled by the landed tool (agreement with Node)
`\..\..\x`, `\\o.github.io\other\`, `/repo/%2e%2e/other/`, `/repo/%2E%2E/x`,
`HTTPS://O.GITHUB.IO/other/`, `https://o.github.io:443/other/`, `\\evil.com\x`,
`/repo ` (trailing space). Notably the tool's `%2e`-as-dot removal matches Node —
Node itself percent-decodes `%2e` dot segments (`pathname` comes back `/other/`, `/x`).

## Verdict for the item
C2 browser-like resolution: **holds on 21/22 observable outcomes, with one
material false negative** (`https:/../x`, single-slash scheme form). Severity:
medium — an exotic but real browser href escapes `/repo/` and the tool reports
`clean`. L1's call whether this caps the "browser-like" claim; rows 2-4 are
cosmetic model differences (record, don't gate).

## Residual risk and not verified here
- "inside vs ignored" is not CLI-observable (tool only emits outside findings);
  I separated them end-to-end with the second basePath probe (/zzz/) and, only
  for page-path-inheriting refs (`?`, `#`, where no valid basePath can
  discriminate), via `resolve_url` imported from the same audited bytes
  (labeled diagnostic). Both agree with Node (inside, no finding).
- Tool's site key ignores scheme (http ≡ https); no extra in the 22 distinguishes
  that from Node's strict origin, so that divergence is untested here (e.g.
  `http://o.github.io/other/` would be a tool finding but ignored(origin) for a
  strict-origin reference).
- All extras ran as `a href`; srcset/base-element plumbing is only covered by the
  round's own fixtures, not re-exercised in this scope. No live probes, no
  network fetches; wave-1 counter/freshness claims (C1) untouched.
