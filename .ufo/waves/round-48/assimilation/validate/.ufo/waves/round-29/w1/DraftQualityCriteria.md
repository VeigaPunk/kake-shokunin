# Draft QUALITY.md criteria — round 29 (draft only, nothing landed)

Seat `KakeR29.DraftQualityCriteria` (scribe). Scope: draft text for `corpus/QUALITY.md` and the "not repaired this round" paragraph. No product file, gate, counter, fixture, corpus entry or lesson was edited; no git or jj command was run in the lane. Canonical draft copies (house wrapping): `/fast/scratch/hyaku/kake-r29/w1/DraftQualityCriteria/quality-draft-qualities.md` and `/fast/scratch/hyaku/kake-r29/w1/DraftQualityCriteria/not-repaired-round29.md`. The two blocks below repeat that wording with wider wrapping to stay inside the report length limit.

## Commands run (read-only, in /home/vgpnk/Projects/shokunin/kake-shokunin)

| Command | Exit | Observed |
|---|---|---|
| `ls scripts/fixtures/citing-set \| wc -l` | 0 | 29 fixture cases |
| `grep -rl reason scripts/fixtures/citing-set \| wc -l` | 0 | 0 files name a reason code |
| `python3 -c` over `scripts/fixtures/citing-set/*/expected.json` | 0 | all 29 hold exactly the keys `exit` and `findings`; e.g. case 15 is `{"exit": 2, "findings": ["input_invalid"]}` — id only, no reason |
| `grep -n 'item.get("id") == want_finding' .ufo/waves/round-28/c1_interface_count.py` | 0 | line 141 — the counter grades the finding id only |
| `grep -n '"findingReasons"' .ufo/waves/round-28/c1_interface_count.py` | 0 | line 150 — the observed reason is collected for display, never asserted |
| `grep -n 'quote\|word' .ufo/waves/round-28/c2_source_count.py` | 0 | lines 126–131 — one quote per Gate line, 1–25 words, no source read |
| `grep -c <8 round-28 reason labels> scripts/citing_set.py` | 0 | 1,1,1,1,3,2,2,1 occurrences; the only other mentions are `corpus/lessons/round-28.md` and `corpus/lessons/round-28-verifier-spotcheck.md` (prose) |
| `grep -n 'Drift sentinels' -A 12 /home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md` | 0 | line 173: "Same axis+surface claim or same routed defect class in a lane 3 rounds running → The lane's next round must work a different frontier area." |

## Draft criteria (append-only block for the end of `corpus/QUALITY.md`)

Every prior line of `corpus/QUALITY.md` stays byte-identical (round-20 ruling). The round-28 bullet "Conformance exceptions stay named" (`corpus/QUALITY.md:317`) is cited, not edited.

> ## Fixtures, reason codes and quote truth — round 29
>
> Grounding: `corpus/lessons/round-28-verifier-spotcheck.md:208-230` (routed defects 1 to 3), `PROTOCOL.md:398-402` (§Gate standard, Self-test), the committed fixture set `scripts/fixtures/citing-set/` (29 cases, each `expected.json` holding an exit code and a finding-id list only) and the round-28 counters `.ufo/waves/round-28/c1_interface_count.py` and `.ufo/waves/round-28/c2_source_count.py`. This section appends to "Counters and field evidence — round 28" (`corpus/QUALITY.md:298`).
>
> - **A committed fixture asserts the reason code, not only the finding id.** A gate that can emit more than one reason under the same finding id ships committed fixtures whose expected values name the reason code next to the finding id, and the fixture runner compares it. Reason codes that exist only in the gate source are uncovered behaviour, not regression coverage. Round 28's gate emitted eight new reason codes (`document_not_regular_file`, `document_not_json`, `corpus_directory_missing`, `corpus_empty`, `not_a_directory`, `population_id_unreachable`, `revision_not_found`, `root_not_repository_top_level`; `corpus/lessons/round-28-verifier-spotcheck.md:70-74`), while all 29 committed fixtures assert only the exit code and the finding-id list. Fails if: the committed fixture runner passes while no committed fixture expectation names a reason code. Round 28 observed `grep -rl reason scripts/fixtures/citing-set` → 0 files, and in code and fixtures the reason labels appear only in `scripts/citing_set.py` (the other mentions are the round-28 lesson and spot-check prose). Limit: a fixture set that names a reason code while the runner never compares it fails the same way.
> - **A counter compares the reason code, not only the id.** A counting command that grades a repair asserts, per case, the expected exit, the expected verdict and the expected reason code of the finding it grades. Collecting the observed reason into a summary for display is not a comparison. The round-28 counter matched on the finding id only (`.ufo/waves/round-28/c1_interface_count.py:141`) and carried the observed reason in a display field (`.ufo/waves/round-28/c1_interface_count.py:150-151`), so a gate that returned the right id with the wrong reason scored a full pass. Fails if: the counter exits 0 on a case whose gate output carries the expected finding id with an absent or different reason. This bar applies to the next round that works the surface; round 29 did not work it (see the round-29 note below).
> - **A Gate quote is found in retained source text.** A Gate quote counts only when it is an exact substring of retained visible source text whose digest the counter verifies against the round's committed receipt before comparing. A shape check (one quote per Gate line, the id, the URL, the access date, 1 to 25 words) is quote shape, not quote truth: the round-28 C2 counter read the quote out of the entry line and counted its words (`.ufo/waves/round-28/c2_source_count.py:126-131`) without opening the source. Fails if: the counter that grades Gate quotes exits 0 on a committed row whose quote is not a substring of the retained text, or whose retained text digest differs from the receipt digest. The round-scoped counter `.ufo/waves/round-29/c1_quote_truth.py` (digest verification plus a one-letter-flip control) shows the shape of such a check; it is round-scoped evidence and does not by itself satisfy this standing bar for later rounds.

## Draft: "not repaired this round" text for routed defects 1 and 2

> ### Not repaired this round (routed defects 1 and 2)
>
> Round 28 routed two defects on the citing-set surface. Round 29 repaired neither and says so plainly.
>
> Routed defect 1 — committed fixtures for the round-28 reason codes — stays open. All 29 committed fixtures under `scripts/fixtures/citing-set/` still assert only an exit code and a finding-id list; `grep -rl reason scripts/fixtures/citing-set` returns 0 files, and in code and fixtures the eight round-28 reason codes exist only in `scripts/citing_set.py`. The regression coverage for those codes still lives only in the round-scoped counter `.ufo/waves/round-28/c1_interface_count.py`, which is not a committed fixture and is not run by the gate's own self-test.
>
> Routed defect 2 — the round-27 failure families outside the declared C1 set — stays open on the terms round 28 recorded: the `JSON-PROTOCOL` duplicate-key and nonfinite cases; `S01`-style ids that measure clean; repeated CLI options resolved by last value wins; the deep-corpus traceback; and the missing `O_NOCTTY`.
>
> Why this round did not repair them: the session drift sentinel for "same axis+surface claim or same routed defect class in a lane 3 rounds running" (`/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:173`) requires the lane's next round to work a different frontier area. The citing-set surface was worked in round 27 (the round-27 C1 citing-set completeness claim, its counter and its fixture tree) and again in round 28 (the C1 interface repair of `scripts/citing_set.py`); repairing it a third round running is the case that sentinel names. Round 29 therefore took a different frontier area, project-site base paths for GitHub Pages, and carried both defects forward as named debt.
>
> Consequence for the record: the first half of routed defect 3, that the C1 counter checks finding ids and not reason codes, is unchanged. The round-29 C1 counter measures the new base-path source rows S040 to S043, not the citing-set surface. Nothing in this round changes the citing-set gate, its fixture set or its counters. The next round that works the citing-set surface inherits both defects, and the three criteria above apply to it.

## Evidence pointers and limits

- Routed defects: `corpus/lessons/round-28-verifier-spotcheck.md:208-230`. Gate standard, Self-test clause: `/home/vgpnk/Projects/shokunin/PROTOCOL.md:398-402`. Round-28 QUALITY section to append after: `corpus/QUALITY.md:298-332`; the bullet this section narrows: `corpus/QUALITY.md:317`.
- Not verified here: I did not execute `scripts/citing_set.py`, `scripts/citing_set_selftest.py`, the round-28 counters or the round-29 quote counter. Every statement above is read from committed bytes, and the drift-sentinel rule is quoted from the session goal file, not adjudicated.
- The three criteria are drafts. The L1 decides whether they land and where the "not repaired" paragraph lands (the round-29 lesson and the round report are the natural homes).
