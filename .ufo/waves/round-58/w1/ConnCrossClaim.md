# ConnCrossClaim

## PATTERN:

Sources read (all lane, read-only git): round-58 contract.md C1, round-58 C1 ledger draft
(`w1/ExecLedgerBuild.files/receipt-rewrites.json`), counter `c58_receipt_rewrites.py`, round-57
`receipt-errata.json`, `considerthese/2026-10-26.md` proposals 2/4/5, `SKILL.md` gate registry.

The four artifacts describe one object: **a lane claim about a past measurement, plus the bytes
that back it**. Each is a different projection of the same record:

1. Round-57 C1 errata (`receipt-errata.json` v1) — entries `{path, from, to, commit, note}`;
   `from`/`to` are revision labels that appear *inside* the receipt text. It discloses rewrites of
   the `revision:` line after the receipt's first commit (6 relabels, rounds 52/55/56).
2. Round-58 C1 ledger (`receipt-rewrites.json` v1) — events `{path, commit, status, fromBlob,
   toBlob, kind, note}`; `fromBlob`/`toBlob` are git blob ids, `kind` ∈ relabel/fill/rerun/
   append/format/delete/readd. This is the generalized event history; the errata's relabels are a
   subset of it (19 events total: 12 relabel, 6 rerun, 1 fill).
3. D3 / considerthese proposal 5 (historical-gate list) — gates that go red *by design* at the tip
   because their pinned values (rows/revisions) froze at an older measured revision (e.g.
   `c56_quote_truth.py` 6/8 on later trees). The claim stays true of the measured revision, not of
   the tip.
4. considerthese proposal 2 (receipt-rewrite watch) — a daily `git log --follow` over `controls/`
   files, flagging `revision:`/result lines changed after the first commit; the same event class
   the C1 counter walks, with a different traversal method (per-file `--follow` vs whole-ancestry
   walk).

Shared skeleton: every instance has (a) `path` — the byte carrier (receipt file, or gate row in
`SKILL.md`); (b) `measured_revision` — the revision the claim ran over (errata `from`; gate pin);
(c) `committed_at` — the commit that introduced the claim bytes (errata `to`); (d) `history` —
post-commit mutations with git-visible bytes; (e) a note naming resolvable evidence; (f) a truth
value at the checked tip that is only meaningful *relative to* `measured_revision`.

## CONTRADICTIONS:

None on the 6 shared events. Verified against the lane git (read-only):

- All 6 errata entries appear in the round-58 ledger with identical `(path, commit)` and
  `kind=relabel`: c1-ledger-real & c2-quote-real @ a4a890cf; after-c1-readme-index &
  after-c2-quote-truth @ 955e3d7b; after-c1-selftally & after-c2-quote-truth @ ad06cb8a.
- For each, the ledger's `fromBlob` == `git ls-tree <commit>^ -- <path>` and `toBlob` ==
  `git ls-tree <commit> -- <path>` (exact blob match).
- Blob contents carry the errata labels: `git show <fromBlob>` contains the errata `from` hex and
  `git show <toBlob>` contains the errata `to` hex for all 6. Sample diff (c1-ledger-real) shows
  the only change is the revision line `3a50ae4321e64856229c7cd0d39d3557b204d489` →
  `1ae8de5d4dee8300624b0db2a94497ff905942c5`.
- No ledger event sits on an errata path at any other commit; no errata entry is absent from the
  ledger.
- The remaining 13 ledger events (6 relabels + 6 reruns + the round-57 fill) are genuinely outside
  the errata's disclosure — consistent with the contract's "13 never disclosed".

Work-in-progress notes (not contradictions): the draft ledger still carries `note: "TODO"` for
every event (the contract and the C1 junk control require a resolvable evidence pointer, so
unpointed notes would fail the counter), and it lives in `w1/ExecLedgerBuild.files/`, not yet at
the counter's expected path `.ufo/waves/round-58/receipt-rewrites.json`. It contains 0 round-58
events, as expected (`new_rewritten=0`; `new_receipts` is separate).

## PROPOSAL: (for a later round)

One minimal shared record type whose fields are the union of the three existing projections:

```
{
  "schema": "kake-measurement-claim-v1",
  "claims": [
    {
      "id": "r55-after-c2-quote-truth",
      "kind": "receipt" | "gate",
      "path": ".ufo/waves/round-55/controls/after-c2-quote-truth.txt",
      "tool": "c55_quote_truth.py",               // identity, for gate runs
      "measured_revision": "faf9abe81d1ef5925733f756a918527483073fe8",  // errata `from` / gate pin
      "committed_at": "64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6",      // errata `to`
      "current_blob": "<sha at checked tip>",
      "history": [                                 // round-58 ledger events for this path
        {"commit": "955e3d7bd6d1eff5060e4cebbed51891bb53027a", "status": "M",
         "fromBlob": "4fd472c9c3a24e77ce2bf7a0dd79bcc5abf91521",
         "toBlob": "85cdf7b31f890236a04e41024a32241da370f42d",
         "kind": "relabel"}
      ],
      "pin": true | false,                         // declared historical pin (D3 / proposal 5)
      "note": "<resolvable pointer>"
    }
  ]
}
```

Why this suffices:

- `history` carries relabels, fills and reruns with git-visible bytes (round-58 C1 semantics);
  `measured_revision` + `committed_at` reproduce the errata semantics, and with `current_blob`
  let a check prove a relabel changed exactly the pin line, nothing else.
- `kind` + `tool` + `pin` let the same check run the named tool at `measured_revision` and at the
  tip: red-at-tip is expected-historical when `pin=true`, a regression otherwise. That covers the
  D3 / proposal-5 list without a separate artifact.
- The field set is a strict superset of the round-58 ledger; errata `from`/`to` map onto
  `measured_revision`/`committed_at`; `SKILL.md` gate rows already carry Name/Entry command/Verdict
  map/Self-test/Pinned-values cells, so `tool`/`pin` just formalize the existing implicit pattern.

A single future counter can then: (1) walk the ancestry for all receipt/gate paths and reconcile
with `history[]`; (2) run each tool at both revisions; (3) assert complete disclosure
(undisclosed=0), current blobs matching the committed claim unless the change is declared, and no
unexpected tip-red. This replaces three separate marks (errata, ledger, historical-gate list) with
one check. Round-58's frozen counters are untouched. Existing conventions to carry over: ASCII hex
only, status from git, and a note that must name a resolvable pointer (empty/`TODO` fails, as the
C1 junk control already does).

VERDICT: The round-58 C1 ledger and round-57 errata agree on all 6 shared events (same commit, same
from/to, exact blob match) — no contradiction; the three projections unify into one
`measurement-claim` record for a later round's single check.
