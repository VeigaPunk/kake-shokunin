A control reaches 1434/1434 (met, counter exit 0): `delimiter_proxy.py`, sha256 `164debbd3b4dcdbc67f502df9aad3cd1e87e834255be51f3ee9f46b3bb8b8a17` — a global
character allow-list plus authority/delimiter structure, with no per-component character table. Constant and trivial outputs stay at or below 802/1434.

Seat KakeR41.CtlConstantFamily, r41 wave 1, lane tip `abf457d0`. Counter `.ufo/waves/round-41/c1_count.py` sha256 `2acc443a…67b4`.
Every score below is one run of
`prlimit --as=4000000000 timeout 900 python3 -B <lane>/.ufo/waves/round-41/c1_count.py --root <lane> --tool-file <tool> --label <L> --seed 41001 --out <receipt>`;
the exit column is the counter's exit code. Tools and receipts: `/fast/scratch/hyaku/kake-r41w1/CtlConstantFamily/` (`*.py`, `receipts/*.json`, each receipt carries the full `toolSha256`).
Seed 41001 for every row (the winner also ran seeds 7, 41004 and random 218723470873580, all 1434 met, exit 0).

| tool (sha256 prefix) | passed/1434 | loc / sitemapUrl | min byComponent | exit | work skipped; cases that caught it |
|---|---|---|---|---|---|
| `const_clean.py` eec5928b9666 | 798 | 398/630, 400/804 | port 28/239 | 1 | no URL judgment at all; every invalid case (636) caught it |
| `const_check_invalid.py` 414ce8f2282f | 802 | 398/630, 404/804 | query 131/239 | 1 | no URL judgment; all 398 valid `loc` cases caught it |
| `const_loc_findings.py` 9c2b757431a9 | 632 | 232/630, 400/804 | fragment 102/239 | 1 | no URL judgment; all 398 valid `loc` cases caught it |
| `const_both.py` d9cae90b1414 | 636 | 232/630, 404/804 | path 79/239 | 1 | no URL judgment; valid cases of both fields caught it |
| `empty_stdout.py` f881c7807794 | 0 | 0/630, 0/804 | 0/239 every | 1 | no output at all; judge note `output unreadable`, every case caught it |
| `flipped.py` bab233c30c19 | 662 | 398/630, 264/804 | port 14/239 | 1 | base judgment inverted, no RFC rule added; valid `loc` (no finding is possible when the check is an error) and base-rejected invalid `sitemapUrl` caught it |
| `union_blacklist.py` a935369de0fa | 1264 | 543/630, 721/804 | port 93/239 | 1 | union charset + percent rule only, no position; 146 port-insert and 24 `[ ] : @ #` insert cases caught it |
| `proxy_port_only.py` a545b6f26778 | 1412 | 617/630, 795/804 | fragment 234/239 | 1 | union + percent + port digits, no bracket/`#`/`@` rule; the 22 misplaced-delimiter cases caught it |
| `delimiter_proxy_noport.py` 9d2e63495671 | 1303 | 563/630, 740/804 | port 110/239 | 1 | full proxy minus the port rule; port (110/239) and two host cases caught it |
| **`delimiter_proxy.py` 164debbd3b4d** | **1434** | 630/630, 804/804 | 239/239 every | **0 met** | no per-component repertoire, no scheme/host repertoire, no IPv4/IP-literal-content test; nothing caught it |
| base `4de35f8c…1460` (do nothing) | 1049 | 509/630, 540/804 | port 239/239 | 1 | reference point: matches the section's base figure at this seed (1058 at seed 7) |
| reference `6d7c2dd4…010a` | 1434 | 630/630, 804/804 | 239/239 every | 0 met | reference repair re-scores as declared |

Findings.
- `.ufo/waves/round-41/c1_count.py:265-268` reads an error item as "no `loc_not_absolute`", so any tool that marks every `sitemapUrl` `check_invalid` is credited for all 398 valid `loc` cases without judging a `loc` (const_check_invalid loc 398/630 exactly). That is also why `flipped.py` scores 662 and not 1434−1049: it rejects every valid `sitemapUrl`, every group check becomes an error, and no `loc` finding is ever emitted.
- Constant ceiling at seed 41001 is 802/1434 (55.9%): all-valid is 798, all-invalid is 636, and a manifest-only split (multi-entry file = `loc` checks, single-entry file = `sitemapUrl` checks) reaches the same 398+404 = 802. No constant output can pass this counter.
- `delimiter_proxy.py` rules, in full (docstring has them): (1) ASCII must be in the union of every RFC 3986 component repertoire, non-ASCII accepted; (2) each `%` introduces two hex digits; (3) at most one `#`; (4) the authority is non-empty with at most one `@`; (5) host-port is `[literal]` (non-empty, no inner bracket, optional `:digits`) or bracket-free with optional `:digits` port; (6) no bracket outside that literal. It knowingly judges **no** character per component (no userinfo/host/path/query/fragment repertoire, no scheme test), and it is right only because every case is one inserted unit inside an otherwise valid URL.
- It falls in the SCORECARD's control classes ("common-character allow-list", "misplaced gen-delims", "one component", "the percent-triplet rule", "generator-shape keyed") and outside the "not a control" class (it does not judge each component's characters against that component's repertoire). Whether authority parsing plus those six rules counts as "the work however written" is the L1's call; I hold no verdict, but under the written classes this is a control that meets the predicate, so kill rule (1) would apply before the claim is frozen.
- Component attribution: port inserts dominate every cheap tool's misses (146 of `union_blacklist`'s 170 misses; base passes port 239/239); the digits-only port rule alone lifts 1264 → 1412, and the remaining 22 are misplaced `[ ] : @ #`.

Checked statements. "Base scores 1049": holds (1049 at seed 41001, 1058 at seed 7). "Reference scores 1434": holds (1434, exit 0, at seed 41001, tool sha256 `6d7c2dd4…`). "1434 = 630 `loc` + 804 `sitemapUrl`": holds. "Constant-clean 805, all-`check_invalid` 813, every-entry-flagged 627": consistent within seed noise — my equivalents at seed 41001 are 798, 802, 632 and `oracleInvalid` moves 627–642 over four seeds. "A control cannot meet the predicate by skipping the declared work": wrong for this counter as written — `delimiter_proxy.py` meets it while skipping per-component judgment.

Limits and risks. The proxy's exactness rests on the counter's single-unit insertion shape; a second inserted unit, a component-wise percent-decode case or a case with an empty host would need more rules. No lane file, index or jj state was touched; the only lane write is this report. No tool installed, nothing upgraded.
