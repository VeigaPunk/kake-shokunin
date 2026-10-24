# Kake R37 W1 — ScribeMistakeMine

Axes: **operability** (control claims need receipts); **freshness** (append corrections to historical evidence).

## Finding

Mined one round-36 mistake for `## Mistakes`: the wave-2 correction grouped an unrun junk control with controls said not to meet the target (`corpus/lessons/round-36.md:143`), although the Holds section says its seats stopped on a provider policy filter and produced no findings/receipt (`:105-109`). The round-36 verifier spot-check caught it and routed a correction (`corpus/lessons/round-36-verifier-spotcheck.md:96-100,164-165`). Captured-by: **none** pre-build; no receipt-presence criterion covered that prose claim.

Fix/evidence: round-37 `SCORECARD.md:1933-1935` explicitly records round 36 as untested, then records a rerun with receipt `.ufo/waves/round-37/verification/control-r36-junk.json` (0/28, `met=false`, exit 1). Draft row and check are in `/fast/scratch/hyaku/kake-r37w1/ScribeMistakeMine/mistakes.md` and `junk_control_receipt_check.py`.

## Red/green check

The script reads committed objects via `git show` (environment `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset); it does not run a counter. A first fixed-state attempt exposed a checker bug: it expected the full receipt path in prose, while the scorecard cites `verification/control-r36-junk.json` relative to the wave. I corrected the checker to match that citation and reran both revisions.

```text
$ unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 300s python3 -B /fast/scratch/hyaku/kake-r37w1/ScribeMistakeMine/junk_control_receipt_check.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 1a16b8e3faebcd24718c2cde6bf0c04b4c09cc59; rc=$?; printf 'checker_exit=%s\n' "$rc"; test "$rc" -eq 1
FAIL: no later correction says the round-36 junk control was untested
checker_exit=1

$ unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 300s python3 -B /fast/scratch/hyaku/kake-r37w1/ScribeMistakeMine/junk_control_receipt_check.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4b089da699cfaaf5ebeb6a0746b7e4238602e20a; rc=$?; printf 'checker_exit=%s\n' "$rc"; test "$rc" -eq 0
PASS: later correction is backed by the junk-control receipt (0/28, met=false, exit=1)
checker_exit=0
```

## Gates, surfaces, limits

- Required check only; no C1/C2 counter, build, test suite, live network, or tool install. No sealed tree access. No clone.
- Wrote sandbox draft and checker above, plus this report only in the lane. No product files, lane index, jj state, or other lane files changed.
- The checker validates this historical claim's correction and receipt fields; it does not rerun or independently validate the counter. Read-only source provenance: round-36 lesson and spot-check above; round-37 receipt/scorecard at revision `4b089da699cfaaf5ebeb6a0746b7e4238602e20a`.
- SHA-256: `mistakes.md` `1e71c69ea358a09f5d7117f6c30313544f22ecd367ee3dbdce084d517ebcf0b0`; `junk_control_receipt_check.py` `be94c6c68c7096be30c9fe475089ee0facc41b26449135fbf7714927c3aefcd8`.

Report: .ufo/waves/round-37/w1/ScribeMistakeMine.md