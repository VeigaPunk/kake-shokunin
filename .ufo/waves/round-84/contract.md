# kake round 84 — frozen contract (attempt 1)

Frozen at the freeze commit, before any seat of wave `w1` ran. No predicate, item, target or kill
rule below moves after a seat has scored; a later correction is an appended erratum that points, and
the frozen sentence stays the claim's sentence.

Base revision: the lane `master` tip at round open, 2026-11-04. Lane: `kake-shokunin`, axes
**operability + freshness** (plus calibration, the evidence-backed sub-axis added in round 54).

Two claims, distinct axes, causally separable:

- **C1 — calibration (score 2, the lowest non-retired axis).** The round-83 routed-defect queue
  closes. Population: `D1` … `D4` filed at `corpus/lessons/round-83-verifier-spotcheck.md` §6, frozen
  at round open; none added, none dropped.
- **C2 — freshness (score 10, held), capability acquisition.** A changed `policy`-class response
  header's **value** is classified, not only its name: the tool says whether the policy statement
  actually moved (a numeric parameter changed, a directive was added or removed, the field appeared
  or vanished) or whether only the directive order moved. Round 83's stated limit — "a `policy`
  header whose new value changes freshness semantics still reads `policy`" — is this claim's ground.

Both are author-side: admission belongs to the non-author closure, which is not this seat.

## C1 — predicate

    met <=> open == 0

over the four frozen items, decided by

    python3 -B .ufo/waves/round-84/c84_defect_queue.py --root <tree> [--revision <rev>] [--fleet <dir>]

which prints one `item=` line per item, then
`C1v1 revision=<token> items=4 open=<n> closed=<n> met=<true|false>`, exit 0 iff `met`.

Each item is a **state conjunct** re-derived from a non-lesson file plus a **row conjunct** only
prose can carry. An item is `closed` only when both hold; a missing or unreadable file reopens it.
The counter's output never decides an item from a sentence that merely says "closed".

| item | state conjunct (re-derived) | row conjunct |
|---|---|---|
| `D1` | `corpus/lessons/round-84.md` carries a line opening `[r84-correction` that names `round-83.md` and §`Gate`, and cites the four real RFC 9111 headings `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives`, `5.2.3.  Extension Directives`; **each** of those four heading strings is a raw substring of the retained RFC 9111 bytes at `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` | the correction line names `round-83.md` and `Gate` |
| `D2` | `corpus/lessons/round-84.md` carries one line matching `D2 count=<n> span=838-844 measure=words-full-span`, and `<n>` equals the word count the counter re-derives from the retained RFC 9111 bytes over lines 838–844 inclusive (`len(re.findall(r"\S+", "".join(lines[837:844])))`) | the same line names the span boundary `838-844` |
| `D3` | `.ufo/waves/round-84/w1-spec.json` item roles count `connector >= 1`, **and** `.ufo/waves/round-84/w1-results.json` carries at least one results row with `agent == "connector"` and non-empty output | the round lesson or `SCORECARD.md` names the connector seat |
| `D4` | `.ufo/waves/round-84/controls/census-before.txt` exists, records `census_exit=0`, and its `W04` line set equals the set the counter re-derives from the measured tree's `corpus/SOURCES.md` under the census's own rule (0–3 leading spaces tolerated; URL normalization strips scheme, fragment and one trailing slash, lowercases the host; a row collides when its normalized URL was seen before and this `(url, scope)` pair is new); its `ok` line names a `corpus/SOURCES.md` path | the round lesson names `controls/census-before.txt` |

Controls, committed at the freeze before any after-state:

- `controls/base-c84-defect-queue.txt` — the counter at the freeze revision, exit 1.
- `controls/ctl-c84-junk-queue.txt` — the counter over a tree whose lesson asserts all four items
  closed in prose and whose other files are absent, exit 1.
- `controls/c84-selftest-c1.txt` — the counter's selftest: one green all-four-closed tree, one junk
  prose tree, one mutant per item, and a missing-tree fixture.

## C2 — predicate

Declared surfaces are the three ids and urls frozen at `.ufo/waves/round-81/capture-expectations.json`
(`ds4cc-primary` `https://ds4cc.com/`, `ds4cc-robots` `https://ds4cc.com/robots.txt`,
`ds4cc-sitemap` `https://ds4cc.com/sitemap.xml`). Capture A is `.ufo/waves/round-81/capture`,
capture B is `.ufo/waves/round-82/capture`; the control and equivalence pairs are under
`.ufo/waves/round-84/capture-control/`. No network call is made by the tool or the counter.

    met <=> declared == 3
        and surfaces_a == 3 and surfaces_b == 3
        and receipts_ok      (GET, integer status 100..599, bytes == body length, sha256 == body
                              digest, truncated false, for all six real-pair receipts and all twelve
                              control-pair receipts)
        and real_changed == 0 and real_verdict == "policy-unchanged"
        and ctl_changed == 3 and ctl_mismatch == 0 and ctl_verdict == "policy-changed"
        and eq_changed == 1 and eq_mismatch == 0 and eq_verdict == "policy-rewritten-equivalent"
        and record_equal     (the committed real-pair record equals a fresh run's stdout after
                              stripping one trailing newline per side)
        and determinism      (two fresh runs print identical bytes)
        and tool_offline     (no `socket`, `urllib`, `requests` or `http.client` import in
                              `scripts/policy_value_class.py` outside its docstring)
        and selftest_ok      (the tool's `--selftest` exits 0)
        and counter_selftest_ok

decided by

    python3 -B .ufo/waves/round-84/c84_policy_values.py --root <tree> [--revision <rev>] [--work <dir>]

which prints
`C2v1 revision=<token> declared=… surfaces_a=… surfaces_b=… receipts_ok=0|1 real_changed=… real_verdict=… ctl_changed=… ctl_mismatch=… ctl_verdict=… eq_changed=… eq_mismatch=… eq_verdict=… record_equal=0|1 determinism=0|1 tool_offline=0|1 selftest_ok=0|1 counter_selftest_ok=0|1 met=<true|false>`,
exit 0 iff `met`.

### The tool's frozen CLI (the claim's instrument)

`scripts/policy_value_class.py` prints first one `change=` line per changed `policy`-class header,
sorted by `(surface, header)`, whose class is `policy` under the table
`scripts/header_change_class.py` freezes (imported, never copied):

    change surface=<id> header=<lowercased field name> class=<value-level class>

then, for every declared surface in declaration order, one line:

    surface=<id> changed=<k> reordered=<a> numeric_parameter=<b> directive_added=<c> directive_removed=<d> directive_changed=<e> header_added=<f> header_removed=<g> unclassified=<h> verdict=<v>

then one summary line:

    summary surfaces=<n> changed=<t> reordered=<a> numeric_parameter=<b> directive_added=<c> directive_removed=<d> directive_changed=<e> header_added=<f> header_removed=<g> unclassified=<h> verdict=<v>

with `v` one of `policy-unchanged`, `policy-rewritten-equivalent`, `policy-changed`,
`policy-unclassified` (decisive). Value-level class table, frozen:

- `reordered` — the value's directive multiset is unchanged and only its order moved.
- `numeric_parameter` — the directive names are unchanged and the only difference is the numeric
  value of one parameter (`max-age=600` → `max-age=60`).
- `directive_added` / `directive_removed` — the directive-name set only gained, or only lost, names.
- `directive_changed` — names unchanged but a non-numeric parameter (or its presence) differs, or
  names moved both ways.
- `header_added` / `header_removed` — the field is present on one side only.
- `unclassified` — the value does not parse under the frozen grammar (comma-separated
  `name[=parameter]`); decisive, so a field that cannot be read is never waved through.

Verdict rule: `policy-unchanged` when `changed == 0`; `policy-rewritten-equivalent` when every
change is `reordered`; `policy-unclassified` when any change is `unclassified`; otherwise
`policy-changed`. A surface's verdict is `policy-unchanged` when it has no changed policy header,
and the summary verdict is the strongest surface verdict in the order
`policy-unchanged < policy-rewritten-equivalent < policy-changed < policy-unclassified`.

Exit 0 printed, 1 unevaluable input, 64 usage. It verifies receipts exactly as round 83's classifier
does (GET, integer status, byte count, body sha256, not truncated) and is offline by construction.

### Frozen control expectations

`.ufo/waves/round-84/policy-expectations.json` freezes what each synthetic control pair must
classify, built by `.ufo/waves/round-84/build_control_pairs.py` at the freeze:

| pair | surface | header | change | expected class |
|---|---|---|---|---|
| `control` | `ds4cc-primary` | `cache-control` | `max-age=600` → `max-age=60` | `numeric_parameter` |
| `control` | `ds4cc-robots` | `x-frame-options` | absent → `SAMEORIGIN` | `header_added` |
| `control` | `ds4cc-sitemap` | `referrer-policy` | `no-referrer, strict-origin` → `strict-origin, no-referrer` | `reordered` |
| `equivalent` | `ds4cc-sitemap` | `referrer-policy` | `no-referrer, strict-origin` → `strict-origin, no-referrer` | `reordered` |

The `equivalent` pair exists so an order-only rewrite cannot pass as a policy change; the `control`
pair exists so a real change cannot pass as a rewrite. Both pairs are synthetic by construction:
their bodies and digests are the round-81 capture's, their receipts are copied and only the header
list (and `headerCount`) is edited. `referrer-policy` is seeded into both sides of both pairs so the
reorder has a value to reorder.

Controls, committed at the freeze:

- `controls/base-c84-policy-values.txt` — `tool_absent=1 met=false`, exit 1.
- `controls/c84-selftest-c2.txt` — the counter's selftest.

## Kill rules (frozen)

- A counter that reaches `met` on its junk/prose control is a broken counter: the control's receipt
  is committed anyway and the claim reports `unprovable` for this round.
- A claim whose counting command exits non-zero at the after-state reports `unprovable`; it is never
  narrated green.
- Narrowing a target after landing is a miss, reported as an honest stop.

## Wave shape (frozen at dispatch)

One v1 wave, band 8–16 (run-15). Minimum role split from prompt §3: connector ≥ 1, executor ≥ 3,
scribe ≥ 1, scout ≥ 1, reviewer ≥ 1, critic ≥ 1; attack share ≥ 25 % over
{reviewer, critic, mutation-tester, labrat}. The L1 holds the planner seat; the bounded planning
data-walk rides the `connector` seat, whose sibling-overlap scan is this round's connector duty.
