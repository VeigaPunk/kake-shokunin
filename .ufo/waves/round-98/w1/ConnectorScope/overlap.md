# ConnectorScope — sibling-overlap scan for kake round 98 (read-only)

Seat: ConnectorScope (leaf, no dispatch). Lane: kake (`LANE`). Scope: sibling lanes only.
Mutations: none. Instruments: none executed. Frozen digests: not re-verified (not in seat scope).

## 0. Method and definitions

- Lane set: the 20 sibling `*-shokunin` directories under `/home/vgpnk/Projects/shokunin`
  (revenger, kaidoku, kengaku, kasegi, kagi, tabi, kotoba, kama, kumitate, kotodama, mado,
  tameshi, mori, tsukuroi, chousa, souji, lore, game-dev-2d, game-dev-3d, audio). kake itself is
  excluded from the sibling counts. `kumitate-shokinin/` (typo directory, contains a nested
  `kumitate-shokunin/`) was NOT scanned; it does not match the `*-shokunin` set.
- The `_glob` and first `_grep` over `*-shokunin` returned nothing (the glob did not expand in the
  tool); all sweeps below were re-run with explicit shell expansion.
- Surface (a) sweep: `grep -rIlE 'capabilities_added|^## Capabilities'` over `*.py *.md *.sh *.mjs *.json`,
  excluding `.git .jj .ruff_cache __pycache__`. Instrument-name find over the 20 lanes.
- Surface (b) sweep: `grep -rIlE 'RFC ?5861|rfc5861|stale-while-revalidate|stale-if-error'` over all
  lanes, excluding `.git .jj .ruff_cache __pycache__`. Bare `5861` was rejected as a pattern: it
  matches inside sha256 hex digests (e.g. revenger `.ufo/waves/round-62/preservation/manifest.json`).
- `hits_capcal` = distinct sibling lane-instrument families whose oracle reads MANIFEST
  `capabilities_added` and compares a SCORECARD capability table (strict). Adjacent instruments
  that compare a capability table with a different oracle are listed separately and not counted.
- `hits_5861` = sibling lanes with at least one token-level hit. Normative ground (RFC 5861 text or
  a retained RFC 5861 copy) is counted separately and is 0.

## 1. Lane HEADs (`git -C <lane> rev-parse HEAD`, read-only)

| lane | HEAD |
|---|---|
| kake (master, not sibling) | 7838981e4e40280176085e8aa1f6827eb7133a69 |
| fleet root | 7687441822b3c682766a9f80ec2c6a49ed10d245 |
| revenger | 61e27feb4e8099af7f9bf41fbf69e223354f691e |
| kaidoku | c19d57cd2e65a036478b9e78f6c5397dedfb2bcb |
| kengaku | 997a6fe5fbb4a4af9f38e436bccd8f604da1d746 |
| kasegi | d16d2124fd5262f5a8088aa598f1e628f897d3ab |
| kagi | 072bb0bc1860fcc33418b659cec0dd40d5c0f944 |
| tabi | 58d84eda992ffc11d77d76a2c1019bfe061f9241 |
| kotoba | ab151b17f08e8910efd5ce0d243a791b21365711 |
| kama | 9b4c7af16fdd4bba9e4815f4615f4b003f340747 |
| kumitate | 77ebfe3794214fe06d8047f8698ffe0252f64461 |
| kotodama | 063f70c9ab9aed5297741773292ded6d713d537a |
| mado | 24ba2a9ddac21c1211579231e6ee1d98963f9988 |
| tameshi | f256302b394ae3253df014fe1131e2c20e2c16b6 |
| mori | 73308ff6e5c933f53498e9501ef95917b0ef7171 |
| tsukuroi | 64f45b790f2dbbf63b9b343c47810118a79f7a35 |
| chousa | 378fda82dc2cbcc555a0565052cc408121813cef |
| souji | e063a2fcb3f5f3fb8fb19d2ae1592b1f22e6a333 |
| lore | 0f044aa7c7e4e17cfd5b6278179709b60db45d61 |
| game-dev-2d | 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3 |
| game-dev-3d | 39ca3973c7865456d97fae18033f3f460c6cf8c1 |
| audio | f9da7ee97e0ba95da1803c2afe9c616c519bae18 |

## 2. Surface (a): capability table vs MANIFEST closure records

### 2.1 Strict hits (`hits_capcal` = 2)

| # | lane @ HEAD | path (line) | what it compares | relation to kake r98 |
|---|---|---|---|---|
| 1 | kaidoku @ c19d57cd | `tools/round-32/c2-capability-calibration.py`, `-v2.py`, `-v3.py` | forward and reverse match of SCORECARD `## Capabilities` rows against MANIFEST `capabilities_added` for kaidoku; target `statements=4 match=4 target=4 reverse_mismatch=0` | **PRIOR ART (same surface, same oracle class) and CAUTIONARY.** The lane's own negative control `controls/c2-negative/receipt.json` (cited at `corpus/lessons/round-32-verifier-spotcheck.md:71-72`) scores denial-text rows as `match=4 exit 0`, so the lexical key predicate was measured as falsified. kake's C1 declared limit (junk prose passes the counter) has the same shape; the review conjunct is the only guard in both lanes. |
| 2 | mori @ 73308ff6 | `tools/mori-register-check.py` (round 59 C1; docstring lines 2-15) | binds the active `## Capabilities` register to MANIFEST `rounds[i].capabilities_added[j]`: key, name, first-working-round cell, lane-relative evidence-path existence | **PRIOR ART (closest oracle).** Caution from mori round 57: the frozen C1 counter scanned the superseded first `## Capabilities` table and admitted false-greens (fleet-root `.ufo/reports/round-57/mori.md:12`). kake's `c98_captable.py` also selects a table; the L1 should confirm it reads the active table. kake `SCORECARD.md` has exactly one `^## Capabilities` heading (line 191 at master 7838981), so no current first-table ambiguity. |

Not verified by this seat: the body of `c98_captable.py` (kake, in-lane, out of scope). Whether the
kaidoku v3 reverse check has an equivalent in `c98_captable.py` is an open question for the L1.

### 2.2 Adjacent instruments (same capability surface, different oracle; not counted)

| lane @ HEAD | path | oracle | relation to kake r98 |
|---|---|---|---|
| kengaku @ 997a6fe5 | `plans/round68_capability_table.py` (lines 6-10) | capabilities declared in SCORECARD round sections (rounds 64-68) vs table rows; `MISMATCH n=4` -> `n=0` | **PRIOR ART for the failure mode.** The same defect class as kake C1 (table stopped receiving rows; kengaku round 68 `capability-table-omission`). Named divergence against the kaidoku census, `kaidoku-shokunin/.ufo/waves/round-76/w1/ConnectorCross.md:145-148` (D24). |
| chousa @ 378fda82 | `tools/lane-preflight.py` G05 `scorecard-paths` (`## Capabilities` section scan, around line 229) | existence of `corpus/ tools/ .ufo/` paths in the evidence cell | none to counts; overlaps the evidence-pointer column that C1 reads. |
| tameshi @ f256302b | `tools/selfstate-freshness.py` | freshness of figures that capability rows declare, vs the named instrument output | none (figure freshness, not row membership). |
| kama @ 9b4c7af1 | `tools/round74-selfdesc-canon.py` | resolves the newest capability repertoire across heading forms (bold / `##` / `###`) | none now. Heading-form drift is a known hazard: kake's counter needs the exact `## Capabilities` heading, and kake has one such heading. |

Pre-existing connector census: `kaidoku-shokunin/.ufo/waves/round-76/w1/ConnectorCross.md` lines 127-131
classify kengaku round68, mori register-check, tameshi selfstate-freshness, chousa G05 and kama
round74 as "Duplication with named divergences". kake's `c98_captable.py` is not in that census
(kake's own `.ufo/waves/round-55/w1/ConnectorCrossClaim.md` exists and was not read).

## 3. Surface (b): RFC 5861 / stale-while-revalidate / stale-if-error ground

Token-level sibling hits: **7 lanes, 24 files** (`hits_5861` = 7). Normative ground: **0**.
No sibling lane holds RFC 5861 text or a retained RFC 5861 copy.

| lane @ HEAD | files | what the hit is | relation to kake r98 |
|---|---|---|---|
| kagi @ 072bb0bc | 6 | captured response headers `stale-if-error=86400` (`.ufo/waves/round-27/build/SrcPythonVersions.headers:7,15`); third-party `node_modules` READMEs (`.ufo/waves/round-28/retained-probes/SrcNodeSemver/node_modules/http-cache-semantics/README.md:4`, `lru-cache/README.md:81`) | none (captured data; third-party docs) |
| tsukuroi @ 64f45b79 | 4 | captured headers `cache-control: max-age=60, public, must-revalidate, stale-while-revalidate=60, stale-if-error=300, s-maxage=60` (`.ufo/waves/round-24/w2/RevSourcesC/fetch/S097.hdr:5`, `S098-tag.hdr:8`, `S098-master.hdr:8`, `S099.hdr:5`) | none to the decision. Observation for the L1 or ExecStale only: this real header combines `must-revalidate` with SWR, which the contract's prohibition rule covers, so it is a usable real-world fixture candidate. Not a change request. |
| kama @ 9b4c7af1 | 4 | captured headers `stale-if-error=86400` (`.ufo/waves/round-34/w1/out/ReviewAliasQuotes/fetch/S196.headers:10`; `round-36/w2/out/RevQ224/*`; `round-36/w3/out/RevQ224/headers.txt:10`) | none (captured data) |
| mori @ 73308ff6 | 3 | retained WHATWG Fetch spec `corpus/evidence/sources-r37/S225.src:3234,4029,4033` quoting the SWR response definition and citing `rfc5861.html#n-the-stale-while-revalidate-cache-control-extension` | none. Not RFC 5861 text. Prior art for the Fetch-side reading kake already retained (in-lane `S432`). |
| kotoba @ ab151b17 | 3 | captured headers `s-maxage=300, stale-while-revalidate=31535700` (`.ufo/waves/round-47/build/SrcNewAnthropicEng.json:39`); `round-90/w1/ScoutMutSource/s260-headers-mutmut-index.txt:8,17` | none (captured data) |
| kasegi @ d16d2124 | 3 | captured headers (`.ufo/waves/round-40/wave2/LabFreshFetch.md:31`, `LabFreshFetch.transcript.txt:39`; `round-72/w1/K72ScoutCapture.md:131`) | none (captured data) |
| kumitate @ 77ebfe37 | 1 | retained RFC 9111 HTML `.ufo/waves/round-81/build/L1/captures/rfc9111.html:2410` ("defined in [RFC5861]") and reference entry at `:3778-3780` | **PRIOR ART for the RFC 9111 side** of kake's contract (kake cites RFC 9111 §4.2.4). No conflict: kake keeps its own RFC 9111 at round-96 per the freeze. |

### 3.1 In-lane note (kake, outside sibling scope, reported because the freeze's wording is narrow)

- The freeze's "grep printed nothing" claim is correct only for `scripts/` and `corpus/`. Re-run for kake
  with `--exclude-dir=.ufo` (lane root, not the `.ufo` tree) printed no lines.
- kake `.ufo/waves/` holds 76 hit files. The most relevant is
  `kake-shokunin/.ufo/waves/round-86/w1/ScribeKnowledge/rfc7234-contrast.txt:1840-1841`, which maps
  `stale-if-error` to `[RFC5861], Section 4` and `stale-while-revalidate` to `[RFC5861], Section 3`.
  This agrees with the frozen `stale-contract.md` ground and is prior art for S482. It does not change
  the C2 predicate.
- Also in-lane: round-61 `S432` (retained WHATWG Fetch, the same SWR definition as mori S225), round-63
  quote-class and several retained RFC 9111 copies that cite RFC 5861 in references.

## 4. Axis quote, fleet `AXES.md` (fleet HEAD 7687441822b3c682766a9f80ec2c6a49ed10d245)

Located (line numbers verified by a direct read of `/home/vgpnk/Projects/shokunin/AXES.md:55-83`):

- Lines 59-62: "The six axes measure what the skill knows; they do not measure what the shokunin can now *do*.
  `SCORECARD.md` therefore carries a separate `capabilities:` table — name → what it can now do (one
  line) → evidence pointer (command or path) → first-working round." (heading at line 57:
  `## Capabilities — the repertoire table`)
- **Lines 62-64 (the entry rule):** "Rows enter only through a round that demonstrates the capability
  running; a capability without a passing demonstration in the round report is pre-claiming and does
  not enter the table."
- **Line 80 (SCORECARD contract table):** "| capabilities | The repertoire table (see Capabilities): name → what it can now do → evidence pointer → first-working round |"

Relevance: this rule is the stated basis for kake C1 (a row without a closure record is pre-claiming)
and for C2 (the row lands in the same round as the demonstrating candidate). The fleet `AXES.md`
at fleet HEAD may differ from the MANIFEST pin `f8674006…`; this seat read the working copy at HEAD.

## 5. Verdict inputs

- `hits_capcal` = 2 (strict; kaidoku family, mori register-check). Adjacent, not counted: 4.
- `hits_5861` = 7 lanes (token-level); normative ground = 0.
- `axes_quote` = located (AXES.md:62-64 and :80).

## 6. Limits

- Token-level greps. Sibling instrument bodies were read only at the header/docstring level.
- The hit counts are per-lane file counts; no hit was executed.
- Sibling tips are `HEAD` of each working tree (read-only), not `master`; some lanes may have
  unpushed commits (not checked).
- No tool installs. No writes outside this seat directory.

Verdict input summary: sibling capability-table/MANIFEST instruments exist (kaidoku, mori) and are
prior art to cite; RFC 5861 ground in siblings is token-level only.
