# ScribeLedger — round 88 single v1 wave

## Behavior and axes

Draft-only deliverable completed. Axes: calibration (lowest owned axis, 2 HOLD)
and freshness (10 HOLD). This seat claims no score change, no counter success,
no CLI success and no outside admission. L1 alone integrates independent
candidates; no canonical byte was changed by this seat.

Two candidate files were drafted, both in the seat's own directory:

- `.ufo/waves/round-88/w1/ScribeLedger/gate-agreement-metadata.md` — the D1
  companion entry candidate.
- `.ufo/waves/round-88/w1/ScribeLedger/cache-current-age.md` — the D3
  corrected-entry candidate.

Base commit: `f4479c14813037ad993a49a3dee4028763470f7a`. Freeze named in the
seat brief: v2 `8063739791e21a8d7966fd968913e552e1433881`.

**Freeze moved under this seat (verbatim observation).** While the seat was
working, the lane HEAD advanced to a v3 amendment, commit
`52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`, "round-88: freeze amendment v3 —
validation precedes the wildcard rule", committed 2026-11-04 15:58:05 -0300,
i.e. after `w1.ready.dispatched` (15:52:15). The v2→v3 diff touches
`.ufo/waves/round-88/c88_vary.py` (the `if star: return 'mismatch'` block moves
from before the `normalise()` calls to after them), `.ufo/waves/round-88/contract.md`
(freeze-history paragraph rewritten; constant-stub control numbers restated from
`9/20 + 112/200` and `4/20 + 21/200` to `9/20 + 109/200` and `4/20 + 24/200`;
the sentence "Adapter precedence is declared: input validation runs before the
wildcard rule, so a malformed header map is refused even when the Vary value
contains `*`." added), and the four C2 control receipts. The C1 counter
`.ufo/waves/round-88/c88_defect_queue.py`, the 20-case set
`vary-cases.json` and the three frozen blobs are byte-identical between v2 and
v3 (`git diff 80637397 52e41d2d -- .ufo/waves/round-88/c88_defect_queue.py
.ufo/waves/round-88/vary-cases.json .ufo/waves/round-88/frozen/` is empty), so
no D1 item, case, threshold, control or target moved. Both C2 counter
selftests pass on the current tree (C1 11/11 exit 0; C2 17/17 exit 0; the C2
stub scores are now 7/20+67/200, 9/20+109/200, 4/20+24/200). This seat's
drafts are C1-only and are unaffected by the v3 C2 precedence change.

## Artifacts / touched surfaces

All writes are new seat-owned files plus this report:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger/gate-agreement-metadata.md`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger/cache-current-age.md`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger/c1-counter-receipts.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger/d3-diff-receipts.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger/counter-defects.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ScribeLedger.md`

Nothing under `corpus/`, `scripts/`, `SKILL.md`, `LOG.md` or `SCORECARD.md` was
written, edited or deleted by this seat. No commit, no push, no mutating git or
jj command was run. The scratch root `/fast/scratch/hyaku/kake-r88/ScribeLedger/`
was created explicitly, used for read-only counter runs plus three mirror trees
and two mutant trees, and was deleted after the receipts were copied into the
seat directory. No tree was written under `/tmp`; no `/tmp` path is cited as
evidence. No tool was installed or upgraded by this seat, so there is no
tool/version/channel record to report.

## D1 — the companion entry candidate

File: `.ufo/waves/round-88/w1/ScribeLedger/gate-agreement-metadata.md`.

Provenance trio, lines 1–3, all filled:

```
source: corpus/knowledge/gate-agreement-ledger.json — lane path /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/gate-agreement-ledger.json; ledger sha256 ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506; per-row provenance under .ufo/waves/round-87/snapshots/ (round-84/85/86 verifier spot-checks).
verified-at: 2026-11-04 — ledger bytes re-hashed from the frozen round-88 copy .ufo/waves/round-88/frozen/base-gate-agreement-ledger.json (sha256 ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506) and from base f4479c14813037ad993a49a3dee4028763470f7a; the three per-row snapshot digests re-hashed from the snapshot files themselves; round-88 counter .ufo/waves/round-88/c88_defect_queue.py (item D1-ledger-companion).
recheck: 180d or whenever a verifier spot-check adds, re-decides or withdraws a row; re-hash the ledger and re-read the eight rows; any ledger byte change invalidates the digest quoted above and must be accompanied by a revision of this companion.
```

The sha256 was computed by this seat, not copied from the counter:

```
$ sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/frozen/base-gate-agreement-ledger.json
ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/frozen/base-gate-agreement-ledger.json
```

The same digest reproduces from the base commit blob and from the live lane
worktree copy, so the ledger bytes are unchanged from base:

```
$ git -C LANE show f4479c14813037ad993a49a3dee4028763470f7a:corpus/knowledge/gate-agreement-ledger.json | sha256sum
ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506  -
$ sha256sum LANE/corpus/knowledge/gate-agreement-ledger.json
ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506  LANE/corpus/knowledge/gate-agreement-ledger.json
```

All eight ledger rows are tabulated with round, item, decision and outside
verdict, in the ledger's own file order. The table was checked against the
JSON row by row by script; all eight rows match exactly:

| Round | Item | Decision | Outside verdict |
|---|---|---|---|
| 84 | S457 response max-age semantics | admit | agree |
| 84 | §4.1 normalization as response-directive reorder proof | reject | agree |
| 84 | §5.2.2.2 as max-age anchor | reject | agree |
| 85 | S458 field-specific algorithm | admit | agree |
| 85 | Blanket response-policy reorder equivalence | reject | agree |
| 86 | S459 CrUX Vis docs | admit | agree |
| 86 | S461 RFC 9111 slice | admit | agree |
| 86 | RFC 7234 minimum-duplicate attribution | reject | agree |

Each row's own `source` snapshot path and sha256 were re-hashed from the
snapshot files; the three distinct digests reproduce exactly:

```
$ sha256sum .ufo/waves/round-87/snapshots/round-84-verifier-spotcheck.md
80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9
$ sha256sum .ufo/waves/round-87/snapshots/round-85-verifier-spotcheck.md
948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71
$ sha256sum .ufo/waves/round-87/snapshots/round-86-verifier-spotcheck.md
47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b
```

The entry states the three explanatory points the item required: the file is
evidence metadata under `knowledge/` holding closure-owned decisions and is not
a sourced domain claim (no SOURCES row, no external document to open, quote
and date); the companion exists because a JSON file cannot open with the
provenance trio `source:`/`verified-at:`/`recheck:` that a `knowledge/` entry
must carry, and because the quoted sha256 binds the companion to the exact
ledger bytes, so a ledger change invalidates both; and the ledger bytes are
unchanged from base. The bound is stated explicitly: the entry proves that the
record exists and that each row points at the snapshot whose digest is
recorded — it does **not** prove that an assessment was performed, that the
decision was correct, or that decision accuracy improved. A reader wanting a
row's substance must open the cited spot-check snapshot; the row's own
`source` path is the authority.

## D3 — the corrected-entry candidate

File: `.ufo/waves/round-88/w1/ScribeLedger/cache-current-age.md`, seeded as a
byte copy of `frozen/base-cache-current-age.md` (both sha256
`8bbbeb9edf7e595b2e3edabb39d44c9f0716091bea441b44ece79265c3f07eef` before the
edit) and then edited with exactly two operations.

Operation 1 — the `recheck:` line (base line 3) replaced. The old line named
the ephemeral tokens `/fast/scratch` and `TMPDIR=`. The new line keeps a 180d
cadence, names no ephemeral token, and points at the checklist:

```
recheck: 180d or source/adapter change; GET https://httpwg.org/specs/rfc9111.html#age.calculations and compare §4.2.3 equations; the offline selftest command is checklist item 6 below (it creates its own temporary directory; no fixed scratch path is named here).
```

Operation 2 — one appended checklist item, inserted as item 6 of the existing
"Runnable checklist", carrying the required command verbatim:

```
6. Offline selftest without a fixed scratch path: TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; the shell creates the temporary directory per invocation and it is not a citable evidence path.
```

Proof by `diff -u` against the frozen base (full output in
`w1/ScribeLedger/d3-diff-receipts.txt`):

```
$ diff -u LANE/.ufo/waves/round-88/frozen/base-cache-current-age.md LANE/.ufo/waves/round-88/w1/ScribeLedger/cache-current-age.md
@@ -1,6 +1,6 @@
 source: S462 — …
 verified-at: 2026-11-04 — …
-recheck: 180d or source/adapter change; GET …; offline command TMPDIR=/fast/scratch/hyaku/kake-r87/L1 python3 -B scripts/cache_current_age.py --selftest (create the explicit scratch directory first).
+recheck: 180d or source/adapter change; GET …; the offline selftest command is checklist item 6 below (it creates its own temporary directory; no fixed scratch path is named here).

@@ -70,6 +70,7 @@
    …
    invocation but not a discriminator against constant-zero/Age-only shortcuts.
+6. Offline selftest without a fixed scratch path: TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; the shell creates the temporary directory per invocation and it is not a citable evidence path.

 The frozen counter's 17-case equality is weaker than the complete adapter
diff exit=1
```

Exactly one replaced line and one insertion, confirmed by the counter's own
opcode algorithm over the same two files:

```
replace: base lines 3-3 -> new lines 3-3
insert: base lines 74-73 -> new lines 73-73
replace count = 1
insert count = 1
delete count = 0
base line numbers not carried verbatim into the draft: [3]
```

Line 3 is the replaced `recheck:` line; every other base line is carried
byte-identically and in order. The draft's digest is
`69921db1af2f2d03ac5967ddd2f9862ff4d70c915a27706d3fd0bccbbf2d5912`.

## Counter behaviour (read-only runs; receipts in `w1/ScribeLedger/c1-counter-receipts.txt`)

```
$ python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --selftest
selftest: 11/11 passed            exit=0

$ python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --root LANE --revision f4479c14813037ad993a49a3dee4028763470f7a --work <scratch>/work2
C1v1 revision=f4479c14813037ad993a49a3dee4028763470f7a items=3 open=3 closed=0 met=false
{"D1-ledger-companion": ["companion entry missing"], "D2-diagnostic-type": ["float input diagnostic does not name float (or still says boolean)"], "D3-recheck-path": ["recheck line still names an ephemeral path token '/fast/scratch'", "recheck line still names an ephemeral path token 'TMPDIR='", "entry body lacks the mktemp-form offline selftest command"]}
exit=1

$ python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --mirror <scratch>/mirrorA --work <scratch>/work     # seat drafts + BASE tool
C1v1 … open=1 closed=2 met=false
{"D1-ledger-companion": [], "D2-diagnostic-type": ["float input diagnostic does not name float (or still says boolean)"], "D3-recheck-path": []}
exit=1

$ python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --mirror <scratch>/mirrorB --work <scratch>/work     # seat drafts + counter's repaired-tool fixture
C1v1 … open=0 closed=3 met=true
{"D1-ledger-companion": [], "D2-diagnostic-type": [], "D3-recheck-path": []}
exit=0
```

mirrorA and mirrorB are scratch trees holding the frozen base ledger bytes,
this seat's two drafts, and respectively the base tool and the counter's own
`repaired_tool_bytes()` fixture. Read against that fixture, this seat's D1 and
D3 drafts close their two items and the whole C1 predicate is met. The
remaining D2 failure in mirrorA is the base tool's defect and belongs to the
tool-owner seat; this seat does not touch `scripts/cache_current_age.py`.

The lane's read-only corpus shape gate over the seat drafts is clean:
`node LANE/scripts/corpus-contract.mjs --root <scratch>/mirrorB` →
`0 findings · 2 knowledge entries · 82 lane lessons · 72 skipped · 0 errors —
exit 0`. On the unmodified live lane the same gate reports three pre-existing
findings unrelated to this seat — `missing_metadata:corpus/knowledge/meta-robots-directives.md:{source,verified-at,recheck}` — i.e. the live lane's corpus gate is already red at this revision and this seat neither caused nor fixed it.

## Findings — defects in the round's own C1 counter

Both are in the frozen instrument `.ufo/waves/round-88/c88_defect_queue.py`.
Reproduced by this seat; full transcripts in `w1/ScribeLedger/counter-defects.txt`.
Neither defect changes the shipped drafts, which satisfy the stricter
contract reading as well as the counter.

**A. `item_d3` accepts an ISO date in place of a cadence.** The contract
requires D3 to "keep a cadence in its single `recheck:` line". The counter's
predicate is `rest[:1].isdigit() and ('d' in rest.split()[0].lower() or
rest[:4].isdigit())`, so a recheck line opening with `2026-11-04` passes on the
`rest[:4].isdigit()` branch carrying no cadence interval at all. Mutant:

```
mutant entry recheck: line =  recheck: 2026-11-04 — reopened; see checklist.
counter result: {'D1-ledger-companion': [], 'D2-diagnostic-type': [], 'D3-recheck-path': []}
D3 flagged? False
```

**B. `item_d1` does not require the sha256 on the `source:` line.** The
contract requires the `source:` line to name the ledger path *and* to quote
the ledger's full sha256. The counter checks the digest with `digest not in
text` over the whole companion, so a companion that names the path in
`source:` and relegates the digest to a later paragraph passes D1. Mutant
(digest removed from `source:`, still present in the body):

```
counter result: {'D1-ledger-companion': [], 'D2-diagnostic-type': [], 'D3-recheck-path': []}
D1 flagged? False
```

A third, weaker observation, not a defect in the counter but a limit of its
D1 conjunct: the ledger-bytes check compares the candidate ledger against the
frozen base copy and the sha256 check compares the digest string against the
companion text. Neither checks that the digest in the companion is the digest
of *that* ledger — but because the frozen copy is the comparison basis and the
counter's own `wrong-digest` and `altered-ledger` mutants are both killed in
the selftest, the combination is sound enough for the round. The item's own
phrase "readable only from its bytes" is therefore only enforced through the
frozen-copy equality, not through a re-derivation from the candidate ledger.

No defect was found in the frozen `vary-cases.json` 20-case set: all rows
parse, the ids are 1–20 unique and sequential, the exits and verdicts are
well-formed (7 match, 9 mismatch, 4 invalid), and the counter's own reference
oracle reproduces all 20 frozen verdicts (selftest 17/17). No duplicate
lower-cased field names occur in either the frozen set or the 200 seeded
cases, so the reference's "ambiguous duplicate name, refused" branch is
unexercised by the frozen population — an untested branch, not a wrong one.

## Honest limits

- Draft-only. This seat produced candidate bytes; it did not integrate,
  commit, publish or score anything, and it claims no admission.
- The D1 companion is a *candidate* for `corpus/knowledge/gate-agreement-metadata.md`;
  the file does not exist in the lane yet and its final name, wording and
  placement are L1's decision.
- The D3 candidate is a *candidate* for `corpus/knowledge/cache-current-age.md`;
  the live lane copy is still the base file (sha256
  `8bbbeb9edf7e595b2e3edabb39d44c9f0716091bea441b44ece79265c3f07eef`) and is
  byte-identical to the frozen base copy. This seat did not edit it.
- The mirror runs are read-only counter evaluations over scratch trees; they
  are evidence that the drafts close D1 and D3 under the frozen counter, not
  a claim that the round's C1 predicate is met at any committed revision.
- The D1 entry proves the ledger record exists and is bound to the quoted
  bytes. It does not prove any assessment was performed, that any recorded
  decision was correct, or that decision accuracy improved.
- The eight rows' decisions belong to the round-84/85/86 closure sessions and
  the outside verdicts to the outside reviewer; this seat read the ledger and
  the snapshots' digests, and did not re-adjudicate any row.
- The SOURCES row for RFC 9111 §4.1 named in the round description belongs to
  another seat; this seat wrote no SOURCES row and makes no source-access
  claim for that URL.
- The v3 freeze amendment landed mid-wave, after dispatch. It is recorded
  above as observed; this seat did not author it and did not modify any
  frozen byte.

## Out of scope (not attempted)

- `scripts/cache_current_age.py` and the D2 diagnostic line (tool-owner seat).
- `scripts/vary_match.py`, `corpus/knowledge/vary-matching.md` and the C2
  counter/case-set changes (C2 seats).
- The SOURCES registry row, `SKILL.md`, `LOG.md`, `SCORECARD.md` and the
  round-88 lesson appends (L1 and other seats).
- Any corpus edit, commit, push, deploy, publish or account-state change.
