# ScoutRecheckDue — SOURCES rows due for recheck on 2026-10-23

Leaf seat, read-only. Question: which rows satisfy `opened + recheck <= 2026-10-23`, counts by
status, unparseable rows flagged. **Answer: 0 of 87 rows are due on 2026-10-23. Earliest due
date in the registry: 2027-01-17.** Empty is semantic, not a parse failure (§3 self-test).

## 1. Source of truth
Blob `cd3212796cab7a2afa03b638dbfafe7194df9629:corpus/SOURCES.md`, sha256 `dacb540c…7040532`,
176 lines, 87 rows, all NF=13; header `:7`. Working tree equals it (`git diff --stat cd32127… --
corpus/SOURCES.md` empty; `HEAD` = cd32127…). Semantics: CORPUS.md `:108-109` (recheck = ISO
date or cadence `90d`/`180d`/`on-release`) and fleet `scripts/sources-census.sh:675-685` (`NNd`
→ opened + N; ISO → that date; symbolic → `cadence`, never overdue; report when `due <= today`).

## 2. Counts (observed)

| status | rows | 90d | 180d | 365d | on-release |
|---|---|---|---|---|---|
| mined | 64 | 51 | 0 | 9 | 4 |
| queued | 8 | 3 | 0 | 0 | 5 |
| rejected | 15 | 14 | 1 | 2 | 0 |
| total | **87** | **68** | **1** | **11** | **7** |

kind: cadence 80, ISO date 0, symbolic 7, **unparseable 0**; no `7d`/`30d` row. `opened`:
18×10-19, 9×10-20, 8×10-21, 52×10-22 — none before 2026-10-19, so none can be due.

**Due list on 2026-10-23: empty** (0 rows, no URLs). Next due dates:

| due | rows | status | ids |
|---|---|---|---|
| 2027-01-17 | 10 | mined 7, queued 2, rejected 1 | S003-S007, S013-S017 |
| 2027-01-18 | 5 | mined 5 | S021-S025 |
| 2027-01-19 | 2 | mined 2 | S030, S031 |
| 2027-01-20 | 51 | mined 33, rejected 13, queued 5 | S036-S087 less S056 |
| 2027-04-17 | 1 | rejected 1 | S018 (180d) |
| 2027-10-19 | 5 | mined 5 | S008-S012 |
| 2027-10-20 | 1 | mined 1 | S020 |
| 2027-10-21 | 5 | mined 5 | S028, S029, S032-S034 |
| never time-due | 7 | mined 6, queued 1 | S001, S002, S019, S026, S027, S035, S056 |

## 3. Reproduce (run, exit 0)

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cd3212796cab7a2afa03b638dbfafe7194df9629:corpus/SOURCES.md | awk -F'|' -v today=2026-10-23 '
function ep(s, a){ if (s !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) return -1; split(s,a,"-"); return mktime(sprintf("%04d %02d %02d 00 00 00",a[1]+0,a[2]+0,a[3]+0),1) }
/^ {0,3}\|[[:space:]]*S[0-9][0-9][0-9]?[0-9]*[[:space:]]*\|/ {
  n++; id=$2; st=$9; rc=$11; op=$10; src=$3; gsub(/[[:space:]]/,"",id); gsub(/[[:space:]]/,"",st); gsub(/[[:space:]]/,"",rc); gsub(/[[:space:]]/,"",op); S[st]++; R[rc]++;
  if (rc ~ /^[0-9]+d$/) { due=ep(op)+substr(rc,1,length(rc)-1)*86400; if (ep(today)>=due) { DUE++; u=(match(src,/https?:\/\/[^ ;,|]+/)?substr(src,RSTART,RLENGTH):"-"); u=gensub(/[.,;]+$/,"","g",u); print "DUE " id " due=" strftime("%Y-%m-%d",due,1) " " rc " status=" st " " u } }
  else if (rc !~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) SYM++
}
END { printf "rows=%d due=%d symbolic=%d status:", n, DUE+0, SYM+0; for (k in S) printf " %s=%d", k, S[k]; printf "\nrecheck:"; for (k in R) printf " %s=%d", k, R[k]; print "" }'
```
Output, exit 0: `rows=87 due=0 symbolic=7 status: mined=64 queued=8 rejected=15` /
`recheck: 365d=11 on-release=7 180d=1 90d=68`. Self-test, same command with
`-v today=2027-01-18`: 5 `DUE` lines carrying ids and URLs (e.g.
`DUE S003 due=2027-01-17 90d status=mined https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site`),
exit 0 — so the extractor and URL grab work and `due=0` is not a broken parse.
Cross-checks, all exit 0, all agreeing: `scripts/sources-census.sh overdue --file <blob>
--today 2026-10-23` (87 `cadence`, 0 `overdue`); my `/fast/scratch/hyaku/kake-r36w1/
ScoutRecheckDue/recheck_due.py <blob> 2026-10-23`; `scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin kake --today 2026-10-23` → `kake ok`, only `W04 S033`.

## 4. Findings for the L1 (advisory)
1. **C1's due-scoped target set is empty.** "Re-check rows due 2026-10-23" names zero rows and
   measures nothing — the round-34/35 failure shape again. A real row set must be named in
   advance (all 87, the 7 symbolic rows, or S088-S094 once written), not selected by due date.
2. **`opened` is the only anchor and is immutable** (CORPUS.md:106 allows only
   status/recheck/used-by to change). Round 26 re-fetched and judged HOLD 32 rows on
   2026-10-21 and changed no cell (`corpus/lessons/round-26.md:33`; SourceRulesConnect §5.2
   proposed ISO next-due dates — the registry has **0** ISO-date `recheck` cells, so that
   advance never landed). S003-S007 still compute 2027-01-17 as if the recheck never happened;
   due-ness and verification recency are unrelated quantities in this registry.
3. **`on-release` is undecidable offline** (7 rows; census never judges it overdue). No row
   records an observed release state, and 2 of 7 have no URL: S019 `:27` (own-work local
   script), S056 `:64` (sibling path tameshi `f4e8f7d8`). A URL-only tool silently skips both.
4. **Rejected rows keep live schedules** — 15 rows due 2027-01-17 (S017), 2027-01-20 (13),
   2027-04-17 (S018). A `status=mined` filter drops a sixth of the schedule; state it if used.
5. **Not verified:** event triggers for the 7 symbolic rows (needs network/release state, out
   of scope); the sealed tree and counter were never read, statted or run; no network used.
   Nothing here is an admission or verdict on the round.
