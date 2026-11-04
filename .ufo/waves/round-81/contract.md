# kake round 81 — frozen contract

Frozen before any round-81 seat ran. Base measured revision
`2e11925500dd5a739376c9108c94616243af0cd4` (lane `master` tip at round open, 2026-11-04).
Attempts: 1. Shape: one v1 wave, band 8–16 seats (`ufo-wave-policy.json`,
`waveMinLanes 8`, `waveMaxLanes 16`), ≥25 % attack seats (reviewer, critic,
mutation-tester, labrat — the run-15 directive's role list; sentinel is **not** an
attack role).

Axes: the lane owns **operability 10**, **freshness 10** and the round-54
evidence-backed sub-axis **calibration 2**. Calibration is the lowest non-retired
axis, so C1 works it; the saturation line is 10/10 and the stagnation window is 1
completed round, so the nudge is *not* needed for C1 but the round still carries a
capability (C2) as §AXES requires when a capability has not entered recently.

Motivating evidence:

- `corpus/lessons/round-80-verifier-spotcheck.md` §6 routes six defects
  (R80-1 … R80-6) at the round-80 report, lesson and evidence chain.
- That same spot-check re-ran both round-80 counters and agreed with them, so the
  defects are accuracy/accounting/evidence-reproducibility items, not claim
  failures. Round 81's calibration move is to make each of them decidable from
  bytes by a committed instrument instead of by a sentence.

## C1 — calibration: the round-80 routed-defect queue closes

**Population.** The six items the non-author round-80 closure filed in
`corpus/lessons/round-80-verifier-spotcheck.md` §6: R80-1, R80-2, R80-3, R80-4,
R80-5, R80-6. No item is added or dropped after data.

**Frozen predicate.**

    met <=> open == 0

where each item is *open* unless its condition below holds at the measured
revision, decided from bytes by
`.ufo/waves/round-81/c81_defect_queue.py --root <tree> [--revision <rev>]`.
The counter never reads a word that merely says "closed".

**Item conditions (frozen).**

| Item | Closed when |
|---|---|
| R80-1 | The S453 row of `corpus/SOURCES.md` sits at line **L** at the measured revision, and `corpus/lessons/round-81.md` carries an `R80-1` correction row naming `corpus/SOURCES.md:L` for `S453`. The counter computes L itself, so a pointer that drifts with the registry opens the item again. Filed bytes are never rewritten. |
| R80-2 | `corpus/lessons/round-81.md` carries an `R80-2` correction row containing the numbers the counter re-derives from `.ufo/waves/round-80/controls/ctl-c80-constants.txt`: `constants_failed=<a>/<b>`, the summed case-level failures `<n>/<slots>`, and `const_echo` `<e>/<t>`. A receipt the counter cannot parse opens the item. |
| R80-3 | `corpus/lessons/round-81.md` carries an `R80-3` correction row containing `rfc9110.txt rows=<n>` and `rfc9110.html rows=<m>` where n and m are counted by the counter over the registry's `source` cells at the measured revision. |
| R80-4 | Round 81's own wave settles with a **settled** attack share ≥ 0.25 over the directive's attack roles {reviewer, critic, mutation-tester, labrat}, and `.ufo/waves/round-81/w1-accounting.json` re-derives from `.ufo/waves/round-81/w1-spec.json` and `w1-results.json`: `attack_roles`, requested/settled totals, the share, and the spec's sha256. |
| R80-5 | `.ufo/waves/round-81/junk_tree_build.py` rebuilds round-80's junk control tree from `.ufo/waves/round-81/junk-tree.json` deterministically (two runs, identical file set and digests), and round-80's own counter over the rebuilt tree prints `open=5 closed=1 met=false`, exit 1. |
| R80-6 | `scripts/wave_seat_record.py` re-derives `.ufo/waves/round-81/seat-failures.json` from round-81's `w1-results.json` + `w1-spec.json`, the committed file equals the re-derivation canonically, every seat carries `role`, `status`, `exit`, `error`, and the record names the results-schema limit. |

**Counter.** `.ufo/waves/round-81/c81_defect_queue.py`, `--selftest` must print
`selftest: N/N passed` and exit 0; the selftest builds a green fixture where all
six items close and six mutants (one per item) where each item opens, so no
conjunct is satisfiable-only-on-paper.

**Controls (committed before the after-state).**

- `controls/base-c81-defect-queue.txt` — the counter at the base revision: `open=6 met=false`, exit 1.
- `controls/ctl-c81-junk-queue.txt` — a junk tree that fabricates closure in words:
  it must still report `open>0`, `met=false`, exit 1.
- Kill rule: if the base control or the junk control reports `met=true`, the
  counter is wrong and the claim is not scored.

**Do-nothing control (§9).** A round that skips every claimed action is exactly the
base tree: all six items read open there. A round that rewrites the round-80 report
in words and adds nothing decidable also fails, because every condition reads
lane bytes the report cannot forge (registry line numbers, receipt arithmetic, a
re-run of round-80's counter, a canonical record re-derivation).

## C2 — operability: a fresh domain capture feeds the offline audit chain and the verdict re-derives from committed bytes

**Claim.** The lane takes a fresh GET-only capture of three real surfaces of its
primary property (`https://ds4cc.com/`, `/robots.txt`, `/sitemap.xml`) this round,
records the receipts under `.ufo/waves/round-81/capture/`, and audits them offline
with `scripts/header_audit.py` through a version-1 manifest whose expectation
classes are grounded in `corpus/knowledge/response-header-expectations.md`
(S430–S433) and the new S454 status-semantics row. A committed counter re-derives
the whole chain: receipt digests, byte counts, fetch time, surface allowlist, and
the audit's own output.

**Frozen predicate.**

    met <=> surfaces >= 1
          and every receipt verifies (sha256 of the retained body, byte count, integer status
              in 100..599, RFC 3339 fetch time on or after 2026-11-04T00:00:00Z, GET, not truncated,
              URL host in the manifest's declared allowlist)
          and header_audit over the committed manifest exits 0 or 1 with `checks=<surfaces>`
          and the audit's stdout equals the committed audit receipt byte-for-byte

**Counter.** `.ufo/waves/round-81/c81_capture_audit.py --root <tree> [--revision <rev>]
[--work <dir>]`. `--selftest` must print `selftest: N/N passed` and exit 0, with one
green fixture and five mutants (body digest, byte count, stale fetch time, drifted
audit receipt, empty manifest), each of which must open the item. Measurement is
**offline**: no network at measurement time; the capture happens once, during the
round.

**Controls (committed before the after-state).**

- `controls/base-c81-capture-audit.txt` — the counter at the base revision (no
  round-81 capture): `met=false`, exit 1.
- `controls/ctl-c81-tampered-capture.txt` — a copied capture with one body byte
  flipped: the counter must report the digest mismatch and `met=false`.

**Kill rule.** If the base control reads `met=true`, or the tampered control reads
`met=true`, the counter is wrong and the claim is not scored.

**Capability row.** On `met=true` the capability "capture-once, audit-offline
re-derivation chain" enters `SCORECARD.md`'s capabilities table with this counter
and its receipts.

## Sources

New row **S454** (RFC 9110 §15.5.4/§15.5.5, status semantics for an absent
resource) is admitted this round only if a seat opens it, records HTTP status,
final URL, bytes, sha256, a retained body and a located ≤25-word quote; **S433**
(RFC 9110 field-line and Content-Type sender rules) is re-opened this round with a
fresh access date and the `recheck`/`used-by` change logged old→new in the round
lesson. C2's manifest cites S433 and S454; a C2 that lands without a mined row
opened this round fails §2b's sourced-claim requirement.

## Terms that do not change

Predicates, item conditions, the kill rules and the case populations are frozen
here. An amendment may only clarify a term the counter cannot evaluate; it is
written before any after-state, dated, and recorded in the round lesson. A rule
changed after a seat has scored is not this claim's rule.
