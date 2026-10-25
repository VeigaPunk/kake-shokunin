# ReviewWitnessOracle — C1 witness-fixture oracle independence

- Seat: `ReviewWitnessOracle` (reviewer), wave `kake-r46-residual` (round 46).
- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only; no lane mutation).
- Claim under attack: C1 `scripts/redirect_audit.py` + sealed counter
  `.ufo/waves/round-46/c46_matrix.py`; receipts
  `verification/c1-before-7cdbaefd.json`, `verification/c1-after-ee43e66.json`.
- Question: are the 11 C1 witness fixtures genuinely independent of the tool's
  implementation (expectations not reverse-engineered from `decide()`)?
- Tooling: no `lsp` device/server is exposed to this seat, so caller/definition
  checks were done by importing the committed tool in Python and calling
  `_witnesses()`, `_match_source()` and `decide()` directly (stronger than text
  grep for this question); grep was used only for textual provenance. No tools
  installed; no network. Reproducer:
  `/fast/scratch/hyaku/kake-r46-residual/ReviewWitnessOracle/probe.py`
  (read-only; runs from the lane root). Tool sha256
  `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a`,
  fixture index sha256
  `1171c29eeb74751e61b841182c9f45edc3ab692fd3bd97b1f51d2bf74c1e071d`,
  counter sha256 `7335b001f8a6860fef4d268eecdaac8710aa0224006586ea8435ab292b102164`.

## Verdict

**Independence is not demonstrated; in one case it is demonstrably false.**

- The 14 fixture files are byte-for-byte the canonical JSON serialization of
  `redirect_audit.py::_witnesses()` — the tool's own selftest data, landed in
  the same commit by the same owner. There is no fixture `intent` field and no
  external publisher-intent artifact anywhere in the lane.
- None of the 11 flag witnesses has `expect == committed decide()` (that would
  make it uncaught), so the trivial tautology is absent. But 5 of 11 expects
  are byte-equal to a **tool variant's** decision, and W12's expected value is
  **forced by the mutant-kill assertion to equal the mutant's output** — the
  literal "expect is what a variant of the tool happens to decide" case, with
  an expected status the tool's own contract and S135 exclude.
- The frozen C1 predicate ("11/11 witnesses caught, 0 clean false positives,
  3/3 controls rejected") is still met: each witness exits 1 under the
  committed tool. The defect is in the capability row's wording
  **"independently authored request→expectation checks"**
  (`SCORECARD.md:3917`), in the tool docstring's independence claim
  (`scripts/redirect_audit.py:6,27`), and in the *content* of W12/W4/W11 —
  not in the matrix's pass/fail arithmetic.

## Evidence

### E1. Fixtures are the tool's selftest data (14/14)

```
$ python3 -B /fast/scratch/.../probe.py
== A. fixture files vs tool._witnesses() ==
w1_shadowed_redirect         kind=flag  check=c1 file_equals_selftest=True
...
c8_first_match_correct       kind=clean check=c1 file_equals_selftest=True
equal: 14/14

== B. canonical serialization json.dumps(indent=1, sort_keys=True) ==
canonical: 14/14
```

The on-disk files under `.ufo/waves/round-46/fixtures/{witnesses,clean}/` are
exactly `json.dumps(_witnesses()[i][2], indent=1, sort_keys=True) + "\n"`.
The tool and fixtures were added in the same commit `ee43e66367bf`
(`jj diff --stat -r ee43e66367bf` lists `scripts/redirect_audit.py`,
`fixtures/…`, `c46_matrix.py` together), and the round lesson states the same
owner landed them: "the L1 is the integration owner for the round's build
artifacts: both tools, the sealed counter and the fixtures"
(`corpus/lessons/round-46.md:27-28`). The 14 blobs currently equal their
committed `ee43e66367bf` blobs (verified by `git show <rev>:<path> | sha256sum`
per file), so the working-tree oracle used by the after receipt is the
committed one at this tip.

**No manifest states publisher intent.** The union of top-level keys across
all 14 manifests is `checks, defaultStatus, resourcePrecedence, resources,
rules, version`; each check has only `expect, id, path`. An intent/note/why/
publisher/desc field is absent (probe section F). The only intent statements
are comments inside the tool under test (`redirect_audit.py:309-439`). A
third party cannot re-derive any expectation without reading the
implementation — the dependency the attack asks about.

### E2. Expectations vs committed and variant decisions

Probe section C (verbatim rows of interest):

| witness | committed `decide()` | expect | equals a tool variant? |
|---|---|---|---|
| w1_shadowed_redirect | `{"action":"serve"}` | redirect `/new` 301 | `drop_resource_precedence`, inverted precedence |
| w2_first_match_shadow | rewrite `/index.html` | redirect `/modern` 301 | `drop_first_match` |
| w3_redirect_vs_rewrite | rewrite `/docs/` | redirect `/docs/` 301 | no |
| w4_splat_destination | `…/blog.example.com/a/b` | `…/blog.example.com/a/b/c` | no (decide + `/c`) |
| w5_status_mismatch | redirect 302 | redirect 301 | `drop_status_check` |
| w7_placeholders | `/changelog/2024/03` | `/changelog/03/2024` | no (free polarity) |
| w8_unmatched_none | `{"action":"none"}` | `{"action":"serve"}` | no |
| w9_no_resource_precedence | redirect `/` 301 | `{"action":"serve"}` | inverted precedence |
| w10_default_status | redirect 302 | redirect 301 | no |
| w11_malformed_rule | `{"action":"none"}` | redirect `/x` 301 | no |
| w12_malformed_status | `{"action":"malformed_rule",…}` | redirect `/b` **200** | `accept_malformed_rules` |

All three clean cases are byte-equal to committed `decide()`
(`c6/c7/c8 flag=False`), i.e. the clean half of the oracle is definitionally
"what the tool happens to decide".

### E3. W12's expect is pinned to the mutant, and is not a publisher intent

The selftest's kill rule for a paired mutant is: the mutant must **not** flag
its witness, i.e. `decide_mutant(W) == expect(W)`
(`redirect_audit.py:493-515`). For W12 the mutant is
`accept_malformed_rules` (`reject_malformed=False`). Probe section D:

```
expect_status=200 committed_flags=True  mutant_flags=False mutant_decided={"action":"redirect","location":"/b","status":200}
expect_status=301 committed_flags=True  mutant_flags=True  mutant_decided={"action":"redirect","location":"/b","status":200}
```

With a coherent intent (`301`) the mutant would be caught by W12 and could not
be killed, so `expect` was necessarily set to the mutant's output, `200`.
That value is not a publisher intent: the tool's own `REDIRECT_STATUSES` is
`{301,302,303,307,308}` (`redirect_audit.py:47`), and S135 states "Redirects
(301, 302, 303, 307, 308) … 302 is used as the default status code" and places
other statuses under "Rewrites" (`.ufo/waves/round-46/sources/S135.txt:1`).
The audit's user-facing finding prints `expected: {…,"status":200}`, telling
the publisher they intended a 200 redirect — a false expectation. This is the
clearest instance of an expectation reverse-engineered from `decide()`.

### E4. W11's named class is never exercised

Probe section E: the rule's `malformed_reason()` is `wildcard_not_terminal`,
but the request path `/a/1/b` does not match under `_match_source` (which
treats `source[:-1]` as a literal prefix), so `decide()` returns
`{"action":"none"}`, never `malformed_rule`. No ordinary path yields
`wildcard_not_terminal`; the malformed-rule branch fires only for a path that
literally starts with `/a/*/`. The tool run on the fixture reports
`reason: outcome_mismatch`, `decided: {"action":"none"}`, not the malformed
class the fixture name and the comment "malformed rule shape (wildcard
mid-pattern) matched by the request" advertise
(`redirect_audit.py:403`). W11 is the only witness for that class, and its
`expect` (redirect `/x` 301) is the rule's nominal output, not an outcome any
branch can produce.

### E5. W4's expected destination is `decide()` plus an unsourced suffix

Request `/blog/a/b`, source `/blog/*`, destination
`https://blog.example.com/:splat` → documented expansion is
`https://blog.example.com/a/b` (S135 example: `/blog/* https://blog.my.domain/:splat`;
`corpus/knowledge/redirect-rewrite-rules.md` §Render). The expected
`…/a/b/c` has no source in the manifest, in S050/S135, or in any lane intent
record; it is exactly the committed decision with `/c` appended. No mutant or
witness exercises splat expansion, so this expect is never checked against an
alternative splat semantic — it only has to be unequal to `decide()`.

### E6. W7 is a free polarity, not a sourced intent

W7 and clean case C7 use identical rules and path
(`/updates/:month/:year` → `/changelog/:year/:month`, request
`/updates/03/2024`); W7's expect is `/changelog/03/2024` ("placeholder capture
written in the wrong order by the publisher", line 366) and C7's expect is
`/changelog/2024/03` ("correct placeholder reorder must not flag", line 430).
Both are coherent as *different publishers' intents*, but the manifests state
neither; the pair is distinguished only by which expect is declared. The
placeholder semantics are therefore pinned to the implementation's choice, not
validated by an independent oracle. This is a limitation, not the W12-class
defect.

### E7. The counter never validates the expectation, only the exit

`c46_matrix.py:146` defines `caught = code == 1 and verdict == "failed-policy"`
and records only the finding count; `flagged_claim` for controls is the same
shape (`c46_matrix.py:179`). The finding's `expected`/`decided`/`reason` are
never compared to the intended class. Any implementation that flags each
witness for any reason passes. `corpus/QUALITY.md:319` requires the fixture-
oracle granularity to be stated on the record ("the round-27 runner compares
only exit code and the multiset of finding ids, so finer differences are
outside what a passing run shows"); the round-46 C1 claim does not state it.

## Per-witness re-derivation (from the only available intent statements)

"Stated intent" is the `_witnesses()` comment, the only intent text that
exists; "re-derived" uses the manifest fields plus the S050/S135 semantics.

| Witness | Stated intent (only source) | Re-derived expect | Committed expect | Independence |
|---|---|---|---|---|
| w1_shadowed_redirect | publisher intended the redirect; resource presence defeats it | redirect `/new` 301 | same | intent coherent, but value equals `drop_resource_precedence` output |
| w2_first_match_shadow | SPA fallback listed first, legacy redirect never fires | redirect `/modern` 301 | same | intent coherent, value equals `drop_first_match` output |
| w3_redirect_vs_rewrite | expectation says redirect, rule rewrites | redirect `/docs/` 301 | same | derivable from intent + rule destination |
| w4_splat_destination | "wrong destination: splat substituted to the wrong host path" | not derivable (no intended URL stated) | `…/a/b/c` | **decision-perturbed, unsourced** |
| w5_status_mismatch | rule says 302, expectation 301 | redirect 301 | same | intent coherent, value equals `drop_status_check` output |
| w7_placeholders | "placeholder capture written in the wrong order by the publisher" | not derivable ("wrong" defined only by the expect; C7 asserts the complement) | `/changelog/03/2024` | **free polarity, unsourced** |
| w8_unmatched_none | publisher expected a serve | `{"action":"serve"}` | same | derivable (bare assertion) |
| w9_no_resource_precedence | publisher expected the asset served, redirect fires | `{"action":"serve"}` | same | intent coherent, value equals inverted-precedence output |
| w10_default_status | rule omits status, default 302, expectation 301 | redirect 301 | same | coherent; no variant equals it |
| w11_malformed_rule | malformed wildcard "matched by the request" | no redirect derivable; class unreachable | redirect `/x` 301 | **nominal output, class not exercised** |
| w12_malformed_status | malformed status (200 is not a redirect status) | no valid redirect intent exists | redirect `/b` **200** | **reverse-engineered from the accept-malformed branch; domain-invalid** |

## Findings (by severity)

### F1 — High — the "independently authored" claim is unsupported; the fixtures are the tool's own selftest data

`SCORECARD.md:3917` advertises "independently authored request→expectation
checks"; `redirect_audit.py:6` says "independently authored expectation" and
`:27-30` says the expectations are authored independently of the rules "which
is what keeps the audit from being tautological". Evidence E1 shows the 14
files are canonical dumps of `_witnesses()`, same commit, same owner, with no
intent field and no external intent artifact. Whatever the authoring
direction, the fixture set and the decision function are one artifact family;
the strongest defensible statement is "expectations authored alongside the
rules", not "independently authored". This does not falsify the frozen
predicate, but the capability row's wording overstates the evidence.

### F2 — High — W12's expectation is reverse-engineered and domain-invalid

Evidence E3. The expected status 200 is forced to equal the
`accept_malformed_rules` mutant output by the kill rule; with a valid 301
intent the mutant would be caught. The audit's user-facing `expected` object
therefore reports an intent the platform does not support (S135: 301/302/303/
307/308 are redirect statuses; 200 is a rewrite/proxy status). The witness
still flags under the committed tool, so the matrix stays green and it still
kills the accept-malformed mutant (that mutant is uncaught). The defect is the
oracle value: the audit's report tells a publisher they intended status 200,
and the fixture's expected object endorses the invalid outcome rather than a
valid redirect intent.

### F3 — Medium — W4's expected destination is `decide()` + `/c`

Evidence E5. No manifest field, S050/S135 statement, or intent record yields
`https://blog.example.com/a/b/c` for request `/blog/a/b`; the documented
expansion is `…/a/b`. The expect is a hand-perturbed decision. No witness or
mutant tests splat expansion against an alternative semantic, so the
expectation's only role is inequality.

### F4 — Medium — W11 does not exercise the malformed-rule class it names

Evidence E4. `wildcard_not_terminal` is decided only for a request path that
literally contains the non-terminal `*`; ordinary paths get `none` with
`reason: outcome_mismatch`. The only witness named `malformed_rule` for this
class never reaches the `malformed_rule` branch, and its expect is the rule's
nominal output rather than a reachable outcome.

### F5 — Medium — oracle-mirroring pattern

5/11 flag expects are byte-equal to a tool variant's decision (W1, W2, W5, W9,
W12); 3/3 clean expects are byte-equal to committed `decide()`. For the four
mutant-paired witnesses (W1, W2, W5, W12) the equality is *required* by the
selftest's kill rule, so their expects are pinned to the implementation family
by design. For W1/W2/W5 the pinned output is at least a coherent publisher
intent; for W12 it is not (F2). This is the signature of differential probes,
not independently authored oracles. Cite `redirect_audit.py:309-314,493-515`.

### F6 — Medium — the counter scores exit/verdict only; fixture-oracle granularity is unstated

Evidence E7. `caught` never inspects `expected`, `decided`, or `reason`.
`corpus/QUALITY.md:319` requires the granularity be stated on the record; the
C1 claim doesn't. A tool that flags each witness for the wrong reason passes.

### F7 — Low — W7's intent is a free polarity (paired with C7)

Evidence E6. Coherent as two different publishers' intents, but neither is
recorded; the fixture pair pins placeholder expansion to the implementation's
choice. No predicate failure.

## What holds

- The committed tool flags each of the 11 witnesses individually (exit 1,
  verdict `failed-policy`, one finding each) — re-run directly; matches the
  after receipt rows (`witnesses.caught = 11`).
- The three clean cases exit 0 (no false positives), and the before receipt
  correctly shows the tool absent with all witnesses uncaught.
- The receipt's tool sha256 matches the worktree tool
  (`1e1dff18…`), and the fixture/counter blobs match the measured commit.
- The controls' rejection logic is unaffected by this finding.

## Residual risk / verification gaps

- **No external intent source exists.** Grepping the lane for the distinctive
  expected strings (`blog.example.com`, `changelog/03/2024`,
  `changelog/2024/03`) returns only `scripts/redirect_audit.py`. The review
  therefore cannot establish *any* publisher intent independently of the tool;
  it can only test coherence with S050/S135.
- **The oracle is not digest-pinned in the receipt.** `c46_matrix.py:119-120`
  reads fixtures from the working tree, outside the measured revision, and the
  receipt contains no fixture sha256. The blobs currently match
  `ee43e66367bf`, so the after receipt is valid at this tip, but byte-level
  re-derivation depends on an unpinned tree.
- **LSP unavailable.** No `lsp` device/server answered in this seat; semantic
  checks used direct Python import introspection, textual provenance used grep.
- I did not run `c46_matrix.py` end-to-end (not needed for this question; the
  matrix-blindness attack is another seat's scope). Each witness was run
  through the tool directly instead.
- W4/W7/W11 could be defended as legitimate publisher intents *if* an external
  intent record existed; none does. The findings stand on the absence of that
  record plus the exact decision-perturbation/variant equalities above.

## Recommendation (no edits made)

1. Add an `intent` (or `why`) field to each manifest stating the publisher
   failure narrative and its source, authored before the tool (or in a
   separate commit), so the expectation is checkable without reading
   `decide()`. Move the `_witnesses()` intent comments out of the tool file or
   duplicate them into the manifests.
2. Repair W12: use a coherent expected status (301) and redesign the
   accept-malformed mutant pairing so the kill does not require the invalid
   value (e.g. pair it with a witness whose expected outcome is a valid
   redirect and whose malformed status is a separate witness class).
3. Either source W4's expected URL from a stated intent, or change the witness
   to a splat semantic with a derivable destination; add a splat mutant.
4. Add a witness that actually reaches `wildcard_not_terminal` (or drop the
   class claim from W11 and the contract); W11's name/comment currently
   overclaim.
5. State the fixture-oracle granularity in the C1 row (exit + verdict +
   finding count; `expected`/`decided`/`reason` not compared), per
   `corpus/QUALITY.md:319`.
6. Soften the capability-row wording from "independently authored" to what the
   evidence supports until items 1-3 land.
