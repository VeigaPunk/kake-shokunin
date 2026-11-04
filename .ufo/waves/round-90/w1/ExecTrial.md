VERDICT: C2 holds on real data (5/5 seeds met=true; 48/48 capture cases agree); the gate's advisory `utf8-required` gap is an artifact of the gate's own harness environment, not a property of the candidate.

# ExecTrial — round 90 real-data trial of the gate and the candidate

Seat ExecTrial (leaf; no dispatch, no labrat used). Lane HEAD `79e1aac2`; `scripts/` clean in the
working tree. The candidate and gate bytes are unchanged from the C2 carrier
(`git diff --stat 7f6c68f1 HEAD -- scripts/cache_key.py scripts/cache_key_conformance.py` is empty).
- `scripts/cache_key.py` sha256 `3a658326714108ebec8f26c6dfcff9007ad781915b909616e9313d664e7da996` (last touched in `9784ad54`, round 89)
- `scripts/cache_key_conformance.py` sha256 `2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591` (`7f6c68f1`)
- Host: Python 3.14.8, 32 CPUs, host locale `LANG=en_US.UTF-8`.

All receipts are under `.ufo/waves/round-90/w1/ExecTrial/receipts/`. Scratch
`/fast/scratch/hyaku/kake-r90/ExecTrial/` held the working copies and was deleted before yield.
I made no fixture clone, no git mutation, no network GET and no production edit.

## 1. Gate on the candidate, 5 seeds, `--generated 600`

Command (per seed, `--work`/`TMPDIR` = scratch, `--verbose`, default `--jobs 8`):
`python3 -B <LANE>/scripts/cache_key_conformance.py --candidate <LANE>/scripts/cache_key.py --generated 600 --seed <s> --work <scratch>/work --verbose`

| seed | exit | wall | last two lines |
|---|---|---|---|
| 1 | 0 | 17.490 s | `advisory=1/3 outside-contract-gaps=utf8-required,nul-in-value` / `clauses=6/6 hand=70/70 generated=600/600 sandbox=ok seed=1 met=true` |
| 90 | 0 | 18.703 s | same, `seed=90 met=true` |
| 4242 | 0 | 14.695 s | same, `seed=4242 met=true` |
| 20261104 | 0 | 13.551 s | same, `seed=20261104 met=true` |
| 2147483646 | 0 | 9.889 s | same, `seed=2147483646 met=true` |

There were no `FAIL` lines under `--verbose`. The gate's `ckc-*` work directory was removed after each run.
Receipts: `receipts/seeds.txt`, `receipts/seed-<s>.out`. Wall time varies 9.9–18.7 s with host load, since other seats were running at the same time.

## 2. Recorded Vary captures → candidate vs gate `reference()`

Round 89's ExecTrial named its sources as the `response.json` captures under
`.ufo/waves/round-61/capture/*` (12) and `.ufo/waves/round-81/capture/*` (3). I checked the six cited
capture sha256 values against `.ufo/waves/round-89/w1/ExecTrial/outputs/provenance.json` and all six match.

Driver `receipts/trial90.py` loads `scripts/cache_key_conformance.py` with `importlib` from its path.
For each payload it compares five readings:
(a) `reference(obj)`;
(b) the candidate run plain (`python3 -B`);
(c) the candidate run through the gate's own `run_candidate` with the gate's `SANDBOX`, then `judge()`;
(d) the round-89 frozen reference `.ufo/waves/round-89/w1/ExecTrial/driver/reference_c89_key.py`;
(e) the round-89 recorded stdout, where one exists.

Command: `TMPDIR=<scratch>/work python3 -B trial90.py <LANE> <scratch>/trial-out`. Exit 0, and the last line was
`trial90 cases=48 agree=48 disagree=0`.

Population:
- **12** round-89 inputs, byte for byte. R1–R6 are real recorded Vary values; X1–X5 are synthetic refusals. Each is 5-way equal, including the round-89 recorded output.
- **36** cases rebuilt from all 15 header-bearing captures. Each capture gets a `full` variant (every nominated field present) and a `none` variant (no request headers, so every nominated field is absent → GS). The 7 captures with two `Vary` lines also get a `join-comma` variant (`","` instead of `", "`). The 4-way reading is equal on all 36. Every `join-comma` key is identical to its `", "` key, because OWS is trimmed, so round-89 defect D1 (line-combination rule) does not change any key on this corpus.
- This adds captures round 89 did not use: round-61 ds4cc-kimi, ds4cc-primary, lucario-ghp, plazir15-ghp, the four 404s, and round-81 ds4cc-robots.

Receipts: `receipts/trial90.out` (per-case line) and `receipts/trial90-results.json` (payloads, all outcomes, capture sha256/status/vary lines).

Limits:
- Request headers are **constructed**, not recorded. The captures are responses only.
- No capture carries a `*` or a malformed `Vary`, so the real data gives zero real-data refusals. All refusal evidence here is synthetic (X1–X5).
- Agreement between the gate's `reference()` and the c89 reference is agreement between two lane-authored oracles. It is not outside evidence.

## 3. Advisory line and direct stdin probes (exact bytes)

The candidate's advisory line on all 5 seeds was `advisory=1/3 outside-contract-gaps=utf8-required,nul-in-value`, so `raw-control` passes.

Probe driver: `receipts/probe_adv.py`. Each stdin was sent two ways:
- **plain**: `python3 -B cache_key.py`, host env;
- **gate**: the gate's exact argv `-I -S -B sandbox.py cache_key.py` and env `PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8`.

Full rows are in `receipts/advisory-probes.json` and `receipts/probe.out`.

| probe | stdin (hex) | plain | gate env |
|---|---|---|---|
| utf8-required (gate's own bytes) | `7b22757269223a22ff222c22726571756573745f68656164657273223a7b7d7d` | rc=1 `invalid_input: input is not valid JSON` | **rc=0 `{"key": "\udcff"}`** |
| utf8 bad in value | `{"uri":"u","request_headers":{"a":"\xc3("},"vary":"a"}` | rc=1 refuse | rc=0 key with `\udcc3` |
| utf8 overlong `\xc0\xaf` | uri `"\xc0\xaf"` | rc=1 refuse | rc=0 `\udcc0\udcaf` |
| raw-control (gate's bytes) | `{"uri":"u\x1f","request_headers":{}}` | rc=1 refuse | rc=1 refuse |
| contract worked example 5 **as written (raw US/RS)** | `{"uri":"https://e.test/a","request_headers":{"a":"x\x1fb\x1ey"},"vary":"a"}` | rc=1 refuse | rc=1 refuse |
| nul-in-value (gate's bytes, JSON `\u0000`) | `{"uri":"https://e.test/p","request_headers":{"a":"x\u0000y"},"vary":"a"}` | rc=0 key containing U+0000 | rc=0 same |
| raw NUL byte in value | `…"a":"x\x00y"…` | rc=1 refuse (JSON strict) | rc=1 refuse |
| NUL in uri / unnominated value (escaped) | | rc=0 (accepted) | rc=0 |

Whether each gap reproduces:
- **nul-in-value: reproducible** in both environments with the gate's exact bytes. The candidate keys a value containing NUL, which RFC 9110 §5.5 makes invalid. It also accepts escaped NUL in the URI and in unnominated headers; the gate has no advisory case for those.
- **raw-control: not a gap** for this candidate. Python's `json` strict mode refuses raw U+0000–U+001F inside strings, in both environments.
- **utf8-required: NOT reproducible by a direct stdin probe in the host environment.** The candidate refuses there. It reproduces only under the gate's harness. `receipts/env-matrix.txt` isolates the cause:
  - `-I` sets `ignore_environment=1`, so the gate's `PYTHONIOENCODING=utf-8` is dropped.
  - With `LC_ALL=C.UTF-8`, CPython 3.14 then opens stdin as `utf-8/surrogateescape`.
  - Every other combination tested (no `-I`; or `LC_ALL=en_US.UTF-8` with `-I`) gives `utf-8/strict` and rc=1.

## 4. Defects found

- **DT90-1 (gate harness).** `run_candidate` passes `PYTHONIOENCODING=utf-8` together with `-I`, so that setting is dead. The resulting `surrogateescape` stdin manufactures the `utf8-required` advisory gap for any candidate that reads `sys.stdin` as text. The advisory line therefore reports a property of the harness as a property of the candidate. This is not scored into `met`, and every scored payload is ASCII (`json.dumps` with the default `ensure_ascii`), so C2's numbers are unaffected. The routed contract gap still reads wrong. Fix options for L1: drop `-I` in favour of `-E -s`, or set `PYTHONUTF8`-independent strict decoding by giving the sandbox `sys.stdin.reconfigure(errors="strict")` before `run_path`; also disclose the change.
- **DT90-2 (contract vs gate/candidate).** The c2-contract says worked example 5's JSON "carries them raw". Sent literally, that input is refused by the candidate, and by `json.loads` in the gate's own reference path, as RFC 8259 §7 requires. The gate sends example 5 JSON-escaped (disclosed in a source comment), and its advisory `raw-control` expects REFUSE. The contract's example 5 is therefore not reproducible as written. The contract text should be corrected: the controls are JSON-escaped, not raw.
- **DT90-3 (advisory coverage, minor).** NUL is probed only in a nominated value. The candidate and `reference()` also accept escaped NUL in `uri` and in unnominated header values. If L1 routes the §5.5 gap, scope it to all header values, and add the URI if desired.
- **DT90-4 (contract silence, observed).** Duplicate JSON object keys are last-wins in both the candidate and `reference()`: `{"a":"1","a":"2"}` gives value `2`, and `{"uri":"u1","uri":"u2"}` gives key `u2`. Case-only duplicates are refused but exact duplicates are not. The contract does not decide this. Candidate and oracle agree, so it is not a C2 defect, but it is an unrouted gap next to the "duplicate header name" refusal. RFC 8259 §4: names SHOULD be unique.
- Real-data limits from round 89 still stand: constructed requests, and zero recorded refusals (§2).

## 5. Tools

No tools were installed or upgraded; I used only the host `python3` (3.14.8). No pacman. No network.

## 6. Checks for L1

- Re-run one seed after any DT90-1 fix. Expect `advisory=2/3 outside-contract-gaps=nul-in-value` for this candidate. That expectation comes from the host-env probe, and I have not run the gate with such a fix.
- `python3 -B receipts/trial90.py <LANE> <out>` re-derives the 48-case agreement. It needs `TMPDIR` set to a scratch directory and writes only under `<out>`.
