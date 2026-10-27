# S432 §3.6 source finding

Source: `.ufo/waves/round-61/sources/S432.html`, committed retained body, lines 6149–6187. The section heading is `3.6. X-Content-Type-Options header` (6150). The substantive prose is one sentence spanning lines 6151–6154, with markup split across lines:

> The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.

Exact source text across markup: line 6151 begins “The” then a `<dfn>` whose `<code>` text is `X-Content-Type-Options`; line 6152 continues “response … header can be used to require checking of a … response’s” and starts `<code>Content-Type</code>`; line 6153 continues “header against the … destination of a”; line 6154 completes “request.” Tags and hyperlink anchors are markup, not source wording. The sentence expressly supports only the proposition that the named response header can require checking the response Content-Type against the request destination; it does not by itself assert a live property’s headers or broader browser policy.

Quote candidate: the complete one-sentence passage above, using markup-normalized inline-code formatting for the two header names. Avoid quoting only the generic first clause/lead-in; include the check, compared value, and destination. Nearby but separate text: lines 6157–6181 define the `determine nosniff` algorithm; lines 6183–6187 specify the value ABNF and case-insensitivity. Those are not part of the prose sentence and should not be silently merged into its quotation.

Evidence command: `read` of `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html:6148-6190` returned the above line content. Contract corroboration: `.ufo/waves/round-62/contract.md` lines 7 and 9 identifies the generic lead-in issue and intended substantive sentence. No source edit or lane-state change performed.