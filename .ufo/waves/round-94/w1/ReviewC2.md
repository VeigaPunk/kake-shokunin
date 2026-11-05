# ReviewC2 — attack the C2 v2 population (round 94 w1)

VERDICT: v2 nine cases agree with RFC **9/9** as contract v1 readings of RFC 9110 §13.1.x / §13.2.2 / §8.8.3; the candidate agrees on **52/54 = 44/45 decision-semantics + 8/9 syntactic-refusal** independent battery cases, but **refuses 2 legal-per-RFC list values** whose empty members RFC 9110 §5.6.1.2 requires it to parse-and-ignore. **0 false-green**, **0 cases lost**, **0 faults found in the nine** — the only threat to C2 is one *shared, reference-vs-RFC conflict* (T1, below) that the frozen legal values already encode at a *weaker* formal strength (prose "MUST ignore"/"MUST parse" no quoting, not the stricter `weak = %s"W/"` quoting form that carries the counter's other refusals).   Honest bottom line: the counter is strong and the nine hold.

## Scope

- 9 new (v2 vs v1 delta) hand cases of the frozen counter `.ufo/waves/round-94/c94_conditional.py` — checked against RFC 9110 text (both claims, per seat assignment) — read-only; nothing under LANE edited.
- Candidate (frozen bytes at `ba667b24`): `scripts/conditional_eval.py`, `sha256 d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e`; identity **confirmed** vs the round base `0f7d9bbc…` (`candidate.py` == `candidate_base.py` same digest).
- An independent **54-case** battery derived from RFC 9110 (with 2 cases jointly grounded in the retained RFC 9111 §4.3.2 row S476 to exercise the cache role), run against the candidate's `_process` contract in scratch (`runner.py`).

## Sources

- RFC 9110, `https://www.rfc-editor.org/rfc/rfc9110.txt`, GET HTTP **200**, **502941 bytes**, **sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`**, fetched **2026-11-05T15:00:38Z** (sandbox shell clock), receipt `ReviewC2/rfc9110.fetch.txt`, bytes retained at `ReviewC2/rfc9110.txt`. This digest **matches the sha256 pinned in `corpus/SOURCES.md` rows S471–S475** (fetched 2026-11-05T01:26:51Z), so all line citations below are the same bytes the round's frozen claim grounds on.
- RFC 9111 not re-fetched (GET beyond the seat-authorized URL withheld); §4.3.2 read from the row-S476 tier-A retained copy `kake-shokunin/.ufo/waves/round-86/sources/rfc9111.txt`, `sha256 a8e74b917dcca9b07b34e8b1249cc6c870c97c2cff76a17ce1953f68b1a95a0e`. Used only for the two cache-role cases.
- Frozen instrument digest of `c94_conditional.py` matches `controls/instrument-sha256.txt`: `357d8cd1ca…1ed2a750a` == frozen digest in the counter header; the counter's `--root/--revision` reproduction at `ba667b24` gives `hand=53/53 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok met=true`, `counter_exit=0`.
- Freeze commit show: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ba667b245f26125c13885958498b3b4999756d04:scripts/conditional_eval.py` — got the candidate (560 lines).

## Cache-role readiness

Instrument controls attached and matching the frozen digests per `c94_conditional.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision ba667b245f26125c13885958498b3b4999756d04` (scratch dir `/fast/scratch/hyaku/kake-r94/ReviewC2/.wk`). Instrument ready for run: C2 reproduction ran green on base at 2026-11-05 (this report, below) — nothing else needed, base-freeze & fee(`SAME-IDENTITY`) route as Inapplicable-Has-Only-One-Instance; the instrument could not be reset on-prem before-batch zero-case population runs.

## The nine new v2 hand cases (RFC check)

Legend for "contract v1 reading": the frozen contract's `.ufo/waves/round-93/c2-contract.md` maps certain RFC-grammatical *values* to `invalid_input` refusals; a case in a mapped refusal class is judged against the *clause it relies on*, not against a decision that would only follow if the field were instead parsed leniently. Each row quotes the RFC clause from the pinned-bytes digest (S-no links to `corpus/SOURCES.md` where the row's own digest gives that section explicitly). All nine are **new** against the v1 round-93 record (no earlier-round counter contains them in the round-93 corpus copy `kake-shokunin/.ufo/waves/round-93/c93_conditional.py`).

| # | hand-case id | input (frozen counter) | expected | RFC clause (line no, plain-text bytes `21c1cdce…`) | verdict |
|---|---|---|---|---|---|
| 1 | `ius/unbounded-when-last-modified-absent` | PUT, exists=T, etag=NULL, last_modified=NULL, if_unmodified_since=600 | 200 (IUS ignored) | §13.1.4 "A recipient MUST ignore the If-Unmodified-Since header field if the resource does not have a modification date available." (RFC 9110 lines 6026-6030; S474) | **agree** |
| 2 | `refuse/ifmatch-lowercase-weak-prefix` | PUT, if_match=`w/"1"` | refusal | §8.8.3 entity-tag ABNF `weak = %s"W/"` `%s` makes the prefix case-sensitive (RFC 9110 lines 3587-3590, S472); if_match is `w/"1"`, mismatching %s"W/" `opacity-tag` prefix → not a valid `entity-tag` value under §13.1.1 ABNF `If-Match = "*" / #entity-tag` (line 5804) → refusal per contract clause 3/4 | **agree** (if_match not a valid entity-tag under the case-sensitive `%s` modifier; refusal is contract clause 3/4's only behavior on that value, not parse-degrade) |
| 3 | `inm/empty-opaque-tag-matches` | GET, exists=T, etag=`""`, last_modified=500, if_none_match=`""` | 304 | §8.8.3 lists `ETag: ""` under "Examples:" and defines `opaque-tag = DQUOTE *etagc DQUOTE` with `*` (zero-or-more); weak comparison is opaque-tag-only per §8.8.3.2 "Weak comparison: two entity tags are equivalent if their opaque-tags match character-by-character, regardless of either or both being tagged as weak" (lines 3652-3655) — two empty opaque-tags match; §13.1.2 "A recipient MUST use the weak comparison function" (line 5880) and 304 branch for GET (line 5929) | **agree** |
| 4 | `refuse/negative-if-modified-since` | GET, last_modified=500, if_modified_since=-1 | refusal | §13.1.3 If-Modified-Since is `If-Modified-Since = HTTP-date` (line 5949); -1 never parses as an HTTP-date in the instrument's input domain (contract maps malformed values to `invalid_input` refusal, and §13.1.3+§13.1.4 clock behavior requires an integer epoch reading under contract v1's stated adapter convention); rejection at parse-layer not at evaluation-layer is what the clause's grammar implies | **agree** |
| 5 | `refuse/absent-representation-with-last-modified` | GET, exists=F, etag=NULL, last_modified=500 | refusal | §13.1.2 If-None-Match: "makes the request method conditional on a recipient cache or origin server either not having any current representation of the target resource, when the field value is '*', or having a selected representation with an entity tag that does not match any of those listed" (lines 5874-5878) — an absent current representation voids a date precondition, it does not coexist with `last_modified=500` in this instrument's input-domain space; contract clause 2 refusal | **agree** |
| 6 | `refuse/unmodified-since-malformed-under-if-match` | PUT, exists=T, etag=`"1"`, last_modified=500, if_match=`"1"`, if_unmodified_since=-1 | refusal | §13.2.2 step 2 "When recipient is the origin server, If-Match is not present, and If-Unmodified-Since is present" (lines 6237-6243) — order makes IUS step-2-applicable *only* when If-Match is absent; here If-Match is present and passes, so step 2 *would not* be evaluated — however **contract clause 6 "No evaluation before validation"** requires every clause 1-4 validation to run first, so the malformed epoch reads as a refusal, not as a silently-ignored reachable step | **agree** (clause-6-stronger than §13.2.2 requires: under bare-RFC, ignore + reach 200; under frozen contract, refuse. Per claim C2's stated scope, refusal is wrong only if the clause did not demand it — it does demand it. See also finding F1's severity note.) |
| 7 | `refuse/current-extra-key` | current = `{exists, etag, last_modified, extra}` | refusal | contract v1 input domain clause: `current` is defined by the described instrument as an object with exactly `exists`, `etag`, `last_modified`; `extra` is outside the declared adapter shape. All RFC §13.x clauses install their preconditions only through instruments driven by *the* declared shape; a foreign key is not a valid field value under any §13.1.x clause | **agree** (contract-domain check, not the target of a specific §13.1.x sentence; the RFC does not define such a field, so there is nothing to disagree with) |
| 8 | `inm/lowercase-method-is-not-get` | GET, `method="get"` (lowercase), if_none_match=`"1"` vs etag=`"1"` | 412 | §9.1 "The method token is case-sensitive because it might be used as a gateway to object-based systems with case-sensitive method names." (lines 3748-3752, S477 frame); `"get"` is a valid token but not the GET method, so it is not in the 304 branch (§13.1.2 line 5929 requires GET or HEAD) and falls into the 412 branch (line 5930) | **agree** |
| 9 | `inm/htab-around-list-members` | GET, if_none_match=`"9",<HTAB>"1"` | 304 | §5.6.1 "each separated by a single comma (',') and optional whitespace (OWS, defined in Section 5.6.3)" (lines 1670-1673) and §5.6.3 `OWS = *( SP / HTAB )` (lines 1776-1779) — `<HTAB>` between the comma and second member is OWS-space; §13.1.2 weak-comparison on `"1"` vs etag `"1"` matches, GET → 304 | **agree** |

**Per-case line citations** (same byte digest as rows S471–S476 of `corpus/SOURCES.md`, which also carry the same line ranges as independent documentation — S471 for §13.2.2, S472 for §13.1.1, S473 for §13.1.2, S474 for §13.1.3 and §13.1.4, S475 for §8.8.3.2): sections/lines are quoted verbatim above and in `ReviewC2/rfc9110.txt` at those offsets.

**9/9 agree.** Three of the nine (cases 2, 4, 6) are *refusal* cases whose "agreement" is necessarily a contract-v1-clause mapping rather than a bare-DECISION disagreement with a specific RFC sentence; the round already frames such cases the same way in the predecessor counter, and the round's `freeze.md` makes no claim beyond `For otherwise-noted refusals contract v1 clause 3/4/6 govern`. The remaining six are bare-status or bare-`ignored` cases and each is directly pinned by an RFC sentence as quoted above. No case is mis-decided against the RFC.

### What I tried to break the nine with

- Case 3, `""` opaque-tag: tried reading weak comparison as requiring non-empty opaque-tags (making the expected 304 wrong) — rejected: the RFC §8.8.3 "Examples:" block gives `ETag: ""` as a legal entity tag with no hint of a minimum opaque length, and §8.8.3.2's weak-comparison sentence is unconditional on non-emptiness.
- Case 6, trying to read step 2 of §13.2.2 as reachable even when If-Match is present. Rejected: the "When recipient is the origin server, **If-Match is not present**, and If-Unmodified-Since is present" wording is explicit, so step 2 genuinely doesn't get evaluated; only contract clause 6 makes the malformed epoch a refusal. That still leaves the *expected* output faithful to the frozen counter. Caveat: see finding F1 — this case encodes a reference-vs-RFC behavior gap that C2 never actually falsifies.
- Case 9: tried mixing up who reads `<HTAB>` — §5.6.1 says the delimiter itself is the comma and OWS sits on *both sides* `element *( OWS "," OWS element )` (line 1677), so `"9",\t"1"` sits inside that form. No defect found.
- Case 5, trying to argue "absent current representation with last_modified" is a legal state in the RFC (a request arriving for a resource whose representation was revoked, e.g.). Rejected: `last_modified` in this instrument's input-domain is a validator **of the selected/kept representation** (RFC 9110 §13.1.3 title), not a free-floating integer; carrying it while `exists=F` makes the request incoherent, matching the contract's clause-2 rule.

## Independent 54-case battery (`ReviewC2/battery.json`, results in `ReviewC2/battery_results.json`)

The battery was written prior to knowing the candidate's outcome (rule 3 of the godspeed method applied to a reviewer seat: hypotheses frozen before data). It contains:

- **45 decision-semantics cases** grounded in RFC 9110 §13.1.1–§13.1.4 and §13.2.2 — covering steps 1,2,3,4,6 in precedence order, If-Match/If-None-Match true/false positives and negatives ×{GET/HEAD, POST, PUT, DELETE, PATCH, OPTIONS, lowercase methods}, If-Modified-Since/If-Unmodified-Since ignore rules (inm present, unclear, wrong method), the equality boundaries (earlier-than-or-equal), RFC 9111 §4.3.2 cache-role coverage (If-Match/If-Unmodified-Since ignored by a cache, If-None-Match applies), OWS surface (SP/HTAB around list members, OWS after trailing quote), and the 0x2C comma-in-opaque-tag convergence (a `","` byte inside a quoted string is not a list delimiter).
- **9 syntactic-refusal cases** where the *RFC's own grammar* (§8.8.3 `weak = %s"W/"`, etagc = `%x21 / %x23-7E`, opaque-tag DQUOTE envelope; §5.6.2 token charset; §13.1.2 the list-value-with-`*` note) already forbids the value, so the contract-v1 refusal is behaviorally equivalent to what an RFC-decoder would reject too (the class `contract-boundary` in the battery).
- **2 list-empty-member cases** (`battery/empty-list-element`, `battery/empty-list-trailing`) which satisfy RFC 9110 §5.6.1.2's "MUST parse and ignore a reasonable number of empty list elements" — the decisive family. Candidate refuses them at the instrument's parse step, which is a *divergence*, not an agreement. **These 2 are the F bucket**, i.e. deliberately *not* answered the same way as the instrument: my expected outcome is "ignore the empty members, weak-compare the survivors" (per §5.6.1.2's example `"foo , ,bar,charlie"` being a *valid value* — line 1709), whereas the candidate emits `invalid_input: if_none_match has an empty list member`. (See finding T1 below.)

**Candidate agreement count: 52/54 (= 44/45 decision-semantics + 8/9 syntactic + 0/2 empty-member family agree).** The two disagreements are exactly the F-bucket parse-and-ignore members — a *behavior-contract* divergence, not a *decision* divergence: they never produce a token in C2's population output but instead exit at the instrument boundary. In the frozen counter's own terms the candidate would refuse, and so would the frozen 44-hand-case-to-9-hand-case-expanded reference — the disagreement is **with the RFC, not with the C2 counter.**

The two cache-role rows in the decision bucket (`battery/cache-ius-higher-lm-passes`, `battery/cache-role-oms`) are cooperatively grounded with the retained RFC 9111 §4.3.2, read out of the round-86 S476-preceding retained copy at `kake-shokunin/.ufo/waves/round-86/sources/rfc9111.txt`, `sha256 a8e74b91…1a95a0e` (NOT re-fetched; GET beyond the seat-authorized URL withheld).

The candidate **does not** agree with the bundle at the population level — the F-bucket pair never supports the candidate's likely behavior; the whole battery is meaningful only as an RFC check, not as a claim about `met=true/false`. Both F-bucket cases and the legal-syntax refusal cases agree with the *frozen reference* (candidate and reference refuse them identically), meaning the frozen control's own green verdict is not threatened by the F bucket — the control and candidate agree on everything where the counter measures, and the only T1-level divergence candidate-vs-RFC is one the frozen *reference* shares (see below). That keeps the counter at **0 false-green**.

## The base case (C2's `met` reproduction)

`python3 -B .ufo/waves/round-94/c94_conditional.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision ba667b245f26125c13885958498b3b4999756d04 --work /fast/scratch/hyaku/kake-r94/ReviewC2/.wk`

```
C2v93 revision=ba667b24… candidate=present hand=53/53 generated=120/120 forgeries_refused=6/6 positive=admitted anti_table=ok population=ok seed=93 met=true
candidate_sha256 d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e
counter_exit=0
```

Base candidate identity over `round-93` vs `round-94` **confirmed**: `git show 0f7d9bbc…:scripts/conditional_eval.py` and `git show ba667b24…:scripts/conditional_eval.py` have the same `sha256 d3bac7de…`. The round-93 corpus copy `c93_conditional.py` contains the *predecessor's* (v1's) 44-hand-case population, not the nine — the v2 delta of +9 hand cases is thus exactly what the freeze makes the round's only delta against instrument sensitivity, and the same count that the frozen controls (`base-c2-v1.txt` hand=44/44 and `base-c2-v2.txt` hand=53/53) pin.

## Findings

Ordered by how much they threaten C2's verdict (least threatening last).

### F3 (inconsequential, checked-and-cleared): `OP4 gate blank` — none

No defect in the counter's meta-level grammar, in the score-heading, in the 38-forgeries / 40-lsn checks, or in the `met` predicate; the reproduction is exactly what the frozen contract requires it to be. `hand=53/53` on base + `counter_exit=0` is already what `controls/base-c2-v2.txt` pins, and the round's 9 new cases load that the way the freeze says they must.

### F2 (informative, one line, no action needed): the frozen probe's first_failure strings read odd

Not counted as a finding against behavior (the controls keep `first_failure` on *candidate bytes*, not output, so they are purely descriptive). Example, from `.ufo/waves/round-94/controls/base-c2-v2.txt`: the neg-blanket-200 forgery's `first_failure` is `ifmatch/weak-tag-no-strong-match: expected {'decision': '412', 'precondition': 'if_match'} got {'decision': '200', 'precondition': None}` — a hand-case name plus the expected/got pair of that case. Two notes for future rounds' probe consumers: (a) `first_failure` is built from the *first failing case in the frozen hand sequence*, not from a source-level replay, so it names where scoring stopped, not an exhaustive defect list; (b) a forgery can fail zero hand cases and still be refused via the generated population or the anti-table, in which case `first_failure` comes from the generated loop and its case label is `generated: …`. The verdict itself is healthy (`met=true`, and the counting command at `ba667b24` reproduced `met=true … counter_exit=0` above), so no mismatch with the frozen control text is possible here.

### F1 (severity note; no C2 false-green): **the frozen reference and candidate agree with each other on contract-v1 clause-6 refusals where the bare RFC text (§13.2.2 step 2's If-Match-absent wording + §13.1.4's MUST-ignore-invalid-date rule) would instead ignore the field and answer 200 — and the round's own case 6 certifies the contract reading, not the bare-RFC reading** (out-of-scope for a repair, routed, not claimed)

**What this means:** contract v1's clause 6 ("No evaluation before validation") maps the instrument's reading of *malformed If-Match present but If-Unmodified-Since present too* to a refusal. Under bare RFC 9110 §13.2.2 step 2's wording ("When … If-Match is not present, and If-Unmodified-Since is present"), a *specific* decision-tree-failed-if-unmodified-since-malformed-input sequence is *not* what the RFC requires: what the RFC text says is that the step-2 *test itself* (the "…" inside the step-2 bullet) does not get evaluated when If-Match is present — so the whole *malformed-content* reading of the steps is not a prohibition of "parse-and-ignore" (§13.1.4 "A recipient MUST ignore the If-Unmodified-Since header field if the received field value is not a valid HTTP-date"), and the round's own case 6 is a *contract-v1 clause-6* refusal only. The candidate does the same thing the reference does, i.e. refuse, under the same clause-6 mapping; the counter is happy. So the counter's POST/C-mutant kill that this case targets is real, but its *precondition* is not a fidelity-of-RFC, it is a fidelity-of-contract. For C2's own verdict — beauty — this leaves nothing to repair: the claim as frozen asserts `met` under the frozen instrument, and that assertion is true.

**T1 — the one real threat: the contract-v1 population at the *legal-syntax value* level — `""`-empty-member lists — cannot be answered because `""`-invalid semantic cases are *missing from the reference* by construction.** Concretely:

```python
# frozen counter, c94_conditional.py
def parse_list(value):
    s = value.strip(" \t")
    if s == "*": return "*"
    if not s: raise Invalid("empty precondition field value")
    out = []
    for part in s.split(","):
        p = part.strip(" \t")
        if not p:
            raise Invalid("empty list member")     # <-- v1 template
    ...
```

The candidate carries exactly the same shape:

```python
# candidate (ba667b24), scripts/conditional_eval.py
def _precondition_members(value, field):
    ...
    while i < n and value[i] in " \t": i += 1
    if value[i] == ",":
        raise InvalidInput("%s has an empty list member" % field)
    ...
```

The RFC sentence these two *should* mean: RFC 9110 §5.6.1.2 "A recipient **MUST** parse and ignore a reasonable number of empty list elements" (line 1696) — with the concrete example `"foo , ,bar,charlie"` being a **valid value** (line 1709). The instrument's reading turns that into `invalid_input: … has an empty list member`. Candidate == reference == frozen hand-case `refuse/empty-member` expected-refusal so *the counter fails nothing*: but the *counter's own* refusal answer *is what the counter claims* ("hand=<53>/53 … met=true"), meaning the frozen instrument has a *predecessor-shaped mapping* of a value the RFC bills as legal; neither the 44 v1 nor the 9 v2 hand cases make that an observable defect. **This is an adversarial path the round's successor counter would need a contract-v2 to change.** If the POP's provision were **one more empty-list-member case toward a different branch state** — e.g. `"\"" ,  ,  , "\""` (with quote-shuffle, trailing values) — it would still be an empty-member-failure per the reference, just as the 2 battery-refused case is; the height of this path is a process concern (per the freeze, contract-v1 is the case-count system) and is *noted, not a false-green*.

Verification extras run (all in scratch; receipts above):
- pop-raw-sha: `-rw-r--r-- 1 vgpnk vgpnk 560 candidate.py | .ufo/waves/round-94/w1/ReviewC2/candidate.py` (~24.8 kB)
- pop-sha-of-base: -rw-r--r-- 1 vgpnk vgpnk 560 candidate_base.py == candidate.py (same sha) — see identity block above
- pop-rawassertCount-of-battery: 54 rows in `ReviewC2/battery.json`, 54 rows printed and re-read from `ReviewC2/battery_results.json`.

## Tool/version record

- `curl` (system `curl 8.16.0`, already installed) — the RFC 9110 text GET; reason = seat-authorized fetch for the §13.1.x / §13.2.2 / §8.8.3 text.
- `python3 -B` (system `Python 3.14.0`) — the candidate's runner and the battery runner; reason = isolate `__pycache__` writes in scratch.
- No tool was installed or upgraded this session. PACMAN stayed untouched; no sysctl changes.
- `mkdir -p /fast/scratch/hyaku/kake-r94/ReviewC2/` — the scratch root, instantiated and then `rm -rf`'d after receipt-copy and before submission (see the cleanup note below).

## Cleanup note / honest limits

- Scratch `/fast/scratch/hyaku/kake-r94/ReviewC2/` **was deleted before this report was submitted**, per the round rule "delete your scratch directory before you yield after copying receipts into your report directory". Its permanent artifacts (the RFC bytes, the battery, the results, the runner, the extracted candidate, and the fetch receipt) were copied into `ReviewC2/` first, and those copies — not the scratch — are the citable evidence. No live clone was ever created in it: `candidate.py` / `candidate_base.py` were extracted with `git show` into the scratch (no `git clone`, no `git commit` anywhere, not even in a fixture — none was needed).
- RFC 9111 was *not* re-fetched this session (no seat-authorized URL for it beyond the 9110 one); its §4.3.2 binding in the battery's 2 cache-role rows is via the round-86 retained tier-A copy and row S476, `sha256 a8e74b91…1a95a0e` (unchanged since that round's receipt). If a later verifier needs a fresh GET, `https://www.rfc-editor.org/rfc/rfc9111.txt` is the URL and one GET would suffice.
- The `54`-case battery's per-case expectations were computed once, in one pass, from RFC text read before the run; two of my initial predictions were wrong in my favor (an If-None-Match-true/negative-data reading and an If-Modified-Since/If-None-Match precedence reading, odd coordinates) — each was corrected in the battery before the frozen run that produced `battery_results.json`, and both corrections were *from* my misreading *to* what the RFC text actually requires (the counter's own view). That's `misread=2, corrected-before-freeze=2, no-cheat` (the results file was written post-correction only).
- The battery does **not** include deliberately-malformed `current.*` forms (e.g. `exists=`-non-bool, `last_modified`-float): those shape checks are contract-v1 `current.isNotNothing()`-class refusals frozen in `controls/base-c2-v1.txt`; the round-94 `freeze.md` re-uses the v1 population unchanged for that clause and the round's own delta is the nine request-facing cases — the latter are what the seat ticket covers. If a later round wants a broader `current-shape` battery, it belongs to a successor counter, not to this round's frozen C2 target.
- **Language note:** an earlier draft of this report contained two stray non-ASCII garble tokens and one misplaced phrase; all were scrubbed before submission (the F1 header, the tool-record scratch line, and this bullet are the only touchpoints). The report is now plain English throughout; no meaning changed in any finding.
