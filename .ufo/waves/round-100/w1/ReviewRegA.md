# Round 100 w1 — ReviewRegA (C1 review conjunct, seat A)

Seat: judge the 8 C1 units at repair commit `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` (= lane
`master` tip, verified `git rev-parse master`): the seven kept registry rows and the fenced history
block. Reporter only; no repairs made, no lane tree mutated, no git/jj mutation anywhere.

## Instrument verification (before attacking)

- `controls/instrument-sha256.txt` (frozen): all 21 listed digests recomputed in the worktree and
  matched, including `c100_registry.py` = `c25d981e…` and `c100_fresh304.py` = `e7dff63b…`; both
  counters also byte-identical at instruments commit `d7b73d16` (`git show … | sha256sum`).
- Worktree `SKILL.md` sha256 `397b6dec…` is byte-identical to `e84a1871:SKILL.md` — line citations
  below are valid for both.
- Counter semantics read from source (`.ufo/waves/round-100/c100_registry.py`): D1 duplicated =
  tool invoked by ≥2 registry rows outside fences; D2 probe_mismatch = verdict map not naming the
  exit code returned for the single argument `--zz-bogus-r100`; fenced blocks are excluded by
  `strip_blocks`. The declared counter limit (everycode) is covered by this review.

## Method

For each kept row: full source read of the tool (every return / exit path, parser behaviour), then
observed runs in scratch (no network needed for any run below):

| Observation | Command (lane cwd) | Observed |
|---|---|---|
| unknown-flag probes, all 7 tools | `python3 -B scripts/<t>.py --zz-bogus-r100 </dev/null` | cache_key rc=1; cache_key_conformance rc=2; live_snapshot rc=64; response_snapshot rc=64; robots_audit rc=64; source_snapshot rc=2; x_robots_tag_audit rc=64 — each named by its row's map |
| cache_key refusal paths | stdin empty / bad JSON / bad shapes | rc=1 `invalid_input: …` on stderr; success rc=0 `{"key": …}` on stdout |
| conformance end-to-end | `python3 -B scripts/cache_key_conformance.py --candidate scripts/cache_key.py --work <scratch> --seed 7` | rc=0, `clauses=6/6 hand=92/92 generated=120/120 sandbox=ok met=true`, advisory line unscored; scratch empty afterwards (finally-rmtree) |
| x_robots selftest | `python3 -B scripts/x_robots_tag_audit.py --selftest` | rc=0, stdout exactly `selftest: 33/33 passed` |
| robots_audit selftest | `python3 -B scripts/robots_audit_selftest.py` | rc=0, `204/204`, `verdict: clean` |
| source_snapshot recording fault | valid list (invalid item), `--manifest /proc/no-such-root/…` | rc=1 traceback (unhandled `mkdir` at `source_snapshot.py:281`) — NOT 2 |
| history verbatim | `cmp` fenced rows vs `git show 3989618d:SKILL.md` lines 494/1079/1104/1370/1505/1621/1624 | 7/7 IDENTICAL |

## Verdicts (8/8 agree — details in `w1/ReviewRegA/verdicts.tsv`)

| Unit | Verdict | Basis (see tsv for path:line) |
|---|---|---|
| cache_key.py | agree | map {0,1} exact; write scope stdin/stdout/stderr only; no selftest mode true |
| cache_key_conformance.py | agree | map {0,1,2} exact (2 = reference self-check / usage); scratch under `--work` only, observed met=true |
| live_snapshot.py | agree | 0/2/64 true, 1 unused; `--reaudit` offline; writes confined to `--out/<id>/` (validator manifest-mode writes nothing) |
| response_snapshot.py | agree | 0/2/64 true, 1 unused; O_EXCL never overwrites; receipts under `--out` exclusively |
| robots_audit.py | agree | constants 0/1/2/64 verbatim; read-only; selftest runner observed rc=0 204/204 |
| source_snapshot.py | agree | all cells true; two routed findings below (cause-set overbreadth on `2`; `receipts.json` omitted from write scope) |
| scripts/x_robots_tag_audit.py (round-80 grammar) | agree | 0/1/2/64 all realized; `selftest: 33/33 passed` observed; reads only |
| history-block | agree | 7/7 rows byte-identical to their labelled base lines; labels' tool + current-row Name all correct; set equals `controls/base-c1.txt` duplicated=7 |

## Routed findings (no repair made; verdicts not flipped)

1. **source_snapshot verdict map, cause overbreadth** (`SKILL.md:1729` map cell; code
   `scripts/source_snapshot.py:140-146, :217-256, :281, :298-301, :305`): the cell reads
   "`2` bad input or fetch-recording fault", but no fetch/recording fault can produce 2 —
   per-item faults are recorded as rc=0 receipts (record() catches URLError/HTTPException/OSError/
   ValueError → `ok:false`; build_check → `recorded=false`), and an environmental recording fault
   was observed exiting **1** with a traceback (unhandled `manifest_path.parent.mkdir`). All actual
   2-paths are input faults (unreadable/undecodable/non-list input, argparse usage — observed
   rc=2). The frozen D2/counter-limit review scope (never-returned *codes*) is satisfied — code 2
   is returned and named — and both round-99 reviewers agreed these exact cells (RegA "agree with
   note", RegB called the phrase truthful), so this is routed as a cause-level accuracy finding,
   not a verdict flip. Correction, if taken: "`2` bad input (file or usage)" and fold fetch faults
   into the 0-cell description ("receipted, not fatal").
2. **source_snapshot write scope omission** (`SKILL.md:1729` vs `scripts/source_snapshot.py:298-301`):
   the tool always also writes `receipts.json` next to the manifest; the cell names only "the
   manifest and body files it names". Location is still covered (same directory as the manifest;
   no write outside `--out-dir`/manifest dir + mkdir), matching the note both round-99 reviewers
   recorded when agreeing.
3. Convention note (no action): "1 not used" cells are judged against designed/returned paths per
   this table's established convention; unhandled-crash exit 1 exists for every Python tool
   including these, and both round-99 reviewers applied the same reading.

## Residual risk / verification gaps

- Network-dependent behaviours (live_snapshot/response_snapshot/source_snapshot real GETs) were
  verified by code read only; bounds forbade network. Their map cells verified here do not depend
  on transport outcomes (those are receipts/data by design).
- `--jobs`/`--python`/`--verbose` (cache_key_conformance) and `--validator` (live_snapshot) exist
  but are outside the entry-command cells; not judged as omissions since the entry form runs as
  written (verified for the canonical candidate).
- The C2 candidate (`scripts/freshen_304.py`) is ExecFresh's deliverable this wave; not in my 8
  units. Ordering-rule check (repair SKILL.md ≡ `pos` fixture bytes) is the L1's.

No tool installs/upgrades were needed or made (git, python3, coreutils only).

REVIEWREG-A agree=8 disagree=0 of 8
