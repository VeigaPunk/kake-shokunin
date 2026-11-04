# CriticClaims — round 88, wave w1 — falsification report

Seat: critic. Assignment: falsify C1 (calibration, lowest owned axis, 2 HOLD) and C2
(freshness, 10 HOLD) using committed bytes only; build the assigned lookup/heuristic
stubs and report every false-green actually executed. No production edits, no commits,
no delegation, no network, no tool installs.

Evidence root: `.ufo/waves/round-88/w1/CriticClaims/` (82 files; `manifest.sha256`).
Scratch `/fast/scratch/hyaku/kake-r88/CriticClaims/` was deleted after copying receipts.

## 0. The freeze moved during the wave — read this before any score

The seat names freeze **v2** `8063739791e21a8d7966fd968913e552e1433881`. While this seat
was reading and scoring, the counter was replaced by **v3** `52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`
(“freeze amendment v3 — validation precedes the wildcard rule”), committed at
`2026-11-04T15:58:05-03:00`, six minutes after dispatch (`w1.ready.dispatched`
`2026-11-04T15:52:15`).

Committed-byte facts (both versions read from git; every score below prints the counter
sha and `random_sha256` in its receipt):

| fact | v2 `285bca22…` | v3 `e4cf5ad9…` |
|---|---|---|
| commit | `80637397` 15:49:39 | `52e41d2d` 15:58:05 |
| `reference()` order | `*` short-circuits **before** validating headers | headers validated **before** `*` |
| random labels r53, r150, r193 | `mismatch` (exit 0) | `invalid` (exit 1) |
| random counts | match 67 / mismatch 112 / invalid 21 | 67 / 109 / 24 |
| `random_sha256` | `004a8eb75b95ed45919734cee6d2b501a6f9b8da61e654c58ec1ee2b87bc2b50` | `52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981` |
| base control `controls/base-c2.txt` | `004a8eb…` | rewritten to `52714a…` |
| L1 candidate `w1/L1/vary_match.py` | not present | added in the same commit; sha `2da573d3…` |

The 200 inputs are identical between versions (checked pairwise; `receipts/c2/v2v3_labels.json`:
`"same_inputs": true`, exactly three verdict flips). So v3 did move case **labels**,
contradicting its own sentence “No item, case, threshold, control or target moved”: the
constant-mismatch control moved 112→109 and always-invalid 21→24, and three expected
verdicts moved. The file mtimes are `w1/L1/vary_match.py` 15:56:39, `c88_vary.py`
15:57:12, commit 15:58:05: the candidate existed before the oracle was edited, and the
oracle edit is exactly what flips the candidate from **197/200 under v2** to **200/200
under v3** (§2.5).

Consequence: a C2 receipt is only meaningful with its counter sha. This report scores
both committed versions. The seat's named freeze (v2) is used wherever “freeze v2” is
written; v3 results are labelled.

## 1. C2 — the assigned lookup probe

Stub: `tools/lookup20_exit2.py` (sha `c62bf7b5…`), table keyed on `sha256(stdin bytes)`
of the 20 frozen payloads built with the harness's own `json.dumps({vary,stored,presented})`;
unknown input exits 2.

```
$ TMPDIR=/fast/scratch/hyaku/kake-r88/CriticClaims \
  python3 -B <counter> --tool tools/lookup20_exit2.py --work work/<name>
```

| counter | frozen | random | met | exit | receipt |
|---|---|---|---|---|---|
| v2 `285bca22` | **20/20** | **0/200** | false | 1 | `receipts/c2/v2_lookup20.json` |
| v3 `e4cf5ad9` | **20/20** | **0/200** | false | 1 | `receipts/c2/v3_lookup20.json` |

**The random population kills the 20-case lookup. Said plainly:** it scores 0/200 on
both versions. Cause is measured, not assumed: `frozen_random_payload_overlap: 0`
(`receipts/c2/v3_analysis.txt`), so every random payload is unknown to a table keyed
only on the frozen 20. With a best-constant fallback (unknown → `mismatch`) the same
20-case table scores 20/20 + **109/200** on v3 (`receipts/c2/lookup20_bestconst.json`),
still a kill.

So the literal probe passes. The contract's stronger sentence is nevertheless false —
see §2, where a lookup table keyed on the **whole** population passes 200/200.

## 2. C2 — false-greens actually executed

### 2.1 A lookup table over the committed seed passes 20/20 + 200/200

The counter commits the generator, the seed `88_088`, and therefore all 200 random
inputs before any candidate exists. A table over the 216 distinct payloads (220 cases,
4 duplicate payloads) needs no profile logic:

```
$ python3 -B build_table_for.py counters/v2/c88_vary.py stubs_v2   # import committed generator
$ python3 -B build_table_for.py counters/v3/c88_vary.py stubs_v3
$ python3 -B <counter-v2> --tool stubs_v2/lookup220.py --work work/v2_lookup220
$ python3 -B <counter-v3> --tool stubs_v3/lookup220.py --work work/v3_lookup220
```

(As run under scratch; the evidence copies of the two tables are
`tools/lookup220_v2_table.py` and `tools/lookup220_v3_table.py`, and the receipts record
the run-time `file:` paths.)

v3 result, exit **0** (`receipts/c2/v3_lookup220.json`, table sha `af6b4433…`):

```json
{"cases_sha256": "c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d", "claim": "C2", "details": [], "frozen": 20, "frozen_total": 20, "met": true, "random": 200, "random_sha256": "52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981", "random_total": 200, "revision": "file:stubs_v3/lookup220.py", "tool_sha256": "af6b44333b55dc3f60a6473b86df81b9d909adc17bb3a421dc0946478890d3d1"}
```

v2 result is identical except the pinned v2 hashes (`receipts/c2/v2_lookup220.json`,
table sha `2bcd1594…`, `random_sha256` `004a8eb…`, `met: true`, exit 0).

This directly contradicts both committed texts:

- `c88_vary.py:11-12` (both versions): “A lookup table keyed on known inputs cannot
  pass this population.”
- `contract.md` C2 kill rule (v2 lines 73-75; v3 lines 77-79): “a lookup table keyed
  on known inputs cannot pass it.”

The claim is true only for a table keyed on the **frozen 20**. It is false for a table
keyed on the 200 “random” cases, because those are equally known at freeze time. The
counter's anti-lookup sentence is a non-sequitur: the reference-vs-frozen selftest does
not hide the population; it publishes it.

### 2.2 An oracle-import stub passes 20/20 + 200/200 with zero profile logic

`tools/oracle_import.py` reads stdin, imports the counter by absolute path, calls its
`reference()` and prints the verdict. No reader is implemented. v3, exit **0**
(`receipts/c2/oracle_import.json`, tool sha `c498fb31…`):

```json
{"cases_sha256": "c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d", "claim": "C2", "details": [], "frozen": 20, "frozen_total": 20, "met": true, "random": 200, "random_sha256": "52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981", "random_total": 200, "revision": "file:stubs/oracle_import.py", "tool_sha256": "c498fb31561c04081aaf35e93c07a7f6c0491d63f200c2207f076bc526d355bb"}
```

The counter runs the candidate with inherited cwd and no read restriction, so the
oracle is reachable. This is a measurement-isolation defect, not a hypothetical: the
candidate executable can read `.ufo/waves/round-88/c88_vary.py` and `vary-cases.json`
at scoring time. (The static 216-entry table in §2.1 passes without any runtime read,
so sandboxing alone would not fix the lookup hole.)

### 2.3 The random population is not trivially separable, but it is shallow

Three cheap heuristics, scored on v3 (`receipts/c2/heur_*.json`; each exit 1):

| stub | rule | frozen | random |
|---|---|---|---|
| `heur_star_substring.py` | `mismatch` iff `*` appears anywhere in stdin, else `match` | 9/20 | **92/200** |
| `heur_exact_eq.py` | `match` iff `stored == presented` as Python objects | 11/20 | **158/200** |
| `heur_naive_iface.py` | name-fold, presence check, exact value equality; no OWS trim, no list combination, no value validation | 17/20 | **188/200** |

No tested one-line rule reaches 200, so the population is **not degenerate** under the
specific separator the seat proposed (“does the JSON contain `*`”: 92/200). But 94 % is
reachable by a reader that omits two of the three declared transformations (leading/
trailing OWS removal and ordered multi-line combination) and omits the refusal rules.
Its 12 random failures are exactly the transformation cases: 4 OWS, 3 OWS+non-string,
3 list, 2 non-string (`receipts/c2/naive_failures.txt`; `heur_naive_iface.json`).
The population mostly rewards exact equality, not the declared profile.

Population redundancy: 200 cases, **196 distinct payloads**, 4 duplicate payloads in
three groups (r50/r94/r182, r67/r92, r142/r163); all duplicates carry the same expected
verdict, so determinism is not violated, but the batch has 2 % redundancy
(`receipts/c2/v3_analysis.txt`).

### 2.4 The random labels drift from the declared profile: one unstated rule costs 2/200

`contract.md` declares “multiple field lines combine in order with `, `” but never says
a zero-element list is refused. The reference refuses it (`normalise()` requires a
non-empty list). The frozen 20 contain no empty-list case. Consequence, executable:
`tools/alt_empty_list_v3.py` implements the v3 reference exactly **except** it reads a
zero-line list as the empty combined value (`', '.join([]) == ''`). It matches all 20
hand labels and scores **198/200** on v3, failing r53 and r183
(`receipts/c2/v3_alt_empty_list_v3.json`, tool sha `95f01bda…`, exit 1):

```json
{"cases_sha256": "c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d", "claim": "C2", "details": [{"case": "r53", "err": "", "exit": 0, "ok": false, "out": "mismatch"}, {"case": "r183", "err": "", "exit": 0, "ok": false, "out": "mismatch"}], "frozen": 20, "frozen_total": 20, "met": false, "random": 198, "random_sha256": "52714a5f4ae9b66ee444f39284b6e5ce575c6ae5760965fb8736e6983444b981", "random_total": 200, "revision": "file:stubs/alt_empty_list_v3.py", "tool_sha256": "95f01bda3b53ca07df5a8ed7ce4ca0d0639819393861339143e67ab0fe9bd79e"}
```

On v2 the same empty-list reading scores 199/200, failing r183 only
(`receipts/c2/v2_alt_empty_list.json`). This falsifies the contract's inference at
`contract.md` C2 (v3 lines 77-79): agreement with the 20 hand labels does **not** prevent the
generated batch drifting from the spec-derived one, because the 20 labels underdetermine
the adapter's refusal set. A candidate must guess the reference's unstated `[]` rule.

### 2.5 The v2→v3 amendment is load-bearing for the L1 candidate

`tools/candidate_L1.py` is the committed `w1/L1/vary_match.py` (sha `2da573d3…`).

| counter | frozen | random | met | exit | receipt |
|---|---|---|---|---|---|
| v2 `285bca22` | 20/20 | **197/200** (r53, r150, r193) | false | 1 | `receipts/c2/v2_candidateL1.json` |
| v3 `e4cf5ad9` | 20/20 | **200/200** | true | 0 | `receipts/c2/v3_candidateL1.json` |

The candidate validates headers before `*`; v2's reference did the opposite. The v3
amendment changes exactly those three labels. The amendment and the candidate were
committed together (v3 adds `w1/L1/vary_match.py`); by bytes alone the reference and the
candidate now share the same precedence, so the differential population cannot serve as
an independent check of that candidate. Why the edit was made is not provable from bytes
(`[INFERENCE]` on motive); the 197→200 effect is measured.

Timeline fingerprint of the change, from this seat's own run: `tools/lookup220.py` was
built from the counter as read before the rewrite and scored against v3. It failed
exactly r53/r150/r193 with `out: "mismatch"` (197/200, `receipts/c2/lookup220.json`) —
the three relabelled cases, not a lookup miss.

### 2.6 What would catch the C2 false-greens (smallest safe corrections)

1. **Secret-at-scoring-time population.** Commit `sha256(seed || nonce)` before the
   candidate exists; reveal the seed only when scoring and print the generated
   `random_sha256` in the receipt. A static 216-entry table then cannot be built.
   Do not commit the seed and generator in the same bytes the candidate can read.
2. **Isolate the candidate.** Run it with an empty cwd, `env -i`, and no read access to
   LANE/counter/case file (namespace/bwrap or a throwaway account); plus a static check
   that the candidate does not open external paths. This kills §2.2 but not §2.1.
3. **Pin by hand, not by reference.** Add frozen cases for every precedence/refusal the
   reference currently decides alone: `*` + malformed header map, empty array on a
   nominated field, duplicate lower-cased keys, non-token keys. Then the 20 (or 24)
   hand labels, not the reference, fix the profile; §2.4 becomes impossible.
4. **Freeze once per wave.** The seat's named freeze was v2; HEAD is v3. A post-dispatch
   amendment of the reference/generator/controls must either restart the wave or be a
   separate claim. Every receipt must carry the counter sha (these do).

## 3. C1 — assigned probes and false-greens actually executed

Counter: `c88_defect_queue.py` sha `1d550923…` (identical v2/v3; selftest 11/11,
base `f4479c14` → open=3 exit 1, reproduced in `receipts/c1/c1_base.txt`).

Method: full mirror trees built with the counter's own `mirror_tree()`, then scored:

```
$ python3 -B <c1counter> --mirror <tree> --work <work>
```

### 3.1 D2 — right diagnostic words, wrong arithmetic: PASSES

`c1_fixtures.py` writes `c1trees/d2_constant/cache_current_age.py`: it prints
“date_value must be an integer, not float/boolean” for the two bad inputs, returns a
**constant** `CANNED` object for every accepted payload, and its `--selftest` prints
“selftest: 61 isolated CLI fixtures passed” without running anything.

Result, exit **0** (`receipts/c1/c1_d2_constant.json`):

```
C1v1 revision=mirror:/fast/scratch/hyaku/kake-r88/CriticClaims/c1trees/d2_constant items=3 open=0 closed=3 met=true
{"D1-ledger-companion": [], "D2-diagnostic-type": [], "D3-recheck-path": []}
```

Second valid payload `{"date_value":0,"request_time":0,"response_time":0,"now":100,"age_value":0}`
must give `resident_time=100, current_age=100`; the tool exits 0 and prints
`current_age: 50, resident_time: 30`
(`receipts/c1/c1_d2_constant_second_payload.txt`). D2 only ever exercises its single
committed `VALID` fixture, so a constant-output tool is green.

A weaker variant of the same hole: `c1trees_extra/d2_float_outputs` emits the six terms
as **floats** (`20.0 …`). The counter compares `json.loads(stdout) != VALID_OUT`, and
`20.0 == 20`, so it passes (`receipts/c1/c1_d2_float_outputs.json`, `met=true`) although
the contract says “six integer terms”. The base tool's own selftest asserts
`type(value) is int`; the counter does not.

Key attribution is also untested: `c1trees_extra/d2_hardcoded_key` always writes
“date_value … not float” even when the float is on `request_time`; D2 passes
(`receipts/c1/c1_d2_hardcoded_key.json`, `met=true`) while its probe prints
`invalid_input: date_value must be an integer, not float` for a `request_time` float
(`receipts/c1/c1_d2_hardcoded_key_probe.txt`).

### 3.2 D1 — right sha256, false description: PASSES

`c1_fixtures.py` writes a companion with filled `source:` (naming the ledger),
`verified-at:`, `recheck:`, the true ledger sha256 `ef58f909…`, and a body that says the
ledger “records no decisions”, “every row is still pending”, “sixteen rows disagree”
(the ledger has 8 rows: 3 admit, 5 reject, 8 outside agree). Result, exit **0**
(`receipts/c1/c1_d1_false_desc.json`):

```
C1v1 … items=3 open=0 closed=3 met=true
{"D1-ledger-companion": [], "D2-diagnostic-type": [], "D3-recheck-path": []}
```

A companion of **three metadata lines and no prose at all** also passes
(`receipts/c1/c1_d1_metadata_only.json`). D1 checks presence of three keys, the path
substring, and the digest substring; it never reads a claim from the companion.

### 3.3 D3 — degenerate cadences and line-ending rewrites pass

- `recheck: 0d` passes (`receipts/c1/c1_d3_zero_cadence.json`, `met=true`). The
  predicate accepts `rest[:1].isdigit()` and `'d' in rest.split()[0]`; zero days is not
  a cadence.
- `recheck: 2026-11-04 — reopened; see checklist.` passes via the `rest[:4].isdigit()`
  branch with no interval at all (`receipts/c1/c1_d3_iso_date.json`, `met=true`;
  independently observed by ScribeLedger).
- Rewriting the whole entry with CRLF passes (`receipts/c1/c1_d3_crlf.json`,
  `met=true`), although every base line's bytes changed: entry 5741 B vs base 5554 B,
  +187 `\r`. The history check compares `splitlines()`, which discards `\r`.

### 3.4 The junk-prose control: it does leave exactly one item open — for the wrong reason

Reproduced the counter's exact mutant (mirror green tree, overwrite the tool with the
frozen base tool). Exit **1** (`receipts/c1/c1_junk_control.json`):

```
C1v1 … open=1 closed=2 met=false
{"D1-ledger-companion": [], "D2-diagnostic-type": ["float input diagnostic does not name float (or still says boolean)"], "D3-recheck-path": []}
```

Exactly one open (D2). But the selftest's `junk_prose` mutant is **byte-identically the
same mutation** as its `base_tool` mutant — both are
`(m / TOOL).write_bytes((FROZEN / 'base-cache_current_age.py').read_bytes())` at
`c88_defect_queue.py:269-270` and `:276-277` — and the tree keeps the **correct** prose.
A genuinely junk-prose tree (wrong companion §3.2 + base tool) produces the same
`open=1` and the same item JSON (`receipts/c1/c1_junk_true.json`). The control therefore
cannot distinguish correct prose from false prose; its “1 open” says only that D2 is the
sole behavioural item.

### 3.5 Executed C1 fixtures at a glance

All rows are exit 0, `C1v1 … open=0 closed=3 met=true`, with item JSON
`{"D1-ledger-companion": [], "D2-diagnostic-type": [], "D3-recheck-path": []}`, except
the two junk rows (exit 1, open=1, D2 non-empty as quoted in §3.4).

| fixture | what is wrong | receipt |
|---|---|---|
| `d2_constant` | constant output; arithmetic wrong on any second valid payload; fake selftest | `receipts/c1/c1_d2_constant.json` |
| `d2_float_outputs` | six terms emitted as floats, not integers | `receipts/c1/c1_d2_float_outputs.json` |
| `d2_hardcoded_key` | diagnostic always names `date_value` | `receipts/c1/c1_d2_hardcoded_key.json` |
| `d1_false_desc` | true sha256, false ledger description | `receipts/c1/c1_d1_false_desc.json` |
| `d1_metadata_only` | three metadata lines, no description | `receipts/c1/c1_d1_metadata_only.json` |
| `d3_zero_cadence` | `recheck: 0d` | `receipts/c1/c1_d3_zero_cadence.json` |
| `d3_iso_date` | date replaces the cadence | `receipts/c1/c1_d3_iso_date.json` |
| `d3_crlf` | all base line bytes changed to CRLF | `receipts/c1/c1_d3_crlf.json` |
| `junk_control` | base tool under correct prose | `receipts/c1/c1_junk_control.json` |
| `junk_true` | base tool under false prose | `receipts/c1/c1_junk_true.json` |

### 3.6 What would catch the C1 false-greens

- **D2:** run at least two valid payloads with distinct expected terms computed by the
  counter itself, covering both `max(apparent_age, corrected_age_value)` branches, a
  future Date clamp, omitted `age_value`, and equal times (the frozen base tool's own
  four fixtures are a ready set); require `type(v) is int` for all six terms, not `==`;
  test a float/bool on a key other than `date_value` and require that key named; require
  `--selftest` to report a fixture count ≥ the base's 61 (weak) and run it with an
  isolated `TMPDIR`; ideally diff the candidate against the frozen base tool on generated
  valid payloads.
- **D1:** parse the ledger and require machine-checkable tally lines in the companion,
  e.g. `ledger-rows: 8`, `decisions: admit=3 reject=5`, `outside: agree=8`, and compare
  them; require the digest on the `source:` line if the contract is read strictly. A
  prose-presence check cannot catch a false description.
- **D3:** require a real interval token (`\b[1-9]\d*d\b`) in the recheck line even when
  a date is present; compare raw line bytes (or `splitlines(keepends=True)`) for the
  history-preservation check so CRLF/EOL rewriting is rejected.

## 4. Classification — fixable defect vs declared tradeoff

- **C2 §2.1 (population lookup) — fixable counter defect, judge must reject the claim as
  measured.** The contract's own anti-lookup guarantee is false; `met=true` is
  satisfiable without the capability. Fixed by a scoring-time secret population.
- **C2 §2.2 (oracle import) — fixable measurement-isolation defect.** Fixed by
  sandboxing the candidate; secondary to §2.1.
- **C2 §2.4 (empty-list drift) — fixable case-set defect.** The 20 hand labels do not
  pin a behaviour the reference tests in 2 random cases; add the frozen case or state
  the rule in `contract.md`.
- **C2 §0/§2.5 (v2→v3 mid-wave) — integrity defect, not a tradeoff.** The seat freeze is
  v2, HEAD is v3, the random population and its labels changed, and the carrier
  candidate flips 197→200. The canonical judge must pin one counter sha; a claim
  evaluated at v3 cannot be evidenced by v2 receipts or vice versa.
- **C1 §3.1 (D2 constant/float/key) — fixable behavioural-item defect.** The contract
  calls D2 “behavioural”; one committed fixture and a vacuous selftest check do not
  measure behaviour.
- **C1 §3.2 (D1 semantics) — declared limit, not a surprise.** `contract.md` says the
  closure “does not certify the ledger's decisions”, so a false description passing is
  within the letter of the D1 predicate. If the round's prose claims the companion
  *describes* the ledger, that claim is unsupported and should be rejected or reworded;
  otherwise this is a tradeoff the judge may accept with the limit stated.
- **C1 §3.3 (D3 0d/ISO/CRLF) — fixable textual-check weakness.** “Cadence” and
  “byte-identically” are not enforced in those three ways.

## 5. Honest limits

- All C1 results are **mirror** fixtures exercising `item_d1/d2/d3`; no carrier commit
  existed in the working tree when this seat ran (`git status` showed no modified
  production tracked files). I did not integrate, and I did not score a carrier.
- C2 scores are on committed counter bytes copied to scratch (`counters/v2`,
  `counters/v3`); the lane working tree was read-only. The v2/v3 receipts pin the
  version. My first reads (~15:53) were v2; the counter changed at 15:57:12 and the
  commit landed 15:58:05. The intermediate `receipts/c2/lookup220.json` is the
  fingerprint of a v2 table meeting v3 labels (197/200, exactly r53/r150/r193).
- The 216-entry table is a measurement attack, not a proposed reader; I did not attempt
  to pass it as the carrier. The oracle stub is likewise an isolation probe.
- I did not audit sibling seats or every counter line; I executed the assigned probes
  plus cheap adjacent ones (float output, key attribution, empty-list reading, CRLF,
  ISO/0d cadence). ScribeLedger independently found the D1 digest-placement and D3
  ISO-date variants; my §3.2/§3.3 are independent executions, not copies.
- No network requests, no credentials, no tool installs, no pacman, no commits or
  mutating git/jj commands. No writes outside this seat's scratch and wave paths.

## 6. Reproduce

```sh
W=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/w1/CriticClaims
T=$(mktemp -d /fast/scratch/hyaku/kake-r88/repro.XXXX)   # explicit TMPDIR, never inherited
# C2, v3 column (swap c88_vary_v2_285bca22.py for the v2 column; both read the
# vary-cases.json that sits beside them):
TMPDIR=$T python3 -B "$W/counters/c88_vary_v3_e4cf5ad9.py" --tool "$W/tools/lookup20_exit2.py"      --work "$T/a"
TMPDIR=$T python3 -B "$W/counters/c88_vary_v3_e4cf5ad9.py" --tool "$W/tools/lookup220_v3_table.py"  --work "$T/b"
TMPDIR=$T python3 -B "$W/counters/c88_vary_v3_e4cf5ad9.py" --tool "$W/tools/oracle_import.py"       --work "$T/c"
# C1 (the evidence copy has counters/frozen/ beside the counter):
python3 -B "$W/counters/c88_defect_queue_1d550923.py" --selftest
python3 -B "$W/counters/c88_defect_queue_1d550923.py" --mirror <tree> --work "$T/d"
```

The mirror trees were built by `scripts/c1_fixtures.py` and `scripts/c1_extra.py`; their
`ROOT`/`COUNTER` constants point at the (now deleted) scratch root, so re-point them at a
fresh scratch dir and the evidence counter to regenerate the trees. The receipts quoted
above are the measured artefacts; the fixture scripts are the exact generators.

Exact receipt JSON, stderr/exit files, the 216-entry tables (v2 and v3), the L1
candidate, the C1 fixture scripts, both counter versions and the frozen base blobs are
under `w1/CriticClaims/`; `manifest.sha256` covers all 82 files (manifest excluded from
itself).
