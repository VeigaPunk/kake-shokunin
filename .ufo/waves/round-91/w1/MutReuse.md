# MutReuse — mutation probe of the round-91 C2 tool and the C2 counter

author: MutReuse (mutation-tester seat, round 91 wave 1)
date: 2026-11-04
lane base: `f4fff130a52ae6de49af5de7d568d2ee320ebfb0` (LANE `master` at dispatch)
candidate measured: `scripts/stored_reuse.py`, sha256
`5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299` — **untracked** in LANE at
measurement (`git ls-files scripts/stored_reuse.py` printed nothing); committed byte-identically in
my fixture as `b3f3ca31ace8b68e5dbbcd9c72c85884f02fc415`
counter measured: `.ufo/waves/round-91/c91_reuse.py`, sha256
`0cd610426896fc76b4913c907d83b95d22c7a66c4ecf2da8fc4fc9ecf21ab660` (equals `freeze.md`); never edited

VERDICT: C2's **tool** holds on the measured bytes — the frozen counter reads `met=true` on them and
all 17 required single-point clause mutants are killed — but the C2 **counter's coverage is
incomplete**: 5 tool mutants survive (five clause variants no case exercises) and 9 of 10 counter
mutants survive, of which 4 admit a subject the frozen counter refuses and 4 are structural checks no
frozen subject can reach.

## Setup

Scratch root `/fast/scratch/hyaku/kake-r91/MutReuse/`, fixture `$S/fx` = one `git clone -q --shared`
of LANE, checked out detached at `f4fff130`; `git -C $S/fx rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/kake-r91/MutReuse/fx` before the first fixture commit. Every fixture commit
used `git -C $S/fx` with a local `user.name`/`user.email` set inside that fixture only. No git
mutation was run in LANE.

Counter invocation for every row (the seat's command, with the fixture as root):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-91/c91_reuse.py \
  --root /fast/scratch/hyaku/kake-r91/MutReuse/fx --revision <REV> \
  --work <WORK> --seed 91091
```

Baselines, both `met=true`, exit 0:

| base | rev | receipt |
|---|---|---|
| shipped bytes `5004657d…` | `b3f3ca31` | `receipts/shipped-M00s.txt` |
| counter's reference bytes (reachability control) | `10995409` | `receipts/tool-M00.txt` |

All 17 required mutants were applied **twice**: once to the shipped bytes (primary table below) and
once to the reference bytes, and produced the same verdict and the same failing case in both runs
(reference-base revs in `tool-revs.json`, receipts `receipts/tool-M*.txt`). Drivers are copied
verbatim: `mutate_shipped.py`, `mutate_tool.py`, `score_shipped.py`, `score_tool.py`,
`mutate_counter.py`; rev maps in `tool-revs-shipped.json`, `tool-revs.json`, `counter-mutants.json`.

## (1) Tool mutants — 22 single-point mutants of `scripts/stored_reuse.py`

Killed = the frozen counter reads `met=false`; survived = `met=true` with `hand=45/45
generated=120/120`. Every row is one textual substitution of one clause expression, committed alone
in `$S/fx`.

| # | mutation (contract clause) | rev | exit | met | detector that fired (first failing case) |
|---|---|---|---|---|---|
| M01 | clause 9: drop `s-maxage` | `3de0ce14` | 1 | false | `s-maxage-shared freshness_lifetime=10 want 100` + 6 generated |
| M02 | clause 9: use `s-maxage` when not shared | `3f0e8e96` | 1 | false | `s-maxage-ignored-private` + 8 generated |
| M03 | clause 9: `Expires` before `max-age` | `d8999394` | 1 | false | `max-age-beats-expires freshness_lifetime=120 want 60` (hand only) |
| M04 | clause 10: drop `private` | `cd7e1ca4` | 1 | false | `not-storable-private-shared` + 2 generated |
| M05 | clause 10: drop `Vary: *` | `470b74a6` | 1 | false | `not-storable-vary-star` + 2 generated |
| M06 | clause 10: drop request `no-store` | `bdfb9855` | 1 | false | `not-storable-request-no-store` + 5 generated |
| M07 | clause 16: `current_age < lifetime` as `<=` | `7d31db95` | 1 | false | `stale-boundary`, `only-if-cached-stale` + gen53 |
| M08 | clause 12: drop request `no-cache` | `b5108095` | 1 | false | `request-no-cache` (hand only) |
| M09 | clause 13: drop stored `no-cache` | `10f4a493` | 1 | false | `stored-no-cache` + gen50 |
| M10 | clause 17: drop `must-revalidate` | `cd4e0667` | 1 | false | `must-revalidate-stale` (hand only) |
| M11 | clause 17: drop `proxy-revalidate` | `0777518e` | 1 | false | `proxy-revalidate-shared` + gen22 |
| M12 | clause 18: ignore the `max-stale` argument | `0d6a4397` | 1 | false | `stale-max-stale-too-old` + 3 generated |
| M13 | clause 20: drop `only-if-cached` | `8ba02f45` | 1 | false | `only-if-cached-stale` + 5 generated |
| M14 | clause 10/21: report `current_age` on `not-storable` | `aa9dc466` | 1 | false | 7 hand + 63 generated (`hand=38/45 generated=56/120`) |
| M15 | clause 9: clamp a negative lifetime to 0 | `290f01b7` | 1 | false | `expires-negative freshness_lifetime=0 want -100` (hand only) |
| M16 | clause 4: accept a quoted delta-seconds | `d78049b9` | 1 | false | `refuse-quoted-delta expected refusal, rc=0` (hand only) |
| M17 | clause 1: accept duplicate header names | `5b665b72` | 1 | false | `refuse-duplicate-header-name expected refusal, rc=0` (hand only) |
| **M18** | clause 10: `Vary: *` only as the whole value | `291229d0` | **0** | **true** | **survived** |
| **M19** | clause 4: do not lowercase directive names | `347b0e56` | **0** | **true** | **survived** |
| **M20** | clause 2: trim SP only, not HTAB | `76e8c6c7` | **0** | **true** | **survived** |
| **M21** | clause 2: drop the NUL refusal | `7d358853` | **0** | **true** | **survived** |
| **M22** | clause 4: skip an empty directive instead of refusing | `94129e59` | **0** | **true** | **survived** |

17/22 killed, 5/22 survived. Receipts: `receipts/shipped-M01.txt` … `shipped-M17.txt`,
`receipts/x-tool-M18.txt` … `x-tool-M22.txt`.

Six of the killed mutants (M03, M08, M10, M15, M16, M17) are caught by **exactly one hand case and
zero generated cases**; the seeded population contributes nothing to them. Combined with F2 below
(a deleted hand case is invisible), each of those clauses is one silent edit away from unguarded.

## (2) Counter mutants — 10 single-point mutants of `c91_reuse.py`

Each mutant was scored twice: against the shipped tool (a correct candidate, so a sound counter must
still read `met=true`) and against each of the five frozen forgery subjects via `--candidate` (a sound
counter must read `met=false`). All five forgeries were refused by every mutant, so the forgery column
is a single summary.

| # | mutation | met vs shipped tool | forgeries refused | verdict |
|---|---|---|---|---|
| C01 | delete one hand case (`fresh-max-age`) | **true** (`hand=44/44`) | 5/5 | **survived** (verdict-level; the tally shows 44/44) |
| C02 | accept an extra output key | **true** | 5/5 | **survived** — killable by probe P1 |
| C03 | ignore the type of a value | **true** | 5/5 | **survived** — killable by probe P2 |
| C04 | skip the generated population | false (`generated=0/120`) | 5/5 | killed |
| C05 | skip one forgery subject (`neg-pin-reader`) | **true** (`4/4`) | 4/4 | **survived** (verdict-level; the tally shows 4/4) |
| C06 | stop checking the population pins | **true** | 5/5 | **survived** — liveness shown by fixture X2 |
| C07 | stop checking the anti-table | **true** | 5/5 | **survived** — liveness shown by fixture X1 |
| C08 | accept a refusal that writes stdout | **true** | 5/5 | **survived** — killable by probe P3 |
| C09 | ignore forgery run errors in `admitted` | **true** | 5/5 | **survived — provably equivalent** |
| C10 | accept any refusal stderr prefix | **true** | 5/5 | **survived** — killable by probe P4 |

Receipts: `receipts/x-counter-C01.txt` … `x-counter-C10.txt` (shipped tool) plus the
conforming-stand-in matrix in `counter-mutants.json` / the earlier run (identical verdicts).

C09 is an **equivalent mutant**: `score_subject` diverts an errored case into `errors` and never into
`hand_ok`/`gen_ok`, so `h_ok == len(cases)` already implies `not errs` — the term at
`c91_reuse.py:572` is dead.

### Killable survivors, demonstrated with crafted subjects

Four "otherwise correct" subjects were derived from the shipped bytes by one output-shape edit,
committed at `a0a8e105` under `probes/`, and scored with `--candidate`:

| probe | edit | frozen counter | mutant counter |
|---|---|---|---|
| P1-extra-key | adds a 4th key `cacheable` | `met=false`, exit 1 (`hand=9/45`) | C02 `met=true`, exit 0 |
| P2-float-values | emits ints as floats (`60.0`) | `met=false` (`hand=16/45 generated=64/120`) | C03 `met=true` |
| P3-stdout-on-refusal | writes `{}` to stdout on refusal | `met=false` (`hand=36/45`) | C08 `met=true` |
| P4-wrong-refusal-prefix | stderr `error: …` instead of `invalid_input:` | `met=false` (`hand=36/45`) | C10 `met=true` |

Receipts: `receipts/probe-pristine-P*.txt`, `receipts/probe-C0*-P*.txt`. These are the subjects the
freeze did not include: the counter **can** say no, the frozen population just never asks.

### Structural checks that are live but unreachable by any frozen subject

- X1 `c3273296`: shipped bytes plus a comment carrying the hand-case-1 digest → frozen counter
  `anti_table=hit met=false`, exit 1 (`receipts/demo-X1-digest.txt`). C07 removes that refusal and
  reads `met=true`.
- X2 `e4431f37`: `.ufo/waves/round-91/frozen/c2-population.sha256` with one digest altered →
  `population=drift met=false`, exit 1 (`receipts/demo-X2-pins-drift.txt`). C06 removes that refusal
  and reads `met=true`.
- `--generated 0`: the frozen counter on the shipped tool reads
  `hand=45/45 generated=0/0 … met=true`, exit 0; `--generated 1` reads `1/1 … met=true`
  (`receipts/demo-generated-0.txt`, `demo-generated-1.txt`). No edit to the counter is needed to
  weaken its generated population.

## Findings (each is a proposal; the frozen counter and contract were not edited)

**F1 — five missing case classes in the tool battery (M18–M22).** Each mutant is a clause variant
the contract decides and no case exercises. Proposed hand cases (all verified to be decided
identically by the counter's reference and the shipped tool, i.e. they are oracle-safe):

| mutant | clause left unguarded | proposed case | expected |
|---|---|---|---|
| M18 | clause 10: "one of its members is `*`" | `Vary: "Accept, *"` | `not-storable`, null, null |
| M19 | clause 4: "its name is lowercased (ASCII)" | stored `Cache-Control: "MAX-AGE=60"`; and `"max-age=60, MAX-AGE=30"` | `reuse`, 60, 30; refusal |
| M20 | clause 2: "trimmed of leading and trailing SP and HTAB" | stored `Cache-Control: "\tmax-age=60 \t"` | `reuse`, 60, 30 |
| M21 | clause 2: "A value containing CR, LF or NUL is a refusal" | stored `X-Note: "a\0b"` | refusal |
| M22 | clause 4: "An empty directive is a refusal" | stored `Cache-Control: "max-age=60, , no-store"` | refusal |

Root cause is the sampler: `generate()` emits only lowercase directive names, SP-only padding, bare
`*` for Vary, no NUL/LF values, and no empty directives, and the 45 hand cases hold one
representative per clause. (M21 is *not* R90-D: R90-D is the storage-key NUL question; clause 2
already decides NUL in header **values**.)

**F2 — the counter's `met` is self-referential to two arguments.** `met` requires
`hand_ok == len(cases)` and `refused == len(FORGERIES)` (`c91_reuse.py:580-581`), so deleting a hand
case (C01 → `44/44 met=true`) or a forgery (C05 → `4/4 met=true`) leaves `met=true`. `freeze.md`
states absolute "hand 45/45" and "all five frozen forgery subjects", so the counter can print a
`met` the freeze predicate does not authorise. Proposed: `HAND_CASES = 45`, `FORGERY_COUNT = 5` as
literals (or a digest of the case-name list) and exact equality in `met`.

**F3 — the anti-table hashes different bytes than the candidate sees.** `run_one` feeds
`json.dumps(inp)` (`:431`); the anti-table scans for `sha_bytes(json.dumps(inp, sort_keys=True))[:16]`
(`:559`). For hand case 1 the two serialisations are `0884022e63b1afd6` (stdin) and
`bcab8f63ae7cc1c8` (anti-table), so a lookup table keyed on the exact stdin bytes is not detected.
The seed is fixed by the freeze command (`--seed 91091` is available and deterministic), so such a
table is constructible. Proposed: hash the same payload that is fed (or both), and freeze a
stdin-keyed table subject.

**F4 — the contract does not decide a bare delta-seconds directive.** `Cache-Control: max-age` with
no argument is neither refused nor decided: the counter's reference *and* the shipped tool both raise
an uncaught `TypeError` (`int > None`), exit 1, traceback on stderr, no `invalid_input:` prefix
(reproduced directly against both files). Clause 4 only constrains "a delta-seconds argument"; the
absence of an argument is unstated. Proposed clause: "a delta-seconds directive with no argument is
a refusal", plus a hand case. This is the one input I found where the tool would be scored as a
failed refusal had a case existed.

**F5 — the five frozen forgeries are all wholesale failures.** At the shipped base they score
`hand ≤ 14/45` and `generated=0/120` (`neg-allowlist` 14, `neg-blanket-refuse` 9, the other three 0).
None probes the scoring edges, so C02/C03/C08/C10 survive despite being killable (probes P1–P4).
Proposed: freeze P1–P4 as forgery subjects alongside the five.

**F6 — `met` is a random sample unless `--seed` is passed.** The freeze's command carries no
`--seed`, so the generated population (and therefore the verdict) varies per run; the receipt prints
the seed but the predicate does not pin it. Proposed: pin `--seed 91091 --generated 120` in the
freeze command and require the counter to compare against literals (see F2, and the `--generated 0`
demonstration above).

**F7 — the receipt's headline line does not name the scored bytes.** `candidate=present` is printed
without the path or digest; `--candidate` can point anywhere and `candidate_sha256` appears only in
the second (detail) line. Proposed: print `candidate_sha256` (or its first 12 hex) in the headline.

**F8 — failure messages are not reproducible.** `run_one` reports the first differing key by
iterating `KEYS_OUT`, a `set` (`:16`, `:460`), and Python string hashing is per-process randomised.
Same revision `cd7e1ca4`, same seed, four runs:
`freshness_lifetime=60 want None`, `decision='reuse' want 'not-storable'`, `current_age=30 want
None`, `freshness_lifetime=60 want None`. Receipts are therefore not byte-reproducible even though
the verdict is. Proposed: iterate a fixed tuple in a fixed order.

**F9 — the two structural checks are belt-and-braces with no subject.** Anti-table (X1) and
population pins (X2) both force `met=false` when exercised, but no frozen subject or control does
exercise them, so C06/C07 survive. Proposed: add X1 and X2 to `controls/`.

**F10 — C09's `not errs` term is dead** (`:572`). Delete it, or accept it as an equivalent mutant.

## Honest limits

- I measured the shipped tool's **working-tree bytes** (`5004657d…`), not a committed revision: at
  measurement `git ls-files scripts/stored_reuse.py` was empty and the file was untracked, so the
  counter could not have read it from any LANE revision. If the executor lands different bytes, the
  tool table must be re-run against the landed blob (the patch table is byte-anchored and will
  `SKIP` on any clause whose source line moved).
- Only seed `91091` was used for the generated population (the seat's command). I did not sweep
  seeds; F6 is argued from the counter source, not from a seed sweep.
- The 16-input differential probe (shipped vs the counter's reference) found **no** divergence
  except the shared `TypeError` of F4, which supports "the shipped tool conforms" but is not a
  contract-conformance proof beyond the clauses I probed.
- The counter-mutant matrix against the shipped tool used `--candidate` on a committed probe path;
  the five frozen forgeries were likewise scored through `--candidate`, which is the counter's own
  supported interface.
- Scratch `/fast/scratch/hyaku/kake-r91/MutReuse/` was deleted after copying receipts; nothing under
  `/tmp` was written; no commit, stage or push was run in LANE.

## Reproduction

```
git clone -q --shared LANE $S/fx && git -C $S/fx checkout -q --detach f4fff130
git -C $S/fx config user.name "MutReuse fixture"; git -C $S/fx config user.email mutreuse@fixture.local
git -C $S/fx rev-parse --show-toplevel      # must print $S/fx
python3 -B mutate_shipped.py                # 17 clause mutants + 5 probes, each its own commit
python3 -B score_shipped.py                 # frozen counter over every rev, seed 91091
python3 -B mutate_counter.py                # 10 counter mutants, scored vs tool and 5 forgeries
```
