## Verdict

**P1 observedAt validation gap confirmed** in the byte-identical round-23 `measure_c1.py` at base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Of nine malformed/future cases exercised, eight returned exit 0 and accepted all 17 receipts. `2026-02-30` returned exit 1 only because the string prefix sorts before the lower-bound date, not because the runner validates its calendar date. All three accept controls passed.

This is an author-side sandbox audit, not an independent admission. No lane production file, index, or jj state was modified.

## Findings

### P1 — C1 observedAt prefix comparison admits malformed values (C2 operability, c1 population)

**Exact command pattern (executed once per listed revision):** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1ObservedAt-clone --revision <revision>`. Each command ran after a one-field mutation was committed in the sandbox with `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`; every mutation commit's parent was the frozen base. The output column gives exact observed runner values, including exit status, stderr/traceback, JSON acceptance count, mutated unit result, and stdout final line.

| Case | Revision passed to exact command | Exact observed output summary |
| --- | --- | --- |
| `c1-obs-date-suffix-garbage` | `4b7381ff3361aa097f3e5ecd5a0d3d58d410a323` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; drift-detection pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-hour-25` | `92277238eb22b673450255e58d4221207371a8a9` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; fire-journal-codes pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-no-offset` | `8b65b5b4463befd611507bdc66c058ab39ecb59e` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; fleet-registry pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-impossible-feb-30` | `49e21769a59a8749e67ed7684391d3df0d66fe88` | `exit=1; stderrBytes=0; traceback=false; accepted=16/17; free-read-verbs pass=false; problems=["observedAt missing or before 2026-10-21"]; stdoutTail="}"` |
| `c1-obs-impossible-month-13` | `598bd5ff02d2e4b416bbd8b9bb19cdf08ee10873` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; ghp-subpath-spotcheck pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-far-future-2099` | `4348635794619a1c15531b2928c3f73827e2273e` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; keeper-timer-inert pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-after-commit-2359` | `d8318a6a6362108c25d310e88b45e7a03fb0e82c` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; kimi-subpath-audit pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-nonascii-digits` | `dbb373ac300d9ebfcaa249b8d5e346d129e49ea0` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; mirror-pitfalls pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-free-text` | `cf67efe06a02de4868682af153ef00f55ac9bb52` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; ops-automation pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-dateonly-control` | `15d1995cabea603c5fba23ff8d6fc2861ce10933` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; origin-repos pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-datetime-control` | `3e55bd788b140fe7af0e3e54251eb69bfbc13477` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; publish-channels pass=true; problems=[]; stdoutTail="}"` |
| `c1-obs-lowercase-rfc-control` | `2d32176493700d9223fde4918877893f9f81e8dd` | `exit=0; stderrBytes=0; traceback=false; accepted=17/17; publish-queue pass=true; problems=[]; stdoutTail="}"` |

The runner's only observedAt test is `not isinstance(receipt.get("observedAt"), str) or receipt["observedAt"][:10] < "2026-10-21"` (`measure_c1.py`, line 55). RFC 3339 §5.6 requires its date-time components, including a complete time and offset; §5.7 constrains valid month/day combinations. RFC 5234 Appendix B.1 defines `DIGIT` as `%x30-39`, so fullwidth digits are not RFC 3339 digits. RFC 8259 §8.1 permits UTF-8 JSON, meaning the non-ASCII value is valid JSON text but not a valid RFC 3339 value. The date-only form is not an RFC 3339 date-time, but it is the actual `observedAt` form of all 17 round-23 receipts and the valid date-only control specified for this audit; keep it accepted under the existing receipt contract.

Python probe evidence: `re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", "２０２６-１０-２１")` is true, while the same pattern with `[0-9]` is false; `int("２０２６")` returns `2026`, and `date.fromisoformat("２０２６-１０-２１")` raises `ValueError`. Avoid Unicode-aware `\\d` or numeric conversion alone as grammar validation. RFC 3339 §5.6 also explicitly permits lower-case `t` and `z`; RFC 5234 §2.3 explains ABNF string case-insensitivity.

**Smallest fix:** replace the ten-character lexical test with explicit parsing/validation of the lane's date-only control and the supported RFC 3339 date-time form: ASCII digits, full calendar validation, required offset for a date-time, accepted lower-case `t`/`z`, and clear lower/upper time bounds. Catch parse failures as ordinary receipt rejection, never as a traceback. RFC 9110 §8.3.1 defines HTTP media-type syntax; it does not define `observedAt` and is not a basis for these C1 cases (the `contentType` issue is outside this scoped audit).

### P2 — Future observation values are accepted without a temporal upper bound (C2 operability, c1 population)

**Exact commands and observed output:** the `c1-obs-far-future-2099` and `c1-obs-after-commit-2359` commands above each returned `exit=0; stderrBytes=0; traceback=false; accepted=17/17; mutated unit pass=true; problems=[]; stdoutTail="}"`. The fixed sandbox committer time was `2026-10-21T12:00:00Z`; the accepted values were respectively `2099-12-31` and `2026-10-21T23:59:59Z`.

RFC 3339 validates syntax and instant representation, not whether an event is in the future. The rejection expectation here follows the round-24 contract's explicit gap description (“malformed or future” timestamps) and the meaning of `observedAt`: the second value postdates the commit recording it, and the first is in the far future relative to that same fixed record time. **Smallest fix:** after syntax/calendar validation, compare instants against the applicable recorded observation/evaluation bound rather than only a date prefix; retain and document the existing date-only control separately.

## Checked and held

- Frozen contract read: `.ufo/waves/round-24/contract.json`; round-23 C1 runner docstring says `observedAt >= 2026-10-21`, exit 0 for all accepted, 1 otherwise, and 2 for unreadable revision/population.
- Lane HEAD and clone HEAD both observed at `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; base commit time `2026-10-21T06:00:18-03:00`. Clone path: `/tmp/kake-r24-GapC1ObservedAt-clone`.
- Lane working-tree `measure_c1.py` SHA-256 and base-commit file SHA-256 both observed as `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5`.
- Unmodified base control command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1ObservedAt-clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436`; exact summary: `exit=0; traceback=false; stderrBytes=0; accepted=17/17; claimVerdicts={"HOLD":79,"STALE":55,"UNVERIFIABLE":42}; stdout last line="}"`.
- Two out-of-array probes (integer and null `observedAt`) each returned exit 1, no traceback, `accepted=16/17`, and `problems=["observedAt missing or before 2026-10-21"]`; they are not part of the 12-case JSON array because the assigned audit is malformed strings plus controls.
- An independent parsing rule checked the nine rejection values and three controls against their expectations (zero mismatches), and accepted all 17 base receipts against the base committer instant. It is a consistency check, not a replacement-runner test.
- RFC source pages read: RFC 3339 §§4.4, 5.6, 5.7; RFC 5234 §§2.3, B.1; RFC 8259 §8.1; RFC 9110 §8.3.1. No tooling was installed or updated.
- Retained per-case runner stdout/stderr and full commit/run metadata in `/tmp/kake-r24-GapC1ObservedAt-l0wL/`; JSON case array also stored there as `c2-gap-c1-observedAt.json`.

The following is the required C2 malformed-case array (9 expected rejects, 3 accept controls); `r23Observed` records each actual round-23 runner exit, traceback state, and stdout tail. **Notably, all 12 are cases actually committed and run.**

```json
[
  {
    "id": "c1-obs-date-suffix-garbage",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21garbage",
    "expect": "reject",
    "why": "Trailing characters after a valid day are not an RFC 3339 full-date or date-time (RFC 3339 section 5.6 productions have no suffix); the round-23 test compares only observedAt[:10], so the suffix is never examined.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-hour-25",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21T25:00:00Z",
    "expect": "reject",
    "why": "RFC 3339 section 5.6 defines time-hour as 2DIGIT ; 00-23, so hour 25 is not a valid date-time; the round-23 prefix test never reads the time part.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-no-offset",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fleet-registry.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21T12:00:00",
    "expect": "reject",
    "why": "RFC 3339 section 5.6 full-time requires a time-offset (Z or numeric), and section 4.4 calls unqualified local time unacceptable for Internet timestamps; the round-23 prefix test accepts it.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-impossible-feb-30",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/free-read-verbs.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-02-30",
    "expect": "reject",
    "why": "RFC 3339 section 5.7 caps February date-mday at 28 (29 in leap years), so 2026-02-30 is not a valid full-date; the round-23 runner rejects it only because '02' sorts before '10', so the impossible day is never tested.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-impossible-month-13",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/ghp-subpath-spotcheck.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-13-01",
    "expect": "reject",
    "why": "RFC 3339 section 5.6 defines date-month as 2DIGIT ; 01-12; the round-23 prefix test accepts 2026-13-01 because '3' sorts after '0' at the sixth character.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-far-future-2099",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/keeper-timer-inert.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2099-12-31",
    "expect": "reject",
    "why": "A valid RFC 3339 full-date (section 5.6) dated after the sandbox commit 2026-10-21T12:00:00Z that records it; the lane's own gap statement names future-looking observedAt strings as malformed.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-after-commit-2359",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/kimi-subpath-audit.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21T23:59:59Z",
    "expect": "reject",
    "why": "A valid RFC 3339 date-time (section 5.6) 11h59m59s after the committer time 2026-10-21T12:00:00Z that records it; an observation cannot postdate its commit, so the bound must compare instants, not calendar days.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-nonascii-digits",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/mirror-pitfalls.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "２０２６-１０-２１T１２:００:００Z",
    "expect": "reject",
    "why": "RFC 3339 section 5.6 is built on ABNF DIGIT, defined in RFC 5234 Appendix B.1 as %x30-39 (ASCII 0-9 only); RFC 8259 section 8.1 requires UTF-8 JSON, so the bytes parse and only the date grammar can reject them.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-free-text",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/ops-automation.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "unknown",
    "expect": "reject",
    "why": "Neither an RFC 3339 full-date nor date-time (section 5.6); the round-23 prefix test accepts it because 'u' sorts after '2'.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-dateonly-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/origin-repos.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21",
    "expect": "accept",
    "why": "Control: the date-only form 2026-10-21 is what all 17 round-23 population receipts carry (an RFC 3339 section 5.6 full-date); the replacement must keep the 17/17 control accepted. The sandbox commit is empty because the value is unchanged.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-datetime-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/publish-channels.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21T11:59:59Z",
    "expect": "accept",
    "why": "Control: a valid RFC 3339 date-time (section 5.6, time-offset Z) inside the window and before the committer time 2026-10-21T12:00:00Z.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-obs-lowercase-rfc-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/publish-queue.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21t11:59:59z",
    "expect": "accept",
    "why": "Control: RFC 3339 section 5.6 NOTE allows lower-case 't' and 'z' (ABNF string literals are case-insensitive, RFC 5234 section 2.3); Python's datetime.fromisoformat rejects this form, so a naive stdlib parse would over-reject.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  }
]
```

## Limits

- Probe scope is C1 `observedAt` grammar/temporal acceptance only. RFC 9110 §8.3.1 and `contentType` validation were not tested here.
- Round-23 runner receipts and all sandbox mutations were left unchanged; generated commits exist only in `/tmp/kake-r24-GapC1ObservedAt-clone`. No builds, linters, formatters, or tests were run. Parent integration/gate remains outstanding.
- The fixed commit-time comparison is test context for future values, not cryptographic proof of when a network observation happened; the round-24 contract itself describes future-looking timestamps as part of the gap.
