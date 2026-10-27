# ReviewerGateSpot — hostile non-author gate spot-check (round 63)

Role: simulated hostile non-author spot-check of the round's two gate
decisions recorded in `corpus/lessons/round-63.md` §Gate (`:32-48`):

- **Admit (a):** the S432 Fetch §3.6 field-purpose span, classed
  `collapsed-only` (`corpus/lessons/round-63.md:32-39`).
- **Reject (c):** `considerthese/2026-10-26.md` proposal 2, the daily
  git-log receipt-rewrite watch (`corpus/lessons/round-63.md:43-48`).

Method: for each decision I re-opened the underlying sources at the
measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` (and the live
tree `15eb965c`), built the strongest honest disagree case I could, then
weighed it. All commands below were run read-only against
`/home/vgpnk/Projects/shokunin/kake-shokunin` except one re-derivation
written to `/fast/scratch/hyaku/kake-r63/ReviewerGateSpot/` (deleted).

---

## Decision 1 — Admit: S432 §3.6 span as `collapsed-only`

### Evidence re-opened (all verified, none fabricated)

- Retained raw blob `.ufo/waves/round-61/sources/S432.html`, lines
  6149-6155. The sentence is fragmented by inline markup:
  line 6150 `response <a …>header</a> can be used to require checking of a
  <a …>response</a>’s`; line 6151
  `` `<code>Content-Type</code>` `` … `<a …>header</a>`; line 6152
  `against the <a …>destination</a> of a`; line 6153
  `<a …>request</a>.` The field name itself sits in the §3.6 heading
  (`` `<code>X-Content-Type-Options</code>` header``, line 6149) and the
  `<dfn>` on the same line.
- Derived flat text `.ufo/waves/round-63/quote-class/S432.txt`, sha256
  `8b90d096…2a69` — re-derived byte-identical:
  `python3 .ufo/waves/round-63/quote-class/extract_text.py --raw
  .ufo/waves/round-61/sources/S432.html --out <scratch>/S432.rederived.txt`
  → same sha256 `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`.
- Ledger `.ufo/waves/round-63/quote-class/quote-classes.json` sha256
  `5f48e26b…0c42d` at measured commit — matches contract pin.
  Both blob digests verify at `05b0d7f4`:
  raw `63b0a018…911b`, text `8b90d096…2a69` (`git show <rev>:<path> | sha256sum`).
- Live re-open record: `.ufo/waves/round-63/sources/S432.live.html`
  (1,854,393 bytes) — the same §3.6 block is present at the same place;
  `git show 05b0d7f4:…S432.html | sha256sum` = `63b0a018…911b`, matching
  the lesson's byte-identical claim.
- Round-50 rule, `corpus/QUALITY.md:1100-1106`: *"a span that survives
  only whitespace collapse is `collapsed-only`. The class is recorded
  together with the sha256 of both blobs"* — with the operational test
  "comparing the span against both retained blobs."
- Round-50 precedent: `.ufo/waves/round-50/c50_quote_class.py:101-106`
  `classify` = "in raw → raw-substring; in text only → collapsed-only";
  BLOBS table `:49-52` pins `S273.txt`/`S273.raw.html` under
  `.ufo/waves/round-49/sources/`.
- Round-49 provenance, `corpus/lessons/round-49.md:34`: "The S273 quote is
  a substring after whitespace collapse, not of the raw HTML. The counter
  scores the collapsed blob committed at `.ufo/waves/round-49/sources/S273.txt`."
- Mechanical check (this seat ran it):
  - S273 quote ∈ `' '.join(S273.raw.html.split())` → **True** (pure
    whitespace collapse suffices; text-blob test and collapse test
    coincide).
  - S432 ledger quote ∈ `' '.join(S432.html.split())` → **False**; ∈
    `S432.txt` → **True**. Whitespace collapse does NOT suffice; markup
    stripping is required.
- `scripts/quote_class.py:32-36` same two-blob `classify`; selftest case
  `s432_real` (`:63-71`) expects `collapsed-only`; after-c2 receipt prints
  `selftest=4/4`.
- Frozen counter `c63_calibration.py:59-67` inlines the same classify;
  receipt `controls/after-c1.txt` prints `derived=collapsed-only … met=true`.
- Round-62 criterion `corpus/QUALITY.md:1412`: "keep a field's purpose
  separate from claims about its exact value or algorithm," grounded in
  the same r61 spot-check; criterion names the located proposition
  (X-Content-Type-Options / Content-Type / destination — all present).
- The grounded section `corpus/knowledge/response-header-expectations.md`
  `xcto_nosniff_value` (`:69-96`) attributes to S432 both the field's
  purpose and the nosniff value rule; the `[r63-correction]` block
  (`:222-250`) quotes the span and calls it "a field-purpose statement,
  kept separate from the nosniff-only value rule per the round-62
  criterion." No-harm verified: the `[r62-correction]` block (`:218-220`)
  is preserved verbatim above it; SOURCES.md S432 row (`:178`) unchanged
  (`mined`, `2026-10-27` recheck).

### Strongest honest disagree case

**The label `collapsed-only` is wrong under the written rule, and the
admission silently extends the rule rather than naming a new class.**

1. The round-50 rule's normative gloss is explicit: `collapsed-only` =
   "survives *only whitespace collapse*" (`QUALITY.md:1102-1103`). The
   S432 span does not survive whitespace collapse of the retained raw —
   verified: the ws-collapsed raw does not contain it (output above).
   It survives only markup stripping + whitespace collapse — a strictly
   stronger normalization, because the sentence crosses `<dfn>`,
   `<code>` and `<a>` element boundaries.
2. The precedent is sharper than the lane admits. S273 (the canonical
   `collapsed-only` case) *does* survive pure whitespace collapse of its
   raw blob — verified True above. So in round 49/50, "substring of the
   committed text blob" and "survives whitespace collapse" coincided;
   the rule's operational test and its prose gloss were observationally
   equivalent. Round 63 is the first case where they diverge, and the
   gate kept the operational test while the written gloss went
   unamended. Under a literal reading of the committed rule, the honest
   derivation is "absent under whitespace-collapse; present under
   markup-strip" — a class with **no name** in QUALITY.md.
3. This is not cosmetic for the claim. `c63_calibration.py:139-143`
   requires `derived == "collapsed-only" == row.matchClass`; under the
   written-gloss derivation the derived class is not `collapsed-only`,
   `class_match=0`, `quote_correction=0`, `met=false`, and C1 is
   unprovable. The green depends on the operational widening — the same
   kind of predicate-semantics gap the round exists to repair.
4. "Its own two blobs" is stretched: S273's text blob was a *retained*
   capture (round-49 committed mirror); S432's text blob is a lane
   artifact *generated this round* from the other blob. The recipe is
   committed and deterministic (verified byte-identical re-derivation),
   and the ledger is honest about it ("substring of the committed
   flat-text rendering only" — `quote-classes.json:15`), but the class
   is now recipe-relative: a different reasonable recipe (e.g., one that
   decorates `<code>` with backticks) yields a flat text where this
   quote is absent → `absent`, different class, different verdict. The
   round-50 rule pins blob sha256s, not a recipe, and the r63-correction
   still says "its two retained blobs" (`response-header-expectations.md:226`)
   — one is retained, one is derived.
5. Minor record defect: the lesson's re-open record quotes
   "response header can be used to require checking of a response’s
   Content-Type header against the destination of a request"
   (`round-63.md:56-58`) — this is **not** a substring of the committed
   flat text (verified False): it drops the leading
   "The `X-Content-Type-Options`" words *and* the literal backticks
   around `Content-Type`. Quoted in quotation marks and labeled
   "Located quote … ≤25 words", it is a third span that differs from
   both the ledger quote and the r63-correction quote.

### Weighing it — does the admit survive?

**Yes, on substance; with a recorded label-fidelity defect.** Everything
that grounds the admission is real: the span is verbatim located text
(the backticks are literal source bytes, not recipe decoration — raw
line 6151 `` `<code>Content-Type</code>` ``); the recipe is committed,
deterministic, and reproduces the pinned blob; the ledger is honest
about the derivation rather than laundering it as a raw substring (the
exact sin round-62 avoided); the live re-fetch is byte-identical; the
span is 21 whitespace tokens (within the 6–25 rule); and it genuinely
states the proposition the knowledge section attributes to S432 —
the section's own first line is "gives the field its purpose." The
disagree damages *rule fidelity*, not *grounding*: the correct verdict
shape is "admit, but the class needs either a new name
(`rendered-only`/`markup-stripped`) or a QUALITY.md amendment recording
that `collapsed-only` means the operational two-blob test (in flat-text
blob, not in raw), plus fix the lesson's misquoted 'Located quote'."
A hostile reviewer can fairly say the lane admitted under a rule that,
read literally, does not cover the case — and that this is the second
consecutive round where the S432 row's evidence story needed repairing.
But they cannot say the evidence was fabricated or the proposition
unsupported; the substantive-support criterion (`QUALITY.md:1412`,
authored round 62) is satisfied by construction.

Residual risk: any future reader applying the written gloss
("whitespace collapse") to audit `quote-classes.json` will derive a
contradiction the ledger does not flag — the note *describes* the
derivation but never admits the gloss divergence. Severity: low-medium;
fix is one sentence in QUALITY.md or a renamed class in a later round
(precedent exists: classes are lane-internal labels, and
`markup_collapsed_only` already exists as a *selftest fixture id* in
`scripts/quote_class.py:49` — the vocabulary for the honest name was
already in the tree).

---

## Decision 2 — Reject: considerthese proposal 2 (receipt-rewrite watch)

### Evidence re-opened

- Proposal text `considerthese/2026-10-26.md:30`: *"Receipt-rewrite
  watch. Each day, list files under `.ufo/waves/round-*/controls/` that
  have more than one commit touching them (`git log --follow`), and flag
  any whose `revision:` or result line changed after the first commit.
  r56 and r57 both did this and only the verifier caught it; it's a
  cheap read I can do from GitHub."*
- Reject reason `corpus/lessons/round-63.md:43-48`: "aggregate
  bookkeeping; the semantic class it watches (receipt rewrites) is
  already countered by `c58_receipt_rewrites.py`, and a git-log watch
  adds a second ledger without adjudicating anything. Flip: repeated
  verifier/gate comparisons showing the semantic counter misses a
  receipt-rewrite class the log watch would catch."
- The counter `.ufo/waves/round-58/c58_receipt_rewrites.py`:
  - Surface (docstring `:14-17`): every path ever committed under
    `.ufo/waves/round-<N>/control(s)/` — **any round, any depth** —
    on the first-parent line, vs. the disclosure ledger
    `.ufo/waves/round-58/receipt-rewrites.json`.
  - Predicate (`:64-65`, `:231-238`): `undisclosed==0 AND phantom==0 AND
    malformed==0 AND wrong_kind==0 AND unpointed==0 AND symlinks==0 AND
    new_rewritten==0 AND new_receipts==2`; only `new_rewritten` and
    `new_receipts` are round-58-scoped (`NEW_RE`, `NEW_RECEIPT_RE` `:68-69`).
    `undisclosed` covers *all* rounds — an undisclosed rewrite of any
    round's receipt flips it red at any later tip.
  - Byte-level `classify` (`:140-170`): distinguishes
    append/format/pin-only/pending-fill/content/delete/readd — strictly
    more adjudication than the proposal's "revision:-or-result-line
    changed" heuristic, which false-positives on disclosed appends and
    errata entries.
  - Declared limits (docstring `:50-52`): receipts **outside**
    `control(s)/` dirs not covered (79 such rewrites noted
    w1/ExecEventsIndependent); side-branch states; pre-push history
    rewrites; note-prose truth.
- Is the counter actually *live*? Yes:
  `SKILL.md:1293` registers it as an offline gate; r59 re-ran it at its
  tip (`ExecHistoricalGates.md:44`, `ReviewerNoHarm.md:18` — `met=True`,
  events=19); r60 seat tables list it live (`ExecC1Registered.md:22`).
  This seat re-ran it on the current tree:
  `python3 .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision HEAD`
  → `events=19 undisclosed=0 phantom=0 … new_receipts=2 met=True`,
  exit 0 — i.e., **zero** receipt-touching commits exist anywhere on the
  first-parent line after the 19 ledgered r52-r57 events, and the ledger
  covers all of them.
- The motivating events: r56 relabelled two receipts' `revision:` lines;
  r57 committed a `pending` C1 receipt and filled it later
  (`considerthese/2026-10-26.md:19`); both surfaced only via verifier
  spot-checks (`round-57-verifier-spotcheck.md` §5 D1 per c58 docstring),
  not via the external daily read that was already running — i.e., the
  daily read demonstrably missed the class in its own window.

### Strongest honest disagree case

1. **The stated reason mischaracterizes the mechanism.** The proposal
   writes no ledger — "a git-log watch adds a second ledger" describes
   something the proposal isn't. It is a *detection read* that produces
   flags; adjudication happens in the daily report prose. The lane's
   reject argued against a heavier artifact than was proposed.
2. **The reject answers a question that wasn't asked.** The proposal is
   for the *external reflection's own daily read* ("a cheap read I can
   do from GitHub"), not for lane machinery. Recording it as
   "Reject (c), not implemented" treats an external-workflow suggestion
   as a lane-adoption candidate; the lane cannot implement or refuse a
   read the author performs outside it. The accurate disposition is
   "out of lane scope" — which is a different, thinner reason.
3. **"Already countered" conflates machinery with cadence.** c58 exists
   and was re-run at r59/r60, but is an offline check performed at
   discrete tips, not a daily check. Between a run and the next run, an
   undisclosed rewrite can remain unchecked. The proposal targets that
   latency and an independent vantage; the lane's own history (r56, r57)
   shows the reported rewrites were caught at verifier spot-checks. The
   reject does not assess that cadence/vantage delta.
4. **The flip condition is awkwardly framed, but not proved unreachable.**
   It asks for repeated verifier/gate comparisons showing a class the
   semantic counter misses but the log watch catches. On the stated
   current-tip, first-parent receipt population, c58's event surface
   appears broader: it checks all control(s) paths, while the watch
   specifically flags paths with multiple touches and selected changed
   lines. However, proposal `git log --follow` does not specify
   first-parent traversal; c58 explicitly does (`--first-parent`,
   docstring `:14-17`). A merged side-branch history or other difference
   in Git-log semantics could therefore produce a genuine coverage
   difference. The lane did not test this, so calling the flip
   unreachable is stronger than the evidence permits. A better flip
   condition would name either this traversal difference or the distinct
   cadence/vantage delta (an undisclosed rewrite reaches a verifier or
   later round before a c58 re-run flags it).
5. The strongest reason the reject survives: c58's `undisclosed`
   component covers all undisclosed rewrites in any round's controls
   tree on the measured first-parent line whenever run, with better
   byte-level adjudication than the revision/result-line heuristic.
   Today it prints `undisclosed=0` over 19 historical events and all
   subsequent first-parent commits. The watch's remaining value is
   earlier detection between c58 runs, an independent vantage, and
   possibly different Git traversal semantics; the proposal does not
   specify the latter.
### Weighing it — does the reject survive?

**Yes on outcome, no on stated reasoning.** The decision not to build
the watch as lane work is defensible: it substantially overlaps a
registered live gate's event surface, whose byte-level adjudication is
stronger, and its clear delta is cadence/vantage — thin against a
counter that prints `undisclosed=0` on demand. But the recorded reason
contains two factual defects (the "second ledger" mischaracterization;
treating an external daily-read proposal as a lane-implementation
decision) and the flip condition does not test the potential difference
in traversal or cadence/vantage. A hostile reviewer cannot overturn the
outcome — the machinery genuinely exists, is registered in SKILL.md,
and verifies green on the live tree — but can fairly say the gate's
stated grounds are incomplete. Cost of the honest fix: explain that the
proposal substantially overlaps the live c58 gate, then use a flip
condition that tests side-branch traversal or an undisclosed rewrite
reaching a verifier before a c58 re-run.

---

## Verdict

| Gate decision | Survives hostile spot-check? | Notes |
|---|---|---|
| Admit (a): S432 span `collapsed-only` | **Survives on substance; recorded defect** | Grounding, disclosure, digests, recipe, live re-fetch all verified. `collapsed-only` label diverges from the written round-50 gloss ("whitespace collapse") — span requires markup stripping; needs a new class name or QUALITY.md amendment. Lesson `:56-58` "Located quote" is not a substring of the flat text (verbatim-record defect). |
| Reject (c): considerthese proposal 2 | **Survives on outcome; reason incomplete** | Live c58 gate overlaps the proposal's receipt surface and adjudicates byte-level classes (verified `met=True`, `undisclosed=0`, events=19 at tip `15eb965c`). Reason mischaracterizes the watch as a "second ledger" and does not weigh cadence/vantage or unspecified Git-log traversal; flip condition needs those dimensions. |

Neither decision flips under a hostile reading; both gate records carry
smaller fidelity defects a non-author review should note and the lane
should repair append-only.

## Verification performed (commands and outputs)

- `git -C kake-shokunin show 05b0d7f4:<path> | sha256sum` for
  `round-61/sources/S432.html` → `63b0a018…911b`;
  `round-63/quote-class/S432.txt` → `8b90d096…2a69`;
  `quote-classes.json` → `5f48e26b…0c42d`;
  `c63_calibration.py` → `bcd16f68…3fc91`; `scripts/quote_class.py` →
  `431e75e8…1f14`. All match contract pins.
- `python3 .ufo/waves/round-63/quote-class/extract_text.py --raw
  .ufo/waves/round-61/sources/S432.html --out
  /fast/scratch/hyaku/kake-r63/ReviewerGateSpot/S432.rederived.txt` →
  byte-identical sha256 `8b90d096…2a69` (scratch dir deleted after).
- Python substring probes (quoted above): S273 ws-collapse True /
  raw False / text True; S432 ws-collapse **False** / raw False /
  text True; lesson re-open quote in flat text **False**.
- `python3 .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision HEAD`
  → `events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0
  unpointed=0 symlinks=0 new_rewritten=0 new_receipts=2 met=True`, exit 0
  (tip `15eb965c1d0f`).
- Ledger census: `receipt-rewrites.json` events by round =
  `{round-52: 6, round-54: 5, round-55: 4, round-56: 3, round-57: 1}` —
  includes the r56/r57 rewrites as disclosed events.
- Receipts read (not re-run): `controls/after-c1.txt` `met=true` exit 0;
  `after-c2.txt` `present=1 selftest=4/4 frozen_cases=ok met=true`;
  `base-c1.txt` `met=false` exit 1; `control-marker-fixture.txt` old
  c62 `met=true` / c63 `met=false`; `control-junk-fixture.txt` `met=false`.
- Tooling: no installs; pacman untouched. Writes: this report and one
  scratch re-derivation under `/fast/scratch/hyaku/kake-r63/ReviewerGateSpot/`
  (deleted). No commits, no registry edits, no .ufo/state changes.
