# ScoutMisroot — fleet-root untracked census vs "kake" / "round-51" naming

- Seat: `L1Kake51.ScoutMisroot-2` · lane `kake` · round 51 wave 1 · axis: operability
- Measured fleet repo: `/home/vgpnk/Projects/shokunin` at `8052650d1c76`
- Measured lane revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`
- Every statement below is from a command I ran in this session; no other seat's conclusion is reused.

## Command

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
```

Result: **15 modified** (12 tracked `.ufo/state/*.report-baseline` — chousa, kagi, kaidoku,
kake, kama, kengaku, kumitate, mado, mori, souji, tameshi, tsukuroi — plus `.ufo/watchdog.log`,
`scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md`) and **17 untracked** paths.

Each untracked file was read (full-content case-insensitive regex
`kake|round[-_ ]?51|r51|round51`, plus a 600-byte head / title extraction for the large bodies).
The name was never used as evidence.

## Classification table (17 untracked paths)

| # | path | observed content (first-hand) | names `kake` | names round-51 | classification |
|---|------|-------------------------------|--------------|----------------|----------------|
| 1 | `.omp/mcp.json` | JSON MCP config, one disabled stdio server `rea-agents@6.7.0` | no | no | neither; tool config |
| 2 | `.scratch/goal-20261025-hyaku-12h.md` | hyaku run-6 12h plan; line 56: `No report: kake r51, kotodama r69, mado r35, revenger r68, tameshi r41 →` | **yes** (1 line) | **yes**, as `r51` (same line) | names both; operator-run scratch note about an orphaned attempt-1 claim |
| 3 | `.ufo/state/kotoba.report-baseline` | `68 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | no | no | neither; driver runtime (pid + sha256 of empty) |
| 4 | `.ufo/state/kotodama.report-baseline` | `69 e3b0c442…b855` | no | no | neither; driver runtime |
| 5 | `.ufo/state/revenger.report-baseline` | `68 e3b0c442…b855` | no | no | neither; driver runtime |
| 6 | `bm.json` | Cloudflare "Just a moment..." interstitial (HTML despite `.json`) | no | no | neither; blocked-fetch capture |
| 7 | `live.html` | National Museum of Ireland — Collections Online page (gtag, `rel=canonical`) | no | no | neither; site page capture |
| 8 | `live_s228.html` | Anubis v1.26.2 proof-of-work challenge, `issuedAt 2026-10-22T17:45:20+02:00`, UA `Mozilla/5.0`, `X-Real-Ip 179.218.13.209` | no | no | neither; blocked-fetch capture |
| 9 | `nama.html` | National Archaeological Museum — "Page not found" | no | no | neither; 404 capture |
| 10 | `s395.txt` | empty file, 0 bytes | no | no | neither; empty placeholder |
| 11 | `scripts/hyaku/append-closure.py.bak-20261023T040735Z` | generic hyaku closure appender (names `hyaku`/`shokunin` only) | no | no | neither; stale script backup (differs from live tracked `append-closure.py`) |
| 12 | `scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` | generic hyaku fleet-commit helper (names `hyaku`/`shokunin` only) | no | no | neither; stale script backup (differs from live tracked `fleet-commit.sh`) |
| 13 | `tf_bavelas.html` | Cloudflare "Just a moment..." interstitial | no | no | neither; blocked-fetch capture |
| 14 | `unblob.log` | unblob run log, `file=/tmp/test-fw.bin`, extraction dir `.` | no | no | neither; tool log from other work |
| 15 | `wb2.html` | Wayback Machine "suspected abusive bot traffic" block page | no | no | neither; blocked-fetch capture |
| 16 | `write` | 25 bytes exactly `agent://U100N079H334f935b` (no newline) | no | no | neither; spilled `write`-tool payload (agent URI mistaken for a path) |
| 17 | `xc.xml` | Perseus "Too many requests" (429) page | no | no | neither; blocked-fetch capture |

Counts: 1 names `kake`; 1 names round 51 (same file, abbreviated `r51`); 16 name neither.

## Findings

**F1 — no kake/round-51 artefact is misrooted in the fleet tree.** Of 17 untracked paths, the
only one whose bytes name this lane and this round is `.scratch/goal-20261025-hyaku-12h.md`
line 56, and it names them as a *stale-claim worknote* ("No report: kake r51 … → `fail`"),
not as wave evidence. Nothing untracked in the fleet root is evidence for C1 or C2.

**F2 — the three untracked baselines are untracked by policy, not by accident.** Content is
`<pid> <sha256-of-empty-file>`; no lane or round identifier. `scripts/hyaku/fleet-commit.sh`
refuses these paths explicitly: `case $p in .ufo/state/*|.ufo/watchdog.log) … exit 64`. So no
lane can commit them and their untracked state carries no signal.

**F3 — the ten scratch/fetch items are inert and unlinkable to the claims.** None of the ten
contains `kake`, `round-51`/`r51`, `S262`/`S263`, `developers.google.com`,
`search/docs/crawling-indexing`, `googlebot` or `canonicalization` (full-file grep on each).
Five are anti-bot/error pages (Cloudflare ×2, Anubis, Wayback block, Perseus 429), one is a
site page, one a 404, one an unblob log, one an empty file, one a 25-byte spilled agent URI.
`live_s228.html` carries a source-row-shaped *filename* (`s228`), but its body is an Anubis
challenge — content cannot substitute for a retained source body. As receipts they could only
be tied to any claim through an out-of-band filename mapping that the bytes do not contain.

**F4 — the two `.bak` files are stale copies, not lane artefacts.** Both differ from the live
tracked scripts (`diff -q` → DIFFERS) and mention only `hyaku`/`shokunin`; they are generic
driver code, dated from the `…20261023T040735Z` snapshot.

**F5 — structural invisibility between the two repos.** `git check-ignore -v kake-shokunin`
→ `.gitignore:1:*-shokunin/`. The lane root is ignored by the fleet repo, so lane bytes can
never appear in this status; the fleet-root census therefore cannot prove absence of
kake/round-51 artefacts *inside* the lane, and the lane repo is the only place round-51
evidence can be observed (see below).

**F6 — mtime attribution (no naming force).** 13 of 17 share mtime
`2026-10-24 18:07:20.653` — one restore/extract batch; `.scratch` goal `2026-10-25 03:34`;
baselines `22:45`, `03:23`, `03:23`. This supports F3/F4 (bulk scratch) but decides nothing.

## Operability cross-check against the two frozen claims (read-only, lane repo)

Both counters are documented as `git show`-only. Commands and printed results:

1. `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root <lane> --revision 9d13768c…`
   → `C2 quote-truth 8/8 met=True`, exit **0** (all of C1..C8 `pass`).
2. `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root <lane> --revision 9d13768c…`
   → `C1 ledger 0/3 met=False`, exit **1**; L1 `settlement receipt absent at the measured
   revision`, L2 `route map absent at the measured revision`, L3 same as L1.
3. Same two counters at the base `007d66e4…` → C2 **0/8** exit 1, C1 **0/3** exit 1. The
   do-nothing controls in `contract.json` hold.
4. C1's 0/3 is structural at this revision, not a counter defect: the ledger's constants are
   `SETTLEMENT=settlement.json`, `TASKCALL=w51-taskcall.json`, `ROUTE_MAP=route-map.json`,
   `PROBE_DIR=route-probes`, `TIMING=wave-timing.json`, `ACCOUNTING=round-time-accounting.json`,
   `GRANT=wave-grant.txt`, `LOG=LOG.md`, reports under `w1/`. `git ls-tree -r HEAD --
   .ufo/waves/round-51` lists 158 tracked files but **none** of those; `git ls-tree -r HEAD --
   .ufo/waves/round-51/w1` lists **0**. They exist only as untracked worktree files
   (`route-map.json`, `route-probes/` ×9, `w51-taskcall.json`, `wave-grant.txt`,
   `wave-start-utc.txt`) or not at all (`settlement.json`, `wave-timing.json`,
   `round-time-accounting.json`). Because the counter reads committed bytes only, no revision
   reachable today (base or tip) can pass L1. Committing the wave artefacts — and this report —
   is the only action that can move C1.
5. **Freeze-hygiene fact for C2 (attack surface, not a verdict).** `contract.json` was frozen
   at `19a99bd` ("declare the two claims, freeze both counters …"). `9d13768` then adds two
   lines to `c51_quote_truth.py`:
   `if isinstance(receipts.get("sources"), dict): receipts = receipts["sources"]`.
   `receipts.json` top-level keys are `[schema, fetchedAt, fetcher, access, sources]`, so the
   fix is load-bearing. I ran the **frozen bytes** (`git show 19a99bd:…` → `/tmp/…`, read-only)
   against the measured tip: it prints `C2 quote-truth 7/8 met=False`, `C6_receipt_pins FAIL —
   S262/S263: no receipt in …/receipts.json`, exit **1**. Only the post-freeze amended counter
   yields 8/8 at the same revision. `LOG.md` discloses the change, dates it "before any wave
   seat scored", and asserts predicate/conditions/evidence unchanged. Whether a post-freeze
   counter edit is compatible with "declared and frozen BEFORE any score" is a reviewer call;
   the byte-level fact is that the declared command as frozen does not reproduce 8/8.

## Limits / unknowns

- Large HTML bodies were classified by whole-file regex plus head/title extraction, not by
  reading every line; the naming question is closed by the full-file regex, and no header-only
  inference is made about their body text beyond what the regex searched.
- The lane's `w1/` grew between two of my reads (4 → 7 files: `ExecAccountingPrototype.md`,
  `ExecRowShape.md`, `MutationRoute.md` appeared) — concurrent seats. All revision-based claims
  above are pinned to `9d13768c…`, not to the moving worktree.
- At report time the lane worktree also carried uncommitted **tracked** edits that are not mine:
  `SCORECARD.md` +33 lines (a "Round 51 — declared claims" section) and `corpus/SOURCES.md`
  +2 lines (a new `S160` crawl-budget row). They lie outside the measured revision; the frozen
  counters do not read them, and they must be committed deliberately, not swept in, before any
  final measurement.
- No tools were installed or upgraded. Scratch: `/tmp/c51_quote_truth_frozen_19a99bd.py` only.
- Bounds honoured: no mutating git/jj command, no lane or fleet edit other than this file.
