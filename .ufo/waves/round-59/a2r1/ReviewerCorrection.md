# ReviewerCorrection

Attack target: lane build ab6e100e442046006fa039315f5bd33bb516940b, `corpus/knowledge/crawler-identity.md` vs base fd6303ce5c14b3f892dec586297a942ab6e4193b.

## Scope checks run

1. **Append-only / inserted lines only: PASS.** `git diff base..ab6e100 -- corpus/knowledge/crawler-identity.md` is a single hunk `@@ -32,6 +32,20 @@`, 14 insertions, 0 deletions (diffstat `14 +`). The old bullet text is byte-identical; the correction is appended as a continuation of the same bullet.
2. **Quote spans vs retained bodies: PASS.** `span_tools check S425` for the three quoted fragments (the counter's own text-node/block code):
   - `"The source IP address of the request."` → units 7, chars 37, in_text_node True, count_in_body 1, unique True, within_ceilings True.
   - `"The reverse DNS hostname of the source IP."` → units 8, chars 42, in_text_node True, count_in_body 1, unique True, within_ceilings True.
   - `"your logs may show visits from several IP addresses"` → units 9, chars 51, in_text_node True, count_in_body 1, unique True, within_ceilings True.
   The first signal (`The HTTP user-agent request header.`) is correctly **named, not quoted** — inline markup splits it into multiple text nodes (documented in `crawler-identity-signals.md`), so quoting it would fail the one-text-node rule.
3. **Citations resolve: PASS.** [S425]/[S426] rows exist in `corpus/SOURCES.md` (lines 171–172); both referenced files (`googlebot-verification.md`, `crawler-identity-signals.md`) exist at the build.
4. **CommonMark rendering: PASS** (verified with `/usr/bin/cmark`, not by eye): every inserted line has exactly 2 leading spaces and no blank line is inserted, so the correction is a lazy continuation rendering **inside the bullet's paragraph** — `<strong>[r59-correction 2026-10-27]</strong>`, `<em>only</em>`, and the two code spans render inline; the next bullet still starts its own `<li>` (not swallowed).

## FINDINGS:

**F1 (low, attribution precision) — "a server log records the requesting IP address as well as the user-agent" is a general fact, not an S425 statement, and is not marked.**
- Sentence: "The claim in the bullet above is wrong as stated: a server log records the requesting IP address as well as the user-agent, and Google's crawler overview gives three identification signals, not one [S425] — …".
- Support: S425 never states that a log records the IP; its nearest text only implies it ("Therefore, your logs may show visits from several IP addresses"). S426 states it directly — its procedure reads "the accessing IP address from your logs" (reverse DNS step) and "the original accessing IP address from your logs" (forward-DNS verify step). In the correction sentence the single [S425] marker sits after the three-signals clause, so the log-recording clause reads as page-sourced when it is actually a general technical fact (standard access-log format).
- Fix: mark the clause — e.g. attach it to S426 ("…records the requesting IP address as well as the user-agent — the verify procedure reads 'the accessing IP address from your logs' [S426]") or add an explicit general-fact qualifier. Low severity: the assertion itself is true and the three-signals half is correctly sourced.

**F2 (observation, no action required) — correction merges into the same paragraph as the text it supersedes.** Because no blank line precedes `**[r59-correction 2026-10-27]**`, cmark renders the correction inline right after "…the fetched HTML was produced for." inside one `<p>`. This satisfies "renders as part of the bullet"; but "historical text" and its superseding correction are visually one paragraph. If visual separation is wanted, a blank line before the marker (keeping the 2-space indent) yields a second `<p>` inside the same `<li>` — still part of the bullet, no breakout. Presentation choice, not a defect.

## Sentence-by-sentence support (no other defects found)

- "three identification signals, not one [S425]" — S425 body: "Google's crawlers identify themselves in three ways:" with items user-agent / source IP / reverse DNS hostname. Holds.
- "Its technical-properties section adds…" — S425 section "Technical properties of Google's crawlers and fetchers": "these clients are distributed across many datacenters… Therefore, your logs may show visits from several IP addresses." Holds, quote exact.
- "the user-agent header is what separates the Smartphone and Desktop subtypes quoted above… still does not say which viewport" — preserved consequence, supported by the in-file S263 quotes and S425 signal #1. Keeps what the old bullet got right; only the word *only* is retired. Holds, no overstatement.
- "verifying… is a check on the logged IP (reverse then forward DNS, or a match against Google's published IP ranges), set out in `googlebot-verification.md`" — matches S426's printed four-step manual procedure and the automatic IP-range alternative; the lane file exists and documents it. Holds.
- "the fuller reading… is `crawler-identity-signals.md` (S425)" — file exists (82 lines) and covers the three signals plus the datacenter spread. Holds.
- "The sentence above stays as historical text; this correction supersedes it." — old text untouched at build. Holds.

No fabrication observed: every quote above was machine-checked against the retained bodies via the counter's own span code; nothing in this report is unverified.

VERDICT: Correction is append-only, factually supported by S425/S426, preserves the old bullet's valid consequence, and renders inside the bullet per CommonMark; only finding is one low-severity unmarked general-fact clause (log-records-IP) that should cite S426 — PASS with nit.
