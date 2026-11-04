# ExecAuditTool — C2 offline hreflang audit tool (round 76, w1)

Seat: `ExecAuditTool`, kake lane round 76, attempt 1, wave w1. Base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
Frozen terms: `contract.md` §C2 plus `amendment-2.md` (17 classes; it changes several earlier derivations)
and `amendment-6.md` (E1/E2 freeze the canonical and `multiple_xdefault` readings below; E3 states the target
over decided cases). Nothing outside this seat's wave directory and its own scratch was written; the scratch
was removed before this report was finished.

## 0. Deliverables

| Path (relative to the lane root) | sha256 |
|---|---|
| `.ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py` | `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` |
| `.ufo/waves/round-76/w1/ExecAuditTool/fixture-3page/manifest.json` | `68c0e7cf17d9506aa79a7d163190d448d3975817122d2430eaf5a16512d946f5` |
| `.ufo/waves/round-76/w1/ExecAuditTool/fixture-3page/home.html` | `f451f2e06195f5a9f553fab743546bd53379c89b58e94b1115beb47a1a5dbaa3` |
| `.ufo/waves/round-76/w1/ExecAuditTool/fixture-3page/de.html` | `a888cd08ac8323921901fd41710e7768ef3306814683c5e3f501c1d96621ff07` |
| `.ufo/waves/round-76/w1/ExecAuditTool/fixture-3page/blog.html` | `69ef61ce062f6d0dc7b386d7bbe770b3b844683afffc2418a3d27ef146af03f9` |

The hashes are the observed output of
`sha256sum hreflang_audit.py fixture-3page/manifest.json fixture-3page/home.html fixture-3page/de.html fixture-3page/blog.html`
(`receipts/sha256.txt`).

Receipts under `w1/ExecAuditTool/receipts/`: `selftest.stdout.txt`, `selftest.stderr.txt` (empty),
`fixture-3page.stdout.txt`, `fixture-3page.text.txt`, `preview-8.stdout.txt`, `cases.txt`, `sha256.txt`,
`retained-surfaces.txt`, `matrix-peer.txt`.

The L1 copies `hreflang_audit.py` to `scripts/hreflang_audit.py`; this seat did not write into `scripts/`.

## 1. What the tool is

`hreflang_audit.py --manifest PATH [--root DIR] [--json]` reads a v1 manifest, parses each local page,
and prints a deterministic finding list. Read-only, network-free, standard library only. `--selftest
--work DIR` builds 56 isolated fixture trees under `DIR` and runs the tool as a subprocess on each.

```
usage: hreflang_audit.py --manifest PATH [--root DIR] [--json]
       hreflang_audit.py --selftest --work DIR
```

argv rules: `--manifest` is required unless `--selftest`; `--work` is required with `--selftest`;
`--selftest` rejects `--manifest` and `--json`; `--root` defaults to the process cwd; each option may be
given once (a repeat is a usage error); `-h` exits 0; every other usage error exits 64.

Exit map: `0` clean, `1` policy findings, `2` input faults, `64` usage (including `version != 1`, A15).
`--json` prints exactly `{version, pages, findings, counts, exit}`; each finding is
`{id, severity, page, detail}` with `severity` in `policy` / `info` / `input` (A1; `input` is this tool's
name for the third class, which A1 does not name). `counts` is
`{policy, info, input, by_id}` with `by_id` covering all 12 frozen ids.

Order is fixed: input faults first (manifest order), then per-page findings in manifest order, then the
frozen id order, then document order. The order is not part of the claim; A16 compares ids as a multiset.

## 2. Selftest tally

```
$ python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py --selftest --work <scratch>/work7
selftest 59/59 passed
exit=0
```

`receipts/selftest.stdout.txt` records that line and `exit=0`; `receipts/selftest.stderr.txt` is empty.
59 = 56 fixture cases + 3 harness checks (byte-identical repeat run, a deliberately wrong expected id that
the comparator must reject, and the five-key JSON shape). Every finding id has at least one red and one
green case; input faults, the tag-grammar corners, rel/markup corners, and all amendment-A rules are
covered. The complete case inventory with expected `{exit, pages, ids-multiset}` is
`receipts/cases.txt` (57 lines: 56 case lines plus a `cases=56` trailer).

## 3. Three-page fixture — construction and observed run

Fixture (all under `fixture-3page/`, `--root` = that directory):

- `home.html` — url `https://site.example/`, canonical self; alternates: `en`→`https://site.example/`,
  `en`→`https://site.example/de/`, `en_GB`→`https://site.example/de/`, `x-default`→self twice,
  `fr`→`/`, `es`→`https://other.example/`, and one alternate with no `hreflang` →
  `https://site.example/blog/`.
- `de.html` — url `https://site.example/de/`, canonical `https://site.example/`; alternates: `en`→home.
- `blog.html` — url `https://site.example/blog/`, canonical self; alternates: `en`→self, `en`→home,
  `en_US`→self.

Manifest (`fixture-3page/manifest.json`): three entries with ids `home`, `de`, `blog`, files
`home.html`, `de.html`, `blog.html`, and the three URLs above.

Command and observed output (exact; the JSON form is quoted in full below):

```
$ python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py \
    --manifest .ufo/waves/round-76/w1/ExecAuditTool/fixture-3page/manifest.json \
    --root .ufo/waves/round-76/w1/ExecAuditTool/fixture-3page
hreflang_missing_value page=home alternate has no hreflang value (href='https://site.example/blog/')
hreflang_invalid_tag page=home hreflang 'en_GB' is neither x-default nor BCP-47 under the frozen grammar
hreflang_relative_href page=home alternate href is not absolute with a host (href='/')
hreflang_duplicate_pair page=home pair (tag=x-default, href='https://site.example/') occurs again as occurrence 2
hreflang_multiple_xdefault page=home x-default 1 of 2 on one page
hreflang_multiple_xdefault page=home x-default 2 of 2 on one page
hreflang_nonreciprocal page=home target https://site.example/de/ declares no return alternate for tag=en_GB to https://site.example/
hreflang_external_target page=home target https://other.example/ (tag=es) is outside the manifest
hreflang_self_missing page=de no absolute alternate equals the page's own url https://site.example/de/
hreflang_canonical_not_self page=de canonical https://site.example/ is not the page url https://site.example/de/
hreflang_invalid_tag page=blog hreflang 'en_US' is neither x-default nor BCP-47 under the frozen grammar
hreflang_nonreciprocal page=blog target https://site.example/ declares no return alternate for tag=en to https://site.example/blog/
pages=3 findings=12 policy=11 info=1 input=0 exit=1
exit=1
```

The `--json` form of the same run (exit 1), verbatim:

```
{"version": 1, "pages": 3, "findings": [{"id": "hreflang_missing_value", "severity": "policy", "page": "home", "detail": "alternate has no hreflang value (href='https://site.example/blog/')"}, {"id": "hreflang_invalid_tag", "severity": "policy", "page": "home", "detail": "hreflang 'en_GB' is neither x-default nor BCP-47 under the frozen grammar"}, {"id": "hreflang_relative_href", "severity": "policy", "page": "home", "detail": "alternate href is not absolute with a host (href='/')"}, {"id": "hreflang_duplicate_pair", "severity": "policy", "page": "home", "detail": "pair (tag=x-default, href='https://site.example/') occurs again as occurrence 2"}, {"id": "hreflang_multiple_xdefault", "severity": "policy", "page": "home", "detail": "x-default 1 of 2 on one page"}, {"id": "hreflang_multiple_xdefault", "severity": "policy", "page": "home", "detail": "x-default 2 of 2 on one page"}, {"id": "hreflang_nonreciprocal", "severity": "policy", "page": "home", "detail": "target https://site.example/de/ declares no return alternate for tag=en_GB to https://site.example/"}, {"id": "hreflang_external_target", "severity": "info", "page": "home", "detail": "target https://other.example/ (tag=es) is outside the manifest"}, {"id": "hreflang_self_missing", "severity": "policy", "page": "de", "detail": "no absolute alternate equals the page's own url https://site.example/de/"}, {"id": "hreflang_canonical_not_self", "severity": "policy", "page": "de", "detail": "canonical https://site.example/ is not the page url https://site.example/de/"}, {"id": "hreflang_invalid_tag", "severity": "policy", "page": "blog", "detail": "hreflang 'en_US' is neither x-default nor BCP-47 under the frozen grammar"}, {"id": "hreflang_nonreciprocal", "severity": "policy", "page": "blog", "detail": "target https://site.example/ declares no return alternate for tag=en to https://site.example/blog/"}], "counts": {"policy": 11, "info": 1, "input": 0, "by_id": {"hreflang_missing_value": 1, "hreflang_invalid_tag": 2, "hreflang_relative_href": 1, "hreflang_duplicate_pair": 1, "hreflang_multiple_xdefault": 2, "hreflang_self_missing": 1, "hreflang_nonreciprocal": 2, "hreflang_canonical_not_self": 1, "hreflang_external_target": 1, "input_unreadable": 0, "input_duplicate_url": 0, "input_url_not_absolute": 0}}, "exit": 1}
```

Same bytes as `receipts/fixture-3page.stdout.txt` (which appends the `exit=1` line).

Why each of the 12 findings is there, under the amended rules:

`home` (8 findings):
1. `missing_value` — the last alternate has no `hreflang` (A10 covers the empty value; absence is C2's own
   sentence).
2. `invalid_tag` — `en_GB` fails the frozen grammar (`_` never accepted).
3. `relative_href` — `fr` → `/` has no scheme+authority; A4 forbids resolving it.
4. `duplicate_pair` — `(x-default, https://site.example/)` occurs twice; the second occurrence is the
   finding (A2).
5…6. `multiple_xdefault` twice — two x-default elements on a page with more than one; A2 is read as one
   finding per offending `<link>` element (interpretation I5).
7. `nonreciprocal` — `en_GB`→`/de/`; `de` declares no `en_GB` return.
8. `external_target` (info) — `es`→`other.example`, outside the manifest; exit stays 1 because of the
   policy findings (A1).

`de` (2 findings):
9. `self_missing` — its only alternate points at `home`, never at itself.
10. `canonical_not_self` — canonical `https://site.example/` ≠ `https://site.example/de/`.

`blog` (2 findings):
11. `invalid_tag` — `en_US`.
12. `nonreciprocal` — `en`→`home` because `home` declares no `en`→`blog` return.

The `home` `fr`→`/` relative href contributes to no self/reciprocity/external finding (A4); `home` is
self-listed by its absolute `en` and `x-default` links regardless.

## 4. Amendment 2 — cases whose verdict the amendment changed

These were re-marked from the pre-amendment derivation and re-derived under A1–A16. No case is scored
under both.

| Case | Before (my pre-amendment derivation) | After | Rule |
|---|---|---|---|
| `relative_href_absent_red` | exit 1, `hreflang_relative_href` | renamed `no_href_ignored_green`, exit 0, no ids | A9 |
| `alternate_stylesheet_red` | exit 1, `hreflang_missing_value` | renamed `alternate_stylesheet_green`, exit 0 | A13 |
| `relative_href_scheme_relative_red` | `{relative_href, external_target}` | `{relative_href}` | A4 |
| `relative_href_red` | `{relative_href}` (the relative href also resolved to self) | `{relative_href}` after adding an absolute self link so A4's non-resolution cannot also fire `self_missing` | A4 |
| `canonical_relative_resolved_green` | clean because `../dir/` resolved to self | renamed `canonical_relative_no_finding_green`; clean because a non-absolute canonical href contributes no canonical finding | A4; E1 |
| `multiple_xdefault_red` | 2 findings (one per page) | 4 findings (two x-default elements on each of two pages) | A2; E2 |
| `input_version_2` | exit 2, `input_unreadable` | exit 64, no ids | A15 |
| all cases | `class` field | `severity` field; info-only run exits 0 | A1 |
| every case | `pages` = readable-page count | `pages` = manifest `pages` length | A16 |

The fixture's total moved 11 → 12 for the same reason as `multiple_xdefault_red`. New cases added for the
newly decided classes: `invalid_tag_padded_red`, `structure_rel_uppercase_red`,
`structure_rel_mixedcase_green`, `self_missing_normalized_green`, `self_trailing_slash_red`,
`input_duplicate_url_normalized`, `input_duplicate_file`, `input_symlink_page`,
`input_parent_symlink_escape`, `canonical_with_hreflang_green`, `duplicate_pair_three_red`,
`multiple_xdefault_three_red`, `nonreciprocal_cycle_red`, `parser_svg_math_skipped_green`,
`parser_svg_selfclose_green`, `parser_script_selfclose_green`, `parser_noscript_scanned_red`,
`mixed_fault_and_policy`.

## 5. External matrix evidence (peer counter, read-only run by this seat)

`ExecAuditMatrix` reported two tool defects at 22:04; both were real and are fixed. Their counter, run
against this tool, now prints (verbatim tail of `receipts/matrix-peer.txt`):

```
cases=69 decided=66 correct=66 wrong=0 undecided=3 constants_failed=4/4 met=true
EXIT=0
```

Command:

```
$ python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py --root . \
    --tool .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py \
    --revision b758cb040d53374b1b63b89702c7128f77212d23 --work <scratch>/matrixwork2
tool_sha256=0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac
```

The constants each fail at least one decided case: `const_noop` 66/66, `const_report_all` 66/66,
`const_always_clean` 50/66, `const_empty_list` 45/66. Under Amendment 6 E3 the target is stated over
**decided** cases: 66/66 correct with 4/4 constants failed; the three `undecided` rows are excluded and are
never counted as passes.

The two defects and their fixes:

1. `invalid-tag-padded` — I had whitespace-trimmed the `hreflang` value, turning `" en "` into a valid
   tag and a duplicate pair. The frozen grammar is anchored, so the value is validated exactly as written;
   trimming was removed. Covered now by `invalid_tag_padded_red` (padded + unpadded same-href pair must
   yield one `invalid_tag` and no `duplicate_pair`).
2. `structure-rel-uppercase` — `rel_tokens` split the value but never lowercased the tokens, so
   `rel="ALTERNATE"` was not seen (A13). Fixed with ASCII lowering of every token. Covered by
   `structure_rel_uppercase_red` and `structure_rel_mixedcase_green`.

One peer case remains marked undecided that A15 now decides: `undecided-shared-file`. A15 says two pages
may not share a `file` and a path that is not a regular file is `input_unreadable`; the observed
`exit=2 ids=["input_unreadable"] pages=2/2` is the derivable verdict, so the case should be re-marked and
re-derived rather than excluded. The other two undecided rows (`undecided-svg-template-crossing`,
`undecided-unreadable-undecodable`) stay outside the score; see I14 and I17.

## 6. Retained-surface preview (for ExecAuditRealRun; not the official real run)

Census command and observed output: `receipts/retained-surfaces.txt`. Twelve directories exist under
`.ufo/waves/round-23/live/`; **eight** contain `page.html`, `manifest.json`, `fetch.json`, `audit.json`.
The other four — `charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi` — contain only
`audit.json` and `fetch.json`; each `fetch.json` records `status: 404`, `bytes: 13409`, sha256
`93ddca9a….c8fca966` (elided in prose; the full value is in the receipt), and no body was retained. That
matches A17 (8 served pages, four `not-served`), not §C2's "12 retained real surfaces" sentence. The
real-run seat can audit 8 and must state the four.

All eight retained `page.html` files match their `fetch.json.sha256` (8/8 `sha_ok=OK`), and the tool run
over them is clean:

```
$ python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py \
    --manifest .ufo/waves/round-76/w1/ExecAuditTool/preview-8/manifest.json --root . --json
observed: pages=8 findings=[] counts.policy=0 counts.info=0 counts.input=0 exit=0
   (the exact one-line JSON and the appended `exit=0` line are receipts/preview-8.stdout.txt)
```

Only `charter-ghp` carries hreflang declarations (`x-default` and `en`, both to its own URL, canonical
self); it is clean under C2. The other seven carry no `rel=alternate` at all. This preview measures the
retained 2026-10-21 bytes, not live serving.

## 7. Interpretations (L1: turn into amendments or tool fixes)

I1. **Non-language `rel=alternate`.** C2's first finding is literally "`<link rel="alternate">` with no
hreflang value", and A13 excludes only `stylesheet`. A feed alternate
(`<link rel="alternate" type="application/rss+xml" href=...>`) therefore yields
`hreflang_missing_value`. Probe observed: one such link → `hreflang_missing_value`, exit 1. If the intent
was "alternate links that carry `hreflang` only", that needs an amendment.

I2. **Whitespace.** `href` values are stripped of leading/trailing ASCII whitespace before comparison
(HTML's URL parsing); `hreflang` values are not trimmed (matrix-confirmed, §5). A3 does not state either.

I3. **Non-absolute canonical href.** A4's "contributes to no other finding (… canonical …)" is applied to
the canonical link itself: a relative canonical href produces no `hreflang_canonical_not_self` on that
page. Frozen as Amendment 6 E1; the alternative reading (unresolved ≠ page URL ⇒ finding) is not used.

I4. **Canonical link with no `href`.** Treated like I3 (frozen as E1): the page's canonical exists but has
no URL to compare, so no canonical finding. A9's "not an alternate" sentence speaks only of alternates.

I5. **`multiple_xdefault` granularity.** Frozen as Amendment 6 E2: one finding per x-default element on a
page that has more than one (2 → 2, 3 → 3), while `self_missing` and `canonical_not_self` stay once per
page. The peer matrix's `multiple-xdefault-pair` expects 4 for two pages × two x-defaults, matching this
reading.

I6. **`duplicate_pair` granularity.** One finding per repeat occurrence (2 identical → 1; 3 → 2).
`duplicate-pair-two-pairs` in the peer matrix matches.

I7. **`external_target` granularity.** A2 names policy findings; the informational class is emitted one
per absolute annotation by analogy.

I8. **URL normalization (A3) details.** Default port is removed only for `http:80` and `https:443`; other
schemes have no registry default in this tool. Percent-encoding, query and fragment text, and userinfo are
preserved; an empty `?`/`#` marker is not distinguished; IPv6 brackets are restored around the lowercased
host. Scheme need not be `http(s)` (A12).

I9. **Duplicate declarations use the same equality.** `input_duplicate_url` compares normalized URLs;
`input_duplicate_file` compares `posixpath.normpath(file)` so `a/./b` and `a/b` collide.

I10. **`pages` (A16).** The manifest `pages` list length, including entries that faulted (so a run with an
unreadable page still reports the manifest count). An unparseable manifest reports 0; a version-2 manifest
reports its list length in the exit-64 JSON object.

I11. **Input-fault severity name.** A1 names `info` and `policy`; input faults carry `severity: "input"`.

I12. **Usage JSON.** With `--json`, a `version != 1` manifest still prints the five-key object with
`exit: 64` (A16's parseable-object rule) and the usage message on stderr; without `--json` only stderr.

I13. **No size caps.** C2 states none; manifest and page files are read whole.

I14. **Non-UTF-8 bytes are not `input_unreadable`.** Pages decode as UTF-8 (BOM ignored) with a latin-1
fallback, so `b"\xff"` at offset 0 is readable text, not a fault. The peer matrix leaves this class
undecided; its observed verdict from this tool is exit 0. If C2's `input_unreadable` is meant to cover
undecodable bytes, that is an amendment plus a tool change.

I15. **No head restriction.** A6 says "first in document order", so the first `rel=canonical` anywhere
outside skipped regions counts; a body canonical is not rejected.

I16. **`rel` token set.** A link whose tokens include `stylesheet` (with `alternate`) is not an alternate;
`alternate` plus any other token (e.g. `feed`) is.

I17. **Subtree skipping.** `template`/`svg`/`math` are depth-counted; `<template/>` opens a subtree (HTML
ignores the slash) while `<svg/>`/`<math/>` open nothing (A13). Cross-boundary shapes
(`<template><svg>…</template>`) and SVG/MathML integration points are not modeled beyond this; the peer
matrix keeps that row undecided.

I18. **Duplicate attributes.** First occurrence wins (HTML parse rule); not stated in C2/A2.

I19. **A relative return cannot satisfy reciprocity.** A4 forbids resolving it, so a target that declares
only a relative return link still produces `hreflang_nonreciprocal` on the source annotation.

I20. **Empty `href`.** `href=""` is present, so the element is an alternate and yields
`hreflang_relative_href`; a missing `href` attribute is not an alternate (A9).

I21. **Finding `page` for input faults.** Manifest-level faults use `page: null`; per-entry faults use the
entry's `id`. A3's "the id in each finding names the page it was found on" is honored for page findings.

## 8. Limits and unclaimed checks

- No live fetch, HTTP headers/`Vary`, redirect inspection, rendering/JS, browser language negotiation,
  search-engine selection/ranking, or claim about a page's actual language. These are C2's stated limits.
- The parser is a bounded tolerant scanner, not an HTML tree builder (see the module docstring for the
  exact non-goals: implied tags, `<meta charset>` sniffing, foreign-content namespace rules, tag-soup
  recovery).
- The real-input run belongs to `ExecAuditRealRun`; §6 is a preview with the same manifest inputs and is
  not citable as that seat's receipt.
- Nothing in this seat's work was network-accessed. `grep -n "/tmp" hreflang_audit.py` → no match
  (`rc=1`). Imports are `argparse, json, os, posixpath, re, shutil, stat, string, subprocess, sys,
  tempfile, html.unescape, urllib.parse.urlsplit` — stdlib only.
- Manifest mode writes nothing: a `git status --porcelain` and per-file `stat` snapshot of the fixture
  before/after a run were identical (`git_status_same=yes`, `fixture_stat_same=yes`).
- No tool was installed or upgraded (`pacman` untouched); no PATH directory was modified.
- Scratch `/fast/scratch/hyaku/kake-r76/ExecAuditTool` held the work dirs, probes and matrix runs; every
  receipt was copied into `w1/ExecAuditTool/receipts/` before `rm -rf -- <scratch>`.

## 9. Handoff notes for the L1

- Copy `w1/ExecAuditTool/hreflang_audit.py` to `scripts/hreflang_audit.py` as-is; the file is
  self-contained and repositionable (no relative data dependencies).
- The peer matrix already scores this exact hash `correct=66/66 met=true` over decided cases; Amendment 6
  E3 fixes that target and excludes the three undecided rows, and `ExecAuditMatrix` may re-run for the
  receipt. `undecided-shared-file` is derivable under A15 as exit 2 / `input_unreadable`, but E3 excludes
  the undecided residue from the score either way.
- The two Amendment 6 readings (E1 non-absolute canonical, E2 `multiple_xdefault` multiplicity) were
  already implemented here before the freeze; no tool change is needed for E1–E3.
