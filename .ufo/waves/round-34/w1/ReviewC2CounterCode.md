# ReviewC2CounterCode — attack on .ufo/waves/round-34/c2_source_census.py

Sandbox: /fast/scratch/hyaku/kake-r34/w1/ReviewC2CounterCode/ (clone checked out at the frozen
wave rev a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f; lane working-tree copy verified byte-identical
to that rev, 251 lines). Baseline: at a2fe31b the counter gives met=0/5, exit 1, with JSON, and its
recount of the retained 102-page archive succeeds: pages=102 og:title=87 og:type=87 og:image=1
og:url=87 all-four=1 og-url-equals-canonical=87 (baseline.json in the sandbox). Because the entry,
lesson Gate and S067-S070 registry rows do not exist yet, I built a minimal compliant baseline
G=dcc120be7da125e0cc419d9f79d31039fbc5704e (4 registry rows in the real 11-cell shape, entry with
cites after line 8 + census line, lesson `## Gate` quotes taken from the retained S06x.txt, control
asserted) → met=5, exit 0. All mutants below are sandbox commits reachable by short sha in the
sandbox clone; every run is `python3 -B .ufo/waves/round-34/c2_source_census.py --root <clone>
--revision <rev>`. No lane file except this report was touched; no pacman installs.

## Defects (severity-ranked)

- **D1 HIGH, false positive — fence state is not tracked before line 8 of the entry, so junk
  reaches 5/5.** `entry_body = unfenced(entry.splitlines()[8:])` starts fence tracking at line 9;
  a fence opened in lines 1-8 makes every later in-fence line count as unfenced, for both
  condition b and the census (condition e), which the docstring requires "outside fenced code".
  m1=40c898c3169e808303981ff7c25494cbb5cacf4d: entry with ``` on line 3 and line 16, the only
  S067-S070 cites (line 12) and the census line (line 14) inside that fence → rc=0, met=5/5,
  census.statedLines=1. The rendered entry contains no visible cite and no visible census.
- **D2 HIGH, false positive — condition a searches the Registry section fence-blind.** Rows come
  from `section_lines(registry, "## Registry")` with no `unfenced` filter (unlike the entry), so a
  compliant-looking row inside a code block passes a_row. m2=465a0854b3effc7cfecc84c56adea39591211f9a
  (real S067 row deleted, identical row inside a fenced block inside `## Registry`) → rc=0, met=5/5.
  The counter also never requires the line to sit in a rendered table — any `| S067 |…` prose line
  in the section counts (spec looseness, same direction).
- **D3 MEDIUM, parser/renderer divergence via escaped pipes — regression of the round-33 F3 fix.**
  The naive `row.strip().strip("|").split("|")` (no `(?<!\\)\|`) mishandles `\|`:
  (a) false negative — m3=0e00de1d436fcb1a570a01c47b19831321a3cdd9 puts `ogp.me\|site` in the source
  cell of a GFM-legal row → naive split adds a cell, cells[7] shifts off `mined`, a fails → rc=1,
  met=4/5; (b) false positive — m4b=44fdccd666e5864927848a47839de487af26b2a7 renders status cell
  `x\|mined` followed by `2026-10-22`: the rendered table's 8th cell is `2026-10-22` (not `mined`),
  yet naive splitting yields cells[7]=`mined`, cells[8]=`2026-10-22` → a_row=True, rc=0, met=5/5 —
  the counter checked a row that no renderer would produce. (`\\|` is handled correctly by the
  naive split; the round-33 lookbehind over-merge of `\\|` is inverted here, not present.)
- **D4 MEDIUM, crash paths on malformed input violate "exit 0 when the count ran … 2 on bad
  input" — all three exit 1 with a traceback and no JSON:**
  - m5=99588be56db2b419cb20763296b8d8f89e611c4c: receipts.json `"url": 123` →
    `TypeError: 'in <string>' requires string as left operand, not int` at `url and url in cells[1]`.
    Repo-controlled bytes (retained receipts) are enough to trigger it.
  - m6=41f0e0d39007300e17c43981c000a24eec49ac64: census line with a 5000-digit `pages=` value
    matches `\d+`, then `map(int, …)` → `ValueError: Exceeds the limit (4300 digits)`. Same
    defect class as round-33 N2 (int on unbounded digit run).
  - m8b=503a71af740723f765dd9e66fdbc55b9b86a3df8: retained page with
    `<link rel="canonical" href="http://[">` → `urljoin` raises
    `ValueError: Invalid IPv6 URL` inside recount (probe: urljoin('https://ds4cc.com/x/','http://[')
    raises). Upstream-controlled rather than repo-controlled, but the docstring's bad-input
    promise does not hold.
- **D5 LOW, census-position doc/code mismatch, both directions.** Docstring e: "the entry carries
  exactly one line outside fenced code of the form …" with no position constraint; the code only
  searches lines 9+. m7b=614a4f54cd65e02965521c08df1756f237bb8d6a (correct census line on line 2,
  cites after line 8) → statedLines=0, rc=1, met=4/5. m7c=8634dfe2e8f6f26b83e8b36fa5f7b3df608cc017
  (wrong census line `pages=0 …` on line 2 plus the correct line after line 8) → rc=0, met=5/5 with
  statedLines=1: the docstring's "exactly one" is violated but the extra line is invisible.
- **D6 LOW, false negative — `## ` toggling is fence-blind (round-33 F4 still present).**
  section_lines treats a fenced `## …` line as a heading. m9=e3f3867e45df7ce13c8362395f4ec2780e382f12
  (fenced `## fenced heading` inside `## Registry` before the rows) → rows lost, met=1/5, rc=1.
  Same shape would truncate `## Gate` and break c.
- **D7 LOW, recount vs HTML spec — duplicate attributes.** The attrs dict comprehension keeps the
  LAST occurrence; HTML parsers keep the FIRST. Probe: `<meta property="og:title" content="a"
  property="og:url" content="b">` → counter records only og:url=b. A page can therefore be counted
  differently from what a browser/OG scraper sees. (No effect demonstrable on current retained
  bytes; divergence only.)
- **D8 LOW, fence-detector divergences.** `^\s{0,3}(`{3,}|~{3,})` accepts a tab-indented ``` as a
  fence (probe: True; GFM says tab indent makes it an indented code block, fence literal), and
  accepts a closing-fence line with trailing info text. Also a first `<link rel=canonical>` without
  href is skipped and a later canonical link IS adopted (probe: href `/x/` picked), while the
  docstring says "the first <link rel=canonical> href".
- **D9 LOW, Unicode-aware regexes accept non-ASCII census lines.** Probe (exercised): a census
  line with `pages=२२` matches `\d+` and int()s to 22; a trailing U+00A0 passes `\s*$`. The
  frozen form is ASCII; cosmetic, but the accepted language is wider than the docstring's `N`.

## Checks with no defect

- b word-boundary: `\bS067\b` rejects `S0670` (probe: no match) — round-33 N3's entry-cite shape is
  fixed here; the row first cell uses anchored regex + `cells[0] == sid` equality.
- Census integrity chain is sound: first tree.txt line must equal `commit 7fc6aa2f…`, every other
  line must be a blob .html ls-tree line, pax comment must equal COMMIT, path sets must be equal,
  and every member is re-hashed as a git blob (sha1 of `blob <len>\0` + bytes). My m8 first attempt
  (tar built without the pax comment) was cleanly rejected with
  "archive pax comment is not the pinned commit" — the pax check actually bites.
- Recount semantics match the docstring: literal lowercase `property="og:X"`, content stripped of
  exactly HTML ASCII whitespace (WS = " \t\n\r\f", correctly excluding \v), page counted once via
  any(), first non-empty og:url, first canonical token match case-insensitively via
  `.lower().split()`, urljoin resolution against `https://ds4cc.com/<path>` with trailing
  `index.html` (incl. root `index.html` → site root), all-four and og-url-equals-canonical follow.
- Exactly-one census line (post-line-8, unfenced) enforced: 0 or ≥2 matching lines fail the census.
- a/c section windows reject preamble decoys: rows are searched only inside `## Registry`
  (round-33 F1 fix carried over); heading equality is `line.strip() == heading` so trailing-space
  headings (round-33 N4) now toggle correctly; `### …` does not match `## `.
- d: sha256 over raw retained bytes, `status == 200` strict, quote must be a collapsed substring of
  the collapsed text; quote selection requires exactly one 6-25-word curly-quoted span on exactly
  one `- <id> — ` Gate line. Control (flip_letter not in text) asserted for all four baseline
  quotes; a control hit forces exit 1 (code-read).
- receipts parsing is type-guarded (non-dict receipts/rec → checks fail, no crash — m5's crash is
  the non-string url value only). GIT_* env vars stripped before every git call. Revision-not-found
  path returns exit 2 with JSON (code-read; not run).

## Not verified

- Performance/DoS (huge entry, unbounded tar members into memory) — not tested.
- HTMLParser behavior on deeply pathological nesting beyond the one malformed page in m8b.
- Whether the L1's actual future entry/lesson/registry wording trips any D5/D8 false negative.
- Exit-2 bad-revision path only code-read. Round-33 holds (counter-trust and sandbox-threat-model
  questions) were not touched.

## Commands

- `git clone -q <lane> clone && git -C clone checkout -q a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`
- `python3 -B clone/.ufo/waves/round-34/c2_source_census.py --root clone --revision a2fe31b…` → exit 1, met 0/5
- Battery: `python3 -B build_mutants.py` and `python3 -B round2.py` (sandbox;
  /fast/scratch/hyaku/kake-r34/w1/ReviewC2CounterCode/{build_mutants.py,round2.py,baseline.json,round2.out})
- Per mutant: same counter invocation; observed rc/met pairs are quoted per defect above.

Tooling: none installed (pacman paused; host python3 3.14.8 and git sufficed).
