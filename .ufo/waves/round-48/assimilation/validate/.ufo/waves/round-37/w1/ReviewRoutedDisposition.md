# ReviewRoutedDisposition — round-37 wave 1 (reviewer, leaf)

I did not touch `/fast/scratch/hyaku/kake-r37/`. I only read path strings that appear in lane files.
One stray write: I dumped the item prompts to `/tmp/kake-w1-items.txt`, then moved the file into
`/fast/scratch/hyaku/kake-r37w1/ReviewRoutedDisposition/w1-items.txt`. Nothing was written in the lane
except this report. No tools were installed. No counter was run.

Inputs: `corpus/lessons/round-36-verifier-spotcheck.md:151-172` (routed list), `git show 4b089da:SCORECARD.md`
(declaration and control call), `.ufo/waves/round-37/w1-spec.json` (32 items, read with `jq -r '.items[]'`, exit 0),
the prompt duty `.ufo/prompts/kake-round-37.md:322-325` ("turn every … routed defect into a lesson-backed
QUALITY.md criterion or fix, or say in the report why not"). The session goal file
`.scratch/goal-20261022-hyaku-12h.md` holds no kake-36/37 routes (grep → no match), so I used the routes named in my assignment.

## Verdict
Every routed item has at least one wave-1 item. None of them rests on C1, the round's only claim:
all eight are dispositioned as non-claim repairs or rules. Four gaps leave part of an item unaddressed: G1 (the limit line for
item 3), G2 (control sandboxes were siblings of the key, item 2/7), G3 (the 18 round-36 undecided points, item 8),
G4 (`used-by` for the new rows, item 6).

## Disposition table
| # | Routed item | Wave-1 items | Disposition | Gaps / evidence |
|---|---|---|---|---|
| 1 | `bf9b2089` orphaned | ScribeR36Corrections (1); ScribeQualityCriteria ("cited hash resolves or names its bundle"); ScribeMistakeMine candidate | non-claim repair | `git cat-file -t bf9b2089` → "Not a valid object name"; `git bundle list-heads .ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle` → `bf9b2089… refs/heads/postfix`. `round-36.md:154` already names the bundle, but `SCORECARD.md:1748` does not, so that line needs the append. QUALITY r36 (e) checks only 40-hex hashes in declaration sections, so the new criterion must also cover short hashes in result sections. |
| 2 | Containment (seats wrote into the lane) | the wave context bounds (sandbox only, L1 copies); ScribeQualityCriteria (L1 runs `jj-lane.sh state` after each wave) | non-claim repair (rule) | No check script enforces it yet. Observed `git --no-optional-locks status --porcelain`, exit 0: only L1 files (` M make_w1_spec.py`, `?? w1-*.json/txt`, `?? w1/`), no seat files so far. **G2**: see item 7. |
| 3 | Wording "meets (a)–(g)"; the 9 sealed survivors need killing fixture classes; append a limit line | ExecC2Fixtures (formerly C2, now non-claim); RevengerSurvivors; MutSelftestTolerance; MutC2Counter; ReviewC2Counter | non-claim repair, partial | 9-survivor check below. **G1**: no item drafts the limit line. ScribeR36Corrections covers only items 1, 5 and 6; ScribeQualityCriteria writes criteria, not row text. `round-36.md:11` still says "meets the public contract (a)–(g)", and capability row `SCORECARD.md:197` has no limit naming the 9 mutants or M24 (it only links `round-36.md` "Carried open", which lists neither). |
| 4 | Key v2 changed after scoring; rule of record; casefold class loosened (24→26) | declaration ("original rule kept as the rule of record (round-36 routed defect 4)"); ScribeQualityCriteria | addressed as a rule | No check script. Untested this round, because no key change has happened. The casefold loosening is not repaired: acceptable, since the round-36 claim is closed and the verdict is unchanged. |
| 5 | Junk control recorded as if it ran | the control-wave seat CtlC1Junk ran and finished (no policy filter); ScribeR36Corrections (5) | fixed (run) plus text correction | Under the round-36 counter: 0/28, exit 1 (`verification/control-r36-junk.json`, `.exit`=1). Under the round-37 counter: 0/28, exit 1. The receipt's `toolSha256` `4c23062f…cb33e` equals `sha256sum retained/controls/CtlC1Junk-source_recheck_junk.py` (observed). Lines to correct: `SCORECARD.md:1746` and `round-36.md:143` ("No do-nothing, junk, … met/reached 25"). The receipt's `toolFile` is a path in the forbidden tree, so anyone re-checking must use the retained copy. |
| 6 | Gate lines S091, S093, S094; `used-by` of S088–S092 | ScribeR36Corrections (6) | non-claim repair | **G4**: ScribeSourcesRows (new rows S095–S097) is not told the `CORPUS.md:107` rule ("`used-by` — paths of the knowledge entries or lessons"). The new rows risk repeating the defect by naming `scripts/robots_audit.py`. ScribeKnowledgeEntry's `corpus/knowledge/robots-txt-rules.md` is the right `used-by` target. |
| 7 | QUALITY r36 (f) has no polarity receipt; (d) passes a root listing over a key; (a) has no bare-id negative | ExecCriteriaRepairs (`polarity_check.py`, `control_tree_check.py` v2, `bare_id_check.py`) | non-claim repair | (f) as written (`QUALITY.md` "Round-36 criteria" (f)) has two halves: polarity, and "checks do not share one fixed label". `polarity_check.py` covers only polarity. **G2**: the control-wave sandboxes were `/fast/scratch/hyaku/kake-r37/ctl/<Seat>/` (`ctl/CtlC1Junk.md:11-33`), siblings of the key at `/fast/scratch/hyaku/kake-r37/private/cases.json` (`ctl/MutRefPass.md:7`). v2 as specified inspects only "the listed tree", so it cannot see a key next to it; the control seats' key-blindness rests on their instructions. Wave 1 moved to `kake-r37w1/`, so this is fixed going forward but not recorded as a limit. |
| 8 | Carried tool defects | ExecRecheckHardening (attribute `<script`, FIFO, huge manifests, `body_path` race); round-37 counter at declaration; ReviewSealedCounter; SentinelCounterJail | partly fixed (non-claim), partly carried | Round-37 `sealed_count.py` handles D1 (`:96-99`, `TypeError` → `repr`), D2 (`:128` `setdefault`) and earlier-case visibility (`:233` removes each run's directory). Still carried: `:197` `Path(args.tool_file).read_bytes()` is unguarded, so a missing `--tool-file` crashes with exit 1 ("not met") instead of 2 [INFERENCE, code read; not run, because the C1 counter is forbidden to me]. `:167` binds scratch read-write, so files a tool writes survive across runs; no answer leaks, and it is Sentinel's scope. **G3**: the 18 undecided round-36 contract points have no item (CriticContractAmbiguity attacks the round-37 contract), and no item drafts the line carrying them forward. The hardening also amends contract (c) of an admitted capability, so the SKILL registry row (`SKILL.md` ~1060, "101 fixtures", one selftest) and the capability row need updating when it lands. |

## The 9 sealed survivors against the C2 counter (selftest fixture classes)
Command: `jq '.perMutant[]' .ufo/waves/round-37/verification/c2-at-621fb528.json` (exit 0); fixture lines from `git show 4b089da:scripts/source_recheck_selftest.py`.
| Mutant | Rule skipped | Killed at base 621fb528 | Killer (line) | Tolerant (`accept`)? |
|---|---|---|---|---|
| M07 | redirect resolved from the original URL | no | — | ExecC2Fixtures target |
| M08 | dot segments kept | no | — | ExecC2Fixtures target |
| M13 | raw start tags case-sensitive | yes | `c09-script-end-tag-case-insensitive` (:378) | no |
| M20 | parameter names case-sensitive | yes | `f11-charset-parameter-name-case-insensitive` (:501) | no |
| M24 | BOM mark kept | no | — | ExecC2Fixtures target |
| M26 | `ascii` read as ASCII | yes | `f05-charset-ascii-means-windows-1252` (:473) | no |
| M28 | invalid bytes dropped | yes | `f16-invalid-bytes-become-replacement-character` (:521) | no |
| M31 | empty id accepted | yes | `g07-check-with-empty-id` (:545) | no |
| M32 | version unchecked | yes | `g02-manifest-version-not-1` (:529) | no |

`accept=` appears only at :286, :539, :601 and :631, none of them a killer above. So the selftest already has a
killing class for 6 of the 9. The 3 in both sets (M07, M08, M24) plus the selftest-only M09 and M11 are
exactly ExecC2Fixtures' 5 targets. If that item reaches 32/32, every one of the 9 has a selftest class.
Gaps: (i) the sealed side is not extended. That is acceptable: the round-36 key was revealed at `fd1fb723`,
so new sealed cases for a closed claim certify nothing. (ii) Each of the 6 is killed by exactly one fixture
(`killerCount` 1), which is fragile. (iii) A 32/32 result does not show contract grounding, because the
snapshot control met the same counter (control call). Only per-fixture contract-sentence names plus a
wave-2 review of their expectations against the round-36 text can separate the two.

## Not routed but named in the spot-check (`:30-37`)
The report's "no fleet-root file carries this lane" needs a qualification (driver `.ufo/state/kake.report-baseline`). No item covers it;
it is wording for the L1's round-37 report.

## Recommendations to L1 (advisory)
G1: give ScribeR36Corrections (or a wave-2 scribe) the limit-line append for `round-36.md:11` and the `SCORECARD.md:197` row.
G2: record the control-sandbox-next-to-key fact as a limit, or extend `control_tree_check` v2 to the seat root's parent.
G3: carry the 18 points forward in `round-37.md` "Carried open".
G4: check the `used-by` of S095–S097 against `CORPUS.md:107` at integration.

## Not verified
Wave-1 outputs (none existed when I read; `w1/` held only `swarm-registry.json`). Whether ExecC2Fixtures reaches 32/32.
Whether the `--tool-file` crash still happens (code read only). The contents of any file under `/fast/scratch/hyaku/kake-r37/`.
