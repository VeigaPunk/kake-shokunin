# ScribeLesson — round 84 wave w1

Delivered `corpus/lessons/round-84.md` — 170 lines / 14,634 bytes, sha256
`fe0c3ee8a0e051654ca9f64f54e5306cc5b2f4de10c282b53869f17976dae417`
(`.ufo/waves/round-84/w1/ScribeLesson/lesson-file.txt`). The file carries the required sections in
the required order: header with lane, round 84, attempt 1, base `fe42ad11…`, freeze `f358022f…` and
the two claims on their axes (`C1` calibration, score 2; `C2` freshness, score 10, capability
acquisition); `## Corrections` with one row per `D1`–`D4` and the file that re-derives each; the
`[r84-correction 2026-11-04]` line; exactly one `D2 count=66 span=838-844 measure=words-full-span`
line; a line naming `controls/census-before.txt` and its 22 `W04`; `## Gate` for `S457` with one
admit and three rejects (reason + flip condition each), the URLs, the 2026-11-04 access date and
≤25-word located quotes; and `## Mistakes` with five `class · evidence pointer · captured-by · fix`
rows. A short `## Risk` and `## Author-side status` follow; neither claims an after-state.

## Commands and exits

| Command | Exit | Reading |
|---|---|---|
| `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root .` before the lesson | 1 | `items=4 open=3 closed=1 met=false` — `D4` closed (22=22), `D1`/`D2` had no lesson line, `D3` no results (`counter-worktree-before-lesson.txt`) |
| same counter `--revision fe42ad11eb1084ad2ea68d12c5bbb2922a089868` | 1 | `items=4 open=4 closed=0` — the freeze's `controls/` are not in the base tree, so `D4` reads its receipt absent (`counter-at-base-revision.txt`) |
| `python3 -c 'import re; t=open(".ufo/waves/round-83/w1/ScoutSources/rfc9111.txt",encoding="utf-8",errors="replace").read(); L=t.splitlines(); print("nlines",len(L)); print("derived",len(re.findall(r"\S+","\n".join(L[837:844]))))'` | 0 | `nlines 1956`, `derived 66` (`d2-oneliner.txt`; full seven-line span also in `d2-count.txt`) |
| `python3 -c` raw-substring test of the four RFC 9111 headings over the same file | 0 | all four `True`, each `count=2` (`d1-heading-raw.txt`) |
| `grep -n '^5\.2\.2\.[12]\.  ' .ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` | 0 | `1208:5.2.2.1.  max-age`, `1222:5.2.2.2.  must-revalidate` (`d1-section-grep.txt`) |
| `grep -c $'\tW04\t' .ufo/waves/round-84/controls/census-before.txt` | 0 | `22` |
| `python3` census re-derivation via `c84_defect_queue.census_w04` + same-URL counterfactual | 0 | `rows 196 derived_w04 22`; `S457` normalizes to `httpwg.org/specs/rfc9111.html`; a second row on `S456`'s URL with a distinct scope gives 23 and a new `S457` collision (`d4-census-w04.txt`) |
| `sha256sum` on both retained copies | 0 | `.txt` `aeb52adb…` (identical to round 83's retained copy), `.html` `999f4013…`, 178,573 bytes |
| `python3` quote-location script over four spans, both renderings | 0 | 24 / 16 / 8 / 24 words; each a normalized substring of the `.txt` and of the HTML line and visible text (`gate-quote-check.txt`) |
| `python3 -B .ufo/waves/round-84/c84_defect_queue.py --root .` after the lesson | 1 | `item=D1 closed=1 state=1 row=1 four real headings cited and retained`; `item=D2 closed=1 state=1 row=1 claimed=66 derived=66`; `item=D4 closed=1 … 22=22`; `item=D3 closed=0 … w1-results.json absent`; `open=1 closed=3 met=false` (`counter-worktree-after-lesson.txt`) |

## D1 — real headings, measured

The retained bytes at `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` (84,477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`) contain `5.2.  Cache-Control`
(two spaces, line 1081), `5.2.1.  Request Directives` (1111), `5.2.2.  Response Directives` (1203)
and `5.2.3.  Extension Directives` (1408), each twice (table of contents and body). The correction
line cites those four verbatim and names `corpus/lessons/round-83.md` §`Gate`; the counter's `D1`
therefore reads `state=1 row=1`. Round 83's `Common Cache-Control Directives` title is quoted in
the correction only to mark it absent from the retained bytes.

## D2 — one count, one boundary

`len(re.findall(r"\S+", "\n".join(lines[837:844])))` over the retained file is **66**. The seven
physical lines (838–844 inclusive) begin `Another validator is the entity tag given in an ETag
field` and end `the listed entity tags).`; dropping the final parenthetical would be the 48 round 83
recorded, which is why the lesson states the full-span measure and boundary.

## D4 — census receipt and the W04 risk

`controls/census-before.txt` records `census_exit=0`, an `ok` line naming
`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, and 22 `W04` lines. The counter
re-derives 22 from the current `corpus/SOURCES.md` **after** `ScribeRegistry` appended `S457`
(line 204, URL `https://httpwg.org/specs/rfc9111.html`), because that URL is not `S456`'s
(`https://www.rfc-editor.org/rfc/rfc9111.txt`). The counterfactual is measured, not assumed: the same
row on `S456`'s URL with a distinct scope raises the derived set to 23. That is the lesson's
`## Risk` note; the frozen counter is not patched.

## Gate — what was decided

Admit `S457` (status `mined`, `opened=2026-11-04`, `recheck=180d`, `used-by`
`corpus/knowledge/policy-value-classes.md`), anchored on `https://httpwg.org/specs/rfc9111.html`,
HTTP 200, 178,573 bytes, sha256 `999f4013…`, with admissibility quotes of 24 and 16 words at
`rfc9111.txt` 1214–1216 / HTML line 282 and `rfc9111.txt` 587–588 / HTML line 269. Rejects: §4.1's
`reordering field values when order is not significant` as the ground for `reordered` (8 words;
`Vary` request matching, not response directive order); §5.2.1.1's request `max-age` (24 words,
1122–1124; a client preference, not a response header); and the wave spec's `§5.2.2.2`/`max-age`
pairing (the bytes put `max-age` at §5.2.2.1 and `must-revalidate` at §5.2.2.2). Each reject states
the observation that would flip it.

## Findings not central to the lesson

- The `w1-spec.json` `ScoutSources` item pairs `§5.2.2.2` with `max-age`; the retained bytes put
  `max-age` at `5.2.2.1.` (1208) and `must-revalidate` at `5.2.2.2.` (1222). Reported as the
  `section-number` mistake row; the registry row's anchor cell records the same correction.
- `ScoutSources/fetch-meta.txt` and `fetch-meta-httpwg.txt` carry `http_code`, `url_effective`,
  `content_type` and `size_download`, but no RFC 3339 fetch stamp and no sha256, though the item
  asked for both. The Gate says so and recomputes both digests from the retained bodies; the access
  date rests on the row's `opened` cell and the wave's run date. This seat made no network call.
- The counter's `D4` compares the frozen before-receipt to the **measured** tree, so a future round
  that adds a second registry row on a held URL with a distinct scope should expect `D4` to reopen.
- `corpus/knowledge/policy-value-classes.md` was present when this seat read it (14,271 B then,
  14,392 B at the final check — another seat was still writing) and its `source:` line cites `S457`,
  the httpwg URL and the txt rendering for its quoted spans; this seat did not edit it.

## Files touched

Production: `corpus/lessons/round-84.md` only. Receipts: eleven files under
`.ufo/waves/round-84/w1/ScribeLesson/` (`counter-worktree-before-lesson.txt`,
`counter-at-base-revision.txt`, `counter-worktree-after-lesson.txt`, `d1-heading-raw.txt`,
`d1-section-grep.txt`, `d2-count.txt`, `d2-oneliner.txt`, `d4-census-w04.txt`,
`gate-quote-check.txt`, `s457-row.txt`, `lesson-file.txt`). No sibling repo, fleet-root, `considerthese/`
or `corpus/SOURCES.md` write; no VCS mutation; no scratch directory was created (no clones, fixtures
or counter work dirs), so nothing is left behind; no tool install or upgrade.

## Limits

- C1's after-state is not claimed. `D3` needs `.ufo/waves/round-84/w1-results.json`, which WAVE-DONE
  produces; at this writing the counter exits 1 with `open=1 closed=3 met=false`. The L1's after
  receipt is the reading of record.
- The Gate is author-side. Admission belongs to the non-author closure, which owes the independent
  re-open of the retained `.txt` and `.html`, the line-level quote check for `S457`, and a decision on
  the three rejects.
- The 2026-11-04 access date is the row's `opened` date and the wave's run date; the scout's
  metadata files carry no fetch timestamp, so this seat does not claim one.

## Verdict

Delivered: `corpus/lessons/round-84.md` with D1–D4 corrections (real RFC 9111 headings, one D2
measurement on the 838–844 boundary, the connector seat named, the census-before receipt line), the
`S457` Gate with one admit and three reasoned rejects, and five mistake rows; measured C1 state at
this writing is `open=1 closed=3 met=false` (`D3` awaiting WAVE-DONE), and no after-state is claimed.
