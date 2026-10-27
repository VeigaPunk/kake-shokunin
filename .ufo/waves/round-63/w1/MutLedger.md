# MutLedger — Round 63, seat MutLedger

**Mission:** Mutation-test `.ufo/waves/round-63/quote-class/quote-classes.json`
against the frozen C1 counter `.ufo/waves/round-63/c63_calibration.py`
(sha256 `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`).
≥5 single-field corruptions, each run on its own corrupted tree in scratch;
verdict killed/survived recorded per mutant.

## Method

- Detector executed: `python3 -B c63_calibration.py --root <clone> --revision <commit>`
  run from the scratch clone cwd; the counter script bytes were extracted via
  `git -C clone show 05b0d7f4:.../c63_calibration.py` and verified sha256
  `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` (frozen).
- Tree vehicle: `git clone --no-hardlinks` of the fleet repo into
  `/fast/scratch/hyaku/kake-r63/MutLedger/clone`, detached at measured commit
  `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; each mutation = one commit on
  top (throwaway identity `MutLedger r63 <mutledger-r63@scratch.invalid>`,
  config scoped to the clone only). `git rev-parse --show-toplevel` asserted
  equal to the clone dir before every commit.
- Baseline validation (same detector, same clone):
  - `05b0d7f4…` → `… met=true`, exit 0 (pristine; matches after-c1 receipt)
  - `13d45198…` → `… quote_correction=0 blobs_match=0 … met=false`, exit 1
    (matches base-c1 control)
- Pristine ledger blob sha256 at measured commit (from `git show`):
  `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` —
  equals the contract-frozen ledger sha.

## Mutants (single-field corruptions of the ledger S432 row / classes array)

| # | Mutation | Mutated-commit sha | Counter output (key fields) | Verdict |
|---|----------|--------------------|------------------------------|---------|
| M1 | `textSha256` first hex char `8`→`9` (`8b90d096…`→`9b90d096…`) | `f94fb6f16a173d3f6c5893ed6c2b051cb05cee82` | `blobs_match=0 derived=unevaluable quote_correction=0 met=false` exit=1 | **KILLED** |
| M2 | `matchClass` `"collapsed-only"`→`"raw-substring"` | `8cffcdf50ec05863a82d7053d487a62060c2d6ef` | `blobs_match=1 derived=collapsed-only class_match=0 quote_correction=0 met=false` exit=1 | **KILLED** |
| M3 | `quote` apostrophe normalized U+2019 `’`→`'` U+0027 | `fe763a4e5e2c7863de6c865aaac592b0dbbe1175` | `blobs_match=0 derived=unevaluable quote_correction=0 met=false` exit=1 | **KILLED** |
| M4 | `locatedRawLines` field removed entirely | `e224f0a9280b2c01bead6e1905513d6523eec3e0` | `blobs_match=1 derived=collapsed-only class_match=1 quote_correction=1 met=true` exit=0 | **SURVIVED** |
| M5 | Extra row `{id:"S999", quote:"bogus extra row", matchClass:"absent", sha256s:"00…0"}` appended to `classes` | `3740e99b93e6c74a9abbcb39489554942129fc64` | `blobs_match=1 derived=collapsed-only class_match=1 quote_correction=1 met=true` exit=0 | **SURVIVED** |

Mutated ledger file sha256s (committed blob, from `git show <M>:…json`):
- pristine `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`
- M1 `330a3c01381a523fac729272c6b37b4d56f7e4bf2feb0822005ecfa6b4a47b1d`
- M2 `47663cdf96c250dfb11a8340c6afec6151b2a72f1f63d903c86588c7a7375533`
- M3 `8873cba8ca1d76351e80b33bca8ebd14fb5c163e6966426610265f01fa33a398`
- M4 `0621656c955d505114ed31c561faee71afee843aea04479c59edb0679c205961`
- M5 `d19a8344487998d78e585bab61977176ce9c77cfc02d2e69fe5002c1ec81e98e`

## Coverage findings (survived mutants)

- **M4 — `locatedRawLines` ungated.** The counter never references the field
  (it reads `id`, `quote`, `matchClass`, `textSha256`, `rawSha256` only).
  Removing provenance line-numbers from the ledger passes `met=true`. The
  line evidence stays checkable only in `note` free-text. Coverage finding,
  not a contract breach: the counter's frozen semantics bind the four used
  fields; `locatedRawLines` is informational.
- **M5 — no strict-schema / closed-set check on `classes`.** An extra row
  with a foreign `id` (even carrying garbage shas and `absent` class) passes
  `met=true`: the counter materializes `{row["id"]: row}` and consults only
  `S432`. Additional/duplicate rows are invisible to it. Coverage finding
  likewise — nothing in the frozen predicate requires rejecting extra ids.

All three corruption axes the counter is documented to gate (blob-shas,
quote string, recorded class) are killed. The two survivors are on fields
outside the counter's re-derivation surface.

## Restoration evidence

- After each mutant commit: `git checkout --detach 05b0d7f4…` reset the
  working tree; ledger file sha256 re-verified
  `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` before
  the next mutation.
- Final restore: working-tree ledger `cmp -s` against the byte-saved pristine
  copy → byte-identical; detector re-run on `05b0d7f4…` → `met=true` exit 0.
- Fleet repo untouched: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin
  status --porcelain -- <ledger> <counter>` → 0 lines; fleet working-tree
  shas still frozen (`5f48e26b…`, `bcd16f68…`). All mutations lived only in
  the scratch clone (deleted afterward per lane bounds).

## Commands (exact, cwd = fleet root unless noted)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin \
  /fast/scratch/hyaku/kake-r63/MutLedger/clone
git -C clone checkout --detach -q 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
git -C clone show 05b0d7f4:…/c63_calibration.py > c63_calibration.py   # sha bcd16f68…
python3 -B c63_calibration.py --root . --revision 05b0d7f4…           # met=true  exit 0
python3 -B c63_calibration.py --root . --revision 13d4519…           # met=false exit 1
# per mutant: edit ledger → git add -A && git commit →
python3 -B c63_calibration.py --root . --revision <M-sha>            # verdicts above
git checkout --detach -q 05b0d7f4…   # restore, sha re-verified each round
rm -rf /fast/scratch/hyaku/kake-r63/MutLedger
```

## Tooling

No installs performed. `python3 -B` used to keep `__pycache__` out of the
scratch clone. No files written outside my own scratch dir and this report.
Scratch `/fast/scratch/hyaku/kake-r63/MutLedger/` deleted after evidence
capture.
