# ScoutGround — round-89 wave-1 report

Seat: ScoutGround (recon + bounded planning data-walk). Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Base revision
`76225160d0dff8d2042fbcd037bd08b0971d5e07`. Freeze commit `08ab46a1`; dispatch
commit `2e700b9a`.

**Full findings with every file:line, receipt and measurement:**
`.ufo/waves/round-89/w1/ScoutGround/findings.md`
**Receipts copied into that directory:** `base-absence.txt`,
`capture-header-inventory.txt`, `round-89-edit-anchors.txt`,
`c2-counter-mutant-coverage.txt`, `freeze-timing.txt`, `counter-state-at-head.txt`,
plus copies of `base-c1.txt`, `base-c2.txt`, `c1-selftest.txt` and
`c2-selftest-v1-committed.txt`.

No production file was written. No commit, no push, no mutating git or jj
command, no subagent dispatch, no live network request. My only writes are
`.ufo/waves/round-89/w1/ScoutGround/` and this file. Scratch
`/fast/scratch/hyaku/kake-r89/ScoutGround/` was deleted after the receipts were
copied.

**Tools:** no install or upgrade was needed — everything ran on the host's
existing `git` and `python3` 3.14. Nothing was added, so no channel/reason
record is owed.

---

## 1. Ground inventory — what C2 covers vs duplicates

Searched `corpus/`, `scripts/`, `SKILL.md`, `PROVINCE.md` for
`(?i)\bvary\b` and for cache-key / key-construction / stored-response /
request-header-selection terms. Every hit with file:line is in `findings.md` §1.

**Covers (new ground).** The lane holds the *match* half of RFC 9111 §4.1 only.
Four lane statements say so independently, and they are the anchors C2 rests on:

- `corpus/knowledge/vary-matching.md:262–264` — "Nothing here constructs, derives or compares a cache key … the key itself is a separate construction."
- `corpus/knowledge/vary-matching.md:5` and `corpus/SOURCES.md:210` (S463) — scope cells ending "**not cache-key construction**".
- `corpus/lessons/round-88.md:44–46` — "cache-key construction, storage, revalidation, freshness, serving and browser behaviour remain open."
- `corpus/README.md:708–709` — the same fence on the round-88 frontier row.

The `Vary` *grammar* and the §4.1 source are already held (S463; RFC 9110
§12.5.5 at `corpus/lessons/round-81-gate/rfc9110.txt:5675`), so C2 reuses that
ground and adds the construction operation on top of it — an expansion of the
same axis, not a second source claim.

**Duplicates (must not be re-claimed).** RFC 9110 `token` alphabet
(`scripts/vary_match.py:41–52`), ASCII-only lowercasing (`:56–58`), OWS edge
trimming (`:41,62,126`), `Vary` split + member token check (`:60–77`),
case-insensitive header lookup with case-variant duplicate refused (`:79–99`),
the `*` wildcard decision (`:67–68`), the `invalid_input:` convention (`:139`),
and the §4.1 source body (`corpus/knowledge/vary-matching.md:1`).

**Two deliberate divergences from the r88 reader**, both required by the C2
contract and worth naming so a later reader does not read them as contradictions:
the r88 reader *dedupes* a duplicate `Vary` member, C2 *refuses* it; and the
r88 reader *refuses* an empty `Vary` value, C2 treats it as absent and emits
the bare URI key. The `mori-shokunin` S594 adjacency is recorded at
`corpus/README.md:711–713` — report, do not absorb.

## 2. Base absence — proven

`git cat-file -e 76225160…:scripts/cache_key.py` → exit 128, "exists on disk,
but not in …"; `git cat-file -e 76225160…:corpus/lessons/round-89.md` → exit
128, "does not exist". Neither path is in the base tree at all. Receipt:
`base-absence.txt`.

## 3. Recorded header data a domain trial could map to C2

**Round-23 carries no response headers.** Its 12 `live/*/fetch.json` files have
keys `bytes, contentType, error, fetchedAt, finalUrl, method, redirects,
sha256, status, truncated, url` — no `headers`. `live/*/manifest.json` is a
static canonical-URL manifest, not a capture manifest. The cause is the lane's
own r26 lesson (`round-26/w1/FetchCritic.md:51,105,120–122`): the fetcher sent
no `Accept-Encoding` and `HEADERS` omitted `content-encoding` and `vary`.

**Round-61 is the primary corpus.** `round-61/capture/manifest.json` is the
capture manifest; 12 `round-61/capture/<id>/response.json` carry a `headers`
array of `{name,value}` (duplicates preserved, wire order) with `headerCount`.
Ten carry `Vary: Accept-Encoding`; four kimi.page surfaces carry **two**
`vary` members (`Accept-Encoding`, `Origin`); `ufo-fsd-kimi-pro` carries **no
`Vary` at all**. Every header key per file is in
`capture-header-inventory.txt`.

**Round-81** repeats the shape for three surfaces (`ds4cc-primary`,
`ds4cc-robots`, `ds4cc-sitemap`), all with `Vary: Accept-Encoding`.
`round-81/population/*/fetch.json` is *not* a capture manifest — it holds only
`{id, url}`.

**The best C2 input is round-88's trial**, because it is the only place in the
lane that recorded the *request* side: `.ufo/waves/round-88/w1/ExecTrial/`
holds `capture.json` (url, status, `vary_observed_verbatim: "Accept-Encoding"`,
`credentials_or_cookies_sent: false`, `content_encoding_header_present:
false`), `response-headers.txt` (raw `HTTP/2 200` headers), and
`loopback-request.txt` (the request header set: `Host`, `User-Agent`,
`Accept: */*`, and the note that no `Accept-Encoding` and no cookie was sent).
From those three files a C2 trial payload is directly derivable — `uri =
"https://ds4cc.com/"`, `vary = "Accept-Encoding"`, `request_headers = {Host,
User-Agent, Accept}`. The nominated field `accept-encoding` is **absent** from
that request, so the contract's absent-marker branch is exercised by the real
surface — the one distinction the r88 reader cannot make.

**Honest limit:** no capture records a request header map. The r61/r81
captures record `userAgent: "round61"` and `method: "GET"` and nothing else
about the request. An r89 trial must reuse `loopback-request.txt` or record its
own; it must not present `userAgent: "round61"` as a request header map.

## 4. LANE files needing a round-89 edit (base anchors)

| # | file | base lines | anchor |
|---|---|---|---|
| 1 | `SCORECARD.md` | 5504 | insert after 5504; headings `## Round 88` 5459, `### Demonstrated repertoire` 5490, `### Planned — after round 88` 5496. **Item A targets lines 5469 and 5488** (stale `22/22`) and needs one new `integrated-selftest: 35/35` marker line |
| 2 | `LOG.md` | 3027 | insert after 3027; last heading `## Round 88 — …` at 2963 |
| 3 | `SKILL.md` | 1615 | insert after 1615; last heading `## Round 88 — …` at 1597 (registry table 1605–1609) |
| 4 | `corpus/README.md` | 713 | insert after 713; last heading `## Round-88 frontier step — Vary match semantics` at 701 |
| 5 | `PROVINCE.md` | 701 | insert after 701; last heading `## Round 87 — Age arithmetic only` at 692; `## Frontier` at 20–37 |
| 6 | `corpus/lessons/round-89.md` | — | **absent at base**; created during the wave (`28532540`, markers `d9c972da`, wave-review `a225647f`) |
| 7 | `corpus/lessons/round-88.md` | 327 | line **265** is the stale `22/22` item A targets; lines 329–336 already carry two `[r89-correction 2026-11-04]` blocks (appended, append-only); line 329 already satisfies item F's "`[r89-correction` + `L1 mistakes`" half |

Receipt: `round-89-edit-anchors.txt`.

---

## 5. Defects found in the round's own counters, contract and case set

### 5a. The C2 counter does not detect six contract violations (mutants reach `met=true`)

I built thirteen one-line mutants of the committed candidate
`scripts/cache_key.py` and scored each with the counter's own
`score_candidate(source, work, SEED=89089)`. Six reach `met=true` while
breaking an explicit `c2-contract.md` clause:

| mutant | clause broken | result |
|---|---|---|
| M1 — drop the CR half of the CR/LF check | "a header value … contains CR or LF" must be refused | `16/16 200/200 9/9` → **met=true** |
| M2 — dedupe a duplicate `Vary` member instead of refusing | "two `Vary` members are equal case-insensitively" must be refused | **met=true** |
| M4 — treat a missing `request_headers` as `{}` | "`request_headers` is missing or not an object" must be refused | **met=true** |
| M7 — do not escape the URI | §4 "In the URI, each name and each value, `%` becomes `%25`" | **met=true** |
| M11 — do not escape the `Vary` member *name* | §4 escaping covers "each name" | **met=true** |
| M13 — sort by the raw member text, not the lowercased name | §1 / §5 "sorted by the lowercased name" | **met=true** |

Seven others (M3 empty header name, M5 no OWS trim, M6 no sort, M8 escape
order, M9 `*` as a token, M10 case-fold, M12 reverse sort) are killed.

**Root cause, precisely:** the scored population cannot discriminate these
rules. The only CR/LF case is `lf-value-refused` (LF only) and `VALS` holds no
control character; there is no duplicate-`Vary`-member case and `rng.sample`
draws names without replacement; `REFUSALS` has `headers-not-object` but not
`request_headers` absent; every frozen and generated URI is
`https://e.test/` + one of `a, b, c/d, p?q=1, r#f` — no `%`, no separator — and
every `Vary` member name is drawn from the lowercase `NAMES` list, so raw and
lowercased sort order always coincide.

Behavioural witnesses (all measured):

```
M1  {"vary":"a","request_headers":{"a":"x\ry"}}  -> exit 0, key accepted (must refuse)
M7  uri "https://e.test/50% x" -> 'https://e.test/50% x\x1fa\x1e1'  (reference: '…50%25 x…')
M11 vary "x%y"               -> '…\x1fx%y\x1e\x1c'  (reference: '…\x1fx%25y\x1e\x1c')
M13 vary "aB,Ac"             -> '…\x1fac\x1e2\x1fab\x1e1'  (reference: '…\x1fab\x1e1\x1fac\x1e2')
```

**Independent corroboration:** ExecControls scored the same six gaps against
the same counter (`w1/ExecControls/scoring-receipt.txt`: `adv-cr-only`,
`adv-missing-headers`, `adv-no-dup-vary`, `adv-no-uri-escape`,
`adv-no-name-escape`, `adv-raw-sort` all `cand_met=true`); ConnectorScope
reached the same root cause from the source side (`w1/ConnectorScope.md:144`).
The gaps are real and reproducible.

**This is the R88-1 shape recurring one axis later.** R88-1 was "a table over
the committed seed or an oracle-import stub passes C2", mitigated by "the
property population is generated at scoring time" — but a generated population
is only as strong as the fixed `VALS`/`NAMES` alphabets it draws from. These
six are not tables or oracle imports; they are plausible correct-looking
implementations that violate the contract and reach `met=true`. The counter's
own selftest checks five mutants, none of them these.

**Recommended form:** route as an instrument limit in `corpus/lessons/round-89.md`
with each mutant, its contract clause and its population gap. Do **not** add
cases to the frozen set and do **not** re-score. (The lane's own wave-review
section, `corpus/lessons/round-89.md:200` onward, already routes the URI-escape
mutant, the refusal-coverage gap and the reference-copy shortcuts — my six are
the same class, re-derived independently.)

### 5b. The freeze was amended after dispatch — a live R88-E recurrence

```
08ab46a1  ct=1793826745  18:12:25  freeze — two claims, counters, contract, frozen cases, base controls
2e700b9a  ct=1793826784  18:13:04  wave-1 dispatch evidence (spec, validated payload, ready marker)
46a43e94  ct=1793826978  18:16:18  freeze v2 — shortcut guard no longer refuses a docstring …
```

`46a43e94` is **194 seconds after dispatch** and 334 after the freeze. It
changed `c89_key.py` (the `FORBIDDEN` tuple and the guard body) and re-derived
`controls/base-c2.txt`. This is R88-E again, in the shape the round claims to
close (`corpus/lessons/round-88-verifier-spotcheck.md:268–273`).

**The amendment was justified** — measured: under the v1 guard the *correct*
L1 candidate was falsely refused (`v1 guard(w1/L1/cache_key.py) = shortcut
guard: source names '.ufo/waves'`; v2 returns `None`). The v1 tuple
`('c89_key', '.ufo/waves', 'round-89', 'frozen', 'c2-cases', 'oracle')` matched
any candidate whose *docstring* mentioned the wave path, `round-89` or the word
`frozen`. The v2 tuple plus the `open(`/`.ufo` line check is materially
tighter against the real shortcuts.

**But C1 item E cannot see it.** `item_e` uses
`git log --diff-filter=A` — the commit that *first adds* `c89_key.py`
(`08ab46a1`, before dispatch) — so it reads `[]` (pass) and is blind to the
later **amendment**. Its selftest asserts "E passes when the freeze commit
precedes dispatch" and "E fails when dispatch is committed first"; it has no
case for *amend-after-dispatch*.

**Independent corroboration:** `ReviewCounterC1` reached the same conclusion in
the committed lesson (`corpus/lessons/round-89.md:158` onward) as **RC-1** ("E
reads HEAD, not `--revision`") and **RC-2** ("E ignores post-dispatch edits to
the frozen counter"). The lesson's verdict line already reflects it: "C1
unadmitted (item A open; B, C, D, F decided by prose and not behaviour; E not
revision-pinned)."

**Recommended form:** a disclosure, not a counter repair — the amendment's
witness (v1 refuses the correct candidate, v2 does not) and the fact that
item E's `--diff-filter=A` formulation cannot see an amendment.

### 5c. `freeze.md` was not updated with the freeze-v2 amendment (partly routed)

`freeze.md` is unchanged at `46a43e94` and still describes the v1 guard; the
base receipt's own text changed under it (`ctl-table` moved from
`source names '.ufo/waves'` to `source names 'c2-cases'`). The *receipt* half is
now routed — `corpus/lessons/round-89.md:60` and `:227–229` record that
`21770586` overwrote `controls/base-c2.txt` with the v2 re-run, and the
freeze-time bytes are restored as `controls/base-c2-freeze-v1.txt` (from
`08ab46a1`) with the v2 re-run kept and labelled. **The `freeze.md` half is
still open**: the freeze document does not name the v2 amendment. One-line
erratum in the lesson, not a silent edit of frozen bytes.

### 5d. A base receipt was momentarily truncated in the worktree

During this seat's run, `git status` showed
`M .ufo/waves/round-89/controls/c2-selftest.txt` with the file at **0 bytes**
against a committed 44-line version. The committed bytes are intact at
`08ab46a1` (copy in this directory as `c2-selftest-v1-committed.txt`); the file
was restored (2139 bytes, `selftest: 43/43 passed`, still so at HEAD).
Recorded because a momentarily-empty committed receipt is exactly the R88-C
failure shape, and the committed receipt is the authority.

### 5e. Minor — the `## Round 88` window in `SCORECARD.md` has no closing `## `

`item_a` closes the window at the next `## ` line; at base there is none after
5459 (the file ends at 5504), so the window runs to EOF. Benign, but a r89
section appended *without* its own `## ` heading would be swallowed by it, and
any `22/22` inside would then need a `[r89-correction …]` tag.

### 5f. Minor — item A needs a marker format the lane has never used

`marker()` matches `^integrated-selftest:` at line start. `SCORECARD.md` at base
had the string only inside prose and zero markers. The value must be what the
tool prints: `scripts/vary_match.py --selftest` prints
**`selftest: 35/35 passed`** (measured at base and at HEAD, exit 0) — *not* the
`22/22` the old SCORECARD and lesson claim. This is exactly R88-A, and the
correct marker value is `35/35`. (At HEAD, `SCORECARD.md:5514` now carries
`integrated-selftest: 35/35` — correct.)

### 5g. The `controls-count` pin is revision-bound and the count moves

`item_d` requires `controls-count: <n>@<rev>` with `<n>` equal to a recount at
`<rev>`, counted as `git ls-tree -r --name-only <rev>` filtered on
`/controls/`. Measured: base `76225160` → **1590**; `08ab46a1` → 1600;
`2e700b9a` → 1600; `46a43e94` → 1600; `f62e7954` → 1602; and it keeps rising as
this wave files controls. R88-D was exactly this ("The count is exact at
`f60a852a` (1577), but at filing HEAD `741fb728` it is 1590"). The pin must name
a revision **and** a count true at that revision. **Verified at HEAD:** the
lesson's `1604@21770586` re-derives exactly — recount = **1604**.

### 5h. What the round-89 lesson must carry (re-derived)

- `## Gate` of `corpus/lessons/round-88.md` parses, with the counter's own
  logic at base: **admits=2, rejects=2** (admits: RFC 9111 §4.1, RFC 9110
  §12.5.5; rejects: the counter-pass proposition, the empty-`Vary` proposition).
  So both `gate-sample:` and `r88-gate-summary-correction:` must read
  `admits=2 rejects=2`.
- The round-88 `controls/` paths named in `SCORECARD.md` and
  `corpus/lessons/round-88.md` all resolve at base — brace-expanded and checked
  with `git cat-file -e`: `after-c1-carrier.txt`, `after-c2-carrier.txt`,
  `base-c1.txt`, `base-c2.txt`, `integrated-trial.txt`. R88-C is therefore
  repairable either by pointing at a real receipt (`receipt=<path>` — the wave
  committed `.ufo/waves/round-89/controls/r88-c1-rerun-at-55d67f15.txt`, whose
  content is `C1v1 revision=55d67f15… items=3 open=0 closed=3 met=true`) or by
  `retracted`.
- `F_COLS = ('class','evidence','captured-by','fix','witness')`; the `## Mistakes`
  header must contain all five and there must be ≥1 data row.

---

## 6. State at HEAD `acc69ba5` (re-measured; receipt `counter-state-at-head.txt`)

The lane moved while this seat worked. Current measurements:

- **C2 counter**: `C2v1 … frozen=16/16 props=200/200 refuse=9/9 controls=5/5
  met=true`, exit 0, against the committed `scripts/cache_key.py`.
- **C1 counter**: `items=6 open=1 closed=5 met=false`, exit 1. Only **item A**
  is open, and only on the three stale `22/22` claims: `SCORECARD.md:5469`,
  `SCORECARD.md:5488`, `corpus/lessons/round-88.md:265`. Items B, C, D, E, F
  now pass.
- **Remaining item-A work**: tag the three `22/22` lines with
  `[r89-correction …]` (or correct the number per R88-A's "never by rewriting
  filed bytes" rule); the marker value is **35/35**.
- The lesson's `controls-count: 1604@21770586` re-derives exactly.
- The lane's own committed wave-review sections already carry the verdicts my
  §5a/§5b findings imply: "C1 unadmitted (item A open; …; E not
  revision-pinned). C2 unadmitted (its target certifies the instrument's
  sample, not the declared capability; the axis is mislabelled)."

**Boundary:** I did not re-derive the wave-review verdicts themselves, the
critic's axis-mislabelling claim, or the `mori-shokunin` S594 adjacency
analysis beyond naming the lane's own record of it.
