# ConnectorOverlap — sibling + corpus overlap, and the §10 assimilation input

Seat `ConnectorOverlap`, lane `kake`, round 75, attempt 1, wave `w1`. Read-only: no lane file was
written, no sibling lane was written, no git/jj mutation was made anywhere.

Measured at lane base `c9c5e484c533aa65f4374b841a3edcf572ed19a9` (working tree, which for every
path cited below equals the base — the four knowledge entries and `SKILL.md` rows read here are
untouched by the round). Scratch tree `/fast/scratch/hyaku/kake-r75/ConnectorOverlap/` was created
per the seat rule and removed before yield; it held nothing (every scan was a read of committed or
working-tree bytes), so there is no receipt to copy in.

Commands used, all read-only, exit 0 unless stated:

```
find . -maxdepth 6 -type f \( -iname '*attest*' -o -iname '*provenance*' -o -iname '*receipt*' \
  -o -iname '*supply*chain*' -o -iname '*sigstore*' \) | grep -v '^./kake-shokunin'
grep -rIl -E 'in-toto|sigstore|SLSA|attestation statement|provenance predicate' .
grep -rIl --include='*.py' --include='*.mjs' -E 'git cat-file|rev-parse.*:.*path|committed blob' */scripts */tools
grep -rIn -E 'instrument[- ]receipt|selftest_mode' <7 candidate lanes>
grep -n -E '^\| *S(371|401|407|412|319) ' corpus/SOURCES.md      # 0 hits, all five
ls .ufo/waves/ | grep -E '^round-1[456]$'                      # 0 hits
ls .ufo/waves/corpus-expansion-1/audit-wave.py                  # No such file (exit 2)
```

---

## 1. Sibling lanes — who already owns a digest-bound receipt / attestation / provenance instrument

Twenty sibling checkouts under `/home/vgpnk/Projects/shokunin/`, kake excluded. The filename sweep
and the `in-toto|sigstore|SLSA` grep were run over the whole trees; the `.ufo/waves/**/sandboxes/`
and `node_modules` hits (kagi round 27/28) are wave sandboxes and vendored `@sigstore/*` packages,
not lane instruments, and are excluded from the verdicts below. Verdicts are on landed artefacts:
a knowledge entry in `corpus/knowledge/` cited by that lane's `SKILL.md`, or a `scripts/`/`tools/`
file with a registry row.

| # | Lane | File:line | What it actually binds | Verdict vs kake C2 |
|---|---|---|---|---|
| 1 | **tabi** | `scripts/check-measurement-binding.mjs:2-6`; selftest `scripts/selftest-measurement-binding.mjs:1-6`; rows `SKILL.md:1840`, `:1939` | "Binds each counted claim to the identity of what measured it: the counter script bytes (**sha256 blob digest**), the revision the count was measured at, and the declared counted inputs" — driven by a per-claim manifest (`corpus/evidence/round-16/measurement-binding.json`), `--at` = lane tip by default, self-test 76 cases / 13 reasons | **Closest match to the C2 primitive.** Adjacent, not duplicate: tabi's population is caller-named manifests (one claim at a time), C2's is a **registry-derived inventory** cross-checked by two independent derivations, and C2 binds a fourth fact tabi has no field for — `selftest_mode`. |
| 2 | **chousa** | `tools/digest-in-tree.py:3-6`; row `SKILL.md:163`; `tools/receipt-pin.py`, row `SKILL.md:159`; entries `corpus/knowledge/receipt-digest-provenance-r67.md:1`, `receipt-binding-r38.md:1`, `receipt-identity-r65.md:1`, `receipt-expectation-digests-r40.md:1` | "every sha256 a receipt pins must re-derive from bytes committed in the repository" — extracts 64-hex pins from a receipt and checks each against **blob membership** at a revision (`--all-objects` for the object DB); `receipt-pin.py` binds receipt *headers* to a revision | **Adjacent — the sibling whose wording C2 could accidentally restate.** Distinction C2 must draw: chousa asks "is this digest *somewhere* in the tree" (membership); C2 asks "is *this path's* committed blob this digest, this length, and does it register `--selftest`" (identity + shape). chousa's own docstring already disclaims execution authenticity and entailment. |
| 3 | **tameshi** | `corpus/knowledge/receipt-revision-binding.md:1,5,17,21`; gate `tools/receipt-revision-gate.py` (selftest 19/19, `:2`); rows `SKILL.md:47`, `:1547` | "A receipt is evidence only for the content it was measured against": every certified receipt carries `rev=<sha>` / `"rev": "<sha>"` in its own bytes; exit 3 with `RECEIPT_REV_CONTENT_DRIFT` / `RECEIPT_REV_UNRESOLVABLE` | **Adjacent.** Subject is the *measured tree* at a revision (receipt→revision); C2's subject is the *instrument file's* identity. **But see the source collision below.** |
| 4 | **souji** | `corpus/knowledge/fleet-root-capture-receipt-grammar.md:16-24`; counter `census/round-53/c1-counter.py` | `# TOOL_SHA256=…` "must agree with the sha256 of `tools/souji-fleet-root-census.py`'s bytes at the measured revision" + `CAPTURE_SHA256` + `ENTRIES` recount | **Adjacent.** One instrument, one capture, digest embedded in the run receipt. C2 is the transposed shape: one receipt, sixteen instruments, no run. |
| 5 | **kagi** | `corpus/knowledge/tac-evidence-integrity.md:1` | `tac-check` custody records and `--register` semantics for local evidence | **Distinct.** Custody of secret-adjacent evidence; no digest population, no registry derivation. |
| 6 | **kaidoku** | `.ufo/waves/round-17/tools/receipt-validate.py` (+ `-v2.py`), `.ufo/waves/round-17/w2/receipt-forge.py`, `corpus/knowledge/2026-10-13-r3-jq-provenance.md` | a wave-local receipt validator and a forge control | **Distinct.** Wave artefacts under `.ufo/waves/`, no `scripts/` row, no knowledge entry citing it. |
| 7 | **kotoba** | `corpus/knowledge/corpus-integrity-round11.md:1` | two counting commands that could not count (pattern blindness) | **Distinct.** Counting defect class, no digest binding. |

**No lane names kake's instrument.** `grep -rIn -E 'instrument[- ]receipt|selftest_mode'` over
chousa, tameshi, kaidoku, kagi, kotoba, souji, tabi returns no landed hit — the only `receipt
population` hits are chousa wave drafts about its own receipt set (`.ufo/waves/round-40/w1/
ReviewActivePopulation.md:1`, `CriticC1Control.md:43`). The **registry-derived population** is
unowned ground.

**The source collision, stated plainly.** Kake's planned frontier row S443
(`https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md`, 2,492 B, sha256
`cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`) is **the same document, the same
bytes and the same digest** as tameshi's already-landed S281
(`tameshi-shokunin/corpus/knowledge/receipt-revision-binding.md:1`, fetched 2026-10-28, tag v1.2.0,
byte-identical at `main` the same minute). S443 is new *inside kake's S-space*; it is not new
fleet-wide. Two consequences the scribe should honour:

- Kake may cite S443 for the `subject`/`digest` sentence — that is proper source grounding.
- Kake must **not** present the sentence as newly discovered ground, and the SCORECARD capability
  row (`Instrument receipt binding` → first-working round 75) must be scoped as *kake's first
  registry-bound instrument inventory*, not as a first digest-binding capability in the fleet:
  tabi (:1 above), chousa (:2), souji (:4) and tameshi (:3) each hold a working variant.

**Answer to the seat's question.** Kake's C2 **duplicates no lane's instrument** and is **adjacent
to four**: tabi's measurement-binding gate (the same primitive), chousa's `digest-in-tree` (the
same premise, membership instead of identity), souji's `TOOL_SHA256` (the same fact, embedded in
one run receipt) and tameshi's receipt-revision gate (the same warrant sentence). Its **distinct
ground** is exactly one thing: *the registry's own instrument set is an inventory that must be
complete and self-describing* — population 16 derived twice, `{sha256, bytes, selftest_mode}` per
file, `met = (bound == population)`. Kake owning "publisher/instrument evidence" and not
"supply-chain provenance" is correct and no lane contests it: no lane owns supply-chain provenance
at all, and tameshi quotes the in-toto sentence without claiming that province.

---

## 2. Corpus overlap inside kake — what `corpus/knowledge/instrument-receipts.md` may not restate

`corpus/knowledge/instrument-receipts.md` and `corpus/knowledge/instrument-receipts.json` do not
exist at base (`grep -n 'instrument_receipts\|instrument-receipts' SKILL.md SCORECARD.md
corpus/QUALITY.md` → 0 hits). The four held entries, with the claim each already owns:

| Held entry | Binding subject | Digest? | Re-derived by | Population | Already-held claim the new entry must **not** restate |
|---|---|---|---|---|---|
| `corpus/knowledge/receipt-integrity.md:58` (+ README:60) | receipt → the run that wrote it | `counterSha256`, `driverSha256` | re-running the counter under the v2 driver | none (one run) | "a receipt whose `counterSha256` ≠ sha256 of the invoked counter is stale" — **already the entry's counter-binding gate.** Also held: exit gate, `note != "tool absent"`, mtime window, seed. |
| `corpus/knowledge/sidecar-reobservation.md:15,19,62` | note → the citing **line** | `lineSha256` of the line's current text | `--check` / `--write` with a `history` array; `os.stat` for `present` | 174 entries, one sidecar | "a digest binds the note to the line it annotates", "presence is a three-valued verdict from `os.stat`", "`--check`/`--write` with a history array". **The sidecar answers *does this host still have it*; C2 answers *is this the byte the registry row measured*.** |
| `corpus/knowledge/freshness-sweep.md:1` + `freshness-pins.json:1-7` (schema `kake-freshness-pins-v1`) | counts / floors | **no sha256** | `scripts/freshness-sweep.mjs` | named pins | "pin the baseline in JSON, edited in the same commit as the prose; floors tolerate growth, equalities are drift predicates". |
| `corpus/knowledge/gate-status-ledger.md:1,3,58` | gate → recorded verdict at a revision | **no digest** | the row's documented command + its control receipt | 28 members | "a red row is expected-red only while its receipt chain says so; every re-adjudication needs a dated receipt; `live`/`historical` is a decision, not an accident". C2 supplies the **join key this ledger lacks** (a per-instrument digest), which is additive. |

Three further criteria are already frozen and therefore make C1 an *enforcement* round, not a
knowledge round — worth saying so the lesson does not file new ground:

- `corpus/QUALITY.md:1190` — a stated selftest tally must be the tally the documented command
  prints (C1's **E2/E3**).
- `corpus/QUALITY.md:1386` — "the Kind cell must name all the mechanisms a rerun shows" (C1's
  **E1** substitution margin, and R2's demotion).
- `corpus/QUALITY.md:797` — every lane tool with an exit contract has a registry row (the
  population's existence rule).

**Verdict.** Of C2's four per-entry facts — `path`, `sha256`, `bytes`, `selftest_mode` — the first
two are already held three times over in the lane (`receipt-integrity.md:58` for `sha256`,
`sidecar-reobservation.md:15` for a line digest bound by path) and `--check` re-derivation is held
twice (`sidecar`, `freshness-sweep`). The genuinely new content is **`bytes` + `selftest_mode` +
the population**: an instrument's *length* and its *self-test affordance* are bound facts, and the
population is derived from `SKILL.md` by two independent derivations whose agreement is itself part
of the receipt. The entry's title and first paragraph should therefore be about **inventory
completeness and instrument identity**, not about "digest-bound receipts" — under the second name
the entry is a restatement of `receipt-integrity.md` plus chousa's `digest-in-tree`.

**Naming inconsistency, flagged not changed.** The lane's two existing JSON receipt schemas carry
the lane prefix (`kake-freshness-pins-v1` at `freshness-pins.json:2`, `kake-paths-sidecar-v1` per
`sidecar-reobservation.md:11`); contract §C2 freezes `instrument-receipts/v1` without it. The
contract is frozen, so this is an appended-amendment candidate for the L1 at most — not a silent
edit and not something this seat may fix.

---

## 3. Assimilation (§10) — `merge/kake/` decision input

Read only: `/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` (166 lines) and the four
entries under `merge/kake/knowledge/corpus/knowledge/`. Nothing was adopted, nothing was written
into the source repo. Shared blocker for all four: **every locator they cite is unreachable in the
lane.** `ls .ufo/waves/ | grep -E '^round-1[456]$'` → 0 hits, and
`.ufo/waves/corpus-expansion-1/audit-wave.py` → "No such file" (exit 2). The ids they claim
(S371, S401, S407, S412, and the S319 they name) return **0 hits** in `corpus/SOURCES.md`, whose tip
is **S442** — so adopting any of them as written would insert ids below the tip and, for the S319
sentence, cite a row that does not exist.

| # | Target path | Sources cited (ids + URLs) | Collision | Province | Recommendation |
|---|---|---|---|---|---|
| 1 | `corpus/knowledge/receipt-integrity-after-prune.md` | **S401** = own measurement `lanes/kake/round14/.evidence/receipt_integrity_r14.txt` (own-work; **no URL**); recheck `bash lanes/kake/round14/.evidence/receipt_integrity_r14.sh` | id S401 not held; path not held; **subject adjacently held** by `corpus/knowledge/receipt-integrity.md` (that entry binds receipt→run; this one claims receipt→artifact existence + quote match — a different, narrower claim) | In — own evidence layer is Core (`PROVINCE.md:17`, "the lane's own gates") | **Refuse.** Flip: re-point the locators at surviving bytes under `.ufo/waves/` and assign an id above S442; then it is an append to `receipt-integrity.md`, not a new file. |
| 2 | `corpus/knowledge/receipt-integrity-round15.md` | **S407** = `lanes/kake/round15/.evidence/receipt_integrity_r15.txt` (own-work; no URL); recheck `bash lanes/kake/round15/.evidence/…` | as #1; and it is a **superseded restatement** of #1 (28 own-work rows, 26 in #1) | In | **Refuse.** Flip: only if the lane wants the one-digit S206 misquote as *history* — and then it belongs in `corpus/lessons/`, not `corpus/knowledge/`. |
| 3 | `corpus/knowledge/receipt-integrity-round16.md` | **S412** = `lanes/kake/round16/.evidence/receipt_integrity_r16.txt` (own-work; no URL); recheck `bash lanes/kake/round16/.evidence/…` | as #1–#2, **plus a hard collision**: it asserts "the row now numbered **S319** quotes its appendix as …" — kake holds no S319 (`grep -n -E '^\\| *S319 ' corpus/SOURCES.md` → 0 hits) | In by topic, **out by referent** (the cited row does not exist in this lane) | **Refuse.** Flip: the S319 referent is resolved in this lane's id space and the locator re-pointed; otherwise the entry lands a claim about a row the reader cannot open. |
| 4 | `corpus/knowledge/staged-evidence-gap-locator-kinds.md` | **S371** = `lanes/kake/round10/.evidence/repair_locator_kinds_r10.txt` (own-work; no URL); recheck `python3 .ufo/waves/corpus-expansion-1/audit-wave.py` (path absent) | id S371 not held; **ground is the staged package's 24 rows**, which the lane has not adopted as a set (registry tip S442; the merge report's near-duplicate table alone already lists 10 of its rows against held ones) | Marginal — corpus hygiene **about a package**, not about the lane's own corpus | **Refuse.** Flip: only after the merge's staged rows are adopted, at which point the 24-row locator list must be **regenerated** against the adopted set, never copied. |

`Assimilation: none` is therefore the evidence-backed outcome for this round, on a mechanical
ground (four unreachable locator sets and five ids below the registry tip) rather than a taste
judgement. MERGE-REPORT.md itself says "**Nothing was written into the lane repo**" and its adopt
checklist step 5 requires appending, not replacing — neither is satisfiable while the locators are
dead.

---

## 4. `considerthese/2026-10-26.md` Part 2 — what the lane actually holds

| # | Proposal | Status at base `c9c5e484` | Evidence |
|---|---|---|---|
| 1 | Read the lane's own tools instead of duplicating them | **Implemented at instrument level; the daily "report only a change or a red" ritual is not a lane artefact** | `SCORECARD.md:4350` — "Landed-vs-claimed check … (considerthese proposal 1)"; `SCORECARD.md:4379` — `scripts/id_resolver.py` row. No committed receipt records a daily read; that is a reporting practice, so nothing is landable. |
| 2 | Receipt-rewrite watch | **Implemented, round 58 C1** | `.ufo/waves/round-58/c58_receipt_rewrites.py:8-9` (population: every path at any depth under `.ufo/waves/round-<N>/control(s)/`, first-parent line); `corpus/QUALITY.md:1311` — "`considerthese/2026-10-26.md` (2026-10-26) proposal 2, adopted as round-58 C1"; `corpus/lessons/round-58.md:125`. |
| 3 | Operator-decision queue | **Implemented, round 59** | `corpus/lessons/round-59.md:205` — "proposal 3 (operator-decision queue) is implemented here as the lane's routed-item queue"; the fleet `.ufo/l0-questions.md:277` carries the routed items (the three dangling ids S303/S304/S352, `gate-status-ledger.md` r72 note). |
| 4 | Gate-agreement ledger (verifier agree/disagree per round on admits/rejects) | **OPEN — genuinely unimplemented** | `grep -rIn -iE '\bagree' corpus/QUALITY.md corpus/README.md SKILL.md` returns no agree/disagree tally (only `QUALITY.md:657` "revision agreement", `:1044` "agrees with the oracle", `SKILL.md:168` "live re-reads agree"). `c66_gate_status_hostportable.py`'s `agreement=17` is registry-label-vs-observed, a different quantity. |
| 5 | Historical-gate list | **ALREADY IMPLEMENTED, round 66** — the seat brief's premise is **false** | `corpus/knowledge/gate-status-ledger.md:1` "(adopted r66)", `:3` "`considerthese/2026-10-26.md` proposal 5 (assimilation, adopted r66)", `:7-10` the adoption statement, `:58` "## Older known-historical entries (proposal 5's original list)", plus r72 re-adjudications at `:76-97`. |

**The contradiction, stated and not smoothed.** Contract §Frontier says proposal 5 "is mined **at
most once**". That once was **r66**, four rounds before this round's base. The round-75 plan
(record the live/historical split C1 freezes as a `QUALITY.md` criterion citing that file and date)
would be the **second** mining of the same proposal. It is still admissible — the *artefact* is
different (an admission criterion, not a ledger) — but only if the criterion's grounding names both
`considerthese/2026-10-26.md` (2026-10-26) **and** `corpus/knowledge/gate-status-ledger.md:1-10`
as the prior adoption, and says that the criterion is what makes r66's Kind distinction enforceable
at registry-admission time. Written without that cross-reference, the round files a "new"
proposal-5 adoption the corpus has held since r66 — the same defect class C1 exists to remove (a
claim about state its instrument does not have), landed by the round that removes it.

**Flip condition for the L1.** If the criterion does not cite the r66 adoption: drop the §Frontier
proposal-5 line, and if the round wants a considerthese mining, land **proposal 4** instead — it is
the one genuinely open proposal, and P4's quantity is already measured every round
(`c66_gate_status_hostportable.py` prints `agreement=N`; every `corpus/lessons/round-NN-verifier-
spotcheck.md` carries the per-row agree/disagree cells), so a ledger of it is a bounded scribe
artefact with no new instrument.

---

## 5. One bounded move (Godspeed: evidence → axes → move → risks → verification)

**Axes.** (a) C1 calibration `mismatches 2 → 0`; (b) C2 operability `bound 0 → 16`; (c) corpus /
registry consistency (claims about state the corpus actually holds); (d) receipt-disclosure
integrity (the r58 class: a receipt changed after commit without disclosure).

**Evidence for the defect.** `c58_receipt_rewrites.py:8-9` fixes the disclosure population as
"every path ever committed under `.ufo/waves/round-<N>/control/` or `.ufo/waves/round-<N>/controls/`
(any round, any depth) on the first-parent line of the measured tip". Contract §C2 places its
receipt at **`corpus/knowledge/instrument-receipts.json`** — outside that population. So round 75
would create a receipt that can be relabelled or rewritten after commit with no event, on the very
path that certifies all sixteen instruments. That is the r57 D1 defect (`controls/after-c1-receipt-
pins.txt` committed `pending`, filled in later, report said no receipt was rewritten) reproduced on
a new path, and it is the class proposal 2 was adopted to close.

**Proposed move.** The C2 **after-receipt** — `controls/after-c2-receipts.txt`, a `controls/` file
and therefore already inside the watched population — carries two extra lines derived by one
command from the committed bytes:

```
receipt_path=corpus/knowledge/instrument-receipts.json
receipt_sha256=<sha256sum of that file>   receipt_bytes=<wc -c>
```

No frozen term moves: the C2 stdout line stays exactly
`C2v1 revision=<rev> population=16 bound=B mismatches=M met=<bool>`, the population stays 16, the
predicate stays `(bound == population) and (mismatches == 0)`, and no file is added beyond the
control receipt §C2 Controls already mandates ("Receipts live under `controls/`").

**Affected axes.** C2 unchanged-to-better (one derived line in a receipt it must write anyway);
C1 unchanged (C2's receipt is outside the 16); (c) + (the receipt's own identity becomes a claim
the corpus can re-derive); (d) ++ (the receipt that certifies 16 instruments is itself disclosed).
No axis harmed: the move forbids nothing, adds no population member, and touches no counter.

**Risks.** (i) Ordering: the digest must be taken **after** `--write` and both must land in one
commit, else the recorded digest is stale — and by `c58`'s own rule ("the plain first addition of a
path is not an event") the receipt's first commit is not an event, so the control line must be in
that first commit, not a later one. (ii) The tempting alternative — adding
`corpus/knowledge/**` to `c58_receipt_rewrites.py`'s population — would change a landed counter's
predicate mid-round and open E-class findings across unrelated history; it is out of scope and this
seat does not recommend it. (iii) The control receipt is prose-plus-lines, so a reader must not
mistake the `sha256` line for one of the C1/C2 result lines; the `receipt_` prefix keeps it apart.

**Verification (all runnable at the tip, none needing the move to have been tried first).**

1. `python3 -B scripts/instrument_receipts.py --root . --revision <tip> --check` → the frozen line,
   exit 0.
2. `sha256sum corpus/knowledge/instrument-receipts.json` equals the `receipt_sha256` in
   `controls/after-c2-receipts.txt` (the one-command re-derivation).
3. `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>` → exit 0
   (its five zero-conjuncts), i.e. the new control receipt's first commit introduces no event and
   the receipt path is covered (via the control line) for any later round.

**Not claimed.** This seat verified no counter run, no C1/C2 measurement, and no landed state — the
lane tree is read-only here and the counters belong to the executor seats. The four assimilation
verdicts are locator-level, not content-level: they say the entries cannot be re-derived where they
point, not that their prose is wrong.
