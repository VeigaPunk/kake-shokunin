# ReviewerFalseGreenDead — round-63 C1 fabricated-evidence false-green

Seat goal: construct ANY git tree on which `c63_calibration.py` prints
`met=true` while the S432 disagreement is semantically unresolved (no genuine
retained blobs, no honest correction). Success ⇒ C1 dead per the contract kill
rule.

**Verdict: ATTACK SUCCEEDED — C1 is unprovable.** Three independent trees print
`met=true` (exit 0), including one in which every S432 evidence byte is
fabricated: the "retained" `S432.html` is git's canonical **empty blob**
(`e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, 0 bytes), the "flat-text
rendering" is 192 hand-typed bytes, and the ledger records the fabricated
shas. The counter calls this `blobs_match=1 derived=collapsed-only
class_match=1 unresolved=0 met=true`.

## Root cause — the "semantic binding" is self-referential, not frozen

`.ufo/waves/round-63/c63_calibration.py` (frozen sha256
`bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`, verified)
lines 107–145: `blobs_match` compares `sha256(raw_blob)`/`sha256(text_blob)`
against `rawSha256`/`textSha256` **in the ledger committed in the same tree at
the same revision**. The contract pins the ledger sha256 (`5f48e26b…010c42d`)
and both blob sha256s in prose only; the counter source contains none of them
(`grep -E '5f48e26b|8b90d096|63b0a018' c63_calibration.py` → no hits). The only
hard pins are `PATHS`, `FROZEN_QUOTE` (lines 44–55) and the string
`collapsed-only` at line 142.

Consequences, all confirmed by execution:

1. **Intra-tree sha consistency ≠ provenance.** Any fabricated
   (raw, text, ledger) triple that is mutually sha-consistent and satisfies
   `quote ∈ text`, `quote ∉ raw` yields `blobs_match=1 class_match=1`.
2. **The raw→text derivation is never checked.** `classify()` (lines 59–67)
   runs two substring tests only; `extract_text.py` need not exist and the
   text blob need not render the raw blob (fixture B).
3. **The "correction" gate is the routed c62 defect, relocated.** Lines
   121–125 require three literal substrings (`[r63-correction`, FROZEN_QUOTE,
   LEDGER_REL) — the block may assert anything, including the falsified
   round-62 claim verbatim (fixtures A and C do).
4. **`disagreements` is display-only.** When `resolved=1`, line 165 forces
   `unresolved=0`; the counter prints `met=true` while itself counting
   `disagreements=1`.
5. **No ancestry check.** `git rev-parse --verify` (lines 87–91) accepts any
   resolvable rev; nothing requires descent from BASE `13d45198…`.

## Fixture A — fabricated evidence package (zero genuine bytes)

Driver: `/fast/scratch/hyaku/kake-r63/ReviewerFalseGreenDead/make_fixtures.py`
(loads `FROZEN_QUOTE` from the counter module itself for byte-exactness).
Tree `0268c05052f80308d527be06390a3952b7667f62` (`git init -q`, throwaway
`-c user.name/-c user.email` identity, `rev-parse --show-toplevel` verified):

```
$ git ls-tree -r -l HEAD
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391   0  .ufo/waves/round-61/sources/S432.html
100644 blob a5bd355064d4ce3fa2c5ba23981cbe18184b98d5 192  .ufo/waves/round-63/quote-class/S432.txt
100644 blob 62ade4eb5f6e730b44844d37e1c26457b3629585 826  .ufo/waves/round-63/quote-class/quote-classes.json
100644 blob ff09a0d211f9f926efda421b51ccc8254417d018 242  corpus/QUALITY.md
100644 blob c5893b53a9f7d6f680fb32ac44a4f98c87055bc6 108  corpus/SOURCES.md
100644 blob e62e9d1eeee1dd65bbc9ea731eb0c84b76c0b320 487  corpus/knowledge/response-header-expectations.md
100644 blob a5120a6923d11c4fb735c58669834b5e3e0a2bd2 232  corpus/lessons/round-61-verifier-spotcheck.md
100644 blob 6c3a0c38b11df849a8f0775e0d45e37dc8ae110d 208  corpus/lessons/round-63.md
```

- `S432.html` = 0 bytes (the disagreement's raw source does not exist).
- `S432.txt` = `Fabricated flat text, no provenance: <FROZEN_QUOTE>\n` —
  sha256 `65477b8c96a1f5a2a409da191e8070aed2f0b1d0e2facfe88aa44aab4a05bae2`.
- Ledger `rawSha256` = `e3b0c442…b855` (empty-input sha256), `textSha256` =
  `65477b8c…bae2`, `quote` = FROZEN_QUOTE, `matchClass` = `collapsed-only`,
  `recipe` = `"fabricated — no extraction performed"`.
- Knowledge `[r63-correction]` block quotes the span, cites the ledger path,
  and asserts (dishonestly — disproved by the tree's own 0-byte raw blob) that
  the span *is a literal substring of the retained S432.html*.
- Spotcheck retains a `| S432 | … | Disagree — … |` row ⇒ `disagreements=1`.

Run:

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py \
    --root /fast/scratch/hyaku/kake-r63/ReviewerFalseGreenDead/fixture-a-fabricated --revision HEAD
revision=0268c05052f80308d527be06390a3952b7667f62 disagreements=1 quote_correction=1 \
blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 \
source_row=1 unresolved=0 met=true
exit=0
```

## Fixture B — genuine raw blob + fabricated "rendering"

Real `.ufo/waves/round-61/sources/S432.html` copied byte-exact from the
measured commit (sha256 `63b0a018…bad911b`, 1,854,393 bytes) + fabricated
193-byte `S432.txt` (`Not derived from the raw blob at all: <FROZEN_QUOTE>`) +
ledger recording (real raw sha, fake text sha). Tree
`87982aafae22208d84c7e3aba180d3fbffa385a6`:

```
… quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true
exit=0
```

Proves the derivation relationship (the entire substance of `collapsed-only`)
is unverified.

## Fixture C — genuine evidence + dishonest correction

All real blobs and the **real** ledger (`5f48e26b…010c42d`) copied byte-exact;
only the corpus files are fabricated, and the `[r63-correction]` block asserts
the round-62 falsified claim verbatim ("the span is a literal substring of the
retained S432.html; the outside Disagree was therefore wrong and is
dismissed"). Tree `8ce73fa17181ba2217c1a32a2b94b6bd053c593e`:

```
… quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true
exit=0
```

Proves `quote_correction=1` carries no honesty guarantee: it passes while the
recorded correction asserts the opposite of the evidence the ledger encodes.

## What a real repair needs (recommendation, not applied)

- Pin the ledger sha256 and both blob sha256s as constants in the counter
  (as the contract pins the counter's own sha), not intra-tree lookups.
- Re-execute the `extract_text.py` recipe against the raw blob and compare
  bytes, or pin the text blob's provenance independently of the ledger.
- Gate on `disagreements`/`unresolved` instead of masking them when
  `resolved=1`, and verify the correction's asserted claim rather than its
  marker strings.
- Require `--revision` to be a descendant of BASE (`git merge-base --is-ancestor`).

## Housekeeping

- Commands: `git init/commit` (scratch only, throwaway identity), `git
  ls-tree/cat-file/show/rev-parse` (read-only), `python3`, `sha256sum`,
  `grep`. No fleet mutation except this report; no installs (system
  python3 3.14.8 / git 2.56.0 sufficed).
- Fixture repos deleted after evidence capture; the recipe is fully
  reproducible from `make_fixtures.py` retained in the seat scratch dir.
