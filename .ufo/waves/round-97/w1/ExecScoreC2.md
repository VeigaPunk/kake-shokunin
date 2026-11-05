# ExecScoreC2 — C2 scored at the lane tip with the frozen successor counter; slot controls reproduced independently

Seat: ExecScoreC2 (kake round 97, wave 1). Scope: score C2 on the current lane tip
with the frozen successor counter, reproduce the C2 pre-freeze slot controls, run the
selftest. All work in my scratch `/fast/scratch/hyaku/kake-r97/ExecScoreC2/` (removed
before yield) with one `git clone --shared` of LANE; deliverables in
`.ufo/waves/round-97/w1/ExecScoreC2/`. No lane bytes written; no mutating git outside
my clone; no tools installed (python3 + /usr/bin/git only, both preexisting).

## 1. Frozen digest verification — PASS

`sha256sum` over the lane tree vs `.ufo/waves/round-97/controls/instrument-sha256.txt`
and the assignment's frozen values:

| file | observed | frozen | verdict |
|---|---|---|---|
| `.ufo/waves/round-97/c97_index.py` | `8535150e91bd610bd42186b3ad8be23477b0386a1f8d14b95aba8375788aa008` | same | match |
| `.ufo/waves/round-97/c97_reval.py` | `f3895a32464ffe88d08cfeae5cd4ace1d4b1df6a472871c19c96131164e39266` | same | match |
| `.ufo/waves/round-97/frozen/neg-lookup-table.py` | `898df9a2ce5ea7713d3d5c33ada13250a667c490eccbaf642556295ca9c460cc` | same | match |

No mismatch: no finding, no repair made. Lane tip confirmed
`git -C LANE rev-parse master` → `9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (the
stated C1 repair commit).

## 2. C2 scored at the tip — met=true, exit 0

Command (`score-tip.txt` line 1): `python3 -B .ufo/waves/round-97/c97_reval.py --root
<clone> --revision 9e27ce0b2a8d168e032ab79ea11471b36eaceedf --work <scratch>/w`,
`TMPDIR=<scratch>`, run from the clone cwd; single shared clone verified
`git rev-parse --show-toplevel` = clone dir, detached at the tip.

- Line 1: `C2v97 revision=9e27ce0b2a8d168e032ab79ea11471b36eaceedf candidate=present hand=37/37 generated=104/104 heldout=56/56 forgeries_refused=7/7 positive=admitted mutants=14/14 survivors=none anti_table=ok population=ok seed=97 met=true`
- Line 2: JSON detail — `anti_hits: []`, all 7 forgeries `refused_ok: true`, all 14 mutants `killed: true`, `pins: 9`, `hand_failures: []`.
- rc: `exit=0`.
- Scored candidate blob:
  `git -C <clone> show 9e27ce0b…:scripts/reval_exchange.py | sha256sum` →
  `192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212` — equals the
  landed candidate digest named in the freeze. Both predicate conjuncts hold.

## 3. Slot controls re-run independently — 4/4 reproduced

Each slot is a fixture commit in my clone built exactly per the committed
`controls.sh` recipe: detached on the instruments revision `a2208ac7…`, slot subject
copied over (or candidate deleted), committed with my seat identity via `-c` flags,
then scored through the public CLI. Comparisons in `compare.md`; per-field result:
every field matches the committed `ctl-c2-slot-*.txt` receipts except the two declared
expected differences — the revision id (new commits) and the held-out case totals
(candidate-present slots: `52/52→58/58`, `22/57→22/52`, `0/55→0/52`; the held-out
population is seeded from `int(revision[:15],16)`, so a new commit id redraws the
case set; pass/fail structure identical). Hand and generated totals match exactly
everywhere, including `20/37` on oracle and the full `0/37 0/120 0/60` absent line.

| slot | subject | line-1 met | exit | reproduced |
|---|---|---|---|---|
| pos | `.ufo/waves/round-96/frozen/pos-good-reval.py` | true | 0 | yes |
| table | `.ufo/waves/round-97/frozen/neg-lookup-table.py` | false (heldout) | 1 | yes |
| oracle | `.ufo/waves/round-96/frozen/neg-oracle-import.py` | false (hand/generated/heldout) | 1 | yes |
| absent | candidate deleted | false (`candidate=absent`) | 1 | yes |

## 4. Selftest — PASS

`python3 -B .ufo/waves/round-97/c97_reval.py --selftest --work <scratch>/sel` →
`selftest 8/8 fixtures scored as declared; mutants killed 14/14 survivors=none;
anti_table=ok; generated-vs-reference seeded cases=33`, `exit=0` — byte-equal in
content to `controls/ctl-c2-selftest.txt`. (`selftest.txt`)

## Findings

- None against the instruments: digests matched before and after all runs; every
  receipt line reproduced within the declared expected differences; fail-closed
  behavior confirmed on all three forgeries and the absent slot.
- Routed (already self-reported by the owning seat): ConnectorScope-23 ran
  `rm -rf /fast/scratch/hyaku/kake-r97` deleting sibling scratch trees mid-wave; my
  first slots attempt died as four `checkout-fail` shells. I re-derived the clone and
  all fixtures from the frozen recipe; the receipts here are the clean re-derivation.
  No frozen byte was touched (digest table above re-verified post-incident: same
  three hashes).

## Deliverables

`score-tip.txt`, `slot-pos.txt`, `slot-table.txt`, `slot-oracle.txt`,
`slot-absent.txt`, `selftest.txt`, `compare.md`, this report — all in
`.ufo/waves/round-97/w1/ExecScoreC2/`. Scratch tree deleted before yield.
