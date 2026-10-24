# Correction5S021 — falsify `[r26-recheck S021 STALE]` (line 25, cross-domain)

Seat: KakeR26-2.Correction5S021 (critic, leaf). Milestone r26-recheck-falsify. Axis judged: freshness.
Candidate e28312b14b076584fedd696fae2a684e460bd11e, base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006.
Target: `corpus/knowledge/static-canonical-preflight.md:186` (candidate), correcting base line 25.

Verdict: **AGREE**. I tried three ways to show the correction is wrong, and each one failed. The original sentence's attribution is unsupported at its own scope. The correction is accurate, and every quote in it is verbatim. The base bytes are preserved as an exact prefix. Two low-severity wording observations follow; neither one changes the outcome.

## 1. Original bytes preserved (prefix check)

Command:

```
n=$(git show 97404de…:corpus/knowledge/static-canonical-preflight.md | wc -c)
git show e28312b…:corpus/knowledge/static-canonical-preflight.md | head -c $n | cmp - <(git show 97404de…:corpus/knowledge/static-canonical-preflight.md) && echo PREFIX_OK
```

Output: `PREFIX_OK`. Base is 14076 bytes and the candidate is 16987 bytes, so only bytes were appended. `git show e28312b…:… | cmp - <worktree file>` reported `worktree==candidate`. Base line 25 is unchanged in the candidate: `'one. Cross-domain canonical is likewise not intrinsically invalid.'`.

## 2. Is the original wrong at its own stated scope?

Yes, as an attribution, though not as a fact.

- Base lines 18-25 form a single paragraph whose subject is S021, which this entry calls "Google's" guide: "Google's “Use rel=canonical link annotations” requires…", "Its “Best practices”…", "These are Google's documented processing rules…". Line 25 is joined to line 23-24's S021-backed clause by "likewise". Line 23-24 is "Absence of a declaration is not inherently a site error", which matches S021's "none of them are required". Read in place, line 25 is therefore presented as S021-scoped.
- Retained S021 bytes (`fetched/text/S021-1.txt`, 21019 bytes; manifest row S021 sha256 4edda778…, last-modified Fri, 10 Jul 2026) contain nothing that supports it. The counts are `cross` 0, `cross domain`/`cross-domain` 0, `hostname` 0, `another domain` 0, `different domain` 0, `other domain` 0, `external` 0, `syndicate` 0. `domain` has 1 hit, and it is about TLS certificates ("wildcard certificate that can be used for multiple subdomains on a domain"). `other site` has 1 hit, and it is about external signals consolidating to a same-site preferred URL.
- A strongest-counterexample attempt failed. S021 says "Google supports explicit rel canonical link annotations as described in RFC 6596", and RFC 6596 §3 permits a different domain, so one could argue S021 supports the claim by incorporation. That still means the support comes from RFC 6596 (S020), not from S021's own text, which is exactly where the correction routes it.
- A live cross-check was done with one plain public GET of the SOURCES.md S021 URL, held in memory and not saved. It returned status 200, 194799 bytes and last-modified `Fri, 10 Jul 2026 10:12:15 GMT`, the same size and date as the retained bytes. The body sha256 differs (1a063d77…), and I attribute that to dynamic page tokens [INFERENCE]. The only `cross` matches were `crossorigin` attributes and the JavaScript flag `MiscFeatureFlags__remove_cross_domain_tracking_params`, neither of which is content. The RFC 6596 sentence is present: "Google supports explicit rel canonical link annotations as described in RFC 6596 ." The extra space comes from link markup.
- The fact itself is true under S020. Base line 14 already says "a different hostname may be valid", and SOURCES.md:28 (the S020 row) says "Relative and cross-host targets are permitted". The defect is therefore misattribution, and the right fix is to re-route the sentence to S020 rather than retract it. That is what the correction does.

## 3. Is the correction accurate and verbatim?

Candidate line 186:

> [r26-recheck S021 STALE] Line 25's “Cross-domain canonical is likewise not intrinsically invalid” is not stated by S021: the 2026-10-21 re-fetch has no cross-domain canonical statement and defers annotation semantics to RFC 6596. Read it as an S020 claim (RFC 6596 §3: the target IRI MAY “Exist on a different hostname or domain.”). The fragment wording at line 21 remains governed by the existing [r23-correction] at lines 140-142. Evidence: w1/PairS021StaticCanonicalPrefl.md.

| Claim in correction | Check | Result |
|---|---|---|
| Quote of line 25 | substring of base line 25 (count 1 in line 186) | verbatim (period omitted inside quote; harmless) |
| "no cross-domain canonical statement" in re-fetch | negative searches above, retained + live | holds |
| "defers annotation semantics to RFC 6596" | S021: "Google supports explicit rel canonical link annotations as described in RFC 6596." | paraphrase holds; see observation O1 |
| RFC 6596 §3, target IRI MAY “Exist on a different hostname or domain.” | `S020-1.txt`: "3. The Canonical Link Relation" @2926, quote @3606, "4. Examples" @6608; preceding text "The target (canonical) IRI MAY: … o Exist on a different hostname or domain." (1 occurrence) | verbatim, inside §3, MAY correct |
| "line 21" fragment wording | base line 21: "rejects fragment canonicals and explains that JavaScript may affect the signal." | correct |
| "[r23-correction] at lines 140-142" | base lines 140-142 = the "rejects fragment canonicals" overstates S021 correction; unchanged in candidate (prefix) | correct |
| Evidence path | `.ufo/waves/round-26/w1/PairS021StaticCanonicalPrefl.md` row 10 | exists, matches (Correction C) |

The ledger is consistent. `statements.json` lists S021 with `stale: 1`, and the candidate file carries exactly one `[r26-recheck S021 STALE]` tag. `measure.py:450-454` requires the tag count to be at least the `stale` value, so the requirement is satisfied.

## Observations (low; no correction required)

- **O1, "defers" is slightly broad.** The sentence it summarises sits in a paragraph that immediately adds Google-specific restrictions: annotations with hreflang/lang/media/type are ignored, and the link element is accepted only in `<head>`. "Defers" therefore describes the base relation semantics, not everything Google does. That scope matters only for line 25's cross-domain question, and there it is accurate. If the text were ever reworded, the smallest fix would be "adopts RFC 6596's annotation semantics ('as described in RFC 6596')".
- **O2, label versus axis.** This is a misattribution that already existed when the sentence was authored, not drift in the source. S021's last-modified date of 2026-07-10 predates the 2026-10-20 opening, and the pair report concedes that no earlier copy was retained. Under the contract, though, STALE is decided against the bytes re-fetched this round (contract.json claim.after). The same usage appears in the S026 and S030 blocks. The label is therefore used consistently and is not false provenance. The row receipt `rechecks/S021.json` says `HOLD` with `correction: null` while the statement-level tag says STALE. That is intentional: contract-amendment.json requires statement-level tags in the statement ledger, and the umbrella bullet at the top of this EOF section explains the split between row-level and statement-level verdicts.

## Scope and bounds

- Commands I ran: read-only `git show`, `cmp`, `wc`, `grep`, in-memory python reads of the retained text, and one plain public GET of the S021 URL from SOURCES.md, which was not saved. I wrote nothing except this report. I did not read or run any round-24 material.
- Tool installs or updates: none.

Report: .ufo/waves/round-26/w2/Correction5S021.md

```json
{"target":"[r26-recheck S021 STALE] corpus/knowledge/static-canonical-preflight.md:186 (base line 25 cross-domain)","verdict":"AGREE","severity":"none"}
```
