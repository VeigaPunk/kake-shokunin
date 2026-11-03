# Mini SKILL.md fixture f06 — duplicate rows, one with a dead path

### Round 71 gate registry additions

Two rows below mention the round-71 freshness counter; the second is a stale alias row left behind
by a rename.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c71_tmp.py | gate (live; freshness: stale /tmp citations in SKILL.md; predicate frozen in `.ufo/waves/round-71/contract.md` section C2) | `python3 -B .ufo/waves/round-71/c71_tmp.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-71/c71_tmp.py --selftest` | base receipt is the control | read-only over committed bytes; scratch only | kake round 71 |
| tmp-counter-pre-rename | gate (historical; the c71_tmp.py counter's pre-rename row, kept by mistake after the rename) | `python3 -B .ufo/waves/round-71/c71_tmp_pre_rename.py --root . --revision <commit>` | `0=met`; `1=not met` | none (stale) | withdrawn with the rename | read-only | kake round 71 |

At most one of the two entry commands resolves.
