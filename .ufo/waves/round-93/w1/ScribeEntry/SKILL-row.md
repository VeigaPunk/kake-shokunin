# ScribeEntry — draft SKILL.md registry block (round 93 C2)

**Status: DRAFT. Not landed. `SKILL.md` was not edited by this seat** — the L1
(`KakeR93`) owns `LANE/SKILL.md` this wave because `ExecC1Fixes` is repairing
the six E5 dangling paths in it. The L1 appends this block after
`ExecC1Fixes` lands.

## Exact anchor

Append a **new section** at the **end of the file**, after the current last
line of `SKILL.md` — the round-92 section's closing paragraph, which ends
"...L1's re-run at the landing revision is what counts." (today that is line
1680, the last line of the file; `wc -l SKILL.md` → 1680).

Do **not** insert into the round-92 table. The round-92 section owns the
round-92 rows; round 93 gets its own `## Round 93 — ...` section with its own
table, in the same shape as the round-91 and round-92 sections immediately
above it (`## Round 92 — heuristic freshness decision and the round-91
instrument repairs`, which begins at line 1649 with prose, then a table with
the header `| Name | Kind | Entry command | Verdict map | Selftest | Pinned
values | Write scope | Owner |`, then a `**How to verify.**` line, then a
closing "Two limits worth carrying" paragraph).

The block below is that section, verbatim and ready to append.

---

## Draft block (append verbatim)

```markdown
## Round 93 — conditional request evaluation decision

`corpus/knowledge/conditional-request-evaluation.md` (S471–S476, RFC 9110
§13.2.2, §13.1.1–§13.1.4, §8.8.3.2 incl. Table 3; RFC 9111 §4.3.2) supplies
the conditional-request decision: given a supplied current representation and
supplied precondition field values, which status a recipient would answer
with. The probe answers one question over caller-supplied values: `200`,
`304` or `412`, and which precondition decided it. No clock, no HTTP-date
parsing (the dates are integer epoch seconds, the lane's adapter convention
shared with `scripts/stored_reuse.py` and `scripts/heuristic_freshness.py`),
no network, no cache store, no validator generation, no storage, freshness,
serving or forwarding decision, and no claim about any live CDN, Pages front
or Render service. The C2 counter is a new frozen instrument that scores the
candidate against the round-93 contract v1 and requires the six frozen forgery
subjects to be refused while the frozen positive control is admitted; it does
not repair the round-92 counters.

| Name | Kind | Entry command | Verdict map | Selftest | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| conditional_eval.py | probe | `printf '%s' '<payload>' \| python3 -B scripts/conditional_eval.py` with stdin JSON `{method,current:{exists,etag,last_modified},request:{if_match,if_none_match,if_modified_since,if_unmodified_since},role?}` | 0 clean/decided (stdout `{"decision": "200"\|"304"\|"412", "precondition": <name>\|null}`); 1 failed/`invalid_input:` on stderr with empty stdout; a decision is not a storage decision, a freshness decision, a revalidation exchange, a serving or forwarding permission, or any live property's behaviour | `python3 -B scripts/conditional_eval.py --selftest` → `selftest <n>/<n>` over its own in-memory fixtures | contract `.ufo/waves/round-93/c2-contract.md` (v1, clauses 1–12); vocabulary `200` / `304` / `412`; precondition names `if_match` / `if_unmodified_since` / `if_none_match` / `if_modified_since` / `null`; If-Match uses the strong comparison function and If-None-Match the weak one (RFC 9110 §8.8.3.2 Table 3); `role: "cache"` skips If-Match and If-Unmodified-Since (RFC 9111 §4.3.2); dates are integer epoch seconds, never HTTP-dates | stdin/stdout/stderr only; writes nothing | kake |

**How to verify.** `python3 -B .ufo/waves/round-93/c93_conditional.py --root . --revision <rev> --work <explicit-scratch>` must print `candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok met=true`, exit 0 (exit 1 on any failed conjunct, exit 2 on reference or hand-case drift before any candidate is scored, on an unresolved revision, or on argparse usage); and `python3 -B scripts/conditional_eval.py --selftest` must print a final `selftest <n>/<n>` line, exit 0.

Two limits worth carrying beside this row. The C2 gate scores the *contract*,
not the RFC: its 44 hand cases and its 120-case seeded generated population
were written by the same round as the contract, so `met=true` is conformance to
contract v1 and never evidence about a deployed server's behaviour; the same
applies to the C1 gate over its own battery, whose fixtures the same round
wrote. And the C2 gate's `anti_table` conjunct is a substring screen over the
six forgery file stems and the hand-case input digests, so a legitimate
candidate that merely quoted a stem in prose would be refused — a designed
false-positive, not a defect. At the time these rows were written
`scripts/conditional_eval.py` was not yet a LANE commit, so the C2 gate at
HEAD read `candidate=absent … met=false`; the `met=true` line at the carrier
is the C2 seat's receipt and L1's re-run at the landing revision is what
counts.
```

---

## Notes for the L1

1. **The `S471`–`S476` ids are computed, not observed.** The round-93
   `ScribeSources` seat has not written `.ufo/waves/round-93/w1/ScribeSources/rows.append.md`
   yet, so there is no declared id list to read. The highest existing id in
   `corpus/SOURCES.md` is `S470` (verified in the working tree and at `HEAD`),
   and the dispatch item's anchor order gives the six rows: 13.2.2 precedence,
   13.1.1 If-Match strong comparison, 13.1.2 If-None-Match weak comparison,
   13.1.3 + 13.1.4 ignore rules (one row), 8.8.3.2 comparison table, RFC 9111
   4.3.2. So `S471`…`S476` in that order. **If the sibling's
   `rows.append.md` lands with a different count or order, its order wins and
   the `S471`–`S476` range in the draft block above and in the knowledge
   entry's `source:` line must be corrected to match.** Two independent
   derivations (this seat's, and a peer seat's) produced the same list, but
   both are derivations from the dispatch item, not from the sibling's file.

2. **E5 dependency.** This row names `scripts/conditional_eval.py`, and the
   E5 class of the C1 counter requires every repo-relative path named inside
   a `SKILL.md` table row to exist **at the measured revision**. The tool is
   currently untracked (`git status` shows `?? scripts/conditional_eval.py`),
   so the row is an E5 mismatch until the tool is committed at the carrier.
   `ExecC2Tool` owns that file.

3. **E3 dependency.** The knowledge entry's `source:` line names `S471`–`S476`.
   The E3 class requires every `S<digits>` id on a knowledge entry's `source:`
   line to resolve to a row id in `corpus/SOURCES.md` at the measured
   revision. Until the L1 appends those rows, the entry is an E3 mismatch.
   Both dependencies clear together when the L1 appends the rows and commits
   the tool.

4. **The `Write scope` cell is prose, not a path** — "stdin/stdout/stderr only;
   writes nothing", the exact shape of the round-92 probe row. An earlier
   draft of this cell named the seat's own wave directory
   `.ufo/waves/round-93/w1/ScribeEntry/`, and the E5 class flagged it: E5
   resolves each named path with `git show <rev>:<path>`, which **fails for a
   directory** even when the directory exists at the carrier. Measured in the
   scratch clone: that draft produced `E5=1 … names missing path
   .ufo/waves/round-93/w1/ScribeEntry/`; the prose cell produces no E5
   finding. Do not name a directory in any table row.

5. **Counter line-shape check.** The C2 counter's receipt line is
   `C2v93 revision=<sha> candidate=present hand=H/H generated=G/G
   forgeries_refused=F/F positive=admitted|refused anti_table=ok|hit
   population=ok|drift seed=<n> met=true|false`. The `**How to verify.**`
   line above quotes the freeze's declared target reading
   (`candidate=present hand=44/44 generated=120/120 forgeries_refused=6/6
   positive=admitted anti_table=ok population=ok met=true`), which is what
   the freeze states the counter prints at the carrier; the `C2v93 revision=`
   prefix and the `seed=93` suffix are on the same line and are not quoted,
   matching the round-92 row's style of quoting the conjuncts.
