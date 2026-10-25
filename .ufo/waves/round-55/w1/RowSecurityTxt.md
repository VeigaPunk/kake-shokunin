# RowSecurityTxt

Claim C1 (coverage-map calibration). Read `corpus/knowledge/security-txt-publishing.md` in full (126 lines) and `corpus/README.md` `## Coverage map` header plus the existing rows. One row drafted below; no file edited.

## ROW:

```markdown
| security.txt publishing on GitHub Pages (r35) | `knowledge/security-txt-publishing.md` (S078–S080, S082–S086, S001–S002, S006) | Where `/.well-known/security.txt` lives and the duplicate rule, HTTPS and `text/plain` serving, the registered fields with cardinality, the `Expires` horizon, contact order, encryption and signing, host scope, two live files, and dot-directory handling for a Jekyll branch build versus an Actions artifact build |
```

Mechanical check on this exact line: Coverage = 42 units (10–45); no `|` in any cell; does not start with `TBD`; shares `security` and `Jekyll` with the H1 (`# Publishing a security.txt from GitHub Pages`, line 10) and `Actions`, `artifact`, `branch`, `build`, `scope` with the first 1500 characters; Entry ids copied from the file's own `source:` line (line 1), excluding the rejected S081/S087. Area = 6 words.

## EVIDENCE:

1. `corpus/knowledge/security-txt-publishing.md:20` — "A website's file belongs under `/.well-known/` (S078)." (7 units, raw substring). Rest of the duplicate-rule clause: lines 26–29 ("A root copy is tolerated for legacy clients and may redirect (S078)", "With both present, the well-known copy must be used (S078)").
2. `corpus/knowledge/security-txt-publishing.md:48` — "`Expires` is mandatory, exactly once, an RFC 3339 date-time; a horizon shorter" (12 units, raw substring). Supports "the `Expires` horizon"; cardinality wording ("exactly once", "at most once" line 51, "optional, repeatable" line 53) supports "registered fields with cardinality".
3. `corpus/knowledge/security-txt-publishing.md:67` — "It applies to the host actually used to fetch it, not its parents or" (14 units, raw substring). Supports "host scope"; line 70 adds that RFC 8615 leaves scope to the registering application.
4. `corpus/knowledge/security-txt-publishing.md:87` — "drops hidden paths by default; v5.0.0 adds an `include-hidden-files` input" (10 units, raw substring). Supports "dot-directory handling … Actions artifact build"; lines 77–80 supply the Jekyll branch-build half (`include`, S006/S080).

Also traceable without a quoted passage: contact order (line 47, "Several `Contact` lines are ordered by preference, first line preferred (S078).", 11 units), encryption and signing (lines 57–61), two live files (§The two live files, lines 97–107), HTTPS/`text/plain` (lines 35–36). All quotes verified as raw substrings with Python `in` against the retained file; no check was rerun on any source.

## RISKS:

- **The row is not new.** `corpus/README.md:337` already carries a coverage-map row for this exact file, Area "security.txt publishing on GitHub Pages (r35)". Appending the drafted line would create a duplicate; it should replace or merge into line 337. Reported rather than silently appended, since this seat may write only its own report.
- **The existing row is out of step with the file.** Its Entry cell lists `(S078–S080, S082–S085, plus S006 re-opened)` but the file's `source:` line (line 1) also names S086, S001 and S002 — sources the existing row's own Coverage text cites. It further claims "the publisher-facing generator's step that creates the file under the `.well-known` directory of the project (S079)"; `grep -n generator` on the knowledge file returns nothing, so that clause rests on no sentence in the current body (overreach or drift).
- **Round tag is derived, not literal.** The header has no `r35` token; `(r35)` comes from the `round-35` path strings in `verified-at:` (line 2) and `counter:` (line 8). If a literal tag is required, the Area must drop it.
- **Body text the row must not repeat.** The appended corrections contradict uncorrected body lines: line 8 caps size at 1500 words while the wave-2 correction says counter v2 caps at 2200; line 8 says the probes are sealed while the correction places them in `.ufo/waves/round-35/sealed/`; line 52 attributes the English default to S078 and S079 but the round-36 correction narrows it to S078; lines 28–29 present the root copy as "a redirect or byte copy" though S078 requires only that the well-known copy be used; lines 83–85 present `.nojekyll` as the lever without its [INFERENCE] tag; lines 90–91 hold only for upload-pages-artifact v4.0.0 and later (v3.0.1 drops no dotfiles).
- **What the row deliberately does not say.** Not "every registered field" (the file's own `coverage:` line uses "every"; the body enumerates fields with cardinality, so the row says "the registered fields"), and no conformance claim for the two live files: S084/S085 are retained bodies only, so headers, TLS and redirects are unobserved. S084's `Expires` is regenerated per response, so its recorded date is expected churn and the row quotes no date.
- **Freshness.** `verified-at: 2026-10-22`, three days before this round's date; `recheck: 90d` puts the next due date near 2027-01-20. Not stale, but the file predates round 55, so this row adds a map entry, not a new observation.

VERDICT: One format-compliant coverage-map row drafted and mechanically verified; the file is already covered at README:337, so the row is a replacement candidate, and that existing row plus six uncorrected body lines carry overreach/drift the map cannot fix.
