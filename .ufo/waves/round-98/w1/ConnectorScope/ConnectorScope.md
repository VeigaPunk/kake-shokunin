# ConnectorScope — report (kake round 98, leaf seat, read-only)

Full evidence, per-lane HEADs, file/line cites and definitions: `overlap.md` in this seat directory.
Location note: the spec's `Report:` path `.ufo/waves/round-98/w1/ConnectorScope.md` lies outside this
seat directory, which the hard bounds forbid. The report is therefore written here, inside
`w1/ConnectorScope/`, and the L1 may copy it to the spec path.

## Findings

1. **Surface (a), capability table vs MANIFEST (strict, 2 instrument families):**
   - kaidoku `tools/round-32/c2-capability-calibration{,-v2,-v3}.py` (kaidoku HEAD c19d57cd): the same
     oracle class as kake C1. Its own negative control was measured as falsified
     (`corpus/lessons/round-32-verifier-spotcheck.md:71-72`, denial rows score `match=4 exit 0`). Cite as
     prior art and as a warning that the lexical predicate passes denial text.
   - mori `tools/mori-register-check.py` (mori HEAD 73308ff6): binds the active register to MANIFEST
     `capabilities_added`. Caution: mori round 57 found a frozen counter scanning the superseded first
     table and admitting false-greens (fleet `.ufo/reports/round-57/mori.md:12`). kake SCORECARD has one
     `## Capabilities` heading (line 191), so no current first-table ambiguity; the L1 should confirm
     `c98_captable.py` selects the active table.
   - Adjacent, not counted: kengaku `plans/round68_capability_table.py` (same failure mode, prior art;
     named divergence at kaidoku `.ufo/waves/round-76/w1/ConnectorCross.md:145-148`), chousa
     `tools/lane-preflight.py` G05, tameshi `tools/selfstate-freshness.py`, kama
     `tools/round74-selfdesc-canon.py`.

2. **Surface (b), RFC 5861 / SWR / SIE ground (token-level, 7 sibling lanes, 24 files; normative ground 0):**
   no sibling holds RFC 5861 text. Hits are captured response headers (kagi, tsukuroi, kama, kotoba, kasegi),
   third-party READMEs (kagi), a retained WHATWG Fetch copy (mori S225, prior art to kake S432), and a
   retained RFC 9111 capture that cites RFC 5861 (kumitate round-81, prior art for the RFC 9111 side).
   No conflict with kake C2. One fixture observation for the L1 only: tsukuroi's captured header
   `must-revalidate, stale-while-revalidate=60, stale-if-error=300` is a usable real-world case.

3. **In-lane note (outside sibling scope):** the freeze's "grep printed nothing" holds only for `scripts/`
   and `corpus/`. kake `.ufo/waves/round-86/w1/ScribeKnowledge/rfc7234-contrast.txt:1840-1841` maps
   stale-if-error to RFC 5861 §4 and SWR to §3, which agrees with `stale-contract.md`.

4. **Axis quote (fleet `AXES.md`, fleet HEAD 7687441822b3c682766a9f80ec2c6a49ed10d245):** located.
   Lines 62-64 ("Rows enter only through a round that demonstrates the capability running; a capability
   without a passing demonstration in the round report is pre-claiming and does not enter the table."),
   line 80 (the SCORECARD contract row for `capabilities`), heading at line 57.

## Commands run (rc observed)

- Lane HEADs: `git -C <lane> rev-parse HEAD` for 20 sibling lanes plus kake `master` and fleet HEAD; all rc 0.
- Surface (a): `grep -rIlE 'capabilities_added|^## Capabilities' … --include=*.py,*.md,*.sh,*.mjs,*.json`; per-lane tally; rc 0.
- Surface (b): `grep -rIlE 'RFC ?5861|rfc5861|stale-while-revalidate|stale-if-error' …` per-lane tally; rc 0.
- Line-level cites: `grep -nE …` and `sed -n` on the named files; rc 0 for each (exit codes of the
  `grep -nE` runs were 0; the empty kake-outside-`.ufo` grep printed no lines, grep rc 1 by definition).
- `read` of `AXES.md:55-83`: rc 0.

## Tooling

No installs. No upgrades. No host config changes. No tool outside the existing shell and read tools.

## Scratch and cleanup

No scratch fixtures were created. The seat directory was created at
`/fast/scratch/hyaku/kake-r98/ConnectorScope/` and removed before yield.

## Verdict

CONNECTOR hits_capcal=2 hits_5861=7 axes_quote=located
