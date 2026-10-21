# Review 2.4.1 — Bypass Blocks

**Verdict: Disagree (one criterion-specific issue).**

The card's `id`, title, Level A designation, and pinned source URL match the saved source. Its `sourceQuote` matches the sole normative sentence at `source-wcag22.html#bypass-blocks` (lines 1432–1441): “A mechanism is available to bypass blocks of content that are repeated on multiple web pages.” It is within the 6–25-word quote limit. The card remains `not-assessed`, and its manual walk-through is not presented as source-only conformance evidence. The linked `mechanism` definition (`source-wcag22.html#dfn-mechanism`, lines 3318–3329) notes that a mechanism may be provided in content or by the platform, user agents, or assistive technologies; its second note says a mechanism relied on for a claimed conformance level needs to meet all success criteria for that level. The criterion section itself has no additional note.

## Finding

- **Field:** `failureExample` (line 322), specifically: `a "Skip to content" link exists in the markup but points to an id that no longer exists ... so activating it does not move past the menu.` The scenario does not say this is the only bypass mechanism. A broken skip link alone does not establish that no mechanism is available: another content-, platform-, user-agent-, or assistive-technology-provided mechanism could still let users bypass the repeated navigation. As written, the example is not necessarily a failure of 2.4.1, which requires an available mechanism rather than that a particular link work.
- **Source:** `source-wcag22.html#bypass-blocks` (the criterion); `source-wcag22.html#dfn-mechanism` and its Note 1 (permitted mechanism providers).
- **Minimal correction:** qualify the example to say that **no other mechanism is available to bypass the repeated navigation block** (or otherwise make clear that the broken link is the only available mechanism).