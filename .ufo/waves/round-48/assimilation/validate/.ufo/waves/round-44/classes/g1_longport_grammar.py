"""G1 (round-44 class run): grammar defects behind six-digit in-range ports.

The 298 main values alternate loc and sitemapUrl, all with a malformed percent
escape and an in-range, zero-padded port. Half place the defect in a later path
segment, beyond the 64-code-point abbreviation window. The final prefixpair is
an isolated cache-key witness: two clean paths differ only by an in-range versus
out-of-range port of equal digit length.
"""


def _unique_token(rng, used):
    while True:
        value = rng.choice("abcdefghijklmnopqrstuvwxyz") + "".join(
            rng.choice("abcdefghijklmnopqrstuvwxyz0123456789")
            for _ in range(rng.randint(11, 17)))
        if value not in used:
            used.add(value)
            return value


def _unique_host(rng, h, used):
    while True:
        host = h.tok(rng, 8, 12) + "." + rng.choice(h.TLDS)
        if host not in used:
            used.add(host)
            return host


def _defective_url(rng, h, host, ident, later):
    scheme = h.rcase(rng, rng.choice(("http", "https")))
    port = h.long_port(rng, out_of_range=False)
    if later:
        first = h.tok(rng, 44, 52)
        path = "/%s/%s%%" % (first, ident)
    elif rng.random() < 0.5:
        segment = h.tok(rng, 8, 12)
        path = "/%s%%%s/%s" % (segment[:2], segment[2:], ident)
    else:
        path = "/%s?q=%%" % ident
    return "%s://%s:%s%s" % (scheme, host, port, path)


def cases(rng, h):
    units = []
    used_hosts = {"cachewitness.example"}
    used_ids = set()
    n = 0
    for i in range(298):
        host = _unique_host(rng, h, used_hosts)
        ident = _unique_token(rng, used_ids)
        value = _defective_url(rng, h, host, ident, i < 149)
        field = "loc" if i % 2 == 0 else "sitemapUrl"
        units.append(("value", field, value))
        n += 1

    # V4 drops the port digits from its parse-cache key. Keep this two-value
    # primer separate from the malformed-grammar corpus above.
    path = "/cache-path/cache-item"
    good = "http://cachewitness.example:000080" + path
    bad = "http://cachewitness.example:999999" + path
    units.append(("prefixpair", good, bad))
    n += 2
    return units, n
