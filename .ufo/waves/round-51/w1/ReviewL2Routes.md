# ReviewL2Routes — adversarial read of `check_l2`

Seat: `L1Kake51.ReviewL2Routes-2` · axis: operability · claim under attack: C1 L2 (route receipts)
Instrument: `.ufo/waves/round-51/c51_wave_ledger.py` lines 145–197 (frozen at `9d13768`), predicate `met: ledger_checks_passed == 3 of 3`.

## 0. State at review time

The wave evidence is **not committed**. `route-map.json`, `route-probes/`, `w51-taskcall.json` and the
`sources/`, `controls/`, `assimilation/` trees are untracked at `9d13768` (`git status --porcelain`).

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL   - settlement receipt absent at the measured revision
  L2 FAIL   - route map absent at the measured revision
  L3 FAIL   - settlement receipt absent at the measured revision
exit=1
```

So L2 is not evidenced at any revision yet. What follows is a review of the frozen code plus the
bytes staged in the working tree, executed against throwaway git fixtures under `/tmp/l2run/`
(each fixture = `git init` + the artifact files + `commit`; `check_l2(root, rev)` imported from the
lane script, which was never modified). 40 fixtures were run; every verdict below is an observed
result, not a reading. No tool was installed.

## 1. Answers to the three questions

### Q1. Can a failing probe receipt be used by a role without failing? — **Yes, three independent ways.**

**Hole 1a — the failure predicate is the self-declared `ok` flag, never the integer status.**
`line 186` decides "failing" as `receipt.get("ok") is False`; `httpStatus` is only type-checked
(`177–179`, `183–185`) and never compared to any success class. A receipt that says
`"httpStatus": 403, "ok": true` is a passing receipt as far as the ledger is concerned, so the
used-route guard at `180–181` is satisfied too.

| fixture | receipt | verdict |
|---|---|---|
| `01_used_http403_oktrue_noexcerpt` | used alias, `httpStatus 403`, `ok true`, no excerpt | **PASS**, notes `[]` |
| `01b_used_http500_oktrue` | used alias, `httpStatus 500`, `ok true` | **PASS**, notes `[]` |
| `01c_used_http0_oktrue` | used alias, `httpStatus 0`, `ok true` | **PASS**, notes `[]` |

**Hole 1b — `receipts.setdefault(alias, receipt)` (line 169) keeps the first receipt per alias and
silently discards the rest.** Ordering is `git ls-tree` byte order, i.e. the filename decides which
receipt is authoritative. Proven on the **real** working-tree bytes: adding a failing receipt for the
used alias as `zzz-failing.json` yields PASS; the identical bytes as `aaa-failing.json` yield FAIL.

| fixture | file name | verdict |
|---|---|---|
| `42_failing_first` | `aaa-failing.json`, used alias, `ok false`, 403, excerpt | FAIL — 3 notes (`used but its receipt is not ok`, `was used by a role`, `not recorded as a deviation`) |
| `43_failing_last` | same bytes as `zzz-failing.json` | **PASS**, notes `[]` |

**Hole 1c — only `*.json` is read (line 155).** The real receipt directory already contains a failing
receipt for the exact alias the whole wave uses, under a `.txt` name:

```
.ufo/waves/round-51/route-probes/commandcode_deepseek_deepseek-v4.1-flash.txt
# alias=commandcode/deepseek/deepseek-v4.1-flash ... probedAt=2026-10-24T23:25:24-03:00
error: failed to run prompt: Model "commandcode/deepseek/deepseek-v4.1-flash" is not configured in config.toml.
# exit=1
```

`check_l2` on the real bytes reports `facts {'roles': 10, 'receipts': 2}` — 2 of the 9 probe files in
that directory are visible (**PASS**, `40_real_bytes`). The same failure content as `.json` is caught
(`30_named_failing_no_deviation` → FAIL, `failing route ghostroute is not recorded as a deviation`),
so visibility is decided by extension, not by content. Related: `158–159` (`if raw is None: continue`)
skips an unreadable receipt with no note; a newline-named receipt is listed quoted by `ls-tree`, fails
`git show`, and vanishes — `31_newline_named_failing` → **PASS** with the failing bytes committed.

**Hole 1d — values other than the literal `False` are not "failing".** `ok` missing (`14`), `ok: 0`
(`15` — `0 is False` is false under `is`), `ok: "false"` (`20`) all PASS with `httpStatus 403` and no
excerpt and no deviation record.

### Q2. Can a receipt omit its excerpt and still pass? — **Yes, whenever `ok` is not literally `False`.**

The excerpt requirement lives entirely inside `if receipt.get("ok") is False:` (`186–189`). Because of
Hole 1a the failure flag is self-declared, so `{"httpStatus": 403, "ok": true}` with no
`bodyExcerpt` passes (`01`), as does `{"httpStatus": 403}` with no `ok` at all (`14`).

Guards that do work, and their fixtures:

- `188–189` `isinstance(excerpt, str) and excerpt.strip()` → `04_unused_fail_noexcerpt` FAILs with
  `failing probe receipt for xai-oauth/grok-4.7-fast carries no body excerpt`.
- The excerpt's *content* is unvalidated: `18_placeholder_excerpt` sets `"bodyExcerpt": "N/A"` on a
  403 and PASSes. Nothing ties the excerpt to a status, an endpoint, or a retained body (no probe
  body is kept at all), so the excerpt is a non-empty-string token, not evidence.

### Q3. Can a role's alias be absent from every receipt? — **Yes, two ways; a third is guarded.**

The used-route universe is built at `line 171`:
`used = {r.get("kimiModel") for r in roles.values() if r.get("kimiModel")}`.

- **Hole 3a — a role with no `kimiModel` (or `""`) is filtered out of `used` and therefore out of every
  receipt obligation.** `08_role_without_kimiModel` (delete `roles.scout.kimiModel`) → **PASS**.
- **Hole 3b — the role universe comes from the route map alone.** `check_l2` never reads the dispatch
  payload (`TASKCALL`, defined at 47, read only at `100` inside `check_l1`) or the settlement
  (`SETTLEMENT`, 46, read at `99`/`202`). A route map that keeps 1 of 10 roles passes while the
  payload still dispatches all 10: `09_routemap_missing_9_roles` → **PASS**, `facts {'roles': 1}`.
  On today's bytes the two agree (payload histogram: scout 6, connector 1, executor 9, scribe 4,
  reviewer 10, critic 10, mutation-tester 5, sentinel 1, revenger 1, simplifier 1 = 48 seats; route
  map has exactly those 10 keys, no payload-only or map-only role), but nothing in the counter would
  notice if they diverged.
- **Guarded** — a role whose `kimiModel` names a route with no parseable `.json` receipt is caught at
  `174–175`: `16_used_route_txt_only` and `19_kimiModel_points_elsewhere` (`devin/swe-2-max`, which has
  only a `.txt` receipt) both FAIL with `no committed probe receipt for used route …`.

Corollary: `used` is a set and `receipts` is keyed by alias, so **one receipt vouches for every role
that names its alias** — here all 10 roles / 48 seats rest on the single
`commandcode_deepseek-v4.1-flash.json`. There is no per-seat or per-role dispatch record in the
committed bytes, so nothing can contradict a role that names the passing alias.

## 2. The deviation guard is prose matching, and `deviations` is never read

`192–196` builds `recorded` by concatenating every role's free-text `probe` string and requires
`alias in recorded` — a raw substring test. `route_map["deviations"]` is never referenced anywhere in
the file (`grep deviations` → no hit).

| fixture | route map | verdict |
|---|---|---|
| `05a_deviations_array_but_prose_silent` | structured `deviations` correct, prose silent | **FAIL** — honest deviation rejected |
| `05b_prose_but_no_deviations_array` | `deviations` deleted, prose intact | **PASS** — structured record unread |
| `06_alias_is_substring_of_prose` | failing receipt for a route named `xai`, no such route in the map; prose mentions `xai-oauth/grok-4.7-fast` | **PASS** — borrowed mention |
| `30_named_failing_no_deviation` | failing route `ghostroute`, no mention | FAIL at `195–196` |

So the guard both rejects a correctly recorded deviation and accepts a failing route that shares a
substring with an unrelated line of prose. It also only scans `roles[*].probe`; a role with no `probe`
string contributes nothing, and a route map with one role makes `recorded` narrow.

## 3. Crash paths: the declared exit 2 does not exist

`main()` (263–296) has no exception handling and `sys.exit(main())` (line 297) is the only exit; the
docstring's `2 the evidence cannot be evaluated` is unimplemented — no code path returns 2
(`grep -n "exit(2)\|return 2"` → only line 297).

`check_l2` assumes every JSON file and the route map itself are objects with `.get`. Observed:

| fixture | input | result |
|---|---|---|
| `12_receipt_json_array` | `route-probes/arr.json` = `[1, 2]` | `AttributeError: 'list' object has no attribute 'get'` |
| `12b_receipt_json_null` | `null` | `AttributeError: 'NoneType' …` |
| `21_routemap_is_array` | `route-map.json` = `[1,2]` | `AttributeError: 'list' …` (line 150) |
| `22_roles_is_list` | `"roles": ["scout"]` | `AttributeError: 'list' … 'values'` (line 171) |
| `32_kimiModel_int` | one `kimiModel: 5` among strings | `TypeError: '<' not supported` (line 172 `sorted`) |
| `24_cli_array_receipt` | same as 12 through the CLI | **exit 1, empty stdout**, stderr ends in `AttributeError…` |

A single malformed receipt or route map destroys the output of all three checks (L1/L3 included,
since the loop at 269 aborts before printing) instead of scoring an honest miss. That is the opposite
of the contract's "a miss on any of L1, L2 or L3 is an honest stop".

## 4. Fields never read (freshness / authenticity gap)

`grep` over the counter for `probedAt`, `endpoint`, `leg`, `operatorAlias` → **no hits**. Consequences:

- No wave window: a receipt from a prior round satisfies L2. The directory mixes rounds —
  `.txt` probes dated `2026-10-24T23:23–23:25`, the `.json` probes dated `2026-10-25T03:30–03:31` —
  and nothing distinguishes them.
- No endpoint/alias coherence: `xai-oauth_grok-4.7-fast.json` carries
  `"endpoint": "provider route via kimi CLI (not used by this wave)"`, which is not a URL, and is
  accepted as an "HTTP status" receipt because the status is an integer field the author typed.
- No leg coverage: the used alias's only visible receipt is `"leg": "http-edge"`; the completion-leg
  claim ("answered PONG via `omp -p …`") exists only as prose in `detail` and in `roles[*].probe`.
- `isinstance(status, int)` accepts booleans (`isinstance(True, int)` is `True`): `10_httpStatus_bool`
  produced no `no integer httpStatus` note (it failed only for the unrelated deviation check); a
  string status is caught (`11_httpStatus_string` → `carries no integer httpStatus`).
- `facts` reports only counts (`{'roles': …, 'receipts': …}`), so an audit reader cannot see which
  routes were checked or which receipt files were folded away by `setdefault`.

## 5. Guards that hold (with the mutation that exercises them)

| guard | line | fixture | observed |
|---|---|---|---|
| route map must exist | 147–149 | tip `9d13768` | FAIL `route map absent at the measured revision` |
| role bindings non-empty | 151–152 | — (not exercised) | code path present; no fixture run |
| non-JSON receipt is a miss | 162–164 | `13_unreadable_receipt_gitlink` | FAIL `probe receipt … is not JSON` |
| receipt must name an alias | 165–168 | — (not exercised) | code path present; no fixture run |
| used route must have a `.json` receipt | 174–175 | `16_used_route_txt_only`, `19` | FAIL `no committed probe receipt for used route …` |
| used route's receipt must be `ok is True` | 180–181 | `02_used_http403_okfalse_excerpt` | FAIL `used but its receipt is not ok` |
| integer status required | 178–179 / 183–185 | `11_httpStatus_string` | FAIL `carries no integer httpStatus` |
| failing receipt needs a non-blank excerpt | 188–189 | `04_unused_fail_noexcerpt` | FAIL `carries no body excerpt` |
| failing route must not be used | 190–191 | `02` | FAIL `failing route … was used by a role` |
| failing route must appear in probe prose | 195–196 | `30_named_failing_no_deviation` | FAIL `not recorded as a deviation` |

Baseline control: the real working-tree bytes PASS (`40_real_bytes`, notes `[]`), so the holes above
are escapes from a passing configuration, not from a fixture the counter would have rejected anyway.

## 6. Severity, and what a committed L2 would still not prove

High — any of these makes a failing route usable while L2 reports pass:
`186` (`ok` instead of status decides failure), `169` (`setdefault` discards a failing duplicate
receipt; proven on real bytes by `42` vs `43`), `155` (`.txt` receipts invisible; the real directory
carries a `# exit=1 / Model … is not configured` probe for the used alias).

High — `263–297`: malformed evidence crashes the whole counter with no `exit 2`, so "3 of 3" can be
lost or the tool can die mid-wave with no machine-readable verdict.

Medium — `171` (role universe is the route map alone; missing `kimiModel` exempts a role),
`192–196` (prose substring, `deviations` unread).

Medium — `186` (`ok` absent/`0`/`"false"` all exempt a 403 from the excerpt and deviation duties).

Low — `188` (excerpt content unvalidated, `"N/A"` passes), `178/184` (bool status), unread
`probedAt`/`leg`/`endpoint`/`operatorAlias` (no freshness or leg coverage), `158–159` (silent skip of
an unreadable path), thin `facts`.

What a passing L2 would still not prove: that any seat ran on the declared route. The route map is
self-authored; the dispatch payload carries no per-seat model; and one alias receipt covers all 10
roles. The counter can prove that a receipt file exists and that its author wrote `ok: true` — not
that the wave's transport used it.

Recommended minimal repairs (not applied; the counter is frozen and the L1 owns the bytes):
decide failure from `httpStatus` with `ok` cross-checked (and reject non-int/bool), key receipts by
file path and treat a second receipt for one alias as a miss, drop the extension filter or require a
committed inventory of probe files, read `route_map["deviations"]` for exact route equality instead of
prose substrings, require `kimiModel` on every role and check `set(roles) == set(payload roles)`,
validate `probedAt` against the wave window and `leg`, and add the `exit 2` path from the docstring.

## 7. Files read

Read: `.ufo/waves/round-51/c51_wave_ledger.py` (whole, 297 lines), `contract.json`,
`route-map.json`, `route-probes/*.json` and `*.txt` (all 9), `w51-taskcall.json` (counts + registry
roles), `git log --oneline -3`, `git status --porcelain`.
Written: this file only. Scratch: `/tmp/l2run/` (driver + 40 fixture repos). No lane, fleet, jj or git
index was mutated; no install performed.

Not read: `settlement.json`, `wave-timing.json`, `round-time-accounting.json` — they do not exist yet
(that absence is why L1/L3 fail at `9d13768` and why L2's route map is still uncommitted).
