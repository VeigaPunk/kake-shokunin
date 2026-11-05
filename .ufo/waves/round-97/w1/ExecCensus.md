# ExecCensus — frontier-step receipts (kake r97 w1)

Report trailer for seat ExecCensus. Full receipts: `w1/ExecCensus/census.md`; raw outputs in
`w1/ExecCensus/{census-now.txt,mirror-validate.txt}` and `w1/ExecCensus/assimilation/{reg-ids,staged-ids,collisions,guard-proof.txt}`.
Lane tip verified `9e27ce0b…eedf`; frozen digests c97_index.py / c97_reval.py / frozen/neg-lookup-table.py
all match `controls/instrument-sha256.txt` (sha256sum rc=0 ×3) before any work. No tool installed.

## Findings

1. **Census now (rc=0).** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
   → exit 0, 40 × W04 (pre-existing duplicate-URL class), zero E-class; W04 line set
   byte-identical to pre-freeze `controls/census-before.txt` (diff empty).
2. **Assimilation guard (§10 pipeline verbatim).** reg-ids=217 (S001…S480), staged-ids=129
   (S287…S415), collisions=8 (S312 S329 S367 S372 S373 S374 S390 S409) — same id set as the
   committed round-96 receipt; reg delta 216→217 is exactly S480 (not staged). Guard proof:
   a 2-space-indented `  | S002 |` scratch row still extracts and collides (nonempty
   collisions file) — indented rows cannot bypass the guard.
3. **Planned S481 append, scratch mirror.** Verbatim S479 row shape, id→S481, URL→
   `errata_search.php?rfc=9111`; census `--file` run → **exit 1**, fully attributed by a
   baseline (no-S481) delta run: baseline already carries 19 E11 findings (lane-root-relative
   used-by paths absent under a corpus-only mirror) + 40 W04; S481 adds exactly one E11 of
   that same class (it copies S479's used-by, which names `.ufo/waves/round-95/freeze.md`).
   No E03/E04/E01/E02 or any other finding for S481; W04 set unchanged; extractor rows
   217→218. At the real lane root every used-by path exists (finding 1's run is that
   context: exit 0), so appending this row shape to the real registry is expected to keep
   exit 0 with only the pre-existing W04 class.

## Routed observations (reporter only; nothing repaired)

- The §10 sample path writes to `…/round-97/assimilation`; this seat's bound write area is
  `…/round-97/w1/ExecCensus/assimilation` — receipts live there (spec prevails for seats).
- 8 staged-vs-registry collisions persist unchanged since r92: any `merge/kake` adoption
  still requires the §10 scratch renumber map before append.
- Environment: ConnectorScope-23's scratch wipe removed this seat's then-empty scratch tree;
  recreated before use, no receipt lost (disclosed in census.md §5).

Scratch root `/fast/scratch/hyaku/kake-r97/ExecCensus/` deleted before yield.

Verdict line (commands and rcs in census.md §1–§4):

EXEC-CENSUS census_rc=0 collisions=8 guard=ok mirror_rc=1
