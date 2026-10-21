# Row S027 — freshness recheck (round 26)

```json
{"id":"S027","verdict":"HOLD","fetchIndex":1,"quote":"urlsplit() does not perform validation. See URL parsing security for details.","anchorObserved":"fetched/text/S027-1.txt is one 30,322-char line; page self-labels 'urllib.parse — Parse URLs into components — Python 3.15.1 documentation' at offset 0; 'Warning urlsplit()' admonition at offset 7,261 (immediately after the urlsplit() signature); body heading 'URL parsing security ¶' at offset 16,630, with its TOC entry intact in the page index","reason":"Re-fetched 2026-10-21T15:10:49Z: status 200, finalUrl identical to the recorded URL, 119,730 bytes, sha256 a27468b3…42d9f1; Last-Modified 2026-10-21T13:04:29Z shows a same-day regeneration of the live 3.15 docs for the 3.15.1 patch. Both anchors survive: the urlsplit Warning still refers to 'URL parsing security', whose body states the APIs 'do not perform validation of inputs', tells callers to 'code defensively' and verify each returned component, and says the functions 'cannot be claimed compliant with either' WHATWG or RFC 3986 — so caller-side validation and non-equivalence to browser URL parsing both remain directly supported. The scope's resolution half is separately grounded by urljoin's own Warning that joining an attacker-controlled url is 'generally not secure'. Citation usage still agrees: corpus/knowledge/static-canonical-preflight.md (~L74-77) repeats 'do not perform validation … cannot be claimed as an exact WHATWG URL implementation', and corpus/lessons/round-22.md L50 quotes the identical warning sentence. Version advanced 3.15 → 3.15.1 within the anchored family; no teaches/anchor/version claim is now wrong, so no correction.","correction":null}
```

## Caveats

- Living, unpinned doc: freshness here is content-at-anchor support, not byte identity; no earlier S027 capture exists in this lane, so drift is judged against the row's stated claims, not a round-22 byte diff.
- Version pin: page now reads "Python 3.15.1 documentation" (patch bump from the row's "Python 3.15"). The family is unchanged and the anchor cell is append-only, so HOLD — L1 may note the 3.15.1 label if it records anchor observations.
- Anchor position: the Warning sits in the urlsplit() entry and the quoted security section is a top-level section; both offsets record the single-line text view (no line numbers available beyond line 1).
- One fetch index only; no redirect, no retry, content-type text/html per manifest.json.
- New 3.15 APIs visible on the page (missing_as_none, keep_empty, unwrap) do not touch either anchor or the teaches.
- Scope wording: the "resolution" clause rests on urljoin's separate Warning, not on the security section, which names only urlsplit()/urlparse().
- Used-by check: knowledge entry's "exact WHATWG URL implementation" is a narrower rendering of the doc's "cannot be claimed compliant with either" (WHATWG or RFC 3986); still supported in kind.
- No tools installed or upgraded; no network access beyond the retained fetch in the lane.
