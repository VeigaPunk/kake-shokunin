# ConnectorC — kake round 81 (w1, attempt 1)

**Verdict.** No sibling lane holds the ground C2 enters: kake's `response_snapshot`/`header_audit`
pair is *cited* by three lanes and *word-shadowed* by one (audio, a RIFF/WAVE chunk audit), and
RFC 9110 §15.5.5 status semantics is held by three lanes at three different framings; its
§15.5.4 hide-as-404 sentence is held by none, but the wave's own lesson already rejected that
anchor and amended the contract before any after-state, so nothing is left to contest. The staged
package still collides on **8** ids (unchanged since r80) and **S454 is free in both id spaces**;
the row's *scope* overlaps `S088` in-lane, and I measured what the census does with that: a
re-worded scope cell gives **W04 (warning, exit 0)** — what the lesson's drafted row gets — while a
cell copied from `S088` gives **E04 (error, exit 1)**. That boundary is string equality, not
semantics, and nothing in C1's counter reads scope text. Second-order: C2's capability row would be
the *second* row for a capability already on `SCORECARD.md:206` and in the fleet MANIFEST.

Axes: calibration (C1's routed-queue closure — §3's E04 boundary sits one registry cell away
from turning this round's admit into a census red), operability (C2 — §1 and §5).

---

## 1. Sibling overlap — C2's ground is uncontested; three lanes cite kake's tools

Scan root `/home/vgpnk/Projects/shokunin`, all read-only, all exit 0 except the greps noted.

| term | fleet hits outside kake | who holds what |
|---|---|---|
| `header_audit` / `response_snapshot` | **15 lines: 12 in 4 sibling lanes, 3 in two fleet reports** (`sibling-hits.txt` §1) | **no sibling implementation.** 3 are citations of *kake's own* tools: `kengaku-shokunin/.ufo/waves/round-68/w1/SiblingOverlap.md:117` ("`scripts/header_audit.py`/`base_path_audit.py` audit saved GET bytes offline", graded *term-level, weak*), `tsukuroi-shokunin/.ufo/waves/round-49/w1/R49ConnWave.md:36` ("kake-shokunin/scripts/header_audit.py \| offline manifest audit"), `tabi-shokunin/.ufo/waves/round-36/w2/ExecDeltaLive/evidence/moved-lanes.json:1265,1271,1451,1453` (a file list of kake's round-61 wave). 1 is a **false friend**: `audio-shokunin/corpus/live/r76-scribe/raw_header_audit.py:1-11` parses RIFF/WAVE chunk sizes ("compare the DECLARED chunk sizes against the bytes actually on disk") — an audio *container* header, not an HTTP response |
| `capture-once` / `audit-offline` | **156 lines, 0 holding the chain** | dominant hits are a different sense: kaidoku **82 × "re-capture once;"** (`kaidoku-shokunin/SKILL.md:785`, a receipt-retry rule) and mori's "capture once into a file" pipe-test hygiene (`mori-shokunin/.ufo/waves/round-13/build/PipeSource.md:106`). The two structural neighbours are different classes: `game-dev-2d-shokunin/corpus/lessons/r103-receipt-shape-gate.md:10-12` is an offline auditor over stored **verdicts.json** records (stored-record gate, no HTTP, no digest/byte-count/allowlist re-derivation); `kagi-shokunin/.ufo/waves/round-23/falsify/RevS017.md:186` records the *negative* — "No capture bytes are retained in-repo (only the TSV digests). An offline auditor cannot…". kagi therefore cannot hold the ground |
| `15.5.4` / `15.5.5` / `404 Not Found` | 3 registry rows + 1 connector note | **chousa `S061`** (`chousa-shokunin/corpus/SOURCES.md:71`, §15.5.5/§15.5.11, framed *origin-server vs local-copy availability*); **tabi `S107`** (`tabi-shokunin/corpus/SOURCES.md:121`, §15.4 redirects + method rewrites + `Retry-After`, 404/410 used as link-preflight labels, `tabi-.../round-27/w1/ConnSiblingOverlap.md:52,58`); **kake `S088`** (`corpus/SOURCES.md:96`, "HTTP response status meanings for 3xx redirects, Location references, 404 Not Found and 410 Gone"). `grep '403 Forbidden' */corpus/SOURCES.md` → **0 rows fleet-wide** |

`PROVINCE.md:38-47` (§Adjacent) assigns tabi the browser/client-crawler side, chousa research
method, kagi secrets, kama local model serving; none claims response-header auditing or RFC 9110
status semantics. **Province check:** C2 fetches three surfaces of `ds4cc.com` — the lane's first
named property (`PROVINCE.md:3`) — through the capture/audit pair its own Frontier paragraph
already assigns to itself ("Publisher response-header expectations … plus the GET-only capture and
offline audit `scripts/response_snapshot.py` / `scripts/header_audit.py` (round 61)"). **Inside
province, on named ground, uncontested.**

## 2. Registry collision re-check — 191 / 129 / 8 (unchanged since r80)

Committed instrument that exists for this: `.ufo/waves/round-70/w1/ExecMirror/guard.sh`
(sha256 `f9dde4573ba817eb26dd286607c64ca1dcbed08464fb101cc08b58fe1040347a`), whose own command shape
is the one the item quotes.

```
$ bash .ufo/waves/round-70/w1/ExecMirror/guard.sh \
    corpus/SOURCES.md /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md <scratch>/guard2
registry-ids=191 staged-ids=129 collisions=8
COLLISION: S312 S329 S367 S372 S373 S374 S390 S409
exit=1
```

| metric | value |
|---|---|
| lane registry ids | **191** (`lane-ids.txt`), range `S001`…`S453`, 0 duplicate ids |
| staged ids | **129** (`staged-ids.txt`), range `S287`…`S415`, 0 duplicate ids |
| **id collisions** | **8** — `S312 S329 S367 S372 S373 S374 S390 S409` (`collisions.txt`) |
| nature | each of the 8 is the **same source** on both sides (identical title and URL; scope cell re-worded) — already-assimilated rows still present in the staged file, not a genuine scope clash |
| drift vs round 80 | registry 190 → **191** rows, max id `S452` → **S453**, collisions **8 → 8**. Lane registry blob at base `1f84cda5…`, sha256 `fa0137a1ea39a6c63280625eccccec8a62316a1dc1fb60423968cfd458dfa86e`; staged file sha256 `5f0cd4c4debc647f3d1e2a85519d4ae2b000d91dad49765514871fa502e9f0cc` = **byte-identical to the r80 record**, so adoption is still blocked for the same reason, not a new one |
| staged RFC 9110 rows | **0** — `grep -n '9110\|15\.5\.4' SOURCES.append.md` matches only a prose note line; the package contributes nothing to C2's grounding |

## 3. S454 — the id is free; the scope is not, and the census grades that distinction differently

**Id.** `grep -n 'S454' corpus/SOURCES.md` → **0 hits** (lane max `S453`, `corpus/SOURCES.md:200`);
staged file max `S415` → **0 hits**. Sibling lanes do use the id in their own spaces — `mado`
`S454` = CPython `dict(mapping, **kwargs)` (`mado-shokunin/corpus/SOURCES.md:405`), `kama` staged
`S454` = a health-matrix row (`/home/vgpnk/Projects/shokuknow/lanes/kama/round14/SOURCES-PROPOSED.md:22`)
— which are lane-local id namespaces, not collisions for kake. **S454 is available.**

**Scope.** It is *not* unclaimed, in this lane:

| holder | row | scope claimed | §15.5.4? |
|---|---|---|---|
| kake | `corpus/SOURCES.md:96` `S088` | "HTTP response status meanings for 3xx redirects, Location references, 404 Not Found and 410 Gone" | **no** — anchor names 15.4, 10.2.2, 15.5.5, 15.5.11 |
| kake | `corpus/SOURCES.md:179` `S433` | Content-Type field semantics + field lines | no |
| chousa | `SOURCES.md:71` `S061` | 404/410 as origin-server statements, not local-copy availability | no |
| tabi | `SOURCES.md:121` `S107` | redirects/method rewrites + `Retry-After`; 404/410 as labels | no |

**What the census actually does** (measured, not predicted — `--today 2026-11-04`, three candidate
rows inserted inside the lane's `## Registry` section, receipts `census-A/B/C*.out`):

| variant | url cell | scope cell | census verdict |
|---|---|---|---|
| A | `…/rfc9110.txt` | new text ("Status semantics for an absent resource… distinct from S088's redirect statuses") | `W04 S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` — **warning** |
| B | `…/rfc9110.html#section-15.5.4` | **copied verbatim from S088** | `E04 S454 duplicate url www.rfc-editor.org/rfc/rfc9110.html within scope …` — **error, exit 1** |
| C (clean symlinked mirror) | `…/rfc9110.html#section-15.5.4` | new text | `W04 S454 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes`; codes `21 W04 / 3 E11`, exit 1 from those three E11 only (`census-C-clean.out`) |

Read the E11 lines in A and B as an artifact of the harness, not a property of the row: both ran `--file` against a registry copy outside the tree, so the copy cannot resolve `used-by` paths and every row draws E11 (`census-A.out` likewise reports E11 on rows S001…S453). Variant C is the same row in a mirror whose `corpus/knowledge` and `corpus/lessons` are symlinks, so its only E11 are three genuinely absent fleet paths (`.ufo/waves/round-41/c1_count.py`, `…/oracle_crosscheck.py`, `.ufo/waves/round-73/contract.md`).

Baseline for comparison: `sources-census.sh validate --today 2026-11-04 <lane>` on the untouched
lane → **20 W04, 0 E-codes, exit 0** (`census-lane.out`). So:
**S454 is a distinct-scope row only if its scope cell says so in words; it will add a 21st W04
(warning, harmless) either way, and it becomes E04 — a hard red — the moment the cell reuses
S088's scope string.** The lane's own convention is the fix: `S453` spends its scope cell on
"distinct scope from S010's validators, S028's URI schemes, S033's media types, **S088's redirect
statuses** and S433's Content-Type field lines" (`corpus/SOURCES.md:200`).

### 3b. What the round already decided, and the one residual risk my measurement adds

I read the wave's own lesson after finishing the runs above. It had **already** fixed S454's scope
the other way: admitted as "§15.5.5 *404 Not Found* and §15.5.11 *410 Gone*"
(`corpus/lessons/round-81.md:102`, row at `:139`), with §15.5.4 **rejected as an absent-resource
anchor** (`:158-165`) and the contract's "§15.5.4/§15.5.5" prose corrected by
`.ufo/waves/round-81/amendments/amendment-1.md` §A2 (`capture-expectations.json`'s bytes frozen,
as its `_note` requires). My independent runs agree with every number in that section: `:144`
records the same `W04 … rfc9110.txt across scopes`, and `:145-152` records the same `--file` E11
artifact I describe above — two seats, two harnesses, one result.

So the §15.5.4 route is closed by decision, and my remaining contribution is the **boundary**: the
census's W04/E04 split is decided by *string equality of the scope cell*, not by scope semantics.
Variant B proves it — identical URL and a cell copied from `S088` produces **E04 and exit 1**,
whereas the semantically-overlapping but re-worded cell produces only W04. Consequences for the
integration:

1. `corpus/lessons/round-81.md:139`'s row is safe **as written**; it stops being safe the moment a
   later hand edit re-uses S088's scope sentence (or a census revision normalises scope strings
   before comparing). Nothing in the counter would catch that: C1 reads registry line numbers, not
   scope text.
2. The admitted row is narrower than S088 by *reading*, not by section: both cite §15.5.5, and
   S088 additionally holds §15.4/10.2.2. The lesson says so (`:153-157`) and names S454 as the row
   to withdraw if section overlap is later ruled fatal — I record that as the correct disposition,
   not a defect.
3. §15.5.4's hide-as-404 permission stays unheld fleet-wide (`grep '403 Forbidden' */corpus/SOURCES.md`
   → 0 rows), and its 18-word sentence is an exact (whitespace-collapsed) substring at
   `rfc9110.txt:7583-7585`: `"hide" the current existence of a forbidden target resource MAY
   instead respond with a status code of 404`. That is future ground, not this round's row — and
   not an absent-resource statement, which is why the lesson's reject is right.
4. `capture-expectations.json:7`'s frozen `grounding.status` string still reads "S454 — RFC 9110
   §15.5.4/§15.5.5", so anyone auditing C2's committed chain sees the superseded anchor unless the
   amendment is read with it. The lesson points at the amendment (`:164-165`); the L1 should keep that
   pointer in the report's evidence list rather than quoting the frozen string alone.

## 4. `considerthese/2026-10-26.md` — one still-unimplemented proposal, grounded

**Pick:** Part 2 proposal **4**, `considerthese/2026-10-26.md` §Part 2:

> "Gate-agreement ledger. Track the verifier's agree/disagree count on admits and rejects per round
> (r56 6/6 with one reason disagreement on S388; r57 7/7) so I can say when the lane's own gate can
> be trusted more and when it's drifting, instead of reading each spot-check separately."

**Unimplemented — declared, not inferred.** `corpus/lessons/round-58.md:128-130`: "Proposals 1
(landed_check, id_resolver, frontier map) are already landed tools; 3 (operator-decision queue), 4
**(gate-agreement ledger) not taken this round** (one per round)"; `corpus/lessons/round-59.md:225`:
"Proposals 1 …, **4 (gate-agreement ledger)** and 5 (historical-gate list) are not taken this
round." `grep -rn 'gate-agreement' corpus/ SKILL.md` returns only those two declining sentences —
no ledger file.

**What the proposal points at, and what the lane already does.** The per-round datum exists, but
only as a table inside each spot-check: `corpus/lessons/round-80-verifier-spotcheck.md:147`
(`| Item | Gate decision | Re-opened source | Agree/Disagree | Reason |`) with the verdict at
`:154` ("the gate's admit and three reject/defer decisions agree with the outside re-open"). The
proposal's own r57 number is traceable the same way — `round-57-verifier-spotcheck.md:81-88` has 8
rows and `:94` states "2 of 2 admits and **5 of 5 re-checked** rejects agree", i.e. the table
carries one row marked `not checked`, so "7/7" hides `rows=8 checked=7 not_checked=1`. That gap is
exactly the drift signal a ledger would hold and no committed file holds: the only cross-round
ledger adopted from this considerthese file is proposal 5, and its `agreement=17`
(`corpus/knowledge/gate-status-ledger.md:24`) is explicitly *not* this datum — "evaluability, not
agreement" (`:25`).

**Lands as:** a QUALITY/lesson row pointer only. It is not evidence for C1 or C2 and I did not
implement it.

## 5. Second-order notes for the L1 (verified, not claimed)

1. **Capability row duplication.** `SCORECARD.md:206` already carries "Offline response-header
   expectation audit" (`scripts/response_snapshot.py; scripts/header_audit.py`, first-working
   round 61), and the fleet MANIFEST registers it at `/rounds[821]/capabilities_added[0]`. The
   contract's capability sentence therefore adds a **second** row for a capability already
   credited; per `AXES.md:57-64` a row must be demonstrated, so the new text has to name the new
   conjunct — offline re-derivation of receipt digests, byte counts, fetch time, allowlist and the
   audit's own stdout from committed bytes — and must not present capture+audit as new.
2. **Manifest join is shape-compatible, and I checked the three files against each other.**
   `capture-expectations.json` uses `surfaces[]` (`id`,`url`,`expect`);
   `c81_capture_audit.py:115-130` and `scripts/header_audit.py:197-201` require
   `{"version":1,"checks":[…], "allowlist":[…]}` with `checks[].source`. So the mechanical join is
   a **rename `surfaces`→`checks` plus a per-surface `source`**; `https` may be omitted
   (`header_audit.py` `declared_https` falls back to the URL scheme, and all three surfaces are
   `https://`), while `allowlist` must be top-level or `evaluate` rejects the manifest.
3. **Capture tool emits every key the frozen counter verifies.** `scripts/response_snapshot.py:161-180`
   writes `url`, `finalUrl`, `method`, `status`, `headers[]`, `bytes`, `sha256`, `truncated`,
   `fetchedAt`, `bodyFile` — all eight keys `verify_receipt` (`c81_capture_audit.py:59-99`) reads.
   One edge: `bodyFile` is `null` for an empty body, and `verify_receipt` treats a non-string
   `bodyFile` as `no bodyFile` → opens the item. All three named surfaces are non-empty, but a
   0-byte response (HEAD-like 204/304) would fail the claim rather than the tool.

## Receipts

`.ufo/waves/round-81/w1/ConnectorC/` (all sha256 below):

| file | sha256 | what it is |
|---|---|---|
| `census-lane.out` | `7772522f96de873f8a21f0bc46d983b02d0be8d151345412f9b1dd5b34f486ce` | untouched lane, `validate --today 2026-11-04`: 20 W04, exit 0 |
| `census-A.out` | `6788237e62bda5c0ad36f246a8b6fb701cdbe9ca2d41c9e903e5db5f784e05f4` | S454 variant A (`.txt`, new scope) → W04 |
| `census-B.out` | `40d20cac67c0169aa3d1ba54e1e91cd42a7608973e74381b260c5d295bf4a048` | S454 variant B (S088 scope copied) → E04 |
| `census-C.out` | `e266f1dc6aece5024d37a8306dfea6a9b76eb55c6a98f7e08c63a68ef02a3c32` | S454 variant C, flat mirror |
| `census-C-clean.out` | `f2f7932cc7ae7957d638888f23e47d555fea1799cabc1d708012e3f63470be4b` | S454 variant C, symlinked mirror: 21 W04 + 3 E11 (`round-41/*`, `round-73/contract.md` absent there) |
| `guard.out` | `a98c07c858276dbf25b8d605d0263c1ab846597f8dfa61758ad22bbfa37ba5a1` | committed guard: `registry-ids=191 staged-ids=129 collisions=8`, exit 1 |
| `lane-ids.txt` | `729cdbc503ac45604541ac552dfd76016c0e29344ce2d2fcc21a72643a44e005` | 191 lane ids |
| `staged-ids.txt` | `3938ec94ee29d52d27e6192603a9c30b9bfee3a8969600c7207478c3828f9deb` | 129 staged ids |
| `collisions.txt` | `a443d89dc53a6ad4d6c8d6c7204116f378bdd479620dcbb95a02a92def8ea9a0` | 8 ids |
| `sibling-hits.txt` | `c64ac3dae3454f46d6d4215004efd273a1420afacea998b2ae0ec1d496eacd4b` | the fleet greps behind §1: per-lane hit counts, the 15 full `header_audit`/`response_snapshot` `file:line` hits, the `15.5.x` registry rows, the capture-once per-lane histogram |

No production file written. Scratch tree `/fast/scratch/hyaku/kake-r81/ConnectorC` removed before
yield. No tool installed or upgraded. No network request was made by this seat: every byte cited is
from the lane tree or the read-only shokuknow staging area.
