# ReviewerC2Registry — attack on C2's registry-row check

Seat: `L1Kake54.ReviewerC2Registry` · round-54 w1 · read-only review.
Target: `.ufo/waves/round-54/c54_ops_debt.py` registry half (P2.1 of contract.md
C2: row for `c53_gate_truth.py` with kind `gate`, entry command, verdict map,
selftest spelling, pinned/frozen proof, write scope, owner).

**Live-state caveat.** During this review a sibling executor landed commit
`8e408e0` and began an in-flight rewrite of the counter. Three states were
observed:

- **Committed (HEAD `8e408e0`)** counter: heading-scoped substring check
  (`REQUIRED = ("c53_gate_truth.py", "gate", "--revision", "0=", "--selftest",
  "exec-quality-gate", "read-only")`; `all(token in line)`; first match wins).
- **Worktree (in-flight, uncommitted)** counter: 8-cell anchored
  `registry_row_ok`, but currently crashes (`NameError: NAME_RE`, line 86) —
  mid-refactor; sibling presumably finishing.
- Committed `SKILL.md:213` row (Name cell `c53-gate-truth`, scope cell lacking
  the literal `read-only`) fails both counters; worktree row text adds
  `read-only` (`Normal path is read-only and reads …`).

Evidence method: scratch clone `/tmp/kake-c2-reg` (disposable, lane untouched),
mutant SKILL.md variants committed on top of `8e408e0`, counters run against
`--revision <mutant>` — the counter reads committed bytes only, so commits were
required. Two dozen mutants run; results below.

## Findings by severity

### HIGH — committed counter: `REQUIRED` does not establish most fields; false-greens demonstrated

`all(token in line for token in REQUIRED)` over the whole matched *line* (not
cells). Proven on mutants against the committed counter (each got
`registry=present`):

| Mutant | Result |
|---|---|
| Owner cell emptied (`… | read-only |  |`) | **present** — no owner token exists; field unestablished |
| Name cell `bogus` (script name only in command cell) | **present** — `c53_gate_truth.py` needn't be the Name cell |
| Kind cell `probe` | **present** — `gate` is a substring of `c53_gate_truth.py`/`exec-quality-gate`, so the kind token is *vacuous* on any matching line; `eviltool` also passed |
| Row deleted; prose sentence carrying the 7 tokens inside the section | **present** — no `^\|` row shape required |
| Single-cell `| <7 tokens> |` row | **present** — cell count never checked |
| Verdict cell `-`, `0=` moved into command cell | **present** — verdict-map anchor `0=` is positional-free |
| `--selftest` only in command/selftest prose | present |

So per the contract's 8 fields: **owner is entirely missing** (no REQUIRED
token), and name/class/command/verdict/selftest/pin/scope are token-*implied*,
not established — every one demonstrably passable while its real cell is wrong
or empty. `exec-quality-gate` doubles as command-path and pin anchor, so the
pinned-proof cell can be blank. A "row" that asserts `0=ok` but never maps
`1=fail` passes: the check cannot distinguish a gate from a probe.

### MEDIUM — scope is the *section*, not the table

- Scan runs `### Owned freshness gate registry` → next `## ` (`SKILL.md:208` →
  `## Live-vs-source drift detection:217`). Correct outer bound (C7: tokens
  after `## ` → `absent`).
- But non-table content inside the section is in-scope: the `Where to learn
  more:` prose (line 215) or any inserted `### ` subheading does not terminate.
  Mutant B5 (worktree counter): a crafted 8-cell row under an injected
  `### Rogue` heading → `registry=present` — placement outside the table passes.
  (CriticC2RegistryPlacement owns this attack; corroborated here.)
- Heading match is exact-strip equality; a renamed heading → `absent`
  (fail-closed, fine).

### MEDIUM — first-match `break`: shadowing both ways

Both counter versions stop at the first in-scope line containing
`c53_gate_truth.py`. Mutants: a token-less mention or malformed row ahead of the
valid row → `absent` (false-red, C8/B3/B4). A crafted *valid* row ahead can
also mask the absent real row (false-green). Row order should not decide the
verdict; all candidate lines should be evaluated, `present` iff any passes.

### MEDIUM — substring tokens survive negation (worktree refactor too)

`registry_row_ok` still uses `in` for cells 2–6. Mutant B8: write-scope cell
`Normal path is never read-only and writes everywhere` → `registry=present`.
Same injection class applies to `exec-quality-gate` (pin cell) and `0=`
(verdict cell — `0=` alone, with no `1=`/`2=`/`64=` mapping, still passes;
a verdict map requiring failure semantics is not established).

### LOW — name-convention friction (worktree refactor)

`cells[0] == "c53_gate_truth.py"` requires the *filename* in the Name cell, but
the landed row and every sibling row use display names (`c53-gate-truth`,
`freshness-sweep`, `corpus-contract`). Mutant B2 → `absent`. If the contract
means "row naming the script," the check is consistent but brittle to
backticks/case; if it means the registry's naming convention, it's a false-red.
Also: `cells[0]=="c53_gate_truth.py"` fails a backticked `Name` while
`MANIFEST_ROW_RE` tolerates backticks — inconsistent quoting policy.

### TRANSIENT — worktree counter crashes

`.ufo/waves/round-54/c54_ops_debt.py` (uncommitted, md5 `4780f2f7…`):
`NameError: NAME_RE` at line 86 — the sibling refactor deleted `NAME_RE`'s
definition (renamed to `MANIFEST_ROW_RE` without updating the call site).
Every invocation exits 1 *with a traceback on stderr*; fail-closed but reports
a Python crash, not a measured `not-met`. Expected to be fixed in flight; the
committed counter is unaffected.

### Out-of-scope interaction (manifest half, noted)

Committed counter's `MANIFEST_RE` rejects backticked filenames; committed
`settlement.md` uses `` `Name.md` `` → `settled=[]`, `manifest=incomplete
uncovered=4` at HEAD even with all seven rows present. So at HEAD the do-
nothing-looking receipt is double-red. Worktree regex fixes backticks and adds
a non-empty-reason requirement (ReviewerC2Manifest territory).

## Answers to the assigned questions

1. **Does it only look inside the owned freshness gate table?** *No — inside
   the section, not the table.* Any line under `### Owned freshness gate
   registry` until the next `## ` qualifies: prose lines, injected `###`
   subsections, non-row text. The next-`## ` outer bound is correct.
2. **Do REQUIRED tokens establish name/class/command/verdict/selftest/pin/
   scope/owner?** *No.* Committed counter: owner field has no token at all;
   the other seven are line-wide substrings, every one satisfiable from the
   wrong cell (or no cell) — all demonstrated green. The `gate` kind token is
   additionally vacuous (contained in `c53_gate_truth.py`). The in-flight
   refactor correctly anchors all eight cells (including `kake` owner), but
   keeps substring injection on cells 2–6, the shadowing break, and the
   section-not-table scope.

Verdict for the wave: the committed check admits the listed false-greens and
misses the owner field; the replacement fixes anchoring but carries the four
residual holes above plus a live crash. Findings only — no admission claimed.
