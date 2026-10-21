## Verdict

Counterexample found: several unprobed body-metadata paths are reported `clean` by the current validator. The committed probe passes its 11 cases, but does not cover body `meta[http-equiv]`; a second canonical in the omitted body-after-foreign paths is currently rejected, not clean.

## Findings

### P2 — Body `meta[http-equiv=refresh]` falls through to clean

- **Exact commands:**
  - `TMPDIR=/tmp/kake-r23w2-CritRelaxationProbe-1tBz python3 /tmp/kake-r23w2-CritRelaxationProbe-1tBz/probe_missing_paths.py /tmp/kake-r23w2-CritRelaxationProbe-1tBz`
  - `TMPDIR=/tmp/kake-r23w2-CritRelaxationProbe-1tBz python3 /tmp/kake-r23w2-CritRelaxationProbe-1tBz/probe_integration_meta.py /tmp/kake-r23w2-CritRelaxationProbe-1tBz`
- **Exact outputs:**
  ```text
  {"case":"body_meta_refresh","exit":0,"verdict":"clean","findings":[]}
  {"case":"body_meta_refresh_after_svg","exit":0,"verdict":"clean","findings":[]}
  {"case":"body_meta_refresh_after_svg_breakout","exit":0,"verdict":"clean","findings":[]}
  {"case":"second_canonical_after_svg","exit":1,"verdict":"failed-policy","findings":[{"id":"canonical_outside_head","page":"https://example.test/cases/page.html"}]}
  {"case":"second_canonical_after_svg_breakout","exit":1,"verdict":"failed-policy","findings":[{"id":"canonical_outside_head","page":"https://example.test/cases/page.html"}]}
  {"case":"second_canonical_in_foreignobject","exit":2,"verdict":"could-not-evaluate","findings":[{"id":"html_unsupported","page":"https://example.test/cases/page.html"}]}
  {"case":"svg_foreignobject_selfclosing_meta_refresh","exit":0,"verdict":"clean","findings":[]}
  {"case":"math_annotation_selfclosing_meta_refresh","exit":0,"verdict":"clean","findings":[]}
  ```
- **Cases:** the `clean` rows use `<meta http-equiv="refresh" content="0;url=https://wrong.test/">` directly in the body, after a closed SVG, after an SVG `<p>` breakout, and self-closing inside SVG `foreignObject` / MathML `annotation-xml encoding="text/html"` integration points.
- **Evidence / impact:** `relaxation_probe.py` lines 22–36 has no body-meta case. In `canonical_audit.py`, `_foreign_token` (206–210) only treats `base`, `head`, and canonical `link` as ambiguous; `handle_starttag` after head closure (289–298) has no `meta` branch; foreign-context self-closing tokens return through `_foreign_token` (299–304). This leaves these inputs supported with the unchanged head canonical and produces `clean`. Impacts QUALITY.md “Parser relaxations and live receipts” (139–144) and the judged **operability** axis: the relaxation probe does not enumerate this body/integration-point token class. If refresh navigation is treated as part of the effective published destination, the clean result is also a policy blind spot; that browser-level consequence is an inference, not exercised here.
- **Smallest safe correction:** fail closed for body `meta[http-equiv]` and for that token at HTML integration points, including self-closing syntax, then add direct-body, post-foreign, SVG `foreignObject`, and MathML `annotation-xml` probe rows expected not clean. If refresh/navigation is intentionally outside this audit's promise, explicitly narrow the QUALITY criterion and probe contract rather than claiming coverage of every head-affecting path.

### P2 — Omitted canonical-link routes are probe gaps, but these examples currently fail closed

- **Exact command:** the first command above.
- **Exact outputs:** `second_canonical_after_svg` and `second_canonical_after_svg_breakout` both return `exit:1`, `verdict:"failed-policy"`, finding `canonical_outside_head`; `second_canonical_in_foreignobject` returns `exit:2`, `verdict:"could-not-evaluate"`, finding `html_unsupported`.
- **Cases omitted from the committed probe:** a second canonical link after a closed SVG, after a body breakout (`<svg><p>x</p></svg>`), and inside a `foreignObject` HTML integration point. These do not currently produce clean, so they are not confirmed validator bypasses. Add them to `ATTACKS` to make the canonical-link-after-foreign / breakout behavior durable against future parser relaxations.
- **Impacted axis:** Parser relaxations probe completeness / operability, not a demonstrated current canonical-link acceptance defect.
- **Smallest safe correction:** add these exact forms as `expect: not clean`; preserve the current `canonical_outside_head` / `html_unsupported` handling.

## Checked and held

- Ran the committed probe against the current working-tree validator:
  `TMPDIR=/tmp/kake-r23w2-CritRelaxationProbe-1tBz python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/relaxation_probe.py --validator /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`
- Exact summary: `"passed": true`, `"met": 11`, `"total": 11`. Its nine attack cases all returned `exit:2`, `verdict:"could-not-evaluate"`; both controls returned `exit:0`, `verdict:"clean"`.
- Held: the omitted canonical-link variants tested above are rejected. No production files were changed; only this report was written in the lane.

## Limits

Only the validator CLI was exercised with local manifests; no browser/runtime was launched, so browser handling of refresh directives is not claimed as an observed result. No build, lint, formatter, or service action was run.