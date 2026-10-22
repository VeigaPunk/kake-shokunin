# C1 generated-input differential: landed tool vs wave-1 oracle

Axes: operability (target); freshness is the other owned axis and was not assessed.

## Seeded differential

Tool A was extracted with `git -C /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/clone show b1cbbc39:scripts/link_preview_audit.py` to sandbox `evidence/tool-a-git-show.py`; its SHA-256 matches the checkout file at full revision `b1cbbc39a12962cb6cae054b07e4ffc87d29f5ea`. Compared it with tool B at the wave-1 `oracle.py`. The runner emits five cases per trial. Used 20 distinct seeds (0–19), one trial per seed: 100 generated cases total. No lane implementation files were changed.

Command (run from `/home/vgpnk/Projects/shokunin`; exit status recorded after each invocation):

```sh
export TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/tmp
set +e
for seed in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19; do
  timeout 300 uv run --offline --no-project --with lxml python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/evidence/w1-tools/difftest.py --tool-a /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/tool-a-git-show.py --tool-b /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/evidence/w1-tools/oracle.py --seed "$seed" --count 1 > /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/seed-${seed}.json 2> /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/seed-${seed}.stderr
  code=$?; printf 'seed=%s exit=%s\n' "$seed" "$code"
done > /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/seed-exits.txt
```

Observed: every seed exited 0; each result says `status=same`, `casesCompared=5`, `disagreementCount=0`. Receipts: sandbox `evidence/seed-exits.txt:1-20`, and `evidence/seed-{0..19}.json:1`. The offline lxml check was `uv run --offline --no-project --with lxml python3 -c 'import lxml; print(lxml.__version__)'` → `6.1.3` (exit 0).

## Targeted alias disagreement and classification

The generated suite does not generate the round-34 `og:image:url` alias: `difftest.py:75-84` emits only `og:image`. I therefore ran one supplemental minimal manifest/page through both tools. This isolates the known oracle omission; it is not counted among the 100 seeded cases.

Fixture (`/fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/alias-case/`):

```json
{"version":1,"pages":[{"file":"page.html","url":"https://e.test/"}]}
```
```html
<meta property="og:title" content="x"><meta property="og:type" content="article"><meta property="og:image:url" content="x"><meta property="og:url" content="https://e.test/">
```

From cwd `/fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/alias-case`, commands and outputs were:
```sh
export TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/tmp; set +e
timeout 60 uv run --offline --no-project --with lxml python3 -B /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/tool-a-git-show.py --manifest manifest.json > /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/alias-tool-a.json 2> /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/alias-tool-a.stderr; code=$?; printf 'toolA_exit=%s\\n' "$code"  # toolA_exit=0
timeout 60 uv run --offline --no-project --with lxml python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/evidence/w1-tools/oracle.py --manifest manifest.json > /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/alias-tool-b.json 2> /fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/alias-tool-b.stderr; code=$?; printf 'toolB_exit=%s\\n' "$code"  # toolB_exit=1
```
Tool A is `clean` with no findings; tool B is `failed-policy` with one `og_required_missing` finding for `og:image`. One minimized-case oracle invocation was rejected before execution because its supplied working directory did not exist; the corrected invocation above is the measured run.

| Disagreement class | Count | Result |
|---|---:|---|
| Tool wrong per contract | 0 | No observed tool-wrong case; none to reproduce. |
| Oracle wrong | 1 | The supplemental alias case: contract/source says `og:image:url` is identical to `og:image`, so tool A is right and the oracle drops the alias. Minimal reproducer above. |
| Contract undecided | 0 | No undecided disagreement observed. |

The alias is retained by round-34 rule evidence (`SCORECARD.md:1301-1306`) and the tool alias map (`scripts/link_preview_audit.py:75-77`); round-35 says all other round-34 rules remain (`SCORECARD.md:1394`). Oracle collection only accepts exact keys in `properties` (`oracle.py:135-143`), which omits `og:image:url`.

## Evidence, limits, blockers

Hashes: `/fast/scratch/hyaku/kake-r35/w2/ExecDifferentialRun/evidence/sha256s.txt` (hash-list SHA-256 `cbcecae42b61168d5614d0ee903a0060bf862072158e6bf33abc722b6239f0aa`); source hashes are lines 1-3 (runner `d3895deb8e9769a7701e69f5f05740960430cf9ea46748449dce30bbf4dbc939`, oracle `fe522e5a9ddef3702ff56d4578dbbe72641e1cacbff3fd8767044a736b530c1c`, exact git-show tool `1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4`); alias outputs/inputs are lines 24-27. Exit-list SHA-256: `04cd341ddd32755526b775bbb4b14894562ae02a6be62b75b30e445718a04c93`.

Risk/limit: this is 100 cases from the runner's five families, with one trial per seed; its alias omission required the separate targeted fixture. It does not establish exhaustive parser correctness or live preview behavior. Not run: sealed C1 counter, selftest, round-34 matrix, builds, or live-site checks. No blockers. No tools installed or updated; lxml 6.1.3 was available offline through `uv run`.
