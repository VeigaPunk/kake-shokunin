# ConnectorOverlap — sibling-overlap census for the round-43 instruments and rows

Seat `kake-r43-w1-ConnectorOverlap`, wave 1, milestone r43-verify. Axes: operability,
freshness. Read-only over sibling lanes; no lane file other than this report was written;
no tools installed or updated (nothing beyond present grep/glob/read was needed; host
pacman remains paused per the 2026-10-20 ruling).

## Verdict line

CONFORMANT — no sibling lane pre-holds any round-43 instrument or row: the c39→c43
counter lineage (`c4*_count*.py`), `registry_count_check.py`, and the Mistake-5 generator
classes (6+-digit ports, case-fold pairs under segment-cased sitemapUrls, tail-defective
shared-prefix pairs, repeated-host blocks, the localhost/example.invalid/sitemaps.invalid/
test.invalid common-host table) appear in no sibling; S129/S130 name sibling paths that
exist and whose quoted spans locate; no sibling artifact references `c43_count_v4` or any
seat score predating freeze `b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee`.

## Overlap table (lane, artifact, relation to kake r43)

| Lane | Artifact | Relation to kake r43 |
|---|---|---|
| tameshi | `.ufo/waves/round-33/w1/CtlDoNothing.md` (§Verdict ¶2, `:11`; companion `ReviewFreeze.md`, CONFORMANT freeze audit) | S129 origin. Method import: pre-data control classes (do-nothing) scored against a frozen counter (`kill=0/18 accept=8/8 predicate_pass=False`), plus byte-level freeze conformance review — the method behind kake r43's kill rules and freeze receipts. Quote verified verbatim. |
| kama | `corpus/knowledge/self-assessment-at-writing.md` (`:7`) | S130 origin. Quote "records a calibration error present when the statement was written" verified verbatim; grounds kake's registry-arithmetic correction (Mistake 7). |
| kama | `corpus/SOURCES.md` rows S174–S177 (`:186-189`), `corpus/README.md:440`, `corpus/lessons/round-29.md:105-146` | Only sibling registry quoting the S130 document — as its own origin rows (used-by `self-assessment-at-writing.md`), not an import of kake's S130 row. No sibling quotes tameshi's `round-33/w1/CtlDoNothing.md`/`ReviewFreeze.md`. |
| kama | `.ufo/waves/round-23/falsify/advice/SentinelDoSW2.md:32` | Closest Mistake-5 class prior art in the fleet: 12,000 long shared-prefix HTTPS URLs as an adversarial corpus (memory-exhaustion against kama's auditor). Same class *family* (shared-prefix repetition), different instrument: bulk corpus, not pair/tail-defect generation, no ports/case-fold/host tables. |
| mori | round-32 C0 control wave (fleet report `.ufo/reports/round-32/mori.md:16-17`; counter `count-c1.py`, mori `.ufo/waves/round-32/`) | Same control taxonomy (do-nothing at base and freeze, junk table, forged receipt) kake r43 uses as kill-rule controls; mori's counter claim shape is registry-rows (`rows_ok`), not tool-equality+CPU. |
| kaidoku, kama, mori | `count-c1.py`/`count-c2.py`(-a1) counters (e.g. kama `.ufo/waves/round-29/count-c1.py`; kaidoku `.ufo/waves/round-22..24/tools/`; mori `.ufo/waves/round-31..36/`) | Name-shape overlap only (`count-c1.py`). Claim shapes are completeness/accounting/registered-counted/self-assessment rows; none is "exit code and stdout bytes equal a reference tool + median CPU ratio ≤ 2.0". |
| chousa | `corpus/knowledge/gate-baseline-r8.md:24-84`, `corpus/evidence/README.md:583`, `corpus/lessons/2026-10-16-gate-behavioral-baseline.md:6-7` | Precedent for the S129/S130 move itself: sibling-lane method import (mori's drift-pin) with named sibling repo paths — kake's adjacency imports follow this established fleet pattern. |
| chousa | research-gate fixtures using `example.invalid`/`test.invalid` (e.g. `.ufo/waves/round-32/controls/L1-design-v2/c2-dup-control-gate.sh:3624,3885`; round-31 mutants) | Same reserved-TLD tokens, different role: exempt/blocked remote-URL chain fixtures. Not host-class repetition generators; no `sitemaps.invalid` use anywhere outside kake. |
| kagi | `.ufo/waves/round-28/sandboxes/Conn{Kasegi,Kengaku,Tabi,Tsukuroi,SourcesCensus}/` | Prior connector-over-siblings instrument role in the fleet (sandboxed sibling wave trees under probe), pre-dating this census seat. |
| tsukuroi | `.ufo/waves/round-34/w1/ExecCensusCounterV5/score-census-handoff-v5.py:254-258` | Method kinship, opposite direction: os.urandom entries chosen so *no* shared prefix marks a planted distractor — the same anti-keying concern as kake v3/v4's random tokens defeating value-caching. |

## Census detail (per assignment item)

1. **Counters/fixtures with the c43_count_v4 claim shape.** Lane-scoped content search
   `c4[0-9]+_count|registry_count_check` over every sibling `.ufo/waves` and `corpus`:
   0 matches (audio has no `.ufo/`; its evidence lives in `corpus/live`, also 0).
   Claim-shape search `RATIO_LIMIT|median CPU|CPU time on each|times the round-4` over
   all sibling `.ufo/waves`: 0 matches. The equality+CPU-ratio counter lineage is
   kake-only back to round 39; the only fleet-level reference to the family outside the
   lane is the hyaku closure archive `/home/vgpnk/Projects/shokunin/.ufo` (1 file:
   `waves/hyaku/frozen/.../MANIFEST.json`, an archive of kake r42's `c42_count_v3`).
   `registry_count_check.py` is likewise kake-only.
2. **Registry rows quoting S129/S130 sources.** Sibling corpus search for
   `round-33/w1/CtlDoNothing|round-33/w1/ReviewFreeze|self-assessment-at-writing`:
   matches only in kama's own corpus (origin rows above). No sibling imports either
   source; kake's S129/S130 are novel adjacency rows, and both quoted spans locate
   verbatim in the named sibling files.
3. **Mistake-5-style classes.** Sibling-wide search for
   `shared.prefix|repeated.host|common.host|6+-digit|randint((100000|999999)` plus
   `sitemaps.invalid|example.invalid|test.invalid`: no generator for any kake r43 class.
   Residual "shared prefix" hits are upstream imports or unrelated idioms: kama
   llama.cpp sources (`server-context.cpp:3702+`, imported upstream code), kagi's
   captured PEP 440 text (`.ufo/waves/round-27/captures/S043.body:918`), lore's
   append-only byte-prefix registry checks (`.ufo/waves/round-96/seats/V53-byte-prefix-2.md:67-78`),
   kengaku's list-diff severity metric (`corpus/evidence/round12-ladder/probe_r12.py:360`),
   mado kitty/xdg source reading, souji exemption-prefix fix, tabi TMPDIR churn note.
   `sitemaps.invalid`: zero sibling occurrences. No `6+-digit`/`randint(100000|999999)`
   port generator exists outside kake.

## Novel ground (as valuable as overlap)

Round 43's specific instruments are fleet-novel: the equality+CPU-ratio predicate and its
c39→c43 counter lineage, `registry_count_check.py` (able-to-fail registry-arithmetic
checker), the 6+-digit-port class, case-fold pairs under segment-cased `sitemapUrl`,
tail-defective shared-prefix pairs in both orders, repeated-host blocks, and the
common-host table including `sitemaps.invalid`. The nearest fleet relatives are kama r23's
shared-prefix URL corpus (bulk memory attack), tameshi r33's frozen-counter control
method (imported as S129), and tsukuroi r34's anti-shared-prefix randomization.

## Evidence and commands (all read-only; exit semantics noted)

- Content searches above were run with the session grep tool over explicit absolute
  sibling paths (gitignore-respecting). Zero-match searches ⇒ exit-1 semantics ("No
  matches found"); timed-out whole-lane searches were re-scoped per lane to `.ufo/waves`
  and `corpus` and then completed; lanes without `.ufo/waves` (audio, game-dev-2d,
  game-dev-3d) were reported as missing paths by the tool and covered via their
  `corpus` trees.
- First-hand reads: `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md:1-43`,
  `.../ReviewFreeze.md:1-28`, `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md:7`,
  kake `c43_count_v4.py:1-83` (PREDICATE at `:78-80`), kake `corpus/lessons/round-43.md`
  (S129/S130 rows `:16-17`, registry 128→130 `:19-20`), kake `corpus/SOURCES.md:136-138`.
- Coverage caveat: glob over the parent tree is gitignore-blinded (lanes are nested
  repos), so file enumeration was content-search-based as above; no lane-internal
  gitignored scratch was enumerated.

No tool installs/updates. No network use. No lane or sibling mutation. No scoring runs
(this seat's item is the census; nothing here exercises or scores the frozen counter).
