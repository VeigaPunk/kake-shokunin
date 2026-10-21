#!/usr/bin/env python3
"""Count C2 surfaces with a reproducible canonical-policy receipt of live-served HTML.

Usage: measure_c2.py --root LANE --revision COMMIT
Population: .ufo/waves/round-23/c2-population.json at the measured revision, accepted only
if its sha256 equals the frozen digest. For each surface, at the measured revision,
live/<id>/fetch.json must name the population url, a GET, fetchedAt >= 2026-10-21 and a
sha256 of the stored body. Then either
  * served (2xx text/html): live/<id>/page.html's sha256 equals fetch.sha256, and
    re-running that revision's scripts/canonical_audit.py on a fresh manifest
    (url = fetch.finalUrl, expectedCanonical = population) in a temporary directory
    reproduces live/<id>/audit.json's exit and result exactly; or
  * not served: audit.json is {"verdict":"not-served","status":fetch.status,...},
    no page.html is stored, and fetch.status is not a 2xx text/html response.
Exit 0 iff all surfaces pass; 1 otherwise; 2 when inputs cannot be read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

ROUND = ".ufo/waves/round-23"
POPULATION_SHA256 = "ac58c80fda73cae194fcc75bf56f62b19ea5443048ddf822fcee8d08e7c75d98"


def show(root: str, revision: str, path: str) -> bytes | None:
    done = subprocess.run(["git", "-C", root, "show", f"{revision}:{path}"], capture_output=True, check=False)
    return done.stdout if done.returncode == 0 else None


def served(fetch: dict) -> bool:
    status, ctype = fetch.get("status"), fetch.get("contentType") or ""
    return (isinstance(status, int) and 200 <= status < 300 and fetch.get("error") is None
            and not fetch.get("truncated") and ctype.split(";")[0].strip().lower() == "text/html")


def check(root: str, revision: str, validator: bytes, surface: dict) -> tuple[list[str], str | None]:
    prefix = f"{ROUND}/live/{surface['id']}"
    raw_fetch, raw_audit = show(root, revision, f"{prefix}/fetch.json"), show(root, revision, f"{prefix}/audit.json")
    if raw_fetch is None or raw_audit is None:
        return ["fetch.json or audit.json missing"], None
    try:
        fetch, receipt = json.loads(raw_fetch), json.loads(raw_audit)
    except json.JSONDecodeError as exc:
        return [f"receipt JSON invalid: {exc}"], None
    if not isinstance(fetch, dict) or not isinstance(receipt, dict):
        return ["fetch/audit must be JSON objects"], None
    problems = []
    if fetch.get("url") != surface["url"] or fetch.get("method") != "GET":
        problems.append("fetch url/method does not match population GET")
    if not isinstance(fetch.get("fetchedAt"), str) or fetch["fetchedAt"][:10] < "2026-10-21":
        problems.append("fetchedAt missing or before 2026-10-21")
    if type(fetch.get("status")) is not int or not 100 <= fetch["status"] <= 599 or fetch.get("error"):
        problems.append("fetch did not record a usable HTTP response")
    previous, chain = fetch.get("url"), fetch.get("redirects")
    if not isinstance(chain, list) or len(chain) > 5:
        problems.append("fetch redirect chain missing or too long")
    else:
        for hop in chain:
            if not isinstance(hop, dict) or hop.get("from") != previous or hop.get("status") not in {301, 302, 303, 307, 308}:
                problems.append("fetch redirect chain inconsistent")
                break
            previous = hop.get("to")
        if fetch.get("finalUrl") != previous:
            problems.append("fetch finalUrl differs from redirect chain")
    page = show(root, revision, f"{prefix}/page.html")
    if not served(fetch):
        if page is not None:
            problems.append("page.html stored for a non-served response")
        expected_receipt = {"verdict": "not-served", "status": fetch.get("status"), "exit": None, "error": None}
        if receipt != expected_receipt:
            problems.append("non-served surface lacks a matching not-served receipt")
        return problems, "not-served"
    if page is None or hashlib.sha256(page).hexdigest() != fetch.get("sha256"):
        return problems + ["page.html missing or digest differs from fetch.sha256"], None
    if len(page) != fetch.get("bytes"):
        problems.append("page.html length differs from fetch.bytes")
    with tempfile.TemporaryDirectory(prefix="kake-r23-c2-") as tmp:
        with open(os.path.join(tmp, "canonical_audit.py"), "wb") as stream:
            stream.write(validator)
        os.mkdir(os.path.join(tmp, "s"))
        with open(os.path.join(tmp, "s", "page.html"), "wb") as stream:
            stream.write(page)
        manifest = {"version": 1, "pages": [{"url": fetch.get("finalUrl"), "file": "page.html",
                                             "expectedCanonical": surface["expectedCanonical"]}]}
        with open(os.path.join(tmp, "s", "manifest.json"), "w", encoding="utf-8") as stream:
            json.dump(manifest, stream)
        try:
            done = subprocess.run([sys.executable, "-B", os.path.join(tmp, "canonical_audit.py"), "--manifest",
                                   os.path.join(tmp, "s", "manifest.json"), "--json"],
                                  capture_output=True, text=True, timeout=60, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return problems + [f"validator could not complete: {type(exc).__name__}"], None
    try:
        actual = {"exit": done.returncode, "result": json.loads(done.stdout)}
    except json.JSONDecodeError:
        return problems + ["validator did not emit JSON"], None
    if receipt != actual:
        problems.append(f"audit.json {receipt!r} != reproduced {actual!r}")
    return problems, actual["result"]["verdict"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args(argv)
    resolved = subprocess.run(["git", "-C", args.root, "rev-parse", "--verify", f"{args.revision}^{{commit}}"],
                              capture_output=True, text=True, check=False)
    population = show(args.root, args.revision, f"{ROUND}/c2-population.json")
    validator = show(args.root, args.revision, "scripts/canonical_audit.py")
    if (resolved.returncode != 0 or population is None or validator is None
            or hashlib.sha256(population).hexdigest() != POPULATION_SHA256):
        print(json.dumps({"error": "revision, frozen population or validator unreadable", "revision": args.revision}))
        return 2
    revision = resolved.stdout.strip()
    rows = []
    for surface in json.loads(population)["surfaces"]:
        problems, verdict = check(args.root, revision, validator, surface)
        rows.append({"id": surface["id"], "pass": not problems, "verdict": verdict, "problems": problems})
    accepted = sum(row["pass"] for row in rows)
    print(json.dumps({"revision": revision, "validatorSha256": hashlib.sha256(validator).hexdigest(),
                      "accepted": accepted, "total": len(rows), "surfaces": rows}, indent=1, sort_keys=True))
    return 0 if accepted == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
