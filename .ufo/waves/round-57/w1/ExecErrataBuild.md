# ExecErrataBuild

Claim C1 (calibration). Built the candidate `receipt-errata.json` for
`.ufo/waves/round-57/c57_receipt_pins.py`, derived all six entries from full-hash first-parent history at base
`28fa0b23e699303725aba2727094531f5e44494d` (never from the counter's 12-char prefixes), and proved the file against
the counter in a throwaway clone. Deliverable:
`.ufo/waves/round-57/w1/ExecErrataBuild.files/receipt-errata.json`.

## ENTRIES:

Six relabels, each with exactly two committed versions of the path (oldest = introduction, later = relabel). No
other population path relabelled (`relabels_in_history=6` at base). `from` is the revision line the receipt was
first committed with; `to` is the label the later commit wrote; in all six cases `to` equals the commit that
introduced the receipt itself.

| path | from | to | commit | subject of `commit` |
|---|---|---|---|---|
| .ufo/waves/round-52/control/c1-ledger-real.txt | 3a50ae4321e64856229c7cd0d39d3557b204d489 | 1ae8de5d4dee8300624b0db2a94497ff905942c5 | a4a890cf1381a194891689dcbba0bf524350926b | round 52: measured receipts, drift reconciliation, scorecard and province |
| .ufo/waves/round-52/control/c2-quote-real.txt | 3a50ae4321e64856229c7cd0d39d3557b204d489 | 1ae8de5d4dee8300624b0db2a94497ff905942c5 | a4a890cf1381a194891689dcbba0bf524350926b | round 52: measured receipts, drift reconciliation, scorecard and province |
| .ufo/waves/round-55/controls/after-c1-readme-index.txt | faf9abe81d1ef5925733f756a918527483073fe8 | 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 | 955e3d7bd6d1eff5060e4cebbed51891bb53027a | round-55: measurement receipts, settlement, SCORECARD and LOG |
| .ufo/waves/round-55/controls/after-c2-quote-truth.txt | faf9abe81d1ef5925733f756a918527483073fe8 | 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 | 955e3d7bd6d1eff5060e4cebbed51891bb53027a | round-55: measurement receipts, settlement, SCORECARD and LOG |
| .ufo/waves/round-56/controls/after-c1-selftally.txt | f8438a282d5946b386812d784cc617edcbc9201d | 4cb225fb032b04166fb0232bc98a7bcce72675ec | ad06cb8a17bda28f0691b95aecda13cd4708ea6c | round-56: measurement receipts, SCORECARD and LOG revision pins |
| .ufo/waves/round-56/controls/after-c2-quote-truth.txt | f8438a282d5946b386812d784cc617edcbc9201d | 4cb225fb032b04166fb0232bc98a7bcce72675ec | ad06cb8a17bda28f0691b95aecda13cd4708ea6c | round-56: measurement receipts, SCORECARD and LOG revision pins |

Derivation (run in the lane, read-only):

```
git -C . log --first-parent --format=%H -- <path>        # 2 commits per path, newest first
git -C . show <commit>:<path> | grep -E '^[[:space:]]*revision[[:space:]]*[:=]'
```

Per-path version evidence (oldest version -> later version, revision line of each; subjects in the table above):

```
52/c1-ledger-real.txt        1ae8de5d..(rev 3a50ae43..)  ->  a4a890cf..(rev 1ae8de5d..)   [introducing: 1ae8de5d, frozen baselines]
52/c2-quote-real.txt         1ae8de5d..(rev 3a50ae43..)  ->  a4a890cf..(rev 1ae8de5d..)
55/after-c1-readme-index.txt 64c0ce12..(rev faf9abe8..)  ->  955e3d7b..(rev 64c0ce12..)   [introducing: 64c0ce12, content revision]
55/after-c2-quote-truth.txt  64c0ce12..(rev faf9abe8..)  ->  955e3d7b..(rev 64c0ce12..)
56/after-c1-selftally.txt    4cb225fb..(rev f8438a28..)  ->  ad06cb8a..(rev 4cb225fb..)   [introducing: 4cb225fb, C2 selftest 86 checks]
56/after-c2-quote-truth.txt  4cb225fb..(rev f8438a28..)  ->  ad06cb8a..(rev 4cb225fb..)
```

## ERRATA JSON:

Verbatim `.ufo/waves/round-57/w1/ExecErrataBuild.files/receipt-errata.json` (4317 bytes; each `from`/`to`/`commit`
is full 40-hex, verified programmatically):

```json
{
  "schema": "kake-r57-receipt-errata-v1",
  "note": "Six historical relabels (rounds 52, 55, 56) derived from first-parent history at 28fa0b23e699303725aba2727094531f5e44494d. Every entry names the revision the receipt was first committed with (from) and the later label (to) written by the commit in `commit`.",
  "entries": [
    {
      "path": ".ufo/waves/round-52/control/c1-ledger-real.txt",
      "from": "3a50ae4321e64856229c7cd0d39d3557b204d489",
      "to": "1ae8de5d4dee8300624b0db2a94497ff905942c5",
      "commit": "a4a890cf1381a194891689dcbba0bf524350926b",
      "note": "First committed in 1ae8de5d4dee8300624b0db2a94497ff905942c5 claiming to have run over 3a50ae4321e64856229c7cd0d39d3557b204d489 (the round-52 frozen baseline); a4a890cf1381a194891689dcbba0bf524350926b ('round 52: measured receipts, drift reconciliation, scorecard and province') rewrote the revision line to 1ae8de5d4dee8300624b0db2a94497ff905942c5, the commit that introduced the receipt itself."
    },
    {
      "path": ".ufo/waves/round-52/control/c2-quote-real.txt",
      "from": "3a50ae4321e64856229c7cd0d39d3557b204d489",
      "to": "1ae8de5d4dee8300624b0db2a94497ff905942c5",
      "commit": "a4a890cf1381a194891689dcbba0bf524350926b",
      "note": "First committed in 1ae8de5d4dee8300624b0db2a94497ff905942c5 claiming to have run over 3a50ae4321e64856229c7cd0d39d3557b204d489 (the round-52 frozen baseline); a4a890cf1381a194891689dcbba0bf524350926b ('round 52: measured receipts, drift reconciliation, scorecard and province') rewrote the revision line to 1ae8de5d4dee8300624b0db2a94497ff905942c5, the commit that introduced the receipt itself."
    },
    {
      "path": ".ufo/waves/round-55/controls/after-c1-readme-index.txt",
      "from": "faf9abe81d1ef5925733f756a918527483073fe8",
      "to": "64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6",
      "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a",
      "note": "First committed in 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 claiming to have run over faf9abe81d1ef5925733f756a918527483073fe8 (the round-55 content revision); 955e3d7bd6d1eff5060e4cebbed51891bb53027a ('round-55: measurement receipts, settlement, SCORECARD and LOG') rewrote the revision line to 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6, the commit that introduced the receipt itself."
    },
    {
      "path": ".ufo/waves/round-55/controls/after-c2-quote-truth.txt",
      "from": "faf9abe81d1ef5925733f756a918527483073fe8",
      "to": "64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6",
      "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a",
      "note": "First committed in 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 claiming to have run over faf9abe81d1ef5925733f756a918527483073fe8 (the round-55 content revision); 955e3d7bd6d1eff5060e4cebbed51891bb53027a ('round-55: measurement receipts, settlement, SCORECARD and LOG') rewrote the revision line to 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6, the commit that introduced the receipt itself."
    },
    {
      "path": ".ufo/waves/round-56/controls/after-c1-selftally.txt",
      "from": "f8438a282d5946b386812d784cc617edcbc9201d",
      "to": "4cb225fb032b04166fb0232bc98a7bcce72675ec",
      "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c",
      "note": "First committed in 4cb225fb032b04166fb0232bc98a7bcce72675ec claiming to have run over f8438a282d5946b386812d784cc617edcbc9201d (the round-56 C2 selftest/lesson commit); ad06cb8a17bda28f0691b95aecda13cd4708ea6c ('round-56: measurement receipts, SCORECARD and LOG revision pins') rewrote the revision line to 4cb225fb032b04166fb0232bc98a7bcce72675ec, the commit that introduced the receipt itself."
    },
    {
      "path": ".ufo/waves/round-56/controls/after-c2-quote-truth.txt",
      "from": "f8438a282d5946b386812d784cc617edcbc9201d",
      "to": "4cb225fb032b04166fb0232bc98a7bcce72675ec",
      "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c",
      "note": "First committed in 4cb225fb032b04166fb0232bc98a7bcce72675ec claiming to have run over f8438a282d5946b386812d784cc617edcbc9201d (the round-56 C2 selftest/lesson commit); ad06cb8a17bda28f0691b95aecda13cd4708ea6c ('round-56: measurement receipts, SCORECARD and LOG revision pins') rewrote the revision line to 4cb225fb032b04166fb0232bc98a7bcce72675ec, the commit that introduced the receipt itself."
    }
  ]
}
```

## PROOF RUN:

Baseline (lane at base, before errata) — 6 UNDISCLOSED, exit 1:

```
C1 receipt-pins undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False
  population=45 relabels_in_history=6
  UNDISCLOSED .ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
  UNDISCLOSED .ufo/waves/round-52/control/c2-quote-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
  UNDISCLOSED .ufo/waves/round-55/controls/after-c1-readme-index.txt faf9abe81d1e -> 64c0ce12ffe3 at 955e3d7bd6d1
  UNDISCLOSED .ufo/waves/round-55/controls/after-c2-quote-truth.txt faf9abe81d1e -> 64c0ce12ffe3 at 955e3d7bd6d1
  UNDISCLOSED .ufo/waves/round-56/controls/after-c1-selftally.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
  UNDISCLOSED .ufo/waves/round-56/controls/after-c2-quote-truth.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
  revision: 28fa0b23e699303725aba2727094531f5e44494d
EXIT=1
```

Scratch clone at base + errata committed at `.ufo/waves/round-57/receipt-errata.json`:

```
D=/tmp/r57errata.0lbMcc
TOP=/tmp/r57errata.0lbMcc
COMMIT=3c5baad8fceb228ede2a8ec3a9e6deea0cf25a39
C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False
  population=45 relabels_in_history=6
  revision: 3c5baad8fceb228ede2a8ec3a9e6deea0cf25a39
EXIT=1
```

`undisclosed_relabels=0 phantom_errata=0` with `relabels_in_history=6` — all six relabels disclosed, no phantom.
`met=False` / exit 1 only because the round-57 conditions are untouched in this fixture (`new_receipts=0`,
`scorecard_pin=0`); those are outside this seat. `cmp` confirmed the committed blob is byte-identical to the
deliverable.

## CORRUPTION RUN:

Same clone, one entry's `to` rewritten `1ae8de5d4dee8300624b0db2a94497ff905942c5` -> `28fa0b23e699303725aba2727094531f5e44494d`
for `.ufo/waves/round-52/control/c1-ledger-real.txt`, committed as `f874019e0fb546e7e2dec771bc50704d43779662`:

```
C1 receipt-pins undisclosed_relabels=1 phantom_errata=1 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False
  population=45 relabels_in_history=6
  UNDISCLOSED .ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
  PHANTOM .ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 28fa0b23e699 at a4a890cf1381
  revision: f874019e0fb546e7e2dec771bc50704d43779662
EXIT=1
```

Both counters move exactly to 1, so the pair is sensitive in both directions: a missing disclosure shows as
UNDISCLOSED, an invented one as PHANTOM, and the clean six-entry file clears both.

Scope/state: only `.ufo/waves/round-57/w1/ExecErrataBuild.files/receipt-errata.json` and this report were written in
the lane; no git/jj mutation, no commit, no pacman, no tool installs, no subagent dispatch. Scratch clone left at
`/tmp/r57errata.0lbMcc` (throwaway, identity `selftest`).

VERDICT: Six full-hash relabel entries built and proven — clean run `undisclosed_relabels=0 phantom_errata=0` (6 relabels in history), corrupted `to` run `1/1`; C1's remaining failures are the untouched round-57 conditions (`new_receipts=0`, `scorecard_pin=0`), not the errata.
