# kake round 77 — frozen contract (attempt 1)

Frozen before any seat ran. Base revision `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` (lane `master` tip at
round open, 2026-11-03). Host: Linux, python 3.13, node. Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Scratch root `/fast/scratch/hyaku/kake-r77`.

Two claims. C1 works the lane's lowest non-retired axis (calibration, score 2). C2 is an operability
capability move on declared frontier ground. Scores stay HOLD: operability 10, freshness 10, calibration 2 —
no scalar moves this round; each claim lands a verdict, not a number.

## C1 — calibration (score 2, HOLD): every SHONEN box is classified from committed bytes

**Claim.** Each box of `SHONEN.md` is classified by the lane's own counter from committed bytes at one
named revision, with a resolvable evidence pointer and a recorded derivation; no box is left unexamined,
and no box marker asserts more than the derivation supports.

**Counting command (frozen form).**

```sh
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision <full-hash> [--work <scratch>]
```

**Printed fields (frozen).** One line:

```
C1 revision=<rev> boxes=<n> evidenced=<n> gap=<n> unexamined=<n> mismatches=<n> met=<true|false>
```

**Predicate (frozen; the same sentence in the ledger, the counter and the report).**

```
met  <=>  boxes == 4  and  unexamined == 0  and  mismatches == 0
```

**Definitions (frozen).**

- `box` — an item line of `SHONEN.md` matching `^- \[([ x~])\] `; the lane has exactly 4.
- Ledger — `corpus/knowledge/shonen-ledger.json`, schema `shonen-ledger/v1`, one row per box with
  `box` (1–4), `marker` (`" "`, `"~"`, `"x"`), `status` (`evidenced` | `gap`), `checks` (non-empty array of
  `{id, path|command, observed, holds}`), optional `reason` + `flip` when `status=gap`, optional `verifier`
  (a named non-author) required when `marker="x"`.
- `evidenced` — ledger row with `status="evidenced"` whose every check has `holds=true` **after the counter
  re-derives `observed` from committed bytes at `<rev>`**: `path` checks require the path to exist at the
  revision; `command` checks are re-run by the counter (or their committed receipt is re-read at the
  revision) and compared with the recorded `observed`.
- `gap` — ledger row with `status="gap"`, a non-empty `reason`, and a non-empty `flip` (the condition that
  would make it evidenced). Counts as examined, never as evidenced.
- `unexamined` — a box with no ledger row, or a row with an empty `checks` array.
- `mismatch` — (a) a marker that asserts more than the row supports: `"~"` or `"x"` with no row, `" "` with
  an `evidenced` row, `"x"` without `verifier`; (b) a check whose named `path` does not exist at `<rev>`;
  (c) two rows for one box; (d) a `status=evidenced` row whose re-derived check disagrees with its recorded
  `observed`.

**Kill rule (frozen).** A counter that takes the ledger's `holds` flags as given is invalid: a row whose
re-derived observation contradicts its recorded `observed` must produce a mismatch. A counter that reports
`met=true` on the base tree (no ledger) or on a ledger whose rows carry empty `checks` is invalid.

**Target.** Base `a2cc5f51`: `boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false`, exit 1. After:
`boxes=4 evidenced=<e> gap=<4-e> unexamined=0 mismatches=0 met=true`, exit 0 — every box classification
derived, gaps named with their flip conditions rather than ticked.

**Edit surface.** `SHONEN.md` (markers + one evidence line per box), `corpus/knowledge/shonen-ledger.json`,
`.ufo/waves/round-77/c77_shonen_ledger.py` and its controls.

## C2 — operability (score 10, HOLD; capability acquisition): sitemap container and format coverage

**Claim.** `scripts/sitemap_audit.py` decides every case of a frozen container/format matrix correctly over
three families the round-39 tool refused — the gzip container (limit applied to the **decompressed** size),
the plain-text sitemap (one absolute URL per line), and syndication feeds (RSS 2.0 and Atom 1.0) — while its
delivered selftest still passes and four degenerate constants each fail at least one case.

**Counting command (frozen form).**

```sh
python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool scripts/sitemap_audit.py \
  --revision <full-hash> --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts \
  --work <scratch>
```

**Printed fields (frozen).** One line:

```
C2 revision=<rev> cases=<n> decided=<n> correct=<n> wrong=<n> constants_failed=<k>/4 met=<true|false>
```

**Predicate (frozen).**

```
met  <=>  cases == decided  and  wrong == 0  and  constants_failed == 4
```

**Contract sentences (the frozen reading, all from S012 opened 2026-11-03).**

- G1. A sitemap file may be gzip-compressed; **the file once uncompressed must be no larger than
  52,428,800 bytes**. The limit therefore applies to decompressed bytes.
- G2. Container is decided by the gzip magic `1f 8b`, not by the file name; a file without the magic is
  read as plain bytes whatever its extension.
- T1. A text sitemap holds one URL per line, fully specified (scheme + authority), UTF-8, at most 50,000
  URLs, no larger than 52,428,800 bytes, and no other information (no header, footer or comment line).
- F1. RSS 2.0: the URL is the `<item><link>` text; the modified date is the optional `<pubDate>`.
- F2. Atom 1.0: the URL is the entry's `<link href>`; the modified date is the optional `<updated>`.
- F3. A sitemap-index `<loc>` may name a Sitemap, an Atom file, an RSS file or a simple text file; the index
  audit itself is container-agnostic.
- X1. A document whose root is none of `urlset`, `sitemapindex`, `rss`, `feed` is `format_unsupported`
  (exit 2) — never silently clean.

Existing round-39 behaviour (XML limits, entry counts, `loc` form/scope, `lastmod`/`changefreq`/`priority`,
exit alphabet 0/1/2/64) is unchanged and stays covered by the existing selftest.

**Matrix (frozen population; case ids fixed here, bytes built in-wave).** 20 cases, each a manifest naming
one local file plus its served URL, expected exit and expected finding-id set:

| id | family | expected |
|---|---|---|
| g01 | gzip XML urlset, 2 entries | clean (0) |
| g02 | gzip whose decompressed body exceeds 52,428,800 bytes | finding `sitemap_too_large` (1) |
| g03 | gzip magic with a truncated stream | input fault (2) |
| g04 | `.gz` name, plain XML body, valid | clean (0) |
| t01 | plain text, 3 absolute URLs | clean (0) |
| t02 | text with a non-URL line (`# comment`) | finding `text_line_not_url` (1) |
| t03 | text with a relative URL (`/page`) | finding `text_url_not_absolute` (1) |
| t04 | empty text file | finding `text_empty` (1) |
| t05 | text with 50,001 URL lines | finding `text_too_many_entries` (1) |
| t06 | gzip-compressed text, 2 URLs | clean (0) |
| t07 | text with a BOM-prefixed first URL | clean (0) |
| r01 | RSS 2.0, 2 items with link + pubDate | clean (0) |
| r02 | RSS item missing `<link>` | finding `feed_item_missing_link` (1) |
| r03 | RSS `<pubDate>` malformed | finding `lastmod_invalid` (1) |
| r04 | RSS `<link>` relative | finding `loc_not_absolute` (1) |
| a01 | Atom 1.0, 2 entries with link href + updated | clean (0) |
| a02 | Atom entry link missing `href` | finding `feed_item_missing_link` (1) |
| a03 | Atom `<updated>` malformed | finding `lastmod_invalid` (1) |
| s01 | sitemap index whose `<loc>`s end `.txt`, `.rss`, `.atom` | clean (0) |
| d01 | XML document rooted at `<html>` | input fault `format_unsupported` (2) |

**Constants (frozen; each must fail ≥1 case).** (1) always-clean printer, (2) report-every-id printer,
(3) empty-findings printer that keeps the real exit codes, (4) the round-39 XML-only tool itself.

**Kill rule (frozen).** A matrix that compares only exit codes, or whose constants are not each required to
fail at least one case, is invalid. A case whose expected value is changed after the base run is not this
claim's case.

**Edit surface.** `scripts/sitemap_audit.py` (+ `scripts/sitemap_audit_selftest.py`),
`.ufo/waves/round-77/cases/**`, `.ufo/waves/round-77/consts/**`,
`.ufo/waves/round-77/c77_sitemap_matrix.py`, and the receipts under `.ufo/waves/round-77/controls/`.

## Frontier step (round 77)

- `corpus/SOURCES.md`: S012 (`sitemaps.org/protocol.html`) re-opened 2026-11-03 (HTTP 200, 45,292 B,
  sha256 `5e757059…`) — its `used-by` gains the round-77 entry, old→new logged in the lesson. New rows
  S447 (RFC 1952, gzip container) and S448 (RFC 4287, Atom 1.0) opened the same round, each with a
  ≤25-word located quote in `corpus/lessons/round-77.md` `## Gate`. New entry
  `corpus/knowledge/sitemap-formats.md` cites S012/S447/S448. Census before and after both recorded.
- Mistake mined into `corpus/lessons/round-77.md` `## Mistakes` (class · evidence pointer · captured-by ·
  fix), from the round-76 closure's routed defects and this round's own evidence.
- `Assimilation:` the `merge/kake` package's staged ids S287–S415 are all below the lane's registry tip and
  already occupied by different rows; the id-collision check is re-run this round and adoption stays
  closed. `considerthese/2026-10-26.md`: all five proposals are implemented in the lane (r58, r66, r72 and
  report practice) — no unimplemented proposal is mined.
- Round-76 routed defects 1–6: D1 is repaired by the C2 re-run at a full-hash committed revision
  (`ExecRevisionReceipts`), D2/D3 become `corpus/QUALITY.md` criteria, D4/D5/D6 become append-only
  correction lines in the lesson and `SCORECARD.md`.

## Round shape (frozen)

One v1 wave `w1`, 14 seats: scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1,
connector 1, sentinel 1. Attack share 4/14 = 28.6 % (≥25 %). One connector (≤2). Residual call: none
planned; if a verification item appears after the wave it rides one ordinary `task` call of ≤4 seats and
counts in the round total (≤16). The L1 holds the canonical planner seat.
