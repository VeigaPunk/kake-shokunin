# ExecControls — round 89, wave 1: adversarial shortcut controls for C2

Seat: ExecControls. Scope: build shortcut stubs for the C2 Vary-nominated
cache-key counter (`c89_key.py`), measure which property class kills each,
state the contract clause each violates, and flag any stub that reaches
`met=true` (a counter defect, reported not fixed).

## Method

15 stubs written under `.ufo/waves/round-89/w1/ExecControls/adv-*.py`. Each is
a from-scratch implementation of the `c2-contract.md` interface (stdin JSON →
`{"key": ...}` / `invalid_input:` exit 1) carrying exactly one deliberate
defect, so the counter's three scored layers (16 frozen cases, 200 generated
properties at seed 89089, 9 refusal items) isolate the violated clause.

Each stub was scored by importing the frozen counter itself
(`c89_key.score_candidate(source, work, seed)` from a byte-identical scratch
copy of `c89_key.py`) — the same code path `main()` uses for
`--candidate scripts/cache_key.py`. No production files touched; scoring ran
in `/fast/scratch/hyaku/kake-r89/ExecControls/` (deleted after receipts were
copied).

Receipts:
- `w1/ExecControls/scoring-receipt.txt` — per-stub one-line counts.
- `w1/ExecControls/scoring-detail.txt` — per-stub counts, first failing
  property class, all failed classes, frozen/refuse failure labels.

Note on `controls=`: the counter's `score_controls()` resolves its
`CONTROLS` dir relative to the counter file (`HERE / 'controls'`). My
scratch copy therefore globbed an empty dir and printed `controls=0/0`; that
line is a scratch artifact, not a counter result. The candidate triple
(frozen/props/refuse) is unaffected — it does not depend on `CONTROLS`.
Against the real lane the committed stubs still score `controls=5/5`
(base-c2.txt), so `met` for a candidate additionally requires
`controls=5/5`, which is constant across my runs.

## Results — the five mandated stubs

| stub | defect | frozen | props | refuse | first failing prop class | clause violated |
|---|---|---|---|---|---|---|
| adv-lower-values | values `.lower()`ed | 15/16 | 180/200 | 9/9 | `value_case` | §3 values byte-exact, no case folding |
| adv-sort-no-escape | members sorted; separators emitted raw (only `%`→`%25`) | 15/16 | 185/200 | 9/9 | `separator_collision` | §4 separators → `%1C`–`%1F`, none raw in a component |
| adv-uri-only | full validation, key = `ESC(uri)` alone | 6/16 | 120/200 | 9/9 | `value_case` | canonical form: key built from URI + nominated names + values |
| adv-space-trim | values strip `' '` only, HTAB kept | 15/16 | 180/200 | 9/9 | `value_edge_ows` | §3 value trimmed of SP **and HTAB** |
| adv-absent-empty | absent member emits `RS` with no `GS` | 15/16 | 180/200 | 9/9 | `absent_vs_empty` | absent (`GS`) ≠ present-empty (`''`) |

None of the five reaches `met=true`. Each is killed by exactly the property
class its clause maps to, plus one frozen case — the counter's class→clause
coverage is tight for these five.

`adv-uri-only` detail: frozen 6/16 (only the no-vary/empty-vary cases pass),
props 120/200 — every `same` relation passes trivially (identical keys) and
every `different` relation fails except `uri_change` (URI really does
differ). First failing class `value_case`; also fails `absent_vs_empty`,
`separator_collision`, `percent`.

## Additional probes (10)

| stub | defect | frozen | props | refuse | met |
|---|---|---|---|---|---|
| adv-wildcard-ok | `*` member treated as a field name | 15/16 | 200/200 | 8/9 | false |
| adv-member-ows | vary members not OWS-trimmed | 13/16 | 40/200 | 8/9 | false |
| adv-no-sort | pairs emitted in vary order | 15/16 | 180/200 | 9/9 | false |
| **adv-no-dup-vary** | case-insensitive dup members keyed, not refused | 16/16 | 200/200 | 9/9 | **true** |
| **adv-no-uri-escape** | URI emitted raw | 16/16 | 200/200 | 9/9 | **true** |
| **adv-no-name-escape** | field names emitted raw | 16/16 | 200/200 | 9/9 | **true** |
| **adv-cr-only** | CR accepted, only LF refused | 16/16 | 200/200 | 9/9 | **true** |
| **adv-missing-headers** | absent `request_headers` → `{}` | 16/16 | 200/200 | 9/9 | **true** |
| **adv-bad-json** | no JSON guard → traceback | 16/16 | 200/200 | 9/9 | **true** |
| **adv-raw-sort** | members sorted by raw case, not lowered | 16/16 | 200/200 | 9/9 | **true** |

## Counter defects found — 7 stubs reach `met=true`

Each was re-run on a hand-built discriminating input the counter never
generates; all seven violate `c2-contract.md` yet score a perfect
`frozen=16/16 props=200/200 refuse=9/9`:

1. **adv-no-dup-vary** — `vary:"A,a"` → contract refuses case-insensitive
   duplicate members; stub emits both pairs. *Gap:* no frozen case, no
   `REFUSALS` item, and `_rand_case` (`rng.sample`, unique names) never
   generates a duplicate member, so the duplicate-member refusal clause is
   completely untested.
2. **adv-no-uri-escape** — `uri:"https://e.test/50%"` → contract escapes
   `%`→`%25` in the URI; stub emits `50%` raw. *Gap:* every frozen and
   generated URI is `%`- and separator-free (`https://e.test/{a,b,c/d,
   p?q=1,r#f}`), so URI escaping is untested. (Name/value escaping *is*
   tested — `percent-escaped`, `separator-in-value-escaped`, props
   `percent`, `separator_collision`.)
3. **adv-no-name-escape** — `vary:"a%b"` → contract escapes names; stub
   emits `a%b` raw. *Gap:* `%` is a legal `token` char but no test name
   contains it (`NAMES` list and frozen varies are all `%`-free), so name
   escaping is untested.
4. **adv-cr-only** — value `x\ry` → contract refuses "CR or LF"; stub
   accepts (checks `\n` only). *Gap:* the only newline-bearing case
   (`lf-value-refused`) uses LF; CR-only is untested.
5. **adv-missing-headers** — `{"uri":"u","vary":"a"}` with no
   `request_headers` key → contract refuses "missing or not an object";
   stub treats missing as `{}`. *Gap:* every scored input includes
   `request_headers` (the `headers-not-object` refusal uses `[]`, not an
   absent key).
6. **adv-bad-json** — stdin `{not json` → contract refuses "input is not a
   JSON object"; stub dies with a traceback (exit 1 but stderr lacks the
   `invalid_input:` prefix). *Gap:* every scored payload is well-formed
   JSON; `not-an-object` sends `[]` (valid JSON, wrong type).
7. **adv-raw-sort** — `vary:"B,a"` → contract sorts by the *lowercased*
   name (`a` then `b`); stub sorts raw members case-sensitively (`B`<`a`
   → `b` then `a`). *Gap:* all generated members are lowercase and frozen
   members are `Accept*`/lowercase where raw and lowered order coincide;
   no test distinguishes case-sensitive from case-insensitive member sort.

### Assessment

The counter's **property population is doing real work** — the five
mandated semantic shortcuts each die on exactly their mapped class, and
`member-ows` shows the exit-code path also bites (props 40/200, first fail
`name_case`, 8 of 10 classes hit). But the **frozen cases + 9 refusal items
+ 10 property classes leave seven contract clauses with zero coverage**:
duplicate-member refusal, URI escaping, name escaping, CR-only refusal,
missing-`request_headers` refusal, malformed-JSON refusal, and
case-insensitive member ordering. A candidate implementing the contract
*except* any one of those seven scores `met=true` — i.e. the C2 counter as
frozen would admit 7 distinct contract violations. This is a defect in the
round's own measurement, reported per seat rules; not fixed here (L1 owns
integration; counters are frozen).

Suggested minimal additions for a future counter revision (for L1's
consideration, not applied): one frozen or refusal item per clause —
`vary:"A,a"`, a URI containing `%` or a separator, a vary/name containing
`%`, a value containing `\r` only, an input omitting `request_headers`, a
non-JSON stdin payload, and a mixed-case vary like `"B,a"` asserting
lowercased-name order.

## Honest limits

- Scoring used `score_candidate()` directly (same function `main()` calls);
  the `controls=5/5` conjunct was not re-measured in scratch (empty
  `CONTROLS` glob) but is invariant — it scores the committed `ctl-*.py`
  stubs, not my candidates.
- `props_ok` counts per-pair; `n_prop_fail_entries` in the detail file is
  the number of failing (label,input-pair) draws, which for a killed class
  equals its 20 draws.
- The seven `met=true` results are counter-coverage findings, not claims
  that those stubs are "correct" — each was verified to diverge from
  `c2-contract.md` on the discriminating input noted above.
- No tools installed; no network used; scratch deleted after receipts
  copied (see below).

## Files

- `w1/ExecControls/adv-*.py` — 15 stub candidates (5 mandated + 10 probes).
- `w1/ExecControls/scoring-receipt.txt`, `scoring-detail.txt` — receipts.
- This report.
