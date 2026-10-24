# Rejection05S011: falsify the L1 rejection of S011 K-11 (freshness-sweep.md:58)

Round 26 · C1 freshness · milestone r26-recheck-falsify · leaf critic (no dispatch)
Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.

## Verdict: AGREE (the rejection is correct)

I tried to show that the rejection hides staleness and could not. The pointer
`corpus/knowledge/freshness-sweep.md:58` in `crawl-scope-per-host.md:22` named
the right row when it was written. Both the base label (`cb807bc`) and the
round-21 register (baseline `5009ecaa`) resolve it to the same row. Under the
round-21 rule, that row is now at line 62, which is exactly what the git
history shows. The seat's STALE verdict came from reading a base-scoped pointer
against current line numbers. QUALITY round 26 classifies that reading as a
note, not a stale claim.

## What was attacked

- Ledger (`statements.json`, pair `S011`): `"seatStale": 1, "stale": 0`,
  `l1Disposition`: "freshness-sweep.md:58 pointer is base-scoped (\"Refines at
  base cb807bc\"); +4 rule covers current coordinates."
- Seat finding (`w1/PairS011CrawlScopePerHost.md`, K-11): "Line 58 is now the
  H4 history row … The only table row naming robots is A4 … now at line 62."
- Rule (`corpus/QUALITY.md:216-221`): "STALE means the statement is wrong or
  unsupported at its own stated scope. … a pointer explicitly scoped to a base
  revision … is not a stale claim … A statement whose attribution was false
  even at its base revision is STALE."

The strongest counterexample would show the attribution was false at base, or
that the +4 rule maps line 58 to the wrong row. Both were tested.

## Evidence

1. **The statement is explicitly base-scoped.** `crawl-scope-per-host.md:20-22`
   (unchanged at B and C): "**Refines at base `cb807bc`.** Makes host/path scope
   explicit for `corpus/knowledge/sitemap-orphan-audit.md:40-47` and
   `corpus/knowledge/freshness-sweep.md:58`; …". `git blame -L 18,26 97404de --
   corpus/knowledge/crawl-scope-per-host.md` attributes all of lines 18-26 to
   `02b6dd0` ("round-20: resume …", 2026-10-19).

2. **The attribution was true at base and when it was written.** The row was
   located with `git show <rev>:corpus/knowledge/freshness-sweep.md | awk
   '/ds4cc sitemap\/robots pre-push/{print NR}'`:

   | revision | role | line of A4 "ds4cc sitemap/robots pre-push state" | line 58 is |
   |---|---|---|---|
   | `cb807bc` | stated base | 58 | A4 |
   | `02b6dd0` | pointer authored | 58 | A4 |
   | `9639ec7` | round-20 post-review | 58 | A4 |
   | `5009ecaa` | round-21 register baseline | 58 | A4 |
   | `df6196b` | round-21 four-line prefix | 62 | H4 |
   | `97404de` (B) | base | 62 | H4 |
   | `e28312b` (C) | candidate | 62 | H4 |

   A4 is a host-scoped robots/sitemap row for ds4cc. That matches the
   statement's purpose: separating the ds4cc.com history from
   `veigapunk.github.io`.

3. **The +4 rule applies and lands on the right row.**
   - `corpus/lessons/round-21.md:113-118`: "For each listed file: old line N at
     baseline `5009ecaa` is current line N+4."
   - `:127`: "| freshness-sweep.md | N → N+4 |"
   - `corpus/QUALITY.md:69-71`: "All pre-round-21 literal pointers … retain their
     baseline coordinates. Add four for current coordinates …".
   - `git merge-base --is-ancestor 02b6dd0 5009ecaa` succeeds, so the pointer is
     pre-round-21. `5009ecaa:crawl-scope-per-host.md:22` already contains
     "`corpus/knowledge/freshness-sweep.md:58`".
   - 58 + 4 = 62, and line 62 at B is "| A4 | armed | ds4cc sitemap/robots
     pre-push state | `sitemapStatus` 404 | `200` → `LISTED-LIVE` |".

4. **No other drift.** `git log cb807bc..97404de -- corpus/knowledge/freshness-sweep.md`
   lists `02b6dd0`, `9639ec7`, `df6196b` and `3d07733`. The table above shows
   that only `df6196b` moved the row. The round-24 commit `3d07733` is a
   pure EOF append (`@@ -188,0 +189,13 @@`, 13 insertions). The diff from B to C
   does not touch `freshness-sweep.md`.

5. **The S011 substance holds in the retained bytes.**
   `fetched/text/S011-1.txt` contains "in the top-level path of the service" ×1
   and "scheme:[//authority]/robots.txt" ×1. That is the RFC 9309 §2.3
   host-root rule the refinement relies on (manifest sha256 `bbaa2806…`,
   HTTP 200, 2026-10-21T15:10:38Z).

## Non-blocking notes (no verdict change)

- **The candidate's append names a different baseline.** Under
  "## Round-26 source recheck", `crawl-scope-per-host.md` (C) says: "Pointers
  labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate
  rule)". The round-21 rule's baseline is `5009ecaa`, not `cb807bc`. The two
  agree for this pointer only because lines 1-58 of `freshness-sweep.md` are
  positionally identical across `cb807bc` → `5009ecaa` (evidence 2). The
  outcome is still correct. A precise wording would be "baseline `5009ecaa`
  (+4 per lessons/round-21.md register); for this file `cb807bc` and
  `5009ecaa` coordinates coincide."
- **The seat's K-10 HOLD read the wrong coordinates.** For the sibling pointer
  `sitemap-orphan-audit.md:40-47` (same base label; that file is also in the
  +4 register, `round-21.md:137`), the seat judged current lines 40-47.
  Base lines 40-47 at `cb807bc` ("## Procedure …" through "inside base path")
  are current lines 44-51 at B, and their content is byte-identical. HOLD is
  correct at the right coordinates, so no staleness is hidden. It is the same
  current-versus-base confusion that produced K-11's false STALE.

## Minimal correction

None required for the rejection. Optional wording precision is in the first
note above.

## Commands run

`git cat-file`/`git log`/`git blame`/`git show <rev>:<path>` with awk line
extraction, `git diff -U0`, `git merge-base --is-ancestor`, and a Python stdlib
substring count on `fetched/text/S011-1.txt`. No network GET, no writes beyond
this report. No tools were installed or upgraded.

```json
{"target":"S011 K-11 L1 rejection (crawl-scope-per-host.md:22 -> freshness-sweep.md:58)","verdict":"AGREE","severity":"none"}
```
