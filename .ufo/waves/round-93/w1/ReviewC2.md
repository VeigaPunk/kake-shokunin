# ReviewC2 — scoped findings (full report: `w1/ReviewC2/ReviewC2.md`)

VERDICT: C2 clean on the author-declared final bytes — **162/162 cases agree**
(deterministic across two runs). The review found 2 real tool defects in
earlier builds; both were fixed before the final bytes. The frozen positive
control still shares both defect behaviours — that is the round's load-bearing
instrument finding (F3).

Scored: `scripts/conditional_eval.py` sha256
`d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e`
(24 854 B, mtime 22:44:13-03:00, untracked at HEAD `191ef8dd`).

1. **F1 (clauses 3+4), found on `5a3bd465…`, FIXED in final** — quote-blind
   `value.split(",")` refused legal quoted-comma entity-tags
   (`If-Match: "a,b"` + `ETag: "a,b"` → `invalid_input`, exit 1; etagc includes
   0x2C: contract clause 3, RFC 9110 §8.8.3 at `rfc9110.txt:9871-9874`). Also
   reproduced live on mid-state `e38f8720…`.
2. **F2 (Input/Output), found on `5a3bd465…`/`b659029e…`, FIXED in final** —
   non-UTF-8 stdin crashed with a raw `UnicodeDecodeError` traceback instead of
   the required `invalid_input:` refusal (crash-not-rejection, QUALITY.md
   round-24 bar). Final bytes refuse cleanly.
3. **F3 INSTRUMENT FINDING, OPEN** — frozen `pos-good.py` (sha256 `0fe018a8…`)
   scores 160/162 on the same battery: it refuses the legal quoted-comma tag
   and crashes on non-UTF-8 stdin, falsifying the freeze's "independent
   contract-faithful" declaration on those two points. [INFERENCE] the counter's
   44 hand cases + 120 generated cases do not exercise quoted-comma members or
   non-UTF-8 stdin (the reference would have failed them pre-freeze), so the
   frozen counter cannot discriminate this defect class — it would have read
   `met=true` on the defective `5a3bd465…` bytes too. Successor population
   needs a quoted-comma case and a non-UTF-8 stdin case (R92-4/R92-5 class).
   Route; do not patch the frozen reference post-scoring.
4. **F4 PROCESS** — five digests observed during review
   (`55e94971` → `e38f8720` → `5a3bd465` → `b659029e` → (`10bf2b1e`) →
   `d3bac7de`); one mid-state regressed; author declared "final" twice within
   two minutes. Every number in my report is pinned to a digest; final
   measurements are against `d3bac7de…`. My first 160/160 reading was an
   artifact of a harness comparison bug (tool refusals auto-agreed); disclosed
   in the report, corrected harness is `w1/ReviewC2/battery.py`.
5. Contract-vs-RFC order/comparisons verified faithful against the retained
   sources (C-OBS-4); `current.etag` clause-3 scope, `role: null`, duplicate
   stdin keys are under-decided contract points to pin next revision
   (C-OBS-1..3). No illegal input accepted on any scored digest.

Claim relevance (recommendation only): on `d3bac7de…` I have no finding that
contradicts the C2 after-state (`met=true`); the routed debt is F3.

Receipts: `w1/ReviewC2/{ReviewC2.md, cases.json, agreement.txt, battery.py,
posgood_cases.json, posgood_agreement.txt}`.
