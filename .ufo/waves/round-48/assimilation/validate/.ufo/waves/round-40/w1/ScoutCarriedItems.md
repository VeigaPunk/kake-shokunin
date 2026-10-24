# ScoutCarriedItems — round-40 wave 1

Axes: operability (judged), freshness (items 4, 8, 10). Tip `f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8` (HEAD). Attacked statement: SCORECARD.md:2530 “items 2–10 open, item 1 fixed” and :2527–2529 (M06 fixture not landed; two `MutRecheckOversize` boundary mutants carried). Read-only. No tool installed. No counter scored.

Commands (cwd lane): `git rev-parse HEAD` exit 0; `git merge-base --is-ancestor d8a20a99 f043c721` exit 0; `git diff --stat d8a20a99 f043c721 --` the defect paths → only `SCORECARD.md` +132 and `corpus/SOURCES.md` +5 (S110–S114 appended; S011 row untouched); `git diff --quiet` of the code/receipt/entry paths below exit 0 (byte-identical to `d8a20a99`); `sha256sum` exit 0. Selftests not re-run.

| Item | Status | Evidence at f043c721 | Attacked “still open” |
|---|---|---|---|
| 2 lone-surrogate URL | open | `scripts/robots_audit.py:87-89,199` still `surrogatepass`; contract still silent `SCORECARD.md:2323-2325`; no surrogate pin in `robots_audit_selftest.py` | holds |
| 3 bracket host | open | `scripts/robots_audit.py:513-531` `urlsplit` hostname `ValueError` → None; no `[not-ipv6]` fixture; contract only non-empty host `SCORECARD.md:1808-1811` | holds |
| 4 S011 outside scope | open | `corpus/SOURCES.md:19` still §§2.3/2.3.1.4; `robots-txt-rules.md:31,33,49,57-63,69,77` still cite S011 for §§2.2/2.5; S099 at `:107` unused by the entry | holds |
| 5 symlinked manifest directory | open | `scripts/robots_audit.py:38,550` still `realpath`; fixtures f23/f24 are file links only (`robots_audit_selftest.py:719-727`); split still only noted `SCORECARD.md:2055-2056` | holds |
| 6 U+FFFD per byte | open | `scripts/robots_audit.py:213` `errors="replace"` (maximal subpart, not per byte); pins are single `\xff` only (`robots_audit_selftest.py:368,492,758`); wording `SCORECARD.md:1819-1820` | holds |
| 7 duplicate JSON names | open | `scripts/robots_audit.py:464-466` `json.loads` without `object_pairs_hook`; `SCORECARD.md:2258` still “undecided and untested” | holds |
| 8 counter harm receipts lack `toolRevision` | open | `r36-counter-on-145a6468-tool.json:5-7` and `r37-counter-on-3ed8e15c-tool.json:5-7` have `toolFile`/`toolSha256` only | holds |
| 9 forgeable `runner` | open | `pinned_selftest.py:220` sets `runner`, `:286` `receipt.update(summary)` overwrites it, `:289-305` pin block never restores `runner` | holds |
| 10 timeline receipts omit invocation | open | `timeline-r38.txt:1-15` is three result blocks (times, PASS, exit); no argv, repo, wave or receipt path | holds |
| (j) survivor M06 | open | `control_consequence_check.py:46-48,107` resolves bytes only in `main`; selftest `:174` calls `evaluate` with a precomputed sha; 20 fixtures `:145-166`, no same-bytes / unresolved-revision case. sha256 `5952be5a…ff33b` = RerunCcCheckFinal pristine. Patch not in the tree | holds |
| MutRecheckOversize M4 (`>`→`>=`) | open | `source_recheck.py:619` still `len(data) > MAX_BODY_BYTES` | holds |
| MutRecheckOversize M8 (cap+1) | open | `source_recheck.py:53` still `16 * 1024 * 1024`; g36 body is `BODY_CAP+1` plus `<p></p>` (`source_recheck_hardening_selftest.py:70,255`), not the exact boundary | holds |

Item 1 stays closed on the same bytes: `source_recheck.py:619-620` returns None; g36 still `:248-258`. sha256 `source_recheck.py` `2ce8c0d9…87e1a`, hardening selftest `39828378…13178` (the round-39 fixed bytes). `robots_audit.py` `f4d057c4…baace`. Round 40’s commit does not touch these sites.

No code ran against the tools. Unrun checks are not claimed passed.
