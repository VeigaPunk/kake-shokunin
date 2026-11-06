# ReviewRegB — C1 review conjunct, seat B (round 100, kake)

Seat: ReviewRegB. Review only; no lane mutation; read-only git in the lane. Independent of seat A
(did not read `w1/ReviewRegA*`). Target revision for every judgment:
`e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f` (= lane `master` tip at review time, `git rev-parse master`).
Verdicts: `w1/ReviewRegB/verdicts.tsv` (8 lines). Receipts: `w1/ReviewRegB/probes-receipt.txt`,
`w1/ReviewRegB/fence-verbatim-receipt.txt`, `w1/ReviewRegB/counter-e84a187.txt`.

## Preconditions

- Frozen instrument digests verified before attacking:
  `cd .ufo/waves/round-100 && sha256sum -c controls/instrument-sha256.txt` — all entries OK, rc=0.
- All four pinned commits resolve as commits: base `3989618d`, instruments `d7b73d16`, freeze
  `69cdc1eb`, repair `e84a1871` (`git cat-file -t`, rc=0 each).
- Blob-exact extraction: `git show <rev>:<path>` into the seat scratch; every code/row line number
  below is a blob line number at the named revision.

## Per-unit verdicts (summary; full reasons in verdicts.tsv)

| # | Unit (Name cell) | Row | Unknown-flag rc (code + observed) | Verdict |
|---|------------------|-----|-----------------------------------|---------|
| 1 | `cache_key.py` | SKILL.md:1707 | 1 — no argparse, argv ignored, stdin path fails (cache_key.py:120-126); observed rc=1 | agree |
| 2 | `cache_key_conformance.py` | SKILL.md:1708 | 2 — argparse required-arg fault (cache_key_conformance.py:521-527,581); observed rc=2 | agree |
| 3 | `live_snapshot.py` | SKILL.md:1718 | 64 — SystemExit remap (live_snapshot.py:198-199); `1 not used` true: no return-1 path (:250,:252); observed rc=64 | agree |
| 4 | `response_snapshot.py` | SKILL.md:1721 | 64 — same remap (:228-229); `1 not used` true (:266,:268); observed rc=64 | agree |
| 5 | `robots_audit.py` | SKILL.md:1723 | 64 — manual argv guard, zero argparse references (:109-112,:656-660); audit 0/1/2 (:622-628); observed rc=64 | agree |
| 6 | `source_snapshot.py` | SKILL.md:1729 | 2 — argparse required-arg fault (:271-276,305); map names only 0/2, both true; observed rc=2 | agree |
| 7 | `scripts/x_robots_tag_audit.py (round-80 grammar)` | SKILL.md:1512 | 64 — Parser.error override (:443-448), missing --manifest (:461); audit exit 0/1 (:265), Fault 2 (:467); observed rc=64 | agree |
| 8 | fenced history block | SKILL.md:1748-1771 | n/a — 7 rows byte-identical to base at labelled lines; labels correct; no other live row invokes the seven (counter duplicated=0) | agree |

Empirical corroboration: every map names exactly the code its tool returns for `--zz-bogus-r100`
(observed on blob-exact extractions; counter's sandboxed probes agree, probe_mismatch=0).
Self-test cells exercised: x_robots `--selftest` → `selftest: 33/33 passed`, rc=0 (matches the cell
exactly; the superseded row's 26/26 is history, correctly not claimed here);
`scripts/robots_audit_selftest.py` → passed=204/204, verdict clean, rc=0 (10.7 s), matching row
1723's self-test cell. "no self-test (no `--selftest` mode)" cells for cache_key.py,
cache_key_conformance.py, live_snapshot.py, response_snapshot.py, source_snapshot.py: grep shows 0
`selftest` mentions in each tool — true; cache_key_conformance's reference self-check runs inside
main() (cache_key_conformance.py:521), as its cell describes.

## Fenced history block (unit 8)

- Heading SKILL.md:1748, fence 1756-1771, exactly 7 `[SKILL.md:<line> at 3989618d; tool …; current
  row Name …]` label lines (1757,1759,1761,1763,1765,1767,1769), each followed by its removed row.
- Verbatim: `cmp` byte-identical for all 7 pairs against round base `3989618d` at the labelled
  lines (494, 1079, 1104, 1370, 1505, 1621, 1624) — byte counts 551/352/609/1040/707/434/639.
- Labels: all 7 "current row Name" cells correct (see fence-verbatim-receipt.txt).
- The repair changed no kept cell: all 7 kept rows byte-identical between base and e84a187
  (base:cur = 1714:1707, 1715:1708, 1725:1718, 1728:1721, 1730:1723, 1736:1729, 1517:1512).
- No other live registry row invokes one of the seven tools: `c100_registry.py --revision e84a187`
  prints `duplicated=0` exit 0. The three near-misses checked by hand:
  - SKILL.md:1617 (`c89 key capability`): command position invokes `.ufo/waves/round-89/c89_key.py`;
    `scripts/cache_key.py` appears only as the `--candidate` argument value. It is a different
    instrument's row, not a second answer for cache_key.py. (c89_key.py exists at e84a187.)
  - SKILL.md:1489 (`scripts/meta_robots_audit.py`): suffix-similar name only; entry command invokes
    meta_robots_audit.py.
  - SKILL.md:1724 (`robots_audit_selftest.py`): invokes the selftest runner; robots_audit.py appears
    in Name/kind prose and as the runner's tool under test.
- Counter reproduction (receipt counter-e84a187.txt): `python3 -B .ufo/waves/round-100/
  c100_registry.py --root <lane> --revision e84a187… --work <scratch>` →
  `tools=55 rows=146 listed=55 unlisted=0 dangling=0 duplicated=0 probe_mismatch=0 exec_fail=0
  mismatches=0 met=true`, exit 0 — the freeze's target line exactly.

## Findings by severity

No High or Medium findings; no live `disagree`. Informational notes (routed, not repaired):

1. **Note — source_snapshot write-scope understates receipts.json.** SKILL.md:1729 scope cell says
   "writes the manifest and body files it names"; the tool also always writes
   `<manifest dir>/receipts.json` (source_snapshot.py:297-301). Under-statement, not a falsehood
   (it does write the manifest and bodies; the superseded row it replaced disclosed the receipts
   file at fence line 1760). Verdict-map calibration is unaffected.
2. **Note — cache_key_conformance scratch fallback.** SKILL.md:1708 scope cell "per-case scratch
   under `--work` only"; code falls back to `TMPDIR`/system temp when `--work` is omitted
   (cache_key_conformance.py:530). The registered entry command always passes `--work`, so the
   cell holds for registered usage.
3. **Note — cache_key.py ignores argv.** No argparse; an unknown flag never faults and the probe
   lands on the stdin-failure path (rc=1). The map already names 1 for the refusal, so D2 and the
   row are correct; any future re-write of this map must keep naming 1, not a parser code.
4. **Note — declared counter limit exercised, covered.** live_snapshot/response_snapshot maps name
   `1 not used` (a code the tool never returns) — truthful declarations, and precisely the class
   the freeze's `everycode` control showed D2 cannot catch. This review checked every named code in
   all 7 kept maps against reachable return/sys.exit/parser paths: no named code is false, no
   reachable designed code is misdescribed. Interpreter-default exit 1 on an uncaught exception
   exists for every Python tool here and is not a designed verdict path; no kept row claims
   otherwise.

## Tooling record

No tools installed or upgraded (operator authorization not exercised): used system `python3`,
`git`, `cmp`, `grep` only. Scratch root `/fast/scratch/hyaku/kake-r100/ReviewRegB/` (deleted after
receipts were copied into `w1/ReviewRegB/`); lane touched read-only (`rev-parse`, `cat-file`,
`ls-tree`, `show`, `status --porcelain`); no fixture repo or clone needed; no host config touched.

## Verdict

8 units judged, all `agree`. `REVIEWREG-B agree=8 disagree=0 of 8`
