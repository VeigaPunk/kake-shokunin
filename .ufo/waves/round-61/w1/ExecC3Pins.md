# ExecC3Pins

Claim C3 pin table. Read-only over the registry: `corpus/SOURCES.md` is unchanged by this seat (`git status
--porcelain corpus/SOURCES.md` empty); the edits below are proposals for the L1 to apply. Base revision
`9f07731a873585e655a6518233ea39f5d9fb8204`, access date 2026-10-27. Artifacts live in
`.ufo/waves/round-61/w1/ExecC3Pins.files/`: `pins.tsv`, `proposed_rows.tsv`, `pin_replacements.txt`,
`pin_cells.json`, `compute_pins.py` (re-runnable), `anchor_probe.py` + `anchor_probe.tsv` (independent cross-check).

## PINS:

Rule as frozen in the contract: pin a row when its fetch is HTTP 200 **and** the anchor material still occurs in
the fresh body → the recheck cell moves from its cadence to `opened + cadence` (`Nd` cells) or `opened + 90d`
(`on-release`/`on-use` cells). `opened` is 2026-10-19 for all ten due rows; the cell is field index 10 of the
`|`-split registry row (13 fields per row).

| row | old cell | new cell | basis |
|---|---|---|---|
| S002 | `on-release` | `2027-01-17` | opened + 90d (non-`Nd` cadence); anchor clause `v4.0.0 What's Changed` |
| S003 | `90d` | `2027-01-17` | opened + 90d |
| S004 | `90d` | `2027-01-17` | opened + 90d |
| S005 | `90d` | `2027-01-17` | opened + 90d |
| S006 | `90d` | `2027-01-17` | opened + 90d |
| S007 | `90d` | `2027-01-17` | opened + 90d |
| S008 | `365d` | `2027-10-19` | opened + 365d |
| S009 | `365d` | `2027-10-19` | opened + 365d |
| S010 | `365d` | `2027-10-19` | opened + 365d |

S001 is **not** pinned: see `SKIPS`. Nine pins, one carry.

Fetch evidence (read-only, `.ufo/waves/round-61/recheck/receipts.json`): all ten receipts carry `status` 200,
`userAgent` `round61`, `fetchedAt` 2026-10-27T09:15:41Z…09:15:56Z. I re-summed every retained `S0xx.html`: all ten
`sha256` and byte counts equal their receipt (10/10). S010's receipt `url` keeps the `#section-8.8` fragment and its
`effectiveUrl` is the fragmentless page, so the fragmentless form is what the audit of a pinned cell should cite.

Anchor basis (authoritative): `ExecC3Quote`'s `.ufo/waves/round-61/w1/ExecC3Quote.files/verdicts.tsv` — 9
`anchor_found` (S002–S010), 1 `anchor_moved` (S001), 0 `page_changed`, 0 `fetch_failed`. My independent probe
(`anchor_probe.tsv`) cross-checks material presence, not location: it found every fetched-scope component present on
all ten rows. The divergence is exactly S001, where presence holds but the row's anchor is **line-addressed** and
the cited lines do not point at the material in the fetched body — the quote seat's location rule wins, so S001 is
carried. `compute_pins.py` reads the verdict table first and only falls back to the probe when it is absent; both
paths record `verdict_source` per row in `pin_cells.json` (all ten rows here: `ExecC3Quote`).

## BOUND CHECKS:

`Nd` rows: `opened < new ≤ opened + cadence`; the two non-`Nd` cadences: `opened < new ≤ opened + 90d`.

| row | opened | new | upper bound | check |
|---|---|---|---|---|
| S002 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality at the upper bound |
| S003 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality |
| S004 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality |
| S005 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality |
| S006 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality |
| S007 | 2026-10-19 | 2027-01-17 | 2027-01-17 (+90d) | pass, equality |
| S008 | 2026-10-19 | 2027-10-19 | 2027-10-19 (+365d) | pass, equality at the upper bound |
| S009 | 2026-10-19 | 2027-10-19 | 2027-10-19 (+365d) | pass, equality at the upper bound |
| S010 | 2026-10-19 | 2027-10-19 | 2027-10-19 (+365d) | pass, equality at the upper bound |

Arithmetic is exact-date arithmetic (`datetime.date` + `timedelta`): 2026-10-19 + 90d = 2027-01-17 and + 365d =
2027-10-19 (no leap day falls between, so the year step is 365 days). Since the pin is *defined* as
`opened + cadence`, every pinned row sits exactly on its upper bound: the test holds only with an inclusive upper
bound, which is what contract C3 condition C2 states (`opened < pinned ≤ opened + cadence`). If the counter seat
implements a strict `<`, all nine pins fail — flag, not a table change. The nine values also reproduce the dates the
contract predicts (S003–S007 and S002 → 2027-01-17; S008–S010 → 2027-10-19), derived here independently from the
registry's own `opened`/`recheck` cells.

## SKIPS:

**S001 — no pin, cadence `on-release` retained.** Fetch was HTTP 200 (2529 bytes, sha256 in the receipt) but the
quote verdict is `anchor_moved`: the row's anchor is line-addressed (`inputs.include-hidden-files lines 17-20 and
Archive artifact steps lines 37-39`) and in the fetched body (v4.0.0 `action.yml`, the row's first URL) the
`Archive artifact` steps sit at lines 24–39 / 42–57 / 60–76 and `include-hidden-files` occurs 0 times — that input
belongs to the row's second URL (main `5f3270…`), which this round did not fetch (one GET per row). This is **not**
`page_changed`: the invariant-exclusion material (`--exclude=.git`, `--exclude=.github`, `--exclude=".[^/]*"`) is
on the page. Gate note text as emitted in `gate_notes.txt` (elided once at the quote-seat detail, marked `…`; the
file carries it whole):

```
- S001 — https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml — accessed 2026-10-27 — recheck carried, no date pin: HTTP 200 (2529 bytes); quote verdict: anchor_moved; quote seat: action.yml v4.0.0: Archive artifact steps lines 24-39 (Linux), 42-57 (macOS), 60-76 (Windows); …; cadence cell `on-release` retained unchanged, row status `mined` retained unchanged.
```

(The file carries the untruncated detail with ASCII double quotes normalised to single quotes, so the Gate line
cannot be misread as carrying a quote span.)

No other row is skipped. Two conditions attached to pinned rows, neither of which changes a cell:

- **S002 — partial coverage, honest carry in its Gate text.** The row names the v4.0.0 *and* v5.0.0 release pages;
  only the v4.0.0 page was fetched (`v5.0.0` occurs 0 times in the body). The pin stands on the verified
  `v4.0.0 What's Changed` clause; the Gate line must name the v5.0.0 clause as unverified this round — not as
  changed, not as re-verified.
- **Counter C5 shape.** One unpinned due row, and it has a Gate note naming the observed state (HTTP status, byte
  count, verdict, relocated lines); no pinned row lacks a Gate line.

## APPLICATION (how the nine cells land)

- `proposed_rows.tsv`: per pinned row, the **full registry row line with only field 10 changed**. Applied all nine
  to a scratch copy of the live `SOURCES.md` and diffed: 167 registry rows, exactly 9 lines differ, each a 13-field
  row whose only differing field is index 10, old→new as in `PINS:`; the other 158 rows are byte-identical
  (contract C6: rows outside the recheck cell stay unchanged).
- `pin_replacements.txt`: the cell-position form (`split on '|'`, replace index 10) is the safe one. The substring
  form is listed with its file-wide occurrence count because it is **not unique**: `| 2026-10-19 | 90d |` occurs 10
  times (S003–S007 + S013–S017), `| 2026-10-19 | 365d |` 5 times (S008–S012), `| 2026-10-19 | on-release |` 2
  times. A global replace would corrupt S011–S017.
- New cell strings are bare ISO dates (`2027-01-17`, `2027-10-19`) — the form the C3 counter's C2 condition
  parses as a concrete date; no cadence suffix survives in a pinned cell, per the contract's wording.
- The lesson `## Gate` old→new log is exactly these nine pairs plus the S001 carry line; registry cell edit + Gate
  line are the only changes this claim makes to a row.

## NOTES / RISKS

- Quote-seat findings that affect the **Gate scribe**, not my cells: S005's step-4 and CNAME sentences each occur
  twice (apex + subdomain), so neither is page-unique — the tsv ships a section-specific span; S008's section now
  reads 8480–8620 vs the anchor's 8478–8617 (+2/+3, same material); S009 exact (1682, 1708–1710). None of these
  moves a pin: S005/S008/S009 are `anchor_found`.
- `compute_pins.py` exits 2 when `SOURCES.md` is unreadable or a frozen due row is missing; re-run it after the C2
  append seats add S430–S433 (appends sit below the due rows and do not disturb field 10 of S001–S010).
- The "ten oldest rows" set is taken as frozen by the contract; I did not re-derive the tie-break across the 16
  rows opened 2026-10-19 (that is the counter's C1 condition, not this seat's).
- Nothing was scored: counters are frozen by the L1 after this wave. I edited no registry row, lesson, counter or
  sibling artifact — only `ExecC3Pins.md` and `ExecC3Pins.files/`.
- No credentials, tokens, `op://` refs or private URLs appear here. Tooling: nothing installed or upgraded; no
  pacman, no host service touched. Scratch (`/fast/scratch/hyaku/kake-r61/ExecC3Pins`) deleted; nothing is cited
  from it.

VERDICT: nine pins computed and bound-checked (S002–S007 → 2027-01-17, S008–S010 → 2027-10-19; all equality at the inclusive upper bound) with S001 carried as `anchor_moved` (Gate note naming HTTP 200, the relocated lines and the unfetched second URL), proposed as full rows with field 10 as the only change and 158 rows byte-identical; ExecC3Quote's verdict table, not my probe, is the anchor basis.
