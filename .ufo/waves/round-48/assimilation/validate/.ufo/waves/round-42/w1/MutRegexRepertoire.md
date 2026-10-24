NOT MET — none of eight mutants met; all eight were killed by equality run A.

Axes: operability (URL-judgment equality and CPU); freshness unchanged. Mutation-probe results only, not a round verdict.
`S=/fast/scratch/hyaku/kake-r42w1/MutRegexRepertoire`; `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `C=$R/.ufo/waves/round-42/c42_count.py`.
Own rewrite: `$S/fast.py:76-87`, possessive repetitions of disjoint character runs/percent triplets, flattened path repertoire; remaining tool unchanged.
Rewrite SHA256: `96ecab8d8c1e5f5f479435fc0c82c1f593342044417149390052bd7c19e70ec7`.
Reference `$S/../../kake-r42/shared/tip41.py` (actual source `/fast/scratch/hyaku/kake-r42/shared/tip41.py`) SHA256: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
Counter SHA256: `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`; same counter and seed 424201 for pristine, every mutant and every restoration.

Exact counter-command template (all 17 fully expanded argv and observed exits are in `$S/commands.json`):
`timeout 900 prlimit --as=8000000000 -- env TMPDIR="$S/tmp" python3 -B "$C" --root "$R" --tool-file "$S/$tool.py" --label "MutRegexRepertoire-$label" --seed 424201 --out "$S/$label.json"`
Bindings: pristine `(tool,label)=(fast,pristine)`; mutant `(n,n)`; restored `(n,restored-n)` for every name n below. Mutant exits 1; pristine/restored exits 0. At most two counters concurrently.
Pristine receipt `$S/pristine.json`: equalRuns 8/8; ratios T1–T5 `[1.135,1.330,1.100,1.073,1.638]`; met true; every timing candRepsEqual 5/5.
Expected detector: changing one repertoire member should make A's exit/stdout comparison fail, independently of any cheaper CPU; observed exactly that for all eight.

Mutant artifacts retained at `$S/mutants/<name>.py`; active `$S/<name>.py` paths used by the counter have since been restored. Each mutant changes exactly the listed single character-class member on one line.
Receipts in this table are `$S/<name>.json`; ratios are ordered T1,T2,T3,T4,T5; every row met=false, exit=1, verdict=killed.
| Name | One-line change / archived source line | Mutant SHA256 | equalRuns | Ratios | Runs catching it |
|---|---|---|---|---|---|
| userinfo_drop_colon | userinfo class minus `:`; :80 | a61bda5242df97512c0cbdefd19efd31613159948f0a3cd344fa0e7d7371dd69 | 7/8 | 1.127,1.299,1.069,1.033,1.644 | A |
| host_drop_tilde | host class minus `~`; :82 | ec16485550990f854cd89f129a3718c1d340de9d52ad3078532087e62d042ac1 | 7/8 | 1.132,1.287,1.109,1.088,1.570 | A |
| path_drop_at | path class minus `@`; :84 | 2100af28da521e8678886efcd8ab83a50ffc12ad0630e44e5e60c5c154a2cd8c | 1/8 | 0.955,1.017,0.934,1.058,1.211 | A,B,C,T1,T2,T3,T5 |
| query_drop_slash | query class minus `/`; :85 | e4e7e6c69ba4eff92d17b7e416c05a9649f31c82a337a935a72e354edc15201d | 2/8 | 1.050,1.235,1.081,1.085,1.597 | A,C,T1,T2,T3,T5 |
| fragment_drop_question | fragment class minus `?`; :86 | 4674e40a7f4bdd1c07e0c67e45f5fad8a4dabacdf9e166c9de540e0695f2c148 | 2/8 | 1.061,1.256,1.053,1.041,1.512 | A,C,T1,T2,T3,T5 |
| host_drop_equal | host class minus sub-delimiter `=`; :82 | ddc965f60a830fa4328eb96afc596e4da40c5c25a7201b093f36ee6febb2156a | 7/8 | 1.080,1.325,1.100,1.074,1.682 | A |
| path_add_bracket | path class plus `[`; :84 | acab57f3bc63abba0d57fe52c5da08a319cfd082a1d6bc4e82a5e3be1ecc6683 | 4/8 | 1.151,1.402,1.127,1.064,1.603 | A,C,T1,T5 |
| fragment_add_hash | fragment class plus `#`; :86 | 1badc7cb1803e423e1bf9802e379a081bcf32b3875dd5691947e4aab743a0c04 | 7/8 | 1.135,1.322,1.091,1.052,1.663 | A |

Restoration: all eight active files restored byte-for-byte to the rewrite; before/after SHA256 both `96ecab8d8c1e5f5f479435fc0c82c1f593342044417149390052bd7c19e70ec7`; per-file byte equality and mutant hashes in `$S/restoration.json`.
Same bounded counter rerun on EVERY restored file; each equalRuns=8/8, met=true, exit=0, timing candRepsEqual=5/5 throughout. Receipt `$S/restored-<name>.json`:
| Restored name | Ratios T1–T5 |
|---|---|
| userinfo_drop_colon | 1.109,1.382,1.146,1.059,1.528 |
| host_drop_tilde | 1.118,1.294,1.086,1.070,1.620 |
| path_drop_at | 1.124,1.295,1.139,1.064,1.605 |
| query_drop_slash | 1.118,1.389,1.078,1.061,1.607 |
| fragment_drop_question | 1.088,1.271,1.117,1.043,1.671 |
| host_drop_equal | 1.108,1.294,1.127,1.080,1.662 |
| path_add_bracket | 1.115,1.277,1.089,1.082,1.674 |
| fragment_add_hash | 1.098,1.281,1.090,1.084,1.671 |

Own generated comparison: `timeout 180 prlimit --as=8000000000 -- python3 -B "$S/differential.py"` → exit 0; 58,002 values, 26,732 reference-accepted, zero `_parse_url` or regex-acceptance differences (`$S/differential.json`). Includes ASCII, percent sequences, non-ASCII/surrogates, randomized components, and lengths through 200,000.
Witness detector, identical logic across phases: `timeout 20 prlimit --as=8000000000 -- python3 -B "$S/witness_probe.py" --phase <phase>`; pristine exit 0/equal 8 of 8; mutated exit 1/equal 0 of 8; restored exit 0/equal 8 of 8. Exact tuples/None recorded in `$S/witness-{pristine,mutated,restored}.json`.
Witnesses in table order: `https://user:pass@example.com/a`, `https://a~b.example/a`, `https://example.com/a@b`, `https://example.com/a?b/c`, `https://example.com/a#b?c`, `https://a=b.example/a`, `https://example.com/a[b`, `https://example.com/a#b#c`. First six: reference tuple → mutant None; last two: reference None → mutant tuple.
Meeting mutant with witness: none found; all eight are genuine behavior-changing controls and all were detected, not merely rejected on speed.
Checked statements: generated rewrite equality holds on these samples; pristine CPU bound holds; eight-member mutant detection holds at seed 424201; exact restoration holds. Claiming universal equivalence or universal mutation coverage from this probe would be overstated.
Additional evidence commands: `timeout 10 prlimit --as=8000000000 -- python3 -B "$S/summarize.py"` → 0 (`summary.json`); `timeout 10 prlimit --as=8000000000 -- sha256sum /fast/scratch/hyaku/kake-r42/shared/tip41.py "$S/fast.py" "$C"` → 0, reference/rewrite/counter hashes unchanged.
Tooling: Python 3.14.8; no installs/updates, no network, no lane source edits. Three async submissions were refused by the global background-job cap and retried synchronously; no detector run was lost. Every started counter/probe exited; no owned process tree remains.
