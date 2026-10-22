# MutCounterV2 — mutation test of the C2 counter version 2 checks

Target: `.ufo/waves/round-35/sealed_count.py` (counter v2, sha256 `1b4d9d59…469b`, lane tip
`7deacc4629c1d05a34fb919d8095e99efc7b712f`). Axis: freshness (C2). Sandbox:
`/fast/scratch/hyaku/kake-r35/w2/MutCounterV2/clone`.

## Method

Built 8 single-point mutants of the counter, ran every mutant and the pristine counter over the 9
retained C2 controls with the revealed key (`sealed/c2-probes.json`, sha256 `111bceea…8d61d`,
matches the pin), and compared each measurement against the recorded receipt
`verification/control-v2-c2-<name>.json`. Baseline is sound: the pristine counter reproduces every
recorded receipt field exactly, so the detector is the receipt, not my judgement. A mutant is KILLED
when its measurement on a control differs from that receipt.

    git clone -q <lane> .../clone                                            # exit 0
    git -C .../clone checkout -q 7deacc4629c1d05a34fb919d8095e99efc7b712f   # exit 0
    git -C .../clone fetch <lane>/.ufo/waves/round-35/retained/*.bundle       # exit 0 (5 control + 2 critic heads)
    git -C .../clone fetch <lane>/.ufo/waves/round-34/retained/r34-c2-hollow-0cce15f0.bundle  # exit 0 (0cce15f0)
    python3 gen_mutants.py clone/.ufo/waves/round-35/sealed_count.py mutants  # exit 0, 8 files
    python3 score.py clone/.ufo/waves/round-35/sealed_count.py mutants/*.py # exit 0
    python3 build_attacks.py ; build_attacks2.py ; build_attacks3.py       # exit 0 each
    python3 score_attacks.py clone/.../sealed_count.py mutants/*.py         # exit 0

## Mutant table

| # | Mutant | Change (counter line) | Killed by retained control | Verdict-level kill | Harmful |
|---|---|---|---|---|---|
| m1 | no-comment-stripping | `clean()` keeps HTML comments (`:202`) | `critic-dilute-comment` | yes | no |
| m2 | no-cf-stripping | `clean()` keeps format chars (`:199`) | `critic-zwsp-hiddenrows` | yes | no |
| m3 | size-whitespace-words | `size` uses `text.split()` not `[a-z0-9]+` (`:243`) | 6 controls, only via the informational `words` field | **no** | **yes** |
| m4 | second-registry-allowed | later `## Registry` sections count (`:219`) | none | **no** | **yes** |
| m5 | tilde-fences-ignored | `~~~` fences not detected (`:210`) | none | **no** | **yes** |
| m6 | receipt-url-check-removed | receipt URL not required in source cell (`:269`) | `critic-dilute-comment`, `junk`, `keyword`, `transcript` | yes | no |
| m7 | used-by-check-removed | used-by cell need not name the entry (`:269`) | none | **no** | **yes** |
| m8 | copied-threshold-0.5 | `C2_MAX_COPIED` 0.25 → 0.5 (`:66`) | none | **no** | **yes** |

**Survivors (no retained control kills them at verdict level): m3, m4, m5, m7, m8.** Under m4, m5,
m7, m8 all nine recorded receipts are byte-identical; under m3 only the `words` field moves.

## The survivors are harmful: each admits an entry the pristine counter rejects

Attack revisions built in the sandbox clone, each branching independently from the real build
`95abec21` and breaking exactly one condition. Pristine exit 1 (rejected) in every row.

| Attack | Revision | Pristine fails | Mutant that accepts it (exit 0, `met` true) |
|---|---|---|---|
| atk-usedby — qualifying rows no longer name the entry in used-by | `a5d36930` | `cites` | m7 |
| atk-secondreg2 — qualifying rows moved to a second `## Registry` section | `2578acf3` | `cites` | m4 |
| atk-tildefence2 — qualifying rows hidden in a `~~~` fence | `da6ee67d` | `cites` | m5 |
| atk-copied — entry padded with 600 verbatim S078 words (shingle share 0.2986) | `c4377ae3` | `copied` | m8 |
| atk-sizepad — entry padded with 500 hyphenated tokens (2388 `[a-z0-9]+` runs, 1798 whitespace words) | `4089b401` | `size` | m3 |

Every mutant still measures the declared target `95abec21` as `met` true, exit 0, identical to
pristine (words 1388, copiedShare 0.0, 12/12 probes). So none of this is a false alarm on the build.

## Findings

1. **The retained C2 control set does not hold four of the counter's conditions at verdict level.**
   A counter that drops the used-by check, the first-Registry-section rule or the tilde-fence rule,
   or that doubles the copied threshold to 0.5, passes all nine recorded controls unchanged, and each
   such counter accepts a hollow entry (a registration or a transcription the pristine counter
   rejects). This is a coverage finding about the controls, not a licence to change the contract:
   the contract is the counter as declared at `81d9fd74`/`bd14096a`.
2. **The `size` word-counting rule is unpinned.** m3 changes `[a-z0-9]+` runs to whitespace words
   and no control's `met`/`conditions` move; an entry with 2388 counted words passes m3 and fails the
   pristine 2200-run cap. The declared claim says "≤ 1500 words" (SCORECARD round-35 C2 row) while
   counter v2 uses 2200 `[a-z0-9]+` runs, and the landed entry's own `counter:` line still says
   "≤ 1500 words" — wording the counter does not implement. The controls do not decide which count
   is intended.
3. The two conditions the controls *do* pin at verdict level (comment/Cf stripping, receipt-URL
   match) rest on one control each, so the set is thin.

## Restoration, scope, limits

- Lane file untouched: `sha256sum .ufo/waves/round-35/sealed_count.py` = `1b4d9d59…469b` before
  and after; `git status --short .ufo/waves/round-35/sealed_count.py` empty; the clone's copy is
  byte-identical. Mutants exist only under the seat sandbox `…/MutCounterV2/mutants/`.
- Mutant sha256: m1 `8b034462…c41e5a`, m2 `a38dacfd…bb8044`, m3 `27b12ac6…37cbe3`, m4 `690e2f52…c995f56`,
  m5 `5fd537aa…1c987941`, m6 `ec1f4709…6265a7b9`, m7 `70a4422b…5f4866`, m8 `5d5b7423…62d6153`.
- Evidence: `/fast/scratch/hyaku/kake-r35/w2/MutCounterV2/results/{raw,table,attacks,summary}.json`
  and scripts `gen_mutants.py`, `score.py`, `build_attacks{,2,3}.py`, `score_attacks.py` beside them.
- No live request to any host; no lane property contacted; no tool installed.
- Not verified: the C1 path was not mutated; probe regex leniency, the `clean()` NFKC step,
  `split_row` escaped-pipe handling and the pinned text hashes against a swapped source directory
  were not tested. The attack revisions are my constructions: they show the mutants are exploitable
  in principle, not that an author would commit them. Whether the four uncovered rules remain
  wanted is the L1's call; a coverage finding only says the retained controls do not hold them.
