# CriticC1Semantics

Attack on C1's rule family before freeze. All lane evidence is read-only (`git show/ls-tree/log` vs
base 9f07731 + HEAD eaa9177); constructions run in scratch fixtures under
`/fast/scratch/hyaku/kake-r61/CriticC1Semantics/` via a literal-rules simulation (`specsim.py`),
transcript in `.files/evidence.md`. Two structural landmines are reachable at the lane's own HEAD
today; the rest are constructions on the frozen rules.

## FALSE GREENS:

- **FG1 — pending_filled never arms on a non-span `pending` line (missed rule: pending_filled).**
  Rule: v1's *result span* must contain the literal word `pending`. The motivating r57 defect
  (.ufo/waves/round-57/controls/after-c1-receipt-pins.txt v1 = `pending` / `  revision: <sha>` /
  `EXIT=0`) has `pending` on a line that matches NO span keyword — the real r57 fill would emit
  `rewrite` (its fill added a `met=` line), never `pending_filled`. Construction (fix_A, confirmed):
  v1 `{pending, "  revision: 111..1", EXIT=0}` → fill `{result rows: ..., same revision, EXIT=0}`:
  span identical, `pending` gone ⇒ zero findings. Any fill that keeps every span line byte-identical
  and puts the result on non-span lines is invisible.
- **FG2 — JSON colon-form result fields are outside the span (missed rule: result span).**
  Span keywords `met\s*=`, `findings\s*=`, `members\s*=` require `=`; JSON uses `"met": true`.
  Real population file `.ufo/waves/round-52/control/c1-mutation-ladder.json` is watched (grammar via
  embedded `EXIT=`/`revision:` tails), yet its result fields `"met": true`, `"families_caught": 13`,
  `"findings"` are colon-form → rewriting `"met": true→false` leaves the span set identical ⇒ no
  event (fix_B confirmed). Every `.json` receipt in the population has this hole.
- **FG3 — grammar added late with the rewrite in the same commit (missed rule: grammar detection /
  rewrite event).** Detection keys on the FIRST committed version only. v1 no grammar → never a
  receipt ⇒ later commits that add `# receipt:` and rewrite the result together are invisible
  (fix_D confirmed). In the population: 49 of 144 files have no grammar in v1/base (selftest
  one-liners r55–r60, c2 JSON verdicts, the R60-D3 T1 receipts); the tool alone cannot see their
  rewrites — only member_changed can, and member findings have no disclosure path.
- **FG4 — deletion of a receipt (missed rule: rewrite event / range bound).** "tree holds a
  different blob" vs the path being ABSENT is unspecified. If the population is tip-scanned the
  deleted path isn't enumerated at all (fix_E confirmed → zero findings). If the list is frozen,
  an implementer skipping absent blobs still emits nothing. Counter-level `member_missing` is the
  only backstop; the TOOL's claim ("undisclosed rewrites detectable") has a hole for the most
  destructive rewrite — deletion.
- **FG5 — R2 `events=<k>` is a free variable (missed rule: counter).** R2 expects
  `receipts=144 events=<k> undisclosed=0`, `<k>` unbound. The honest walk finds 12 events (E2); a
  lazy tool reporting `events=0` still passes R2's shape. Fixtures cover rewrites but the real-lane
  case does not pin the extracted count.
- **FG6 — `pending` substring vs word.** If armed at all, `pending` substring-matches
  `pending_review`; a benign edit removing that phrase reads as a fill. Spec says "literal word"
  but no boundary is stated.
- **FG7 — span is a set: duplicate/order invisible.** Removing a second identical `EXIT=0` line or
  swapping result lines changes no span set ⇒ no event. Marginal.

## FALSE REDS:

- **FR1 — extra_member fires on the round's own measurement apparatus (rule: member/extra_member).**
  HEAD holds 146 path-rule files vs 144 frozen; the two extras are
  `.ufo/waves/round-61/controls/census-before.txt` and `population-144.txt`, committed in eaa9177
  before any seat ran (E1). Any counter enforcing extra_member on the real lane ⇒ R2 exit-0
  unreachable by construction; every wave receipt committed under `round-61/controls/` (where the
  receipt rule puts them) adds more.
- **FR2 — disclosure-registry coverage vs 12 real events (rule: disclosure cover).** Literal rules
  extract 12 historical events (E2); receipt-errata.json covers 6. A registry built only from the
  errata (ExecC1Disclose's spec) leaves 6 undisclosed ⇒ R2 fails at freeze. Includes the r57 fill —
  emitted as kind `rewrite`, not `pending_filled` (E3).
- **FR3 — phantom_disclosure punishes honest disclosure (rule: phantom).** fix_C confirmed: a
  cosmetic non-span edit disclosed anyway ⇒ entry names a non-event (path,commit) ⇒
  phantom_disclosure finding. The rule flags extra-careful bookkeeping, not just deception.
- **FR4 — revert pair double-counts (rule: rewrite event).** fix_F confirmed: rewrite + revert to
  base bytes ⇒ two undisclosed_rewrite findings though the final blob equals v1 and member_changed
  is clean. Benign recovery still needs two disclosure entries.
- **FR5 — prose incidental to span keywords.** `met\s*=`/`EXIT\s*=`/`members\s*=` are unanchored:
  prose or quoted strings containing them (e.g. c1-mutation-ladder's `old_tail` values) are span
  lines; editing such prose fires `rewrite`. Real population receipts already trigger this way
  (E2's r52 events ARE `old_tail` string edits).
- **FR6 — grammar on first version punishes headerless-history.** Any population file whose first
  version was grammar-less but later gained a header is never watched; conversely a file grammar'd
  once stays a receipt forever. First-version-only detection is brittle both directions.

## TIGHTENINGS:

- **T1 (closes FR1, minimal):** scope `extra_member` to files under `round-<N>` dirs with N strictly
  less than the measurement round, or exempt the measurement round's own `controls/` tree — the
  round-61 files are apparatus, not historical receipts. One-sentence contract edit.
- **T2 (closes FR2):** the disclosure registry MUST be built from the extracted event list
  (ExecC1History's table = the 12 events above), not only the six errata entries; and pin R2 to
  `events == <extracted count>` (closes FG5 too).
- **T3 (closes FG1):** redefine pending_fill arming as "the first committed version's TEXT contains
  the word `pending` (word boundary, case-insensitive) and a later version's text does not" — the
  span is the wrong container; the r57 case arms on a non-span line by construction.
- **T4 (closes FG2):** extend the span alternation to allow `:` separators for `met`, `findings`,
  `members` (i.e. `met\s*[:=]` etc.) — one-character-class change per keyword; keeps L4/L5
  semantics, covers the JSON population.
- **T5 (closes FG3/FR6):** detect receipts by population membership, not v1 grammar — every frozen
  path is watched; grammar then only supplies the pending/span heuristics. If too broad, at minimum
  declare the 49 grammar-less files intentionally member-only.
- **T6 (closes FG4):** state explicitly that a receipt path absent in C's tree (deletion) is an
  event candidate whose span is the empty set ⇒ `rewrite` at C; also state the tool's population
  source (frozen list vs tip-scan) — the spec never says how the tool learns the 144 paths
  (no `--population` flag exists; `receipts=144` is otherwise unreachable).
- **T7 (closes FR3):** `phantom_disclosure` only for entries naming a population receipt path with
  no event at that commit; entries for non-receipt/non-population paths are noted, not findings.
- **T8 (spec hardening):** (a) disclose cover should require `kind` equality — a wrong-kind entry
  currently covers any event at (path,commit); (b) define malformed disclosure = unparseable JSON
  OR missing required key → exit 2; (c) state whether `--disclosures` reads `<rev>:path` committed
  bytes (fixtures then commit the registry) or worktree; (d) define `receipts=` as frozen-member
  count; (e) word-boundary `pending`; (f) L5's file should be named "outside the fixture's frozen
  list" or its expected-0 reconciled with member_changed.

VERDICT: C1's rule family has two structural landmines reachable at lane HEAD (extra_member on the round's own files; registry covering 6 of 12 real events) that make R2 unreachable as frozen, plus a pending_filled rule that cannot arm on the r57 defect it was written for — tightenings T1–T3 are the minimum safe corrections before the L1 freezes v1.
