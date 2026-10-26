# ReviewerPinsCode

Code review of `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/c57_receipt_pins.py` (version 1, 349 lines). Every defect below was reproduced in an isolated scratch Git repository (`tempfile.mkdtemp`, `git -C "$D" init -q`, verified `--show-toplevel`).

## FINDINGS:

### F1 (HIGH) — Unpinned round-57 `after-*` receipts bypass `new_unpinned` if named outside `NEW_RE` (`after-c1.txt`, `after-c1-x.json`, `control/`)
- **Line:** `55–56`, `117–119`, `140` (`NEW_RE`, `POP_RE`, `for path in sorted(p for p in present if NEW_RE.match(p)):`)
- **Status:** `confirmed by running`
- **Failing input:** Commit `.ufo/waves/round-57/controls/after-c1.txt` (or `.ufo/waves/round-57/controls/after-c1-x.json`, or `.ufo/waves/round-57/control/after-c1-x.txt`) with `revision: 9999999999999999999999999999999999999999` once (never rewritten), alongside valid `after-c{1,2,3}-x.txt`. Because `POP_RE` matches `control|controls` and `.txt|.json`, the file is counted in `population`, and `r[0].startswith(f"{WAVE}/")` excludes it from `old`, but `NEW_RE` only checks `controls/after-c([0-9]+)-[^/]+\.txt`. The unpinned round-57 receipt is never checked by the `new_unpinned` loop (`new_unpinned=0`, `met=True`).
- **Fix:** Treat any round-57 receipt in `present` whose basename starts with `after-` (or any receipt in `present` under `f"{WAVE}/"` that is not a `base-*` or `*selftest*`/`*census*` control, or explicitly any `after-*` under `.ufo/waves/round-57/{control,controls}/` not matching `NEW_RE`) as `new_unpinned += 1`:
  ```python
  for path in sorted(p for p in present if p.startswith(f"{WAVE}/") and os.path.basename(p).startswith("after-") and not NEW_RE.match(p)):
      new_unpinned += 1
      notes.append(f"{path}: malformed new after-receipt filename")
  ```

### F2 (HIGH) — Duplicate identical `revision:` lines in a new receipt collapse in `set(...)` and pass `len(revs) == 1`
- **Line:** `143`, `145` (`revs = set(REV_RE.findall(text))` and `len(revs) == 1`)
- **Status:** `confirmed by running`
- **Failing input:** Commit `.ufo/waves/round-57/controls/after-c1-x.txt` containing two identical lines `revision: <measured_rev>\nrevision: <measured_rev>\n`. `REV_RE.findall(text)` returns a 2-element list, but `set(...)` collapses it to length 1, returning `new_unpinned=0` and `met=True` despite the receipt carrying two revision lines.
- **Fix:** Preserve list length before deduplicating:
  ```python
  rev_list = REV_RE.findall(text)
  revs = set(rev_list)
  ok = (len(rev_list) == 1 and measured_rev is not None ...
  ```

### F3 (HIGH) — Stripping a receipt's pin in commit $C_2$ and writing a new pin in commit $C_3$ misses the second relabel (and Delete $\to$ Re-add resets `prev`)
- **Line:** `103–115` (`if text is None: prev = set(); continue` and `if prev and cur != prev: ... prev = cur`)
- **Status:** `confirmed by running`
- **Failing input:**
  1. Strip-then-relabel: commit 1 writes `.ufo/waves/round-56/controls/after-c1.txt` with `revision: a*40`; commit 2 strips the revision line (`cur = set()`); commit 3 writes `revision: b*40`. Commit 2 records `(path, a*40, "", c2)` and sets `prev = set()`. At commit 3, `if prev and cur != prev:` is false because `prev` is empty, so the `a*40 -> b*40` (or `"" -> b*40`) relabel at commit 3 is never recorded; disclosing only commit 2's strip in `receipt-errata.json` leaves the forged pin `b*40` at tip undisclosed with `undisclosed_relabels=0`.
  2. Delete-then-readd: commit 1 writes `revision: a*40`; commit 2 deletes the path (`prev = set()`); commit 3 re-adds the path with `revision: b*40`. `relabels` records `0` relabels (`relabels_old=0`, `undisclosed_relabels=0`), only incrementing `deleted_receipts=1`.
- **Fix:** Do not overwrite `prev` with an empty set when a previously pinned receipt loses its revision line or is deleted; keep the last non-empty revision set in `prev` (or record transitions from `""` when `ever_pinned` is true) so a subsequent commit that introduces a different revision `b` is also recorded as a relabel:
  ```python
  if cur:
      prev = cur
  ```

### F4 (HIGH) — Malformed `receipt-errata.json` or `measured.json` crashes with unhandled exceptions (exit 1 traceback) or silently passes instead of `Unevaluable` (exit 2)
- **Line:** `122–127`, `132–136`, `176–178`
- **Status:** `confirmed by running`
- **Failing input:**
  1. `receipt-errata.json` is `{"entries": [{"path": 1, "from": 2, "to": 3, "commit": 4}]}`: `measure()` succeeds because ints are hashable, then `report()` crashes at `r[1][:12]` with `TypeError: 'int' object is not subscriptable` (unhandled traceback, exit 1 instead of exit 2).
  2. `receipt-errata.json` is `""` (0-byte file): `if errata_text:` is `False`, so an empty committed file silently evaluates as 0 entries instead of raising `Unevaluable` (whereas `"   \n"` raises `Unevaluable`).
  3. `receipt-errata.json` has duplicate identical entries `{"entries": [E, E]}`: `entries` is a `set`, silently deduplicating the duplicate entry instead of flagging a phantom/malformed errata list.
  4. `measured.json` is `[]`, `null`, `"str"`, or `123`: `json.loads(measured_text).get("revision")` raises `AttributeError` (only `ValueError` is caught on line 135), crashing `main()` with an unhandled traceback instead of exit 2 (`Unevaluable`) or clean handling.
- **Fix:** Check `if errata_text is not None:`, validate that `json.loads(errata_text)` is a `dict` whose `"entries"` is a `list` of `dict`s with `str` values (and `len(entries) == len(raw_entries)` to reject duplicates), and validate `measured.json` similarly under `try ... except (ValueError, TypeError, AttributeError)` raising `Unevaluable`.

### F5 (MEDIUM) — `new_receipts` count is misleading when `new_nums` has 1, 2, or $\ge 4$ elements containing non-`{1,2,3}` claim numbers
- **Line:** `159` (`new_receipts = len(new_nums & {"1", "2", "3"}) if len(new_nums) == 3 else len(new_nums)`)
- **Status:** `confirmed by running`
- **Failing input:**
  1. Commit pinned receipts for `after-c1-x.txt` and `after-c4-x.txt`: `new_nums = {"1", "4"}`, `len(new_nums) == 2 != 3`, so `new_receipts` reports `2` even though only 1 of `{1, 2, 3}` is present (and `after-c4-x.txt` is not flagged in `new_unpinned`).
  2. Commit pinned receipts for `after-c1-x.txt`, `after-c2-x.txt`, `after-c3-x.txt`, and `after-c4-x.txt`: `new_nums = {"1", "2", "3", "4"}`, `new_receipts` reports `4` and `met` is `False` without any `notes` entry explaining why.
  3. Commit `after-c01-x.txt`, `after-c2-x.txt`, `after-c3-x.txt`: `NEW_RE` captures `"01"`, `len(new_nums) == 3`, `new_receipts` is `2` with no note in `notes`.
- **Fix:** Require the claim number in `NEW_RE` (or in the `new_unpinned` check) to be in `{"1", "2", "3"}` (else increment `new_unpinned` and append to `notes`), and define `new_receipts = len(new_nums & {"1", "2", "3"})` unconditionally.

### F6 (MEDIUM) — `scorecard_pin` does not require `measured_rev` to be 40-hex, uses unanchored substring match, and truncates if a code block in `## Round 57` contains `^## `
- **Line:** `155–158` (`m = re.search(r"(?ms)^## Round 57\b.*?(?=^## |\Z)", sc)` and `measured_rev[:12] in section`)
- **Status:** `confirmed by running`
- **Failing input:**
  1. `measured.json` has `{"revision": "round-57-pin-placeholder"}` and `SCORECARD.md` under `## Round 57` contains `"round-57-pin-placeholder"`: `scorecard_pin` evaluates to `1` even though `measured_rev` is not a hex commit hash.
  2. `SCORECARD.md` under `## Round 57` has no mention of `measured_rev`, except an unrelated hash/string `ffff<measured_rev[:12]>ffff` containing those 12 characters mid-token: `measured_rev[:12] in section` evaluates to `1`.
  3. `SCORECARD.md` under `## Round 57` includes a fenced code block containing a line starting with `## ` before the `measured at <rev>` line (or two `## Round 57` sections where the first is a stub): `re.search` stops at the first `^## `, returning `scorecard_pin = 0`.
- **Fix:** Require `HEX40.fullmatch(str(measured_rev))` for `scorecard_pin`, match `r"(?ms)^## Round 57\b.*?(?=^## Round \d+\b|\Z)"` (or check all `## Round 57` matches), and require a hex-boundary prefix match `re.search(rf"(?<![0-9a-f]){re.escape(measured_rev[:12])}[0-9a-f]*\b", section) is not None`.

### F7 (LOW) — `intro` commit and `touched` under `--first-parent` merge commits or re-added new receipts
- **Line:** `86`, `144` (`git(root, "log", "--first-parent", "--diff-filter=A", "--format=%H", tip, "--", path).strip().split("\n")[-1]`)
- **Status:** `confirmed by running`
- **Failing input:**
  1. If a receipt is added and later relabelled on a side branch before being merged into the first-parent line via `git merge --no-ff`, `git log --first-parent --name-status` only shows `A` at the merge commit (`undisclosed_relabels = 0`).
  2. If a round-57 receipt is added at $C_1$, deleted at $C_2$ (`measured_rev`), and re-added at $C_3$, `split("\n")[-1]` picks $C_1$ (oldest `A`) instead of $C_3$ (current `A`, `split("\n")[0]`), failing `is_ancestor(measured_rev, intro)`.
- **Fix:** Use `split("\n")[0]` (most recent `A`) for `intro` (deletion is already caught by `deleted_receipts`), and if side-branch history must be audited across merges, omit `--first-parent` on the relabel scan or reject merge commits after `BASE_REV`.

## NO-DEFECT CHECKS:
- **`measure` commit header `@@` lines and `--name-status --no-renames` parsing (lines 86–98):** Verified by running. `--format=@@%H` emits `@@<40-hex>` and file status lines always contain `\t`; commit messages are not emitted, so `@@` in commit messages cannot spoof `commit`. `--no-renames` disables `R`/`C` rename/copy detection so moves/copies are emitted as `D` + `A` lines, and root commits are emitted with `A` lines (`--root` is default in `git log`).
- **`touched` order oldest-first via `reversed` (line 104):** Verified by running. `git log --first-parent` emits newest-to-oldest along the first-parent chain; `reversed(commits)` visits versions strictly oldest-first.
- **`deleted_receipts` filtering (line 116):** Verified by running. Only paths in `deleted` where at least one committed version in `touched[p]` matched `REV_RE` are counted; deleting an unpinned scratch file in `controls/` does not increment `deleted_receipts`.
- **Strict ancestor check on `new_unpinned` (lines 77–79, 146–147):** Verified by running. `git merge-base --is-ancestor` is reflexive (`True` when `anc == desc`), and line 146 explicitly guards `measured_rev != intro`, enforcing strict ancestry.
- **Exit codes (lines 325–346):** Verified by running. Exit `0` iff `met(v)` is `True`; `1` when `met(v)` is `False`; `2` on `Unevaluable`; `64` on missing `--revision` or invalid CLI flags (`SystemExit` caught).

VERDICT: 7 logic/validation defects found and confirmed by running on scratch repos (3 HIGH in receipt/relabel/pin checks, 1 HIGH in JSON/errata error handling, 2 MEDIUM in `new_receipts` and `scorecard_pin`, 1 LOW in merge/re-add `intro` resolution).
