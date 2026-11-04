## Coverage — round 82 (2026-11-04)

| Area | Entry | Coverage |
|---|---|---|
| Capture-to-capture drift gate (r82) | `knowledge/capture-drift-validators.md` + `scripts/capture_delta.py` + `.ufo/waves/round-82/capture/` + `.ufo/waves/round-82/controls/after-c2-delta.txt` (S455; RFC 9110 §8.8.1 and §8.8.3) | Two dated GET-only captures of the same three declared `ds4cc.com` surfaces (round-81 capture A, round-82 capture B), every receipt verified offline against its retained body (GET, integer status, byte count, body sha256, RFC 3339 fetch time, not truncated); the delta compares status, body sha256, byte count and the header mapping per surface and prints `surfaces=… identical=… changed=… added=… removed=…`. The committed record re-derives from committed bytes at a measured revision, and identical-capture and one-byte-flipped controls both read `met=false`. Not covered: which answer is correct, whether a future change would be detected, or that a capture came from a socket — a well-formed fabrication with real digests passes. |

Sources opened this round: S455 (RFC 9110 §8.8.1 Weak versus Strong and §8.8.3 ETag, tier A,
new row; the retained-copy provenance and quoted spans are in
`knowledge/capture-drift-validators.md`); registry 192 → 193 rows, census exit 0
(`.ufo/waves/round-82/controls/census-after.txt`).

Frontier line: the capture-to-capture drift gate enters as a freshness instrument, not a property
verdict; an occurrence oracle (proving a capture came from the network, not from bytes) stays
frontier and is the honest limit of the C2 counter.
