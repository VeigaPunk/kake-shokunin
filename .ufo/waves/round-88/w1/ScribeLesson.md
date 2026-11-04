# ScribeLesson — round 88, wave w1 (census + round lesson + counter probes)

Seat `ScribeLesson` (scribe, leaf member — no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Base commit
`f4479c14813037ad993a49a3dee4028763470f7a`; freeze named in the brief v2
`8063739791e21a8d7966fd968913e552e1433881`; LANE HEAD at the end of this seat v3
`52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`.

Findings are lane-internal, not outside admission. No production byte was edited.

## 1. Census — full output and exit code

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes
kake	W04	S450 duplicate url html.spec.whatwg.org/multipage/semantics.html across scopes
kake	W04	S451 duplicate url www.rfc-editor.org/rfc/rfc3339.txt across scopes
kake	W04	S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S454 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S455 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S461 duplicate url httpwg.org/specs/rfc9111.html across scopes
kake	W04	S462 duplicate url httpwg.org/specs/rfc9111.html across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

**Exit code: 0.** Retained verbatim at `w1/ScribeLesson/receipts/census-before.txt`
(sha256 `8fb144c8d7f3d9f429d9db2c31b3b35c882d8ae832e88a13a4c9819110736004`).

The **after** run, re-executed at the end of this seat, produced a byte-identical
output apart from the trailer line (`census_before_exit=0` →
`census_after_exit=0`); retained at `w1/ScribeLesson/receipts/census-after.txt`
(sha256 `a22db80bfbfc13a2fe1354f12e8d3aed197be69615fcd6afcadec1b76bd0a2f2`).
24 `W04` lines, `ok`, exit 0 — unchanged.

Census note for L1 (not yet observed, so not claimed as done): the round's
`S463` row and the two knowledge entries are **not** in the lane yet — the
registry still ends at S462 (`grep -c 'S463' corpus/SOURCES.md` → 0) and
`corpus/knowledge/vary-matching.md` does not exist. When they land, `W04` should
rise by one (the census normaliser strips the `#…` anchor, so
`httpwg.org/specs/rfc9111.html` is the same URL key already used by S461/S462 in
other scopes) and the row's `used-by` path must exist on disk or `E11` fires. The
post-integration census is L1's to take; **no such receipt exists yet**.

## 2. Deliverable

`w1/ScribeLesson/round-88.md` — the round-88 lesson draft: `## Gate` (four
candidates, two admits and two rejects, each with URL, access date, a ≤25-word
located quote, reason and flip condition), `## Mistakes` (one mined mistake with
class, evidence pointer, captured-by criterion, fix, and the witness that reddens
the fix), plus claims, limits, reviews and census before/after sections.

## 3. Behaviour and gates

| Gate | Result | Receipt |
|---|---|---|
| C1 counter selftest (re-run by this seat) | **11/11**, exit 0 | `receipts/c1-selftest.txt` |
| C2 counter selftest (re-run by this seat) | **17/17**, exit 0 (`match=67 mismatch=109 invalid=24`) | `receipts/c2-selftest.txt` |
| C1 at base `f4479c14` | `open=3 closed=0 met=false`, exit 1 — detail strings byte-identical to `controls/base-c1.txt` | `receipts/base-c1-rerun.txt` |
| C2 at base `f4479c14` | `frozen=0/20 random=0/200 met=false`, exit 1, tool absent | `receipts/base-c2-rerun.txt` |
| C1 counter with the C2 case file deleted from a copy of the wave dir | **11/11**, exit 0 — the r87 eager-fixture-load defect does **not** recur | `receipts/c1-selftest-without-c2-fixture.txt` |
| L1's committed candidate `w1/L1/vary_match.py` (sha256 `2da573d3…`) under the v3 counter | `frozen=20/20 random=200/200 met=true`, exit 0 | `receipts/l1-candidate-c2-score.txt` |
| Probe script P1–P11 | exit 0, deterministic JSON | `receipts/scribe-probes.json`, `probes/round88-scribe-probes.py` |

No carrier revision was scored by this seat: `scripts/vary_match.py`,
`corpus/knowledge/vary-matching.md` and `corpus/knowledge/gate-agreement-metadata.md`
are **absent at HEAD**; the candidates live in peer wave directories. **Pending
receipts** (named, not invented): the carrier C1/C2 measurements, the integrated
`S463` row, the two integrated knowledge entries, the integrated lesson, the
post-integration census, and the outside closure spot-check.

## 4. Defects found in the round's own counters and case set

All reproduced by this seat over committed lane bytes; full output in
`receipts/scribe-probes.json`, script in `probes/round88-scribe-probes.py`.

**C2-1 — the counter is satisfiable without the capability (measurement defect).**
A stub that imports the committed counter's own `reference()` and prints its
verdict scores `frozen=20/20 random=200/200 met=true`, exit 0 (probe `P10`; the
stub is `probes/stub-delegate-to-committed-oracle.py`). The counter runs the
candidate with inherited cwd and no read restriction, so the oracle is reachable
at scoring time. Related, and not re-measured by this seat: the contract's
sentence “a lookup table keyed on known inputs cannot pass it” is defeated by a
table over the *committed* seed, because the generator and seed are committed
bytes — a peer seat (CriticClaims §2.1) measured that shape.

**C2-2 — the freeze moved after dispatch and three seeded labels moved with it.**
Measured directly (`P1`): the v2 and v3 counters generate the **same 200 inputs**
(same ids, same order, same payloads) but label `r53`, `r150`, `r193`
`mismatch` → `invalid`; the population digest moves `004a8eb75b95…` →
`52714a5f4ae9…`, and the constant-stub control scores move with it
(`9/20 + 112/200` → `9/20 + 109/200`, `4/20 + 21/200` → `4/20 + 24/200`). The
v3 commit's sentence “No item, case, threshold, control or target moved” is
accurate about the 20-case set and the C1 items and inaccurate about the
200-case labels. Additional measurement by this seat: the L1 candidate shipped in
that same commit scores **197/200 under the v2 oracle and 200/200 under v3** —
the amendment is load-bearing for the candidate it ships with. A seat that
scored a faithful candidate against v2 would have recorded a false miss.

**C2-3 — the reference accepts a trailing LF as a token character (soundness
hole).** `TOKEN` ends in `$`, which in Python matches before a final newline:
`is_token('accept-encoding\n')` is `True`. Measured: `reference('*\n', …)` returns
`match` for maps whose values differ, and `reference('accept-encoding\n', …)`
returns `match` where the field values differ — the wildcard rule and the
nominated-field rule are both bypassed by one LF. 0 of the 220 committed cases
contain an LF or CR, so no score moves today; the committed candidate copies the
same regex. The reference-vs-frozen selftest cannot see it.

**C2-4 — two declared behaviours are unpinned by the 220-case population.**
Branch coverage measured by this seat (`P2`): 0 disagreements with the reference,
but three branches are never exercised — a non-token header-map key, an ambiguous
case-variant duplicate name, and a non-dict request map. Two mutants that change
declared behaviour therefore still score `20/20 + 200/200 met=true`
(`P11`): merging duplicate names instead of refusing them, and accepting non-token
header-map keys instead of refusing them. A third mutant — refusing to trim OWS
around `Vary` members — is killed (`16/20 + 110/200`), so that clause is pinned.

**C1-1 — D2's two conjuncts are weaker than their wording.**
`c88_defect_queue.py:111` compares the six terms with `obj != VALID_OUT`, i.e.
Python equality, so `20.0 == 20` passes; `:124` accepts the candidate's own
`--selftest` as a green banner (`'selftest' not in p.stdout.lower()`), which the
candidate prints. Three mirror trees built from the counter's own `mirror_tree()`
green fixture all score `open=0 closed=3 met=true`, exit 0 (`P3`, `P4`, `P5`):
(a) the six terms emitted as **floats** `20.0 …` with the tool's own type
assertion relaxed to accept them — the tool's own `--selftest` still prints
`selftest: 61 isolated CLI fixtures passed`, exit 0; (b) the arithmetic replaced
by a **hardcoded table** for the one probed payload and the `--selftest` replaced
by a printed banner with no fixture run — the counter's selftest conjunct is
satisfied by that banner, and a second valid payload (`age_value` omitted)
returns `invalid_input: unsupported input`; (c) the arithmetic left intact and
only the `--selftest` replaced by the printed banner — `open=0 closed=3 met=true`.
This is the r87 “weak exact-type predicate” mistake re-instantiated in the
round-88 counter, in the very item that was supposed to close it. A type-strict
comparison kills (a) and (b) but not (c): the selftest conjunct has to be
replaced by evidence the counter computes itself (its own expected values for ≥2
payloads).

**C1-2 — D3's history check is not byte-identity, and its cadence test is
vacuous.** The history check compares `str.splitlines()` output, so every base
line's bytes may change: a full CRLF rewrite of the entry still scores
`open=0 closed=3 met=true`, exit 0 (`P6`) although the contract says “preserve
every other base line byte-identically”. The cadence predicate
(`rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())`)
accepts `recheck: 5` — a bare number that names no cadence — with
`open=0 closed=3 met=true`, exit 0 (`P8`).

**C1-3 — D1's ledger-path binding is a substring test.** A companion whose
`source:` line names `corpus/knowledge/gate-agreement-ledger.json.bak` — a path
that does not exist — closes D1 (`P7`). The contract requires the companion to
name *the* ledger path.

**C1-4 — D3 is also over-strict in one direction (false red).** A pure insertion
immediately after the `recheck:` line, which the contract permits (“other
differences must be pure insertions”), is reported as
`history-preservation violation at base line 3 (replace)` and exits 1 (`P9`),
while the same line inserted in the body passes. difflib merges the insertion
into the `recheck:` replace opcode.

**C1-5 — the r87 eager unrelated-fixture load does not recur.** Positive
control: a copy of the wave directory with `vary-cases.json` deleted still runs
the C1 counter's selftest 11/11, exit 0. The r87 defect (the C1 counter loading
the C2 case file at startup) is closed in the r88 instrument.

## 5. Sources opened this round

| URL | HTTP | bytes | sha256 | accessed (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T18:56:05Z |
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T19:01:34Z |

One unauthenticated GET each; no credentials, cookies, session values or tokens
sent; a `set-cookie` header came back from the CDN and was **not** resent;
nothing published, deployed or changed in any account. Both bodies retained with
their response headers under `w1/ScribeLesson/receipts/`. The RFC 9111 body is
byte-identical to the lane's round-87 retained copy; the RFC 9110 body is
byte-identical to the lane's round-81/82 retained copies.

Located quotes used in the lesson's Gate (each ≤25 words, each verified present
byte-exactly in the retained body by whitespace-normalised substring match):

- RFC 9111 §4.1 ¶1, txt lines 528–534: “the cache MUST NOT use that stored
  response without revalidation unless all the presented request header fields
  nominated by that Vary field value match” (24 words).
- RFC 9111 §4.1, txt lines 556–557: “A stored response with a Vary header field
  value containing a member "*" always fails to match.” (17 words).
- RFC 9111 §4.1, txt lines 552–554: “a header field is absent from a request, it
  can only match another request if it is also absent there” (20 words).
- RFC 9110 §12.5.5, txt line 5675: “Vary = #( "*" / field-name )” (7 words).
- RFC 9110 §5.2, txt lines 1499–1502: “its combined field value consists of the
  list of corresponding field line values within that section, concatenated in
  order” (19 words).
- RFC 9110 §5.3, txt line 1522: “For consistency, use comma SP.” (5 words).
- RFC 9110 §5.6.1.2, txt lines 1695–1697: “A recipient MUST parse and ignore a
  reasonable number of empty list elements” (13 words).
- RFC 9111 §4.2, txt line 621: “response_is_fresh = (freshness_lifetime >
  current_age)” (5 words).

## 6. Touched surfaces

Writes, all inside the seat's two allowed paths:

```
.ufo/waves/round-88/w1/ScribeLesson.md                      this report
.ufo/waves/round-88/w1/ScribeLesson/round-88.md             the lesson draft
.ufo/waves/round-88/w1/ScribeLesson/receipts/                census ×2, RFC bodies + headers,
                                                            counter selftests ×3, base reruns ×2,
                                                            L1 candidate score, probe JSON,
                                                            P3-P5 tool detail, commands
.ufo/waves/round-88/w1/ScribeLesson/probes/                  the reproducible probe script + sources
```

Scratch `/fast/scratch/hyaku/kake-r88/ScribeLesson/` was created explicitly, used
as the only work area, and **deleted before this yield** after the receipts above
were copied in. No `/tmp` path is cited anywhere as evidence; no inherited
`TMPDIR` was relied on (every run set `TMPDIR` explicitly to a scratch
subdirectory). No clone was made.

Read-only: the lane repo (`git rev-parse`, `git log`, `git show`, `git diff`,
`git status`, `git cat-file`), the peer wave reports, and the two RFC documents
over the network.

## 7. Out of scope / not done

- No production byte edited: no `scripts/`, `corpus/`, `SKILL.md`, `LOG.md`,
  `SCORECARD.md`; no commit, no push, no mutating git/jj command, no fleet-repo,
  sibling-lane, `shokuknow` or source-tree write.
- No registry row added (S463 is a peer seat's candidate, not mine to land), no
  knowledge entry landed, no lesson landed in `corpus/lessons/`.
- No carrier revision scored, no candidate evaluated at an integrated commit, no
  outside admission or closure claim.
- No live surface contacted beyond the two RFC documents; no claim about
  cache-key construction, storage, revalidation, freshness, serving or browser
  behaviour.
- No subagent dispatch, no delegation.
- No tool installed or upgraded: Python 3.14.8 and curl were already present.
  **PACMAN was not touched** (host-wide pause honoured); no `uv`, no `npx`, no
  write to `~/.local/bin` or any PATH directory.

## 8. Limits of this report

- Every defect above is a defect in the round's **instruments or case set**, not
  in a production byte: no production byte exists for this round at HEAD.
- The mirror trees are built with the counter's own `mirror_tree()` helper, so
  they share its notion of a compliant tree; a tree written from scratch outside
  that builder was not scored by this seat.
- Probe outcomes are deterministic and reproducible from
  `probes/round88-scribe-probes.py`, but they characterise the instrument's
  discriminating power, not the truth of any candidate.
- The population-wide statements are over the one committed 220-case batch
  (frozen sha `c461cbd8…`, random sha `52714a5f…` under v3 / `004a8eb7…` under
  v2); the generator's cross-version reproducibility was not re-measured here.
