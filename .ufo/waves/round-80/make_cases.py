#!/usr/bin/env python3
"""Round-80 case-set authoring record (frozen with `contract.md`).

Each row is the field value plus the `directives` and `findings` the frozen grammar (round-79
contract + round-80 amendment 1) entails. The expectations are hand-derived from the grammar text
and the two cited sources — never from a run of the tool. Re-running this script reproduces
`cases/cNN/manifest.json` and `expect/expect.json` byte for byte.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# (case id, header value, expected global directives, expected findings)
CASES = [
    ("c32", "unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT",
     ["unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT"], []),
    ("c33", "unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT",
     ["unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT"], []),
    ("c34", "unavailable_after: Sun Nov  6 08:49:37 1994",
     ["unavailable_after:Sun Nov  6 08:49:37 1994"], []),
    ("c35", "unavailable_after:2025-12-31",
     ["unavailable_after:2025-12-31"], []),
    ("c36", "unavailable_after:2025-12-31T23:59:59-03:00",
     ["unavailable_after:2025-12-31T23:59:59-03:00"], []),
    ("c37", "unavailable_after: Wed, 03 Dec 2025 13:09:53 PST",
     [], ["xrt_invalid_value"]),
    ("c38", "noindex, unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, noarchive",
     sorted(["noindex", "unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT", "noarchive"]), []),
    ("c39", "unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, "
            "unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT",
     sorted(["unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT",
             "unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT"]),
     ["xrt_duplicate_directive"]),
    ("c40", "googlebot: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT",
     [], []),
    ("c41", "unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, frobnicate",
     ["unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT"], ["xrt_unknown_directive"]),
    ("c42", "max-snippet: 20, unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT",
     sorted(["max-snippet:20", "unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT"]), []),
    ("c43", "unavailable_after: Sun Nov 16 08:49:37 1994, noindex",
     sorted(["noindex", "unavailable_after:Sun Nov 16 08:49:37 1994"]), []),
]

# Per-bot scopes (only the cases whose value carries a bot prefix).
BOTS = {"c40": {"googlebot": ["unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT"]}}


def effective_of(tokens: list[str]) -> list[str]:
    """Round-79 contract §effective: positives removed; nosnippet suppresses the max caps."""
    kept = [t for t in tokens if t not in ("all", "index", "follow")]
    if "nosnippet" in kept:
        kept = [t for t in kept if not (t.startswith("max-snippet:")
                                        or t.startswith("max-video-preview:"))]
    plain: set[str] = set()
    caps: dict[str, int] = {}
    for token in kept:
        if token.startswith("max-snippet:") or token.startswith("max-video-preview:"):
            name, _, value = token.partition(":")
            caps[name] = min(caps[name], int(value)) if name in caps else int(value)
        else:
            plain.add(token)
    return sorted(plain | {f"{name}:{value}" for name, value in caps.items()})


def main() -> int:
    expect = {"schema": "xrt-expect/v1", "cases": {}}
    for cid, value, directives, findings in CASES:
        directory = HERE / "cases" / cid
        directory.mkdir(parents=True, exist_ok=True)
        doc = {"schema": "x-robots-tag-manifest/v1",
               "checks": [{"id": cid, "url": f"https://example.test/{cid}",
                           "headers": [{"name": "X-Robots-Tag", "value": value}]}]}
        (directory / "manifest.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        expect["cases"][cid] = {
            "exit": 1 if findings else 0,
            "findings": findings,
            "checks": {cid: {"directives": directives,
                             "effective": effective_of(directives),
                             "bots": BOTS.get(cid, {})}},
        }
    (HERE / "expect").mkdir(parents=True, exist_ok=True)
    (HERE / "expect" / "expect.json").write_text(
        json.dumps(expect, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"cases={len(expect['cases'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
