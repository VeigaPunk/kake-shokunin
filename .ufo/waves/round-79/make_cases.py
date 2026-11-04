#!/usr/bin/env python3
"""Round-79 frozen case generator — writes cases/cNN/manifest.json and expect/expect.json.

Deterministic and idempotent: the committed outputs are the frozen case set. Values follow
contract.md §"C2 tool interface" exactly; the oracle lives outside the case directories so
the tool under test receives payloads only.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = HERE / "cases"
EXPECT = HERE / "expect" / "expect.json"


def check(cid: str, *values: str, name: str = "X-Robots-Tag", url: str | None = None) -> dict:
    return {"id": cid, "url": url or f"https://example.test/{cid}",
            "headers": [{"name": name, "value": v} for v in values]}


def one(cid: str, directive: str) -> dict:
    return check(cid, directive)


CASES_DEF: dict[str, dict] = {
    "c01": one("c01", "noindex"),
    "c02": one("c02", "noindex, nofollow"),
    "c03": one("c03", "none"),
    "c04": one("c04", "all"),
    "c05": one("c05", "googlebot: noindex"),
    "c06": one("c06", "noindex, googlebot: nofollow"),
    "c07": check("c07", "noindex", "nosnippet"),
    "c08": one("c08", "max-snippet:50, nosnippet"),
    "c09": one("c09", "index, noindex"),
    "c10": one("c10", "follow, nofollow"),
    "c11": one("c11", "noindex; nofollow"),
    "c12": one("c12", "noindex,,nofollow"),
    "c13": one("c13", "max-snippet:abc"),
    "c14": one("c14", "max-image-preview:huge"),
    "c15": one("c15", "max-video-preview:-1"),
    "c16": one("c16", "unavailable_after:2025-12-31T23:59:59Z"),
    "c17": one("c17", "unavailable_after:tomorrow"),
    "c18": one("c18", "googlebot:"),
    "c19": one("c19", "NoIndex"),
    "c20": one("c20", "indexifembedded"),
    "c21": one("c21", "max-snippet:50, max-snippet:100"),
    "c22": {"id": "c22", "url": "https://example.test/c22",
            "headers": [{"name": "X-Robots-Tag", "value": "noindex"}]},  # duplicate id, see below
    "c23": {"id": "c23", "url": "https://example.test/c23",
            "headers": "noindex"},
    "c24": None,  # invalid JSON body
    "c25": {"id": "c25", "url": "https://example.test/c25",
            "headers": [{"name": "X-Robots-Tag", "value": "noindex"}]},  # wrong schema, see below
    "c26": one("c26", "noarchive, notranslate, noimageindex"),
    "c27": one("c27", "max-image-preview:Large"),
    "c28": one("c28", "googlebot: noindex, nofollow"),
    "c29": one("c29", "googlebot: noindex, bingbot: noindex"),
    "c30": check("c30", "noindex", name="X-ROBOTS-TAG"),
    "c31": check("c31", "DENY", name="X-Frame-Options"),
}


def manifest(cid: str) -> dict | str:
    if cid == "c22":
        body = {"id": "c22", "url": "https://example.test/c22",
                "headers": [{"name": "X-Robots-Tag", "value": "noindex"}]}
        return {"schema": "x-robots-tag-manifest/v1", "checks": [body, dict(body)]}
    if cid == "c24":
        return "{not json"
    if cid == "c25":
        return {"schema": "x-robots-tag-manifest/v2", "checks": [CASES_DEF["c25"]]}
    return {"schema": "x-robots-tag-manifest/v1", "checks": [CASES_DEF[cid]]}


def c(cid: str, directives=None, effective=None, bots=None, findings=None) -> dict:
    return {"exit": 0 if not findings else 1, "findings": sorted(findings or []),
            "checks": {cid: {"directives": sorted(directives or []),
                             "effective": sorted(effective or []),
                             "bots": {k: sorted(v) for k, v in sorted((bots or {}).items())}}}}


EXPECTATIONS: dict[str, dict] = {
    "c01": c("c01", ["noindex"], ["noindex"]),
    "c02": c("c02", ["nofollow", "noindex"], ["nofollow", "noindex"]),
    "c03": c("c03", ["nofollow", "noindex"], ["nofollow", "noindex"]),
    "c04": c("c04"),
    "c05": c("c05", bots={"googlebot": ["noindex"]}),
    "c06": c("c06", ["noindex"], ["noindex"], bots={"googlebot": ["nofollow"]}),
    "c07": c("c07", ["noindex", "nosnippet"], ["noindex", "nosnippet"]),
    "c08": c("c08", ["max-snippet:50", "nosnippet"], ["nosnippet"]),
    "c09": c("c09", ["index", "noindex"], ["noindex"], findings=["xrt_mutually_exclusive"]),
    "c10": c("c10", ["follow", "nofollow"], ["nofollow"], findings=["xrt_mutually_exclusive"]),
    "c11": c("c11", findings=["xrt_unknown_directive"]),
    "c12": c("c12", ["nofollow", "noindex"], ["nofollow", "noindex"], findings=["xrt_empty_rule"]),
    "c13": c("c13", findings=["xrt_invalid_value"]),
    "c14": c("c14", findings=["xrt_invalid_value"]),
    "c15": c("c15", ["max-video-preview:-1"], ["max-video-preview:-1"]),
    "c16": c("c16", ["unavailable_after:2025-12-31T23:59:59Z"],
             ["unavailable_after:2025-12-31T23:59:59Z"]),
    "c17": c("c17", findings=["xrt_invalid_value"]),
    "c18": c("c18", findings=["xrt_bot_scope_empty"]),
    "c19": c("c19", ["noindex"], ["noindex"]),
    "c20": c("c20", ["indexifembedded"], ["indexifembedded"],
             findings=["xrt_indexifembedded_without_noindex"]),
    "c21": c("c21", ["max-snippet:100", "max-snippet:50"], ["max-snippet:50"],
             findings=["xrt_duplicate_directive"]),
    "c22": {"exit": 2, "error": "xrt_input_duplicate_id"},
    "c23": {"exit": 2, "error": "xrt_input_check_shape"},
    "c24": {"exit": 2, "error": "xrt_input_bad_json"},
    "c25": {"exit": 2, "error": "xrt_input_schema"},
    "c26": c("c26", ["noarchive", "noimageindex", "notranslate"],
             ["noarchive", "noimageindex", "notranslate"]),
    "c27": c("c27", ["max-image-preview:large"], ["max-image-preview:large"]),
    "c28": c("c28", bots={"googlebot": ["nofollow", "noindex"]}),
    "c29": c("c29", bots={"bingbot": ["noindex"], "googlebot": ["noindex"]}),
    "c30": c("c30", ["noindex"], ["noindex"]),
    "c31": c("c31"),
}


def main() -> int:
    CASES.mkdir(parents=True, exist_ok=True)
    for cid in sorted(CASES_DEF):
        d = CASES / cid
        d.mkdir(parents=True, exist_ok=True)
        body = manifest(cid)
        text = body if isinstance(body, str) else json.dumps(body, indent=1) + "\n"
        (d / "manifest.json").write_text(text, encoding="utf-8")
    EXPECT.parent.mkdir(parents=True, exist_ok=True)
    EXPECT.write_text(json.dumps({"schema": "xrt-expect/v1", "cases": EXPECTATIONS},
                                 indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"cases={len(CASES_DEF)} expect={EXPECT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
