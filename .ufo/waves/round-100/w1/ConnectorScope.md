# ConnectorScope — round 100 sibling-overlap report

Full table, commands and HEADs: `.ufo/waves/round-100/w1/ConnectorScope/overlap.md`.
Scope: `/home/vgpnk/Projects/shokunin/*-shokunin`, kake skipped; read-only (`git ls-files`, `git grep`, `git show`, `git rev-parse HEAD`, `sha256sum`, all rc 0).

## Hits by surface

C1 duplicate/shadow rows (10 hits): tsukuroi `tools/check-registry-coverage.py` (@64f45b79, REGISTRY-ROW-DUPLICATE); mori `tools/mori-gate-registry.py` (@7765969c, `duplicate=` counter); tameshi `tools/registry-check.py` (@f256302b, exit-vs-expect and superseded rows); kaidoku `tools/round-86/gate-registry.py` (@0b518f56, declared-vs-observed exit map); kaidoku `tools/round-100/registry-selftest-truth.py` (@0b518f56, same round label and marker, name collision only); tabi `scripts/check-instrument-registry-r68.mjs` (@58d84eda, duplicate-row); kotoba `verifiers/check_gate_registry.py` (@673d1e2e, duplicate-row fixture); kumitate `scripts/source-dupes.mjs` (@814068f0, pinned duplicate groups); kama `tools/gate-registry-check.py` (@9b4c7af1, verdict-cell presence); kotodama `tools/check-gate-registry.py` (@db88f107, coverage, citable).

C1 exit probes (4 hits): kumitate unknown-flag probes asserting exit 64 across seven scripts (@814068f0); kama `--no-such-flag` probes (@9b4c7af1); mori `check_cli … exit 2` and `--no-such-option` (@7765969c); kotodama `--bogus` usage battery (@db88f107).

C2 grounds (7 hits): no sibling lane parses Cache-Control directives. Citable: mori RFC 9111 pin `corpus/evidence/sources-r79/rfc9111.txt` (@7765969c), sha256 `aeb52adb…` byte-identical to kake's round-99 copy; mori anchor receipts `.ufo/waves/round-79/evidence/anchor-rfc9111-r79.txt`; three RFC 9110 copies, sha256 `21c1cdce…` byte-identical to kake's round-100 copy (chousa @378fda82, tabi @58d84eda, mori @7765969c); kama captured `Cache-Control: must-revalidate,no-cache,no-store` (@9b4c7af1); kagi raw headers (@f5977284). Overlap: tabi `corpus/knowledge/network-evidence-rung.md` D7 (@58d84eda), wire 304 vs effective client status.

Pointer note: in the pinned RFC 9110 copy, the Whitespace definition is §5.6.3 (OWS defined at line 1521); §5.5 is Field Values and uses OWS. Cite §5.6.3 for the whitespace definition.

## Contradictions

None found. The tabi run5 "no-cache did not force revalidation" note is recorded as a tension to check, not a contradiction ([INFERENCE]: the stored entries predate the no-cache response).

## Technique for c100_registry.py

Superseded rows stay executable and must resolve to a live active row: `tameshi-shokunin/tools/registry-check.py` lines 30-38 (superseded rows run, counted as `superseded=K`, excluded from N/M) and 277-297 (`superseded_by` must name an existing `status == active` row). Apply to the fenced `## Round 100 — superseded registry rows` block: each fenced row's tool path must resolve to exactly one active row, else fail with a `superseded-orphan` finding.

## Counts

hits=21 overlaps=14 contradictions=0 techniques=1 (citable=7; the 14 overlaps are rows 1-9, 11-14, 19 in overlap.md).

## Observed, outside scope

The kake lane tree has uncommitted changes (`M .ufo/waves/round-100/make_spec_w1.py`, `?? .ufo/waves/round-100/assimilation/`) at the time of the scan. Not touched.

CONNECTOR hits=21 overlaps=14 contradictions=0 techniques=1
