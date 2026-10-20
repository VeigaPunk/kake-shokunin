# Attack27 — comment-decoy parser boundary

## Result

No falsification in the assigned scope. The frozen `comment_decoy` case and one adjacent comment-terminator probe both produced the independently derived outcomes. The comment-decoy claim survives these two probes; this is not evidence for general HTML5 parser equivalence.

## Independent expectations

- Frozen case: `.ufo/waves/round-22/cases.json` specifies exit `0` and `clean`. Independently, its fixture `.ufo/waves/round-22/fixtures/comment_decoy/page.html` contains one active `<link rel="canonical">` in the explicit head whose URL matches the manifest. The wrong-looking link is inside an ordinary HTML comment, so it is comment text, not a second link element. Contract policy in `.ufo/waves/round-22/contract.json` requires exactly one canonical link and compares its normalized URL to `expectedCanonical`.
- Neighbor: `/tmp/kake-r22-Attack27-comment-boundary/page.html` changes the comment close to `--!>` and places a wrong canonical link after it, then a second comment and a matching canonical link. In HTML comment tokenization, `--!>` closes the comment (with a parse error); therefore two canonical link elements are active in the explicit head. Under the frozen exactly-one policy the independently expected result is exit `1`, finding `canonical_multiple`. The implementation's finding precedence is consistent with this expectation (`scripts/canonical_audit.py`, `evaluate_page`, duplicate-count check).

## Executed commands and observations

1. Command:
   ```text
   python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case comment_decoy
   ```
   Exit: `0`

   Exact stdout:
   ```text
   PASS caseId=comment_decoy exit=0 findings=clean
   SUMMARY selection=comment_decoy accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
   ```

   This matches the independently derived frozen expectation: exit `0`, `clean`.

2. Command:
   ```text
   python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack27-comment-boundary/manifest.json --json
   ```
   Exit: `1`

   Exact stdout:
   ```json
   {"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
   ```

   This matches the independently derived neighbor expectation: exit `1`, `canonical_multiple`.

## Residual risk / verification gaps

These checks cover the frozen ordinary-comment fixture and one adjacent `--!>` terminator case only. No claim is made about all malformed/truncated comments or browser tree construction. The contract explicitly bounds this capability to static HTMLParser analysis and disclaims HTML5/browser or search-engine selection equivalence. No production files were changed; the synthetic manifest and page are isolated under `/tmp`.
