# ScribeKnowledge source receipt

Date: 2026-11-04. Author-side documentation seat; not independent closure.

## Executed commands

1. `mkdir -p /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeKnowledge && curl --request GET --proto '=https' --max-time 90 --silent --show-error --dump-header /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeKnowledge/s458-http-headers.txt --output /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeKnowledge/s458-referrer-policy.html --write-out 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\n' https://w3c.github.io/webappsec-referrer-policy/`
   - Exit 0; http_code=200; size_download=246577; url_effective=https://w3c.github.io/webappsec-referrer-policy/.
2. `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeKnowledge/s458-referrer-policy.html`
   - Exit 0; sha256=339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6.

Read tools also independently retrieved the public source, read the contract and full count.py, inspected existing corpus provenance conventions, and located the algorithm in this seat’s retained HTML. No candidate decoder or counter was run; no tests, build, lint, or deployment ran.

## Located quotation

URL: https://w3c.github.io/webappsec-referrer-policy/#parse-referrer-policy-from-header

§8.1 step 3, retained HTML lines 1612–1614; quote is rendered text with HTML tags removed and whitespace normalized:

> For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.

Manual whitespace-token enumeration: For(1) each(2) token(3) in(4) policy-tokens,(5) if(6) token(7) is(8) a(9) referrer(10) policy(11) and(12) token(13) is(14) not(15) the(16) empty(17) string,(18) then(19) set(20) policy(21) to(22) token.(23). Total 23, within 25-word maximum. This is not a raw contiguous HTML substring; tags and source line breaks intervene. Raw original is retained, not reconstructed.

Other source locations: heading 1596–1598; header-list extraction 1604–1605; empty initial policy 1608; return 1621; unknown-values explanation 1866–1870.

## Limits and hygiene

No tools installed or updated. Scratch `/fast/scratch/hyaku/kake-r85/ScribeKnowledge/` was not created or used, so no scratch data needs removal. All substantive drafts and receipts were written directly into the assigned seat output directory; production remained read-only. No VCS mutations, sibling writes, dispatch, credentials, account actions, browser, live property requests, publish, or deploy actions.
