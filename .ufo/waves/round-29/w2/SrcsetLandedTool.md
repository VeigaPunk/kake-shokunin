# Wave 2 — SrcsetLandedTool (falsify C2 srcset parsing)

Seat: KakeR29.SrcsetLandedTool. Attacked item: C2 tool `scripts/base_path_audit.py`, srcset
parsing, committed bytes at 7697990cbca20291f3b0367b8ff4220e93b38b03 (sandbox clone verified:
`git rev-parse HEAD` → 7697990cbca20291f3b0367b8ff4220e93b38b03).

## Method

Oracle: wave-1 battery `/fast/scratch/hyaku/kake-r29/w1/ReviewSrcsetParsing/battery.py`
(`parse_srcset_spec` = WHATWG port, fetched 2026-10-22 per its docstring). Ran it standalone
first (exit 0) to record expectations; its spec column is cited below.

Vehicle: per battery input, a small manifest in the sandbox. Page
`<!doctype html><base href="/other/"><img srcset="INPUT">`; manifest
`{"version":1,"basePath":"/site/","pages":[{"file":"page.html","url":"https://example.com/site/page.html"}]}`.
`<base href="/other/">` moves the resolution base outside `/site/` (page URL itself stays
inside, as `audit_manifest` requires, scripts/base_path_audit.py:667-671), so every same-site
candidate surfaces as a finding whose `value` is the reported candidate URL, in order.
`referencesChecked` counts parsed candidates and sees even non-http candidates.

Driver: `python3 -B drive_battery.py` (sandbox /fast/scratch/hyaku/kake-r29/w2/SrcsetLandedTool/,
TMPDIR inside sandbox), exit 0. Ten subprocess runs of
`python3 -B clone/scripts/base_path_audit.py --manifest cases/SN/manifest.json`.

## Per-input result (expected = battery spec column; observed = tool findings[].value)

| In | Input | Expected (WHATWG) | Observed (manifest) | Count | Verdict |
|----|----|----|----|----|----|
| S1 | `a.png 1x, /b.png 2x` | a.png, /b.png | a.png, /b.png | 2/2 | agree |
| S2 | `a.png 1x,b.png 2x` | a.png, b.png | a.png, b.png | 2/2 | agree |
| S3 | `a,b.png 1x` | a,b.png | a,b.png | 1/1 | agree (naive would split) |
| S4 | `data:image/png;base64,iVBORw0KGgo= 2x` | full data URL | (no finding — data: is not http(s), resolve_url:391-397 returns None); referencesChecked=1 proves single candidate | 1/1 | agree |
| S5 | `https://example.com/a,b.png 2x` | https://example.com/a,b.png | same, one candidate | 1/1 | agree (naive would split) |
| S6 | `a.png 1x,/b.png` | a.png, /b.png | a.png, /b.png | 2/2 | agree |
| S7 | `a.png,/b.png 2x` | a.png,/b.png (glued) | a.png,/b.png | 1/1 | agree (naive would split) |
| S8 | `,a.png 2x` | a.png | a.png | 1/1 | agree |
| S9 | `a.png 1x,,b.png` | a.png, b.png | a.png, b.png | 2/2 | agree |
| S10 | `a.png (density 2)` | (none — bad descriptor) | (none, verdict clean) | 0/0 | agree |

Direct import channel (`landed.parse_srcset` vs battery `parse_srcset_spec`) agreed on all 10,
including S4's exact data-URL string. Exit codes: 1/failed-policy where findings exist, 0/clean
for S4 and S10. Naive comma-split would have differed on S3, S4, S5, S7, S10; the landed tool
differs on none. **The battery target holds: 10/10.**

## Beyond-battery divergences found while attacking (same oracle, same harness)

Root cause is descriptor validity, scripts/base_path_audit.py:69-70 regexes and
`_valid_srcset_descriptors`:465-479 — no zero-width check, density grammar narrower than the
oracle's.

- P1 `a.png 0w` — oracle: [] (zero width is an error); landed: [`a.png`]; manifest run emitted a
  finding for a candidate a browser would never use (exit 1, failed-policy). Over-report.
- P2 `/secret.png .5x` — oracle: [`/secret.png`] (`.5x` is a valid density); landed: [] (regex
  `^[0-9]+(?:\.[0-9]+)?x$` requires a leading digit) → verdict clean, exit 0. **Missed
  violation**: an outside-base-path candidate the gate should flag is silently dropped.
- P3 `/secret.png 5.x` — oracle keeps the candidate (`\d+(\.\d*)?x`); landed drops it → clean.
  Caveat: whether real WHATWG accepts `5.` as a fraction was not verifiable offline (no fetch
  authorization); against the battery oracle it is a divergence, same direction as P2.
- P4 `a.png 0.0x` — agree (both keep). Note the oracle itself is a declared "validity subset";
  it never applies the real spec's zero-density error, so P4 cannot separate the two.

Fixture coverage check: only D3 and D14 in scripts/fixtures/base-path touch srcset, both with
plain values — the committed selftest would not catch P1/P2/P3 either.

## Verdict (recommendation; L1 decides)

- Item attacked (10-input srcset battery vs landed tool at 7697990): **holds**, 10/10 agreement
  on candidate URLs, candidate counts, and naive-split discrimination.
- Landed srcset parsing is not fully WHATWG-conformant beyond the battery: P2 (and P1) are real
  divergences at 7697990, P2 in the false-negative direction for the gate.

## Not verified / limits

- No installs performed (nothing to record under the tooling directive).
- Real WHATWG grammar not re-fetched (no named-URL authorization for this seat); P2/P3 real-spec
  status rests on the battery oracle; P2's `.5x` validity also matches my reading of the WHATWG
  floating-point grammar [INFERENCE, unverified against fetched spec text].
- Only `img srcset` exercised via manifest; `source srcset` shares the same `parse_srcset` call
  (extract_references, base_path_audit.py:538-553) and was only checked by import.
- HTML-parser-level effects (entity decoding in attributes, duplicate srcset attributes,
  template suppression) were out of scope.
