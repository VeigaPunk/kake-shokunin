# CriticC1Semantics evidence transcript (all read-only vs lane; fixtures under /fast/scratch/hyaku/kake-r61/CriticC1Semantics)

## E1 — extra_member landmine (HEAD vs frozen list)
$ git -C <lane> ls-tree -r HEAD --name-only | grep -E '\.ufo/waves/round-[0-9]+/(.*\/)?controls?/.*\.(txt|json)$' | wc -l
146
$ git -C <lane> ls-tree -r 9f07731a873585e655a6518233ea39f5d9fb8204 --name-only | grep -E '...same...' | wc -l
144
$ comm -23 <path-rule files at HEAD, sorted> <population-144.txt, sorted>
.ufo/waves/round-61/controls/census-before.txt
.ufo/waves/round-61/controls/population-144.txt
=> at ANY measured revision ≥ eaa9177 (contract commit), two files match the path rule outside
   the frozen 144 => extra_member ×2 => R2's `exit 0` is unreachable if the counter enforces
   extra_member on the real lane. The two files are the round's own measurement apparatus,
   committed in eaa9177 before any seat ran.

## E2 — historical events under literal rules (full first-parent walk first-add .. base)
Literal-rules pass over all 144 population paths (grammar check on first committed version,
event = first-parent commit whose blob differs and whose result-span set differs):
  rewrite  .ufo/waves/round-52/control/c1-ledger-real.txt          a4a890cf1
  rewrite  .ufo/waves/round-52/control/c1-mutation-ladder.json     1ae8de5d4
  rewrite  .ufo/waves/round-52/control/c1-mutation-ladder.json     a4a890cf1
  rewrite  .ufo/waves/round-52/control/c1-mutation-ladder.json     fd91527a2
  rewrite  .ufo/waves/round-52/control/c2-quote-real.txt           a4a890cf1
  rewrite  .ufo/waves/round-54/controls/c1-selftest.txt            8e408e00f
  rewrite  .ufo/waves/round-54/controls/c1-selftest.txt            a631cc024
  rewrite  .ufo/waves/round-55/controls/after-c1-readme-index.txt  955e3d7bd
  rewrite  .ufo/waves/round-55/controls/after-c2-quote-truth.txt   955e3d7bd
  rewrite  .ufo/waves/round-56/controls/after-c1-selftally.txt     ad06cb8a1
  rewrite  .ufo/waves/round-56/controls/after-c2-quote-truth.txt   ad06cb8a1
  rewrite  .ufo/waves/round-57/controls/after-c1-receipt-pins.txt  20217f23e
TOTAL = 12 events. Errata (.ufo/waves/round-57/receipt-errata.json) covers 6 of them.
Uncovered: c1-mutation-ladder@1ae8de5d4, @a4a890cf1, @fd91527a2;
           r54 c1-selftest@8e408e00f, @a631cc024; r57 after-c1-receipt-pins@20217f23e.
=> a disclosures registry built only from the errata leaves 6 events undisclosed => R2 fails.
   The r57 fill emits kind `rewrite` (v1 span = {"  revision: ...", "EXIT=0"}; the word
   `pending` sits on a non-span line => pending_filled does not arm).

## E3 — r57 v1 shows pending outside the span
$ git show 31b61a4:.ufo/waves/round-57/controls/after-c1-receipt-pins.txt
pending
  revision: 32754df75774dd38e8a96fcda375fc93adf97f1e
EXIT=0
=> v1 result span = {"  revision: 32754df...", "EXIT=0"} — contains NO word `pending`.
   The motivating r57 defect cannot emit `pending_filled` under the literal rule;
   it emits `rewrite` only because the fill ADDED a `met=` span line.

## E4 — grammar coverage at base (first committed version AND base blob)
49 of 144 population files carry no grammar line (`# receipt:`, `EXIT=`, `^VERDICT:`)
in either their first committed version or their base blob — including receipt-shaped
run records: round-55/56 selftest receipts (one-line tallies), round-37/48 c2 JSON
verdicts ("met": false + revision: inside), round-60 T1 receipts (the R60-D3 class),
all census/registry/rows before/after files. These are watched only by member_changed.

## E5 — JSON colon-form gap (real population file)
c1-mutation-ladder.json span lines at base: only `"old_tail": "  revision: <sha>",` and
`"new_tail": "EXIT=<n>"` (quoted tails). Its result fields — "met": true,
"families_caught": 13, "families": 18 — are colon-form, matching NO span keyword.
Rewriting "met": true->false or "findings"->0 leaves the span set identical => invisible.

## E6 — scratch fixture demos (literal-rules sim, specsim.py in this dir)
fix_A: v1 {pending / "  revision: 111..1" / EXIT=0} -> v2 {result rows / same revision /
       same EXIT=0}: span identical => pending fill produces NO finding (pending_filled
       does not arm on a non-span line; rewrite needs a span diff). CONFIRMED none.
fix_B: JSON receipt v1->v2 changes "findings":3->0 and "met":false->true (colon form,
       never span-matched), "revision"+EXIT= identical => NO finding. CONFIRMED none.
fix_C: receipt gets a cosmetic (non-span) edit, author discloses it anyway => tool finds
       no event => the disclosure is a phantom_disclosure finding. CONFIRMED.
fix_D: file added without grammar, grammar header + rewritten run line land in one
       commit, then EXIT=0->1: first-version gate never opens => NO finding. CONFIRMED.
fix_E: receipt deleted => path absent from a tip-scan => NO finding; under the frozen
       list, "different blob" vs absent is ambiguous. member_missing only.
fix_F: rewrite + revert-to-base pair => TWO undisclosed_rewrite findings though final
       bytes equal v1. CONFIRMED.
