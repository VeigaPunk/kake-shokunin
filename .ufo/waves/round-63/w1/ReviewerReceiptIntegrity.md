# ReviewerReceiptIntegrity — round-63 control receipts, receipt-rewrite defect class

Scope: the six committed control receipts under `.ufo/waves/round-63/controls/` —
`base-c1.txt`, `base-c2.txt`, `control-marker-fixture.txt`, `control-junk-fixture.txt`,
`after-c1.txt`, `after-c2.txt`. Checked: revision pins, recorded commands, whether any
receipt was written/rewritten after later commits touched its inputs, and whether each
receipt describes a run its pinned inputs cannot reproduce.

**Verdict: clean — no receipt-rewrite defect found.** Every receipt is committed once,
blob-identical to its commit, and every recorded output line + exit code reproduces
byte-exact (repo receipts) or field-for-field modulo the ephemeral scratch fixture
revision (fixture receipts, by design).

## 1. Rewrite check (`git log --follow` / full name-status history)

Per-file `git log --follow` shows exactly ONE commit per receipt:

- `base-c1.txt`, `base-c2.txt`, `control-marker-fixture.txt`, `control-junk-fixture.txt`
  — added in `6d8c52a6` (2026-10-27 09:54:45, "freeze contract; …").
- `after-c1.txt`, `after-c2.txt` — added in `7f77d12b` (2026-10-27 10:19:59,
  "green-after receipts at measured commit 05b0d7f4").

`git log --all --no-renames --name-status -- .ufo/waves/round-63/controls/` shows only
`A` (add) events — zero `M`, `D`, or re-add events on any ref. The empty-message
commits `37e5b634`, `06cfd360`, `c5459a38`, `e92ef6f6` appearing under `--all` are
duplicate snapshots on `refs/jj/keep/*` side-refs (same timestamps, add-only), never
on master's first-parent line (`git log --first-parent` shows only `7f77d12b`,
`6d8c52a6`).

Blob identity — receipt bytes at HEAD = index = bytes as committed:

| receipt | blob @ commit | blob @ HEAD |
|---|---|---|
| base-c1 | e3a833e8 @6d8c52a6 | e3a833e8 |
| base-c2 | 550579d7 @6d8c52a6 | 550579d7 |
| control-marker-fixture | b8fb627d @6d8c52a6 | b8fb627d |
| control-junk-fixture | e12d746d @6d8c52a6 | e12d746d |
| after-c1 | 087bb5a8 @7f77d12b | 087bb5a8 |
| after-c2 | 1eb9909c @7f77d12b | 1eb9909c |

Working tree clean (`git status --porcelain`: only untracked `w1/` wave files).

## 2. Input-timeline check ("written after later commits touched its inputs")

Counters evaluate pinned git revisions via `git show <rev>:<path>` (both counters,
`git_show()`); the only working-tree input is the counter script itself.

- `c63_calibration.py`, `c63_quote_tool.py`, `quote-classes.json` were introduced in
  `6d8c52a6` and never modified since (`git log --follow`: single commit each). Their
  sha256s at `6d8c52a6`, `05b0d7f4`, and HEAD are all identical to the frozen contract
  values: `bcd16f68…`, `9fcbfad0…`, `5f48e26b…` respectively. The counter code that
  produced every receipt is byte-identical to today's — all receipts reproduce with
  current tooling.
- `scripts/quote_class.py` changed in `05b0d7f4` (`40655dd8…` → `431e75e8…`, cwd
  fixture binding), *after* the four control receipts were committed in `6d8c52a6`.
  No harm: `base-c2` pins `--revision 13d45198` where the tool is absent (`present=0`
  holds either way), the marker/junk receipts don't invoke the tool, and the after
  receipts were committed in `7f77d12b`, *after* the tool change, pinning `05b0d7f4`
  where the new sha is live. Consistent with the contract's pre-wave freeze note.
- Ordering: `05b0d7f4` (measured, 10:19:30) → `7f77d12b` (after receipts, 10:19:29+)
  → `15eb965c` (wave spec). After receipts postdate their pinned input; the only
  commits postdating them (`15eb965c`, wave spec + untracked `w1/`) touch no receipt
  input path.
- Fixture receipts' inputs: marker fixture binds to committed
  `.ufo/waves/round-62/controls/false-green-fixture/corpus/` (committed `a5a0c444`,
  before the receipts); its 5 file sha256s match the round-62 L1 receipt pins exactly
  (verified: `0a9a0348…`, `635089aa…`, `373b9d25…`, `d7033c6d…`, `a27f4338…`).

## 3. Reproduction check — every receipt re-run

Commands executed verbatim from `/home/vgpnk/Projects/shokunin/kake-shokunin`
(counter scripts at HEAD = frozen blobs):

- `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d45198…` →
  `disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false`, exit 1 — **byte-exact vs `base-c1.txt`**.
- `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d45198…` →
  `present=0 selftest=unevaluable met=false`, exit 1 — **byte-exact vs `base-c2.txt`**.
- `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4…` →
  `disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0 — **byte-exact vs `after-c1.txt`**.
- `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4…` →
  `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0 — **byte-exact vs `after-c2.txt`**.

Fixture receipts rebuilt in own scratch `/fast/scratch/hyaku/kake-r63/ReviewerReceiptIntegrity/`
(repos `git init -q`, `rev-parse --show-toplevel` asserted equal before first commit,
throwaway identity `rri@scratch`; deleted after use):

- Marker fixture: byte-exact `cp -a` of the committed corpus, one commit
  (`b5339f13…`). `c62_calibration.py` → `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true`, exit 0; `c63_calibration.py` → `quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`, exit 1 — **field-for-field vs `control-marker-fixture.txt`**.
- Junk fixture: corpus with S432 Disagree + planted `[r63-correction]` frozen quote
  + ledger-path string, criterion lesson/QUALITY markers, S432 row — no blobs/ledger.
  `c63_calibration.py` → `disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false`, exit 1 — **field-for-field vs `control-junk-fixture.txt`**.

## 4. Observations (not defects)

1. **Fixture revision pins are ephemeral.** `7833be88…` (marker) and `7da479c2…`
   (junk) are scratch-repo commit hashes; `git cat-file -t` shows neither exists in
   the fleet object store. The exact recorded `revision=` line cannot re-run — only
   the semantic vector can (and does). Receipts disclose this ("scratch git repo",
   "fixture rev", `<fixture>`/`<rev>` placeholders), matching the round-62 precedent
   (`counter-false-green-l1.txt` names rev `6e5a1607…`, also ephemeral, corpus pinned
   by sha256). For the marker fixture the *content* pin is the committed corpus —
   intact. This is the class's known soft spot, not a rewrite.
2. **Junk-fixture recipe is unpinned.** Its corpus exists nowhere committed (the
   `fixtures/` dir is empty/untracked), unlike the marker fixture whose corpus is
   committed. The recorded field vector is reproducible, but the exact fixture bytes
   are unverifiable. A future receipt could pin the fixture file sha256s as the L1
   receipt does.
3. `control-junk-fixture.txt` records the command with `--revision <rev>` rather
   than the literal hash — consistent placeholder style, output verified.

## Residual risk

Low. The receipts' claims (red-before ×2, after ×2, old-c62 green defect + new-c63
red, junk red) all reproduce; counters' git-revision reads make pinned inputs
immutable; no post-commit receipt mutation exists. Remaining gap is confined to
ephemeral fixture rev pins (§4.1–4.2), which is disclosed and precedented.

No tools installed. Scratch `/fast/scratch/hyaku/kake-r63/ReviewerReceiptIntegrity/`
deleted. No files mutated outside this report.
Report: .ufo/waves/round-63/w1/ReviewerReceiptIntegrity.md
