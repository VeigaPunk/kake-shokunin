# Round 100 C2 critic attacks — CriticClaims seat (kake r100, hyaku run 15)

Instrument attacked: `.ufo/waves/round-100/c100_fresh304.py`
(sha256 `e7dff63b93d33254ea278bf34d18ae98fc1462616aedad46e6ff416c6d3f3fed`, verified against
`controls/instrument-sha256.txt` before attacking; `sha256sum -c` reported no mismatch line).
Contract attacked: `.ufo/waves/round-100/fresh304-contract-v2.md`
(sha256 `343b3a558c5d2fb3059f9f9e1de2d26d0c9d7ff9fb977035f905b0729d09a092`, verified).
All runs were `--candidate-file` scorings in my scratch root; candidate files are committed here in
`candidates/`. Baseline reproduction (before any mutation):

```
$ python3 -B .ufo/waves/round-100/c100_fresh304.py --candidate-file candidates/pos-oracle-repro.py --work <scratch>/work/c2pos
revision=None candidate=present sha256=be23494573ee14aa49e423ebce738053a06ac9f9fc6807ca8af0b4b2a37705e2 hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true
rc=0
```

This matches `controls/ctl-c2-pos-oracle.txt` (the frozen oracle, byte-identical copy) and confirms
the `--candidate-file` default seed is the constant `100100`.

## Escape class: met=true while violating a named v2 clause

Method: start from the frozen oracle bytes, mutate exactly one behavior in a corner that no hand
case and no generated case (grammar, seed 100100) exercises, score, then demonstrate the contract
violation on an input outside the 391-case population (probe runner: scratch `probe.py`, direct
`python3 -I -B` runs, oracle vs mutant on identical stdin).

| # | candidate (sha256 prefix) | counter line | violated clause | divergence probe (oracle vs candidate) |
|---|---|---|---|---|
| X1 | `candidates/cand-v22-overtrim.py` `17ca2454` | `candidate=present sha256=17ca2454… hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 | **V2-2** (trim is SP/HTAB only; "inner whitespace kept byte-for-byte"; a leading `\v` (0x0B) is neither SP nor HTAB) | stored `X-V` = `"\u000bTOP"`: oracle outputs `"\u000bTOP"`, candidate outputs `"TOP"` (stripped `\v` — Python `str.strip()` trims all whitespace). All scored values have only SP/HTAB edges, so `strip()` ≡ `strip(OWS)` on all 391 cases. |
| X2 | `candidates/cand-e5-bom.py` `6e4e5e9f` | `… hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 | **e5** (stdin that is not a JSON document is refused; a UTF-8 BOM is outside the RFC 8259 JSON grammar — the frozen reference refuses it) | stdin = `\xef\xbb\xbf{"stored":…valid…}`: oracle rc=1 `invalid_input: invalid json`, empty stdout; candidate rc=0 decision JSON. Caveat disclosed: RFC 8259 permits implementations to ignore a BOM; the deviation from the frozen reference on an unscored input class is the point — the 391 cases contain no BOM case (the `RAW` set covers truncated/non-UTF-8/empty/trailing-garbage/whitespace only). |
| X3 | `candidates/cand-v21a-eqempty.py` `2a22a35d` | `… hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 | **V2-1a** (`cache-directive = token [ "=" … ]` — a token is REQUIRED before `=`; value `=` does not parse, so it must be refused) | 304 `Cache-Control: "="`: oracle rc=1 `invalid_input: malformed cache-control`; candidate rc=0 `update` with the bare `=` copied as data. |
| X4 | `candidates/cand-sandbox-conditional.py` `5e4dcb9a` | `… hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 | **V2-2** — but only OUTSIDE the scoring sandbox | Candidate checks `set(os.environ) == {"PATH","LANG","HOME"} and HOME=="/tmp"` (the counter's exact sandbox env). Under the counter it is byte-faithful (met=true honestly, all 391 sandboxed runs); under any other environment it over-trims like X1 (probe, plain env: `"\u000bTOP"` → `"TOP"`). The sandbox isolates the candidate from the counter's process but cannot detect that the candidate detects the sandbox. |
| X5 | `candidates/cand-v2e1-storedcc.py` `b569de9d` | `… hand=91/91 generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 | **V2-1 final line + e1** ("Only the 304's Cache-Control is examined; stored Cache-Control values are copied as data"; update starts from ALL stored fields except V2-3's three) | stored `Cache-Control: no-cache="x"`: oracle copies it into `updated[0].headers`; candidate silently drops it (drops any stored cache-control matching `no-cache|private`). The generated grammar only ever stores `max-age=<int>`; no hand case stores a no-cache/private-flavoured Cache-Control. |

Every counter line above is the literal stdout first line of the recorded run; rc lines are in the
run outputs (scratch `work/c2-*.out`, receipts reproduced below before scratch deletion).

## Considered and dismissed

- **Seed specialization.** With `--candidate-file` the seed is the constant 100100; at scoring time
  it is `int(first 8 hex of REV, 16)` — public but only known AFTER the candidate is committed at
  REV, and the candidate process sees no arguments or environment (fixed argv, `--clearenv`), so a
  candidate cannot learn the seed at runtime and cannot embed the matching table in advance without
  inverting a 2^32 commit-id search. Dismissed as impractical; the neg-theft control already closed
  the runtime channel.
- **V2-1b / e2 / e7 / V2-3 corners.** Attempted mentally against the HAND list and the grammar:
  qualified forms both syntaxes and case variants are hand-covered (7 cases); malformed stored ETag
  is covered for non-last elements (e2-stored-bad-etag-lm304) and generated kind 3 covers the last;
  ties are hit frequently by the grammar (received range −2..3). No unscored corner found worth a
  fixture; the five escapes above were the productive ones.

## Framing defects

- **F2-capability:** the predicate cannot distinguish an independent implementation from a static,
  behavior-identical copy of the counter's own REF (renamed/reformatted; neg-theft only blocks the
  RUNTIME `/proc` channel, and `pos-oracle.py` itself — generated from that REF by
  `build_frozen.py` — already scores met=true). "Capability acquisition" is operationally
  "agreement with a published reference on 391 public cases". Routed, not repaired.
- **F4-sandbox-blindness:** the contract's scoring section claims the sandbox "closes R99-9 W1-W4";
  it closes the channels but cannot see candidate-side environment-conditional behavior (X4 scored
  met=true and violates V2-2 in every non-counter environment). The predicate certifies behavior
  only in one environment.
