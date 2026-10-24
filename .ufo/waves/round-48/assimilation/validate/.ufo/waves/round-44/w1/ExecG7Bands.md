# ExecG7Bands — round 44, wave 1

## Axes and change

- **Operability:** covered the G7 witness classes for the five assigned repetition-memo controls.
- **Freshness:** unchanged; this assignment only adds the offline class generator.

Wrote `.ufo/waves/round-44/classes/g7_band_memos.py`. `cases(rng, h)` returns 240 `value`/`loc` units in 120 first-seen clean-then-defective pairs: 40 length keys (6001–6040), 40 slash-count keys (64–103), and 40 `(length, first-percent-index)` keys (1600–1639, 1000–1039). The defect member substitutes `%G4`; defpos pairs retain a valid `%41` at the same first-percent index in both members. Values are deterministic from `rng` and use only the counter helpers.

## Control and reference inspection

Inspected each control's `_uri_ok` memo insertion against the round-41 parser saved at `/fast/scratch/hyaku/kake-r44/ExecG7Bands/round41_sitemap_audit.py`. The controls memoize by length for 6001–199999; slash count for 64+ slashes (the band variant additionally requires length <=1799); and `(length, first '%' index)` for a first percent at 1000+ (the band variant additionally requires length <=1799). Round 41's `_URI_RE` requires `%[0-9A-Fa-f]{2}` and `_parse_url` rejects values not matching it. `_audit_loc` records `loc_too_long` at the 2048-codepoint limit and then continues to `_parse_url`, allowing the length-band grammar difference to remain observable.

**Constraint conflict:** the length memo cannot be witnessed by a `loc` value <=2048 because its key range begins at 6001. I used 6001–6040-codepoint `loc` pairs, preserving the required `loc_not_absolute` difference; both reference and control also report the shared `loc_too_long` finding for those pairs. Depth and defpos values remain below 2048.

## Probe evidence

Exact probe invocation form (each command below was run with the shown seed and control):

```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G7 --tool-file .ufo/waves/round-44/controls-r43/<control> --seed <seed>; rc=$?; printf 'probe_exit=%s\\n' "$rc"; exit 0
```

All ten probe JSON results had `equal: false`; each emitted `probe_exit=1` (semantic witness). Decisive JSON fields are reproduced below; the probe's `ref41Tail`/`candTail` fields are omitted.

| Control | Seed | Probe JSON decisive fields |
|---|---:|---|
| `repeat-ctl_len_memo_band.py` | 44001 | `{"probe":"G7","seed":44001,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"07347417fbd1d51fea930a642392212da3b99f54d0cc612ce4a2dcf7be701fd5","candOutSha256":"98e556af78c22bf3dcefefc8f061b2e5e8a07bab205762ea8b193d449f0d8e19","equal":false}` |
| `repeat-ctl_len_memo_band.py` | 44002 | `{"probe":"G7","seed":44002,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"af58873353721e6a736b9278557161324b3fd47de79c5d8aee66a504c15cb3cd","candOutSha256":"5e5290e5d32cb890fffdabdfe35a1bd95f20421738e20358a32f4ec0f44df5f1","equal":false}` |
| `repeat-ctl_depth_memo_band.py` | 44001 | `{"probe":"G7","seed":44001,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"07347417fbd1d51fea930a642392212da3b99f54d0cc612ce4a2dcf7be701fd5","candOutSha256":"7a243ffcdd8e654b3742e0feabc2b674faa1409f049ed7829e3dafd2a9663642","equal":false}` |
| `repeat-ctl_depth_memo_band.py` | 44002 | `{"probe":"G7","seed":44002,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"af58873353721e6a736b9278557161324b3fd47de79c5d8aee66a504c15cb3cd","candOutSha256":"fff6af835bb959f52704202f55ba6651b2f28fe4e0b2e020cd6da7cdea19f1d6","equal":false}` |
| `repeat-ctl_defpos_memo_band.py` | 44001 | `{"probe":"G7","seed":44001,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"07347417fbd1d51fea930a642392212da3b99f54d0cc612ce4a2dcf7be701fd5","candOutSha256":"4ab32999dfc76fd545c72576bf3ba34bad2b976b99af114a2b2bc2d0ae2f170f","equal":false}` |
| `repeat-ctl_defpos_memo_band.py` | 44002 | `{"probe":"G7","seed":44002,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"af58873353721e6a736b9278557161324b3fd47de79c5d8aee66a504c15cb3cd","candOutSha256":"9af5a0e354e1e1188bfc720d6b8802dbc8a799f8a7108a483e386790d6ae73c5","equal":false}` |
| `repeat-ctl_depth_memo_deep.py` | 44001 | `{"probe":"G7","seed":44001,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"07347417fbd1d51fea930a642392212da3b99f54d0cc612ce4a2dcf7be701fd5","candOutSha256":"7a243ffcdd8e654b3742e0feabc2b674faa1409f049ed7829e3dafd2a9663642","equal":false}` |
| `repeat-ctl_depth_memo_deep.py` | 44002 | `{"probe":"G7","seed":44002,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"af58873353721e6a736b9278557161324b3fd47de79c5d8aee66a504c15cb3cd","candOutSha256":"fff6af835bb959f52704202f55ba6651b2f28fe4e0b2e020cd6da7cdea19f1d6","equal":false}` |
| `repeat-ctl_defpos_memo_late.py` | 44001 | `{"probe":"G7","seed":44001,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"07347417fbd1d51fea930a642392212da3b99f54d0cc612ce4a2dcf7be701fd5","candOutSha256":"4ab32999dfc76fd545c72576bf3ba34bad2b976b99af114a2b2bc2d0ae2f170f","equal":false}` |
| `repeat-ctl_defpos_memo_late.py` | 44002 | `{"probe":"G7","seed":44002,"units":240,"values":240,"ref41Exit":1,"candExit":1,"ref41OutSha256":"af58873353721e6a736b9278557161324b3fd47de79c5d8aee66a504c15cb3cd","candOutSha256":"9af5a0e354e1e1188bfc720d6b8802dbc8a799f8a7108a483e386790d6ae73c5","equal":false}` |

## Commands and files

The following shell commands were run (no tools installed):

- `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG7Bands /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w1`
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py > /fast/scratch/hyaku/kake-r44/ExecG7Bands/round41_sitemap_audit.py`
- The ten probe commands represented in the table above, using the exact executable portion and control path shown there, with `--seed 44001` or `--seed 44002`; each was wrapped with `rc=$?; printf 'probe_exit=%s\\n' "$rc"; exit 0` to preserve the expected probe exit code in the output.

Written paths:

- `.ufo/waves/round-44/classes/g7_band_memos.py`
- `.ufo/waves/round-44/w1/ExecG7Bands.md`
- `/fast/scratch/hyaku/kake-r44/ExecG7Bands/round41_sitemap_audit.py` (reference-source scratch copy)

No build, full counter run, lint, formatter, or other test was run. No LSP interface was available in the provided tool inventory, so LSP was not used. **Blocker:** none; the 2048-vs-6001 length-band constraint conflict is recorded above.
