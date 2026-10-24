#!/usr/bin/env python3
"""Compare two validator revisions on the committed live snapshots (served pages only).

Usage: evaluability.py --root LANE --before COMMIT --after COMMIT
Both validators are materialized with `git show <commit>:scripts/canonical_audit.py` into a
temp dir and run on every live/<id>/page.html with the frozen expectedCanonical and the
fetch finalUrl. Reports, per surface, verdict and findings for each revision and counts of
"evaluated" verdicts (clean or failed-policy, i.e. not could-not-evaluate).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

ROUND = ".ufo/waves/round-23"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()
    root = os.path.abspath(args.root)
    population = json.load(open(os.path.join(root, ROUND, "c2-population.json")))["surfaces"]
    rows, counts = [], {"before": 0, "after": 0}
    with tempfile.TemporaryDirectory(prefix="kake-r23-eval-") as tmp:
        validators = {}
        for label, commit in (("before", args.before), ("after", args.after)):
            path = os.path.join(tmp, f"{label}.py")
            with open(path, "wb") as stream:
                stream.write(subprocess.run(["git", "-C", root, "show", f"{commit}:scripts/canonical_audit.py"],
                                            capture_output=True, check=True).stdout)
            validators[label] = path
        for surface in population:
            directory = os.path.join(root, ROUND, "live", surface["id"])
            page = os.path.join(directory, "page.html")
            if not os.path.isfile(page):
                continue
            fetch = json.load(open(os.path.join(directory, "fetch.json")))
            case = os.path.join(tmp, surface["id"])
            os.mkdir(case)
            with open(page, "rb") as source, open(os.path.join(case, "page.html"), "wb") as target:
                target.write(source.read())
            manifest = os.path.join(case, "manifest.json")
            with open(manifest, "w", encoding="utf-8") as stream:
                json.dump({"version": 1, "pages": [{"url": fetch["finalUrl"], "file": "page.html",
                                                    "expectedCanonical": surface["expectedCanonical"]}]}, stream)
            row = {"id": surface["id"]}
            for label, validator in validators.items():
                done = subprocess.run([sys.executable, "-B", validator, "--manifest", manifest, "--json"],
                                      capture_output=True, text=True, check=False)
                result = json.loads(done.stdout)
                row[label] = {"exit": done.returncode, "verdict": result["verdict"],
                              "findings": [f["id"] for f in result["findings"]]}
                counts[label] += result["verdict"] != "could-not-evaluate"
            rows.append(row)
    print(json.dumps({"before": args.before, "after": args.after, "served": len(rows),
                      "evaluated": counts, "surfaces": rows}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
