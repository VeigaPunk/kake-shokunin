# ConnectorC — round 77, attempt 1, wave w1

Seat ConnectorC (connector, leaf, read-only). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`,
base `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`, contract `.ufo/waves/round-77/contract.md` read first.
Nothing in this seat redefines C1, C2, their predicates, or the axes. No lane file was edited except
this report and the three id files under `.ufo/waves/round-77/assimilation/` that item 2 orders the
connector to produce. No sibling bytes were imported into kake; overlap is reported, never copied.
Scratch `/fast/scratch/hyaku/kake-r77/ConnectorC` (used for the guard proof only) was deleted before
yield.

Axis reading used for the move (item 5): calibration 2 HOLD, operability 10 HOLD, freshness 10 HOLD.
This seat measures the round's own self-description against committed bytes; it moves no score.

---

## 1. Sibling overlap

Population: the 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (kake excluded).
`/home/vgpnk/Projects/kimi-shokunin/` is the only `*-shokunin` outside `shokunin/`; it holds
`commands/ docs scripts skills templates` and no `.ufo/`, no `corpus/`, no `SHONEN.md`, no sitemap
surface — no overlap.

### 1a. Sitemap-format audit (gzip / plain text / RSS / Atom)

Searched names and content across every sibling:

```sh
find /home/vgpnk/Projects/shokunin -maxdepth 8 -iname '*sitemap*' \
  -not -path './kake-shokunin/*' -not -path '*/node_modules/*' \
  -not -path '*/.git/*' -not -path '*/.jj/*'
```
→ exactly 2 hits, both **fetched fixtures**, not tools:
`mado-shokunin/.ufo/waves/round-18/fetch/SrcWalkerDocsSite/gitbook-sitemap.xml` and
`…/gitbook-sitemap-pages.xml` (round-18 evidence captures of a docs site).

```sh
for d in */; do grep -rIl --include='*.py' --include='*.js' --include='*.ts' \
  -E 'sitemapindex|urlset|52.?428.?800|52428800|application/rss|atom\+xml' "$d"; done
```
→ no sibling hit. Three false positives were opened and dismissed:
- `tabi-shokunin/corpus/evidence/round-13/aria/node_modules/playwright*` — vendored bundle text.
- `tsukuroi-shokunin/.ufo/waves/round-44/make-w1-spec.py:73` — `52428800` is `devinfo/2` `scrub_speed_max` for a btrfs probe, unrelated to sitemap bytes.
- `chousa-shokunin/.ufo/waves/round-29/build/ExecTool/quote-reopen.py:213-215,282` — `gzip` is HTTP `Content-Encoding` decompression (`wbits = 16 + zlib.MAX_WBITS`), not a container-format decision; no sitemap, no text sitemap, no feed.

**Verdict: kake C2 duplicates no sibling artifact.** No lane holds a container/format matrix, a
decompressed-size rule, a plain-text-sitemap reader, or an RSS/Atom entry reader. C2 is the first
such tool in the fleet tree under `shokunin/`.

### 1b. SHONEN / promotion-box ledger

Every one of the 20 siblings carries `SHONEN.md` with exactly 4 boxes (fleet seed
`.ufo/waves/round-13/shonen-seed.txt`; the seed is 4 lines of `- [ ] <predicate>` under
`# <name> — Promotion checklist`). Measured per lane:

```sh
for d in */SHONEN.md; do lane=${d%%/*}; ev=$(grep -c '^      Evidence: ' "$d"); \
  boxes=$(grep -cE '^- \[[ x~]\] ' "$d"); marked=$(grep -cE '^- \[(x|~)\] ' "$d"); done
```

| lane | boxes | marked `x`/`~` | `Evidence:` lines | SHONEN instrument | duplicates kake C1? |
|---|---|---|---|---|---|
| kasegi-shokunin | 4 | 3 | 4 | `corpus/instruments/shonen-form.py` (79 ln), `shonen-form-selftest.py`, `shonen-shipped-fixtures.json`, `shonen-shipped-fixture-check.py` | **partly** — grammar + pointer validity + `x` needs non-author attestation (see below) |
| audio-shokunin | 4 | 3 | 0 | `reports/round-1-calibration/count_checklist.py` (52 ln) | **partly** — box parse, canonical-predicate check, evidence resolution at a revision (see below) |
| chousa-shokunin | 4 | 4 | 0 | report `round-43/w1/ScribeShonen.md` (marks `~`, refuses `x` without a non-author) | no |
| game-dev-3d-shokunin | 4 | 1 | 0 | `reports/round-106/shonen-draft.md` | no |
| kotodama-shokunin | 4 | 4 | 0 | `reports/round-23/shonen-survey.md`, `reports/round-32/dossier-d11-shonen-boxes.md` | no |
| game-dev-2d | 4 | 3 | 0 | — | no |
| kagi, kama, kengaku, kotoba, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi | 4 each | 4 each | 0 | — | no |
| kaidoku, kumitate | 4 each | 0 | 0 | — | no |
| **kake** (this lane) | 4 | 0 | 0 | C1 builds one this round | — |

What the two closest siblings actually hold, with the exact rules, because "partly" needs a boundary:

- **audio `count_checklist.py`** (read in full, 52 lines): `git show <rev>:SHONEN.md`,
  `re.split(r"(?m)^- \[([x~ ])\] ")`, `PREDICATES` compared against the 4 seed predicates, and
  `resolved = [path for path in references if path in paths]` where `paths = git ls-tree -r` at the
  same revision; outputs `boxes`, `canonical_predicates`, `boxes_with_resolvable_evidence`,
  `checked_without_resolvable_evidence`, `checked_boxes`, `asserted_boxes`, `open_boxes`.
  That is C1's *derivation* layer: box parse, seed-predicate check, evidence pointer resolved at
  `<rev>`, and `x`-without-evidence counted. It is **not** a ledger: no per-box `status`
  (`evidenced`/`gap`), no recorded `observed` re-derived and compared (so it cannot produce C1's
  mismatch class (d)), no `reason`/`flip`, no `verifier` field.
- **kasegi `shonen-form.py`** (read in full, 79 lines): `- [m] <label>` + an indented
  `      Evidence: <pointer> — <note>` line; pointer rules are `path.is_absolute()` → `SF-POINTER`,
  `'..' in path.parts` → `SF-POINTER`, `token != path.as_posix()` → `SF-POINTER` (rejects `./` and
  doubled separators), `resolved.is_relative_to(root)` and `is_file()`; `mark == 'x'` →
  `SF-VERIFIER` with the in-source reason "This author-side checker cannot attest independence."
  That is C1's *pointer grammar* and C1's `x ⇒ verifier` rule in executable form, for one lane's
  hard-coded preamble (`# kasegi-shokunin — Promotion checklist`), and it is a form gate only
  ("never promotion or semantic truth").
- No sibling holds a `shonen-ledger/v1` file: `grep -rIl -E 'shonen-ledger|"unexamined"'` over the
  tree returns no sibling instrument, and `find -iname '*ledger*.json'` returns none matching a
  SHONEN ledger.

**Verdict.** Kake C1 would duplicate no sibling *ledger*: the ledger layer (per-box status, recorded
`observed` re-derived at `<rev>`, mismatch on disagreement, `reason`+`flip` for gaps, `verifier` for
`x`) exists nowhere in the sibling set. It would reuse two already-invented layers — audio's
derivation and kasegi's pointer grammar — and that reuse is free because both are per-lane
instances, not shared fleet tools: the fleet ships only the seed
(`.ufo/waves/round-13/shonen-seed.txt`); `scripts/` and `templates/` contain no SHONEN parser.

Base-rate observation (report only, not a claim, no sibling instrument run): **18 of 20 siblings
mark at least one box `x` or `~` with zero `Evidence:` lines**, and 6 of them mark all four. Kake C1's
mismatch class (a) — a marker that asserts more than its row supports — is therefore the fleet's
normal state, not kake's peculiarity. That raises the assimilation value of C1 and also warns that a
later cross-lane reuse must not be presented as "kake is ahead"; the predicate is what is new.

---

## 2. Assimilation id-collision check (contract §Frontier)

Command, run verbatim as specified (fleet root cwd irrelevant; all paths absolute):

```sh
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-77/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kake/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Observed:

```
reg count: 184
staged count: 129
collision count: 8
```

Additional measured context (same files):
```
reg ids in [S287,S415]: 8
reg ids below S415: 153
reg total: 184
max id anywhere in SOURCES.md: S446
unique S-ids anywhere in SOURCES.md: 184   (row position: 184 — no id used outside a row)
```

### `$A/reg-ids` (184)

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020
S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040
S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060
S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080
S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100
S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124 S125 S126 S127 S128 S129 S130 S131 S132 S133 S134 S135 S136 S137 S138 S139
S249 S262 S263 S273 S274 S286
S312 S329 S367 S372 S373 S374 S390 S409
S416 S417 S418 S419 S420 S421 S422 S423 S424 S425 S426 S427 S428 S429 S430 S431 S432 S433 S434 S435
S436 S437 S438 S439 S440 S441 S442 S443 S444 S445 S446
```

### `$A/staged-ids` (129)

```
S287 S288 S289 S290 S291 S292 S293 S294 S295 S296 S297 S298 S299 S300 S301 S302 S303 S304 S305 S306
S307 S308 S309 S310 S311 S312 S313 S314 S315 S316 S317 S318 S319 S320 S321 S322 S323 S324 S325 S326
S327 S328 S329 S330 S331 S332 S333 S334 S335 S336 S337 S338 S339 S340 S341 S342 S343 S344 S345 S346
S347 S348 S349 S350 S351 S352 S353 S354 S355 S356 S357 S358 S359 S360 S361 S362 S363 S364 S365 S366
S367 S368 S369 S370 S371 S372 S373 S374 S375 S376 S377 S378 S379 S380 S381 S382 S383 S384 S385 S386
S387 S388 S389 S390 S391 S392 S393 S394 S395 S396 S397 S398 S399 S400 S401 S402 S403 S404 S405 S406
S407 S408 S409 S410 S411 S412 S413 S414 S415
```

### `$A/collisions` (8)

```
S312 S329 S367 S372 S373 S374 S390 S409
```

**Renumber map: none.** No staged id needs renumbering to be free of an id collision, because only 8
of the 129 collide and 121 are free in the registry's id space. The collision is not an id-space
exhaustion; it is eight staged rows pointing at documents the lane later re-mined under the *same*
id (see item 4). Any renumber map produced later must be content-derived, not id-derived — item 5.

### Guard-bite proof (synthetic, in scratch)

Built `/fast/scratch/hyaku/kake-r77/ConnectorC/reg.md` (3 rows: col-0, indented, col-0) with an
indented row carrying a staged id, then ran the 0–3-space parser and the column-zero-only parser:

```
$ cat -A reg.md
| S900 | scratch-a | $
  | S312 | indented-collider |$
| S901 | scratch-b |$

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+' | sort
S312 S900 S901
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' reg.md | grep -oE 'S[0-9]+' | sort
S900 S901

0-3-space collisions: S312
col0-only collisions: []
```

So an indented `  | S312 |` row is caught by the frozen form and silently missed by the
column-zero form. **Caveat, and it is material:** this guard is *forward-looking only* on today's
bytes. Both real files contain no indented row:

```
reg    col0=184 indented(1-3)=0 tabs=0
staged col0=129 indented(1-3)=0 tabs=0
col0 parser output == 0-3 parser output: reg=yes staged=yes
col0 collisions=8   (same 8 as the frozen form)
```

The 0–3-space tolerance bites only if a formatter or a copy-paste indents a row; on the committed
pair the two parsers are interchangeable. A round record that says the guard "was shown to bite on
the lane's rows" would overclaim; it was shown to bite on a synthetic row.

---

## 3. `considerthese/2026-10-26.md` §Part 2 — five proposals

Read-only; that file was not edited. Proposals quoted from `2026-10-26.md` §Part 2 (added
`fdae359f`, 2026-10-26).

| # | proposal | implemented in | evidence |
|---|---|---|---|
| 1 | Read the lane's own tools instead of duplicating them (read `id_resolver` / `landed_check` / frontier-map receipts daily, report only a change or a red) | **unimplemented** | `corpus/lessons/round-67.md:127-131`: "proposals 1–4 evaluated; none adopted … proposals 1/3 need surfaces this host lacks"; `.ufo/waves/round-71/w1/ScoutConsider.md`: "Proposal 1 … personal reflector workflow, not lane-implemented". No receipt-reading practice exists: `grep -rn -E 'id_resolver\|landed_check' .ufo/reports/round-6*.md .ufo/reports/round-7*.md` → 0 hits. |
| 2 | Receipt-rewrite watch (list `controls/` files with >1 commit, flag changed `revision:`/result lines) | **r58** — `.ufo/waves/round-58/c58_receipt_rewrites.py` | Added `fff3eea6` 2026-10-26; the proposal file `fdae359f` is an ancestor of that commit (`git merge-base --is-ancestor` → true), so the counter postdates the proposal. Contract text at the file head: population = every file under any `control(s)/` dir, first-addition-in-a-deleting-commit, `pin-only`/`content`/`pending-fill` kinds. |
| 3 | Operator-decision queue (rows needing the operator, with rounds waited) | **r59, once** — `.ufo/waves/round-59/w1/ScribeConsiderthese.md` | Added `cdf089b1` 2026-10-26. It is a one-round inventory: a 9-row table with "First raised / Waited / Current state", closing with "Filing them is integrator work under the L0 durability rule". No standing queue exists afterwards — `grep -rn -iE 'decision-required\|operator-decision\|queue' .ufo/reports/round-7*.md` → 0 hits; r67 records proposal 3 as not adopted. |
| 4 | Gate-agreement ledger (verifier agree/disagree count per round) | **unimplemented as a ledger; a count exists** | `.ufo/waves/round-62.md`-adjacent Gate: `corpus/lessons/round-62.md:13` records it "not implemented" with an explicit flip condition ("repeated verifier/gate comparisons show a durable need to summarize more than the specific cases already recorded"). r67 repeats "proposal 4 is verifier-side data, not lane-ownable". But `.ufo/waves/round-66/c66_gate_status_hostportable.py:677-688` computes and prints `agreement` = members with zero v1-class label mismatches (r66 `agreement=17`, r67 `agreement=18`) — an aggregate number, not the per-review ledger the proposal describes. |
| 5 | Historical-gate list (gates red by design, so a pinned red is not read as a regression) | **r60 counter + r66 adoption** | `.ufo/waves/round-60/w1/ExecC1Counter.files/c60_gate_status.py` (SKILL.md gate-registry labels vs observed exits); `corpus/knowledge/gate-status-ledger.md` added by `f2b9e081` 2026-11-01, whose own head reads "Adopted from `considerthese/2026-10-26.md` proposal 5"; r66 also ships `.ufo/waves/round-66/c66_gate_status_hostportable.py`; r72 `w1/ScoutGateRows.md` is the relabel census over those rows (historical labels at lines 27-45). |

No unimplemented proposal is mined this round by this seat. **Note the contract's own sentence is
not supported as written** — see "Contradictions" (b).

---

## 4. `merge/kake` MERGE-REPORT — occupied ids holding different content

`/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` states "proposed rows accepted: **129**",
"lane registry currently holds **145** rows; first staged id is **S287**", and "`129` rows, in the
11-column schema". Schema check passes: honoring `\|` escapes, all 129 staged rows and all 184 lane
rows parse to exactly 11 cells (`re.split(r'(?<!\\)\|')` → `{11: 129}` and `{11: 184}`; a naive
`split('|')` misreports 96/7/1 rows at 12/13/14 cells because command cells contain pipes such as
`curl … | grep -c …` — that is a measurement artifact, not a package defect).

**Yes — 8 staged ids are occupied by rows of different content, and the difference is that the lane
row is a later, fuller revision of the same document.** Concrete example pair, first 80 characters of
each row:

- staged (`SOURCES.append.md`, `| S312 |`): `| S312 | 百度搜索资源平台 — 平台工具使用手册（移动适配） — https://ziyuan.baidu.com/college/courseinfo` (opened `2026-10-24`)
- lane (`corpus/SOURCES.md:156`, `| S312 |`): `| S312 | 百度搜索资源平台 — 平台工具使用手册（移动适配） — https://ziyuan.baidu.com/college/courseinfo` (opened `2026-10-25`)

Same id, same title, same URL, same kind/tier; the row text differs below the fold:

| cell | staged S312 | lane S312 |
|---|---|---|
| scope | `Baidu's own list of the reasons a **mobile page fails to match its desktop page*…` | `**Baidu's own list of the reasons a mobile page fails to match its desktop page*…` |
| anchor | `§ 移动适配 → 对应关系错误的五类原因 (章节时间戳 2020-08-14)` | `§ 移动适配 → 对应关系错误的常见原因 (章节时间戳 2020-08-14)` |

So a bare adoption would not merely duplicate an id; it would insert a *narrower* claim beside a
later one. The same shape holds for the other seven: S367 lane covers meta-tag **and** server
methods, staged covers server only; S373 lane covers `「*」` and `「$」`, staged `「$」` only; S372/S374/
S390/S409 differ in scope/anchor/teaches and 4 rows also differ in `opened` (`2026-10-25` vs
`2026-10-24`).

**And the id check under-counts the risk by 19.** Joining on document URL rather than id:

```sh
# per-row first https URL in each registry row / staged row, then set intersection
reg urls=156  staged urls=96  shared urls=27
of those 27 staged rows, ids NOT in the collision list: 19
id-colliding rows that also share a URL: 8 / 8
```

Concrete free-id pairs (staged line → lane row):
`S287` (append line 7) → `S137` (`corpus/SOURCES.md:145`) same
`…/javascript/javascript-seo-basics`; `S288` (line 8) → `S138` (:146); `S289` (line 9) → `S139`
(:147); `S296` (line 16) → `S080` (:88). Those ten-digit-free ids would sail past `comm -12` on ids
and land a second row for a document the lane already holds.

---

## Contradictions (stated, not smoothed)

**(a) Contract §Frontier: "the `merge/kake` package's staged ids S287–S415 are all below the lane's
registry tip and already occupied by different rows".** Measured: 184 registry ids, max `S446`, so
*below the tip* is true; *all … occupied* is false — 8 of 129 staged ids occur in the registry and
**121 do not**. The sentence's operative conclusion (adoption stays closed) is still right, but for
a different reason: 27 staged rows name a document the lane already holds, 19 of them under a free
id. The guard as frozen (`comm -12` on ids) cannot see those 19.

**(b) Contract §Frontier: "`considerthese/2026-10-26.md`: all five proposals are implemented in the
lane (r58, r66, r72 and report practice)".** Measured: proposal 1 is unimplemented
(`round-67.md:127-131`, confirmed by `round-71/w1/ScoutConsider.md`), proposal 4 is recorded as not
implemented (`round-62.md:13`) and as "not lane-ownable" (`round-67.md:127-131`) although r66/r67
print an `agreement=` count; proposal 3 exists only as a one-round r59 artifact. Proposals 2 and 5
are implemented and are the r58 / r60+r66 pair the contract names. "r72" corresponds to the
`ScoutGateRows.md` relabel census, which consumes proposal 5's labels; it does not implement a fifth
proposal.

**(c) The guard form is defensive, not load-bearing, on today's bytes** (0 indented rows in both
files; 0–3-space and column-zero parsers return identical id sets and the same 8 collisions).

No contradiction was found in C1's or C2's own base numbers; this seat measured neither claim's
counter (out of seat scope, `ExecMatrix-2` / `ExecRevisionReceipts` own those).

---

## 5. One proposed move

**Make assimilation closure content-addressed and state the measured triple instead of the
auditor's quantifier.**

Concretely, for the round-77 Frontier record (and the lesson's assimilation line): replace
"staged ids S287–S415 are all … occupied by different rows" with the derivation

```
staged rows 129 · id collisions 8 · staged rows naming a document the lane already holds 27
(of which 19 sit on ids the registry does not use) · free staged ids 121 · renumber map none
```

and require, for any future adoption, that a staged row name which held row it extends (the
MERGE-REPORT's own line 126 rule: "The operator should check that the staged row adds an aspect the
held row does not already carry") rather than relying on id collision.

### Affected axes

- **Calibration (2, HOLD) — improves.** The sentence being replaced asserts more than its derivation
  supports, over committed bytes. This is C1's own failure class applied to the contract text rather
  than to `SHONEN.md` boxes: claim ≤ derivation, with the derivation printed. Nothing about the
  2-score changes; the HOLD stays.
- **Operability (10, HOLD) — neutral.** C2's tool, matrix, constants and edit surface are untouched;
  no counter is added, no gate changes verdict, no case changes expected value.
- **Freshness (10, HOLD) — neutral.** No source row, recheck date, or `used-by` cell is touched; the
  move reads `corpus/SOURCES.md` and the staged package only.

### Second-order effects traced

- **Runtime / contract.** The Frontier bullet is frozen for this round; a leaf may not edit
  `contract.md`. The move therefore lands through the seat that owns the round record
  (`corpus/lessons/round-77.md` `## Gate`/Frontier text and the closure report), which must carry the
  triple with its command, exactly as C1 requires an evidence pointer to resolve at a revision.
- **Substrate.** If the false quantifier is copied into `corpus/lessons/round-77.md`, the next round's
  Frontier step inherits it and the 121 free ids read as "id space already used", which is the
  opposite of the truth; a future round would either wrongly believe assimilation is closed by
  exhaustion or, after discovering the 121 free ids, wrongly believe a renumber makes adoption safe.
- **Adoption policy.** With 121 free ids, renumbering is trivially available, so the id guard is the
  *weak* check and document identity is the strong one. Stating 27/19 keeps adoption closed on
  evidence (the lane holds those documents) instead of on a false premise (all ids occupied).
- **Verification.** The number is cheap to re-derive and must be re-derived at the closing revision,
  not copied: three `grep`/`comm` lines plus one URL join. If the lane mints rows between now and
  closure, the triple changes and the sentence must change with it.

### Risks

- **Freeze risk.** Writing the triple into `contract.md` now would amend a frozen contract mid-round.
  The move must be recorded by the closure seat, not by a wave seat.
- **Over-reading the count.** URL equality is a coarse proxy: MERGE-REPORT line 126 is explicit that
  one page can support several claims. The sentence must read "27 staged rows name a document the
  lane already holds", never "27 duplicates to reject"; 8 of the 27 are also id collisions, and those
  8 are the later-revision rows already shown in item 4.
- **Synthetic-proof drift.** The indentation tolerance is a forward guard (0 indented rows today). If
  the round record cites the guard-bite proof, it must call it synthetic, or it commits the same
  class of overclaim the move is meant to remove.
- **Scope creep.** Making the check a counter/gate is not proposed: an unfrozen counter that gates
  adoption inside a round with a frozen contract would be a second, unplanned instrument. It stays a
  printed derivation in the round record.

### Verification (what reproduces each number)

```sh
# id triple (item 2 block, verbatim) -> 184 / 129 / 8
wc -l < .ufo/waves/round-77/assimilation/{reg-ids,staged-ids,collisions}

# registry ids inside the staged range
awk -F'S' '{n=$2+0; if(n>=287 && n<=415) c++} END{print c+0}' .ufo/waves/round-77/assimilation/reg-ids   # 8

# document overlap: 27 shared URLs, 19 on free ids
python3 - <<'PY'   # first https URL per row, both files; set intersection
PY

# schema: 11 cells per row honoring escapes
python3 -c "import re,collections;S=re.compile(r'(?<!\\\\)\|');..."   # staged {11:129}, reg {11:184}

# SHONEN sibling base rate
for d in /home/vgpnk/Projects/shokunin/*/SHONEN.md; do ... done   # 20 files, 4 boxes each, 18 with marked>0 & evidence=0
```

Not verified by this seat, and not claimed: no sibling instrument was executed; no sibling or fleet
file was read into kake; C1's `c77_shonen_ledger.py` and C2's `c77_sitemap_matrix.py` were not run
(other seats own them); the `merge/kake` package was not adopted, copied, or modified.

---

## Tooling

No tool was installed or upgraded (pacman paused host-wide; nothing was needed). Scratch
`/fast/scratch/hyaku/kake-r77/ConnectorC` removed after the guard proof; the receipts it produced are
quoted in §2 above.

Files written by this seat: this report, and the item-2 outputs
`.ufo/waves/round-77/assimilation/{reg-ids,staged-ids,collisions}`.
