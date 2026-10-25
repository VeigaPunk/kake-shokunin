# RowAccessPacket

Claim C1 (coverage-map calibration). Read in full: `corpus/knowledge/accessibility-review-packet.md` (182 lines) and `corpus/README.md` header + `## Coverage map` (lines 1–50, rows through `Field performance (r28)`), plus the round-25 section table at README:153–156 that already names this file. No file outside this report was modified; no tool, selftest or packet command was run.

ROW:

```markdown
| WCAG 2.2 accessibility review packet | `knowledge/accessibility-review-packet.md` (S035) | Fixed Level A/AA WCAG 2.2 criterion population: one `not-assessed` card per criterion with located quote, publisher check, evidence needed, failure example, limitation; a local gate validates structure, metadata and quote binding, never website conformance |
```

Checks against the assignment's constraints: 3 cells; Entry is the backticked `knowledge/accessibility-review-packet.md` followed by `(S035)` copied from the file's own `source:` line (line 1); Coverage = 34 words (10–45); no `|` character inside Coverage; does not start with `TBD`; shares `publisher` with the H1 and `criterion`, `website`, `conformance` with the first 1500 characters; no `all`/`every`/`complete` claim and no count that the file does not itself state.

EVIDENCE:

- `accessibility-review-packet.md:15` — "The fixed population is the Level A and AA success criteria in W3C's" (13 words, raw substring). Grounds "Fixed Level A/AA WCAG 2.2 criterion population"; the 12 December 2024 Recommendation is named on line 16.
- `accessibility-review-packet.md:25` — "`accessibility-review-cards.json` contains one card per selected criterion:" (7 words). With `:28` — "limitation. Each card's status is `not-assessed`." (6 words) — grounds "one `not-assessed` card per criterion" and the field list (lines 25–28: identifier, title/level, source URL, located quote, publisher check, evidence needed, failure example, limitation).
- `accessibility-review-packet.md:138` — "The gate validates **structure, metadata and quotation binding only**." (9 words). Grounds "a local gate validates structure, metadata and quote binding".
- `accessibility-review-packet.md:8` — "publisher review work. It does **not** measure a website's accessibility." (10 words). Grounds "never website conformance"; line 52 names the separate JSON field `websiteConformance` = `not-assessed`.

RISKS:

1. **Duplicate ground in README.** The canonical `## Coverage map` table has no accessibility row, but the round-25 section table already carries `| Publisher accessibility review preparation | knowledge/accessibility-review-packet.md, knowledge/accessibility-review-cards.json (S035) | ...` at README:156. Adding my canonical row leaves two rows describing the same file unless the r25 table row is retired or cross-referenced. I cannot edit README; that decision belongs to the integrator/planner.
2. **Entry-cell divergence.** The existing r25 row pairs the packet with `knowledge/accessibility-review-cards.json`; my row is packet-only because the assignment scopes one row to this file. Card coverage is therefore still asserted only by the r25 table row.
3. **What the row cannot say.** It cannot claim any page, build or process was evaluated (file:8, file:109), cannot claim card prose is semantically adequate or true (file:138–141: a nonempty field is "not mechanically judged true, adequate or usable"), cannot claim the pinned WCAG source is still the current online release (file:~158–160: the offline gate cannot observe a new release), and cannot claim AAA coverage or 4.1.1 Parsing coverage (file:17–19: AAA outside the packet; 4.1.1 removed).
4. **Verification limits of this seat.** I did not run `scripts/accessibility_packet.py`, the selftests or `frozen_replay.py`, so "a local gate validates…" is the file's stated behavior, not my observed run. The referenced paths exist (population.json 63401 B, source-wcag22.html 512457 B, cards JSON 163613 B, script 9618 B, all dated 2026-10-21), but I did not execute them.
5. **Typos noticed in the file itself.** `:176` "an explicit local maximum of64 object/array levels" and `:180` "the64-level parse boundary" are missing a space ("of 64", "the 64-level"). Cosmetic, but it is the same paragraph that states the depth rule.
6. **Round-25-only provenance.** `:160` "W2 ReviewSource reopened both URLs this round and reported identical bytes" is a round-25 claim; nothing in this round re-checked it. `verified-at: 2026-10-21` in the header is likewise not re-dated.

VERDICT: One new canonical coverage-map row drafted for `knowledge/accessibility-review-packet.md` (S035), all statements traceable to file:15/25/28/138/8; main risk is the pre-existing r25 table row at README:156 duplicating this ground.
