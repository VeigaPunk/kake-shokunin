> Lane-internal findings. Not outside admission. No production byte was written by this seat.

# MutReader — round 88 mutation test of the C1 and C2 counters

## 0. What this seat did

Mutation-tested the round's two counters against a real implementation.

- **C2 target:** ExecReader's candidate `w1/ExecReader/vary_match.py`
  (sha256 `fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6`, 294 lines,
  stable across two hashes 3 s apart at 15:59). It did **not** exist when this seat started
  (checked 15:52: `ls` → "No such file or directory"); it appeared at 15:59, so it is the
  mutated artefact, as the seat spec prefers. A second, independent reference written by this
  seat (`ref_vary_match.py`, sha256 `8ec3da48…`) was mutated in parallel as a cross-check.
- **C1 target:** a green mirror tree built by the counter's own `mirror_tree()` fixture builder,
  then one mutant per item plus extra probes (19 mutants, one file per mutant).
- 60 mutants total, every one a single-point source edit with an asserting patcher
  (`text.count(anchor) == 1`), so no silent no-op mutant exists in this set.

## 1. Live instrument and its provenance (a finding in itself)

The seat spec named freeze **v2** `80637397`. While this seat was reading, LANE HEAD moved to

| object | sha256 | note |
|---|---|---|
| `c88_vary.py` v2 (`80637397`) | `285bca2242f98b49d4736e0b3a0a008059aac3b77c68fa31a0cd284af6fecd3c` | materialised by this seat into `c2-v2/` |
| `c88_vary.py` v3 (`52e41d2d`, live) | `e4cf5ad943a2f54742562ad169f437197c01bb67eb423aa93d457ba912c95124` | the counter scored here |
| `c88_defect_queue.py` | `1d550923261bb8e68859fcab48e1fdca61913d790ec288d4947ecffd47db0aa5` | unchanged v2→v3 |
| `vary-cases.json` | `c461cbd87bc9b4818381c42cd847ee94c642bedfb2cf6c829a1828c311b0802d` | unchanged v2→v3 |
| ExecReader candidate | `fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6` | copy at `exe_vary_match.py`; source untouched |
| self-written reference | `8ec3da4860ec9106d694bf9b28800be5443a7186e215449c997fe87fa4d9326a` | `ref_vary_match.py` |

Commit `52e41d2d` ("freeze amendment v3 — validation precedes the wildcard rule", file mtime
2026-11-04 15:57:12) moved `if star: return 'mismatch'` in `reference()` from **before** to
**after** request-map validation. 5 lines of `c88_vary.py`; no case, seed, generator or threshold
moved. Both revisions were scored here, because the seat spec named v2 and the live file is v3.

## 2. Baselines (all green before any mutant is read)

| run | command tail | exit | result |
|---|---|---|---|
| C2 at base `f4479c14`, v3 counter | `--root LANE --revision f4479c14` | 1 | `frozen=0/20 random=0/200 met=false`, `tool_sha256: null` |
| C2 candidate, **v3** counter | `--tool exe_vary_match.py` | **0** | `frozen=20/20 random=200/200 met=true`, `random_sha 52714a5f…` |
| C2 candidate, **v2** counter | `--tool exe_vary_match.py` | **1** | `frozen=20/20 random=197/200 met=false` — fails `r53,r150,r193` |
| C1 at base `f4479c14` | `--root LANE --revision f4479c14` | 1 | `open=3 closed=0 met=false` |
| C1 green mirror | `--mirror mirrors/green-baseline` | **0** | `open=0 closed=3 met=true` |
| counter selftests | `--selftest` ×2 | 0 / 0 | C2 `17/17`, C1 `11/11` |

C2 mutant scores are only meaningful where the unmutated baseline is green. Under **v2** the
faithful candidate already fails 3/200, so every mutant of it inherits those 3 failures and
"kill counts" become noise. All C2 kill data below is therefore from the **v3** counter.

## 3. C2 — 21 single-point mutants of ExecReader's candidate, v3 counter

Command per row: `python3 -B LANE/.ufo/waves/round-88/c88_vary.py --tool <mutant> --work <scratch>/work/v3-live-<name>`
(exact argv, exit and tallies for every run are in `receipts/commands.txt`, raw JSON in
`receipts/exec_sweep.json`). **15 killed, 6 survived.**

| mutant | single-point defect | frozen | random | frozen killer cases | verdict |
|---|---|---|---|---|---|
| e01 | field names compared case-sensitively (`low = key`) | 19/20 | **200/200** | 2 | killed |
| e02 | no OWS trim before the value compare | 19/20 | 196/200 | 9 | killed |
| e03 | array lines combined sorted (unordered) | 18/20 | 199/200 | 16, 17 | killed |
| e04 | `*` handled as an ordinary token | 18/20 | 189/200 | 7, 8 | killed |
| e05 | absent-from-both treated as mismatch | 19/20 | **200/200** | 4 | killed |
| e06 | one-sided absence treated as match | 18/20 | 188/200 | 5, 6 | killed |
| e07 | value compare case-folded | 19/20 | 173/200 | 3 | killed |
| **e08** | internal whitespace runs collapsed (`' '.join(v.split())`) | 20/20 | 200/200 | — | **SURVIVED** |
| e09 | empty/non-token Vary member accepted as match | 19/20 | 189/200 | 14 | killed |
| **e10** | ambiguous case-variant duplicate accepted (last wins) | 20/20 | 200/200 | — | **SURVIVED** |
| e11 | fields not nominated by Vary are compared too | 20/20 | 196/200 | — (r31,r108,r110,r197) | killed |
| e12 | OWS trimmed on the stored side only | 20/20 | 193/200 | — (r7,r24,r103,…) | killed |
| e13 | non-string scalar values coerced with `str()` | 19/20 | 195/200 | 19 | killed |
| e14 | non-string Vary coerced with `str()` | 19/20 | 196/200 | 20 | killed |
| **e15** | empty field value treated as absent | 20/20 | 200/200 | — | **SURVIVED** |
| **e16** | list values accept non-string elements | 20/20 | 200/200 | — | **SURVIVED** |
| e17 | empty array accepted as the empty string | 20/20 | 198/200 | — (r53,r183) | killed |
| e18 | v2 precedence restored (star before validation) | 20/20 | 197/200 | — (r53,r150,r193) | killed |
| e19 | token grammar admits SP | 19/20 | 198/200 | 15 | killed |
| **e20** | Vary members not deduplicated | 20/20 | 200/200 | — | **SURVIVED (equivalent)** |
| **e21** | token grammar admits any non-space, non-comma char | 20/20 | 200/200 | — | **SURVIVED** |

### 3.1 Survivors, with the cases that let them through

Every witness below was run through both binaries with `python3 -B`, stdin the JSON payload
(full transcript in `receipts/exec_survivors.json`).

**e08 — internal whitespace collapsed.** `{'vary':'accept-encoding','stored':{'accept-encoding':'gzip;  q=1'},'presented':{'accept-encoding':'gzip; q=1'}}`
→ candidate `mismatch` (exit 0), mutant `match` (exit 0). Frozen case 18 is the only internal-
whitespace case and it pairs *no* space with *one* space (`gzip;q=1` vs `gzip; q=1`), which a
run-collapsing normaliser still reports as a mismatch. No case anywhere contains a double SP or
an HTAB run inside a value: **`double_ws` class = 0/20 frozen, 0/200 random**.

**e10 — duplicate-key refusal removed.** `{'vary':'accept-encoding','stored':{'Accept-Encoding':'gzip','accept-encoding':'br'},'presented':{'accept-encoding':'br'}}`
→ candidate exit 1 `invalid_input: stored field name 'accept-encoding' is an ambiguous case-variant duplicate`,
mutant `match` (exit 0). The generator never puts upper-case keys in `stored`/`presented`
(it uppercases only the *Vary* members), so **`dup_case_key` class = 0/20, 0/200**. The clause
is pinned only by the candidate's own selftest, which the counter does not consult.

**e15 — empty value treated as absent.** `{'vary':'accept-encoding','stored':{},'presented':{'accept-encoding':''}}`
→ candidate `mismatch`, mutant `match`. Reference rule: one side absent, the other `''` is a
mismatch; treating `''` as absent turns it into absent-both → match. The generator injects
`''` as a value and separately pops fields from `stored`, but never in the same case, so
**`absent_vs_empty` class = 0/20, 0/200**.

**e16 — list element type check removed.** `{'vary':'accept-encoding','stored':{'accept-encoding':['gzip',5]},'presented':{'accept-encoding':'gzip, 5'}}`
→ candidate exit 1 with `invalid_input: … must be a string or a non-empty array of strings`;
mutant exits 1 with a `TypeError` traceback, i.e. its stderr does **not** begin
`invalid_input:`, so a case of this shape would fail the counter's own pass criterion.
**`mixed_list` class = 0/20, 0/200.**

**e21 — token grammar too permissive.** `{'vary':'café','stored':{'café':'x'},'presented':{'café':'x'}}`
→ candidate exit 1 `invalid_input: Vary member 'café' is not a token`, mutant `match`.
All generator names are ASCII, so **`nonascii` class = 0/20, 0/200**.

**e20 — deduplication removed: equivalent mutant, not a coverage gap.** Members are deduplicated
before the all-must-match conjunction, and a repeated conjunct cannot change the verdict. Verified
by 100,000 in-process `decide()` comparisons against the candidate with the same adversarial value
pool: **0 splits**. The counter cannot kill it and should not be expected to.

### 3.2 The frozen set pins each clause about once, and the random set carries four kills alone

- Mutants killed by **exactly one frozen case and zero random cases**: e01 (only case 2) and
  e05 (only case 4). The generator never upper-cases request-map keys and never builds a
  nominated field absent from both maps, so those two clauses rest on a single hand case each.
- Mutants with **no frozen killer at all** — only the seeded population kills them: e11 (4
  random kills), e12 (7), e17 (2), e18 (3). A frozen-only counter would let all four through.
- The five surviving defect classes are exactly the five zero-coverage classes. The mapping is
  1:1: what survives is what no case was written for.

### 3.3 The v3 amendment is load-bearing, and v2 could not have scored this candidate

- v2 and v3 label the same 200 generated inputs differently in exactly three cases: `r53`,
  `r150`, `r193`. All three are `*`-bearing Vary values with a malformed request map; v2's
  reference returns `mismatch` before validating, v3 refuses. 5/200 random cases have
  `star_with_invalid`; **0/20 frozen cases do**.
- Under v2 the faithful candidate scores `20/20 + 197/200 met=false` (exit 1). Under v3 it scores
  `20/20 + 200/200 met=true` (exit 0). A seat that had scored this candidate against v2 would have
  recorded a miss for a correct implementation.
- e18 is the same defect in reverse: restoring v2 precedence is invisible to all 20 frozen cases
  and killed only by those 3 random cases.
- Cross-check: this seat's own v2-order reference scores `20/20 + 197/200` under v3 on the same
  three cases — the delta is the amendment, not the candidate.

### 3.4 Secondary cross-check: 20 mutants of a self-written reference (v2-order, v2 counter)

`mutants_selfref/`, scored while the live counter was still v2 (green baseline 20/20 + 200/200):
**15 killed, 5 survived — m08 (ws collapse), m11 (dup-key refusal), m16 (empty value as absent),
m17 (list element type), m19 (empty-member guard removed)**. m19 is equivalent: 0 splits over
100,000 in-process `reference()` comparisons against its own base, and the guard is redundant
because `is_token('')` already refuses the empty member. The other four are the *same four gaps*
found independently in a second implementation — evidence about the case set, not about one
candidate. This sweep is a v2-instrument check only: the same file scores 197/200 under v3.

## 4. C1 — 19 mutants in mirror trees

Command per row: `python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --mirror <mirror> --work <scratch>/work/c1-<name>`
(exits and full stdout in `receipts/c1_sweep.json`, `receipts/c1_extra.json`, `receipts/commands.txt`).
Green baseline: `open=0 closed=3 met=true`, exit 0. **11 caught, 8 not.**

| mutant | item | what the tree does | exit | open | verdict |
|---|---|---|---|---|---|
| c1_d1_source_dropped | D1 | `source:` names no ledger path | 1 | D1 | caught |
| c1_d1_digest_zeros | D1 | quotes 64 zeros instead of the sha256 | 1 | D1 | caught |
| c1_d1_ledger_altered | D1 | one ledger item retitled (bytes differ) | 1 | D1 | caught |
| c1_d1_verified_empty | D1 | `verified-at:` present but empty | 1 | D1 | caught |
| **c1_d1_source_path_suffix** | D1 | `source:` names `gate-agreement-ledger.json.bak` | **0** | — | **NOT CAUGHT** |
| c1_d2_base_message | D2 | float diagnostic reverted to "not boolean" | 1 | D2 | caught |
| c1_d2_bool_says_float | D2 | boolean diagnostic also says "float" | 1 | D2 | caught |
| **c1_d2_hardcoded_key** | D2 | diagnostic always names `date_value` | **0** | — | **NOT CAUGHT** |
| **c1_d2_hardcoded_valid** | D2 | the 80/90/100/130/5 payload is a hardcoded literal | **0** | — | **NOT CAUGHT** |
| **c1_d2_vacuous_selftest** | D2 | `--selftest` prints a green line, runs 0 fixtures | **0** | — | **NOT CAUGHT** |
| **c1_d2_no_arithmetic** | D2 | zeros arithmetic + hardcoded valid + vacuous selftest | **0** | — | **NOT CAUGHT** |
| c1_d3_base_recheck | D3 | base `recheck:` line restored | 1 | D3 | caught |
| c1_d3_ephemeral | D3 | `recheck:` names `TMPDIR=/fast/scratch` | 1 | D3 | caught |
| c1_d3_no_mktemp | D3 | body uses `mkdir scratch`, not `mktemp -d` | 1 | D3 | caught |
| c1_d3_edited_line | D3 | an unrelated base line edited | 1 | D3 | caught |
| c1_d3_two_recheck | D3 | a second `recheck:` line appended | 1 | D3 | caught |
| **c1_d3_zero_cadence** | D3 | `recheck: 0d; …` | **0** | — | **NOT CAUGHT** |
| **c1_d3_iso_date_only** | D3 | `recheck: 2026-11-04 — opened this round` (no cadence) | **0** | — | **NOT CAUGHT** |
| **c1_d3_forbidden_mktemp** | D3 | body says `Never run … mktemp -d … --selftest` | **0** | — | **NOT CAUGHT** |

### 4.1 C1 survivors, with the bytes that got through

- **D1 `.bak`.** The mirror's source line reads
  `source: corpus/knowledge/gate-agreement-ledger.json.bak — lane metadata ledger; ledger sha256 ef58f9…`.
  `corpus/knowledge/gate-agreement-ledger.json.bak` **does not exist in LANE** (`Path.exists()` → False),
  yet `D1` closes. Cause: `item_d1` tests `LEDGER in l`, a substring test, so any longer path that
  contains the ledger path satisfies "names the ledger path". A source line naming a
  non-existent lookalike is accepted.
- **D2 key.** With the payload `{"date_value":1,"request_time":2,"response_time":3,"now":3.5}` the mirror
  prints `invalid_input: date_value must be an integer, not float` — the offending key is `now`,
  the message names `date_value`. The counter only ever feeds `date_value` as the offending key,
  so it cannot see this.
- **D2 lookup table.** `c1_d2_hardcoded_valid` returns a literal for the one probed payload and the
  real arithmetic otherwise (second payload `17/23/29/40/2` → correct `12,6,8,12,11,23`).
  `c1_d2_no_arithmetic` goes further: it returns **all zeros for every payload** and still closes
  D2 with `open=0 closed=3 met=true`, because (a) the only valid fixture is the hardcoded literal,
  (b) validation (float/bool) is a separate code path and stays correct, and (c) the `--selftest`
  gate is self-attested — the vacuous version prints `selftest: 0 isolated CLI fixtures passed`
  and exits 0. A carrier can therefore satisfy D2 while computing nothing.
- **D3 `0d`.** `recheck: 0d; reopen https://…` closes D3: the test is
  `rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())`, so `0d` is a
  "cadence".
- **D3 ISO date.** `recheck: 2026-11-04 — opened this round; …` closes D3 through the
  `rest[:4].isdigit()` arm. `contract.md` D3 requires the entry to "keep a **cadence**"; a fixed
  date is not a cadence. This is a contract-vs-counter divergence, not just a loose regex.
- **D3 forbidden command.** The appended line
  `6. Never run TMPDIR=$(mktemp -d) python3 -B scripts/cache_current_age.py --selftest; that command is forbidden in this entry.`
  closes D3: the test only asks that one line contain `mktemp -d`, `scripts/cache_current_age.py`
  and `--selftest`, with no direction, existence or executability check. An entry that forbids
  the offline command it is required to carry passes.

## 5. Defects found in the round's own instruments and case set

Ordered by consequence. Per the kill rule, none of these rewrites the contract; they are
discriminating-power findings for L1.

1. **C1/D2 is satisfiable by a tool that computes nothing** (`c1_d2_no_arithmetic`: `met=true`
   with all six terms zero on every real payload). One valid fixture plus a self-attested
   `--selftest` cannot measure the arithmetic. A second, differently-shaped valid payload that
   is not the hardcoded one would kill it.
2. **C1/D1 accepts a source naming a non-existent lookalike** (`.bak`), because the ledger path
   is matched by substring containment rather than as a path token.
3. **C1/D3 accepts `0d` and a bare ISO date** although the contract requires a cadence, and
   accepts a body line that *forbids* the required command.
4. **C2/v2 scored a correct candidate as a miss** (`20/20 + 197/200`): the freeze was amended
   from v2 to v3 during this wave, after the seat spec was written. v3 fixes the reference
   precedence and restores a green baseline; the seat spec still names v2. Any C2 seat that ran
   between the spec and commit `52e41d2d` (15:57:12) would have reported a false miss.
5. **C2 case-set gaps, each with a live survivor:** no case with an internal SP/HTAB **run**
   (e08), no case-variant duplicate key (e10), no absent-vs-empty pair (e15), no mixed-type list
   (e16), no non-ASCII token candidate (e21). Counts: 0/20 and 0/200 in every one of these classes.
6. **C2 generator blind spots:** it upper-cases only Vary members, never the request maps
   (why e01 survives all 200 random cases); it never builds a nominated field absent from both
   maps (why e05 does); and it never emits a double space.
7. **C2 kill concentration:** two mutants are killed by exactly one frozen case and zero random
   cases (e01 by case 2, e05 by case 4); four mutants are killed only by the seeded population
   (e11, e12, e17, e18). The frozen set pins each declarative clause about once.
8. **C2 star precedence has no frozen coverage:** `star_with_invalid` = 0/20 frozen, 5/200 random.
   The only hand case binding the star rule (case 7/8) uses well-formed maps, so the precedence
   question v3 exists to answer is answered only by generated inputs.
9. **C2 dead guard (harmless):** `if not members or any(m == '' for m in members)` is redundant
   with `is_token('')`; removing it is an equivalent mutant (0/100k), so it is unreachable code,
   not a defect in behaviour.
10. **C2 receipt truncation:** `details=(frozen_details + random_details)[:12]` means a receipt
    can show 12 failures for a candidate with 20; the tallies stay correct, so this is a
    diagnostic limit only.

## 6. Limits — what this does not show

- No live surface, no network, no RFC text was exercised; the claim under test is the counters'
  discriminating power, not the profile's conformance to RFC 9111 beyond the declared text.
- Mutants are single-point edits of a faithful implementation. A survivor means "this defect is
  invisible to the frozen case set and the seeded population"; it does not mean the contract is
  wrong or the clause should be dropped.
- The C1 mirrors are built by the counter's own `mirror_tree()` fixture builder, so they share its
  notion of a compliant tree. A compliant tree written from scratch outside those builders was not
  scored, and the D1 head-of-file window (`splitlines()[:8]`) was not probed with a longer front
  matter.
- ExecReader's candidate is an untracked wave file; it was scored with `--tool`, not at a git
  revision. Its sha256 is recorded before and after this seat (`fdceef47…`, unchanged).
- The 200-case population is deterministic; every class count above is over that fixed batch.

## 7. Restoration, tooling, scope

- Writes: this directory, `.ufo/waves/round-88/w1/MutReader.md`, and scratch
  `/fast/scratch/hyaku/kake-r88/MutReader/` (one working copy per target, no clones, no git/jj
  mutation). Scratch was deleted after the receipts above were copied; no `/tmp` path is cited.
- ExecReader's candidate was copied, never edited: `fdceef474e618d6664c15333cba6a1fa136fbc44f2791bbbdbf92d234fb287d6`
  before and after.
- No production byte (`scripts/`, `corpus/`, `SKILL.md`, `LOG.md`, `SCORECARD.md`), no commit, no
  push, no fleet-repo or sibling-lane write.
- Tools installed or upgraded: **none**. Python 3.11 stdlib only; no network GETs were performed
  by this seat.

### Receipt index

| file | contents |
|---|---|
| `receipts/exec_sweep.json` / `.txt` | 2 baselines + 21 mutants × 2 counters: argv, exit, tallies, failing case ids and per-case exit/stdout/stderr |
| `receipts/exec_survivors.json` / `.txt` | population class counts, per-mutant kill attribution, 5 witness transcripts, e20 100k equivalence |
| `receipts/c1_sweep.json` / `.txt` | 1 baseline + 18 C1 mutants: mirror path, argv, exit, summary line, per-item failures |
| `receipts/c1_extra.json` / `.txt` | `c1_d2_no_arithmetic` (3-point) + second-payload transcript + D1 `.bak` existence check |
| `receipts/c2_sweep.json` / `.txt`, `receipts/c2_survivors.*` | secondary self-written reference sweep (v2 counter) — see `receipts/CORRECTION-m19.md` |
| `receipts/commands.txt` | every counter invocation with its exit |
| `mutants_exec/`, `mutants_selfref/` | mutant sources + `manifest.json` (source sha256, patch anchor and replacement per mutant) |
| `exe_vary_match.py`, `ref_vary_match.py` | the two artefacts under test (copies) |
| `c2-v2/` | v2 counter + case set materialised from `80637397` |
| `logs/` | the drivers/probes that produced the receipts |
| `mirrors/` | the 20 C1 mirror trees as scored (`green-baseline` + 18 + `c1_d2_no_arithmetic`); the `--mirror` paths inside `commands.txt` are the now-deleted scratch paths, these are the same trees |
