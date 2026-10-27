# ReviewerQualityCriteria — round 63

## Findings

No actionable defect in the round-63 QUALITY criterion. It improves on round 62 by giving a runnable counter command and a concrete negative control that reproduces the routed defect, while keeping the rule scoped to frozen calibration counters and their `resolved` predicate.

## Evidence and comparison

- `corpus/QUALITY.md:1412` (round 62) states that a quote must substantively support its attributed proposition and grounds the concern in `corpus/lessons/round-61-verifier-spotcheck.md` (S432 admit/disagree) and retained Fetch §3.6. Its falsifier is a reviewer judgment about whether the quote identifies the header/check or is incorrectly used for a `nosniff`-only claim; it is not a runnable command. This is a reasonable semantic criterion, but less directly falsifiable than later executable criteria.
- `corpus/lessons/round-62-verifier-spotcheck.md`, “Discernment spot-check” and “Routed defects,” agrees that the new criterion was grounded and had a falsifier, and routes the separate marker-only counter false-green. `corpus/lessons/round-62.md:18–25` calls that defect “vacuous,” says no prior criterion caught it, and specifies the repair. Round 61’s outside verdict is explicit at `corpus/lessons/round-61-verifier-spotcheck.md`, “Discernment spot-check” (S432 Disagree) and “Routed defects”; round-61 `contract.md` records no corresponding QUALITY criterion, consistent with the outside spot-check’s finding that the disagreement had not yet been learned into one.
- `corpus/QUALITY.md:1416` (round 63) is grounded in the named round-62 routed defect and receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`; it also cites `corpus/lessons/round-63.md` §Mistakes. The criterion limits its claim to a frozen calibration counter’s `resolved` predicate, rather than general quote quality, research practice, or every counter. It requires committed-byte evidence, a frozen counter, and a failure on the actual marker-only attack, avoiding the round-62 defect’s marker-only false green.

## Falsifier run

Built a throwaway fixture under `/fast/scratch/hyaku/kake-r63/ReviewerQualityCriteria/fixture`, verified `git -C "$D" rev-parse --show-toplevel` returned that exact path before committing, and copied the committed fixture corpus byte-for-byte. All five fixture file SHA-256 values matched the committed corpus under `.ufo/waves/round-62/controls/false-green-fixture/corpus/` (including `QUALITY.md` `373b9d254dff8668…` and the round-61 spot-check `0a9a034861b19ba9…`). The generated fixture revision was `231b5fa4ea69b34dc8aac83525ce418236513b6f`.

Command, from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```sh
python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D" --revision "$REV"
```

Output: `revision=231b5fa4ea69b34dc8aac83525ce418236513b6f disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true`; exit 0.

Round-63 criterion falsifier:

```sh
python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"
```

Output: `revision=231b5fa4ea69b34dc8aac83525ce418236513b6f disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`; exit 1. This matches the criterion’s expected result and demonstrates the old counter’s false-green on the same bytes. The fixture directory was removed after the run (`scratch cleaned`).

Also exercised the actual measured-revision and base commands:

- `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` → `... derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`; exit 0.
- `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa` → `... derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false`; exit 1.

The frozen inputs also match the stated digests: c63 calibration counter `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`; `scripts/quote_class.py` `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`; quote-class ledger `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`. Ledger row S432 records `collapsed-only` and both retained-blob digests; `corpus/knowledge/response-header-expectations.md:222–250` contains the round-63 correction and class explanation. The round-63 C2 base/after receipts separately show `present=0 … met=false` and `present=1 selftest=4/4 frozen_cases=ok met=true`.

## Residual risk and verification gaps

The criterion’s command is runnable, but its `<fixture>` and `<fixture rev>` placeholders require the documented setup: copy the marker-only corpus into a throwaway Git repository, commit it, then pass that revision. The committed fixture directory itself is not a Git repository. The setup and byte identity are recorded above and in the round-62 receipt, so this is a modest discoverability/setup requirement rather than an unfalsifiable criterion.

One bounded implementation caveat: `c63_calibration.py:147–150` checks the presence of `substantive`, `round-61-verifier-spotcheck.md`, and purpose terms anywhere in `corpus/QUALITY.md`; it does not parse or bind the round-63 criterion heading specifically. This does not invalidate the round-63 criterion’s own runnable marker-control falsifier, but the counter’s `criterion` field alone should not be treated as semantic validation of the entire QUALITY criterion.

No code, counter, contract, receipt, or corpus file was edited. No install was performed.