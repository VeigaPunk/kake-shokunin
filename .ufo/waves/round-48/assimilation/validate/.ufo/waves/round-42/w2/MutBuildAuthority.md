NOT MET — counter v3 (`ce2d5a0c…`) admits a control: the landed byte-table build with a five-digit cap on the
port scan (`M8-port-five-digits`, sha256 `391608309640…`) **meets** the frozen predicate on two independent
seeds and judges `http://host.example:0000080/` differently from the round-41 tool. Kill rule (2) fires.

# Method
Attacked the landed build's userinfo / host / port scan (`scripts/sitemap_audit.py` at `020bc457`, tool sha256
`914ebdee…`): `_TABLE_USERINFO`, `_TABLE_REGNAME`, the `@` split in `_uri_ok` and the `:` port loop in `_scan`.
Detector = the frozen counter, no `--seed`; baseline = sandbox copy `build.py` (sha256 `914ebdee…`, byte-equal
to the lane file) whose `_parse_url` equals the round-41 tool's on all 26 hand witnesses (True) — detector sound.
Every tool is `build.py` with one localized change; receipts in `/fast/scratch/hyaku/kake-r42w2/MutBuildAuthority/`.
Command (each tool, exit 0 met / 1 not met):
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py --root . --tool-file <tool> --label MutBuildAuthority-<tag> --out <receipt>`
Baseline `build.py` bytes were never edited; lane file sha256 re-checked after the runs (`914ebdee…` unchanged).

# Tools (dir `/fast/scratch/hyaku/kake-r42w2/MutBuildAuthority/`)
| tool | sha256 | one-member change | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | caught by |
|---|---|---|---|---|---|---|---|
| M1-regname-at.py | 2a27cf27ea594c6e… | `_REGNAME_ASCII` gains `@` | 190728216666685 | 8/10 | 0.936/1.371/1.322/1.307/1.140 | no | A, E |
| M2-userinfo-at.py | 08315ffd18413774… | `_TABLE_USERINFO` built with `+ b"@"` (one table byte) | 176022259041779 | 7/10 | 1.045/1.339/1.394/1.315/1.183 | no | A, D, E |
| M3-userinfo-no-nonascii.py | 8cfd2c2c71cba145… | userinfo table `non_ascii=False` (bytes 0x80–0xFF flipped) | 208680092354378 | 8/10 | 1.063/1.263/1.374/1.208/1.180 | no | D, E |
| M4-port-empty.py | 129999225794c060… | port branch returns False when `:` has no digit | 255519833345354 | 7/10 | 1.027/1.431/1.433/1.351/1.175 | no | A, D, E |
| M5-empty-userinfo.py | 408e98889dd2bd53… | `@` split requires non-empty userinfo (`at < info_end`) | 92197510405589 | 8/10 | 1.011/1.706/1.389/1.288/1.169 | no | A, D |
| M6-port-digit9.py | 591820e591b2564b… | port digit bound `0x39`→`0x38` | 7377184409841 | 6/10 | 1.023/1.538/1.414/1.202/1.106 | no | A, B, D, E |
| M7-start-order.py | 554373c5f3942167… | `starts = (at, info_end + 1)` order swap (equivalent rewrite, apparatus control) | 275058546627076 | 10/10 | 1.076/1.174/1.336/1.458/1.364 | **yes** | none |
| M8-port-five-digits.py | 391608309640431a… | port loop stops after 5 digits (`seen < 5`) | 181283774493343 | 10/10 | 1.003/1.469/1.342/1.164/1.122 | **yes** | none |
| M8 (re-score) | same | same | 223355685332418 | 10/10 | 1.1315/1.6811/1.6444/1.3052/1.1558 | **yes** | none |

# Witnesses (mutant `_parse_url` vs round-41 `_parse_url`; run-A values reproduced from the receipts' seeds with
the counter's own generators)
- M1 (A): `httP://:@x1kn9,nA@4k%143k.org/i10tlsv` → mutant `('http','4k%143k.org',80,'/i10tlsv')`, tip41 `None` (accepts a double-`@` host).
- M2 (A): `hTtps://w6%Fct!le:0fZu@r1%97b*.example/bqs2wf,3/u6:Cu'` → `None` vs `('https','r1%97b*.example',443,…)`; 215 such A-values.
- M3 (D): `hTtP://hb%F5b:5hm5āu&xjf@imNxsdEj.test/30%EfEe82p/wqj%09%9E%eC.coo` → `None` vs `('http','imnxsdej.test',80,…)`; (E): `http://any&w8:q\x80hSZ@ox6d.com/tmfJ` → `None` vs `('http','ox6d.com',80,'/tmfJ')`.
- M4 (A): `Http://uzp%D6%644.net.:/k9eitj` → `None` vs `('http','uzp%d6%644.net.',80,'/k9eitj')` (empty port).
- M5 (A): `httPs://@gi6f%DDt0i.com/e9%93q2'6wH` → `None` vs `('https','gi6f%ddt0i.com',443,…)` (empty userinfo).
- M6 (A): `hTtP://wr9aDnF.org:89//hf8)m%5d9?bp62a4sx~@` → `None` vs `('http','wr9adnf.org',89,'//hf8)m%5d9')`.
- **M8 control witness**: `http://host.example:0000080/` → M8 `None`, tip41 `('http','host.example',80,'/')`; CLI on `cli/m.json`+`cli/s.xml`: build and tip41 exit 0 `{"verdict":"clean"}` (out sha256 `e2108664…`), M8 exit 1 `failed-policy`, `loc_not_absolute` entry 1 (out sha256 `6220232920…`).
- M7: none found — `_parse_url` equal to tip41 on all 10,229 values the counter generates at seed 208680092354378 (A–E) and on the 26 hand witnesses; met, therefore behaviour-equal, **not a control**.

# Why the port cap escapes (coverage gap, path:line)
`scripts/sitemap_audit.py:198` is the mutated loop; the counter never generates a 6+ digit port:
`c42_count_v3.py:188` `str(rng.randint(10,99))` + ≤1 inserted unit, `:254` `randint(1,65535)`, `:333`
`str(rng.randint(10,9999))` + 1 unit; `long_value` heads carry no port; `.ufo/waves/round-41/realrun/*.xml` has
no `:[0-9]{6,}` at all (grep empty), so T4 cannot reach it either. The frozen differential's port list
(`equivalence/equiv_diff.py:18`, `…"08","0x50"`) has no leading-zero form longer than 5 digits, so it misses it
too. `urlsplit` normalises leading zeros (`int("0000080")==80`), so every port of 6–N digits numerically ≤65535
is a value the round-41 tool accepts and a length-capped scanner rejects; the cap survives on any seed.

# Statement audit
- "counter v3 keeps the round-41 tool's judgments on the URL rule" for the my area tables/`@`/`:` membership: **holds** — 6/6 single-member mutants killed, each with a generated-corpus witness in A, B, D or E.
- Same claim as a guarantee of the port rule: **overstated** — M8 meets twice; the port length class is unrepresented.
- "Kill rule (1) does not fire under v3 / no control met v3" (build-scored section, wave 1): **wrong after this seat** — kill rule (2) fires with M8 (met + witness).
- Counter docstring "every unit … inserted … port": **holds** (unit set is exhaustive); implicit completeness of port *lengths*: **wrong**.
- Apparatus: build == tip41 on 26 hand witnesses, M7 equivalent rewrite meets with no witness: **holds** (a `met` without witness is correctly not a control; a `met` with witness, as M8, is).
