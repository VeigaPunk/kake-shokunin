# r27 W2 — AuditNoHarm (freshness / no-harm lane)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate,
`tree 7a20eeaef8431d1d8a65aebf29e62e26207d8739`, index clean).
Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Method: read-only Git blobs (`cat-file`/`ls-tree`) only. **No old gate, counter,
fixture or selftest was executed.** No source edit, no commit, no worktree write
outside this report. No network. No tool install.

## Attacked items and independent expectations (declared before each check)

| # | Attack | Expected result before running | Actual |
|---|---|---|---|
| A1 | 26 baseline knowledge files: is every base byte string still a byte-prefix of the candidate blob? | 26/26 prefix=True, 0 file missing, 0 renamed | **26/26 prefix=True**; path sets base==declarations==candidate (26 each); missing=0, extra=0 |
| A2 | Unauthorized deletion anywhere in tree | 0 deletions base→candidate | **0 deletions** (1295 base paths → 1568 candidate; +273 added, 0 removed, 0 renamed) |
| A3 | In-place rewrite inside the 4 amended knowledge files | append-only (0 removed lines) | **0 removed lines in all 4**; single EOF hunk each |
| A4 | Registered older scripts mutated | 7 pre-existing scripts byte-identical, 0 changed | **7/7 byte-identical**, 0 changed; 120 added (118 fixtures + `citing_set.py` + `citing_set_selftest.py`) |
| A5 | Source pins rewritten | `freshness-pins.json` + `freshness-sidecar.json` byte-identical | **both byte-identical** (2db3d777…, b09849f0…) |
| A6 | r26 wave/receipt/contract/ledger files rewritten | 279 r26 paths, identical tree digest | **279/279 identical**; tree digest `58e215f56eecf1d0b48b3fee…` on both revisions |
| A7 | Older wave trees (r20–r25) rewritten | 0 changed / 0 missing in each | **0 changed, 0 missing, 0 added** for round-20…25 (121/194/212/218/124) and `.ufo/round-20` (63) |
| A8 | Frozen oracle targets rewritten | contract/c2-oracle/c1-before/frozen-expected identical to declarations | **all 4 identical** to `be375d9` (6d2d7f51…, 1d038205…, af55d0a4…, 628b7a05…) |
| A9 | r26 ledger/population copied into r27 frozen/ | byte-equal copies | `frozen/ledger.json` == r26 `statements.json` (c2026376…); `frozen/population.json` == r26 `population.json` (16330e1e…) |
| A10 | frozen/expected.json pins still describe base bytes | all 28 pins match the frozen copies | **28/28 pins match**; the 26 corpus pins match the base blobs (the 4 amended candidate blobs differ from the pin by design — pin is the frozen base input) |
| A11 | Original counter bytes still at declarations | `count_c1.py`=a1e46d19…, `c2_count.py`=93f39b0f… at `be375d9` | **both match**; candidate `c2_count.py`=913a797f… (matches correction file); candidate `count_c1.py`=8d4c22ef… (post-strict-enforcement `9ba102d` f2632131…, plus carry-errata integration) |
| A12 | Wave files invented outside authorized scope | additions only under `.ufo/waves/round-27`, `scripts/`, `corpus/lessons` | **exactly**: 152 r27-wave, 120 scripts, 1 `corpus/lessons/round-27.md`; 0 touches to `fleet/`, MANIFEST, or domain sources |
| A13 | manifest `frozen-candidate.json` sourceFiles vs candidate blobs/worktree | 214/214 hash-equal, 0 absent | **214/214 match** at candidate and in the worktree; 0 mismatch |
| A14 | STALE correction markers land in the citing file | `[r27-recheck S0NN STALE]` present for all 3 STALE pairs | **3/3 present** (S004/ghp-served-set, S005/sitemap-orphan-audit, S005/static-canonical-preflight) |
| A15 | Ledger arithmetic: 58 obligations | r26 41 ∪ r27 18 − overlap 1 = 58 | **exactly 58**; overlap = {(S004, ghp-served-set.md)}; complete-ledger ≡ union (0 diff each way) |
| A16 | Registry `used-by` routing never loses an entry | monotone (no lost used-by) | **0 lost**; 6 rows gained (S001–S006) |
| A17 | r20 replay-proof input pins vs candidate | stale pins pre-existing at base, not a r27 regression | 37/43 stale **at base already**; 4 changed since base (SKILL.md, corpus/QUALITY.md, corpus/README.md, sitemap-orphan-audit.md) — all append-only/registry edits, not a pin regression |

## Exact hashes

Knowledge files amended (base → candidate bytes, base SHA→cand SHA, prefix):
- `ghp-custom-domain.md` 4475→5101 B, 65dd561af5cc…→c73d3a12d4e7…
- `ghp-served-set.md` 8001→10080 B, 405b85875268…→35fedf84c3ea…
- `sitemap-orphan-audit.md` 13065→14606 B, 553ad1006e9e…→b0b9ee01c1ab…
- `static-canonical-preflight.md` 19573→23662 B, 833b28f26fa7…→40ebd1dabc12…
Remaining 22 knowledge files byte-identical. Tree digest of the 26 paths:
base `b9a67bf09f81b8aa…` → candidate `7b1b21b22d3e138c…` (difference is exactly
the 4 appends).

## Exceptions found (both minor; neither is a tracked-byte mutation)

**E1 — `corpus/SOURCES.md` is not prefix-preserving (in-place row-cell edit).**
`corpus/SOURCES.md` was modified by rewriting the `used-by` cell of rows S001–S006
in place; base bytes are therefore NOT a prefix of the candidate file
(base 29500 B `5001eadee20c…` → candidate 32041 B `c92807d7558b…`). The edit is
monotone (0 used-by entries lost) and every other column of all 35 rows
(id/source/kind/tier/scope/anchor/teaches/status/opened/recheck) is byte-equal to
base; 4 prose lines are appended. This file is outside the 26 knowledge files and
outside the registered pin set, so it does not breach A1/A5 — but if the wave's
no-harm rule was intended to cover the registry file byte-wise too, this is the
one exception and it should be disclosed, not silently counted as append-only.
Noted for the author: `corpus/SOURCES.md` states "original row cells are not
rewritten" while 6 cells were in fact rewritten.

**E2 — SOURCES.md `used-by` routing is still incomplete (24 gaps), including the
newly discovered pair.** Literal+range citing-set scan of the 26 knowledge files:
46 routing gaps at base → **24 at candidate** (the 6 grouped rows repaired), but
still open: S007/publish-channels, S008×4 (crawl-scope-per-host, ghp-custom-domain,
ghp-etag-anatomy, static-canonical-preflight), **S013/ghp-served-set.md — the
pair this round itself discovered and adjudicated — whose `used-by` was never
extended**, S019×16, S022/static-canonical-preflight, S023/static-canonical-preflight.
`used-by` is routing only (SKILL.md round-27 note says it is never the reviewed
denominator), so this does not affect the C1/C2 denominators; it is an
honesty/completeness gap in the registry routing, largest at S019 (16 files).

**E3 — stray untracked artifact inside the r26 wave directory.** During r27 a
byte-cache was written at `.ufo/waves/round-26/__pycache__/fetch_sources.cpython-314.pyc`
(mtime 2026-10-21 19:01:14, 5526 B, sha 991f94ed931b…), alongside a 17:04
`source_text.cpython-314.pyc`. Tracked r26 bytes are untouched (A6 holds; the
path is untracked and absent from the candidate tree). It is cache pollution in a
directory the wave froze, and its 19:01 timestamp shows r26 `fetch_sources.py`
was imported during r27 — worth an explicit note since "r26 unchanged" reads
stronger than the working-tree state supports. `.ufo/waves/round-27/__pycache__/count_c1.cpython-314.pyc`
is likewise present and **stale** (records source size 5083 vs actual 9801).

## Residual risk / verification gaps

- Semantic support of the 15 HOLD verdicts, the 7 carried-UNVERIFIABLE units and
  the 3-pairs/7-unit carry erratum are not re-proven here (out of this lane; C1
  remains UNPROVABLE per frozen clause 10/13 — 55/58 decided, not green).
- Pair presence ≠ semantic support and ≠ HTTP authenticity; A14 only proves the
  STALE marker is present in the cited file, not that the correction is correct.
- Raw 313 is a mixed field sum; this audit did not attempt to re-derive it.
- Live HTML provenance unprovable from the filtered retained bytes (by design).
- No counter/gate was executed, so all "author measurement" values inside
  `frozen-candidate.json` (`authorMeasurements`) remain author-asserted and
  unverified by this seat; only their *inputs* (file hashes) were checked.
- E2's 24 gaps were computed with the same literal+range rule the counter uses;
  a different (row-aware) definition could shift the count.

**Verdict:** no-harm holds for every measured surface. 26/26 knowledge files are
byte-prefix preserved, 0 deletions tree-wide, 7/7 older scripts and both source-pin
files byte-identical, 279/279 r26 wave files byte-identical (identical tree
digest), all 4 frozen oracle targets identical to declarations, 214/214 manifest
hashes match, ledger arithmetic 41∪18−1=58 exact. Two disclosed exceptions
(E1 registry in-place cell rewrite; E2 24 residual routing gaps incl. the
round's own S013 pair) and one stray untracked r26 pycache (E3) are recorded
above with exact hashes; none is a tracked-byte mutation.
