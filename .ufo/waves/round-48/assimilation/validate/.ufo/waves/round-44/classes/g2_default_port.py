"""G2 (round-44 class run): explicit default-port authority comparisons.

Each pairfile uses its first value as the derived sitemap URL, followed by
five clean locations under that sitemap directory. HTTPS locations omit :443,
which the round-41 parser treats as the default 443 but the target control
mistakenly treats as 80. HTTP mirrors use explicit :80 on the sitemap URL.
"""


def cases(rng, h):
    units = []
    n = 0
    for scheme, port in (("https", "443"), ("http", "80")):
        for _ in range(30):
            host = h.tok(rng, 6, 10) + "." + rng.choice(h.TLDS)
            directory = h.tok(rng, 4, 8)
            first = "%s://%s:%s/%s/sitemap.xml" % (scheme, host, port, directory)
            values = [first]
            for _ in range(5):
                values.append("%s://%s/%s/%s" % (
                    scheme, host, directory, h.tok(rng, 4, 8)))
            units.append(("pairfile", *values))
            n += len(values)
    return units, n
