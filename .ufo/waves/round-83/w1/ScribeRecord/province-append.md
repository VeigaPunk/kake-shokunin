<!-- DRAFT for L1 integration — delete this comment block, then append after
"## Round 82 capture-to-capture drift ground".

Resolved: the ScribeKnowledge entry landed at `corpus/knowledge/header-change-classes.md` (180
lines); its `source:` field names RFC 9111 §3.1 L338-342, §3.2 L369-388, §4 L466-490, §4.2
L581-599, §4.2.3 L719-745 and §4.3.1 L812-850 of the retained 84,477-byte copy (sha256
`aeb52adb…`, `w1/ScoutSources/fetch.txt`), and the citation below copies that scope. If the
L1's tree does not carry the entry, keep the instrument text and drop the entry path.
-->

## Round 83 header-change classification ground

The header-change classification ground narrows the round-82 drift ground's undifferentiated
`changed=<n>` count: a header that moved between the two dated captures is now classified by what
its change means for the served representation. `scripts/header_change_class.py` reads the two
committed trees (capture A under `.ufo/waves/round-81/capture/`, capture B under
`.ufo/waves/round-82/capture/`), verifies each receipt against its retained body (GET, integer
status 100..599, byte count equal to the body, body sha256 equal to the receipt digest, not
truncated), canonicalises each header list (lower-cased name, repeated values joined with `, `),
and sorts every changed header into the frozen class table: `per-request` request/edge metadata
(`date`, `age`, `x-cache`, `x-served-by`, edge ids and timers), `validator` (`etag`,
`last-modified`), `representation` (`content-length`, `content-type`, `content-encoding`, `vary`,
…), `policy` (`cache-control`, `expires`, security headers, `link`, `server`, …) and `unknown`
(everything else, treated as representation-bearing). A surface is `representation-changed` when
status or body sha256 differs, or any changed header is `validator`, `representation` or `unknown`;
otherwise it is `same-object`, and the summary verdict is `representation-changed` if any surface
is. The record is `.ufo/waves/round-83/controls/after-c2-classes.txt` (the tool's stdout, no
command line) — three surface lines plus `summary surfaces=3 diffs=14 per_request=14 validator=0
representation=0 policy=0 unknown=0 verdict=same-object` at the frozen captures — and the counter
`.ufo/waves/round-83/c83_drift_class.py` re-derives the record, the determinism pair, the
control-pair classification (`representation-changed`, `validator>=1`) and the offline property at
a measured revision. The entry is `corpus/knowledge/header-change-classes.md` (S456; RFC 9111 §3.1, §3.2, §4, §4.2, §4.2.3 and §4.3.1 of the retained copy).

What the instrument establishes is narrower than a freshness verdict. It classifies header *names*,
not values: a changed `cache-control` is `policy` even when the new directive changes freshness
semantics, and a changed `etag` is `validator` without saying which version is current. The class
table is frozen, so a changed header outside it is `unknown` and therefore decisive by design — the
conservative direction, never a silent pass. It says nothing about whether either answer is
correct, whether a future change would be detected, or whether a capture came from a socket: a
well-formed fabrication with real digests passes, so provenance stays the capture transcript. No
publish or deploy; the property remains operator-owned.
