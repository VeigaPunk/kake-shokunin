# ScribeKnowledge — kake round 75, wave w1, attempt 1

Seat: leaf scribe, no dispatch. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin` read-only.
Measured revision: base `c9c5e484c533aa65f4374b841a3edcf572ed19a9`; freeze commit
`88f2e05f36f008faf01fcf77afedd33ae3c53e40`; lane HEAD at read time `ab939c46281bc18bcbe248a83a491ee7b7db76f3`
(wave-ready handoff only; `git diff --stat c9c5e484 ab939c46 -- corpus/SOURCES.md SKILL.md
corpus/knowledge corpus/lessons` empty). The only lane write is this file and the receipt
directory named below.

Axes named: (a) **provenance fidelity** — every sentence cites a located quote or a committed
receipt; (b) **locality** — sources are the bytes I fetched/read this session, not memory;
(c) **scope discipline** — no live-property claim, no claim about another host or lane;
(d) **integration fit** — the three blocks match the shapes the lane already lands
(`corpus/knowledge/*.md` header trio, `corpus/QUALITY.md` round-69 addendum bullet form,
`corpus/lessons/round-74.md` section order).

Deliverables are drafts, not edits. Nothing below instructs a production change; the L1 lands it.

## What I executed (and what I only cite)

| # | Command (abbreviated) | Exit | Observed |
|---|---|---|---|
| 1 | `curl -sS -o s443-statement.md https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md` | 0 | `http=200 bytes=2492` |
| 2 | `sha256sum s443-statement.md` | 0 | `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` — equals contract §Frontier |
| 3 | `awk 'NR>=34 && NR<=58'` on the fetched bytes | 0 | `subject` at 34; the raw-substring sentence `Each element MUST have \`digest\` set.` at **37** (6 words); the 22-word context form spans 36–37 and is not a raw substring; digest-matching sentence at 54–55 |
| 4 | `grep -n "S443" corpus/SOURCES.md` | 1 (no match) | row **absent** at read time → knowledge block uses `source: S443 (pending)` |
| 5 | `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision c9c5e484 --base c9c5e484 --work <scratch>` | **1** | `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false`; both finding lines byte-identical to `controls/base-c1-row-truth.txt`, whose output line differs only by its abbreviated revision (`c9c5e484`); 29 s wall |
| 6 | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest --work <scratch>` | **0** | `selftest 8/8`; the file at `c9c5e484` defines `f1`–`f8` (`run_fixture(work, "fN"` at lines 354–483) |
| 7 | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root . --revision c9c5e484 --work <scratch> --selftest` | **2** | `error: unrecognized arguments: --selftest` |
| 8 | `sed -n '1424,1436p' SKILL.md` + cell split | 0 | row 1426 Kind `gate (live; …)`, Self-test `none (no self-test mode …)`; row 1432 Self-test claims `five frozen fixtures: f1 … f5` |

**Not re-run by me, cited as committed receipts:** the cheap-content control
(`controls/ctl-cheapcontent.txt`: `rows=30 live=18 files=16 mismatches=2 classes=E1 E3 met=false`,
exit 1) and the deletion control (`controls/ctl-deletion.txt`: `files=15 append_only=false met=false`,
exit 1). C2's tool and receipt (`scripts/instrument_receipts.py`,
`corpus/knowledge/instrument-receipts.json`) **do not exist** at read time (`ls` → no such file);
the C2 block therefore describes the frozen §C2 predicate, and says so.

Tooling: nothing installed or upgraded this seat (no `uv tool`, no `npx`, no binary). Host
toolchain used: `python3 3.14.8`, `git 2.56.0`, `curl 8.23.0`.

Input read after the first pass: `w1/ScoutSources.md` (the source seat's report) — HTTP 200, 0
redirects, 2,492 B, sha256 `cbe684a1…a455ebea`, located quote line 37 / 6 words / raw substring.
This draft was reconciled to that form (knowledge body, Gate row, Sources bullet, R6).

---

## (a) Draft — `corpus/knowledge/instrument-receipts.md`

````markdown
source: S443 (pending) — in-toto Attestation Framework, Statement v1 (https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md), opened 2026-11-03, HTTP 200, 2,492 bytes, sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea. Row not yet in `corpus/SOURCES.md` at draft time: contract §Frontier admits it only after the L1 re-opens the source in-round, so the row id is carried as pending and no sourced claim rests on it yet
verified-at: 2026-11-03
recheck: 90d
ground: calibration — whether a landed instrument's recorded capability is bound to the bytes that make the claim
scope: one receipt file and the frozen 16-file population; this entry says nothing about any deployed artifact, any other host, or the truth of a self-test's assertions

# Binding a claim to the bytes that make it

## What a digest-bound receipt is

A receipt is one committed record that names, for each file in a population, the identity of the
exact bytes that carry the capability. The lane's shape is `corpus/knowledge/instrument-receipts.json`,
schema `instrument-receipts/v1`:

    {schema, revision, date, host, files[]}
    files[] entry: {path, sha256, bytes, selftest_mode}

`sha256` and `bytes` are taken from the file's **committed blob at `revision`**, not from the
working tree; `selftest_mode` is true when that blob registers a `--selftest` argument. `--check`
re-derives all three from the same revision and compares.

The receipt's job is narrow, and it is worth stating what it does not do: it does not run
anything. It answers one question per file — *is the thing that claims a capability the same
byte sequence the ruler was cut against?* — and leaves the capability's meaning to another
predicate.

## Why a tally without the artifact digest is not evidence

A tally names a run; a digest names bytes. Round 74 landed three instruments and reported
`selftest 8/8`, `selftest 8/8`, `tests=10 passed=true`; a non-author re-ran all three on the
landed bytes and they passed, yet **no committed receipt named those bytes** and the delivered
files hashed differently from the landed ones — the numbers were true and unbound
(`corpus/lessons/round-74-verifier-spotcheck.md` R5). A later reader had no way to attach the
tally to a file, and a later edit to the file could not invalidate it.

The same rule is in the attestation vocabulary this lane borrows. in-toto's Statement v1 defines
`subject` as an array of ResourceDescriptor objects — the artifacts the attestation applies to —
and requires a digest on each element: "Each element MUST have `digest` set." (S443, 6 words,
line 37, raw substring). The spec adds the matching rule itself: subject artifacts are matched
purely by digest, regardless of content type (lines 54-55, blockquote markers removed and
whitespace collapsed — not a raw substring). That is why a name — or a tally written beside a
name — cannot stand in for one.

## The population rule

The same 16 files the C1 predicate measures, and for the same reason: they are the lane's *live*
instruments. Each live gate-registry table row in `SKILL.md` resolves to one instrument file:

1. the Name cell, when it is itself a `.py`/`.mjs` path;
2. else the first `.py`/`.mjs` token of the Entry-command cell;
3. else of the Self-test cell;
4. else of any cell.

Rows whose Kind cell carries `historical` are outside the population — their claims are pinned to
a past revision by their own cells, and re-deriving them is a separate bounded pass (a decision
recorded in the round-75 contract §C1, not an accident). A row may be superseded by a later
appended row but never deleted; the row *effective* for a file is the last one naming it.

The cell order matters: a naive any-`.py`-token scan finds 18 files, because
`scripts/freshness-sweep.mjs` is mentioned inside another row's prose and
`.ufo/waves/round-46/c46_matrix.py` is a witness citation, not the row's instrument
(`.ufo/waves/round-75/controls/base-c2-receipts.txt`).

## Check semantics

`--check` reads the measured revision through git, never through the filesystem:

- byte length from the committed object (`git cat-file -s <rev>:<path>`);
- sha256 over the committed blob's bytes (`git show <rev>:<path>`);
- `selftest_mode` from the same blob's text (does it register `--selftest`?);
- the population itself re-derived from `<rev>:SKILL.md`, so a new live row grows the population
  the same check measures.

Consequences worth stating because they are the point:

- a dirty working tree, an uncommitted receipt, or a receipt written against a path rather than a
  revision cannot pass;
- a receipt is true only at its `revision`; the next commit that touches a population file
  invalidates it by design — re-cutting the receipt is the acknowledgement, and the commit that
  does it is visible;
- a missing entry, or a missing receipt file, is a mismatch (`bound` 0, `mismatches` = population);
- an entry for a file outside the population is not counted toward `bound` and is reported
  separately;
- `met = (bound == population) and (mismatches == 0)`.

## Limits

- **Identity plus declared capability, never meaning.** `sha256` + `bytes` say *these are the
  bytes*; `selftest_mode` says *this blob registers the flag*. A file whose `--selftest` prints a
  constant and exits 0 binds perfectly. Whether the self-test asserts anything is a different
  predicate, measured by a different artifact (a tally receipt, or a counter that kills the
  fixture).
- **The receipt re-runs nothing.** It converts "trust the prose" into "re-derive the identity at
  a named revision". It does not convert a vacuous check into a meaningful one.
- **A self-consistent forgery is out of reach by convention only.** Anyone who can commit can
  pair an empty instrument with a receipt whose digests re-derive; the digest cannot forbid that.
  What the receipt changes is the cost: from editing one line of prose to writing a commit that
  rewrites both the file and its receipt, in a history a non-author reads. That is a convention
  — an append-only log with an outside reader — not a cryptographic guarantee, and the entry
  should not be cited as the latter.
- **Snapshot, not a standing licence.** The receipt covers the population at its revision. A live
  row added later is uncovered until the receipt is re-cut, and `--check` reports it as a mismatch
  rather than silently widening `bound`.
````

Placement: new file, no existing `corpus/knowledge/instrument-receipts.md`. If the L1 lands the
S443 row before committing this file, replace the first `source:` sentence's pending clause with
the row id and the row's own status cell; the body's S443 quote and line range do not change.

---

## (b) Draft — `corpus/QUALITY.md`, append-only section

````markdown
## Round-75 criterion — registry claims are executable as written (append-only)

Grounding: `considerthese/2026-10-26.md` Part 2 proposal 5 (dated 2026-10-26: keep a list of gates
that go red by design on later trees, so a daily report does not mistake a pinned historical gate
for a regression, and can flag when one *should* have been re-pinned); the round-74 non-author
closure's R1 and R2 (`corpus/lessons/round-74-verifier-spotcheck.md`); the frozen round-75
contract §C1 predicates E1–E4.

- **A gate-registry row's claim is executable as written, and its live/historical label is the
  row's own.** Admit: every live-labelled row (`historical` absent from the Kind cell) names a
  command that runs at the measured revision and whose observed output is the state the row
  records — a `gate` row exits 0 from a `--selftest` the instrument actually registers, or its
  Kind cell declares the differential substitute; a row pinned to a past revision carries
  `historical` in its Kind cell and names the revision it is true at, so a later red is read as
  pinned, not as a regression, and the row is formally the point at which the gate would be
  re-pinned. Reject: a `gate (live …)` row whose instrument has no self-test mode and no declared
  differential; a Self-test cell that enumerates a fixture count the counter does not run; a row
  whose Kind label and Self-test cell contradict each other; silently deleting a red row instead
  of demoting or re-pinning it. Able-to-fail:
  `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision c9c5e484 --base c9c5e484 --work <scratch>`
  prints `mismatches=2 classes=E1 E3 append_only=true met=false`, exit 1
  (`.ufo/waves/round-75/controls/base-c1-row-truth.txt`; re-run by the round-75 scribe with the same
  verdict); the deletion control prints `files=15 append_only=false met=false`, exit 1.

Criteria are not rewritten: this section is the round-75 row, and earlier criteria stand unchanged.
````

---

## (c) Draft — `corpus/lessons/round-75.md` skeleton

````markdown
# Round 75 — lessons (kake, attempt 1)

Base `c9c5e484c533aa65f4374b841a3edcf572ed19a9` (lane master at round open). Frozen contract
`.ufo/waves/round-75/contract.md` at `88f2e05f36f008faf01fcf77afedd33ae3c53e40`. Wave `w1`: one
v1 wave, 14 seats (scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1,
connector 1, sentinel 1; attack share 4/14 = 28.6 %; the L1 held the planner seat).
*Settled count: fill from `.ufo/waves/round-75/w1-results.json` before landing.*

Claims: C1 calibration (owned score 2, the lane's lowest non-retired axis), C2 operability
(owned score 10, HOLD; capability acquisition).

## Claims

**C1 — calibration.** The lane's gate registry stops claiming states its instruments do not
have: every live registry row's claim re-derives by execution, `mismatches` 2 → 0 over the frozen
16-file population. Predicate E1–E4 over the row *effective* for each file (the last row naming
it; a row may be superseded by an appended row, never deleted): E1 a `gate` row carries a working
`--selftest` or declares a differential; E2 a recorded `a/b` tally equals the observed pass/total;
E3 two or more enumerated `f<N>` ids equal the observed total; E4 every `.py`/`.mjs` path token in
the row's cells resolves at the measured revision. `append_only` holds when every live row name at
`--base` is still present at the measured revision; `met = (mismatches == 0) and append_only`.

    python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision <rev> \
        --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work <scratch dir outside the lane>

Base control, re-run by the round-75 scribe (29 s wall, scratch outside the clone):
`C1v1 revision=c9c5e484 rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true
met=false`, exit 1 — `controls/base-c1-row-truth.txt`.
*After-state: fill the tip line here from `controls/after-c1-row-truth.txt`; the frozen target is
`mismatches=0 append_only=true met=true`, exit 0.*

**C2 — operability.** Every live registry instrument is bound to a committed receipt that
re-derives from committed bytes: `bound` 0 → 16 of the same 16-file population, `mismatches`
16 → 0. Receipt `corpus/knowledge/instrument-receipts.json`, schema `instrument-receipts/v1`,
one entry per file `{path, sha256, bytes, selftest_mode}` with `sha256`/`bytes` of the committed
blob at the receipt's revision and `selftest_mode` true when the blob registers `--selftest`.
`--check` re-derives all three at `--revision`; a file counts `bound` only when all three match;
a missing entry or a missing receipt is a mismatch. `met = (bound == population) and
(mismatches == 0)`. The tool derives the population independently from `SKILL.md` and its
after-receipt records that the list equals the C1 counter's list.

    python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check

Base: the receipt file is absent → `population=16 bound=0 mismatches=16 met=false`, exit 1
(`controls/base-c2-receipts.txt`). Fabricated receipt: digests that do not re-derive →
`mismatches=16`; a receipt that drops one path → `bound=15`.
*After-state: fill the tip line here from `controls/after-c2-receipts.txt`; the frozen target is
`population=16 bound=16 mismatches=0 met=true`, exit 0.*

## Gate

- **Admit — S443, in-toto Attestation Framework, Statement v1**
  (https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md), opened
  2026-11-03 by this round's source seat and re-fetched independently by the scribe: HTTP 200,
  2,492 bytes, sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` — the
  contract §Frontier digest, byte-identical. Located quote: "Each element MUST have `digest`
  set." (6 words, line 37, raw substring — the source seat's measured range, reconciled in
  `w1/ScoutSources.md` §1.2). The wider context sentence — "Set of software artifacts that the
  attestation applies to. Each element represents a single software artifact. Each element MUST
  have `digest` set." — spans lines 36-37 and is *not* a raw substring and not a naive
  whitespace collapse: it matches only after line-leading blockquote markers are removed, which
  is why the 6-word sentence is the quote the row records. It grounds C2: an artifact is
  identified by digest, not by name or by a number written beside it. Reason it is admitted
  rather than held: it is a primary spec artifact of the project whose vocabulary the receipt
  borrows, its bytes hash-stable across two independent fetches (the source seat's and the
  scribe's), and its scope is exactly one field (`subject`), not a platform behaviour. **Flip
  condition:** the L1's in-round re-open yields a different byte length or sha256, or the 6-word
  sentence is absent at line 37 → the row is rejected for this round and
  `corpus/knowledge/instrument-receipts.md` loses its source sentence (it must then be retitled
  as an unsourced lane-internal note). At draft time the row is **absent** from
  `corpus/SOURCES.md` (grep exit 1), so the knowledge block carries `source: S443 (pending)`;
  the flip is one-directional — once the row lands with these bytes, the pending clause is
  deleted, not softened.
- **Admit — the superseding row for `c69_tmp_honour.py`** demoting its Kind from
  `gate (live; …)` to `instrument`. Reason: the row itself records that it has no self-test mode
  (`SKILL.md:1426`, Self-test cell: "none (no self-test mode; `--selftest` is an argparse error,
  exit 2)"), and E1 forbids a `gate` family row without a working `--selftest` or a declared
  differential. Confirmed by execution at base: `--selftest` → `error: unrecognized arguments:
  --selftest`, exit 2. The demotion is the honest label; the instrument's three terms are still
  exercised by the base and after controls, so nothing is lost but the false family name.
  **Flip condition:** a later row lands a real `--selftest` over isolated fixtures (or a Kind
  cell naming a concrete differential check the row's own command performs) → the row may be
  re-labelled `gate (live …)`.
- **Admit — the superseding row for `c74_registry_gap.py`** recording the eight fixtures it
  actually runs. Reason: its own Self-test cell claims "five frozen fixtures: f1 … f5"
  (`SKILL.md:1432`) while the committed counter defines `f1`–`f8` (`run_fixture(work, "fN", …)` at
  `.ufo/waves/round-74/c74_registry_gap.py:354,368,382,395,414,438,471,483` at `c9c5e484`) and its
  `--selftest` prints `selftest 8/8`, exit 0 (re-run by this seat). E3 measured 5 enumerated ids
  against an observed total of 8. **Flip condition:** if the counter landed at the tip defines
  exactly five fixtures, this appended row is itself wrong and must be superseded again — the row
  records the count observed at the revision it names, never the count the draft wished for.
- **Reject — "add a `--selftest` to `c69_tmp_honour.py`" as a route for this round** (a rejected
  route, not a rejected source). Reason: out of scope. It is a frozen round-69 counter whose
  claims are already exercised by committed base and after controls; adding a self-test suite
  rewrites the surface of a landed instrument and is a bounded change of its own, while the
  round's declared after-state is a Kind demotion. Choosing the demotion is what the honest-label
  criterion asks for; choosing the rewrite would be scope substitution. **Flip condition:** a
  later round freezes a counter with a real `--selftest` over the same three terms, or the
  operator re-scopes the round-69 counter; then the demotion can be reverted with an appended
  row citing the new receipt.
- **Reject — deleting the failing row as a repair.** The deletion control
  (`controls/ctl-deletion.txt`: `rows=27 live=15 files=15 mismatches=2 append_only=false
  met=false`, exit 1) shows the append-only conjunct catching it: the E3 finding stays and a new
  finding names the missing base row. Deletion is therefore not in the repair vocabulary this
  round; supersession is.
- **Admit — `corpus/knowledge/instrument-receipts.md` and the round-75 QUALITY criterion**, as
  drafted: both carry a located quote or a committed receipt, neither makes a live-property
  claim, and the criterion's able-to-fail command is the C1 base control the scribe re-ran
  (exit 1).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| A registry row landed with stale draft prose and a gate label the row itself contradicts — the label and the count in the row were written before the instrument existed and were never re-derived from it | `corpus/lessons/round-74-verifier-spotcheck.md` R1 (the `c74_registry_gap.py` row promises "five frozen fixtures" against an eight-fixture counter) and R2 (`c69_tmp_honour.py` registered `gate (live …)` while its own Self-test cell records "no self-test mode"); live cells at `SKILL.md:1426` and `SKILL.md:1432`; a second copy of the same stale count sits in the counter's own docstring, `.ufo/waves/round-74/c74_registry_gap.py:25` ("the five contract fixtures f1-f5") against `f1`–`f8` in the same file | none at freeze — the round-70 "table row" rule was inherited without a predicate over the row's own text, and the round-74 wave had no counter that read a row's Kind against the instrument it names. Captured this round by contract §C1 E1 (gate without a self-test) and E3 (enumerated fixture ids vs observed total), and by the round-75 QUALITY criterion's "executable as written" row | `.ufo/waves/round-75/c75_row_truth.py`: base `mismatches=2 classes=E1 E3` exit 1 (re-run by the scribe, identical line), cheap-content control `mismatches=2 met=false` exit 1 (`controls/ctl-cheapcontent.txt`, cited not re-run), deletion control `append_only=false` exit 1 (`controls/ctl-deletion.txt`). The counter cannot be satisfied by added rows — only by correcting the effective claim |

No further mistake sweep is claimed at this draft: the wave's attack seats (reviewer ×2, critic,
mutation-tester) record their findings in their own seats, and this table is the round's single
class the counters capture.

## Sources

- **S443 — in-toto Attestation Framework, Statement v1**
  (`https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md`): opened
  2026-11-03, HTTP 200, 2,492 bytes, sha256 `cbe684a1…a455ebea`; located quote 6 words at line 37
  (raw substring), plus the digest-matching sentence at lines 54-55 (blockquote markers removed
  before collapsing). C2's receipt shape rests on the `subject`-digest requirement. Row status:
  **pending** in `corpus/SOURCES.md` at draft time (contract §Frontier: enters only after the L1's
  in-round re-open).
- C1 rests on lane instruments and committed receipts, not on a web source: the predicate is
  contract §C1, the counter `c75_row_truth.py`, and the three controls under
  `.ufo/waves/round-75/controls/`.

## Routed

- **R1 — the stale count has a second home.** `.ufo/waves/round-74/c74_registry_gap.py:25` still
  says "the five contract fixtures f1-f5" while the file defines `f1`–`f8`. The round-75
  superseding row corrects the SKILL cell, not the docstring. Fix: an appended docstring
  correction (or a one-line erratum under the round-74 section) naming this line; do not edit the
  file in place. Flip: a future `--selftest` that defines exactly five fixtures would make the
  sentence true again — not planned.
- **R2 — C2's tool and receipt are absent at draft time.** `scripts/instrument_receipts.py` and
  `corpus/knowledge/instrument-receipts.json` do not exist at `c9c5e484` or at lane HEAD; the
  knowledge entry states the frozen §C2 predicate and must be re-read against the landed tool
  before commit — in particular the `selftest_mode` derivation (static registration vs executed
  mode) and the population cross-check against the C1 counter.
- **R3 — `selftest_mode` is static.** The flag records that the blob registers the argument, not
  that the mode does anything. Named as a limit in the knowledge entry; a future counter could
  bind a non-empty tally, but that is not C2's predicate and must not be folded into it silently.
- **R4 — S443 is pending.** Until the L1's row lands, the knowledge entry cannot be cited as a
  sourced claim; if the re-open fails, the entry must be re-titled as a lane-internal note and the
  QUALITY criterion's grounding unaffected (it cites the closure, not S443).
- **R5 — the criterion's able-to-fail is a counter path.** If `c75_row_truth.py` is later
  superseded, the QUALITY row's able-to-fail command must be re-pointed by a superseding
  criterion row, not edited.
- **R6 — quote form, reconciled.** `w1/ScoutSources.md` §1.2 reports the located quote as the
  6-word sentence at line 37 (raw substring) and records that the 22-word context sentence across
  lines 36-37 is not a raw substring and not a naive whitespace collapse. This draft uses the
  scout's form; a later citation that widens the quote to lines 36-37 must say it was
  marker-stripped first, or it is unverifiable by a raw search. The source seat also records two
  adjacent round-74 documentation defects (`round-74.md:49` says `237-239` for a quote that ends
  on 238; a 21-word label on a 20-word source sentence) — routed to the next scribe pass, not
  this round's claims.
````

---

## Findings for the L1

1. **The C1 base control reproduces** from the lane at `c9c5e484` (my run, exit 1,
   `mismatches=2 classes=E1 E3 append_only=true met=false`; both finding lines identical to the
   receipt, whose output line abbreviates the revision). The counter is able to fail on the
   do-nothing base, which is the claim the `## Mistakes` fix column needs.
2. **The round-74 stale prose has a second copy in the counter's docstring**
   (`c74_registry_gap.py:25` at `c9c5e484`): "five contract fixtures f1-f5" vs `f1`–`f8` and
   `selftest 8/8`. Routed as R1; it is evidence for the class, not a new claim.
3. **`c69_tmp_honour.py --selftest` fails as the row says** — `unrecognized arguments:
   --selftest`, exit 2. The Kind label is contradicted by the instrument and by the row's own
   Self-test cell; the demotion is the honest fix and E1 will read green only after it lands.
4. **S443 verifies byte-for-byte** (2,492 B, sha256 `cbe684a1…a455ebea`) against the contract's
   disclosure; the row is nevertheless **absent** from `corpus/SOURCES.md`, so the knowledge
   block is drafted `pending` per this seat's instruction. The source seat's report (published
   after this draft's first pass) agrees on size and digest and fixes the located quote at
   **line 37, 6 words, raw substring**; this draft was reconciled to that form.

## Limits of this report

- The after-state numbers for C1 and C2 are not observed here; the lesson carries explicit
  `<after-state …>` slots rather than a guess. C2's tool does not exist yet, so nothing about its
  behaviour is claimed.
- The cheap-content and deletion controls are cited from their committed receipts; I re-ran only
  the base control, the `c74` selftest, and the `c69` flag probe.
- `w1/ScoutSources.md` published after this draft's first pass (HTTP 200, 2,492 B, same sha256,
  quote at line 37, 6 words); the draft was reconciled to it. No reconciliation is outstanding on
  the source bytes; the two adjacent round-74 documentation defects the scout reports are routed
  (R6) and not fixed here.
- No production file was created, edited, staged or committed; no git/jj mutation was run
  anywhere. Scratch receipts: `.ufo/waves/round-75/w1/ScribeKnowledge/base-c1-rerun.txt` and
  `.ufo/waves/round-75/w1/ScribeKnowledge/c74-selftest.txt`. The scratch tree
  `/fast/scratch/hyaku/kake-r75/ScribeKnowledge/` was removed after those copies were written.
