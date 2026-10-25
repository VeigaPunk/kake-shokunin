# Round 51 — report-contract checklist (w1/ReviewReportContract)

Scope: the six required sections of `/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-51.md:99-127` (§4),
one entry each with the exact heading text, the evidence that section must carry, and whether the round's
**committed** bytes at lane tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` can already support it or whether it
waits on a measurement that does not exist yet. This seat authored no evidence; every number below was
re-measured live at that revision.

## What this seat re-measured (ground truth)

| command | output | exit |
|---|---|---|
| `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c…` | `C1 ledger 0/3 met=False`; L1 `settlement receipt absent`, L2 `route map absent`, L3 `settlement receipt absent` | 1 |
| `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768c…` | `C2 quote-truth 8/8 met=True`, all of `C1_entries_exist … C8_append_after_mirror` pass | 0 |
| `git show 007d66e4…:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` | `143` | 0 |
| same at `9d13768c…` | `145` | 0 |
| `git diff --numstat 007d66e4… 9d13768c… -- corpus/SOURCES.md` | `2	0` (two added lines, no existing row rewritten) | 0 |
| `git ls-tree -r --name-only <rev> -- corpus/knowledge/ \| wc -l` | `41` at base, `43` at tip | 0 |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | 13 lines: 12 `kake	W04 duplicate url …` warnings + `kake	ok	…/kake-shokunin/corpus/SOURCES.md` | 0 |
| `git ls-tree -r --name-only 9d13768c… -- .ufo/waves/round-51/` | only `contract.json`, both counters, `controls/*`, `assimilation/**` — no `w1/*.md`, no settlement/timing/accounting/route files | 0 |
| `git status --porcelain` (lane) | `??` on `build_wave_evidence.py`, `route-map.json`, `route-probes/`, `w1/`, `w51-spec.json`, `w51-taskcall.json`, `wave-grant.txt`, `wave-start-utc.txt` | 0 |
| `ls .ufo/waves/round-51/w1/` | at 03:33: `swarm-registry.json` only (36,917 B), no seat report. Recheck at 03:35: 12 seat reports written and still untracked (`Exec*`, `Mutation*` ×5, `ScoutCounterC1Base`, `ScoutCounterC2Base`), none committed | 0 |

Control receipts already committed: `.ufo/waves/round-51/controls/c1-before-base.txt` (`C1 ledger 0/3` at
`007d66e4…`) and `c2-before-base.txt` (`C2 quote-truth 0/8` at `007d66e4…`); plus the junk controls
`c1-junk-wave.txt`, `c2-junk-entries.txt`.

## The six required sections — exact heading text, in this order

Prompt §4 lists them as bold bullet labels (`**Work performed** —`, `:104-119`). The only committed
precedent renders them as level-2 headings, and so must the round-51 report:
`.ufo/reports/round-50/kake.md:9,93,114,138,161,176`.

- [ ] `## Work performed`
- [ ] `## Landed changes`
- [ ] `## Before → after measurements`
- [ ] `## Sources & frontier`
- [ ] `## Trend verdicts`
- [ ] `## SHONEN`

`## SHONEN` is the last of the six; host-mechanics sections (Waves, Tool installs, Mistakes, Misroot sweep,
Open L0 questions) come after it, exactly as in the round-50 predecessor (`:191-273`).

### 1. `## Work performed`

Required content (`:104-106`): the section **opens** by naming the round's declared claims (1–3) and each
claim's target axis or capability; then one bullet per work item, every bullet carrying an evidence pointer
(`path:line`, command output, or commit hash).

Evidence it needs:
- claim declaration, frozen before scoring: `.ufo/waves/round-51/contract.json` — `declaredBeforeScoring: true`,
  base `007d66e4…`, C1 on `operability` (capability acquisition), C2 on `freshness` (sourced learning claim),
  with predicates `ledger_checks_passed == 3 of 3` and `conditions_passed == 8 of 8`. Committed at `19a99bd`.
- one pointer per item, and §6 additionally demands the round shape, each wave's seat count, role mix, dead
  seats, any residual call and the round total.

Status at `9d13768c…`: **PARTIAL.** Supported now — the claim naming (contract above; `LOG.md:2044-2056`) and
every C2 work item (commits `19a99bd`, `5591557`, `9d13768`). **Not supportable yet** — the C1 work items:
the 48-seat wave (`wave-grant.txt`: `granted lane=kake wave=r51-w1 seats=48 live=66 pending=0 cap=256`, untracked),
the route probes, the settlement, and the wave shape/seat/role/dead-seat bullets. No seat report is **committed** (12 exist
untracked in the worktree; `git ls-tree` at `9d13768c…` lists no `w1/*.md`), and no settlement exists.

### 2. `## Landed changes`

Required content (`:107-108`): every change tied to a `LOG.md` entry **and** to the commit hash that carries it.

Evidence it needs: a `LOG.md` line number and a commit hash per change; the hash must be the helper's
`landed <hash>` line, not a `rewritten <old> -> <new>` diagnostic.

Status at `9d13768c…`: **PARTIAL.** C2 is fully supported: `LOG.md:2044` (claims frozen) → `19a99bd`;
`LOG.md:2057` (pre-append mirror) → `19a99bd`; `LOG.md:2068` (S262/S263 append + two entries + lesson) →
`5591557`; `LOG.md:2077` (counter receipt-lookup fix) → `9d13768`. **C1 has no landed change**: nothing in the
tree carries `settlement.json`, `wave-timing.json`, `round-time-accounting.json`, `route-map.json`,
`route-probes/`, `w51-taskcall.json` or `wave-grant.txt`, and `LOG.md` names **no round-51 wall-clock figure**
(`grep -n 'wall\|seconds' LOG.md` matches only `:538`, `:1650`, `:1775`, plus the claim prose at `:2047`).
The ledger's L3 requires that figure in `LOG.md` (`c51_wave_ledger.py:241`), so its absence is a second,
independent blocker on C1 landing.

### 3. `## Before → after measurements`

Required content (`:109-110`): one measurement per claim, each with its counting command and the commit it was
measured against.

Evidence it needs: the predicate string printed by the counter, the exit code, and the revision.

Status at `9d13768c…`:
- **C2 complete.** Before: `0/8` at `007d66e4…` (committed control `controls/c2-before-base.txt`). After:
  `8/8`, exit 0 at `9d13768c…` (re-run live above). Counting command:
  `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision <commit>`.
- **C1 before only; the after measurement does not exist.** Before: `0/3`, exit 1 at `007d66e4…`
  (`controls/c1-before-base.txt`) and still `0/3`, exit 1 at tip. Counting command:
  `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision <commit>`.
  An "after" revision cannot exist yet: the ledger reads committed bytes only (`git show`, `git ls-tree`),
  and every input it needs is untracked. Writing `3 of 3` before that revision exists would be a false
  measurement, not a draft.

### 4. `## Sources & frontier`

Required content (`:111-115`): `SOURCES.md` rows before→after with the counting command; rows added by tier;
rows touched old→new; frontier rows advanced. The `SOURCES: unchanged —` escape applies only to a lane with no
`corpus/`; kake has `corpus/`, so the escape is unavailable and the full item is mandatory. This is a
conformance item and the watchdog applies its source-census gate; it is **not** a report-marker predicate.

Evidence it needs:
- rows before→after: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` →
  `143` at `007d66e4…`, `145` at `9d13768c…`.
- rows added by tier: two tier-A `docs` rows, S262 (Google canonicalization) and S263 (Googlebot), both
  `mined`, `opened` 2026-10-24, `recheck` `180d` — `corpus/lessons/round-51.md:8-9` (each Gate line carries
  URL, access date, §, a 9–10-word raw-substring quote, sha256, byte length, HTTP 200) and the registry rows.
- rows touched old→new: none — `git diff --numstat 007d66e4… 9d13768c… -- corpus/SOURCES.md` is `2	0`, so no
  existing row's cell changed.
- frontier rows advanced: two — `corpus/knowledge/canonical-selection.md` (S262) and
  `corpus/knowledge/crawler-identity.md` (S263); knowledge entries `41 → 43`; C2 conditions C1–C6 pass.
- §2b extras: mined mistake present (`corpus/lessons/round-51.md:76` — four classes, each with evidence,
  captured-by and fix); one sourced claim present (C2 rests on S262/S263).
- census before→after, pasted with both exit codes.

Status at `9d13768c…`: **SUPPORTED for rows/tiers/touched/frontier; the census pair is not yet recorded.**
The only census receipts under the wave dir are `assimilation/pre-append/census-{argv,exit,stdout,stderr}.txt`,
which are the **pre-append mirror's `--file` census** (a different measurement from the round census). The
round-start census output and exit are committed nowhere; the live run above is mine, not the round's. The
round-end census must be run and pasted: exit `0` with `kake	ok` and the same 12 W04 duplicate-URL warnings
(`S033, S088, S092, S098, S099, S102, S110, S111, S115, S116, S117, S127`).

### 5. `## Trend verdicts`

Required content (`:116-117`): exactly one verdict each for `expansion`, `quality` and `discernment`, each one
of `improved | harmed | unchanged | unprovable-but-better`, with evidence and **no scalar**. Not a marker
predicate, and the watchdog does not check it — still required.

Status at `9d13768c…`: **PARTIAL, and it must not overreach.**
- expansion — supportable now: two entries on ground the lane did not hold, rows `143 → 145`, entries
  `41 → 43` (evidence above) → `improved`.
- quality — only if scoped honestly: C2's two controls fail and its predicate passes only after the append
  (0/8 → 8/8, junk control 3/8, both committed). Any quality verdict that rests on C1 is `unprovable` until
  C1's after-measurement exists; the C1 instrument is itself the missing evidence.
- discernment — supportable now: two staged entries refused with reason and flip
  (`corpus/lessons/round-51.md:32`), the id-collision guard proven able to fail on an indented fixture
  (`assimilation/guard/*`, lesson `:60`), and the quarantine slice re-derived and left unadopted
  (`assimilation/quarantine-slice`, lesson `:69`) → `improved`.

### 6. `## SHONEN`

Required content (`:118-120`): one line per box of `SHONEN.md` — `[x]` only with a named non-author verifier,
`[~]` with a resolvable evidence pointer, `[ ]` if untouched.

`SHONEN.md` holds exactly four boxes, all currently `[ ]`; the report needs four lines, in this order:
1. `SKILL.md contains real decision tables, error patterns, checklists, cited sources`
2. `At least one end-to-end domain task executed and logged in LOG.md`
3. `Instructions executable by an agent without oral context`
4. `No cross-domain bleed (PROVINCE.md still accurate)`

Status at `9d13768c…`: **`[~]` is supportable for all four; `[x]` is not available.** `[x]` requires a named
non-author verifier, and no round-51 verifier record exists (round closure is a separate, non-author session).
Resolvable pointers for `[~]`: held ground cited to `corpus/SOURCES.md` rows incl. the round's own S262/S263
entries; `LOG.md:2044-2078` for the executed task; absolute-path wave items
(`.ufo/waves/round-51/w51-spec.json`, uncommitted) for oral-context-free execution; `PROVINCE.md` plus the
lesson's refusals for no cross-domain bleed. A report that marks any of these `[x]` without naming a verifier
is a false marker.

## Status summary

| # | Section | Status at `9d13768c…` | Blocker if not supportable |
|---|---|---|---|
| 1 | `## Work performed` | partial | C1's wave items: no **committed** seat reports (12 untracked), no settlement, no route receipts |
| 2 | `## Landed changes` | partial | no commit carries the C1 evidence; `LOG.md` names no round-51 wall clock |
| 3 | `## Before → after measurements` | C2 complete, C1 before-only | C1's after revision does not exist (untracked inputs) |
| 4 | `## Sources & frontier` | rows/tiers/touched/frontier supported; census pair missing | round-start census unrecorded; round-end census not yet run |
| 5 | `## Trend verdicts` | partial | any verdict resting on C1 is `unprovable` today |
| 6 | `## SHONEN` | `[~]`-able, no `[x]` | no named non-author verifier |

## Measurements that do not exist yet

Each of these must exist in committed bytes before the round report can assert C1 and land. State as measured
at 03:35: **absent** = no file on disk; **uncommitted** = file exists, must be committed and re-read.

1. `.ufo/waves/round-51/settlement.json` — **absent.** spawn, `settled`, `dead`, `reports_written`,
   `timeout_seconds`; built by `build_wave_evidence.py` from `w1/<Seat>.md` mtimes after the batch settles.
2. `.ufo/waves/round-51/wave-timing.json` — **absent.** A parsed `startedAt`/`settledAt` pair;
   `wave-start-utc.txt` (`2026-10-25T06:32:17Z`, uncommitted) exists, `settled-utc.txt` does not exist yet.
3. `.ufo/waves/round-51/round-time-accounting.json` — **absent.** `wall_clock_seconds`,
   `aggregate_seat_seconds`, `dead_seat_seconds`, all re-derivable from (1)+(2) by
   `c51_wave_ledger.py:200-255`.
4. `.ufo/waves/round-51/w51-taskcall.json` — **uncommitted.** `counts.spawn` must equal the settlement's spawn
   and the seat list.
5. `.ufo/waves/round-51/route-map.json` — **uncommitted** — role bindings with a `kimiModel` per role and
   every failing probe recorded as a deviation; and `.ufo/waves/round-51/route-probes/*.json` —
   **uncommitted** — integer `httpStatus` per alias, `bodyExcerpt` on every `ok:false` receipt, no failing
   alias used by a role.
6. `.ufo/waves/round-51/wave-grant.txt` — **uncommitted**; must carry `granted lane=kake` (L3's last check).
7. the seat reports themselves: committed `w1/<Seat>.md` files, one per seat the settlement marks
   `report: true`, with basenames equal to the settlement's seat names (L1 compares both directions).
   **12 exist uncommitted** at 03:35; every further seat that lands a report raises the count L1 compares.
8. the wall-clock figure written into `LOG.md` — **absent** (L3 requires the re-derived integer to appear
   there; `LOG.md` names none for round 51).

## Adjacent requirements the six sections do not replace

Per prompt §6 and the round-50 precedent (`:191-273`), the report also carries: **Waves** (shape, seat counts,
role mix, dead seats with last error text, residual call, round total), **Tool installs** (tool, version,
channel, reason — none this seat), **Mistakes** (misroot sweep record required, §2.3), **Misroot sweep**
(fleet-root `git status --porcelain`, byte-exact `cmp` relocation), **Open L0 questions** (appended line in
`.ufo/l0-questions.md`). These extend the six; they never substitute for one.

## Marker rule

A report is contentless — the round **fails** and is relaunched — when it carries placeholder text, no evidence
pointers, or misses a required section **other than** `## Sources & frontier` and `## Trend verdicts`
(`:121-127`). Missing either of those two is `ok` plus one minimum-content conformance defect, logged as one;
the watchdog still applies its source-census gate for `## Sources & frontier`.

## Limits of this checklist

- The C1 run at tip is a **before** reading, not the after-measurement; the ledger reads git bytes only, so
  committing the untracked worktree files without the seat reports would still score 0/3 (L1 needs
  `reports_written == committed .md` count).
- Precedent gap: `round-50` committed `settlement.json`, `route-map.json` and `wave-grant.txt` but **no**
  `wave-timing.json` or `round-time-accounting.json`, so L3's artifacts and the `LOG.md` wall-clock rule have
  no earlier committed instance to copy.
- Files this seat could not read: none. Every path named here was opened or measured at `9d13768c…`.
