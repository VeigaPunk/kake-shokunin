"""G5: cache-collision pairs at prefix cuts 45, 48, and 64, plus head/tail.

Each prefix-cut pair is a clean URL followed by the same URL with one
case-invariant grammar defect at the cut.  The head/tail pairs have identical
first and last 48 code points and a defect only in their middle.  A cache
keyed on the relevant window reuses the clean parse for the defective value;
round 41 judges both values independently.
"""

CUTS = (44, 45, 48, 64, 65, 80)


def _base(rng, h, length):
    value = h.short_url(rng)
    while len(value) < length:
        value += "/" + h.tok(rng, 6, 10)
    return value[:length]


def _fill(rng, h, length):
    return "".join(rng.choice(h.ALNUM + "/-._~") for _ in range(length))


def _bad_char(rng, h):
    defects = tuple(value for value in h.CASE_INVARIANT_DEFECTS if len(value) == 1)
    return rng.choice(defects)


def _prefix_pair(rng, h, cut):
    base = _base(rng, h, cut + rng.randint(48, 80))
    bad = base[:cut] + _bad_char(rng, h) + base[cut + 1:]
    return base, bad


def _headtail_pair(rng, h):
    scheme = h.rcase(rng, rng.choice(("http", "https")))
    host = h.tok(rng, 6, 10) + "." + rng.choice(h.TLDS)
    head = scheme + "://" + host + "/"
    head += _fill(rng, h, 48 - len(head))

    middle = "/" + _fill(rng, h, 24)
    defect_at = rng.randrange(1, len(middle))
    bad_middle = middle[:defect_at] + _bad_char(rng, h) + middle[defect_at + 1:]
    tail = "/" + _fill(rng, h, 47)
    return head + middle + tail, head + bad_middle + tail


def cases(rng, h):
    units = []
    n = 0
    for cut in CUTS:
        for _ in range(10):
            good, bad = _prefix_pair(rng, h, cut)
            units.append(("prefixpair", good, bad))
            n += 2
    for _ in range(40):
        good, bad = _headtail_pair(rng, h)
        units.append(("prefixpair", good, bad))
        n += 2
    return units, n
