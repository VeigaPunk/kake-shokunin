"""G10: long-port URLs whose grammar is cut by head/tail 64-code-point windows.

Each URL is its own loc value. The head cases put a valid path segment across
code point 64, with either a clean continuation or one hidden grammar defect.
The tail cases end in a clean, independently parseable URL suffix; their outer
path is either clean or carries one defect before the retained tail.
"""

PORT = "000080"
REPS_PER_SHAPE = 30


def _safe(rng, h, n):
    alphabet = h.ALNUM + "-._~"
    return "".join(rng.choice(alphabet) for _ in range(n))


def _host(rng, h):
    return h.tok(rng) + ".invalid"


def _head_clean(rng, h):
    host = _host(rng, h)
    prefix = "https://%s:%s/" % (host, PORT)
    segment = _safe(rng, h, max(24, 65 - len(prefix)))
    return prefix + segment + "/" + h.tok(rng)


def _head_hidden_defect(rng, h):
    host = _host(rng, h)
    prefix = "https://%s:%s/" % (host, PORT)
    before = _safe(rng, h, 65 - len(prefix) + rng.randint(0, 7))
    defect = rng.choice(h.CASE_INVARIANT_DEFECTS)
    after = _safe(rng, h, 24)
    return prefix + before + defect + after + "/" + h.tok(rng)


def _tail_suffix(rng, h, host):
    prefix = "https://%s:%s/" % (host, PORT)
    return prefix + _safe(rng, h, 64 - len(prefix))


def _tail_clean(rng, h):
    host = _host(rng, h)
    outer = "https://%s:%s/%s/" % (host, PORT, h.tok(rng))
    return outer + _tail_suffix(rng, h, host)


def _tail_hidden_defect(rng, h):
    host = _host(rng, h)
    outer = "https://%s:%s/%s" % (host, PORT, h.tok(rng))
    defect = rng.choice(h.CASE_INVARIANT_DEFECTS)
    before_tail = _safe(rng, h, 4)
    return outer + defect + before_tail + "/" + _tail_suffix(rng, h, host)


def cases(rng, h):
    units = []
    for make in (_head_clean, _head_hidden_defect, _tail_clean, _tail_hidden_defect):
        for _ in range(REPS_PER_SHAPE):
            units.append(("value", "loc", make(rng, h)))
    return units, len(units)
