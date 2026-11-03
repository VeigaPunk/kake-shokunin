# CriticCoupling — round 72, kake, w1

Base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`. Freeze `a19d38ea`. Read-only on the lane; scratch under
`/fast/scratch/hyaku/kake-r72/CriticCoupling/` (removed before yield). No tools installed.

## Verdict

- **separable = yes** (with two notes: the c71 leg of the J3 control depends on being rebuilt from base; the frozen
  J3 script cannot print the `c72_exit=` line it documents — see F1).
- **sourced = no** (at present). C2 cites S439, the quote's substance is in the retained page, but S439 is not in the
  registry, the retained page has no receipt row, and the located quote is not a raw substring. Becomes yes only when
  the ScribeSources row lands with a receipt and a raw-substring quote (F2).
- **routing = right** (the three dangling ids are unfixable in-lane under the id rule and the append-only guard; the
  round states the gate stays red and does not claim it green). One note: the withdrawal branch in QUALITY.md:1115 was
  not considered in the lesson (F5).

## Findings

**F1 — blocking (receipt reproduction as written), routed to L1.**
`controls/j3-control.sh` runs under `set -eu`. The c72 call exits 1, so the script aborts before
`echo "c72_exit=$?"`. The contract's counting command says it prints `c71_exit=0` and `c72_exit=1`; it prints only
`c71_exit=0`. The script's own exit is 1, which is the c72 result, but the `c72_exit=1` line is never printed.
`controls/c2-j3-control.txt` contains a wrapper line `j3_script_exit=1` instead. The substantive exit codes reproduce;
the receipt as written does not. Disposition: L1 states in the report that c72's exit is taken from the script's exit
status (or from a wrapper), because the frozen script cannot change in-round.
- Evidence: `sh .ufo/waves/round-72/controls/j3-control.sh` → stdout ends at `c72 ... met=False`, script exit `1`;
  no `c72_exit=` line. Receipt `controls/c2-j3-control.txt` line 7 = `j3_script_exit=1`.

**F2 — blocking for the frontier rule, routed to ScribeSources / L1.**
- S439 is absent from the registry at base (`git show 3c68645a:corpus/SOURCES.md | grep -c S439` → 0), at the freeze
  commit (0), and in the working tree (0). That is expected before integration; the row is the ScribeSources draft.
- `sources/receipts.json` lists only `crux-vis.html` and `crux-api-probe.json`. `sources/gitcli.html` has no receipt
  row (`grep -c gitcli receipts.json` → 0): no URL, status, bytes, or sha256 is recorded. The file's sha256 is
  `4e1ea3a5951e10f5c31157d1b03e0938d9b09130c5db099aa5baec6a02714a1e`, mtime 2026-11-03T18:49:05-03:00. The page bytes
  do not carry the URL (only `<title>Git - gitcli Documentation`). The row's URL and access date must come from the
  fetch record, which does not exist in the tree.
- Quote check (`grep -F -c --`): `You can use --end-of-options for this` → **0** raw matches. The raw bytes are
  `You can use <span class='synopsis'><code>--end-of-options</code></span> for this` (`--end-of-options</code></span>
  for this` → 1). A ≤25-word quote cited as plain text is not a raw substring of the retained page. The row must quote
  the tag-split bytes or another raw span (`Because -- disambiguates…` also → 0 raw matches).
- C2's predicate does not depend on S439 (the counter's behavior is measured), so the frontier rule is carried only by
  the source citation. The rule is met only when the row lands with URL, access date, receipt row and raw quote.

**F3 — note (separability), no action needed for the claim as frozen.**
Scratch clone, base `3c68645a` plus the C1 relabel patch `.ufo/waves/round-72/w1/c56-relabel.patch` (applies clean,
commit `d86d2b91`, touches only SKILL.md row c56 line 1253; no `/tmp` token in the patch):

| check | base 3c68645a | cc6b (r71 base) | C1-only tip d86d2b91 | J3 on base | J3 on C1-tip 7e59a7f9 |
|---|---|---|---|---|---|
| c72 counter | exit 0 (met) | exit 1 | exit 0 (met, removed=8 added=8 guard ok) | exit 1 | exit 1 |
| c71 counter | exit 0 | — | **exit 1 (guard=fail)** | exit 0 | exit 1 |

- Selftest `c72_tmp_v2.py --selftest` → exit 0, `11/11` (with and without C1; the selftest has no SKILL.md input).
- C2 receipts therefore reproduce with the C1 edit absent and present for c72 (the claim's counter). Separable: yes.
- The c71 leg is not separable from SKILL.md edits: any later SKILL.md edit reddens c71 (guard=fail), as the c72
  docstring says. The frozen J3 control stays green for c71 only because the script rebuilds from the `BASE` constant
  `3c68645a`, not from the tip. If the control is ever rebuilt from a tip that carries the C1 edit, the c71 leg fails.
  The lesson says c71 "re-reddens ... recorded in the r72 lesson", but `grep -c 're-reddens' corpus/lessons/round-72.md`
  → 0. Add the sentence (note).
- C1 is not coupled to C2's freeze files: `c66_gate_status_hostportable.py --root <clone> --revision a19d38ea …
  --jobs 6` → exit 0, `members=28 evaluated=28 mismatches=4 structural=0 agreement=24 met=True`; base
  `3c68645a` gives the same line (exit 0). The freeze commit's c66 run keeps the 28-member population with
  `structural=0`, so the round-72 counter does not enter the population (cause not traced; observed only).

**F4 — note, mistake classes (M1–M3) checked.**
- M1 (adoption residue, dangling ids) — **real**. `scripts/id_resolver.py --root <clone> --revision 3c68645a` →
  `DANGLING S303/S304/S352 cited-by=corpus/knowledge/crux-bigquery-origin-membership.md owners=- url-match=-`,
  `ids_cited=121 ids_resolved=118 dangling=3`, exit 1. Citations at base: the entry lines 11 and 43. Registry rows for
  S303, S304, S352: 0. Class "adoption residue" is correct; the round-70 closure did not run the resolver.
- M2 (vacuous counter, r71 C2) — **real**. c71 exit 0 on the J3 control (`controls/c2-j3-control.txt`; reproduced
  here, `c71_exit=0`). The counter accepted a command-bearing `/tmp` line annotated only with the phrase. Class
  "counter accepted a bad control" is correct.
- M3 (pre-freeze diagnosis) — **real but a process caveat, not an output defect**. `controls/c1-base.txt` and the C2
  base receipts are committed in the freeze commit and were produced before the freeze; the contract discloses it.
  It is classed as a mistake in the lesson table; that is acceptable if the table says it has no code fix.
- Missed mistakes (candidates for the lesson, not in the table): **M4** the frozen J3 control's receipt is not
  reproducible as written (F1); **M5** the S439 source has no receipt row (F2). Both are receipt-integrity defects of the
  same class as the round's C2 claim.

**F5 — note, routing.**
Routing the three dangling ids to L0 is the right disposition, and the round stopped at an honest partial for the
gate (c57/c58/c59 red, named non-goals). Reasons, checked against the text:
- id rule: `CORPUS.md:89` — `id` is "S + 3 or more digits, the next unused; never reused." S303, S304, S352 are not
  next-unused (S439 is). Registering them under those ids breaks the rule.
- append-only guard: `scripts/append_guard.py` requires every base line to survive as a subsequence; only end-of-file
  or tagged `[rNN-correction YYYY-MM-DD]` insertions are allowed. In-place edits to the three lines are blocked.
- resolver: `id_resolver.py` scans every body `S###` outside HTML comments and fences. No insertion can clear the body
  citations.
- So no in-lane edit can clear `dangling=3` while keeping the rules. An operator decision (an exception to the id rule,
  or a body-edit exception to the guard) is required.
- Note: QUALITY.md:1115 names a second, in-lane disposition for an unsupported citation — "withdrawn by an append-only
  correction". The guard permits an EOF append, so the knowledge claim could be corrected in-lane, while the resolver
  stays red. The lesson rejects only the in-place rewrite and the registration; it does not consider the withdrawal
  branch. Record it as considered-and-not-taken (or taken) so the operator sees the full set.
- Citation slip: the lesson cites "CORPUS.md rule 2" for next-unused; rule 2 is append-only. The id rule is the `id`
  definition at `CORPUS.md:89`. Fix the citation (note).

**F6 — note, wave conformance (checked against `w1-spec.json`, `w1-plan.json`, `w1-dispatch.json`, policy files).**
- Seats: 15 (`plan.counts.spawn=15`, `registry.members`=15, spec items=15).
- Roles: scout 3, executor 2, scribe 2, reviewer 2, critic 2, connector 1, mutation-tester 1, sentinel 1, revenger 1.
  `revenger` is in `proposalRoles` of `scripts/hyaku/ufo-wave-policy-v2.json` and `ufo-wave-policy.json`.
- Attack share: reviewer 2 + critic 2 + mutation-tester 1 + sentinel 1 = 6 of 15 (40 %). Matches.
- Connector: 1 (ConnOverlap). Matches.
- Band: policy `minLanes 8`, `waveMinLanes 8`, `waveMaxLanes 16`; `maxLanes 15` in the spec. Within band.
- Planner: absent from spec and dispatch. The policy's `planner` role is count 1, held by the L1 (`w1.ready`: `l1:KakeR72`).
- One v1 wave: `wave: kake-r72-w1`; dispatch note says one batched task call. Matches.
- `w1.ready.partial` existed at `ls` time and was gone at the next read (replaced by `w1.ready.dispatched`). Not a
  conformance issue.

## Evidence commands (exit codes)

All run in scratch clones or on committed bytes; no lane mutation.

- `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` → exit 0, `11/11`.
- `c72_tmp_v2.py --revision 3c68645a…` → exit 0 (met=True). `--revision cc6b4e0b…` → exit 1. `--revision d86d2b91…`
  (C1-only) → exit 0. `--revision 7e59a7f9…` (J3 on C1 tip) → exit 1.
- `c71_tmp.py --revision 3c68645a…` → exit 0. `--revision d86d2b91…` → exit 1 (guard=fail). `--revision 7e59a7f9…` → exit 1.
- `sh .ufo/waves/round-72/controls/j3-control.sh` (with `HYAKU_SCRATCH` set to scratch) → script exit 1; output has
  `c71_exit=0` and no `c72_exit=` line (F1).
- `c66_gate_status_hostportable.py --root <clone> --revision a19d38ea… --jobs 6` → exit 0, agreement=24, members=28,
  structural=0. `--revision 3c68645a… --jobs 6` → exit 0, agreement=24, mismatches=4.
- `id_resolver.py --root <clone> --revision 3c68645a…` → exit 1, dangling=3 (S303, S304, S352).
- `grep -F -c -- "You can use --end-of-options for this" .ufo/waves/round-72/sources/gitcli.html` → 0;
  `grep -F -c -- "--end-of-options</code></span> for this" …` → 1.
- `git ls-remote origin refs/heads/master` → exit 0 (not used for a finding).

## Counterexample (for F1/F2)

- F1: the frozen script's own transcript shows `c71_exit=0` then the c72 counter output, then nothing; the claimed line
  `c72_exit=1` is absent.
- F2: a row that quotes `You can use --end-of-options for this` would fail the raw-substring check against the
  retained page (0 matches).

## Tooling

No tools installed or upgraded. Scratch tree removed before yield (`ls` shows no `CriticCoupling` directory).
