# ExecCensus

Read revision: `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (lane tip; `git cat-file -t` = commit). Scratch clone
`/tmp/tmp.hT9zlqkbiJ/lane` (`git rev-parse --show-toplevel` = that path) checked out detached at that revision.
The lane working tree's `corpus/` is identical to the tip (`git diff --name-only 4b8c7305 -- corpus/` → 0 files), so the
fleet-run validator below read the tip registry; tip `corpus/SOURCES.md` sha256 `57c83362dbc6ba81dc45351f1bcdc33aecbb2b448a6343a95a1a585feccbe4ea`,
base `28fa0b23…` sha256 `010af7926a03788fa5f36371a0f9452ee3f3ee3c087977a455dc400bb3b5be81`.

## CENSUS:

- Command (confirmed by running):
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  → **exit 0**, 15 stdout lines, 0 stderr bytes.
- Codes: 14 × `W04` (duplicate URL across scopes) on S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117 S127 S416 S417,
  plus the terminal `kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`. No E-code, no W01–W03, no E12.
- Compared with `controls/census-before.txt`: `diff -u` → **no differences, exit 0** (byte-identical). Also byte-identical to
  `controls/census-after-build.txt` (`diff -q` → identical). Consequence: the append introduced no new validator code, but this
  control is *not* discriminative for the append (same 14 W04 before and after; only the `ok` path line is constant) — the
  discriminating pre/post evidence is the two-row diff under APPEND-ONLY plus C3's C8 mirror condition, not this file.
- Cross-check, `census` mode: `sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → exit 0,
  `kake rows 160`, `tier.A 137`, `tier.B 6`, `tier.C 17`, `status.mined 130`, `status.queued 8`, `status.rejected 22`,
  `FLEET invalid 0`, `FLEET missing 0`. Contract C3 after-state "registry 160 rows" is corroborated.

## MANUAL CENSUS:

Run from the scratch-clone root at `4b8c7305`, using verbatim the CORPUS.md block (frozen column-zero form):

| check | command result |
|---|---|
| rows | 160 (base 158, +2) |
| malformed (NF≠13) | 0 |
| tier histogram | `A=137 B=6 C=17` (base `A=135 B=6 C=17`) |
| status histogram | `mined=130 queued=8 rejected=22` (base `128/8/22`) |
| duplicate ids | none printed |
| enum violations (incl. community@A) | none printed |
| missing used-by paths (run from the clone root, so resolved against the tip tree) | none printed |

- Histograms sum to 160 on both axes; base sums to 158. Max id 420 → 422; S421/S422 are lines 167–168, inside `## Registry`
  (line 5) and before `## Paths` (line 170) — no row-shaped content outside the registry (validator E12 silent, agreeing).
- used-by targets exist and cite the right ids: `corpus/knowledge/baidu-dead-link-types.md` → S421,
  `corpus/knowledge/baidu-spider3-dead-link-model.md` → S422. Both rows `docs | A | mined | 2026-10-25 | 180d`.
- Not run: `sources-census.sh selftest` (not in assignment; the validator ran clean against the real registry).

## APPEND-ONLY DIFF:

- `git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:corpus/SOURCES.md` vs
  `git show 28fa0b23e699303725aba2727094531f5e44494d:corpus/SOURCES.md` (confirmed by running `diff -u` on the two blobs):
  **`2 insertions(+), 0 deletions(-)`**, one hunk `@@ -164,6 +164,8 @@`, exactly the S421 and S422 rows inserted after S420.
  No held row was rewritten in place at the tip, and `## Paths`, `## Search log`, `## Leads` are unchanged base→tip, so
  CORPUS rule 2's in-place clause (status/recheck/used-by) is not triggered and no old→new logging is owed.
- **Intermediate history matters** (confirmed by running `git log -p … -- corpus/SOURCES.md`): two commits touch the registry.
  `cddef5b` added the two rows *and* a 4-line `### Round 57 — Baidu dead-link pages` block in `## Search log`
  (`@@ -219,6 +221,10 @@`); `4b8c730` removed that block (`@@ -221,10 +221,6 @@`). Net = the two rows. The removal is disclosed at
  `corpus/lessons/round-57.md:72` ("the append-only rule of the registry (the C3 counter's mirror condition …) keeps this note
  out of `corpus/SOURCES.md` § Search log, so it lives here"); that sentence is absent at `cddef5b` and present at `4b8c730`
  (`git show cddef5b:corpus/lessons/round-57.md | grep -c` = 0), i.e. it landed in the same commit that removed the block. So
  "only two added lines" is true at the tip but **not of every intermediate commit** — a base..tip-only diff hides the add/remove.
  This is prose, not a registry row, so rule 2 is not violated; it is disclosed, not silent.
- `validate_append.sh` census line re-run **by hand** on a scratch mirror of the tip clone:
  `V=/tmp/tmp.hT9zlqkbiJ/mirror-validate`; `cp -r corpus "$V/corpus"`; the same five non-corpus used-by targets copied
  (`SCORECARD.md SKILL.md scripts/source_recheck.py .ufo/waves/round-41/c1_count.py .ufo/waves/round-41/oracle_crosscheck.py`);
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $V/corpus/SOURCES.md`
  → **exit 0**, 15 stdout lines (the same 14 × W04 + `file	ok	<V>/corpus/SOURCES.md`), stderr empty; argv recorded in
  `$V/census-argv.txt`. `--file` reports the path as `file`, not `kake`; the code set is unchanged from the fleet run.
  [INFERENCE] the script's own outputs (`$V/census-exit.txt` etc.) are not written into the lane because `validate_append.sh`
  writes under the lane's `assimilation/validate/`, which a seat must not mutate; the by-hand run keeps the argv/copy list identical.

## COUNTERS AT TIP:

Invocation (confirmed by running): `PYTHONHASHSEED=0 python3 -B .ufo/waves/round-57/<counter> --root /tmp/tmp.hT9zlqkbiJ/lane
--revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f` from inside the clone; outputs kept in `/tmp/tmp.hT9zlqkbiJ/<counter>.out`.

- `c57_quote_truth.py` → **exit 0**. First line:
  `C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`; C1_entries_exist … C8_mirror_bytes all PASS;
  `revision: 4b8c73050470ada9e6583f3b12d659d1bed6a17f`.
- `c57_idresolver_gate.py` → first run **without** `--fleet`: **exit 2**, first line
  `C2 id-resolver-gate unevaluable: Unevaluable: no sibling registries under the fleet or no sibling snapshot`
  (the default fleet is `os.path.dirname(--root)`, gate source line 361 — the mktemp parent of a clone). Re-run with
  `--fleet /home/vgpnk/Projects/shokunin` → **exit 0**, first line
  `C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)`; G1 PASS; G2 PASS (`selftest: 33/33`);
  G3 PASS (`fixture0: dirty exit=1 summary=(12, 3, 9, 6, 3); clean exit=0 summary=(3, 3, 0, 0, 0)` for both fixtures);
  G4 PASS (`exit=1 summary=(99, 94, 5, 5, 0)`); G5 PASS (`exit=0 summary=(106, 106, 0, 0, 0); reference ids_cited=106`);
  `revision: 4b8c7305…`. The 5/5 is the scoreable result; the exit-2 run is the documented scratch-clone behavior
  (contract § Pre-dispatch note), **not** "not met".
- `c57_receipt_pins.py` → **exit 1** (unmet, by design at this tip). First line:
  `C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False  (met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1)`;
  then `population=56 relabels_in_history=6` and `tip: 4b8c73050470ada9e6583f3b12d659d1bed6a17f`.
  Why each missing term is 0, checked by reading the tip tree:
  - `new_receipts=0`: no `controls/after-c{1,2,3}-*.txt` exists at the tip; the only six `after-*` files are rounds 54–56
    (`after-c1-s374`, `after-c2-ops-debt`, `after-c1-readme-index`, `after-c2-quote-truth`, `after-c1-selftally`,
    `after-c2-quote-truth`).
  - `scorecard_pin=0`: `SCORECARD.md` has no `## Round 57` section (last heading is `## Round 56 — declared and measured claims`,
    line 4321) and no `Measured revision: <40-hex>` line at all.
  So C1 cannot be met at `4b8c7305` (needs the three receipts and the SCORECARD pin); the four history terms are already 0,
  which is the half of the after-state that exists at this revision.

## Notes / risks

- C2 default-fleet trap: any clone-based run without `--fleet` records exit 2 *unevaluable*. A report must not read that as
  "not met"; the 5/5 above is the gate result with the real fleet named.
- `controls/census-before.txt` ≡ tip output byte-for-byte; it certifies exit 0 but cannot show the append. Pre/post
  discrimination for the registry append lives in the two-row diff and C3's C8 mirror condition.
- Net-only diffs hide the `cddef5b` → `4b8c730` search-log add/remove; it is disclosed at `corpus/lessons/round-57.md:72`
  and is prose, not a row rewrite.
- Not run (out of seat): the `validate_append.sh` script itself, any counter selftest, any build/lint/test.

Files changed: `.ufo/waves/round-57/w2/ExecCensus.md` (this report) only.

VERDICT: Census clean at `4b8c7305` (validator exit 0, 14 pre-existing W04, identical to before/after controls; 160 rows, 0 malformed/dup/enum/dangling, histograms sum 160); registry append-only net +2 rows with a disclosed intermediate search-log add/remove; C3 8/8 met, C2 5/5 met with `--fleet` (exit 2 unevaluable without it), C1 exit 1 unmet by design (0 receipts, no SCORECARD pin; history terms all 0).
