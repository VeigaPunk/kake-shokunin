# ScribeR3Correction — R3 ledger-population correction (round 47, wave 1)

Seat: scribe · target: verify that the LOG/SCORECARD R3 corrections identify the
adjudication-ledger population as **20 data rows** and **explicitly split 12 LOG.md +
8 SCORECARD.md**, and flag any remaining unqualified "12 rows" statement in the touched
round-47 material. Read-only against the lane; all mutation ran in a disposable clone.

Claim under test: **C2 / R3 limb only** — "ledger population misstated as '12 rows'"
(`corpus/lessons/round-46-verifier-spotcheck.md:69`).

## Verdict (short)

- **Population numbers are correct and independently re-derived**: the committed ledger
  holds **20 data rows = 12 naming `LOG.md` + 8 naming `SCORECARD.md`**, at the frozen base
  and at the round-47 tip.
- **Both prose corrections state the total and the split explicitly** (LOG.md:1793–1796,
  SCORECARD.md:3962–3965) and the r46 table bytes are provably untouched (append-only).
- **Two unqualified "12 rows" sentences survive, by design**: `LOG.md:1780` and
  `SCORECARD.md:3912`. Both are r46-authored, byte-retained, and each is corrected by an
  appended `[r47-correction R3]` block in the same file. No r47-authored unqualified
  "12 rows" exists.
- **Instrument deficit (fresh falsifier)**: the R3 limb of the C2 counter is a single
  substring test on `LOG.md` only (`c47_routed_count.py:134`). It does **not** enforce the
  12/8 split and does **not** read `SCORECARD.md`. Both weakenings were *executed* and both
  survive at `C2_MET` (mutants A and B below). The frozen predicate text itself does require
  the split (`c47_routed_count.py:13–14`, `SCORECARD.md:3947–3948`) — the instrument is
  weaker than its own predicate.

## Population measurement (independent recount)

Ledger: `corpus/quality/citation-adjudications.md`.

```
$ grep -c '^|' corpus/quality/citation-adjudications.md
22                      # = 1 header + 1 separator + 20 data rows
$ awk -F'|' 'NR>9 && /^\|/ {f=$3; gsub(/ /,"",f); c[f]++} END {for (k in c) print k, c[k]}' \
    corpus/quality/citation-adjudications.md | sort
LOG.md 12
SCORECARD.md 8
```

Same split measured on the frozen base blob (`git show cd42e3c3:…`): `LOG.md 12`,
`SCORECARD.md 8`, `^|`-lines = 22. So the population did not change between r46 and r47;
only the prose was wrong.

Corroboration, no duplicate rows: the 20 rows are 20 **distinct** `(token,file)` pairs
(`uniq -d` on the pair list prints nothing) over 18 distinct tokens; the r46 residual
report reached the same number independently (`.ufo/waves/round-46/residual/ReviewReceiptIdentity.md:42`:
"20 distinct `(token,file)` pairs / 30 occurrences … 8 `SCORECARD.md` + 12 `LOG.md`").

Adversarial unit check: the file has 27 lines containing `|` but only 22 starting with `|`;
the extra 5 are `- Row \`token\` | FILE` bullets in the R4 correction block. A counter that
split on `|` anywhere would read 25 "rows". The "20 data rows" claim uses the correct unit
(table rows), and the correction block does not inflate it.

## Append-only proof (the correction did not edit the table)

```
$ git diff --numstat cd42e3c3 714e7074 -- corpus/quality/citation-adjudications.md
25      0       corpus/quality/citation-adjudications.md     # 25 insertions, 0 deletions
$ git show cd42e3c3:… | sha256sum
432a36a2f9a6a20e6083ea223b63aa3c337e1fee4a9a938a08f8f61e57269394     (3444 bytes)
$ head -c 3444 <tip blob> | sha256sum
432a36a2f9a6a20e6083ea223b63aa3c337e1fee4a9a938a08f8f61e57269394     # byte prefix identical
$ git diff --numstat 714e7074 766f461 -- corpus/quality/citation-adjudications.md
(empty — ledger unchanged from the declared after-commit to HEAD)
```

Tip blob sha256 `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669`, 5043 bytes,
54 lines. Conclusion: the R4 correction block is a pure EOF append; the 20 table rows are
byte-identical to r46. The "append-only" wording in both corrections is observed, not merely
asserted.

## Where the corrections land

| Location | Text (verbatim, wrapped) | Section context |
|---|---|---|
| `LOG.md:1793–1796` | "[r47-correction R3] The adjudication ledger's population is **20 data rows** (12 naming LOG.md + 8 naming SCORECARD.md), not the \"12 rows\" written in this entry and the round-46 report; … Same correction appended to SCORECARD.md's" | inside `## Round 46` (1757–1816), 13 lines after the misstatement at 1780 |
| `SCORECARD.md:3962–3965` | "[r47-correction R3] The round-46 section's \"adjudication ledger … (12 rows)\" above is misstated: the ledger holds 20 data rows (12 naming LOG.md + 8 SCORECARD.md); corrected append-only here and in LOG.md." | inside `## Round 47 — declared claims` (3919+), **50 lines after** the misstatement at 3912 and across the section boundary (r46 section ends 3918) |
| `SCORECARD.md:3947–3948` (frozen C2 predicate) | "an R3 correction line naming the 20 data rows (12 LOG.md + 8 SCORECARD.md) in LOG.md" | declared-claims section |
| `c47_routed_count.py:13–14` (frozen predicate docstring) | same sentence | counter |
| `corpus/lessons/round-47.md:7–8,14` | ledger "as \"12 rows\"; the ledger holds **20 data rows** (12 naming LOG.md + 8 naming SCORECARD.md)" | lesson |

Both correction blocks name the total **and** the split explicitly — the target's
"explicitly split" requirement is met in prose at every one of these sites.

## Residual "12 rows" census at HEAD (`766f461`)

Full census over the touched set (`SKILL.md`, `SCORECARD.md`, `LOG.md`,
`corpus/{SOURCES,QUALITY,README}.md`, `corpus/lessons/round-47.md`,
`corpus/knowledge/commit-citation-hygiene.md`, `.ufo/waves/round-47/`). Six occurrences:

| Site | Kind | Qualified? |
|---|---|---|
| `LOG.md:1780` | r46 assertion: "`corpus/quality/citation-adjudications.md` (12 rows, each target re-verified" | **No on the line**; corrected at 1793–1796 ("not the \"12 rows\" written in this entry") |
| `LOG.md:1794` | correction quoting the defect | Yes |
| `SCORECARD.md:3912` | r46 assertion: "(12 rows, every target re-verified non-resolving in the lane repo at round 46)" | **No on the line**; corrected at 3962–3965 ("above is misstated") |
| `SCORECARD.md:3942` | defect quotation ("misstated as '12 rows'") | Yes |
| `SCORECARD.md:3962` | correction quoting the misstated text | Yes |
| `corpus/lessons/round-47.md:7` | quotation + corrected total | Yes |

**Flag (low severity, by design):** exactly two lines still assert "12 rows" as fact with
no qualifier on the line itself — `LOG.md:1780` and `SCORECARD.md:3912`. Append-only
discipline forbids rewriting them, and both are named by the corrections, so this is the
expected residue rather than a new defect. The weaker of the two is **`SCORECARD.md:3912`**:
its correction sits 50 lines later and past a `##` heading, so a reader who stops at the end
of `## Round 46 — measured verdicts` (line 3918) never sees the correction. `LOG.md` keeps
the correction inside the same section (13 lines later).

No other lane file carries a stale row-count for this ledger (whole-lane `grep -rn "12 rows"`
returns only the above plus unrelated historical artifacts under `.ufo/waves/round-2x/`,
`round-35/`, `round-45/`, `round-46/residual/` — none of them the r47 touched set).

## Instrument check — the split is not load-bearing (executed)

Detector: `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <rev>`.
Read-only (`git show` / `git ls-tree` only); reads `LOG.md`, the ledger and the receipt dir —
**never `SCORECARD.md`** (`:121–122`).

R3 leg, `.ufo/waves/round-47/c47_routed_count.py:134`:

```python
r3_fixed = any("R3" in line and "20 data rows" in line for line in log_lines)
```

Pristine runs (lane checkout, read-only):

| revision | output | exit |
|---|---|---|
| `714e7074…` (declared after) | `outstanding=0/4 C2_MET` | 0 |
| `766f461` (HEAD) | `outstanding=0/4 C2_MET` | 0 |
| `cd42e3c3…` (frozen base) | `outstanding=4/4 C2_NOT_MET` | 1 |

Mutants, in `/fast/scratch/hyaku/kake-r47/ScribeR3Correction/sandbox` (local clone, no push
performed; `origin` still points at the lane but nothing was pushed):

| # | Mutation (relative to `714e707` committed bytes) | Commit | Counter | Verdict |
|---|---|---|---|---|
| A | replaced "(12 naming LOG.md + 8 naming SCORECARD.md)" with "(populations as filed in the table)" — **total kept, split deleted** | `8c41a59` | `outstanding=0/4 C2_MET`, exit 0 | **survives** — split unenforced |
| B | deleted the whole `[r47-correction R3]` block from `SCORECARD.md` (`git show mutB:SCORECARD.md \| grep -c 'r47-correction R3'` → `0`) | `1d17e35` | `outstanding=0/4 C2_MET`, exit 0 | **survives** — SCORECARD limb unenforced |
| C (control) | "**20 data rows**" → "**19 data rows**", split kept | `ab83e6a` | `outstanding=1/4 C2_NOT_MET`, exit 1 | killed — the total *is* enforced |

Reading: R3's machine check is satisfied by any single `LOG.md` line containing `R3` and
`20 data rows`. Deleting the R3 line entirely is caught (sibling `MutationC2R3` killed that
with mutant `f6ae3499…`), but *weakening* it is not: a round that got the total right and the
split wrong — or that dropped the SCORECARD copy the C2 predicate promises — would still
record `C2_MET`. Mutant A is precisely the defect R3 describes (population unit split), so
the instrument cannot independently decide the defect it is wired to.

Sibling `MutationC2R3` listed both of these as "adversarial notes (static, not exercised)" and
did not run them. They are executed here; the two reports agree on the detector shape and on
`SCORECARD.md` being unread, and do not conflict on any measured value.

Consistency cross-checks (read-only, no reruns for decoration): `verification/c2-after-714e707.json`
records `{"fixed":{"R3":true,…},"outstanding":0,"verdict":"C2_MET"}` at
`714e7074110469a9ed2a3594677197baa0890905`; `LOG.md:1793` and `SCORECARD.md:3962` are present
at HEAD (`git show 766f461:LOG.md | grep -n 'r47-correction R3'` → `1793`;
`git show 766f461:SCORECARD.md | …` → `3962`), so the correction survives the later
`766f461` spot-check commit.

## Touched surfaces

- Wrote: `.ufo/waves/round-47/w1/ScribeR3Correction.md` (this report) only.
- Scratch: `/fast/scratch/hyaku/kake-r47/ScribeR3Correction/` (sandbox clone + `/tmp` blobs).
- Lane production files, `.jj`, index/refs, `.ufo/state/`, `.ufo/watchdog.log`: untouched;
  no mutating `git`/`jj` command ran in the lane. Pre-existing lane dirt observed and not
  mine: `M .ufo/waves/round-47/w1/swarm-registry.json`, untracked `.ufo/waves/round-46/residual/`
  and sibling `w1/*.md` reports.
- Tool installs: none needed (python3, git, awk, grep already present); nothing recorded.

## Out of scope / not verified

- **R6 limb** of C2 (withdrawal + rerun receipt), **R4** reason fidelity, **R5** hash
  ancestry, **C1** registry/receipt predicates — other seats.
- The r46 residual report says the misstatement also exists in **fleet report lines 13 and 40**
  (`.ufo/waves/round-46/residual/ReviewReceiptIdentity.md:42`). Not inspected: fleet-root files
  are outside this lane's read/write bounds, and no lane correction can reach them. The LOG
  correction's own phrase "the round-46 report" therefore points at a document this lane cannot
  repair — if that fleet-side report is still current, R3 is closed only for the lane.
- Residual request to file the ledger sha256 in the receipt
  (`ReviewReceiptIdentity.md:100`) is unimplemented as of HEAD; no ledger sha256 appears in
  `verification/c2-after-714e707.json`. Reported, not adjudicated here.
- No claim that this wave was dispatched: the correction was verified against committed
  bytes only.

## Reproduce

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
grep -c '^|' corpus/quality/citation-adjudications.md                     # 22
awk -F'|' 'NR>9 && /^\|/ {f=$3; gsub(/ /,"",f); c[f]++} END {for (k in c) print k, c[k]}' \
  corpus/quality/citation-adjudications.md | sort                         # LOG.md 12 / SCORECARD.md 8
git diff --numstat cd42e3c3 714e7074 -- corpus/quality/citation-adjudications.md  # 25  0
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision 714e7074110469a9ed2a3594677197baa0890905
python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision cd42e3c310ba442e89dde638ba6401adaefaf3e8
grep -nE "(^|[^0-9])12 rows|12-row" LOG.md SCORECARD.md SKILL.md corpus/*.md corpus/lessons/round-47.md \
  corpus/knowledge/commit-citation-hygiene.md
# mutants: sandbox at /fast/scratch/hyaku/kake-r47/ScribeR3Correction/sandbox, revisions 8c41a59 / 1d17e35 / ab83e6a
```
