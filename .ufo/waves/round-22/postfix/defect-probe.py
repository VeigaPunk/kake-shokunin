#!/usr/bin/env python3
"""Run the wave-2 defect reproducers against one canonical_audit.py.

Usage: defect-probe.py --validator PATH. Fixtures live in a fresh temporary
directory; nothing is written elsewhere and no network is used. Each probe has
an expectation fixed from the wave-2 report before any fix was run; exit 0 only
if every probe meets it.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

DOC = "https://example.test/project/a.html"


def page(directory, html, name="page.html"):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, name), "w", encoding="utf-8") as stream:
        stream.write(html)


def manifest(directory, expected=DOC, name="manifest.json"):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as stream:
        json.dump({"version": 1, "pages": [{"url": DOC, "file": "page.html", "expectedCanonical": expected}]}, stream)
    return path


def run(validator, argv):
    done = subprocess.run([sys.executable, "-B", validator, *argv], capture_output=True, text=True, timeout=30)
    try:
        payload = json.loads(done.stdout)
    except json.JSONDecodeError:
        payload = None
    return done.returncode, payload


def ids(payload):
    return [f["id"] for f in payload["findings"]] if isinstance(payload, dict) else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator", required=True)
    validator = os.path.abspath(parser.parse_args().validator)
    clean_html = f"<head><link rel=canonical href='{DOC}'></head>"
    records = []
    with tempfile.TemporaryDirectory(prefix="kake-r22-defect-probe-") as root:
        def probe(name, source, argv, expected_exit, expected_payload_check, check_text):
            code, payload = run(validator, argv)
            ok = code == expected_exit and expected_payload_check(payload)
            records.append({"probe": name, "source": source, "expected": f"exit {expected_exit}; {check_text}",
                            "actualExit": code, "actualStdout": payload, "ok": ok})

        d = os.path.join(root, "empty_authority")
        page(d, "<head><link rel=canonical href='///project/a.html'></head>")
        probe("network_path_empty_authority", "w2/Attack05.md", ["--manifest", manifest(d)], 1,
              lambda p: ids(p) == ["canonical_url_invalid"], "canonical_url_invalid")

        d = os.path.join(root, "base_empty_authority")
        page(d, "<head><base href='///project/'><link rel=canonical href=a.html></head>")
        probe("base_empty_authority", "w2/Attack05.md (propagates through base)", ["--manifest", manifest(d)], 1,
              lambda p: ids(p) == ["base_url_invalid"], "base_url_invalid")

        bad = os.path.join(root, "mismatch")
        page(bad, "<head><link rel=canonical href='https://example.test/wrong.html'></head>")
        good = os.path.join(root, "clean")
        page(good, clean_html)
        probe("repeated_manifest", "w2/BoundaryCLIErrors.md P2b",
              ["--manifest", manifest(bad), "--manifest", manifest(good)], 64,
              lambda p: p == {"verdict": "could-not-evaluate", "pagesChecked": 0, "findings": []},
              "usage could-not-evaluate JSON, not the last manifest's clean verdict")

        probe("usage_error_json", "w2/BoundaryCLIErrors.md P2a", ["--manifest", manifest(good), "--bogus"], 64,
              lambda p: p == {"verdict": "could-not-evaluate", "pagesChecked": 0, "findings": []},
              "stdout is the usage could-not-evaluate JSON object")

        d = os.path.join(root, "manifest_symlink")
        page(d, clean_html)
        manifest(d, name="target.json")
        os.symlink("target.json", os.path.join(d, "manifest.json"))
        probe("manifest_symlink", "w2/BoundarySymlinks.md residual", ["--manifest", os.path.join(d, "manifest.json")], 2,
              lambda p: ids(p) == ["input_invalid"], "input_invalid")

        d = os.path.join(root, "prefix", "real", "sub")
        page(d, clean_html)
        manifest(d)
        os.symlink("real", os.path.join(root, "prefix", "alias"))
        probe("caller_prefix_control", "w2/BoundarySymlinks.md P2 (scoped: caller-trusted prefix)",
              ["--manifest", os.path.join(root, "prefix", "alias", "sub", "manifest.json")], 0,
              lambda p: ids(p) == [], "clean (documented caller-chosen location)")

        probe("clean_control", "positive control", ["--manifest", os.path.join(good, "manifest.json")], 0,
              lambda p: ids(p) == [], "clean")

        dv = os.path.join(root, "dotdot")
        page(os.path.join(dv, "deep", "real"), "<head></head>")
        page(os.path.join(dv, "deep"), "<head><link rel=canonical href='https://example.test/wrong.html'></head>")
        manifest(os.path.join(dv, "deep"))
        page(dv, clean_html)
        manifest(dv)
        os.symlink(os.path.join("deep", "real"), os.path.join(dv, "alias"))
        probe("dotdot_after_symlink", "residual/CritScope.md P2 (kernel resolves alias/.. to deep/)",
              ["--manifest", os.path.join(dv, "alias", "..", "manifest.json")], 1,
              lambda p: ids(p) == ["canonical_mismatch"],
              "canonical_mismatch from the kernel-resolved deep/ manifest+page, not lexical dotdot/")
    ok = all(r["ok"] for r in records)
    print(json.dumps({"validator": validator, "passed": ok, "met": sum(r["ok"] for r in records),
                      "total": len(records), "probes": records}, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
