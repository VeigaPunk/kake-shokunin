# kake round 79 — frozen contract (attempt 1)

Frozen before any seat ran. Base revision `0898085450ee1b65d910f1dcb7a0efc20b413b88`
(lane `master` tip at round open, 2026-11-04). Lane checkout:
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Round shape: one v1 wave `w1`, 14 seats
(scout 2, executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1,
sentinel 1; attack share 4/14 = 28.6 %). The L1 holds the canonical planner seat; a bounded
planning data-walk rides the `Connector` and `Critic` items.

Axes owned by the lane: **operability + freshness**, plus **calibration** as a round-54
evidence-backed sub-axis. The lowest non-retired axis is calibration (score 2), so C1 works
it. Scores are held; a claim moves evidence, not a scalar.

## Claims

### C1 — calibration: receipt-rewrite disclosure is complete and enforced as a standing gate

The lane's calibration ledger (`.ufo/waves/round-58/receipt-rewrites.json`) discloses every
post-freeze change to a committed measurement receipt. It was not kept current: the frozen
round-58 counter, re-run at the base, reports **5 undisclosed receipt rewrites** — two in
round 75 (`controls/after-harm-battery.txt`, at `3ae076ab3e01` and `0df52aed0b68`), three in
round 78 (`controls/base-c2-sweep.txt` at `c758904c15c2`, `controls/after-c1-population.txt`
and `controls/after-c3-matrix.txt` at `406021c765fd`). The round-78 non-author closure found
only the one it had already traced (its R1); the gate finds five.

C1 makes the record current and the gate standing:

1. every undisclosed event gains a ledger entry with its true `fromBlob`/`toBlob`, its
   byte-level `kind`, and a note naming a repo-relative path that exists at the measured
   revision and records the rewrite (append-only `[r79-correction 2026-11-04]` rows in
   `corpus/lessons/round-75.md` and `corpus/lessons/round-78.md`);
2. the disclosure rule enters `corpus/QUALITY.md` as a criterion with an able-to-fail
   control;
3. a standing, round-agnostic counter replaces the round-58-scoped predicate.

**Counter.** `python3 -B .ufo/waves/round-79/c79_receipt_ledger.py --root . --revision <rev>`
(imports the frozen round-58 event/ledger/classification semantics; generalizes only the
predicate).

**Predicate (frozen).**

    met <=> undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0
           AND unpointed == 0 AND symlinks == 0 AND round_rewritten == 0

`round_rewritten` counts receipt events on `.ufo/waves/round-<--round>/control(s)/` paths
(`--round` default 79) — the round-58 `new_rewritten` rule, parameterized. The round-58
`new_receipts == 2` conjunct is dropped: it pinned a file count of one round, not a rule.

**Before → after.** Base `0898085`: `undisclosed=5 ... met=false`, exit 1. Carrier: the five
events disclosed, `undisclosed=0`, `met=true`, exit 0. The frozen round-58 counter must also
print `undisclosed=0 met=True` at the carrier (cross-check, not the claim's counter).

**Kill rule.** The claim dies if the after receipt is not byte-exactly reproducible by the
closure with the command above at the measured revision, or if any ledger entry fails the
counter's `phantom`, `malformed`, `wrong_kind` or `unpointed` checks, or if any note points
at a path that does not record the rewrite.

**Controls (committed before any after-state).**

- `controls/base-c1-receipt-ledger.txt` — the base run (`undisclosed=5`, `met=false`, exit 1):
  the do-nothing control. A round that only *says* the ledger is current cannot move it.
- `controls/ctl-c1-fabricated.txt` — a scratch ledger with five invented `toBlob` values:
  must be red (`phantom`/`wrong_kind`/`malformed` > 0).
- `controls/ctl-c1-drop-one.txt` — a scratch ledger with four of five entries: must be red
  (`undisclosed=1`).
- `controls/ctl-c1-cheap-note.txt` — a scratch ledger whose notes are empty strings: must be
  red (`malformed>0`).
- `controls/c1-selftest.txt` — the counter's own selftest.

### C2 — operability (capability): offline X-Robots-Tag declaration audit

S449 (the round-78 robots-meta row) scopes itself to page-level directives and explicitly
excludes **header processing**. The header carrier is real publisher ground — useful for
non-HTML resources and for hosts that can set response headers — and it has its own grammar:
multiple `X-Robots-Tag` field lines, comma-separated rules, and the optional
`<bot-name>:` scope ("An optional `<bot-name>:` specifies the user agent that the subsequent
rules should apply to", S452). The lane holds no instrument for it.

C2 lands `scripts/x_robots_tag_audit.py`: it reads a version-1 manifest of recorded response
header fields plus URLs, read-only and network-free, and decides for every check the declared
directive set, the effective global restriction set and the per-bot sets, with a closed
finding vocabulary. It fetches nothing, judges no crawler behaviour and claims no live
property.

**Counter.** `python3 -B .ufo/waves/round-79/c79_xrt_matrix.py --root . --tool-revision <rev>
--cases .ufo/waves/round-79/cases --expect .ufo/waves/round-79/expect/expect.json --consts
.ufo/waves/round-79/consts --work <scratch>` (same CLI accepts `--tool <worktree path>` for
pre-commit runs; exactly one of the two).

**Predicate (frozen).**

    met <=> decided == cases AND wrong == 0 AND constants_failed == 4/4 AND selftest_ok

`decided` counts cases whose run produced a parseable `x-robots-tag-report/v1` JSON object;
`wrong` counts decided cases whose exit, finding-id set, or per-check `directives`/`effective`/
`bots` sets differ from `expect/expect.json`. A case is compared on **all** of: exit code,
the report's global finding-id list, and every check's three sets. `selftest_ok` is the
counter's own `--selftest` result at the measured run (it is re-run inside every measurement).

**Before → after.** Base `0898085`: `git cat-file -e <rev>:scripts/x_robots_tag_audit.py`
exits 128 (`controls/base-c2-tool-absent.txt`), matrix `decided=0 met=false` exit 2. Carrier:
`decided=31 correct=31 wrong=0 constants_failed=4/4 met=true` exit 0.

**Kill rule.** The claim dies if the measured bytes are not the bytes named by the receipt
(tool sha256 + bytes in the receipt must equal `git show <rev>:scripts/x_robots_tag_audit.py`),
if any case in `expect/expect.json` is undecided or wrong, if fewer than four constants fail,
or if the counter's selftest does not pass on the measured run.

**Controls (committed before the tool exists).**

- `controls/base-c2-tool-absent.txt` — `git cat-file -e` rc 128 at the base.
- `controls/base-c2-matrix.txt` — the matrix at the base (`decided=0`, exit 2).
- `controls/ctl-c2-constants.txt` — the four degenerate constants run through the frozen
  matrix before the tool exists; each must fail ≥1 case.
- `controls/c2-selftest.txt` — the counter's own selftest.

**Real-input run.** The 12 recorded surfaces of round 61 (`capture/*/response.json`) yield
`realrun/manifest.json`; the audit at the carrier must exit 0 and report `checks=12`. That is a
statement about those recorded header sets only, not about the live hosts today.

## C2 tool interface (frozen)

`scripts/x_robots_tag_audit.py --manifest PATH [--json]`; default text output.

Manifest (`x-robots-tag-manifest/v1`):

```json
{"schema": "x-robots-tag-manifest/v1",
 "checks": [{"id": "c01", "url": "https://example.test/page",
             "headers": [{"name": "X-Robots-Tag", "value": "noindex, nofollow"}]}]}
```

Strictness: `schema` must equal the literal; `checks` a non-empty list; `id` a non-empty
string, unique; `url` a non-empty string; `headers` a list of `{name: non-empty string,
value: string}`; extra keys are ignored. Unknown header names are ignored (only fields whose
name is ASCII case-insensitive `x-robots-tag` are read). Zero such fields is a valid check
with empty sets.

Grammar (pinned readings; the source is S452, the directive vocabulary is S449+S452):

1. Each `x-robots-tag` field value is split on ASCII `,`; every segment is trimmed of ASCII
   whitespace. An empty segment yields `xrt_empty_rule`.
2. A segment whose first `:` prefix is `^[A-Za-z0-9_-]+$` **and whose lowercased prefix is
   not a known directive name** is a bot scope: the prefix is the bot name (normalized
   lowercase), and the remainder (after `:`) is one rule parsed under that scope. A segment
   of that shape with an empty remainder yields `xrt_bot_scope_empty` and adds no bot entry.
   The scope persists for the remaining segments **of that field value**; a new bot scope
   replaces it. Scope does not cross field lines (a field without a prefix is global).
3. Otherwise the segment is a directive: split at the first `:` into name and optional value;
   name lowercased. Known names: `all, index, noindex, follow, nofollow, none, nosnippet,
   indexifembedded, max-snippet, max-image-preview, max-video-preview, notranslate,
   noimageindex, unavailable_after`. An unknown name yields `xrt_unknown_directive` and the
   segment contributes nothing.
4. Values: value-less directives (`all, index, noindex, follow, nofollow, none, nosnippet,
   indexifembedded, notranslate, noimageindex`) with a value yield `xrt_invalid_value` and
   contribute their name. `max-snippet`/`max-video-preview` require `^-?\d+$` (else
   `xrt_invalid_value`, dropped). `max-image-preview` requires `none|standard|large`
   (case-insensitive; normalized lowercase; else `xrt_invalid_value`, dropped).
   `unavailable_after` requires one of the three frozen date shapes (below; else
   `xrt_invalid_value`, dropped).
5. Frozen date shapes for `unavailable_after`: ISO 8601
   `^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:\d{2})?)?$`; RFC 822
   `^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
   \d{4} \d{2}:\d{2}(:\d{2})? GMT$`; RFC 850
   `^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), \d{2}-(Jan|Feb|Mar|Apr|May|
   Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2} \d{2}:\d{2}:\d{2} GMT$`. A date-only ISO value is
   accepted (a stated limit of this lane grammar).
6. Normalization: `none` expands to `noindex` + `nofollow`; `all` contributes nothing;
   `index`/`follow` are kept as declared positive tokens. `index` with `noindex`, or `follow`
   with `nofollow`, in one scope yields `xrt_mutually_exclusive`. `indexifembedded` in a scope
   without `noindex` yields `xrt_indexifembedded_without_noindex`. The same value-bearing
   directive twice in one scope yields `xrt_duplicate_directive`; duplicate value-less
   directives are harmless.
7. `directives` = the declared, normalized tokens of the **global** scope (duplicates kept;
   sorted). `bots` = map bot name → the same for that scope, entries only for scopes that
   carried at least one rule (sorted keys and sorted lists). `effective` = the global
   restrictions: positives (`all`, `index`, `follow`) removed; when `nosnippet` is present,
   `max-snippet:*` and `max-video-preview:*` removed; duplicate `max-snippet`/
   `max-video-preview` collapse to the **minimum** numeric value. Sorted. Per-bot effective
   resolution is out of scope (stated limit).
8. Findings are per check, a sorted **unique** id list; the report's top-level `findings` is
   their sorted unique union. Finding ids: `xrt_empty_rule`, `xrt_bot_scope_empty`,
   `xrt_unknown_directive`, `xrt_invalid_value`, `xrt_mutually_exclusive`,
   `xrt_indexifembedded_without_noindex`, `xrt_duplicate_directive`.
9. Exit: 0 no findings, 1 findings present, 2 input fault, 64 usage. Input faults carry ids
   `xrt_input_unreadable`, `xrt_input_bad_json`, `xrt_input_schema`,
   `xrt_input_duplicate_id`, `xrt_input_check_shape`; the JSON report is
   `{"schema":"x-robots-tag-report/v1","error":{"id":...,"detail":...},"exit":2}` and no
   partial check results are emitted. `--json` prints exactly one JSON object and nothing
   else; text mode prints one `check <id> directives=[..] effective=[..] bots={..}
   findings=[..]` line per check and a final `XRTv1 checks=<n> findings=<k> exit=<c>` line.

## Round shape and seats (frozen)

The case set is `.ufo/waves/round-79/cases/c01…c31` with the oracle outside the case dirs at
`.ufo/waves/round-79/expect/expect.json`; the counter copies each manifest to scratch before
passing it to the tool (opaque input). Four degenerate constants live in
`.ufo/waves/round-79/consts/`. No case or expectation is edited after the first measurement;
a late finding is reported, not folded in.

| Seat | Role | Item |
|---|---|---|
| ScoutSources | scout | Re-open S452 candidate bytes and the two rejected candidates; locate the quotes the entry and Gate use; report whether any existing registry row covers the header carrier |
| ScoutRealInput | scout | Inventory the 12 round-61 captures + the ds4cc source tree; build `realrun/manifest.json`; report which surfaces declare X-Robots-Tag |
| ExecC2Tool | executor | Implement `scripts/x_robots_tag_audit.py` to this contract; run the frozen matrix to met; receipt |
| ExecC2RealRun | executor | Real-input run, instrument-receipt update (`scripts/instrument_receipts.py`), tool digest receipt |
| ExecC1Ledger | executor | Author the five ledger entries (true blobs/kinds) + append-only lesson correction rows; run the c79 counter to met |
| ExecR2R3 | executor | R2: selftest receipt on the landed `c78_shonen_population.py` bytes; R3: scratch-root fix + SCORECARD HOLD correction + `exit=` standard |
| ScribeKnowledge | scribe | `corpus/knowledge/x-robots-tag-header.md` + the S452 SOURCES row (Gate quote, access date) + coverage-map row |
| ScribeRecord | scribe | `corpus/lessons/round-79.md`, `corpus/QUALITY.md` criterion, SCORECARD round-79 section, LOG.md entry |
| ReviewC1 | reviewer | Attack C1: re-derive every blob/kind, check notes actually disclose, try false-positive and drop-one entries |
| ReviewC2 | reviewer | Attack C2: case table vs S452, adversarial manifests, constants, real-run claims |
| CriticC | critic | Falsify the predicates and targets: do-nothing reachability, causal separability, harm to held axes |
| MutC | mutation-tester | Mutate the new tool and the c79 counter; require named kills or a routed survivor |
| ConnectorC | connector | Sibling-overlap scan: which lanes hold X-Robots-Tag / receipt-disclosure ground; pattern reuse |
| SentinelC | sentinel | Security: manifest path handling, symlink/FIFO, unbounded reads, output writes, oracle isolation |

## Scratch

`$HYAKU_SCRATCH/kake-r79/<SeatName>/`, `HYAKU_SCRATCH` defaulting to `/fast/scratch/hyaku`.
Every counter honours `TMPDIR` and accepts an explicit `--work`; nothing citable lives under
`/tmp`.

## Assumptions and limits stated before data

- S452 is MDN (tier B): the directive vocabulary is cross-checked against S449 (tier A); a
  conflict between the two is reported, and S449 wins where it speaks to Google's own
  processing.
- The audit judges declarations, never crawler behaviour, live serving, rendering or
  robots.txt interaction.
- `unavailable_after` accepts only the frozen date shapes; RFC 822/850 branches are pinned by
  cases, not by a general date library.
- Per-bot effective resolution, cross-carrier (meta + header) conflicts, and header
  inheritance across redirect hops are out of scope.
