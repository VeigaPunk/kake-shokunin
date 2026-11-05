# ScribeEntry — round 94, wave 1 (kake / hyaku run 15)

VERDICT: entry drafted, 306 words (336 counting the ground/scope metadata lines), all sentences cited

File written (the only file this seat wrote):
`corpus/knowledge/http-list-and-method-grammar.md` (new; 33 lines, 2 356 bytes,
sha256 664408d8ee3ae4a718cc0013c1a45be4fd0fed59da82b1e4d5c3eff30aeffb0b, 351 words total).

## Province decision

**This grammar belongs in the conditional-request province.** It is needed to decide
If-Match and If-None-Match list members: the method-token case rule decides whether a
request whose method is `get` is a GET request at all (S477 §9.1, 3748-3749), and the
list-member separator rule decides whether a tab-separated member is a member at all
(S478 §5.6.1.2, 1699-1702). Both are load-bearing for the two v2 counter cases
`inm/lowercase-method-is-not-get` and `inm/htab-around-list-members`, so the entry sits
on the same ground as the existing `corpus/knowledge/conditional-request-evaluation.md`
(S471-S476), which it complements rather than repeats.

**Limit of the decision.** The entry decides *grammar only*: the method-token case rule and
the list-member separator/OWS rule. It decides **not** the entity-tag character grammar
(quoted commas, empty elements, obs-text) and **not** any contract-v1 or contract-v2
conformance question; those three are routed to contract v2 and are listed as such in the
entry. It is knowledge only — no gate, no Core promotion, no PROVINCE.md edit (PROVINCE.md
is not in this seat's write scope, and the entry adds no ground that changes a province
line).

## Shape

Lines 1-3 are exactly the required provenance trio:

```
source: S477, S478 (RFC 9110 sections 9.1 and 5.6.1, see corpus/SOURCES.md)
verified-at: 2026-11-05
recheck: 180d
```

Lines 4-5 add `ground:` / `scope:` metadata lines. These are a common lane convention but
not universal: 48 of the lane's 82 `corpus/knowledge/*.md` files carry a `ground:` line in
their first 8 lines (counted by `grep -c '^ground:'` over the head of each file), including
the sibling entry `conditional-request-evaluation.md` this one complements. The `scope:`
line states the boundary of the entry (grammar only, not entity-tag character grammar and
not contract decisions), which the seat item requires me to state; the `ground:` line marks
the entry's axis. Nothing else about the shape is conventional.

Word counts (whitespace tokens, counted by script): trio 15; ground+scope 30; body from
the H1 **306**; everything after the trio **336** — both at or under the 350-word cap.

## Sentence-to-citation map

Body sentence -> row id + section (+ plain-text line span of the fetched RFC body):

| # | Sentence (abridged) | Citation |
|---|---|---|
| 1 | "The method token is case-sensitive." | S477, §9.1, plain-text 3748-3749 (located quote, blockquote) |
| 2 | "So `get` is not the GET method" | S477, §9.1 |
| 3 | "…a matching If-None-Match answer 304 … and 412 …" | S473, §13.1.2, 5928-5932 |
| 4 | "the v2 case `inm/lowercase-method-is-not-get` expects 412 … the method-token case rule decides it, not taste, and the case kills mutant M37" | S473, §13.1.2 (expectation) + S477, §9.1 (the rule that decides it) |
| 5 | "**List members are comma-separated with optional whitespace.**" (blockquote) | S478, §5.6.1.2, 1699-1702 (located quote) |
| 6 | "so members are comma-separated with optional whitespace" | S478, §5.6.1.2 |
| 7 | "Section 5.6.1 names that whitespace OWS and points to Section 5.6.3 for its definition" | S478, §5.6.1, 1670-1672 |
| 8 | "where OWS is SP or HTAB (line 1774), so a tab around a member is legal whitespace" | RFC 9110 §5.6.3, plain-text 1774 (OWS production) — see finding F2 |
| 9 | "If-Match and If-None-Match are entity-tag lists" | S472, §13.1.1, 5799; S473, §13.1.2, 5885 |
| 10 | "…the v2 case `inm/htab-around-list-members` expects that match … and kills mutant M40" | S478, §5.6.1.2 (the match) |
| 11 | "A comma inside a quoted entity-tag: RFC 9110 §8.8.3 admits it; R93-8 records the positive control refusing it." | S455, §8.8.3, 3587 + `corpus/lessons/round-93.md` R93-8 |
| 12 | "Empty list elements: S478's §5.6.1.2 requires a recipient to accept and ignore them; the contract refuses them (R93-9)." | S478, §5.6.1.2, 1695-1699 + round-93 lesson R93-9 |
| 13 | "obs-text in an entity-tag: the same line 3587 admits it; the contract refuses it (R93-9)." | S455, §8.8.3, 3587 + round-93 lesson R93-9 |
| 14 | "Each is a contract-v2 decision, routed by `corpus/lessons/round-93.md` R93-8/R93-9." | routing statement, carries no independent source claim |

No factual sentence in the entry is uncited; every row id it names (S455, S472, S473,
S477, S478) resolves in `corpus/SOURCES.md` at the lane tip, and the three "does not
decide" items name their routing record (round-93 lesson R93-8 / R93-9).

**Citation-granularity note.** Two cited facts cannot carry an S477/S478 id, and I did not
force one onto them: the entity-tag character grammar (a comma and obs-text inside an
opaque-tag) is RFC 9110 §8.8.3, which S455's anchor (`§8.8.3 lines 3570-3617`) covers at
line 3587, so it is cited to S455; and the OWS production (SP or HTAB) is §5.6.3, which no
registry row anchors, so it is cited by section + plain-text line only (finding F2). The
seat item asks that every factual sentence cite a located quote by id and section; every
sentence does carry an id plus a section, and where the id is S455/S472/S473 rather than
S477/S478 the reason is that S477/S478 do not ground that fact — citing them would be a
false attribution.

## Source access

The scout's located quotes existed (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-94/w1/ScoutRFC/quotes.json`),
so the entry uses them. I also ran the same single GET independently as a corroboration:

- `curl -sS -o rfc9110.txt -w "status=%{http_code} bytes=%{size_download} url=%{url_effective}\n" https://www.rfc-editor.org/rfc/rfc9110.txt`
  → `status=200 bytes=502941`, exit 0.
- `sha256sum rfc9110.txt` → `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`
  — byte-identical to the scout's body and to the digest already pinned in rows S471-S476.
- `date -u` → access time `2026-11-05T15:00:25Z` (the scout's own GET: `2026-11-05T15:00:17Z`,
  8 s earlier, same bytes).
- No credentials sent; no other URL fetched; scratch removed (see below).

Both located quotes were re-verified by script against the fetched body
(`.ufo/waves/round-94/w1/ScribeEntry/verify-quotes.py`, exit 0, re-runnable from the lane):
each is an exact whitespace-normalized substring of the body **and** of its own stated line
span — S477 §9.1 3748-3749 (20 words), S478 §5.6.1.2 1699-1702 (23 words), plus §5.6.1
1670-1672 (15 words) and §5.6.3 1774 (7 words) for the OWS production; S473 §13.1.2
5928-5932 (56 words) and S472/S473 field-syntax lines 5799/5885 (5 words each) also
verify, though the entry quotes them only in shorter fragments. The two blockquotes
reproduce the RFC's own line breaks (1699/1700/blank/1702 and 3748/3749), the convention
used by the sibling entry `conditional-request-evaluation.md`.

## Verification run (read-only, scratch clone)

Scratch clone (path shown for provenance; it was deleted before this seat yielded, so the
receipts below are the citable evidence):
`git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin
/fast/scratch/hyaku/kake-r94/ScribeEntry/clone`; `git -C <clone> rev-parse --show-toplevel`
= the clone path. Only the clone was committed; LANE was never committed, staged or
mutated by this seat.

- `python3 -B .ufo/waves/round-94/c94_selfassess.py --root <clone> --revision HEAD --skip-battery`
  → exit 1, line 1: `C1v94 revision=d9ea9ef8… counter=58028584… lessons=88 entries=82
  rows=255 criteria=39 mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=0/8
  predecessor_admits=0/0 floor=2 self_pin=ok met=false`. The 15 mismatches are the
  pre-existing E5 "names a tree, not a blob" SKILL.md rows (ExecC1Repair's scope);
  **E3 = 0**, i.e. the new entry passes the trio/row-id check and adds no mismatch.
  Receipt: `.ufo/waves/round-94/w1/ScribeEntry/c1-entry-and-rows.txt`.
- `node scripts/corpus-contract.mjs --root <clone>` → exit 0, `result: 0 findings · 82
  knowledge entries · 88 lane lessons · 78 skipped · 0 errors` (trio present in the new
  entry's first 8 lines).
- `python3 -B .ufo/waves/round-55/c55_readme_index.py --root <clone> --revision HEAD`
  → exit 1, `index_mismatches=25 knowledge_files=88 met=False`; the new file is reported
  `unindexed: http-list-and-method-grammar.md` (see finding F3).

Scratch `/fast/scratch/hyaku/kake-r94/ScribeEntry/` deleted (whole tree, clone included) after
the receipts below were copied here; the citable artifacts are this report and the three
files under `.ufo/waves/round-94/w1/ScribeEntry/` (`fetch.txt`, `verify-quotes.py`,
`c1-coupling-base-sources.txt`).

## Findings

**F1 (material, for the L1 — landing order).** The C1 counter's E3 class resolves the
row ids on each knowledge entry's `source:` line against the rows present in
`corpus/SOURCES.md` **at the measured revision**. Measured: a clone commit carrying the new
entry against the *base* `corpus/SOURCES.md` (no S477/S478) reads
`mismatches=16 E3=1` with detail `unresolved row id S477, S478` on
`corpus/knowledge/http-list-and-method-grammar.md`; the same tree with the two new registry
rows present reads `mismatches=15 E3=0`. **The entry and the two registry rows must land in
the same revision**, or C1 reads an E3 mismatch that is not the repair's fault. (ExecSourceRows
has already appended S477/S478 in the lane worktree; the L1 must keep them together.)

**F2 (row-anchor gap).** The HTAB fact the entry needs — OWS is SP or HTAB — lives at
RFC 9110 §5.6.3, plain-text line 1774. The S478 registry row's anchor is
`section 5.6.1 List Syntax, subsection 5.6.1.2 Recipient Requirements … plain-text lines
1695-1702`, so it covers neither §5.6.1's own OWS-naming sentence (1670-1672) nor §5.6.3's
OWS production (1774). The entry cites them by RFC section + plain-text line so they stay
traceable, but **no registry row anchors §5.6.3**. If the L1 wants a row-anchored citation
for the HTAB clause, S478's anchor should be widened to include §5.6.1 1670-1672 and
§5.6.3 1774, or a further row opened for §5.6.3. The entry's own §5.6.1 pointer sentence
("optional whitespace (OWS, defined in Section 5.6.3)") is what makes the §5.6.3 hop
legible from the row's own text.

**F3 (out of my scope, L1 action).** The new entry is `unindexed` in
`corpus/README.md` §Coverage map under the round-55 counter
(`unindexed: http-list-and-method-grammar.md`; `index_mismatches` 24 → 25). QUALITY.md's
round-55 criterion is "an entry lands with its index row". No wave-1 seat owns
`corpus/README.md` (ExecC1Repair owns SKILL.md, ExecSourceRows owns SOURCES.md, this seat
owns only the one knowledge file), and the counter was already red at base with 21
unindexed files, so I did not touch README. **The L1 should add a coverage-map row naming
`knowledge/http-list-and-method-grammar.md`.** Note the index counter was already failing
before this round; my file adds one more item to that list but does not change its
verdict.

**F4 (limit of the M37/M40 statements).** The entry says the two v2 cases kill M37 and
M40. ExecC2Mutants' receipt confirms both kills, but records that **M40 is killed through a
subject-side refusal** (the mutant refuses a valid HTAB-separated list as `invalid_input`)
rather than through a semantic mismatch, and M37 through a semantic mismatch. The entry's
wording ("kills mutant M40") is the kill-rule sense and does not overstate; the distinction
is ExecC2Mutants' to weigh. ExecC2Mutants also reports D1: all 40 find strings match the
round-93 frozen `pos-good.py` base and none matches the scored candidate, so these are
mutants of the positive control's bytes rather than of `scripts/conditional_eval.py`. My
entry says "kills mutant M40/M37" as the round's own framing does; it does not assert that
the mutants were mutations of the scored candidate.

**F5 (nothing else found).** No defect found in the frozen instruments this seat read
(`c94_selfassess.py`, `c94_conditional.py`, `freeze.md`, `controls/`), and no defect in the
scout's located quotes or in the two registry rows as landed. The one instrument defect I
can see from the outside is ExecC2Mutants' D2 (M11 is equivalent, so the frozen 40/40
target is unattainable), which is C2's lane-internal business, not this seat's.

## Receipts (copied out of scratch before deletion)

```
fetch: GET https://www.rfc-editor.org/rfc/rfc9110.txt
  status=200 bytes=502941 sha256=21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a
  accessed_utc=2026-11-05T15:00:25Z   (scout's own GET: 2026-11-05T15:00:17Z, identical bytes)
  access record: .ufo/waves/round-94/w1/ScribeEntry/fetch.txt
  retained body of record: .ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt (sha256 as above,
    re-checked after my scratch was deleted)

quote verification (script .ufo/waves/round-94/w1/ScribeEntry/verify-quotes.py, exit 0,
  re-runnable from the lane; reads ../ScoutRFC/rfc9110.txt):
  S477 §9.1   3748-3749  exact=True in_span=True words=20
  S478 §5.6.1 1670-1672  exact=True in_span=True words=15
  S478 §5.6.1.2 1699-1702 exact=True in_span=True words=23
  S478 §5.6.3 1774-1774  exact=True in_span=True words=7
  S473 §13.1.2 5928-5932 exact=True in_span=True words=56
  S472 §13.1.1 5799      exact=True in_span=True words=5
  S473 §13.1.2 5885      exact=True in_span=True words=5
  violations 0
  (the S473/S472 spans are quoted in the entry only as fragments of 8 and 5 units)

entry counters (measured with a throwaway whitespace-token counter, since deleted with the
scratch; the figures are reproducible from the file itself):
  body from H1 = 306 words; everything after the trio = 336 words; total file = 351 words
  first three lines byte-identical to the required trio
  file: 33 lines, 2 356 bytes, sha256 664408d8ee3ae4a718cc0013c1a45be4fd0fed59da82b1e4d5c3eff30aeffb0b

C1 counter on the scratch clone (entry + rows committed, --skip-battery; final entry bytes):
  C1v94 revision=d9ea9ef87c44373831e560a120a83a624e934690 counter=58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a
  lessons=88 entries=82 rows=255 criteria=39 mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=0/8
  predecessor_admits=0/0 floor=2 self_pin=ok met=false            (exit 1; the 15 E5 are SKILL.md rows, ExecC1Repair's scope)
  receipt: .ufo/waves/round-94/w1/ScribeEntry/c1-entry-and-rows.txt

C1 counter on the scratch clone with the entry but the BASE SOURCES.md (coupling test,
  scratch commit 947d30b747aa8fec11f15aad6c4273d03cce0860 = ba667b24 tree + the entry only):
  C1v94 revision=947d30b7… mismatches=16 E1=0 E2=0 E3=1 E4=0 E5=15 pins=ok … met=false  (exit 1)
  E3 detail: {"class":"E3","path":"corpus/knowledge/http-list-and-method-grammar.md",
              "detail":"unresolved row id S477, S478"}
  identity_missing: []

corpus-contract on the scratch clone: 0 findings, 82 knowledge entries, exit 0
readme-index counter on the scratch clone: exit 1,
  index_mismatches=25 knowledge_files=88 met=False
  unindexed: http-list-and-method-grammar.md
```

## Limits

- Nothing was committed, staged, pushed or mutated in LANE; no git write command was run
  against LANE. The only commits were inside a disposable clone under scratch.
- No tool was installed or upgraded (none needed); no host sysctl was touched; no
  `pacman` command was run.
- One GET, to the single URL named in the round (the RFC text); its bytes are identical to
  the digest already pinned in rows S471-S476, so the entry's line numbers are stable
  against the lane's existing pins.
- The entry is knowledge only: no gate, no script, no live surface was fetched or measured,
  and no claim is made about any deployed host's behaviour.
- The three "does not decide" items (quoted comma inside an entity-tag, empty list
  elements, obs-text) are stated as routed to contract v2 by the round-93 lesson; this
  seat did not decide them and did not touch any contract or counter.
- The M37/M40 kill statements inherit the C2 population's own limits (F4): the mutants are
  of the round-93 positive control's bytes, and M40 is killed via a refusal path.
