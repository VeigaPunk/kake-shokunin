# ScribeEntry — round 95, wave 1 (kake / hyaku run 15, attempt 1)

Seat: ScribeEntry (scribe, leaf member — no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Round base
`fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; instruments commit
`43cdd9fc899a2613d8ba7b55edf820825e57b4d1`; freeze commit
`8f638b591e739e1863f5fa22334d5e15178189ed`. Lane HEAD moved during this seat's
work (see §2).

VERDICT: DRAFTS 3 quotes-verified=21/21

## 1. Behaviour — what this seat produced

Three prose drafts, delivered as flat files in this seat's wave directory
`.ufo/waves/round-95/w1/ScribeEntry/`:

| Draft | File | What it is |
|---|---|---|
| Knowledge entry | `entry.md` | `corpus/knowledge/conditional-list-membership.md` — the provenance trio plus contract v2 clauses C1–C5 |
| QUALITY criteria | `quality-criteria.md` | three `## Round 95 — …` sections for `corpus/QUALITY.md` |
| Lesson skeleton | `lesson-skeleton.md` | `corpus/lessons/round-95.md` — header, `## Gate` with DRAFT candidate lines, `## Mistakes` with the two seeded rows |

Supporting receipts, same directory: `verify-quotes.py` +
`quotes-verified.txt`, `battery_coverage.py` + `battery_coverage.out`,
`branch_mutation.py` + `branch_mutation.out`, `entry_probe.py` +
`entry_probe.out`, `head-c1-landed-tip.txt` + `head-c1-landed-tip.json`.

Every check named below was run; the command and its observed rc are given
inline. Nothing in the lane tree was edited by this seat.

### 1a. Quote verification — 21/21 byte-exact

Command: `python3 -B verify-quotes.py` → **rc 0**, `violations 0`
(`quotes-verified.txt`).

Each of the entry's 21 quoted fragments is checked with `grep -F -c` (fixed
string, no regex, no whitespace normalisation) against the raw bytes of a
retained body:

| Body | Path | sha256 | bytes |
|---|---|---|---|
| RFC 9110 | `.ufo/waves/round-94/w1/ScoutRFC/rfc9110.txt` | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 502 941 |
| RFC 8259 | `.ufo/waves/round-90/L1/src/rfc8259.txt` | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` | 28 360 |

Every fragment returned `grep_rc=0` with a count ≥ 1, and every fragment was
also confirmed present in the draft itself (`in_draft=True`). The 21 fragments
cover: the empty-element rule and MUST-accept sentence (RFC 9110 §5.6.1.2,
lines 1695–1702, 6 fragments), the `#element` production and the OWS
production (§5.6.1.2 line 1702, §5.6.3 line 1774, 2 fragments), `etagc` and
its comment plus the `obs-text` definition (§8.8.3 lines 3587–3588, §5.5 line
1589, 3 fragments), the GET/HEAD 304-vs-412 clause (§13.1.2 lines 5928–5932,
5 fragments), the If-Modified-Since ignore rule (§13.1.3 lines 5963–5966,
4 fragments), and the JSON duplicate-names sentence (RFC 8259 §4 line 322,
1 fragment).

I verified the **landed** entry independently of my draft: the same 21 quoted
lines in `corpus/knowledge/conditional-list-membership.md` at HEAD read
`byte-exact verified: 21 ; violations 0`.

### 1b. Clause coverage in the entry

The entry covers all five contract-v2 clauses from
`.ufo/waves/round-95/c2-contract-v2.md`: C1 (empty-element list syntax and the
recipient MUST-accept rule), C2 (obs-text inside an opaque-tag), C3
(`"role": null` = origin), C4 (duplicate object keys refused), C5 (the
GET/HEAD method-filter edges: If-None-Match under OPTIONS → 412 on a match;
If-Modified-Since under OPTIONS → ignored).

**C3 and C4 are labelled as lane conventions, not RFC requirements**, with the
reason shown: RFC 8259 §4 says only that object names SHOULD be unique, so
refusing a duplicate-key document is local receipt-integrity policy. The
entry states this in its own words rather than implying RFC force.

Body length: 262 prose words excluding the quoted RFC fragments and the code
blocks (485 words counting them; 589 for the whole file including the
frontmatter).

## 2. What changed in the lane while this seat worked — a finding for the L1

The L1 integrated the round's corpus work **during this seat's work**, at
commit `9cf924700308995354d85c165acbba9930d02981` ("round-95: land C1 repairs
(15 SKILL rows + 5 registry rows), E3 entry corrections, conditional_eval
contract v2, knowledge entry, S479, QUALITY criteria, round-95 lesson"),
committed 2026-11-05 13:54:46 -0300. This seat's drafts were written at
13:48–14:07.

Consequences, all measured:

- `corpus/knowledge/conditional-list-membership.md` **landed** and is now
  byte-identical to this seat's `entry.md` (the only difference was that the
  landed `source:` line names `S479`, not `S479-pending`, because the S479 row
  landed in the same commit). The landed entry's 21 quotes were re-verified
  byte-exact (21/21).
- `corpus/QUALITY.md` landed **two** `## Round 95` sections, not three:
  `## Round 95 — instrument-population criteria` (bullets R95-A, R95-B, R95-C —
  the three rules this seat was asked to draft, condensed into one section) and
  `## Round 95 — held-out divergence beside the frozen met line` (R95-D). This
  seat's three-section form is therefore **redundant** with what landed; §4
  records what this seat adds beyond it.
- `corpus/lessons/round-95.md` landed with four Mistakes rows (amendment-A
  governance, the entry-identity pin design, the inherited R94-8 pointer, and a
  seat-spec defect) — **not** the two rows this seat was asked to seed. My
  seeded row 2 (the R94-8 `base_rev` pointer) is present in substance as the
  landed row 3; my seeded row 1 (E5 accepting trees) is **not** in the landed
  lesson.

**Ordering constraint the L1 satisfied, and one to keep.** The frozen C1
counter audits every `## ` section of `corpus/QUALITY.md` whose heading
matches `Round[- ]\d+` and whose body contains the string `criteri`, and
requires each such section to cite a `corpus/lessons/…` path that is a
**non-empty blob at the measured revision**. The landed criteria sections cite
`corpus/lessons/round-95.md`, which landed in the same commit, so the
constraint holds. The landed file reads `criteria=40` at HEAD against the base
pin of 39.

A related observation the L1 may want: the landed section
`## Round 95 — held-out divergence beside the frozen met line` does **not**
contain the string `criteri` within its first 400 characters, so the counter
does not treat it as a criteria section — it is counted neither in the
`criteria=40` total nor in the E2 lesson-citation audit. It cites
`corpus/lessons/round-95.md` all the same, so nothing is currently unbacked;
the observation is that a Round-95 section can sit in the file without being
audited by the frozen rule.

Command: `python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision HEAD --work <scratch>`
→ **rc 1**, line 1:
`C1v95 revision=9cf924700308995354d85c165acbba9930d02981 counter=8fd27d62… lessons=90 entries=83 rows=260 criteria=40 mismatches=0 E1=0 E2=0 E3=0 E4=0 E5=0 pins=identity battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 self_pin=ok met=false`
(`head-c1-landed-tip.txt`, `head-c1-landed-tip.json`).

Note the two numbers that matter for the closure, both consistent with the
landed lesson's own rows 1 and 2: `mismatches=0` (the three E3 entry repairs
landed) but `pins=identity` with three `entry-content:` identity findings
(`corpus/knowledge/crawl-budget-consequences.md`,
`corpus/knowledge/crux-keyless-check.md`,
`corpus/knowledge/kimi-subpath-audit.md`), so `met=false`. The landed lesson
records the same identity-pin defect in its row 2.

**Instrument digests verified before any attack** (command
`sha256sum .ufo/waves/round-95/c95_selfassess.py .ufo/waves/round-95/c95_conditional.py`,
rc 0):

| File | Observed sha256 | Pinned in `controls/instrument-sha256.txt` | Match |
|---|---|---|---|
| `c95_selfassess.py` | `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` | same | yes |
| `c95_conditional.py` | `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` | same | yes |

No mismatch. Nothing under `controls/` or `frozen/` was touched; no instrument
was patched.

## 3. The finding this seat adds — the round-95 battery's shape coverage gap

The QUALITY criterion this seat was asked to draft (a) is *"a counter's `met`
conjunct battery must cover every rule class the counter enforces"*. Measuring
it against the frozen round-95 counter produced a **proved gap**, which is
not recorded anywhere in the landed corpus (grep for the branch strings over
`corpus/lessons/round-95.md` and `corpus/QUALITY.md`: no hits).

**Method (two scripts, both exit 0, both read-only against the lane).**

1. `battery_coverage.py` enumerates the **23 distinct finding shapes** the
   frozen `audit()` can emit (from the `mismatches.append({...})` call sites)
   and maps the counter's **19 defect routes** onto them using the counter's
   own matching rule (`fragment in detail`). **7 of the 23 shapes have no route
   that expects them**: E1 `vacuous Gate: no reject decision line (route R01)`,
   E2 `section … names no corpus/lessons/ file`, E2 `section … cites missing
   <lesson>`, E3 `missing source:`, E3 `missing verified-at:`, E3
   `missing recheck:`, E3 `vacuous source: no row id, URL or path locator`.
   The script then builds a scratch fixture for each uncovered branch and shows
   the frozen `audit()` really emits it — all 7 are reachable.

2. `branch_mutation.py` **proves** the gap rather than enumerating it. It
   applies one surgical mutation per uncovered branch to a scratch copy of the
   frozen counter — placed in a lane-shaped side tree so that
   `predecessor_clean()` resolves the round-94 predecessor exactly as in the
   lane, making every battery field comparable — then runs the mutated
   counter's own `battery()`. Result for **all seven** mutations: the mutated
   counter's battery reads
   `battery=20/20 admit=5/5 shadow_absent=1 predecessor_admits=10/19`
   — byte-for-byte the pristine verdict — **while the mutated branch stops
   firing**. A regression in any of those seven branches is therefore invisible
   to the battery the `met` conjunct counts.

**What this is and is not.** At the *class* level the criterion as landed is
satisfied: E1, E2, E3, E4 and E5 each have at least one route, and the base
control reads `battery=20/20`. So the landed R95-A wording is true as written,
and this finding **refines** it to shape level rather than contradicting it.
The same defect, one granularity down, is the round-94 mistake 10 / R94-7
class that the round set out to close.

This is **distinct** from MutC1's survivor M03/M03b (E1-vocabulary,
`.ufo/waves/round-95/w1/MutC1.md` lines 89, 109–119): M03 mutates the `admit`
half of the disjunction and is invisible to battery *and* base run because
every fixture satisfies both alternatives at once. My mutations remove a whole
branch instead, and each still leaves the battery at 20/20. Same family,
different mechanism; the two findings compose.

**Routing.** The successor C1 counter must assert a **named finding per
emitted shape**, not a route count: one route per shape the audit can emit,
each expecting that shape's own detail string, so a branch that stops firing
drops the battery count. This is the round-96 routing input for the
already-landed R95-A criterion, and it is drafted as row 5 of
`lesson-skeleton.md` and as the able-to-fail witness in
`quality-criteria.md`.

## 4. Scope of this seat's drafts against what landed

| Drafted by this seat | Landed state at HEAD | Residual value of this seat's draft |
|---|---|---|
| `entry.md` (knowledge entry) | **landed**, byte-identical | none for the entry itself; this seat's independent re-verification of the landed 21 quotes (21/21) and the E3 ordering constraint are the contribution |
| `quality-criteria.md` (3 criteria) | landed as R95-A/R95-B/R95-C bullets inside one `## Round 95 — instrument-population criteria` section, plus R95-D in a second section | the **shape-level** battery-coverage proof (§3) — the landed R95-A is class-level and its witness cites the round-94 counter's 4/12 coverage, not the round-95 counter's own 7 uncovered shapes |
| `lesson-skeleton.md` (lesson) | landed with 4 rows, not this seat's 2 | seeded row 2 is present in substance as the landed row 3; **seeded row 1 (E5 accepting trees) is absent from the landed lesson**, and **row 5 (the proved shape-coverage gap) is new** |

Measured with the frozen counter's own `audit()` (`entry_probe.py`, exit 0):

- The entry's `source:` line names **S479**, a row that did not exist at the
  round base. Audit with the real lane `corpus/SOURCES.md` (S479 absent):
  **E3 finding `unresolved row id S479`**. Audit with the S479 row inserted
  (the scout's drafted row text): **E3 findings 0**. The landed state has the
  row, so this is clean at HEAD — but it is a hard ordering constraint: the
  entry and the S479 row must land in the same commit or the entry raises an
  E3 finding and the C1 repair route becomes unreachable.
- The three drafted QUALITY sections each cite `corpus/lessons/round-95.md`.
  Audit **without** that file: **3 × E2 `cites missing corpus/lessons/round-95.md`**.
  Audit **with** it: **E2 findings 0**. Same ordering constraint, now
  satisfied by the landed commit.
- The drafted lesson skeleton audited on its own: **E1 findings 0, all
  findings 0**. The E1 rule that applies to lessons of round ≥ 95 (an `## Gate`
  section carrying both admit and reject decision vocabulary) is satisfied by
  the skeleton — the `DRAFT` Gate lines carry an explicit reject candidate
  (`amendment A … rejected`).

## 5. Touched surfaces

- **Written** (this seat's wave directory only, all flat):
  `.ufo/waves/round-95/w1/ScribeEntry/{entry.md, quality-criteria.md,
  lesson-skeleton.md, verify-quotes.py, quotes-verified.txt,
  battery_coverage.py, battery_coverage.out, branch_mutation.py,
  branch_mutation.out, entry_probe.py, entry_probe.out,
  head-c1-landed-tip.txt, head-c1-landed-tip.json}` and this report at
  `.ufo/waves/round-95/w1/ScribeEntry.md`.
- **Read only**: the lane tree, the two counters, `controls/`, `frozen/`,
  `corpus/`, `SCORECARD.md`, `SKILL.md` lines 181–240, and the sibling seats'
  wave files.
- **Not touched**: `corpus/knowledge/`, `corpus/QUALITY.md`,
  `corpus/lessons/`, `corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md`,
  `scripts/`, `.ufo/state`, `MANIFEST.json`, every other seat's directory, the
  fleet repo. No mutating git or jj command was run anywhere; the only git
  commands used were read-only (`show`, `ls-tree`, `cat-file`, `rev-parse`,
  `log`, `status`, `diff`, `grep`). Fixture repos were built by the counter's
  own `make_repo` inside scratch.

## 6. Findings

1. **The round-95 C1 counter's `met` battery counts routes, not finding
   shapes.** 7 of the 23 shapes its audit can emit have no route; all 7 are
   reachable; and a mutation that removes any of them leaves the battery
   reading `battery=20/20 admit=5/5 shadow_absent=1 predecessor_admits=10/19`,
   identical to the pristine counter. Proved, not inferred (§3). Not recorded
   in the landed corpus. Route to round 96: assert a named finding per emitted
   shape.
2. **The landed `## Round 95 — held-out divergence beside the frozen met line`
   QUALITY section is not audited by the frozen E2 rule**, because the frozen
   criteria detector requires the string `criteri` within the first 400
   characters of the section. It cites `corpus/lessons/round-95.md` all the
   same, so nothing is unbacked today; the observation is that a Round-95
   section can sit in the file outside the counter's audit.
3. **An ordering constraint now satisfied, worth keeping.** The knowledge
   entry names S479 and the QUALITY sections cite
   `corpus/lessons/round-95.md`; both were landed in the same commit as their
   dependencies, so E2 and E3 are clean at HEAD. If either is landed alone,
   the C1 counter raises an E2/E3 finding and the declared repair route
   becomes unreachable.
4. **The lane HEAD moved under this seat** (freeze `8f638b59` → ruling
   `4f443b3f` → landing `9cf92470`), with an `Amendment A` section still
   present in `.ufo/waves/round-95/freeze.md` at HEAD (lines 144–172) that
   names the *withdrawn* digests `04be4a7d…` / `9eff04c5…`. The authoritative
   digests are the ones in `controls/instrument-sha256.txt` at HEAD, which this
   seat verified to match the on-disk counters. A reader who hashes the values
   named in that freeze section will compute a mismatch against the restored
   bytes.
5. **This seat's seeded mistake row 1 (E5 accepting trees) is absent from the
   landed lesson.** The condition is still live at the round base
   (`controls/base-c1.txt` reads `E5=15`, every finding `names a tree, not a
   blob`), and the repair route (naming a concrete committed non-empty blob for
   each of the 13 directory rows) is R94-5, still open.

## 7. Out of scope for this seat

No instrument, control, frozen file, registry row, `SKILL.md` row, lesson
decision or QUALITY verdict is mine to make. This seat drafted prose and
measured; it did not admit anything, did not score either claim, and did not
patch a counter. The E1/E2/E3/E4/E5 findings above are measurements of the
frozen instruments, not proposals to change them.

## 8. Tooling

No tool was installed, upgraded or uninstalled by this seat; no pacman
invocation was made (pacman is paused host-wide). The seat used only the
preinstalled `python3` (Python 3.14.8, `python3 -B`), `git` (read-only) and
POSIX utilities. The counter's own selftest needs no extra dependency.

## 9. Scratch

Scratch root `/fast/scratch/hyaku/kake-r95/ScribeEntry/` was created and
**removed** before this report was written; every receipt it held was copied
into `.ufo/waves/round-95/w1/ScribeEntry/` first (`quotes-verified.txt`,
`battery_coverage.out`, `branch_mutation.out`, `entry_probe.out`,
`head-c1-landed-tip.txt`, `head-c1-landed-tip.json`).

## 10. Artifact index

| Path (relative to LANE) | What it is |
|---|---|
| `.ufo/waves/round-95/w1/ScribeEntry/entry.md` | knowledge-entry draft (now byte-identical to the landed entry) |
| `.ufo/waves/round-95/w1/ScribeEntry/quality-criteria.md` | three QUALITY.md criteria drafts + the E2 ordering constraint |
| `.ufo/waves/round-95/w1/ScribeEntry/lesson-skeleton.md` | lesson skeleton (2 seeded rows + the proved shape-coverage row 5) |
| `.ufo/waves/round-95/w1/ScribeEntry/verify-quotes.py` | 21-fragment `grep -F` byte-exactness verifier |
| `.ufo/waves/round-95/w1/ScribeEntry/quotes-verified.txt` | its output (`violations 0`) |
| `.ufo/waves/round-95/w1/ScribeEntry/battery_coverage.py` | 23-shapes vs 19-routes coverage enumeration + reachability |
| `.ufo/waves/round-95/w1/ScribeEntry/battery_coverage.out` | its output |
| `.ufo/waves/round-95/w1/ScribeEntry/branch_mutation.py` | the per-branch mutation proof |
| `.ufo/waves/round-95/w1/ScribeEntry/branch_mutation.out` | its output (7/7 proven gaps) |
| `.ufo/waves/round-95/w1/ScribeEntry/entry_probe.py` | E2/E3 ordering probe over the frozen `audit()` |
| `.ufo/waves/round-95/w1/ScribeEntry/entry_probe.out` | its output |
| `.ufo/waves/round-95/w1/ScribeEntry/head-c1-landed-tip.txt` | frozen counter run at HEAD (rc 1, `met=false`) |
| `.ufo/waves/round-95/w1/ScribeEntry/head-c1-landed-tip.json` | its JSON detail line |

VERDICT: DRAFTS 3 quotes-verified=21/21
