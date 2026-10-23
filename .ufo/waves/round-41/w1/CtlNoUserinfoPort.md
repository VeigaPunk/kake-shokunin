Port-only base-delegation variant `no-port-v2.py` reaches 1434/1434; it removes the repair's port regex, but the unchanged base `parts.port` still validates ports. The genuinely port-blind variants do not meet.
# CtlNoUserinfoPort — bounded mutation probe
Axes: operability (assigned detector separation); freshness (lane-owned, unchanged). No round judgment or integration performed.
All tool/receipt names below are relative to `S=/fast/scratch/hyaku/kake-r41w1/CtlNoUserinfoPort`; `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `C=$R/.ufo/waves/round-41/c1_count.py`.
Reference and counter SHA-256: `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`, `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`.
Mutation: replace only selected component regexes with permissive authority text; preserve the base TAB/LF/CR guard. `v2` excludes structural `@` from the port wildcard to prevent unrelated regex backtracking. `blind` additionally replaces `port = parts.port` with `port = None` (actual omitted port judgment).
Expected detector: pristine/restored meet; genuinely skipped userinfo or port judgments score below 1434. Same counter bytes and seed 41001 throughout.
## Actual results and retained tools
byField order is `loc,sitemapUrl`; byComponent order is `fragment,host,path,port,query,userinfo`, each component denominator 239. Every receipt has `note:null`, `toolExit:2` (expected mixed-invalid manifest), and 1434 cases; counter exit is listed separately.
| Tool | SHA-256 | Receipt | passed | byField | byComponent numerators | met / counter exit | Skipped work; caught cases; mutant verdict |
|---|---|---|---:|---|---|---|---|
| `probe.py` pristine/restored | `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a` | `pristine.json`, `restored.json` | 1434 both | 630/630,804/804 | 239,239,239,239,239,239 | true / 0 both | None; both baseline and restoration hold. |
| `no-userinfo-port.py` | `5e3b47323602a0078c44314901e17c89c5887cf9b8071f728cae8da31877fdc1` | `both.json` | 1362 | 609/630,753/804 | 239,237,239,239,239,169 | false / 1 | Both repair regexes omitted, base acceptance retained; 70 userinfo + 2 host misses; killed. |
| `no-userinfo.py` | `07535ba6d653eea0106593c81e9fcfcb072d281e9ae924baa2fda5ad2a1b166d` | `userinfo.json` | 1364 | 610/630,754/804 | 239,239,239,239,239,169 | false / 1 | Userinfo grammar omitted; 70 userinfo misses; killed. |
| `no-port.py` | `c555c905543c8d39de0893679156b5042ed7f6d7a638945835ee480aeed8692c` | `port.json` | 1431 | 628/630,803/804 | 239,237,239,239,239,238 | false / 1 | Port repair regex omitted; base port judgment retained; 2 host + 1 userinfo misses from wildcard backtracking; killed. |
| `no-port-v2.py` | `6e2f0fc38db68be9ba9a3add5b4938c245d398d9beb1bc2156a6bdcc7e6980e9` | `port-v2.json` | 1434 | 630/630,804/804 | 239,239,239,239,239,239 | true / 0 | Port repair regex omitted, base port judgment retained; no caught cases; survived (redundant regex ablation, not end-to-end port blindness). |
| `no-userinfo-port-v2.py` | `25aa838c644270a9528f0144fc1c20566f4a1c0f59fc2919974831290dd3074e` | `both-v2.json` | 1364 | 610/630,754/804 | 239,239,239,239,239,169 | false / 1 | Both repair regexes omitted, base acceptance retained; 70 userinfo misses; killed. |
| `no-userinfo-port-blind.py` | `74b24a65e0c0bba03532f5e7cbd9fc2f737a4a1e5dcccb5647d74afbdcb7415f` | `both-blind.json` | 1161 | 523/630,638/804 | 239,237,239,38,239,169 | false / 1 | Userinfo grammar and all port judgment omitted; 70 userinfo + 201 port + 2 host misses; killed. |
| `no-port-blind.py` | `e0f10d9825ba0354e475c82b73874c9f186bde1bf3fe3887b9c4c8733c783ed7` | `port-blind.json` | 1231 | 543/630,688/804 | 239,237,239,38,239,239 | false / 1 | All port judgment omitted; 201 port + 2 host misses; killed. |
## Exact score commands (expand S/R/C as defined above)
```sh
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/probe.py" --label CtlNoUserinfoPort-pristine --seed 41001 --out "$S/pristine.json" # exit 0
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-userinfo-port.py" --label CtlNoUserinfoPort-both --seed 41001 --out "$S/both.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-userinfo.py" --label CtlNoUserinfoPort-userinfo --seed 41001 --out "$S/userinfo.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-port.py" --label CtlNoUserinfoPort-port --seed 41001 --out "$S/port.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-port-v2.py" --label CtlNoUserinfoPort-port-v2 --seed 41001 --out "$S/port-v2.json" # exit 0
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-userinfo-port-v2.py" --label CtlNoUserinfoPort-both-v2 --seed 41001 --out "$S/both-v2.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-userinfo-port-blind.py" --label CtlNoUserinfoPort-both-blind --seed 41001 --out "$S/both-blind.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/no-port-blind.py" --label CtlNoUserinfoPort-port-blind --seed 41001 --out "$S/port-blind.json" # exit 1
timeout 900 prlimit --as=4000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/probe.py" --label CtlNoUserinfoPort-restored --seed 41001 --out "$S/restored.json" # exit 0
```
## Findings / checked statements
- **holds:** omitting userinfo judgment is detected here: `$S/no-userinfo.py:78`, `userinfo.json:29-34` malformed `%4G`, `:37-41` U+0010; 70 total userinfo misses include malformed percent triplets, controls, space, forbidden punctuation, and split-triplet insertions.
- **holds:** actual port blindness is detected: `$S/no-port-blind.py:81,125`; `port-blind.json:29-47` includes `:4u0`, `:7%414`, `:9a3`; 203 total misses (201 generator-port, 2 generator-host cases whose inserted colon changes the parsed component). Receipts cap detailed misses at 200, so totals use byComponent.
- **wrong:** deleting the repair's port regex necessarily scores below target: `$S/no-port-v2.py:81` reaches 1434. This surviving ablation is a coverage observation, not authority to change the contract.
- **overstated:** calling that survivor an end-to-end port skip: `$S/no-port-v2.py:125` still reads `parts.port`; `/usr/lib/python3.14/urllib/parse.py:176-185` requires ASCII digits and 0–65535. It delegates the named work to the unchanged base parser, so is not evidence of a fully port-blind tool meeting.
- **holds:** reference bytes restored exactly. Before hash `6d7c2dd445fc7d3b2df7c3307d18f05c7f2cf6154830430dbc15dd372509010a`; final-mutant probe hash `e0f10d9825ba0354e475c82b73874c9f186bde1bf3fe3887b9c4c8733c783ed7`; after hash equals before. `timeout 30 prlimit --as=4000000000 -- cmp -s "$S/probe.py" /fast/scratch/hyaku/kake-r41/shared/ref_fix.py` exit 0; following bounded `sha256sum` prints that same reference hash for both files. Restored detector again 1434/1434, exit 0.
No baseline failure; six killed ablations and one surviving redundant-regex ablation; no inconclusive runs. Only the assigned sandbox and this report were written; no network, package installs/updates, background processes, or lane-source changes. Retained variants are measurement artifacts, not a shipped repair.
