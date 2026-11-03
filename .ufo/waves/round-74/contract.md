# kake round 74 — frozen contract (attempt 1)

Author: L1 `KakeR74`. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Base revision:
`ced2878a1e77f57afb4ee3baebf1021e5130399b` (lane master at round open; `jj-lane.sh state` ahead=0
behind=0). Frozen before any seat ran: the predicates, populations, counters, controls and kill rules
below are fixed. A rule changed after any seat has scored is not this claim's rule.

Round shape: ONE v1 wave `w1`, 14 seats (policy band 8–16), roles scout 2, executor 4, scribe 2,
reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1. Attack share 4/14 ≈ 28.6 %
(reviewer, critic, mutation-tester). The L1 holds the planner seat (the wave validator rejects
`planner`; the mapping is recorded in the report). No residual call is planned; a residual is ≤4
seats and counted in the round total.

## Pre-freeze diagnosis (disclosed; measured before this file was written)

- **C1:** at base, 7 of the 8 counters named by the frozen contracts of rounds 69–73 have no
  `SKILL.md` gate-registry table row; only `c73_tmp_v3.py` is registered. Receipt:
  `controls/base-c1-registry.txt`.
- **C2:** at base, `corpus/knowledge/freshness-sidecar.json` carries 148 `kind=absent` entries and 26
  `kind=restored`; on this host 144 of the 148 absent entries name a token that resolves
  (`stat` ok), 4 name a genuinely absent token (3 distinct tokens), and no restored entry names an
  absent token. Receipt: `controls/base-c2-sidecar.txt`.
- **Blindness control:** the standing freshness sweep at base exits 1 for one unannotated
  `~/projects` miss and never names the 144 contradictions; it cannot see them. Receipt:
  `controls/base-c2-sweep.txt` (run in a scratch clone at base; `--selftest` 36/36).

## Claim C1 — calibration (lowest owned axis; score 2, HOLD)

**Axis:** calibration — the lane's self-assessment (its gate registry) against observed repo state.

**Frozen population (8 counter files, named by the frozen contracts of rounds 69–73, each under its
own round directory):**

| # | Counter | Contract | Path |
|---|---|---|---|
| 1 | `c69_recorded_counts.py` | `.ufo/waves/round-69/contract.md` §C1 | `.ufo/waves/round-69/c69_recorded_counts.py` |
| 2 | `c69_tmp_honour.py` | `.ufo/waves/round-69/contract.md` §C2 | `.ufo/waves/round-69/c69_tmp_honour.py` |
| 3 | `c70_pointer_audit.py` | `.ufo/waves/round-70/contract.md` §C1 | `.ufo/waves/round-70/c70_pointer_audit.py` |
| 4 | `c71_calibration.py` | `.ufo/waves/round-71/contract.md` §C1 | `.ufo/waves/round-71/c71_calibration.py` |
| 5 | `c71_tmp.py` | `.ufo/waves/round-71/contract.md` §C2 | `.ufo/waves/round-71/c71_tmp.py` |
| 6 | `c72_tmp_v2.py` | `.ufo/waves/round-72/contract.md` §C2 | `.ufo/waves/round-72/c72_tmp_v2.py` |
| 7 | `c73_tmp_v3.py` | `.ufo/waves/round-73/contract.md` §C2 | `.ufo/waves/round-73/c73_tmp_v3.py` |
| 8 | `c73_wave_pointers.py` | `.ufo/waves/round-73/contract.md` §C1 | `.ufo/waves/round-73/c73_wave_pointers.py` |

**Frozen predicate:** C1 is met iff, at the measured revision and over that population,

1. every counter has at least one `SKILL.md` gate-registry **table row** whose cells contain its exact
   filename. A prose mention outside a table row does not count; a row naming the counter in any cell
   counts (the registry uses both first-cell names and alias rows);
2. the counter path named by each such row resolves at the measured revision
   (`git cat-file -e <rev>:<path>` exits 0);
3. the round-74 section's own row names `c74_registry_gap.py` (`own_row=true`).

**Counter:** `.ufo/waves/round-74/c74_registry_gap.py` — offline, committed bytes only.
`0=met / 1=not met / 2=unevaluable / 64=usage`; `--revision <rev>`, `--root <lane>`, `--json`,
`--selftest` (fixture set, function-level or scratch-tree). The counter's run at base MUST reproduce
`controls/base-c1-registry.txt` exactly (`unregistered=7`, `met=false`, exit 1); a mismatch is a defect.

**Before (base):** `unregistered=7` of 8, `own_row` absent → exit 1.

**Do-nothing control:** a round that adds no registry row leaves `unregistered=7`; the base receipt is
that control, and the counter is required to reproduce it at base.

**Kill rule (after-state):** C1 fails if `unregistered > 0`, or any population row's counter path does
not resolve at the measured revision, or `own_row=false`, or the counter's `--selftest` does not kill
every one of its fixtures: (f1) an unregistered population counter; (f2) a row naming a counter in a
non-first cell must count as registered; (f3) a prose-only mention must not count; (f4) a row whose
entry-command path does not resolve must fail conjunct 2; (f5) a missing/renamed counter file must be
`unevaluable`, never silently met.

**After target:** `unregistered=0`, `own_row=true`, every row path resolves, counter exit 0.

## Claim C2 — freshness (score 10, HOLD)

**Axis:** freshness — stale self-assessment claims re-verified against the live host and fixed.

**Frozen predicate:** C2 is met iff, at the measured revision,
`python3 -B .ufo/waves/round-74/c74_sidecar_reobserve.py --root . --revision <rev>` prints
`absent_notes_resolving=0 restored_notes_absent=0 unevaluable=0 met=true` and exits 0, and

1. every entry of `corpus/knowledge/freshness-sidecar.json` whose prior `kind` was `absent` and whose
   token resolves on the measuring host is `kind=restored` with a new note carrying the re-observation
   date `2026-11-03`, the host class, and a `stat ok` present-state statement;
2. every flipped entry preserves its prior note byte-for-byte in a `history` array (entries
   `{date, kind, note}`), so no prior observation is lost;
3. every new note for a `kind=restored` entry does not match the sweep's absence vocabulary
   (`absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing`);
4. the sweep's sidecar binding validation accepts the file:
   `node scripts/freshness-sweep.mjs --selftest` = `36/36 passed`, and
   `node scripts/freshness-sweep.mjs --offline` exits 0 or 1 with no `Error:` line and the same
   single named drift class (`~/projects`, the open L0 `kake | round-69` case) — never exit 2.

**Counter:** `.ufo/waves/round-74/c74_sidecar_reobserve.py` — offline; resolves each entry's token
with `os.stat` (present / absent on `FileNotFoundError`/`NotADirectoryError` / unevaluable on any
other `OSError`), expands `~/` from `HOME`, never follows an entry's `file` field for existence.
`0=met / 1=not met / 2=unevaluable / 64=usage`; `--revision`, `--root`, `--json`, `--selftest`.
The counter's run at base MUST reproduce `controls/base-c2-sidecar.txt` exactly
(`entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 restored_absent=0
contradictions=144 met=false`, exit 1); a mismatch is a defect.

**Repair tool:** `scripts/sidecar_reobserve.py` — `--check` (report only), `--write --date 2026-11-03
--host <class>` (rewrite the sidecar deterministically), `--selftest`; refuses to flip an unevaluable
entry; preserves the prior note under `history`; writes no file when `--check` is used; honours
`TMPDIR` and accepts a scratch argument; carries no `/tmp` code literal.

**Before (base):** `contradictions=144` → exit 1 (`controls/base-c2-sidecar.txt`).

**Blindness control:** `controls/base-c2-sweep.txt` — the standing sweep exits 1 with
`VERDICT: DRIFT — §paths: 1 unannotated miss` and never names the 144 contradictions; the lane's
instrument cannot see them.

**Kill rule (after-state):** C2 fails if `absent_notes_resolving > 0`, `restored_notes_absent > 0`,
`unevaluable > 0`, any history entry differs from the base note bytes, any restored note matches the
absence vocabulary, the sweep binding throws (`paths sidecar binding invalid`), `--selftest` drops
below `36/36`, or `--offline` exits 2 or gains an `Error:` line. It also fails if the counter's
`--selftest` does not kill its fixtures: (g1) a contradicted absent entry; (g2) a stale restored
entry; (g3) an unevaluable probe must exit 2, never 0; (g4) a note with absence vocabulary under
`kind=restored`; (g5) a missing `history` array on a flipped entry; (g6) `~/` expansion from `HOME`.

**After target:** the 144 contradicted entries flipped to `restored` with history preserved and dated
present-state notes; the 4 genuinely absent entries (3 tokens: `~/Projects/plazir-15-site` ×2,
`~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`) stay
`kind=absent`; counter exit 0.

## Harm battery at the landing tip (no axis harmed)

- `node scripts/freshness-sweep.mjs --selftest` → `36/36 passed`; `--offline` exit ≤1, same single
  named drift, no `Error:` line.
- `c66_gate_status_hostportable.py` exit 0 (`members=28`, `agreement` unchanged from base);
  `c70_pointer_audit.py` exit 0; `c72_tmp_v2.py` exit 0 (`findings=[]`);
  `c73_wave_pointers.py` `met=true`; `c73_tmp_v3.py` `--selftest` full and `findings=[]`.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0.
- `git diff <base>..<tip> -- corpus/SOURCES.md` adds only the new rows; no prior row edited.
- No SCORECARD score cell edited; SCORECARD/LOG changes are append-only tails.
- No `/tmp` code literal in any new or edited file (`c73_tmp_v3.py` stays green over `SKILL.md`).

## Frontier / sources (CORPUS.md contract v1)

- Two rows are opened this round by `ScoutSources` and retained under
  `.ufo/waves/round-74/sources/`: `S441` (`https://docs.python.org/3/library/os.path.html#os.path.exists`)
  and `S442` (`https://docs.python.org/3/library/os.html#os.stat`). Each new row's `## Gate` entry
  records the URL, the 2026-11-03 access date and a ≤25-word located quote from the retained bytes.
  C2's instrument and the new knowledge entry cite them (the round's sourced claim).
- Census before: exit 0, 178 rows (`W04` duplicate-URL warnings allowed). Census after must be exit 0.
- Mistake to mine: the round-73 `M3` class — host-relative `kind=absent` notes contradicted 144 times
  on this host, invisible to every lane instrument. Fix: the re-observation tool and counter, shown
  able to fail by the base receipt and the selftest fixtures.
- Assimilation: none. The shokuknow `merge/kake` package adds no row this round; no package source is
  opened, so no package entry is adopted (CORPUS.md rule 4: no row without an admitted entry).

## Seat write scope

The lane checkout `/home/vgpnk/Projects/shokunin/kake-shokunin` is read-only for every seat: seats
never edit production files, never commit, push or run a mutating git/jj command anywhere, never
touch the fleet repo or a sibling lane. Each seat writes only its report and artifacts under
`.ufo/waves/round-74/w1/` (absolute path in its item) and its scratch tree under
`/fast/scratch/hyaku/kake-r74/<seat>/`, which it deletes before yielding. The L1 applies every
production edit after the wave settles.

## Amendment 1 — 2026-11-03, after the W1 attack seats, before any after-state

Terms only. The claims, the frozen populations and the after-targets are unchanged; no lane edit
has been measured yet. Each change closes a defect measured by the wave-1 attack seats
(`w1/CriticClaims.md` §1.2–1.6 and §2.1–2.7, `w1/ReviewerC1.md` H1/H2, `w1/ReviewerC2.md` High).

### C1 amendments

- **A1 (registration cells).** A row credits a counter only when the filename appears in the row's
  **Name**, **Entry command** or **Self-test** cell. A filename only in the Kind, Verdict,
  Pinned-values, Write-scope or Owner cell does not register it. Measured false positive this
  closes: `SKILL.md:1198` cites `c46_matrix.py` in its Pinned-values cell while gating
  `scripts/redirect_audit.py`.
- **A2 (one counter per row; bound path).** A row credits exactly one population counter; if two or
  more population filenames appear in its credited cells, it credits none. Conjunct 2 binds to the
  first backticked `.py` token in that row's **Entry command** cell; its basename must equal the
  counter filename and `git cat-file -e <rev>:<path>` must exit 0. This closes the one-dump-row
  exploit and the singular/plural ambiguity.
- **A3 (`own_row` bound).** `own_row=true` iff a row between the `### Round 74` heading and EOF names
  `c74_registry_gap.py` in its credited cells. A row anywhere else in the file does not count.
- **A4 (label honesty).** A new row's Kind cell starts `gate (live` only when its counter exits 0 at
  the measured revision under the row's entry command. Otherwise it starts `instrument (historical`
  (or `historical`) and names the pinned revision, the measured non-green state, or the successor.
- **A5 (placement).** Every `SKILL.md` addition lands after line 935 (the largest sidecar-pinned
  `SKILL.md` line), or the sidecar is re-pinned in the same commit. Measured: an insert at line 512
  makes the sweep exit 2 (`paths sidecar binding invalid: SKILL.md:512`); an EOF append leaves it at
  exit 1 with the same drift.
- **A6 (reproduction).** "Reproduce the control" means the named fields (population, each counter's
  `rows` and `file_exit`, `unregistered`, `met`) plus `own_row=false` at base, not byte-identical
  stdout: the control predates `own_row`. `file_exit` is the exit code of
  `git cat-file -e <rev>:<population path>`. The counter prints `own_row=<bool>` in its plain
  summary from this amendment on.
- **A7 (severity).** A missing or renamed population counter is `unevaluable` (exit 2, reported),
  never a kill. Only `unregistered>0`, a credited row whose entry-command path fails to resolve, or
  `own_row=false` are 1-conditions.

### C2 amendments

- **B1 (severity).** An unevaluable probe is exit 2 and is reported as could-not-evaluate, never as
  a failed claim. On this host the measured unevaluable count is 0, so the claim is evaluable.
- **B2 (vocabulary).** The banned restored-note vocabulary is the sweep's list plus
  `removed|deleted|purged|returned|reappeared|came back|recreated`. The counter and the repair tool
  both enforce the extended list; the sweep's own binding stays the sweep's list (it is a
  registered instrument, not this claim's counter). Measured hole this closes: a note saying
  "removed … reappeared" passes the sweep and would have passed the unamended counter.
- **B3 (base bytes).** The counter pins the base revision `ced2878a` and compares each flipped
  entry's `history` against the base entry's `{date, kind, note}` for the same `file:line:token`.
  A self-consistent history that differs from the base bytes is a finding.
- **B4 (L0 wording).** Conjunct 4 passes on zero drift; only a new drift class, exit 2, or an
  `Error:` line fails. The open L0 `kake | round-69` case is not a dependency (the critic measured
  all three plausible rulings as passing).
- **B5 (field names).** The predicate's `absent_notes_resolving`, `restored_notes_absent` and
  `unevaluable` are the counter's `absent_present`, `restored_absent` and
  `absent_unevaluable + restored_unevaluable`. The base receipt's names are the control's; the
  counter's summary is authoritative and carries `annotation_findings=<n>`.

### Harm battery corrections (terms only)

- Census command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin kake` (the script lives at the fleet root; `bash scripts/...` from
  the lane exits 127).
- Flags: `c70_pointer_audit.py --root . --revision <rev> [--base <rev>]`;
  `c72_tmp_v2.py --lane . --revision <rev>`; `c73_wave_pointers.py --root . --revision <rev>`;
  `c73_tmp_v3.py --lane . --revision <rev>`.
- c66 baseline pinned: `members=28 evaluated=28 mismatches=3 structural=0 agreement=25
  scores_held=3/3 met=True` at base; the tip must not regress it.
- `/tmp` clause scoped: the literal is checked in the three new/edited instrument files
  (`scripts/sidecar_reobserve.py`, `.ufo/waves/round-74/c74_registry_gap.py`,
  `.ufo/waves/round-74/c74_sidecar_reobserve.py`) and in `SKILL.md` via `c73_tmp_v3.py`; the
  contract itself is excluded (it quotes the guard).
