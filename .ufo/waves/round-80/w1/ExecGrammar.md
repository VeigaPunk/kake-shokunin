# ExecGrammar — round 80 w1 report

**Verdict: amendment 1 is implemented in `scripts/x_robots_tag_audit.py` and the C2 counter over the final bytes prints `frozen wrong=0 a2 wrong=0 constants=4/4+4/4 selftest=ok met=true`, exit 0 — the frozen predicate holds.**

## Tool state (before → after)

- before (freeze commit `f20163c1`, clean tree): sha256 `dd83c2c8e9046faa0a62afda4cea00fee85468e83d2f1720c92159fb11f2609b`, 19680 bytes; `--selftest` → `selftest: 26/26 passed`, exit 0.
- after (working tree, identical to committed bytes; `git diff -- scripts/x_robots_tag_audit.py` empty at settlement commit `782ec6e9`): sha256 `d1ea524fcd8399b6eb5b8d52864784424a3596bc32aaeb32b2e99916cb5573f0`, 23677 bytes; `--selftest` → `selftest: 33/33 passed`, exit 0.

## What I changed (and only this file)

1. `scripts/x_robots_tag_audit.py:13-16` — module docstring grammar paragraph gains the round-80 amendment-1 sentence (comma after the leading weekday token of an `unavailable_after` value stays inside the value).
2. `scripts/x_robots_tag_audit.py:61-65` — new `ASCTIME_RE`: the RFC 9110 §5.6.7 asctime form exactly as amendment A2 writes it — `(Mon|…|Sun) (Jan|…|Dec) {1,2}[0-9]{1,2} hh:mm:ss YYYY` (day-of-month 1–2 spaces + 1–2 digits).
3. `scripts/x_robots_tag_audit.py:66-75` — new `DATE_COMMA_RE`: matches one piece of the comma-split value that ends exactly at a leading weekday token of an `unavailable_after` value (3-letter IMF-fixdate names and full RFC 850 names, case-sensitive spellings mirroring the shape regexes); optional `bot` prefix (`[A-Za-z0-9_-]+`); directive name matched case-insensitively, consistent with `parse_rule`'s lowercasing.
4. `scripts/x_robots_tag_audit.py:113-115` — `parse_rule`'s `unavailable_after` disjunction gains `ASCTIME_RE`. No other directive, finding id, or exit code touched.
5. `scripts/x_robots_tag_audit.py:121-142` — `parse_field` loop restructured from `for raw in value.split(",")` to an indexed `while`: when `DATE_COMMA_RE` matches the current piece and its `bot` group is absent or names a non-`KNOWN` token, the piece merges with the next via the consumed comma (`raw += "," + pieces[index+1]`), restoring the value verbatim, e.g. `unavailable_after: Wed` + `,` + ` 03 Dec 2025 13:09:53 GMT`. All other commas keep the round-79 rule; each segment start glues at most one comma (the three accepted comma-bearing shapes carry exactly one).

Semantics decisions, grounded in the amendment text: A1's scope is limited to `unavailable_after` values, so `noindex: Wed, …` (a `KNOWN` head) does not merge and keeps round-79 behavior; the regex anchors with `$` (not `\s*$`) because the comma must *immediately* follow the weekday token, so `Wed , 03…` still splits. No frozen case discriminates either decision; I flagged both to `KakeR80`, who left the `$` form in place.

## Selftest (requirement 4)

All original cases kept (t01–t23 + 3 fault checks). Seven cases (t24–t30) covering the IMF comma shape with seconds (t24), IMF without seconds (t25), RFC 850 comma shape (t26), asctime two-space day (t27), the `noindex, <date>, noarchive` boundary (t28), the `… PST` negative → `xrt_invalid_value` only (t29), and the per-bot comma date (t30) are present and pass. **Authorship note for the record:** mid-flight `KakeR80` stood me down from the file and added t24–t30 itself (from ScoutRecon's list, it said) after my parser edits were already in the tree; I had prepared an equivalent set but never applied it. The line moved `selftest: 26/26 passed` → `selftest: 33/33 passed`, exit 0 both times.

## Measure (requirement 5) — exact output, verbatim

Command (run twice over identical bytes; work dirs under my scratch):

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/c80_measure.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/x_robots_tag_audit.py --work /fast/scratch/hyaku/kake-r80/ExecGrammar/final
frozen: cases=31 decided=31 wrong=0 constants=4/4 selftest_ok=true ok=True
a2: cases=12 decided=12 wrong=0 constants=4/4 selftest_ok=true ok=True
C2v1 revision=worktree frozen_cases=31 frozen_wrong=0 a2_cases=12 a2_wrong=0 constants=4/4+4/4 selftest=ok met=true
exit=0
exit=0
```

Both runs identical (`…/final` and `…/final2`). Base control comparison: `controls/base-c80-a2.txt` records `a2 wrong=10 met=false` at `9998dc7a` — the amendment moved all ten comma/asctime cases to decided-correct with no regression on the frozen 31 (which contain no comma-bearing date values; verified by inspection of `.ufo/waves/round-79/cases`).

## Robustness (requirement 6)

Untouched by my diff: the regular-file check, 16 MiB size cap, JSON-fault handling, and the argparse subclass exiting 64 on usage errors (`scripts/x_robots_tag_audit.py:404-408` region, unchanged). The counter independently re-verifies the round-79 repairs' standing: `constants=4/4` in both runs, `selftest_ok=true` in both, frozen matrix `wrong=0`.

## Evidence retained

- `.ufo/waves/round-80/w1/ExecGrammar/tool-state.txt` — before/after sha256, byte counts, selftest lines, git log context.
- `.ufo/waves/round-80/w1/ExecGrammar/measure-final.txt` — the verbatim measure output above (both runs).

## Scratch discipline

All counter `--work` output lived under `/fast/scratch/hyaku/kake-r80/ExecGrammar/`; my scratch tree was deleted before yield and its absence verified.

## Risks / blockers

None open. Mid-flight coordination note: `KakeR80` twice measured the tree while my edits were landing and stood me down from further writes to the tool; the final bytes carry my parser/regex work plus the L1-authored selftest cases, and the measure was re-run over those exact committed bytes after the stand-down. No case, oracle, contract, or round-79 artifact was touched; no other lane file written.
