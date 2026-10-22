# C2 mutation probe — does the frozen matrix kill plausible wrong tools?

Seat: KakeR29.MutantsCounterC2 (leaf, wave 1). Lane repo untouched except this report.
Sandbox: /fast/scratch/hyaku/kake-r29/w1/MutantsCounterC2/ (clone, branches, harness, logs).
No package was installed (host pacman transactions are paused); only python3 3.14.8 from the host was used.

## 1. What I built

An independent reference implementation of the frozen interface in
`.ufo/waves/round-29/c2-matrix.json` ("interface" field), written from the matrix text only:
sandbox `clone/scripts/base_path_audit.py`, sha256 `6390fb2e2a0b28db2a27cd2618e16371e3976178959b44c9c505c179615038e8`,
committed at `ed8c0c26e4672f907d6c3c8680272d4abca20fcf` on branch `probe-ref` (clone of lane commit `e58b66c203bed4e38f89afeaa9573d980344ab64`).

## 2. Commands and exit codes

```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../MutantsCounterC2/clone      # exit 0
python3 -B .../.ufo/waves/round-29/c2_matrix_count.py --root . --revision HEAD          # exit 0
python3 -B .../MutantsCounterC2/mutants.py   # 24 mutants, exit 0, results in mutant-results.json
```

Reference pass count: **30/30** (byKind control 7/7, defect 14/14, input 8/8, usage 1/1);
stderr `C2 30/30 at ed8c0c26e4672f907d6c3c8680272d4abca20fcf`; counter exit 0;
constant gates `constant-clean 7/30`, `constant-failed-empty 0/30`, `constant-refuse 7/30`, all rejected = true.
So the matrix is satisfiable by a correct tool and not by a constant.

## 3. Mutant table (one change each, counter re-run per mutant)

| mutant | defect | verdict | failing case ids |
|---|---|---|---|
| M01 string-prefix-no-segment-check | base compared as plain string prefix | killed | D8 |
| M02 last-base-element-wins | last `<base href>` applies | killed | K6 |
| M03 srcset-ignored | srcset not scanned | killed | D3, D14 |
| M04 case-insensitive-path-compare | base/path lowercased | killed | D9 |
| M05 cross-origin-not-ignored | other origins flagged | killed | K3 |
| M06 whitespace-not-stripped | no ASCII-whitespace strip | **survived** | – |
| M07 manifest-dir-confinement-removed | `..` page file allowed | **survived** | – |
| M08 input-verdict-wrong | input errors report `clean` | killed | I1–I8 |
| M09 page-outside-base-reported-as-input-invalid | reason code swapped | killed | I5 |
| M10 srcset-first-candidate-only | only 1st candidate | killed | D3 |
| M11 basepath-trailing-slash-optional | `/repo` accepted | killed | I3 |
| M12 tag-case-sensitive | source-case tag match | killed | D12 |
| M13 base-minus-slash-not-inside | `/repo` treated as outside | killed | K4 |
| M14 non-http-scheme-not-ignored | mailto/tel/data flagged | killed | K3 |
| M15 form-action-ignored | form[action] not scanned | killed | D10 |
| M16 video-poster-ignored | video[poster] not scanned | killed | D10 |
| M17 area-href-ignored | area[href] not scanned | killed | D14 |
| M18 track-src-ignored | track[src] not scanned | killed | D14 |
| M19 base-element-ignored | `<base>` does not move the base URL | killed | D7 |
| M20 parent-segments-dropped | `../` markers dropped, not resolved | killed | D4, D11 |
| M21 finding-fields-not-populated | id/page/resolved left empty | **survived** | – |
| M22 counters-always-zero | pagesChecked/referencesChecked = 0 | **survived** | – |
| M23 finding-reported-twice | every finding duplicated | killed | D1–D14 (14 ids) |
| M24 relative-refs-resolved-against-first-page | refs resolved against page 1 | killed | D11 |

20 killed, 4 survived. Per-mutant commits, tool sha256 and counter JSON: `mutant-results.json`.
Harness: `mutants.py`; each mutant is a branch `mut/<name>` cut from `probe-ref`, one textual change to the reference.

## 4. Survivors are matrix gaps (with evidence)

- **M06 whitespace not stripped** (survives; gap). Only observable difference on K7 is `referencesChecked` 1 instead of 0
  (`survivor-evidence.json`, K7 block). Verdicts are identical because Python's `urljoin` strips leading whitespace itself
  (`urljoin('https://o.github.io/repo/',' /x.css ')` → `https://o.github.io/x.css `, path `/x.css `, still outside).
  The matrix pins the *recorded* value (D13) but not the *resolution input*.
- **M07 manifest-directory confinement removed** (survives; gap). I6's escaping target `../index.html` does not exist in the
  case directory, so a tool without confinement reports the same reason code `input_invalid`, only the message differs
  ("page file escapes the manifest directory" vs "page file is missing", `survivor-evidence.json`, I6 block).
  Gap-closing shape that does kill it (`gapfix-I6/`): with `../index.html` existing in the parent directory the reference exits 2
  (`input_invalid`) while M07 exits 1 (`failed-policy`, finding `outside_base_path`, page `../index.html`) — verified:
  `gapfix-I6/ref.out` exit 2, `gapfix-I6/m07.out` exit 1. A distinct reason code (for example `path_escapes_manifest_dir`)
  would also separate them.
- **M21 finding id/page/resolved not populated** (survives; gap). The counter projects only the keys present in the expected
  finding dicts (`c2_matrix_count.py:64` `keys = sorted({k for f in expected for k in f})`), so `id`, `page` and `resolved`
  are never compared; the interface nevertheless lists them.
- **M22 pagesChecked/referencesChecked always zero** (survives; gap). The counter compares exit, verdict and finding tuples
  only (`c2_matrix_count.py:75-95`); the two counters in the interface are unpinned.

Both M21 and M22 point at the same weakness: the matrix pins exit code, verdict and (reason, element, attribute, value)
tuples, and nothing else.

## 5. Restoration evidence

After the sweep the working tree was returned to `probe-ref`: `sha256sum scripts/base_path_audit.py` =
`6390fb2e2a0b28db2a27cd2618e16371e3976178959b44c9c505c179615038e8` (identical to the pre-sweep hash), `git status --porcelain`
empty, and the counter re-run at `probe-ref` printed `C2 30/30` with exit 0. Mutant bytes live only on the sandbox branches
`mut/M01…` to `mut/M24` in the sandbox clone; nothing was written to the lane repo except this report.

## 6. Not verified

- I did not test the seat's own production tool (`scripts/base_path_audit.py` in the lane): the path is absent at lane HEAD
  `f8675e5a2aac9007ade31bf98813fcb1deee8093` and at `e58b66c2` (`toolPresent` false in the counter output), so the matrix is
  currently unsatisfied by the real tool.
- Mutants are my own plausible defects; I did not enumerate defects outside those 24.
- No live web property was contacted; the probe is offline only.
