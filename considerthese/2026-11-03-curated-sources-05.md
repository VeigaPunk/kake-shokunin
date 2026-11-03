# Consider these: retiring a cache diagnostic, not freshness checks

**Status: unassimilated reading after hyaku, subject to João's later manual instruction.** Primary sources checked 2026-11-03 UTC. This is a historical-to-current standards comparison, not a performance ranking or deployment proposal.

## Timeline and exact reading

- **June 2014:** [RFC 7234](https://www.rfc-editor.org/rfc/rfc7234), §§4.2.4 and 5.5, defined Warning codes including 110 for stale responses and 111 for failed revalidation. Read this as the superseded protocol contract, not a present-day checklist.
- **June 2022:** [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html), §5.5 and Appendix B, obsoleted Warning because it was not widely generated or surfaced. The editor identifies RFC 9111 as Internet Standard STD 98 and RFC 7234 as obsolete. These numbered publications are fixed document pins; publication age does not make the newer standard obsolete.

## What changed, and what did not

The older method expected an additional diagnostic channel attached to a cached response. The newer contract removes that channel and points readers toward other response information, including Age. That is a genuine requirements transition, not evidence that caches ceased serving stale responses. Freshness calculation, validation and restrictions on serving stale content remain distinct questions under RFC 9111 §§4.2–4.3. An absent Warning field is therefore not a modern freshness verdict.

**Earlier method still useful:** retain the old code vocabulary when interpreting an archived response or explaining a legacy intermediary's output. Do not silently erase historically meaningful fields from an evidence record. Conversely, do not fail a current publisher merely because a superseded diagnostic is absent. These are proposed review practices, not claims about any particular hosting provider.

## Future comparison question

After hyaku, could an existing, authorized header record receive opposite verdicts solely because two reviewers selected different specification editions? On paper, record observation date, asserted protocol contract, observed diagnostic fields, freshness inputs and missing timing evidence. Then ask which conclusion follows from bytes actually retained and which would require another observation. Keep a historical interpretation beside the current-contract interpretation rather than rewriting one into the other. No new requests to a live property are proposed here.

## Novelty, limits and rights

RFC 9111 already appears in the lane inventory and is disclosed as the baseline. RFC 7234 and the focused Warning retirement comparison add the historical dependency missing from the previous retirement/link-context notes. Both RFCs invoke BCP 78 and IETF Trust Legal Provisions; extracted code has separate notice requirements. Only original commentary is included. No captures, source text, deployment settings, training inputs or corpus entries are changed.
