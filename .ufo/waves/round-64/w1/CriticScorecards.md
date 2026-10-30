# CriticScorecards — round-64 SCORECARD discipline audit at T0

Seat: `CriticScorecards` (critic, leaf; no subagent dispatch).
Revisions: base `1a48131577ba82c967650561be34e8dba909432a` (round-63 tip);
T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; tip `cc8add1fa740b920ea5179a71152680ab220c70c`.

## Verdict

- Scores hold at operability 10, freshness 10, calibration 2. **PASS.**
- Round-63 SCORECARD section stands unchanged. **PASS.**
- No round-64 landing rows exist at T0. **PASS.**
- Planned-row / predicate history: no post-hoc narrowing of any frozen `met` conjunction or control set. Six findings (F1–F6) are recorded below. None moves a score. F1 (missing pre-freeze do-nothing receipt) should be closed before admission.

## Checks that pass

1. **Scores unchanged.** `git rev-parse 1a481315:SCORECARD.md 4c8295fa:SCORECARD.md cc8add1f:SCORECARD.md` returns the same blob `23edbe0163a9f63cc3ba0288295c0c2a855afe64` for all three. T0 score rows, `SCORECARD.md:17-19`: `| operability | 10 |`, `| freshness | 10 |`, `| calibration | 2 |`. Every T0 added line that mentions a score reads the current lowest-axis value `2/10` (`contract.md` C1 heading; `corpus/lessons/round-64.md` C1 bullet). No new rating appears in any T0 artifact.
2. **Round-63 section unchanged.** The same blob identity covers `SCORECARD.md:4533-4563` at all three revisions. `LOG.md` is also identical (`c47d1dcec5677b34755933c32518e1cebbb788e5`) at all three. `git status --porcelain -- SCORECARD.md LOG.md` is empty in the lane.
3. **No round-64 landing rows.** `git show 4c8295fa:SCORECARD.md | grep -n -i 'round[ -]*64\|r64'` returns one line, `4560`, a round-63 sentence referring to "the round-64 repair recipe". There is no `## Round 64` heading and no round-64 capability row. The quote-class row at `SCORECARD.md:204` is the pre-existing round-50 row. T0 touched only `corpus/QUALITY.md` (`@@ -1420,3 +1420,7 @@`) among the score-bearing files.
4. **Frozen instruments.** `sha256sum` at T0 (`git show 4c8295fa:<path> | sha256sum`) and in the working tree both match the contract:
   - `c64_calibration.py` = `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`
   - `c64_quote_tool.py` = `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`
   - `fixtures/build_fixtures.py` = `7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3`
   - `fixtures/stub_tool.py` = `7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde`

## Predicate history: round-63 settlement recipe vs round-64 declared predicates

Source recipe: `corpus/lessons/round-63.md` §"Routed to round 64". Declared predicates: `.ufo/waves/round-64/contract.md`.

| Round-63 recipe item | Round-64 declared predicate (evidence) | Direction |
|---|---|---|
| Pin ledger and both blob sha256s as constants | C1 pins four blob shas (raw, text, ledger, recipe) and the located span `6150-6154` (`c64_calibration.py:66-70, 90-95`) | widened |
| Re-execute `extract_text.py` in-counter over the raw blob | `recipe_rederive` requires output == committed text blob and `TEXT_SHA` (`c64_calibration.py:226-229`); round-63 had no such check | widened |
| Gate `disagreements`/`unresolved`, not masked | `met` requires `unresolved==0` and `disagreements>=1` (`c64_calibration.py:267-270`); c63 had `unresolved = disagreements if not resolved else 0` (`c63_calibration.py:164-166`) | met widened; printed field narrowed (F2) |
| Wire frozen shas into kill rules | contract kill rules: any pinned sha differing ⇒ `unprovable` (`contract.md:56-61`); C2 tool-sha kill rule (`contract.md:88-`) | widened |
| Bind prose block-level; lesson Gate quotes "the spot-check's actual verdict line" | `lesson_gate` requires the 16-word span "is only a generic lead-in, not substantive evidence for a response-header expectation" (`c64_calibration.py:78-81, 256`) | narrowed from line to substring (F3) |
| Guard C2 JSON parsing | `safe_json` guards every parse (`c64_quote_tool.py`, `safe_json`) | widened |
| Pin selftest fixtures to the measured revision | tool and fixtures materialised from `git show <rev>` blobs (`c64_quote_tool.py:159-170`) | widened |
| Define "stub" as tool sha ≠ frozen sha | `tool_sha=mismatch` ⇒ `met=false` before execution (`c64_quote_tool.py:154-157`; `contract.md` C2 stub definition) | exact |

Claim-level comparison (round-63 contract predicate → round-64 contract predicate):

- **C1 controls:** round-63 had base, marker-fixture and junk-fixture (2 controls). Round-64 has base, marker, digest-consistent fabrication, junk and ledger-mutation (4 controls). **Widened.**
- **C1 met:** round-63 `met = resolved` where `resolved = quote_correction ∧ criterion ∧ lesson_gate ∧ source_row` (`c63_calibration.py:164,166`). Round-64 `met` is that conjunction plus `pins ∧ recipe_rederive ∧ class_match ∧ disagreements≥1 ∧ unresolved==0` (`c64_calibration.py:268-270`). **Strict superset.**
- **C2:** round-63 predicate was `present=1 selftest=4/4 frozen_cases=ok met=true`, base `present=0 met=false`. Round-64 adds the tool-sha pin and counter-side re-derivation. **Widened** on the measured side; base falsifier rebased (F4).
- **C3:** no round-63 predicate existed. The round-64 predicate is the round-63 could-not-evaluate fault itself (exit 2 → exit 0). It accepts a partial offline verdict (F5).

No post-hoc narrowing of a frozen `met` conjunction or control set was found. The narrowings that do exist (F2, F3) are declared in the same commit as the counters and contract (`4c8295fa`). They are not post-hoc relative to any wave score. Provenance limit: see F6.

## Findings

**F1 — The round-63 do-nothing counterexample has no committed pre-freeze receipt (process gap).**
- Round-63 `w1/CriticClaims.md:56-67` shows c63 `met=true` on fixture `09cd73d5` (round-62 tree + a fabricated 155-byte `S432.txt` + self-consistent ledger + marker lesson). That is component-identical to the round-63 after receipt.
- `corpus/QUALITY.md:1420` (round-63 criterion) requires: "before freezing, build the cheapest control that skips the claimed work — including digest-self-consistent fabrication … score it with the frozen counter, and commit the receipt."
- `.ufo/waves/round-64/controls/` has no such receipt. The enumerated controls (`contract.md:51-55`) are base, marker `4c666e76`, fabrication `f924538e`, junk `82dcba0d`, ledger-mutation `5b981bd0`. The `f924538e` receipt has `lesson_gate=0 quote_correction=0 criterion=0`, so it is not the round-63 construction. Sibling `w1/ExecDoNothing.md` covers D1 (base) and D2 (sidecar-only repin); its verdict section lists no round-63 fixture.
- **Observed check (scratch, not committed).** I cloned the lane at base `1a481315` into `/fast/scratch/hyaku/kake-r64/CriticScorecards/dn` (`git -C dn rev-parse --show-toplevel` = that path, asserted before commit), replaced `.ufo/waves/round-63/quote-class/S432.txt` with the 155-byte frozen quote plus newline, and committed as `8a5dc0f3c8cb201b5237dca801d19e2bb0da7a16`. The frozen T0 counter, run as:
  ```
  TMPDIR=/fast/scratch/hyaku/kake-r64/CriticScorecards/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root <clone> --revision HEAD
  revision=HEAD disagreements=1 pins=0 pin_drift=drift:text recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
  exit 1
  ```
  The attack fails at the text-blob pin before any ledger or class logic runs. Caveat: this rebuilt the blob-substitution component at the round-63 tip, not the original round-62 tree.
- **Verdict:** no score or `met` change. The control receipt the round-63 criterion requires is absent. Any committed receipt must be labelled a post-scored closure observation; a control added now is not this round's freeze-time control.

**F2 — The printed `unresolved` field no longer summarises the four components.**
- c63: `unresolved = disagreements` unless all of `quote_correction, criterion, lesson_gate, source_row` are 1 (`c63_calibration.py:164-165`).
- c64: `unresolved = max(disagreements − lesson_gate, 0)` (`c64_calibration.py:267`). It prints `unresolved=0` whenever `lesson_gate=1`, even when another component is 0.
- `met` is unaffected: `c64_calibration.py:268-270` conjoins those components directly. No committed receipt has `lesson_gate=1` with another component 0, so the difference is unexercised.
- **Verdict:** reporting-semantics narrowing; not a `met` narrowing.

**F3 — The lesson-gate binding is a substring, not the verdict line the recipe names.**
- Recipe text: "e.g. the lesson Gate must quote the spot-check's actual verdict line" (`round-63.md` §Routed). The recipe says "e.g.".
- Verdict cell, `corpus/lessons/round-61-verifier-spotcheck.md:33`: `“Web developers and conformance checkers must use the following” is only a generic lead-in, not substantive evidence for a response-header expectation. …`
- Counter binds `SPOT_VERDICT_SPAN` = "is only a generic lead-in, not substantive evidence for a response-header expectation" (`c64_calibration.py:78-81`, check at `:256`). A Gate quoting only that clause passes. The requirement is weaker than the full verdict line.
- The span is declared in the freeze commit, so this is a declared choice. Current green is not affected: `corpus/lessons/round-64.md` quotes the span.

**F4 — The C2 base falsifier is rebased, not narrowed.**
- Round-63 predicate: `present=0 met=false` at base (`round-63/contract.md:51-53`). That base was the round-62 tip, where no tool existed.
- Round-64 base is the round-63 tip `1a481315`, where `scripts/quote_class.py` exists, so the base prints `met=true`. `contract.md:71-74` states this. `w1/ExecDoNothing.md` confirms it as expected.
- The falsifier is replaced by the stub differential: `controls/stub-c64.txt` (`tool_sha=mismatch met=false`, exit 1) against `controls/stub-c63-defect.txt` (`met=true`, exit 0). Both files were read.
- **Verdict:** C2 has no base→measured delta on the lane tree (both `met=true`). It is a gate hardening, not a capability. Consistent with the SCORECARD: no score change and no capability row at T0.

**F5 — The C3 predicate accepts a partial offline verdict.**
- Predicate: "prints `VERDICT: OK` and exits 0" (`contract.md:104-119`).
- `controls/sweep-after.txt` prints `VERDICT: OK (exit 0, partial: offline)`, with §armed and §history "complete=false, never counted as pass".
- The §paths evidence that the kill rule requires is in `controls/no-harm/sweep.txt:5-6`: `§paths 172 files · 679 occurrences · 106 unique tokens` and `resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10`.
- **Verdict:** the claim should read "§paths evaluates offline; remote sections not run", not "sweep complete". The `unresolved 10` in §paths is not explained in the receipt. Freshness score stays 10 (`SCORECARD.md:18`). No inflation.

**F6 — Freeze provenance is not visible in git history.**
- `git log --diff-filter=A -- .ufo/waves/round-64/contract.md` returns only `4c8295fa`. The contract, both counters, fixtures, controls, sidecar re-pin, lesson and SKILL rows all first appear in that one commit.
- Earlier rounds separated freeze and build: round-60 `b3b9e29c`, round-61 `eaa9177e`. Round-63 froze with its build (`6d8c52a6`), so this is not new, but it means git cannot show the predicate existed before the counters were scored.
- Filesystem mtimes order the artifacts (contract 07:57, counters 07:50-07:51, controls 08:00, dispatch 08:07), but mtimes are not evidence.
- The four frozen instrument shas in `contract.md` match the committed and working-tree bytes (check 4 above), which is the strongest available freeze evidence.

## Commands run

```
git rev-parse 1a481315:SCORECARD.md 4c8295fa:SCORECARD.md cc8add1f:SCORECARD.md
git show 4c8295fa:SCORECARD.md | grep -n -i 'round[ -]*64\|r64'
git diff 1a481315 4c8295fa -- corpus SKILL.md LOG.md SCORECARD.md .ufo/waves/round-64/contract.md | grep '^+' | grep -i 'score\|rating\|10/10\|axis'
git show 4c8295fa:<c64 instrument> | sha256sum      # and working-tree sha256sum
git log --oneline --diff-filter=A -- .ufo/waves/round-64/contract.md
git show 1a481315:.ufo/waves/round-63/{contract.md,c63_calibration.py,c63_quote_tool.py}   # copied to scratch for comparison
git clone -q --no-hardlinks <lane> <scratch>/dn ; git -C <scratch>/dn checkout -q -B r64dn 1a481315 ; (fabrication commit 8a5dc0f3)
TMPDIR=<scratch>/tmp python3 -B .ufo/waves/round-64/c64_calibration.py --root <scratch>/dn --revision HEAD   # exit 1
```

## Tools

None installed or upgraded. Used: `git` (read-only on the lane; clone and commit in scratch only), system `python3` (frozen counter, run once).

## Scratch

`/fast/scratch/hyaku/kake-r64/CriticScorecards/` (clone `dn`, extracted round-63 files, `diffstat.txt`, `tmp/`). Deleted before yield. The outputs quoted above are retained in this report.

## Lane tree

Only this report was written, at `.ufo/waves/round-64/w1/CriticScorecards.md`. No tracked file, frozen claim, counter, receipt, contract or lesson was edited.
