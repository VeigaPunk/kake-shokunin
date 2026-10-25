# CriticPredicateSizing — kake round 50 wave 1

Attack on the two frozen claims against the claim-sizing rule
(`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-50.md` §9): one concrete
after-state re-derivable with one command over committed bytes, a do-nothing
control that cannot reach it, no universal clause the counter does not
enumerate.

Contract read: `.ufo/waves/round-50/contract.json` (`declaredBeforeScoring:
true`, base `9619af67c52939daac502ca7a24c9d714f3f51db`).

## Control runs (executed, not reasoned)

| command | revision | output | exit |
|---|---|---|---|
| `c50_quote_class.py --revision 9619af6…` | base | `C1 classed 0/3 met=False` | 1 |
| `c50_quote_class.py --revision 33eec7f…` | pre-append | `C1 classed 0/3 met=False` | 1 |
| `c50_durable.py --revision 9619af6…` | base | `C2 durable 0/1 met=False` | 1 |

Base failures (C1): `class ledger absent`, `retained blob absent`, `lesson
absent`, `no live registry row`, `entry absent`. Pre-append failures (C1):
`lesson absent`, `no live registry row`, `entry absent` — the ledger and S286
blobs landed at `33eec7f` but the counter still reads 0/3, so the intermediate
state cannot reach `met` either.

## C1 — `met: classed == 3 of 3 declared ids` (freshness, capability)

**Verdict: PASS — well-sized, no fix required.**

- **One concrete value, one command, committed bytes.** The counter reads only
  via `git show <rev>:<path>` (`COMMITTED_BYTES_ONLY = True`,
  c50_quote_class.py:42, 91-98). `classed` is a single integer derived from
  three declared ids; `met` is `classed == len(DECLARED_IDS)` (line 243). A
  closure re-derives the verdict with exactly the frozen counting command.
- **Do-nothing control cannot reach it.** At base `9619af6` the counter
  returns 0/3 (verified above). A junk-row sham is blocked by three
  independent pins: R1 requires sha256 of the actual retained blobs
  (lines 191-194), R2 re-derives the class from blob content and rejects a
  swapped label (lines 183-190 — a counterfeiter cannot just write
  `matchClass: raw-substring`, it must equal `classify(quote, raw, text)`),
  R3 requires the derived-class sentence verbatim in the lesson and rejects
  the opposite sentence (lines 199-207). R4 binds S286 to the live registry,
  the knowledge entry tail, and the Gate quote (lines 208-232). Fabricating
  the ledger without the blobs, entry, registry row, and lesson sentences all
  agreeing is not cheaper than doing the work.
- **No unenumerated universal.** The predicate quantifies over exactly the
  declared set `{S273, S274, S286}` — the counter iterates `DECLARED_IDS`
  (line 43) and nothing else. "3 of 3" is an enumerated conjunction, not a
  universal over an open set.

**Residual weakness (not a sizing failure, noted for the closure):**
`registry_rows` parses only rows under a `## Registry` heading with ≥10
pipe cells (lines 124-129). Verified against the mirror: the S286 row yields
cells[6]=`mined`, [7]=`2026-10-24`, [8]=`180d`, [9]=entry path — indexing is
correct. But a registry row with fewer than 10 cells, or under a differently
cased heading, would be silently skipped and reported as "no live registry
row" rather than a parse error. That is a fail-closed behavior (it makes
`met` harder to reach fraudulently, not easier), so it does not weaken the
control.

## C2 — `met: durable == 1 of 1` (operability)

**Verdict: PASS — well-sized, no fix required.**

- **One concrete value, one command, committed bytes.** `durable` is 0 or 1
  (c50_durable.py:245), derived entirely from `git show` and
  `git merge-base --is-ancestor` over committed bytes. One command
  re-derives it.
- **Do-nothing control cannot reach it.** At base `9619af6` all four artifact
  families are absent (`order proof absent`, `wave-cite proof absent`,
  `LOG.md … does not cite the wave`, `settlement absent`) — verified above,
  exit 1. The conjunctive chain is long: pre_rev must be a *strict* ancestor
  carrying a mirror that contains S286 while the live registry does not
  (lines 143-154), the census argv must be a `--file` validation of that
  mirror without `--root` (lines 160-163), exit 0 with no E03/E04
  (lines 164-167), grant_rev must be a second strict ancestor distinct from
  pre_rev carrying a one-line grant of 32-64 seats (lines 186-205), a
  `kimi --prompt` dispatch without `--auto` (lines 206-213), LOG.md silent
  about the wave at grant_rev but citing it plus grant_rev at the measured
  revision (lines 214-226), and a settlement whose `spawn` equals granted
  seats with empty `replacements` (lines 227-240). The pre-append commit
  `33eec7f` already exists and satisfies only the order-proof half; the
  grant half still requires real wave-dispatch evidence. A sham cannot meet
  both ancestry pins with committed bytes alone.
- **No unenumerated universal.** "1 of 1" is the single check; every
  sub-condition is explicitly enumerated in the counter's reason list.

**Residual weakness (not a sizing failure, noted for the closure):** the
grant-line regex `GRANT_RE` (line 53) fixes `wave=r50-w1` — the durability
proof is bound to this wave only. Correct for this round's claim; a future
wave would need a new counter, which is consistent with per-round frozen
instruments.

## Ruled-out attack surfaces

- **Predicate-string mismatch**: `PREDICATE` is identical in the contract
  JSON, both counters' constants, and (per docstrings) the plan — no paraphrase
  drift detected.
- **Worktree reads**: both counters open nothing outside `git show`/
  `git merge-base`; the `COMMITTED_BYTES_ONLY` flag is honest.
- **Exit-code laundering**: `met` drives the exit code (0/1); a could-not-
  evaluate path exits 2 and prints an error JSON, never a silent `met: true`.
- **`--json` side channel**: the flag only mirrors stdout to a file; it does
  not alter scoring.

## Net verdict

Both claims satisfy §9: single re-derivable value, do-nothing control verified
to fail at both base and the pre-append intermediate, no unenumerated
universals, frozen predicate string consistent across contract/counters.
**No fix required for either claim.** C1 is the harder instrument (sha256 +
re-derived class + three artifact cross-references per id); C2 is the wider
instrument (two ancestry-pinned revisions, eleven conjuncts). Both are
calibrated to fail closed.

Report: .ufo/waves/round-50/w1/CriticPredicateSizing.md
