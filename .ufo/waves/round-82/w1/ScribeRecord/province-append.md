## Round 82 capture-to-capture drift ground

The capture-to-capture drift ground enters as a freshness instrument, not a property verdict. Two
dated GET-only captures of the same three declared `ds4cc.com` surfaces — capture A under
`.ufo/waves/round-81/capture/`, capture B under `.ufo/waves/round-82/capture/` — are compared
offline by `scripts/capture_delta.py`, which verifies every receipt against its retained body and
prints one stable line per surface plus `surfaces=… identical=… changed=… added=… removed=…`. The
record is `.ufo/waves/round-82/controls/after-c2-delta.txt` (the tool's stdout, no command line),
and it re-derives from committed bytes at a measured revision
(`python3 -B .ufo/waves/round-82/c82_capture_delta.py --root . --revision <rev>`). The entry is
`corpus/knowledge/capture-drift-validators.md` (S455, RFC 9110 §8.8.1 and §8.8.3). What the
instrument establishes is that two recorded instants agree or differ in status, body bytes and
header mappings. It says nothing about which answer is correct, whether a future change would be
detected, or whether a capture came from a socket — a well-formed fabrication with real digests
passes, so provenance stays the capture transcript. No publish or deploy; the property remains
operator-owned.
