# Round 93 C1 predicate — self-assessment conformance (frozen before data)

This sentence is the claim's predicate in the plan, the condition in
`.ufo/waves/round-93/c93_selfassess.py` and the label in the receipt:

> **met <=> at the measured revision the pinned population has not shrunk and the counter
> enumerates zero mismatches across classes E1–E5.**

Classes, each one sentence (the counter's docstring carries the same five):

- **E1** — every lane-authored round lesson (`corpus/lessons/round-*.md`, excluding
  `*-verifier-spotcheck.md` and `*aggregator*`) carries a line exactly `## Gate`.
- **E2** — every `## ` section of `corpus/QUALITY.md` whose heading matches `^Round[- ]<digits>`
  and whose first 400 characters mention "criteri" names at least one existing
  `corpus/lessons/<file>` path.
- **E3** — every `corpus/knowledge/*.md` carries non-empty `source:`, `verified-at:` and
  `recheck:` lines within its first 8 lines, and every `S<digits>` id on its `source:` line
  resolves to a row id in `corpus/SOURCES.md`.
- **E4** — in every lane-authored round lesson, the `## Mistakes` table is contiguous: no blank
  line sits between two lines that both start with `|`.
- **E5** — every repo-relative path (`scripts/…`, `corpus/…`, `.ufo/…`) named inside a `SKILL.md`
  table row exists at the revision (brace lists expanded, a trailing `:<line>` or
  `:<start>-<end>` stripped, `<…>` placeholders and `*` skipped).

Population pins (measured at the base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`):
`lessons=87 entries=80 rows=255 criteria=39`. A smaller population at the measured revision is
`pins=short` and met=false whatever the mismatch count, so deleting the surface cannot buy a pass.

Counting command (one command over committed bytes; scratch under `$HYAKU_SCRATCH`):

```sh
python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision <REV>
```

Exit 0 iff met; 1 otherwise; 2 on unevaluable input. Line 1 is the receipt; line 2 is JSON detail
listing every mismatch with class, path and the exact disagreement, so any single row can be
re-derived with `git show <REV>:<path>` and `grep`.

Target: **0 mismatches** (base measurement: 20). Do-nothing control: the base run itself
(`controls/base-c1.txt`, `mismatches=20 … met=false`, exit 1) — a round that repairs nothing scores
exactly the base reading and cannot reach the target. Instrument controls:
`controls/ctl-c1-selftest.txt` (a synthetic lane with one planted defect per class reports exactly
those five findings and exits 1; repaired, it reads 0 and exits 0).

Not claimed: that a repaired statement is *true* beyond the predicate it states (E3 checks the
presence and resolution of the metadata trio, not that the source supports the entry), and that the
population covers every self-assessment statement the lane makes — only the five enumerated classes.
