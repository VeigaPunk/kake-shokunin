# Redirect-audit usefulness attack

**Axis:** operability.

## Verdict

**PASS against the current claim's operational usefulness as evidenced here; not a rejection of the general technique.** A rule interpreter can catch a publishing failure that the HTML-only tools cannot, but the round claim does not identify a specific host/rules-file format, and the implementation is absent from this checkout. So the real capability is plausible, not yet demonstrated by this artifact. This does not establish that it is merely “JSON says what JSON says”; it identifies the missing binding that would distinguish the two.

## Counterexample: a real, distinct failure class

A route-order regression can make a legacy URL fail its intended redirect: a broad SPA fallback/rewrite shadows a more specific permanent redirect, leaving the browser at the legacy URL with fallback content instead of moving to the new URL. That is externally observable as the wrong URL/content and missing 301/Location behavior. An offline interpreter of the actual ordered publisher rules, compared against independently authored request → expected action/destination cases, can catch this before deployment. The manifest supplies the oracle; the parsed rules supply the behavior under test, so this need not be tautological.

The existing tools cover different surfaces: `scripts/base_path_audit.py` explicitly excludes HTTP redirects and response status (`:27-29`); `scripts/canonical_audit.py` says it does not inspect redirects, responses, or readiness (`:4-6`, `:110-111`); `scripts/link_preview_audit.py` is offline and explicitly does not establish which URL the host serves (`:16`, `:45-46`). None evaluates redirect/rewrite selection or status/destination semantics.

## Strongest local counterexample to current operability

The lane's concrete static-host evidence is Render, but its docs say redirect/rewrite rules are defined in the Render Dashboard “no code required” (`corpus/knowledge/render-static-sites.md:36`); an existing resource takes precedence over every rule (`:38-40`), and among applicable rules first match wins (`:40`). Thus a repository-side rules file that is not the deployed authority can pass while the Dashboard is wrong; even a faithful rule-file simulation can disagree with the deployed outcome if the published tree contains a resource at the path. The lane also records no operator-owned Render static site: its Render property is a Docker web service (`:126-139`).

The target implementation is not present in this checkout. Decisive command and verbatim output:

```text
$ python3 -B scripts/redirect_audit.py --help
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/redirect_audit.py': [Errno 2] No such file or directory
(exit 2)
```

Therefore I could not establish whether the tool parses an actual publisher input, models first-match/wildcard/action semantics, or compares those results to independent expectations; no runtime finding is claimed.

## Smallest safe correction

Name the target host and exact rule source, and bind the audited bytes to the source actually consumed at deploy time. For Render, either use a provenance-bearing read-only Dashboard export/snapshot and include whether a published resource shadows the rule, or explicitly narrow the claim to a local rules-file semantics audit and do not imply it verifies Render publication. Keep expected outcomes independently authored; include a shadowed-specific-redirect witness and a redirect-vs-rewrite/wrong-destination witness. Report a static prediction, not live-serving verification.

## Files and checks

- Wrote: `.ufo/waves/round-46/w1/CriticGateDesign.md` only.
- Command run: `python3 -B scripts/redirect_audit.py --help` (above; exit 2).
- No tests or builds run; no tools installed.
