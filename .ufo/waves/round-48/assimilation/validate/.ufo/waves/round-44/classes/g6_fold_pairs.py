"""G6: fold-memo witnesses for the four casememo controls.

Shapes (derived from the frozen control sources; verified by probes):

- v3/v4 (`_uri_ok` verdict memo keyed on value.lower(), v4 gated at <=64 cps):
  an IP-literal pair whose ZONE ID carries the case swap. The round-41 scanner's
  IP-literal table is ASCII-only, so the folded member is rejected
  (`loc_not_absolute`) as written, while the memo answers it from the ASCII
  member's stored clean verdict (U+212A lower()s to 'k'). Both members are kept
  well under 64 code points so the v4 gate wraps both lookup and store.
  The ASCII member is generated first so its verdict is the one stored.

- v7/v8 (`_parse_url` tuple memo, consulted only for non-ASCII values, keyed on
  lower() resp. casefold()): the swap sits in the FIRST path segment. The shared
  sitemapUrl names member 1's first-segment directory (case-sensitive), so the
  round-41 tool flags member 2 loc_out_of_scope; the memo returns member 1's
  parse (ASCII path) and the control judges it in-scope. KELVIN (U+212A) pairs
  fire both v7 and v8; long-s (U+017F) pairs fire v8 only (lower() leaves U+017F
  unchanged, casefold() maps it to 's').

Deterministic from rng only; standard library only; no I/O, no environment
reads, no imports of control tools.
"""

_KELVIN = "\u212a"
_LONG_S = "\u017f"


def _ip_zone_pair(rng, h):
    """(ascii, folded) pair differing only by KELVIN in the IP-literal zone id."""
    scheme = h.rcase(rng, rng.choice(("http", "https")))
    tail = "/".join(h.tok(rng, 4, 8) for _ in range(rng.randint(1, 2)))
    ascii_v = "%s://[::1%%25k]/%s" % (scheme, tail)
    folded = "%s://[::1%%25%s]/%s" % (scheme, _KELVIN, tail)
    return ascii_v, folded


def _first_segment_pair(rng, h, marker, ascii_letter):
    """(ascii, folded) pair differing only by `marker` for `ascii_letter` in segment 1."""
    scheme = h.rcase(rng, rng.choice(("http", "https")))
    host = h.fill(rng, "host", 3, 8) + "." + rng.choice(h.TLDS)
    head = h.tok(rng, 4, 6)
    rest = "/".join(h.tok(rng, 4, 8) for _ in range(rng.randint(1, 2)))
    ascii_seg = head + ascii_letter
    folded_seg = head + marker
    ascii_v = "%s://%s/%s/%s" % (scheme, host, ascii_seg, rest)
    folded = "%s://%s/%s/%s" % (scheme, host, folded_seg, rest)
    return ascii_v, folded


def cases(rng, h):
    units = []
    for _ in range(60):
        units.append(("foldpair",) + _ip_zone_pair(rng, h))
    for _ in range(60):
        units.append(("foldpair",) + _first_segment_pair(rng, h, _KELVIN, "k"))
    for _ in range(60):
        units.append(("foldpair",) + _first_segment_pair(rng, h, _LONG_S, "s"))
    return units, 2 * len(units)
