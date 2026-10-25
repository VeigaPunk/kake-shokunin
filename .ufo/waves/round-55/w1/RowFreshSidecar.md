# RowFreshSidecar

Seat: C1 coverage-map calibration, one new coverage-map row for
`corpus/knowledge/freshness-sidecar.json`. Lane repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`, base revision
fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d, round date 2026-10-25.

Read: the whole knowledge file (275 lines, 30 entry objects, 15 616 bytes by `wc -c`);
`corpus/README.md` header (lines 1-14) and the full
`## Coverage map` table (lines 15-45, header row plus 27 existing rows) for the exact
`| Area | Entry | Coverage |` format. No file was edited; no git/jj mutation; no
network; no pacman; no campaign tool run.

ROW:

```markdown
| Local-path freshness sidecar | `knowledge/freshness-sidecar.json` | 30 entries, each naming a cited file and line number, a `~/Projects/...` path token, the line SHA-256, kind `absent` or `restored`, date 2026-10-21, and a note carrying the `test -e` exit code and marking the citation historical. |
```

Cell checks (all run, output observed):

- Area = 3 whitespace tokens (limit 8). No round tag emitted: regex `r\d\d|round \d\d`
  over the file returns 0 matches, and the file's only header is the `schema` key, so
  there is no round tag in the file to carry.
- Entry = backticked `knowledge/freshness-sidecar.json` with no ` (S###)` suffix:
  `S\d{3}` over the file returns 0 matches, and the file has no `source:` line — its
  per-entry keys are `file`, `line`, `token`, `lineSha256`, `kind`, `date`, `note`
  (verified by parsing the JSON; key union = exactly those seven).
- Coverage = 37 units (limit 10-45); contains `|`: no; starts with `TBD`: no.
- Coverage shares 5+ letter words with the file's first 1500 characters: `entries`,
  `token`, `historical`, `absent`, `Projects`. The file has no H1 line (`#` at start:
  no), so the first-1500-character half of the rule is the only applicable half.
- Row line splits on `|` into exactly 3 cells matching `| Area | Entry | Coverage |`.
- "30 entries" is a measured property of the file, not a copied prose count: JSON parse
  gives `len(entries) == 30` and `grep -c '"file":'` = 30. The file states no count in
  prose (see RISKS 5).
- No duplicate row risk: `grep -n 'freshness-sidecar' corpus/README.md` returns no
  match, so the file is absent from the existing coverage map.

EVIDENCE (each passage is an ASCII-double-quoted raw substring of the cited lines,
verified by Python `in` over the file bytes; unit counts in parentheses):

1. `corpus/knowledge/freshness-sidecar.json:2` — "kake-paths-sidecar-v1" (1 unit), and
   `:3` "entries" (1 unit) → grounds the schema string and that the body is an `entries`
   array.
2. `corpus/knowledge/freshness-sidecar.json:5,7` — "corpus/knowledge/drift-detection.md"
   (1 unit) and "~/Projects/plazir-15-site" (1 unit); the `line` key between them holds
   77 → grounds "each naming a cited file and line number" and "a `~/Projects/...` path
   token".
3. `corpus/knowledge/freshness-sidecar.json:8-10` —
   "41c223b664b859f2669df3a8e69e5e1c81aecaf74facd72cc9f36fc01db10a55" (1 unit),
   "absent" (1 unit), "2026-10-21" (1 unit) → grounds "the line SHA-256", "kind `absent`
   or `restored`" (the `restored` spelling appears 26 times in the file) and the date.
4. `corpus/knowledge/freshness-sidecar.json:11` — "absent (test -e exit 1)" (5 units)
   and, same line, "is a historical record, not an executable instruction" (8 units) →
   grounds the `test -e` exit code and "marking the citation historical". The `restored`
   notes carry the same shape: "present (test -e exit 0; checkout 1fbdb8ed)" (7 units).

RISKS:

1. **Seven stale line digests in the file (found, not repaired).** Of the 10 `SKILL.md`
   bindings, lines 364, 423, 431, 445, 448, 449, 450 hold `lineSha256` values that match
   neither base fcaf4b85 nor the worktree (`SKILL.md` is 1223 lines in both; the other
   three bindings at 16, 19, 20 match both). Lines 448 and 449 show a one-line shift
   signature: recorded(448) = actual(449) and recorded(449) = actual(450). The remaining
   20 non-`SKILL.md` bindings all verify against the worktree. Consequence: the row
   describes the digest field accurately, but the field's values are partly wrong.
   `scripts/freshness-sweep.mjs:382` throws when `sha256(line) !== e.lineSha256`, and
   `corpus/knowledge/freshness-sweep.md:197` states stale hashes fail closed (exit 2), so
   this file would currently break `loadPathSidecar`. The sweep itself was **not run**
   (out of this seat's scope; the failure mode is read from the code path, not observed).
2. **All 30 entries are dated 2026-10-21**, four days before the round date. The row says
   the date but cannot say the recorded present/absent states still hold on 2026-10-25;
   nothing in the file re-checks, and re-checking is not this seat's claim.
3. **Verification limits stated inside the notes**: the `restored` notes end with
   "Deployment, chat binding and byte continuity with the historical checkout remain
   unverified." The row must not imply those were verified; it does not.
4. **No H1 and no `source:` line**, so the row carries neither a round tag nor ` (S###)`
   ids — unlike neighbouring rows such as `knowledge/field-performance-cwv.md` (S036–S039).
5. **The file states no count.** "30 entries" is derived from the array length; if a later
   edit adds or drops an entry the row goes stale silently. The `absent`/`restored` split
   (4/26) and the 7 distinct tokens are omitted from the row for length and because
   enumerating them adds no navigational value; the row therefore does not claim them.
6. **Naming drift in the file itself**: the `schema` value is `kake-paths-sidecar-v1`
   and `corpus/knowledge/freshness-sweep.md:197` calls it the "paths sidecar", while the
   filename is `freshness-sidecar.json`. The row follows the filename (Entry cell must
   name the file) and repeats the schema string verbatim.
7. **Consumer outside the file's own text**: `scripts/freshness-sweep.mjs` loads this
   path, validates `schema === 'kake-paths-sidecar-v1'` and the entry key shape, and
   indexes it by `file:line:token`. That is a real use of the file, but it is not
   traceable to the file's own text, so the row does not assert it.
8. **Unexpanded reference**: the notes say "earlier W7 attribution historical" without
   any W7 record or link inside the file; the row cannot explain it and does not try.

VERDICT: One coverage-map row drafted for `knowledge/freshness-sidecar.json` (3-token Area, no round tag or S-ids because the file has neither, 37-unit Coverage sharing `entries`/`token`/`historical`/`absent`/`Projects` with the first 1500 characters); all four evidence passages are verified raw substrings, and the file carries seven stale `SKILL.md` line digests that would fail the freshness sweep's digest check.
