#!/usr/bin/env python3
"""Write receipts/tool-versions.txt: the same two runs against every pinned tool
snapshot, so the real-input result is shown to be version-stable rather than a
single lucky build."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r76/ExecAuditRealRun"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditRealRun")
PINNED = os.path.join(WAVE, "pinned")
RECEIPTS = os.path.join(WAVE, "receipts")
MANIFEST = os.path.join(WAVE, "real-manifest.json")
WORK = os.path.join(S, "work-tool")
TMP = os.path.join(S, "tmp")
ENV = dict(os.environ, TMPDIR=TMP, PYTHONDONTWRITEBYTECODE="1")


def main() -> int:
    rows = [
        "# the real-input run and the selftest against every pinned ExecAuditTool snapshot",
        "# (the live file was rewritten by its own seat while this receipt was produced)",
    ]
    for leaf in sorted(os.listdir(PINNED)):
        if not leaf.endswith(".py"):
            continue
        path = os.path.join(PINNED, leaf)
        blob = open(path, "rb").read()
        digest = hashlib.sha256(blob).hexdigest()
        selftest = subprocess.run(
            [sys.executable, "-B", path, "--selftest", "--work", WORK],
            env=ENV, capture_output=True, text=True,
        )
        real = subprocess.run(
            [sys.executable, "-B", path, "--manifest", MANIFEST, "--root", LANE, "--json", "--work", WORK],
            env=ENV, capture_output=True, text=True,
        )
        verdict = "unparseable"
        pages = findings = None
        try:
            payload = json.loads(real.stdout)
            pages = payload.get("pages")
            findings = len(payload.get("findings", []))
            verdict = "json"
        except json.JSONDecodeError:
            pass
        rows.append(f"[{leaf}]")
        rows.append(f"  sha256={digest} bytes={len(blob)}")
        rows.append(f"  selftest exit={selftest.returncode} :: {selftest.stdout.strip() or '(no stdout)'}")
        rows.append(
            f"  real-input exit={real.returncode} output={verdict} pages={pages} findings={findings}"
        )
        if real.returncode not in (0, 1, 2, 64):
            rows.append(f"  stderr={real.stderr.strip().splitlines()[-1] if real.stderr.strip() else ''}")
    live = os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py")
    with open(live, "rb") as fh:
        live_blob = fh.read()
    rows.append("[live file at receipt time]")
    rows.append(f"  sha256={hashlib.sha256(live_blob).hexdigest()} bytes={len(live_blob)}")
    with open(os.path.join(RECEIPTS, "tool-versions.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
