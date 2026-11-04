# ExecCases — round-88 w1 (C2 independent expectation set + adversarial batch)

Seat: `ExecCases`, leaf executor, lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Nothing outside `.ufo/waves/round-88/w1/ExecCases/` and `w1/ExecCases.md` was written.
No production byte, no commit, no push, no git/jj mutation, no delegation.
No tool was installed (nothing was needed); no network request was made.

## Result in one block

| item | value |
|---|---|
| frozen expectations derived | **20/20**, and 20/20 agree with the frozen labels (`receipts/expectations-vs-frozen.txt`, exit 0) |
| fresh adversarial inputs | **18** (`extra-cases.json`), none repeats a frozen tuple (`receipts/freshness.txt`: `{"collisions": [], "extras": 18, "frozen": 20}`, exit 0) |
| candidate `w1/ExecReader/vary_match.py` sha256 `fdceef47…` | frozen **20/20**, extras **15/18** (`receipts/ExecReader-extras.txt`, `ExecReader-frozen.txt`) |
| official C2 counter on that candidate | `frozen=20 random=200 met=true`, exit 0, `random_sha256=52714a5f…` (`receipts/official-counter-tool-runs.txt`) |
| counter reference vs my expectations | frozen 20/20; extras 15/18 — the same three misses as the candidate |
| frozen case I believe is *wrong* against the declared profile | none; four cases (14, 15, 19, 20) rest on adapter rules, not on RFC text — see F2/F5 |

The 18 → 15 gap is not a candidate bug: all three misses (X04, X07, X15) are inputs whose
verdict `contract.md` does not define. The candidate and the counter's reference give the same
answer on every one of the 38 inputs I scored.

## Axes (named before the work)

1. **Spec fidelity** — does each of the 20 frozen labels follow from a cited sentence, or from an
   undeclared adapter convention? (Outcome: 16 from RFC text + profile, 4 from adapter convention.)
2. **Discriminating freshness** — do fresh inputs expose cases the 20 do not reach?
   (Outcome: 3/18 expose an undeclared rule; 2 more expose a spec-vs-profile divergence.)
3. **Byte-freeze integrity** — are the bytes I score the bytes the contract froze?
   (Outcome: they moved under me — F1.)

## Read order and independence

`contract.md` → `c88_vary.py` (docstring + profile + reference) → `vary-cases.json` →
`c88_defect_queue.py` → wrote `expectations.json` → wrote `extra-cases.json` → only then scored anything.

The candidate did not exist while the expectations were written:

```
expectations.json          mtime=2026-11-04 15:56:51 -0300
extra-cases.json           mtime=2026-11-04 15:57:36 -0300
w1/ExecReader/vary_match.py mtime=2026-11-04 15:59:20 -0300   (appeared 2.5 min later)
```

(`receipts/independence.txt`.) I did read the counter's `reference()` block before writing the
table — it is the counter, not the candidate — and the table was derived from the written profile
plus the RFC sentences, not from that code. Where my reading and the reference differ, it is
reported below rather than smoothed over.

## Table 1 — the 20 frozen cases

`expected` is what the round's declared contract requires; `spec` is RFC 9111 §4.1 read strictly,
only where it differs.

| id | expected | frozen | agree | deciding text / note |
|---|---|---|---|---|
| 1 | match | match | yes | identical trimmed value; no transformation needed |
| 2 | match | match | yes | names are case-insensitive (RFC 9110 §5.1), values equal |
| 3 | mismatch | mismatch | yes | profile folds no value case. `spec`: match (content codings are case-insensitive, §4.1 bullet 3 is *permitted*) |
| 4 | match | match | yes | absent from both — §4.1 absence sentence |
| 5 | mismatch | mismatch | yes | absent on stored side only |
| 6 | mismatch | mismatch | yes | absent on presented side only |
| 7 | mismatch | mismatch | yes | `"*" always fails to match` |
| 8 | mismatch | mismatch | yes | a `*` member dominates an otherwise matching list |
| 9 | match | match | yes | adding/removing whitespace where syntax allows |
| 10 | mismatch | mismatch | yes | profile does not reorder. `spec`: ambiguous, field-specific rule could match |
| 11 | match | match | yes | every nominated field matches |
| 12 | mismatch | mismatch | yes | one nominated field differs |
| 13 | match | match | yes | case-variant duplicate member adds no conjunct (§5.1 + list-of-names) |
| 14 | invalid_input | exit 1 | yes | **adapter**, not RFC: see F5. `spec`: match (zero nominated fields ⇒ vacuous universal) |
| 15 | invalid_input | exit 1 | yes | **adapter**: `accept encoding` is one list member, not a token; `mismatch` equally defensible |
| 16 | match | match | yes | two field lines combine in order with `, ` (§5.2) |
| 17 | mismatch | mismatch | yes | combination is ordered; sides differ |
| 18 | mismatch | mismatch | yes | profile folds no internal whitespace. `spec`: match (OWS around `;` is in `weight = OWS ";" OWS "q=" qvalue`) |
| 19 | invalid_input | exit 1 | yes | **adapter domain**: field value is the JSON number 5 |
| 20 | invalid_input | exit 1 | yes | **adapter domain**: `vary` is the JSON number 5 |

18 of 20 are pure §4.1/§5.1/§5.2; cases 3, 10, 18 are the declared conservative profile exercised
deliberately (a `mismatch` there is conformant because §4.1 only says the cache **MAY** reuse a
matching response); cases 14, 15, 19, 20 are adapter conventions.

## Table 2 — 18 fresh inputs (not in the frozen set)

`expected` = declared contract; `got` = both the ExecReader candidate and the counter reference
(identical on all 18); `spec` recorded only where it differs.

| id | axis | expected | got | agree | basis |
|---|---|---|---|---|---|
| X01 | repeated identical members | match | match | yes | a repeated name adds no conjunct |
| X02 | Vary value is only OWS | invalid_input | invalid_input | yes | adapter; **spec: match** (zero members, §5.6.1.1 ignore empty elements) |
| X03 | `*, accept-encoding`, star first | mismatch | mismatch | yes | `*` fails wherever it sits |
| X04 | request key with trailing space | mismatch | invalid_input | **no** | nominated field is absent on that side (absence sentence); refusal is defensible but undeclared — F2 |
| X05 | member with `_` | match | match | yes | `_` is tchar, so it is a valid field-name |
| X06 | JSON array of one value | match | match | yes | one line combines to itself |
| X07 | empty array as value | mismatch | invalid_input | **no** | zero field lines ⇒ field absent; reference refuses — F3 |
| X08 | empty string on one side only | mismatch | mismatch | yes | present-but-empty ≠ absent |
| X09 | empty string both sides | match | match | yes | identical values |
| X10 | non-nominated field differs | match | match | yes | only nominated fields participate |
| X11 | three field lines | match | match | yes | ordered combination, `, ` |
| X12 | HTAB after the Vary comma | match | match | yes | OWS around list comma |
| X13 | value differs by internal HTAB | mismatch | mismatch | yes | profile; **spec: match** (whitespace after a list comma is removable) |
| X14 | quoted member | invalid_input | invalid_input | yes | DQUOTE ∉ tchar |
| X15 | two keys differing only in name case | match | invalid_input | **no** | §5.1+§5.2 combine in order; reference calls it an ambiguous duplicate — F4 |
| X16 | `*` with both maps empty | mismatch | mismatch | yes | star must not be short-circuited by an empty-map match |
| X17 | array with trailing empty element | mismatch | mismatch | yes | profile; **spec: match** (§5.6.1.1) |
| X18 | leading OWS + upper-case member | match | match | yes | OWS is not part of the name; names case-insensitive |

Tally: **15/18** for the candidate, the L1 candidate (`receipts/L1-extras.txt`) and the counter
reference. The three misses are exactly the three inputs whose verdict no committed document
defines; the candidate's own refusals name its conventions verbatim
(`receipts/refusal-messages.txt`):

```
invalid_input: presented field name 'accept-encoding ' is not a token
invalid_input: presented field 'accept-encoding' value must be a string or a non-empty array of strings
invalid_input: stored field name 'accept-encoding' is an ambiguous case-variant duplicate
```

## Findings

**F1 — the freeze was amended mid-wave (v2 → v3), 6 minutes after dispatch. Severity: high for
evidence hygiene, none for the case set.**

My first read of the frozen inputs (15:52) captured contract sha256 `b8f7db94…` and counter
`285bca22…`. Both changed under me:

```
mtime 15:57:12  .ufo/waves/round-88/c88_vary.py   sha256 e4cf5ad9…   (was 285bca22…)
mtime 15:57      contract.md                       sha256 639035d3…   (was b8f7db94…)
commit 52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644   2026-11-04T15:58:05-03:00
  "round-88: freeze amendment v3 — validation precedes the wildcard rule"
```

`git diff f60a852a 52e41d2d` (`receipts/freeze-delta-v2-v3.diff`, 314 lines) moves the wildcard
check after input validation in `reference()`, adds `w1/L1/vary_match.py`, rewrites
`contract.md`'s freeze history and profile, and regenerates `controls/base-c2.txt`,
`controls/ctl-c2-constant-*.txt` and `controls/c2-selftest.txt`. I re-verified the regenerated
controls are self-consistent with v3 (`base-c2.txt random_sha256=52714a5f…`, constant-invalid
stub `random=24`), and the case set never moved (`vary-cases.json` sha256 `c461cb…` before and
after; all 20 labels unchanged; reference still 20/20 on them).

Consequence to manage: **any receipt written between 15:52 and 15:58 cites a superseded
contract** (mine included). It also means the three random cases r53/r150/r193 changed label
under the v3 rule (mismatch → invalid_input); 21 → 24 invalid cases. The contract's own sentence
"nothing in this contract, in the two counters or in the case set is edited after a seat scores"
is arguably kept (no candidate file existed before 15:56 and none had been scored), but the
amendment landed while the 14 dispatched seats were working from v2, so their evidence and
reports should be re-pinned to `52e41d2d`.

**F2 — `contract.md` never enumerates the adapter's refusal rules, yet 24/200 random labels and
4/20 frozen cases are refusals. Severity: high for reachability, not a mislabelled case.**

The contract's "Profile (declared, bounded)" paragraph describes only the match rule and the
conservative comparison. The refusal triggers (non-string `vary`, non-string field values, empty
members, empty `Vary`, non-token members) live in `c88_vary.py`'s docstring and in ExecReader's
item, not in the contract. v3 added only the *precedence* sentence. A reader implementing the
contract as written can return `match`/`mismatch` where the counter expects `invalid_input` and
miss C2 with no document telling it why. The 24 invalid labels split exactly (one trigger each,
`receipts/invalid-random-triggers.txt`):

| trigger | n | ids |
|---|---|---|
| empty member (`vary` ends in `,`) | 7 | r46 r122 r137 r147 r172 r184 r186 |
| empty / OWS-only `Vary` | 4 | r61 r77 r152 r194 |
| non-string `Vary` | 4 | r26 r40 r90 r169 |
| non-string stored value | 5 | r16 r76 r134 r150 r193 |
| non-token member | 2 | r34 r109 |
| empty array as a field value | 2 | r53 r183 |

Only the non-string carriers are even hinted at by the counter docstring; the empty-element and
empty-array rules appear nowhere in the contract.

**F3 — empty JSON array as a field value is labelled by a rule declared nowhere.
Severity: medium (2/200: r53, r183).** r183 is `invalid` because `presented.accept-language
== []`; r53 is `invalid` for the same reason with a `*` also present, which v3 otherwise routes
to `mismatch`. Zero field lines is the same input as "field absent", which the absence sentence
makes a `mismatch`; the candidate's message ("must be a string or a non-empty array of strings")
is the first place the non-empty rule appears. Either declare it in the contract or label those
cases `mismatch`.

**F4 — two request-map keys differing only in name case are refused as "ambiguous".
Severity: low today, medium if the generator ever emits them.** `reference()` refuses when
`low in out` after case-folding. RFC 9110 §5.1 + §5.2 make those two field lines of one field
and combine them in order; Python dicts preserve order, so the combination is well defined.
No frozen or random case exercises it (census: 0 of 200), so it is latent — X15 is the probe.

**F5 — frozen case 14 (`Vary: ""`) forces an answer that RFC 9110 §5.6.1.1 points the other way.
Severity: medium; case-set narrowing, honestly labelled.** The case's own basis says "local
adapter refuses it", and the wave does declare the convention, so the case is not mislabelled
*against the wave*. But a strictly conformant reader — zero nominated fields ⇒ §4.1's `MUST NOT`
is vacuously satisfied; §5.6.1.1 requires a recipient to "parse and ignore a reasonable number
of empty list elements" — answers `match` and scores **19/20**, i.e. the claim is unreachable
for it. The same holds for X02/X17. Recommend the contract state that the reader is a *local
adapter* whose input domain excludes empty elements, so the narrowing is visible in the claim.

**F6 — the C2 counter has no exception path around `subprocess.run`: a hanging candidate
crashes the counter with no receipt. Severity: medium (operational).** Demonstrated with a stub
that sleeps 30 s:

```
subprocess.TimeoutExpired: Command '['/usr/bin/python3', '-B',
  '/fast/scratch/hyaku/kake-r88/ExecCases/c2-hang/frozen/vary_match.py']' timed out after 20 seconds
HANG_EXIT=1
```

No JSON line is printed, so the predicate's receipt disappears exactly when a seat's candidate is
broken — the case where the counter is most needed. `score()` should catch `TimeoutExpired` and
count the case as failed. (Same shape for a candidate killed by a signal.)

**F7 — bytecode of the frozen counters sits inside the freeze directory. Severity: low.**
`.ufo/waves/round-88/__pycache__/c88_vary.cpython-314.pyc` (mtime 15:57) and
`c88_defect_queue.cpython-314.pyc` (15:54) are untracked files in the frozen tree; an import with
matching source mtime+size executes them. All my runs used `python3 -B` with
`TMPDIR=/fast/scratch/hyaku/kake-r88/ExecCases/tmp`; the CLI (`__main__`) path never reads them.

**F8 — the 20-case set is internally consistent.** No case contradicts the declared profile; the
20 labels, the constant-stub counts (7/9/4) and the reference agree. The defects above are about
*what the contract documents*, not about a wrong label under that contract.

## Exact commands and exits

```
# hashes at run time (16:00 -03:00)
sha256sum c88_vary.py            -> e4cf5ad943a2f54742562ad169f437197c01bb67eb423aa93d457ba912c95124
sha256sum vary-cases.json        -> c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d

# freshness of the extras
cd .../w1/ExecCases && python3 -B freshness.py            exit 0
  {"collisions": [], "extras": 18, "frozen": 20}

# my expectations vs the frozen labels
python3 -B expect_check.py                                exit 0
  {"cases": 20, "disagreements_with_frozen": [],
   "verdict_histogram": {"invalid_input": 4, "match": 7, "mismatch": 9}}

# trigger census of the 24 invalid random labels
python3 -B classify_random.py                             exit 0
  {"invalid_total": 24, "by_trigger": {"empty-member": 7, "vary-empty": 4, "vary-nonstr": 4,
   "stored-nonstring-value": 5, "non-token-member": 2, "presented-empty-list": 2}}

# candidate (read-only: copied into --work and run there)
python3 -B runner.py --tool ../../w1/ExecReader/vary_match.py \
  --work /fast/scratch/hyaku/kake-r88/ExecCases/run-extras    exit 1   (15/18)
python3 -B runner.py --tool ../../w1/ExecReader/vary_match.py \
  --cases ../../vary-cases.json --work .../run-frozen         exit 0   (20/20)

# official counter, both candidates
python3 -B c88_vary.py --tool .../w1/ExecReader/vary_match.py --work ...   exit 0, met=true
python3 -B c88_vary.py --tool .../w1/L1/vary_match.py         --work ...   exit 0, met=true

# counter selftest under the frozen bytes
TMPDIR=... python3 -B c88_vary.py --selftest              exit 0   (17/17)
```

Replay for L1 (scratch TMPDIR required; `runner.py` accepts any `--work`):

```
TMPDIR=/fast/scratch/hyaku/kake-r88/L1 python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecCases/runner.py \
  --tool /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/ExecReader/vary_match.py \
  --work /fast/scratch/hyaku/kake-r88/L1/run
```

## Limits

- **No network.** No URL is named in this seat's item, so the RFC sentences are either reproduced
  locally (`contract.md`, `vary-cases.json` bases) or recalled from model knowledge. I marked each
  one `quote_status: local|recalled` in `expectations.json`. F5's §5.6.1.1 sentence and the
  `weight = OWS ";" OWS "q=" qvalue` grammar are `recalled`; ScoutSpec holds the fetched text.
  Nothing here proves cache-key construction, storage, freshness, serving or browser behaviour.
- **No live surface** was contacted; no page behaviour is asserted.
- The three extras marked `no` in Table 2 are disagreements with a *convention*, not with RFC
  text; X04/X07 in particular have two defensible answers. I report them as under-specified, not
  as candidate bugs, and the batch keeps them so L1 can see the gap rather than hide it.
- I did not re-score the candidate after 16:00; its sha256 `fdceef47…` is the one I measured.
- The frozen case file was never edited; the only writes are under `w1/ExecCases/`.

## Files written

```
.ufo/waves/round-88/w1/ExecCases/
  expectations.json                    20 cases: expected, reason, deciding sentence, spec_reading
  extra-cases.json                     18 fresh inputs: expected, spec_reading, basis, axis
  runner.py                            read-only scorer (--tool / --ref), same rule as the counter
  freshness.py                         proves no extra tuple repeats a frozen one
  expect_check.py                      my 20 expectations vs the frozen labels
  classify_random.py                   trigger census of the invalid half of the seeded population
  receipts/  freshness.txt, expectations-vs-frozen.txt, reference-vs-frozen.txt,
             reference-vs-extras.txt, ExecReader-frozen.txt, ExecReader-extras.txt,
             L1-extras.txt, official-counter-tool-runs.txt, refusal-messages.txt,
             invalid-random-triggers.txt, counter-timeout-crash.txt,
             independence.txt, freeze-commits.txt, freeze-delta-v2-v3.diff
w1/ExecCases.md                        this report
```

Scratch `/fast/scratch/hyaku/kake-r88/ExecCases/` was deleted after the receipts were copied;
nothing was cited from `/tmp`.
