# ScoutSpotSpan — round-64 C1 spot-span binding (scout, leaf)

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`. Base `1a48131577ba82c967650561be34e8dba909432a`. Read-only: only `git show`, `git grep`, `git rev-parse`, `git status`, `git clone --no-local` into scratch. No mutating git in the lane. Scratch `/fast/scratch/hyaku/kake-r64/ScoutSpotSpan/` (deleted before yield).

## Verdict

- The three asserted facts hold at T0, byte-exact.
- The counter's binding is one-sided. `c64_calibration.py` pins the span constant against the lesson Gate, but it never reads the spot file's verdict text and never sha-pins the spot file. An edit that rewords the S432 verdict out from under the span keeps `met=true` (attack A1 below). The contract text ("binds the round-64 lesson Gate block to the round-61 spot-check's actual verdict span") is therefore only half-enforced.
- Frozen predicate arithmetic for the `disagreements=1` input is correct at T0: exactly one spot-file line carries both `S432` and `Disagree`.

## Verified facts (T0)

1. Span occurs verbatim exactly once in the spot file.
   - `git show 4c8295fa:corpus/lessons/round-61-verifier-spotcheck.md | grep -o -F '<span>' | wc -l` → `1`.
   - Line 33, byte offset 3171. Byte slice is identical to the frozen constant (hex-compared).
   - Full line 33: `| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body \`.ufo/waves/round-61/sources/S432.html\` | Disagree | “Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation. Lesson itself identifies it as a generic lead-in. |`
2. The round-64 lesson Gate quotes it.
   - `corpus/lessons/round-64.md` at T0: `## Gate` section, `gate_len=3527`, span count `1`, `lesson_gate_bool=true` using the counter's own `section()` helper and the counter's boolean expression.
   - Quoted at lesson line 95, inside `"..."` after `row "S432 / Fetch" — its reason:`. Verbatim, one occurrence in the whole lesson.
   - The Gate section is the only `## Gate` heading in the lesson.
3. `SPOT_VERDICT_SPAN` equals the spot text byte-for-byte.
   - `c64_calibration.py` at T0 (sha256 `5489eb2f…088adf`, frozen sha matches):
     `SPOT_VERDICT_SPAN = ("is only a generic lead-in, not substantive evidence for a " "response-header expectation")` at lines 78–81.
   - `SPOT_VERDICT_SPAN == target` → `True`. UTF-8 bytes equal → `True`.
4. S432 `Disagree` count is exactly one.
   - Spot file: `grep -n -F 'Disagree'` → one line only, line 33.
   - Counter metric `sum("S432" in ln and "Disagree" in ln ...)` → `1`. Matches `disagreements=1`.
   - Lowercase `disagree` on lines 36 and 42 is not counted by the metric, which is correct (those lines lack `S432` on the same line as `Disagree`, and the metric is case-sensitive).
5. Pins for the spot file: the counter reads `SPOT_REL` only for the disagreement count (`c64_calibration.py` lines 193, 343–346); `SPOT_REL` is absent from `PIN_SHAS`.

## Attacks and results

Run as `python3 -B counter.py --root <fixture> --revision <fixture head>` on scratch clones of the T0 tree. All edits were committed in scratch fixtures only.

| id | edit (scratch fixture) | result | met |
|---|---|---|---|
| T0 | none (`git archive 4c8295fa` → fixture `fdd3a725`) | `disagreements=1 pins=1 … lesson_gate=1 … unresolved=0 met=true` | true (exit 0) |
| A1 | spot S432 verdict sentence reworded so the span no longer appears in the spot file (`fxA`, `8e067ba1`); lesson Gate still quotes the old span | `disagreements=1 … lesson_gate=1 … unresolved=0 met=true` | **true (exit 0)** |
| A2 | spot S432 `Disagree` → `Agree` (`fxB`, `83a85fff`) | `disagreements=0 … unresolved=0 met=false` | false (exit 1) |
| A3 | duplicate planted `S432 / Fetch dup … Disagree` row appended (`fxC`, `e6c8d81e`) | `disagreements=2 … unresolved=1 met=false` | false (exit 1) |
| A4 | span removed from lesson Gate (replaced with different wording) (`fxD`, `79357e2e`) | `disagreements=1 … lesson_gate=0 unresolved=1 met=false` | false (exit 1) |
| A5 | "span moved" check (`fxE`, `fe2bbc5c`) | my edit was a no-op (span stayed in Gate); **discarded, not evidence** | n/a |

A1 is the finding. The counter treats the spot file as an opaque source for the disagreement count and does not compare the verdict reason to the span. Editing the verdict reason without touching the lesson produces green. The pinned sha set (raw, text, ledger, recipe) does not cover the spot file, so nothing catches the drift.

Residual: `SPOT_VERDICT_SPAN` binds to the lesson only. Binding to the spot file is enforced by no code path in the counter. The only check on that link is the human/integrator reading of the spot file. Equivalent gap for the spot file's own bytes: the counter does not sha-pin `corpus/lessons/round-61-verifier-spotcheck.md`, so the spot file can change without any pin failing.

## Commands and output (exact)

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:corpus/lessons/round-61-verifier-spotcheck.md | grep -o -F 'is only a generic lead-in, not substantive evidence for a response-header expectation' | wc -l
1
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:corpus/lessons/round-61-verifier-spotcheck.md | grep -n -F 'Disagree' | cut -c1-40
33:| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body `.ufo/waves/round-61/sources/S432.html`
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:corpus/lessons/round-64.md | grep -n -F -B2 -A2 'is only a generic lead-in'
93-**Outside verdict:** the round-61 non-author spot-check `Disagree` on the
94-S432 admission (`corpus/lessons/round-61-verifier-spotcheck.md`, row
95:"S432 / Fetch" — its reason: "is only a generic lead-in, not substantive evidence for a response-header expectation")
$ sha256sum (T0 blobs, via git show)
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  c64_calibration.py   (frozen OK)
b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013  round-61-verifier-spotcheck.md
b4ac2fbd4ca77fdb66c54ce514719d743127b1c895b2d044e564609a796b1271  round-64.md
$ python3 -B counter.py --root fx --revision fdd3a725...   (fx = git archive of T0)
revision=fdd3a72548c706842c98e1a2c692a24508c7c1db disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B counter.py --root fxA --revision 8e067ba1...   (spot verdict reworded, lesson unchanged)
revision=8e067ba1483ec68123b4b373ab866cccc9f72644 disagreements=1 ... lesson_gate=1 ... unresolved=0 met=true
exit=0
```

Lane `git status --porcelain` read-only check: only pre-existing untracked round-64 seat/artifact paths; nothing written into the lane tree by this seat.

## Remaining unknowns

- Whether the lane intends the spot file to be pinned. The contract pins raw/text/ledger/recipe but names the spot file only via the lesson Gate and the `disagreements` metric. I did not decide intent; I report the gap.
- A1 is a counter-level gap. Whether it reproduces the round-63 defect class as a "wave attack green" depends on the kill-rule reading ("any wave attack reproduces a marker-only / stub / do-nothing / digest-consistent-fabrication green"). A reworded-spot fixture is none of those four named classes verbatim; I flag it, I do not classify it against the kill rule.

## Tooling

No tools installed or upgraded. Used: `git` (read-only and scratch clone/archive/commit), `python3` stdlib (3.14 host), `grep`, `sha256sum`, `cmp`.

## Scratch

Scratch tree `/fast/scratch/hyaku/kake-r64/ScoutSpotSpan/` removed after report write.
