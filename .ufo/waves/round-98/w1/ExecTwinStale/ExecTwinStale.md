# ExecTwinStale — round 98 C2 differential falsifier (report)

Target: differential falsifier of the C2 oracle, an independent twin written from the contract only.

## Method
- Read ONLY `LANE/.ufo/waves/round-98/stale-contract.md` and the RFC 5861 body. Did not read `c98_stale.py` or any `frozen/*.py` code. The frozen oracle `frozen/pos-oracle.py` was run only as a CLI (stdin JSON; rc 0 decided / rc 1 refused).
- Frozen-digest check: `sha256sum frozen/pos-oracle.py` = `bfb48d819d21cdca2c2b8ee579f2e319ddc0716c70275a65efac49a933faf8d1`, equal to the pinned line 11 of `controls/instrument-sha256.txt`. RFC 5861 body sha256 `1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e`, equal to the pin.
- `twin.py` written from the contract (stdlib only, Python 3.14.8, `python3`). Exit 2 reserved for twin internal errors (none observed).
- `gen.py`: independent seeded generator (malformed fields, quoted-strings with commas/escapes, duplicate directives, case variants, boundary ages, every error kind, dirty and clean families, malformed JSON, invalid UTF-8, BOM, duplicate keys, 5000-digit integers). Targeted cases carry expectations derived by hand from the contract; `TWIN!=EXPECT` and `ORACLE!=EXPECT` are reported separately.
- Both instruments run as subprocesses on identical stdin per input.

## Results (deliverable run)
Command: `python3 gen.py --count 2400 --seed 98 --work /fast/scratch/hyaku/kake-r98/ExecTwinStale --out <seat>`; rc=0 (observed). Log: `diff-run.txt`.
- inputs=2505 (targeted 105, random 2400)
- twin: decided=872 refused=1633 internal_errors=0; decisions: revalidate 388, error-through 130, fresh 112, not-an-error 195, serve-stale-revalidate 30, serve-stale-error 17
- match=2496 disagree=9
- expectation failures: twin=0, oracle=4 (the four int-limit inputs below)

Extra seeds (scratch corroboration, same generator, rc=0 each): seed 1 inputs=3105 disagree=6; seed 2 inputs=3105 disagree=11; seed 3 inputs=3105 disagree=8. Receipts: `diff-run-seed{1,2,3}.txt`.

## Classification (details and quoted contract sentences in `disagreements.md`)
- oracle-defect = 4: the oracle refuses valid 5000-digit integers with Python's 4300-digit conversion limit, surfaced as `invalid_input:` (rc 1). Three are 1*DIGIT delta-seconds the contract says to clamp (`swr-huge-clamped`, `swr-huge-clamped-inside`, `swr-leading-zeros-5000`); one is a 5000-digit `current_age` the contract does not list as refused (`big-age-staleness-exact`; contract states no magnitude bound, so the L1 may reclassify that row as contract-ambiguity).
- contract-ambiguity = 5: duplicate top-level `"event"` key. The contract is silent on repeated keys. Twin refuses (my policy); oracle takes last-wins. A scratch probe twin with last-wins matches the oracle on all such inputs (`probe-lastwins-output.txt`).
- twin-defect = 0.
- No format-bad outputs (exit-0 stdout not exactly one JSON object + newline, or exit-1 stdout non-empty / stderr not `invalid_input:`) appeared in any run.

## Self-caught slips (not instrument findings)
- Two of my own hand-derived expectations were wrong on the first run (`error-503-counts`, `error-504-counts`: correct answer `serve-stale-error`, inclusive boundary, staleness 50 ≤ 50). Both implementations returned it; I corrected the expectation. Not counted as disagreements.
- gen.py had an import-order slip and a stray indentation slip; both fixed. Neither touched the twin.

## Agreed interpretations (not contract-proven)
Listed in `disagreements.md` section D: null `shared`/`request_cc` refused; presence of `no-cache`/`must-revalidate`/`proxy-revalidate`/`s-maxage` regardless of value; invalid request `stale-if-error` falls back to response value; C1 U+0080–U+009F accepted in quoted-strings, refused outside; refusals take precedence over decisions; `staleness` reported on all decided paths. The L1 may want these pinned.

## Tooling
No tools installed. Used system `python3` 3.14.8 only. No pacman, no ~/.local/bin writes, no sysctl changes, no lane/fleet/git mutation.

## Scope notes
- Report location: the spec's `.ufo/waves/round-98/w1/ExecTwinStale.md` path sits outside this seat's directory, which the hard bounds forbid. I wrote the report inside `w1/ExecTwinStale/` instead; the L1 may copy it up.
- Scratch `/fast/scratch/hyaku/kake-r98/ExecTwinStale` removed after receipts were copied into the seat directory. Nothing else under `/fast/scratch/hyaku/kake-r98` was touched.
- Fixture-only probe file `probe-lastwins-twin.py` is a scratch variant, not a deliverable; it is retained only as a receipt.

## Reproduce
`cd <scratch> && python3 <seat>/gen.py --count 2400 --seed 98 --work <scratch> --out <seat>` (deterministic from seed). `python3 <seat>/gen.py --count 3000 --seed 1 ...` for the extra seeds.

EXEC-TWIN inputs=2505 disagreements=9 oracle_defects=4 contract_ambiguities=5
