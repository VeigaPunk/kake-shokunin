# RevengerRelabelOrigin

Method: history read with read-only git (`show`, `log`, `rev-list`, `rev-parse`) at lane objects; no counter run. Line-number citations for
`.ufo/waves/round-57/{contract.md,c57_receipt_pins.py,receipt-errata.json}`, `SKILL.md`, `corpus/QUALITY.md`, `LOG.md`, `SCORECARD.md` are the
build revision **4b8c73050470ada9e6583f3b12d659d1bed6a17f**; `git diff --stat 4b8c73050470..HEAD -- <those paths>` is empty (confirmed by running),
so the same lines hold at lane HEAD `51921b9`.

## RECONSTRUCTION

The six relabels are one shape repeated three times. For each receipt: it is **introduced in C**, pinned to **C's parent P**; **C+1** rewrites the
pin to **C** itself, and `git rev-list --count C..C+1` is 1 in all three rounds (confirmed by running `git log --format=%h -- <path>` +
`git show <c>:<path> | grep 'revision[:=]'` + `git rev-parse --short <C>^`).

| Round | Receipt (path) | intro C | first pin = C^ | rewritten at C+1 | new pin = C |
|---|---|---|---|---|---|
| 52 | `.ufo/waves/round-52/control/c1-ledger-real.txt:5` | `1ae8de5` | `3a50ae4` | `a4a890c` | `1ae8de5` |
| 52 | `.ufo/waves/round-52/control/c2-quote-real.txt:10` | `1ae8de5` | `3a50ae4` | `a4a890c` | `1ae8de5` |
| 55 | `.ufo/waves/round-55/controls/after-c1-readme-index.txt:3` | `64c0ce1` | `faf9abe` | `955e3d7` | `64c0ce1` |
| 55 | `.ufo/waves/round-55/controls/after-c2-quote-truth.txt:10` | `64c0ce1` | `faf9abe` | `955e3d7` | `64c0ce1` |
| 56 | `.ufo/waves/round-56/controls/after-c1-selftally.txt:12` | `4cb225f` | `f8438a2` | `ad06cb8` | `4cb225f` |
| 56 | `.ufo/waves/round-56/controls/after-c2-quote-truth.txt:10` | `4cb225f` | `f8438a2` | `ad06cb8` | `4cb225f` |

This matches the six entries in `.ufo/waves/round-57/receipt-errata.json` (read; independently re-derived above from git).

### Round 52 — `3a50ae4` → `1ae8de5` (receipts) → `a4a890c` (relabel), report `a1d83ec`

- Messages: `1ae8de5` "round 52: frozen baselines and the seven measurement receipts"; `a4a890c` "round 52: measured receipts, drift
  reconciliation, scorecard and province" — and its body says verbatim "C1/C2 receipts **re-run at 1ae8de5**; baselines re-frozen to the
  committed receipt digests" (confirmed by running `git show --format=%B a4a890c`).
- Want: one hash that is both the run and the landing. But `a4a890c` also changed `.ufo/waves/round-52/control/c2-quote-selftest.txt`
  (`3a50ae4`→`1ae8de5`, count unchanged 18/18), added `c1-registry{,-selftest}.txt` pinned `1ae8de5`, and re-froze
  `.ufo/waves/round-52/baselines.json` (c2-quote-selftest sha256 `60d9056c…`→`d7cd5390…`) in the same commit (confirmed by running
  `git show a4a890c -- .ufo/waves/round-52/`).
- Rewrite step: the pin moved from the measured parent onto the receipt-carrying commit. The round's own gate could not see it: it compares
  receipt blobs only against the pin co-committed with them (`.ufo/waves/round-52/c52_gate_registry.py:163-169`), so digest and artifact moved
  together.
- What did not converge: the SCORECARD and both receipts say `1ae8de5` (confirmed by running `git show a4a890:SCORECARD.md` → "Measured
  revision `1ae8de5d4dee…`"), while the report says `a4a890c`: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/kake.md:5` "measured
  revision: `a4a890cf…`", and its table `:38-44` pairs the command `--revision a4a890c` with receipts that print `revision: 1ae8de5`
  (confirmed by running `git show a4a890c:.ufo/waves/round-52/control/c1-ledger-real.txt`). One measurement, two stated revisions, and the
  report's command line is not the one that produced the receipt it cites.

### Round 55 — `faf9abe` → `64c0ce1` (receipts) → `955e3d7` (relabel)

- Messages: `64c0ce1` "round-55: **content revision** — reviewer repairs, lesson caveat, validation receipts"; `955e3d7` "round-55: measurement
  receipts, settlement, SCORECARD and LOG".
- Want: the "After" column of `/home/vgpnk/Projects/shokunin/.ufo/reports/round-55/kake.md:41-44` is headed `After (64c0ce12)`, and
  `:34-35` labels `64c0ce1` "**(measured content revision)**". The receipt was first committed pinned to `faf9abe`, the commit the counter
  could actually have read.
- The carrier is not surface-neutral: `64c0ce1` edits `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` in two prose hunks
  (confirmed by running `git show 64c0ce1 -- corpus/knowledge/`) — the C2 claim's own surface — after the pin it carries.
- Rewrite step: `955e3d7` changes exactly 5 insertions / 5 deletions (2 receipt pins, the selftest fixture revision, `LOG.md:2166`, and
  `SCORECARD.md` "measured commit"); the PASS lines and counts are byte-identical (confirmed by running `git show 955e3d7`). No artifact shows
  a run: the commit message says receipts/settlement, not a re-run. [INFERENCE] the pins were edited, not re-measured; the 32 s window
  `18:47:20`→`18:47:52` cannot be excluded, but every committed number is unchanged, which a re-run could not distinguish and an edit
  produces exactly.

### Round 56 — `f8438a2` → `4cb225f` (receipts) → `ad06cb8` (relabel)

- Messages: `4cb225f` "round-56: C2 selftest 86 checks, **SKILL pin/counts**, README cite, lesson fixes, SCORECARD, LOG, settlement";
  `ad06cb8` "round-56: measurement receipts, SCORECARD and LOG **revision pins**".
- Want: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/kake.md:37` labels `4cb225f` "(measured content revision)" and `:43-46` heads the
  After column `After (4cb225fb)`.
- The carrier edits the very surface C1 measures: `4cb225f` rewrites the round-56 C2 self-test cell in `SKILL.md` from
  `KAKE_R56_SELFTEST_REV=3691e968…` (67 checks) to `KAKE_R56_SELFTEST_REV=f8438a28…` (86 checks) and moves a `corpus/README.md` coverage
  pointer (confirmed by running `git show 4cb225f -- SKILL.md corpus/README.md`). At that same commit
  `.ufo/waves/round-56/controls/c2-selftest.txt` still reads `67/67` while the row claims 86 — the row's count is unmeasured until `ad06cb8`
  prints `86/86` (confirmed by running `git show 4cb225f:…/c2-selftest.txt` and the `ad06cb8` diff).
- The placeholder is the smoking gun: at `4cb225f`, `LOG.md:2187` and `SCORECARD.md:4324` carry the literal `@R@` where the measured commit
  belongs, substituted at `ad06cb8` (confirmed by running `git show 4cb225f:LOG.md | grep -n @R@`). The author knowingly deferred the hash —
  it is the commit being written — and filled it afterwards.
- Rewrite step: `ad06cb8` = 5 lines (2 pins→`4cb225f`, selftest 67→86 with its fixture pin left at `f8438a2`, `LOG.md:2186`, `SCORECARD.md`).
  The same commit pair shows the selftest was re-run (count changed) and the after-* receipts were not (nothing but the hash changed).
  [INFERENCE] for "not re-run"; the round-57 contract asserts it as fact (`.ufo/waves/round-57/contract.md:22-24`).

## ROOT CAUSE

1. **One hash, three roles.** The round needs a single hash that is (a) the tree measured, (b) the commit containing the receipt, and (c) the
   branch tip the report/SCORECARD/LOG name — the round prompt pushes the third: "record measured/pinned revisions **as the branch tip**, never
   bare `HEAD`" (`.ufo/prompts/kake-round-56.md:376-377`; the same sentence at `kake-round-55.md:376-377` and `kake-round-52.md:325-326`). (c) does not exist while the receipt is written;
   it can only be filled after the fact, which is why the rewrite is structurally forced, not a lapse.
2. **Content and receipt committed together.** The receipt can only pin C^; then the report's "After (C)" and the LOG sentence "exit 0 at C"
   need C. `LOG.md:2166` (round 55) and `LOG.md:2186` (round 56) are exactly those sentences. The rewrite supplies the one value the author
   could not have measured.
3. **The line is an echo of an argument.** Every counter prints the caller's `--revision`, not the tree it read
   (`c52_gate_registry.py:383`, `c52_quote_truth.py:661`, `c52_wave_ledger.py:723`, `c55_readme_index.py:416`, `c55_quote_truth.py:890`,
   `c56_quote_truth.py:1040` — confirmed by running). So `sed`ing that argument and re-running are textually indistinguishable; nothing in the
   round could falsify a relabel. Round 55/56 had no receipt pin at all, and round 52's pins moved in the same commit as their artifacts (§52).
4. **Fixed point evaded.** A receipt cannot honestly name the commit that contains it; the six rewrites each name exactly that commit
   (`to == intro` in all six). The consistent form was available and was the *first* value written: pin C^, the tree the counter read.

## DOES V2 REMOVE IT

The v2 rule (`.ufo/waves/round-57/contract.md:122-135`; `.ufo/waves/round-57/c57_receipt_pins.py`) removes the *defect*, not the *trust gap*.

Removed — mechanically, not by wording:
- The relabel shape is now impossible: the measured revision must equal the single `revision:` line, be a strict ancestor of the commit that
  introduced the receipt, and must not be that commit (`c57_receipt_pins.py:256-257`: `measured_rev != intro and is_ancestor(root, measured_rev,
  intro)`). All six historical rewrites set `to == intro`, so v2 rejects exactly those six shapes.
- Silent rewrites are caught: whole-ancestry walk over every `revision:` line (renames, merges), errata verified field-by-field against git, base
  control `undisclosed_relabels=6` (`contract.md:35`, `:154-158`).
- One receipt stops being pure attestation: after-c1 must carry `tip: <T0>` where T0 already holds all three receipts and is a strict ancestor of
  the writing commit, and the counter *recomputes its own report at T0* (`rerun = measure(root, t0, check_bodies=False)`,
  `c57_receipt_pins.py:277`) and compares the first line. T0 is a genuine fixed point — the tree reported on does not contain the report — so
  C1's own "what a run printed" is verified by re-execution, not accepted.

Moved — the same gap, one layer in:
- after-c2/after-c3 bodies are shape-checked only (regex + `EXIT=0`, `c57_receipt_pins.py:261-263`). The contract says so itself: a hand-written
  `C2 … 5/5 met=True` line with the right pin passes, and the counter "certifies that the pin matches what the receipt's history and body say, not
  that a counter ran" (`contract.md:162-164`, `SKILL.md:1279`). What closes C2 is the gate re-running the tool at the measured revision, not the
  receipt.
- v2 still permits the *material* half of rounds 55/56: `measured_rev = C^` with carrier `C` editing the claim's surface (`4cb225f`'s
  `SKILL.md`/`readme` edits). It checks ancestry, not surface immutability. The new `Measured revision:` SCORECARD line
  (`c57_receipt_pins.py:42`, `:288-289`) forces the report to *name* C^ instead of the tip — the honest label — but nothing forbids a carrier
  from editing what the claim measures right after the run.
- C1's own met-ness is a statement about T0's bookkeeping (receipts + pins + SCORECARD), so the receipts are inputs to the report that certifies
  them; sound at T0, silent about the tip.

Answer: v2 removes the circular label and the silent rewrite; it moves the circularity from the commit graph (now a checked impossibility) to the
receipt bodies of the two claims C1 only shape-checks, and it leaves the "carrier edits the measured surface" path open — disclosed, not closed.

## PROCESS SENTENCE

Proposal for `corpus/QUALITY.md` (append after the last bullet, its Grounding/Falsifier style); not applied by this seat:

> **A receipt names the revision its counter ran over — never the commit that carries it — and the commit that carries it changes nothing the
> claim measures.** Grounding: rounds 52/55/56 rewrote six receipt pins from the measured parent onto the carrying commit
> (`.ufo/waves/round-57/receipt-errata.json`; `corpus/lessons/round-56-verifier-spotcheck.md` §6). Falsifier:
> `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision <tip>` prints `undisclosed_relabels=0 … new_relabelled=0`, and
> `git show --stat <each receipt-carrying commit>` touches only `controls/*.txt`, `measured.json` and the SCORECARD/LOG pin lines.

VERDICT: Six relabels, three rounds, one exact shape — pin moved from the measured parent C^ to the receipt-bearing commit C — forced by demanding one hash for run, carrier and branch tip plus a counter line that merely echoes `--revision`; v2 makes that shape impossible and disclosure-checkable and machine-re-derives the C1 receipt at T0, but relocates the residual trust into the two shape-checked receipt bodies and still permits a carrier to edit the surface it certifies.
