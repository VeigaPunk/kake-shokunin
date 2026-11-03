# ScribeKnowledge receipts — round 74 w1

Raw outputs retained before the scratch tree `/fast/scratch/hyaku/kake-r74/ScribeKnowledge/`
was removed. Every file here was produced by a command in the report's receipts table; no
file was edited by hand afterwards.

| file | produced by | outcome |
|---|---|---|
| `census.py` | scribe-authored, run as `python3 -B census.py [rev]` | exit 0; independent `os.stat` census of the base sidecar |
| `census-out.txt` | `python3 -B census.py > census-out.txt` | sha256 `1d4fb00e184b1c27bdcd22c649083f368ef1c19fba4320c434bc0352fa283935` — identical to `.ufo/waves/round-74/controls/base-c2-sidecar.txt` (`diff -u` exit 0) |
| `counter-base-out.txt` | `python3 -B .ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py --root <lane> --revision ced2878a…` | exit 1; one summary line |
| `counter-base-err.txt` | same run, stderr | empty |
| `tool-demo.txt` | fresh scratch copy of the base sidecar, `w1/ExecC2Tool/sidecar_reobserve.py` `--check`, `--write --date 2026-11-03 --host linux-x86_64`, second `--write --date 2026-11-04` | exits 0/0/0; `flipped=144 wrote=true`; second write `flipped=0 wrote=false` with identical shas (`7c5fda74…b77b8`) |
| `parsed-summary.txt` | JSON read of the demo output | 170 restored / 4 absent; 144 `history` arrays; every history equals the base `{date,kind,note}` as a decoded object; 144 `\u2014` escapes in the file |
| `serialisation-probe.txt` | `json.dumps` round-trip of the base bytes, both `ensure_ascii` settings | `ensure_ascii=True` not byte-identical; `ensure_ascii=False` byte-identical; 432 non-ASCII bytes, all in `note` of the 144 entries |

Unevaluable refusal (reported in the report body, receipt 8) was observed in a mode-000
fixture directory as uid 1000: both `--check` and `--write` exited 2 with
`unevaluable=1` and `error=one or more tokens could not be evaluated; no write`, and the
sidecar sha256 was unchanged across the pair.

Scratch tree removed after these files were copied; the scratch path no longer exists.
