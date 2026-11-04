# ScoutRecon — round 82 wave w1

Read-only recon at base `419866015b1f58e01f061cde9a77d490653d3c76` against `.ufo/waves/round-82/contract.md`. No production file written, no socket opened, no fleet-repo write, no VCS mutation. Lane files were read through `git show`/`cat-file`/`rev-parse`; the counters and probes ran in `/fast/scratch/hyaku/kake-r82/ScoutRecon` (deleted before yielding; receipts under `.ufo/waves/round-82/w1/ScoutRecon/`).

## Commands run (absolute paths shortened to `<lane>` = `/home/vgpnk/Projects/shokunin/kake-shokunin`, `<fleet>` = `/home/vgpnk/Projects/shokunin`)

| Command | Exit |
|---|---|
| `git -C <lane> show 41986601:corpus/SOURCES.md \| grep -n '^| S433 '` | 0 |
| `git -C <lane> show 41986601:.ufo/waves/round-81/controls/after-c1-final.txt` | 0 |
| `git -C <lane> show 41986601:.ufo/waves/round-81/seat-failures.json` | 0 |
| `git -C <lane> show 41986601:.ufo/waves/round-81/controls/c81-selftest-c2.txt \| grep -n 'selftest:'` (→ line 24) | 0 |
| `git -C <lane> cat-file -e 41986601:<each of the two after-c81 paths>` (both absent) | 1 |
| `git -C <lane> cat-file -e 41986601:.ufo/waves/round-81/controls/after-c1-final.txt` | 0 |
| `git -C <lane> ls-tree --name-only 41986601:.ufo/waves/round-81/controls/` (16 receipts) | 0 |
| `git -C <lane> ls-tree -r --name-only 41986601:.ufo/waves/round-82/` (no output: tree absent at base) | 0 |
| `git -C <lane> show 41986601:corpus/lessons/round-80.md \| grep -n 'r82-correction\|SOURCES.md:20[01]'` (only line 51) | 0 |
| `git -C <lane> show 41986601:corpus/QUALITY.md \| wc -l` (1684) and `grep -c '22/22'` (0) | 0 / 1 |
| `git -C <fleet> cat-file -e 7678247a^{commit}` and `7678247a^^{commit}` | 0 / 0 |
| `git -C <fleet> rev-parse 7678247a:.ufo/reports/round-81/kake.md 7678247a^:.ufo/reports/round-81/kake.md` (→ `f39b6df2…`, `07b1238c…`, differ) | 0 |
| `python3 -B .ufo/waves/round-82/c82_defect_queue.py --root <lane> --revision 41986601… --work <scratch>/base` | **1** |
| same counter over a base-export fixture plus prose-only rows (`prose-probe`) | 1 |
| same counter over a base-export fixture with three plausible mis-phrasings (`hazard-probe`) | 1 |
| `python3 -B … --root <lane>` (worktree, no `--revision`) at 12:55Z and 12:59Z | 1 / 1 |
| `git -C <lane> status --porcelain` (read-only) | 0 |

## 1. The filed queue, restated (what the outside verifier measured → what it asked for)

- **D1** — measured: the `S433` row in `corpus/SOURCES.md` is byte-identical to base (`recheck` `180d`, `used-by` only `corpus/knowledge/response-header-expectations.md`) although the round-81 report line 126 and the SCORECARD block state `180d → 2027-05-03` and the `used-by` addition as landed. Asked: apply the permitted in-place cells (`status`/`recheck`/`used-by`, CORPUS.md §SOURCES rule 2, logged old→new) or withdraw the claim by append.
- **D2** — measured: the before→after rows name `2b46f5c4…` as the measured commit, while `after-c1-final.txt`/`after-c2-final.txt` record `revision=498a0969…`; `2b46f5c4` only adds the receipts. Asked: cite `498a0969` (blob-stable to the tip) or re-run both counters at the tip and commit their receipts.
- **D3** — measured: `7678247a` edits the filed fleet report in place (lane-tip line, wave bullet, landed-changes row, claim row) instead of appending an erratum naming the superseded text. Asked: record the superseded lines in the next report's erratum.
- **D4** — measured: report and lesson say a "3,771-byte" progress log; `seat-failures.json` records `output_bytes: 3801` and the committed output encodes to 3,801 bytes. Asked: re-derive the number from the record and correct by append.
- **D5** — measured: `corpus/lessons/round-81.md` §Settlement names `controls/after-c81-defect-queue.txt` and `controls/after-c81-capture-audit.txt`, which do not exist; the committed receipts are `after-c1.txt`/`after-c1-final.txt` and `after-c2-carrier.txt`/`after-c2-final.txt`. Asked: append the correction.
- **D6** — measured: the QUALITY round-81 criterion cites `controls/c81-selftest-c2.txt` as `18/18` while the receipt prints `selftest: 22/22 passed`; the lesson §Claims carries `18/18` too (partly self-corrected later). Asked: append a superseding criterion row naming the corrected tally.
- **D7** — measured: the report asserts a green standing ledger (`C1v2 revision=5ae1f32b… events=40 … met=true`, exit 0) but no such receipt exists at that revision or at the tip. Asked: commit the gate receipt at the measured revision.
- **D8** — measured: R80-1 asked for the pointer in `.ufo/reports/round-80/kake.md:158` and `corpus/lessons/round-80.md:51` to be corrected by erratum/append; both still read `corpus/SOURCES.md:201` (S453 is on line 200). Asked: append one, or state why not.

## 2. Re-derivation at the base revision

| Item | Base fact I re-derived | Byte the frozen counter reads | Non-lesson conjunct at base |
|---|---|---|---|
| D1 | `S433` at `corpus/SOURCES.md:179`, 11 cells: cell 10 (`recheck`) = `180d`, cell 11 (`used-by`) = `corpus/knowledge/response-header-expectations.md` | `registry_row("S433")` cells 9/10 must be `2027-05-03` and contain `corpus/lessons/round-81.md`; plus a lesson line tagged `D1` carrying `180d` + `2027-05-03` | **open** — two cells must change |
| D2 | `after-c1-final.txt` line 1 is `$ … --revision 498a0969499f70830b7c992eb36ea364672f1a1b …`; the `C1v1` line repeats it | `HEX40.search(receipt)` → `498a0969…`; a lesson line tagged `D2` must carry that **full 40-hex** token, `2b46f5c4`, `superseded` | **satisfied** |
| D3 | fleet: `7678247a` and its parent resolve; `.ufo/reports/round-81/kake.md` = `f39b6df22e305aad…` vs `07b1238c4b8f1877…` — differ | a lesson line tagged `D3` carrying `erratum` and one 7–40-hex fleet token whose report blob differs from its parent's | **satisfied** (historical fleet fact; no round-82 write) |
| D4 | `seat-failures.json` → `seats.MutC.output_bytes = 3801`, `role: mutation-tester` | a lesson line tagged `D4` carrying `3801` + `superseded`, **and no other lesson line** containing `3771`/`3,771` without `superseded` | **satisfied** |
| D5 | both `after-c81-*` paths absent at base (`cat-file -e` = 1); `after-c1-final.txt` present (also `after-c1`, `after-c2-carrier`, `after-c2-final`, `after-c2-audit`) | a lesson line tagged `D5` naming both dead paths **and** `.ufo/waves/round-81/controls/after-c1-final.txt`; then a presence re-check | **satisfied** |
| D6 | `c81-selftest-c2.txt:24` = `selftest: 22/22 passed`; `QUALITY.md` (1684 lines) has **0** lines carrying `22/22` | one `QUALITY.md` line carrying `22/22`, `supersedes`, `round-81` | **satisfied** |
| D7 | `.ufo/waves/round-82/controls/after-c1-ledger-gate.txt` absent at base — the whole `round-82/` tree is created by freeze `082b7dd3` | receipt text must contain `undisclosed=0` and `met=true`; lesson line tagged `D7` naming `after-c1-ledger-gate.txt` | **open** — receipt must exist |
| D8 | `corpus/lessons/round-80.md:51` reads `corpus/SOURCES.md:201`; no `[r82-correction` line anywhere in the file at base | a round-80 line carrying `[r82-correction` + `corpus/SOURCES.md:200`; a lesson line tagged `D8` naming `.ufo/reports/round-80/kake.md` + `corpus/SOURCES.md:200` | **open** — append must land |

**The brief expected no item's state conjunct to be satisfied at base; that is wrong for five, and it is measurable.** A scratch copy of the `41986601` export plus five prose rows (lesson rows D1–D5 and one QUALITY line, no other byte touched) scores `closed=5 open=3`: **D2, D3, D4, D5 and D6 close; D1, D7 and D8 stay open** (`ScoutRecon/prose-probe.txt`, exit 1). So the three items that need a lane byte to change are exactly **D1** (two registry cells), **D7** (a new gate receipt) and **D8** (an append to `round-80.md`); the other five are pure transcription once their inputs exist — which they all already do at base.

**Row-writing hazards, measured on the same export** (`ScoutRecon/hazard-probe.txt`, exit 1):

- D2 written as `498a0969…` (truncated) → **D2 open**; the row needs the full 40-hex token.
- any second lesson line carrying `3,771` without `superseded` → **D4 open** even when the D4 row itself is perfect. A scribe quoting the round-81 sentence verbatim fails the item.
- D5 written with the round-81 lesson's own short form `controls/after-c81-defect-queue.txt` → **D5 open**; the counter needs `.ufo/waves/round-81/controls/…`.
- From code + row shape (not a separate fixture): D1 compares the `recheck` cell for exact string equality, so `2027-05-03 (365d)` fails; a `|` inside any `S433` cell makes `NF!=13`, the row unreadable, and the item reads `S433 row absent`; D6 needs the literal `supersedes`, not `superseded by`.

## 3. Where each fix lands, and who owns it

| Item | File · section · exact location | Owner | Note |
|---|---|---|---|
| D1 | `corpus/SOURCES.md` §Registry, `S433` row line 179, cells 10 (`recheck`) and 11 (`used-by`) | ExecRegistry | other 9 cells immutable; line must stay 179 |
| D2 | `corpus/lessons/round-82.md` §Corrections | ScribeLesson82 | full 40-hex token required |
| D3 | same, §Corrections | ScribeLesson82 | only the register half can land (flag b) |
| D4 | same, §Corrections | ScribeLesson82 | must keep `3,771` off every other line |
| D5 | same, §Corrections (state verified by the registry seat) | ScribeLesson82 | full relative paths only |
| D6 | `corpus/QUALITY.md`, one appended criterion row after the round-81 criterion (heading line 1662; file ends 1684) | ScribeRecord | append only |
| D7 | `.ufo/waves/round-82/controls/after-c1-ledger-gate.txt` (new) + round-82 §Corrections row | ExecRegistry + ScribeLesson82 | receipt already in worktree, 294 B, `met=true` |
| D8 | `corpus/lessons/round-80.md` appended `[r82-correction` section + round-82 §Corrections row | ScribeRecord (prose) + ScribeLesson82 (row) | see flag a |

Flags:

- **(a) D8's production half is not named by the seat that must write it.** `w1-spec.json` mentions `round-80.md` exactly once — inside ScribeLesson82's item ("the record scribe appends the `[r82-correction` row"). ScribeRecord's own six steps name only `corpus/QUALITY.md` and its four drafts, and step 6 forbids `SCORECARD.md`/`LOG.md`/`PROVINCE.md`/`corpus/README.md`; `round-80.md` is never named. The append is already in the worktree (`M corpus/lessons/round-80.md`, new section at end), so this is an ownership-wording defect, not an unfilled gap. Reported, not repaired.
- **(b) Two asks cannot land inside this round's write scope.** D8's fleet-report erratum (`.ufo/reports/round-80/kake.md:158`) and D3's substantive erratum (the four superseded statements of `.ufo/reports/round-81/kake.md`, which must ride `.ufo/reports/round-82/kake.md`) are fleet files; the lane's `.ufo/reports/` holds only `round-20/kake.md`. The counter scores the lane register only, so D8's "append one, or state why not" closes via its "state why not" half, which is the L1's at integration.
- **(c) `corpus/SOURCES.md` has two writers in one wave**: ExecRegistry (S433 cells, line 179) and ScribeKnowledge (S455 row inserted immediately after S454, plus its `used-by`). Different regions, one file, last writer wins — sequence them or give one seat the pen. The insert-below-S454 choice is the one that preserves line 200 = S453 (D8's pointer) and line 179 = S433; an insert above line 179 would silently falsify D8's claim while leaving its literal string true.
- **(d) Nothing is scoreable until the L1 commits.** `--revision` mode reads `git archive <rev>` only, so seat edits are invisible to the counter until integration; the measured revision D2 demands is exactly that discipline.
- **(e) D6 has no lesson row** — the counter reads `QUALITY.md` directly. ScribeRecord's row and ScribeLesson82's §Corrections are independent; neither can close the other's item.

## 4. Planning data-walk (dependency order)

| # | Step | Writes | Proving artifact | Depends on |
|---|---|---|---|---|
| 1 | freeze | `contract.md`, both counters, `population/`, five controls — committed at `082b7dd3`; no seat writes | `controls/base-c82-defect-queue.txt` (`open=8`, exit 1 — reproduced byte-identically today), `ctl-c82-junk-queue.txt` (`open=8`), `c82-selftest-c1.txt` (`11/11`), `base-c82-capture-delta.txt`, `ctl-c82-identical-capture.txt`, `c82-selftest-c2.txt` (`9/9`) | — |
| 2 | capture B | `.ufo/waves/round-82/capture/{ds4cc-primary,ds4cc-robots,ds4cc-sitemap}/{response.json,body.bin}` + `manifest.json` (ExecCapture) | `scripts/response_snapshot.py` stdout; each receipt's `sha256`/`bytes` equal to `body.bin`; `truncated=false`; `fetchedAt ≥ 2026-11-04T12:42:00Z`; manifest ids/urls = the frozen three, in order | — |
| 3 | registry cells | `corpus/SOURCES.md` S433 cells (ExecRegistry) | row before/after, `grep -n` still 179, 11-cell awk, `scripts/sources-census.sh validate --root <fleet> kake` exit 0 | — |
| 4 | ledger receipt | `.ufo/waves/round-82/controls/after-c1-ledger-gate.txt` (ExecRegistry) | `C1v2 revision=082b7dd3… events=40 undisclosed=0 phantom=0 … met=true`, `exit=0` (present in worktree) | — |
| 5 | delta record + tampered control | `controls/after-c2-delta.txt` (tool stdout only), `controls/after-c2.txt` (counter at a named revision), `controls/ctl-c82-tampered-capture.txt` (ExecDelta) | two byte-identical tool runs (`sha256sum` + `cmp`); summary `surfaces=3 identical=k changed=m added=0 removed=0`; tampered tree `receipts_ok=0 met=false` | 2 |
| 6 | lesson rows | `corpus/lessons/round-82.md` §Corrections (ScribeLesson82) | `c82_defect_queue.py --revision <carrier>` prints `open=0 … met=true`, exit 0; the lesson alone pre-scores 5/8 until 3, 4, 5 land | 3, 4, 5 (+ round-80 append for D8) |
| 7 | QUALITY row | `corpus/QUALITY.md` (ScribeRecord) | D6 detail `criterion=yes receipt22=yes` (live worktree already reads `closed`) | — |
| 8 | attacks | `w1/{ReviewC1,ReviewC2,CriticClaims,MutC,ConnectorC}.md` + receipts; no production bytes | each report names the conjunct its fixture broke and the counter's exit; MutC survivors are routing findings | 5 for the C2 half; C1 half only on 1 |
| 9 | integration | L1 commits the carrier; writes `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `corpus/README.md` from `w1/ScribeRecord/*.md`, and `.ufo/reports/round-82/kake.md` in the fleet (carrying D3's and D8's errata) | the carrier commit + both counters re-run at that revision (`C1 open=0 met=true`; C2 `record_equal`/`determinism`/`selftest_ok`) + `git status --porcelain` empty | 2, 3, 4, 5, 6, 7, 8 |

Two ordering facts for the dispatch: steps 2, 3 and 4 are mutually independent and can run concurrently (5 is the only network-gated step); step 6 must not be written before 3/4/5, or its rows assert receipts that do not exist yet — and a scribe that guesses C2's `identical=?`/`changed=?` invents a finding.

## 5. Counter at the base revision (verbatim)

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-82/c82_defect_queue.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 419866015b1f58e01f061cde9a77d490653d3c76 --work /fast/scratch/hyaku/kake-r82/ScoutRecon/base
D1 open recheck='180d' used-by='corpus/knowledge/response-header-expectations.md' log=no
D2 open receipt revision=498a0969499f70830b7c992eb36ea364672f1a1b log=no
D3 open no D3 erratum line
D4 open no D4 line carrying 3801 and superseded
D5 open no D5 line naming both dead paths and the live receipt
D6 open criterion=no receipt22=yes
D7 open after-c1-ledger-gate.txt absent
D8 open round-80 correction=no log=no
C1v1 revision=419866015b1f58e01f061cde9a77d490653d3c76 items=8 open=8 closed=0 met=false
exit=1
```

`diff` of those eight item lines + summary against `controls/base-c82-defect-queue.txt` (dropping that file's `$` line): **identical, exit 0**. The frozen base control reproduces.

## Live snapshots (worktree; host clock is UTC−03:00; other seats writing)

- **12:55Z** (`worktree-snapshot-0955.txt`, mtime 09:55 local): `open=7 closed=1 met=false` — D6 closed (QUALITY row landed), D7 `receipt green=yes log=no`, D8 `round-80 correction=yes log=no`, D1 `recheck='180d' … log=no`, and `corpus/lessons/round-82.md` not yet present.
- **12:59Z** (`worktree-snapshot-1259Z.txt`): `open=1 closed=7 met=false`, exit 1 — **D2–D8 all closed; D1 is the only open item**, still `recheck='180d'` (the S433 cells are not yet edited). `corpus/lessons/round-82.md` §Corrections now carries rows for D1–D8 at lines 80–94, the appended QUALITY criterion is at `corpus/QUALITY.md:1695`, and `S455` sits at `corpus/SOURCES.md:202` (after S454 at 201), so `S433` stays at 179 and `S453` at 200 — the two line pointers D8's row and the S433 edit depend on.

Both are snapshots of in-flight writes, not verdicts; neither is a `--revision` measurement.

## Limits

- I re-derived the base revision from committed bytes and ran the C1 counter and two scratch probes. I did not run the C2 counter, either gate's selftest, or any fetch; gate receipts elsewhere are read, not re-executed — the one exception is the C1 base control, which reproduces byte-for-byte.
- The worktree moved while I read it: at 12:55Z only D6 was closed; at 12:59Z D2–D8 were closed and D1 was the sole open item. Both readings are snapshots of other seats' in-flight writes — the scored after-state must come from a `--revision` run at the carrier commit.
- Scratch `/fast/scratch/hyaku/kake-r82/ScoutRecon` removed before yielding; receipts copied into `.ufo/waves/round-82/w1/ScoutRecon/` (`counter-base.txt`, `prose-probe.txt`, `hazard-probe.txt`, `worktree-snapshot-0955.txt`, `worktree-snapshot-1259Z.txt`, and the 13 seat-item dumps `item-*.md`).

## Verdict

Recon complete, no production file written. C1's base state is `open=8 closed=0 met=false` (exit 1), identical to the frozen control. Five of eight items (D2–D6) close on prose alone over unchanged bytes; three (D1, D7, D8) need real lane bytes. D8's fleet-report erratum and D3's substantive erratum are outside every seat's write scope; `corpus/SOURCES.md` has two writers in this wave; D8's production half is assigned only in a sibling's item text. At 12:59Z the worktree scored `open=1 closed=7`, with **D1** — the two S433 cells — the only item still needing a lane byte.
