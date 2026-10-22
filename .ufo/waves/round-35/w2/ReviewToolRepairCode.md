# ReviewToolRepairCode — wave-2 falsify report (r35, C1)

Attacks the C1 repair code: `git diff 318561ef b1cbbc39 -- scripts/link_preview_audit.py`
(end-tag stack, `handle_startendtag`, input_invalid vs page_unreadable split, pagesChecked,
finding order/ids, docstring vs behavior). Verdict: the repair is faithful to contract bullets
(a)-(c) as declared in SCORECARD.md:1378-1395. No actionable defect found in the stack logic or
the split; findings below are Low/Informational. Sealed counter rerun reproduces 24/24 (exit 0).

## Commands run (all in sandbox; no lane mutation)

1. Diff (exit 0): `git -C <clone> diff 318561ef b1cbbc39 -- scripts/link_preview_audit.py`
   (58 insertions/20 deletions: SUPPRESSED_ELEMENTS at line 77; new handle_endtag 106-112;
   handle_startendtag 114-117; og_url_multiple finding 271-277; mixed input+policy result
   302-303).
2. Sealed counter (exit 0, met true, passed 24/24, toolSha256 1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4):
   `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root <clone> --revision b1cbbc39 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc`
3. Probe suite (exit 0, 24/24 probes pass their expectation):
   `python3 -B probes/run_probes.py`
4. Base-vs-repair comparison (2 probes, base rc 0 clean vs repair rc 1 failed-policy): shows the
   repair materially changes behavior (see below).

## Probe results (work dir: probes/work/<name>; manifest JSON in probe_results.json)

Stack logic — all match the documented design and contract bullet (b):
- q1/q1b nested same-name: inner `</template>` keeps outer open; meta between them ignored
  (failed-policy missing og:title when no outside title; clean with outside title).
- q2/q2b `</template>` with open `<svg>` inside: both close; meta after is collected (clean);
  without outside title, missing-title finding (failed-policy). This is the assignment's named case.
- q4/q9 mis-nesting `<svg><template></svg>` / `<math><template></math>`: matching end closes
  nested suppressed element (clean). Consistent with HTML5 foreign-content pop-until-match.
- q3/q5/q21b stray end tags (`</template>` first; `</svg>` inside open template) are no-ops;
  template stays open until its own `</template>` (clean).
- q8 unclosed `<template>` suppresses to EOF (failed-policy, all four missing).
- q7 `<svg/>` opens nothing (clean); q10 self-closed `<link .../>` outside is collected (clean);
  meta/link inside open template/svg/math ignored (q20, sealed cases 01/02/11/14/19).

input_invalid vs page_unreadable / pagesChecked — contract bullet (c):
- q14 bad page URL, q17 duplicate JSON key, q18 symlink escape: manifest-level input_invalid,
  page null, pagesChecked 0, exit 2.
- q13 missing file + readable page: page_unreadable (+ policy findings beside it), pagesChecked 1,
  exit 2, findings order input-first (matches sealed case-06/15).
- q15/q22 (directory/FIFO page), q16 (17 MiB > read bound): page_unreadable, pagesChecked 0.
- q23 all-readable multi-page: failed-policy, pagesChecked 2, only the bad page's findings.

Finding order/ids: q11 page with two og:url (first relative) emits order
[og_url_multiple, og_url_not_absolute]; sealed case-24 key lists [not_absolute, multiple].
The counter compares a sorted projection (sealed_count.py `project()`) and SCORECARD.md:1393-1395
declares `id`/`pagesChecked`/order uncompared, so this is not a defect. IDs match the key format
`<page>:<reason>:<property>` (policy) and `<reason>:<page>` (input).

## Findings

- LOW — self-closed `<template/>` opens nothing (link_preview_audit.py:114-117 skips any
  suppressed-named startendtag). In HTML syntax the self-closing flag is ignored for non-void
  HTML elements, so `<template/>` opens a template; the tool then collects meta an HTML renderer
  would treat as inside the template (false-negative risk on missing-required). Contract bullet
  (b) only specifies `<svg/>`, so this corner is unspecified. Repro: q6 (`<template/>` + full
  set) → rc 0 clean; per HTML semantics the post-template meta should be suppressed. HTMLParser
  event trace confirms `handle_startendtag('template')` fires for `<template/>`.
- INFO — stale comment at link_preview_audit.py:71-72 ("an oversized file is an input finding")
  vs observed/contract classification `page_unreadable` for over-read-bound (q16; bullet (c)
  explicitly lists "over the read bound"). Code follows contract; comment should say "input-category".
- INFO — per-page `input_invalid` branch (238) is practically unreachable: `load_manifest`
  pre-validates the same resolve (202-206), so an escaping path fails the whole manifest at load
  (q18). It survives only as a TOCTOU guard between load and read.

## Residual risk / verification gaps

- Did not exercise the TOCTOU symlink swap between load and read (the only path that reaches the
  per-page input_invalid branch).
- Did not run the claimed selftest 45/45 or round-34 matrix 28/28 (other seats' checks; out of
  item scope).
- No live-network use (owned-site restriction, not applicable). Runs were single-process
  sequential, bounded by `timeout`.

## Deliverables (all under /fast/scratch/hyaku/kake-r35/w2/ReviewToolRepairCode/)

- `clone/` — lane clone at b1cbbc39 (read-only use; no lane mutation)
- `probes/run_probes.py`, `probes/probe_results.json` — harness + results (24 probes)
- `base_tool.py` — 318561ef copy used for the base-vs-repair comparison
