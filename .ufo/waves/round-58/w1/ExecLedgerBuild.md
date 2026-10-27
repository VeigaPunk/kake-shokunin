# ExecLedgerBuild

Claim C1 (calibration — receipt rewrites disclosed). Built the candidate disclosure ledger mechanically from git at
base `044048597d62f3199494b63b36e90dd57825e350`, then proved it against `c58_receipt_rewrites.py` in a shared clone.

## SCRIPT:

`.ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py` (stdlib only; 106 lines).
`importlib.util.spec_from_file_location` loads the counter by path from `<root>/.ufo/waves/round-58/c58_receipt_rewrites.py`
and imports `events` + `classify`; no hash is ever typed by hand.

    build_ledger.py --root <lane> --revision <rev> [--note TEMPLATE] [--out FILE] [--verify]

* events come from `counter.events(root, tip)` (oldest-first, `--no-renames --first-parent`, receipt paths only);
* every entry carries all seven counter `FIELDS`: `path, commit, status, fromBlob, toBlob, kind, note`;
* `kind = counter.classify(status, blob(fromBlob), blob(toBlob))`;
* `note` defaults to the literal `TODO` (L1 merges the scribes' notes); `{path}` in `--note` expands to the entry's
  receipt path, which is how the `see <receipt path>` proof variant was generated — same script, one flag;
* unresolved revision → exit 2; `--verify` additionally runs `counter.measure()` and propagates its verdict.

Exit 0 written, 1 (`--verify`) not met, 2 unevaluable, 64 usage. Two consecutive builds at base are byte-identical
(`cmp` clean) — no dependence on mtimes, locale or dict order.

## LEDGER:

`.ufo/waves/round-58/w1/ExecLedgerBuild.files/receipt-rewrites.json` — 19 events, `"schema": "kake-r58-receipt-rewrites-v1"`.
Verbatim entries (one per line for compactness; the file itself is `json.dumps(indent=1)` of the same values):

```json
{"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "1ae8de5d4dee8300624b0db2a94497ff905942c5", "status": "M", "fromBlob": "69a045918a98b0a19abcc068eda6063083976afa", "toBlob": "9a95330d6e14f1db5daa7d03102fd626c92f3cc2", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-52/control/c1-ledger-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "bd10242546748d4b53c1e0320ae9224fab726c95", "toBlob": "ce0e0394aef9e93454373799d4c36cf05b5208f3", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "9a95330d6e14f1db5daa7d03102fd626c92f3cc2", "toBlob": "23252321f30d92a90dd85351e2057833e6388350", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-52/control/c2-quote-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "a7b5d69484beceed9cecf2cb19a38e4fd65a6f53", "toBlob": "aee2e7d949ce6074f6da105dfc25aa0ac248cf50", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-52/control/c2-quote-selftest.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "ad318495b0b7ca4ef3ee62789d09189b0d79402b", "toBlob": "907047dd6ed29914b2d84c8ca2c6fac1db1cab8d", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "fd91527a286086c1f4e6d4f44f715a907f041b5d", "status": "M", "fromBlob": "23252321f30d92a90dd85351e2057833e6388350", "toBlob": "d13c735262629ce56ceb89c247c6567f0dc786bc", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-54/controls/c1-selftest.txt", "commit": "8e408e00fbe1c5908df62ba79e78c944bda479e2", "status": "M", "fromBlob": "812bc1caf3d24212e03e89ff2b4801eadba83b19", "toBlob": "3f66acc2a744bc06653d57dd563bbbba56d5d175", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-54/controls/base-c1-s374.txt", "commit": "a0a4fd482700110600b0327c2fce1a270b272136", "status": "M", "fromBlob": "f4cf6d5e334fb437dc3c9c69e8b58db706c78c04", "toBlob": "661b6bd740b08d42734dd8c1b4bd1b0a21cfe407", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-54/controls/base-c2-ops-debt.txt", "commit": "a0a4fd482700110600b0327c2fce1a270b272136", "status": "M", "fromBlob": "559bf9ba22ab5fee698afc3897d0e013feb5aa11", "toBlob": "67a6902af5d611155cc6d8fdcbdcc94a031ebdc7", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-54/controls/c1-selftest.txt", "commit": "a631cc0246b97f2a949d61186c7466468faf94d6", "status": "M", "fromBlob": "3f66acc2a744bc06653d57dd563bbbba56d5d175", "toBlob": "15d76dc6e17dbcf59e1c7d5a8952e1607d6ddb70", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-54/controls/sources-census.txt", "commit": "5826682b37811470980b3f263e148dd5292d8026", "status": "M", "fromBlob": "350215f3013cf42528fc098c6906effab1799408", "toBlob": "9fadd501bfb39591f627165e8e69ad48902d2bd4", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-55/controls/c1-selftest-v2.txt", "commit": "64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6", "status": "M", "fromBlob": "77c713ecd9262b019ec54a9bc4c7a40c565edfcc", "toBlob": "39f9bb85393c1096d10cef9d122effcffa0f7848", "kind": "rerun", "note": "TODO"}
{"path": ".ufo/waves/round-55/controls/after-c1-readme-index.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "status": "M", "fromBlob": "05ce598c8f6039ed77a24fc4e21a7668e82a0c11", "toBlob": "5b1c9c6e01dc689883c49c933217f27bfee2a7b5", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-55/controls/after-c2-quote-truth.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "status": "M", "fromBlob": "4fd472c9c3a24e77ce2bf7a0dd79bcc5abf91521", "toBlob": "85cdf7b31f890236a04e41024a32241da370f42d", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-55/controls/c2-selftest.txt", "commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "status": "M", "fromBlob": "6a028ccb4dcd1c9774acb673298f61d7e2d616e2", "toBlob": "85430aabd7d1d3986449a371dc64b43d4931be27", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-56/controls/after-c1-selftally.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "status": "M", "fromBlob": "23043b22469e9a90f40fcdfa28ab6c4a1c590f3a", "toBlob": "913e60244240603f53bf598e7663d3b2e3486750", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-56/controls/after-c2-quote-truth.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "status": "M", "fromBlob": "236f6238f11c4ed8be66da126b2b56edaa7255c9", "toBlob": "ce5a87958f844740a1b9d04ab563c7eaa2dd856a", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-56/controls/c2-selftest.txt", "commit": "ad06cb8a17bda28f0691b95aecda13cd4708ea6c", "status": "M", "fromBlob": "f96bb110a3d31dcc42ada9139ca321e803f10b42", "toBlob": "1cfd5667817ebafb4deda77ef7ae24cd1fc6415f", "kind": "relabel", "note": "TODO"}
{"path": ".ufo/waves/round-57/controls/after-c1-receipt-pins.txt", "commit": "20217f23eca15862febe14545523832e21584106", "status": "M", "fromBlob": "417ca0c615baecf6dbba1c4f5c9df3079ee4516a", "toBlob": "b514c80d7f367a02415d7fb11915a54eed6b809d", "kind": "fill", "note": "TODO"}
```

Kind histogram: relabel 12, rerun 6, fill 1. All 19 statuses `M`; no `D`/`A` receipt event exists in the base ancestry.
`note` is `TODO` in all 19 on purpose: the counter's `unpointed` clause fails until the notes are merged, which is the
L1's step (a note is a human statement, not a derivable value — the script never invents one).

## PROOF RUN:

Scratch clone `/fast/scratch/hyaku/kake-r58/ExecLedgerBuild/l` (`git clone -q --shared`), checked out at base
`044048597d62f3199494b63b36e90dd57825e350`; `rev-parse --show-toplevel` verified before the commit.

Fixture note: at the base revision `.ufo/waves/round-58/` is **untracked** in the lane (`git ls-tree` at base returns
nothing for that prefix), so the clone also needed the counter itself copied in for `build_ledger.py --root <clone>`.
The counter is not a receipt path, so that first addition is not an event and does not affect any count.

Commit `8d41cdc6d4d933b9879ef0f93cd40bc924b6fffd` (selftest identity) = 19-entry ledger with `note` replaced by
`see <receipt path>` (generated by the same script: `--note 'see {path}'`) + `.ufo/waves/round-58/controls/after-c2-x.txt`
+ `.ufo/waves/round-58/controls/after-c3-x.txt`.

    C1 receipt-rewrites events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=2 met=True
      ledger: .ufo/waves/round-58/receipt-rewrites.json present (19 entries)
      revision: 8d41cdc6d4d933b9879ef0f93cd40bc924b6fffd
    EXIT=0

`met=True`. Full transcript: `ExecLedgerBuild.files/proof-run.txt`; the note-bearing ledger:
`ExecLedgerBuild.files/receipt-rewrites.proof-notes.json`. Checked structurally: the tracked and the TODO ledger are
equal on `path/commit/status/fromBlob/toBlob/kind` for all 19 entries and differ on `note` only (19/19).

## CORRUPTIONS:

Three isolated `git worktree add --detach` checkouts of `8d41cdc`, one single-field corruption each, one commit each,
counter re-run (`ExecLedgerBuild.files/corruptions.txt`). Each turned `met=False`, on exactly the intended clause:

| corruption | commit | counter line | exit |
|---|---|---|---|
| toBlob of entry 1 → `000…0` | `bca2ba2ce7b38b50f95142f8826b9a62fe26868f` | `undisclosed=1 phantom=1 … met=False` | 1 |
| kind of entry 1 `relabel` → `rerun` | `e220be30dd403dca2f76b52697c5c01de4e4ed4b` | `wrong_kind=1 … met=False` | 1 |
| note of entry 1 → `"x"` | `9376bcc9ce133833a803bc13f4383f553fa43a43` | `unpointed=1 … met=False` | 1 |

Every other counter cell stayed at its passing value in all three runs (`events=19`, `malformed=0`, `new_rewritten=0`,
`new_receipts=2`), so the failure is attributable to the corrupted field alone and not to fixture drift.

## Risks / notes

* `kind` is produced by the same `classify` the counter grades with, so kind-correctness is correct-by-construction
  rather than independently cross-checked; a genuine second reading of the 19 blob pairs is another seat's job
  (`ExecEventsIndependent` is in this wave). The values themselves (path/commit/blobs) are independent: they come from
  `git log`/`ls-tree` at the measured tip, which is why the wrong-`toBlob` corruption is caught as phantom+undisclosed.
* The ledger must be committed at the final tip *together with* both control receipts; `new_receipts == 2` is part of
  the same predicate and the two dummy files here are proof scaffolding only, not the real receipts.
* Once the L1 replaces `TODO` with the scribes' prose, re-verify with `build_ledger.py --verify` (or the counter):
  the notes must name a path that exists at the tip, or a commit that resolves — `note` is the only field the script
  cannot derive.
* Scratch `/fast/scratch/hyaku/kake-r58/ExecLedgerBuild` deleted after copying the receipts. Nothing in the lane was
  written except `.ufo/waves/round-58/w1/ExecLedgerBuild.files/` and this report; no lane git/jj mutation.

VERDICT: ledger built mechanically from git at base (19 events, kinds relabel 12 / rerun 6 / fill 1) and proven — met=True on the note-pointing clone, met=False on each of three single-field corruptions.
