# ExecRobotsTool — round-38 C2 build (operability)

Built C2: `scripts/robots_audit.py` at `2dab7f31` amended to the round-38 contract (rules (h), (i),
(k); the round-37 contract kept). Work happened only in my sandbox; the lane, its jj state and Git
index are untouched, and I never entered `/fast/scratch/hyaku/kake-r38*` or looked for the key.
I did not open `.ufo/waves/round-38/retained/controls/` or the `ctl/` code.

## Deliverables (sandbox `/fast/scratch/hyaku/kake-r38w1/ExecRobotsTool/`)
- `final_robots_audit.py`, same bytes as `clone/scripts/robots_audit.py`, sha256
  `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace` (base bytes
  `944d2f51…d3e5`; identical at `af43a50f` and `2dab7f31`).
- `robots_audit_r38.patch`, sha256 `7484d3280daa93f2ec925b6aa26b5d08d0d197192b74e66e6217175983d9e91d`,
  unified diff vs `af43a50fa399881eead9381d835b78a015e277a6`: 86 added / 10 removed lines (15 of
  the added lines blank), 8 hunks, docstring plus the three rules only.
- `r38_selftest.py` (36 cases, `be78adb…`), `r38_probes.py` (`bbda4df…`);
  receipts `own_selfcheck_final.txt` (`a5582ef…`), `probes_final.txt` (`7e73178…`),
  `perf_final.txt` (`58bf8f3…`), `r37_counter_receipt.json` (`3367198…`),
  `selftest_receipt.json` (`a571857…`), `charset_check.txt` (`81219c8…`); case dirs under `cases/`,
  64 MiB inputs under `perf/`.

## Change and readings (final line numbers)
- (h): `json.loads(..., parse_int=parse_json_int, parse_constant=reject_json_constant)` at :465.
  `NaN`/`Infinity`/`-Infinity` outside a string raise in `reject_json_constant` (:429), so the
  manifest is one `input_invalid` and nothing is evaluated. `parse_json_int` (:421) counts digits
  and returns the `_LONG_INTEGER` sentinel (:409) above `_INT_TOKEN_DIGITS` = 15 (:154): no `int()`
  call on long tokens, so neither the 4300-digit `ValueError` nor quadratic conversion occurs. The
  sentinel is not an `int`, so a long `robotsStatus` is `check_invalid` (others still evaluated), a
  long `version` is `input_invalid`, and a long number in an unread field changes nothing. `1e400`
  stays a float, hence not an integer status.
- (i): `url_characters_ok` (:508) applies `_URL_FORBIDDEN_RE` (:149) inside `parse_http_url` before
  `urlsplit` (:517). Exactly the 43 forbidden ASCII characters are rejected (space, U+0000–U+001F,
  U+007F, `"` `<` `>` `\` `^` `` ` `` `{` `|` `}`); non-ASCII is kept. `charset_check.txt` shows
  allowed 85, forbidden 43, regex set equal, non-ASCII and empty strings accepted.
- (k): `audit_manifest` (:605) normalizes the path once and compares it to `/robots.txt`; `%2E` and
  `%72` forms are allowed, `?x=1`, `/ROBOTS.TXT`, `%2F`, `/robots.txt/` go to the rules, an empty
  query is the implicit allow, and `Disallow: /robots.txt` cannot override it.
- Docstring: the old raw-path reading is replaced with (k); (h) and (i) readings added; title and
  contract summary name the C2 amendments. No other behaviour touched; stdlib only, no network,
  writes or subprocess.

## Harm instruments on the final file (sha `f4d057c4`)
- `python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --tool-file scripts/robots_audit.py
  --key-revision 424aa248` → exit 0, `passed: 28 / 28`, `target: 25`, `met: true`,
  `toolSha256 f4d057c4…` (`r37_counter_receipt.json`).
- `python3 -B scripts/robots_audit_selftest.py --tool scripts/robots_audit.py` → exit 0,
  `137/137`, verdict `clean`, perContract a13 b19 c15 d17 e16 f27 g15 usage7 verdict8.
- Both also held 28/28 and 137/137 on the intermediate build `a1d4590b`; only docstring text changed
  after that.

## My own manifests (36, written from the amendment text only)
- `python3 r38_selftest.py --tool clone/scripts/robots_audit.py` → exit 0, 36/36. Includes `NaN`
  inside a string; `NaN`/`Infinity`/`-Infinity` outside; `1e400` status; `-0` as status and unused;
  5000-digit and 16-digit statuses; long `version`; long number in an extra field; 14 excluded
  characters in one manifest; `%zz`; non-ASCII URL; `robots%2Etxt`; `%72obots.txt`; `/robots.txt?x=1`;
  `/robots.txt?`; `#frag`; `/ROBOTS.TXT`; `/robots%2Ftxt`; `/robots.txt/`; escape plus query.
- The same driver on the base bytes → exit 1, 18/36; it fails 7 of 13 (h), 7 of 10 (i), 4 of 13 (k)
  (`base_selfcheck.txt`, `a702842…`).
- `python3 r38_probes.py` → exit 0 (`probes_final.txt`): 43 characters × 6 positions = 258 checks,
  all `check_invalid`, `checksEvaluated` 0, exit 2 (base: 248 evaluated, 10 findings); ten long
  statuses (4300, 4301, 5000, 100000, 1000000 digits, each sign) all `check_invalid` with the
  neighbouring check evaluated (base: a single `input_invalid`, evaluated 0); the same tokens in
  unread fields change nothing; six implicit-allow and six rule-decided `/robots.txt` forms exactly
  as declared (base emits three extra findings).
- Timing (`perf_final.txt`): 64 MiB single-integer `robotsStatus` 0.080/0.082/0.095 s (exit 2,
  `check_invalid`); 64 MiB single integer in an unread field 0.075/0.082 s (clean, evaluated 1);
  64 MiB of 33 554 412 small integers 2.13 s (clean). All far inside the 20 s bound.

## Not verified, risks, blockers
- Counter v3 was not run and C2's score is unmeasured by me (sealed key; no access by design).
- The 15-digit sentinel threshold is a lane reading, documented in the docstring; it is observably
  exact because the only integers the contract reads are `version` (1) and `robotsStatus` (3 digits).
  Duplicate JSON member names remain undecided and untested, as declared.
- Per-integer Python callback overhead: a manifest of millions of small integers costs ~2.1 s at the
  64 MiB cap (C-level `json` default would be faster); still within the bound.
- `checksEvaluated` semantics are unchanged and asserted on every one of the 36 cases and all probes.
- No tool installs or upgrades; no network use. No blockers.
