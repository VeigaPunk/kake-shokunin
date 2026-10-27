## Superseded axis-table evidence (round 59)

Appended 2026-10-27 (UTC; round 59 opened 2026-10-26 -03:00), append-only. The three
evidence cells below are reproduced byte-for-byte from the axis table of
`SCORECARD.md` at `fd6303ce5c14b3f892dec586297a942ab6e4193b` (rows 17, 18, 19; third
cell of each row) because round 59's C1 claim (`calibration`) replaced those cells
instead of deleting the history. The frozen base counter
`python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <lane> --revision fd6303ce5c14b3f892dec586297a942ab6e4193b`
exits 1 with `mismatches=16` (`controls/base-c1-axis-evidence.txt`), decomposed as
11 unresolved pointers + 3 rows with no on-axis receipt + 2 rows with no tally found
in a cited blob:

- operability — 4 unresolved pointers: `cli.mjs:935` ("not a committed path at the
  revision"), and `:836-839`, `:932`, `:393` ("line pointer with no preceding
  resolved file"); no on-axis round receipt; no tally.
- freshness — 7 unresolved pointers: `corpus/claims` ("not a committed path at the
  revision") and six `/tmp/kake-r17/` files — `scout-claims.md`, `claims-delta.tsv`,
  `critic.md`, `reviewer-cites.md`, `scout-pins.md`, `scout-live.md` ("absolute or
  home path (not committed bytes)"); no on-axis round receipt.
- calibration — 0 pointers at all (so none unresolved) and no tally anywhere in the
  cell; no on-axis round receipt.

The quoted cells are historical evidence, not current pointers: do not resolve them
against today's tree and do not count them as a live table row (each is quoted, so it
begins with `>` rather than `|`). Their byte-exactness is what the round-59 C1 counter
checks with `superseded_kept`.

### operability — base score 10, row 17, evidence cell 1060 bytes

> Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified.

### freshness — base score 10, row 18, evidence cell 1224 bytes

> **r17 HOLD 10:** the standing instrument caught a real between-sweep world change before prose repair: lowercase `~/projects` was consolidated into `~/Projects` and removed, making a cited descendant miss; cite corrected to the surviving canonical report, `pathsMissSet` 9→10. Full r16 inventory re-run: 160 claims (117/117 HOLD; 15/15 r16 stale repairs still correct; 7 carried UNVERIFIABLE; 21 HISTORICAL-OK) + 16/16 new claims HOLD; 9 new deltas found and resolved/qualified (W6 path+mtime/child rename, ETag edge flip, 2 r17 self-stale counts, inode wording, dangling `corpus/claims`, ledger locus, README range gloss). Instrument integrity also improved: `projectsChildrenSet` 36 informational set; `pathsFiles` count→39-entry evaluated list; bad pins now fail closed exit 2 with a permanent case (`--selftest` **10/10**). Final §paths = 66 targets / 49 resolve / 10 declared-absent / 0 drift / 39 files; 33-file state sha guard identical. Live exit 1 remains solely expected PQ-14 `plazir-live-source-gap`. Evidence: `corpus/knowledge/freshness-sweep.md` §r17, `corpus/lessons/round-17.md`, `LOG.md` r17, `/tmp/kake-r17/{scout-claims.md,claims-delta.tsv,critic.md,reviewer-cites.md,scout-pins.md,scout-live.md}`.

### calibration — base score 2, row 19, evidence cell 450 bytes

> Round-58 calibration move: the receipt-ledger counter's measured population had 19 post-commit receipt events with no ledger disclosures at base; at T1 it independently re-derived all 19 events, verified each note pointer/blob/kind, and found 0 undisclosed. This is a bounded calibration improvement (machine disclosure completeness, not a claim that every past run occurred); the new selftest and residual critic preserve the known note-truth limit.
