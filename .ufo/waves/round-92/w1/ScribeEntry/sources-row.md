# Round 92 — ScribeEntry — draft `corpus/SOURCES.md` row for RFC 9111 §4.2.2

**Status: draft only. `corpus/SOURCES.md` was NOT edited by this seat** (the L1 appends it).
The row below is the exact one-line form the L1 should append to the `## Registry` table in
`corpus/SOURCES.md`, after the last existing row (S469) and before `## Paths`.

- **id** `S470` — next unused after S469 (the highest id in the registry at the time of writing is
  S469; `grep -cE '^\| S470' corpus/SOURCES.md` → 0 before this draft). No existing row carries
  RFC 9111 §4.2.2: `grep -n '4\.2\.2' corpus/SOURCES.md` returns only S028, which is **RFC 9110**
  §4.2.1/§4.2.2 (URI schemes) — a different document, a different section, a different topic. So this
  row is a new scope on the same URL as S467/S469 (the census will raise one advisory W04
  "duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes"; W04 does not affect the exit
  code — see the round-91 census receipts for the same pattern on S469).
- **tier** A · **kind** spec · **status** mined · **recheck** 180d · **opened** 2026-11-04
- **used-by** `corpus/knowledge/heuristic-freshness.md`

## The row (one line, eleven cells)

```
| S470 | RFC 9111: HTTP Caching, section 4.2.2 Calculating Heuristic Freshness — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | When a cache may assign a heuristic expiration time, when it must not, which responses heuristics may be used on, and the encouraged fraction of the interval since Last-Modified; grounds the heuristic-freshness decision instrument's permission, prohibition, cacheability gate and 10% fraction; distinct from S461's duplicate/lifetime reading, S462's age arithmetic, S469's request-directive/lifetime/stale-serving reading and S028's RFC 9110 URI-scheme scope | Section 4.2.2 heading plain-text line 686, permission lines 688-693, prohibition lines 695-696, cacheability restriction lines 697-701, fraction and 10% lines 706-709; June 2022; fetched 2026-11-05T00:30:25Z HTTP 200, 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; retained .ufo/waves/round-92/L1/src/rfc9111.txt (same digest) | A cache may assign a heuristic expiration time only when no explicit time is specified, must not use heuristics when an explicit expiration time is present, may use them only on responses without explicit freshness whose status is heuristically cacheable or that are marked explicitly cacheable, and is encouraged to use no more than some fraction of the interval since Last-Modified, with 10% typical | mined | 2026-11-04 | 180d | corpus/knowledge/heuristic-freshness.md |
```

## Cell-by-cell

| # | cell | content |
|---|---|---|
| 1 | id | `S470` — next unused after S469; never reused |
| 2 | source | `RFC 9111: HTTP Caching, section 4.2.2 Calculating Heuristic Freshness — https://www.rfc-editor.org/rfc/rfc9111.txt` (title — canonical URL) |
| 3 | kind | `spec` |
| 4 | tier | `A` — tier is scoped to this row's scope (a normative standards document for the topic it names), not a global judgment |
| 5 | scope | what the section decides and what it does not: permission, prohibition, cacheability gate, fraction; distinct from S461/S462/S469 and from S028 (RFC 9110 URI schemes) |
| 6 | anchor | exact plain-text line numbers of the heading and of the four rule bodies, the RFC's month (June 2022), the fetch date/status/bytes/sha256, and the retained path with its digest |
| 7 | teaches | one grounded learner benefit: the four rules, in the source's own words, including that 10 % is *typical*, not required |
| 8 | status | `mined` — the row is cited by `corpus/knowledge/heuristic-freshness.md` |
| 9 | opened | `2026-11-04` (the round date; the source was opened this round by this seat — see `receipt.txt`) |
| 10 | recheck | `180d` |
| 11 | used-by | `corpus/knowledge/heuristic-freshness.md` |

## Constraints the L1 should observe when appending

1. **Append only.** No existing row's cell is touched. The table row must be inserted between the
   S469 row and the `## Paths` heading.
2. **No `|` inside any cell.** The row above has 12 pipe characters (13 fields for a
   `|`-delimited line with a leading and trailing pipe) — the census's `NF!=13` check counts 13
   fields for the manual census; re-run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
   after the append and expect exit 0.
3. **Ordering with the knowledge entry.** The census's `used-by` check requires the cited path to
   exist on disk; `corpus/knowledge/heuristic-freshness.md` is written by this seat, so the entry
   must land before the census is validated. (Round-91 scribe recorded the same sequencing
   constraint, F8.)
4. **One advisory warning expected.** W04 "duplicate url www.rfc-editor.org/rfc/rfc9111.txt across
   scopes" — the same URL is already carried by S467 and S469 on different sections. W04 is advisory
   and does not change the exit code.
5. **No credential material, no private URL.** The row names only a public RFC URL.
