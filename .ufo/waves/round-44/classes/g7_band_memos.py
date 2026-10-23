"""G7: first-seen clean/defective URI pairs for the repetition memo bands.

Each clean value primes one round-43 process-global memo key. Its following
partner keeps that key but contains one malformed percent escape, which the
round-41 grammar checks independently as ``loc_not_absolute``.
"""


def _pair(rng, h, length, slash_count=None, first_percent=None):
    scheme = h.rcase(rng, rng.choice(("http", "https")))
    host = h.tok(rng, 4, 8) + "." + rng.choice(h.TLDS)
    prefix = scheme + "://" + host + "/"
    body_length = length - len(prefix)
    body = [rng.choice(h.FILL["path"]) for _ in range(body_length)]

    defect_at = 32
    if first_percent is not None:
        percent_at = first_percent - len(prefix)
        body[percent_at:percent_at + 3] = list("%41")
        defect_at = percent_at + 5

    if slash_count is not None:
        needed = slash_count - prefix.count("/")
        reserved = set(range(defect_at, defect_at + 3))
        available = [i for i in range(body_length) if i not in reserved]
        for i in rng.sample(available, needed):
            body[i] = "/"

    clean = prefix + "".join(body)
    bad_body = body.copy()
    bad_body[defect_at:defect_at + 3] = list("%G4")
    defective = prefix + "".join(bad_body)
    return clean, defective


def cases(rng, h):
    units = []
    n = 0

    # The length memo starts at 6001; _audit_loc still parses these after
    # recording the shared loc_too_long finding at its 2048-codepoint limit.
    for length in range(6001, 6041):
        clean, defective = _pair(rng, h, length)
        units.append(("value", "loc", clean))
        units.append(("value", "loc", defective))
        n += 2

    # Band and deep variants share the >=64-slash key; the band has an
    # additional <=1799-codepoint gate.
    for offset in range(40):
        clean, defective = _pair(rng, h, 1200 + offset, slash_count=64 + offset)
        units.append(("value", "loc", clean))
        units.append(("value", "loc", defective))
        n += 2

    # The valid %41 primes the exact first-percent position. The malformed
    # %G4 follows it, leaving both the first-percent index and value length
    # unchanged for the band and late variants.
    for offset in range(40):
        clean, defective = _pair(rng, h, 1600 + offset, first_percent=1000 + offset)
        units.append(("value", "loc", clean))
        units.append(("value", "loc", defective))
        n += 2

    return units, n
