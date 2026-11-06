# ScribeLesson — round-99 mistake mining, the considerthese proposal, and the Gate skeleton

Seat: ScribeLesson (scribe, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (`LANE`).
Round base `cde408e5817bf1376c701d8decc5469fa82b2985`; instruments
`2345e309640adac6c36e41eca87409085ba3a276`; freeze `ab35eacebf922f4f598237590f0220d63111dc94`;
C1 repair `9d341d1b46f16dbfbb41af75dd6d4966808dfa5d`; lane tip at this seat's last read
`7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916` (`git -C LANE rev-parse master`; the tip moved twice
during this seat's work, so every pointer is quoted from committed bytes).

**Counts.** `mistakes` = rows in the `## Mistakes` table (4). `proposal` = the QUALITY criterion id
this round adds (**R99-A**). `gate_rows` = rows in the `## Gate` section (3): S484 admit, S485
admit, and the merge/kake package reject.

## Deliverables

- `.ufo/waves/round-99/w1/ScribeLesson/lesson-draft.md` — **the deliverable the seat item names**:
  the `## Mistakes` table (4 rows), the `## Gate` skeleton (S484 + S485 admits, the merge/kake
  reject), the QUALITY criterion **R99-A**, the "Not mined, and why" list, the routes to round 100,
  and the open items this seat does not close.
- `.ufo/waves/round-99/w1/ScribeLesson/frontier_first_named.py` — the draft check command for R99-A.
- `.ufo/waves/round-99/w1/ScribeLesson/diagnose_unlisted.py` — the read-only per-tool diagnosis that
  re-uses the **frozen** counter's own rule helpers.
- Receipts in the same directory: `receipt-c1-base-reproduce.txt`,
  `red-control-A-count-accuracy.txt`, `red-control-frontier-map.txt`,
  `diagnose-unlisted-base.txt`, `diagnose-classes.txt`, `frontier-derived.txt`, `frontier-refs.txt`.
- This report is written twice, byte-identically, at `.ufo/waves/round-99/w1/ScribeLesson.md` (the
  trailer path the brief names) and at `.ufo/waves/round-99/w1/ScribeLesson/ScribeLesson.md` (inside
  this seat's own directory). Both are untracked files under `w1/` written by this seat only.

Everything here is a **draft for the L1**. No corpus file, counter, contract, ledger or registry was
edited by this seat; no C1 or C2 verdict is asserted; nothing was committed, pushed, published or
deployed; no other runtime was invoked.

## Frozen digests verified before use

`sha256sum` against `.ufo/waves/round-99/controls/instrument-sha256.txt` — **all 11 entries match**
(the 3 named instruments read directly; the 8 `frozen/` subjects are the counter's own subjects and
were not modified):

| file | pinned | observed | result |
|---|---|---|---|
| `c99_registry.py` | `0f39bbbcd73bc032374848601c85f2228abab749f7e92c3ca15603dbbb642351` | same | match |
| `c99_fresh304.py` | `d13bba5d6b663b171ab57d42b5ec054b5f73d8deb8f9fd64f14adad455b6bc4b` | same | match |
| `fresh304-contract.md` | `2be46b4d8dcc57539b0a45e2e3b7b57e76cb1c4e570891e8cdea88c5ebbba2a6` | same | match |

The two retained source bodies were hashed independently: `sources/rfc9111.txt` =
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (84 477 bytes, matching the
freeze's stated `aeb52adb…`) and `sources/eid9185.html` =
`83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3` (10 655 bytes). **No frozen byte
was touched.**

## Re-derivations run by this seat (read-only against the lane)

| receipt | command | observed rc / line |
|---|---|---|
| `receipt-c1-base-reproduce.txt` | `python3 -B .ufo/waves/round-99/c99_registry.py --root . --revision cde408e5817bf1376c701d8decc5469fa82b2985 --work <scratch>` | rc=1, `tools=54 rows=124 listed=28 unlisted=26 dangling=0 exec_fail=1 mismatches=26 met=false` — byte-identical to committed `controls/base-c1.txt` apart from the trailing `exit=1` line, which the reproduction prints as `rc=1` |
| `red-control-A-count-accuracy.txt` | `grep -c .` over each committed assimilation receipt vs the count each lesson quotes | r96 lesson quotes **217**, its cited receipt holds **216**; r98 lesson quotes **218**, the round-99 receipt holds **220** (delta `S482`, `S483`) |
| `diagnose-unlisted-base.txt` | `python3 -B .ufo/waves/round-99/w1/ScribeLesson/diagnose_unlisted.py --revision cde408e58…` (imports the frozen counter and re-uses its `tables`/`cells`/`SPAN`/`names_path`/`verdict_ok`) | 26 tools classified into 4 sub-classes: **11** with no row mentioning them, **13** with a near-miss row failing exactly one rule (7×R2, 3×R3, 2×R5, 1×R5-on-two-rows), **1** (`robots_audit.py`) passing R1–R4 and failing only at R5's execution |
| `diagnose-classes.txt` | the same run, tabulated | histogram `{no_row: 11, R2: 7, R5: 2, R3+R5: 3, R2+R5: 2, R5-exec: 1}` |
| `red-control-frontier-map.txt` | `python3 -B .ufo/waves/round-99/w1/ScribeLesson/frontier_first_named.py --root <lane>` | positive control rc=0 `named_open=4 map_rows=4 missing=0 wrong=0 met=true`; negative 1 (row deleted) rc=1 `missing_open_ground 4.3.4`; negative 2 (first-named moved later) rc=1 `wrong_first_named 4.3.4 map_says_r97 first_named_r93`; negative 3 (section removed) rc=1 `map_rows=absent`; lane tip rc=1 `map_rows=absent missing=4` |
| `frontier-refs.txt` / `frontier-derived.txt` | section-ref sweep over `SCORECARD.md`'s `Planned — after round N` sections | 4 grounds named open: `15.4.5` and `4.3.4` first named in **r93**, `4.3` and `4.1` first named in **r95**; `corpus/README.md` has no `## Open frontier` section |
| — | `python3 -B scripts/robots_audit_selftest.py '[--tool' 'PATH]'` vs `python3 -B scripts/robots_audit_selftest.py` (scratch extraction of the base tree) | bracketed form **rc=2**, plain form **rc=0** — this is the counter's `exec_fail 1104 scripts/robots_audit.py rc=2` |

## Findings

1. **Mistake row 1 — registry drift, and it is four classes, not one.** The 26 unlisted tools are
   not 26 missing rows. **11** tools have no row mentioning them at all; **13** have a near-miss row
   that fails exactly one of the counter's R1–R5 rules — 7 on **R2** (the entry cell names the tool
   by a *different label*, e.g. `scripts/citing_set.py` registered as `citing-set` at
   `SKILL.md:628`), 3 on **R3** (verdict map does not map both 0 and 1), 2 on **R5** (no usable
   self-test span), 1 on R5 across two candidate rows; and **1** (`scripts/robots_audit.py`) passes
   R1–R4 and fails only at R5's *execution* — its self-test span
   `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` is not runnable as written (the
   bracketed placeholder is not the counter's `<placeholder>` form, so it reaches the tool as the
   literal argv `'[--tool' 'PATH]'`, rc=2). **A successor that only asked "is there a row mentioning
   this tool?" would call 15 of the 26 green.** Routed R99-4.
2. **Mistake row 2 — population drift.** The round-96 lesson quoted "217 registry ids" while the
   receipt it names holds 216; the round-96 closure flagged it as a "count-accuracy note" and routed
   it as prose, so it was never mined and the round-98 lesson repeated the shape one round later.
   Nothing binds a cited count to the revision it was measured at. Routed R99-1.
3. **Mistake row 3 — review-conjunct collapse.** Round 98's C1 conjunct ran on one live reviewer
   (`ReviewCapA` produced no files); the failure was carried as a route, and the r98 report never
   named that the second reviewer was dead. Round 99's freeze closes the *verdict* ("Both review
   seats dead or verdict-less → unmet"); the *report's disclosure* is still open. Routed R99-2.
4. **Mistake row 4 — duplicate registry rows, a class this round's own repair created and the
   frozen counter cannot see.** The repair adds 26 rows without superseding the older rows naming the
   same tools, so **16 of the 26 repaired tools are named by two or more rows** at the repair commit
   (`robots_audit.py` by four). The counter computes `listed` as a *set* and
   `mismatches = unlisted + dangling`, so a stale non-conformant row shadowing a conformant one is
   invisible to it — the counter's own receipt still reports `exec_fail 1104 scripts/robots_audit.py
   rc=2` at the repair, unchanged from base. **The repair met its frozen target; this is a residue
   the target does not name, not a violation.** Routed R99-5 and R99-6.
5. **The proposal: R99-A, from `considerthese/2026-11-05.md` Part 2 proposal 4** ("Open-frontier map
   from the Planned sections"). Proposal 2 is taken (round-98's R98-B) and proposal 3 is already
   implemented (QUALITY.md:1848, R95-D), so proposal 4 is the right pick. The lane has the input half
   and not the output half: `SCORECARD.md` carries 12 `Planned — after round N` sections (rounds
   84–98) each ending in a `Frontier:` clause, and `corpus/README.md` has **no** `## Open frontier`
   section, so no ground carries the round it was first named. The concrete instance this round
   re-derives: the merged 304 field set (`§4.3.4`) was first named open in the **round-93** Planned
   section (`SCORECARD.md:5748`) and named open again in r94, r96 and r97 — **four rounds of a ground
   this round finally picks up as C2** — and nothing records that it was four rounds old.
6. **The R99-A check command is shown able to fail, four ways.** The draft checker
   (`frontier_first_named.py`) reads committed bytes only and writes nothing. A scratch clone of the
   lane with a conformant map appended and committed (`db0a7662`, fixture identity, never the lane)
   reads `met=true` rc=0; deleting one map row, moving a row's first-named round **later** than the
   round that named it open, and removing the whole section each read rc=1 with a distinct diagnostic
   (`missing_open_ground`, `wrong_first_named`, `map_rows=absent`). The lane tip itself reads rc=1
   with four missing grounds.
7. **The check command's own limits are stated, not hidden** — it reads free prose, a map row naming
   a ground *earlier* than the naming round passes by construction, and it knows nothing about
   whether a ground is still open. The criterion binds the *artefact*; the check is this seat's
   approximation of it.
8. **The Gate skeleton is filled from the scout's own landed receipts.** `w1/ScoutRfc9111/report.md`
   §2–§3 landed during this seat's work with three GET receipts (RFC 200 / 84 477 B /
   `aeb52adb…`; errata 302→301→200 / 10 655 B / `83c3b795…`; errata-search 302→200 / 40 374 B), both
   bodies **byte-identical to the retained copies**, `quotes = 6/6 located and verified`, and
   `errata-touching = 1` (EID 9185 only; no erratum touches §3.1 or §3.2). The draft's quotes and
   the six located line ranges are the scout's, cited as the scout's first-party evidence; **this
   seat performed no live GET** and independently re-derived only the two retained-body digests and
   the section heading line numbers.
9. **The merge/kake reject is re-derived.** `.ufo/waves/round-99/assimilation/collisions` holds 8
   ids (`S312 S329 S367 S372 S373 S374 S390 S409`); the wave-time populations are 220 registry ids
   and 129 staged ids, the delta against round 98's own receipt (218) being `S482` and `S483`. No
   renumber map exists, so the reject stands with a renumber-map flip condition.

## Out of scope for this seat (not touched, not claimed)

- No product code, instrument, counter, contract, ledger, registry or corpus file was edited. The
  two scripts this seat wrote are **drafts inside its own seat directory** and carry no registry
  row; landing either under `scripts/` would itself require a conformant `SKILL.md` row (mistake 1).
- No C1 verdict: the counter half's receipts are committed and the base half was reproduced
  read-only, but **this seat read neither reviewer verdict file's contents** and asserts no verdict.
- No C2 verdict: this seat did not run `c99_fresh304.py` and did not read `scripts/freshen_304.py`.
- No mutating git or jj command was run in the lane or the fleet repo. `git status --porcelain` in
  the lane shows only files other seats and the L1 are editing — none of them this seat's. The one
  fixture commit this seat made (`db0a7662`) is in its own **scratch clone**, whose toplevel was
  asserted with `git rev-parse --show-toplevel` before the commit and whose identity is
  `scribelesson@example.invalid`.
- No commit, push, publish or deploy; no other runtime invoked.

## Tooling

No tool was installed or upgraded by this seat; the work used the repository's committed Python 3
counter, `git` and standard shell tools already present on the host. No `pacman`, `uv`, `npx` or
`~/.local/bin` action was taken.

## Out-of-lane note (reported, not acted on)

The round-98 closure routed **R98-C3** (`corpus/lessons/round-98-verifier-spotcheck.md:141`): the
round-98 report cites the C1 tip receipt at `77adb17e` while the receipt's own `# cmd:` line names
`--revision 76f834aa…` (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-98/kake.md:66` against
`kake-shokunin/.ufo/waves/round-98/controls/tip-c1.txt:1`). The wording defect lives in a
**fleet-repo** file this seat may not edit; it is reported here for the L1 rather than repaired.

LESSON mistakes=4 proposal=R99-A gate_rows=3
