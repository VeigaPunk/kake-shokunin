source: S011, S012, S013 (corpus/SOURCES.md) — https://www.rfc-editor.org/rfc/rfc9309 §2.3/§2.3.1.3/§2.3.1.4
verified-at: 2026-10-19 (RFC 9309 published September 2022; Google docs updated 2026-07-08)
recheck: on RFC or project-site inventory change — curl -fsSL https://www.rfc-editor.org/rfc/rfc9309.txt | grep -cF 'top-level path of the service'

# Crawl scope follows host and path

**Claim (falsifiable).** Robots rules are discovered at the service's root
`/robots.txt`, not separately at each project-page subpath. The three lane
project sites under `veigapunk.github.io/<repo>/` therefore share the one
host-root robots policy. A 4xx robots response means crawlers MAY access
resources; a 5xx/network-unreachable response means they MUST assume
complete disallow, subject to RFC 9309's long-outage allowance.

Sitemaps have a second, path-based boundary: sitemaps.org limits their URL
set by location and requires same-host URLs. For Google, unless submitted
through Search Console, a sitemap affects only URLs under its parent
directory; a site-root sitemap can cover all paths on that site. A
`Sitemap:` line in the host-root robots file is a supported discovery route.

**Refines at base `cb807bc`.** Makes host/path scope explicit for
`corpus/knowledge/sitemap-orphan-audit.md:40-47` and
`corpus/knowledge/freshness-sweep.md:58`; the historical ds4cc.com 404 at
`corpus/knowledge/publish-queue.md:88-93` is a different host and is not a
current observation about `veigapunk.github.io`.

**Source checks (quotes reopened 2026-10-19).**
- S011 §2.3: “in the top-level path of the service”; §2.3.1.3:
  “MAY access any resources on the server”; §2.3.1.4: “MUST assume complete
  disallow.”
- S012, Sitemap file location: “The location of a Sitemap file determines
  the set of URLs that can be included in that Sitemap.” It gives
  `/catalog/sitemap.xml` as including `/catalog/` URLs, not `/images/`.
- S013, Sitemap best practices: “unless you submit your sitemap through
  Search Console, a sitemap affects only descendants of the parent
  directory.” It also describes listing a full sitemap URL in robots.txt.

**Lane population recheck (2026-10-19).**
```
grep -oE 'veigapunk\.github\.io/[A-Za-z0-9-]+/' SKILL.md corpus/knowledge/fleet-registry.md | sed 's/^[^:]*://' | sort -u | wc -l
3
```
RFC recheck from the header argv returned `1` occurrence.

**Named debt.** The current status of `https://veigapunk.github.io/robots.txt`
and whether it lists project sitemaps remain unknown. Owner: operator/webzites.
An operator-authorized free read can settle this; no lane property was probed.

## How it clears corpus/QUALITY.md
- **Replayable claim:** states the RFC sections, exact command, and measured lane population.
- **Missing substrate stays visible:** current host-root robots and sitemap contents remain named debt.
- **Admission authority:** cites RFC 9309, the sitemap protocol, and Google's scoped guidance.
- **Citation-local absence:** refines live lane procedures and labels historic observations as such.
- **Shape-only probe environment:** no live response, credential, or session data was collected.