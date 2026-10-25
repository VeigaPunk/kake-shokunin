# CriticHarm — round 51 wave 1 (owned axes: operability, freshness)

Seat: `L1Kake51.CriticHarm-2`. Scope: can round 51's committed bytes be shown to harm an owned
axis? Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (lane tip). Base:
`007d66e4e8360a5f88d29a93eeedd8066dad4434`. Read-only; only this file was written. No tool
install or upgrade was made. The worktree was **not** static during this review: co-running seats
modified five tracked files (`PROVINCE.md`, `SCORECARD.md`, both admitted entries, and the mirror
`SOURCES.md`) while it ran, so every claim below is pinned to `git show <rev>:<path>` blobs, not to
a worktree read.

## Verdict

**No harm observed to operability or freshness from this round's committed bytes.** All three
standing gates exit 0. Five attacks were run; four clear the claim, one leaves a reproducibility
caveat that does not flip any condition (A2). A transient live-tree anomaly is recorded (A4); it
is not in committed bytes.

## Standing gates — the three named in the assignment, with real exits

| # | command | exit | what it printed |
|---|---|---|---|
| 1 | `node scripts/freshness-sweep.mjs --selftest` | **0** | `selftest: 35/35 passed` (hermetic `/tmp/kake-r16/selftest`; write-confinement mutation proof 27/27 mutants, 31/31 pinned APIs) |
| 2 | `python3 -B scripts/citation_lint.py --root /home/vgpnk/Projects/shokunin/kake-shokunin` | **0** | `"verdict": "clean"`, `"violations": 0`, population `["SCORECARD.md","LOG.md"]`, 31 adjudicated citations |
| 3 | `python3 -B scripts/ledger_latest_check.py` | **0** | `rescore-tally MATCH quoted=14 derived=14`; `donothing-ratios MATCH T1 4.21, T5 7.05`; `build-ratio-range MATCH T1 1.00–1.01, T5 1.11–1.22`; `ledger-quotes: 3 figures, 0 mismatches` |

Additional reader-runnable gates (not in the assignment, run to widen the net):

| command | exit | output |
|---|---|---|
| `node scripts/corpus-contract.mjs` | **0** | `0 findings · 40 knowledge entries · 46 lane lessons · 35 skipped · 0 errors` |
| `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <lane>/.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` | **0** | stdout **byte-identical** to the committed `census-stdout.txt` |
| same census, `--file <lane>/corpus/SOURCES.md` (live registry) | **0** | same 12 `W04` duplicate-URL findings, no `E`-finding |
| `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768…` | **0** | `C2 quote-truth 8/8 met=True` |
| `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768…` | **1** | `C1 ledger 0/3 met=False` (L1/L3: settlement absent; L2: route map absent) — expected: the wave evidence is post-settlement work named in the dispatch |
| `node scripts/freshness-sweep.mjs` (live, not `--selftest`) | **1** | `VERDICT: DRIFT — §armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly` |

The live sweep's exit 1 is **not attributable to round 51**. Control: a `/tmp/c51base` clone
(`git clone --no-hardlinks`, then `checkout 007d66e`) run of the same script also exits **1** with
byte-identical verdict lines; `declaredAbsent 65 · drift 0 · unresolved 10` on both sides, and
`set-delta miss: no new miss`. The only delta is the three corpus files this round adds
(`files 125→128`, `set-delta +69→+72`): `canonical-selection.md`, `crawler-identity.md`,
`lessons/round-51.md`. The drift lives in external pins (`PQ-2` remote moved, `ds4cc` sitemap,
`plazir-15-site`), not in the lane corpus.

## Attacks run

**A1 — "the pre-append mirror already contains the append."**
`git show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` carries S262/S263
at lines 152–153, its `canonical-selection.md`, `crawler-identity.md` and `lessons/round-51.md` are
byte-identical to the live counterparts at the append commit (`git show 19a99bd:<mirror> | cmp -`
`<(git show 5591557:<live>)` — all four IDENTICAL), and 127 of 130 mirror corpus files equal the
live tree at that commit. **Disposition: cleared, not harm.** LOG.md discloses the design ("the mirror is the
lane's `corpus/` plus the two new rows and the two admitted knowledge files"); it is a candidate
tree validated before landing the live registry, the correct shape for "validate the exact bytes
you will write". The ordering condition C8 does not read the mirror copy: `REGISTRY` is
`corpus/SOURCES.md`, and the counter reads `show(root, mirror_commit, REGISTRY)` — the live
registry at `19a99bd`, which holds 143 rows and **0** of the two ids, versus 145 at the tip. The
census receipt is reproducible: re-running it against the committed mirror file today exits 0 with
stdout identical to the committed receipt.

**A2 — "the counter was edited after the declaration."** Real, disclosed, no false pass.
Running the **declaration-time** counter blob (`git show 19a99bd:.ufo/waves/round-51/c51_quote_truth.py`)
against the measured revision prints **`C2 quote-truth 7/8 met=False`, exit 1**, failing C6 with
`S262/S263: no receipt in …/receipts.json` — the counter looked for the receipts at the top level
while `receipts.json` nests them under `sources`. Commit `9d13768` adds the 2-line unwrap and the
counter then scores 8/8. LOG.md records the fix, its cause, and the re-runs (base 0/8, junk control
fails 3/8). The predicate string, the eight condition sentences, the sha256 equality test and the
row-URL test are unchanged, so no condition is weakened — but the *artifact* named by the contract's
counting command is not frozen. Residual caveat, smallest safe correction: name the counter's blob
sha in `contract.json` (or in the LOG line) so a reader knows which counter produced the 8/8.

**A3 — "the assigned row ids are an identity change."** The shokuknow package stages the same two
URLs as **S149/S150**; the lane landed them as **S262/S263**. Cleared: ids are lane-local (the
campaign absent-defect register itself reuses `S262` for `mori` round 4), the round's staged pool
is S250–S370 (`assimilation/staged-ids`), and the live registry has no second row for either URL
(`…/canonicalization` matches only S262; `S022` is `canonicalization-troubleshooting`; `…/googlebot`
matches only S263). Census over the live registry exits 0 with no `E`-finding. Documentation nit
only: the lesson's "Id collision check" never states the S149/S150 → S262/S263 mapping.

**A4 — transient live-tree write (recorded, not committed).** At ~03:36–03:37 −03:00 a row
`| S149 | Google Search Central — What is URL canonicalization — …/canonicalization | docs | A | …`
appeared at `corpus/SOURCES.md:154` in my read. On re-read the line was gone;
`git show HEAD:corpus/SOURCES.md | grep -c S149` = 0, `git diff --quiet HEAD` clean, row count 145
at `5591557` and at HEAD. The row was in scratch at review time — `/tmp/row-s149.txt`
(mtime 03:36:21 −03:00, 900 B, id S149, same URL as S262, gate text "…Google selects the most
complete and useful page…") and the package head `/tmp/pkg-head.md` (mtime 03:34:53, lines 19–20 =
S149/S150) — so a co-running seat was exercising that prototype row against the live registry.
Both scratch files are external to the lane and may be swept; the finding does not depend on them:
the durable evidence is `HEAD` carrying no S149 row while the worktree read did. No committed harm;
a live-tree hazard to operability while the wave runs.

**A5 — "C1 is non-discriminating today."** `c51_wave_ledger.py` prints 0/3 at the tip and the
committed control `controls/c1-before-base.txt` prints the same 0/3 for `007d66e`. The instrument
is introduced in-round and its evidence lands after settlement, so the base control is a recorded
receipt, not a re-runnable command: `.ufo/waves/round-51/` does not exist at `007d66e` (verified in
the `/tmp/c51base` clone), so the contract's counting command cannot run at base. Not harm — the
dispatch fixes the order — but the operability claim is **not yet provable from committed bytes**:
at the measured revision C1 remains 0/3.

## Impacted axes

- **operability** — no regression found: corpus contract 0, census 0 (live and mirror), ledger
  check 0, both counters execute. C1 is 0/3 by design, not by breakage.
- **freshness** — no regression found: two entries + one lesson add three corpus files, sweep
  reports `set-delta miss: no new miss`, citation lint clean, and the live drift is present
  identically at base.

## Not run / not readable

- Contract's C1 command at base `007d66e`: file absent (as above); the base 0/3 is quoted from the
  committed control, not re-derived by me.
- `citation_lint` was run at the lane root only; its population is `SCORECARD.md` + `LOG.md` by
  design, so it does not lint the new corpus entries (the corpus-contract gate covered their shape,
  and the freshness sweep covered their path citations).
- The live freshness sweep depends on external state (`~/Projects/plazir-15-site`, the `ds4cc`
  sitemap, the `origin` remote); its exit 1 is environment-dependent and was reproduced at base.
