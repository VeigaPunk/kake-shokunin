#!/usr/bin/env python3
"""Probe one canonical_audit.py against the ways body markup can feed the canonical decision.

Usage: relaxation_probe.py --validator PATH
Every page has a relative head canonical `a.html` that matches expectedCanonical when
resolved against the document URL; each attack adds body markup a browser could turn
into an effective base (or other head-affecting token). Expectation, fixed from
w1/FalsifyForeignContent and w1/ScribeKnowledgeDelta before the fix: never `clean`.
Controls must stay clean. Exit 0 iff every expectation holds. Temp files only.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

DOC = "https://example.test/cases/page.html"
EXPECTED = "https://example.test/cases/a.html"
HEAD = "<head><link rel=canonical href=a.html></head>"
WRONG = "<base href='https://wrong.test/root/'>"
ATTACKS = {
    "body_base": f"{HEAD}<body>{WRONG}</body>",
    "body_base_selfclose": f"{HEAD}<body><base href='https://wrong.test/root/'/></body>",
    "foreignobject_base": f"{HEAD}<body><svg><foreignObject>{WRONG}</foreignObject></svg></body>",
    "svg_head_breakout_base": f"{HEAD}<body><svg><head></head>{WRONG}</svg></body>",
    "svg_mismatched_end_base": f"{HEAD}<body><svg><math></svg>{WRONG}</math></body>",
    "svg_title_hidden_base": f"{HEAD}<body><svg><title>{WRONG}</title></svg></body>",
    "svg_style_hidden_base": f"{HEAD}<body><svg><style>{WRONG}</style></svg></body>",
    "svg_script_hidden_base": f"{HEAD}<body><svg><script>{WRONG}</script></svg></body>",
    "math_annotation_base": f"{HEAD}<body><math><annotation-xml encoding='text/html'>{WRONG}</annotation-xml></math></body>",
}
CONTROLS = {
    "control_body_svg": f"{HEAD}<body><svg viewBox='0 0 1 1'><title>Icon</title><path d='M0 0'/></svg></body>",
    "control_void_selfclose": f"{HEAD}<body><input type=checkbox /><img src=a.png /><br/></body>",
}


def run(validator: str, root: str, name: str, html: str) -> dict:
    directory = os.path.join(root, name)
    os.mkdir(directory)
    with open(os.path.join(directory, "page.html"), "w", encoding="utf-8") as stream:
        stream.write(html)
    manifest = os.path.join(directory, "manifest.json")
    with open(manifest, "w", encoding="utf-8") as stream:
        json.dump({"version": 1, "pages": [{"url": DOC, "file": "page.html", "expectedCanonical": EXPECTED}]}, stream)
    done = subprocess.run([sys.executable, "-B", validator, "--manifest", manifest, "--json"],
                          capture_output=True, text=True, check=False)
    return {"exit": done.returncode, "verdict": json.loads(done.stdout)["verdict"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator", required=True)
    validator = os.path.abspath(parser.parse_args().validator)
    rows = []
    with tempfile.TemporaryDirectory(prefix="kake-r23-relaxation-") as root:
        for name, html in ATTACKS.items():
            actual = run(validator, root, name, html)
            rows.append({"case": name, "expect": "not clean", **actual, "ok": actual["verdict"] != "clean"})
        for name, html in CONTROLS.items():
            actual = run(validator, root, name, html)
            rows.append({"case": name, "expect": "clean", **actual, "ok": actual["verdict"] == "clean"})
    ok = all(row["ok"] for row in rows)
    print(json.dumps({"validator": validator, "passed": ok, "met": sum(r["ok"] for r in rows), "total": len(rows),
                      "cases": rows}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
