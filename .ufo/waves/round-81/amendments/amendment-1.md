# Round-81 amendment 1 — two instrument corrections, before any after-state

Written 2026-11-04, after the freeze commit `a77b8a19c2b65a07dfbe40aaf7ec86aaeee2f9cb`
and **before any round-81 after-state existed**: `.ufo/waves/round-81/w1-results.json`
does not exist at this moment, so no C1 after-value, no share and no wave accounting has
been scored by anything. Predicates, item conditions, targets and the kill rules are
unchanged by this amendment; only an instrument's reading and a prose anchor are
corrected.

## A1 — C1's R80-4 counter counted empty-output seats as settled

**The divergence.** Contract §C1 and `.ufo/waves/round-81/make_accounting.py:35-37` both
say a seat whose output is empty does not count as settled. `c81_defect_queue.py`'s
`p_r80_4` did the opposite:

    settled = [r.get("name") for r in (results.get("results") or []) if isinstance(r, dict)]

Every row of `w1-results.json` counted — empty ones included — so the counter's
`settled_total`, `settled_attack` and `share` were computed over a larger population than
the contract declares. Consequence: a record written by the committed builder (honest
population) would open R80-4 as soon as any seat returned empty output, and — worse in the
other direction — the counter could print a green share that the contract's sentence calls
red whenever the two populations straddle the 0.25 floor.

**Found by** the wave's `ScribeLesson` seat, decided from bytes, before the carrier:
`w1/ScribeLesson/receipts/accounting-probe.txt` (builder prints `settled 2/5 share=0.400`)
and `accounting-probe.txt`'s companion `counter-formula-probe.txt` (the counter's formula
gives `3/6 share=0.500` on the same synthetic bytes).

**Correction.** `p_r80_4` now selects settled seats by non-empty output, exactly as the
contract sentence says:

    settled = [r.get("name") for r in (results.get("results") or [])
               if isinstance(r, dict) and isinstance(r.get("name"), str)
               and (r.get("output") or "").strip()]

and the selftest gains two fixtures: a green case where one attack seat's output is empty
and the record uses the non-empty population, and a mutant record that counts the empty
seat as settled (which must open the item). This is round-80's own amendment-2 pattern: the
predicate sentence is the claim; the instrument is corrected to implement it.

**Receipts re-cut** by this correction, all disclosed in
`.ufo/waves/round-58/receipt-rewrites.json`: `controls/base-c81-defect-queue.txt`,
`controls/ctl-c81-junk-queue.txt` (verdict lines unchanged) and
`controls/c81-selftest-c1.txt` (tally 13/13 → 15/15). The verdicts do not move: base
`open=6 met=false`, junk `open=6 met=false`.

## A2 — S454's anchor sections were wrong in this contract's prose

Contract §C1's Sources paragraph and `capture-expectations.json`'s `grounding.status`
string name "RFC 9110 §15.5.4/§15.5.5". In the retained body
`.ufo/waves/round-80/sources/rfc9110.txt` those sections are:

    7569:15.5.4.  403 Forbidden
    7587:15.5.5.  404 Not Found
    7667:15.5.11. 410 Gone

So §15.5.4 is the wrong anchor for an absent resource. **S454 anchors at §15.5.5 (404 Not
Found, line 7587) and §15.5.11 (410 Gone, line 7667)**; §15.5.4 is named in the lesson's
`## Gate` as the reject that grounds the correction. `capture-expectations.json`'s bytes are
frozen and stay unchanged — the counter reads only its `allowlist` and `checks`, and this
amendment plus the round lesson carry the correction. The manifest's per-surface
expectations are unaffected.

## A1 receipt outcome (measured, after the correction)

The three receipts were re-run against the corrected counter at commit
`0a27045e4b1b18ae521c9be508429262fdf993ca`. Two came out **byte-identical** — the base
control (`2346b4d6…`) and the junk control (`b03b3097…`) — because no item's verdict and no
detail line moved for them; they are re-runs, not rewrites, and need no ledger event. Only
`controls/c81-selftest-c1.txt` changed (`d1f71947…` → `209dab5a…`: two fixture lines added,
the tally `13/13` → `15/15`), and that one is disclosed in
`.ufo/waves/round-58/receipt-rewrites.json` with `kind=content`.
