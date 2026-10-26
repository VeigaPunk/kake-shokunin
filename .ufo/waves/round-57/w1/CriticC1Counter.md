# CriticC1Counter

Attack surface: `contract.md` C1 + `c57_receipt_pins.py` v1 (349 ln), base control `controls/base-c1-receipt-pins.txt`
(`undisclosed_relabels=6 … population=45 new_receipts=0 scorecard_pin=0 met=False`, one `revision:` line = base
`28fa0b23…`, body says `met=False`). Method: 16 fixtures built in `mktemp -d` git sandboxes and scored by importing the
counter's own `measure()`/`met()` with `python3 -B` (git-object reads only; no lane write, no lane checkout, no jj/git
mutation). Every value below is **observed**, not predicted; exit is 0 iff `met()`, per the kill rule.

## S0 — structural: C1's own "after" receipt cannot honestly be `met=True` at its own pin

`measured_rev` must be a **strict ancestor** of the commit that introduces `after-c1-*.txt` (l.145-147). At any such
ancestor the three receipts do not exist, so the C1 counter run there necessarily prints `new_receipts=0 … met=False` —
which is exactly what the base control is. The pin rule therefore forces the C1 receipt to be either (a) a pre-state run
whose body contradicts the predicate, or (b) a fabricated body. The counter reads no receipt body, so it cannot tell
(a) from (b). This is the root that makes attack A1 possible; the declared limit ("does not test that a counter was
actually run at the pinned revision", docstring l.30) is not a side note — for C1 it is load-bearing.

## ATTACKS:

**A1 — do-nothing: pin the base revision, ship three copies of the base control. (met=True, exit 0)**
Input: (i) `receipt-errata.json` with the 6 historical relabels (from, to, commit taken from the counter's own
`UNDISCLOSED` lines + `git log -1 --format=%H -- <path>` — tuple equality is the only check, l.128-129); (ii)
`measured.json {"revision":"28fa0b23e699303725aba2727094531f5e44494d"}`; (iii) `SCORECARD.md` `## Round 57` containing
`28fa0b23e699`; (iv) `cp` the committed `controls/base-c1-receipt-pins.txt` to `controls/after-c{1,2,3}-*.txt` unchanged.
Observed: `undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3
scorecard_pin=1 met=True`. The receipt body literally reads `new_receipts=0 scorecard_pin=0 met=False` while the
predicate says met. No counter is ever run at any after-state revision; the only work is mechanical errata bookkeeping.
Selftest: **no** (no scenario pins a pre-work revision; no scenario reads a body).

**A2 — SCORECARD pin satisfied by a negation/comment. (met=True, exit 0)**
Input: section `## Round 57` = `NOT measured at <12hex>; <!-- <12hex> -->`. `scorecard_pin` is a bare substring test
(l.158), so any occurrence counts. Observed `scorecard_pin=1 met=True`. Selftest: **no** (l.287 tests omission only).

**A3 — three bare revision-only receipts. (met=True, exit 0)**
Input: `after-c{1,2,3}-*.txt` each containing exactly one line `revision: <measured>`, nothing else. Observed
`new_unpinned=0 new_receipts=3 met=True`. No claim token, no counted line, no predicate sentence is required, although
the contract says the predicate sentence is "the same sentence … in every receipt label". Selftest: **no**.

**A4 — three identical bodies. (met=True, exit 0)**
Input: the C1 receipt text copied into all three `after-c*` files. Only the file *names* carry claim numbers; bodies are
unread. Observed `met=True`. Selftest: **no**.

**A5 — real receipts hidden in a sibling directory. (met=True, exit 0)**
Input: the relabelled real receipts under `.ufo/waves/round-57/controls2/` (not matched by `POP_RE`, l.56 — it admits
only `control|controls`), plus three pinned stubs under `controls/`. Observed `met=True`, and the relabel in
`controls2/` is invisible (`relabels_old=0`). Selftest: **no**.

**A6 — old receipt relabelled through a different key, or in JSON. (met=True, exit 0)**
Input: `.ufo/waves/round-56/controls/after-c1-selftally.txt` = `pinned: <A>` → `pinned: <B>`; or
`…/after-c1-selftally.json` = `{"revision":"<A>"}` → `{"revision":"<B>"}`. `REV_RE` (l.57) is line-anchored on the bare
word `revision`, so neither is seen: `relabels_old=0`, `deleted_receipts=0`, `met=True`. Live instance: the population
path `.ufo/waves/round-52/control/c1-mutation-ladder.json` carries three `"old_tail": "  revision: <hex>"` pins that the
counter cannot parse — the `.json` arm of `POP_RE` is dead weight (1 of 51 population paths, 0 parseable). Selftest:
**no**. (Partly declared out of surface; the JSON arm is not.)

**A7 — duplicate identical revision line in a new receipt. (met=True, exit 0)**
Input: one new receipt with `revision: <measured>` twice. `revs` is a set (l.143), so `len(revs)==1`. Observed
`new_unpinned=0 met=True`. Selftest: **no** (l.285 only covers two *different* values).

**A8 — `git mv` + relabel in one commit: relabel hidden, failure undisclosable. (met=False, exit 1 — for the wrong reason)**
Input: rename a round-56 receipt and rewrite its revision line in the same commit. Observed `relabels_old=0` (the D-side
`blob is None` branch resets `prev`, l.105-108; the new path has a single version, so no pair is formed) and
`deleted_receipts=1` (l.116). Any errata entry for the relabel would be **phantom** (there is no relabel to match), so
the state cannot be disclosed, and `deleted_receipts` is a latch: it never returns to 0 without rewriting history.
Selftest: **no** (l.280 tests deletion alone; the mv+relabel composition is untested and behaves as "hidden relabel +
hard fail").

**A9 — errata `commit` is 40-hex and exists but is not the relabelling commit. (met=False, exit 1)**
Input: correct path/from/to, `commit` = the pre-relabel commit. Observed `phantom_errata=1 undisclosed_relabels=1`.
Selftest: **yes** (l.279 class; same tuple-equality path, only the value differs — the fixture uses `f`*40, this attack
uses a real commit, and both fail identically).

**A10 — relabel on a side branch, merged. (met=False, exit 1 — detected)**
Input: relabel on `side`, `merge --no-ff`. `--first-parent` makes merge diffs first-parent diffs, so the merge commit
shows `M` and the relabel is recorded at the merge (observed `relabels_old=1 undisclosed_relabels=1`). No hiding gap;
only provenance is off by one commit (errata must name the merge, not the true relabel commit). Selftest: **no**, but
nothing to fix.

**A11 — `measured.json` and the receipts in the same commit, pinning any ancestor. (met=True, exit 0)**
Input: one commit adds `measured.json`, the SCORECARD pin and the three receipts; `measured.json` names an earlier
commit. Observed `met=True`. Nothing ties `measured.json` to the run it claims. Selftest: **no**.

## WRONG-REJECT:

**W0 (S0)** The honest C1 receipt at its own pinned revision records `met=False`; a reviewer who writes the run's real
output is fine, but any attempt to record the *after* state honestly is rejected by l.147 — so the counter rewards the
A1 fabrication and punishes the honest after-run. No correction is possible inside the current pin rule; see R1+R2.

**W1 — net disclosure of a multi-step relabel is rejected.** Input: receipt `A → B → C` (two commits), errata says
`(path, A, C, commit_of_C)` — the semantically true disclosure a human writes. Observed
`undisclosed_relabels=2 phantom_errata=1 met=False`. The counter records pairwise steps (l.109-114) and matches tuples
exactly, so the true statement is counted as a phantom *and* leaves both steps undisclosed. Selftest: **no**.

**W2 — `deleted_receipts` is a latch with no disclosure channel.** Input: delete a receipt and re-add it byte-identical.
Observed `deleted_receipts=1 met=False`, though the tip is indistinguishable from an honest state. Same for an
accidental `git mv` (A8) and for a legitimate cleanup of a superseded duplicate. Nothing in `receipt-errata.json` can
clear a deletion. Selftest: **no**.

**W3 — an extra receipt breaks the predicate.** Input: after-c1..c3 plus a legitimate `after-c4-selftest.txt`.
Observed `new_receipts=4 met=False` (l.159). Conversely two files for claim 1 plus 2 and 3 gives
`new_receipts=3 met=True` (the set dedups). The rule is inconsistent in both directions. Selftest: **no** (neither case).

## RECOMMENDED COUNTER CHANGES: (before any C1 data is scored; keep the frozen predicate string unchanged)

**R1 — anchor the measured revision to a revision where the run was possible.** In the pin block (l.145-147) add
`and is_ancestor(root, counter_intro, measured_rev)`, with
`counter_intro = git(root,"log","--first-parent","--diff-filter=A","--format=%H",tip,"--",f"{WAVE}/c57_receipt_pins.py").strip().split("\n")[-1]`
(= `b9a5d012f7fd…`, verified: `merge-base --is-ancestor b9a5d01 28fa0b2` returns 1). Kills A1 and A11: the base
revision does not contain the counter, so a "run" there is not a round-57 run. One line, no new I/O.

**R2 — make the C1 receipt's counted line checkable.** Re-run `measure(root, measured_rev)` (git-object only, no
checkout) and require the `after-c1-*` receipt to contain that exact `C1 receipt-pins …met=…` line; for `after-c2/c3`
require the claim-specific token (`gate_conditions_passed` / `conditions_passed`). Kills A3, A4, and the A1 copy (the
copied body is a *C1* body in a C2/C3 file). This is the cheap way to convert the declared limit in the docstring (l.30)
into a checked property without changing the predicate.

**R3 — scorecard pin must be an assertion, not an occurrence.** l.158:
`scorecard_pin = int(bool(measured_rev) and re.search(r"(?i)measured at\s+`?[0-9a-f]{0,4}" + re.escape(measured_rev[:12]), section) is not None)`.
Kills A2.

**R4 — make the relabel detector rename-aware and the deletion count non-latching.** l.86: drop `--no-renames` for the
log walk; in the loop (l.105-108) when `text is None`, pair the deleted path's `prev` with any path *added* in the same
commit whose first version differs only in its revision set, and record the relabel under the new path. l.116: count
only paths absent from `present` (deleted and not re-added), or add a `deletions` array to `receipt-errata.json` that
discloses a deletion like a relabel. Kills the A8 blind spot and W2.

**R5 — parse the pins the population already contains.** Either drop `\.json` from `POP_RE` (l.56) or add
`JSON_REV = re.compile(r'"revision"\s*:\s*"([0-9a-f]{40})"')` and union it into the revision set. Today
`round-52/control/c1-mutation-ladder.json` sits in the population with three unread pins.

**R6 — make `new_receipts` a name-set test, not a count.** l.159:
`new_receipts = len(new_nums & {"1","2","3"})` and add `and len(new_nums) == 3` to `met()`'s derivation, so an extra
claim-4 receipt is reported as a note instead of a failure (W3) while a missing claim still fails. Do not touch the
frozen predicate text; the value it compares stays `== 3`.

Tool installs: none. Lane state: read-only; the only file written is this report. Scratch fixtures lived in
`mktemp -d` sandboxes, each verified `rev-parse --show-toplevel` == its own root.

VERDICT: C1 v1 is satisfiable with zero after-state measurement (three `cp`s of the base control pinned to `28fa0b2`, observed met=True/exit 0) because nothing anchors `measured_rev` to a revision containing the counter or checks a receipt body; fix R1+R2 (one line + one re-run) before any C1 data is scored.
