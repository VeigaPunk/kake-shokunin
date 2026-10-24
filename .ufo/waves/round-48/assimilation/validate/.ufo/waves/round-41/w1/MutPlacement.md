# MutPlacement — wrong-string RFC-check mutations
**Survivors first: first2048, locLong16, strip — each 1434/1434, met=true, counter exit 0.**
Axes: operability (tested); freshness (pinned inputs, unchanged). Local mutation findings only; L1 owns integration/scoring.
Built 10 independent single-defect mutants; 7 killed, 3 survived, 0 inconclusive. No network or installs.
Artifacts: `/fast/scratch/hyaku/kake-r41w1/MutPlacement/mutants/<name>.py`; mutable probes in `probes/`; receipts `<name>-<phase>.json`.
Counter: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py`, SHA256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`.
Reference before/after and all restored probes: SHA256 `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`.
Expected detector for each defect: counter exit 1, passed<1434, provided pristine/restored phases meet.
Each named mutant received the same seed-41001 pristine → mutated → restored detector; two counters at once, 900s/4GB limits.
Exact 30 executed commands, exits, outputs, all phase counts/hashes: `/fast/scratch/hyaku/kake-r41w1/MutPlacement/probe-results.json`.
One exact command (others expanded in the ledger):
`env TMPDIR=/fast/scratch/hyaku/kake-r41w1/MutPlacement/tmp timeout 900 prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/MutPlacement/probes/strip.py --label MutPlacement-strip-mutated --seed 41001 --out /fast/scratch/hyaku/kake-r41w1/MutPlacement/strip-mutated.json` → exit 0.
Result columns: passed denominator 1434; L/S denominators 630/804; component order fragment,host,path,port,query,userinfo (each /239).
| Tool/location under mutants/ | One behavior change | SHA256 | passed | L,S | Components | met;exit | Verdict |
|---|---|---|---:|---|---|---|---|
| `first2048.py:113` | check value[:2048] | `60e1b7f29a1c5cdcc31bb589a4b754303ca2971dab311b2efe3953c0ab042704` | 1434 | 630,804 | 239,239,239,239,239,239 | true;0 | survived |
| `locLong16.py:110,113,329` | strict loc check only if len>16 (one guard; signature/guard/call plumbing) | `852509f3f9a79a528f0ed95aca82bb932eaf0f7f06dade5d6dd994d56c67c4b6` | 1434 | 630,804 | 239,239,239,239,239,239 | true;0 | survived |
| `strip.py:113` | check value.strip() | `dd1fca7bbda110604ca2d242d0e2d87afb03e774e7cf70773af13f10b405ed80` | 1434 | 630,804 | 239,239,239,239,239,239 | true;0 | survived |
| `dropFragment.py:113` | check prefix before first # | `7283cfcf00bdee1e69bb6935a048c2f60a12688534061726fc2f3313701a2881` | 1343 | 600,743 | 151,239,237,239,238,239 | false;1 | killed |
| `dropQuery.py:113` | check prefix before first ? | `fb0d516a441e90ba3b46f96fb4a7093b7fd127c9080e5190d53111e03a266e78` | 1301 | 585,716 | 199,239,238,239,147,239 | false;1 | killed |
| `first20.py:113` | check value[:20] | `36a3c5b1adb090bd1aa04f1401655680afd7802914868a4e97676efcc9f977bd` | 1046 | 471,575 | 142,223,152,231,133,165 | false;1 | killed |
| `geturl.py:115` | check parts.geturl() inside existing try | `6df5e25e944a382f4ed292602044ec72db115126da3399bfabf123e5a66440a0` | 1398 | 612,786 | 233,233,233,233,233,233 | false;1 | killed |
| `lowerUpperHex.py:113` | check lowercased value with upper-case-only hex | `538ae9674491d0d5fefe0933f11f557a876be8e48040366f834853286a682653` | 817 | 319,498 | 119,125,120,217,127,109 | false;1 | killed |
| `skipFragment.py:113` | skip RFC check if # is present | `f732161b34085384479999d4cbc96bbb7f61b0989d8db3245188a13082afebaa` | 1274 | 573,701 | 151,225,219,239,218,222 | false;1 | killed |
| `skipQuery.py:113` | skip RFC check if ? is present | `32ae0b19767b5f368bc983e6b39c11562e50d8b919f363f01f7b8a917458381f` | 1219 | 554,665 | 199,215,207,238,147,213 | false;1 | killed |
**All ten pristine phases AND all ten restored phases:** passed=1434; byField={loc:630/630,sitemapUrl:804/804}; byComponent={fragment:239/239,host:239/239,path:239/239,port:239/239,query:239/239,userinfo:239/239}; met=true; exit=0; tool SHA256 equals the reference above.
Restoration evidence: every actual probe was restored byte-exact (including final LF); counter toolSha256 before=after for each, plus final sha256sum exit 0. Archived mutant bytes remain available, hashes equal the scored mutated bytes.
Findings / checked statements:
- **holds:** the bounded seed-41001 detector rejects geturl, first20, lowerUpperHex, query/fragment bypass and query/fragment truncation defects (table).
- **wrong:** “this detector kills every assigned wrong-string/check-placement defect”: three explicit survivors (mutants/first2048.py:113, mutants/locLong16.py:113,329, mutants/strip.py:113).
- **overstated:** “1434/1434 demonstrates judgment of every written URL”: `.ufo/waves/round-41/c1_count.py:102-119,122-163` uses bounded fills and interior insertion only; these three defects are not distinguished.
- [INFERENCE; not executed] strip accepts manifest ` https://x/a`; locLong16 accepts loc `https://x/a^`; first2048 accepts manifest `https://x/` + 2100 `a` + `^`. Each written value violates URI grammar, while the checked string/branch does not.
All counter notes were null. The mixed valid/invalid manifests make audited-tool exit 2 normal; counter exits above, not that tool exit, determine verdicts.
No detector rerun was needed after a receipt-display truncation; compact JSON reads recovered outputs. All bounded processes exited; no jobs/services remain.
Tools installed/updated: none. No lane source, shared reference, index, or sibling file was changed.
