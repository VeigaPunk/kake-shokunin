# Round 29 wave 2 — CrossSchemeDecision: same-site test across http and https (C2)

Seat: critic, leaf, advisory only. Axis judged: operability. Target: `scripts/base_path_audit.py` at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03 (tool sha256 e32646159b65…, matrix sha256 75c08f641a31…). Sandbox: /fast/scratch/hyaku/kake-r29/w2/CrossSchemeDecision/ (clone at 7697990; a variant `mut` at sandbox commit 61d666e2 that changes only `_site_key` to return `(scheme, host, port)`, the WHATWG origin; variant tool sha256 988ef6beb56f…). Python 3.14.8. No install, no network, no lane write except this report.

## Verdict: keep the behaviour, document it (and fix the contract wording that contradicts it)

## The choice as landed
- `_site_key` drops the scheme and keeps the port only when it is not the scheme default (`scripts/base_path_audit.py:345-352`); it is compared to the page key at :581 and :700.
- Stated in the module docstring (:36-37 "http and https on the same host are the same site") and the `_site_key` docstring (:346-350).
- Not stated where a user looks: `--help` (DETAILS, :136-141) only says references that "point at another site are ignored", with "site" undefined. The knowledge entry's "Can" bullet (`corpus/knowledge/pages-base-path.md:52`) does not state it.
- Contradicted by the round's own contract text: `.ufo/waves/round-29/c2-matrix.json:11` says "ignored: ... other origins (scheme, host, port); same-origin references ... are inside", and `SCORECARD.md:626` declares C2 as covering "same-origin references". The builder records the deviation as an L1 steer (`.ufo/waves/round-29/w1/BuildBasePathAudit.md:47`). That leaves two written authorities that disagree.

## Commands (all run in the sandbox, TMPDIR inside it)
- `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision 7697990…` (in clone): exit 0, "C2 30/30", constant gates all rejected.
- Same counter on the variant at 61d666e2 (in mut): exit 0, "C2 30/30", constant gates all rejected.
- `python3 -B scripts/base_path_selftest.py`: exit 0, "30/30 fixtures passed" in both clone and mut.
- `rg -c "http://" c2-matrix.json scripts/fixtures/base-path`: no matches. No case pins a cross-scheme reference, so the counter and the selftest cannot tell the two choices apart.
- `real_input_run.py --tool <tool> --sites sites --out <sandbox>` for both: exit 0 each. Findings (exit, verdict, resolved URLs) are identical between landed, variant and the committed `real-input/out/*.json`: charter-ghp exit 1 with 3 findings, lucario-ghp exit 0, plazir15-ghp exit 1 with 1 finding. The snapshots hold no `http://` reference, so the real input shows no difference.
- `python3 -B probe.py <landed> <variant>`: exit 0, page base path `/repo/` (`probe.py`, `probe.out` in sandbox):

| # | page | reference | landed | WHATWG origin |
|---|---|---|---|---|
| P1 | https://o.github.io/repo/ | `a href=http://o.github.io/other/` | exit 1, finding | exit 0, ignored |
| P2 | https | `link href=http://o.github.io/style.css` | exit 1, finding | exit 0, ignored |
| P3 | https | `script src=http://o.github.io/repo/app.js` | exit 0 | exit 0 |
| P4 | http://o.github.io/repo/ | `img src=https://o.github.io/logo.png` | exit 1, finding | exit 0, ignored |
| P5 | https | `base href=http://o.github.io/` + `img src=logo.png` | exit 1, finding | exit 0, ignored |
| P6 | https | `img src=http://o.github.io:443/logo.png` | exit 0 | exit 0 |
| P9 | https | `img src=http://o.github.io:80/logo.png` | exit 1, finding | exit 0, ignored |
| P10 | https://www.example.com/repo/ | `img src=http://www.example.com/logo.png` | exit 1, finding | exit 0, ignored |
| P11 | https | `a href=https://o.github.io/other/` | exit 1, finding | exit 1, finding |

P7 and P8 (`https://o.github.io:80/` from an https or http page) are ignored by both, because port 80 under https is not a default port.

## Case for S040 "http(s)" (the landed choice)
- S040's default-location row gives the project site as `http(s)://<owner>.github.io/<repositoryname>` (`sources/S040.txt`; table mapping in `w1/SrcS040AboutPages.md:63`). That is one publication reachable under both schemes, and the tool's job is to catch escapes from the base path, not to enforce origin isolation.
- Strongest counterexample against the WHATWG choice: S042's own `absolute_url` example produces `http://example.com/my-baseurl/...` (entry :34). A Jekyll build with an `http://` `url` and an empty or wrong `baseurl` emits `http://<owner>.github.io/assets/style.css` into a page served over https. That is the P2 shape: a subresource outside the base path, which the WHATWG key silently ignores. P4, P5, P9 and P10 are misses of the same kind.
- False positives: no new class. A cross-scheme link to a sibling project (P1) is the same class as a same-scheme sibling link (P11), which the entry already says leaves the base path on purpose (:60). A real false positive needs http and https on one host to serve different trees. [INFERENCE] That does not happen on github.io; it is possible only on an unusual custom-domain setup. No retained source states it either way.

## Case for the WHATWG origin
- It matches the frozen contract text (matrix :11) and the declared claim wording (SCORECARD :626), and it is the browser's security boundary.
- False positives: none beyond the landed choice. Misses: every cross-scheme escape (P1, P2, P4, P5, P9, P10), including subresources. For a base-path audit that is a coverage loss with no gain in precision. The wave-1 matrix critic called it "a false negative" (`w1/CriticMatrixOracle.md:7`).

## Shared limits (neither choice)
- P3, an in-base `http://` subresource on an https page, is clean under both. Mixed-content blocking is serving behaviour, and the docstring already excludes that (:28-29).
- "Site" here means host plus non-default port, not the HTML "site" (scheme and registrable domain): `example.com` and `www.example.com` are different keys. [INFERENCE] On `<owner>.github.io` the two notions coincide, because github.io is a public suffix. Not checked against the public suffix list.

## Smallest safe correction (document, not change)
1. Add one sentence to `--help` DETAILS after :141: same site means the same host and non-default port; http and https on one host are the same site, so a cross-scheme reference outside basePath is reported.
2. Add the same sentence to the entry's "Can" bullet (`pages-base-path.md:52`), citing S040's `http(s)` row.
3. Record in SCORECARD that matrix :11's "(scheme, host, port)" and :626's "same-origin" are superseded by the steer on the scheme only. Do not edit the frozen matrix in this round. Pin P2 (and P1) as a case in the next matrix version, so the counter stops being blind to this choice.
- Impact on C2's number: none. Both choices score 30/30 with gates rejected, so the 30/30 says nothing about this design either way.

## Not verified
- Browser behaviour for P1–P10, GitHub Pages http-to-https redirection, mixed-content handling, and public suffix list membership: none observed. No live probe and no URL fetched.
- Only `_site_key` was varied. Other resolution paths were not attacked by this seat.
