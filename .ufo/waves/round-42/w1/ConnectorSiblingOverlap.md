# ConnectorSiblingOverlap — round 42 wave 1 (read-only scan)

Axes: operability (scan completeness), freshness (pointer currency). No code changed.

Commands (read-only): `grep -rn ... *-shokunin/SCORECARD.md corpus/QUALITY.md corpus/SOURCES.md scripts/` (exit 0); `ls`/`sed` spot checks (exit 0). No counter runs.

## (a) Harm rules pricing runtime cost / change vs guard

| pointer | one-line relevance (reuse / must not duplicate) |
|---|---|
| kake-shokunin/SCORECARD.md:2746,2843,2976 | Own harm rule classifies r41 fixtures 29 change / 13 guard; reuse its H1–H4 shape, do not reclassify |
| mado-shokunin/corpus/QUALITY.md:320 | Post-patch fixture never credited as pre-patch guard; reuse registration-order discipline |
| kumitate-shokunin/SCORECARD.md:474,699 | Origin-I/O amendment prices cost explicitly; reuse cost-recording, not silent re-baseline |
| mori-shokunin/corpus/QUALITY.md:104 | Green fixture never establishes drift freshness; reuse, no guard-as-freshness |
| tameshi-shokunin/corpus/QUALITY.md:176 | Lane guard = removal changes a verdict; reuse definition when naming guards |
| souji-shokunin/corpus/QUALITY.md:79 (Q30) | Per-repo process bound + session kill; reuse for capped URL checks |
| kama-shokunin/corpus/QUALITY.md:203 (KQ36) | Registered counting command re-run at landed tip; reuse re-anchor duty |
| kotoba-shokunin/corpus/QUALITY.md:36-37 (Q25/Q26) | Counter must fail on mutant; headline asserts only measured clauses; reuse |

## (b) Regex backtracking / URL-validation cost defects

| pointer | one-line relevance |
|---|---|
| kake-shokunin/scripts/sitemap_audit.py:67-86 | Claimed `_URI_RE` slow on long adversarial values; do not duplicate its backtracking |
| kake-shokunin/scripts/source_recheck.py:93-100 | Appendix-B `_URI_REF_RE` uses negated classes (linear) but `.*` fragment under re.S; treat as split, not validation |
| chousa-shokunin/tools/quote-reopen.py:80,165-220 | `URL_RE = https?://\S+` plus urlsplit checks (scheme/userinfo/host/port); reuse validation checklist, not regex |
| kagi-shokunin/corpus/SOURCES.md:47 (S040) | re whitespace teaching (str.isspace) for URL/regex char classes; reuse, do not invent |
| kake-shokunin/corpus/SOURCES.md:123-124 (S115/S116) | urlsplit removes C0/space/TAB/CR/LF and does not validate; reuse as non-validation boundary |

## (c) Superseding-row practice in SOURCES.md

| pointer | one-line relevance |
|---|---|
| kake-shokunin/corpus/SOURCES.md:220-225 | Anchor/scope/teaches cells change only via superseding rows; reuse, never edit in place |
| chousa-shokunin/corpus/SOURCES.md:235,240 | Supersession keeps prior rows as history; reuse append-only correction |
| kagi-shokunin/corpus/SOURCES.md:70,118,160,188 | Case-sensitive quote correction via new row, not cell rewrite; reuse |
| kaidoku-shokunin/corpus/SOURCES.md:135,159,165,169 | Supersession counts and family accounting; reuse for row accounting |
| kama-shokunin/corpus/SOURCES.md:43+ | Superseding row carries corrected locator only; reuse scope discipline |

Findings: sibling lanes share the superseding-row and guard-registration idioms but no sibling carries a URL-check cost defect comparable to kake's `_URI_RE`; chousa's URL validation is a checklist over urlsplit, not a regex, and is the safe shape to mirror. Must not duplicate: kake's backtracking regex, in-place SOURCES.md cell edits, or post-hoc guard crediting.
