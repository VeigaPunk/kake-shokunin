Sibling-overlap scan for kake round-45 wave 1. Seat: ConnectorSiblingOverlap. Scan clock: 2026-10-24 00:16:28 local. Result: **no overlap found** (no contested write scope).

# Attack result

Named attack: other lane repos' current-round work touching (1) the `c44_audit.py` differential-counter audit family, (2) the `scripts/sitemap_audit.py` counter family, (3) kake corpus `SOURCES` repairs, plus the needles `receipt`, `witness`, `ledger_latest_check`.

**Pass on the negative:** no sibling newest wave, tracked tree, or commit since 2026-10-01 writes those surfaces. Generic `receipt` / `witness` hits do not co-occur with the precise needles inside claim docs (`also_precise=0` on every lane).

# Axes

- Adjacency (this seat): improved by separating name collisions from write conflicts. No sibling is in the r45 write set.
- Operability, freshness (lane claims C1/C2): not harmed. No foreign editor of `c44_audit.py` / `c45_*` / `sitemap_audit.py` / `kake-shokunin/corpus/SOURCES.md`.

# Evidence

## Decisive sweep (newest `.ufo/waves/round-*` per sibling, kake excluded)

Command (python3 + `rg`, sandboxes and retained-probes excluded from the precise count). Verbatim:

```
SWEEP_START 2026-10-24 00:16:28
newest_waves=19
PRECISE clean chousa-shokunin        round-37     files=0
PRECISE clean kagi-shokunin          round-28     files=0
PRECISE clean kaidoku-shokunin       round-34     files=0
PRECISE clean kama-shokunin          round-31     files=0
PRECISE clean kasegi-shokunin        round-23     files=0
PRECISE clean kengaku-shokunin       round-29     files=0
PRECISE clean kotoba-shokunin        round-63     files=0
PRECISE clean kotodama-shokunin      round-64     files=0
PRECISE HIT   kumitate-shokunin      round-51     files=4
    kumitate-shokunin/.ufo/waves/round-51/w2/SimplDedup.md
    kumitate-shokunin/.ufo/waves/round-51/w2/ConnOverlap2.md
    kumitate-shokunin/.ufo/waves/round-51/w1/ConnSiblingOverlap.md
    kumitate-shokunin/.ufo/waves/round-51/build/DistWave1/wave2-items.md
PRECISE clean lore-shokunin          round-103    files=0
PRECISE clean mado-shokunin          round-28     files=0
PRECISE clean mori-shokukin          round-21     files=0
PRECISE clean mori-shokunin          round-39     files=0
PRECISE clean revenger-shokunin      round-63     files=0
PRECISE clean souji-shokunin         round-22     files=0
PRECISE clean tabi-shokunin          round-22     files=0
PRECISE clean tameshi-shokukin       round-18     files=0
PRECISE clean tameshi-shokunin       round-35     files=0
PRECISE clean tsukuroi-shokunin      round-36     files=0
precise_file_total 4
```

Claim-doc filter (`*spec*.json`, `plan.md`, `contract.md`, `SCORECARD.md`, `claims.json`) for `receipt|witness`: every lane `also_precise=0`. Generic hit counts, not contests: chousa 1, kagi 254 (spec-named files inside a large tree; precise needles still 0), kaidoku 1, kama 1, kasegi 0, kengaku 2, kotoba 2, kotodama 4, kumitate 3, lore 0, mado 3, mori-shokukin 0, mori 1, revenger 2, souji 1, tabi 3, tameshi-shokukin 0, tameshi 2, tsukuroi 1.

## Filename sweep outside `kake-shokunin`

`find /home/vgpnk/Projects/shokunin -maxdepth 5` for `*sitemap_audit*`, `*c44_audit*`, `*c45_audit*`, `*ledger_latest_check*`, `*c44_count*`, `*c45_count*`, then drop `/kake-shokunin/`. Output was only `=== FIND DONE ===` (empty). Kake-local copies confirmed: `kake-shokunin/scripts/sitemap_audit.py`, `scripts/sitemap_audit_selftest.py`, `scripts/ledger_latest_check.py`. `c44_audit.py` is under `.ufo/waves/round-44/` (the maxdepth-5 find dropped it with the kake path filter).

## Tracked `git grep` and commit messages

`git grep -l -E 'c44_audit|c45_audit|sitemap_audit|ledger_latest_check'` in every sibling with `.git`, excluding kake:

- `kumitate-shokunin`: the same four round-51 files above.
- `tameshi-shokunin`: `.ufo/waves/round-32/w1/ConnectorOverlap.md` only.

`git log --since=2026-10-01 --all -i --grep='c44_audit|sitemap_audit|ledger_latest_check|c45_audit'` across siblings: no lane printed; trailer `=== DONE COMMITS ===`.

Fleet prompts for the live rounds (`chousa-round-38`, `mori-round-39`, `tsukuroi-round-36`, `revenger-round-63`, `kumitate-round-51`, `kotoba-round-63`, `kotodama-round-64`): no matches for those needles. `kake-round-45.md` mentions `SOURCES.md` only as the per-lane frontier contract, not a shared file.

## What the four kumitate hits actually say

They are citations that refuse a merge, not edits of kake bytes.

- `kumitate-shokunin/.ufo/waves/round-51/build/DistWave1/wave2-items.md:340` — "Keep nonce ledger distinct from kake r44's `ledger_latest_check.py` — same word, different family."
- `w1/ConnSiblingOverlap.md:75` quotes kake r44's `c44_audit.py` witness classes and `scripts/ledger_latest_check.py`. Line 125: do not call kumitate's walk "the receipt ledger" next to that checker.
- `w2/ConnOverlap2.md:17` and `:82` repeat the non-merge after kake r44 landed (`ledger_latest_check.py` vs kumitate `receipt-attest`). `:139`: scoring overlap by the heading "receipt-derived ledger figures" would false-contest a landed sibling.
- `w2/SimplDedup.md:286` restates item 89.

Kumitate's own frozen claim (`w1-spec.json`) is C1 `receipt-attest` (rule A51) and C2 `invocation-attestation` (rule D51). Different instrument, different repo.

Exact-path search for `kake-shokunin/(scripts/sitemap_audit|scripts/ledger_latest_check|corpus/SOURCES|.ufo/waves/round-4[45]/c4[45])` in sibling newest waves (json, sandboxes, retained-probes, `*census*` excluded): **one hit**, not a writer.

- `kasegi-shokunin/.ufo/waves/round-23/build/OverlapWeb.md:16-17` — kake `corpus/SOURCES.md` rows S018/S022/S024 are different documents from kasegi's same numbers (DebugBear vitals, Google canonicalization, WHATWG `base`). Also cites `kake-shokunin/scripts/freshness-sweep.mjs` fetching `ds4cc.com/sitemap.xml`. That is not `sitemap_audit.py`. Round-23 is the stale newest kasegi wave (not a 2026-10-24 live round).

## Live lanes, different claims (so the generic words are not this surface)

- mori r39 `contract.md:5-18`: `count-c7.py`, `tools/mori-sources-appendonly.py`, "fabricated-witness" payloads for drift-corpus C1. Not c44 witness classes.
- revenger r63 `build-spec.json`: revenger lane only; precise needles 0.
- kotoba r63: G9 closure + routed-repairs counter.
- kotodama r64: linguistics entry, `accept-o.py` / `accept-ca.py`.
- tsukuroi r36: five live tools' child env (their `tools/run-receipt.py` is a score harness; kumitate already separated it). Precise needles 0.
- chousa: no `.ufo/waves/round-38` directory anywhere under the lane (`find` empty). Newest wave is closed round-37 (claim-pin / pin-capture). `git log -3`: `95e33de` verifier spot-check, `e85ea21` round-37 claims, `b905217` freeze. Fleet prompt `chousa-round-38.md` has zero needle hits. Live peer `chousa-r38` therefore has no wave tree to read; treated as an absent artifact, not as overlap.
- tameshi current wave is round-35 (precise clean). The sitemap mention is historical: `tameshi-shokunin/.ufo/waves/round-32/w1/ConnectorOverlap.md:16` lists `sitemap_audit_selftest.py` among kake harness meta-tests and marks it "adjacent (seeded faulty cases, different audit gate)."

# Proposed move

One boundary, not a shared edit. When r45 writes the kake `SOURCES` lesson and any capability sentence:

1. Keep row ids lane-local. Kasegi already recorded that S018/S022/S024 are different documents (`OverlapWeb.md:16`). Do not "repair" kake rows to match another lane's numbers.
2. Do not rename the witness/ledger wording toward kumitate's "nonce ledger" or "receipt ledger". Their close item 89 greps the kumitate SCORECARD cell for `ledger_latest_check` and expects no hit. Kake's checker name staying `ledger_latest_check.py`, and the r45 driver staying the `c44_audit` / `c45_*` family, is what keeps the census from merging them.

No file outside this report was written. No tool installed.

# Risks

- chousa-r38 is dispatched but has no wave directory yet. This scan cannot see claims that appear only after `round-38/` is created. Re-sweep that dir if it appears; do not block r45 on it.
- Word-level grep of `receipt` or `witness` will keep false-contesting kumitate, mori, tsukuroi, kotoba, and chousa. The precise-needle plus path sweep is the discriminator. Kagi's 254 generic claim-doc hits are the cautionary case (precise count still 0).
- `freshness-sweep.mjs` fetching a sitemap URL (kasegi r23 note) is a different program from `sitemap_audit.py`. Folding them together would invent a conflict.

# Verification

Unrun by this seat, for the integrator: `rg -l 'c44_audit|c45_audit|sitemap_audit|ledger_latest_check' <sibling>/.ufo/waves/<newest-round>` should stay at the four kumitate citation files until a sibling actually opens those paths. This seat did not re-run kake `c45_matrix.py` or `c45_freshness.py`.

# Files written

- `.ufo/waves/round-45/w1/ConnectorSiblingOverlap.md` (this file only)

# Blockers

None. Absent artifact recorded: `chousa-shokunin/.ufo/waves/round-38` does not exist.
