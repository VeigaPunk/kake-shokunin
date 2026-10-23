# MutStructure — survivors first
Axes: operability (structural-mutant detection); freshness unchanged. Eleven independent one-line mutants; seed 41001; 33 counter runs: pristine → mutated → restored for each.

## Survivors and declared class
- `m03_empty_host` survives 1434/1434. Outside the effective skip-work class: only `_rfc3986_uri` loses the empty-host guard (`ref_fix.py:94`); `_parse_url` still rejects it at `ref_fix.py:121–122`. [INFERENCE] This is a masked/equivalent tool mutant, not demonstrated acceptance of an empty host.
- `m06_path_question` survives 1434/1434. Inside the literal single-structure/add-one-component-member class (`SCORECARD.md:2737–2739`): adds `?` to path segments (`ref_fix.py:82`). [INFERENCE] Its accepted URI language is unchanged: the first `?` can instead begin the existing query, which already permits every path character plus `/` and `?` (`ref_fix.py:83`); downstream parsing is unchanged.
- `m08_scheme_leading_digit` survives 1434/1434. Outside the effective skip-work class: `_URI_RE` permits a digit first (`ref_fix.py:77`), but `_parse_url` still requires a recognized http/https scheme (`ref_fix.py:116–119`); scheme is not one of the six generated components (`c1_count.py:44,124`). [INFERENCE] No tool-level grammar violation is established.
Classifications and equivalence caveats were recorded in `manifest.json` before scoring; no contract is changed. Round judgment belongs to L1.

## Method and evidence
`R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `S=/fast/scratch/hyaku/kake-r41w1/MutStructure`. All mutant artifacts are `$S/mutants/<m>.py`; the counter scored byte-identical `$S/probes/<m>.py` copies.
Expected detector: the unchanged C1 counter returns exit 1 / met=false when a mutant disagrees with its RFC oracle; baseline failure would make that mutation inconclusive.
Exact command template (33 expansions in `$S/commands.json`, each with actual output and exit): `timeout --kill-after=5 900 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r41w1/MutStructure/probes/<m>.py --seed 41001 --label MutStructure-<m>-<p> --out /fast/scratch/hyaku/kake-r41w1/MutStructure/<m>-<p>.json`, with p = pristine, mutated, restored.
Counter SHA256: `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`. Pristine/restored reference SHA256: `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`.
Every one of the 22 pristine/restored runs: passed=1434/1434; byField={loc:630/630,sitemapUrl:804/804}; byComponent={userinfo:239/239,host:239/239,port:239/239,path:239/239,query:239/239,fragment:239/239}; met=true; counter exit=0. Each receipt independently hashes the actual bytes.
Full receipts: `$S/<m>-<p>.json`; exact commands, outputs, per-run hashes and compact findings: `$S/commands.json`; pre-score edits/classes: `$S/manifest.json`.

## Per-mutant output (survivors first)
Each tool path is `$S/mutants/<m>.py`; source line is unchanged. Component vector order: userinfo, host, port, path, query, fragment; every denominator is 239. Field denominators: loc=630, sitemapUrl=804; passed denominator=1434.
| Mutant : line | Single change | Tool SHA256 | passed | loc / sitemapUrl | byComponent numerators | met | counter exit | verdict |
|---|---|---|---:|---|---|---|---:|---|
| `m03_empty_host:94` | delete early empty-host condition | `4b1a504cf11a45463e502f930352b02333e8d21d56eb1fd75ca6e2feb39ca4c3` | 1434 | 630 / 804 | 239,239,239,239,239,239 | true | 0 | survived |
| `m06_path_question:82` | add ? to path-segment repertoire | `0681806c2820985a7a5b14d87b21018b27762ec5268de8eb05324ad218076c83` | 1434 | 630 / 804 | 239,239,239,239,239,239 | true | 0 | survived |
| `m08_scheme_leading_digit:77` | initial scheme class adds 0-9 | `00e21862073a791779bf9c78855fd1179ef36ef17c4ec96c157b88dd623cedb4` | 1434 | 630 / 804 | 239,239,239,239,239,239 | true | 0 | survived |
| `m01_pct_one_hex:74` | percent hex count {2}→{1} | `40281dab919f13ed4cbd61855933e7ad8f7460c036f00d9ee3d2b8c85964f3a3` | 1372 | 603 / 769 | 231,225,239,232,220,225 | false | 1 | killed |
| `m02_pct_uppercase_only:74` | pct hex [A-Fa-f]→[A-F] | `bd727c3a5915bd4a98040b75e6fe478a61f3ab2befa42ea8e4f31805c40db891` | 951 | 386 / 565 | 137,142,228,147,153,144 | false | 1 | killed |
| `m04_port_digits_removed:81` | optional port [0-9]* removed | `bcf71a750cee3d9e5bdccb3e5dcc99b254977730a54ad5299634368a62a0aa47` | 1333 | 573 / 760 | 221,218,213,224,226,231 | false | 1 | killed |
| `m05_second_at:78` | add @ to userinfo repertoire | `12e8c028746dac245a9efd8ccf2efd0bb3aae5d8a27a1197234c10f2ac01e163` | 1433 | 629 / 804 | 238,239,239,239,239,239 | false | 1 | killed |
| `m07_query_hash:83` | query [/?]→[/?#] | `ac4b93e73196b6c86ed39b271d120f4408b761da12bec28fcb86869dfbd8a1bd` | 1432 | 629 / 803 | 239,239,239,239,238,238 | false | 1 | killed |
| `m09_drop_end_anchor:84` | remove final URI \Z | `3bcd1062f7d2d1a01abc64d00eb3166701e74da348856cc4622e785e361760cf` | 1013 | 491 / 522 | 163,159,233,160,147,151 | false | 1 | killed |
| `m10_pct_values_only:113` | guard RFC check with contains-% | `af5fa52690c9fd534976fde454fcce99f8f6269420c60a81dff995734f47ea00` | 1392 | 619 / 773 | 233,229,237,231,230,232 | false | 1 | killed |
| `m11_port_unrestricted:81` | port [0-9]*→[^/?#]* (additional digits-rule interpretation) | `c2a8b2e268de35d88a3a47977bd735fdb958a1d326a39ff20faabafbade8ff0c` | 1425 | 625 / 800 | 238,237,233,239,239,239 | false | 1 | killed |

## Checked statements and restoration
- **Wrong:** an unrestricted statement that the counter kills every assigned structural mutant; observed 8 killed, 3 survived, 0 inconclusive. This is not a round verdict.
- **Holds:** all 11 pristine baselines and all 11 restored copies meet the same detector; all mutant scores have note=null. Byte hashes in mutated receipts equal retained mutant artifacts; every before/after probe hash equals the reference hash above.
- **Overstated:** treating these three survivors as observed incorrect URL judgments. Two retain downstream enforcement; the path/query boundary mutation appears language-equivalent. No additional distinguishing behavioral check was run.
- **Holds:** each mutant changes exactly one source line/occurrence, not a cumulative patch. Original reference and lane implementation/counter were never edited. The only lane write is this report.
Initial hash command (exit 0): `timeout 30 prlimit --as=4000000000 sha256sum /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py`.
Final hash command (exit 0): `timeout 30 prlimit --as=4000000000 sha256sum /fast/scratch/hyaku/kake-r41/shared/ref_fix.py /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/c1_count.py /fast/scratch/hyaku/kake-r41w1/MutStructure/reference.py /fast/scratch/hyaku/kake-r41w1/MutStructure/mutants/*.py /fast/scratch/hyaku/kake-r41w1/MutStructure/probes/*.py`; shared reference unchanged, all 11 probes restored exactly, all 11 mutant artifacts retained for L1 rescoring.
Two counter runs at a time; every started command completed. No network, installs, upgrades, extra runtime, repository mutations or background jobs. Only seed 41001 was exercised; no all-seed detection claim.
