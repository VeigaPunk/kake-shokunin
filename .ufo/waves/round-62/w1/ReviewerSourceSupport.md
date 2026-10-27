# ReviewerSourceSupport — S432 quote support

## Finding

The substantive §3.6 sentence supports a narrowly stated X-Content-Type-Options purpose claim: the response header can require checking the response's `Content-Type` against the request destination. It does **not**, by itself, support the specific `nosniff` value constraint or the audit's ASCII-case-insensitive comparison; those are grounded in §3.6's following value grammar and algorithm, respectively. Keep those as separately located/paraphrased support if the knowledge entry claims them.

## Source and quote boundary

Re-opened canonical source: `https://fetch.spec.whatwg.org/` via `read`; returned title Fetch, Living Standard last updated 19 October 2026, revision `59afe349913d56898c947576216f1c2579308be7`. The retained opened body is `.ufo/waves/round-61/sources/S432.html`.

At §3.6, the complete sentence is split across inline markup / lines 6151–6154:

> `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.

The quote-worthy substantive span starts at the words **“response header can be used…”** (line 6152) and ends at **“…of a request.”** (line 6154); include the field name from the immediately preceding markup at line 6151 when presenting the full sentence, but do not misrepresent markup boundaries as absent text. The rejected prior span, “Web developers and conformance checkers must use the following,” is only an introductory lead-in to the value definition, not evidence for the field's purpose (round-61 verifier spot-check, `corpus/lessons/round-61-verifier-spotcheck.md:33`).

## Reproduction/evidence

- `read` `https://fetch.spec.whatwg.org/`: canonical source reopened; metadata above.
- `read` `.ufo/waves/round-61/sources/S432.html:6145-6160`: §3.6 heading and sentence at lines 6149–6154; subsequent `determine nosniff` algorithm begins at 6157–6159.
- `read` `corpus/lessons/round-61-verifier-spotcheck.md:28-36`: preserves S432 as **Admit / Disagree**, explains that the earlier generic lead-in was non-substantive, and records the unresolved learned-criterion gap.
- `read` `corpus/knowledge/response-header-expectations.md`: current xcto passage quotes only fragments (“can be used to require checking of a” and the generic lead-in) at lines 69–87. The purpose sentence above is a grounded substantive replacement; the entry separately describes value grammar and algorithm at lines 81–87.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff -- corpus/knowledge/response-header-expectations.md corpus/lessons/QUALITY.md corpus/lessons/round-62.md` → no output at review time; therefore no proposed working-tree correction/criterion was present for me to assess. This is a source-support recommendation, not a claim that the correction has landed.

No lane files other than this report were written; no score/counter run or mutation was performed.