# CtlTrivial — round-38 C1 pre-freeze controls (do-nothing family)

Leaf seat `KakeR38.CtlTrivial`, built from the public declaration only. The sealed key tree
`/fast/scratch/hyaku/kake-r38/` was never listed, read, stat'ed or searched; the round-38 counter
was never run; its key was not consulted. No lane file touched except this report; git read-only.
No tool installed (python 3.14.8, bwrap 0.13.1 present); no pacman transaction attempted.

## Files (absolute path, sha256, expected score of 20)
| file | sha256 | expected |
|---|---|---|
| `/fast/scratch/hyaku/kake-r38ctl/CtlTrivial/constant_clean.py` | `d1a777c9e4f0db5d0b7a99da3a0c67b4726a81d8c128d445c8fda0f59619796a` | 0 |
| `/fast/scratch/hyaku/kake-r38ctl/CtlTrivial/junk.py` | `1c305fe5a2b27101c6c4fc4907d8ec2785cf8558b3358ef7febd119b4f2cebd9` | 0 |
| `/fast/scratch/hyaku/kake-r38ctl/CtlTrivial/all_false.py` | `5b7bd68a04edbf7ca0aa1346c76d7b37b1d08ce1d6bf60779dd392593d97baa7` | 1 |
| `/fast/scratch/hyaku/kake-r38ctl/CtlTrivial/no_reader.py` | `61f4e937f966510f1620ae5aed09b0e350bc9745ff53513d7973ac071f9d9436` | 1 |

Each is one self-contained stdlib file, CLI `--manifest PATH`, one JSON report on stdout. Demo
inputs I wrote are under `demo/`: `manifest.json`, `robots.txt`, `make_fixtures.py` (generates
`huge_status.json`, `nan.json`, `urlchar.json`, `bigfield.json`), plus `huge_status_64m.json`,
`probe.json`, `badver.json`, `inf.json`, `notjson.json`, `sealed.json`.

## What each skips
- `constant_clean.py` — reads no argument, opens no file; prints `version 1, verdict clean,
  checksEvaluated 0, findings []`, exit 0. Skips every rule (a)–(k) and every fault rule.
- `junk.py` — prints `not a report`, exit 0. Skips even producing a report; unparseable stdout.
- `all_false.py` — plain `json.loads`, then per check: expect `allow` → `blocked`, expect
  `disallow` → `exposed`; always `failed-policy`, exit 1. Skips (a), every fault rule and all
  rule reading; it only mirrors the stated expectation.
- `no_reader.py` — implements exactly the usage rule, (a) status rule, (f) check faults, (g)
  manifest faults, (h) numbers and (i) URL characters, and opens **no** robots file: 200–299
  decides `allow` for every URL (so (k)'s `/robots.txt` allow holds vacuously). Skips (b), (c),
  (d), (e) and (k)'s rule-decided half: every 2xx check whose file would `disallow` is judged
  `allow`, and every 2xx `allow` expectation against a blocking file is missed.

## Demonstrations (sandbox; every run under `timeout`)
- `constant_clean.py --manifest demo/manifest.json` → exit 0,
  `{"version":1,"verdict":"clean","checksEvaluated":0,"findings":[]}`.
- `junk.py --manifest demo/manifest.json` → exit 0, stdout `not a report`.
- `all_false.py --manifest demo/manifest.json` → exit 1, `failed-policy`, 5 findings
  (`blocked` c1/c3/c4/c5, `exposed` c2).
- `no_reader.py --manifest demo/manifest.json` → exit 2, `could-not-evaluate`, 4 evaluated,
  findings `exposed` c2, `blocked` c4, `check_invalid` c5; c1's 2xx file disallows `/private/x`
  yet the control allows it (the skipped (b)/(d) work); c3 404 allow.
- `demo/huge_status.json` (5000-digit `robotsStatus`) → exit 2, one `check_invalid` for that id,
  `checksEvaluated 1` (other check still evaluated) — (h).
- `demo/nan.json`, `demo/inf.json` (`-Infinity`), `demo/notjson.json` → exit 2, one
  `input_invalid` with `check: null`, `checksEvaluated 0` — (g)/(h); `demo/urlchar.json` (space
  in url) → exit 2, `check_invalid` — (i).
- `demo/bigfield.json` (exactly 64 MiB, all digits in an unread field) → exit 0, `clean`, 0.12 s;
  `demo/huge_status_64m.json` (64 MiB digits as `robotsStatus`) → exit 2, one `check_invalid`,
  0.08 s — (h) length bound inside the 20 s budget.
- `demo/probe.json` (13 checks): non-ASCII url kept and 404→allow (`exposed`); `\`, tab, `{` in a
  url → `check_invalid`; repeated second id → `check_invalid`; `ftp://`, `http:///x`,
  `../`-escaping robots, `B ot` UA, `404.0` status → `check_invalid`; 410 with a bogus `robots`
  value → no finding (field ignored below 2xx). Exit 2, 4 evaluated.
- `no_reader.py` with no args → exit 64. No-open proof: `grep -n 'open(' no_reader.py` → line 106
  only (the manifest); a mode-000 (unreadable, still statable) robots file was accepted and the
  run returned `clean`, exit 0 — a reading tool would need its bytes.

## Expectation and attack
Predicted 0/0/1/1 per the declaration's separation rows. The counter is wrong only if
`no_reader.py` reaches 19: that would mean some sealed case is fully decided by
(a)+(f)+(g)+(h)+(i), i.e. holds no 2xx check whose decision depends on file bytes. The strongest
local counterexample is a case of only 4xx/5xx and fault runs; the declaration forbids that for
(g)/(d)/(i)/(k) by requiring one holding and one non-holding check per case, but (h)'s fault runs
are legitimately fault-only, so a case made only of those runs would pass this control. That is a
case-mix risk, not a defect in the files: if the score returns ≥19, the case mix — not the
control — needs redesign before any build. Limit: no_reader satisfies (k)'s positive half
vacuously, so (k)'s negative half (`/robots%2Etxt`, `/%72obots.txt` allow shapes, rule-decided
paths) is reachable only through a reader control, outside this seat's four files.
