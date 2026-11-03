# Mini SKILL.md fixture f02 — prose-only mention; kill-rule f3 shape

### Round 70 gate registry additions

The round-70 audit reuses the standing counter `c70_pointer_audit.py`; its frozen predicate lives in
`.ufo/waves/round-70/contract.md` section C1. No row is appended this round; registering it stays
routed to the next round.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| freshness-sweep | gate (live; sidecar binding validation) | `node scripts/freshness-sweep.mjs --offline` | `0=ok`; `1=drift`; `2=invalid` | `node scripts/freshness-sweep.mjs --selftest` | single named drift class | read-only | kake |

No registry row names the round-70 counter yet; the paragraph above is context only.
