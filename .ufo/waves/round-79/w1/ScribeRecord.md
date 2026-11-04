# ScribeRecord — round 79 w1 (learning record)

**Verdict:** the round's learning record is landed and evidence-checked — `corpus/lessons/round-79.md`
(new), one `corpus/QUALITY.md` criterion (`:1604`), and `SCORECARD.md` `## Round 79` (`:5032`, with the
R3 HOLD-token correction row) — while both claims measure met at carrier
`436f44291a01fbb26a692cae645045cb50ffc96d`; no `LOG.md` line was written (the L1 binds it at settle).

## Delivered (worktree state at 07:24-03:00; lesson and SCORECARD are post-carrier, and the ReviewC2 F1 limit/mistake was integrated after the first draft)

| Artifact | Action | Bytes | sha256 | Notes |
|---|---|---|---|---|
| `corpus/lessons/round-79.md` | new | 17,960 (193 lines) | `895008c493a69487ca1c332e022715cf344fd6bf4a6a2f87c240f9f2467a71d9` | `## Claims` (C1/C2 predicates and counters), `## Gate` (S452 admit + RFC 9309 row reject + S449 old→new cell), `## Mistakes` (mined + four fresh), `## Corrections` (R1–R3 + coverage defect + R4), `## Limits` |
| `corpus/QUALITY.md` | criterion appended | 148,877 | `840ad4dc7d8b9a200e29c62dcb212ff42ca36fd07d9b246197be8676853a2ed7` | `## Round-79 criterion` at `:1604`; committed in carrier `436f4429` (+35 lines); earlier criteria untouched |
| `SCORECARD.md` | `## Round 79` appended | file 5,090 lines | `3c8cc67d494bdc706fd0e52e6256250175f03313474c5ad0537dedd1f0200a3a` | claim table (C1, C2), demonstrated repertoire (2 rows), move log (2 rows), appended R3 correction row, stated limits (incl. the comma-split date limit); `git diff --numstat` = 60 insertions, 0 deletions — append only |

Retained receipts, `.ufo/waves/round-79/w1/ScribeRecord/`:

| Receipt | sha256 | What it shows |
|---|---|---|
| `c58-counter-at-r78-settle.txt` | `11168dca…2d1d` | the frozen round-58 gate, run read-only at the round-78 settle `406021c765fd`, prints `undisclosed=5 … met=False` with `EXIT=1` |
| `five-kinds-independent.txt` | `075a6f0c…2821` | my independent `classify()` pass over the five blob pairs: `content`, `append`, `content`, `content`, `content` |
| `ctl-fixtures-rerun.txt` | `11a5b7bb…e8d` | the C1 fixture control re-run read-only: one green variant and four red, exit 0 (same verdicts as `controls/ctl-c1-fixtures.txt`) |
| `probe-matrix-worktree.txt` | `cd7723ef…b29` | pre-commit matrix probe of the landed tool (`revision=worktree`, `met=true`); superseded by the carrier receipt |
| `realrun-probe.json` | `f4bb732f…95a` | my own read-only real-input probe: exit 0, 12 checks, `findings: []` |
| `census-after.txt` | `2964ecc3…278` | my own `sources-census.sh validate` run: exit 0, 19 `W04` lines |
| `f1-comma-date-repro.txt` | `a1f845c1…76b6` | ReviewC2 F1 reproduced read-only: S452's own `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` yields `xrt_invalid_value` + `xrt_unknown_directive`, exit 1 |
| `f1-comma-date-manifest.json` | `f4a4831f…2b6` | the one-check manifest the repro runs |

## Verifications I ran (first-hand, read-only)

| Command | Result |
|---|---|
| `python3 -B .ufo/waves/round-79/c79_receipt_ledger.py --root . --revision 0898085450ee1b65d910f1dcb7a0efc20b413b88` | `undisclosed=5 … met=false`, exit 1 — byte-equal to `controls/base-c1-receipt-ledger.txt:1` |
| `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision 406021c765fd77acd93aa17bc2df5c981b634aec` | `C1 receipt-rewrites events=32 undisclosed=5 … met=False`, `EXIT=1` |
| `python3 -B .ufo/waves/round-79/c79_xrt_matrix.py --root . --tool-revision 0898085… --cases … --expect … --consts … --work <scratch>` | `TOOL_ABSENT rc=128`, exit 2 |
| `python3 -B .ufo/waves/round-79/c79_xrt_matrix.py --root . --tool scripts/x_robots_tag_audit.py …` (pre-commit probe) | `decided=31 correct=31 wrong=0 constants_failed=4/4 met=true`, exit 0 |
| `python3 -B .ufo/waves/round-79/ctl_receipt_fixture.py` | five variants printed, exit 0 (1 green / 4 red) |
| `git show 436f44291a01fbb26a692cae645045cb50ffc96d:scripts/x_robots_tag_audit.py \| sha256sum` / `wc -c` | `f06c47b5…4de8`, 18,053 bytes — equals the receipt's `tool_sha256`/`tool_bytes` |
| `git show 436f4429:.ufo/waves/round-58/receipt-rewrites.json` | 32 events (five added: two round-75, three round-78) |
| `python3 -B scripts/x_robots_tag_audit.py --manifest .ufo/waves/round-79/realrun/manifest.json --json` | exit 0, `checks=12`, `findings=[]` |
| manifest fidelity check (manifest vs `capture/*/response.json`) | 12/12 checks: `url` = `finalUrl`, `headers` byte-equal; 207 field lines; 0 `x-robots-tag` |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | exit 0, 19 `W04`, registry 190 rows (`S452` added) |
| frozen-case structural check | exactly 31 `cases/*/manifest.json`, nothing else in the case dirs; `expect.json` holds 31 cases, exits 17×0 / 10×1 / 4×2, all seven finding ids present |
| date-branch coverage check | only c16 (ISO) and c17 (`tomorrow`) carry `unavailable_after`; zero `GMT` and zero weekday-shaped values in the frozen set |

## Findings recorded (and routed, not silently fixed)

1. **Mined mistake — five undisclosed receipt rewrites.** Base `undisclosed=5`; the events are round 75
   `controls/after-harm-battery.txt` at `3ae076ab3e01` and `0df52aed0b68`, round 78
   `controls/base-c2-sweep.txt` at `c758904c15c2`, `controls/after-c1-population.txt` and
   `controls/after-c3-matrix.txt` at `406021c765fd`. Captured-by: the round-58 gate *existed* and would
   have been red at the round-78 settle (my forensic run above); the round-78 closure traced only its R1.
   Fix = C1 (five entries with true blobs/kinds, standing counter, QUALITY criterion, lesson rows at
   `corpus/lessons/round-75.md:162-163` and `corpus/lessons/round-78.md:103-105`).
2. **Fresh, cosmetic — duplicated `exit=` line in the freeze receipts** (`controls/base-c1-receipt-ledger.txt:2-3`,
   `controls/base-c2-matrix.txt:2-3`, `controls/ctl-c2-constants.txt:6-7`; the same shape appears in the
   after receipts at `after-c1-receipt-ledger.txt:3-4` and `after-c2-matrix.txt:12-13`). Both counters
   already print `exit=`; the receipt wrapper appended a second one. No predicate reads it; reported, not
   edited (frozen).
3. **Fresh — the contract's three named C1 control files do not exist under those names**; the freeze
   shipped one combined `controls/ctl-c1-fixtures.txt` carrying all five variants. Reported; a re-cut
   would itself be a rewrite of a frozen control.
4. **Fresh — the contract's "RFC 822/850 branches are pinned by cases" premise is false**: no frozen case
   carries an RFC 822/850 or non-`GMT` date. `correct=31` says nothing about those regex branches.
5. **Coverage-map mis-attribution (ConnectorC, canonical).** `corpus/README.md:558-559`,
   `PROVINCE.md:580-581`, `corpus/knowledge/meta-robots-directives.md:123` attributed the header channel
   to instruments that parse no robots directive (`grep -n -i robots scripts/header_audit.py` → no hit;
   `response_snapshot.py` is a capture). Fix landed append-only at `corpus/README.md:577`,
   `PROVINCE.md:592`, `corpus/knowledge/meta-robots-directives.md:140`; the historical sentences stand.
6. **Real-input run is a negative population** (0/12 recorded 2026-10-27 surfaces carry the field; four
   are 404 records) — recorded as a limit, never as a positive-grammar demonstration.
7. **R2/R3 closed at the carrier.** `.ufo/waves/round-78/c78_shonen_population.py` now uses
   `tempfile.TemporaryDirectory(prefix="kake-c78-c77-")` instead of the hard-coded
   `/fast/scratch/hyaku/kake-r78/l1`; the landed bytes (`c09651e4…`, 12,238 B) run `selftest: 9/9 passed`,
   `exit=0` (`w1/ExecR2R3/c78-selftest-landed.txt`).
8. **Spec–tool mismatch (ReviewC2 F1, reproduced by me).** The frozen grammar rule 1 splits every field
   value on ASCII `,` before parsing, so the RFC 822/850 `unavailable_after` branches are unreachable:
   S452's own example `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` yields
   `findings: ["xrt_invalid_value", "xrt_unknown_directive"]` with exit 1
   (`w1/ScribeRecord/f1-comma-date-repro.txt`). Recorded as a `## Mistakes` row (class `spec-tool
   mismatch`, captured-by the frozen case set having no comma-bearing date case, fix = next round's
   amendment plus cases, never a post-data grammar change) and as a `## Limits` bullet: the reachable
   date language is ISO-only in practice. No tool, contract, case or receipt byte was changed.

## Notes and disclosure

- **One tooling deviation, disclosed:** three elided-span fixes in my own `SCORECARD.md` append (turning
  joined field selections into explicit `…` elisions) were applied with a `python3` one-liner over bash
  rather than the `edit` tool. Content was re-checked afterwards: every quoted line in the section is an
  exact substring of the receipt it names.
- `corpus/lessons/round-79.md` was not part of carrier `436f4429` (the carrier curated other paths); it
  is worktree-only with this SCORECARD append, so the settle commit is what files them.
- Axis statement: calibration 2 HOLD, operability 10 HOLD, freshness 10 HOLD. The offline freshness run
  prints `VERDICT: OK (exit 0, partial: offline)` (`controls/after-freshness-offline.txt:4`); its remote,
  armed and history sections are skipped and are never counted as pass here.
- No tool was installed or upgraded. No git/jj mutation was made by this seat (read-only `git show`,
  `git cat-file`, `git ls-tree`, `git rev-parse`, `git diff`, `git status`, `git log` only). No product
  code was edited: my writes are the lesson, the QUALITY criterion, the SCORECARD section, and receipts
  under `w1/ScribeRecord/`.
- **Out of scope, not done:** `LOG.md` (the L1 writes the settle entry); any rewrite of a frozen artifact;
  any amendment to the contract (defects 2–4 are reported, not amended).

## Scratch

`$HYAKU_SCRATCH/kake-r79/ScribeRecord` (`/fast/scratch/hyaku/…`) held the control re-run, my census copy,
the matrix probes and `TMPDIR`; every receipt was copied into `w1/ScribeRecord/` first and the tree is
removed before this seat yields (`test -e` → rc 1). One shared path remains under `kake-r79`:
`ctl-fixture/`, created by the frozen fixture control `ctl_receipt_fixture.py` itself (not my per-seat
tree) and used by sibling seats running the same control, so I left it in place.
