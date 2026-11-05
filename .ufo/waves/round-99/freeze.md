# kake round 99 — freeze (claims, predicates, counters, kill rules; written before any seat ran)

Round base `cde408e5817bf1376c701d8decc5469fa82b2985` (lane `master`, = remote at round start).
Instruments commit `2345e309640adac6c36e41eca87409085ba3a276` (both counters, the C2 contract,
control subjects, retained RFC 9111 + EID 9185 bodies, SKILL.md instrument rows). Every control
below was executed against those committed instruments BEFORE this freeze and before any seat ran;
receipts are in `controls/` and are committed with this file. Digests: `controls/instrument-sha256.txt`.

Fresh-start reads (run-15 amendment 35; kake fresh-start authorised): the last three rejected
closures r94, r96, r98 and their spot-checks. r98's root failure was a live reviewer's `disagree`
on two L1-written rows (C1 kill rule), plus a dead review seat; r96/r94 failed on instrument and
population defects found after scoring. This round therefore (a) executes every do-nothing,
forgery and positive control before the freeze, (b) writes the C1 rows before the wave so both
review seats judge final bytes, and (c) keeps the kill rule, counter and target unchanged after
any seat scores.

## C1 — calibration (score 3, the lowest owned non-retired axis)

Surface: the gate/probe registry tables of `SKILL.md` (the lane's self-assessment of which tools it
owns, how to run them, what their exits mean, and how to self-test them) against the committed
tools directly under `scripts/` (observed repo state). Routed by the r98 closure (R98-C1: a gate
without a registry row).

- Counter: `python3 -B .ufo/waves/round-99/c99_registry.py --root . --revision <REV> --work <scratch>`
  (semantics in its docstring; rules R1-R5; one executed self-test command per row).
- Draft history (honest): a first draft of the counter printed `unlisted=29` at base; before any
  receipt was committed its parser was amended twice (a leading `VAR=$(...)` assignment is
  dropped before the forbidden-token check; a verdict digit may be followed by a backtick). The
  committed instrument at `2345e309` is the only scored instrument.
- Before (base `cde408e5`): `tools=54 … unlisted=26 dangling=0 … mismatches=26 met=false`, exit 1
  (`controls/base-c1.txt`).
- Target: at the C1 repair commit, `unlisted=0 dangling=0 mismatches=0 met=true`, exit 0.
- Review conjunct: two reviewer seats, ReviewRegA and ReviewRegB, each judge every one of the 26
  rows the repair adds, writing `w1/<seat>/verdicts.tsv` lines `<row name>\t<agree|disagree>\t<reason>`.
- **Predicate (frozen):** C1 is met iff the counter prints `met=true` exit 0 at the repair commit
  AND every repair row has at least one live reviewer verdict AND no live verdict is `disagree`.
- **Kill rule (frozen):** one live `disagree` on any repair row → C1 unmet, recorded unmet; the row
  may be corrected later but the verdict does not flip. Both review seats dead or verdict-less → unmet.
  A row missing from a live seat's file counts as no verdict from that seat.
- Score rule: met → calibration 3 → 4. Unmet → stays 3.
- Controls (pre-freeze, scratch clone commits with fixture identity, never the lane):
  positive = base + the repair section → expected `met=true`; names-only rows → expected
  `met=false`; the real rows inside a fence → `met=false`; every `no self-test` cell replaced by a
  `--selftest` command the tool lacks → `met=false` (exec_fail); owner forged → `met=false`;
  junk prose in well-formed rows → expected `met=true` — **declared counter limit**, caught only by
  the review conjunct; selftest 20/20.
- Ordering rule: C2 adds `scripts/freshen_304.py` to the population, so the C2 commit must carry
  its own conformant registry row; C1 is scored at the repair commit and re-read at the tip
  (reported, not re-scored).

## C2 — freshness (HOLD 10), capability acquisition, sourced on S484

Surface: a new decision the lane did not hold — which stored responses a 304 (Not Modified) freshens
and what their updated header fields are (RFC 9111 §4.3.4 + §3.2 with the §3.1 exceptions).
Contract: `.ufo/waves/round-99/fresh304-contract.md` (lane conventions LC1-LC6 marked).
Source rows opened this round: S484 (RFC 9111 §3.1/§3.2/§4.3.4, retained
`sources/rfc9111.txt` sha256 `aeb52adb…`), S485 (EID 9185, Reported, on the §4.3.4 initial-set
paragraph, retained `sources/eid9185.html`).

- Counter: `python3 -B .ufo/waves/round-99/c99_fresh304.py --root . --revision <REV> --work <scratch>`
  (default seed = int(first 8 hex of the scored revision, 16); 240 generated cases).
- Before (base): `candidate=absent met=false`, exit 1 (`controls/base-c2.txt`).
- Target: at the C2 content commit, `candidate=present hand=50/50 generated=240/240 met=true`,
  exit 0, and the scored sha256 equals `git show <REV>:scripts/freshen_304.py | sha256sum`.
- **Predicate (frozen):** exactly that line, exit 0, at the C2 content commit.
- **Kill rule (frozen):** any hand or generated failure at that commit → C2 unmet; no re-seeding,
  no contract or counter edit after a candidate is scored.
- Controls (pre-freeze, `--candidate-file`): positive oracle `met=true`; seven forgeries
  (constant, hand-table lookup, must-not→no-update, first-match-not-most-recent, no §3.2
  exclusions, weak comparison in the strong rule, lenient refusals) all `met=false`.
- Capability row enters SCORECARD only as "met on the frozen predicate"; admission is the
  outside closure's.

## Frontier step

Census before/after (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`);
rows S484/S485 written only after the scout seat's in-round re-open; one mined mistake in
`corpus/lessons/round-99.md`; assimilation: collision check committed (`assimilation/`, 8
collisions, no renumber map → nothing appended).
