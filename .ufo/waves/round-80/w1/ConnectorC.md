# ConnectorC — kake round 80 (w1, attempt 1)

**Verdict.** No sibling lane contests kake's ground (HTTP-date parsing, header-level robots
directives, date-grammar validation): fleet-wide the terms appear only in kake's own files. The
`merge/kake` staged package still collides on **8 ids** at the base blob and cannot be adopted this
round. One proposal in `considerthese/` is still unimplemented and directly covers C1's R79-8. One
bounded move follows from a cross-instrument fact nobody has written down: round 78's meta-robots
audit **already implements the comma merge** C2 needs, and it **rejects RFC 850 / asctime** — so
after C2 the lane will hold two instruments that disagree on the same literal, and only explicit
per-carrier scoping keeps that from becoming a C1-class report defect.

---

## 1. Sibling-overlap — kake's claim is uncontested

Scans (all read-only, cwd `/home/vgpnk/Projects/shokunin`):

| command | result |
|---|---|
| `grep -rn -iE 'HTTP-date\|IMF-fixdate\|RFC ?850\|asctime' .ufo/reports --include='*.md'` | **0 lines** (exit 1) |
| `grep -n -iE 'http-date\|imf-fixdate\|rfc ?850\|rfc ?9110\|asctime\|x-robots-tag\|unavailable_after\|date-grammar' */PROVINCE.md` | only `kake-shokunin/PROVINCE.md:419,555,571,580,592` |
| same terms, `--include='SKILL.md' --include='*.md'` across kagi/tsukuroi/mado/kengaku/kumitate/kama | 1 hit: `kumitate-shokunin/.ufo/waves/round-68/build/K68ScoutS211/captures/transports-2025-11-25.md:42` — a captured `x-robots-tag: noindex` line inside a transport capture, not a parser or a province claim |
| `grep -n -iE 'http-date\|…\|unavailable_after' MANIFEST.json` | 2 hits, both kake's own: `MANIFEST.json:43898` capability `"Offline X-Robots-Tag declaration audit"` and `:43910` kake's round-79 completion digest |

Nearest neighbours, named and dismissed:

- `kengaku-shokunin/PROVINCE.md:541-543` — date-grammar validation exists there, but the province
  **unowns** it: "What a correct 1-hour slot … and **RFC 5545 / iCalendar conformance, are
  unowned**", verified by its own fleet-wide grep. Calendar domain, not HTTP; an explicit disclaimer,
  not a claim.
- `kama-shokunin/PROVINCE.md:190` — grades *response headers* of a local `POST /v1/completions`; the
  fields are JSON `id`/`created`, no HTTP-date semantics, and the ground is the LLM serving plane.
- `kagi-shokunin/PROVINCE.md:75` — `corpus/release-clock.py` feed anchors are ISO-8601
  (`release-clock.py:1220` observes `updated 2026-10-15T18:50:14Z`), not HTTP-date.
- `tsukuroi-shokunin/tools/measure-update-recheck.py:76` — `%Y-%m-%dT%H:%M:%SZ` on its own receipts.
- `mado` and `kumitate` have no HTTP-surface ground at all (desktop plane; Windows build host).

The only province statement on the ground is kake's own `PROVINCE.md:592-596` (`[r79-correction]`),
which assigns the `X-Robots-Tag` response-header channel to `scripts/x_robots_tag_audit.py` — i.e.
kake took it deliberately, in writing, last round. **Not contested.**

## 2. `considerthese/` — one still-unimplemented proposal that fits

**Pick:** `considerthese/2026-10-23.md:36`

> "Split seat failures by cause (dead at spawn, quota, provider refusal, safety-filter model switch,
> orchestrator death) instead of a single dead count, since each cause has a different fix."

**Why it fits.** It is the durable fix for the class C1's R79-8 scores. R79-8's evidence is missing
exactly this datum: `.ufo/waves/round-79/w1-results.json` carries two zero-byte seats with
`note: null` (`ExecC2Tool`, `CriticC` — re-derived: `bytes=0 note=None` for both), which is why the
non-author closure filed R79-8 at all. It is **still unimplemented**: round-80's
`.ufo/waves/round-80/w1/swarm-registry.json` members carry only `kind`/`agentId`/`role`/`item` — no
failure-cause field — so the class recurs every wave. Cost is one registry field plus one tally line
over bytes the lane already writes; read-only, no new claim.

**Everything else in that file has landed or does not fit:**
receipt-rewrite watch (`:30`) → round-79 standing gate `c79_receipt_ledger.py` (docstring:
"standing receipt-rewrite disclosure gate"); historical-gate list (`:33`) →
`corpus/knowledge/gate-status-ledger.md:8,46,60`; landed-check / id-resolver / frontier map
(`:29`, plus `2026-10-25.md:26-29`) → `scripts/landed_check.py`, `scripts/id_resolver.py`, per
`2026-10-26.md:29`. Runner-up, unimplemented but off-theme: gate-agreement ledger
(`2026-10-26.md:32`) — calibration trend, not HTTP-date grammar, receipt discipline or queue closure.

## 3. Assimilation census — 8 id collisions, adoption still blocked

Receipt: `w1/ConnectorC/collision.out` (sha256 `10c81f73…`), produced by
`w1/ConnectorC/collision_check.py` (my own read-only census, sha256 `4dfee979…`), exit **0**,
`consistent true`, against the base blob exported from `9998dc7` (staged
`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` sha256 `5f0cd4c4…`; registry blob
sha256 `e9a50be8…`).

| metric | value |
|---|---|
| staged rows (0–3 leading spaces, 13 fields, escaped pipes not split) | **129** (dup ids 0) |
| registry rows at base | **190**, max id **S452**, `S453` absent (dup ids 0) |
| **id collisions** | **8** — `S312, S329, S367, S372, S373, S374, S390, S409` |
| nature of each collision | `same_url=True`, `bytes_identical=False`; registry row opened **2026-10-25**, staged row **2026-10-23/24** → the lane re-derived those sources independently in rounds 55–57 |
| staged rows whose URL the registry already holds | **27** (8 under the same id, 19 under another id) |
| staged URLs absent from the registry | **62** (of 89 distinct) |
| staged id range | `S287..S415` |

Corroboration from the fleet's own validator:
`scripts/sources-census.sh validate --file …/SOURCES.append.md` parses exactly **129** rows
(`E12` ×129, exit 1 because an append fragment has no `## Registry` section), so the 0–3-space rule
yields the same population I counted.

**Adoptable this round? No — blocked, and not by me only:**

1. Next free id is **S453**, which C1's R79-1 reserves for the RFC 9110 row; new rows would start
   at **S454**. The package assumed `first_id: S287` against a 145-row registry (`MERGE-REPORT.json`:
   `existing_rows 145, renumbered []`).
2. 8 duplicate ids and 27 duplicate URLs would trip census `E03`/`E04` on a literal append.
3. The package's own adopt checklist step 1 requires reading "`SOURCES-PROPOSED.md`", which **does
   not exist** in the package (`find /home/vgpnk/Projects/shokuknow -name 'SOURCES-PROPOSED*'`
   returns only lore's files; the kake package is 107 files: `SOURCES.append.md` +
   `MERGE-REPORT.{md,json}` + 98 under `knowledge/` + 6 under `amendments/`), and `SOURCES.append.md`
   carries **0** `## Gate` blocks. The gate the checklist demands cannot be run as written.
4. 129 rows × per-row re-open is a round of its own; it is outside C1's six-item population and
   C2's date shapes, and outside my write scope.

Stability check: the working tree moved mid-round (191 rows, `S453` present — a scribe has written
the C1 row). Re-running against the working tree gives the **same 8 collisions**
(`collision-worktree.out`, sha256 `f7bcb8b4…`, exit 0), so the count is not a snapshot artefact.

## 4. Cross-check — no sibling claims R79-1..R79-8

`grep -rn -E 'R79-[1-8]\b' .ufo/reports` → **0 hits** (exit 1). What does exist is a *namespace*
collision: kengaku and kama use `R79-C1`/`R79-C2` for **their own** round-79 claims
(`.ufo/reports/round-79/kengaku.md:7`, `.ufo/reports/round-79/kama.md:18`). A future pattern scan
for `R79-` will therefore harvest foreign claims; only kake's `R79-<digit>` ids mean routed defects.

---

## 5. The move (one, bounded)

**Scope the round's date-grammar statements per carrier, and record the divergence with an observed
receipt — do not harmonize the instruments this round.**

The fact nobody has written down: the round-78 instrument already contains **both** mechanisms C2 is
about to add to the header tool, and it uses them to reach the **opposite** verdict.

- `scripts/meta_robots_audit.py:676-688` already merges one comma-separated fragment back into an
  `unavailable_after` value ("an RFC 822 weekday needs its comma-joined tail merged back"), on a
  *parse-failure* trigger — round-78 prior art for amendment A1, written before round 79 repeated the
  split defect in the header tool.
- `scripts/meta_robots_audit.py:74-78` and `:389`: grammar is RFC 3339 full-date/date-time plus
  RFC 822 `[EEE,] D Mon YYYY HH:MM:SS ZONE`; "**RFC 850 is declared not implemented**".
- `scripts/meta_robots_audit.py:1249-1252`, frozen case `m25_rfc850_unimplemented_invalid`, expects
  `[invalid_value, unknown_directive]` for `Sunday, 06-Nov-94 08:49:37 GMT` — the exact finding pair
  the contract names as the header tool's *before* state, for the exact literal case **c33** requires
  to be clean.

Observed, not inferred (`w1/ConnectorC/meta-date-probe.out`, sha256 `9d627281…`; the same tree's
`meta_robots_audit.py --selftest` prints `selftest: 94/94 passed`, exit 0):

| probe (round-80 case shape) | meta tool today |
|---|---|
| p1 = c32 `Wed, 03 Dec 2025 13:09:53 GMT` | accepted, exit 0 |
| p2 = c33 `Sunday, 06-Nov-94 08:49:37 GMT` | `meta_robots_invalid_value` + `meta_robots_unknown_directive`, exit 1 |
| p3 = c34 `Sun Nov  6 08:49:37 1994` | `meta_robots_invalid_value`, exit 1 |
| p4 = c43 `Sun Nov 16 08:49:37 1994, noindex` | date rejected, `noindex` kept, exit 1 |

So after C2 lands, the same literal is **valid through the header carrier and invalid through the
meta carrier**, and `PROVINCE.md:571` ("RFC850 remains unsupported") will read as a lane-level
statement to any reader who does not also read the round-80 amendment.

**The move:** in this round's PROVINCE/knowledge/lesson text, state the `unavailable_after` grammar
**per carrier** — header = RFC 9110 §5.6.7's three shapes as amended by A1/A2 (c32–c43); meta =
S449's Google-accepted set as frozen by round-78 contract C3 + amendment 3 B6 and pinned by case
`m25` — cite the probe receipt, and file the harmonization as an explicit routed item (it is blocked:
round-78's grammar, matrix and receipt are frozen). Two riders: (a) do **not** port the meta tool's
parse-failure merge trigger into the header tool — A1's weekday-position rule is the frozen rule and
is what keeps c39's two comma-bearing dates separating; (b) the receipt must quote the probe as
observed output, not as a claim about the header tool.

**Axes.** operability ↑ (a caller can predict which carrier accepts which shape — the round's own
subject), calibration ↑ (prevents a C1-class report/registry defect, the lane's most-routed class);
harm to none: no case, oracle byte, predicate, constant or frozen receipt moves, and the round-78
matrix stays green.

## 6. Risks

- Writing "RFC 850 supported" unscoped would be contradicted by `PROVINCE.md:571` and by `m25`'s
  observed behaviour — precisely the defect class C1 scores.
- Harmonizing this round would edit round-78's frozen grammar/matrix; it must stay routed.
- The meta tool's merge is looser than A1 (fires on any parse failure); copying it would move the
  header tool outside the frozen amendment's scope.

## 7. What I ran (verbatim, with exit codes)

| command | exit |
|---|---|
| `grep -rn -iE 'HTTP-date\|IMF-fixdate\|RFC ?850\|asctime' .ufo/reports --include='*.md'` | 1 (no lines) |
| `grep -rn -iE 'unavailable_after\|x-robots-tag\|http-date\|imf-fixdate\|rfc ?850' --include='SKILL.md' --include='*.md' <six sibling repos>` | 0 (one capture hit) |
| `grep -rn -E 'R79-[1-8]\b' .ufo/reports` | 1 (no lines) |
| `git show 9998dc7…:corpus/SOURCES.md > $S/SOURCES.base.md` | 0 |
| `python3 -B .ufo/waves/round-80/w1/ConnectorC/collision_check.py "$S/SOURCES.base.md"` | 0 (`consistent true`) |
| `python3 -B .ufo/waves/round-80/w1/ConnectorC/collision_check.py …/corpus/SOURCES.md --any-shape` | 0 |
| `./scripts/sources-census.sh validate --file …/SOURCES.append.md` | 1 (E12 ×129 — fragment, not a registry) |
| `python3 -B scripts/meta_robots_audit.py --manifest $S/probe/p{1,2,3,4}/manifest.json --json` | 0,1,1,1 |
| `python3 -B scripts/meta_robots_audit.py --selftest` | 0 (`selftest: 94/94 passed`; receipt `w1/ConnectorC/meta-selftest.out`, sha256 `ef6bc965…`) |

Scratch (`/fast/scratch/hyaku/kake-r80/ConnectorC`) held the base blob export and the four probe
manifests; deleted after the receipts above were written into `w1/ConnectorC/`. No tool was installed
or upgraded; no git/jj mutation was run; I wrote only `w1/ConnectorC.md` and `w1/ConnectorC/`.
