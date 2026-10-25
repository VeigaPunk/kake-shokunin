# CriticC2Contract

Seat: critic on claim C2 (freshness: Yahoo! JAPAN robots.txt assimilation, quote-true), attacked
before any build. Read: `contract.md` (frozen), `contract.json`, all 699 lines of
`c55_quote_truth.py`, and the `cases` dict in `selftest()`. Lane repo read-only (`git show`,
`git ls-tree`, `git log`); the only lane path written is this report. No pacman, no tool install.

Pre-build state (`git show HEAD`, HEAD = 143e592): base registry 155 rows; base rows S372/S373 carry
`opened 2026-10-25`, `recheck 180d`, used-by `[nofollow]` / `[nofollow, baidu]` (so C3's round-date
test and its held-row byte test do not collide); the three entries and `assimilation/validate/` are
absent; sources, receipts, mirror, mirror-pin are committed at b467ac3/143e592.

**Selftest: UNRUN.** `python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` exits 2 with
`selftest: missing round-55 evidence corpus/lessons/round-55.md` (evidence lands with the build).
Coverage claims below are read from `cases`, not executed. Base control
`controls/base-c2-quote-truth.txt` = `0/8 met=False`, exit 1 (read, not re-run).

Method: every fixture is built with the counter's own `_build()` — `tempfile.mkdtemp`, `git -C $D
init -q`, toplevel equality check, commits with `-c user.name=selftest -c user.email=selftest@local`
— under `/tmp` only, then `run_checks(d, tip)` with `BASE_REV` set to the fixture base. Each fixture
uses the real base registry blob, the real retained bodies and real receipts; only the named detail
differs. Control fixture F0 (well-formed shape, real bodies/receipts, prose a placeholder) = **8/8,
exit 0**, so the harness accepts a well-formed build and every result below is attributable to the
named mutation.

ATTACKS:

- **A1c — one boilerplate span in all six quote slots (strongest).** Gate quote and entry
  quote for all three ids = `"ここから本文です"` (8 units; `grep -cF` = 1 in each of S372/S373/S418 —
  the skip-navigation string), entry prose replaced by a false claim
  ("The operator permits every crawler unconditionally and robots.txt is ignored."). **8/8, exit 0.**
  62 six-character CJK windows are common to all three bodies (`お問い合わせ` = exactly 6 units,
  `ここまでです`, `のページでは`, …), each a legal Gate quote; a 6-unit variant of the same fixture
  (`いウェブペー`) also reaches 8/8. C5 (line 297 Gate, line 315 entry) only tests
  `substring of that body`; nothing ties the span to the robots rule. Selftest: **not covered**
  (`fail_entry_quote` fabricates a span; no case for true-but-trivial).
- **A2 — `[INFERENCE` escape hatch.** Append below the header
  `> [INFERENCE] "この文字列は保持本文に存在しません"`. **8/8, exit 0** — line 307 `continue`s the
  whole line before the span scan at 309, so a fabricated quote on any line containing that marker
  is never tested. Not covered.
- **A3 — truthful quotes, mis-glossed prose.** Keep the three truthful spans, replace all prose with
  the opposite assertion ("case is ignored and every path matches"). **8/8, exit 0.** C5 has no gloss
  or polarity test. Not covered.
- **A4 — receipt for a body that is not the page.** `sources/S418.html` := the S372 bytes, receipt
  S418 `{sha256, bytes}` recomputed, receipt `url` left at `…/002885.php`, S418 quotes taken from the
  S372 body. **8/8, exit 0.** C6 hashes whatever body is committed (line 340) and compares only the
  receipt URL string to the row URL (line 356); no document-identity test exists. Not covered
  (`fail_receipt_url` changes the URL, not the body).
- **A6 — census receipt forged, census never run.** `census-argv.txt` =
  `# census was never run; argv forged` + `cat --file <VALIDATE_REG>`, `census-stdout.txt` =
  `file\trows\t156` + `file\tok`, `census-exit.txt` = `exit=0`. **8/8, exit 0.** C7 (368–392) is a
  receipt: substring tests on argv, `exit=0`, no `E03/E04`, last line's second tab field `ok`. The
  observed census format in `controls/census-before.txt` is `kake\tW04\t<finding>` /
  `kake\tok\t<abs path>` — line 380 accepts `x\tok`, so even the format is not pinned. Not covered
  (every `fail_validate_*` case assumes a real run).
- **A7 — curly quotes below a header.** `> “この文字列は保持本文に存在しません”`. **8/8, exit 0** —
  line 309 matches only `"`. Not covered.
- **A8 — validated document is not the appended block.** `validate/corpus/SOURCES.md` carries
  `| S263x |` while the landed registry is clean. **8/8, exit 0** — line 386 compares only the three
  adopted rows (and the three entries at 388–391), not the validated document as a whole. Not covered
  (`fail_validated_row_differs` mutates the adopted S418 row itself).
- **A9 — control, blocked.** Edit a non-adopted landed row (`| S263 (edited) |`): **7/8, exit 1**
  (`registry rows 155 != mirror rows 155 + 1`; `append-only: … != mirror bytes`, line 432). C8 is the
  one condition that resists. Covered by `fail_not_append_only`.
- Not an attack (tested, negative): the quote ceiling is defeated only by long ASCII tokens, and the
  longest ASCII token in any body is 57 chars (`https://s.yimg.jp/images/templa/mhdemg/v2/static_mhd.html`,
  1 unit under the declared rule) — the ceiling holds as declared; no fixture.

WRONG-REJECT:

- **W1 — relative `--file` argument (genuine defect).** argv `python3 -B tools/census.py validate
  --file corpus/SOURCES.md` with the census run from inside the scratch dir, byte-identical scratch
  registry and genuine stdout/exit: **7/8**, `validation argv does not name the validated scratch
  registry` (line 372, substring test against the repo-relative path). Not covered.
- **W3 — Gate line carrying an extra quoted token (genuine defect).** A truthful, more informative
  Gate line ending `… — accessed 2026-10-25 — status "200"`: **7/8**, because line 293 takes
  `quotes[-1]` = `200` (1 unit). Not covered.
- **W5 — curly quotes in the Gate line.** **7/8** (`Gate line carries no double-quoted located
  quote`, line 289/293). Keep the rejection (the round rule fixes ASCII double quotes), but it is
  inconsistent with A7, where the same form below a header is unchecked. Not covered.
- **W4 — held-row `used-by` ordering.** Same three paths, prior entries preserved, alphabetical
  order: **7/8** (line 264, exact list). *Defensible*: the contract's C4 sentence freezes
  "prior + entry N", so the canonical judge should keep this — tradeoff, not a defect.
- **W6 — short but genuine rule fragment.** Gate quote `「*」記号` (2 units, the operator's own
  heading, raw substring): **7/8** on the 6-unit floor (line 295). Contract-frozen 6..25 —
  tradeoff, keep.
- **W2 — bold provenance keys are NOT a wrong-reject.** `- **source:** S418 …` passes **8/8**
  (C2's `^[-* ]*source *:` tolerates the asterisks). Reported so no fix is added for it.
- Raw-substring vs HTML entities is not a live wrong-reject this round: the three bodies carry only
  `&gt;` twice each (nav/JS), no `&amp;`/`&quot;` in rule text.

RECOMMENDED COUNTER CHANGES: (all inside existing condition names; the frozen predicate sentence
`met: conditions_passed == 8 of 8` is untouched)

1. **C5, line 307** — narrow the exemption: `continue` only when the line *starts* with the marker
   and carries no `"`; otherwise fail with "an inference-tagged line carries a quote". Kills A2.
2. **C5, line 309 (and 289)** — reject `“`/`”` below a header and in a Gate line with "curly quotes
   are not the declared quote form" (the round rule mandates ASCII). Makes W5 and A7 one rule.
3. **C5, line 293** — select the last span with `units(q) >= 6`
   (`quotes = [q for q in quotes if units(q) >= 6]`, fail when empty) instead of `quotes[-1]`.
   Fixes W3 without loosening anything.
4. **C5, new after line 297 and inside the span loop (after 315)** — require the Gate quote and every
   ≥6-unit entry span to occur at or after the page's main-content boundary
   (`text.find(q) >= text.find("<h2")`). Measured: skip-nav at 2216/2226/2244, first `<h2` at
   2505/2516/2534; truthful rule spans at 3249/3604. Kills A1/A1b/A1c, and also pushes S418's Gate
   quote out of the `<meta name="description">` (offset 369) into the body.
5. **C5, same block** — require at least one ≥6-unit span per entry to be absent from the other two
   retained bodies (page-unique rule text). Verified: each truthful span is absent from the other two
   bodies; all 62 common 6-unit boilerplate spans are not. Kills A1 even if the boundary marker moves.
6. **C6, new after line 340** — require `value="{ROW_URL[sid]}"` in the decoded body (the page's own
   URL field: exactly one per body, `class="urlcolor"` once per body; cross-links use `<a href=…>` and
   do not match). Kills A4.
7. **C7, line 372** — resolve the `--file` argument against a `cwd=` line recorded in the argv
   receipt and compare `os.path.normpath` to `VALIDATE_REG` instead of a substring test. Fixes W1.
8. **C7, line 386** — compare the whole validated registry to the landed registry under the C8
   restore rule (line 432), not only the three adopted rows. Kills A8.
9. **C7, before line 392** — make C7 a re-run rather than a receipt: materialise the committed append
   block into a temp registry from `git show` bytes and invoke the census entry point in-process,
   requiring its exit and stdout to match the receipt; minimum interim: pin the observed format
   (`tail[-1].split("\t")[:3] == ["kake","ok",abspath(VALIDATE_REG)]`, findings prefixed
   `kake\tW04\t`, row count present) instead of `tail[-1].split("\t")[1:2] == ["ok"]` (line 380).
   Kills A6. No worktree read, no network — inputs still come from `git show`.
10. **C4, line 264** — no semantic change; keep the order requirement (frozen) and add the expected
    list to the note so W4's rejection is self-explaining.

Timing: apply before the build lands. At HEAD the entries and `assimilation/validate/` are absent
(selftest exit 2), so changes 1–9 are still test-set refinements declared before C2's data exists;
after the build lands they are post-hoc and the contract's "frozen before data" property is lost.
Precedent in-tree: `c55_readme_index.py` is already revised in the working tree ("version 2 (before
any build was measured)") by the C1 seats, while `c55_quote_truth.py` is unmodified at HEAD — so a C2
counter v2 applied now keeps the same pre-data footing.

Impacted axes: freshness (8/8 today certifies "three entries carrying one short boilerplate
substring each",
not three truthful re-grounded entries); operability (C7's receipt-only design lets a build claim a
census validation that never ran); calibration (C1 shares the descriptive-cell idea, not this code —
no cross-impact found).

VERDICT: 8 of 8 is reachable with junk (skip-nav quote + fabricated prose, `[INFERENCE]` escape,
mis-gloss, swapped body, forged census receipt, curated validate document) and four truthful forms
are wrongly rejected (relative `--file`, extra quoted token, curly Gate quote, used-by order);
recommend the ten line-level changes above, applied before the build.
