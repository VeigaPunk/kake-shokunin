"""Round-44 G3 cases for URLs whose authority is followed by no path."""


def cases(rng, h):
    units = []
    n = 0
    for i in range(120):
        host = h.tok(rng) + "." + rng.choice(h.TLDS)
        value = "https://" + host
        units.append(("value", "loc", value))
        n += 1

        if i == 0:
            # This exact no-port value gets a derived `/sitemap.xml` URL.
            units.append(("prefixpair", value + "/", value))
            n += 2
        elif i <= 60:
            port = h.long_port(rng, out_of_range=False)
            ported = "https://" + host + ":" + port
            # Root-path sitemap gives this pathless loc the `/` scope prefix.
            units.append(("prefixpair", ported + "/", ported))
            n += 2

    return units, n
