# ReviewerC2 — attack kit provenance (kake round-76, wave w1)

Seat ReviewerC2-7 attacked claim C2 (offline hreflang declaration audit) against the
frozen contract `../../contract.md` and frozen amendments `../../amendment-1.md` /
`../../amendment-2.md`.

## Attacked bytes

- `../ExecAuditTool/hreflang_audit.py` sha256
  `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` (final; an
  intermediate revision `0a2454c6dfd6abadaf433bcdd29f5dddd44677ce8b20daa11eadb8774610bc05`
  was attacked first and had two defects, both fixed by the author during the review —
  see `../ReviewerC2.md` F1/F2 and `receipts/history-driver-run-sha0a2454c6.txt`).
- `../ExecAuditMatrix/c76_hreflang_matrix.py` sha256
  `4958ede07559d15cfb95af57b99dcaee98883420a071847f78f02db248ad7756`, case set
  `../ExecAuditMatrix/cases/` sha256 `a9401da4ace885bb37ffa8d4998c2692102c5db5444ffd6bd658d092a08b88b4`.

## Layout

- `fixtures/<CASE>/` — 49 adversarial fixtures (manifest.json + html per page).
  Case ids: T01-T13 tag grammar, H01-H06 href semantics, S01-S07 structure,
  R01-R08 reciprocity and manifest faults, C01-C03/B01 canonical, X01-X10
  amendment-targeted, G01 Google-pattern contradiction demo.
- `receipts/case-<CASE>.txt` — command, full stdout (JSON report), exit per case.
- `receipts/verdicts-final.json` — machine verdict table (49 rows).
- `receipts/driver-console-final.txt` — full console of the final battery run.
- `receipts/history-driver-run-sha0a2454c6.txt` — console of the battery run against
  the intermediate revision (shows the pre-fix X01 mismatch).
- `receipts/tool-selftest.txt` — `--selftest` receipt for the final bytes (59/59, exit 0).
- `receipts/tool-hygiene.txt` — greps: no literal temp-dir string, no network imports.
- `receipts/matrix-*.txt` — four matrix campaigns: asdelivered (met=true), two A16
  mutants (rejected), multiset-collapse falsifier (rejected).
- `receipts/sources-quotes.txt` — grounding quotes fetched 2026-11-03 by public GET
  from developers.google.com, rfc-editor.org, iana.org.
- `driver_reviewerc2.py` — the battery driver (`python3 driver_reviewerc2.py
  <tool-path> <tag>`); writes only under this directory.

## Reproduce

```sh
S=<your scratch>; mkdir -p "$S/tmp"
TMPDIR="$S/tmp" python3 -B .ufo/waves/round-76/w1/ReviewerC2/driver_reviewerc2.py \
  .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py rerun
python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py \
  --selftest --work "$S/tmp/selftest"
python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py \
  --root . --tool .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py \
  --revision a0491fcd041cbc3fff2c964ecf6268557e45a5c1 \
  --work "$S/mwork" --min-decided 24
```
