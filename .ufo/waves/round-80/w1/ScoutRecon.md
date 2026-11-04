# ScoutRecon — round 80 recon: the `unavailable_after` parser this round repairs

**Verdict:** at base `9998dc7a` the whole grammar hinges on one naive `value.split(",")`
(`scripts/x_robots_tag_audit.py:111`); both comma-bearing HTTP-date shapes are therefore unreachable,
the asctime shape has no regex at all, and a predicted A1+A2 patch inserted at exactly three points
(`:58`, `:100`, `:111`) leaves all 31 frozen round-79 verdicts byte-identical (measured 31/31) while
deciding 12/12 of the round-80 oracle.

All line numbers refer to the base bytes
`git show 9998dc7a586b9fe76379014c8123aa3606f2d8b9:scripts/x_robots_tag_audit.py`
(410 lines, `sha256 dd83c2c8e9046faa0a62afda4cea00fee85468e83d2f1720c92159fb11f2609b`, equal to the
working tree at recon start). Retained receipts, shas and per-case tables:
`.ufo/waves/round-80/w1/ScoutRecon/`. Runs executed 2026-11-04; no lane file was edited.

## 1. The one split site and its consequences

`parse_field` (`:106-131`) is the only place a field value is decomposed, and `:111`
(`for raw in value.split(",")`) is the only ASCII-comma split in the file (`grep -n 'split(",")'`
returns exactly `111:`). It is reached once per header from `audit` (`:203`). Consequences for a value
that contains a comma, all measured (probe manifests kept in the receipt dir, `results.json.probes`):

1. **Value truncation.** The comma terminates the segment, so a value-bearing directive's value stops
   at the comma. For `unavailable_after` the truncated value (`Wed`, `Sunday`, `Sun Nov 16 08:49:37
   1994`) matches none of the three shapes → `xrt_invalid_value` (`:100-102`) and the token is dropped
   entirely (`p01`, `p03`, `p05`, `p06`).
2. **Tail reparsed as a directive.** The remainder becomes an independent segment (`:111-130`). A date
   tail has no usable `name:` head — the first `:` falls inside the time, so `:70` partitions to
   `03 Dec 2025 13`, whose lowercased name is not in `KNOWN` → `xrt_unknown_directive` (`:73-75`;
   `p01`, `p08`, `p09`).
3. **Tail misread as a bot scope.** If the remainder *does* have a `BOT_RE`-shaped head that is not a
   known name, `:117-125` makes it a per-bot scope and the rest of the field value binds to that bot
   (`scope` persists to `:130`). A real date tail cannot trigger this (it contains spaces, and
   `BOT_RE` is `^[A-Za-z0-9_-]+$`, `:49`), but a hand-written tail can: `unavailable_after: Wed,
   googlebot: noindex` → `bots={"googlebot":["noindex"]}` plus `xrt_invalid_value` (`p12`);
   `googlebot: unavailable_after: Wed, 03 Dec … GMT, noarchive` puts `noarchive` in the bot scope
   (`p16`).
4. **Empty tail.** `unavailable_after: Wed,` → `xrt_invalid_value` + `xrt_empty_rule` (`:113-115`;
   `p11`).
5. **Duplicate blindness.** Because the truncated token is dropped, `scope_findings` (`:157-160`)
   counts zero or one `unavailable_after:` and never fires `xrt_duplicate_directive` for two
   comma-bearing dates: c39 at base is `[xrt_invalid_value, xrt_unknown_directive]`, the oracle wants
   `xrt_duplicate_directive` (`results.json.a2.c39.expected`).
6. **Scope of the damage.** ISO values and every other directive behave as documented: a comma in
   `max-snippet: 20, 30` still splits (`max-snippet:20` + `xrt_unknown_directive`, `p13`), and
   `unavailable_after: 2025-12-31, noindex` is already clean at base (`p17`, identical under patch).
   U+FF0C is not a separator; only ASCII `,` splits.

## 2. The three date regexes and exactly what they accept

| const | lines | accepted shape | comma? |
|---|---|---|---|
| `ISO_RE` | 50 | `YYYY-MM-DD`, optional `[T\| ]hh:mm`, optional `:ss`, optional `Z` or `±hh:mm` | **no** |
| `RFC822_RE` | 51-54 | `Wkd, DD Mon YYYY hh:mm[:ss] GMT` — 3-letter weekday, 2-digit day, 4-digit year, literal `GMT`, seconds optional | **yes**, after the weekday |
| `RFC850_RE` | 55-58 | `Weekday, DD-Mon-YY hh:mm:ss GMT` — full weekday, 2-digit day/month/year, seconds mandatory, literal `GMT` | **yes**, after the weekday |
| *(none)* | — | asctime `Wkd Mon [ ][0-9]{1,2} hh:mm:ss YYYY` | value has no comma |

- `ISO_RE` accepts c35/c36 and selftest t15; it rejects offsets without a colon (`+0300`),
  fractional seconds, 2-digit years, lowercase `t`/`z`, unpadded fields and any trailing space.
- `RFC822_RE` accepts the c32/c38/c41/c42 values. It rejects a 1-digit day (`Wed, 3 Dec …`), the
  RFC 850 year shape, full weekday names, and every zone other than literal `GMT` (`PST` → c37). The
  comma that the shape requires is the very byte `:111` cuts on, so the regex is dead code at base.
- `RFC850_RE` accepts the c33 value and c39's second date. It rejects 3-letter weekdays, 4-digit
  years, a missing seconds field and non-`GMT` zones. Also dead at base for the same reason.
- Asctime is rejected **independently of the split**: `unavailable_after: Sun Nov  6 08:49:37 1994`
  has no comma and still yields `[xrt_invalid_value]` at base (`p04`). In c43 the comma is a segment
  terminator *after* a complete value, so the base run keeps `noindex` and adds
  `xrt_invalid_value` only (`p05`).

## 3. `parse_rule` on a weekday-headed segment at base (measured)

- `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (c32) → segments
  `unavailable_after: Wed` and `03 Dec 2025 13:09:53 GMT`.
  `parse_rule` sees name `unavailable_after` (known) with value `Wed`; `:100` fails all three shapes →
  `xrt_invalid_value`, returns `[]` (`:101-102`). The second segment's head is not a known name →
  `xrt_unknown_directive` (`:73-75`). Report: `findings=["xrt_invalid_value","xrt_unknown_directive"]`,
  `directives=[]`, `effective=[]`, exit 1. Exit code 1, verified (`p01`).
- RFC 850 variant (c33) → the same two findings (`p03`).
- Bot-prefixed (c40) → the same two findings **plus an empty bot scope** `{"googlebot": []}`: `:124`
  materialises the scope before `parse_rule` drops the invalid value (`p02`).
- Wrong zone `… PST` (c37) → same two findings at base (`p08`); the tail is never reached as a value.
- Asctime (c34) → `[xrt_invalid_value]` only; c43 → `[xrt_invalid_value]` only with `noindex` kept
  (`p04`, `p05`).
- A field value that *is* `Wed, 03 Dec 2025 13:09:53 GMT` (head literally a weekday) → both segments
  are unknown names, so `[xrt_unknown_directive]` **only**, no `xrt_invalid_value` (`p07`).
- `unavailable_after: Wed,` → `[xrt_empty_rule, xrt_invalid_value]` (`p11`).

Full JSON for each probe: `.ufo/waves/round-80/w1/ScoutRecon/results.json` (`probes`), manifests in
`.../ScoutRecon/probes/`.

## 4. Minimal patch surface for amendment 1, and why the 31 frozen cases cannot move

**Insertion points (exact):**

1. **New module constant after `:58`** (the closing `)` of `RFC850_RE`): `ASCTIME_RE`
   = `^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|…|Dec)` + **` {1,2}[0-9]{1,2}`** + ` hh:mm:ss YYYY$`.
   The day field is the trap: the amendment's `(Nov) {1,2}[0-9]{1,2}` means **1–2 spaces between the
   month token and the digits**, not "separator space + padding". My first draft kept the space on
   the month alternative and then required ` {1,2}` → 2–3 spaces: c34 passed, c43
   (`Sun Nov 16 …`, one space, 2-digit day) failed with `[xrt_invalid_value]`, i.e.
   `a2_correct=11/12`. Counterfactual retained as `ScoutRecon/tool_badspacing.py` +
   `bad-spacing-run.log`. The patch landed in the worktree at recon time (`ASCTIME_RE` with
   `r"(Jan|…)"` then `r" {1,2}[0-9]{1,2} "`) has this right.
2. **`parse_rule`, one line at `:100`**: add `or ASCTIME_RE.match(value)` to the disjunction. Nothing
   else in `parse_rule` touches commas; `:103` already emits the raw value verbatim.
3. **`parse_field`, replace `:111`** with a merge-aware split; helper function inserted immediately
   before `:106`. The helper's predicate must mirror `:117` exactly — strip the segment, partition on
   the first `:`, unwrap one bot prefix only when `BOT_RE.match(head)` **and** `head.lower() not in
   KNOWN`, then require the remaining head lowercased `== "unavailable_after"` and the remaining rest
   stripped to be exactly one weekday token (`Mon`…`Sun`, `Monday`…`Sunday`). Then join exactly one
   following comma part (each comma-bearing shape has exactly one comma; a repeated bare weekday
   date joins again on the next iteration, measured in `p09`).
   - **Case-insensitive name is required for consistency**: `parse_rule` lowercases at `:71`, and t14
     already accepts `NoIndex`. `Unavailable_After: Wed, 03 Dec … GMT` merges only under an
     insensitive predicate (`p15`: base `invalid+unknown`, patched clean).
   - **Do not unwrap a known head**: `noindex: unavailable_after: Wed,` must stay invalid per `:73`
     / `:117`; A1's scope is "only `unavailable_after` values".
4. **Do not touch** `effective_of` (`:133`), `scope_findings` (`:157`), `audit` (`:199`),
   `render_text`, `load_manifest`, the finding vocabulary, or the exit alphabet (A3).

**No-regression proof.** I extracted the base file from git, applied exactly items 1–3 as a scratch
copy, and ran base vs predicted patch with `--json` over all 31 manifests of
`.ufo/waves/round-79/cases/c*/manifest.json`, comparing normalized report JSON **and** exit code:
`frozen_identical=31/31 diffs=0` (`ScoutRecon/results.json` summary; per-case table
`ScoutRecon/frozen-identity.txt`; both selftests print `selftest: 26/26 passed`, exit 0). Structural
reason the answer is "no" for each case: only **c16** and **c17** carry `unavailable_after`, both ISO
values with no comma, no weekday token and no asctime shape; no frozen field value contains a comma
that follows a weekday token, so the merge never fires; no frozen value is asctime-shaped, so the new
regex never matches; **c24** (`{not json`) and **c25** (schema `v2`) are input faults that never reach
`parse_field`; **c12** exercises the empty-segment path and **c22** the multi-header path, both
untouched. `c32-c43` (round-80) under the predicted patch match the oracle 12/12.

**Behaviour changes that are sanctioned but worth naming** (no case covers them; do not "fix" them
silently): `unavailable_after: Wed, noindex` loses `noindex` under A1 — the comma belongs to the value,
which then fails every shape (`p14`, base keeps `noindex`, patched drops it); `… PST` shrinks from
`invalid+unknown` to `invalid` only (A3, c37, `p08`); a repeated bare weekday date merges twice
(`p09`).

## 5. Selftest count and what A5 implies

- Current: 23 `_case` entries (`cases = [` at `:262`, entries `:263-323`, close `:324`; t01-t23) + 3
  fault documents (`faults = [` at `:333`) →
  `total = len(cases) + len(faults)` (`:350`), printed by `:351`. Measured at base and in the
  pre-edit worktree: **`selftest: 26/26 passed`, exit 0**. Existing date coverage is t15 (ISO), t16
  (`tomorrow` → invalid), t22 (two ISO dates → duplicate); nothing comma-bearing.
- A5 ("three accepted comma-bearing shapes, the asctime shape, and the segment boundary after a
  comma-bearing value") implies **at least 5 new `_case` entries → `selftest: 31/31 passed`** if the
  minimal set is added:
  - `t24` IMF-fixdate with seconds: `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (c32);
  - `t25` IMF-fixdate without seconds: `unavailable_after: Wed, 03 Dec 2025 13:09 GMT`
    (`RFC822_RE`'s optional-seconds branch — the third comma-bearing shape);
  - `t26` RFC 850: `unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` (c33);
  - `t27` asctime: `unavailable_after: Sun Nov  6 08:49:37 1994` (two-space day; pin the one-space
    2-digit day too, or c43 remains the only witness — see the c43 trap in §4);
  - `t28` segment boundary: `noindex, unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, noarchive`
    → three directives, no findings.
- Ambiguity to settle in the receipt: the only shapes that can carry a comma are IMF-with-seconds,
  IMF-without-seconds and RFC 850 (asctime has none), which makes the 5-case set the faithful minimum.
  If A5 meant IMF/RFC 850/asctime, the minimum is 4 and the count is 30. A5 fixes no number ("the count
  is whatever the tool prints"); a sixth negative case (`… PST` → `xrt_invalid_value` only, pinning
  A3) would print 32 — recommended, since c37's finding set is the one that *shrinks*.

## 6. Coordination findings for the L1 / ExecGrammar

1. **`controls/c80-selftest.txt` does not exist yet** (`ls .ufo/waves/round-80/controls/` has no such
   file). R79-3 (`c80_defect_queue.py:155-169`) compares the receipt's `selftest: N/N passed` line to
   a re-run of the tool and fails on mismatch. It must be captured **after** the A5 growth lands —
   capturing 26/26 now would fail against a 31/31 tool.
2. At recon end the worktree held a **partial** patch (`git diff --stat`: 18 insertions, 3 deletions;
   `DATE_COMMA_RE` at `:70`): docstring term, `ASCTIME_RE` (correct spacing) and `DATE_COMMA_RE`,
   but `parse_field:111` still splits naively and no `_segments` helper exists yet, so `DATE_COMMA_RE`
   is unused and c32-c43 still fail. Mid-flight, not a defect; the merge at `:111` is the remaining
   edit.
3. `DATE_COMMA_RE` as written matches an optional bot head `[A-Za-z0-9_-]+`; the caller must reject a
   head in `KNOWN` (its own comment says so) or `noindex: unavailable_after: Wed,` would merge against
   `:117`.
4. `c39`'s second date is RFC 850, not IMF; both merge identically (`results.json.a2.c39` is correct
   under the predicted patch).
