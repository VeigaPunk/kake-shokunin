<!-- DRAFT for L1 integration — delete this comment block, then append as a new
"## Coverage — round 83 (2026-11-04)" section at the end of `corpus/README.md`.

Placeholders: <<sources-line>> (S456 row + registry/census counts from `w1/ScribeKnowledge.md`).
The S456 section scope is resolved from the landed entry: RFC 9111 §3.1, §3.2, §4, §4.2,
§4.2.3 and §4.3.1 of the retained 84,477-byte copy (see `w1/ScoutSources/fetch.txt`).

Guard: `corpus/knowledge/header-change-classes.md` landed at 180 lines in this wave and cites
`S456` in its `source:` field. If the L1's tree does not carry it at integration time, drop that
path from the Entry cell and say so in the report — do not cite an absent entry.
-->

## Coverage — round 83 (2026-11-04)

| Area | Entry | Coverage |
|---|---|---|
| Header-change classification (r83) | `knowledge/header-change-classes.md` + `scripts/header_change_class.py` + `.ufo/waves/round-83/controls/after-c2-classes.txt` (S456; RFC 9111 §3.1, §3.2, §4, §4.2, §4.2.3 and §4.3.1) | Two dated capture trees of the same three declared `ds4cc.com` surfaces (round-81 capture A, round-82 capture B), each receipt verified offline against its retained body and each changed header classified against the frozen class table as `per-request`, `validator`, `representation`, `policy` or `unknown`; a surface is `representation-changed` when status or body sha256 differs or any changed header is validator/representation/unknown, else `same-object`. The committed record re-derives from committed bytes at a measured revision, and a control pair must classify `representation-changed` with `validator>=1` while an identical pair reads `met=false`. Not covered: whether either answer is correct, whether a future change would be detected, or whether a capture came from a socket; the table classifies header names, not values. |

Sources opened this round: <<sources-line>>.

Frontier line: header-change classification moves from the round-82 drift ground to a classified
instrument over the frozen captures; an occurrence oracle (proving a capture came from the network,
not from bytes) and value-level classification (a changed `cache-control` directive read for what
it changes) stay frontier and are the honest limits of the C2 counter.
