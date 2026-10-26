# ExecC1Dryrun

Dry run of the final C1 landing in a scratch clone of lane revision `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (read at
`git show 4b8c730:...`; the lane working tree was not touched). Artifacts attacked: `.ufo/waves/round-57/c57_receipt_pins.py`
(v2), `c57_idresolver_gate.py` (v2, `--fleet`), `c57_quote_truth.py` (v2), `measured.json`, `SCORECARD.md`,
`controls/after-c{1,2,3}-*.txt`. Everything below is **confirmed by running** in `/tmp/tmp.0ku5WnJeTm` (clone of the lane,
identity flags inside the clone only); nothing is `git show`-inferred unless marked. Script:
`.ufo/waves/round-57/w2/ExecC1Dryrun.files/landing.sh` (`bash -n` clean; run end-to-end exit 0).

## SEQUENCE:

Copy-pasteable; this is exactly what `landing.sh` executes (LANE/FLEET/BUILD are variables in the script).

```bash
D=$(mktemp -d); git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin "$D"
git -C "$D" checkout -q 4b8c73050470ada9e6583f3b12d659d1bed6a17f
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
G=(git -C "$D" -c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false)
W=.ufo/waves/round-57
# (1) stand-in content revision X
"${G[@]}" commit -q --allow-empty -m "stand-in content revision X"; X=$(git -C "$D" rev-parse HEAD)
# (2) measure at X (both counters AT X, not at T0)
python3 -B "$D/$W/c57_idresolver_gate.py" --root "$D" --revision "$X" --fleet /home/vgpnk/Projects/shokunin > "$D/.c2"; C2=$?
python3 -B "$D/$W/c57_quote_truth.py"    --root "$D" --revision "$X" > "$D/.c3"; C3=$?
{ cat "$D/.c2"; echo "EXIT=$C2"; } > "$D/$W/controls/after-c2-idresolver.txt"
{ cat "$D/.c3"; echo "EXIT=$C3"; } > "$D/$W/controls/after-c3-quote-truth.txt"
printf '{"revision": "%s"}\n' "$X" > "$D/$W/measured.json"
printf 'revision: %s\npending: replaced at the tip\nEXIT=0\n' "$X" > "$D/$W/controls/after-c1-receipt-pins.txt"
printf '\n## Round 57 — declared and measured claims\n\nMeasured revision: %s\n' "$X" >> "$D/SCORECARD.md"
"${G[@]}" add -A; "${G[@]}" commit -q -m "round-57: measured revision X, c2/c3 receipts, C1 placeholder"; T0=$(git -C "$D" rev-parse HEAD)
# (3) the C1 receipt: run at T0 (documents met=False, see FORMAT NOTES 1) then the counter's own re-derivation
python3 -B "$D/$W/c57_receipt_pins.py" --root "$D" --revision "$T0"      # prints met=False; not the body line
DERIVED=$(python3 -B - "$D" "$T0" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("c57_receipt_pins", sys.argv[1] + "/.ufo/waves/round-57/c57_receipt_pins.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
v = m.measure(sys.argv[1], sys.argv[2], check_bodies=False)
print(m.report_first_line(v)); sys.exit(0 if v["met"] else 1)
PY
)
{ printf '%s\n' "$DERIVED"; printf '  tip: %s\n' "$T0"; printf '  revision: %s\n' "$X"; echo "EXIT=0"; } \
  > "$D/$W/controls/after-c1-receipt-pins.txt"
"${G[@]}" add -A; "${G[@]}" commit -q -m "round-57: C1 receipt is the run at T0"; TIP=$(git -C "$D" rev-parse HEAD)
# (4) verify at the tip: exit 0 and the printed first line must equal the receipt's first line
python3 -B "$D/$W/c57_receipt_pins.py" --root "$D" --revision "$TIP"; echo "C1_EXIT=$?"
```

Three commits: `X` -> `T0` -> `TIP` (scratch: `e3b7dc2` -> `82d525a` -> `67b4fa9`). Re-run cost: 3–4 s total on the loaded host.

## OUTPUTS:

Measured at the scratch revisions named above (all `confirmed by running`).

- `C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)` — G2 `selftest: 33/33`, G4 `exit=1 summary=(99, 94, 5, 5, 0)`,
  G5 `exit=0 summary=(106, 106, 0, 0, 0); reference ids_cited=106`, `  revision: <X>`, exit 0.
- `C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`, C1..C8 PASS, `  revision: <X>`, `EXIT=0`, exit 0.
- C1 at T0 (exit 1):
  `C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=1 new_receipts=2 scorecard_pin=1 met=False  (met: …)`
  + `  population=59 relabels_in_history=6`
  + `  UNPINNED .ufo/waves/round-57/controls/after-c1-receipt-pins.txt: body carries no single \`tip: <40-hex>\` line or no EXIT=0`
- C1 re-derived at T0: same line with `new_unpinned=0 new_receipts=3 … met=True  (met: …)`.
- C1 at TIP (exit 0): the re-derived line byte-for-byte, `  population=59 relabels_in_history=6`, `  tip: <TIP>`; `C1_EXIT=0`.
- Receipt shapes as committed at TIP:
  - `after-c1-receipt-pins.txt` = 4 lines: report line / `  tip: <T0>` / `  revision: <X>` / `EXIT=0`.
  - `after-c2-idresolver.txt` = gate stdout verbatim (`  revision: <X>` second-to-last) + `EXIT=0` (gate prints no `EXIT=`).
  - `after-c3-quote-truth.txt` = counter stdout verbatim (already ends `EXIT=0`) + `EXIT=0` (two identical EXIT lines, the
    base-control convention).
  - `measured.json` = `{"revision": "<X>"}`; SCORECARD tail = `## Round 57 — declared and measured claims` + `Measured revision: <X>`.

## BREAKS:

Each break is a later commit on the scratch clone after the met TIP, then a run at the new tip (`confirmed by running`).

1. **`after-c2` revision line `X` -> build rev** (`1c51d86`): `new_relabelled=1 new_unpinned=1 new_receipts=2 met=False`, exit 1,
   note `UNPINNED …after-c2-idresolver.txt: revisions=['4b8c730…'] measured=e3b7dc2… introduced=82d525a…`.
2. **Re-run and overwrite `after-c1`** — three responses:
   - honest re-run at the *previous* tip (`5c2c69e`, `tip:` rebound to the old tip, pin unchanged): **`met=True`, exit 0** — this is
     not a relabel and the counter accepts it (it re-derives only at the recorded ancestor), so a later rewrite is undetectable
     as long as the pin and an ancestor that holds all three receipts are preserved;
   - overwrite with the **printed T0 line** (`048496f`): `new_unpinned=1 new_receipts=2 met=False`, exit 1, note
     `body line 'C1 receipt-pins …' != re-derived 'C1 receipt-pins …' (met=True)`;
   - two `tip:` lines (`1a0f073`): `body carries no single \`tip: <40-hex>\` line or no EXIT=0`, `new_unpinned=1 new_receipts=2`, exit 1.
3. **SCORECARD pin changed to the build rev** (`d475aa3`): every other counter stays 0, `scorecard_pin=0 met=False`, exit 1.
   (`after-c1`'s body line is not flagged: it is re-derived at T0, whose SCORECARD is untouched.)
- Extra probes: `after-c3` as if the counter had been run **at T0** (`4cac4eb`) -> `new_relabelled=1 new_unpinned=1 new_receipts=2`,
  exit 1 (identical shape to break 1); `after-c2` with its `EXIT=0` line removed (`4248c27`) -> `new_unpinned=1 new_receipts=2`, exit 1
  (note text quotes the correct first line yet still fails — the message does not say `EXIT=0` is what is missing).

## FORMAT NOTES:

1. **Step (3) cannot be done literally.** A fresh `after-c1` can never pass its own body check at the commit that introduces it:
   its `tip:` must be a *strict ancestor that already holds all three receipts*, so at T0 the counter prints
   `new_unpinned=1 new_receipts=2 met=False` (measured). The receipt's first line must be the counter's **re-derivation at T0 with the
   body check off** — the same expression the counter validates against (`measure(T0, check_bodies=False)` + `report_first_line`);
   equivalently, the first line the counter prints at the TIP once the body is in place. Copying either the T0 output or the finished
   tip output wholesale also works only if the `tip:` line inside is the ancestor (T0), never the writing commit.
2. **`tip:` belongs to the counter, `revision:` to the claim.** The counter's report ends with `  tip: <the revision it measured>`;
   the receipt needs exactly one `tip:` line naming T0 (strict ancestor of the writing commit, holding all three receipts) and exactly
   one `revision:` line naming X. Appending a second `tip:` line fails (measured), and the tip regex is line-anchored, so no prose may
   follow the 40-hex value.
3. **Claim receipts are run at X, not at T0.** `after-c2`/`after-c3` bodies must start with their counter's `met=True` report line
   (byte-identical, two spaces before `(`) and carry `EXIT=0`; their printed `  revision:` line is the revision passed with
   `--revision`, so it must be X (pinning them to T0 breaks the pin equality — measured, `4cac4eb`).
4. **`EXIT=` must be appended.** The C2 gate prints no `EXIT=`; C3 already prints `EXIT=0` and the convention (base controls)
   appends a second one. Without an appended line the C2 body fails even when its first line is correct (measured, `4248c27`).
5. **One receipt per claim, in `round-57/controls/`, named `after-c<1|2|3>-*.txt`.** Any second `after-*` file for a claim, or an
   `after-*` file anywhere else in that directory, is `new_unpinned` (`c1-selftest-v2.txt` check 24 confirmed by reading).
6. **The placeholder carries the pin.** At T0 the re-derivation counts receipts by pin only, so `after-c1`'s placeholder must already
   carry exactly one `revision: <X>` line (its body is irrelevant: the T0 run flags it, the re-derivation does not); a pin-less
   placeholder makes T0 bodies-off `new_receipts=2`, and the receipt's own first line then never matches.
7. **SCORECARD pin** is a labelled line `Measured revision: <40-hex>` (backticks optional) inside a `## Round 57` section, and every
   such line in that section must equal X; the section regex stops at the next `## Round <digits>`.
8. **`measured.json`** must be a JSON object with a string `revision` (a list is exit 2); X must descend from the counter's
   introduction (`b9a5d01`) and be a strict ancestor of T0.

Risks: the run was against `4b8c730`; the L1 must re-run `landing.sh` with `BUILD=<actual build tip>` — C2's G4/G5 read the live
siblings at `/home/vgpnk/Projects/shokunin` (they were unchanged and matched `sibling-snapshot.json` on 2026-10-25) and G5 reported
`ids_cited=106`, so a different build tree can move that number without invalidating the landing. No tools installed (python3/git
only; pacman untouched). No lane, jj or fleet state was written; the only lane writes are this report and `landing.sh`.

VERDICT: C1 lands met in 3 commits (X -> T0 -> TIP) once the C1 receipt's first line is the counter's bodies-off re-derivation at T0, not the T0 run's met=False line; all three named breaks are caught (exit 1), and an honest re-run/overwrite of `after-c1` is accepted (exit 0).
