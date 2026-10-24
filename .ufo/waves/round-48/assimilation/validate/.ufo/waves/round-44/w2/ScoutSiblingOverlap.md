# ScoutSiblingOverlap — sibling overlap vs kake r44 C1/C2

Seat: `kake-r44.ScoutSiblingOverlap`. Read-only. No installs.

## Axes

1. Recall — last 3 rounds of kumitate, tameshi, kama (waves + SCORECARD), not the literal `round-4*` glob alone.
2. Precision — do not merge a shared word (`re-deriv`, `witness`, `class`, `receipt`) into kake C1/C2.
3. Citation — a shared `corpus/SOURCES.md` `teaches` row cites a sibling artifact only when it is the same method.

## Attack and verdict

**Named attack:** last-3-round sibling work on differential-counter witness classes, ledger receipt re-derivation checkers, or witness-class gates overlaps kake r44 C1/C2 enough that a shared SOURCES.md `teaches` row should cite it.

**FAIL.** Do not add or retarget a `teaches` row at this sibling work for C1 or C2.

- C1 (class-module witness under `--classes v5`, placebo, 27 controls, open G6 casememo) has **zero** name hits in the searched trees.
- C2 (`scripts/ledger_latest_check.py`: last LOG/SCORECARD figure vs committed receipt JSON) has **zero** name hits. Near instruments re-derive different objects.
- The only shared clauses already have rows: S129/S131 (tameshi r33 freeze / do-nothing) and S130/S132 (kama writing-revision principle). Those rows do not teach G1–G10 class witnessing or the three-figure ledger checker, and the newer sibling artifacts should not be folded into them.

Confidence: high on the negative name sweep; high that the near-misses below are different objects.

## Scope actually searched

Literal `round-4*` exists only under kumitate (10 dirs, newest three `round-47` `round-48` `round-49`). Tameshi and kama have **zero** `round-4*` dirs (their tips are 35 and 31). Last three round dirs by number:

| lane | waves | SCORECARD |
|---|---|---|
| kumitate | `round-49`, `round-50`, `round-51` (also name-swept `round-47` and `round-48`, the rest of the newest `round-4*` trio) | headings for 48, 49, 50 exist; **no** `## Round 51`; physical EOF is still the round-47 section (`SCORECARD.md:2226`) because later rounds were inserted earlier (`:1756` round 50, `:1829` round 49) |
| tameshi | `round-33`, `round-34`, `round-35` | tail is `## Round 35` (`SCORECARD.md:1672`) |
| kama | `round-29`, `round-30`, `round-31` | tail is `## Round 31 attempt 2` (`SCORECARD.md:1650`) |

## Decisive command output (verbatim)

Artifact-name sweep, 2026-10-23. `rg` exit 1 = no match. First `--classes v5` invocation was invalid (`rc=2`, pattern eaten as a flag) and is **not** evidence; the rerun is.

```
=== artifact-name sweep (last-3 waves + 3 SCORECARDs) ===
NEEDLE 'ledger_latest_check' files=0 rc=1
NEEDLE 'c44_count' files=0 rc=1
NEEDLE 'controls-27' files=0 rc=1
NEEDLE 'casememo' files=0 rc=1
NEEDLE '--classes v5' files=0 rc=2
NEEDLE 'differential-counter' files=0 rc=1
NEEDLE 'differential counter' files=0 rc=1
=== round-4* dirs present? ===
kumitate round-4* count 10 last3-of-those ['round-47', 'round-48', 'round-49']
tameshi round-4* count 0 last3-of-those []
kama round-4* count 0 last3-of-those []
=== kumitate SCORECARD ## Round 49/50/51 headings ===
1756:## Round 50 — claim, closure audit and limits (2026-10-23)
```

Rerun of the broken needle (`rg -l -F --no-messages -- '--classes v5'` on the same 9 wave dirs + 3 SCORECARDs):

```
rc=1
```

Same fixed needles on kumitate `round-47` and `round-48` only (`ledger_latest_check`, `c44_count`, `controls-27`, `casememo`, `differential counter`, `differential-counter`, `witness class`, `witness-class`, and `-- '--classes v5'`):

```
fixed_rc=1
classes_rc=1
```

Broader lexical census (not a hit list to cite; counts only). Patterns were case-insensitive. `diff-counter` = `differential[-_ ]counter|diff.?counter`. `witness-gate` = `witness gate|witness-gate|ho_witness`. `ledger-rederiv` = `ledger_latest|re-?deriv|receipt-derived|ledger receipt`.

```
kumitate round-49 files=25  diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=3 class-gate=0 casememo-g6=0
kumitate round-50 files=97  diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=10 class-gate=0 casememo-g6=0
kumitate round-51 files=19  diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=1 class-gate=0 casememo-g6=0
tameshi  round-33 files=38  diff-counter=0 witness-class=0 witness-gate=7 ledger-rederiv=3 class-gate=0 casememo-g6=0
tameshi  round-34 files=70  diff-counter=0 witness-class=0 witness-gate=45 ledger-rederiv=17 class-gate=0 casememo-g6=0
tameshi  round-35 files=76  diff-counter=0 witness-class=1 witness-gate=1 ledger-rederiv=13 class-gate=0 casememo-g6=0
kama     round-29 files=828 diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=26 class-gate=0 casememo-g6=0
kama     round-30 files=133 diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=5 class-gate=0 casememo-g6=0
kama     round-31 files=847 diff-counter=0 witness-class=0 witness-gate=0 ledger-rederiv=40 class-gate=0 casememo-g6=0
```

The single `witness-class` file is `tameshi-shokunin/.ufo/waves/round-35/w2/SimplifyCodeView.md` (phrase "six witness classes" = lexical edge probes of `code_view`, quoted below).

## What each near-miss actually is

### C1 — differential-counter witness classes

Kake C1 is counter v5 appending class runs G1–G10 (`c44_count_v5.py` docstring; `controls-27.tsv` maps 27 controls onto G1–G10; placebo swaps class modules). No sibling file in the searched trees names that counter, that TSV, casememo, or `--classes v5`.

Kumitate already recorded the non-merge, round 49, `r49/ConnSiblingOverlap.md:196-208`:

```
## What NOT to absorb (out of province — kumitate must not import these)
1. tameshi's sealed held-out set authoring machinery, set-aware witness/equivalence rules
   (`corpus/knowledge/witness-equivalence-rule.md`), ...
3. kama's `count-c1.py` extractor and its six statement classes — kama-owned; only the
   writing-revision *principle* is cited.
5. kake's sitemap/URL counter machinery and kotodama's locator/reopener tools — no overlap with either
   claim beyond the shared discipline clauses already cited in §B.
```

That seat's own claims are cap-run / bind-oracle / doctrine probes (rounds 49–50) and, in the frozen round-51 plan, `scripts/receipt-attest.mjs` (nonce + sidecar over an invocation record). Not a class-module differential counter.

### Witness-class gates (tameshi r33–r35) — same words, different object

Tameshi's gate is `ho_witness_ok` on bash tally-audit copies (amendment 6, set-aware accept/kill). Round 34 mutates that gate (seat reports titled "C1 witness gate"). Round 35 `SimplifyCodeView.md:163-164`:

```
the checks. No false-accept path via `code_view` was constructible; all six witness classes
degrade to rc∈{1,2} or a misattributed kill.
```

Those six classes are comment/heredoc/backslash edge witnesses of a code view, not G1–G10 sitemap shapes. Kake already cites the adjacent discipline (do-nothing control + freeze byte check) as S129, superseded by S131, from tameshi `round-33/w1/CtlDoNothing.md` and `ReviewFreeze.md` only. S129's `teaches` cell (`corpus/SOURCES.md:137`) is the freeze/do-nothing pattern, not `ho_witness_ok`. Citing the r34 gate or the r35 six lexical classes from a C1 class-witness row would merge domains. Kumitate's lines 198–200 say the same: do not cite tameshi witness/equivalence rules as receipts.

### C2 — ledger receipt re-derivation

Kake C2 compares the **last** match of three fixed figures (`rescore-tally`, `donothing-ratios`, `build-ratio-range`) in `SCORECARD.md` / `LOG.md` to values derived from committed round-43 JSON (`scripts/ledger_latest_check.py:23-46`, `:227-245`). No sibling file names `ledger_latest_check`.

Nearest checkers, and why they are not that contract:

- **Tameshi r35 C2** is a six-class record-mismatch counter, not a latest-figure-vs-receipt check. `residual/ResidualReviewC2.md:13-16` and the re-run at `:94-95`:

```
C2_R35: m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 entries=40 sources_rows=99 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C2_R35_PASS=true
```

  SCORECARD tail (`:1672`) calls this "C2 six-class record repair". m1–m6 are knowledge-header keys, README mentions, and untracked wave files (`ResidualReviewC2.md:14-16`), not T1/T5 ratios or distinct `toolSha256`.

- **Kama r30 `count-c1.py:1-12`** re-derives statement classes P/H/N/C/T/Q from committed text at writing revision W and refuses the oracle `holds`/`evidence` fields. `controls/RefInstrument/REPORT.md:111-114` states that. SCORECARD `:1513-1514` (round-30 corrections, not the physical tail) says the round-30 counter re-derived its class check at W. That is the writing-revision principle already taught by S130/S132 (`kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`). The six statement classes stay kama-owned (kumitate `:203-204`). Kama r31 tail is chat-completions eligibility and meaning-cell corrections (`SCORECARD.md:1650-1706`), not a ledger-figure checker. Older "receipt re-derived by `tests/llamacpp-live/check-receipt.py`" lines (`SCORECARD.md:591-592`, `:628`) are the round-16 llama.cpp lifecycle gate; they matched `re-deriv` and are not last-3-round work and not LOG-figure re-derivation.

- **Kumitate "re-deriv"** hits are proxy-stanza / claims re-derivation and the phrase "prevent re-derivation" in `r49/ConnSiblingOverlap.md:25`. Round-51 plan `:21-37` `receipt-attest` verifies an invocation receipt's inner digest, sidecar, and nonce uniqueness (`RECEIPT: VALID|REPLAY|TAMPERED`). It does not read the last stated number in a ledger and compare it to an older receipt. Round-50 SCORECARD C1 (`:1770-1782`) is the cap-run mount-root guard (`BINDGUARD50`), not a ledger checker.

## SOURCES.md citation decision

No new shared `teaches` row should cite kumitate r49–r51, tameshi r34–r35 witness-gate/code-view classes, or kama r29–r31 `count-c1.py` / `count-c2.py` as a source for kake r44 C1 or C2.

Leave S131 and S132 as they are: they already cite the only overlapping method clauses (pre-data do-nothing + freeze bytes; self-assessment checked at the writing revision). Extending either `teaches` cell to the sibling class machinery would violate the non-merge those lanes already wrote down.

Lane roots have no `SOURCES.md`; the registry that would carry the row is `kake-shokunin/corpus/SOURCES.md`. Not edited.

## Paths opened (content read, not just listed)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `kake-shokunin/.ufo/waves/round-44/w2-spec.json` (item prompt, line 154)
- `kake-shokunin/corpus/SOURCES.md:137` (S129 `teaches`)
- `kake-shokunin/corpus/lessons/round-44.md` (S131/S132 table, via search)
- `kake-shokunin/scripts/ledger_latest_check.py` (contract and `run_check`, via search)
- `kake-shokunin/.ufo/waves/round-44/controls-27.tsv` (class map, via search; not a sibling path)
- `/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-44.md` (SOURCES contract pointer, via search)
- `kumitate-shokunin/SCORECARD.md` (`:-40` and `:1756-1785`)
- `kumitate-shokunin/.ufo/waves/round-49/r49/ConnSiblingOverlap.md` (`:173-210`)
- `kumitate-shokunin/.ufo/waves/round-51/plan.md` (`:1-43`)
- `tameshi-shokunin/SCORECARD.md` (`:-40`)
- `tameshi-shokunin/.ufo/waves/round-35/w2/SimplifyCodeView.md` (`:140-176`)
- `tameshi-shokunin/.ufo/waves/round-35/residual/ResidualReviewC2.md` (via search, lines 13–16 and 94–95)
- `kama-shokunin/SCORECARD.md` (`:-40`, plus heading search)
- `kama-shokunin/.ufo/waves/round-30/count-c1.py` (`:1-43`)
- `kama-shokunin/.ufo/waves/round-30/controls/RefInstrument/REPORT.md` (`:97-130`)

Searched but not opened as documents: the other wave files that only contributed to the count tables above (dispatch JSON, mutation-seat reports, kama `w2/out/**`). Fleet-root `SOURCES.md` hits under `.ufo/waves/hyaku/` and `scripts/fixtures/` were from a too-wide `teaches` search and are out of this item's lanes; not used as overlap evidence.

## Files written

- `.ufo/waves/round-44/w2/ScoutSiblingOverlap.md` (this report)
- scratch directory created, empty: `/fast/scratch/hyaku/kake-r44/ScoutSiblingOverlap/`

## Blockers

None. Unrun: no counter, no `ledger_latest_check.py`, no sibling test suite (this seat is a scan). Kumitate round 51 may still be in flight; the plan on disk is what was read, not a close receipt.

## Commands (exact)

```
ls -d /home/vgpnk/Projects/shokunin/{kumitate,tameshi,kama}-shokunin/.ufo/waves/round-*
python3  # per-round file counts + rg -l topic patterns (census block above)
python3  # artifact-name sweep (decisive block above)
rg -l -F --no-messages -- '--classes v5' <9 wave dirs + 3 SCORECARDs>
rg -l -F --no-messages -e ledger_latest_check -e c44_count -e controls-27 -e casememo -e 'differential counter' -e differential-counter -e 'witness class' -e witness-class -- kumitate round-47 round-48
rg -l -F --no-messages -- '--classes v5' kumitate round-47 round-48
rg -n '^## Round ...' on the three SCORECARD.md files
mkdir -p /fast/scratch/hyaku/kake-r44/ScoutSiblingOverlap
```
