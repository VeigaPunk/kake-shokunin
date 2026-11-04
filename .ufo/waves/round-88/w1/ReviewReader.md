# ReviewReader — kake round 88, C2 (freshness) review

Non-author reviewer seat. Lane `kake-shokunin`; one v1 wave, 14 seats. My only writes are
this file and `.ufo/waves/round-88/w1/ReviewReader/` (plus scratch, deleted). No production
edits, no commits, no git/jj mutation, no delegation, no GET (my item named no URL), no tool
installs (Python 3.14.8 preinstalled).

Pins used throughout (sha256 of bytes): contract **v3** `639035d3…`, counter **v3**
`e4cf5ad9…`, case set `c461cbd8…`, my reader `cbfcf50f…`, L1 candidate `2da573d3…`,
ExecReader candidate `fdceef47…`. Full list in `w1/ReviewReader/hashes.txt`.

## 0. Freeze timing (it changed under this seat)

| time (-03:00) | event | bytes |
|---|---|---|
| 15:44:46 | `vary-cases.json` written | `c461cbd8…` |
| 15:51:29 | `w1.ready` | — |
| 15:52:15 | `w1.ready.dispatched` — wave dispatched | — |
| 15:56:39 | `w1/L1/vary_match.py` written (enters history in the v3 commit) | `2da573d3…` |
| ~15:57 | my `indep.py` first written | later `cbfcf50f…` |
| **15:58:05** | **freeze amendment v3, commit `52e41d2d`** — reference precedence changed, contract rewritten, base/stub receipts regenerated, L1 candidate added | contract `639035d3…`, counter `e4cf5ad9…` |
| 15:59:20 | `w1/ExecReader/vary_match.py` written | `fdceef47…` |

I read the **v2** contract (`b8f7db94…`) and **v2** counter (`285bca22…`) at 15:54–15:56, i.e.
before v3 landed; I re-read both at 15:58+ and every behavioural receipt here is against v3.
My reader was written against the v2 text, but v3's added rule ("input validation runs before
the wildcard rule") is what I had already implemented, so no verdict moved. The v3 commit is
honest about itself in `contract.md`, but a seat dispatched at 15:52 and reading immediately
sees a different counter than the one that scores it; receipts must be pinned by hash (mine are).

Order of reading is recorded in `w1/ReviewReader/read-order.txt`: contract → counter →
case set → defect queue → candidate-existence check → my implementation → (only later) the
L1 and ExecReader candidates. No candidate bytes were read before `indep.py` existed. Exact
statement: L1's candidate *file* already existed at 15:56:39, but my seat named ExecReader's
candidate and the production path; I did not check `w1/L1/` and did not read it until ~16:04.

## 1. Independent implementation and what it scores

`w1/ReviewReader/indep.py` — written from RFC 9111 §4.1 and RFC 9110 §5.1/5.2/5.3/5.5/5.6.1
plus the declared profile. Same CLI contract as `contract.md` (one JSON object on stdin;
`match`/`mismatch` on stdout, exit 0, empty stderr; `invalid_input:` on stderr, exit 1,
empty stdout). Flags expose the spec-true variants the declared profile does not name:
`--refuse-empty-elements`, `--refuse-empty-list`, `--refuse-combined-lines`, `--keep-ctl`.

| implementation | flags | frozen | random | exit | receipt |
|---|---|---|---|---|---|
| `indep.py` default (spec-faithful) | — | **19/20** | **187/200** | 1 | `receipts/c88-score-indep-default.json` |
| `indep.py` + profile flags (wrapper) | refusal policy | 20/20 | 200/200 | 0 | `receipts/c88-score-profile-mode.json` |
| L1 candidate `w1/L1/vary_match.py` | — | 20/20 | 200/200 | 0 | `receipts/c88-score-L1-candidate-v3.json` |
| ExecReader candidate `w1/ExecReader/vary_match.py` | — | 20/20 | 200/200 | 0 | `receipts/c88-score-ExecReader.json` |

Commands (from lane root, `W=$PWD/.ufo/waves/round-88`):

```
python3 -B $W/c88_vary.py --selftest                          # exit 0, 17/17  (receipts/c88-selftest.txt)
python3 -B $W/c88_defect_queue.py --selftest                  # exit 0, 11/11  (receipts/c1-selftest.txt)
python3 -B $W/c88_vary.py --tool $W/w1/ReviewReader/indep.py --work <scratch>/work-default   # exit 1, 19+187
python3 -B $W/c88_vary.py --tool <scratch>/profile_mode.py   --work <scratch>/work-profile   # exit 0, 20+200
python3 -B $W/c88_vary.py --tool $W/w1/L1/vary_match.py      --work <scratch>/work-l1-v3       # exit 0, 20+200
python3 -B <scratch>/blobs/c88_v2.py --tool $W/w1/L1/vary_match.py --work <scratch>/work-l1-v2 # exit 1, 20+197
python3 -B $W/c88_vary.py --tool $W/w1/ExecReader/vary_match.py --work <scratch>/work-exec     # exit 0, 20+200
```

The gap between the first two rows is the subject of finding **S2**: the frozen metric is only
satisfiable by refusing inputs that RFC 9110 §5.6.1.2 tells a recipient to parse.

## 2. My expected-verdict table vs `vary-cases.json`

`w1/ReviewReader/expected-table.json` (derived from the spec text and the declared profile; each
row carries the deciding sentence and a separate `spec_note`). Compared mechanically:
**20/20 agree, 0 disagreements** (`frozen-compare.json`, `table_vs_file.agree=20`).

Four labels need a note rather than a correction:

- **case 14** (`Vary: ""` → exit 1). The basis is accurate as an adapter statement, but the spec
  reading is *match*: RFC 9110 §5.6.1.2 says a recipient "MUST accept lists that satisfy
  `#element => [ element ] *( OWS "," OWS [ element ] )`" — an empty string is a zero-element
  list, and §4.1's conjunction over zero nominated fields is vacuously true. The refusal is a
  declared adapter choice, not a spec rule; see S2.
- **case 3/10/18** are over-conservative by declaration (no value case-folding, no reordering,
  no internal-whitespace folding). §4.1 permits the third transformation but does not require
  it, so the mismatch labels are sound; my table records the field-specific alternative in
  `spec_note`.
- **case 16** cites §5.2 for the `", "` combine. §5.2 defines the combined field value
  ("concatenated in order, with each field line value separated by a comma"); the sentence that
  permits a recipient to insert OWS is §5.3 ("separated by a comma (",") and optional whitespace
  (OWS)"). Citation nit, not a wrong label.
- Case set is *not blind to me*: the mandated reading order put `vary-cases.json` before any
  implementation work, so this table is not an independent second labelling. It is a
  derivation check, not a blind replication. Stated as a limit.

## 3. Behavioural differential (20 frozen + 22 fresh + 6 extra = 48 inputs)

Fresh inputs live in `w1/ReviewReader/fresh.json` (ids F1–F22, each with the deciding rule) and
the six extra probes in `w1/ReviewReader/candidate-diff-*.json` (X1–X6).

**vs ExecReader's candidate (`fdceef47…`): 36/48 agree, 12 disagreements.**
**vs L1's candidate (`2da573d3…`): 35/48 agree, 13 disagreements.**

Every disagreement is one of five classes; in all of them the candidate equals the counter's
reference, so the disagreement is with my spec-faithful default:

| class | inputs | ref / candidate | mine | which side is spec-correct |
|---|---|---|---|---|
| empty `Vary` value | case 14, F17 | invalid | match | **mine** — zero-element `#field-name` list; §5.6.1.2 |
| empty list element in `Vary` | F1, F2 | invalid | match | **mine** — "MUST parse and ignore a reasonable number of empty list elements" (§5.6.1.2) |
| two JSON keys naming one field in different case | F4, F5, X2 | invalid | match | **mine** — §5.2 defines the repeated field name's value as the in-order concatenation |
| `[]` as a field value | F6, F7 | invalid | match | **mine** under "zero field lines = absent"; the JSON shape is undeclared, so the refusal is *defensible adapter strictness*, not spec-mandated |
| `*` + empty element (`Vary: "*,",`) | F8 | invalid | mismatch | split: §4.1 says a `*` member always fails and §5.6.1.2 says ignore the empty element (**mine**); v3's declared precedence says validate first (**candidate**). Both defensible; the declaration wins for scoring |
| CR at a value edge (`"gzip\r"` vs `"gzip"`) | X3 | mismatch | match | **mine** — §5.5 gives reject (invalid) or replace-with-SP (match); mismatch is neither branch |
| unknown extra input key | X1 | L1: invalid, ExecReader: match | match | adapter shape only; the contract names three keys and does not say extra keys are refused. L1's refusal is defensible; no spec bearing |

No disagreement was found on: name case-insensitivity, OWS trimming, absent-both, present-one,
`*` alone, byte-different values, quoted-string interiors, obs-text, non-nominated fields,
single-member lists, duplicate `Vary` members.

## 4. Attacking the conservative asymmetry

### 4a. The intended profile admits no unsound `match` — argument

RFC 9111 §4.1 (retained body `w1/ScribeVary/rfc9111.html`, sha256 `999f4013…`, fetched by that
seat; verified by me):

> The header fields from two requests are defined to match if and only if those in the first
> request can be transformed to those in the second request by applying any of the following:
> adding or removing whitespace, where allowed in the header field's syntax; combining multiple
> header field lines with the same field name; normalizing both header field values in a way that
> is known to have identical semantics, according to the header field's specification …

(Line breaks and bullet markers normalised to a single block; wording unchanged.)

The declared profile applies only the first two, never rewrites value characters, and compares
the remainder byte-for-byte. A `match` therefore implies that one side's significant bytes can
be turned into the other's by whitespace removal that the field's syntax allows plus line
combination — both explicitly permitted. Identity is the zero-step case, so reflexivity holds.
Absence and the `*` rule are handled separately and correctly (`absent both` / `absent one` /
`always fails`).

Adversarial search: 20 000 generated payloads (`attack.json`, seed 88 777; case-variant keys,
lists, `[]`, ints, `*`, empty members, CR/LF/NUL, quotes, tabs, obs-text, long values). Every
`match` from the reference (1 047) and from my reader (4 229) was checked against a
significant-bytes oracle (CTL→SP per §5.5, per-line edge OWS, comma join, OWS around commas
collapsed). **0 violations.** A value-folding reader *would* be unsound, and the profile's
refusal to use the third transformation is what prevents it: e.g.
`Authorization: "Bearer AbC"` vs `"bearer abc"` → both readers say `mismatch`; a case-folding
reader would say `match` across two distinct credentials.

### 4b. …but the *implementation* does produce an unsound `match`: the trailing-LF token

`c88_vary.py:40` compiles `TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")` and
`:44 is_token` uses `TOKEN.match`. In Python `$` also matches **before a final newline**, so a
field name ending in one LF is accepted as a token. `reference` uses `is_token` for `Vary`
members and for both header maps; `w1/L1/vary_match.py` copies the same regex (`:22`) and the
same `TOKEN.match` uses (`:41`, `:53`).

Measured (`receipts/lf-quirk.json`; `is_token("accept-encoding\n") == True`):

| probe | input | reference | L1 cand. | ExecReader | mine | required |
|---|---|---|---|---|---|---|
| P1 | `vary="accept-encoding\n"`, stored `gzip`, presented `br` | **match** | **match** | invalid | invalid | mismatch or invalid |
| P2 | same member inside a list, values differ | **match** | **match** | invalid | invalid | mismatch or invalid |
| P7 | `vary="*\n"`, values differ | **match** | **match** | invalid | invalid | mismatch (star) or invalid |
| P8 | `vary="*\n"`, both maps empty | **match** | **match** | invalid | invalid | mismatch (star) or invalid |

Why `match` is not permitted: §5.5 says "a recipient of CR, LF, or NUL within a field value MUST
either reject the message or replace each of those characters with SP before further processing
or forwarding of that message".
Replacing the LF in `"*\n"` gives `"* "`, and OWS removal leaves the member `"*"`, for which §4.1
says "A stored response with a Vary header field value containing a member "*" always fails to
match." Replacing the LF in `"accept-encoding\n"` names the real field, whose values differ.
Both permitted branches exclude `match`; the wildcard rule can be bypassed with a single
trailing newline. This falsifies the profile sentence "a `match` verdict is always produced by
transformations §4.1 permits" and the knowledge entry's "every `match` it produces is a
transformation the source permits", for the reference and for the L1 candidate as shipped.

The population cannot see it: 0 frozen and 0 random cases carry LF (`join-probe.json`), and the
17/17 selftest never tests one.

## 5. Reference audit against the spec and its declaration (13 inputs)

`w1/ReviewReader/reference-audit.json` / `receipts/reference-audit.txt`. Counts: 5 reference
verdicts equal the declared expectation, 8 inputs are undeclared by the profile, 1 equals the
spec expectation on all readings (A10, the duplicate-member control), **0 contradictions with
the v3 declaration** (the v2↔v3 precedence change resolved the one I first found).

| id | input | ref | declared | spec | judgment |
|---|---|---|---|---|---|
| A1 | `Vary: "accept-encoding,"` | invalid | undeclared | match | over-refusal; violates the §5.6.1.2 MUST |
| A2 | same field name twice in different case, both sides | invalid | undeclared | match | over-refusal of the §5.2 combined value |
| A3 | field value `[]` both sides | invalid | undeclared | match | over-refusal (adapter shape undeclared) |
| A4 | `Vary: "*,"` | invalid | invalid | mismatch | follows v3 precedence; contradicts §4.1 star + §5.6.1.2 |
| A5 | `"a\rb"` vs `"a b"` | mismatch | mismatch | match or invalid | §5.5 MUST not implemented |
| A6 | `"gzip,br"` vs `["gzip","br"]` | mismatch | mismatch | match | OWS around list commas is insignificant (§5.6.1.2); conservative |
| A7 | `Vary: ""` | invalid | undeclared | match | as case 14 |
| A8 | `["gzip",""]` vs `"gzip"` | mismatch | mismatch | match | empty element ignored (§5.6.1.2) |
| A9 | `Vary: "a, ,b"` (OWS-only element) | invalid | undeclared | match | as A1 |
| A10 | duplicate `Vary` members, differing case | match | match | match | control, agrees |
| A11 | non-token *unrelated* key in one map | invalid | undeclared | invalid or match | whole-message refusal; safe, narrow |
| A12 | `Vary: "*\n"` | **match** | undeclared | invalid or mismatch | **unsound** — see 4b |
| A13 | map keys ending in LF | match | undeclared | invalid | invalid message judged reusable |

## Findings (severity ordered)

**S1 — HIGH — unsound `match`: a trailing LF is accepted as a token character** (`c88_vary.py:40,44,84`;
`w1/L1/vary_match.py:22,41`). `Vary: "*\n"` → `match` (wildcard bypassed) and
`Vary: "accept-encoding\n"` with `gzip` vs `br` → `match`. Evidence `lf-quirk.json` P1/P2/P7/P8;
`join-probe.json`. Spec: §5.5 reject-or-replace + §4.1 star rule; neither branch yields `match`.
Untested by the 20 frozen and 200 random cases; the 17/17 selftest cannot catch it. Fix direction
(not applied): `fullmatch`/`\Z` (or an explicit char-class check) and reject-or-SP-replace
CR/LF/NUL before any name test.

**S2 — HIGH (claim level) — the frozen metric scores a recipient MUST as a failure.** Case 14 and
13/200 seeded cases (`7` empty list element, `4` empty `Vary`, `2` `[]` value) are labelled
`invalid`; a reader that follows RFC 9110 §5.6.1.2 ("MUST parse and ignore a reasonable number of
empty list elements … MUST accept lists that satisfy …") scores **19/20 + 187/200 → `met=false`**
(`receipts/c88-score-indep-default.json`). C2 is therefore satisfiable only by refusing what the
RFC says to parse. The v3 profile declares *precedence* but not the refusal catalogue, so the
scored semantics are underspecified relative to the claim. Refusals are safe (never an unsound
`match`), but they are not "conservative" in the §4.1 sense — they decline to answer.

**S3 — MEDIUM — the `", "` join spelling is load-bearing and over-specified.** The profile fixes
`", "`; RFC 9110 §5.3 permits "a comma (",") and optional whitespace (OWS)". My reader with
`JOIN=","` scores **18/20 + 186/200** (`join-probe.json`) — on top of case 14 it loses case 16, and
it loses r106, one of the only two random cases that carry a multi-line value. A spec-permitted serialisation fails the claim.

**S4 — MEDIUM — freeze amendment after dispatch, oracle aligned with the author's candidate.**
Commit `52e41d2d` (15:58:05) rewrote the reference precedence; the same commit added
`w1/L1/vary_match.py` (written 15:56:39). L1's candidate scores **20/20 + 197/200 against v2**
(fails r53, r150, r193) and **20/20 + 200/200 against v3**. The random half is consequently a
regression test between two author artefacts, not an independent spec oracle; the frozen half is
unaffected by the change. Allowed by the letter of the contract ("not edited after a seat
scores"), but seats dispatched at 15:52 saw v2 bytes, so every receipt must be hash-pinned.

**S5 — MEDIUM — CR/LF/NUL in *values* are compared raw** (`reference`, and both candidates). The
§5.5 MUST is reject-or-replace; the reference does neither, returning `mismatch` where the replace
branch mandates `match` (A5; `stored "gzip\r"` vs `"gzip"` → `mismatch`, X3). Safe direction
(no unsound `match`), but it is a conformance defect in the frozen oracle.

**S6 — LOW — undeclared over-refusals**: case-variant duplicate map keys, `[]` values, non-token
unrelated keys, and (L1 only) unknown extra input keys. Each is safe and each narrows the
reader's capability; none is derivable from §4.1 or §5.2.

**S7 — LOW — control blindness and unpinned digests.** The counter's selftest covers ids,
well-formedness, the three constant stubs, reference-vs-frozen agreement and a silent stub; it
does not cover LF names, empty `Vary` elements, `[]`, CR/LF values or case-variant keys — exactly
the classes where the reference diverges. `cases_sha256`/`random_sha256` are printed but never
compared to a constant inside the counter, so a case or generator edit is silently
self-consistent; the "frozen" digests live only in receipts.

**S8 — NIT — case 16 cites §5.2 for the OWS-bearing combine sentence, which is §5.3** in RFC 9110.

## Residual risk and verification gaps

- **C2 as frozen cannot be met by a reader that follows RFC 9110 §5.6.1.2's MUST.** L1 must choose:
  ship the refusal policy (passes, but the profile must then declare the refusal catalogue), or
  keep the spec reading and restate the target. I did not edit anything; this is a decision for L1.
- **S1 is a live soundness defect in the reference and in L1's candidate**; if L1 ships
  `w1/L1/vary_match.py` to `scripts/vary_match.py`, the carrier inherits it. The frozen population
  cannot detect it, so a green C2 receipt is not evidence of soundness.
- Not run: any interpreter other than CPython 3.14.8 (ExecReader's receipt claims 3.12–3.15 for
  the digest; I did not re-run); the C1 items at a carrier revision (my seat is the C2 reader; I
  ran only the C1 counter's selftest, 11/11); fuzzing beyond 20 000 payloads; any HTTP/Live
  surface (not claimed).
- Quotes: RFC 9111 §4.1 from the retained body fetched by ScribeVary this round (sha verified);
  RFC 9110 §5.2/5.3/5.5/5.6.1 from `.ufo/waves/round-36/sources/S088.txt` (fetched by an earlier
  round). No GET by this seat — my item named no URL, so no fetch is claimed.
- Candidate scopes: `w1/L1/vary_match.py` and `w1/ExecReader/vary_match.py` are peer artefacts;
  they can change after my pin. Scores above are for sha `2da573d3…` and `fdceef47…`.

## Artefacts

`w1/ReviewReader/indep.py` (reader), `expected-table.json`, `frozen-compare.json`,
`random-divergence.json`, `fresh.json`, `attack.json`, `reference-audit.json`,
`candidate-diff-l1.json`, `candidate-diff-execreader.json`, `join-probe.json`, `lf-quirk.json`,
`read-order.txt`, `hashes.txt`, instruments (`harness.py`, `audit.py`, `cand_diff.py`,
`join_probe.py`, `lf_probe.py`, `profile_mode.py`), and `receipts/` with the raw scorer output,
selftests, reference-audit text and the v2↔v3 diff.
