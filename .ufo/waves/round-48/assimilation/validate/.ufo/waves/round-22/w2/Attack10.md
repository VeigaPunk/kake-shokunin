# Attack10 — `attr_uppercase` falsification (round 22, wave 2)

Frozen candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD, clean status for
`scripts/canonical_audit.py`, `cases.json`, `fixtures/attr_uppercase`).
Environment: Python 3.14.8, Linux. No production bytes changed; neighbor fixtures live under
`/tmp/kake-r22-attack10/`. No subagents, no installs, no network, no git/jj writes.

## Independent expectation (derived before running)

Contract policy: exactly one canonical link in an explicit head; rel is an ASCII
case-insensitive token list; HTML attribute names are ASCII case-insensitive; href resolves
against the first head base or the document URL; HTTP(S) only, no fragment; normalized URL is
compared to `expectedCanonical`.

Frozen fixture `fixtures/attr_uppercase/page.html`:

```html
<!doctype html><html><head><LINK REL="canonical" HREF="a.html"></head><body></body></html>
```

Manifest: document `https://example.test/project/index.html`, expected
`https://example.test/project/a.html`. `HREF` is the same attribute as `href`, so `a.html`
resolves to `https://example.test/project/a.html` → policy clean, exit **0**, findings empty
(matrix renders empty findings as the single id `clean`).

Parser mechanism check (independent of the tool), `html.parser.HTMLParser`:

```
'link' [('rel', 'canonical'), ('href', 'b.html'), ('href', 'a.html')]
```

Stdlib lowercases tag and attribute names and preserves duplicate attributes in source order;
duplicate resolution is therefore the tool's own `attrs_first_wins` rule.

Frozen bytes confirmed against `frozen/expected.json`:

```
20837f52d741089a980595120e07b422ccc3dcba90bde553f9560d37a4f6a899  fixtures/attr_uppercase/page.html
c6accc96e01ebd08dca2b13631544f65608e5c4e4c693d4a4b047b016758d4f7  fixtures/attr_uppercase/manifest.json
```

Both match the `expected.json.inputs` entries exactly.

## Assigned run

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case attr_uppercase
```

stdout:

```
PASS caseId=attr_uppercase exit=0 findings=clean
SUMMARY selection=attr_uppercase accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Exit: **0**. Matches the independent expectation exactly.

Direct public CLI on the same frozen fixture:

```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/attr_uppercase/manifest.json
```

stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}` — exit **0**.

Public selftest (`--selftest`): exit **0**, 56/56 cases `ok`, including
`{"name":"attr_uppercase","expected":{"exit":0,"id":null},"actual":{"exit":0,"id":null},"ok":true}`
and `duplicate_attrs_first_wins` ok.

## Nearest-neighbor attack — case-variant duplicate attribute names

Fixture `/tmp/kake-r22-attack10/dup_attr_case/` (manifest identical to the frozen one):

```html
<!doctype html><html><head><LINK REL="canonical" HREF="b.html" hReF="a.html"></head><body></body></html>
```

Independent expectation: since attribute names are case-insensitive, `HREF` and `hReF` are the
same attribute; the first occurrence wins, so href = `b.html` → `canonical_mismatch`, exit **1**.
(i.e. the lowercased-attribute lookup must not fall through to the later case variant.)

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-attack10/dup_attr_case/manifest.json
```

stdout:

```
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Exit: **1**. Matches independent expectation; explicit `--json` run also exits **1**.

Paired order control `/tmp/kake-r22-attack10/dup_attr_case_control/` — identical bytes except
`HREF="a.html" hReF="b.html"`: stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`,
exit **0**. Together the pair proves first-occurrence-wins with case-insensitive attribute
identity, rather than last-wins or "any matching attribute" acceptance.

## Before/after controls

- BEFORE revision `7c61c8cc791bde36dd5e3688bdfea2678d90146c`: `git show 7c61c8c:scripts/canonical_audit.py`
  and `git show 7c61c8c:.ufo/waves/round-22/cases.json` both exit **128** (paths absent), matching
  the claim's before state "no lane-owned runnable canonical-policy validator".
- AFTER (candidate `c0fd6d5`): matrix PASS and CLI clean as recorded above.

## Verdict

**Claim survives** for `attr_uppercase`. Expected exit/id derived independently (0/`clean`) equals
observed in both the frozen matrix and direct CLI. The nearest-neighbor case-variant duplicate
attribute probe behaves per policy (mismatch rejected as exit 1/`canonical_mismatch`) with a
paired clean control, so the case-insensitivity path is not a blanket accept.

Residual unknowns (not gates for this case): this is author-side post-integration evidence, not
independent non-author closure; only CPython 3.14.8 was exercised; the case covers static
`HTMLParser` input only, not browser/HTML5 tree-builder conformance. No production file was
edited and no additional cases were run.
