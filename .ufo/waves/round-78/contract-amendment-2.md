# kake round 78 — contract amendment 2 (terms only, before any after-state)

Recorded 2026-11-03 after the critic's pre-run attack found four sizing defects in C3 and after
the L1 re-read the opened source for its exact line pointers. No C3 after-state exists when this
amendment is written (`scripts/meta_robots_audit.py` is still absent from the tree), so no case has
been decided. C1 and C2 are untouched.

This amendment **tightens** the C3 predicate and fixes the amendment-1 receipts. It is the C3
analogue of the round-77 g03 repair: a tool that echoes the label it was handed must not pass.

## B1 — the tool never sees the expectation (label leak)

Amendment-1 text had the tool read `expect.effective` / `expect.findings` and report
`meta_robots_expected_mismatch`. A five-line tool that echoes the manifest's `expect` would then
satisfy every case while opening no HTML, and the four constants (which do not read `expect`)
would still fail ≥1 case, so `constants_failed == 4` and `met == true`.

**Corrected interface.** The manifest a tool reads is:

```json
{"schema":"kake-meta-robots-manifest/v1",
 "agents":["robots"],
 "checks":[{"id":"<id>","path":"<lane-relative html>","url":"https://…"}]}
```

`expect` never appears in that manifest. The matrix keeps each case's `expect.json` beside the
manifest and compares against it; a mismatched case is the matrix's finding, not a tool finding.
`meta_robots_expected_mismatch` is therefore **removed from the tool's finding vocabulary** —
the tool never knows an expectation.

## B2 — the tool's stdout schema is defined

With `--json`, the tool prints exactly one JSON object on stdout:

```json
{"version":1,"checks":[{"id":"<id>","effective":["follow","index"],
                        "findings":["meta_robots_ignored_rule"]}]}
```

- `checks` lists one object per processed check, in manifest order.
- `effective` is the sorted effective-set list from the closed vocabulary
  (`index`, `noindex`, `follow`, `nofollow`, `all` is never emitted, `none` expands,
  `nosnippet`, `indexifembedded`, `noimageindex`, `notranslate`, `max-snippet:<n>`,
  `max-image-preview:<none|standard|large>`, `max-video-preview:<n>`,
  `unavailable_after:<input-as-written>`).
- `findings` is the sorted, de-duplicated list of finding ids for that check.
- On an input or check fault (missing file, bad manifest JSON, duplicate check id) the tool prints
  `{"version":1,"error":"<code>"}` and exits 2; no per-check objects are required then.
- Without `--json` the tool prints a human summary; only the JSON form is compared.

The closed finding vocabulary (exactly these five):
`meta_robots_empty_content`, `meta_robots_invalid_value`, `meta_robots_unknown_directive`,
`meta_robots_tag_outside_head`, `meta_robots_ignored_rule`.

## B3 — `correct` compares three fields

Frozen text compared only the finding-id set and the exit code, so a tool that reports no
findings on a clean-looking page passed regardless of the effective set — the claim's primary
output. **Corrected:** a case is `correct` iff the tool's exit code, its `effective` list and its
`findings` list all equal the case's `expect.json`. A case whose exit is 2 is correct iff the
tool's exit is 2 and its `error` code equals the expected one (no effective/findings comparison).

## B4 — the case-id set is frozen

`cases == decided` is self-referential if the directory defines the set: a missing family would
read as a pass. **Corrected:** the frozen case set is the 34 ids below. The matrix requires the
`--cases` directory to hold exactly these ids (missing or extra → `met=false` with a named
finding) and reports `cases=34` from the frozen list, never from a directory count.

```
g01_absent_tag            g02_noindex               g03_none_expansion
g04_all_default           g05_index_follow_one      g06_conflicting_noindex
g07_conflicting_nofollow  g08_max_snippet_two       g09_max_image_preview_two
g10_max_video_no_limit    g11_max_snippet_invalid   g12a_unavailable_datetime
g12b_unavailable_date     g12c_unavailable_rfc822   g13_unavailable_invalid
g14_uppercase             g15_empty_content         g16_unknown_directive
g17_googlebot_ignored     g18_googlebot_with_agents g19_body_tag_respected
g21_self_closing          g22_single_quotes         g23_noarchive_ignored
g24_trailing_comma        g25_nosnippet_dominates   g26_max_snippet_zero_video_minus_one
g27_indexifembedded       g28_within_content_conflict g29_max_image_preview_none
g30_max_snippet_minus_one g31_missing_content       g32_nocache_ignored
g33_lowercase_t_z         g34_missing_file_exit2    g35_duplicate_id_exit2
```

(The `g20` id is retired unbuilt: with B1 there is no tool-side expectation finding, so the
"declared noindex against an index expectation" scenario is the matrix's own comparison, exercised
by its selftest and by the constants.)

## B5 — the tool's selftest is part of `met`

Frozen text required `--selftest ≥ 40` as a deliverable but never ran it. **Corrected:** the
matrix runs the tool's `--selftest` from the same revision's blob; it must exit 0 and print a final
line `selftest: P/T passed` with `P == T ≥ 40`. `met` gains the conjunct `selftest_ok`.

**Predicate (final):** `met <=> cases == 34 and decided == 34 and correct == 34 and
constants_failed == 4 and selftest_ok`.

## B6 — grammar terminals amendment 1 left open

- **RFC 822:** accept the canonical form with an optional weekday and comma —
  `[EEE,] D Mon YYYY HH:MM:SS ZONE` — where `ZONE` is `GMT|UT|UTC|EST|EDT|CST|CDT|MST|MDT|PST|PDT`
  or a `±HHMM` numeric zone, plus the page's own `DD Mon YYYY HH:MM:SS ZONE` form.
- **RFC 3339:** lowercase `t` and `z` are accepted (RFC 3339 §5.6 permits them; `rfc3339.txt:425`).
- **RFC 850:** declared **not implemented** (limit). A value in that form yields
  `meta_robots_invalid_value`; the limit is stated in the knowledge entry, and the flip is a case
  that pins it.
- **`indexifembedded`:** this is a declaration audit, not a crawler simulation. `indexifembedded`
  enters the effective set whenever declared (it only *has an effect* with `noindex`); no
  "most restrictive" clause applies to it, and the expected list for g27 is
  `["follow","index","indexifembedded","noindex"]`.
- **`missing content` attribute** ≡ empty content → `meta_robots_empty_content`, effective set =
  default.
- A `meta` element carrying `http-equiv` and no `name` is not a robots tag and is never counted.

## Pointer corrections to amendment 1 (append-only)

Amendment 1's line pointers were written before the stripped text was re-read; the quotes are
correct but several pointers were not. Corrected pointers in `w1/L1Sources/robots-meta-tag.txt`:
A1 quote → `:242-243` (place-in-head sentence `:208-209`); A2 quote → `:400-403` with the
date-only example at `:410`; A3 "aren't used by Google Search and are ignored" → `:412`, with the
rule list `:414-432`; A4 numeric-ignored → `:334` and `:383`, date-ignored → `:404`;
A5 conflicting-rules quote → `:280-282`, `max-snippet:0` → `:338-339`, `-1` no limit → `:341-343`
and `:381`. `indexifembedded` is `:317-323`. The 404 URL's body size was measured twice on
2026-11-03: the L1's own GET (47,506 B) and the scout's retained raw (47,502 B) — both are recorded,
neither is used as evidence. `[r78-correction 2026-11-03]`
