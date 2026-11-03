# Consider these: resource retirement signals

**Status: unassimilated future reading after hyaku.** Primary sources checked 2026-11-03 UTC. Source candidate only, not a training round, admission or readiness claim. No candidate software, binaries, live targets or private artifacts were run, tested or uploaded.

## RFC 8594: Sunset versus cache expiry

**Original summary.** Sunset announces expected resource retirement, not representation freshness. It is a hint rather than an availability guarantee; ordinary scope is the responding resource. A sunset link can explain policy or migration, but does not itself authorize moving consumers. This distinction is useful when reviewing a publisher's planned URL retirement alongside redirects and cache headers.

**Exact source.** [RFC 8594, May 2019](https://www.rfc-editor.org/rfc/rfc8594.txt), Informational, DOI 10.17487/RFC8594. The numbered published RFC is the revision pin, not a rolling draft. The publication date is printed in the document header.

**Reading path.** Read §§1.2 and 1.4, then §§3–6 and §8. Focus on retirement timing, cache separation, scope and trust in linked migration information.

**Future question.** After hyaku, consider a paper-only retirement worksheet for one already authorized publishing surface: old URL, notice date, intended final behavior, migration owner and independent cache policy. Could a reviewer mistakenly classify a fresh cached representation as evidence that the underlying URL will remain available? Which statements describe intent, and which would need a later observation? Leave uncertain fields blank rather than inventing a universal header requirement.

**Limits and rights.** This does not establish hosting-provider header support or change any website. The RFC's copyright notice invokes BCP 78 and [IETF Trust Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/tlp-5/); prose and extracted code have different terms. Keep this original commentary separate from normative text.

**Novelty.** No RFC 8594/Sunset match in the reviewed inventories and prior notes. Existing migration, caching and response-header work is related; the added question is advance retirement signaling, not another crawler rule.

Any later adoption requires independent review after hyaku. No training or deployment changes.
