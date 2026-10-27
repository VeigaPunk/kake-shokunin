# C1 counter evidence

## Frozen v1 behavior at B1

Scratch: `/fast/scratch/hyaku/kake-r60/ReviewerC1Counter/` (shared clone of the lane, detached at B1; top-level verified against that exact scratch clone). It was removed by an EXIT trap.

Command:

```sh
python3 -B <scratch>/base/lane/.ufo/waves/round-60/c60_gate_status.py --selftest --work <scratch>/work
```

Observed output: `selftest 76/76 passed` (all 76 checks printed PASS).

Command:

```sh
python3 -B <scratch>/base/lane/.ufo/waves/round-60/c60_gate_status.py --root <scratch>/base/lane --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --work <scratch>/work --jobs 6
```

Observed final output line: `C1 gate-status members=28 mismatches=0 scores_held=3/3 met=True`.

## Adversarial parser probes

Reproduction script: `C1CounterProbe.py` in this directory. It was run from the seat scratch directory with:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w2/ReviewerC1Counter.files/C1CounterProbe.py
```

Observed output:

```text
HTML-comment-only row: candidate row accepted True label= live e_T= 0 classes= []
fence case: parsed_table_rows= 1 rendered_mentions= [2, 5] mentions_count= 2 canonical_vs_hidden= True
fence row classification: ['duplicate_row']
never-met e_T=0,e_P=2: classes= ['never_met_but_green']
```

The first probe supplied a valid-looking row whose command text and member path were only inside a same-line HTML comment; `eval_member` accepted it and classified its mocked live exit as clean. The fence probe supplied one ordinary registry row plus a path mention inside a fenced block using invalid closer `````python``; only one table row was parsed, yet the hidden row mention caused `duplicate_row`. The last probe supplied never-met exits 0 and 2; the class list omits the bad-exit class.

## LSP availability

Attempted `read xd://lsp`; the runtime returned `No such tool: xd://lsp` (no LSP device is mounted). No grep-based semantic claims were made.
