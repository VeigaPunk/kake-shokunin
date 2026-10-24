# KakeR35.CriticC1Sufficiency: does 22 of 24 on the C1 sealed cases need real parsing?

Attacked: what C1's sealed score (24/24 at b1cbbc39, target 22) proves about the repair of
`scripts/link_preview_audit.py`. Result: a regex-only tool with no HTML parser scores 24/24
on the sealed counter. The sealed cases cannot tell real parsing from regular expressions, and
the target of 22 is met even with contract bullet (c) skipped entirely [INFERENCE, arithmetic
below]. Only the selftest, whose fixtures the builder wrote, catches the regex tool.

## Tools (sandbox commits on 7deacc46 in /fast/scratch/hyaku/kake-r35/w2/CriticC1Sufficiency/clone)
Each commit replaces only `scripts/link_preview_audit.py` and removes `.ufo/waves/round-35/sealed/*.json`.
The counter exits 2 on a revision that holds a key, and 7deacc46 holds one.
- T1 regex (`critic-regex` 9dc96fca, tool sha256 e1647075…): the b1cbbc39 tool with `MetadataParser`
  replaced by regular expressions written from the public contract (SCORECARD.md:1379-1396).
  One non-greedy `<(template|svg|math)…>.*?</\1>` strip with no nesting count and a `(?<!/)>`
  lookbehind for `<svg/>`; `<meta|link …>` and attribute regexes; no comment, character-reference
  or raw-text handling.
- T2 base+(c) (`critic-base_c` b63bb5e0, c7d8b733…): the 16a6b8b8 tool plus only the two
  `audit_manifest` hunks of the (c) repair.
- T3 base+naive (a) (`critic-base_naive_a` 9a0549a1, 32124a63…): the 16a6b8b8 tool plus
  `if text.count("og:url") > 1: og_url_multiple`.
Sources: /fast/scratch/hyaku/kake-r35/w2/CriticC1Sufficiency/tools/{regex,base_c,base_naive_a}.py.

## Commands (cwd = clone, TMPDIR = sandbox tmp; outputs in …/CriticC1Sufficiency/out/)
`timeout 600 python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision critic-<t> --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc`
`timeout 600 python3 -B scripts/link_preview_selftest.py --tool <sandbox>/tools/<t>.py` (45 fixtures at 7deacc46)
`timeout 600 python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision critic-<t>`

| Tool | Sealed C1 (exit) | Failed sealed cases | Selftest (exit) | Round-34 matrix |
|---|---|---|---|---|
| T1 regex | 24/24, met (0) | none | 43/45 (1) | 28/28, constants rejected (0) |
| T2 base+(c) | 16/24 (1) | 01 02 11 12 14 19 23 24 | 40/45 (1) | 28/28 (0) |
| T3 base+naive (a) | 16/24 (1) | 01 02 04 06 11 14 15 19 | 37/45 (1) | 28/28 (0) |
| reference b1cbbc39 | 24/24 (0) | none | not rerun | not rerun |
| control 16a6b8b8 (committed `verification/control-v2-c1-base-tool.json`) | 14/24 | 01 02 06 11 12 14 15 19 23 24 | — | — |

T1 selftest failures: `svg_nested_suppression` and `template_suppressed_metadata`. Both nest a
container inside a same-name container, and the non-greedy strip ends at the inner end tag.

## Why the sealed cases are weak on (b)
I profiled the sealed case HTML (out/ has the counter JSON; script inline in my session).
- (b) cases 01, 02, 11, 14 and 19 each hold one container at depth 1: template, svg, template,
  template, math. No sealed case nests containers, self-closes `<svg/>`, or puts a container in
  a comment, a character reference or a raw-text element. Two of the four (b) sub-rules
  ("nesting is counted", "a self-closed `<svg/>` opens nothing") have no sealed case.
- (a) is mostly tested by count: in 12, 23 and 24 the string `og:url` appears exactly twice and
  both values are non-empty. Only case-04 (a second `og:url` with `content=""`, expected
  clean) separates "non-empty element" from a substring count. T3 loses exactly that case.
- (c) has two cases (06: a directory page; 15: a missing page beside a policy page). T2 fixes
  exactly those two and nothing else.

## Is 22 of 24 the claimed work? No.
- Per case, attribution is disjoint (T2 and T3 runs, base control): (b) fixes 5 cases, (a) 3,
  (c) 2. Base 14 + (a) 3 + (b) 5 = 22, so a tool that skips all of (c) still meets the target
  [INFERENCE: not built, tool cap of three; 06 and 15 hold no container and one og:url each].
  Skipping (a) gives 21 and skipping (b) gives 19, so the threshold forces (a) and (b), not (c).
- Depth-1 regex stripping meets (b) on all five sealed cases (T1). A substring count for (a)
  costs one case. With (c), T3's approach plus T1's strip would score 23 [INFERENCE, not run].
- So the sealed 24/24 proves that the tool meets (a), (c) and single-level (b) on these
  inputs. It does not prove the parser-based nesting and self-close behaviour that the
  contract and the tool docstring claim. That evidence comes only from the selftest fixtures
  `svg_nested_suppression`, `template_suppressed_metadata` and `svg_self_closing_guard`. The
  builder added them at b1cbbc39, so they are not sealed and not independent of the build.

Impacted axis: operability (C1's strength and provenance). This is a fixable defect in the
evidence, not in the tool: the b1cbbc39 tool passes the selftest nesting fixtures (45/45
claimed; I did not rerun it).

Smallest safe correction: change the C1 claim wording in SCORECARD round-35 so that it says
the sealed set covers single-level (b) only, and cite the selftest nesting and self-close
fixtures, marked builder-authored, as the only evidence for those sub-rules. For a future
sealed set: add nested same-name containers, `<svg/>` followed by metadata, a container inside
an HTML comment, and an `og:url` substring that is not a meta element. Also set the target so
that no full contract bullet can be skipped (24 of 24, or at least 2 cases per bullet with
the target at total minus 1).

## Not verified
- The b1cbbc39 selftest (45/45) and the "base+(a)+(b) without (c) = 22" and "23" combinations
  were not run.
- T1 was not tried on adversarial inputs beyond the sealed set and the selftest.
- T1 was written after I saw the sealed expected reason lists, but before I read any sealed
  HTML. It was not tuned to the key: its first build is the one scored.
- No tools were installed or updated.
