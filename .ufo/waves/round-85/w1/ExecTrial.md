# ExecTrial — round 85 retained Referrer-Policy witness

## Axes and scope

Calibration: distinguish the experimental general classifier's syntactic verdict from field semantics. Freshness: independently derive the effective Referrer-Policy token from retained ordered fields. This is author-side domain preparation, not independent closure, a production-decoder test, publication approval, or full D84-queue closure. Assimilation: none.

Read host RULES.md, frozen contract and count.py before trial execution. Production remained read-only; no VCS mutations, dispatch, network requests, installs, builds, lint, formatters, selftests, or counters were run. No LSP tool is exposed in this seat's tool inventory; no production symbol refactor was attempted.

## Trigger → action → outcome → handoff

- **Trigger:** the r84 retained equivalent control reverses a Referrer-Policy list but its general classifier calls the change rewritten-equivalent.
- **Action:** independently implemented `retained_trial.py` under this seat's deliverable directory. It reads response headers in stored array order, selects matching field names case-insensitively, preserves field values and comma-token order, strips surrounding whitespace, then searches backward for the last case-sensitive recognized token. It imports no production decoder or classifier. It also invokes the r84 general classifier explicitly as an offline subprocess.
- **Outcome:** opposite lists have different effective policies, despite the general classifier's equivalence label. Both trial and r84 classifier exited 0; stderr was empty.
- **Handoff:** retain this concrete witness for L1's bounded C2 integration and semantic explanation. L1 owns candidate integration and post-integration gates; this trial does not contribute to the ten-case numerator or establish 10/10.

## Exact inputs and decoded result

A: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/a/ds4cc-sitemap/response.json`

B: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/b/ds4cc-sitemap/response.json`

| Side | Ordered field values (JSON) | Ordered tokens | Effective |
|---|---|---|---|
| A | `["no-referrer, strict-origin"]` | no-referrer → strict-origin | `strict-origin` |
| B | `["strict-origin, no-referrer"]` | strict-origin → no-referrer | `no-referrer` |

Each side contains one matching field, named `referrer-policy`, at zero-based response-header index 23. A's last recognized token is strict-origin; B's last recognized token is no-referrer. These are distinct tokens, not merely equivalent spellings. Exact input SHA-256 hashes and ordered extraction are retained in `trial-output.json`.

**Provenance limit:** these are real retained control files, not observations of a live policy change. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/build_control_pairs.py:4-13,30-37` describes synthetic header edits over round-81 retained captures, with bodies/digests untouched. No live target was contacted.

## Executed commands and exits

Scratch creation: `mkdir -p /fast/scratch/hyaku/kake-r85/ExecTrial` — exit 0.

Trial (cwd and TMPDIR both `/fast/scratch/hyaku/kake-r85/ExecTrial`):

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ExecTrial/retained_trial.py
```

Exit 0; stderr empty. Outer invocation metadata is retained in `trial-command.json`. Its JSON stdout is retained without tool-display truncation in `trial-output.json`.

The trial explicitly executed:

```sh
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py --a /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/a --b /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/capture-control/equivalent/b --declared /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture-expectations.json
```

Exit 0; stderr empty. Exact classifier stdout is separately retained in `r84-classifier.stdout.txt`, including:

```text
change surface=ds4cc-sitemap header=referrer-policy class=reordered
surface=ds4cc-sitemap changed=1 reordered=1 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-rewritten-equivalent
summary surfaces=3 changed=1 reordered=1 numeric_parameter=0 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-rewritten-equivalent
```

The classifier receipt includes hashes of its script, sibling header classifier and declaration input. No new production tool was required or executed.

Cleanup: `rmdir /fast/scratch/hyaku/kake-r85/ExecTrial` — exit 0; stdout/stderr empty; retained in `cleanup.json`. Scratch contained no generated artifacts and was removed after receipts were persisted.

## Defect, risks and limits

Observed semantic counterexample: an order-insensitive `Counter` comparison (`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/policy_value_class.py:55-60`) is sufficient for the frozen general grammar's `reordered` classification but not for Referrer-Policy effective-token equivalence. The existing script documents its frozen grammar rather than individual HTTP fields' richer grammars at lines 8-10. This report does not change its contract or claim that its exit 0 grants publication approval.

This independently implemented reference procedure was exercised only on the assigned retained pair. It is not a replacement CLI or proof of general unsupported-input handling, production implementation correctness, browser enforcement, C1 completeness, or C2's frozen ten-case score. No blockers. No tools installed or updated.

Report: .ufo/waves/round-85/w1/ExecTrial.md
