"""G4 (round-44 class run): loc scope must include the effective port.

Each pairfile puts a loc on one port first, so layout_f derives its manifest
sitemapUrl from that same scheme, host, port, and directory. A second loc uses
a different explicit port under the same directory. Round 41 flags that loc
out of scope; the round-43 port-dropped control compares only scheme and host.
"""

PORT_PAIRS = (("8443", "9443"), ("8080", "8081"), ("443", "80"))


def cases(rng, h):
    units = []
    n = 0
    for _ in range(60):
        first_port, second_port = rng.choice(PORT_PAIRS)
        scheme = rng.choice(("http", "https"))
        host = h.fill(rng, "host", 3, 8) + "." + rng.choice(h.TLDS)
        directory = h.tok(rng, 5, 9)

        def loc(port):
            return "%s://%s:%s/%s/%s" % (scheme, host, port, directory, h.tok(rng, 5, 10))

        values = [loc(first_port), loc(second_port)]
        values.extend(loc(first_port) for _ in range(4))
        units.append(("pairfile", *values))
        n += len(values)
    return units, n
