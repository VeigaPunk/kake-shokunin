# SKILL.md URL-rule amendment draft

Axis: operability.

## Draft
Proposed placement: append after `SKILL.md` line 1155 (new line 1156).

```text
### Sitemap file audit — round-41 URL judgment (candidate; pre-freeze)
Planned C1 repairs `_parse_url` for `loc` and manifest `sitemapUrl` (contract sentences 4 and 22): require RFC 3986 `URI` grammar, not merely what `urlsplit` accepts.
S102 asks sitemap URLs to follow RFC 3986 URIs and RFC 3987 IRIs; planned source S117 is RFC 3986 §3 / Appendix A.
Require an `http` or `https` scheme and an authority with a non-empty host.
Out of class: U+0080 and above retain round-40 acceptance as IRI characters; IP-literal contents and ports above 65535 remain unchanged.
Count: `python3 -B .ufo/waves/round-41/c1_count.py --root . --revision <rev> [--seed N] --out <receipt>` (or `--tool-file <path>`); exit 0 met, 1 not met, 2 cannot evaluate.
```

## Findings and evidence
- Holds — `SKILL.md:1118-1155` is the current sitemap-audit section; line 1155 is its end, so append at line 1156.
- Holds — `SCORECARD.md:2680-2689` gives the URL rule, S102 and planned S117 references, and out-of-class choices; `2696-2709` gives the counter command, exit meanings, and predicate details.
- Holds — the draft makes no claim of admission. The SCORECARD section is explicitly pre-freeze (`2672-2678`).
- Source check — `corpus/SOURCES.md` had no `| S117 |` match; this draft calls S117 planned and does not represent it as an admitted source row.

## Gates, surfaces, and limits
- Read-only checks: `functions.grep(pattern="sitemap_audit", path=".../SKILL.md")` returned the sitemap section; `functions.grep(pattern="Round 41 — C1 counter candidate", path=".../SCORECARD.md")` found the round-41 section; `functions.grep(pattern="\\| S117 \\|", path=".../corpus/SOURCES.md")` returned no match. Tool calls returned results; no shell exit codes apply.
- Counter, build, selftest, and other gates were not run; no score or admission claim is made.
- Only this report was written. `SKILL.md`, `SCORECARD.md`, and the lane sources remain unedited. No tools installed.
- Out of scope: evaluating RFC source accuracy or the counter's strength; this is a draft only.
