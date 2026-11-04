# ScribeVary — round 88 wave 1 (knowledge entry + registry row for the conservative Vary-match profile)

Seat: `ScribeVary` (scribe, leaf member — no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Lane HEAD when this seat ran: `52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`
(freeze amendment **v3**). Base commit `f4479c14813037ad993a49a3dee4028763470f7a`.
Freeze v2 `8063739791e21a8d7966fd968913e552e1433881` is v2 of the counter; the
counter on disk at run time is v3, which moved the wildcard rule behind
input validation (see **Defects found**, D-3 and D-4 — and note that two
findings I first wrote were withdrawn after re-checking).

## Behavior delivered

Two candidate artifacts, in this seat's wave directory only:

1. `LANE/.ufo/waves/round-88/w1/ScribeVary/vary-matching.md` — the knowledge
   entry candidate for the conservative Vary-match profile.
2. `LANE/.ufo/waves/round-88/w1/ScribeVary/sources-row.md` — the registry row
   candidate for the new SOURCES row.

Plus the retained source body and its response headers, kept beside them so
the entry's quotes are checkable:

3. `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.html` (178573 bytes,
   sha256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`)
4. `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.headers`

No production file was edited. `corpus/SOURCES.md`, `corpus/knowledge/`,
`scripts/`, `SKILL.md`, `LOG.md` and `SCORECARD.md` are untouched — `git
status --porcelain` in the lane shows only untracked wave files. No commit,
no push, no mutating git or jj command, no write outside this seat's wave
directory and its own scratch root.

## The entry: what it says

Opens with the three provenance lines in the first three lines, each with a
non-empty value on the same line (the lane's `scripts/corpus-contract.mjs`
trio rule: `source:` / `verified-at:` / `recheck:` inside the first 8 lines):

- `source:` names **S463** — the new registry row — the RFC 9111 §4.1 URL
  `https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses`, the
  retained body path, its byte count and its sha256, and states that S461
  and S462 keep their own scopes.
- `verified-at:` gives **2026-11-04**, the own-GET completion time 18:52:31Z,
  HTTP 200, 178573 bytes, the same sha256, and the two earlier retained
  copies of the same URL it is byte-identical to. It also states what this
  seat did *not* do (did not run the candidate CLI, score the counter, or
  close C2).
- `recheck:` gives the cadence **180d, due 2027-05-03**, or sooner after a
  source change, and the re-fetch instruction. It names **no ephemeral
  path** — the scratch location is left to the reader. (This mirrors the
  r87 D3 finding, where a `recheck:` line naming `/fast/scratch`, `TMPDIR=`
  or `/tmp/` was the defect; the line here avoids all three.)

Two further metadata lines follow, in the house style of
`corpus/knowledge/cache-control-effective.md` and
`corpus/knowledge/cache-current-age.md`: `ground:` (freshness — round-88 C2,
a bounded conservative Vary-match reader over supplied request-header maps)
and `scope:` (the §4.1 match rule read offline from two supplied header
maps; not cache-key construction, storage, revalidation, freshness, serving
or any browser behaviour).

### Sections, as specified

- **Located quotes** — the MUST NOT sentence (§4.1 ¶1), the three permitted
  transformations (§4.1 ¶2 definition and ¶3 list), the absence sentence
  (§4.1 ¶4) and the `*` sentence (§4.1 ¶5). Each quoted span is blockquoted
  (not double-quoted) so a span-extraction check reads it as source text,
  and each is a **raw substring** of the retained body. The class was
  derived with the lane's own tool, not asserted:
  `python3 -B scripts/quote_class.py classify --raw <body> --text <flat
  rendering> --quote <span>` returns `raw-substring` for all seven spans.
  The flat rendering was produced by
  `.ufo/waves/round-63/quote-class/extract_text.py` (the lane's own recipe),
  78839 chars from 178573 bytes. Each span is also **within the lane's
  25-unit ceiling** for a new entry's quoted spans (measured: 22, 21, 11,
  10, 21, 20, 11 units), which is why the MUST NOT span and the §4.1
  definition span are quoted as trimmed raw runs rather than whole
  sentences; the entry prints the full sentences in prose and says which
  run it quoted.
  Where the retained HTML splits a sentence across markup nodes, the entry
  says so and quotes the contiguous raw run, naming the modal and subject in
  prose; the full sentence as printed is labelled **collapsed-only** against
  the raw body by the same classifier, and the entry does not claim it as a
  raw substring.
- **A page-uniqueness subsection** — each of the seven spans occurs exactly
  once in the retained body and in no other retained page in the lane, so
  all seven count as page-unique. The entry records the one near-miss: a
  shorter form of the whitespace item (without the final *'s syntax*) does
  occur in the retained RFC 7234 body, which is why that span was quoted at
  its full length.
- **Decision table** — rules R1–R11, rule → verdict, applied in order, first
  rule that fires decides. Covers the token check, the empty-member check,
  the ambiguous-duplicate-name refusal, the non-string value refusal, the
  `*` rule, the absent-field rule, the OWS-trim comparison, the list
  combination and the ASCII case-insensitive name comparison.
- **The twenty frozen cases** — a table mapping each of the 20 frozen case
  ids to the rule that fires first and the verdict, so the table is checkable
  against `vary-cases.json` line by line.
- **Precedence** — a subsection stating that input validation runs *before*
  the wildcard rule, that the frozen 20 do not contain such a case, and that
  the 200-case seeded population does (3 cases), with the counter's own
  reference implementation answering them `invalid`.
- **Error patterns** — 10 bullets, each naming the wrong move, the rule
  that catches it, and the source relation that makes it wrong.
- **Runnable checklist** — three commands, each starting with
  `printf '%s' '<payload>' | python3 -B scripts/vary_match.py`: one match,
  one mismatch, one refused input, with the expected stdout/stderr/exit for
  each. The `scripts/vary_match.py` path is the production path the round
  contract names; the entry states that the file is L1's to integrate and
  that at the base commit no such script exists, and it names the frozen
  reference implementation as the source of the expected verdicts.
- **Explicit non-claims block** — no cache-key claim, no storage claim, no
  revalidation claim, no freshness claim, no browser claim, no live surface
  asserted clean, the **conservative asymmetry** (*`match` is always a
  transformation §4.1 permits; `mismatch` may be stricter than a
  field-specific rule*), and the statement that **ordered line combination
  and OWS trimming are local adapter conventions**, not §4.1 quotations. It
  also states that the decision table is a reader specification, not a
  conformance suite, and that the entry records no score of its own.

### House style

Read first, as the item required: `LANE/corpus/knowledge/cache-control-effective.md`
and `LANE/corpus/knowledge/cache-current-age.md`. The entry follows both:
provenance lines first, a bounded scope line, a title, located quotes with
their paragraph anchors, a decision table, an error-patterns list, a runnable
checklist with the exact command form, and a closing *what this entry does
not establish* section.

## The registry row

One row, **11 columns**, in the `corpus/SOURCES.md` schema
(`id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by`):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S463 | RFC 9111 — HTTP Caching, §4.1 Calculating Cache Keys with the Vary Header Field — https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses | spec | A | The Vary match rule for two requests: the transformations that make nominated header fields match, the absent-field rule and the always-fails wildcard; not cache-key construction, storage, revalidation, freshness, serving or browser behaviour | RFC 9111 June 2022 section 4.1 paragraphs 1 to 5, retained HTML line 269; opened 2026-11-04, GET-only, HTTP 200, 178573 bytes, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64; retained .ufo/waves/round-88/w1/ScribeVary/rfc9111.html | Two requests match when the first can be transformed into the second by whitespace removal, field-line combination or known-semantic normalization; a field absent from both requests matches; a member `*` always fails to match | mined | 2026-11-04 | 180d | corpus/knowledge/vary-matching.md |

**Column count of every row drafted — reported:**

| Row | Where | Columns | Pipe characters |
|---|---|---|---|
| S463 | the registry row above, in `sources-row.md` | **11** | 12 (all delimiters) |
| schema header | the header row immediately above it, in `sources-row.md` | **11** | 12 (all delimiters) |

**No cell contains a literal pipe.** Verified mechanically: splitting the
drafted row on `|` yields 13 fields, the first and last empty, leaving 11
cells, and the row contains exactly 12 pipe characters — the 12 delimiters.
The `teaches` cell spells the wildcard member as `` `*` ``; the `scope` and
`anchor` cells contain no pipe.

**Id: S463, and the collision check.** The lane registry currently ends at
**S462**, so S463 is the next free id, as the item expected. `grep -n
'S463' corpus/SOURCES.md` returns nothing — no collision in the lane
registry. The `merge/kake` package's `SOURCES.append.md` holds 129 staged
rows in the range S287–S415 and does **not** claim S463; intersecting the
two id sets gives the eight collisions the contract mentions — **S312, S329,
S367, S372, S373, S374, S390, S409** — none of them S463. (Other lanes in
the fleet each have their own S463; ids are lane-local, so that is not a
collision.)

**Schema conformance, checked with the lane's own validator.** The row was
appended to a scratch mirror of `corpus/SOURCES.md` and validated with
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--file <scratch>/corpus/SOURCES.md`. Result for S463:

- **No `E01`–`E10` fires.** 11 cells (awk NF=13, as the contract
  requires); `S463` matches `S[0-9]{3,}`; the id is unique; `kind=spec`,
  `tier=A`, `status=mined` are all in the enums; `opened=2026-11-04` is a
  valid ISO date not in the future; `recheck=180d` matches the `^[0-9]+d$`
  cadence form; tier A is not `community`.
- **`W04` fires**: *duplicate url httpwg.org/specs/rfc9111.html across
  scopes*. The URL is already used by S461 and S462, and the census's URL
  normalizer strips the fragment, so the `#caching.negotiated.responses`
  anchor does not create a distinct URL key. `W04` is a warning, not an
  error, and it already fires for S461 and S462 today. **`E04` does not
  fire**: it needs the same URL *and* the same scope text, and this row's
  scope text is distinct from S461's (*Response Cache-Control first-match
  lifetime and duplicate-value first-occurrence option…*) and S462's
  (*Conservative current-age arithmetic on supplied timestamps only…*).
  The `teaches` cell says `supersedes` nothing and needs to.
- **`E11` fires against the lane registry until L1 lands the entry.**
  `E11` checks that each `used-by` path exists on disk, and
  `corpus/knowledge/vary-matching.md` does not exist because this seat's
  candidate lives at `.ufo/waves/round-88/w1/ScribeVary/vary-matching.md`.
  The `used-by` cell names the landed path, as every other mined row does,
  so the row and the entry must land together. Confirmed by removing the
  placeholder file from the scratch mirror and re-running the validator:
  `file E11 S463 missing used-by corpus/knowledge/vary-matching.md`.
- `W01`/`W02`/`W03` do not apply (tier A, status `mined`, `used-by` is a
  path, not `—`).

The lane's own census on the **unmodified** lane registry, for reference:
`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kake` → exit 0, with only `W04` warnings (including for S461 and S462 on
this same URL).

## Gates

| Gate | Command | Result |
|---|---|---|
| Counter selftest | `python3 -B LANE/.ufo/waves/round-88/c88_vary.py --selftest` | **17/17 PASS, exit 0** |
| Decision table vs the 20 frozen cases | `python3 -B check_table.py` (scratch) | **20/20 reproduced** |
| Decision table vs the 200 seeded cases | same script | **200/200 reproduced** |
| Entry trio shape | `node scripts/corpus-contract.mjs --root <scratch mirror>` | the drafted entry produces **no** `missing_metadata` finding (only the pre-existing `meta-robots-directives.md` failure, which is a base-lane finding, not this seat's) |
| Drafted row shape | `bash scripts/sources-census.sh validate --file <scratch mirror>` | **no E-code for S463 except the expected E11**; `W04` only |
| Checklist commands | the three `printf '%s' … | python3 -B …` invocations, run against `.ufo/waves/round-88/w1/L1/vary_match.py` | match → `match`, exit 0; mismatch → `mismatch`, exit 0; refused → `invalid_input: vary has an empty member`, exit 1, empty stdout |
| L1 candidate against the counter | `python3 -B LANE/.ufo/waves/round-88/c88_vary.py --tool LANE/.ufo/waves/round-88/w1/L1/vary_match.py --work <scratch>` | `frozen=20/20 random=200/200 met=true exit 0`, `cases_sha256 c461cbd8…`, `random_sha256 52714a5f…` (observed, not claimed as this seat's result) |
| Whole-package check | a 50-assertion sweep over both deliverables (scratch script, deleted after the run) | every assertion passed except one that was itself a false positive — see **Known limits** |

Source acquisition — one GET, GET-only, no credentials, cookies or session
values sent, no account state changed:

```
curl --fail --silent --show-error --max-time 60 -D rfc9111.headers \
     -o rfc9111.html 'https://httpwg.org/specs/rfc9111.html'
exit=0
HTTP/2 200, content-length: 178573, date: Wed, 04 Nov 2026 18:52:31 GMT
sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64
```

The body is byte-identical to the round-86
(`.ufo/waves/round-86/w1/ScribeKnowledge/s457-rfc9111.html`) and round-87
(`.ufo/waves/round-87/w1/ScoutAge/rfc9111.html`) retained copies of the same
URL, verified by byte comparison. Headers retained alongside the body.

## Touched surfaces

Written (this seat's wave directory only):

- `LANE/.ufo/waves/round-88/w1/ScribeVary/vary-matching.md`
- `LANE/.ufo/waves/round-88/w1/ScribeVary/sources-row.md`
- `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.html`
- `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.headers`
- `LANE/.ufo/waves/round-88/w1/ScribeVary.md` (this report)

Read: the round-88 contract, counter, case set and defect-queue counter;
`corpus/SOURCES.md`; `corpus/knowledge/cache-control-effective.md`;
`corpus/knowledge/cache-current-age.md`; `corpus/knowledge/response-header-expectations.md`;
`corpus/QUALITY.md`; `corpus/README.md`; `scripts/census` tooling
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`),
`scripts/corpus-contract.mjs`, `scripts/quote_class.py`,
`scripts/landed_check.py`; the r56 quote-truth counter
`.ufo/waves/round-56/c56_quote_truth.py`; the r63 flat-text recipe
`.ufo/waves/round-63/quote-class/extract_text.py`; retained bodies from
rounds 61, 81, 86 and 87; the `merge/kake` package at
`/home/vgpnk/Projects/shokuknow/merge/kake/` (read-only).

Not written: `corpus/`, `scripts/`, `SKILL.md`, `LOG.md`, `SCORECARD.md`,
`MANIFEST.json`, any sibling lane, `/home/vgpnk/Projects/shokuknow`, any
source tree, any PATH directory, any fleet-root tracked file.

## Out of scope

- Landing the entry, the row, the script or the README index row. L1 owns
  integration; the seat brief says finders and candidates only.
- Editing `corpus/SOURCES.md` or `corpus/knowledge/` to add the row.
- Writing `corpus/knowledge/vary-matching.md` under its production path.
- Scoring C2, closing C2, or any counter verdict claimed as this seat's.
- The `merge/kake` assimilation package: read-only here, and the round
  reports `Assimilation: none` on the contract's own grounds.
- The L1 candidate CLI's own review (another seat's).

## Defects found

Reported findings, lane-internal. Nothing outside admission.

**D-1 — the round's own control receipts are stale relative to the v3
counter.** *WITHDRAWN — this finding was checked and does not hold.*

- *What I first wrote:* that `controls/c2-selftest.txt` and the
  `ctl-c2-constant-*.txt` controls carry the v2 population
  (`mismatch=109 invalid=24`) while the counter prints the v3 one
  (`mismatch=112 invalid=21`).
- *What re-checking showed:* the committed controls and the live counter
  **agree**. `controls/c2-selftest.txt` prints `match=67 mismatch=109
  invalid=24` and `stub mismatch scores 109/200`; the live
  `python3 -B LANE/.ufo/waves/round-88/c88_vary.py --selftest` prints the
  same figures. The live counter's `RANDOM_SHA` is
  `52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981`,
  which is exactly the `random_sha256` in `controls/base-c2.txt` at HEAD
  and in all three `ctl-c2-constant-*.txt` controls
  (`match` 7/20+67/200, `mismatch` 9/20+109/200, `invalid` 4/20+24/200).
- *Why I got it wrong:* the v3 commit `52e41d2d` moved the `if star:`
  branch after the `normalise()` call and updated the counter, the
  contract's stub-score sentence, `base-c2.txt`, the three
  `ctl-c2-constant-*.txt` files and `c2-selftest.txt` **together, in one
  commit**. My first pass had read the pre-v3 files from the working tree
  before that commit landed in the lane (it landed at 15:58:05, after the
  wave dispatched at 15:52:15) and compared them against the post-v3
  counter. The v2 numbers (`mismatch=112 invalid=21`,
  `random_sha256 004a8eb7…`) are the numbers the counter printed *before*
  that commit; they are not what the committed controls say now.
- *Net:* **no defect.** The round's controls are consistent with the round's
  counter. I record the withdrawal because the seat brief asks for every
  defect found, and a wrong finding that is not retracted is worse than no
  finding.

**D-2 — the round-88 contract text and the committed controls disagree about
the C2 stub scores.** *WITHDRAWN — this finding was checked and does not
hold.* `contract.md` at HEAD states the constant-`mismatch` stub scores
`9/20 + 109/200` and the always-`invalid` stub `4/20 + 24/200`, which is
what the counter prints and what the committed controls record. The v3
amendment updated that sentence together with the counter. Same cause and
same withdrawal as D-1.

**D-3 — the frozen case set cannot distinguish the wildcard rule from the
validation rule, but the seeded population can.** No frozen case has a `*`
member together with a malformed header map (frozen cases with a `*` member:
7 and 8, both with valid sides; frozen cases with any malformed side: 19
only, and it has no `*`). So the 20 frozen verdicts alone cannot tell
"wildcard before validation" from "validation before wildcard" — both
orderings give the same answer on all 20. The reference implementation's
choice (validation first) is observable only in the 200 seeded cases, of
which exactly 3 exercise it: **r53, r150 and r193**, each with a `*` member
and a malformed side, each expecting `exit=1` with a `null` verdict.
This is a coverage gap in the hand-labelled set, not an error in it: the
frozen cases are exactly as frozen (sha256
`c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d`,
unchanged between v2 and v3), and the seeded population carries the
distinguishing cases. Reported because the seat brief asks for defects in
the round's own case set, and because a reader who scores only the frozen
20 would not know which precedence the reference implements.

**D-4 — the round's freeze amendment landed after the wave was
dispatched.** The v3 commit `52e41d2d` is dated 15:58:05; the wave was
dispatched at 15:52:15 (`w1.ready.dispatched` mtime) and the seat spec
was written at 15:50:40 (`w1-spec.json` mtime). The contract's own
freeze-history text says v3 was landed "still before any candidate was
scored and before any production byte changed", which is consistent — but
it was landed **after seats had been dispatched and were reading the
counter**. Any seat that read `c88_vary.py` before 15:58:05 saw the v2
reference (wildcard before validation) and the v2 `random_sha256
004a8eb7…`; any seat that read it after saw v3. This seat was in that
window and re-derived the semantics from the live file, but the hazard is
real for any seat that read the counter early and cached its numbers.
Not a contract violation, and the amendment was honestly recorded in the
contract's own freeze history; reported because the round moved a frozen
input under a running wave.

**D-5 — the lane's corpus-contract gate is already red at base.**
`node scripts/corpus-contract.mjs --root .` exits 1 with 3 findings, all on
`corpus/knowledge/meta-robots-directives.md` (missing `source:`,
`verified-at:`, `recheck:`). This is a pre-existing base-lane finding, not
caused by this seat; the drafted entry adds no new finding (verified
against a scratch mirror containing the drafted entry).

**D-6 — the `merge/kake` package's id collisions are exactly eight and do
not include S463**, but the package holds 129 staged rows in the range
S287–S415 while the lane registry now runs to S462. Any future adoption
run must renumber; the round reports `Assimilation: none`. Not a defect in
this round's work; recorded because the seat brief asks for defects in the
round's own counters and case set, and because the eight-id list was
re-derived here rather than taken on trust.

## Known limits

- **The entry records no score.** It does not claim `20/20`, `200/200` or
  `met=true` for anything. The counter selftest and the L1-candidate score
  in the *Gates* table are this seat's observations, recorded as such, and
  the entry text says so in its non-claims block.
- **The quoted spans are raw against the retained HTML body only.** The
  full MUST NOT sentence and the full `*` sentence are *collapsed-only*
  against that body, because the retained rendering puts the subject, the
  modal and the word `Vary` in separate markup nodes. The entry says this
  rather than presenting a de-marked sentence as a raw quote. The §4.1
  definition sentence is likewise printed in full in prose and quoted as a
  trimmed raw run, so that every quoted span stays inside the lane's
  25-unit ceiling.
- **Page-uniqueness was checked against the retained bodies present in this
  lane at run time** (round-81 RFC 9110 html and txt, the round-86 RFC 7234
  body, the round-61 S433 body, plus the round-86 and round-87 copies of
  this same URL). A page retained elsewhere in the fleet could share a
  span. The seven spans were each confirmed to occur exactly once *in this
  body*, which is the property a quote-truth counter can re-derive.
- **`used-by` cannot be satisfied by this seat.** `E11` will fire against
  the lane registry until L1 lands `corpus/knowledge/vary-matching.md`
  alongside the row.
- **`W04` is expected on the new row** — the same URL as S461 and S462, in a
  third scope. It is a warning and the lane's census still exits 0.
- **No tool was installed or upgraded.** Every command used here is
  pre-existing on the host (`python3`, `node`, `bash`, `curl`, `sha256sum`,
  `awk`/`gawk` inside the census script). Per the operator tooling
  directive, PACMAN is paused host-wide and nothing was installed, so there
  is no tool/channel/reason line to report. `/home/vgpnk/.omp/agent/RULES.md`
  was not needed for an install decision and was not consulted for one.
- **The `scripts/vary_match.py` checklist commands cannot run in the lane
  yet** — the file does not exist at base and is L1's to land. The three
  commands were exercised against L1's candidate at
  `.ufo/waves/round-88/w1/L1/vary_match.py`, and the expected outputs in the
  entry are the frozen reference implementation's verdicts for the same
  three inputs.
- **One assertion in the whole-package sweep failed, and it was a false
  positive in the check itself.** The check asked that *no* untracked file
  exist outside this seat's directory; the lane legitimately holds
  untracked files from sibling seats (`w1/ConnectorScope/`,
  `w1/CriticClaims/`, `w1/ExecCases/`, `w1/ExecDefects/`,
  `w1/ExecReader/`, `w1/ExecTrial/`, `w1/L1/`, `w1/MutReader/`,
  `w1/ReviewCounter/`, `w1/ReviewReader/`, `w1/ScoutSpec/`,
  `w1/ScribeLedger/`) and the dispatcher's own `w1.ready` /
  `w1.ready.dispatched` markers, all of which predate this seat's first
  write. The scope assertions that do hold: `git diff --name-only HEAD` is
  empty (no tracked file modified), `git status --porcelain corpus/
  scripts/ SKILL.md LOG.md SCORECARD.md` is empty (no production edit), and
  the only files this seat wrote are the five listed under **Artifact
  paths**.

## Artifact paths

- `LANE/.ufo/waves/round-88/w1/ScribeVary/vary-matching.md` — entry candidate
- `LANE/.ufo/waves/round-88/w1/ScribeVary/sources-row.md` — registry row candidate
- `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.html` — retained source body
  (178573 bytes, sha256 `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`)
- `LANE/.ufo/waves/round-88/w1/ScribeVary/rfc9111.headers` — response headers
- `LANE/.ufo/waves/round-88/w1/ScribeVary.md` — this report

Scratch root `/fast/scratch/hyaku/kake-r88/ScribeVary/` held the GET, the flat
text rendering, the table-driven rule checker, the row validator and the
census mirror; it was deleted after the receipts above were copied into the
wave directory. No `/tmp` path was used and no `/tmp` path is citable here.
