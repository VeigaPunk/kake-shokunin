# Round 45 — receipt-integrity hardening and standing-claim re-verification

## Gate

One row per new registry row, labeled per new row (round-44 closure observation). The S133 admit
grounds the C1 knowledge entry `corpus/knowledge/receipt-integrity.md`; the S134 reject satisfies
the round-44 closure requirement that this round's Gate log at least one screened reject. A third
opened non-primary source was screened and carries no decision (candidate-only row, last table row).

| ID | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S133 | https://docs.python.org/3/library/subprocess.html | accessed 2026-10-24, HTTP 200, 208,624 bytes, sha256 `eceda6f6…e5bdf0dd`, retained at `.ufo/waves/round-45/sources/subprocess.html` | "A negative value -N indicates that the child was terminated by signal N (POSIX only)." (§Popen Objects → `Popen.returncode`, paragraph 3; 15 words; the same entry's paragraph 2 gives the None-while-running half) | admit — grounds the receipt-gate exit-status reading (kind `docs`, tier A, status `mined`, used-by `corpus/knowledge/receipt-integrity.md`); the v1 driver read `p.returncode` and never gated on it (`c44_audit.py:54-61`), and the round-44 review recorded `"exit": -9` rows certifying `ok=true` |
| S134 | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means (read via the Stack Exchange API) | accessed 2026-10-24, API read HTTP 200, 723-byte JSON, sha256 `702954fd…716ffcd1` (a plain HTML GET of the same URL answers HTTP 403) | "A negative return code usually means that the process was terminated by a signal." (accepted answer by `sth`, first paragraph; 14 words) | **reject** — the answer's durable point is already carried by the tier-A primary S133, and its `-11 is SIGSEGV` claim is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and the answer becomes an illustrative example |
| — (candidate only, no id) | https://stackoverflow.com/a/5631819 | accessed 2026-10-24 via the Stack Exchange API (answer id 5631819, score 363, accepted, owner Eli Bendersky; the HTML page answers HTTP 403; retained at `.ufo/waves/round-45/sources/so-a5631819.json`) | "A negative value -N indicates that the child was terminated by signal N (Unix only)." (answer body, first paragraph; 15 words) | candidate only, no decision — a second non-primary source on the same topic, opened while cross-checking S133/S134; it restates the same documentation passage with older wording ("Unix only") and adds no authority beyond S133, so it is not proposed as a Gate decision |

## Mistakes

14. **Class: instrument trusted receipts without binding them to the run — the witness gate
    certified whatever bytes sat at a receipt path, never checking that *this* invocation wrote
    *these* bytes, so "witnessed" was a statement about a directory rather than about a
    measurement.** Evidence: the frozen v1 driver `.ufo/waves/round-44/c44_audit.py` (sha256
    `8ee2c8bf…2d0c75`) records the counter's exit on every row and never reads it
    (`run_counter :54-61` returns `p.returncode`; `score() :157` stores it; `semantic_witness
    :63-66` and `expectation_ok :69-83` never consult `exit`, `note`, mtime or `counterSha256`).
    Three HIGH defects with that one root cause, preserved verbatim at
    `.ufo/waves/round-44/w2/ReviewCounterContract.md` defects **1a** (`:41-55`), **1b** (`:57-71`),
    **1c** (`:73-96`): an exit-2 counter-error receipt with a class divergence witnesses; a
    `note: "tool absent"` receipt witnesses on every class key though nothing ran; a SIGKILL-ing
    counter with pre-planted receipts certifies `ok=true` exit 0 while the summary records
    `"exit": -9` on every row. Re-derived independently on today's bytes by
    `.ufo/waves/round-45/w1/ReviewV1Defects.md` — all six probes fire (A/B/C receipt-layer, D/E
    stale-plant end-to-end, F live backdate). Captured-by: two frozen texts between them should
    have caught it — round-44 kill rule (2) ("Any witness that is a timing-only failure, a
    v4-corpus divergence, or a counter error → not a witness", `SCORECARD.md:3459-3462`) named the
    counter-error class but was never wired to the receipt's `exit` field, and the capability row's
    "per-row receipts re-derive at their recorded seeds" (`SCORECARD.md:218`, echoed in the C1 claim
    text `:3617`) certified *seed*-binding while leaving *run*-binding unchecked — it constrained
    what a receipt may be cited for, not which invocation wrote it. The round-45 C1 kill rule (2)
    ("re-derives from committed bytes at its recorded inputs") repeats the class and needed the
    validity gate to actually close it. Fix: driver v2
    `.ufo/waves/round-45/c45_audit.py` applies one `receipt_validity()` gate (`:68-96`) through
    shared row builders (`build_control_row :107`, `build_build_row :131`): exit ∈ {0,1} else
    `counter_error`; `note != "tool absent"` else `tool_absent`; counter-sha binding, a
    receipt→control toolSha256 binding, seed presence and a run-window mtime check else
    `stale_receipt`; invalid rows earn no witness or not-met
    credit; build count pinned; cohort dir self-created and refused non-empty; run-manifest written
    before any spawn. Able to fail: `python3 -B .ufo/waves/round-45/c45_matrix.py --stage before`
    records `invalid_accepted=3` on the frozen v1 driver and `--stage after` records
    `invalid_accepted=0`, `rejections_named=3` (counter_error, tool_absent, stale_receipt),
    `honest_witnessed=27`, `honest_build_met=3` (`verification/matrix/{before,after}.json`); the
    stale-backdate fixture keeps the counter exit inside {0,1} so the mtime branch — not the exit
    branch — refuses it; the shipped `--selftest` runs the three invalid classes plus an honest
    control through `main()` itself in a temp cohort (`_selftest_cohort :223`).

15. **Class: attribution — a filed count bound to a receipt's numbers but not to the receipt's
    identity (same mistake class as 14, recurring in the freshness claim).** Evidence: the frozen
    C2(c) leg states "the round-44 claim receipt's 27 witnessed controls re-derive as 22 class-only
    + 1 mixed + 4 met" and fixes the MET tuple `after=(4/4, false, 22/1/4)`. The receipt the claim
    names is the final claim receipt `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
    (sha256 `9dead4d7…c076d1`, witnessed 27, `ok=true`), which re-derives as **26 class-only + 1
    mixed + 0 met**. The `22/1/4` tuple re-derives only from the **earlier** 23-witness receipt
    `verification/claim/after-v5.json` (sha256 `2383efae…ce0902`, `ok=false`) — the pre-G6-fix
    cohort whose four casememo rows were still `met`. Found independently by four wave-1 seats:
    `w1/ExecWitnessSplit.md`, `w1/ScoutRoutedLedger.md`, `w1/CriticC2Scope.md`,
    `w1/ScribeLessonMistakes.md`; the C2(c) leg is reported falsified-as-declared in SCORECARD.md
    (round 45 measurement append), not amended. Captured-by: the same kill-rule-(2) gap as entry
    14 — a leg that says "the claim receipt" must bind its tuple to that receipt's identity (path +
    sha256), not to values some same-named receipt happens to carry. Fix:
    `c45_freshness.py` re-derives the split from the named receipt's committed bytes and prints the
    measured truth (`witness_split class_only=26 mixed=1 met=0`); the SCORECARD correction names
    both receipts with sha256s; any future filed count against a receipt must cite path + digest.
    Able to fail: the two committed receipts are the red state — the jq command is green on the
    receipt the claim does not name and red on the one it names.

**Correction (appended, round 45 wave 2):** entry 14's fix description, read alone,
implied the run-binding closes provenance. It does not, and SCORECARD.md records C1 as
NOT MET as declared for exactly this reason: the window + counter-sha + toolSha256
bindings refuse the three demonstrated defect classes, but mtime is mutable metadata and
a self-reported sha authenticates a field, not a writer — a receipt written during the
window by different bytes carrying the expected shas is indistinguishable from an honest
one (`w1/CriticC1Predicate.md`, `w2/AttackKnowledgeEntry.md` F1). Two more named limits
from wave 2: the run window is cohort-wide for its start (a receipt bound to a sibling
control of the same cohort also passes the window; the toolSha256 binding added in wave
2 closes the receipt→control leg of that), and closing causal provenance fully needs
counter-side cooperation that a receipt field or echoed nonce alone cannot provide —
`w2/AttackC1Sentence.md` and the operator L0 question carry the disposition.
