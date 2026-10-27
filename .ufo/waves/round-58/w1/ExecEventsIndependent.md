# ExecEventsIndependent

Claim C1 (calibration), independent re-derivation of the receipt-event population at base
`044048597d62f3199494b63b36e90dd57825e350`. I did not import, copy or call into
`.ufo/waves/round-58/c58_receipt_rewrites.py`; I ran it once as a black box (`--list`) only to obtain the
list I had to compare against. All scratch work was under `/fast/scratch/hyaku/kake-r58/ExecEventsIndependent/`
(deleted when done; receipts copied into `.files/` first).

## SCRIPT:

`.ufo/waves/round-58/w1/ExecEventsIndependent.files/events.py` (stdlib only: argparse/json/os/re/sys/subprocess;
13256 bytes). Method, chosen to differ from the counter at every step:

- ancestry: `git rev-list <rev>` — the whole ancestry, no pathspec, no `--first-parent` (341 commits at base;
  338 under `--first-parent`; 2 merges; 1 root).
- per commit: `git diff-tree -r --no-renames -z --name-status <c>^1 <c>`, root commit with `--root`.
- population: `^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$`.
- event: `M` or `D` of a population path, or `A` of a path already seen earlier in the oldest-first walk
  (first `A` = creation). Blob ids via `git rev-parse <rev>:<path>` at `<c>^1` and `<c>`.

Runs (all exit 0; `TMPDIR` set to the scratch dir):
`python3 -B events.py --compare counter_base.out [--detail|--json]`.
Second, independent mechanism for the same population: `git log --format=%H <rev> -- <path>` for all 70
population paths — per path the commit count equals `touches` and `touches - 1 == events` for all 70,
totalling 19. Receipts: `.files/final.out` (full stdout), `.files/final.json`, `.files/counter_base.out`.

## AGREEMENT:

Counter at base (`--root <lane> --revision 0440485…`, exit 1): `events=19 undisclosed=19 phantom=0
malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`, ledger absent.

- Set equality: **equal**, on the full quintuple `(path, commit12, status, fromBlob12, toBlob12)`, not just the
  path set: counter 19 vs independent 19, 0 only-counter, 0 only-independent.
- Status: all 19 are `M`. No `D`, no re-add, no rename in the population at base.
- Distribution: round-52 `control/` 6, round-54 `controls/` 5, round-55 `controls/` 4, round-56 `controls/` 3,
  round-57 `controls/` 1. 16 of the 70 population paths ever committed carry the 19 events; 54 are written once
  and never touched.
- Repeat rewrites: `round-52/control/c1-mutation-ladder.json` 3 events (4 commits, 4 distinct blobs) and
  `round-54/controls/c1-selftest.txt` 2 events (3 commits, 3 blobs); the other 14 paths have 1 event each. Sum 19.
- No revert: for all 16 rewritten paths `distinct_blobs == touches` and first blob ≠ tip blob, so every event is
  a real content change, not a re-commit of identical bytes.
- Full ancestry vs `--first-parent`: identical event sets (the 2 merges contribute no population event and no
  event is reachable only through a second parent), so the counter's `--first-parent` log option does not shrink
  the population.
- Round-57 D1 spot-check reproduced directly: parent blob of `round-57/controls/after-c1-receipt-pins.txt` at
  `20217f23eca1` is the literal `pending` plus a `revision:` line; the commit blob is the full
  `C1 receipt-pins … met=True` predicate line. The `fill` class is real.
- No `round-58` path appears in any event at base: the population is clean for `new_rewritten == 0`.

## OUTSIDE POPULATION:

Same walk, every path outside the population that changes after its first commit (oldest-first, `M` counts):

| stratum | paths | events |
|---|---|---|
| `control(s)/` depth ≥ 2 — excluded by the counter's `[^/]+$` | 475 ever created | **0** |
| `.ufo/waves/round-*/*.json` | 10 | 10 |
| `.ufo/round-*/**` | 5 | 5 |
| `.ufo/waves/round-*/w*/**` | 12 | 15 (10 seat `.md` reports = 13 events; 2 `swarm-registry.json` = 2) |
| `.ufo/` data artifacts outside the population (non-`.md`, data extensions) | **79** | **79** |
| non-`.ufo` repo files (reports/ledgers/corpus/scripts) | 147 | 889 |

The depth-2 exclusion is **inert**: 0 of 475 nested `control(s)/` files is ever rewritten after creation, so the
`[^/]+$` pattern hides nothing. The non-`.ufo` row is scale only, not receipts (`SCORECARD.md` 122, `LOG.md` 113,
`SKILL.md` 70, `corpus/SOURCES.md` 65, …); `scripts/id_resolver.py` is there with 1 event at `32754df75774` —
that is the C2 fix commit, not a receipt.

Rows overlap on purpose (they answer the assignment's four widen questions). Disjoint accounting of everything
outside the population that changes after its first commit: 325 paths / 1104 events, of which 178 paths / 215
events under `.ufo/` (67 `.json`, 51 `.py`, 45 `.md` / 57 events, 10 `.txt`, 2 `.sh`, 1 `.mjs`, 1 `SHA256SUMS`,
1 `.exit`) and 147 paths / 889 events outside `.ufo/`. The 79 data-artifact paths are exactly the `.ufo/` paths
that are neither `.md` nor code, and each carries exactly one rewrite.

The 79 `.ufo/` data artifacts split into 23 whose file name declares them receipts/evidence and 56 that do not.
The 23 (path, events=1, commit):

```
.ufo/waves/round-24/w1-deaths.json                                  6883f1d580d8
.ufo/waves/round-26/receipt-locator-errata.json                     a2be0dc53845
.ufo/waves/round-26/statements.json                                 b44daedc9658
.ufo/waves/round-27/pairs.json                                      cd2e95b00116
.ufo/waves/round-34/sources/receipts.json                           9ef758c95d5e
.ufo/waves/round-35/sources/receipts.json                           95abec210c35
.ufo/waves/round-36/verification/control-base.json                  cd3212796cab
.ufo/waves/round-36/verification/control-declaration.json           cd3212796cab
.ufo/waves/round-39/sources/SHA256SUMS                              4c080d3d4ef1
.ufo/waves/round-40/census-after.txt                                83b482040cd2
.ufo/waves/round-40/resid-dispatch-log.txt                          83b482040cd2
.ufo/waves/round-40/w1-dispatch-log.txt                             83b482040cd2
.ufo/waves/round-41/w2-dispatch-log.txt                             c4eb7e73c073
.ufo/waves/round-42/w1-dispatch-log.txt                             1e1da6975dfb
.ufo/waves/round-43/verification/freeze/sweep-before.exit           a377c5d0b98e
.ufo/waves/round-43/w1-dispatch-log.txt                             a377c5d0b98e
.ufo/waves/round-44/verification/claim/ledger-after.txt             942fe187034c
.ufo/waves/round-45/fixtures/counter-error/control-receipt.json     dc7f03e7c8ba
.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json dc7f03e7c8ba
.ufo/waves/round-45/verification/matrix/after.json                  dc7f03e7c8ba
.ufo/waves/round-45/verification/matrix/before.json                 dc7f03e7c8ba
.ufo/waves/round-51/assimilation/pre-append/census-correction.txt   842c1b44a590
.ufo/waves/round-52/baselines.json                                  a4a890cf1381
```

The 56 unnamed decompose exactly (each 1 event): 35 `round-36/verification/ablations/*.json`, 7
`round-23/{receipts/*.json ×5, recovery-audits.json, wave-inventory.json}`, 4 `.ufo/round-20/*.json`,
3 `round-22/*` (`frozen/expected.json`, `w2-spec.json`, `wave-inventory.json`), and 7 singles:
`round-25/w2/swarm-registry.json`, `round-31/a2-w2/seat-status.json`,
`round-35/verification/criterion-control-description-r35-correction.txt`,
`round-45/verification/freshness/freshness.json`, `round-45/verification/matrix/run-log.txt`,
`round-46/residual-spec.json`, `round-47/w1/swarm-registry.json`. Full list in `.files/final.out` under
`EVIDENCE`.

## RECOMMENDATION:

1. **C1's number is sound.** 19 is not an artifact of the counter's regex, of `--first-parent`, of `--no-renames`
   or of history simplification: an independent walk of the full ancestry reproduces the same 19 events down to
   both blob ids, and a third mechanism (`git log -- <path>` per population path) gives 19 as well.
2. **Do not widen the population this round.** The contract is frozen and already declares the limit ("receipts
   outside `control(s)/` dirs"). Widening now would be a post-data contract change and would multiply the ledger
   ~4× without changing the claim's truth.
3. **Cheap honesty fix for the C1 report (not the counter):** the claim title says "every post-commit change to a
   measurement receipt" while the surface is `control(s)/`. Add one sentence naming the quantified residual —
   "19 in-scope events; 79 `.ufo/` data-artifact rewrites outside the surface, of which 23 receipt-named, listed in
   `w1/ExecEventsIndependent.md`". That removes the only overbreadth a critic can attack, at no cost to the
   predicate.
4. **Depth-2 exclusion needs no action** (0 of 475 nested files rewritten). If a future round wants the simpler
   regex `^\.ufo/waves/round-[0-9]+/(control|controls)/.+$`, it is behaviour-neutral today — but that is a v2
   change, not this round's.
5. **For the build seat writing the ledger:** three of the six round-52 events are the same path
   (`control/c1-mutation-ladder.json`), and two of the five round-54 events are the same path
   (`controls/c1-selftest.txt`), so rows must be distinct `(path, commit)` pairs — a duplicate entry is counted
   `phantom` — and each note pointer must resolve at the measured tip, not at the event commit.

Not run by me (out of scope): the counter's `--selftest`, the post-build tip measurement, any build edit. No tools
installed or upgraded (none needed); no pacman; scratch dir deleted after copying receipts.

VERDICT: 19-event population independently reproduced with exact blob-level agreement at base, the nested-controls exclusion is inert, and 79 `.ufo` artifact rewrites (23 receipt-named) lie outside the frozen surface as the contract already declares.
