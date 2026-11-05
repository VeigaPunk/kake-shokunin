# ScribeEntry — round 96 (kake, hyaku run 15, attempt 1), wave 1

Seat: scribe. Deliverables under `.ufo/waves/round-96/w1/ScribeEntry/`.
Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Round base `bde9869144f69c5a459c0d2c93f5135922fe3a8d`; instruments commit
`7ae3e9b07e2435f7fde6e73838d9fa14488b8dda`; freeze commit
`049e8eca2f0fa5e981232eb4efe367357dce578c`.

**VERDICT: SCRIBE quotes=13/13 located**

## What this seat produced

Three deliverables, all drafts for the L1 to integrate (this seat writes nothing
outside its own seat directory):

| File | What it is |
|---|---|
| `.ufo/waves/round-96/w1/ScribeEntry/knowledge-entry.md` | The draft of `corpus/knowledge/revalidation-exchange.md`: the C2 knowledge entry, provenance trio on lines 1-3, two-stage decision, the C1-C6 clause table with RFC-exact vs lane-convention labeled, 13 located quotes, and a closing exclusions paragraph |
| `.ufo/waves/round-96/w1/ScribeEntry/s480-row.md` | The finalized S480 SOURCES row (11 cells) with its cell-by-cell check, its source/quote grounding, its census receipts, and three findings for the L1 |
| `.ufo/waves/round-96/w1/ScribeEntry/quotes-verified.txt` | The per-quote line + word count receipt: 13 quotes, `violations=0`, exit 0 |

Three checkers produced the receipts (all read-only against the lane; all exit 0):

| Checker | Command | Result |
|---|---|---|
| `verify-quotes.py` | `python3 -B verify-quotes.py` | `violations=0 quotes=13`, rc 0 |
| `check-census.py` | `python3 -B check-census.py` | control rc 0, with-S480 rc 0, zero E-findings, `violations=0`, rc 0 |
| `check-e3.py` | `python3 -B check-e3.py` | prospective E3 clean, rc 0 |

Plus `instrument-digests.txt`, `body-digests.txt` and `census-baseline.txt` as
supporting receipts.

## Behavior — the knowledge entry

**Provenance trio, lines 1-3, byte-exact to the seat spec** (verified by comparing
the draft's first three lines against the spec strings extracted from
`.ufo/waves/round-96/w1-spec.json`):

```
source: S480 <https://www.rfc-editor.org/rfc/rfc9111.txt> §4.3, lines 812-949 (retained sha256 aeb52adb……)
verified-at: 2026-11-05
recheck: 180d
```

All three comparisons returned True. Lines 4-5 add `ground:` and `scope:` in the
lane's exemplar shape (both `conditional-request-evaluation.md` and
`stored-response-reuse.md` carry the same five-line head).

**The two-stage decision** is the entry's spine: construction (§4.3.1, which
validators the cache sends) then handling (§4.3.3, what the received status means
for the stored response). The entry says why the stages are separate — a status code
is only a validation answer to a request that carried a validator.

**The clause table C1-C6** carries a two-column labeling, RFC-exact ground vs lane
convention, one row per contract clause, and follows the contract's own
distinctions rather than restating them:

- **C1** validator selection — RFC-exact: the stored entity tags MUST be sent (848-850)
  and a cache's own revalidation uses If-None-Match, which takes precedence over
  If-Modified-Since (888-891), so If-Match and If-Range are never constructed. Lane
  convention: the decision names, and "no validator stored" being a refusal rather
  than an empty conditional request.
- **C2** both validators together — RFC-exact: the Last-Modified SHOULD (852-854) and
  the both-validators sentence (861-862). Lane convention: treating the SHOULD as
  sent — the RFC makes it conditional, the contract decides the condition away.
  The contract itself labels C2 a lane convention; the entry keeps that label.
- **C3** a 304 — RFC-exact: the stored response can be updated and reused (935-936).
  Lane convention: the decision name, and §4.3.4 left out.
- **C4** a 5xx — RFC-exact: the permission (944-949). Lane convention: reporting the
  permission rather than choosing a branch.
- **C5** any other 200-499 — RFC-exact: the cache MUST use the full response (940-941).
  Lane convention: deciding the class from the status code alone, with the
  payload-less-204 case named as an exclusion.
- **C6** refusals — nothing in §4.3 fixes an input grammar; the whole refusal set is
  the lane's, including the S034 duplicate-key convention.

**Every quote is ≤ 25 words and carries its line number.** 13 quotes, R1-R13, each
a raw substring of the retained RFC 9111 body, each confined to its stated line
span, each present verbatim in the draft. Word counts are whitespace-separated
tokens, all 11-25. The six quotes the contract v1 names (848, 852, 861, 935, 938,
944) are R4, R5, R6, R8, R9 and R11.

**The citations are S480 plus the re-read rows S456 and S476**, and the entry says
which is which: S480 opens §4.3.1 and §4.3.3; S456 (re-read) holds the §4.3.1 and
§4.3.4 spans R3 and R13 come from; S476 (re-read) holds the §4.3.2 span R7 comes
from. This is the entry's own distinction, matching what those two rows' `anchor`
cells already say (S456's anchor names "§4.3.1 lines 812-850 ... §4.3.4 lines
986-988"; S476's anchor names "§4.3.2 heading plain-text line 866 ... lines
887-891").

**The closing paragraph is an explicit exclusions paragraph**, naming all four
required exclusions: **no storage** (nothing stores, indexes, evicts or selects a
stored response), **no keys** (no cache key is computed and no key identity is
named), **no merged-field update** (§4.3.4's merged header field set of a 304 is
out of scope, with lines 986-988 cited), and **no live cache** (no claim about any
deployed cache, CDN, proxy or browser). It closes by separating the two permissive
decisions from observations: `may-reuse-stored` reports a permission the RFC grants,
`construct` reports validators a cache would send, not traffic on a wire.

## Behavior — the S480 row

The row is finalized from ScoutRFC's opened-source draft, with the scope cell
extended to name S456's reading alongside S476's and S470's, the anchor cell's line
ranges corrected to the body's actual bullet extents, and the `used-by` cell set to
the two paths the seat spec names.

- **11 cells.** `len(row.split('|')[1:-1]) == 11` → True.
- **No pipe characters in any cell.** Every pipe in the row line is a column
  delimiter; no cell holds a literal or escaped pipe.
- **`kind` spec, `tier` A**, scoped to §4.3.1/§4.3.3 only.
- **`status` `queued`** — the freeze's Sourced-claim requirement reserves the `mined`
  decision for the L1, so the status is left as it is.
- **`opened` 2026-11-05, `recheck` 180d.**
- **`used-by`** `corpus/knowledge/revalidation-exchange.md, corpus/lessons/round-96.md`
  — the knowledge entry and the round-96 lesson.
- **The `teaches` cell carries a verbatim quote**, "In most cases, both validators
  are generated" (7 words), which is a raw single-line substring of the body at
  plain-text line 861.

**Census-clean, measured.** `check-census.py` builds two lane-shaped scratch
mirrors (the control's `corpus/SOURCES.md` is `cmp`-identical to the lane's, rc 0),
inserts the row at line 226 after S479, and runs the fleet's read-only
`scripts/sources-census.sh` against each:

- control `validate` → **rc 0**, `mirror ok`, zero E-findings;
- with-S480 `validate` → **rc 0**, `mirror ok`, zero E-findings;
- the only added line is `W04 S480 duplicate url www.rfc-editor.org/rfc/rfc9111.txt
  across scopes` — the pre-existing duplicate-URL warning class that S456, S467,
  S469, S470 and S476 already carry for the same URL at different scopes. A
  warning, not an E-finding; the exit stays 0;
- `census` with S480 → rows **217** (216 at base), tier.A 192 (191),
  status.queued 9 (8), status.mined 186, status.rejected 22, FLEET.missing 0.

The lane's own census at base reads rows 216 / tier.A 191 / queued 8 / mined 186,
matching (`census-baseline.txt`, rc 0).

## Evidence — every command and its observed result

| Command | rc | Observed |
|---|---|---|
| `python3 -B verify-quotes.py` | 0 | `violations=0 quotes=13`; 13/13 rows `ok`, each with `span=True file=True draft=True words_ok=True`; `table_ids=13 missing_in_table=none extra_in_table=none` |
| `python3 -B check-census.py` | 0 | `row cells: 11 (want 11)`; `no literal or escaped pipe in any cell: yes`; `row sha256: b8f64b015447f6af984acb0cc1496d4495241d9de608352259b619a1e38451ce`; control mirror `cmp` rc 0; both census runs rc 0 with zero E-findings; `violations=0` |
| `python3 -B check-e3.py` | 0 | prospective E3 `problems: none`; `source: lines in the first 8 lines: 1`; `violations=0 (prospective E3 clean)` |
| `node scripts/corpus-contract.mjs --root .` (mirror with the draft entry at `corpus/knowledge/revalidation-exchange.md`) | 0 | `result: 0 findings · 84 knowledge entries · 90 lane lessons · 80 skipped · 0 errors` |
| `sha256sum` of both RFC bodies + `cmp` | 0 | both `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, 84477 bytes each, `cmp_rc=0` |
| `sha256sum` of the frozen instruments | 0 | `c96_selfassess.py` `a282da65…`, `c96_reval.py` `ec40aec1…`, `reval-contract-v1.md` `65f0a347…`, `c95_selfassess.py` `8fd27d62…` — all equal to `controls/instrument-sha256.txt`; **no instrument was amended** |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (lane, read-only) | 0 | `kake ok`, zero E-findings, only the pre-existing W04 warning class |

The six contract-named clause quotes were re-located independently of ScoutRFC's
receipt, with `grep -n -F` on the retained body: 848, 852, 861, 935, 938, 944, each
an exact substring of the line it is named at — 6/6, matching ScoutRFC's
`SCOUT fetch=0 sha-match=yes quotes=6/6 located`.

## Findings for the L1 (routed, not repaired)

1. **The `used-by` paths do not exist yet.** `corpus/knowledge/revalidation-exchange.md`
   is this seat's draft, and `corpus/lessons/round-96.md` is the round's lesson, which
   no seat has written. The census's E11 check runs only on `mined` rows, so nothing
   fires today — but flipping S480 to `mined` before both paths land produces an E11
   finding. **Land the entry and the lesson first; flip the status last.**
2. **The entry's `source:` line names S480, so the entry and the row must land
   together.** Under the C1 counter's E3 audit, an `S###` id in a `source:` line
   that is not a row id in `corpus/SOURCES.md` is an E3 finding. Measured, not
   asserted (`e3-conformance.txt`): against the lane's current SOURCES.md the draft
   shows `unresolved row id S480`; against the prospective SOURCES.md with the row
   inserted, `problems: none`.
3. **The S480 anchor cell's line ranges were corrected** against the body: the
   SHOULD Last-Modified bullet is lines 852-854 (not 852-855 — 855 is blank), the
   full-response bullet is 938-942 and the 5xx bullet is 944-949. The received
   draft's ranges ran one line past each bullet's end. The row sha256 after the
   correction is `b8f64b01…`.
4. **`corpus/README.md` coverage map has no row for the new entry.** The map lists
   every lane knowledge entry, and the README rule is "an index row is a claim —
   write the row when the file exists, not before". The L1 adds the row when it
   lands the entry. This seat does not write the README (out of its write scope).

## Out of scope for this seat — named, not done

- **The instruments were not touched.** Digests re-verified against
  `controls/instrument-sha256.txt` and unchanged (`instrument-digests.txt`). No
  repair to any counter, contract or population.
- **The candidate `scripts/reval_exchange.py` was not scored and not edited.** It
  is another seat's file; this seat only read it to confirm the refusal diagnostic
  wording (`invalid_input: <reason>` on stderr) that the entry describes.
- **No claim was scored, no gate was closed, no lesson was written.** The
  round-96 lesson and its `## Gate` (which should record the S480 row's ≤25-word
  quote with its location, per SOURCES contract rule 1) are the L1's.
- **No git or jj mutation was run.** Read-only git only (`rev-parse`, `cat-file`,
  `show`, `status`, `ls-tree`). No commit, no add, no push, no checkout, no reset,
  no stash; no jj command of any kind.
- **No sysctl was read or changed.** Nothing in this seat's checks needed one.
- **No tool was installed or upgraded.** No `pacman`, `uv tool install`, `npx` or
  `cargo install` was run; `python3` (3.14), `node` (v24.21.0), `curl` (8.23.0),
  `git` and `cmp` were already present and were used as-is.

## Scratch and cleanup

The seat's scratch tree is `/fast/scratch/hyaku/kake-r96/ScribeEntry/`. Its
receipts were copied into this seat's directory **before** deletion:
`body-digests.txt` and `census-baseline.txt` were copied from the scratch
`receipts/` directory; `census-with-s480.txt`, `e3-conformance.txt`,
`quotes-verified.txt` and `instrument-digests.txt` were written directly into the
seat directory. The scratch tree is deleted before this seat yields — a seat that
ends with its tree still on disk would report that as its own defect, and this
seat does not. One live clone or fixture repo per seat: no fixture repo was
created at all (the census mirrors are copies of corpus files in scratch, not a
clone of the lane), and no mirror of the lane was taken.

## Report paths

- `.ufo/waves/round-96/w1/ScribeEntry.md` — this report.
- `.ufo/waves/round-96/w1/ScribeEntry/knowledge-entry.md` — the knowledge entry draft.
- `.ufo/waves/round-96/w1/ScribeEntry/s480-row.md` — the finalized S480 row draft.
- `.ufo/waves/round-96/w1/ScribeEntry/quotes-verified.txt` — the per-quote receipt.
- `.ufo/waves/round-96/w1/ScribeEntry/verify-quotes.py` — the quote checker.
- `.ufo/waves/round-96/w1/ScribeEntry/check-census.py` — the census checker.
- `.ufo/waves/round-96/w1/ScribeEntry/check-e3.py` — the E3 conformance checker.
- `.ufo/waves/round-96/w1/ScribeEntry/instrument-digests.txt`,
  `.ufo/waves/round-96/w1/ScribeEntry/body-digests.txt`,
  `.ufo/waves/round-96/w1/ScribeEntry/census-baseline.txt`,
  `.ufo/waves/round-96/w1/ScribeEntry/census-with-s480.txt`,
  `.ufo/waves/round-96/w1/ScribeEntry/e3-conformance.txt` — supporting receipts.

**VERDICT: SCRIBE quotes=13/13 located**
