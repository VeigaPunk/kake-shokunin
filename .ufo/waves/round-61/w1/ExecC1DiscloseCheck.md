# ExecC1DiscloseCheck

Round-61 w1 (build) · lane kake-shokunin · seat leaf · access date 2026-10-27 (UTC) · walked to base `9f07731a873585e655a6518233ea39f5d9fb8204` (first-parent chain, 371 commits). Independent re-implementation of the contract C1 rules in `ExecC1DiscloseCheck.files/walker.py` (read-only `git rev-list`/`ls-tree`/`cat-file` on a `--shared` scratch clone; worktree never read). Per-entry evidence in `ExecC1DiscloseCheck.files/entry-verify.txt`; machine-readable event list in `events.json`.

EVENTS FOUND: 12 (all kinds rewritten below; 11 `rewrite` + 1 `pending_filled` under Amendment-A1 semantics, see notes).

- `rewrite .ufo/waves/round-52/control/c1-ledger-real.txt a4a890cf1381a194891689dcbba0bf524350926b` — `revision:` line relabelled `3a50ae43→1ae8de5d` (the relabel lands in the same commit that introduced the receipt).
- `rewrite .ufo/waves/round-52/control/c2-quote-real.txt a4a890cf1381a194891689dcbba0bf524350926b` — same relabel pattern in the same commit.
- `rewrite .ufo/waves/round-52/control/c1-mutation-ladder.json 1ae8de5d4dee8300624b0db2a94497ff905942c5` — 18 `old_tail` `revision:` values re-pinned (span-matched lines).
- `rewrite .ufo/waves/round-52/control/c1-mutation-ladder.json a4a890cf1381a194891689dcbba0bf524350926b` — second re-pin of the 18 `old_tail` values.
- `rewrite .ufo/waves/round-52/control/c1-mutation-ladder.json fd91527a286086c1f4e6d4f44f715a907f041b5d` — third re-pin (round-53 commit).
- `rewrite .ufo/waves/round-54/controls/c1-selftest.txt 8e408e00fbe1c5908df62ba79e78c944bda479e2` — two `ok correction_*` rows appended; span changes only because each row carries `met=False`.
- `rewrite .ufo/waves/round-54/controls/c1-selftest.txt a631cc0246b97f2a949d61186c7466468faf94d6` — two more rows appended (`unrelated_marker`, `correction_removed_render`).
- `rewrite .ufo/waves/round-55/controls/after-c1-readme-index.txt 955e3d7bd6d1eff5060e4cebbed51891bb53027a` — `revision:` relabelled `faf9abe8→64c0ce12`.
- `rewrite .ufo/waves/round-55/controls/after-c2-quote-truth.txt 955e3d7bd6d1eff5060e4cebbed51891bb53027a` — same relabel in the same commit.
- `rewrite .ufo/waves/round-56/controls/after-c1-selftally.txt ad06cb8a17bda28f0691b95aecda13cd4708ea6c` — `revision:` relabelled `f8438a28→4cb225fb`.
- `rewrite .ufo/waves/round-56/controls/after-c2-quote-truth.txt ad06cb8a17bda28f0691b95aecda13cd4708ea6c` — same relabel in the same commit.
- `pending_filled .ufo/waves/round-57/controls/after-c1-receipt-pins.txt 20217f23eca15862febe14545523832e21584106` — first version (`31b61a4d`) was the bare word `pending`; `20217f23` replaced it with the real C1 line + `tip:` + `revision:` + `EXIT=0`.

COVERED: 12 of 12. Verified against the lane file `.ufo/receipt-disclosures.json` as it exists in the working tree (untracked, written by `ExecC1Disclose`, sha256 `71f9971bb962b9e054fa79f355f14fba6860f8b24d867a1c699950af4b276709`; byte-identical to `ExecC1Disclose.files/receipt-disclosures.snapshot.json` — see `registry-sha256.txt`). Every event's (path, commit) pair has an equal entry.

UNCOVERED: none.

PHANTOMS: none. For each of the 12 entries I verified independently: commit exists (`cat-file -t`=commit), is an ancestor of base `9f07731a` (`merge-base --is-ancestor`), the commit touches its path (`ls-tree` blob present in child), and the result span differs from the first parent's (`entry-verify.txt`).

NOTES:
- (c) Schema: the JSON parses; `schema` = `kake-receipt-disclosures-v1`; `entries` is a list of 12 objects each carrying string `path`, `commit` (40-hex), `kind` ∈ {`rewrite`,`pending_filled`}, `note`, `disclosed-by`; no missing fields, no per-entry extras. Extra top-level keys beyond the contract's `{"entries": [...]}` shape — `schema`, `note` — are self-describing and tolerated by the `ExecC1Tool2` draft parser (`doc.get("schema")`, `entries` list required).
- Receipt detection cross-count for amendment A1: 95 of 144 population files carry a receipt-grammar line in their first committed version (49 do not: round-37/40/48 JSON fixtures, census/selftest files etc.); identical count under first-version, any-version, and base-version grammar reads — consistent with A1's `receipts=95` and `undisclosed=12` at base absent a registry. Three independent extractions agree exactly on the 12-event set (mine, `ExecC1Disclose.files/events.json`, `ExecC1History.files/disclosure-candidates.json`).
- Kind note (not a coverage defect — matching is path+commit per contract): at `20217f23` the registry says `pending_filled`; the sibling tool's own event list says `rewrite`. Under the pre-amendment rule (pending tested inside the result span — the bare `pending` line is not a span line) it is a `rewrite`; under A1 (pending tested over the whole first version) `pending_filled` also fires. Registry kind matches A1.
- Pending sweep under A1 whole-version semantics: four other receipts contain `pending` in their first version (`drift-before.txt`, `sweep-after.txt`, `c1-selftest-v1.txt`, `c1-selftest-v2.txt`) but never lose it in a later version → no additional `pending_filled` events.
- `eaa9177e` (lane HEAD during w1) touches no population path — the event set at eaa9177 == at base.

VERDICT: C1 disclosures registry is complete and exact — all 12 independently-derived events covered by (path,commit)-equal entries, zero phantoms, schema parses as `kake-receipt-disclosures-v1`; the registry is a faithful mirror of lane history.
