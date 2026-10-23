# Round 41 — RFC 3986 URL rule for the sitemap audit (C1) and an oracle-labelled counter

author: kake L1, round 41 attempt 1 (KakeR41)

Claim and rules: `SCORECARD.md` "Round 41 — C1 counter candidate" (pre-freeze, `abf457d0`) and "Round 41 —
kill rule (1) fired on counter v1" (`9e3c31d2`). Base `8eb121c8`. Outside check of round 40:
`corpus/lessons/round-40-verifier-spotcheck.md` (not edited here).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-41/sources/`, sums in `SHA256SUMS`
there; fetched 2026-10-23T09:39:11Z).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S117 | https://www.rfc-editor.org/rfc/rfc3986.txt | 2026-10-23T09:39:11Z, HTTP 200, 141,811 bytes, sha256 `3102dae4…d683` (= S098's retained text) | "URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]" (§3, line 867; Appendix A line 2697) | admit, A, spec, mined |
| S118 | https://pypi.org/pypi/abnf/2.9.1/json | 2026-10-23T09:39:11Z, HTTP 200, 8,215 bytes | "validate a whole string against a rule (raises ParseError otherwise)" (README in `info.description`); wheel digest `cdcac127…0917` = vendored oracle | admit, B, code, mined |
| S119 | https://pypi.org/pypi/rfc3987/1.3.8/json | 2026-10-23T09:39:11Z, HTTP 200, 9,900 bytes | "Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)" (`info.summary`); wheel digest `10702b1e…ce53` = vendored second oracle | admit, B, code, mined |

Re-opened by wave-1 scouts (`.ufo/waves/round-41/w1/ScoutReopenS117.md`, `ScoutReopenOracles.md`,
`ScoutIRIRule.md`): live RFC 3986 bytes equal the pin; both PyPI digests equal the vendored wheels; the
sitemaps.org page (S102) still has sha256 `5e757059…1654` and the sentence "Please check to make sure that
your URLs follow the RFC-3986 standard for URIs, the RFC-3987 standard for IRIs, and the XML standard."
RFC 3987 (https://www.rfc-editor.org/rfc/rfc3987.txt, sha256 `7cc9e3c4…7878`) was opened by `ScoutIRIRule`
to test a wording; no row rests on it, so no row is written.

Row changes: S117, S118, S119 added. No `status`, `recheck` or `used-by` change to an existing row.

Rejects this round (recorded before the build):
- **Rejected: counter v1 as C1's admission instrument.** Reason: 15 of 141 live-seat control receipts meet
  its predicate, among them a percent-rule partial repair (`CtlNoPct` `terminal_pct`, trailing `%`) and a
  generator-shape tool (`CtlGeneratorShape` `v1_shape`); kill rule (1) → C1 exploratory.
- **Rejected: "U+0080 and above stay accepted … as RFC 3987 IRI characters".** Reason: RFC 3987 `ucschar`
  starts at U+00A0 and has holes, and S102 asks for URL-escaping (`ScoutIRIRule`, `CriticClassScope` 7);
  the behaviour is kept as unchanged legacy acceptance and the SKILL text says so.
- **Rejected: the reference's own IP-literal check** (`6d7c2dd4…`). Reason: outside the class and untested
  by the counter (`CriticClassScope` 8); the landed build `0b485431…` leaves IP literals to `urlsplit` as
  the base did.
- **Rejected: "S098 already teaches the URI production"** (`ScoutReopenS117`: S098 is §§2.1–2.3 only), so
  S117 is a new row, not a re-cite.
- **Not changed: the single-point-mutant classification** (`CriticPredicate`, `CriticClassScope` 6 call it
  a QUALITY (n) conflict). Reason: it was frozen at `abf457d0` before any control was scored and is the
  stricter reading; changing it after scores would be a rule changed after data.

## Wave 1 — the control wave fired the kill rule

37 seats, 0 dead, 0 refused. The meeting tools and the classes that did not meet are in the SCORECARD
kill-rule section. What the receipts teach: the oracle-labelled generator separates every skip that
changes the answer on the cases it generates (constant 802, no-reader 1193, id/position-keyed ≤1051,
isolation probe base-level, per-character table 1309, every one-component and one-field skip ≤1355, all
28 repertoire-drop mutants ≤1424), but a generator that inserts only at interior positions and uses one
IP-literal template leaves sub-shapes no case reaches. Counter v2 (information only) closes the two found
gaps: under v2, `terminal_pct`, `v1_shape`, `strip`, `delimiter_proxy` and `m07_query_hash` fail. Still
meeting under v2 are tools that the seats or the receipts show to be equivalent to the grammar on the
generated class (allow-list plus delimiter rules on top of `urlsplit`, a reference-decoding RFC check,
mutants whose admission `urlsplit` rejects downstream). A counter cannot and should not separate those;
deciding which tools are controls by construction ("an allow-list") instead of by behaviour is what left
the classification open.

Other wave-1 findings carried forward: `SentinelSandbox` HIGH — the tool can read bubblewrap's own
environment at `/proc/1/environ` (v2 passes a minimal environment; nothing label-bearing was in it,
`CtlIsolationProbe`); MEDIUM — the counter's stdin is inherited and output capture has no byte cap (open
for the next counter); `ReviewCounterCode` MEDIUM — an inserted delimiter can move the unit into another
parsed component, so `byComponent` overstates per-component coverage (labels stay right);
`ConnectorSiblingOverlap` — no other lane tool decides URL validity by `urlsplit` acceptance the way
`sitemap_audit.py` did; `source_recheck.py`'s Appendix-B reading is comparably loose (a separate claim).

## Mistakes

1. **Class: a generated counter whose case support is narrower than the class it names.** Evidence:
   counter v1 (`c1_count.py:117-119`, `insert` at `randint(1, len-1)`) never puts a unit at either end of a
   component and generates one IP-literal template (`:149` before v2); `terminal_pct` (accepts a trailing
   `%`) and `v1_shape` (keys on the template) meet it (`verification/w1/CtlNoPct__terminal_pct.json`,
   `CtlGeneratorShape__v1_shape.json`). The SCORECARD class sentence said "an interior position", so the
   gap was declared but not seen as a gap. Captured-by: QUALITY (o) as amended in round 40 — non-author
   controls before the freeze; it caught this before any build data. Fix: QUALITY (u) — a generated counter
   inserts at every position, ends included, and generates absent and empty optional components and varied
   forms of every non-target part; check: the two tools are standing controls. Shown able to fail: under v1
   both meet (red: `verification/w1/*terminal_pct.json` and `*v1_shape.json`, `met: true`); under v2 both
   fail (`verification/w1v2/CtlNoPct__terminal_pct.json`, `CtlGeneratorShape__v1_shape.json`, `met: false`).
2. **Class: dead-seat leftovers counted as independent controls (round-40 routed defect 1).** Evidence:
   `corpus/lessons/round-40-verifier-spotcheck.md:44-57`; round 40's "27 of 76" included four receipts of
   the dead seat `CtlUTabOnly`. Live seats only: **26 of 72** (`w1/ReviewR40Restatement.md`). Captured-by:
   none in round 40 (the closure's recount). Fix: QUALITY (s) with
   `.ufo/waves/round-41/criteria/live_tally_check.py`. Shown able to fail: exit 1 on round 40 (four
   dead-seat receipts listed, `verification/criteria/live-tally-r40.txt`); exit 0 on round 41 (no dead seat).
3. **Class: a build revised after the attack checked only by the L1's reruns (round-40 routed defect 2).**
   Evidence: `round-40-verifier-spotcheck.md:71-74,166-167`; no round-40 seat report names the final tool
   `4de35f8c…`. Captured-by: none in round 40. Fix: QUALITY (t) with
   `.ufo/waves/round-41/criteria/fresh_review_check.py`; in round 41 the build was revised before it landed
   (`6d7c2dd4…` → `0b485431…`) and wave 2 reviews the landed bytes. Shown able to fail: exit 1 on round 40
   (`verification/criteria/fresh-review-r40.txt`, 0 seat reports name `4de35f8c…`).
4. **Routed defect 3 (QUALITY (r)) — answered, not a new mistake.** The round-41 counter names case
   directories, mounts, files and ids at random and keeps labels in the counter process; the round-40
   standing controls score `CtlKeyFinder` ×4 0/1434 and the label- and position-keyed tools ≤1051
   (`verification/r40standing/`), so the (r) check is green on this counter and was red on round 40's.

Sweep for others: the wave-1 critics and reviewers above; their findings are carried, rejected or fixed in
this lesson and the SCORECARD kill-rule section.

## Corrections to round 40 (appended; the round-40 report and lesson are not edited)

- Round-40 correction (routed defect 1): the wave-1 control tally is restated over live seats only — 26 of
  72 receipts meet the frozen 30-witness predicate; the dead seat `KakeR40.CtlUTabOnly`'s four leftover
  tools are listed apart (1 of 4 met: `tool_tab_only_query` 30/30) and are not counted as independent
  controls; 26 ≥ 1, so kill rule (1) still fired before the build `56d57ee4` and no round-40 conclusion
  changes. (Sentence from `w1/ReviewR40Restatement.md`, recounted from committed bytes at `8eb121c8`.)
- Routed defect 4 (interior C0 controls other than TAB/CR/LF in `loc` and `sitemapUrl`): decided against
  RFC 3986 by C1 — every C0 control and DEL is rejected in `sitemapUrl`; in `loc` they cannot occur in
  well-formed XML 1.0 at all, so sentence 8 (`xml_malformed`) already decides them there.
