# Mini SKILL.md fixture f04 — prefix collision (c72_tmp.py vs c72_tmp_v2.py)

### Round 72 gate registry additions

The row below is a historical marker for the retired first edition; the v2 counter itself is
registered in a later round or not at all.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| tmp-counter-first-edition | gate (historical; retired first edition kept for the audit trail; the file left the tree when v2 landed) | `python3 -B .ufo/waves/round-72/c72_tmp.py --revision <commit>` | `0=met`; `1=not met` | none (retired) | superseded by the v2 row | read-only | kake round 72 |

Round 72's live counter is the v2 edition; see the round-72 contract for why the v1 path no longer
resolves while its row remains.
