# ReviewQualityCriteria — r30 w1: QUALITY.md round-28+ criteria vs this round's plan

Method: read `corpus/QUALITY.md` sections round 28 on (lines 298-401, working copy at review
time); verified working-tree state (fixtures, gate, runner); read both round-30 counters and
both before-receipts. I did not run any counter and did not mutate anything. No tooling
installed. Sandbox unused (no writes outside my report).

## Working-tree facts the table rests on

- `scripts/fixtures/citing-set/`: 29 cases; `grep '"reason"'` over them → 0 files. Matches the
  r29 open-debt paragraph (`QUALITY.md:396-401`).
- `scripts/citing_set.py`: no `document_duplicate_key` / `document_nonfinite_number` strings —
  the two new reason codes are not yet implemented.
- `scripts/citing_set_selftest.py:179-181`: today's runner rejects any non-string findings entry
  ("findings must contain only strings") and compares the sorted id multiset only
  (`:272-277`) — so the C1 build must change the runner, not only add fixtures.
- `corpus/knowledge/render-static-sites.md` and `corpus/lessons/round-30.md` do not exist yet;
  SOURCES rows for S049-S052 not yet landed. All C2 entry-side criteria are plan-level here.
- Counters exist and match their docstrings: `.ufo/waves/round-30/c1_reason_count.py` (548
  lines; full-tuple judge at :181-201, fixture scan :391-404, rename-mutant runner :423-452,
  constant stubs :101-102) and `.ufo/waves/round-30/c2_quote_truth.py` (129 lines; committed
  bytes only via `git show`, digest+substring check, one-letter-flip control).
- Before-receipts: `verification/c1-before-0356681.json` (0/14; controls 3/3;
  constantGatesRejected true; runnerBaseline 29 cases exit 0; pins counter/gate/runner sha256)
  and `verification/c2-before-0356681.json` (0/4).

## Criterion → status table

| QUALITY.md lines | Criterion (short) | Status for this round's plan |
|---|---|---|
| 307-316 | Counter must reject a constant (controls + recorded mutant) | SATISFIED by built counter: K1-K3 valid-input controls, and all 14 checks re-run under constant-clean and refuse-everything stubs, each required <14 (before receipt already shows both 0/14, rejected). Obligation: save the after-run receipt at the landed commit — the recorded-mutant showing must exist for the after claim, not only at base. |
| 317-322 | Conformance exceptions named; fixture-oracle granularity on the record | PENDING writer obligation. The interface contract states the granularity (exit code + sorted multiset of (id, reason); legacy string entries compare as id-only; exit comparison unchanged). That statement must land verbatim in `corpus/lessons/round-30.md`/SCORECARD; round-30.md is absent today. Report-length overruns stay listed per seat. |
| 323-327 | No-harm keeps its measured scope | SATISFIABLE, watch. Touched surfaces: gate, runner, citing-set fixtures. Legacy string form stays accepted and the 29 prior cases keep passing (pinned runnerBaseline). Any no-harm receipt must name exactly these surfaces; never restate as universal CLI safety. Round-24 policy stop stays unretried. |
| 328-332 | No field data is not a pass | NOT TRIPPED if the entry stays deploy-semantics. Grep for CrUX/Core Web Vitals/Lighthouse/field data/LCP/CLS/INP over retained S049-S052.txt: one incidental hit ("inP" inside "renderSubdomainPolicy", S052.txt:1) — no field-data vocabulary. The entry is unwritten; if any performance sentence lands it must name page/origin-level CrUX or "no field data" plus the 28-day window, else it fails this bar. |
| 346-361 | Committed fixture asserts the reason code, runner compares it (incl. Limit at 359-361) | OPEN DEBT → this round's repair target. Today 0/29 fixtures name a reason. Plan satisfies: object-form expected entries; counter requires, per all 10 codes (R01-R08 + duplicate-key + non-finite), a committed fixture naming it (`fixture` part) AND a rename-mutant run where the runner must exit nonzero once the code is renamed in the gate (`compared` part) — that exactly enforces the Limit clause (a fixture set that names reasons the runner never compares fails). Where it could still fail: fewer than one object fixture for any one of the 10 codes, or a runner that accepts object entries but compares ids only (the rename mutant catches that too). |
| 362-374 | Counter compares the reason code, not only the id | SATISFIED by built counter. `judge()` compares exit, verdict and the full (id, reason) tuple per case (:181-201); observed reasons are not display-only. Round 30 is "the next round that works the surface" per :373-374. |
| 375-388 | Gate quote found in retained source text, digest verified | SATISFIED by built counter. Reads committed bytes only; checks registry row mined/2026-10-22/URL, entry body cite below the 8-line header, exactly one Gate line with one curly 1-25-word quote, retained .txt sha256 equal to receipts.json textSha256, and the whitespace-collapsed quote an exact substring; one-letter-flip control must miss. Collapse matches the :399-401 note. Residual below. |
| 389-395 | A new gate ships its fixtures in the same round | NOT TRIPPED: no new gate is declared; citing_set and base_path gates pre-exist. If any seat introduces a gate late, this bar applies at birth (fixtures + reason-naming expectations in the same round). |
| 396-401 | Status paragraph: citing-set fixtures are open debt | MUST NOT BE EDITED in place. The paragraph stays byte-identical (round-20/21 ruling; correction-register practice). The repair is evidenced by the counter at the landed commit; any "now covered" status is an appended tail, not a rewrite of lines 396-401. |

Adjacent note (r27 freeze rules, just before the window): the before-receipt pins
counter/gate/runner sha256 but NOT the fixture bytes. Converting legacy `expected.json` files
rewrites committed bytes; pin the 29 before-files (per-file sha256 or a copy) in wave evidence
so the old/new expected sets and replays stay auditable.

## Residual risk

- c2_quote_truth's flip control mutates only the quote; a bug that made the digest comparison
  always true would not be killed by any control. Implemented behavior is correct (sha_ok is
  conjunctively required); residual is mutant-coverage, not behavior.
- F04 (exit 64 repeated options) and F06 (O_NOCTTY) are coverable only by counter-built cases —
  the fixture runner's per-case argv cannot express them. Fine under the standing bars, but the
  lesson must not claim the committed fixture suite covers every input class.
- r28 round-28 counter granularity history (:320-322) stays as history; do not restate it as
  the current oracle.

## Commands run (all read-only, exit codes)

- `ls scripts/fixtures/citing-set | wc -l` → 29 (exit 0).
- grep `"reason"` over `scripts/fixtures/citing-set/` → no matches (0 files).
- grep `document_duplicate_key|document_nonfinite_number` over `scripts/citing_set.py` → no matches.
- greps for section headers/Fails-if lines in `corpus/QUALITY.md`, runner/counter internals,
  SCORECARD round-30 section, sources CWV vocabulary, receipts.json fields → as cited above.
- Not run: both counters (before values taken from the committed receipts and SCORECARD;
  neither re-executed by this seat), `citing_set_selftest.py`, any jj/git mutating command.

## Not verified by this seat

- That the after-values (14/14, 4/4) hold — nothing is landed yet; gate, runner, fixtures,
  knowledge entry, SOURCES rows and round-30 lesson are all still to be written.
- Byte-level behavior of the future runner on mixed-form cases (one case object, another
  legacy) — contract says per-case uniformity; untestable until implemented.
