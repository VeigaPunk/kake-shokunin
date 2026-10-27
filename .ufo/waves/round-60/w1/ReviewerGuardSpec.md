# ReviewerGuardSpec
round-60 w1 — Claim C2 review (append_guard.py contract vs fleet/lane append-only rules)
Reviewed: contract.md §Claim C2 (base 97cdc12); PROTOCOL.md §Gate standard; CORPUS.md "Corrections are new
entries, never rewrites" + SOURCES rule 2; corpus/QUALITY.md round-59 gate-collision criterion;
round-59-verifier-spotcheck.md §6 (R59-D1); lane history fd6303ce..97cdc12 (read-only git).

## FINDINGS:

- **HIGH — `--selftest` is named but its behavior is frozen nowhere.** PROTOCOL §Gate standard, Self-test:
  a gate "exposes a self-invocation mode over isolated fixtures (temp trees, no network, no live-tree write)
  asserting both the exit code and a stable expected finding-id, with the expected values committed". The C2
  CLI line lists `--selftest`; no contract text says what it must assert. A vacuous `--selftest` (print ok,
  exit 0) satisfies the letter of C2. The 24 cases live in the counter, and the listed "counter selftest
  controls" test the counter, not the tool's self-invocation.
  Fix: freeze in §Claim C2 — `--selftest` builds its own temp fixture repos (git init in a temp dir, no
  network, no live-tree write), asserts per-case exit **and** finding kind **and** the `files=/findings=`
  summary line, prints a tally, exits 0 iff all hold.

- **HIGH — no SKILL.md registry row is required for `scripts/append_guard.py`.** PROTOCOL §Gate standard,
  Registry + Delivery: a child lane's registry home is its own SKILL.md; "closure grades no gate conformant
  until its registry row exists". Lane convention agrees: SKILL.md registers scripts/ gates with the full
  schema (freshness-sweep :212, corpus-contract :388, canonical-audit :412, receipt-replay :538,
  accessibility-packet :556, citing-set :617 — Name | Kind | Entry command | Verdict map | Self-test |
  Pinned values | Write scope | Owner). C1's population regex (`^\.ufo/waves/round-(N)/…c(N)_…`, 48≤N≤59)
  cannot see `scripts/`, so nothing in this round catches the omission.
  Fix: C2 obligation — append_guard.py registered in SKILL.md with verdict map
  `0=clean; 1=findings; 2=could-not-evaluate; 64=usage`, self-test spelling, read-only write scope, owner kake.

- **MEDIUM — three declared exit branches have no falsifier.** Exit map: 0/1/2/64. Cases cover
  base-not-ancestor→2 (K20) and missing `--base`→64 (K21) only. Unfalsified: unresolved `--revision`→2,
  `--root` not a toplevel→2, any usage error other than one missing flag→64. A v1 tool that crashes with a
  traceback (Python exit 1 = "findings") on those inputs still scores 24/24.
  Fix: fold toplevel-violation and unresolved-revision probes into `--selftest` (v2 may add cases; 24 is
  frozen for v1).

- **MEDIUM — fenced-code-block tag visibility is underdetermined.** The rule hides a tag only "outside an
  HTML comment and outside a backtick code span". A tag inside a ``` fenced block is *visible* under the
  letter (fences are not spans); a builder that excludes fences anyway passes all 24 cases (K10 pins inline
  spans only). Reference impl and port can diverge on a plausible input.
  Fix: one frozen sentence — fences do not hide a tag (or they do, plus a case). Either is fine; pick one.

- **MEDIUM-LOW — the tool's "committed bytes only / GIT_* scrubbed / `--root` must be a toplevel" clauses
  have no falsifier among the 24.** No dirty-worktree case (worktree bytes edited, verdict must not move),
  no `GIT_DIR`/`GIT_INDEX_FILE` poisoning case, no subdir invocation. The counter's detached-clone design
  protects the measurement, not the tool's contract. Fix: dirty-worktree + env-poisoning probes in
  `--selftest`.

- **LOW — stdout contract under-pinned: `[:<line>]`, the summary line, and multi-finding ordering are
  asserted by no case** (cases assert exit + kind + path only). A summary-line liar — the exact `tally_liar`
  shape R59-D3 routed for P6 — passes 24/24. Fix: `--selftest` asserts the summary; w2 may pin ordering.

- **LOW — deleted clause variants unexercised:** rule says "not a regular blob there (symlink, submodule,
  tree)"; K18 covers symlink only, a path turned into a directory/submodule is untested. Fix: v2 candidate.

- **LOW — scope boundary vs SOURCES rule 2 should be stated, not implied.** Default scope is
  `corpus/knowledge/**/*.md`; `corpus/SOURCES.md`'s own rule-2 discipline (only `status`/`recheck`/`used-by`
  in place, each logged old→new in the round lesson) is outside the guard by design. Also rule 2's
  "logged old→new in the round lesson" half has no analog in the C2 rule — a bare tagged run is accepted
  with no lesson-log requirement; that stays reviewer-checked per the contract's own "does not test:
  whether a tagged run is faithful". Fix: the SKILL.md row (finding 2) names the scope boundary so the tool
  is not read as a fleet-wide append-only enforcer.

- **Rule-coherence check (no defect):** C2 operationalizes CORPUS.md "Corrections are new entries, never
  rewrites" correctly for knowledge entries — base lines immutable (K4/K5/K12/K13/K14 pin `changed` on any
  byte/line alteration or deletion = "never rewrites"), corrections enter as new inserted lines (K2/K15 =
  "new entries"), matching the in-repo tag practice (`[r59-correction 2026-10-27]` at
  crawler-identity.md:35, the `[r20 …]` marker convention in SKILL.md:111). The rule's kind split is
  coherent: `changed` reserved for B-not-subsequence, `untagged_insertion` when B matches but no tag-valid
  alignment exists — K3 vs K4 and K16 pin that boundary. The tag regex correctly matches through the `**`
  wrapper of the real round-59 tag, and R1 catches a span-naive impl that disables a tag because a backtick
  appears later in the line.

- **R1 fairness — VERIFIED FAIR (run, not inferred):** `git merge-base fd6303ce 97cdc12` = fd6303ce
  (evaluable); `git diff --name-status` over `corpus/knowledge/` in the range shows exactly three paths —
  A crawler-identity-signals.md, M crawler-identity.md, A googlebot-verification.md; the two additions are
  "paths new at revision" (unchecked). The single in-place path diffs 16 added / 0 deleted lines
  (`--numstat`), one contiguous run after base line 34, first line
  `  **[r59-correction 2026-10-27]** The claim in the bullet above is wrong as stated: …` — tag visible
  (no comment/span around it), non-EOF run → rule accepts, expected 0 reachable. c55's `head_changed`
  ("full base text … byte-for-byte as a prefix") does break on it, so R1 demonstrates exactly the R59-D1
  delta, and the counter's c55-port control (must fail K2, K15, R1) pins the contrast from both sides.
  QUALITY round-59 gate-collision criterion satisfied for c55: the a2r1 commit records the `historical`
  marking, and the contract names the collision (R59-D1 → C2).

- **Gate-liveness check (no defect):** the tool can fail (exit 1) and is shown failing on realistic input
  (K3-class, R2 real-lane byte change) — a gate, not a probe. Exit classes map onto the fleet vocabulary
  (0 clean / 1 failed / 2 could-not-evaluate / 64 usage declared). Counter commits land only in its own
  scratch fixtures (K-cases, R2 clone) — lane git/jj untouched, consistent with seat bounds.

## Residual risk
- Tag faithfulness, lesson-log coupling, and SOURCES.md rule-2 discipline remain outside the guard
  (reviewer/critic-checked by design).
- Fenced-block semantics and the three unfalsified exit branches are the likeliest w2 attack surfaces.
- [INFERENCE] `corpus-contract.mjs`/census continue to guard SOURCES.md structure; I did not re-verify that
  here — outside this claim.

VERDICT: C2 is well-formed and R1 is verified fair on the real lane; freeze `--selftest` semantics and require the SKILL.md registry row (plus fenced-block disposition) before the counter is frozen.
