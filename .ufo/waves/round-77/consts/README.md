# C2 degenerate constants

Four tools with the same CLI as `scripts/sitemap_audit.py`
(`python3 -B <tool> --manifest <path>`), each deliberately wrong in one way. The matrix runs
all four over the 20 cases; `constants_failed=<k>/4` counts the constants that fail at least
one case, and the frozen predicate needs `k == 4`.

| file | behaviour | why it must fail |
|---|---|---|
| `always_clean.py` | prints `verdict: clean`, no findings, exit 0 for every input | every case expecting exit 1 or 2 |
| `report_every_id.py` | one finding per known id, exit 1 for every input | every clean case (exit 0), and its id set matches no case |
| `empty_findings_real_exits.py` | runs the measured tool, keeps its exit code and input-fault items, empties every `findings` list | every case whose expected finding set is non-empty |
| `round39_xml_only.py` | the round-39 tool itself, extracted from `a2cc5f51` | gzip, text and feed families (the whole point of the claim) |

## Constant 3 — the measured tool

`empty_findings_real_exits.py` reads `C2_REAL_TOOL` from the environment; the matrix sets it
to the tool it is measuring, so the constant always mirrors that tool's exits. Without the
variable it falls back to `<lane>/scripts/sitemap_audit.py`. This is the probe for the
kill rule "a matrix that compares only exit codes is invalid": its exits are right wherever
the measured tool's are, so only the findings comparison can reject it.

## Constant 4 — the round-39 bytes

Extracted with

```sh
git show a2cc5f51002433e11cc3d2f70e650a6c60ad5e68:scripts/sitemap_audit.py
```

Observed: 657 lines, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`,
git blob `21553d19f93a14facddfa95f07c8f852d64fa82e`. Its per-case decisions are identical to
the base tool's, byte for byte (`.ufo/waves/round-77/controls/base-c2-matrix.txt`).

Run one constant by hand:

```sh
python3 -B .ufo/waves/round-77/consts/always_clean.py --manifest .ufo/waves/round-77/cases/g01/manifest.json
```
