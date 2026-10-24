# RerunC1Sealed — re-run C1 sealed counter vs committed receipts (wave 2, falsify)

Seat: KakeR36.RerunC1Sealed. Axes: freshness, operability. Result: **CLEAN — no finding.**

## Attack
Re-ran the exact counting command for the four named revisions in a fresh sandbox clone at
f3a38bf8e68f6cee386125d34b5e95ac9b2df66e and diffed every emitted JSON field (incl. all 28
`perCase` entries) against `verification/c1-keyrev-at-*.json`. Also verified the tool hash
identity and the key-hash constant.

## Sandbox
`git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r36w2/RerunC1Sealed/clone`
then `git checkout -q f3a38bf8...` (HEAD verified = f3a38bf8). `TMPDIR=/fast/scratch/hyaku/kake-r36w2/RerunC1Sealed/tmp`. bwrap 0.13.1 present at /usr/bin/bwrap. No installs needed.

## Commands (run under `timeout 300`, stdout to sandbox, one fact per line)
`python3 -B <lane>/.ufo/waves/round-36/sealed_count.py --root /fast/scratch/hyaku/kake-r36w2/RerunC1Sealed/clone --revision <REV> --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8`

| --revision | my exit | receipt `.exit` | output vs receipt (`diff -u`) |
|---|---|---|---|
| 4d5b3d550748e5b52af31646b74c1aa435942bde | 0 | 0 | IDENTICAL (passed=28, met=true, toolSha256=577b2d7d…510d48) |
| b720d799ae99c19a7c97f2b1391d4fe928be0e11 | 1 | 1 | IDENTICAL (toolPresent=false, passed=0, met=false) |
| cd3212796cab7a2afa03b638dbfafe7194df9629 | 1 | 1 | IDENTICAL (toolPresent=false, passed=0, met=false) |
| fd1fb723624b742a00a6e8e908f3b42901d627f8 | 2 | 2 | IDENTICAL (`{"error": "key visible at the measured revision"}`, no perCase) |

`diff -u` byte-identical on all four ⇒ claim, predicate, counterSha256, revision, toolPresent,
toolSha256, cases, passed, target, met and every `perCase` {id,passed} element match field by
field. Spot-verified: perCase_n=28 and all true only at 4d5b3d55.

## Hash identity checks
- `git -C clone show 4d5b3d55:scripts/source_recheck.py | sha256sum` → `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48` (== wave-1 deliverable hash).
- Same command at f3a38bf8 → same hash ⇒ tool unchanged between build commit and lane head.
- `sha256sum <lane>/sealed_count.py` → `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e` == `counterSha256` in all receipts (v3).
- `git show fd1fb723:.ufo/waves/round-36/sealed/cases.json | sha256sum` → `44c94838f31af6740a3f1bb4123abe6cbb8df0bbdd3414de7acbb3838863ef1d` == `KEY_SHA256` in sealed_count.py:12.

## Notes on refusal path
The key-visible guard (sealed_count.py:193-196) fires before tool extraction, bwrap spawn or
key load, so the fd1fb723 run is a pure refusal: exit 2, error JSON, zero mutation — matches
the documented "refuses a revision holding the key" contract.

## Evidence
- My outputs: /fast/scratch/hyaku/kake-r36w2/RerunC1Sealed/run-{4d5b3d55,b720d799,cd321279,fd1fb723}.json
- Receipts: .ufo/waves/round-36/verification/c1-keyrev-at-{4d5b3d55,b720d799,cd321279,fd1fb723}.{json,exit}
- Counter: .ufo/waves/round-36/sealed_count.py (refusal :193-196, output :230-235)

## Not verified / residual risk
- Did not re-derive expected case outcomes from `sealed/cases.json` semantics or audit the
  judge/projection logic for soundness — only that committed receipts reproduce deterministically.
- Determinism is strong here (perCase ids come from the key, fresh uuids never reach output);
  a second identical run is expected, not a coincidence to flag.
