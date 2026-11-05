VERDICT: C2's knowledge entry and registry surface land; the C2 counter's frozen
sandbox has a real import-allowlist defect (FINDING F93-1) that can turn a
contract-faithful candidate into `met=false` on an import line alone.

Author: ScribeEntry (kake, round-93 wave 1). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Freeze `bb8012fee38c0e497cdaf36337072737bca0b3cd`; base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`.
Scratch root `/fast/scratch/hyaku/kake-r93/ScribeEntry/` (deleted before this
report was written; every receipt below was copied into the wave directory
first). No commit, stage, stash, checkout, reset, pull, push or `jj` command
was run in the lane. No frozen file was edited.

---

## What this seat delivered

| Deliverable | Path | State |
|---|---|---|
| The C2 knowledge entry | `corpus/knowledge/conditional-request-evaluation.md` | written (16 456 B) |
| The coverage row + frontier narrative | `corpus/README.md` | written (+32 lines) |
| The `SKILL.md` registry row | `.ufo/waves/round-93/w1/ScribeEntry/SKILL-row.md` | **draft only — `SKILL.md` was not edited** (the L1 owns it this wave; `ExecC1Fixes` is repairing the E5 paths in it) |

Receipts, all under `.ufo/waves/round-93/w1/ScribeEntry/`:

| File | What it holds |
|---|---|
| `receipts.txt` | the live GET receipts for both RFC texts (status, bytes, sha256, UTC access time), the `cmp` against the lane's retained bodies, and the re-run readings of both frozen instruments' own selftests |
| `quotes.txt` | 20 mechanical checks over every quoted passage in the entry (`violations=0 checks=20`, exit 0) |
| `tool-probe.txt` | the 13 decision + 6 refusal worked examples run against the delivered candidate **and** the frozen positive control (`mismatches=0`, exit 0) |
| `finding-sandbox-allowlist.txt` | the FINDING F93-1 evidence |
| `SKILL-row.md` | the draft registry block + the exact anchor + five notes for the L1 |
| `verify_entry_quotes.py`, `verify_quotes.py`, `probe_tool.py` | the verifiers, so a non-author re-runs the checks from committed bytes (they read the lane's committed retained bodies at `.ufo/waves/round-93/L1/src/`, which `receipts.txt` proves byte-identical to the live GETs) |

---

## (1) The knowledge entry

`corpus/knowledge/conditional-request-evaluation.md` carries `source:`,
`verified-at:` and `recheck:` in its first 5 lines (E3's requirement is
"within its first 8 lines"), plus `ground:` and `scope:` lines in the same
block, matching the round-92 entry's shape.

It covers, in order: what a conditional request is on the publisher side;
why the evaluation order is normative (RFC 9110 §13.2.2 and the RFC's own
reason for the order); the strong-vs-weak comparison functions with **Table 3
reproduced in full** (§8.8.3.2); the origin-vs-cache difference (§13.2.2's
first two steps are origin-only, RFC 9111 §4.3.2 says If-Match and
If-Unmodified-Since "are not applicable to a cache"); the lane's adapter
convention (dates as integer epoch seconds, no HTTP-date parsing) **and the
narrowing that convention forces**; what the tool decides; what it explicitly
does **not** decide; and the 13 worked decisions + 6 refusals.

### Every source opened this round

Both sources were fetched by this seat with a live GET, twice (once at
`01:27:45Z` for the reading, once at `01:38:44Z` for the receipt file);
both fetches returned HTTP 200 with identical bytes and digests:

| URL | HTTP | bytes | sha256 | accessed (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-05T01:27:45Z, 2026-11-05T01:38:44Z |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-05T01:27:45Z, 2026-11-05T01:38:44Z |

Both are byte-identical to the lane's retained copies
(`.ufo/waves/round-93/L1/src/`) — `cmp` exit 0 for each — so every line
number in the entry is the line number in the fetched body. Receipt:
`receipts.txt`.

### Every quote is located, ≤25 words, and mechanically verified

`quotes.txt` (`violations=0 checks=20`, exit 0) runs three passes:

- **pass A** extracts all 10 blockquotes from the entry and checks each is a
  raw substring of one of the two fetched bodies and is 3–25 words;
- **pass B** checks the 3 inline double-quoted fragments against their stated
  line spans;
- **pass C** checks that the `source:` line's seven declared anchor line
  numbers really are the section headings (`13.2.2.` at 6222, `13.1.1.` at
  5785, `13.1.2.` at 5872, `13.1.3.` at 5942, `13.1.4.` at 6023, `8.8.3.2.` at
  3643, `4.3.2.` at 866).

**Two of my own quotes were over the 25-word limit on the first pass and I
trimmed them** — the §13.2.2 rationale quote (32 → 20 words, span corrected
from 6227-6231 to 6227-6230) and the §15.4.5 304-body quote. Both are now
inside the rule; the verifier is what caught them.

### The worked examples are verified twice over

I derived 13 decisions and 6 refusals **by hand from the contract's clauses**
(clause number recorded per example), then ran each against **both** the
delivered candidate `scripts/conditional_eval.py` and the frozen independent
positive control `.ufo/waves/round-93/frozen/pos-good.py`. All 13 decisions
agree with both; all 6 refusals are refused by both. Receipt:
`tool-probe.txt` (`mismatches=0 decisions=13 refusals=6`, exit 0). The
candidate's `--selftest` printed `selftest 90/90`, exit 0, at the moment of
that measurement.

**The two example families that matter most** are W2 and W6: the *same* pair
of tags (`"abc"` against `W/"abc"`) decides `412` under If-Match's strong
comparison and `304` under If-None-Match's weak comparison — Table 3's third
row, expressed as two decisions. W11 shows the cache role (a non-matching
`if_match` that would be `412` at the origin is not evaluated at a cache);
W12 shows the precedence (If-None-Match present and not matching ⇒ the
precondition is *true* ⇒ evaluation continues ⇒ If-Modified-Since is never
reached ⇒ `200`, not the `304` it alone would have produced).

### Honest limits the entry states

- The dates-as-integers convention is **the lane's, not the RFC's**, and it
  forces a visible narrowing: RFC 9110 §13.1.3/§13.1.4 say an invalid or
  list-valued date field is *ignored*, whereas in the lane's integer encoding
  a non-integer or negative value is a *refusal* at clause 1. The entry says
  this rather than hiding it.
- Nothing here is evidence about any live CDN, Pages front, Render service,
  proxy or browser.
- No storage, no freshness, no revalidation exchange, no forwarding, no
  serving decision, no HTTP-date parsing, no clock, no validator generation.
- The 304 **body** and header set are out of scope: §15.4.5 says a 304 "is
  terminated by the end of the header section; it cannot contain content or
  trailers", and the tool decides the status only.
- The frozen counter scores the **contract**, not the RFC.

---

## (2) The registry ids — computed, and the L1 must confirm them

**The round-93 `ScribeSources` seat has not written
`.ufo/waves/round-93/w1/ScribeSources/rows.append.md`**, so there is no
declared id list to read. I checked: the directory holds only `src/`, and
`find .ufo/waves/round-93 -name 'rows.append.md'` returns nothing.

**The ids this entry cites are therefore computed, not observed.** The highest
existing id in `corpus/SOURCES.md` is `S470` (207 rows; verified in the
working tree and at `HEAD`), and the dispatch item's anchor order gives six
rows, so the entry cites **S471–S476**:

| id | anchor |
|---|---|
| S471 | RFC 9110 §13.2.2 Precedence of Preconditions |
| S472 | RFC 9110 §13.1.1 If-Match (strong comparison) |
| S473 | RFC 9110 §13.1.2 If-None-Match (weak comparison) |
| S474 | RFC 9110 §13.1.3 + §13.1.4 the two ignore rules (one row) |
| S475 | RFC 9110 §8.8.3.2 Comparison (strong/weak + Table 3) |
| S476 | RFC 9111 §4.3.2 |

**⚠ The L1 must confirm these six ids against the sibling's
`rows.append.md` when it lands.** If the sibling drafts a different count or
order, its order wins and the `S471`–`S476` range in the entry's `source:`
line, in the README coverage row, and in the `SKILL-row.md` draft must be
corrected to match. Two independent derivations (mine, and a peer seat's that
I asked) produced the same list, but **both are derivations from the dispatch
item, not from the sibling's file** — so they agree with each other and still
await the authoritative source.

**Two E-class dependencies follow from this**, both measured in a scratch
clone (below):

- **E3** requires every `S<digits>` id on a knowledge entry's `source:` line
  to resolve to a row id in `corpus/SOURCES.md` at the measured revision.
  Until the L1 appends the rows, the entry is one E3 finding.
- **E5** requires every repo-relative path named in a `SKILL.md` table row to
  exist at the measured revision. My draft row names
  `scripts/conditional_eval.py`, which is currently untracked, so the row is
  an E5 finding until `ExecC2Tool`'s file is committed.

Both clear when the L1 appends the rows and commits the tool.

---

## (3) The `SKILL.md` registry row — draft, with the anchor named

**`SKILL.md` was not edited by this seat.** The L1 (`KakeR93`) re-tasked me:
`ExecC1Fixes` owns `SKILL.md` this wave because it is repairing the six E5
dangling paths in it. The draft is in
`.ufo/waves/round-93/w1/ScribeEntry/SKILL-row.md`.

**The exact anchor:** append a **new `## Round 93 — …` section at the end of
the file**, after the current last line of `SKILL.md` — the round-92
section's closing paragraph ending "…L1's re-run at the landing revision is
what counts." (today line 1680; `wc -l SKILL.md` → 1680). **Do not insert into
the round-92 table** — that section owns the round-92 rows. The draft follows
the round-91/round-92 section shape: prose, then the eight-column table
(`| Name | Kind | Entry command | Verdict map | Selftest | Pinned values |
Write scope | Owner |`), then a `**How to verify.**` line, then a closing
"Two limits worth carrying" paragraph.

**Kind: `probe`** — accurate, because the tool decides over supplied values
and writes nothing. The row carries the full stdin/stdout contract, the
exit map (0 decided / 1 refused with `invalid_input:` on stderr and empty
stdout), the `--selftest` line, and the pinned values (the contract, the
`200`/`304`/`412` vocabulary, the five precondition names, the strong/weak
split, the cache-role skip, and the integer-seconds convention). The
`Write scope` cell reads "stdin/stdout/stderr only; writes nothing" and the
`Owner` cell reads "kake", matching the round-92 row.

The `**How to verify.**` line gives the exact command and exit map:

> `python3 -B .ufo/waves/round-93/c93_conditional.py --root . --revision <rev> --work <explicit-scratch>` must print `candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok met=true`, exit 0 (exit 1 on any failed conjunct, exit 2 on reference or hand-case drift before any candidate is scored, on an unresolved revision, or on argparse usage); and `python3 -B scripts/conditional_eval.py --selftest` must print a final `selftest <n>/<n>` line, exit 0.

### One correction I made to my own draft, found by measurement

My first draft's `Write scope` cell named the seat's own wave directory
`.ufo/waves/round-93/w1/ScribeEntry/`. The E5 class **flags it**: E5 resolves
each named path with `git show <rev>:<path>`, which **fails for a directory**
even when the directory exists at the carrier. Measured in the scratch clone,
the draft produced `E5=1 … names missing path .ufo/waves/round-93/w1/ScribeEntry/`;
the prose cell produces no E5 finding. Fixed, and the lesson is written into
`SKILL-row.md` for the L1: **do not name a directory in any `SKILL.md` table
row.**

---

## (4) `corpus/README.md`

Both additions are in the round-92 shape.

**Coverage row** (in the frontier-ground map, immediately after the r92 row,
line 137):

```
| Conditional request evaluation (which status a recipient answers a conditional request with, and which precondition decided it; no clock, no HTTP-date parsing, no storage, no freshness, no serving or forwarding) | r93 (lands this round) | `knowledge/conditional-request-evaluation.md` + `scripts/conditional_eval.py` | S471 S472 S473 S474 S475 S476 |
```

**Frontier narrative** — a new `## Round-93 frontier step — conditional
request evaluation` section at the end of the file, mirroring the round-92
section's two-part shape (a "what moved" paragraph, then a "Frontier line:"
paragraph). It states that the conditional-request evaluation moves from open
ground to held, bounded ground for supplied values only; that the reuse
decision stays with r91 and the heuristic lifetime with r92; and that still
open are the revalidation *exchange* (§4.3.4), the 304 header set (§15.4.5),
the `If-Range`/`Range` step the contract does not implement, HTTP-date
parsing, field-specific header normalisation, validator generation, and every
live-cache/CDN/browser observation.

---

## Verification I actually ran

All in a scratch clone at `/fast/scratch/hyaku/kake-r93/ScribeEntry/clone`
(created by `git clone -q --shared`, detached at the freeze revision
`bb8012f…`, with `update-ref refs/heads/master` pointed at the lane's master
so a replay harness resolves the same carrier revision). **No git mutation was
run in the lane.**

| # | Command (cwd, revision) | Reading | Exit |
|---|---|---|---|
| 1 | `c93_selfassess.py --root . --revision 10ecbd1a…` | `lessons=87 entries=80 rows=255 criteria=39 mismatches=20 E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok met=false` | 1 |
| 2 | `c93_selfassess.py --root . --revision <my scratch commit>` (entry + README + tool committed, **no SOURCES rows**) | `mismatches=21 … E3=2 …` — my entry adds exactly one E3 finding, `unresolved S471, S472, S473, S474, S475, S476`, and nothing else | 1 |
| 3 | `c93_selfassess.py --root . --revision <scratch commit + S471-S476 rows + my SKILL block>` | `mismatches=14 E1=1 E2=8 E3=1 E4=4 E5=0` — **E5 drops to 0** (the L1's `ExecC1Fixes` SKILL.md repair clears the six base E5 findings and my corrected row adds none), E3 back to 1 | 1 |
| 4 | `c93_conditional.py --root . --revision <final scratch commit> --work <scratch>` | `candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true` | 0 |
| 5 | `python3 -B scripts/conditional_eval.py --selftest` | `selftest 90/90` | 0 |
| 6 | `verify_entry_quotes.py` | `violations=0 checks=20` | 0 |
| 7 | `probe_tool.py` (candidate **and** frozen positive control) | `mismatches=0 decisions=13 refusals=6` | 0 |
| 8 | `c93_selfassess.py --selftest` (re-run of the frozen instrument's own battery) | `selftest 5/5 planted findings, exit 1 on planted, exit 0 on repaired` | 0 |
| 9 | `c93_conditional.py --selftest` (re-run of the frozen instrument's own battery) | `selftest 7/7 fixtures scored as declared; drifted-reference cases=4` | 0 |

Rows 1–3 also confirm that **the 14 residual mismatches are not mine**: the
remaining E1 (1) is `corpus/lessons/round-85.md` missing `## Gate`; the E2
(8) are `corpus/QUALITY.md` criteria sections; the E3 (1) is
`corpus/knowledge/meta-robots-directives.md`, whose metadata
`ExecC1Fixes` is repairing in its own working tree; the E4 (4) are blank
lines inside `## Mistakes` tables in `round-29.md`, `round-33.md`,
`round-54.md` and `round-92.md`. None of those five files are in my write
scope, and I did not touch them.

**Verification boundary, stated plainly:** I did **not** run the frozen
counters against the lane's own working tree as a "carrier" measurement.
Every C1/C2 reading above is at a **scratch clone** revision I constructed by
committing my own files there. The lane's carrier reading is the L1's to
take, at the revision it lands.

---

## FINDINGS

### F93-1 — the frozen C2 counter's sandbox import allowlist omits `__future__` (a defect in a FROZEN instrument)

**Nothing frozen was edited.** This is routed, not patched.

The counter's sandbox (`c93_conditional.py`, the `SANDBOX` constant) installs
an audit hook that denies any import whose top-level name is not on a
fixed allowlist. `__future__` is **not** on that allowlist — but
`from __future__ import annotations` is a plain, entirely standard stdlib
idiom, and **the frozen counter's own reference implementation uses it**
(line 37 of `c93_conditional.py`).

Consequence: a candidate that is byte-for-byte contract-faithful and differs
from a passing candidate only by that one import line is **refused by the
sandbox at import time**, before it decides anything. It scores
`hand=14/44 generated=0/120 … met=false` — the 14 "passes" are the refusal
cases, which the counter counts as passing because the subject exits non-zero
with empty stdout, for the wrong reason.

**Measured** (receipt: `finding-sandbox-allowlist.txt`):

1. The delivered candidate, scored by the frozen counter in the scratch clone:
   `candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6
   positive=admitted anti_table=ok population=ok seed=93 met=true`, exit 0.
2. The **same candidate bytes** (`scripts/conditional_eval.py`,
   sha256 `d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e`)
   plus one inserted line — `from __future__ import annotations` at line 32
   (repro sha256 `e9a4b8c68729fcabf28110e0200baccdad4e71aa9339cb256f63a5bd307e1057`),
   committed in a throwaway fixture repo and scored by the same frozen
   counter: `candidate=present hand=14/44 generated=0/120 forgeries_refused=6/6
   positive=admitted anti_table=ok population=ok seed=93 met=false`, exit 1.
3. The sandbox's own stderr for that repro:
   `PermissionError: sandbox: import denied: __future__`
   (raised at `sandbox.py` line 33, the audit hook).
4. `__future__ in allowlist: False`; the counter's own reference imports it
   (line 37): `True`; the frozen positive control does not import it: `False`.

**Why this matters for the round's claim.** The freeze's kill rule says "any
admitted forgery, any hand/generated disagreement, a refused positive
control, an anti-table hit or a population drift is an honest unmet". The
C2 predicate does not list "a subject that could not import" as a distinct
outcome — so a **sandbox-caused import failure is reported as a candidate
disagreement**, indistinguishable from a genuine one. The round-92 routed
defect R92-5 was precisely "check the counter's reference against the
contract by an independent reader before the freeze"; this is the same family
of defect in the *execution environment* rather than in the oracle: the
frozen environment and the frozen oracle disagree about what a legal Python
module may import, and the reference implementation itself is not admissible
under it.

**Flip condition for the successor counter:** a candidate that adds
`from __future__ import annotations` — or any other ordinary stdlib import
the allowlist happens to omit — must still be scored on its decisions, not
refused at import. The minimal fix is to add `__future__` to the allowlist;
the principled fix is to derive the allowlist from the candidate's own
imports and refuse only what the contract forbids (the counter, the fixtures,
the network). Until then, the C2 predicate's `met=true` at the carrier is a
statement about a subject whose import set happens to fit the allowlist.

**Not a claim that the delivered tool is wrong.** The delivered tool as it
stands passes cleanly (reading 1 above). This is a defect in the frozen
instrument's environment, and it is routed, not patched.

### F93-2 — the dispatch's sixth anchor is mis-titled ("cache applicability")

The dispatch item describes the sixth anchor as "RFC 9111 4.3.2 cache
applicability". In the retained `rfc9111.txt`, §4.3.2 is titled
**"Handling a Received Validation Request"** (line 866). Its content is how a
cache handles an inbound conditional request; there is no section titled
"Applicability of Caching" in RFC 9111 at all (the cache-applicability rules
are §3 "Storing Responses to Caches" and §4 "Constructing Responses from
Caches"). A peer seat raised this and I confirm it from the retained body.

This is **not** a defect in my entry: I cite §4.3.2 for what it actually
says — the sentence "the If-Match and If-Unmodified-Since conditional header
fields are not applicable to a cache" — and my `source:` line names the
section by its real title. But it is a live risk for the **sibling scribe's
S476 row**, whose `scope` and `anchor` cells must not describe §4.3.2 as
being about cache applicability. **Flagged for the L1 and the sibling; the L1
should check S476's wording when it lands.** My entry does not depend on the
sibling's wording, and if the sibling's row is retitled the entry still
stands, because the entry quotes the RFC itself.

### F93-3 — the round-93 `ScribeSources` seat has not produced its rows yet

`.ufo/waves/round-93/w1/ScribeSources/` holds only `src/`; no
`rows.append.md` and no report exist. That is a live dependency, not a
defect in an instrument: until it lands, the six registry ids this entry
cites are computed rather than declared (see §2 above). If the sibling
does not land its rows, the L1's own SOURCES append must supply them, or the
entry's `source:` line will be an E3 finding at the carrier.

### F93-4 — minor: the C2 counter's docstring says "30 hand cases", the counter holds 44

`c93_conditional.py`'s module docstring reads "*(30 hand cases + a seeded
generated population decided by this file's own reference)*" and its
`hand_cases()` docstring reads "30 worked cases". The function actually
returns **44** cases (30 decisions + 14 refusals), which is what the
`hand=44/44` reading reports and what the freeze declares. The count in the
docstring is stale, from an earlier draft of the file. Frozen, so routed and
not edited. Harmless to the verdict — the counter reports the live count —
but a reader of the docstring would under-read the population.

### F93-5 — a lane-adjacent observation, outside my write scope

`corpus/knowledge/meta-robots-directives.md` is the E3 finding that survives
my simulated carrier (missing `source:`/`verified-at:`/`recheck:` in its
first 8 lines). `ExecC1Fixes` is repairing it in its own working tree, so I
did not touch it. Recording it here only so the L1 knows the residual E3 is
accounted for.

---

## Answers to the round-92 routed defects this seat touches

| defect | this round's answer |
|---|---|
| **R92-4** (C2 population coverage: one case per clause and per refusal class) | The **frozen counter** now carries 44 hand cases covering clauses 1–12 and 14 refusal classes — the population grew from the round-92's 28. My seat adds **no** case to it (the instrument is frozen), but the entry's own 13 decisions and 6 refusals are an independent, hand-derived exercise of the same clauses: clause 1 (four refusal shapes), 2, 3, 4, 7, 8, 9, 10 (three shapes), 11 (three shapes) and 12. The entry's `tool-probe.txt` is a per-clause trace a non-author can re-derive. |
| **R92-5** (the counter's reference must be checked against the contract by an independent reader before the freeze) | The counter now checks its own reference against every worked case before scoring any candidate and exits 2 on drift. **This seat is an independent reader of the contract**, and I confirmed the delivered candidate against the *frozen positive control* (a separate implementation) rather than against the counter's reference: 13/13 decisions and 6/6 refusals agree with both. **F93-1 is the same defect class in the execution environment rather than the oracle.** |
| **R92-6** (dead seat: the round-92 entry's quotes were verified only by the author and one scout) | The round-92 entry's own spot-check closed this. For **this** round's entry I have made every quote mechanically re-derivable from the fetched bodies by a third party (`quotes.txt`, exit 0) and every worked example re-derivable from the frozen positive control (`tool-probe.txt`, exit 0). A non-author re-run needs only the two RFC texts and the frozen counter's `--selftest`. |
| **R92-7** (carried: K91-3, K91-6, K91-8, K91-9, K91-10) | Not this seat's scope; unchanged by me. |

---

## Out of scope — what I did **not** do

- **I did not edit `LANE/SKILL.md`.** The L1 reassigned it to `ExecC1Fixes`
  mid-round; my registry row is a draft block with the anchor named.
- **I did not edit `corpus/SOURCES.md`.** The six rows are the sibling
  scribe's to draft and the L1's to append. I did not invent a row.
- **I did not edit `corpus/lessons/round-93.md`** (`ScribeSources` and
  `ScribeC1Prose` own the lesson), `SCORECARD.md`, `LOG.md`, `PROVINCE.md`,
  `MANIFEST.json`, or `.ufo/state`.
- **I did not edit any frozen instrument** — `c93_selfassess.py`,
  `c93_conditional.py`, `c1-predicate.md`, `c2-contract.md`, `frozen/`,
  `controls/`. F93-1 and F93-4 are routed, not patched.
- **I did not edit `scripts/conditional_eval.py`** (`ExecC2Tool` owns it). I
  copied it into the scratch clone to score it.
- **I did not commit, stage, stash, checkout, switch, reset, pull or push**
  in the lane, and ran no `jj` command. The only commits I made are in the
  scratch clone and in a throwaway fixture repo under my scratch root.
- **I did not spawn a subagent** (leaf member), and I did not message
  `agent://all`.
- **I did not fetch the RFC-Editor errata pages.** The sibling `ScribeSources`
  seat holds those receipts this round; I did not claim a reject on their
  basis.

## Tooling

**No tool was installed, upgraded or modified.** `curl`, `git`, `sha256sum`,
`cmp`, `wc` and `python3` (stdlib only) were already present and sufficient.
Under the operator's channel rules nothing needed installing, so no
tool/version/channel/reason record is owed. `pacman` was not run, consistent
with the host-wide pacman pause.

## Scratch

`/fast/scratch/hyaku/kake-r93/ScribeEntry/` held one clone
(`clone/`, the permitted scratch clone), the fetched RFC bodies (`src/`), the
three verifier scripts, and the throwaway fixture repo (`reprotree/`) used
for F93-1. **The scratch directory was deleted** after every receipt was
copied into `.ufo/waves/round-93/w1/ScribeEntry/`. No tree was written under
`/tmp`. No ephemeral path is cited as evidence anywhere in the entry or in
this report — the entry's `recheck:` line names only the URLs and the
digests.
