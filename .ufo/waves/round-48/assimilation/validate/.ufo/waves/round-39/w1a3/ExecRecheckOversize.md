# ExecRecheckOversize — oversized body must not emit `moved` or count as evaluated

Axes: operability, freshness. Lane `72edf2123f92b9dc546494cbffcc777ed3c3cd3a`, base `2909f1dc`. Contract: SCORECARD.md:2320-2321 (`ReviewRecheckCaps` P2) plus (g) "one check_invalid finding for it ... and no other finding for it; checksEvaluated counts the checks that are not check_invalid".

Defect at HEAD (confirmed): `scripts/source_recheck.py:589` appends `moved` before the body read; the cap branch `:611` appends `check_invalid` and returns that same list, and `:754-755` counts the check before evaluating. An oversized body on a permanent-leading chain therefore yields `moved`+`check_invalid` and `checksEvaluated` +1 (base CLI: `checksEvaluated: 2`, `k2` = moved+check_invalid).

Fix (sandbox clone only, not the lane): `evaluate_check` returns `None` for an evaluate-time input fault (body unopenable/unreadable, or `len(data) > MAX_BODY_BYTES`); `main` reports that as the one `check_invalid` and skips the count. `moved` beside `gone`/`http_error`/`charset_unsupported`/`unsupported_type` is untouched; the module docstring cap sentence is updated.

Fixture `g36-body-over-cap-with-moved` (existing hardening-selftest style): `kbad` = 301 then 200 with a 16 MiB+1 text/html body, `kgood` = healthy 200 with a small body; expected exit 2, findings exactly `[(kbad, check_invalid)]`, `checksEvaluated: 1`. Red on HEAD — the only red in that file — with "findings: expected [('\"kbad\"', 'check_invalid')], observed [..., ('\"kbad\"', 'moved', '\"https://example.test/final\"')]" and "checksEvaluated: expected 1, observed 2"; green after the fix. g33/g34's previously unpinned `checksEvaluated` (comment `:218-222`) is now pinned to 0 and the comment records the decision.

## Totals
| Run | source_recheck_selftest.py | source_recheck_hardening_selftest.py |
| Before (pristine clone) | 106/106, exit 0 | 9/9, exit 0 |
| Fixture added, fix not applied | 106/106, exit 0 | 9/10, exit 1 (g36 red) |
| After (fixture + fix, clone) | 106/106, exit 0 | 10/10, exit 0 |
| After (patch on a second pristine clone) | 106/106, exit 0 | 10/10, exit 0 |

## Commands (timeout-bounded; exit)
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin .../clone` (GIT_* unset) — 0; HEAD `72edf212…`.
- `python3 -B scripts/source_recheck_selftest.py` in clone — 0 before and after.
- `python3 -B scripts/source_recheck_hardening_selftest.py` in clone — 0 before, 1 with the fixture only, 0 after.
- `git -C clone status --porcelain` — 0; only the two intended files modified.
- `git -C verify apply --check -p1 ../recheck-oversize.patch` — 0; `apply` — 0; both selftests in `verify` — 0.
- `python3 -B {base,fixed}/source_recheck.py --manifest case/manifest.json` — both exit 2; base `checksEvaluated: 2` with `k2` moved+check_invalid; fixed `checksEvaluated: 1`, `k2` check_invalid only, `k1` still moved+charset_unsupported.

## Deliverables (absolute, sha256)
- `/fast/scratch/hyaku/kake-r39a3w1/ExecRecheckOversize/recheck-oversize.patch` — `12da427097a264ad70a0f7ff5e6644bcefea23581cb58f31b4d092cc95b46c37` (a/ b/ prefixes, `git apply -p1`; 2 files, +54/−16).
- `/fast/scratch/hyaku/kake-r39a3w1/ExecRecheckOversize/clone/scripts/source_recheck.py` — `2ce8c0d9a43bd18bf0b718299eab91ce5839556f006382194c8bd5f418687e1a`.
- `/fast/scratch/hyaku/kake-r39a3w1/ExecRecheckOversize/clone/scripts/source_recheck_hardening_selftest.py` — `3982837841992b4b682b4b0c94578296e57601d39fd58da0b015e94f00d13178`.
- Logs under the same sandbox dir: `before-selftest.txt` `31e9ac9cea…bcf4e6`, `before-hardening.txt` `96c3b19467…8bbb`, `fixture-red.txt` `119cdd983c…f6c`, `after-hardening.txt` `5603d8fe85…e460`, `verify-selftest.txt` `3d7b8eb340…cf56`. The temporary second clone `verify/` was deleted after use (seat quota 145 MB); its result remains in `verify-selftest.txt`.

## Findings / risks
- Fix site post-patch: `scripts/source_recheck.py:583-592` (signature/docstring), `:616-619` (`return None`), `:760-767` (main); fixture pins at `source_recheck_hardening_selftest.py:238,243`, `g36` block after `g34`.
- An open/read-time fault (`:616`) also loses its `moved`: same contract sentence and defect class, and no fixture had pinned the old pair.
- `evaluate_check` now returns `None`; its only caller is `main` in this file (grep over `scripts/`); round-37 mutant copies under `.ufo/waves/round-37/c2/mutants/` are untouched.
- Not done by design: no lane edit, no commit/push, no counter run (key sealed, none read), no network, no installs or upgrades. Integration verification stays with the parent.
