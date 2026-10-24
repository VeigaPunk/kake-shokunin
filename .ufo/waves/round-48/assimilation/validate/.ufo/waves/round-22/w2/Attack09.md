# Attack09 — frozen case `rel_uppercase` (round 22, wave 2)

Seat: `KakeR22.Attack09` (scout/falsifier, leaf; no subagent dispatch).
Frozen integrated candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
(`git rev-parse HEAD` in the lane; equals the wave-2 candidate revision).
Production source/oracle/fixture bytes were not modified; this report is the only file written in the lane.
No installs, no package transactions, no builds/tests/lint. Python 3.14.8.

## 1. Frozen case: independent expectation

Read before running anything:

- `.ufo/waves/round-22/cases.json` → `rel_uppercase`: `expectedExit: 0`,
  `expectedFindings: ["clean"]`, rationale "compare the rel token using ASCII case-insensitive matching".
- `.ufo/waves/round-22/contract.json` policy: "rel ASCII case-insensitive token list; resolve href with
  first head base href or document URL".
- `.ufo/waves/round-22/fixtures/rel_uppercase/manifest.json`:
  `url=https://example.test/project/index.html`, `file=page.html`,
  `expectedCanonical=https://example.test/project/a.html`.
- `.ufo/waves/round-22/fixtures/rel_uppercase/page.html` (sha256
  `2a05703638c391b463834ea2393062ee1996ece8a3bc7c6305ca5fbc32d9a1fd`):
  `<!doctype html><html><head><link rel="CANONICAL" href="a.html"></head><body></body></html>`

Derivation from policy + source (`scripts/canonical_audit.py`, sha256
`35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`):

1. `handle_starttag` sees explicit `head`, then `link` inside the open head → `_record_link` (line ~168).
2. `is_canonical_relation` (`:132-134`) lowercases each token with `ascii_lower` (A–Z translate only,
   `:117-118`) and splits only on HTML ASCII whitespace `[ \t\n\r\f]` (`split_ascii_whitespace`, `:121-122`);
   `CANONICAL` → `canonical` → recorded. Exactly one head canonical.
3. `href="a.html"` is non-empty; `normalize_http_url` resolves it against the document URL with no base:
   `https://example.test/project/index.html` + `a.html` → `https://example.test/project/a.html`
   (path case and segments preserved; `:411-466`).
4. Resolved URL equals `expectedCanonical` → no finding → `verdict=clean`, `exit 0`, `pagesChecked=1`.

Matrix's `observed_findings` maps an empty `findings` array to `["clean"]`, so the frozen case must be
`PASS` with `accepted=1, discrepancies=0`. **Expectation fixed before execution: exit 0 / `clean`.**

## 2. Frozen case: observed (exact)

Command and output (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
$ python3 .ufo/waves/round-22/matrix.py --root . --case rel_uppercase
PASS caseId=rel_uppercase exit=0 findings=clean
SUMMARY selection=rel_uppercase accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
$ echo $?
0
```

```
$ python3 .ufo/waves/round-22/matrix.py --root . --case rel_uppercase --json
{"selection": "rel_uppercase", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0,
 "toolMissing": false, "results": [{"caseId": "rel_uppercase", "status": "PASS", "expectedExit": 0,
 "actualExit": 0, "expectedFindings": ["clean"], "actualFindings": ["clean"],
 "stdout": "{\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}\n", "stderr": ""}]}
$ echo $?
0
```

Direct public CLI on the same frozen fixture:

```
$ python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/rel_uppercase/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
$ echo $?
0
```

Observed exit 0 / `clean` matches the independently derived expectation. The frozen case does not falsify
the claim.

## 3. Nearest-neighbor probe (own /tmp tree, same rel-token boundary)

Fixture tree `/tmp/kake-r22-Attack09/rel_nn/` (one fixture directory, five one-page manifests; each page is
an explicit `head` + one head `<link>`; document URL `https://example.test/project/index.html`,
expected `https://example.test/project/a.html`). Specs derived before execution:

| probe | page bytes (rel value / href) | independent expectation |
|---|---|---|
| form-feed separator | `rel="alternate&#12;CANONICAL" href="a.html"` — FF decodes to U+000C, which **is** HTML ASCII whitespace | `clean`, exit 0 |
| entity uppercase | `rel="CANONIC&#65;L" href="a.html"` — charref decodes to `CANONICAL` before token comparison | `clean`, exit 0 |
| path case | `rel="CANONICAL" href="A.HTML"` — rel is case-insensitive but URL path case is significant | `canonical_mismatch`, exit 1 |
| Unicode lookalike | `rel="CANONİCAL"` (U+0130) href `a.html` — ASCII-only folding must not match | `canonical_missing`, exit 1 |
| literal vertical tab | `rel="CANONICAL\x0b"` (raw 0x0B byte) href `a.html` — U+000B is **not** an HTML space character, so the only token is `canonical\x0b` | `canonical_missing`, exit 1 |

Each run was `python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack09/rel_nn/manifest-<probe>.json --json`
from the lane root. Observed stdout / exit:

```
form-feed:  {"findings":[],"pagesChecked":1,"verdict":"clean"}                                   EXIT=0
entity:     {"findings":[],"pagesChecked":1,"verdict":"clean"}                                   EXIT=0
path-case:  {"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],
             "pagesChecked":1,"verdict":"failed-policy"}                                         EXIT=1
unicode:    {"findings":[{"id":"canonical_missing","page":"https://example.test/project/index.html"}],
             "pagesChecked":1,"verdict":"failed-policy"}                                         EXIT=1
vtab:       {"findings":[{"id":"canonical_missing","page":"https://example.test/project/index.html"}],
             "pagesChecked":1,"verdict":"failed-policy"}                                         EXIT=1
```

All five match the pre-registered expectations.

Discriminative value of the neighbors:

- **vtab vs form-feed** is the sharpest pair. A shortcut implementation using `rel.split()`/`.strip()` would
  treat U+000B as a separator and wrongly return `clean` for the vtab page
  (verified: `'CANONICAL\x0b'.split() == ['CANONICAL']`, while
  `re.split(r'[ \t\n\r\f]+', 'CANONICAL\x0b') == ['CANONICAL\x0b']`). The candidate correctly keeps HTML's
  ASCII-whitespace-only tokenization in both directions.
- **path-case** shows the ASCII case-insensitive rel rule does not leak into URL comparison: uppercase rel
  is recognized (otherwise `canonical_missing`), then the uppercased path is correctly rejected
  (`canonical_mismatch`).
- **entity uppercase** shows case folding is applied after attribute character-reference decoding, which the
  frozen fixture does not exercise.
- **U+0130 lookalike** is only weakly discriminative on its own: Python's `str.lower()`/`casefold()` also fail
  to fold `İ` to `i` (it yields `i` + U+0307), so this probe confirms the ASCII-only behavior but would not by
  itself catch a `.lower()` implementation. Recorded as a boundary observation, not as a distinguishing test.

Implementation note (probe construction): a numeric reference `&#11;` is not usable for the vtab probe because
`html.unescape` drops U+000B as an invalid code point (verified: `html.unescape('CANONICAL&#11;')` →
`'CANONICAL'`). The reported vtab run uses a literal 0x0B byte in the attribute value; `HTMLParser` preserves it
(observed attr `('rel', 'CANONICAL\x0b')`).

## 4. Frozen-byte / hygiene observations

- `git rev-parse HEAD` = `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`.
- `git status --porcelain -- scripts .ufo/waves/round-22/fixtures .ufo/waves/round-22/cases.json .ufo/waves/round-22/matrix.py`
  reports only `?? scripts/__pycache__/` (contains `canonical_audit.cpython-314.pyc`, mtime
  `2026-10-20 18:56:06 -0300`). That bytecode cache was not produced by this seat: a controlled run of the
  identical script bytes from an isolated `/tmp` copy in script mode left no `__pycache__`. It is attributable
  to a concurrent peer importing/compiling the module; it is not production source and was left untouched.
- Normal manifest-mode CLI performs no file writes; all probe inputs/outputs lived under
  `/tmp/kake-r22-Attack09/`.
- No tool installs or upgrades were performed.

## 5. Verdict

**Claim survives.** The frozen `rel_uppercase` case is accepted (exit 0, findings `clean`) exactly as derived
independently from the contract policy, case record, fixture bytes, and parser source. Five nearest-neighbor
probes on the same rel-token boundary (FF separator, entity-encoded uppercase, path-case no-leak, U+0130
lookalike, literal VT) all classified as pre-registered, including the pair that would expose naive
`str.split()`/Unicode-folding over-reach. No production bytes were changed; no falsifying discrepancy was found.

Residual unknowns / limits: the derivation is against this tool's stated conservative policy, not WHATWG
conformance or search-engine behavior; only `rel_uppercase` was exercised in the frozen matrix by assignment;
the U+0130 probe cannot distinguish ASCII-lower from Unicode-lower for this token; the worktree's untracked
`scripts/__pycache__/` is owned by concurrent wave activity, not by this seat, and remains unmodified.
