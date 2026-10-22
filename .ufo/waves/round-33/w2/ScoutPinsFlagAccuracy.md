# ScoutPinsFlagAccuracy — is the `freshness-pins.json` flag accurate? (round 33, wave 2)

Seat: KakeR33.ScoutPinsFlagAccuracy. Lane rev 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0.
Sandbox clone: `/fast/scratch/hyaku/kake-r33/w2/ScoutPinsFlagAccuracy/clone` (checked out at the tip).
Independent public clone: `/fast/scratch/hyaku/kake-r33/w2/ScoutPinsFlagAccuracy/ds4cc-public`.
Upstream read-only clone: `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`. No tool installed.

**Verdict: accurate on both clauses, with three scoped caveats (one omission, one grammar
over-attribution, one over-broad "what it takes").**

Flag under test — `corpus/knowledge/sitemap-orphan-audit.md:245-248`:
"still pins `pq2Remote` `e6bd0718` (29 commits behind `7fc6aa2f`) and `sitemapStatus` 404,
which round-23 live observations already contradicted. Re-pinning needs the sweep's armed
section, which fetches owned sites; it was not run this round."
Same flag without numbers: `SKILL.md:946`. Pin text: `corpus/knowledge/freshness-pins.json:34-36`
(`pq2Remote` `e6bd0718`, `pq2Unpushed` 20, `sitemapStatus` 404; file stamp `round` 24 / `updated`
2026-10-21 at :4-5).

## 1. "29 commits behind 7fc6aa2f" — exact and current

Commands and observed output (exit 0 each):

```
git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream rev-list --count e6bd0718..7fc6aa2f   -> 29
git -C .../ds4cc-upstream rev-list --count --first-parent e6bd0718..7fc6aa2f              -> 29
git -C .../ds4cc-upstream rev-list --merges --count e6bd0718..7fc6aa2f                    -> 0
git -C .../ds4cc-upstream merge-base --is-ancestor e6bd0718 7fc6aa2f                      -> YES
git -C .../ds4cc-upstream for-each-ref refs/heads/main                                     -> 7fc6aa2fc124…a90e884
git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git main                      -> 7fc6aa2f…a90e884
```

Plain count, first-parent count and no-merge count all agree at 29, so no merge-side
inflation. My own `--filter=blob:none` clone made today returned `origin/main = 7fc6aa2f`
and `rev-list --count 7fc6aa2f..origin/main -> 0`, so upstream has not moved again;
the number is not date-rotted as of 2026-10-22. `git log` on the range shows 29 linear
commits from `ecb74b1` (2026-09-29) to `7fc6aa2f` (2026-10-21T17:32:55Z). `e6bd0718`
is dated 2026-09-23, i.e. the pin is a round-16 vintage (see §3), not a round-24 one.

Not the checkout distance: `1fbdb8ed..7fc6aa2f -> 1` (operator checkout
`/home/vgpnk/Projects/ds4cc-marketplace`, HEAD `refs/remotes/origin/main` = `1fbdb8ed`).
The prose attaches the 29 to `pq2Remote`, which is correct; a reader who applies 29 to
the checkout would be wrong, but the text does not say that.

## 2. "`sitemapStatus` 404 … round-23 live observations already contradicted" — confirmed

- Receipt `.ufo/waves/round-23/receipts/sitemap-orphan-audit.json:28-33`: c3
  `status=200, bytes=7565, loc_count=96`, verdict STALE, surface `https://ds4cc.com/sitemap.xml`.
- Independent round-23 seats agree at 200/7,565B: `.ufo/waves/round-23/w1/ReverifyPublishQueue.md:9`
  (also robots 200/62B), `ReverifyKimiSubpathAudit.md:9,16` (96 locs),
  `ReverifyGhpSubpathSpotcheck.md:91`, and `receipts/publish-channels.json:42`.
- The pin line itself has not moved since round 16: `git log -S'"sitemapStatus"' --
  corpus/knowledge/freshness-pins.json` names only `ab87a48` (r16, 2026-09-28); round 24's
  commit `3d07733` touched only `pathsMissSet`/`projectsChildrenSet`/`pathsFiles` plus the
  top-level stamp. So "still pins 404" is true and was never re-baselined.

Caveat A (minor grammar): "which round-23 live observations already contradicted" attaches
to the whole conjunction, but round-23 live GETs bear only on `sitemapStatus`; `pq2Remote`'s
staleness is a public-git fact (S065/S066 path), not a live observation. Low severity; the
parenthetical already separates the two. `SKILL.md:946` does not have this ambiguity.
Under the pins file's own semantics (`_comment`: "equalities are drift predicates"), 404 is
a predicate, not an assertion — but the instrument's designed response to 200 is
`LISTED-LIVE` + exit 1 (`scripts/freshness-sweep.mjs:911-913,923`), so calling it stale and
unrepaired is substantively right.

## 3. Caveat B (omission): a third stale value, `pq2Unpushed: 20`

Measured now, read-only:
`git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse HEAD -> 1fbdb8ed`,
`rev-parse refs/remotes/origin/main -> 1fbdb8ed`,
`rev-list --count refs/remotes/origin/main..HEAD -> 0` (the pin says 20).
The flag names only `pq2Remote` and `sitemapStatus`; it never says "only", so this is
incompleteness, not a false statement. It is also a repeat: round-24 wave-1 already measured
it — `.ufo/waves/round-24/w1/ScribeFreshnessKnowledge.md:49-51` ("`pq2Unpushed` (20) …
The local count now is 0"), and that seat asked for `--section=armed` before re-pinning `pq2*`.
Root cause of the persistence: `freshness-pins.json:2` claims "every value carries the round
that last verified it", but the schema has one file-level `round`/`updated` only; round 24
bumped it for a paths-only edit while `pq2*`/`sitemapStatus` stayed at r16. That comment is
false as implemented and should be corrected (or per-value stamps added).

## 4. Caveat C: "re-pinning needs the sweep's armed section, which fetches owned sites"

True for `sitemapStatus` (a live GET of `https://ds4cc.com/sitemap.xml`, an operator property).
Over-broad for the PQ-2 half: `pq2Remote`/`pq2Unpushed` are settled by `git ls-remote` of the
public repository plus local `rev-list` (`freshness-sweep.mjs:894-904`), no owned-site request.
I did not fetch ds4cc.com; today's live status is therefore unknown to me, and if it returned
to 404 the pin would coincidentally match. The flag's past-tense claim stays true either way.

A genuine armed run on this workstation would not be green for reasons unrelated to this flag:
`/home/vgpnk/Projects/webzites/fleet/fleet.config.json` and
`/home/vgpnk/Projects/webzites/state/probe-history.jsonl` are both absent, so PQ-12 falls back
to the pins value after a caught `fleetError` (`freshness-sweep.mjs:836`, then fetches the live
charter page) and §history stays suspended by `probeHistoryAbsent`.

## 5. What an honest re-pin requires

1. Run the armed section in an authorized round and record expected-vs-observed per check
   first. Re-pinning closes the watches: equality with the pin is the green branch for both
   (`freshness-sweep.mjs:901,911-913,923`), so `GATE-OPENED` (remote `e6bd0718` → `7fc6aa2f`)
   and `LISTED-LIVE` (200/7,565B/96 locs at 2026-10-21) must be written into prose before the
   baseline moves, or the fired event is silently erased.
2. Edit `freshness-pins.json` with values freshly measured in that same round:
   `pq2Remote` → `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`; `pq2Unpushed` → the re-measured
   local count (0 today, measured against the checkout's tracking ref at `1fbdb8ed`);
   `sitemapStatus` → observed status and `sitemapBytes` → observed bytes (informational);
   bump `round`/`updated`.
3. Fix the label coupling before pinning `sitemapStatus: 200`: the equality verdict string is
   hard-coded `'PRE-PUSH'` and the human line suppresses " (listing changed)" on equality
   (`freshness-sweep.mjs:911-913,1002`), so a 200-pinned green run would print
   "PRE-PUSH — status 200/…". The equality label (and the A4 row's "pre-push state" name at
   `corpus/knowledge/freshness-sweep.md:62`) must be generalized, or the re-pin replaces one
   false statement with another.
4. Update the prose in the same commit: audit `:245-248`, `freshness-sweep.md:61-62`,
   `SKILL.md:946`, and the pins `_comment`/stamp semantics.
5. Re-run `node scripts/freshness-sweep.mjs --selftest` and a live run. `scripts/corpus-contract.mjs`
   has no coupling to the live values (only a `{"pins":{}}` fixture at :430), so it does not
   constrain the re-pin. A full-file re-pin cannot be validated offline: my sandbox
   `--section=armed --offline --json` run exited 0 with `complete=false, ok=true,
   skipped=["§armed (all remote checks)"], pq2/sitemap=skipped(offline)`
   (`/fast/scratch/hyaku/kake-r33/w2/ScoutPinsFlagAccuracy/armed-offline.json`).

## 6. Unverified / remaining unknowns

- Today's live `ds4cc.com/sitemap.xml` status: not fetched (owned property; no named-URL
  allowance for this seat). Only the 2026-10-21 round-23 observation is used.
- Whether A3/A4 are intended as consumed events (re-baseline) or frozen baselines left to fire
  every run: a design call for the L1, not resolvable from the bytes.
- The 20 formerly-unpushed commits' identity at r16 was not reconstructed; not needed for the
  flag's accuracy.
