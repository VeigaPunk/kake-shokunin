# Mini SKILL.md fixture f08 — entry-command path with a leading './'

### Round 69 gate registry additions

Round 69 registers its TMPDIR counter below; the entry command is written with a redundant leading
dot-slash.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c69_tmp_honour.py | gate (live; operability: the lane gate honours TMPDIR and holds no /tmp root; predicate frozen in `.ufo/waves/round-69/contract.md` section C2) | `python3 -B ./.ufo/waves/round-69/c69_tmp_honour.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --selftest` | no /tmp code literal in any tracked file | read-only over committed bytes; scratch only | kake round 69 |

The path with the leading `./` denotes the same file as the plain root-relative path.
