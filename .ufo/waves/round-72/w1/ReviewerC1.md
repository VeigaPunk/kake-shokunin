# ReviewerC1 — attack on C1 (round 72, w1)

c1_verdict=survives

C1's frozen predicate holds under independent re-derivation: c66 gate-status agreement is exactly 25 of 28 at the
relabel tip, 24 at base, and the only member whose agreement changes is `c56_selftally.py` (disagreement →
agreement). The pin is a commit and an ancestor of base; the pin run of c56_selftally is green 10/10; none of the
ten audited tool scripts changed pin→base — the tip red is the counter's frozen fixture-tree rule meeting four
round-63 fixture files added for an unregistered tool, with every claimed tally still observed-true. The
historical label is an honest description of the tip red, not a mask for a defect.

## 1. Pin verification

- `git cat-file -t 4cb225fb032b04166fb0232bc98a7bcce72675ec` → `commit`, exit 0.
- `git merge-base --is-ancestor 4cb225fb… 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` → exit 0.

## 2. Pin run and audited-tool drift (scratch clone at 4cb225fb)

Pin run (my own, clone at the pin, committed bytes):

```
python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision 4cb225fb032b…   # exit 0
C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True
  45/45 106/106 204/204 235/235 23/23 9/9 19/19 18/18 44/44 54/54 — all claim=observed OK
```

Audited path set (31 paths) derived from the counter source (`.ufo/waves/round-56/c56_selftally.py` at the pin,
committed bytes): the ten POP pinned scripts (`scripts/base_path_selftest.py`, `scripts/source_recheck_selftest.py`,
`scripts/robots_audit_selftest.py`, `scripts/sitemap_audit.py`, `scripts/redirect_audit.py`,
`scripts/citation_lint.py`, `.ufo/waves/round-52/c52_wave_ledger.py`, `.ufo/waves/round-52/c52_quote_truth.py`,
`.ufo/waves/round-55/c55_readme_index.py`, `.ufo/waves/round-55/c55_quote_truth.py`), every `*.py` sibling beside
them at BASE_REV `e48354b7c26b…`, and `scripts/fixtures/` (the counter's `FIXTURE_DIRS`).

`git diff --stat 4cb225fb… 3c68645a… -- <31 paths>` → exit 0, exactly 4 files, +4 lines:

```
scripts/fixtures/quote-class/inline.raw.html | 1 +
scripts/fixtures/quote-class/inline.txt      | 1 +
scripts/fixtures/quote-class/markup.raw.html | 1 +
scripts/fixtures/quote-class/markup.txt      | 1 +
```

Changed audited **tool scripts: none** — all ten pinned scripts and all sibling `.py` files are byte-identical
pin→base. The only change is the four quote-class fixture files. One line each:

- The four fixture files are new test payload for `scripts/quote_class.py` (added in round-63 commit `6d8c52a6`;
  `git grep quote-class 3c68645a -- scripts/` matches only `scripts/quote_class.py`). Not a defect repair to any
  audited tool; not a behavioural change of any audited tool; no registry row's claimed fixture count is
  invalidated (all ten rows still observe claim==observed at the tip-side revision, see §5).
- `scripts/quote_class.py` itself did not exist at the counter's frozen BASE_REV `e48354b7…` nor at the pin
  (`git cat-file -e` fails at both), so the new tool is outside the counter's audit population entirely.

What `tool_changed` actually flags (`helpers_changed`, same source): at rev=base → `['scripts/fixtures/']` for
exactly the six `scripts/` rows, `[]` for the four `.ufo/waves` rows; at rev=pin → `[]` for all ten. The six
`tool_changed` mismatches in the tip-side red are therefore pure collateral of the counter's frozen whole-
fixture-tree comparison against `e48354b7…`, not tool drift in the audited scripts.

**Honesty of the historical label.** Honest. Green at the pin (re-run, exit 0, 10/10), red at the lane tip solely
via the fixture-tree rule, every claimed tally still observed-true, no audited tool byte changed. The relabel
hides nothing: the six tools' selftests pass 100% with counts matching their rows at both revisions. Caveat (see
Findings F1): the new Kind cell's phrase "six audited tools have changed since the frozen base" is byte-imprecise
— the audited *fixture tree* changed; the tool scripts did not.

## 3. c66 label logic (`.ufo/waves/round-66/c66_gate_status_hostportable.py` at base; working tree byte-identical to base)

- Line 539: `label = "historical" if has_hist else ("never-met" if has_nm else "live")`
- Line 562: `pin_run = label in ("historical", "never-met") and pin is not None`
- Lines 585–591 (`elif label == "historical":`): `e_T == 0` → `historical_but_green`; `e_T != 1` →
  `historical_bad_exit`; `e_P is not None and e_P != 0` → `historical_not_green_at_pin`.
- Line 676/679: a member carries a class ⇒ counted in `mismatches`; `agreement = sum(1 for r in results if not r["classes"])`.

Confirmed: a `historical` label with a **green pin run** (`e_P=0`) and a **red tip run** (`e_T=1`) collects zero
classes ⇒ classed as agreement. The same label with a **red pin run** (`e_P!=0`) collects
`historical_not_green_at_pin` ⇒ classed as a disagreement. The pin run is measured by c66 itself at tip time
(`run_member` at the row's pin), not copied from any receipt; at the tip it re-ran c56 at `4cb225fb…` and got
`e_P=0`, matching my own pin run.

## 4. Tip provenance

The measured tip `84b5ecff97548bc8b731f1b3003bc9ec5e7c24c6` (from `w1/c1-relabel-tip.txt`) exists in **no** lane
ref and is not fetchable from the lane repo (`git cat-file -t` fails; `for-each-ref --contains` errors) — expected
pre-WAVE-DONE: ExecRelabel committed it in its scratch clone. Reproduction instead:

- Applied `w1/c56-relabel.patch` (ExecRelabel's `format-patch` of `84b5ecff…`) onto base in my scratch clone:
  `git apply --numstat` → `1  1  SKILL.md`; committed (kake-scratch identity) → reconstruction
  `af83ebe33e46f9353196c6f88167ffce4bd3d0ef`; `git rev-parse HEAD:SKILL.md` →
  `a77064a1aa1d8779c17c03188441bbb266abf7d9` = the patch's new-blob index hash, so the reconstruction's SKILL.md
  is byte-identical to the tip's, and (per the patch + ExecRelabel's `numstat 1/1`) the tip is base + that one line.

## 5. Predicate re-derivation (do not trust, re-run)

Base (my own run, clone at base, frozen counter file identical to working tree):

```
python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . \
  --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 --jobs 6        # exit 0
C1 gate-status members=28 evaluated=28 mismatches=4 structural=0 agreement=24 scores_held=3/3 met=True
  mismatches: c56_selftally, c57_idresolver_gate, c58_resolver_cases, c59_resolver_cases (all live_not_green)
```

Matches contract receipt `controls/c1-base.txt` verbatim on the summary line and member statuses.

Tip (my own run at the reconstruction; `84b5ecff…` per `w1/c1-relabel-tip.txt`):

```
python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . \
  --revision af83ebe33e46f9353196c6f88167ffce4bd3d0ef --jobs 6        # exit 0
C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True
  .ufo/waves/round-56/c56_selftally.py label=historical e_T=1 e_P=0 eval=ok ok
  residual mismatches: c57_idresolver_gate, c58_resolver_cases, c59_resolver_cases (live_not_green, unchanged)
```

Receipt diff (my own): member-status lines of `controls/c1-base.txt` vs `w1/c1-relabel-tip.txt` — 28 lines each,
exactly one changed line:

```
-.ufo/waves/round-56/c56_selftally.py label=live e_T=1 eval=ok MISMATCH live_not_green
+.ufo/waves/round-56/c56_selftally.py label=historical e_T=1 e_P=0 eval=ok ok
```

Both cited control receipts exist and match my runs: `controls/c56-pin-linux.txt` (exit 0, 10/10) and
`controls/c56-tip-linux.txt` (exit 1, `tally_mismatches=6`, six `tool_changed`, observed equal to claim in every
row). Predicate: `agreement == 25`, `evaluated == 28`, only changed member `c56_selftally.py` (disagreement →
agreement) — **all legs hold**. No kill-rule condition triggered.

## Findings

- **F1 [note]** The relabel's Kind cell says "six audited tools have changed since the frozen base". Byte-true
  statement: no audited tool script changed; the shared `scripts/fixtures/` tree gained four files for the
  round-63 `quote_class.py` tool. The phrase is defensible under the counter's own `tool_changed` semantics
  (audited byte-set includes the fixture tree) and the cell immediately states "observed equal to claim", but a
  reader can wrongly infer the six `.py` scripts were modified. Suggest "the audited fixture tree has changed
  since the frozen base" wording before landing (relabel not yet landed; lane HEAD is still freeze commit
  `a19d38ea…`). Non-gating: c66 parses only `historical` + the pin hex.
- **F2 [note]** The measured tip `84b5ecff…` is not an object of the lane repo, so the tip measurement cannot be
  replayed against the lane alone; it is reproducible via `w1/c56-relabel.patch` (verified: applied patch yields
  SKILL.md blob `a77064a1…`, my c66 run at the reconstruction reproduces agreement=25/mismatches=3). After
  landing, `git ls-remote origin refs/heads/master` should equal the landed hash and the receipt should be
  re-runnable at the lane tip directly.
- **F3 [note]** No tooling installs or upgrades were needed or performed; no pacman transactions.

## Counterexample

None found. Every predicate leg re-derived green; no member other than `c56_selftally.py` changes agreement; the
pin run is green; the residual reds (c57/c58/c59) are the contract's disclosed non-goals and are unchanged
base→tip.

## Residual risk / verification gaps

- Tip equivalence to `84b5ecff…` rests on the patch's blob hash (`a77064a1…`), ExecRelabel's `numstat 1/1`, and
  the receipt's own argv lines — not on direct comparison with the (unavailable) tip object.
- The two c66 runs above were re-runs minutes apart on one host; per-member exits are deterministic reads of
  committed bytes, but a flaky timeout (`timed_out` class) would have shown as exit 2 and did not occur.

Environment: python3 3.14.8, git 2.56.0. Lane tree untouched except this report file; scratch
`/fast/scratch/hyaku/kake-r72/ReviewerC1/` deleted before yield.
