# Round-41 w1 — routed defect 1: restating the round-40 control tally over live seats

Seat: KakeR41.ReviewR40Restatement (leaf). Scope: recount committed round-40 wave-1 receipts,
all vs live-only, dead seat `CtlUTabOnly` listed apart. Read-only on the lane; no installs
(jq present as jaq 3.1.1; filter `-s 'map(select(.met))|length'` is plain jq semantics).

## Source bytes

- Commit `8eb121c8`, path `.ufo/waves/round-40/verification/w1`: 79 entries = 76 JSON receipts + 3 `d1check-*.txt`.
- Byte identity with the round-40 tip the closure used: `git rev-parse 8eb121c8:.ufo/waves/round-40/verification/w1 0c732d5a:.ufo/...` → both `73cf898995726c2b7927d55319235c4d5f2a50f3`; `merge-base --is-ancestor 0c732d5a 8eb121c8` → ok (exit 0). The restatement is over unchanged bytes.

## Commands and results (extract: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C <lane> archive 8eb121c8 .ufo/waves/round-40/verification/w1 | tar -x -C <sandbox>/w1`, exit 0)

1. All receipts, in `…/w1/.ufo/waves/round-40/verification/w1`:
   `set -- *.json && echo "json_receipts=$#" && jq -s 'map(select(.met))|length' -- "$@"`
   → `json_receipts=76`, `27`, exit 0.
2. Live receipts only (excluding `CtlUTabOnly-dead__*`):
   `live=(); for f in *.json; do case "$f" in CtlUTabOnly-dead__*) ;; *) live+=("$f");; esac; done && jq -s 'map(select(.met))|length' -- "${live[@]}"`
   → `live_receipts=72`, `26`, exit 0.
3. Dead seat listed apart, one per line (`jq -c '{met,passed,label}'`):
   - `CtlUTabOnly-dead__tool_cr_lf.json` — met false, passed 27
   - `CtlUTabOnly-dead__tool_tab_lf.json` — met false, passed 28
   - `CtlUTabOnly-dead__tool_tab_only.json` — met false, passed 25
   - `CtlUTabOnly-dead__tool_tab_only_query.json` — met true, passed 30
   Dead-seat subtotal: 1 of 4 met (exit 0).

The 26 live met receipts include the four `CtlKeyFinder__*`, `CtlLabelKeyed__ctl_label_keyed`,
`CtlPositionKeyed__ctl_v3_count`, `CtlRCaseFold` lookups, `CtlURawBytes__ctl`,
`L1CriticCounterexample__ctl_sitemapurl_no_lf`, and `MutFamilyU__M11_tab_before_query` (live seat,
met true) — so the "TAB in a query" sub-shape is re-derived independently of the dead seat, as the
round-40 lesson states. Full 27/26 name lists reproducible by the per-file loop in the transcript.

## Exact sentence for the round-41 appended correction

> Round-40 correction (routed defect 1): the wave-1 control tally is restated over live seats only —
> 26 of 72 receipts meet the frozen 30-witness predicate; the dead seat `KakeR40.CtlUTabOnly`'s four
> leftover tools are listed apart (1 of 4 met: `tool_tab_only_query` 30/30) and are not counted as
> independent controls; 26 ≥ 1, so kill rule (1) still fired before the build `56d57ee4` and no
> round-40 conclusion changes.

## Per-statement verdicts (lesson `corpus/lessons/round-40-verifier-spotcheck.md`)

| Statement | Verdict |
|---|---|
| 76 JSON receipts; `jq -s 'map(select(.met))\|length'` → 27 | holds (76 files ending .json, 27, exit 0) |
| Recount without the dead seat: 72 receipts → 26 | holds (72 files, 26, exit 0) |
| `tool_tab_only_query` meets (30/30), in the "27 of 76" | holds (met true, passed 30; the only dead-seat member of the 27) |
| `MutFamilyU__M11_tab_before_query` met true, a live seat | holds (met true in live-only recount; `passed` not separately re-printed) |
| "No result rests on it" (kill rule needs any one) | holds (26 live ≥ 1; drop all 4 dead-seat receipts and the rule still fires) |
| Headline "should read 26 of 72 live plus 1 of 4 dead-seat leftovers" | holds (numbers reproduce exactly from committed bytes) |

## Residual risk and gaps

- This is a recount of committed receipts, not a rerun of the round-40 counter; `met`/`passed` are read
  from receipt bytes, not recomputed. Receipt contents at `8eb121c8` are tree-identical to `0c732d5a`.
- The three `d1check-*.txt` files are not JSON receipts and are excluded from both counts (consistent
  with the round-40 report's "76 JSON files").
