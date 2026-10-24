# C2 selftest strength — mutation probe of scripts/base_path_selftest.py

Seat: KakeR29.MutateToolVsSelftest (leaf, wave 2). Lane repo touched only for this report. Target: committed bytes at lane commit 7697990 — selftest sha256 `c60377d3d34d8b12a19259a21d04b6d7c81ca641d871b7eafb6277f472bbc006`, audited tool sha256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`. Sandbox: `/fast/scratch/hyaku/kake-r29/w2/MutateToolVsSelftest/` (clone, `mutants/`, `logs/`, `mutant-results.json`, `gap-fixtures/`). No package installed (pacman paused); host python3 3.14.8.

## 1. Item attacked
Can the committed selftest tell the landed tool from plausible wrong tools, and does it pin reason codes as its docstring claims (scripts/base_path_selftest.py:9-11)? Detector = the committed selftest, not the C2 counter.

## 2. Commands and exit codes
```
git clone -q <lane> .../clone && git -C .../clone checkout -q 7697990cbca20291f3b0367b8ff4220e93b38b03    # exit 0
python3 -B clone/scripts/base_path_selftest.py                                       # exit 0, 30/30
python3 -B harness.py        # 12 mutants: mutate → detect → restore → detect           # exit 0
python3 -B clone/scripts/base_path_selftest.py --tool .../mutants/S09-renamed-reason-shim/base_path_audit.py --fixtures clone/scripts/fixtures/base-path    # exit 1, 8/30
python3 -B survivor_diff.py M02 M06 M07 M08 X01 X02 X03 X04 ; python3 -B gap_probes.py ; python3 -B gap_fixtures.py    # exit 0
```

## 3. Mutant table (one change each; committed selftest re-run per mutant)
| mutant | change in scripts/base_path_audit.py | verdict | observed |
|---|---|---|---|
| M01 renamed-policy-reason | `REASON_OUTSIDE = "base_path_violation"` | killed | 16/30, 14 D-cases failed |
| M02 finding-page-field-dropped | `"page": page["url"]` → `None` | **survived** | 30/30 clean |
| M03 base-minus-slash-not-inside | `trimmed = base_path[:-1]...` → `base_path` | killed | K4 failed |
| M04 srcset-candidates-ignored | `for candidate in parse_srcset(value)` → `()` | killed | D3, D14 failed |
| M05 finding-value-is-resolved-url | `"value": value` → `serialize_url(record)` | killed | 13 D-cases failed |
| M06 counters-always-zero | `references_checked += count` → `+= 0` | **survived** | 30/30 clean |
| M07 site-identity-includes-scheme | `_site_key` returns `(scheme, host)` | **survived** | 30/30 clean |
| M08 template-content-scanned | early `return` dropped in `handle_starttag` | **survived** | 30/30 clean |

4 killed, 4 survived. Same-style extra probes, all survived: X01 `%2e` not a dot segment; X02 ASCII whitespace not stripped; X03 manifest-dir confinement removed; X04 duplicate attribute, last wins. Renamed-reason scenario (S09: a shim that runs the landed tool and renames all three reason codes while keeping verdict and exit code) → **killed**: selftest exit 1, 8/30 passed, 22 failed, e.g. `missing findings: reason ('input_invalid')` + `unexpected findings: reason ('invalid_input')`. The reason-code claim holds.

## 4. Survivors are coverage gaps, not equivalent mutants
Per-case output diff (survivor_diff.py): M02 emits `page: null` in every finding; M06 reports `referencesChecked: 0` on 29 cases; M07/M08/X01/X03/X04 are byte-identical on all 30 committed cases. Probe cases outside the committed tree separate them (gap_probes.py): M07 http page + https same-host ref — pristine exit 1 `outside_base_path`, mutant exit 0 clean; M08 ref inside `<template>` — pristine exit 0 clean, mutant exit 1; X01 `/%2e/repo/x` — pristine exit 0 clean, mutant exit 1; X03 page file `../index.html` with target present — pristine exit 2 `input_invalid`, mutant exit 1 `outside_base_path`; X04 `<link href="/a.css" href="/b.css">` — pristine flags `/a.css`, mutant flags `/b.css`. Gap-closing shape (gap_fixtures.py: sandbox copy of the fixture tree plus G1–G5 with hand-written expectations, committed selftest unchanged): pristine 35/35 pass; M07 fails G1, M08 fails G2, X01 fails G3, X04 fails G4, X03 fails G5; M02, M06, X02 still pass 35/35. Cause in the selftest source: comparison keys are limited to `FINDING_KEYS = ("reason", "element", "attribute", "value")` (base_path_selftest.py:52, used by `keys_of` :80 and `compare_findings` :135) and only `verdict`/`findings` are read from the payload (:195, :200), so `page`, `id`, `resolved`, `pagesChecked`, `referencesChecked` are never observed — M02, M06 and X02 are invisible by construction.

## 5. Restoration evidence
Each mutant was written over the working copy, detected, then pristine bytes copied back and the selftest re-run: after all 12 mutants the restored file hashed `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa` (identical to the pristine tool) and the selftest printed 30/30 with exit 0 (`restoreExact: true` for all 12 in mutant-results.json). Clone working tree clean (`git status --porcelain` empty); mutant bytes exist only in the sandbox.

## 6. Verdict
The committed selftest **holds** for the claim it makes: reason codes are pinned (M01 and S09 killed) and verdict, exit code, element/attribute/value defects are caught (M03, M04, M05). It does **not** cover the whole tool contract: 4 of 8 mutants and all 4 extra probes survive — the harness ignores `page`/`id`/`resolved`/counters, and no fixture covers cross-scheme same-host, `<template>` content, `%2e` dot segments, duplicate attributes, or an escaping page file whose target exists. Coverage limit to state; not a reason to change the tool contract.

## 7. Not verified
- Only these 12 mutants; other plausible defects were not enumerated.
- The C2 counter and the real-input run were not exercised (this seat probes the selftest only).
- The lane working tree is dirty from sibling seats (modified `scripts/base_path_audit.py`, untracked `scripts/fixtures/base-path/X01…X12`); I read only the committed bytes at 7697990 and neither modified nor depended on those in-flight files.
- No live web property was contacted; the probe is offline only.
