# ConnectorScope — round 100 sibling-overlap scan (read-only)

Seat: ConnectorScope (leaf member, no subagent dispatch), lane kake, round 100 attempt 1.
Surfaces: C1 registry duplicate/shadow rows and unknown-flag exit map; C2 RFC 9111 §5.2 Cache-Control and RFC 9110 §5.5 whitespace grounds.
Scope: `/home/vgpnk/Projects/shokunin/*-shokunin`, kake skipped. Read-only: `git ls-files`, `git grep`, `git show`, `git rev-parse HEAD`, `sha256sum` (all rc 0). No sibling file, no lane file, no fleet file was written.
Scratch: `/fast/scratch/hyaku/kake-r100/ConnectorScope/` (empty; removed before yield). Tool installs: none.

## 0. Method and commands

1. Sibling HEADs: `for d in *-shokunin; git -C "$d" rev-parse HEAD` (rc 0 for all 20 siblings).
2. Canonical tools: `git ls-files | grep -E '^(scripts|tools|verifiers)/[^/]+\.(py|mjs|js|sh|ts|go|rs)$'` gave 800 files; name filter on regist|dup|shadow|exit|probe|verdict|cache|fresh|304|row|selftest|table.
3. Content: `git grep -InE` over the canonical set for `duplicate|shadow|--bogus|unknown flag|no-such|usage.*64`, and `git grep -IlE -i 'cache-control'` across every lane (excluding captures/raw/fixtures). Mutant copies under `.ufo/waves/round-*/falsify|MutC*|sandboxes` were excluded from the hit count; they are copies of a canonical file, not separate instruments.
4. RFC pins: `sha256sum` on every retained RFC 9110 / 9111 copy in the fleet and against kake's pins.

Sibling HEADs used in the table (`git -C <repo> rev-parse HEAD`):

| lane | HEAD |
|---|---|
| tsukuroi | 64f45b790f2dbbf63b9b343c47810118a79f7a35 |
| mori | 7765969c79e6f3df44cce2e303e6a0cf2b054d8b |
| tameshi | f256302b394ae3253df014fe1131e2c20e2c16b6 |
| kaidoku | 0b518f568da7b40a4ab026508d63c942faa7badf |
| tabi | 58d84eda992ffc11d77d76a2c1019bfe061f9241 |
| kotoba | 673d1e2e6f850bb54dda9698cf825cf6788c7d0d |
| kumitate | 814068f08c523f57055840b694a53f875a753cbf |
| kama | 9b4c7af16fdd4bba9e4815f4615f4b003f340747 |
| kotodama | db88f107606aae90efe01344551c7e1ea71cd419 |
| kagi | f5977284a8ce5bab09252be8196ee5dc18489926 |
| chousa | 378fda82dc2cbcc555a0565052cc408121813cef |

## 1. Hits

Relation key: **overlap** = same check surface as C1 or C2; **citable** = usable as a source pin, fixture or precedent without overlapping a check; **contradicts** = conflicts with a frozen claim or RFC text (none found).

### C1 — duplicate/shadow registry rows and exit-code probes

| # | lane @ HEAD | path (lines) | gist | relation |
|---|---|---|---|---|
| 1 | tsukuroi @64f45b79 | `tools/check-registry-coverage.py` (322-323, 547-551, 598-603) | `REGISTRY-ROW-DUPLICATE` when more than one operative SKILL.md row covers one tool; duplicate-highest table finding; selftest fixture `duplicate-row`. | overlap |
| 2 | mori @7765969c | `tools/mori-gate-registry.py` (372-373, 448, 585-587, 721-736) | `duplicate=<n>` counter over distinct registry names occurring more than once; selftest `duplicate_name_rejected`; `REGISTRY=met\|unmet`. Its counter family matches the C1 `duplicated=` naming. | overlap |
| 3 | tameshi @f256302b | `tools/registry-check.py` (30-38, 205-206, 277-297) | Runs every active row; `ROW … expect=<exit> got=<exit> held\|differs`; a row holds when exit equals `expect.exit`. Superseded rows still run, are excluded from N/M and counted as `superseded=K`. `superseded_by` must name an existing active row; duplicate names rejected. | overlap |
| 4 | kaidoku @0b518f56 | `tools/round-86/gate-registry.py` (atoms G2, G5) | G2: the verdict-map cell must declare `0=`, `1=`, `2=` and the observed `--selftest` exit must equal the declared success exit. G5 checks owner-round. Probes the real exit against the documented map. | overlap |
| 5 | kaidoku @0b518f56 | `tools/round-100/registry-selftest-truth.py` (header; START/END markers) | Same round label (r100) and the same `<!-- instrument-registry v2 -->` marker as C1, but for self-test case counts (claimed vs counted, pinned sha256, `mismatches M`). Name collision only: different lane, no shared file. Must not be confused with `c100_registry.py`. | overlap (name collision) |
| 6 | tabi @58d84eda | `scripts/check-instrument-registry-r68.mjs` (82-84) | `duplicate-row` finding when an instrument path appears in two registry rows (`byPath.has`). | overlap |
| 7 | kotoba @673d1e2e | `verifiers/check_gate_registry.py` (273-274, plus phantom-row checks at 275-277) | Selftest fixtures `missing row`, `duplicate row`, `phantom row`; the counter's own duplicate handling is exercised, not only asserted. | overlap |
| 8 | kumitate @814068f0 | `scripts/source-dupes.mjs` (5-15, 35-38, 53-54, 65, 181-182, 236) | Duplicate-group detection over a registry table (sources, not tools). Pinned `known` set: a new group is DRIFT; a stale pin is DRIFT; duplicate `known` entries fail closed (exit 2). Exit map 0/1/2/64. | overlap (adjacent surface) |
| 9 | kama @9b4c7af1 | `tools/gate-registry-check.py` (docstring lines 1-40, grading rules) | Per registered row: `thin-row`, `empty-exit-map`, `missing-path:PATH`. Checks that the verdict-map cell is present and non-empty; does not check the exit value. | overlap (verdict-map cell presence) |
| 10 | kotodama @db88f107 | `tools/check-gate-registry.py` (docstring 1-10; `TOKEN`, `GATEISH`) | Instrument vs registry coverage: unregistered instruments and dead entry-command path tokens. Not a duplicate check. | citable |

**Unknown-flag / exit-code probes (documented map vs real exit):**

| # | lane @ HEAD | path (lines) | gist | relation |
|---|---|---|---|---|
| 11 | kumitate @814068f0 | `scripts/surface-probe.mjs` (1618-1622); `scripts/round-gate.mjs` (1260-1261); `scripts/claims-check.mjs` (1229-1231); `scripts/proxy-check.mjs` (3257-3258); `scripts/routed-ledger.mjs` (673-676); `scripts/kimi-census.mjs` (1023-1024); `scripts/sources-check.mjs` (841-842) | Each runs the tool with an unknown flag (`--bogus`, `--no-such-option`) and asserts the documented exit 64 plus usage on stderr. This is a real-exit probe, not a text match. | overlap |
| 12 | kama @9b4c7af1 | `tools/round73-province-host-drift.py` (406); `tools/round74-selfdesc-canon.py` (518) | `run_tool(["--no-such-flag"])` / `_run_cli(["--definitely-not-a-real-flag"])` probes the unknown-flag exit. | overlap |
| 13 | mori @7765969c | `tools/mori-census.sh` (4706, `check_cli 'cli: unknown arg exit 2'`); `tools/mori-counter-win.py` (356) | Unknown-argument probe asserting exit 2 for the usage class. | overlap |
| 14 | kotodama @db88f107 | `tools/check-evidence-coupling.py` (1787-1790) | Usage battery: `[packet_copy, "--bogus"]` expected to exit with `EXIT_ERROR` (2) and emit JSON. | overlap |

### C2 — RFC 9111 §5.2 Cache-Control and RFC 9110 §5.5 whitespace grounds

No sibling lane contains a Cache-Control directive parser (no `scripts/`, `tools/` or `verifiers/` file parses `Cache-Control`, `no-cache` qualifiers, or `private` field lists). Every `cache-control` string in a canonical tool is an emitter (`res.writeHead(... 'cache-control': 'no-store')`) and is not counted.

| # | lane @ HEAD | path (lines) | gist | relation |
|---|---|---|---|---|
| 15 | mori @7765969c | `corpus/evidence/sources-r79/rfc9111.txt` | RFC 9111 pin: sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, 84477 bytes, 1956 lines. Byte-identical (sha256 match, `sha256sum` rc 0) to kake's `.ufo/waves/round-99/sources/rfc9111.txt`. §5.2.2.4 `no-cache` body at line 1258; §5.2.1.4 at 1164; §4.1 at 526. | citable (digest corroborated) |
| 16 | mori @7765969c | `.ufo/waves/round-79/evidence/anchor-rfc9111-r79.txt` | Receipt file: sha256 of the pin, `wc -l -c`, and four machine-located quotes with word counts. A reusable anchor-receipt pattern. | citable |
| 17 | mori @7765969c | `corpus/knowledge/ua-serving-normative-r79.md` (lines 3, 5, 22, 40) | Quotes RFC 9111 §4.1 (:528–534, :536–550, :552–557, :559–565, :576–579). §4.1 cache-selection only; no §5.2 directive text. | citable (§4.1, not §5.2) |
| 18 | chousa @378fda82; tabi @58d84eda; mori @7765969c | `.ufo/waves/round-32/w1/ScribeSourceC2/rfc9110.txt`; `.ufo/waves/round-27/assimilation/rfc9110.txt`; `corpus/evidence/sources-r100/S221-rfc9110-r100.txt` | Three RFC 9110 copies, all sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, byte-identical to kake's `.ufo/waves/round-100/sources/rfc9110.txt`. In the chousa copy `5.5. Field Values` is at line 1579 and the OWS list rule at 1671-1702. The **Whitespace** definition is §5.6.3 (TOC line 119; OWS defined at line 1521), not §5.5. | citable (pointer precision: whitespace = §5.6.3) |
| 19 | tabi @58d84eda | `corpus/knowledge/network-evidence-rung.md` (D7, lines 304-310; run5/run6 at 94-97) | Wire vs effective status: `responseReceivedExtraInfo.statusCode` is the wire status (304); `responseReceived.status` is the effective client status and can be 200 or 304 for the same wire path; `fromDiskCache`/`fromMemoryCache` are false under revalidation even when the body is served from cache. Relevant to 304 freshening semantics. | overlap (304 semantics) |
| 20 | kama @9b4c7af1 | `corpus/lessons/round-1-critic.md` (36, 58) | Captured response: `Cache-Control: must-revalidate,no-cache,no-store` (no space after the comma). A real spelled-form fixture for list-separator and qualified no-cache parsing. | citable (fixture form) |
| 21 | kagi @f5977284 | `.ufo/waves/round-26/build/ClockS013-evidence/lease.headers`; `…/ClockS023-artifacts/lease.headers`; `…/ClockS024-artifacts/kv-v2.headers` (and about 40 more `*.headers` captures under round-26/27) | Raw captured response headers that carry Cache-Control. Unparsed evidence; usable as fixture material. | citable (fixture material) |

### Excluded hits (not Cache-Control parsing or duplicate detection)

- `kengaku-shokunin` `…/upstream-bottle/bottle.py` 1836: `max_age` cookie option, not Cache-Control.
- `mado-shokunin` `…/RevengerCache/probes/probe5.sh`: XDG cache-control directives, not HTTP.
- `tabi-shokunin` `scripts/chrome-cdp-loopback-round*.mjs`, `webmcp-*.mjs`: `cache-control: no-store` emitted by test servers.
- `game-dev-3d-shokunin` `r94vendor/three.core.js:53806`: prose "cache control of the individual objects".
- `kumitate-shokunin` `scripts/omp-census.mjs` `--max-age`: receipt age in days, not HTTP.
- `kaidoku-shokunin` `…/e2e-real-fixtures.py:261`: a `no-cache` spec argument.

## 2. Counts

- hits = 21 (C1 duplicate/registry rows 10 + C1 exit probes 4 + C2 7)
  - C1 duplicate/registry rows: 10 (rows 1-10)
  - C1 exit probes: 4 (rows 11-14)
  - C2: 7 (rows 15-21)
- overlaps = 14 (rows 1-9, 11-14, 19)
- citable = 7 (rows 10, 15-18, 20, 21)
- contradictions = 0

Contradiction check: the only sibling observation that could read as a conflict with RFC 9111 §5.2 is tabi row 19 (run5 "server sent `Cache-Control: no-cache` — the staging failed to force revalidation"). [INFERENCE] run5 reuses run1's profile, whose stored entries were written before any `no-cache` was sent; RFC 9111 §5.2.2.4 governs a stored response, not a response the server sends later, so this is consistent with the RFC and is not counted as a contradiction. Recorded as a tension to check, not a contradiction.

## 3. Technique for hardening a C1 instrument

**Technique: superseded rows stay executable and must resolve to a live active row.** Source: `tameshi-shokunin/tools/registry-check.py`, lines 30-38 (superseded rows still run, `superseded=K`, excluded from N/M) and 277-297 (`superseded_by` required, must name an existing row, and must be `status == active`).

Application to `c100_registry.py`: the repair moves the seven older duplicate rows into a fenced `## Round 100 — superseded registry rows` block. The counter's duplicate check therefore cannot see them, and the fence itself is not checked for a surviving active row. Hardening: for each row in the fenced block, require that its tool path resolves to exactly one active (non-fenced) row, and fail with a `superseded-orphan` finding when none does. This makes the fence a checked redirect rather than a silent removal. Path and lines above are the source; no edit was made.

## 4. Verdict

Command and rc for the scan: `git ls-files`, `git grep -InE`, `git grep -IlE`, `git show HEAD:<path>`, `git rev-parse HEAD`, `sha256sum` — all rc 0. Sibling HEADs as listed above.

CONNECTOR hits=21 overlaps=14 contradictions=0 techniques=1
