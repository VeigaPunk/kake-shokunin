## Verdict

Counterexample found: **none** against the paired `4/8 → 8/8` evaluator result or the four newly evaluated verdicts. It is a fair *same-input validator replay*, with the qualification below: `before` means the old validator replayed on the current frozen sample, not a historical C2 sample from `b539cc1`.

## Findings

None (no P0–P2 defect found).

**P3 framing qualification — do not present this as a historical surface-state delta.** Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/evaluability.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --before b539cc1 --after 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd
```

Exact summary output:

```json
{"served": 8, "evaluated": {"before": 4, "after": 8}}
```

`evaluability.py` loads only `scripts/canonical_audit.py` from each requested revision. It reads the population and page/fetch files from `--root`, copies each page once, and constructs one manifest with one `fetch.finalUrl` and one `expectedCanonical` before running either validator (`evaluability.py:31–58`). Thus both sides receive the same bytes and expectations. The working tree has no differences in the population/live snapshot paths or evaluator relative to `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`; the `c2-population.json` itself is added between `b539cc1` and the candidate. This is therefore a controlled old-validator-vs-new-validator replay on the candidate's sample, not evidence that the 4/8 state was observed at the old revision.

**Impacted claim/axis:** C2 / operability evidence framing only. Smallest safe correction is to label it “old vs new validator on the same candidate snapshot”; do not add a third operability claim or change C2's numerator.

## Checked and held

- The four rows changing from `could-not-evaluate` were `ds4cc-primary` and `plazir15-ghp` → `clean`; `ds4cc-kimi` and `burnerchrome-kimi` → `failed-policy` (`canonical_missing`). The other four served rows keep their verdicts. “Evaluated” includes policy failures; it does **not** mean all eight pages pass policy.
- The validator diff from `b539cc1` to the candidate adds support for post-head SVG/MathML and self-closing HTML void elements. The changed snapshots use ordinary closed heads and browser-standard cases: the two clean pages have their canonical links in the head; Plazir-15 has seven body SVG elements. The two Kimi pages have no canonical link in the served HTML; their existing links are icon/preload/style links.
- Browser-parity probe: in an offline Chromium tab, passed the four exact snapshots as strings to `DOMParser.parseFromString` (no page scripts or remote requests). Chromium's parsed DOM kept the `ds4cc-primary` and `plazir15-ghp` canonicals as direct head children, found no canonical links for either Kimi page, and parsed the observed body SVGs (0/7/0/1 respectively). These browser parse results agree with all four new verdicts; no newly evaluated result relies on a non-browser SVG/void-tag behavior.
- Reproduced C2 with:

  ```text
  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd
  ```

  Exact count: `accepted: 12`, `total: 12`. The receipts include clean, failed-policy, and not-served verdicts, as C2 defines reproducibility—not universal canonical-policy success—as its acceptance criterion.
- The contract contains C1 and C2 only. Keep the 4/8 → 8/8 as a diagnostic subordinate to C2; the contractual C2 result remains 12/12 reproducible receipts across the full population.

## Limits

This check is about static snapshots and the offline browser's HTML tree construction only. It does not execute page scripts, test search-engine canonical selection, or infer runtime DOM mutations. The old side is a replay of the old validator against the candidate's fixed sample, not a historical live-page measurement from `b539cc1`.