## Verdict

The lowest-axis duty applies. The lane owns only operability and freshness, both score 10 at the declared 10/10 saturation line; the stagnation nudge does not waive the duty because the existing receipt-replay capability first worked in round 23, within the N=1 window. Both frozen claims target those tied-lowest axes (C1 freshness, C2 operability), and both are countable measured claims—not exploratory claims. C2 should update the existing `GET snapshot + canonical receipt replay` capability row once `scripts/receipt_replay.py` is landed and its round-24 demonstration passes; do not add a duplicate capability row or credit an unrun capability.

## Findings

### P2 — Update the existing receipt-replay capability row when C2 is demonstrated

- **Exact inspection commands:** `read("/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:187-213")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py")`.
- **Exact observed output:** SCORECARD.md:193 names `GET snapshot + canonical receipt replay`, points to `scripts/live_snapshot.py` and round-23 evidence, and records first-working round `23`; SCORECARD.md:208-210 declares saturation 10/10 on both owned axes and `N = 1 completed lane round`. The frozen contract at line 33 says C2 touches `scripts/receipt_replay.py and its knowledge/capability pointer`. The attempted script read returned exactly: `Path '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py' not found.`
- **Impacted claim/axis:** C2 / operability; the capabilities-table evidence and description.
- **Smallest safe correction:** After the script exists and C2's measured replay demonstrates it, extend the existing SCORECARD.md:193 row to describe strict malformed-receipt rejection and include `scripts/receipt_replay.py` plus the passing round-24 measurement as evidence. Retain first-working round 23 for the existing snapshot/replay capability; do not add a duplicate row or claim the extension before the demonstration. The frozen contract already calls for this pointer, but the current working-tree read did not find the script, so this is a landing-time requirement, not a verified completion.

### P3 — No lowest-axis or exploratory-claim defect found

- **Exact inspection commands:** `read("/home/vgpnk/Projects/shokunin/AXES.md:25-73")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md:3-15,187-213,314-325")`; `read("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json")`.
- **Exact observed output:** AXES.md:33-35 requires a claim on the lowest non-retired axis unless the nudge waives it; AXES.md:68-73 limits that waiver to all owned axes at/above saturation **and** no capability entered within the stagnation window. SCORECARD.md:3-4 lists operability + freshness as the lane's owned axes; lines 14-15 give each score 10; lines 208-213 give the 10/10 saturation line and N=1; line 193 records the receipt-replay capability's first-working round as 23. SCORECARD.md:324-325 records round-23 freshness and operability moves at 10→10. The frozen contract lines 10-17 identify C1 as freshness and give its 19-target counting command; lines 21-30 identify C2 as operability and give its frozen-case counting command and before/after criteria.
- **Impacted claim/axis:** C1 / freshness and C2 / operability.
- **Smallest safe correction:** None to claim placement or type. Both axes are tied at the lane's low score; round 23's capability entry is within the one-round window, so the nudge does not waive the duty. AXES.md:43-55 defines exploratory claims as real but not countable improvements with no counting command, requiring a named non-author reviewer and a special verdict. C1 and C2 are explicitly `measured` and have falsifiable populations, before/after criteria, and counting commands (contract lines 13-17 and 25-30), so neither is secretly exploratory. The newly cited RFCs (contract line 24) are support for C2's measured validation, not a separate exploratory claim.

## Checked and held

- Lowest-axis duty applies; both frozen claims are on the tied-lowest owned axes and are distinct-axis claims.
- The capability-table action is an update to the existing round-23 receipt-replay row, conditional on round-24 demonstration; no new row is justified by the review alone.
- No round-24 counter, CLI replay, build, test, or independent admission was run or claimed. No tools were installed or updated.

## Limits

This is a source/contract review only. The frozen plan and current SCORECARD.md were read, but `scripts/receipt_replay.py` was not present at the reviewed path, so its implementation and passing demonstration remain unverified.