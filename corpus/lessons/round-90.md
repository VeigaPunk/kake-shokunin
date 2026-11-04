# Round 90 — kake: closing the round-89 routed defects and a conformance gate that tells stubs apart

Author: kake L1 (`KakeR90`). Base `209027f49959e2e2f0e16867a90a7bb38bbcd3f4`; freeze
`4ee62b18fec15af45654a9c8f8d5e7938d2bb796` (`.ufo/waves/round-90/freeze.md`). Outside
closure owns admission and the spot-check of this Gate.

## Gate

Sources opened this round (plain text, retained under `.ufo/waves/round-90/L1/src/`):

| URL | HTTP | bytes | sha256 | accessed (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T22:01:10Z |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T22:01:10Z |
| `https://www.rfc-editor.org/rfc/rfc8259.txt` | 200 | 28360 | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` | 2026-11-04T22:07:31Z |

Admits:

- S466 admit, A, RFC 9110 §5.5 lines 1606–1607: "Field values containing CR, LF, or NUL characters are invalid and dangerous" (12 words). Grounds the gate's every-header CR/LF refusal clause (`cr-unnominated`, `lf-unnominated-novary`) and its advisory NUL case.
- S467 admit, A, supersedes S463 for construction ground. RFC 9111 §2 line 252: "and is composed from, at a minimum, the request method and target URI" (13 words); lines 258–261: "Caches differentiate these responses by incorporating some of the original request's header fields into the cache key as well" (19 words). The §4.1 title (line 526) names key calculation.
- S468 admit, A, RFC 8259 §8.1 lines 485–486: "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8" (18 words); §7 lines 429–431 "the characters that MUST be escaped: quotation mark, reverse solidus, and the control characters (U+0000 through U+001F)" (17 words). Grounds two advisory cases only.

Rejects:

- Reject (proposition): "the round-89 contract's byte layout is what RFC 9111 specifies". S467 §2 composes the key from at least method and target URI; it gives no layout, and the contract omits the method. Layout, escaping and the `GS` absent marker stay adapter conventions.
- Reject (proposition, round-89 MutKey §5.2): "M37 is equivalent because names are tokens and cannot contain `%`". RFC 9110 §5.6.2 `tchar` (S465, `rfc9110.txt` lines 1735–1737) includes "%", so `vary: "A%1F"` with the field absent gives `a%251f` under the contract and `a%1f` under M37; the gate case `name-percent-absent` refuses M37 at the carrier.
- Reject (row candidate): adding NUL to the contract's refusal list this round. S466 says a recipient MUST reject or replace NUL with SP; either choice changes the shipped candidate's contract, so it is routed (R90-2), not decided by the gate. Flip: an explicit contract revision round.

## Registry

- Rows added: S466, S467, S468 (all tier A, kind spec, status mined, recheck 180d). 202 → 205 rows.
- Rows touched: none. S463 is byte-identical (CORPUS.md rule 2: its scope cell is immutable;
  the correction is the new row S467 whose `teaches` opens `supersedes S463 —`). S463's
  status stays `mined`: the match-profile scope it still carries is correct for
  `vary-matching.md`.
- Census `validate --root … kake`: exit 0 before (`controls/census-before.txt`, 26 × W04).

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | False equivalence claim in a mutation report | round-89 `w1/MutKey.md` §5.2 calls M37 equivalent ("names … cannot contain `%`"); `%` is a tchar (S465) | none (round-89 counter had no `%`-name case) | gate case `name-percent-absent`; M37 refused at carrier (`controls/after-c2-carrier.txt`, M37 line `met=false`) |
| 2 | Ledger item list contradicts its count | `SCORECARD.md:5518` and `:5535` say items B, C, D, E, F closed at `f62e7954` (`LOG.md:3038–3041` states only the count, as ReviewC1 found); the frozen c89 counter re-run on a clone at `f62e7954` reads `open=5 closed=1` with only E closed (`controls/r89-c1-at-f62e7954.txt`) | round-89 spot-check D89-2 | C1 item D2: a correction counts only if its receipt re-runs; forgeries D2a/D2b/D2c stay open (`controls/ctl-c1.txt`) |
| 3 | Counter parsed the quoted superseded value as the reading | first control run: positive fixture stayed `open=1` because `OC_RE.search` took `open=5 closed=1` from the quoted statement (`controls/ctl-c1-v0-before-parse-fix.txt`) | the positive control (pre-freeze) | last reading after `f62e7954`; positive fixture then `open=0 closed=3` and every forgery still open (`controls/ctl-c1.txt`) |
| 4 | Sandbox denied the interpreter's own import machinery | first gate draft killed every subject on `os.listdir` (`clauses=0/6` for the shipped candidate) | a sample run before the carrier commit | listing allowed only under stdlib roots; neg-oracle-path-import and neg-exec-source still die with exit 97 |
| 5 | A hand case decided a point the contract leaves open | first gate draft refused non-UTF-8 input as a contract clause; all four frozen positives accepted it. Diagnosis corrected by ReviewGate F4: the cause was the gate's own `LC_ALL=C.UTF-8` child environment (C-family locale → stdin `surrogateescape`), not the candidates; under `en_US.UTF-8` they refuse | sample run before the carrier | moved to an advisory line grounded on S468 and never scored (ReviewGate: a legitimate reading, wrong diagnosis); after the wave the sandbox decodes stdin as strict UTF-8 whatever the locale, and the advisory passes for the positives |
| 6 | Contract example contradicts the JSON it is sent as | `.ufo/waves/round-89/c2-contract.md` example 5 says the separators are carried raw; RFC 8259 §7 requires escaping and the candidate refuses raw (`invalid_input: input is not valid JSON`) | none | gate sends them escaped; advisory `raw-control`; routed R90-3 |
| 7 | Round scratch at the lane root | `?? baseclean.out` (round-89 spot-check D89-1) | spot-check D89-1 | relocated byte-exact to `.ufo/waves/round-90/inherited/baseclean.out`; C1 item D1 checks bytes and the live tree (forgeries D1a/D1b open) |

Disclosure: the gate (production) was developed after the freeze and before the carrier
commit; mistakes 4 and 5 were fixed in that window. The frozen counter, its predicate,
the population pins and the positive/negative labels were not changed after freeze.

## Routed

- R90-1: the contract names no input encoding; the gate now decodes stdin strictly, so the
  `utf8-required` advisory reads the candidate's own refusal (it passes after the wave fix).
- R90-2: NUL in a field value (S466) is kept by the candidate; the contract is silent.
- R90-3: contract example 5 wording ("raw") versus RFC 8259 §7.
- R90-4: the key omits the request method (S467 §2); adapter limit.
- R90-5: two JSON members with the same header name (`{"a":"1","a":"2"}`) are kept by every
  frozen positive (last one wins); the contract refuses names equal case-insensitively but does
  not define duplicate JSON members (round-89 routed item). Advisory `dup-json-member`.
- Carried: RC-1…RC-10 for the frozen round-89 C1 counter stay as recorded; the round-89
  counter is not repaired after scoring. The round-89 L0 questions stay open.

## Operator-decision queue (considerthese/2026-10-26.md, Part 2 proposal 3)

The proposal (operator-authored, 2026-10-26): keep routed items that need the operator,
with how many rounds each has waited, at the top of the report. Grounded by reading
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` on 2026-11-04: every `kake |` line
since round 58 is listed; a grep of the file for non-question lines naming kake found
no recorded answer to any of them. Waited = 90 − filing round.

| Filed (l0-questions.md line) | Question (short) | Rounds waited |
|---|---|---|
| round-58 (180) | §10 quarantine vs frozen-claim conflict, absent-defect slice | 32 |
| round-59 (181) | calibration sub-axis ownership | 31 |
| round-59 (182) | CJK reading of the ≤25-word quote rule | 31 |
| round-65 (232) | L2 floor on the Windows host | 25 |
| round-67 (243) | three host-bound counter repairs (frozen bytes) | 23 |
| round-69 (260) | freshness-sweep `--offline` exit 1 on lowercase `~/projects` citations | 21 |
| round-71 (272) | attack-share role set for the ≥25 % rule | 19 |
| round-72 (277) | S303/S304/S352 cited but unheld | 18 |
| round-86 (294) | D84-4 literal L2 planner seat vs validator | 4 |
| round-89 (299–301) | C1 item A tag rule; C2 guard amendment; C2 instrument revision | 1 |

Round 90 bears on line 301: the conformance gate is the instrument revision that
line asked for, built as a new tool rather than a repair of the frozen round-89
counter, so that question can be answered "superseded by round 90" without any
ruling on round 89's frozen bytes.
