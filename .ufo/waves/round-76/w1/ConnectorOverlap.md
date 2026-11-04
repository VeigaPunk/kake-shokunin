# ConnectorOverlap — round 76 / w1 (kake)

Seat: `ConnectorOverlap`. Scope: (1) sibling overlap, (2) assimilation §10 read-only, (3) `considerthese/2026-10-26.md`
Part 2, (4) sources cross-check.

Base (contract): `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`. Lane tip at scan: `783c7c13db1289ce86653c367d5904593f3a01cf`
(`git log -1 --format='%H %cI'`), two commits above base (`b758cb04` freeze, `783c7c13` amendment 1). `corpus/SOURCES.md`
is byte-stable across them for the population I count: `git show a0491fcd:corpus/SOURCES.md | grep -cE '^\| S[0-9]'` → 181,
worktree → 181.

Method: read-only. No scratch dir was created and none was needed (no tree-level work, no clone); every command below is a
read. No network. Nothing outside this file was written.

---

## 1. Sibling overlap

Population: 22 `*-shokunin` / `*-shokinin` repos under `/home/vgpnk/Projects/shokunin`
(`ls -d *-shokunin *-shokinin | wc -l` → 22, kake included). 19 carry `SKILL.md`; `audio-shokunin`,
`game-dev-2d-shokunin` and `kumitate-shokinin` do not and were scanned by tree.

### (a) offline hreflang audit — **no sibling holds one**

| lane | file:line | what it actually is | relation to kake C2 |
|---|---|---|---|
| kaidoku | `.ufo/waves/round-45/w1/R45W1RevS150/helpers/s113.py:3-6` | six-line live regex census, `re.findall(r'hreflang="([^"]*)"', t)` over one fetched adb page; print `hreflang occurrences N unique M` | not a tool: live fetch, single page, no manifest, no finding vocabulary, no exit contract. No shared input or output with `scripts/hreflang_audit.py`. kake's is **new scope, uncontested** |
| kaidoku | `.ufo/waves/round-45/w1/R45W1RevS150/helpers/driver.py:164-167`, `:247` | the same probe inside a one-round verification driver, case `C16 ... hreflang census (the '17 locales' claim)` | one-round evidence capture, not a capability |
| kaidoku | `.ufo/waves/round-3[5,6,8]/...quarantine*.md` | prose about staged knowledge rows mentioning hreflang | prose only |

Grep that produces this: `grep -rniE 'hreflang' --include='*.py' --include='*.mjs' --include='*.sh' . | grep -v node_modules`
→ **106 hits: 9 in `kaidoku-shokunin`, 97 in `kake-shokunin`, zero in the other 20 lanes.** Filtering to `/tools/`,
`/scripts/` or `/verifiers/` leaves one match, and it is a literal inside a command string in kaidoku's driver
(`round-45/.../driver.py:266`), not code in a tool. (`grep -niE 'hreflang|bcp-?47|quote.truth|language tag'` over every
`*/SKILL.md` returns only `kake-shokunin/SKILL.md`, and there only the existing quote-truth rows.)

**Verdict (a):** no sibling holds an hreflang audit. `duplicate: no · complementary: no · contested: no — empty scope`.

### (b) documentation-quote-truth counter — **no sibling holds one; kake is the sole holder**

`find . -maxdepth 7 \( -name '*quote_truth*' -o -name '*hreflang*' \) -not -path '*/node_modules/*' | awk -F/ '{print $1}' | sort | uniq -c`
→ `52 kake-shokunin` and no other lane.

The three nearest sibling analogues are all **complementary**, not duplicate — each answers a different question than C1's
predicate (`claim-row span ⊂ committed receipt bytes at a revision`, with elision fragments, correction closures and an
append-only conjunct):

| lane | file:line | predicate it implements | why it is not C1 |
|---|---|---|---|
| chousa | `tools/quote-reopen.py:2-34` | re-open a TSV quote against the **live** source; verdicts `VERBATIM / ABSENT / TOO_LONG / NO_SOURCE / UNREACHABLE` | network, per-item rule file, no receipt universe, no revision pin, no append-only conjunct |
| chousa | `tools/claims-audit.py:2-14` | flag statements in a frozen claims file that committed bytes contradict, driven by a hand-authored TSV rule per statement | rule-authored per claim; C1 needs no per-claim authoring — a generic span predicate over every committed receipt |
| tabi | `scripts/check-cited-receipts.mjs:2-15` | a cited `.ufo/waves/round-<N>/` **path must exist** at the citing commit | path existence ≠ content contiguity; a receipt can exist and not contain the quoted bytes |

**Verdict (b):** `duplicate: no · complementary: yes (three lanes, three different predicates) · contested: no`. Nothing to
report as scope contention; nothing to absorb.

### (c) BCP-47 / language-tag validator — **no sibling holds one**

- `grep -rniE 'bcp-?47|bcp47|language.tag|langtag'` → 19 files fleet-wide; the only *code* hits are
  `kotoba-shokunin/verifiers/check_scoped_rules.py:334,1119` and `check_scoped_rules_v32.py:338,1265`. Their
  `LOCALE_SEGMENTS` frozenset (`check_scoped_rules_v32.py:341`) classifies a **URL path segment** as a locale rendering
  (rule `A3(b)`) against a hardcoded list of two-letter segments. No grammar, no subtag structure, no well-formedness test.
  Different question; not reusable.
- `lore-shokunin/corpus/SOURCES.md:36` (row S028, SKOS) mentions "language tag" inside a source row's scope cell — a source
  row, not a validator.
- No sibling has a file whose name contains `bcp` (`find . -maxdepth 5 -iname '*bcp*'` → no output).

**Verdict (c):** `duplicate: no · complementary: no (kotoba's locale-segment alias rule is orthogonal) · contested: no`.

### Consequence for C2

C2's offline, manifest-versioned, findings-id audit is **new scope in the fleet**, and its two supporting capabilities
(BCP-47 grammar, hreflang reciprocity) are new in the lane as well. The only registry-adjacent prior art is kake's own
`corpus/SOURCES.md:31` (S023, the WHATWG `links.html` canonical fragment) — see §4, where it constrains the new row's scope
cell rather than the tool.

---

## 2. Assimilation (§10, read-only) — **`Assimilation: none`**

Staging tree `/home/vgpnk/Projects/shokuknow/merge/kake/`: `MERGE-REPORT.md` (166 lines), `MERGE-REPORT.json`,
`SOURCES.append.md` (129 rows), `knowledge/corpus/knowledge/` (98 files), `amendments/corpus/knowledge/` (6 files).
Staged id range: **S287–S415** (129 contiguous ids), first staged id S287 (`MERGE-REPORT.md:8`).
Lane registry tip: **S443**, 181 rows, identical at base and at scan.

### The three representatives and their locators

| staged entry | locators it cites | resolves in the lane today? |
|---|---|---|
| `knowledge/corpus/knowledge/engine-crawl-contracts.md:1-6` | `source: S287`, `S290`, `S291` | **no** — S287, S290, S291 all absent from `corpus/SOURCES.md` |
| `knowledge/corpus/knowledge/crux-surface-matrix.md:1-6` | `source: S293`, `S294`, `S295`, `S297`, `S298` | **no** — all five absent |
| `knowledge/corpus/knowledge/baidu-dead-link-taxonomy.md:1-2` | `source: S403` | **no** — S403 absent |

Absence test (regex over the registry, not grep on a guess):

```sh
python3 - <<'EOF'
import re
ids=set(int(m.group(1)) for m in re.finditer(r'^\| S(\d{3})\b', open('corpus/SOURCES.md',encoding='utf-8').read(), re.M))
for i in (287,290,291,293,294,295,296,297,298,403): print(f'S{i:03d}', 'PRESENT' if i in ids else 'ABSENT')
EOF
```

Observed: `S287 ABSENT S290 ABSENT S291 ABSENT S293 ABSENT S294 ABSENT S295 ABSENT S296 ABSENT S297 ABSENT S298 ABSENT S403 ABSENT`.
Each representative entry would therefore land with a **dangling `source:` line** — the class round 52 closed. None re-grounds
as written.

### The append-only blocker, measured

```sh
python3 - <<'EOF'
import re
ids=[int(m.group(1)) for m in re.finditer(r'^\| S(\d{3})\b', open('corpus/SOURCES.md',encoding='utf-8').read(), re.M)]
s=set(ids); print('rows',len(ids),'unique',len(s),'min',min(s),'max',max(s))
print('staged 287-415 absent:',len([i for i in range(287,416) if i not in s]),
      'present:',129-len([i for i in range(287,416) if i not in s]))
print('present ones:',[i for i in range(287,416) if i in s])
print('count ids > 415:',len([i for i in s if i>415]))
EOF
```

Observed: `rows 181 unique 181 min 1 max 443` / `staged 287-415 absent: 121 present: 8` /
`present ones: [312, 329, 367, 372, 373, 374, 390, 409]` / `count ids > 415: 28`.

Two independent defects, both fatal to adoption as written:

1. **8 ids are occupied and not identical.** Diffing staged vs lane row-for-row: `both 8 identical 0 differ 8`. Same URL in
   every case, different `scope` / `anchor` / `teaches` cells. The lane's versions are the **later re-adoptions**, not stale
   copies: `corpus/lessons/round-55.md:17-18` records S372/S373 re-opened at `2026-10-25` with sha256-pinned bodies, and
   `corpus/lessons/round-56.md:20` records `S367 is a held row (opened round 53, used-by extended only); this round re-opened
   it with a fresh GET`. Adopting the staged text would **rewrite** those rows — forbidden by C1 kill rule 3 and by
   `scripts/append_guard.py:1-22` (an unmatched base line is `changed P`).
2. **The other 121 ids all sit below the tip.** 28 ids `> 415` already exist, so S287–S415 is a mid-file insertion, never an
   append. The first legal id for anything new this round is **S444** (`grep -cE '^\| S44[4-9]' corpus/SOURCES.md` → `0`).

### Correction to the round-75 premise (bytes, not memory)

Round 75 recorded that `.ufo/waves/round-1[456]/` and `.ufo/waves/corpus-expansion-1/audit-wave.py` are absent. Half of that
is a wrong-tree lookup, and carrying it forward would make this round quote an unrun check:

- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/audit-wave.py` **exists** — 30973 bytes, mtime 2026-10-24 23:30
  (`ls -l`). It is a staging-repo path; it was never supposed to be in the lane.
- The own-work locators the staged rows cite are staging-repo-relative and **all resolve**:
  `lanes/kake/round7/.evidence/merge_renumber_r7.txt` 2610 B (cited at `SOURCES.append.md:76`),
  `round8/.evidence/staged_proposal_census_r8.txt` 1204 B (`:82`), `round9/.evidence/evidence_gap_repair_r9.txt` 3779 B
  (`:86`), `round10/.evidence/repair_locator_kinds_r10.txt` 2470 B (`:91`), `round14/.evidence/registry_census_r14.txt`
  8744 B (`:120`), `round16/.evidence/carrier_map_r16.txt` 1555 B (`:133`) — 6/6 present.
- What *is* absent is `.ufo/waves/round-13…16` **in the lane** (`ls -d .ufo/waves/round-16` → no such file; the lane's wave
  dirs begin at `round-21`). No staged row cites that path.

**Verdict: `Assimilation: none`.** Blocker = the id space: 8 of the 129 ids are already held by rows that are later rewrites
of the same URL, and the remaining 121 would insert below the tip S443. Secondary: each staged entry's own `source:` ids are
absent from the registry, so it would land dangling.

**Flip condition** (not a recommendation to act): a staged topic could re-ground cleanly only by a seat opening its cited URL
this round and writing a **new** row above S443 — which is what r55/r56/r57 did for S367 and S372–S374. That is a new row,
not assimilation, and it needs a fresh fetched body, not the staged text.

---

## 3. `considerthese/2026-10-26.md` Part 2 — implementation status

| # | proposal | status | evidence |
|---|---|---|---|
| 1 | Read the lane's own tools, report only a change or a red (id_resolver dangling, landed_check, frontier ground map) | **partial** | tools exist — `scripts/id_resolver.py`, `scripts/landed_check.py`; `id-resolver-gate` is registered `live only with --fleet` (`SKILL.md:1274`, restated `SKILL.md:1337`) and `scripts/landed_check.py` is explicitly *not* a gate (`SKILL.md:1248`). The resolver's output is consumed when it goes **red** — the round-72 mistake row quotes `ids_cited=121 ids_resolved=118 dangling=3` (`corpus/lessons/round-72.md:24`) — but there is no standing per-round delta read of either tool, and the frontier ground map is not a README section today: `README.md` is 14 lines with one heading, `## What's here` (`README.md:10`), and `grep -niE 'frontier (ground )?map|ground map' README.md` returns nothing |
| 2 | Receipt-rewrite watch (`git log --follow` over `controls/`, flag a changed `revision:`/result line) | **implemented** | `SKILL.md:1293` row `receipt-rewrite-counter`, tool `.ufo/waves/round-58/c58_receipt_rewrites.py`, ledger `.ufo/waves/round-58/receipt-rewrites.json`, `0=met` on `undisclosed/phantom/malformed/wrong_kind/unpointed/symlinks/new_rewritten` all 0. Named blind spot carried at `corpus/lessons/round-75.md:132-139` (the carrier receipt `corpus/knowledge/instrument-receipts.json` lies outside the watched `control(s)/` path) |
| 3 | Operator-decision queue with wait counts | **implemented outside the lane** (operator-owned), no lane-side artifact | the queue is the fleet file `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (180390 bytes, mtime 2026-11-03 21:51): one row per item, shaped `lane \| round-<N> \| question`, 17 rows for kake (`grep -c '^kake \|'` → 17), wait age readable from the `round-<N>` cell, answers inline in the same row (the kama round-11 row ends `— L0 ANSWER (hyaku orchestrator for the operator, 2026-10-19; operator may override)`). The lane keeps no queue of its own: `find . -iname '*operator*'` (excluding assimilation copies) → four wave reports `round-5[89]/round-6[01]/w1/ScoutOperatorLessons.md`, and the only `*queue*` files are `corpus/knowledge/js-rendering-queue.md` and `publish-queue.md`, both technical. The part of the proposal that does not exist is the **lane-side ranked short list**; the items themselves sit as prose at `corpus/lessons/round-75.md:136` (`tool_sha256` in the receipt changes the schema for every lane) and `:141` (host-absolute `/fast/scratch/...` paths in committed evidence) |
| 4 | Gate-agreement ledger (verifier agree/disagree per round) | **not implemented, routed** | `SKILL.md` has no agreement ledger row; `.ufo/waves/round-58/w1/ScribeConsiderthese.md:98-100` — "Gate-agreement ledger — not built this round … No `*agreement*` artifact exists under `corpus/`"; fleet report `.ufo/reports/round-75/kake.md:131` — "Proposal 4 (gate-agreement ledger) is the one still open and is routed" |
| 5 | Historical-gate list | **implemented** | `corpus/knowledge/gate-status-ledger.md:1-10` (entry line 1 reads "adopted r66", citing this very proposal) plus the derived view at `SKILL.md:1329-1339` (`historical:` / `never met:` / `live:` / `outside the population:` classes) |

**Mineable next round?** No. The unfinished set is #1 (partial) and #4 (routed), and neither is knowledge-shaped:
- #1's missing pieces are a README frontier map and a standing delta read of two existing tools — both are bookkeeping over
  artifacts the lane already commits, not a new grounded fact.
- #4's ground is a view over existing per-round spot-check lessons (round-58 scribe: "agree/disagree prose (round-20 …
  round-57) but no cross-round ledger"). It is a **counter**, and it is already routed — building it here would pre-empt the
  routing decision and put a second owner on one file.
- #3's content lives operator-side in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`; only the lane-side ranking is
  missing, which is again bookkeeping, and its items are operator decisions, not corpus claims.

This agrees with the contract's frontier step ("no new proposal is mined this round unless a seat finds one unimplemented and
grounded"): none is grounded as new corpus knowledge.

---

## 4. Sources cross-check for the scout's proposed S-ids

The scout item (`mk_w1_spec.py:65-88`) proposes one row per source for three URLs. **At my scan time
`w1/ScoutHreflangSources.md` does not exist yet** — only its retained-bytes directory and `w1/ScoutHreflangEdge.md` — and no
wave report written so far names an S-id (`grep -nE 'S4[0-9]{2}' ScoutHreflangEdge.md ScribeRegistry.md ReviewerC1.md` →
no output). So the check below is against the **URLs the seat spec fixes**, and it must be re-run against the landed rows for
their actual ids before the L1 admits them. URL-duplication test over `corpus/SOURCES.md`:

| proposed source | existing rows with that URL (in scope) | verdict |
|---|---|---|
| `https://developers.google.com/search/docs/specialty/international/localized-versions` | **none** (`grep -n 'localized-versions\|international/' corpus/SOURCES.md` → no output) | clean |
| `https://html.spec.whatwg.org/multipage/links.html` (`hreflang` attribute of `link`) | **S023** — `corpus/SOURCES.md:31`, anchor `#link-type-canonical`, scope "HTML link-type keyword semantics", teaches "Canonical indicates the preferred URL; link-type keywords compare ASCII case-insensitively", used-by `corpus/lessons/round-22.md` | **same document, different fragment and different rule** → not a URL duplicate, but the new row MUST carry a distinct fragment (`#attr-link-hreflang` or the attribute's own id) and say in its scope cell that it is the `hreflang` attribute. Without that, a reviewer can read it as a re-open of S023 and the census's W04 duplicate-URL note count (14, per `considerthese/2026-10-26.md` Part 1) grows |
| `https://www.rfc-editor.org/rfc/rfc5646.txt` | **none**. The lane holds 12 distinct RFCs — `rfc3339 3986 6596 6797 6874 8259 8615 9110 9111 9116 9309 9844` (`grep -oE 'rfc-editor\.org/rfc/rfc[0-9]+' \| sort -u`) — and no 5646/4646/BCP-47 row | clean |

**Id floor.** Lane tip is **S443**; `grep -cE '^\| S44[4-9]' corpus/SOURCES.md` → `0`. The three proposed rows must be
**S444, S445, S446** in file order — any id ≤ S443 breaks the append-only conjunct, and any gap in S444+ needs a stated reason
because the census counts rows, not ids.

**Ground is openable this round.** The scout's retained bytes exist under `w1/ScoutHreflangSources/` and do carry the
grounding: `whatwg-links.txt` holds `hreflang` at lines 632, 1350, 4042, 4049, 4064, 4080, 4098, 4116, and
`google-localized-versions.txt` holds `x-default` at lines 403, 439, 502, 536. So the `## Gate` quote requirement of the
frontier step is satisfiable from committed bytes rather than from memory.

---

## 5. Contradictions and second-order risks (stated, not smoothed)

1. **"Append 129 rows" is not append.** Eight of the 129 ids are occupied by later rewrites of the same URL. A merge that
   loops `SOURCES.append.md` into the registry rewrites history in eight places and inserts 121 rows mid-file; C1's
   `A1`/`append_only` conjunct and `scripts/append_guard.py` both fire. Any adoption must renumber (or drop) those eight and
   re-ground the rest above S443.
2. **Round 75's assimilation blocker is partly wrong.** `audit-wave.py` exists and the six own-work locators resolve; only the
   in-lane `round-13…16` directories are missing, and no staged row cites them. Repeating the r75 wording would put an unrun
   check into a committed lesson. The defensible blocker is the id space, and it is stronger: it is a collision, not an
   absence.
3. **P2's watch has a named blind spot** (`corpus/lessons/round-75.md:132-139`). Any receipt-rewrite claim this round inherits
   it unless the claim names the carrier receipt as outside the watched path.
4. **S023 : new whatwg row.** Same URL stem, different fragment. Distinctness has to be written into the row, not assumed —
   otherwise the new row is a scope neighbour with no visible boundary, and the `hreflang_self_missing` / reciprocity rules
   (which are about *pages*, not specs) get their first citation in a row that already exists in a different sense.
5. **No sibling contention to report.** All three capabilities are new fleet-wide, so C2's admission rests entirely on the
   matrix + constants + real-input run, not on comparative novelty. That is also why a duplicate-URL row for S023's document
   would be the only cross-lane-visible weakness in the C2 surface.

---

## Receipts — the commands this report rests on

| # | command (cwd) | observed |
|---|---|---|
| R1 | `ls -d *-shokunin *-shokinin \| wc -l` (fleet root) | `22` |
| R2 | `for d in *-shokunin *-shokinin; do [ -f "$d/SKILL.md" ] \|\| echo "NO SKILL: $d"; done` | `NO SKILL: audio-shokunin`, `game-dev-2d-shokunin`, `kumitate-shokinin` |
| R3 | `grep -rniE 'hreflang' --include='*.py' --include='*.mjs' --include='*.sh' . \| grep -v node_modules` (fleet root) | `106` hits → `9 kaidoku-shokunin`, `97 kake-shokunin`, 0 in the other 20 lanes; restricted to `/tools\|scripts\|verifiers/` only `kaidoku-.../round-45/.../driver.py:266` (a literal inside a command string) |
| R4 | `find . -maxdepth 7 \( -name '*quote_truth*' -o -name '*hreflang*' \) -not -path '*/node_modules/*' \| awk -F/ '{print $1}' \| sort \| uniq -c` | `52 kake-shokunin` (no other lane) |
| R5 | `grep -rniE 'bcp-?47\|bcp47\|language.tag\|langtag' --include='*.py' ...` | code hits only `kotoba-shokunin/verifiers/check_scoped_rules.py:334,1119`, `check_scoped_rules_v32.py:338,1265` (line 341 `LOCALE_SEGMENTS`) |
| R6 | `git log -1 --format='%H %cI'` (lane) | `783c7c13db1289ce86653c367d5904593f3a01cf 2026-11-03T21:54:51-03:00`; `git log --oneline a0491fcd..HEAD` → `783c7c13`, `b758cb04` |
| R7 | `git show a0491fcd:corpus/SOURCES.md \| grep -cE '^\| S[0-9]'` / `grep -cE '^\| S[0-9]' corpus/SOURCES.md` | `181` / `181`; tip `\| S443` |
| R8 | staging id scan (`grep -oE '^\| S[0-9]+' SOURCES.append.md \| sed 's/\| //' \| sort -u`) | `S287` … `S415`, `129` ids |
| R9 | id-collision python (see §2) | `rows 181 unique 181 min 1 max 443`; `staged 287-415 absent: 121 present: 8`; present `[312,329,367,372,373,374,390,409]`; `count ids > 415: 28` |
| R10 | staged-vs-lane row diff python | `both 8 identical 0 differ 8` |
| R11 | locator resolution python (see §2) | ten ids, all `ABSENT` |
| R12 | `ls -l /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/audit-wave.py` | `30973` bytes, `2026-10-24 23:30` |
| R13 | six `.evidence` files under `/home/vgpnk/Projects/shokuknow/lanes/kake/` | `2610 / 1204 / 3779 / 2470 / 8744 / 1555` bytes, all present |
| R14 | `ls -d .ufo/waves/corpus-expansion-1` `/` `ls -d .ufo/waves/round-16` (lane) | both `No such file or directory`; lane waves start `round-21` |
| R15 | `grep -n 'Historical-gate list' SKILL.md` / `grep -n 'c58_receipt_rewrites' SKILL.md` / `grep -nE 'id-resolver-gate' SKILL.md` | `1329` / `1293` (+`1390`) / `1274` (+`1337`) |
| R16 | `wc -l < README.md` + `grep -nE '^## ' README.md` | `14` lines, single heading `10:## What's here` |
| R17 | `sed -n '94,102p' .ufo/waves/round-58/w1/ScribeConsiderthese.md` | "Gate-agreement ledger — not built this round … No `*agreement*` artifact exists under `corpus/`" |
| R18 | `sed -n '125,135p' .ufo/reports/round-75/kake.md` (fleet) | "Proposal 4 (gate-agreement ledger) is the one still open and is routed" |
| R19 | `sed -n '1,10p' corpus/knowledge/gate-status-ledger.md` | line 1 "# Gate-status ledger — historical and host-bound gates (adopted r66)"; line 4 "Adopted from `considerthese/2026-10-26.md` proposal 5" |
| R20 | `grep -n 'localized-versions\|international/' corpus/SOURCES.md` | no output |
| R21 | `sed -n '31p' corpus/SOURCES.md` | S023, `#link-type-canonical`, used-by `corpus/lessons/round-22.md` |
| R22 | `grep -oE 'rfc-editor\.org/rfc/rfc[0-9]+' corpus/SOURCES.md \| sort -u` | `rfc3339 3986 6596 6797 6874 8259 8615 9110 9111 9116 9309 9844` (no 5646) |
| R23 | `grep -cE '^\| S44[4-9]' corpus/SOURCES.md` | `0` |
| R24 | `sed -n '125,145p' corpus/lessons/round-75.md` | items 3–5 incl. the rewrite-watch blind spot (line 132) and the two operator decisions (136, 141) |
| R25 | `grep -n 'hreflang' .ufo/waves/round-76/w1/ScoutHreflangSources/whatwg-links.txt` / `grep -n -i 'x-default' .../google-localized-versions.txt` | `632,1350,4042,4049,4064,4080,4098,4116` / `403,439,502,536` |
| R26 | `ls -l .ufo/l0-questions.md` + `grep -c '^kake \|' .ufo/l0-questions.md` (fleet root) | `180390` bytes, `2026-11-03 21:51`; `17` kake rows; row shape `lane \| round-<N> \| question`, L0 answers inline |
| R27 | `grep -niE 'dangling=\|ids_resolved' corpus/lessons/round-7[0-5].md` (lane) | `corpus/lessons/round-72.md:24` — "the id resolver reports `ids_cited=121 ids_resolved=118 dangling=3`"; no such read in rounds 73–75 |

Tooling: nothing installed or upgraded this round (no install channel used; pacman was not touched).
