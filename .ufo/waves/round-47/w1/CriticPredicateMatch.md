# CriticPredicateMatch — frozen predicate vs counter conditions vs receipt labels

Scope: read-only comparison of the two frozen predicate sentences in
`SCORECARD.md` (lines 3919–3968) against `c47_registry_count.py` /
`c47_routed_count.py` docstrings and implemented conditions, and the
`C1_MET`/`C2_MET` receipt labels. No counters executed; no mutating git/jj run.
Axes: operability (C1), freshness (C2).

## Text-level predicate check — VERIFIED

Counter docstrings verbatim-repeat the SCORECARD predicate sentences modulo
markdown backticks and line-wrap (`c47_registry_count.py:5-14`,
`c47_routed_count.py:5-24` vs `SCORECARD.md:3926-3958`). R5 hash pair
`ee43e66367bf23e386ff29029b9ea60515efd9d1` /
`861113eb0eea4d51bd0614c542aa6ecb7cc9a843` identical in both
(`SCORECARD.md:3952-3953`, `c47_routed_count.py:47-50`). No silent predicate
rewording found.

## Label check — VERIFIED

`C1_MET`/`C1_NOT_MET` emitted only at `c47_registry_count.py:137`;
`C2_MET`/`C2_NOT_MET` only at `c47_routed_count.py:160`. Receipts carry those
exact labels (`verification/c1-after-714e707.json:13` `"verdict": "C1_MET"`;
`c2-after-714e707.json:10` `"verdict": "C2_MET"`), matching LOG.md:1850,1865
and SCORECARD.md:3975-3976. No third label anywhere.

## Finding 1 — DISCLOSED literal mismatch: R6 `exit=0` label (freshness)

Frozen predicate (SCORECARD.md:3955-3957) requires the rerun receipt "recording
`--offline` exit=0". Measured: `grep -c "exit=0"
.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt` → **0**; the file
carries `OFFLINE_EXIT=0` (line 87) and `VERDICT: OK (exit 0, partial: offline)`
— never the literal `exit=0`. The `846138c` counter therefore returned
`outstanding=1/4` (receipt `c2-after-846138c.json`, `R6: false`, `C2_NOT_MET`).
The counter was widened at `714e707` to accept `OFFLINE_EXIT=0`
(`c47_routed_count.py:140-143`: `"exit=0" in text or "OFFLINE_EXIT=0" in text`).
This is a matcher widening against the frozen sentence's literal — disclosed
in SCORECARD.md:3978 ("counter instrumentation note (not a predicate change)"),
corpus/QUALITY.md:1085 and corpus/lessons/round-47.md Mistake 4. Semantically
defensible (`--offline` + `OFFLINE_EXIT=0` satisfies the claim's meaning); the
frozen literal never occurs in the artifact. Disclosed → not a hidden scope
change; a strict literalist reading would still call it a label mismatch.

## Finding 2 — unannounced narrowing: R3 matcher drops the required breakdown (freshness)

Predicate (SCORECARD.md:3947-3948) requires a correction line "naming the 20
data rows (12 LOG.md + 8 SCORECARD.md) in LOG.md". Counter
(`c47_routed_count.py:131`) requires only `"R3" and "20 data rows"` on any
LOG.md line — the 12+8 breakdown and the word "correction" are unenforced.
Counterexample: LOG.md edited to a bare `- R3: 20 data rows` still scores
`r3_fixed=true` while violating the frozen condition (and the SCORECARD.md
side's correction could be absent entirely — counter never reads SCORECARD.md).
Actual artifact is compliant (LOG.md:1793-1797 has the breakdown); the
narrowing is latent and unannounced in the docstring.

## Finding 3 — unannounced narrowing: R5 needs no R5 line (freshness)

Predicate requires "an R5 line in LOG.md naming the full hashes".
Counter (`c47_routed_count.py:132`) accepts any line containing both hashes —
no `R5` token required. Counterexample: deleting the `[r47-correction R5
identity]` marker (LOG.md:1813) while keeping the two hashes leaves
`r5_fixed=true`. Actual line 1813 is a proper R5 identity line. Also note LOG
line 1800-1801 puts the hashes on *adjacent separate* lines; only the R5
identity line satisfies both predicate and counter — correct as landed.

## Finding 4 — asymmetric strictness on the R6 withdrawal marker (freshness, advisory)

Predicate asks for "an explicit withdrawal in LOG.md"; counter hard-requires
the exact token `[r47-correction R6 withdrawal]` plus `round-46`/`withdrawn`
(`c47_routed_count.py:133-136`) — stricter than the sentence, while R3/R5 are
looser. Compliant artifact (LOG.md:1814); a differently-worded honest
withdrawal would fail. Recorded as design asymmetry, not a defect.

## Finding 5 — "append-only" unenforced (freshness, advisory)

The predicate opens "prose defects are repaired append-only", but the counter
checks presence of fix lines only; a same-line in-place rewrite (e.g. editing
the '12 rows' cell in place) would still pass if the new lines exist.
Docstring adds no such bound. Other receipts attest append-only repair
(ledger rows retained byte-identical per ledger:32-33; prior lines preserved).
Instrumentation bound, unannounced.

## Finding 6 — C1 latent leniencies (operability, advisory)

(a) "the tool sha256" is enforced only as `SHA256_RE` (any 64-hex token;
`c47_registry_count.py:116-117`) — the junk control "a tally without the tool
sha256 is not a receipt" still passes a receipt with the *wrong* sha.
Honest receipts: `selftest-redirect-audit.txt` carries
`1e1dff18…748a` and `selftest-citation-lint.txt` `3c78a0a8…2987f`, equal to
`sha256sum scripts/redirect_audit.py` / `scripts/citation_lint.py` measured in
the working tree.
(b) "gate-registry row" = any SKILL.md line starting with `|` containing the
path (line 106-109) — not anchored to the registry table; landed rows
(SKILL.md:1197-1198) are real registry rows.
(c) The counter never checks that `scripts/<tool>` itself exists at the
revision — "both round-46 gates" is satisfied by prose+receipt alone.

## Checks NOT run (stated, not claimed)

Counters were not re-executed (read-only review; committed receipts
`c1-before-cd42e3c.json` 0/2 `C1_NOT_MET`, `c2-before-cd42e3c.json` 4/4
`C2_NOT_MET`, `c1-after-846138c.json` `C1_MET`, `c2-after-846138c.json` 1/4
`C2_NOT_MET`, both `714e707` afters MET were inspected as committed bytes).
Receipt sha256s were not re-hashed. The R4 matcher was traced by hand against
`corpus/quality/citation-adjudications.md:31-56` — all five `R4_EXPECTED`
substrings present case-insensitively (e.g. line 40-41 `Corrected reason:
charter repo commit from the 2026-09-28 push series` matches `b74190e`'s
expected phrase).

## Verdict

No undisclosed predicate change and no label mismatch on the landed labels.
One disclosed literal-vs-spelling deviation (Finding 1, disclosed) and two
latent predicate-weakening matchers (Findings 2, 3) that no receipt/mutation
proof exercises — R4 is the only condition with a dedicated mutant control
(`c2-r4-mutation.txt`, 5/5). Counterexample quality: real artifacts compliant;
weaknesses are acceptance-surface, not measured-verdict, defects.

Tooling: no installs/updates (read-only task).
