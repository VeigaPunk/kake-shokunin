# CriticOverreachV2

ATTACKS: B1's landed C3 rows, entries and correction against the wave-1 MUST-NOT bounds and retained source wording (S427/S428/S429). Axes: freshness/source fidelity; evidence precision.

## VIOLATIONS:

No established MUST-NOT violation found in the prose actually present in the three knowledge entries, their correction, or rows S427–S429. The strongest apparent counterexample is the correction's conclusion, `a publisher still cannot count on robots.txt to hold a user-triggered fetch back` (`corpus/knowledge/googlebot-verification.md:41`): this is an operational inference, not wording asserted verbatim by S428. However, the cited source says user-triggered fetchers “generally ignore robots.txt rules” (retained `S428.html`, article paragraph at source lines 1086–1089); the explicit qualifier narrows the claim and the conclusion communicates its consequence without erasing that qualifier. It is not the forbidden absolute “all/always ignore.” `google-user-triggered-fetchers.md:30–34` also preserves both the user-request causation and `generally`, and explicitly says the page gives no exception. Thus this is not a falsifying counterexample.

The older S426 wording remains quoted as an explicitly dated, attributed historical statement (`googlebot-verification.md:38–44`), immediately distinguished from the later S428 statement. It is not presented as the current category rule. The S429 entry retains the key qualifiers `may`, `might`, and `respectable`, and states both non-enforcement and the still-indexable disallowed URL (`robots-txt-limits.md:43–56,70–78`).

## QUALIFIERS KEPT:

- **S427:** the held S426 common-crawler quote keeps “always” and “for automatic crawls”; the special-case quote keeps “may or may not” (`googlebot-verification.md:24–30`). The new S427 row describes common and special-case posture, not a three-category universal (`SOURCES.md:173`; `round-60.md:25–32`).
- **S428:** heading and body say “generally ignore”; the body quotes the user-request cause and disclaims knowledge of exception set (`google-user-triggered-fetchers.md:6,28–34`). The correction calls the later posture qualified, says neither page names the exception, and keeps earlier words historical (`googlebot-verification.md:40–44`).
- **S429:** `robots-txt-limits.md:43,56,64,74–78` preserves `may`, `might`, `respectable`, and the indexability limit; its headline says “may ignore” (`:6`).
- **Unrelated S427 technical limit qualifiers:** this attack's examined new entries do not make the 15MB or caching claims; those are not a basis for alleging overreach here.

## FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| low | corpus/knowledge/googlebot-verification.md:41 | `cannot count on robots.txt to hold ... back` is a paraphrased operational consequence of S428's “generally ignore,” rather than an independently quoted source clause. It remains qualified by adjacent text and is not an overreach violation. | `grep -n 'generally ignore\|cannot count on robots.txt\|neither page names' corpus/knowledge/googlebot-verification.md` plus `grep -n 'fetchers generally ignore robots.txt rules' .ufo/waves/round-60/sources/S428.html` (source occurrence at article paragraph lines 1086–1089) | No change required; retain the adjacent attribution/qualifier. If stricter literal-only prose is desired, describe it explicitly as an inference rather than source wording. |

VERDICT: No supported C3 qualifier violation found; the correction's consequence is a bounded paraphrase of S428's “generally ignore,” not an unqualified universal.