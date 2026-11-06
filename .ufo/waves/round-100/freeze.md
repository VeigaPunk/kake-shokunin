# kake round 100 — freeze (claims, predicates, counters, kill rules; written before any seat ran)

Round base `3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5` (lane `master`, = remote at round start).
Instruments commit `d7b73d161173710d04efc5f66784779bce5746ff` (both counters, contract v2, the C2
frozen oracle and forgeries, the C1 fixture builder, `controls.sh`, retained RFC 9110 body, census
before). Every control below was executed against those committed instruments BEFORE this freeze,
before the C1 repair and before any seat ran: `controls.sh <lane> 3989618d… <scratch>`; receipts in
`controls/`, committed with this file; digests in `controls/instrument-sha256.txt`.

Rejection-history reads (run-15 amendment 35 fresh start; last three closures r97 admitted, r98 and
r99 rejected-honest-stop): r99 C1 died on a live reviewer `disagree` over verdict-map cells written
from docstrings (mistake 5, criterion R99-B); r98 C1 on one live `disagree` with a dead second
reviewer. This round therefore (a) builds a counter that EXECUTES the usage path the verdict map
describes instead of trusting prose, (b) changes no verdict-map cell — the C1 repair only removes
the seven older duplicate rows (kept verbatim in a fenced history block), so the reviewers judge
rows that are already code-checked (six were judged `agree` by both r99 reviewers; the seventh,
`scripts/x_robots_tag_audit.py (round-80 grammar)`, was re-read against the code by the L1 before
this freeze), and (c) keeps every predicate, counter and target unchanged after any seat scores.

## C1 — calibration (score 3, the lowest owned non-retired axis)

Surface: `SKILL.md`'s gate/probe registry tables (the lane's self-assessment of how each tool runs
and what its exits mean) against the committed `scripts/` tools (observed state). Routed: R99-5
(duplicate rows — two answers for one tool), R99-6 (the `robots_audit` row at `SKILL.md:1104` whose
self-test span cannot run), R99-3/R99-11 (a counter that checks row truth by executing the tool, not
by reading prose), the r99 spot-check's R99-C1.

- Counter: `python3 -B .ufo/waves/round-100/c100_registry.py --root . --revision <REV> --work <scratch>`
  (round-99 R1-R5 unchanged; v2 adds D1 `duplicated` — a tool invoked by ≥2 registry rows — and D2
  `probe_mismatch` — a row whose verdict map does not name the exit code the tool returns for the
  single argument `--zz-bogus-r100`; every self-test span and probe runs in a bwrap sandbox with no
  network). Selftest 29/29 (`controls/ctl-c1-selftest.txt`).
- Before (base `3989618d`): `tools=55 … unlisted=0 dangling=0 duplicated=7 probe_mismatch=2
  exec_fail=1 mismatches=9 met=false`, exit 1 (`controls/base-c1.txt`).
- Target: at the C1 repair commit, `unlisted=0 dangling=0 duplicated=0 probe_mismatch=0 mismatches=0
  met=true`, exit 0.
- Review conjunct: two reviewer seats, ReviewRegA and ReviewRegB, each judge 8 units — the seven
  kept rows (Name cells `cache_key.py`, `cache_key_conformance.py`, `live_snapshot.py`,
  `response_snapshot.py`, `robots_audit.py`, `source_snapshot.py`,
  `scripts/x_robots_tag_audit.py (round-80 grammar)`) and the fenced history block — writing
  `w1/<seat>/verdicts.tsv` lines `<unit>\t<agree|disagree>\t<reason>`.
- **Predicate (frozen):** C1 is met iff the counter prints `met=true` exit 0 at the repair commit
  AND every one of the 8 units has at least one live reviewer verdict AND no live verdict is
  `disagree`. The report names which seat(s) carried each unit's verdict (R99-2).
- **Kill rule (frozen):** one live `disagree` on any unit → C1 unmet, recorded unmet; the unit may be
  corrected later but the verdict does not flip. Both review seats dead or verdict-less on a unit →
  unmet. A unit missing from a live seat's file counts as no verdict from that seat.
- Score rule: met → calibration 3 → 4. Unmet → stays 3.
- Controls (pre-freeze; scratch clone commits, fixture identity, never the lane; fixture SKILL.md
  sha256 in `controls/fixture-c1-<mode>-SKILL.sha256`): `pos` (the planned repair) → `met=true`;
  `deleteall` (both rows of each duplicated tool removed) → `unlisted=7 met=false`; `keepold` (the
  seven CURRENT rows removed instead) → `met=false` (unlisted 6, probe_mismatch 2, exec_fail 1);
  `everycode` (the kept cache_key.py row's map rewritten to name 0, 1, 2 and 64) → `met=true` —
  **declared counter limit**: a map naming codes the tool never returns passes D2; the review
  conjunct covers it.
- Ordering rule: the real repair must be byte-identical to the `pos` fixture's SKILL.md (sha256 in
  `controls/fixture-c1-pos-SKILL.sha256`). C2 must not add a second row for `scripts/freshen_304.py`;
  C1 is re-read at the tip (reported, not re-scored).

## C2 — freshness (HOLD 10), capability acquisition: 304 freshening contract v2, sourced

Surface: the lane's 304 freshening decision, moved from contract v1 to v2
(`.ufo/waves/round-100/fresh304-contract-v2.md`): qualified Cache-Control in both argument forms
and any case (F1, LC6 case), unrecognised directives ignored (F10, RFC 9111 §5.2.3), output values
trimmed (F2, RFC 9110 §5.5), stored proxy fields dropped (F3), the seven round-99 escape classes
e1-e7 as hand cases (R99-8), and a sandboxed candidate runner (R99-9). Source rows opened this round:
S486 (RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3) and S487 (RFC 9110 §5.5/§5.6.1.2/§5.6.2/§5.6.4), both
fetched 2026-11-06T01:28Z (RFC 9111 byte-identical to the round-99 retained body; RFC 9110 retained
at `sources/rfc9110.txt`, sha256 `21c1cdce…`); the rows land only after the scout seat's re-open.

- Counter: `python3 -B .ufo/waves/round-100/c100_fresh304.py --root . --revision <REV> --work <scratch>`
  (91 hand cases, the reference agrees with all before any candidate runs; 300 generated cases,
  default seed = int(first 8 hex of the scored revision, 16)). Selftest 2/2.
- Before (base, the landed v1 blob `db3a0f12…`): `hand=72/91 generated=224/300 … met=false`, exit 1
  (`controls/base-c2.txt`) — the do-nothing control.
- Target: at the C2 content commit, `candidate=present hand=91/91 generated=300/300 met=true`, exit 0,
  and the scored sha256 equals `git show <REV>:scripts/freshen_304.py | sha256sum`.
- **Predicate (frozen):** exactly that line, exit 0, at the C2 content commit.
- **Kill rule (frozen):** any hand or generated failure at that commit → C2 unmet; no re-seeding, no
  contract or counter edit after a candidate is scored.
- Controls (pre-freeze, `--candidate-file`): positive oracle `frozen/pos-oracle.py` → `met=true`
  (91/91, 300/300); 13 single-mutation forgeries, one per v2 clause or escape class (F1 token form,
  F10 substring, LC6 case, LC8 lenient, F2 no trim, F3 keep proxy, e1-e7), all `met=false`; the
  oracle-theft forgery `frozen/neg-theft.py` (reads `/proc/<ppid>/cmdline` to load the counter's
  reference) → `hand=0/91 met=false` inside the sandbox.
- Capability row enters SCORECARD only as "met on the frozen predicate"; admission is the outside
  closure's. Contract v2 supersedes v1: the round-99 counter is expected to fail the v2 candidate
  exactly on v1's whitespace-copy and qualified-form cases; that receipt is disclosed, not hidden.

## Frontier step

Census before/after (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`;
before = `controls/census-before.txt`, rc 0, 41 W04); rows S486/S487 written only after the scout
seat's in-round re-open; one mined mistake in `corpus/lessons/round-100.md`; considerthese
2026-11-05 proposal 3 (held-out vs frozen divergence) mined as a criterion; assimilation: collision
check re-derived, adopt nothing unless a renumber map and per-entry re-grounding exist.
