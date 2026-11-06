# ScoutSources — round 100 W1 (scoped findings; full receipts in w1/ScoutSources/report.md, row drafts in w1/ScoutSources/rows.md)

Source re-open for S486/S487, done 2026-11-06T01:48:09Z. One GET per RFC, no retry, both answered HTTP 200 at the requested URL.

- RFC 9111: 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e — equals the retained round-99 body (.ufo/waves/round-99/sources/rfc9111.txt, recomputed this run). match. Confirms the freeze.md line 68-69 assertion; no defect.
- RFC 9110: 502941 bytes, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a — equals the retained round-100 body (.ufo/waves/round-100/sources/rfc9110.txt). match. Byte counts also agree with S484 (84477) and S466 (502941).

Ten verbatim quotes located by plain-text line number in the fetched bodies (byte-identical to retained, so lines hold for both); every quote ≤ 25 words/tokens. RFC 9111: §5.2 token/case-insensitivity sentence 1098-1100, accept-both-forms sentence 1100-1102, cache-directive production 1106, §5.2.2.4 qualified field-name sentence 1273-1279, §5.2.2.7 qualified field-name sentence 1334-1339, §5.2.3 MUST-ignore sentence 1411-1412, §3.1 proxy-fields MUST-NOT-store sentence 358-360. RFC 9110: §5.5 whitespace sentence 1591, §5.6.1.2 accept-syntax production 1702 (introduced 1695-1700), §5.6.4 quoted-string + qdtext productions 1786-1787 (quoted-pair production 1794).

Row drafts ready in w1/ScoutSources/rows.md (11-column shape, no pipes in cells): S486 = RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3 + §3.1 proxy-fields sentence, scope distinct from S484 (narrowed to lines 358-360 in the shared §3.1), S456 (which explicitly excludes cache-directive argument syntax) and S457/S461/S469; S487 = RFC 9110 §5.5/§5.6.1.2/§5.6.2/§5.6.4, scope distinct from S433/S453/S465 plus S466/S478 not-clauses. Both: spec A, status mined, opened 2026-11-06, recheck 365d, used-by corpus/knowledge/freshening-304.md.

Finding to route (not repaired): the prescribed S487 sections already host adjacent held rows — S465 anchors §5.6.2 token production lines 1730-1738 and the §5.6.1.2 empty-element sentence; S478 anchors §5.6.1.2 lines 1695-1702; S466 anchors §5.5 lines 1579 and 1606-1612. S487's anchors (1591, 1702, 1786-1787/1794) are different sentences, and the drafted scope states the distinctness, but the L1/reviewers should confirm the wording before the rows land (freeze says rows land only after this re-open; re-open is now done).

Bounds: writes only under .ufo/waves/round-100/w1/ScoutSources/ plus this trailer; read-only git in the lane; bodies kept in seat scratch /fast/scratch/hyaku/kake-r100/ScoutSources/ only (deleted at yield); no tool installs; no mutating git/jj anywhere; no sysctl or host changes.

SCOUT rfc9111-sha=match rfc9110-sha=match quotes=10/10 rows=2
