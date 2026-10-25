# ExecCensus

Frontier census of `corpus/SOURCES.md` at the revision under attack
`a450e43e696d032e3ac308383f6b3394e0c92860` (tip) against base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`, and against
`.ufo/waves/round-56/controls/census-before.txt`. Every run below happened in my own
`mktemp -d` clone (`git clone -q --no-checkout <lane> "$D" && git -C "$D" checkout -q <rev>`,
`git -C "$D" rev-parse --show-toplevel` verified equal to `$D`); no lane file, index or jj state
was touched. Clones: `/tmp/census-1as4r1ao/kake-shokunin` (tip),
`/tmp/census-hv0xqupg/kake-shokunin` (base). Round date `--today 2026-10-25` for all runs.

`scripts/sources-census.sh` resolves lane ids from `$ROOT/shokunin.conf` (`build_roster`), which a
bare clone lacks; I wrote a one-line conf in each *temp parent* — `LANES="` / `kake|kake-shokunin|kake lane` / `"` —
so `--root <parent> kake` yields the same `kake` label and the same lane dir as the control, with no
live-lane layout required. `validate` on an explicit dir argument also works but relabels the lane
`kake-shokunin`, so the conf route was used.

## CENSUS:

Command (identical for both revisions, `$P` = the temp parent):

```
bash scripts/sources-census.sh validate --root "$P" --today 2026-10-25 kake
bash scripts/sources-census.sh census   --root "$P" --today 2026-10-25 kake
```

| run | exit | output lines | content |
|---|---|---|---|
| tip `a450e43e` validate | **0** | 15 | 14 × `W04`, then `kake	ok	<clone>/kake-shokunin/corpus/SOURCES.md` |
| base `e48354b7` validate | **0** | 15 | same 14 × `W04`, then `kake	ok	…` |
| control `census-before.txt` | `EXIT=0` (recorded line) | 15 + `EXIT=0` | same 14 × `W04`, then `kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` |
| tip `census` | **0** | 13 | `rows 158`, `tier.A 135`, `tier.B 6`, `tier.C 17`, `status.mined 128`, `status.queued 8`, `status.rejected 22`, `missing 0` |
| base `census` | **0** | 13 | `rows 156`, `tier.A 133`, `tier.B 6`, `tier.C 17`, `status.mined 126`, `status.queued 8`, `status.rejected 22`, `missing 0` |

- Row count matches the control's shape: the control's 15 data lines are exactly the 15 lines I get
  (14 warnings + 1 `ok`), and no `E*` code appears at either revision, so the census-before control
  and the tip agree on verdict and on warning count.
- Live cross-check (read-only, `--root /home/vgpnk/Projects/shokunin kake`, `--today 2026-10-25`):
  exit 0, 15 lines, **identical** to the clone-at-`a450e43e` output after normalizing the clone path
  prefix. Live lane HEAD read at the same time was `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`,
  ahead of the revision under attack — so `corpus/SOURCES.md` is unchanged between `a450e43e` and
  `7ad7db5`, and the tip reading is not stale against the worktree.
- Census deltas base → tip: rows +2, `tier.A` +2, `status.mined` +2; `tier.B`, `tier.C`,
  `status.queued`, `status.rejected`, `missing` unchanged. Every added row is tier A and mined, so
  the two counters move together and no tier/status inflation accompanies them.

## MANUAL CENSUS:

The seven frozen commands of `CORPUS.md` §`SOURCES.md — where a shokunin learns` → `### Census`,
run verbatim with `cwd` = the lane root of each clone.

| # | command (from CORPUS.md, verbatim) | base `e48354b7` | tip `a450e43e` |
|---|---|---|---|
| 1 | rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `156` | **`158`** |
| 2 | malformed rows (`NF!=13`) — must print 0 | `0` | **`0`** |
| 3 | tier histogram | `A=133 B=6 C=17` | **`A=135 B=6 C=17`** |
| 4 | status histogram | `mined=126 queued=8 rejected=22` | **`mined=128 queued=8 rejected=22`** |
| 5 | duplicate ids — must print nothing | *(empty)* | ***(empty)*** |
| 6 | enum violations + tier inflation — must print nothing | *(empty)* | ***(empty)*** |
| 7 | mined rows whose used-by paths do not exist — must print nothing | *(empty)* | ***(empty)*** |

All seven agree with the maintained parser on both revisions (rows 156/158, tier A 133/135, mined
126/128). Rows 156 → 158 is the expected before/after.

Row-level delta of the registry (`git diff -U0 e48354b7 a450e43e -- corpus/SOURCES.md`): 3 insertions,
1 deletion, no removals of ids.

- Added `S419` (`corpus/SOURCES.md:165`) and `S420` (`corpus/SOURCES.md:166`), both
  `docs | A | mined | opened 2026-10-25 | 180d`, continuing from base max id `S418` — no id reuse,
  no gap introduced at the frontier (base tail `… S416, S417, S418`; tip tail `… S417, S418, S419, S420`).
- Changed `S367` (`corpus/SOURCES.md:157`): field-level comparison shows **only** `used-by` moved,
  `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` → that path plus
  `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`. That is contract rule 2's
  permitted in-place column set (status/recheck/used-by), not a row rewrite.
- Used-by targets of the added rows exist in the tip tree:
  `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (S419),
  `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (S420) — both `True` on `[ -e ]`, which is
  why manual check 7 and the script's `E11` stay empty.

## W04 SET:

The 14 duplicate-url warnings are **the same ids, in the same order, with the same normalized URLs**
at base, at tip, and in `controls/census-before.txt` (list equality, not set-only):

`S033`, `S088`, `S092`, `S098`, `S099`, `S102`, `S110`, `S111`, `S115`, `S116`, `S117`, `S127`,
`S416`, `S417`.

- No W04 entry was added or retired by the two new rows: `S419`/`S420` carry distinct
  `info-search.yahoo.co.jp/archives/002856.php` / `…002857.php` URLs (their own scope keys), and
  neither appears in any W04 line.
- W04 is a warning class and does not fail validation — consistent with exit 0 at both revisions and
  with the control's recorded `EXIT=0`.
- Not run, and not claimed: the script's `overdue`, `shared` and `selftest` modes (outside this seat's
  assignment), and any `--file`-mode reading of a registry outside the lane.

VERDICT: tip census clean and matching the control — validate exit 0 with the identical 14 W04 ids (S033…S417), rows 156 → 158 (+S419, +S420, both tier A/mined with existing used-by paths), tier A 133 → 135, mined 126 → 128, malformed/duplicate-id/enum/used-by checks all empty, and only S367's used-by column changed in place.
