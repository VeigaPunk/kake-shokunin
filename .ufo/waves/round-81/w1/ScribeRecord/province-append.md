<!-- Draft for PROVINCE.md — a `## Round 81` section appended after the [r80-correction] paragraph at EOF.
     Two paragraphs, matching the short round appends used since round 29. -->

## Round 81 capture-once front step

The capture-once / audit-offline chain enters Core as an instrument. `.ufo/waves/round-81/c81_capture_audit.py`
takes a committed capture tree (three declared `ds4cc.com` surfaces, one GET per URL, retained as
`capture/<id>/response.json`), joins the frozen expectations file to it as a version-1 manifest, runs
`scripts/header_audit.py` over that manifest with no network, and re-derives the whole chain from the
measured revision: body sha256 and byte count against the retained body, an integer status in
100..599, an RFC 3339 fetch time at or after the round's start, GET and not truncated, the URL host
inside the declared allowlist, and the audit's stdout equal to the committed audit receipt. What the
counter itself does not do is re-join the manifest to `capture-expectations.json` — the surface set and
allowlist are re-read from the manifest, so the join is the capture seat's obligation, checked by review
rather than by this predicate. Its base
control reads `surfaces=0 met=false` and its selftest `12/12`, with five mutants — body digest, byte
count, stale fetch time, drifted audit receipt, empty manifest — each opening the predicate. This is
the first lane instrument that binds a *live capture* to an *offline verdict* through committed
bytes rather than through a seat's narrative, and it is Core because the audit it wraps
(`header_audit.py`, round 61) already is. It fetches nothing at measurement time and publishes
nothing.

S454 (RFC 9110 §15.5.5 404 Not Found and §15.5.11 410 Gone; the contract's §15.5.4 anchor is
corrected by amendment 1 A2 and §15.5.4 is 403 Forbidden) fixes the boundary of what any such
verdict may conclude. A 404 Not
Found or 410 Gone answer is the target resource's absence recorded with its status; it is never
folded into a header-policy failure, and a class that reads only 2xx responses draws no conclusion
from it. So an audit verdict here is a statement about the bytes served at one `fetchedAt`, not about
the property's policy, not about whether the resource exists at another instant, and not about
whether any other client sees the same fields. The audit-output equality proves the committed receipt
and the tool's stdout agree; it does not prove who wrote the file. Those limits are stated, not
closed, and publishing stays operator-owned.
