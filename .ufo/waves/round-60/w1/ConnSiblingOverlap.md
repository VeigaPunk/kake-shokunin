# ConnSiblingOverlap

Sibling-overlap scan across `/home/vgpnk/Projects/shokunin/*-shokunin` (read-only) for round 60's three surfaces: gate-status calibration and historical gate labeling (C1), append-only correction guards for knowledge files (C2), and Google user-triggered fetchers / robots.txt posture and limits (C3). Evaluated against base revision `97cdc122379711c2b02a8970752c8782da3ac81d` (2026-10-27). RULES.md channel record: no tools installed or updated.

OVERLAPS:

1. Google user-triggered fetchers and robots.txt posture/limits (C3: S427, S428, S429)
- **tabi-shokunin** (`SKILL.md:2888`, `corpus/adjacency.tsv:6, 12, 13`, `corpus/lessons/round-33.md:105`): holds client-side crawler discipline. Tabi actively obeys robots.txt as a client driver (first request `/robots.txt`, decision table rules D1–D5 in `corpus/knowledge/rate-signal-decision-table.md:49-53`). `tabi` explicitly documents that publisher-side robots and sitemap placement and its offline audit stay kake's (`PROVINCE.md:34-35, 304`).
- **Fleet-wide query scan in sibling `{SKILL.md,corpus,scripts}`**:
  - `user-triggered`: 0 hits across all 20 sibling lane repos (the only occurrences in tabi are third-party Chromium Blink C++ comments in `corpus/evidence/round-20/sources/html_form_element.cc:939` and `round-29/.../html_form_element.cc:939, 977`).
  - `generally ignore`: 0 hits across all sibling lanes.
  - `cannot enforce`: 1 hit in `mori-shokunin/corpus/evidence/sources-r37/S221.src:1705` ("the RFC 5234 ABNF cannot enforce the cardinality of list elements", an RFC 5234 syntax source, unrelated to web crawling).
  - No sibling lane holds knowledge entries or registry rows for `google-user-triggered-fetchers` (S428) or robots.txt publisher limits (S429).

2. Append-only and correction guards (C2: scripts/append_guard.py, c60_guard_cases.py)
- **kama-shokunin** (`SKILL.md:1441-1533`, `tools/append-only-audit.py` v1–v6): operates the fleet's most detailed historical deletion-audit tooling, using `registry/append-only-contract.tsv` and `registry/append-only-disclosures.tsv`. Deletions across git history are evaluated against external disclosure rows and sha256 line keys.
- **tabi-shokunin** (`scripts/check-round-contract.mjs:25, 316-320`): enforces append-only on canonical files (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`) using strict byte-prefix matching (`after.subarray(0, before.length).equals(before)`). This prefix rule flags any mid-file edit as `history_rewritten`.
- **kumitate-shokunin** (`corpus/QUALITY.md:700-721`, Q35 / `.ufo/waves/round-47/quality/q35-append-only.sh`, `scripts/sources-check.mjs:770`): validates `corpus/SOURCES.md` row immutability outside `status`, `recheck`, `used-by`.
- **kotoba-shokunin** (`SKILL.md:486`, `verifiers/check_sources_append_only.py`): verifies `corpus/SOURCES.md` table rows from `--base` to `--rev`.
- **kaidoku-shokunin** (`SKILL.md:1538`, `tools/round-38/registry-immutable.sh`): audits `SOURCES.md` table rows for in-place modifications outside the mutable column set.
- **Distinction in kake's C2**: `scripts/append_guard.py` evaluates markdown files (`corpus/knowledge/**/*.md`) via ordered subsequence alignment, allowing end-of-file appends and mid-file runs only if tagged with `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]`. Unlike `kama`, it requires no external TSV disclosure ledger; unlike `tabi` or historical `kake c55`, it avoids false-positive failures on legitimate mid-file corrections.

3. Gate-status ledgers and historical gates (C1: c60_gate_status.py)
- **kaidoku-shokunin** (`SKILL.md:1294`): records `historical gates, not active claims` in its registry table (e.g., `tools/round-32/c2-capability-calibration.py`).
- **tameshi-shokunin** (`SKILL.md:1602`): records `historical gate, not active` (`.ufo/evidence/round-14/capture-context.py`).
- **tabi-shokunin** (`scripts/check-gate-registry.mjs:21-46`): parses `SKILL.md` gate tables, requiring latest rows to supersede earlier ones (line 38), but checks only schema, column count, and script existence; it does not execute gates or verify exit codes.
- **Fleet-wide query scan**: 11 occurrences of `historical gate` across 10 sibling lanes (`chousa`, `kagi`, `kaidoku`, `kama`, `kotodama`, `kumitate`, `lore`, `mori`, `tabi`, `tameshi`). No sibling possesses an automated calibration counter equivalent to `c60_gate_status.py` that verifies `live` vs `historical` (with 40-hex ancestor pin) vs `never-met` against observed exit codes ($e_T$ and $e_P$).

CONTESTED:

1. **Client-side crawler discipline vs publisher-side placement (C3 vs tabi)**:
   - `tabi` owns client-side browser automation and crawler discipline (RFC 9309 rules D1–D5 in `rate-signal-decision-table.md`).
   - Contested boundary: If kake claimed that general web crawlers or browsers may ignore robots.txt, that would encroach upon tabi's client-side province. However, kake scopes S428 strictly to publisher-side Google crawler identity (verifying incoming request headers and IP ranges) and S429 to publisher limits ("cannot enforce robots.txt rules on crawlers").
   - Finding: The boundary split declared in `kake/PROVINCE.md:34-35` and recorded in `tabi/SKILL.md:2888` holds with zero drift: publisher placement/verification stays kake's; client obedience stays tabi's. Nothing is absorbed.

2. **Append-only verification models (C2 vs kama/tabi/kumitate)**:
   - Fleet models vary: byte-prefix equality (`tabi`), external TSV disclosure ledgers (`kama`), and table-column diffing (`kumitate`, `kotoba`, `kaidoku`).
   - Contested boundary: A lane claiming universal fleet-wide append-only enforcement would collide with sibling tooling.
   - Finding: `scripts/append_guard.py` scopes its default inspection to kake's `corpus/knowledge/**/*.md`. It operates in-lane and establishes no fleet-wide mandate.

3. **Historical gate lifecycle calibration (C1 vs fleet-wide manual status)**:
   - Sibling lanes track historical gates through static Markdown labels or lesson text, risking silent drift when historical gates unexpectedly pass or live gates regress.
   - Contested boundary: Kake's C1 operationalizes `considerthese/2026-10-26.md` proposal 5 (historical-gate list) via `c60_gate_status.py`, testing observed exits ($e_T, e_P$) against recorded status labels across 28 round 48–59 counters.
   - Finding: The population is strictly internal (`kake-shokunin/.ufo/waves/round-(N)/c(N)_*.py`); it judges no sibling gates.

NON-OBVIOUS SYNTHESIS & MOVES:
- **Axis Improved**: Operability (C2) and Calibration (C1).
- **Move**: Maintain clean demarcation between kake's in-file tagged correction rule (`scripts/append_guard.py`) and sibling external ledgers (`kama`) or byte-prefix checks (`tabi`). In kake's Claim C1 registry, preserve the exact historical status and pin (`64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`) for `c55_readme_index.py`, whose byte-prefix failure on `crawler-identity.md` motivated C2; do not attempt to back-port C2's subsequence logic into c55's historical code, as that would alter historical gate bytes.
- **Risks**: Modifying historical gate scripts breaks C1 reproducibility; leaking S428's "generally ignore" phrasing into generic crawling guidance risks contradiction with tabi's client-side obedience rules.
- **Verification**: `python3 -B .ufo/waves/round-60/c60_gate_status.py` confirms c55 is historical and green at its pin; `python3 -B scripts/append_guard.py --selftest` passes 24/24 fixture cases.

VERDICT: Sibling scan confirms zero contested overlap: tabi's crawler discipline is client-side while kake's S428/S429 are publisher-side, and kama/tabi/kumitate append-only mechanisms remain distinct from kake's in-file tagged correction guard; nothing is absorbed.
