#!/usr/bin/env python3
"""Round-48 C2 counter — does the citation lint resolve a token by existence?

Frozen predicate (the same sentence in the SCORECARD declaration, in this
file's PREDICATE constant and in every receipt's `predicate` field):

    met: dead_full_40 == 1 and dead_short == 1 and live_full_40 == 0
         and live_short == 0 and exclusions_clean == 1

The counter builds a scratch git repository with one commit, writes a fixture
population over {SCORECARD.md, LOG.md} that names five kinds of token, and runs
the lint at the given revision over that repository:

  dead_full_40   a 40-hex token that no object carries, in a commit context
                 -> must be reported as a violation
  dead_short     an 8-hex token that no object carries, in a commit context
                 -> must be reported as a violation
  live_full_40   the scratch repository's own 40-hex commit hash, in a commit
                 context -> must not be reported
  live_short     the first 7 characters of that hash -> must not be reported
  exclusions     six exclusion-class tokens (sha256 digest, ellipsis digest
                 prefix, beat pin, UUID fragment, pure digits, plain hex with
                 no commit context) -> none of them may be reported

Exit codes: 0 met, 1 not met, 2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PREDICATE = ("met: dead_full_40 == 1 and dead_short == 1 and live_full_40 == 0 "
             "and live_short == 0 and exclusions_clean == 1")
TOOL = "scripts/citation_lint.py"
DEAD_FULL_40 = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
DEAD_SHORT = "e5455253"


def usage_error(message: str) -> int:
    print(f"c48_lint_count: {message}", file=sys.stderr)
    return 64


def git(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def build_repo(root: str) -> str:
    repo = os.path.join(root, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "c48@example.invalid")
    git(repo, "config", "user.name", "c48")
    with open(os.path.join(repo, "f.txt"), "w", encoding="utf-8") as fh:
        fh.write("base\n")
    git(repo, "add", "f.txt")
    git(repo, "commit", "-q", "-m", "base")
    return repo


def tool_bytes(root: str, revision: str, tool_file: str | None) -> bytes:
    if tool_file:
        with open(tool_file, "rb") as fh:
            return fh.read()
    proc = subprocess.run(["git", "-C", root, "show", f"{revision}:{TOOL}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise FileNotFoundError(TOOL)
    return proc.stdout


def run_tool(repo: str, tool_path: str) -> dict:
    proc = subprocess.run([sys.executable, "-B", tool_path, "--root", repo, "--json"],
                          capture_output=True)
    text = proc.stdout.decode("utf-8", "replace")
    payload = None
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            payload = json.loads(line)
            break
        except Exception:
            continue
    if payload is None:
        return {"error": "tool output is not JSON", "stdout": text[:400],
                "returncode": proc.returncode}
    return payload


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    values = {"root": None, "revision": None, "tool_file": None, "json": None}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--root", "--revision", "--tool-file", "--json"):
            index += 1
            if index >= len(argv):
                return usage_error(f"{arg} needs a value")
            key = {"--root": "root", "--revision": "revision",
                   "--tool-file": "tool_file", "--json": "json"}[arg]
            values[key] = argv[index]
        elif arg.startswith("--"):
            return usage_error(f"unknown argument: {arg}")
        else:
            return usage_error(f"unknown argument: {arg}")
        index += 1
    if not values["root"] or not values["revision"]:
        return usage_error("--root and --revision are required")
    root, revision = values["root"], values["revision"]
    try:
        tool = tool_bytes(root, revision, values["tool_file"])
    except FileNotFoundError:
        print(json.dumps({"error": f"cannot evaluate: {TOOL} is absent at {revision}"}))
        return 2
    tmp = tempfile.mkdtemp(prefix="kake-r48-c48-lint-")
    try:
        repo = build_repo(tmp)
        live = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        live_short = live[:7]
        tool_path = os.path.join(tmp, "citation_lint.py")
        with open(tool_path, "wb") as fh:
            fh.write(tool)
        lines = [
            f"measured at commit `{DEAD_FULL_40}` which resolves",
            f"landed `{DEAD_SHORT}` on the lane branch",
            f"the tip is commit `{live}` today",
            f"the short form `{live_short}` names the same commit",
            "counter sha256 `5cedaa3b` pins the revision bytes",
            "strict check `5111264f…46ad` sets the revision",
            "beat `9c28d29` landed on the scribe remote",
            "chat `1a0acf59-4122-87ce` bound to the slot",
            "seed `43258815593301` used for the timing run",
            "a plain hex token cafe012 sits in prose",
        ]
        with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        with open(os.path.join(repo, "LOG.md"), "w", encoding="utf-8") as fh:
            fh.write("round log\n")
        payload = run_tool(repo, tool_path)
        if "error" in payload:
            print(json.dumps({"error": payload["error"], "detail": payload.get("stdout", "")[:400]}))
            return 2
        flagged = {v["token"] for v in payload.get("violations", [])}
        exclusions = {"5cedaa3b", "5111264f", "9c28d29", "1a0acf59", "43258815593301", "cafe012"}
        result = {
            "schema": "kake-r48-c2-counter-v1",
            "revision": revision,
            "predicate": PREDICATE,
            "toolSha256": __import__("hashlib").sha256(tool).hexdigest(),
            "dead_full_40": 1 if DEAD_FULL_40 in flagged else 0,
            "dead_short": 1 if DEAD_SHORT in flagged else 0,
            "live_full_40": 1 if live in flagged else 0,
            "live_short": 1 if live_short in flagged else 0,
            "exclusions_clean": 0 if (exclusions & flagged) else 1,
            "flagged": sorted(flagged),
            "liveCommit": live,
        }
        result["met"] = bool(result["dead_full_40"] == 1 and result["dead_short"] == 1
                             and result["live_full_40"] == 0 and result["live_short"] == 0
                             and result["exclusions_clean"] == 1)
        text = json.dumps(result, indent=2, ensure_ascii=False)
        if values["json"] and values["json"] != "-":
            with open(values["json"], "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        else:
            print(text)
        return 0 if result["met"] else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
