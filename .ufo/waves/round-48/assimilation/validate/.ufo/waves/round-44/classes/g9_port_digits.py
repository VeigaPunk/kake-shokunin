"""G9 port-digit caches and default-port scope comparisons for round 44.

The digit-cache controls memoise sitemapUrl parses as well as loc parses. The separate
value units below retain the requested same-port/different-host pattern, but a single
value unit cannot witness it: its generated sitemapUrl is parsed through the same cache.
Each cache group therefore also has a pairfile whose first loc anchors its sitemapUrl
and whose second loc has a different host but the same seven-digit port spelling. The
round-41 tool flags that second loc; the digit-only cache reuses the first host.

The default-port control maps explicit ports to the scheme default but leaves an absent
port as None. Thus explicit :443 on the first pairfile value is needed to make its
sitemapUrl authority compare equal to a later explicit :8443 loc after the control's
rewrite. The second batch also retains the requested implicit-port shape as a
non-witness control sample.
"""

_CACHE_PORT = "0008443"  # 7 digits, numerically 8443; cached by both port-digit controls


def cases(rng, h):
    units = []
    n = 0

    # Keep the requested separate-value shape, then expose a cache hit within a single
    # pairfile. In this layout the separate units' sitemapUrl is parsed by the same memo,
    # masking the stale host on both sides of the scope comparison.
    for _ in range(60):
        token = h.tok(rng, 6, 10)
        host_a = "a" + token + ".test"
        host_b = "b" + token + ".test"
        units.append(("value", "loc",
                      "https://%s:%s/%s" % (host_a, _CACHE_PORT, h.tok(rng, 5, 9))))
        units.append(("value", "loc",
                      "https://%s:%s/%s" % (host_b, _CACHE_PORT, h.tok(rng, 5, 9))))
        n += 2

        segment = "p" + h.tok(rng, 5, 9)
        prefix = "/" + segment
        values = [
            "https://%s:%s%s/first" % (host_a, _CACHE_PORT, prefix),
            "https://%s:%s%s/second" % (host_b, _CACHE_PORT, prefix),
            "https://%s:%s%s/third" % (host_a, _CACHE_PORT, prefix),
            "https://%s:%s%s/fourth" % (host_a, _CACHE_PORT, prefix),
            "https://%s:%s%s/fifth" % (host_a, _CACHE_PORT, prefix),
            "https://%s:%s%s/sixth" % (host_a, _CACHE_PORT, prefix),
        ]
        units.append(("pairfile", *values))
        n += len(values)

    # The branch maps an explicit non-default port to the scheme default. Pairfile's
    # first value therefore uses explicit :443 so its derived sitemapUrl compares equal
    # after that rewrite; round 41 still sees the :8443 loc as out of scope.
    for _ in range(60):
        host = h.tok(rng, 6, 10) + ".test"
        segment = "p" + h.tok(rng, 5, 9)
        prefix = "/" + segment
        values = [
            "https://%s:443%s/first" % (host, prefix),
            "https://%s:8443%s/second" % (host, prefix),
            "https://%s:443%s/third" % (host, prefix),
            "https://%s:8443%s/fourth" % (host, prefix),
            "https://%s:443%s/fifth" % (host, prefix),
            "https://%s:8443%s/sixth" % (host, prefix),
        ]
        units.append(("pairfile", *values))
        n += len(values)

        # Preserve the requested implicit-port contrast as a separate sample. In the
        # frozen control the absent port remains None, so this is not the witness shape.
        implicit_host = h.tok(rng, 6, 10) + ".test"
        units.append(("pairfile",
                      "https://%s/sitemap.xml" % implicit_host,
                      "https://%s:8443/sitemap.xml/second" % implicit_host,
                      "https://%s/sitemap.xml/third" % implicit_host,
                      "https://%s:8443/sitemap.xml/fourth" % implicit_host,
                      "https://%s/sitemap.xml/fifth" % implicit_host,
                      "https://%s:8443/sitemap.xml/sixth" % implicit_host))
        n += 6

    return units, n
