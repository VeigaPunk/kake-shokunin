# round-19 re-census — §history suspend semantics repaired; selftest made hermetic

2026-10-14. Steered round 19. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kake*.md`.

## Landed change (one file)

`scripts/freshness-sweep.mjs`:

1. `pins.probeHistoryAbsent` now SUSPENDS **only the canonical** probe-history
   default when it is missing. An explicit `KAKE_PROBE_HISTORY` override that
   does not resolve stays fail-closed `exit 2`. The selftest rebind is gated on
   `KAKE_IN_SELFTEST=1` (set by the proof runner only), so an ambient
   `KAKE_SELFTEST_CANONICAL_HISTORY` cannot silence a real run.
2. `probeHistoryAbsent` joins the consumed-pin list, so it no longer renders
   under the "pins not evaluated" footer while simultaneously driving §history.
3. The selftest's hermetic resolve fixture no longer cites a live host project
   tree, and no longer writes persistent HOME state.

## Verdict lines (measured)

- `node scripts/freshness-sweep.mjs --selftest` → exit 0, **13/13 passed**
  (`e` region marks `B19,B1083,E1139,B1298,E1300,B1318,E1320`, 0 write sites
  outside the region).
- `node scripts/freshness-sweep.mjs --offline` → exit 0,
  `VERDICT: OK (exit 0, partial: offline)`; §history `SUSPENDED`
  (pin-declared), §armed `skipped(offline)`.
- `KAKE_PROBE_HISTORY=<missing>` → exit 2 (explicit bad override fails closed).
- No `$HOME/.kake-freshness-selftest-*` residue after the run (verified).

## Named debt (unchanged, correct)

Bare online `exit 1` stands: PQ-2 + PQ-14 ANOMALY (source repos gone) and
§history SUSPENDED. Do not re-pin to silence them. `~/Projects/ufo-fsd-alpha`
present; `origin-work` absent.

Stale live prose recorded, not rewritten in place: `SKILL.md:59`/`:111` still
name deleted webzites binaries; `freshness-sweep.md:43-53` copies pre-r18 pin
literals; `SCORECARD.md:20` says 14 `~/Projects` children where the receipt
measures 30 (P2b is informational by design).

## Independent audit erratum (appended 2026-10-14)

Independent audit: gates re-ran green (13/13, offline partial exit 0, explicit-bad exit 2, no HOME residue); identity/pathspec/record confirmed. Audit coverage finding: the selftest write-region opens on the line-19 header comment containing the BEGIN token, so a write planted as the first statement of a later function survives the confinement check (scratch mutant, not patched). Carried debt: PQ-2/PQ-14 + suspended history; stale webzites binaries; pre-r18 pin literals; SCORECARD 14-vs-30 children.
