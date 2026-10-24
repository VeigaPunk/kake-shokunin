## Verdict

**Counterexample found.** The post-wave-1 rule is an honest *stricter guard* against the all-`UNVERIFIABLE` saturation attack: it leaves the frozen 17-unit population unchanged and only removes passes. It is disclosed in `measure_c1.py`, and the C1 critique that motivated it preceded integration. However, this is a post-freeze predicate change, not the exact predicate stated by the frozen contract, and the counter still accepts wholly synthetic `HOLD` receipts as 17/17. Thus the tightening fixes one escape hatch but does not make the reported count proof of live re-verification.

The rewrap fallback does admit real line-wrap-only anchors that strict substring matching would reject; I found no non-whitespace mismatch in those cases. All three entries in `rejected.json` are correctly rejected: each differs from the base text by Markdown punctuation/markup, not just whitespace.

## Findings

### P1 — One synthetic `HOLD` per unit still yields a C1 pass

**Exact command** (selftest isolated under `/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA`; its disposable Git clone was created with `--no-hardlinks`):

```sh
TMPDIR=/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA/tmp python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/counter_selftest.py
```

**Exact observed output excerpts:**

```json
{"accepted": 17, "case": "C1 valid receipts", "command": ["/usr/bin/python3", "-B", "/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA/tmp/kake-r23-counter-selftest-d2uknrb_/repo/.ufo/waves/round-23/measure_c1.py", "--root", "/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA/tmp/kake-r23-counter-selftest-d2uknrb_/repo", "--revision", "282584cc9be290aa1fe6d285848cbd89e8aa9399"], "exit": 0, "expectedAccepted": 17, "expectedExit": 0, "passed": true, "total": 17}
{"accepted": 16, "case": "C1 all-UNVERIFIABLE receipt rejected", "command": ["/usr/bin/python3", "-B", "/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA/tmp/kake-r23-counter-selftest-d2uknrb_/repo/.ufo/waves/round-23/measure_c1.py", "--root", "/tmp/kake-r23w2-KakeR22Recovery.CritCounterTightening-2-lUxA/tmp/kake-r23-counter-selftest-d2uknrb_/repo", "--revision", "5a51eef6c48e12d5ad6f35611291dab9337147c5"], "exit": 1, "expectedAccepted": 16, "expectedExit": 1, "passed": true, "total": 17}
```

The C1 selftest fixture in `counter_selftest.py:65-100` deliberately seeds just one claim per unit with `claim: "Synthetic claim for the counter selftest."`, `surface: "fixture://c1"`, `method: "read"`, `observation: "Synthetic fixture observation."`, and `verdict: "HOLD"`; the counter accepts it for every unit. The all-unknown test confirms the new check rejects that one degenerate pattern, but one unsubstantiated `HOLD` replaces it without any live check. The field validator requires non-empty strings, not an observable surface or reviewable evidence.

**Impacted claim/axis:** C1 / freshness. `accepted: 17` can be obtained without live re-verification; it currently proves the population has structurally acceptable receipts plus one `HOLD`/`STALE` label per unit, not that the observation occurred.

**Smallest safe correction:** Do not use this structural counter alone as proof of freshness. Require independently reviewable evidence tied to the decisive claim's actual surface and method, or label the result strictly as receipt/structure coverage and keep live-verification status separately reviewable.

### P2 — The tightened predicate is stricter than the frozen C1 wording

**Exact command:**

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --quiet 6847479d404d1dd93ecb59f99ff735bd7f010a4a 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd -- .ufo/waves/round-23/contract.json .ufo/waves/round-23/c1-population.json && printf 'contract_and_population_unchanged_since_freeze\n'
```

**Exact output:**

```text
contract_and_population_unchanged_since_freeze
```

The frozen contract still says `UNVERIFIABLE (surface gone) counts as re-verified only with a reason`; the later counter additionally rejects a unit whose claims are all `UNVERIFIABLE`, even when every one has a reason. The gate was added in the integration commit as a response to the identified saturation defect, and it is stricter, not a denominator change. The same population digest (`ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf`, 1,730 bytes) was present at freeze commit `6847479`, integration commit `83098b5`, and candidate `5e5afb9`.

**Impacted claim/axis:** C1 / freshness measurement semantics. The current 17/17 is a post-freeze, stricter-code result; it should not be described as an unchanged run of the contract's original acceptance predicate. This change does not inflate the current result, but it can reject an all-unverifiable unit that the frozen text allows with reasons.

**Smallest safe correction:** Keep the frozen population and report this as a separately disclosed stricter gate (or explicitly version the criterion change); do not silently conflate it with the frozen contract predicate.

## Checked and held

- Ran the candidate counter exactly as specified: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`. Exact summary: `accepted: 17`, `total: 17`, `claimVerdicts: HOLD 79, STALE 49, UNVERIFIABLE 40`; every unit row had `pass: true`. Each unit has at least one HOLD or STALE, so the new condition changes no row in this frozen candidate.
- The counter's embedded population hash matches the identical population bytes at freeze, integration, and candidate. The 17 entries remain the 16 historical-not-live-reverified knowledge units plus `SKILL.md` property map; no denominator or population substitution was found.
- Applied the integration fallback to every wave-1 `Reverify*.md` / `Surface*.md` JSON anchor against the base blobs. There are 17 matches that fail strict substring matching but succeed after `anchor.split()` tokens are joined with `\s+`; each matched base excerpt differs only in line wrapping/indentation, and none spans a blank line. The implementation then stores `match.group(0)`, i.e. the exact matched base text.
- The fallback is broader than soft wrapping: the exact probe `python3 -c 'import re; a="alpha beta"; p=r"\s+".join(re.escape(t) for t in a.split()); print("soft_wrap="+str(bool(re.search(p,"alpha\nbeta")))); print("paragraph_break="+str(bool(re.search(p,"alpha\n\nbeta")))); q=r"\s+".join(re.escape(t) for t in "CNAME file".split()); print("punctuation_change="+str(bool(re.search(q,"`CNAME` file"))))'` printed `soft_wrap=True`, `paragraph_break=True`, `punctuation_change=False`. Thus it accepts any whitespace run, including a Markdown paragraph boundary, but no actual normalized anchor in this candidate used a blank line. If the intended equivalence is specifically a soft rewrap, the smallest guard would exclude blank-line separators.
- For the three `rejected.json` anchors, the direct base-blob probe printed `exact=False; whitespace_match=False` for all three. Base text has `**three**` in the fire-journal claim, backticks around both Plazir hostnames in the mirror-pitfalls claim, and backticks around `CNAME` in publish-channels; those are non-whitespace differences omitted from the rejected anchors. Rejection reason `anchor not in unit at base` is therefore correct.

## Limits

No public HTTP GET/HEAD was performed and no claim truth was independently rechecked. The counter selftest is local and intentionally synthetic; it demonstrates the validator's acceptance boundary, not the truth of any wave-1 observation. No production files other than this requested report were written; no builds, lint, or formatters were run; no tools were installed.