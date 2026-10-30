# ScoutSiblingOverlap — round 64 (kake)

Seat: `ScoutSiblingOverlap` (scout, leaf, no subagent dispatch). Read-only scan.
Inputs read at the working trees as found on 2026-10-30; no git or jj mutation
anywhere; no sibling file touched; no tool installed or upgraded; no
network fetch. Scratch used: `/fast/scratch/hyaku/kake-r64/ScoutSiblingOverlap/`
(created empty, removed before yield).

## Verdict

**kake uniquely owns the round-64 ground.** Across all 18 sibling `SKILL.md`
and all 20 sibling `PROVINCE.md` files, no file names the quote-class
machinery, the calibration-counter family, the S432/fetch-spec span, or the
freshness sidecar/sweep instrument as its own. Zero sibling instruments read
kake's sidecar or sweep. Overlaps that exist are lexical (same word, different
object), one same-document citation (WHATWG Fetch, different section), one
lane-local S-id collision, and one **operator-owned** question about the
`calibration` axis itself that bears on C1 (§5).

## 1. Quote-class machinery — uniquely kake

Probe (all 18 `*/SKILL.md` + 31 `*/PROVINCE.md`, sibling lanes only):

```
for f in */SKILL.md */PROVINCE.md (excl. kake*):
  grep -c -i -E "quote.class|quote_class|collapsed-only|raw-substring|raw_substring" "$f"
→ every file hits=0   (38 files: 18 SKILL.md + 20 PROVINCE.md)
```

The only SKILL row naming the machinery is kake's own:
`kake-shokunin/SKILL.md:1348` (`quote-class-counter`, `c50_quote_class.py`,
ledger `.ufo/waves/round-50/quote-classes.json`).

Same-named tools in siblings are different objects, all lane-local:

| Sibling file | What it does | Overlap verdict |
|---|---|---|
| `chousa-shokunin/tools/quote-reopen.py` | Live GET re-open of a located quote; verdicts `VERBATIM`/`ABSENT`/`TOO_LONG`/`NO_SOURCE`/`UNREACHABLE`; registered `chousa/SKILL.md:88` | Different question (live presence vs. retained-blob class). Already recorded: round-63 `ConnSiblingOverlap.md` §CONTESTED 3. Do not cite as class evidence. |
| `kotodama-shokunin/tools/check-gate-quotes.py` | 25-word cap lint on kotodama's own `## Gate` rows | Length lint; unrelated. |
| `mado-shokunin/.ufo/waves/round-35/w1/reports/RevQuotes.md:97-107` | Reviewer uses the phrase "quote-class" about mado's own gate quotes (S203/206/207/208) | Shared word in a mado-internal review; mado does not adopt kake's `raw-substring`/`collapsed-only` vocabulary. Not contested scope. |
| `tsukuroi-shokunin/.ufo/waves/round-48/w2/ConnWave.md:26`, `round-49/w1/R49ConnWave.md:37` | Read-only cross-lane scan that *reads* `kake/scripts/quote_class.py` as a pattern example and lists it in a table | Adjacency read by a reviewer, not an ownership claim. No write. |

No sibling SKILL/PROVINCE names the vocabulary `collapsed-only` or
`raw-substring`, a quote-class deriver, or the round-50/63/64 class ledgers.

## 2. Calibration-counter repair — uniquely kake (family); lexical overlap only

Probe: `calibration` appears in every sibling's `shokunin.conf` axis list
(`shokunin.conf:45-55,81-83`). Sibling *counters* carrying the word in
their file names are lane-scoped instruments over their own claims:

```
kaidoku-shokunin/tools/round-26/c2-calibration.py
kaidoku-shokunin/tools/round-32/c2-capability-calibration{,-v2,-v3}.py
kaidoku-shokunin/tools/round-35/c2-calibration-counter.py
kama-shokunin/tools/round40-calibration-audit.py
mori-shokunin/tools/mori-round41-calibration.py
```

None names kake's `c62_`/`c63_`/`c64_calibration.py` family, the `resolved`
component, the S432 located-line pin, or kake's SCORECARD row. Sibling SKILL
rows that use "calibration counter" (kaidoku `SKILL.md:1677,1794,1797`; mori
`SKILL.md:1018,1144,1273`; kama `SKILL.md:1430`) each describe their own
claims file. Exact-phrase and identifier sweep for kake's family:

```
grep -rn -E "c6[1-4]_calibration|semantics-binding|resolved.*binds" */SKILL.md */PROVINCE.md → 0 (siblings)
```

The only prior report naming the family is kake's own
`.ufo/reports/round-63/kake.md` and `kake-shokunin/.ufo/waves/round-63/w1/ConnSiblingOverlap.md`
(§2): same conclusion at round 63.

## 3. S432 / fetch-spec span — uniquely kake for the S432 row; one same-document adjacency

Probe: `fetch.spec.whatwg.org|nosniff|X-Content-Type-Options` over every
`*/corpus/SOURCES.md`:

```
audio/chousa/game-dev-2d/game-dev-3d/kagi/kaidoku/kama/kasegi/kengaku/kotoba/
kotodama/kumitate/lore/mado/revenger/souji/tabi/tameshi/tsukuroi  → hits=0
mori-shokunin/corpus/SOURCES.md:231  → 1 hit
```

- `kake-shokunin/corpus/SOURCES.md:178` — S432, WHATWG Fetch §3.6
  `X-Content-Type-Options`, proposition: the field has one defined value,
  `nosniff`. kake is the only lane holding a `nosniff` row.
- `mori-shokunin/corpus/SOURCES.md:231` — S225, Fetch Standard §4.5
  HTTP-redirect fetch, proposition: twenty-hop redirect chain limit. Same
  document, disjoint section and proposition.
  **Contest status:** adjacency, not overlap. Per round-63 §CONTESTED 2, S225
  is never counted as coverage of, or a duplicate of, S432. Mori's
  `fetch` row is not a candidate for the round-64 S432 re-open.
- `kotodama-shokunin/corpus/SOURCES.md:461` — lane-local id `S432`
  (Walters Art Museum tsuba records). **S-id string collision only.** Any
  cross-lane citation of this round's S432 must be written `kake/S432`.

Sibling SKILL/PROVINCE files do not mention the `S432` id, `nosniff`, or
the fetch spec (`grep -l` over `*/SKILL.md */PROVINCE.md` for those tokens
→ no hits outside kake).

## 4. Freshness-sidecar / freshness-sweep instrument — uniquely kake

Probes:

```
# sibling SKILL/PROVINCE: sidecar/sweep/paths tokens
grep -n -i -E "freshness.sidecar|freshness.sweep|sidecar binding|paths sidecar|§paths" */SKILL.md */PROVINCE.md (excl. kake*)  → 0 lines

# sibling file names
find . -name "*freshness*" -o -name "*sidecar*" (excl. kake, .ufo)
  → only kaidoku/kumitate per-claim evidence files named *sidecar*-test/*sidecar*-driver,
    and game-dev-3d/reports/round-*/freshness-pin.md, lore/corpus/knowledge/r102-freshness-sweep.md,
    lore .ufo/waves seat files with "freshness" in the name.
```

None of those names is `freshness-sidecar.json` or `freshness-sweep.mjs`.
Their owners are unrelated instruments:

| Sibling | Instrument | Overlap |
|---|---|---|
| `game-dev-3d/reports/round-*/freshness-pin.md` | 3D-engine version pin reports | different artifact class |
| `lore/corpus/knowledge/r102-freshness-sweep.md` | lore's own sweep note | same word, lore-internal |
| `tabi/SKILL.md:1555-1559` | `check-freshness.mjs` `closeout-pin-witness` | different script, tabi-owned, its own registry row |
| `kotoba/verifiers/check_substrate_repin_v2.py` (`SKILL.md:510`) | substrate re-pin freshness counter | different artifact |
| `tsukuroi/tools/check-freshness-r17.py` (`SKILL.md:1899`) | host sync-db freshness | different domain |
| `kasegi/…/check-freshness.mjs` (`SKILL.md:179,1008`) | bounty ops staleness | different domain |
| `kagi/SKILL.md:177` | drift-pin freshness | different domain |

Sibling readers of kake's sidecar or sweep: none. The sidecar's listing
appears only as file-list text in `kasegi-shokunin/.ufo/waves/round-44/wave2/R44W2Scout01.md:445`
(a file inventory, not a read of its content) and as a string in
`souji-shokunin/.ufo/waves/round-43/w1/R43connector01/scan-receipts.json`
(souji's read-only census of kake's SKILL.md text, quoting kake's own
sidecar-binding description). Neither is an ownership claim; neither writes.

Kake's own registration: `kake-shokunin/SKILL.md:212` (freshness-sweep gate
row), `:348-350` (instrument inventory). No sibling gate registry row names
the sweep.

## 5. The one contested item — operator-owned, bears on C1

**Not sibling contest. Operator authority.** `.ufo/l0-questions.md:181`
(kake, round-59, still unanswered in this tree):

> Calibration sub-axis ownership … rounds 54-59 declare a claim on
> `calibration` … while the prompt names kake's axes as operability +
> freshness. Should calibration stay a scored kake sub-axis (then the
> lowest-axis rule keeps landing on it), be folded into operability, or be
> dropped from kake's SCORECARD?

`shokunin.conf:48` lists kake as `operability + freshness`. The round-64
contract scores C1 as "calibration (lowest owned axis, 2/10)". The
contract's C1 claim therefore rests on an L0 ruling that has not been filed.
This scout does not rule on it. Consequence for the integrator: if C1 is
scored, the axis assignment is an operator question, not a sibling
question. Recorded at `shokunin.conf:48`, `.ufo/l0-questions.md:181`,
`contract.md` C1 header.

## 6. Scope searched and not searched

Searched (read-only, working trees): all 18 `*/SKILL.md`, all 31
`*/PROVINCE.md`, all 20 sibling `*/corpus/SOURCES.md`, sibling
`tools/`/`scripts/`/`templates/`/`research/` for name collisions, fleet-root
`scripts/` and `tools/`, `shokunin.conf`, `AXES.md`, `.ufo/l0-questions.md`.

Not searched: `kake-shokunin/.git` history (not required; scout is working-tree);
the full text of every sibling `.ufo/waves/**` seat report (only name-level
and grep-level hits, quoted above). The `MANIFEST.json` and `.ufo/reports/**`
hits for `quote-class` and `freshness-sweep` are kake's own round records
and are not sibling claims.

## 7. Constraints for the integrator (carry-forward from round 63, still true)

1. Cite S432 cross-lane as `kake/S432`.
2. Keep mori S225 distinct from S432; never count it as coverage.
3. Keep `quote_class.py` verdicts (`raw-substring`/`collapsed-only`/`absent`)
   separate from chousa `quote-reopen.py` verdicts.
4. Leave the L0 `calibration` ruling where it is (operator channel).

## 8. Tools and installs

None installed, upgraded, or run. Shell probes were `grep`, `find`, `sed`, `cat`
and `ls`, read-only. The operator tooling directive was not invoked: nothing
here needed an extra tool.

## 9. Blockers

None for the scan. The L0 question in §5 is an operator decision, reported
and not resolved here.
