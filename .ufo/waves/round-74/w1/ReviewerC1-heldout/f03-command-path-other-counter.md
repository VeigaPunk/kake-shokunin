# Mini SKILL.md fixture f03 — row whose entry command names a different counter

### Round 69 gate registry additions

The row below registers the round-69 TMPDIR counter only.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| tmp-honour-counter | gate (live; operability: the lane gate honours TMPDIR and holds no /tmp root; predicate frozen in `.ufo/waves/round-69/contract.md` section C2) | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --selftest` | no /tmp code literal in any tracked file | read-only over committed bytes; scratch only | kake round 69 |

The recorded-counts counter of the same round is registered separately, if at all.
