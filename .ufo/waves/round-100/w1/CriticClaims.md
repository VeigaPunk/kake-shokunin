# CriticClaims — kake round 100, w1 seat report

Falsification review of the two frozen claims as instruments (attack, route, never repair).
All work in the seat's own scratch and `w1/CriticClaims/`; the lane tree was not written outside
`w1/CriticClaims/` and no mutating git/jj command touched LANE or the fleet repo (fixture commits
lived in a scratch clone, deleted after receipts were copied).

## Instrument integrity (pre-attack)

- `sha256sum -c controls/instrument-sha256.txt` → every line OK, no mismatch (rc reflects grep
  finding no non-OK lines; receipts `receipt-c1-baseline.txt` context).
- Baselines reproduced before attacking:
  - C1 at repair commit `e84a1871…`: `tools=55 rows=146 … mismatches=0 met=true`, rc=0
    (== `controls/after-c1.txt`) — `receipt-c1-baseline.txt`.
  - C2 frozen oracle via `--candidate-file`: `candidate=present sha256=be234945… hand=91/91
    generated=300/300 refusals=119/119 seed=100100 met=true`, rc=0 (== `controls/ctl-c2-pos-oracle.txt`)
    — `receipt-c2-baseline.txt`.

## C1 — 6 escapes (met=true while the registry is wrong outside the declared limits)

Fixtures: scratch clone at the repair commit, one commit per attack, counter run per rev.
Full details, verbatim inserted rows and rev ids: `c1-attacks.md`.

- A1 `env python3 -B …`, A2 `bash -c '…'`, A3 `uv run …`, A7 `python3 -X dev …`: second registry
  row for `cache_key.py`, cell-count conformant, owner `kake`, verdict map falsely claiming
  `127` for unknown flags (true observed rc=1, both flag spellings). All four print
  `duplicated=0 probe_mismatch=0 mismatches=0 met=true` rc=0 — the `invoked()` grammar misses
  wrapper prefixes and flag-with-value pairs, so D1/D2 never see the row. A7 was built as a
  negative control and escaped anyway (the counter selftest only covers consecutive flag words).
- A4: duplicate row in a table whose header misses `Write scope` → table dropped wholesale
  (rows=146 unchanged), `met=true` rc=0.
- A5: the tool special-cases the counter's literal magic flag `--zz-bogus-r100` to exit 0
  (SKILL.md unchanged) → `met=true` rc=0; D2 certifies a manufactured exit.
- A6 negative control `python3 -B ./scripts/…` → caught: `duplicated=1 met=false` rc=1.
- Framing (FD1): the claim's "every row's verdict map naming the exit code for an unknown flag" is
  enforced only for parser-recognized rows at one magic flag; the review conjunct covers 8 fixed
  units, so false-map duplicate rows anywhere else are covered by nothing. FD2: no do-nothing or
  cheaper honest control reaches the target (base receipts all `met=false`), but the cheapest
  control reaching met=true at all is a one-row escape (C1) or a reformatted copy of the published
  reference (C2) — the instruments measure their own surface, not the claim sentence. FD3:
  "calibration" holds as a point-in-time fact at the repair commit, not as an enforced property.

## C2 — 5 escapes (met=true while violating a named contract-v2 clause)

Candidates in `candidates/` (byte-mutations of the frozen oracle), scored with `--candidate-file`;
divergence demonstrated on inputs outside the 391-case population (runner: `probe-runner.py`).
Full details: `c2-attacks.md`.

- X1 `cand-v22-overtrim.py` — V2-2: `strip()` trims `\v`; met=true, probe `"\u000bTOP"` → `"TOP"`.
- X2 `cand-e5-bom.py` — e5: accepts a UTF-8 BOM'd document the reference refuses; met=true.
- X3 `cand-v21a-eqempty.py` — V2-1a: accepts bare `=` Cache-Control (no token before `=`);
  met=true, probe rc=0 vs oracle rc=1.
- X4 `cand-sandbox-conditional.py` — V2-2 violated in every NON-counter environment (detects the
  sandbox env `{PATH,LANG,HOME}`/`HOME=/tmp` and behaves faithfully only there); met=true.
- X5 `cand-v2e1-storedcc.py` — V2-1 final line + e1: silently drops stored `cache-control`
  matching `no-cache|private`; met=true, probe shows the field missing from `updated`.
- Considered/dismissed: seed specialization (runtime seed unknown to the candidate; 2^32 commit-id
  inversion impractical; neg-theft closed the runtime channel).
- Framing (F2-capability, in c2-attacks.md): the predicate cannot distinguish an independent
  implementation from a static, behavior-identical copy of the published reference
  (`pos-oracle.py` itself is such a copy and scores met=true; neg-theft blocks only the runtime
  `/proc` channel). F4-sandbox-blindness: the sandbox blocks channels but cannot see
  candidate-side environment-conditional behavior (X4).

## Routed (not repaired)

1. C1 counter: extend/declare `invoked()` grammar (env, bash -c, sh -c, uv run, `-X <value>`,
   `-W <value>`); add a flag-value selftest case.
2. C1 counter: report near-registry tables instead of silently dropping them.
3. C1 counter: randomize or double the D2 probe flag so argv special-casing becomes visible.
4. Freeze framing: scope the C1 claim sentence to the instrument's surface (parser-recognized rows,
   one magic flag, 8 review units) or widen the instruments.
5. C2 framing: rename the capability row's epistemics (agreement-with-published-reference) or add a
   provenance check that survives reformatting.

## Receipts inventory (this directory)

`receipt-c1-{baseline,a1,a2,a3,a4,a5,a6,a7}.txt`, `receipt-c2-{baseline,x1,x2,x3,x4,x5}.txt`,
`probe-runner.py`, `candidates/{pos-oracle-repro,cand-v22-overtrim,cand-e5-bom,cand-v21a-eqempty,cand-sandbox-conditional,cand-v2e1-storedcc}.py`,
`c1-attacks.md`, `c2-attacks.md`. Scratch seat directory deleted after copying.

Tooling installed/updated: none (pacman paused; no install needed — bwrap, python3, git were
already present and sufficient).

CRITIC c1_escapes=6 c2_escapes=5 framing_defects=3
