| mutant | fixture | selftest (pristine -> mutant) | fixture rc | verdict |
|---|---|---|---|---|
| C1-m1-drop-share-conjunct | share-0.2222 | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m2-ignore-bytes-basis | bytes-basis-chars | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m3-erratum-threshold-one | erratum-two-quotes | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m4-drop-bound-equals-population | d3-bound-differs | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m5-drop-attack-floor | attack-floor-one | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m6-drop-killer-row-check | killer-rows-missing | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m7-count-chars-not-utf8-bytes | multibyte-bytes | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 0 -> 1 | killed |
| C1-m8-met-always-true | junk-prose-only | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C1-m0-comment-only-control | green | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 0 -> 0 | survived |
| C2-m1-tool-offline-always-true | tool-imports-socket | 0/selftest: 9/9 passed -> 1/selftest: 8/9 passed | 1 -> 0 | killed |
| C2-m2-control-ok-hardcoded | control-pair-identical | 0/selftest: 9/9 passed -> 1/selftest: 8/9 passed | 1 -> 0 | killed |
| C2-m3-validator-as-per-request | etag-only-change | 0/selftest: 9/9 passed -> 1/selftest: 8/9 passed | 1 -> 1 | killed |
| C2-m4-drop-diffs-positive | captures-identical | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C2-m5-record-equal-weakened | record-wrong | 0/selftest: 9/9 passed -> 1/selftest: 8/9 passed | 1 -> 0 | killed |
| C2-m6-content-length-as-per-request | content-length-change | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 0 | killed |
| C2-m7-accept-truncated-receipt | receipt-truncated | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 1 -> 1 | killed |
| C2-m8-met-always-true | captures-identical | 0/selftest: 9/9 passed -> 1/selftest: 1/9 passed | 1 -> 0 | killed |
| C2-m0-comment-only-control | green | 0/selftest: 9/9 passed -> 0/selftest: 9/9 passed | 0 -> 0 | survived |
