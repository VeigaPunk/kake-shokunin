# ReviewC1 — scoped findings (round 93, w1)

VERDICT: C1 counter falsified — `met=true` reachable without the predicate's work by six
fixture routes; two have live instances at the base. Full attack log with exact commands,
exit codes and per-scenario receipts: `.ufo/waves/round-93/w1/ReviewC1/Attack.md`
(receipts beside it; fixture driver `ReviewC1/receipts/drive.py`, live checks
`ReviewC1/receipts/live.py`). Counter under test: frozen blob
`bb8012f:.ufo/waves/round-93/c93_selfassess.py`, sha256 `4e25b72e…bb7390f`.

## What holds (do-not-touch evidence)

- Base reading reproduces exactly: `mismatches=20 E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok
  met=false`, exit 1 (`ReviewC1/receipts/base-rerun.txt`).
- Canonical planted defects of all five classes are detected 1/1 each
  (`receipts/01-planted-five.txt`); a full-size clean lane reads `met=true` exit 0
  (`receipts/00-sanity-clean.txt`).
- File-level deletion is caught by the pins: lesson deleted → `lessons=86 pins=short`
  (`02-A2a`), criteria section deleted → `criteria=38 pins=short` (`04-A2d`), entry
  deleted → `entries=79 pins=short` (`05-A2e`); missing lesson pointers fire E2 (`07-A4`
  part 1); unevaluable input exits 2 (`19-fail-closed`).

## Falsifications (fixture evidence; live status in brackets)

1. **Shadow module beside frozen bytes (F1, high).** The documented command
   `python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision <REV>` puts the
   counter's own directory first on `sys.path`; an attacker-controlled `subprocess.py`
   there fabricates every `ls-tree`/`show` and the untouched frozen bytes read
   `met=true` exit 0 at a genuinely defective revision (`18-A1b`; disk truth shown in
   the same receipt via `git show` at the same sha). `-B` does not help. [live-capable
   vector; not observed run]
2. **Canned wrapper at the documented path (F2, high).** A Python file at the counter's
   path prints a frozen-format `met=true` line with the real revision, audits nothing,
   exits 0 (`17-A1a`). No self-digest pins the counter bytes in its own output; defense
   is procedural (freeze byte-identity + clean tree). [protocol]
3. **Pins are cardinality-only (F3, high).** A defective counted QUALITY section escapes
   the population (heading loses "criteri", mention moved past char 400) while a junk
   conformant section refills `criteria=39`; `met=true` with the bad pointer still in
   the file (`10-B-E2`). Same one-out-one-in move works for SKILL rows. [structural;
   the 9 uncounted Round sections at base are the ready-made home — see live list]
4. **Mistakes surface is unpinned (F4, high).** Deleting a defective `## Mistakes`
   section (lesson and `## Gate` kept) silences E4 with no pin change: `met=true`
   (`03-A2b`). All 4 live E4 defects at the base are cheaply silenceable this way.
   [live exploitability over the base's own 4 defects]
5. **E3 resolution is token-level, not row-level (F5, medium).** An id cited by an entry
   resolves if the `S\d{3,}` token appears anywhere in SOURCES.md (prose footer
   suffices) (`12-B-E3b`), and 1–2-digit ids are invisible to `ID_RE` (`13-B-E3c`).
   [no live instance: 207/207 tokens are row ids]
6. **E5 admits directories and empty files (F6, medium).** `git show <rev>:<dir>` exits
   0 (tree listing), so a row naming a directory passes; empty blobs pass. Fixture
   `08-A5`. [live: 12 SKILL rows name trees today, incl. `scripts/fixtures`,
   `.ufo/waves/round-51/`, `.ufo/waves/round-80/cases` — all silent]
7. **E4 checks only the first `## Mistakes` section and one gap per lesson (F7,
   medium).** Split table in a second `## Mistakes` section reads `E4=0` (`14-B-E4`);
   two gaps report one (`15-B-E4b`). [no live instance]
8. **Letter gaps (F8, low).** `## Gate ` with trailing space passes E1 though the
   predicate says "exactly" (`09-B-E1`); unbackticked path mentions in rows are never
   resolved (`16-B-E5`). [no live misses; 5 live non-exact Gate headings all coexist
   with an exact one]

## Predicate-level vacuities (not counter defects; the frozen sentence admits them)

Bare `## Gate` heading with no content (`06-A3a`), pointer to an existing lesson whose
content is only a bare heading (`07-A4` part 2), and an id-free `source:` line
(`11-B-E3a`) all read `met=true`. If the claim means "grounds something", that must be
frozen into the predicate sentence before scoring, not repaired after.

## Successor bindings (for the routed list)

Run the counter from a directory holding only its digest-verified blob (or add
`-P`/`-I`); print the counter blob sha256 in receipt line 1; pin surfaces by identity
(per-file digests or a section census), not by count; pin the Mistakes tables; scan
SOURCES.md row ids only (and widen `ID_RE` to `S\d+`); resolve trees/empty blobs in E5;
check every `## Mistakes` section and every gap; and decide whether Gate/QUALITY
vacuity is in or out of the claim — in the sentence, before the wave.

## Limits

Fixtures are synthetic; the carrier does not exist yet (no carrier-side run). No live
instances today for findings 5, 7, 8. First A1a attempt (shell wrapper under
`python3 -B`) failed and is superseded in `drive.py` — driver defect, not a counter
property. No tools installed; no network GETs; scratch deleted after receipts were
copied. I did not edit the frozen instruments, the predicate, or any lane file outside
`w1/ReviewC1/`.
